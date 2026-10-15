"""Served-byte readback of the v0.1.1-preview.4 release, independent of the round's own files.

Downloads every published asset from its public URL with no credential, recomputes sha256, checks it
against the published SHA256SUMS, and inspects the plugin ZIP from the DOWNLOADED bytes.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TAG = "v0.1.1-preview.4"
BASE = f"https://github.com/shw097-team/PIPD-LS-SP/releases/download/{TAG}/"
OUT = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/03_release")
OUT.mkdir(parents=True, exist_ok=True)
API = "https://api.github.com/repos/shw097-team/PIPD-LS-SP/releases/tags/" + TAG


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "hgk-readback"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


meta = json.loads(get(API).decode())
assets = {a["name"]: {"size": a["size"], "api_digest": a.get("digest")} for a in meta["assets"]}
sums_bytes = get(BASE + "SHA256SUMS")
sums = {}
for line in sums_bytes.decode().splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line)
    if m:
        sums[m.group(2).strip()] = m.group(1).lower()

report = {
    "schema": "R5S-ASSET-READBACK/1",
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "release_tag": TAG,
    "release_url": f"https://github.com/shw097-team/PIPD-LS-SP/releases/tag/{TAG}",
    "sha256sums_asset": {"bytes": len(sums_bytes), "has_crlf": b"\r\n" in sums_bytes, "entries": len(sums)},
    "assets": [],
}
zipped = None
for name, info in sorted(assets.items()):
    raw = get(BASE + name)
    digest = hashlib.sha256(raw).hexdigest()
    api_digest = (info.get("api_digest") or "").replace("sha256:", "")
    entry = {
        "name": name,
        "downloaded_bytes": len(raw),
        "api_reported_bytes": info["size"],
        "recomputed_sha256": digest,
        "api_reported_digest": api_digest or None,
        "digest_matches_api": (api_digest == digest) if api_digest else None,
        "sha256sums_entry": sums.get(name),
        "matches_sha256sums": (sums.get(name) == digest) if sums.get(name) else None,
    }
    report["assets"].append(entry)
    if name.endswith(".zip") and "public-skills" in name:
        zipped = raw

if zipped:
    zf = zipfile.ZipFile(io.BytesIO(zipped))
    names = zf.namelist()
    roots = {n.split("/")[0] for n in names}
    root = next(iter(roots)) if len(roots) == 1 else None
    skills = sorted({p.split("/")[2] for p in names if root and p.startswith(f"{root}/skills/") and p.count("/") >= 3})
    bad = zf.testzip()
    report["plugin_zip_inspection_from_downloaded_bytes"] = {
        "sha256": hashlib.sha256(zipped).hexdigest(),
        "members": len(names),
        "top_level_roots": sorted(roots),
        "manifests": [n for n in names if n.endswith("plugin.json")],
        "skill_count": len(skills),
        "skills": skills,
        "skill_md_paths": [p for p in names if root and p.startswith(f"{root}/skills/") and p.endswith("/SKILL.md")],
        "exactly_eight_skills": len(skills) == 8,
        "has_mcp_or_hooks_or_apps": [n for n in names if re.search(r"(^|/)(mcp\.json|hooks/|\.app\.json)", n)],
        "path_escape_or_absolute": [n for n in names if n.startswith("/") or ".." in n.split("/") or "\\" in n],
        "crc_first_bad_member": bad,
        "all_crc_ok": bad is None,
    }
report["claim_ceiling"] = "served-byte readback of the published release only; it says nothing about host installation"
(OUT / "asset_readback_r5s.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=1, ensure_ascii=False)[:4000])
