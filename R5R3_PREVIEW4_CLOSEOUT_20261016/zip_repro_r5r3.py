"""Reconstruct the published v0.1.1-preview.4 plugin ZIP from its frozen source commit.

Recipe taken verbatim from the R6 ZIP_REPRODUCTION.json receipt:
  1) python tools/freeze_public_plugin_source.py --repo-root . --out <out>/ledger.json
  2) python tools/build_public_plugin.py --ledger <out>/ledger.json --source-commit <c> \
        --packaging-root packaging/public-plugin --out-dir <out>/<a|b> --generate-icons
Run twice and compare digests: two builds must agree, and build A must equal the
published asset digest 545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75.

A mismatch is a FINDING, not a failure to hide: report it and stop.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile

PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
SUBJECT = pathlib.Path("C:/Projects/wt-r5r3-preview4-build")
OUT = pathlib.Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout/raw/zip_repro")
FROZEN = "cc6c1930765160697e7e51d6e37735b9220a30db"
PUBLISHED = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return {"cmd": [str(c) for c in cmd], "rc": p.returncode, "stdout_tail": p.stdout[-800:],
            "stderr_tail": p.stderr[-800:]}


def digest(zip_path: pathlib.Path) -> dict:
    b = zip_path.read_bytes()
    z = zipfile.ZipFile(zip_path)
    names = z.namelist()
    return {"path": str(zip_path).replace("\\", "/"), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest(), "entries": len(names),
            "roots": sorted({n.split("/")[0] for n in names}),
            "skill_md": sorted(n for n in names if n.endswith("/SKILL.md")),
            "crc_ok": z.testzip() is None}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rec = {"schema": "R5R3/ZIP-REPRO/1", "frozen_source_commit": FROZEN,
           "published_asset_sha256": PUBLISHED, "subject": str(SUBJECT).replace("\\", "/"),
           "steps": [], "builds": {}}
    rec["steps"].append(run([PY, "tools/freeze_public_plugin_source.py", "--repo-root", ".",
                             "--out", str(OUT / "ledger.json")], SUBJECT))
    for tag in ("a", "b"):
        rec["steps"].append(run([PY, "tools/build_public_plugin.py", "--ledger", str(OUT / "ledger.json"),
                                 "--source-commit", FROZEN, "--packaging-root", "packaging/public-plugin",
                                 "--out-dir", str(OUT / tag), "--generate-icons"], SUBJECT))
        z = OUT / tag / "pipd-ls-sp-public-skills.zip"
        rec["builds"][tag] = digest(z) if z.is_file() else {"missing": str(z)}
    a, b = rec["builds"].get("a", {}), rec["builds"].get("b", {})
    rec["verdict"] = {
        "two_builds_identical": bool(a.get("sha256") and a.get("sha256") == b.get("sha256")),
        "reproduces_published_asset": a.get("sha256") == PUBLISHED,
        "published_sha256": PUBLISHED,
    }
    (OUT / "ZIP_REPRO_R5R3.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n",
                                             encoding="utf-8", newline="\n")
    print(json.dumps(rec["verdict"], ensure_ascii=False))
    print("builds:", {k: (v.get("sha256", "")[:16], v.get("bytes")) for k, v in rec["builds"].items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
