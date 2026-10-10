#!/usr/bin/env python3
"""Admit the R5R (CE-1/CE-2 repair + CODEX-CLI independent verification) obligations.

Typed SharedSpine / ProjectLifecycleController API only — no raw SQL, no state-column writes.
Project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound `admit_requirement`
calls; the R5R ids leave every R5/R5P/R5Q row untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R5R-FAR-001", "P0", "OWNER+FAR",
     "WO-R5R-FAR-001: a FAR quick study enumerates the candidate repairs for CE-1 (validate does not "
     "resolve the schemas the wheel ships, unlike doctor) and CE-2 (compile-pi emits a top-level "
     "_profile_meta that the PI-PKG schema forbids), decides between them against explicit criteria and "
     "records the rejected alternatives with reasons."),
    ("REQ-PIPD-R5R-REPAIR-002", "P0", "PIPD-EC",
     "WO-R5R-REPAIR-002: the selected repair lands in src/ so that an installed wheel resolves its own "
     "schemas the way doctor already does, and so that the four compilers' unmodified stdout is "
     "accepted by validate without hand-editing or sidecar surgery."),
    ("REQ-PIPD-R5R-REGRESS-003", "P0", "PIPD-EC",
     "WO-R5R-REGRESS-003: regression tests pin both behaviours so they cannot silently return — each "
     "new test demonstrated failing against the pre-repair tree and passing after — and the full "
     "deterministic suite stays green."),
    ("REQ-PIPD-R5R-CODEXVERIFY-004", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R5R-CODEXVERIFY-004: independent verification is executed THROUGH THE CODEX CLI (not a Hermes "
     "subagent) on checker model GPT 6.1 SOL-MEDIUM via OpenAI OAuth, in a separate CODEX_HOME and "
     "session, and it must (a) re-derive the repaired behaviour from the built artefact and (b) really "
     "install and really execute PIPD-LS-SP, recording the raw transcript and exit codes. The Maker "
     "does not sign its own final verdict."),
    ("REQ-PIPD-R5R-DOC-005", "P1", "DOCS-OWNER",
     "WO-R5R-DOC-005: the CE-1/CE-2 disclosure is advanced to the repaired state, stating on every "
     "public surface what is now fixed, what is still open, and what is deferred to a superseding "
     "release rather than rewriting the published tag."),
    ("REQ-PIPD-R5R-SURFACE-006", "P1", "GOVERNED-SURFACES",
     "WO-R5R-SURFACE-006: the KANBAN, SWARM, GSTACK and OPENSPEC surfaces are enabled for this round "
     "and their receipts (board id, swarm root, openspec change, stack readback) are recorded."),
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
    (args.out / "r5r_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2500])
    print("checkpoint:", json.dumps(result.get("checkpoint"), ensure_ascii=False, default=str)[:400])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
