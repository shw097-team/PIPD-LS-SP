"""Correct the skill enumeration in the R5S readback: the skill directory name is one level deeper."""
from __future__ import annotations

import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

OUT = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/03_release")
URL = "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.4/pipd-ls-sp-public-skills.zip"
req = urllib.request.Request(URL, headers={"User-Agent": "hgk-readback"})
with urllib.request.urlopen(req, timeout=120) as r:
    raw = r.read()
digest = hashlib.sha256(raw).hexdigest()
zf = zipfile.ZipFile(io.BytesIO(raw))
names = zf.namelist()
root = sorted({n.split("/")[0] for n in names})
skill_dirs = sorted({n.split("/")[2] for n in names if n.count("/") >= 2 and n.split("/")[1] == "skills"})
skill_md = sorted(n for n in names if n.endswith("skills") or "/skills/" in n and n.endswith("SKILL.md"))

d = json.loads((OUT / "asset_readback_r5s.json").read_text(encoding="utf-8"))
d["plugin_zip_inspection_from_downloaded_bytes"].update({
    "members": len(names),
    "top_level_roots": root,
    "skill_directories": skill_dirs,
    "skill_count": len(skill_dirs),
    "skill_md_members": skill_md,
    "skill_md_count": len(skill_md),
    "per_skill_sha256": {n: hashlib.sha256(zf.read(n)).hexdigest() for n in skill_md},
})
d["plugin_zip_recheck"] = {"redownloaded_sha256": digest, "same_bytes_as_first_readback": digest == d["plugin_zip_inspection_from_downloaded_bytes"]["sha256"]}
(OUT / "asset_readback_r5s.json").write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"skill_count": len(skill_dirs), "skills": skill_dirs, "roots": root, "manifest": d["plugin_zip_inspection_from_downloaded_bytes"]["manifests"], "same_bytes": d["plugin_zip_recheck"]["same_bytes_as_first_readback"]}, indent=1, ensure_ascii=False))
