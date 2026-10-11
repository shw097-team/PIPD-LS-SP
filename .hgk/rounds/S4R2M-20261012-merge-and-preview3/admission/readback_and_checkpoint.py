#!/usr/bin/env python3
"""S4R2M HGK readback + checkpoint.

The readback is a READ-ONLY sqlite query against the shared spine (no state write). The checkpoint
is created through the typed lifecycle API. Nothing here writes product code.
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
    out: dict = {"schema": "PIPD-S4R2M-ADMISSION-READBACK/1", "project_id": PID,
                 "db": str(DB), "read_only_query": True, "round": "S4R2M-20261012-merge-and-preview3"}
    out["project"] = ro_query("SELECT project_id,state FROM projects WHERE project_id=?", (PID,))
    out["lifecycle"] = ro_query(
        "SELECT project_id,state,updated_at FROM project_lifecycles WHERE project_id=?", (PID,))
    out["requirements"] = ro_query(
        "SELECT requirement_id,state,priority,acceptance_id,project_id FROM requirements "
        "WHERE requirement_id LIKE 'REQ-S4R2M-%' ORDER BY requirement_id")
    out["taskspecs"] = ro_query(
        "SELECT taskspec_id,requirement_id,owner,writable_root FROM taskspecs "
        "WHERE taskspec_id LIKE 'TS-req-s4r2m-%' ORDER BY taskspec_id")
    out["workorders"] = ro_query(
        "SELECT workorder_id,taskspec_id,writer,base_head,worktree FROM workorders "
        "WHERE workorder_id LIKE 'WO-REQ-S4R2M-%' ORDER BY workorder_id")
    try:
        out["acceptances"] = ro_query(
            "SELECT acceptance_id,requirement_id,verdict FROM acceptances "
            "WHERE requirement_id LIKE 'REQ-S4R2M-%' ORDER BY acceptance_id")
    except sqlite3.Error as exc:
        out["acceptances"] = "ERR(%s)" % exc
    out["leases_remaining"] = ro_query(
        "SELECT resource_id,holder,expires_at FROM leases WHERE resource_id LIKE 'REQ-S4R2M-%'")

    # The admitted write-set must name the worktree the writer will actually use.
    roots = {r.get("writable_root") for r in out["taskspecs"] if isinstance(r, dict)}
    out["writable_root_matches_candidate"] = bool(roots) and roots == {str(CAND)}
    wts = {r.get("worktree") for r in out["workorders"] if isinstance(r, dict)}
    out["workorder_worktree_matches_candidate"] = bool(wts) and wts == {str(CAND)}

    try:
        from hg_kseos.spine import SharedSpine
        from hg_kseos.lifecycle import ProjectLifecycleController
        spine = SharedSpine(DB, HGK / "src/hg_kseos/schema.sql")
        lc = ProjectLifecycleController(spine)
        cp = lc.checkpoint(PID, evidence_refs=[
            "S4R2M.CONTRACT.json", "S4R2M_COMPILER_READBACK.json",
            "S4R2M.lint.receipt.json", "S4R2M.activation.receipt.json",
            "S4R2M.acceptance.receipt.json", "S4R2M.compile.receipt.json",
        ])
        out["checkpoint"] = cp
    except Exception as exc:  # noqa: BLE001
        out["checkpoint"] = "ERR(%s: %s)" % (type(exc).__name__, exc)

    (OUT / "S4R2M_ADMISSION_READBACK.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
