#!/usr/bin/env python3
"""Admit the R9 (A-class gap closure + owner-adjudication execution) obligations.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as R5P/R5Q/R5R/R7:
project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound admit_requirement calls.
New requirement ids (R9) keep every earlier row untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R9-SRCSCAN-001", "P0", "SECURITY",
     "WO-R9-SRCSCAN-001: scan THIS PROJECT'S OWN SOURCE for vulnerabilities. The R7 dependency audit "
     "covered only the declared closure and pip-audit explicitly SKIPPED pipd-ls-sp because it is not "
     "on PyPI, so 'no known vulnerabilities' never covered our code. Produce a source-level result with "
     "its tool, version, rule set and every finding triaged; an empty finding list must state the tool's "
     "detection ceiling rather than imply the code is clean."),
    ("REQ-PIPD-R9-AUDITGAP-002", "P0", "OWNER-EVIDENCE",
     "WO-R9-AUDITGAP-002: audit each of the 10 ACTIVE gaps in the SPEC/DEL crosswalk individually. "
     "PARTIAL_CHALLENGE at 28 evidenced / 10 active / 19 deferred is a COUNT, not a result, and "
     "EVIDENCED != PASS. Each active row must get its own disposition with evidence or be named as still "
     "open; the denominator must be reconciled against the crosswalk rather than restated."),
    ("REQ-PIPD-R9-DEL018MAIN-003", "P0", "OWNER-EVIDENCE",
     "WO-R9-DEL018MAIN-003: resolve DEL-018 on main, where the merged tree has 253 product paths and "
     "253-docs/FRONT_PAGE_HISTORY.md has no disposition in the release-evidence manifest. Extending the "
     "manifest's enumerated subject is a release-evidence definition change and must be adjudicated "
     "explicitly, executed if sanctioned, and must not be achieved by editing the validator."),
    ("REQ-PIPD-R9-CLEANTREE-004", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R9-CLEANTREE-004: re-run the cross-model VERIFY_SECURITY check on a CLEAN committed tree. The "
     "R8 cross-model receipt returned ok:true on the arm but the checker's verdict was FAIL solely "
     "because its strict clean-worktree gate observed the round's own untracked directory. Convert that "
     "harness artifact into a real verdict from a committed tree, keeping the non-mutation guard."),
    ("REQ-PIPD-R9-CREDROT-005", "P0", "CREDENTIAL-BROKER",
     "WO-R9-CREDROT-005: design and implement a HIGH-AUTOMATION, MINIMAL-HUMAN-INTERVENTION credential "
     "scheme so long unattended runs do not depend on a long-lived owner PAT. It must fail closed when "
     "no credential is available, must never place a secret in argv/stdout/logs/prompt/evidence/remote "
     "URL, and must state plainly which residual step still needs the owner and why it cannot be removed."),
    ("REQ-PIPD-R9-KANBAN-006", "P1", "DOCS-OWNER",
     "WO-R9-KANBAN-006: close the round bookkeeping gap - the R8 kanban/swarm terminal state was never "
     "independently re-verified. Verify or explicitly record its state, and produce the kanban, swarm "
     "and openspec artifacts for this round rather than asserting a board state that is not evidenced."),
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
    (args.out / "r9_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
