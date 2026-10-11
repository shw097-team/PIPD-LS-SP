#!/usr/bin/env python3
"""Admit the R7 (DEL-018 closure + successor preview) obligations into the HG-KSEOS lifecycle.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as the R5Q and
R5P rounds: project PIPD-LS-SP-20261008 is already EXECUTING, so these are late-bound
admit_requirement calls. New requirement ids (R7) keep every earlier R5/R5P/R5Q/R5R row untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R7-DEL018-001", "P0", "PIPD-EC",
     "WO-R7-DEL018-001: close DEL-018 RELEASE_MANIFEST@1 by regenerating the evidence manifest and "
     "its seal and rebuilding the publication projection against the current candidate, binding the "
     "new commit/tree, so that build_publication_manifest.py --check --current exits 0 with every "
     "current-tree product path dispositioned. The closure must prove it is NOT a coverage reduction: "
     "every entry dropped relative to the superseded manifest must be shown to be a stale path that no "
     "longer exists, and no product path may be dropped. The manifest/seal/projection are evidence "
     "surfaces only - no runtime, schema, CLI or wheel byte may change."),
    ("REQ-PIPD-R7-SEC-002", "P0", "SECURITY",
     "WO-R7-SECURITY-002: scan the release candidate for secret/PII exposure and for known "
     "vulnerabilities - the repository's own history secret scan and deny-list scan over the tree, a "
     "dependency vulnerability scan of the declared dependency closure in a throwaway environment, and "
     "the repository-native publication attestation built and verified against the local git objects. "
     "Findings are reported with severity and disposition; anything that cannot be scanned is named as "
     "unscanned rather than implied clean."),
    ("REQ-PIPD-R7-REL-003", "P0", "RELEASE-OWNER",
     "WO-R7-RELEASE-003: issue a SUCCESSOR immutable tag and GitHub prerelease carrying the CE-1/CE-2 "
     "repair, under the owner grant already on record (action create_new_immutable_tag_and_prerelease, "
     "target an explicit release commit, prerelease true). main is not overwritten, no force-push, no "
     "existing tag is moved or deleted, and the published wheel bytes must be shown to contain the "
     "repair. Published object hashes are re-downloaded and recomputed by a separate step."),
    ("REQ-PIPD-R7-VER-004", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R7-VERIFY-004: an independent non-Maker checker in a separate process re-derives the "
     "POST-release subject from the published bytes (tag resolves, asset hashes match, clean install, "
     "the repaired behaviour holds on the installed wheel) and reports its own verdict. The Maker "
     "cannot sign its own final verdict and the checker's model attribution is limited to what its own "
     "transcript can carry."),
    ("REQ-PIPD-R7-FAR-005", "P1", "DOCS-OWNER",
     "WO-R7-FAR-005: produce the adjudication study over the three candidate paths and the final "
     "closure research report stating whether every known gap/defect/bug is repaired and closed, with "
     "an explicit claim ceiling and an explicit list of what remains open, unscanned or unverifiable."),
    ("REQ-PIPD-R7-CRED-006", "P0", "CREDENTIAL-BROKER",
     "WO-R7-CREDENTIAL-006: the owner token is read only inside process memory from the credential "
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
    (args.out / "r7_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2500])
    print("checkpoint:", json.dumps(result.get("checkpoint"), ensure_ascii=False, default=str)[:400])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
