#!/usr/bin/env python3
"""Admit the R8 (cross-model verification + main-page consolidation + repo hygiene) obligations.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as R5P/R5Q/R5R/R7:
project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound admit_requirement calls.
New requirement ids (R8) keep every earlier row untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R8-XMODEL-001", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R8-XMODEL-001: replace the same-model independent check of the published v0.1.0-preview.2 with "
     "a CROSS-MODEL check on the CODEX CLI VERIFY lane (checker model gpt-6.1-sol, medium, OpenAI "
     "OAuth), re-deriving the SAME anonymous evidence: ref resolution, release metadata, every asset "
     "hash against SHA256SUMS, and the two repaired behaviours exercised on the DOWNLOADED wheel from a "
     "cwd with no schemas dir and no --root. The maker cannot sign its own verdict, and the receipt must "
     "state what the checker could not verify."),
    ("REQ-PIPD-R8-MAIN-002", "P0", "DOCS-OWNER",
     "WO-R8-MAIN-002: bring the repaired line to the default branch - merge the release lineage into "
     "main so the published preview.2 subject is reachable from the default branch tip - then point the "
     "main front page at the successor preview and add a copy-pasteable quickstart that works from the "
     "published bytes alone. main must not be force-pushed or rewritten; the merge must be a "
     "fast-forward or an honest merge commit, and the pre-existing tag must not move."),
    ("REQ-PIPD-R8-HYGIENE-003", "P1", "DOCS-OWNER",
     "WO-R8-HYGIENE-003: repository hygiene - make the default branch's front page, README and branch "
     "set honest and clean. Branches that are round scaffolding rather than release lineage are to be "
     "classified and, where removal is safe and reversible, removed; nothing that carries unique "
     "history or an unmoved tag may be deleted, and any deletion must name what would be lost."),
    ("REQ-PIPD-R8-FAR-004", "P0", "DOCS-OWNER",
     "WO-R8-FAR-004: FAR studies over (a) merging preview.2 into main with a README front-page pointer "
     "and a quickstart, and (b) repository hygiene across the front page, README and branches - each "
     "proposing the lowest-friction engineering option and executing it - plus a closing report that "
     "states the S4 MVP open-source release claim ceiling and every item that remains open."),
    ("REQ-PIPD-R8-CRED-005", "P0", "CREDENTIAL-BROKER",
     "WO-R8-CREDENTIAL-005: the owner token is read only inside process memory from the credential "
     "file, used for the minimum-scope push this round requires, and is never emitted to argv, stdout, "
     "logs, prompt, evidence, git config, remote URL or any release asset."),
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
    (args.out / "r8_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
