#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / ".hgk" / "artifacts"

"""S3 web pack: the EXACT 5-file set, present and non-empty, with a manifest that agrees."""
EXPECTED = ["index.html", "app.js", "styles.css", "manifest.webmanifest", "README.md"]

def main() -> int:
    from pipd_ls_sp import workspace as Ws
    out = ROOT / "dist" / "web"
    res = Ws.project_surfaces(ROOT, out)
    present = sorted(p.name for p in out.iterdir() if p.is_file())
    exact = sorted(EXPECTED) == present
    nonempty = all((out / f).stat().st_size > 0 for f in EXPECTED)
    man = json.loads((out / "manifest.webmanifest").read_text(encoding="utf-8"))
    payload = {"expected": sorted(EXPECTED), "present": present, "exact_set_match": exact,
               "all_non_empty": nonempty, "manifest_ok": man.get("name") == "PIPD-LS-SP",
               "note": "exact-set equality, not a superset check: an extra file is a projection leak",
               "candidate_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                                capture_output=True, text=True).stdout.strip()}
    payload["verdict"] = "PASS" if (exact and nonempty and payload["manifest_ok"]) else "FAIL"
    (OUT / "s3").mkdir(parents=True, exist_ok=True)
    (OUT / "s3" / "WEB_PACK.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    return 0 if payload["verdict"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
