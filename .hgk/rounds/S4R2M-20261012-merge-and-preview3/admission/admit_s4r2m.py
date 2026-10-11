#!/usr/bin/env python3
"""S4R2M round: admit the four WorkOrders through the HG-KSEOS typed lifecycle API.

No raw SQL, no direct state writes, no duplicate project: the live PIPD project
`PIPD-LS-SP-20261008` is reused and only this round's four new obligations are admitted.
The writable_root is the round's own candidate worktree, so the admitted write-set names the
place the bounded writer actually works.

Idempotent: re-running re-reads what already exists instead of creating a second copy.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
CAND = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt")
ROUND = CAND / ".hgk/rounds/S4R2M-20261012-merge-and-preview3"
OUT = ROUND / "admission"
PID = "PIPD-LS-SP-20261008"
BASE_HEAD = "3f6c7dc52b73cfcba03dccbe576ade75bec1890d"
DB = HGK / "var/shared-spine/hg-kseos.db"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.spine import SharedSpine  # noqa: E402
from hg_kseos.errors import HGKError  # noqa: E402

REQS = [
    ("REQ-S4R2M-DOC-001",
     "WO-S4R2M-DOC-CAL-01: the front page must offer two explicit onboarding paths (CLI/headless "
     "harness vs Skills/document consumption) and must describe --root the way the shipped argparse "
     "surface really behaves, instead of the over-general `GLOBAL and must precede the subcommand`.",
     "P1"),
    ("REQ-S4R2M-VERIFY-002",
     "WO-S4R2M-FOCUSED-VERIFY-02: the frozen candidate must pass an isolated affected regression in a "
     "disposable writable clone while the read-only checker subject keeps identical bytes; 19 schemas "
     "and registry, 8 logical skill directories and 13 CLI commands stay an exact set.",
     "P1"),
    ("REQ-S4R2M-MERGE-003",
     "WO-S4R2M-MAIN-INTEGRATE-03: the approved candidate integrates into main only under owner "
     "approval and only through a non-rewriting fast-forward with a remote ref readback; preview.2 "
     "stays immutable and main is never described as if the published wheel already carried the repairs.",
     "P1"),
    ("REQ-S4R2M-PREVIEW3-004",
     "WO-S4R2M-PREVIEW3-OPTIONAL-04 (conditional): a new preview.3 distribution is built only if the "
     "owner selects it, with a PEP 440 version strictly greater than 0.1.0, a separately download-able "
     "mount pack, and an anonymous re-download readback.",
     "P2"),
]

TESTS = {
    "REQ-S4R2M-DOC-001": ["tests/test_s4r2m_docs_route.py", "tests/test_postrelease_quickstart.py",
                          "tests/test_first_run_examples.py"],
    "REQ-S4R2M-VERIFY-002": ["tests/test_s4r2_affected_only.py",
                             "tests/test_postrelease_contract_hardening.py",
                             "tests/test_postrelease_web_mount.py",
                             "tests/test_postrelease_selfbootstrap.py",
                             "tests/test_ce_repair_regression.py",
                             "tests/test_wheel_distribution.py"],
    "REQ-S4R2M-MERGE-003": ["tests/test_wheel_distribution.py",
                            "tests/test_postrelease_contract_hardening.py"],
    "REQ-S4R2M-PREVIEW3-004": ["tests/test_wheel_distribution.py"],
}


def ro_query(sql, params=()):
    con = sqlite3.connect("file:%s?mode=ro" % DB.as_posix(), uri=True)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(sql, params).fetchall()]
    finally:
        con.close()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    spine = SharedSpine(DB, HGK / "src/hg_kseos/schema.sql")
    out: dict = {"schema": "PIPD-S4R2M-ADMISSION/1", "project_id": PID,
                 "candidate_root": str(CAND), "base_head": BASE_HEAD,
                 "round": "S4R2M-20261012-merge-and-preview3", "requirements": []}

    for req_id, wording, priority in REQS:
        row: dict = {"requirement_id": req_id, "wording": wording, "priority": priority}
        try:
            spine.register_requirement(
                requirement_id=req_id,
                source_locator="project:%s:s4r2m-conditional-merge-obligation" % PID,
                wording=wording,
                acceptance_id="ACC-%s" % req_id,
                oracle="%s materialized with a raw receipt and an independent check" % req_id,
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture="obligation asserted without its workorder or receipt",
                priority=priority,
                project_id=PID,
            )
            row["register"] = "INSERTED"
        except HGKError as exc:
            row["register"] = "EXISTS(%s)" % exc
        token = "TK-%s-S4R2M" % req_id
        try:
            spine.acquire_lease(req_id, "lifecycle-planner", token, ttl_seconds=900)
            row["lease"] = "ACQUIRED"
        except HGKError as exc:
            row["lease"] = "LEASE(%s)" % exc
        try:
            spine.transition_requirement(
                req_id, "FROZEN", actor="lifecycle-planner", token=token,
                expected_version=0, evidence_ref="EV-%s" % req_id,
                idempotency_key="FRZ-%s-S4R2M" % req_id,
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
                owner="PIPD-LS-SP 開發實作指揮官",
                writable_root=CAND,
                permissions={"write_scope": "admitted_candidate_worktree",
                             "network": "loopback_only", "candidate_only": True},
                tests=TESTS[req_id],
                evidence_plan="raw stdout/stderr/exit + subject-bound manifest per the accepted contract",
            )
            row["taskspec"] = ts_id
        except HGKError as exc:
            row["taskspec"] = "TS(%s)" % exc
        wo_id = "WO-%s-%s" % (ts_id.upper().replace("TS-", ""), REQS.index((req_id, wording, priority)) + 1)
        row["workorder"] = wo_id
        try:
            spine.create_workorder(wo_id, ts_id, writer="codex", worktree=CAND, base_head=BASE_HEAD)
            row["workorder_create"] = "CREATED"
        except HGKError as exc:
            row["workorder_create"] = "WO(%s)" % exc
        out["requirements"].append(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
