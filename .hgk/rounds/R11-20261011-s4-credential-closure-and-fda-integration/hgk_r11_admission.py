#!/usr/bin/env python3
"""Admit the R11 (credential closure executed by desktop automation + evidence integration) obligations.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as R5P..R10:
project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound admit_requirement calls.
New requirement ids (R11) keep every earlier row untouched.

This round exists because the previous one ended with a working capability nothing calls and two owner
acts nobody had performed. Two of these obligations are deliberately NOT "make it pass" wording: the
desktop-automation obligation can legitimately end in "the owner's interactive step is unavoidable", and
the activation obligation can legitimately end in "this belongs to its own round". Both are recordable
outcomes; manufacturing a closure is not.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R11-FDAEXEC-001", "P0", "DESKTOP-AUTOMATION-LANE",
     "WO-R11-FDAEXEC-001: execute, by driving the desktop/browser under the owner's explicit in-turn "
     "authorisation, the remaining credential operations for which GitHub exposes no API: delete the "
     "now-redundant personal account GitHub App created in R10 (it still holds a live private-key pair), "
     "and retire the long-lived personal access token that the credential broker no longer needs now that "
     "an ORGANISATION-owned App installation token is its preferred source. Every mutation must be "
     "confirmed by READBACK from GitHub, never by narration, and no credential value may appear in any "
     "artefact. Where an operation cannot complete without the owner's interactive second factor, record "
     "that as the outcome with the exact step that remains, rather than reporting the round as closed."),
    ("REQ-PIPD-R11-FDAEVID-002", "P0", "EVIDENCE-INTEGRATION",
     "WO-R11-FDAEVID-002: integrate this round's use of the desktop-automation capability into a "
     "discipline-and-evidence artefact that CONFORMS TO THAT CAPABILITY'S OWN EVIDENCE CONTRACT in the "
     "Fabric repository (single markdown with raw evidence embedded, no self-hash, manifest raw body "
     "embedded with its declared sha being the embedded body's sha, 3-way mirror, and its preflight "
     "checker reporting PASS) - not a format of this round's own invention. Place it in that team's "
     "evidence folder and update the Fabric repository with ONLY the paths this round authored or "
     "deliberately refreshed. The Fabric working tree already carries dozens of uncommitted entries left "
     "by other sessions; they are NOT this round's work and must not be swept into its commit."),
    ("REQ-PIPD-R11-ACTIVATE-003", "P0", "CONTROL-PLANE",
     "WO-R11-ACTIVATE-003: adjudicate whether the credential broker - now proven end to end for BOTH "
     "read and write, yet referenced zero times by the control plane's config - should be ACTIVATED in "
     "this round or deferred to a round of its own, and execute the adjudicated outcome. Record plainly "
     "that a working capability nothing calls is not yet a delivered capability, and scope any activation "
     "claim to the surface it actually covers. If the honest answer is 'its own round', that is the "
     "deliverable."),
    ("REQ-PIPD-R11-ADMIT-004", "P0", "GOVERNANCE",
     "WO-R11-ADMIT-004: run HGK admission for this round before any work product is written, and produce "
     "the KANBAN, SWARM, GSTACK and OPENSPEC artefacts for the round as files on disk - a board or roster "
     "that exists only in narration is not evidence of one. Where an artefact cannot be produced, say so "
     "rather than asserting a state."),
    ("REQ-PIPD-R11-VERIFY-005", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R11-VERIFY-005: independent check on the CODEX CLI VERIFY lane (checker openai-codex/gpt-6.1-sol, "
     "reasoning medium, OpenAI OAuth), asserting ONLY immutable facts - artefact hashes, the content of "
     "the round artefacts, published tag identities - and merely REPORTING anything that legitimately "
     "moves, such as a branch tip. The maker cannot sign its own verdict, and the receipt must state what "
     "the checker could not verify. Where model diversity between maker and checker is absent, report the "
     "residual honestly instead of claiming separation that does not exist."),
    ("REQ-PIPD-R11-CLOSURE-006", "P0", "CLOSURE",
     "WO-R11-CLOSURE-006: close the round with a report stating the claim ceiling and every item that "
     "remains open, classified by WHO can close it - this round, the owner, or an external acceptor. "
     "Every side effect is disclosed: pushes in each repository touched, the state of the Fabric "
     "working tree, every credential mutation performed through the browser, and any host-side change "
     "made to enable the automation."),
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
    (args.out / "r11_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
