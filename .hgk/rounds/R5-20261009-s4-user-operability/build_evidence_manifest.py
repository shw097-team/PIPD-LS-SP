#!/usr/bin/env python3
"""Build the external-acceptance evidence manifest for the R5 S4 round.

Purpose: an external verifier cloning the public branch must be able to see, for every
piece of round evidence, either the artifact itself or a hash proving what was withheld
and why. Nothing is silently dropped.

Disposition rules:
  DELIVERED          -> committed to the public tree at the listed path
  EXCLUDED_OVERSIZE  -> transcript > 256 KiB; hash + size recorded here instead
  EXCLUDED_SCRATCH   -> Hermes-runtime path, not a repo artifact (recorded only)

Writes .hgk/rounds/R5-20261009-s4-user-operability/EVIDENCE_MANIFEST.json
"""
import hashlib
import json
import os
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/PIPD")
ROUND_REL = ".hgk/rounds/R5-20261009-s4-user-operability"
ROUND = REPO / ROUND_REL
OVERSIZE = 256 * 1024

# Files that must reach the external verifier even though they are transcripts, because
# they carry a verdict or a report rather than raw model traffic.
FORCE_DELIVER = {
    f"{ROUND_REL}/ao/attempt7_codex_01512_verdict/AO_VERDICT.json",
    f"{ROUND_REL}/ao/attempt7_codex_01512_verdict/AO_REPORT.md",
    f"{ROUND_REL}/ao/attempt7_codex_01512_verdict/run_meta.txt",
    f"{ROUND_REL}/ao/attempt7_codex_01512_verdict/AO_PROGRESS.txt",
    f"{ROUND_REL}/ao/attempt_codex_01512/run_meta.txt",
    f"{ROUND_REL}/ao/attempt_codex_01512/AO_PROGRESS.txt",
}

# Whole subtrees that belong to earlier rounds / are already covered elsewhere: left alone.
SKIP_PREFIX = (
    f"{ROUND_REL}/host/",
)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    entries = []
    for p in sorted(ROUND.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith(SKIP_PREFIX):
            continue
        size = p.stat().st_size
        rec = {
            "path": rel,
            "bytes": size,
            "sha256": sha256(p),
        }
        if size > OVERSIZE and rel not in FORCE_DELIVER:
            rec["disposition"] = "EXCLUDED_OVERSIZE"
            rec["reason"] = (
                f"raw transcript {size} B > {OVERSIZE} B threshold; sha256 and size are the "
                "verifiable record of what was withheld. Obtain it from the maker only if the "
                "acceptance requires it."
            )
        else:
            rec["disposition"] = "DELIVERED"
        entries.append(rec)

    delivered = sum(1 for e in entries if e["disposition"] == "DELIVERED")
    withheld = sum(1 for e in entries if e["disposition"] == "EXCLUDED_OVERSIZE")

    # Artifacts that live in the Hermes runtime scratch and are NOT repo artifacts, but
    # whose committed copies are what the verifier reads.
    scratch_note = {
        "note": (
            "The independent-verification contract and the writer order originated in the Hermes "
            "runtime scratch directory. Repo copies are committed at "
            f"{ROUND_REL}/d1repair/CONTRACT-verify-D1.v1.md, "
            f"{ROUND_REL}/d1repair/CONTRACT-verify-D1.v2.md and "
            f"{ROUND_REL}/d1repair/WO-WS-A-codex-writer.md; those copies are the artifacts of record."
        )
    }

    doc = {
        "schema": "pipd-r5s4-evidence-manifest/1",
        "round": "R5-20261009-s4-user-operability",
        "round_dir": ROUND_REL,
        "oversize_threshold_bytes": OVERSIZE,
        "counts": {"total": len(entries), "delivered": delivered, "excluded_oversize": withheld},
        "scratch_note": scratch_note,
        "entries": entries,
    }
    out = ROUND / "EVIDENCE_MANIFEST.json"
    out.write_text(json.dumps(doc, indent=1, sort_keys=False) + "\n", encoding="utf-8", newline="\n")

    print(f"wrote {out.relative_to(REPO)}")
    print(f"  total {len(entries)}  delivered {delivered}  excluded_oversize {withheld}")
    for e in entries:
        if e["disposition"] != "DELIVERED":
            print(f"  WITHHELD  {e['bytes']:>9} B  {e['path']}")
    # Emit the delivered path list for the staged add.
    paths = [e["path"] for e in entries if e["disposition"] == "DELIVERED"]
    (ROUND / "DELIVERED_PATHS.txt").write_text("\n".join(paths) + "\n", encoding="utf-8", newline="\n")
    print(f"  delivered path list -> {ROUND_REL}/DELIVERED_PATHS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
