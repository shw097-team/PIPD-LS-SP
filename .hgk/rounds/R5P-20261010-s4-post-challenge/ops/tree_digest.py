#!/usr/bin/env python3
"""Tree digest equivalence proof: the working tree the round measured vs the pristine export of the
candidate commit. Same digest => the evidence describes exactly the committed candidate.

usage: python tree_digest.py <dir> [<dir> ...]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

SKIP = {".git", "__pycache__", ".hgk", ".venv", "venv"}


def digest(root: Path) -> tuple[str, int]:
    rows = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        rows.append([str(rel).replace("\\", "/"), hashlib.sha256(p.read_bytes()).hexdigest()])
    rows.sort()
    blob = json.dumps(rows, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest(), len(rows)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        p = Path(d)
        dg, n = digest(p)
        print(json.dumps({"dir": str(p), "files": n, "tree_digest": dg}, ensure_ascii=False))
