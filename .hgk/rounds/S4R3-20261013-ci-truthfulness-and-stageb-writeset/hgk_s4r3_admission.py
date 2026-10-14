#!/usr/bin/env python3
"""Admit the S4R3 round's obligations into the HG-KSEOS Shared Spine (typed API only).

Typed SharedSpine / ProjectLifecycleController API, same pattern as R5P/R5Q/R5R/R7/R8/R9/R10/R11:
project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound admit_requirement calls.
Requirement ids iterate off the source order's OWN change_sequence ids
(PIPD-S4-R3-HERMES-HGK-THIN-COMMAND/1: S4R3-STAGE-A-CORE-REPAIR, S4R3-STAGE-B-DISTRIBUTION) rather
than inventing new workstream numbers; the round-level admission/verify/closure obligations carry
their own ids, matching the project's established convention.

ORDERING DISCLOSURE: the two C0-C9 contracts were compiled and the first candidate edits were
authored in the worktree BEFORE this admission ran. Admission therefore precedes the COMMIT, the
PUSH and every publication act, but not the first uncommitted candidate draft. This is recorded in
the round result rather than smoothed over.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-S4R3-STAGE-A-CORE-REPAIR-001", "P0", "CI-OWNER",
     "WO-S4R3-A-001: make the ci workflow's test steps carry the suite's own exit code, and repair at "
     "root cause the 11 full-suite and 2 focused-suite failures observed on hosted Linux at candidate "
     "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed (report S4R3-F001), without skipping, narrowing the "
     "denominator or editing any acceptance oracle. The repair must hold on Linux and on Windows and "
     "the raw log, exit code and denominator must be returned for both."),
    ("REQ-S4R3-STAGE-A-CORE-REPAIR-002", "P0", "TQAEP-OWNER",
     "WO-S4R3-A-002: repair the remaining Stage A portability and guard defects named by S4R3-F001 - "
     "the executable bit of the first-run bash runner, the PowerShell runner's dependence on a "
     "Windows-only environment variable, the repair-subject containment check whose behaviour differs "
     "between a POSIX and a Windows path flavour, the undeclared test dependency that made the "
     "skill-contract checker refuse with TOOL_MISSING, and the destination assertion that mis-stated "
     "what a refused build is allowed to leave behind. Each repair keeps the negative behaviour it "
     "protects."),
    ("REQ-S4R3-STAGE-B-DISTRIBUTION-001", "P0", "PKG07-OWNER",
     "WO-S4R3-B-001: make the Stage B write-set gate measure the change sequence it actually governs. "
     "It must compute its scope against the DECLARED Stage B base, refuse when that base is not an "
     "ancestor of the candidate, publish the full upstream diff as an inventory, and still fail on a "
     "forbidden path written inside the Stage B scope. Widening the allowlist to buy a green run is "
     "forbidden (report S4R3-F002)."),
    ("REQ-S4R3-STAGE-B-DISTRIBUTION-002", "P1", "DX-OWNER",
     "WO-S4R3-B-002: close the Stage B user-facing gaps - ship the single Web fallback document as a "
     "real downloadable artefact with its digest, give the repository one front-page navigation with "
     "one install SSOT, and add exactly ONE user guide, with every hop of README -> guide -> install "
     "SSOT -> fixture resolving. Statements about Preview limitations must match the published "
     "artefacts (report S4R3-F004)."),
    ("REQ-S4R3-ADMIT-003", "P0", "DOCS-OWNER",
     "WO-S4R3-ADMIT-003: keep KANBAN, SWARM, GSTACK and OPENSPEC artefacts for this round as files on "
     "disk - a board or swarm that exists only in narration is not evidence of one - and record the "
     "admission, the compiler receipts and the frozen subject in the round directory."),
    ("REQ-S4R3-VERIFY-004", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-S4R3-VERIFY-004: independent check on the CODEX CLI VERIFY lane (checker gpt-6.1-sol, medium, "
     "OpenAI OAuth, distinct from the maker lane) against the frozen Stage A and Stage B candidates. "
     "The checker re-derives its verdict from the raw receipts, must not read the maker's prose as "
     "evidence, and must end with an explicit PASS/FAIL plus the ids it could not verify."),
    ("REQ-S4R3-CLOSURE-005", "P0", "DOCS-OWNER",
     "WO-S4R3-CLOSURE-005: close the round with a report that states the claim ceiling, the items "
     "closed, and every item that remains open classified by WHO can close it - this round, the owner, "
     "or an external acceptor. Every side effect (pushes, canonical-store writes, control-plane "
     "reads) is disclosed, and merge, release and S4 full pass stay HOLD."),
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
    for req_id, priority, owner, wording in OBLIGATIONS:
        try:
            out = lc.admit_requirement(args.project_id, req_id, wording,
                                       owner=owner, priority=priority)
            result["admitted"].append({"requirement_id": req_id, "owner": owner,
                                       "priority": priority, "result": out})
        except Exception as exc:  # noqa: BLE001 - recorded, never hidden
            result["errors"].append({"requirement_id": req_id,
                                     "error": f"{type(exc).__name__}: {exc}"})
    if args.checkpoint:
        try:
            result["checkpoint"] = lc.checkpoint(args.project_id, evidence_refs=list(args.evidence))
        except Exception as exc:  # noqa: BLE001
            result["errors"].append({"checkpoint": f"{type(exc).__name__}: {exc}"})
    result["status_after"] = lc.status(args.project_id)
    (args.out / "s4r3_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"admitted": len(result["admitted"]), "errors": result["errors"],
                      "status_after": result.get("status_after")}, ensure_ascii=False, indent=1,
                     default=str))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
