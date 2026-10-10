#!/usr/bin/env python3
"""R5 round: filesystem snapshot of the product tree (before/after a bounded writer lane).

Hashes the product paths only (the evidence tree `.hgk/**` is excluded on purpose: it is the
round's own working area). Records git porcelain when a git binary is available.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\PIPD")
PATHS = ["src", "tools", "tests", "schemas", "docs", "skills", "fixtures", "dist",
         "pyproject.toml", "README.md", "LICENSE", "PROVENANCE.md", "SBOM.cdx.json"]
SKIP_PARTS = {"__pycache__", ".git"}


def snap() -> dict:
    rows = {}
    for rel in PATHS:
        p = ROOT / rel
        if p.is_file():
            rows[rel] = {"size": p.stat().st_size,
                         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file() or any(part in SKIP_PARTS for part in f.parts):
                    continue
                rows[f.relative_to(ROOT).as_posix()] = {
                    "size": f.stat().st_size,
                    "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                }
    try:
        porcelain = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "-uall"],
                                   capture_output=True, text=True, timeout=120).stdout.splitlines()
        head = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as exc:  # noqa: BLE001
        porcelain, head = [f"GIT_UNAVAILABLE: {exc}"], ""
    return {"root": str(ROOT), "head": head, "file_count": len(rows), "files": rows,
            "porcelain": porcelain}


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    data = snap()
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8", newline="")
    print(json.dumps({"out": str(out), "head": data["head"], "file_count": data["file_count"],
                      "porcelain_count": len(data["porcelain"])}, ensure_ascii=False))
