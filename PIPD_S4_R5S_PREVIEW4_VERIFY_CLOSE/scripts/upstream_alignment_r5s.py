"""Record the upstream artefacts this session's work must align with, with verifiable digests.

The knowledge base is READ-ONLY: this reads and hashes it, it never writes into it.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

KB = Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD")
PKG = KB / "PIPD-LS-SP_PIPD-PKG/PIPD-LS-SP_PIPD-PKG-00~PKG-10"
OUT = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/landing")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


anchor = [
    ("PKG-00", "authority boundary / role of the package set"),
    ("PKG-02", "PI / Trace: the atom, locator and trace the D1/D2 repair must not break"),
    ("PKG-05", "handoff"),
    ("PKG-06", "TQAEP: positive/negative/regression and anti-false-green"),
    ("PKG-07", "Skills / Host: the exactly-eight skill projection and host qualification boundary"),
    ("PKG-08", "Packaging / Release: wheel, plugin ZIP, immutable tag, asset identity"),
    ("PKG-09", "Regression: the suite baseline and false-green discipline"),
    ("PKG-10", "interop"),
]
files = sorted(p for p in PKG.iterdir() if p.is_file())
rec = {
    "schema": "R5S-UPSTREAM-ALIGNMENT/1",
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "knowledge_base_root": str(KB).replace("\\", "/"),
    "read_only": True,
    "written_into_the_knowledge_base": False,
    "pkg_docs": [{"name": p.name, "bytes": p.stat().st_size, "sha256": sha(p)} for p in files],
    "clause_anchors": [{"doc": d, "why": w} for d, w in anchor],
    "session_edits_to_the_knowledge_base": [],
    "claim_ceiling": "the digests prove which upstream bytes this round was working from; they are not a per-clause semantic verification of those documents",
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "UPSTREAM_ALIGNMENT.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"pkg_docs": len(rec["pkg_docs"]), "first": rec["pkg_docs"][0]["name"] if rec["pkg_docs"] else None}, indent=1))
