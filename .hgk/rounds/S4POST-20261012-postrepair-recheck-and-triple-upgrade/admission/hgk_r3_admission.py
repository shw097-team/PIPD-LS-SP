#!/usr/bin/env python3
"""Admit the R3 (post-repair recheck + triple small upgrade, executing the FAR low-resistance plan)
obligations against project PIPD-LS-SP-20261008.

Typed SharedSpine / ProjectLifecycleController API only, same pattern as R5P..R11: the project is
already EXECUTING, so these are late-bound admit_requirement calls. New requirement ids keep every
earlier row untouched.

Two of these obligations are deliberately NOT "make it pass" wording: the CI obligation can legitimately
end in "the workflow is red for a reason that belongs to the owner" and the publication obligation can
legitimately end in "the external acceptor has the branch and the owner still has to sign the candidate".
Both are recordable outcomes; manufacturing a green result is not.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R3-FAR-001", "P0", "FAR-DEVIATION-STUDY",
     "WO-R3-FAR-001: study the round's own implementation against the three governing documents "
     "(the project blueprint, the command PROMPT and the external post-repair recheck verdict) and "
     "record every deviation with a verbatim locator, including the deviation the maker itself caused "
     "(an unapproved expansion of the verification harness), then propose lowest-friction remedies "
     "ordered by return on effort. The study is a research deliverable: it may not grant itself any "
     "state, and the one remedy that needs a control-plane decision is addressed to the owner."),
    ("REQ-PIPD-R3-EVIDENCE-002", "P0", "EVIDENCE-CLOSURE",
     "WO-R3-EVIDENCE-002: complete the round's Evidence Return Pack with the fields the recheck verdict "
     "found missing (commands with raw exit codes, test counts and log digests; release assets with the "
     "DOWNLOADED sha256 next to the API-reported one; a manifest digest), and record the separation of "
     "duties at identity level rather than asserting it. Published assets were re-downloaded anonymously "
     "and hashed; integrity against API metadata is NOT reproducibility from the tag, and the pack must "
     "say so."),
    ("REQ-PIPD-R3-CI-003", "P0", "MINIMAL-CI-FIRST-RUN",
     "WO-R3-CI-003: make the repository's approved minimal read-only workflow actually execute and record "
     "what it says. The workflow existed but every run had aborted before the first functional step; find "
     "and fix the blocking cause with the smallest change, keep the trigger set read-only, and report the "
     "result step by step. A red run that names a real defect is the deliverable; adjusting the gate so it "
     "passes is not."),
    ("REQ-PIPD-R3-SURFACES-004", "P0", "GOVERNANCE-SURFACES",
     "WO-R3-SURFACES-004: run the admission for this round before the work product is written and produce "
     "the KANBAN, SWARM, GSTACK and OPENSPEC artefacts as files on disk with the real ids and the real "
     "tool output - a board, roster or route that exists only in narration is not evidence of one. Where "
     "an artefact cannot be produced, say so."),
    ("REQ-PIPD-R3-OWNER-005", "P0", "OWNER-ACTION-REQUEST",
     "WO-R3-OWNER-005: turn every gap that only the owner can close into one decision-ready request: the "
     "four supplies that block the public candidate, the four acts reserved to the owner, the external "
     "evidence items no agent can obtain, and the design decisions the round declines to answer for the "
     "owner. The request may not fill any of them in, and may not present a candidate-only state as a "
     "granted one."),
    ("REQ-PIPD-R3-PUBLISH-006", "P0", "EXTERNAL-ACCEPTOR-HANDOFF",
     "WO-R3-PUBLISH-006: publish the candidate and its evidence so an external acceptance officer can "
     "verify it without the maker: the product changeset separated from the round's verification harness, "
     "an entry document whose commands run as written on a clean clone, the failing gates stated at the "
     "top, and a draft pull request that gives the read-only workflow its first real run. Never force, "
     "never push the default branch, never move a tag, and never state a claim ceiling above what the "
     "evidence supports."),
    ("REQ-PIPD-R3-VERIFY-007", "P0", "INDEPENDENT-VERIFY",
     "WO-R3-VERIFY-007: obtain an independent check from a different identity and a different model than "
     "the maker, asserting only immutable facts - digests, the content of the round artefacts, published "
     "ref identities - and merely reporting anything that legitimately moves, such as a branch tip. The "
     "maker cannot sign its own verdict and must state what the checker could not verify."),
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
    (args.out / "r3_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "status_before": result["status_before"],
                      "status_after": result["status_after"], "errors": result["errors"]},
                     ensure_ascii=False, default=str))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
