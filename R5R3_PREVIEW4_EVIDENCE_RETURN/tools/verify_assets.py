"""Served-asset + plugin-ZIP readback for v0.1.1-preview.4 (CK-10/CK-11/CK-12).

Downloads every release asset from the PUBLIC release, recomputes sha256 from the SERVED bytes,
reconciles against the release's own SHA256SUMS, and inspects the plugin ZIP statically.

Usage: verify_assets.py <out-dir>
Writes the downloaded bytes + one JSON report. Read-only w.r.t. the repo; network reads only.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = "shw097-team/PIPD-LS-SP"
TAG = "v0.1.1-preview.4"
API = f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}"
HDRS = {"Accept": "application/vnd.github+json", "User-Agent": "hgk-round-readback/1"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main() -> int:
    out_dir = Path(sys.argv[1]).resolve()
    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    report: dict = {"schema": "R5R3-20261016/served-asset-readback/1", "repo": REPO, "tag": TAG,
                    "claim_ceiling": "static readback of published bytes; not an acceptance"}

    rel = json.loads(fetch(API).decode("utf-8"))
    report["release"] = {"tag": rel["tag_name"], "target_commitish": rel["target_commitish"],
                         "published_at": rel["published_at"], "draft": rel["draft"],
                         "prerelease": rel["prerelease"], "id": rel["id"],
                         "html_url": rel["html_url"]}

    served: dict[str, dict] = {}
    for a in rel["assets"]:
        blob = fetch(f"https://api.github.com/repos/{REPO}/releases/assets/{a['id']}")
        # the API metadata endpoint above is rate-limit-friendly; the bytes come from the browser URL
        data = fetch(a["browser_download_url"])
        sha = hashlib.sha256(data).hexdigest()
        (out_dir / "assets" / a["name"]).write_bytes(data)
        served[a["name"]] = {"size": len(data), "sha256": sha,
                             "api_digest": a.get("digest"),
                             "api_size": a["size"],
                             "browser_url": a["browser_download_url"],
                             "blob_meta_ok": bool(blob)}
    report["assets"] = served
    report["asset_count"] = len(served)
    report["api_digest_matches_recomputed"] = {
        n: (served[n]["api_digest"] == f"sha256:{served[n]['sha256']}")
        for n in served if served[n]["api_digest"]}
    report["api_size_matches_served"] = {n: served[n]["size"] == served[n]["api_size"]
                                         for n in served}

    # --- SHA256SUMS reconciliation -------------------------------------------------------------
    sums_name = "SHA256SUMS"
    sums_report: dict = {"present": sums_name in served}
    if sums_name in served:
        text = (out_dir / "assets" / sums_name).read_text(encoding="utf-8", errors="replace")
        declared = {}
        for line in text.splitlines():
            parts = line.split()
            if len(parts) == 2:
                declared[parts[1].lstrip("*")] = parts[0]
        rows = {}
        for name, digest in declared.items():
            got = served.get(name, {}).get("sha256")
            rows[name] = {"declared": digest, "served": got, "match": got == digest}
        sums_report.update({"declared_entries": len(declared), "rows": rows,
                            "all_match": all(r["match"] for r in rows.values()) if rows else False,
                            "undeclared_assets": sorted(set(served) - set(declared) - {sums_name}),
                            "raw": text})
    report["sha256sums"] = sums_report

    # --- plugin ZIP static inspection ----------------------------------------------------------
    zip_name = "pipd-ls-sp-public-skills.zip"
    zrep: dict = {"present": zip_name in served}
    if zip_name in served:
        blob = (out_dir / "assets" / zip_name).read_bytes()
        zf = zipfile.ZipFile(io.BytesIO(blob))
        names = zf.namelist()
        roots = sorted({n.split("/")[0] for n in names if n})
        skills = sorted({n for n in names if n.count("/") == 3
                         and n.split("/")[1] == "skills" and n.endswith("SKILL.md")})
        skill_dirs = sorted({n.split("/")[2] for n in names
                             if n.count("/") >= 3 and n.split("/")[1] == "skills"})
        traversal = [n for n in names
                     if n.startswith("/") or n.startswith("\\") or ".." in n.replace("\\", "/").split("/")
                     or "\\" in n]
        manifests = [n for n in names if n.endswith("plugin.json") or n.endswith("mcp.json")
                     or n.endswith(".app.json")]
        forbidden = [n for n in names if any(k in n for k in (".hgk/", "hooks/", "mcp.json",
                                                              ".env", "secrets", "id_rsa"))]
        crc_bad = zf.testzip()
        per_member = {n: hashlib.sha256(zf.read(n)).hexdigest() for n in skills}
        zrep.update({
            "zip_sha256": hashlib.sha256(blob).hexdigest(),
            "entry_count": len(names),
            "top_level_roots": roots,
            "single_root": len(roots) == 1,
            "skill_md_count": len(skills),
            "skill_dirs": skill_dirs,
            "skill_dir_count": len(skill_dirs),
            "skill_member_sha256": per_member,
            "traversal_entries": traversal,
            "manifest_members": manifests,
            "forbidden_members": forbidden,
            "crc_testzip_result": crc_bad,
            "crc_ok": crc_bad is None,
            "backslashes_in_names": [n for n in names if "\\" in n],
        })
    report["plugin_zip"] = zrep

    # --- verdict (machine gate for this step) ---------------------------------------------------
    checks = {
        "asset_count_7": report["asset_count"] == 7,
        "api_digest_all_match": all(report["api_digest_matches_recomputed"].values()),
        "api_size_all_match": all(report["api_size_matches_served"].values()),
        "sha256sums_all_match": bool(sums_report.get("all_match")),
        "zip_single_root": bool(zrep.get("single_root")),
        "zip_8_skills": zrep.get("skill_dir_count") == 8 and zrep.get("skill_md_count") == 8,
        "zip_no_traversal": not zrep.get("traversal_entries"),
        "zip_crc_ok": bool(zrep.get("crc_ok")),
        "zip_no_forbidden_members": not zrep.get("forbidden_members"),
        "zip_has_manifest": any(n.endswith("plugin.json") for n in zrep.get("manifest_members") or []),
    }
    report["checks"] = checks
    report["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
