#!/usr/bin/env python3
"""Admit the R5 S4 user-operability repair obligations into the HG-KSEOS lifecycle.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL).
Project: PIPD-LS-SP-20261008 (already EXECUTING) -> late-bound admit_requirement.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R5-DEST-001", "P0", "PIPD-EC",
     "WO-S4-DEST-001: pipd project --out must resolve and refuse any unsafe destination "
     "(empty/., .., cwd, home, filesystem root, repo root, source ancestor/descendant, symlink/junction "
     "escape, MSYS /c/..., preexisting non-empty) BEFORE any create/delete/replace, then stage and publish "
     "atomically; --dry-run performs the same safety validation with zero side effects "
     "(R4 challenge F-R4-S4-01 / S4-USER-SEC-001)."),
    ("REQ-PIPD-R5-DIST-002", "P0", "PKG-08",
     "WO-S4-DIST-002: rebuild a deterministic wheel from the frozen R5 candidate carrying the current "
     "modules (requirements.py, repo_context.py, projection.py) plus the registry and the 19 schemas, with "
     "install-safe resource lookup so a fresh venv install works with no PYTHONPATH and a non-repo cwd; the "
     "stale R2 wheel must be rejected as the R5 distribution artefact "
     "(R4 challenge F-R4-S4-02 / S4-USER-DIST-002)."),
    ("REQ-PIPD-R5-EXPORT-003", "P1", "PIPD-EC",
     "WO-S4-EXPORT-003: pipd export --out must write a real portable bundle (archive + manifest + per-item "
     "checksums) at the requested destination with staging, secret/PII scan and atomic publish, and --dry-run "
     "must write nothing; silently ignoring args.out is a contract violation "
     "(R4 challenge F-R4-S4-03 / S4-USER-EXPORT-003)."),
    ("REQ-PIPD-R5-UAT-004", "P1", "TQAEP-CHECKER",
     "WO-S4-UAT-004: execute UAT-00..12 on the frozen candidate with both a freshly installed wheel and a "
     "source import, recording environment, argv, stdout/stderr/exit, before/after filesystem canary hashes, "
     "replay determinism and checker identity; --help smoke tests do not count "
     "(R4 challenge F-R4-S4-04)."),
    ("REQ-PIPD-R5-PERF-005", "P1", "PERF-OWNER",
     "WO-S2-PERF-005: obtain the owner-ratified provenance for the three timing thresholds and the context "
     "budget, keep the standing 343547 > 20000 FAIL visible, and separate serialized bytes from effective "
     "model context (R4 challenge F-R4-S2-05)."),
    ("REQ-PIPD-R5-PUBLISH-006", "P1", "EVIDENCE-OWNER",
     "WO-R4-PUBLISH-006: produce a fresh publication projection manifest and subject attestation bound to "
     "the R5 candidate (commit/tree/product digest/manifest digest/exclusions) without inheriting any R3/R4 "
     "seal, and keep the local vs published subject distinction explicit (R4 challenge F-R4-PUB-06)."),
    ("REQ-PIPD-R5-ORCH-007", "P1", "HGK-ORCH-OWNER",
     "WO-HGK-ORCH-007: if the S4 install/UAT path actually traverses the Hermes/HGK native command boundary, "
     "add an explicit MSYS /c/... -> Windows path guard, credential/URL redaction and safe process invocation "
     "at that boundary; otherwise record it as an S5 precondition instead of claiming an S4 repair "
     "(R4 challenge F-R4-HARNESS-07)."),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hgk-root", required=True, type=Path)
    ap.add_argument("--project-id", default="PIPD-LS-SP-20261008")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--checkpoint", action="store_true")
    ap.add_argument("--evidence", nargs="*", default=[])
    args = ap.parse_args()

    sys.path.insert(0, str(args.hgk_root / "src"))
    from hg_kseos.spine import SharedSpine
    from hg_kseos.lifecycle import ProjectLifecycleController

    spine = SharedSpine(args.hgk_root / "var/shared-spine/hg-kseos.db",
                        args.hgk_root / "src/hg_kseos/schema.sql")
    lc = ProjectLifecycleController(spine)
    args.out.mkdir(parents=True, exist_ok=True)

    result: dict = {"step": "admit_requirement", "project_id": args.project_id,
                    "status_before": lc.status(args.project_id), "admitted": [], "errors": []}
    for rid, priority, owner, wording in OBLIGATIONS:
        try:
            admitted = lc.admit_requirement(args.project_id, rid, wording,
                                            owner=owner, priority=priority)
            result["admitted"].append(admitted)
        except Exception as exc:  # noqa: BLE001 - record, never hide
            result["errors"].append({"requirement_id": rid, "error": f"{type(exc).__name__}: {exc}"})
    if args.checkpoint:
        result["checkpoint"] = lc.checkpoint(args.project_id, evidence_refs=args.evidence)
    result["status_after"] = lc.status(args.project_id)
    (args.out / "r5_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({k: result[k] for k in ("step", "errors")}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2500])
    if "checkpoint" in result:
        print("checkpoint:", json.dumps(result["checkpoint"], ensure_ascii=False, default=str)[:600])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
