#!/usr/bin/env python3
"""S4-R2 HGK readback + checkpoint.

Readback is a READ-ONLY sqlite query against the shared spine (no state write). The checkpoint is
created through the typed lifecycle API.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
CAND = Path("C:/Projects/Agent_Workspace/PIPD-postrelease-wt")
PID = "PIPD-LS-SP-20261008"
BASE_HEAD = "546bc2e978fc94635eda8999ca91a84737109070"
OUT = CAND / ".hgk/rounds/S4R2-20261011-affected-only/admission"
DB = HGK / "var/shared-spine/hg-kseos.db"

sys.path.insert(0, str(HGK / "src"))


def ro_query(sql, params=()):
    con = sqlite3.connect("file:%s?mode=ro" % DB.as_posix(), uri=True)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(sql, params).fetchall()]
    finally:
        con.close()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    out: dict = {"schema": "PIPD-S4R2-ADMISSION-READBACK/1", "project_id": PID,
                 "base_head": BASE_HEAD, "db": str(DB), "read_only_query": True}

    out["requirements"] = ro_query(
        "SELECT requirement_id,state,priority,acceptance_id,project_id FROM requirements "
        "WHERE requirement_id LIKE 'REQ-S4R2-%' ORDER BY requirement_id")
    out["taskspecs"] = ro_query(
        "SELECT taskspec_id,requirement_id,owner,writable_root FROM taskspecs "
        "WHERE taskspec_id LIKE 'TS-req-s4r2-%' ORDER BY taskspec_id")
    out["workorders"] = ro_query(
        "SELECT workorder_id,taskspec_id,writer,base_head,worktree FROM workorders "
        "WHERE workorder_id LIKE 'WO-TS-req-s4r2-%' ORDER BY workorder_id")
    try:
        out["acceptances"] = ro_query(
            "SELECT acceptance_id,requirement_id,verdict FROM acceptances "
            "WHERE requirement_id LIKE 'REQ-S4R2-%' ORDER BY acceptance_id")
    except sqlite3.Error as exc:
        out["acceptances"] = "ERR(%s)" % exc

    # cross-check: this round's base head really is the previous candidate tip
    out["base_head_matches_previous_candidate_tip"] = bool(ro_query(
        "SELECT 1 FROM workorders WHERE base_head=? AND workorder_id LIKE 'WO-TS-req-s4r2-%' LIMIT 1",
        (BASE_HEAD,)))

    # checkpoint through the typed lifecycle API
    try:
        from hg_kseos.spine import SharedSpine
        from hg_kseos.lifecycle import ProjectLifecycleController
        spine = SharedSpine(HGK / "var/shared-spine/hg-kseos.db", HGK / "src/hg_kseos/schema.sql")
        lc = ProjectLifecycleController(spine)
        cp = lc.checkpoint(PID, evidence_refs=[
            "S4R2.CONTRACT.json", "S4R2_COMPILER_RECEIPT.json", "S4R2_ADMISSION.json",
            "RECONCILIATION_FRESH_EVIDENCE.json", "FINDING_DISPOSITION_MATRIX.json",
        ])
        out["checkpoint"] = cp
    except Exception as exc:  # noqa: BLE001
        out["checkpoint"] = "ERR(%s: %s)" % (type(exc).__name__, exc)

    (OUT / "S4R2_ADMISSION_READBACK.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:3200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
