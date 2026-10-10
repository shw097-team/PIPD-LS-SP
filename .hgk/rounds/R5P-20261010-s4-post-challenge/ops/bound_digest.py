#!/usr/bin/env python3
"""The round's ONE bound product-digest definition, plus the rejected alternative.

Independent challenge C8 (2026-10-10) reported `f2b288ad... (283 files)` from this round's
`product_snapshot.walk` scope while the AO brief published `4a039259...` from `equivalence.py`'s
narrower prefix scope. Both numbers were the round's own; the ambiguity was the round's defect.

This tool fixes the definition: it is `product_snapshot.walk` (PRODUCT_ROOTS, EXCLUDE_DIRS,
EXCLUDE_SUFFIX), rows = [rel_posix, sha256_file] sorted, digest = sha256 of canonical JSON of the
rows. It emits the bound digest for a candidate root together with the rejected alternative, and
states verbatim what a checker must reproduce.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", ".hgk", ".agents", ".hermes", ".venv", "node_modules"}
EXCLUDE_SUFFIX = {".pyc", ".pyo"}
PRODUCT_ROOTS = ["src", "tests", "tools", "schemas", "dist", "docs", "skills", "fixtures",
                 "pyproject.toml", "README.md", "ACCEPTANCE.md", "LICENSE", "PROVENANCE.md",
                 "SBOM.cdx.json", "OWNER_LICENSE_DECISION.yaml", "openspec"]
# The definition `equivalence.py` used for the subject-binding line in the AO brief. REJECTED as the
# bound digest (it silently omits packaging metadata, LICENSE, openspec and other roots).
ALT_ROOTS = ["src", "tools", "tests", "schemas", "skills", "docs", "dist", "fixtures"]

BOUND_DEFINITION = ("product_digest = sha256 of canonical JSON (separators ',',':', ensure_ascii=False, "
                    "keys n/a) of the sorted rows [[posix_relative_path, sha256_file], ...] over "
                    "PRODUCT_ROOTS=" + json.dumps(PRODUCT_ROOTS) + ", excluding any path with a part in "
                    "EXCLUDE_DIRS=" + json.dumps(sorted(EXCLUDE_DIRS)) + " or a suffix in "
                    "EXCLUDE_SUFFIX=" + json.dumps(sorted(EXCLUDE_SUFFIX)) + ".")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walk(root: Path, roots: list[str]) -> list[Path]:
    out: list[Path] = []
    for rel in roots:
        t = root / rel
        if t.is_file():
            out.append(t)
        elif t.is_dir():
            for f in sorted(t.rglob("*")):
                if not f.is_file():
                    continue
                if any(part in EXCLUDE_DIRS for part in f.parts):
                    continue
                if f.suffix in EXCLUDE_SUFFIX:
                    continue
                out.append(f)
    return out


def digest(root: Path, roots=None) -> dict:
    files = walk(root, roots or PRODUCT_ROOTS)
    rows = [[str(f.relative_to(root)).replace("\\", "/"), sha256_file(f)] for f in files]
    rows.sort()
    return {"file_count": len(rows),
            "digest": hashlib.sha256(
                json.dumps(rows, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(),
            "roots": roots or PRODUCT_ROOTS}


if __name__ == "__main__":
    root = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    bound = digest(root)
    alt = digest(root, ALT_ROOTS)
    receipt = {
        "schema": "PIPD-R5P-DIGEST-BINDING/1",
        "candidate_root": str(root).replace("\\", "/"),
        "bound_definition": BOUND_DEFINITION,
        "bound_product_digest": bound["digest"],
        "bound_file_count": bound["file_count"],
        "rejected_alternative": {
            "definition": "equivalence.py product digest over PRODUCT_PREFIXES=" + json.dumps(ALT_ROOTS),
            "product_digest": alt["digest"], "file_count": alt["file_count"],
            "why_rejected": ("narrower scope: omits packaging/legal/openspec roots, so two of the round's "
                             "own scripts published different numbers for the same subject (challenge C8)")},
        "checker_reproduction": ("python ops/bound_digest.py <pristine_root> then compare "
                                 "bound_product_digest"),
    }
    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    if out_path:
        out_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8")
