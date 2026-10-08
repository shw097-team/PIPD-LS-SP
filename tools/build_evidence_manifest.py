#!/usr/bin/env python3
"""Regenerate .hgk/artifacts/evidence_manifest.json (path -> sha256) for the current tree."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

R = Path(r"C:\Projects\Agent_Workspace\PIPD")
man: dict[str, str] = {}
for f in sorted(R.rglob("*")):
    if not f.is_file():
        continue
    if ".git" in f.parts or "__pycache__" in f.parts or f.suffix in (".db", ".pyc"):
        continue
    rel = str(f.relative_to(R)).replace(chr(92), "/")
    man[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
out = R / ".hgk" / "artifacts" / "evidence_manifest.json"
out.write_text(json.dumps(man, indent=0, sort_keys=True), encoding="utf-8", newline="")
print(json.dumps({"entries": len(man), "bytes": out.stat().st_size,
                  "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, indent=1))
