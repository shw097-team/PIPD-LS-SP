#!/usr/bin/env python3
"""S4-R2 round: admit the four affected-only obligations through the HG-KSEOS typed lifecycle API
(no raw SQL, no direct state writes): requirement -> lease -> FROZEN -> TaskSpec -> WorkOrder.

The existing PIPD project is reused; no duplicate project is started. The writable_root is bound to
this round's candidate worktree so the admitted write-set matches where the writer actually works.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
CAND = Path("C:/Projects/Agent_Workspace/PIPD-postrelease-wt")
PID = "PIPD-LS-SP-20261008"
BASE_HEAD = "546bc2e978fc94635eda8999ca91a84737109070"
OUT = CAND / ".hgk/rounds/S4R2-20261011-affected-only/admission"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.spine import SharedSpine  # noqa: E402
from hg_kseos.errors import HGKError  # noqa: E402

REQS = [
    ("REQ-S4R2-DOC-001",
     "F1 F-S4R2-01 / F-S4R2-05 / F-S4R2-09: the front page must keep verifying exactly the "
     "artefacts it downloaded, must point at a REAL copy-paste-able compiler walk-through instead "
     "of placeholders, and must state the .1/.2 distribution-identity hazard with PEP 440 guidance.",
     "P1"),
    ("REQ-S4R2-WEB-002",
     "F1 F-S4R2-06: one versioned web mount pack with a dispatcher SKILL, references, a short "
     "starter prompt and a verifying MANIFEST.sha256, declaring native-skill eligibility and "
     "manual document/Knowledge fallback separately.",
     "P1"),
    ("REQ-S4R2-CONTRACT-003",
     "F1 F-S4R2-02/03/04 and the residual F-S4R2-NEW-01 found while reconciling: duplicate/typed/"
     "unknown profile axes stay refused, risk state stays honestly NOT_ASSESSED, the universal "
     "identity and PI trace fields stay typed, and the ProfileBinding contract fields the "
     "duplicate-axes decision rides on must themselves be typed.",
     "P1"),
    ("REQ-S4R2-SOURCE-004",
     "F1 F-S4R2-10: docs/NORMATIVE_SOURCE_MAP.md pins the external canonical SSOT as a derived "
     "view, plus a minimal replayable examples/self-bootstrap with a typed negative -- never a "
     "competing master copy and never the 16 MB skeleton imported into the runtime tree.",
     "P2"),
]

TESTS = {
    "REQ-S4R2-DOC-001": ["tests/test_postrelease_quickstart.py", "tests/test_wheel_distribution.py"],
    "REQ-S4R2-WEB-002": ["tests/test_postrelease_web_mount.py", "tests/test_web_pack.py"],
    "REQ-S4R2-CONTRACT-003": ["tests/test_postrelease_contract_hardening.py",
                              "tests/test_s4r2_affected_only.py",
                              "tests/test_ce_repair_regression.py",
                              "tests/test_s0_contracts.py"],
    "REQ-S4R2-SOURCE-004": ["tests/test_postrelease_selfbootstrap.py", "tests/test_s1_lite_slice.py"],
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    spine = SharedSpine(HGK / "var/shared-spine/hg-kseos.db", HGK / "src/hg_kseos/schema.sql")
    out: dict = {"project_id": PID, "candidate_root": str(CAND), "base_head": BASE_HEAD,
                 "round": "S4R2-20261011-affected-only", "requirements": []}

    for req_id, wording, priority in REQS:
        row: dict = {"requirement_id": req_id, "wording": wording, "priority": priority}
        try:
            spine.register_requirement(
                requirement_id=req_id,
                source_locator="project:%s:s4r2-affected-only-obligation" % PID,
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
        token = "TK-%s-S4R2" % req_id
        try:
            spine.acquire_lease(req_id, "lifecycle-planner", token, ttl_seconds=600)
            row["lease"] = "ACQUIRED"
        except HGKError as exc:
            row["lease"] = "LEASE(%s)" % exc
        try:
            spine.transition_requirement(
                req_id, "FROZEN", actor="lifecycle-planner", token=token,
                expected_version=0, evidence_ref="EV-%s" % req_id,
                idempotency_key="FRZ-%s-S4R2" % req_id,
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
            spine.create_workorder(wo_id, ts_id, writer="codex", worktree=CAND, base_head=BASE_HEAD)
            row["workorder"] = wo_id
        except HGKError as exc:
            row["workorder"] = "WO(%s)" % exc
        out["requirements"].append(row)

    try:
        out["acceptance_rows"] = spine.query_all(
            "SELECT acceptance_id,requirement_id,verdict FROM acceptances "
            "WHERE requirement_id LIKE 'REQ-S4R2-%'")
    except Exception as exc:  # pragma: no cover
        out["acceptance_rows"] = "ERR(%s)" % exc
    try:
        out["workorder_rows"] = spine.query_all(
            "SELECT workorder_id,taskspec_id,writer,base_head FROM workorders "
            "WHERE base_head=?", (BASE_HEAD,))
    except Exception as exc:  # pragma: no cover
        out["workorder_rows"] = "ERR(%s)" % exc

    (OUT / "S4R2_ADMISSION.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:3500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
