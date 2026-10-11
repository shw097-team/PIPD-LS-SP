#!/usr/bin/env python3
"""Admit the R5Q (Owner Open Source Preview) obligations into the HG-KSEOS lifecycle.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same pattern as the
R5P round's hgk_r5p_admission.py: project PIPD-LS-SP-20261008 is already EXECUTING, so these
are late-bound admit_requirement calls. New requirement ids (R5Q) keep R5/R5P rows untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

OBLIGATIONS = [
    ("REQ-PIPD-R5Q-LIC-001", "P0", "OWNER+LICENSE-FAR",
     "WO-R5Q-LICENSE-001: the owner's open-source grant lands as a single SPDX identifier across "
     "LICENSE, OWNER_LICENSE_DECISION.yaml, NOTICE, pyproject.toml, SBOM.cdx.json and PROVENANCE.md, "
     "keeping the corpus-derived vs agent-authored split; historical non-grant receipts stay "
     "byte-identical and no right the owner does not hold is asserted."),
    ("REQ-PIPD-R5Q-PKG-002", "P0", "PIPD-EC",
     "WO-R5Q-REBUILD-002: the distribution is rebuilt from the frozen release candidate so the shipped "
     "wheel carries the granted SPDX metadata; wheel sha256, WHEEL_MANIFEST build_input_commit/"
     "released_commit and SHA256SUMS are recomputed and the superseded bb070a6f identity is not reused."),
    ("REQ-PIPD-R5Q-UAT-003", "P0", "PIPD-EC",
     "WO-R5Q-UAT-003: clean-venv, no PYTHONPATH, outside the repository, against the ACTUAL released "
     "wheel bytes: doctor positive plus missing-schema typed negative, 19-schema readback, the "
     "intake/compile-pi/bind-pd/compile-ecp/compile-tqaep design chain, validate, project --dry-run with "
     "zero writes, project --out to disposable scratch (5 Web + 3 Host + IR) and export --out with "
     "recomputed archive/manifest/SHA256SUMS."),
    ("REQ-PIPD-R5Q-CRED-004", "P0", "CREDENTIAL-BROKER",
     "WO-R5Q-CREDENTIAL-004: the owner PAT is read only inside process memory from the credential file, "
     "used for a minimum-scope probe of shw097-team/PIPD-LS-SP, and never emitted to argv, stdout, logs, "
     "prompt, evidence, git config or any release asset."),
    ("REQ-PIPD-R5Q-PUB-005", "P0", "RELEASE-OWNER",
     "WO-R5Q-GITHUB-005: an immutable tag and a GitHub prerelease are published against the explicit "
     "release commit with the source archive, the wheel and SHA256SUMS, after proving the tag does not "
     "already exist; main is not overwritten and no existing tag is moved."),
    ("REQ-PIPD-R5Q-AO-006", "P0", "EXTERNAL-VERIFY-LANE",
     "WO-R5Q-AO-006: an independent non-Maker checker in a separate read-only process re-derives the "
     "POST-release subject from the published bytes (download hash match, clean install, doctor, design "
     "chain, license coverage) and the Maker cannot sign its own final verdict."),
    ("REQ-PIPD-R5Q-DOC-007", "P1", "DOCS-OWNER",
     "WO-R5Q-DOC-007: README first screen, Preview Notes and Known Limitations point at the preview tag "
     "rather than the historical R3 main and disclose DEL-018 exit 1 with its three uncovered test paths, "
     "the 12 TT dispositions, CORR-01..08 and the 28/10/19 SPEC/DEL denominator."),
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
    (args.out / "r5q_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2500])
    print("checkpoint:", json.dumps(result.get("checkpoint"), ensure_ascii=False, default=str)[:400])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
