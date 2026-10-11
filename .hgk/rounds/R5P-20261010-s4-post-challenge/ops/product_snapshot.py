#!/usr/bin/env python3
"""Round-local product/evidence snapshotter.

product_digest = sha256 over canonical JSON of sorted [[rel, sha256]] for the product paths
(excluding .git, __pycache__, .hgk evidence and dist/*.whl binary churn is INCLUDED - the wheel is
part of the candidate tuple). Prints a JSON block; also usable as a module.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:/Projects/Agent_Workspace/PIPD")
EXCLUDE_DIRS = {".git", "__pycache__", ".hgk", ".agents", ".hermes", ".venv", "node_modules"}
EXCLUDE_SUFFIX = {".pyc", ".pyo"}
PRODUCT_ROOTS = ["src", "tests", "tools", "schemas", "dist", "docs", "skills", "fixtures",
                 "pyproject.toml", "README.md", "ACCEPTANCE.md", "LICENSE", "PROVENANCE.md",
                 "SBOM.cdx.json", "OWNER_LICENSE_DECISION.yaml", "openspec"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walk(root: Path) -> list[Path]:
    out: list[Path] = []
    for rel in PRODUCT_ROOTS:
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


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO).replace("\\", "/"), *args],
                              capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception as exc:  # noqa: BLE001
        return f"<error: {exc}>"


def snapshot() -> dict:
    files = walk(REPO)
    rows = [[str(f.relative_to(REPO)).replace("\\", "/"), sha256_file(f)] for f in files]
    rows.sort()
    digest = hashlib.sha256(json.dumps(rows, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    return {"schema": "PIPD-R5P-PRODUCT-SNAPSHOT/1",
            "head": git("rev-parse", "HEAD"),
            "tree": git("rev-parse", "HEAD^{tree}"),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty_porcelain": git("status", "--porcelain=v1").splitlines(),
            "file_count": len(rows),
            "product_digest": digest,
            "wheel_sha256": (sha256_file(REPO / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl")
                             if (REPO / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl").is_file() else None),
            "files": rows}


if __name__ == "__main__":
    s = snapshot()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    text = json.dumps(s, ensure_ascii=False, indent=1)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8", newline="")
    print(json.dumps({k: v for k, v in s.items() if k != "files"}, ensure_ascii=False, indent=1))
