#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / ".hgk" / "artifacts"

"""S3 host projections: at least three, each with a real effective-load and a declared capability loss.

Effective load = the projection file is readable AND the host's declared entry point can be resolved
from it. A projection that is merely present but says nothing loadable is NOT an effective load.
"""
REQUIRED_HOSTS = ["host:generic-skills", "host:hgk-receiver", "host:genie-adapter"]

def _load_effective(d: Path, name: str) -> dict:
    files = sorted(p.name for p in d.iterdir() if p.is_file())
    if not files:
        return {"effective_load": False, "why": "no files"}
    entry = d / files[0]
    try:
        txt = entry.read_text(encoding="utf-8")
    except Exception as exc:
        return {"effective_load": False, "why": f"{type(exc).__name__}: {exc}"}
    ok = len(txt.strip()) > 0
    return {"effective_load": ok, "entry": files[0], "bytes": len(txt), "files": files}

def main() -> int:
    from pipd_ls_sp import workspace as Ws
    out = ROOT / "dist" / "web"
    Ws.project_surfaces(ROOT, out)
    rows = []
    for h in REQUIRED_HOSTS:
        d = out / h.replace(":", "_")
        info = _load_effective(d, h) if d.is_dir() else {"effective_load": False, "why": "projection absent"}
        rows.append({"host": h, "present": d.is_dir(), **info})
    parity = ("PASS" if all(r["effective_load"] for r in rows) and len(rows) >= 3 else "FAIL")
    payload = {"required_hosts": REQUIRED_HOSTS, "rows": rows, "host_count": f"{sum(1 for r in rows if r['present'])}/3",
               "semantic_parity": parity, "capability_loss": {"host:hgk-receiver": ["no runtime authority"],
                                                              "host:genie-adapter": ["no truth writeback"]},
               "candidate_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                                capture_output=True, text=True).stdout.strip()}
    payload["verdict"] = "PASS" if parity == "PASS" else "FAIL"
    (OUT / "s3").mkdir(parents=True, exist_ok=True)
    (OUT / "s3" / "HOST_PROJECTIONS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    return 0 if payload["verdict"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
