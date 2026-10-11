#!/usr/bin/env python3
"""POSTRELEASE round: admit the four late-bound repair obligations through the
HG-KSEOS typed lifecycle API (no raw SQL, no direct state writes).

Requirement -> FROZEN -> TaskSpec -> WorkOrder, six per WorkOrder, exactly as
`ProjectLifecycleController.admit_requirement` does -- but with the writable_root
bound to this round's admitted candidate worktree instead of a repo-relative
default, so the admitted write-set matches where the writer actually works.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
CAND = Path("C:/Projects/Agent_Workspace/PIPD-postrelease-wt")
PID = "PIPD-LS-SP-20261008"
BASE_HEAD = "4445db5a6d1b3138946fd7c4fe3b712e4faf1af7"
OUT = CAND / ".hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/admission"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.spine import SharedSpine  # noqa: E402
from hg_kseos.errors import HGKError  # noqa: E402

REQS = [
    ("REQ-S4POST-UX-001",
     "F0 Gate P1 / F1 POST-F01/F08: the published README quickstart must verify exactly the "
     "artefacts it downloaded, and must ship a copy-paste PowerShell branch, so a first-time "
     "user's verbatim copy-paste exits 0.",
     "P1"),
    ("REQ-S4POST-WEB-002",
     "F0 Gate P2 / F1 POST-F05: publish one versioned ChatGPT/Web mount package (short dispatcher "
     "SKILL, references, starter prompt, MANIFEST.sha256) with a five-case consumer UAT that "
     "separates native upload from manual attachment fallback.",
     "P1"),
    ("REQ-S4POST-CONTRACT-003",
     "F0 Gate P3 / F1 POST-F02/F03/F04: identity fields subject_id/version/content_hash/"
     "schema_version must carry a JSON type, PI trace must be an array of TraceLink, and the "
     "profile path must fail closed on duplicate/typed/unknown axes and declare risk_assessment="
     "NOT_ASSESSED rather than implying a risk score it never computed.",
     "P1"),
    ("REQ-S4POST-SELFBOOT-004",
     "F0 Gate P4 / F1 POST-F06: publish docs/NORMATIVE_SOURCE_MAP.md pinning the external "
     "canonical SSOT, plus a minimal replayable examples/self-bootstrap with a source-missing "
     "negative -- a derived view, never a competing master copy.",
     "P2"),
]

TESTS = {
    "REQ-S4POST-UX-001": ["tests/test_postrelease_quickstart.py",
                          "tests/test_wheel_distribution.py"],
    "REQ-S4POST-WEB-002": ["tests/test_postrelease_web_mount.py", "tests/test_web_pack.py"],
    "REQ-S4POST-CONTRACT-003": ["tests/test_postrelease_contract_hardening.py",
                                "tests/test_ce_repair_regression.py",
                                "tests/test_s0_contracts.py"],
    "REQ-S4POST-SELFBOOT-004": ["tests/test_postrelease_selfbootstrap.py",
                                "tests/test_s1_lite_slice.py"],
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    spine = SharedSpine(HGK / "var/shared-spine/hg-kseos.db", HGK / "src/hg_kseos/schema.sql")
    out: dict = {"project_id": PID, "candidate_root": str(CAND), "base_head": BASE_HEAD,
                 "requirements": [], "events": []}

    for req_id, wording, priority in REQS:
        row = {"requirement_id": req_id, "wording": wording, "priority": priority}
        existing = spine.query_one(
            "SELECT state,version FROM requirements WHERE requirement_id=?", (req_id,)) \
            if hasattr(spine, "query_one") else None
        try:
            spine.register_requirement(
                requirement_id=req_id,
                source_locator="project:%s:postrelease-late-bound-obligation" % PID,
                wording=wording,
                acceptance_id="ACC-%s" % req_id,
                oracle="%s materialized + acceptance PASS" % req_id,
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture="obligation without workorder",
                priority=priority,
                project_id=PID,
            )
            row["register"] = "INSERTED"
        except HGKError as exc:
            row["register"] = "EXISTS(%s)" % exc
        token = "TK-%s-POSTREL" % req_id
        try:
            spine.acquire_lease(req_id, "lifecycle-planner", token, ttl_seconds=600)
            row["lease"] = "ACQUIRED"
        except HGKError as exc:
            row["lease"] = "LEASE(%s)" % exc
        try:
            spine.transition_requirement(
                req_id, "FROZEN", actor="lifecycle-planner", token=token,
                expected_version=0, evidence_ref="EV-%s" % req_id,
                idempotency_key="FRZ-%s-POSTREL" % req_id,
            )
            row["freeze"] = "FROZEN"
        except HGKError as exc:
            row["freeze"] = "FREEZE(%s)" % exc
        finally:
            try:
                spine.release_lease(req_id, "lifecycle-planner", token)
            except HGKError:
                pass
        ts_id = "TS-%s" % req_id.lower()
        try:
            spine.create_taskspec(
                taskspec_id=ts_id, requirement_id=req_id, objective=wording,
                owner="PIPD-LS-SP_開發實作指揮官",
                writable_root=CAND,
                permissions={"write_scope": "admitted_candidate_worktree",
                             "network": "loopback_only", "candidate_only": True},
                tests=TESTS[req_id],
                evidence_plan="raw stdout/stderr/exit + subject-bound manifest per acceptance contract",
            )
            row["taskspec"] = ts_id
        except HGKError as exc:
            row["taskspec"] = "TS(%s)" % exc
        wo_id = "WO-%s" % ts_id
        try:
            spine.create_workorder(wo_id, ts_id, writer="codex",
                                   worktree=CAND, base_head=BASE_HEAD)
            row["workorder"] = wo_id
        except HGKError as exc:
            row["workorder"] = "WO(%s)" % exc
        out["requirements"].append(row)

    try:
        out["acceptance_rows"] = spine.query_all(
            "SELECT acceptance_id,requirement_id,verdict FROM acceptances "
            "WHERE requirement_id LIKE 'REQ-S4POST-%'")
    except Exception as exc:  # pragma: no cover
        out["acceptance_rows"] = "ERR(%s)" % exc
    (OUT / "S4POST_ADMISSION.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
