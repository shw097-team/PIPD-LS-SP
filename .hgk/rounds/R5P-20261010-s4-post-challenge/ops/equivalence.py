#!/usr/bin/env python3
"""Line-ending-normalised equivalence proof between the measured working tree and the pristine
export of the candidate commit, plus the product-path digest the round binds as its subject.

usage: python equivalence.py <worktree> <export> <out.json>
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SKIP = {".git", "__pycache__", ".hgk", ".venv", "venv"}
PRODUCT_PREFIXES = ("src/", "tools/", "tests/", "schemas/", "skills/", "docs/", "dist/", "fixtures/")


def norm(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n")


def rows(root: Path, normalize: bool) -> dict[str, str]:
    out = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        b = p.read_bytes()
        out[str(rel).replace("\\", "/")] = hashlib.sha256(norm(b) if normalize else b).hexdigest()
    return out


def digest(pairs: dict[str, str]) -> str:
    blob = json.dumps(sorted(pairs.items()), separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def main() -> int:
    work, export, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    a, b = rows(work, True), rows(export, True)
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    differing = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    prod = {k: v for k, v in b.items() if k.startswith(PRODUCT_PREFIXES)}
    receipt = {
        "schema": "PIPD-R5P-TREE-EQUIVALENCE/1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "normalisation": "CRLF -> LF before hashing (git archive exports blobs; the worktree checks out CRLF on some files)",
        "worktree": str(work),
        "export": str(export),
        "worktree_tree_digest_normalised": digest(a),
        "export_tree_digest_normalised": digest(b),
        "equivalent": not only_a and not only_b and not differing,
        "untracked_only_in_worktree": only_a,
        "only_in_export": only_b,
        "content_differs": differing,
        "product_digest_export": digest(prod),
        "product_files": sorted(prod),
    }
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("equivalent", "untracked_only_in_worktree",
                                              "content_differs", "product_digest_export")},
                     ensure_ascii=False, indent=1)[:900])
    return 0


if __name__ == "__main__":
    sys.exit(main())
