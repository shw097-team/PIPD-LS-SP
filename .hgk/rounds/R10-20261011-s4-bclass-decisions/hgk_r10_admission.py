#!/usr/bin/env python3
"""Admit the R10 (owner-decision adjudication + control-plane credential tooling) obligations.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as
R5P/R5Q/R5R/R7/R8/R9: project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound
admit_requirement calls. New requirement ids (R10) keep every earlier row untouched.

Two of these obligations are deliberately NOT "close the gap" wording: the point of R10 is to obtain
an ADJUDICATION on whether three crosswalk rows' objects should exist at all, and to move credential
tooling off ephemeral scratch - and each of those can legitimately end in "no", recorded with reasons.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R10-AUTHORING-001", "P0", "DOCS-OWNER",
     "WO-R10-AUTHORING-001: adjudicate the three active SPEC/DEL rows whose required SSOT objects do "
     "not exist (PIPD-SP-SPEC-002 -> a materialised PIPD-LIFECYCLE-SPEC@1.1.0; PIPD-SP-SPEC-030 -> an "
     "MCP materialization object; DEL-015 -> ADAPTER_REGISTRY@1). For each, determine whether this "
     "project genuinely OWES the object, whether it is owned by another layer or the external "
     "blueprint, and whether the object can be materialised FAITHFULLY from material that already "
     "exists in this repository without inventing content. Author only what is honestly derivable; "
     "record the rest as scope decisions with the reason. Manufacturing an object whose only purpose "
     "is to move a coverage counter is forbidden: EXISTS != TRUE."),
    ("REQ-PIPD-R10-CREDITOOLS-002", "P0", "CREDENTIAL-BROKER",
     "WO-R10-CREDITOOLS-002: the credential broker designed in R9 currently lives in ephemeral agent "
     "scratch, which is pruned when idle, so it cannot serve an unattended run. Determine the correct "
     "durable home and the correct governance route for installing it, produce the migration plan and "
     "a ready-to-apply candidate, and enumerate exactly the steps that remain human with the reason "
     "each cannot be automated. Any control-plane change it requires is to be identified as its own "
     "admitted round rather than ridden in on a product round. No secret may appear in any artefact."),
    ("REQ-PIPD-R10-ADMIT-003", "P0", "DOCS-OWNER",
     "WO-R10-ADMIT-003: run HGK admission for this round before any work product is written, and "
     "produce the KANBAN, SWARM, GSTACK and OPENSPEC artefacts for the round as files on disk - a board "
     "or swarm that exists only in narration is not evidence of one. Where an artifact cannot be "
     "produced, say so rather than asserting a state."),
    ("REQ-PIPD-R10-EXECUTE-004", "P0", "EXECUTE-LANE",
     "WO-R10-EXECUTE-004: execute the adjudicated plans - author the faithfully derivable SSOT "
     "artefacts, and place the credential tooling candidate in its determined home - using the bounded "
     "writer route, then verify each artefact against the material it was derived from. Where an "
     "adjudication concluded 'do not build', the executed deliverable is the recorded decision and its "
     "reason, not a manufactured object."),
    ("REQ-PIPD-R10-VERIFY-005", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R10-VERIFY-005: independent check on the CODEX CLI VERIFY lane (checker gpt-6.1-sol, medium, "
     "OpenAI OAuth), asserting ONLY immutable facts - published tag identities, artefact hashes, and "
     "the content of the round artefacts - and merely REPORTING anything that legitimately moves, such "
     "as a branch tip. The maker cannot sign its own verdict, and the receipt must state what the "
     "checker could not verify."),
    ("REQ-PIPD-R10-CLOSURE-006", "P0", "DOCS-OWNER",
     "WO-R10-CLOSURE-006: close the round with a report that states the claim ceiling and every item "
     "that remains open, classified by WHO can close it - this round, the owner, or an external "
     "acceptor. Every side effect of the round is disclosed, including pushes, tag integrity and any "
     "canonical-store or control-plane write."),
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
    (args.out / "r10_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
