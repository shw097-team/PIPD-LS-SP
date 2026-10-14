#!/usr/bin/env python3
"""Admit the closure-and-handover round (FAR round 3) into the HG-KSEOS Shared Spine.

The requirement wording carries the alignment premise by path and the four normative rules that shape a
closure: TT closure needs owner+checker evidence (PKG-06 DOC-05), a supersession needs old/new hash plus a
predecessor link (PKG-09 DOC-01), invalidation is affected-only and never deletion (PKG-09 DOC-03),
evidence needs the full envelope (PKG-06 DOC-04). It also records the owner's execution authorisation and
the ceiling that survives it: no self-promotion, no ADMIT, no merge, tag, release or PASS.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROUND_REL = ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
KB = ("知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_PIPD-PKG")


def git_head(path: str) -> str:
    return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()


def specs(round_dir: str, base_head: str) -> list[dict]:
    exec_wording = (
        "Close out and hand over this session's implementation and evidence, aligned to the governing "
        f"corpus at {KB} as the highest premise. The closure must satisfy the corpus's own rules rather "
        "than invent a process: (i) each finding or TT may advance along "
        "OPEN->ASSIGNED->PATCHED->CHECK_PENDING->CLOSED and no further, with owner evidence AND "
        "checker evidence carried, because CLOSED without a checker is the named first failure "
        "TT_CLOSURE_WITHOUT_CHECKER; (ii) every superseded revision is recorded with old_id, new_id, "
        "old_hash, new_hash and supercession_ref such that old_hash != new_hash and predecessor "
        "matches; (iii) invalidation is affected-only - the reverse closure of the superseded node is "
        "marked SUPERSEDED/INVALIDATED and nothing is deleted, and where no output delta can be proven "
        "the conservative branch is taken; (iv) every evidence item carries the full envelope "
        "(source_file, sha256, version, exact_anchor, observed_at, supersedes_hash plus subject, env, "
        "epoch, freshness). Deliverables: a closure disposition for every pending item that names the "
        "next legal state, its owner, the artifact each next state requires and the first failure code "
        "for skipping it; the supersession ledger; the affected-only invalidation; the evidence "
        "envelope; and a receiver handoff bundle shaped for the HGK receiver. The owner authorises "
        "execution of this closure, which is an authorisation to act and NOT an authorisation to "
        "promote: P0-P2 must not be raised to P3-P5 by text, no admission receipt may be asserted, and "
        "no merge, tag, release or PASS may be granted. Where a normative input is absent (no external "
        "qualification issuer, no ADMIT receipt, no human token) record AWAITING_EXTERNAL rather than "
        "supplying a value.")
    verify_wording = (
        "Independently audit the closure and handover artifacts as carried in a bundle: whether a "
        "supersession entry's hashes and predecessor link are internally consistent with its own "
        "recorded values, whether the affected-only set is consistent with the citations the bundle "
        "carries, whether any claim has silently advanced a state without the evidence that state "
        "requires, and whether the handoff bundle avoids asserting an admission or a PASS. The "
        "executor's prose is a claim. Name every item the bundle does not let you settle.")
    return [
        dict(requirement_id="REQ-S4R3FAR3-CLOSURE-HANDOVER-001", priority="P1",
             owner="FAR3-CLOSURE-EXECUTE", writer="codex",
             writable_root=round_dir, base_head=base_head, objective=exec_wording,
             tests=["every pending item names its next legal state and the artifact that state requires",
                    "no state is advanced without the evidence that state requires",
                    "superseded revisions are recorded and nothing is deleted"],
             evidence_plan=f"{ROUND_REL}/evidence/12_GATES/CLOSURE_*.json plus the handoff bundle"),
        dict(requirement_id="REQ-S4R3FAR3-CLOSURE-VERIFY-002", priority="P1",
             owner="EXTERNAL-VERIFY-LANE", writer="codex-cli-verify-lane",
             writable_root=round_dir, base_head=base_head, objective=verify_wording,
             tests=["the supersession invariant is recomputed from the carried values",
                    "the affected-only set is checked against the carried citations",
                    "no admission or PASS is asserted anywhere in the bundle"],
             evidence_plan=f"{ROUND_REL}/far-study/rem3/verify/"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hgk-root", required=True, type=Path)
    ap.add_argument("--b-worktree", required=True)
    ap.add_argument("--project-id", default="PIPD-LS-SP-20261008")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    sys.path.insert(0, str(args.hgk_root / "src"))
    from hg_kseos.spine import SharedSpine
    from hg_kseos.lifecycle import ProjectLifecycleController

    base_head = git_head(args.b_worktree)
    round_dir = f"{args.b_worktree}/{ROUND_REL}"
    spine = SharedSpine(args.hgk_root / "var/shared-spine/hg-kseos.db",
                        args.hgk_root / "src/hg_kseos/schema.sql")
    lc = ProjectLifecycleController(spine)
    args.out.mkdir(parents=True, exist_ok=True)
    result: dict = {"step": "s4r3_far3_closure_admission", "base_head_at_admission": base_head,
                    "admitted": [], "errors": []}
    for spec in specs(round_dir, base_head):
        rid = spec["requirement_id"]
        ts_id, wo_id = f"TS-{rid.lower()}", f"WO-TS-{rid.lower()}"
        try:
            spine.register_requirement(
                requirement_id=rid, source_locator=f"project:{args.project_id}:closure-handover-order",
                wording=spec["objective"], acceptance_id=f"ACC-{rid}",
                oracle=f"{spec['objective'][:80]} ... materialized + acceptance PASS",
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture=f"closure {rid} claimed with a state advanced past its evidence",
                priority=spec["priority"], project_id=args.project_id)
            spine.acquire_lease(rid, "lifecycle-planner", f"TK-{rid}", ttl_seconds=300)
            try:
                spine.transition_requirement(rid, "FROZEN", actor="lifecycle-planner",
                                             token=f"TK-{rid}", expected_version=0,
                                             evidence_ref=f"EV-{rid}", idempotency_key=f"FRZ3-{rid}")
            finally:
                spine.release_lease(rid, "lifecycle-planner", f"TK-{rid}")
            spine.create_taskspec(
                taskspec_id=ts_id, requirement_id=rid, objective=spec["objective"], owner=spec["owner"],
                writable_root=Path(spec["writable_root"]),
                permissions={"write_scope": "declared_root_only", "network": "none",
                             "remote_push_merge": "FORBIDDEN",
                             "declared_root": spec["writable_root"]},
                tests=spec["tests"], evidence_plan=spec["evidence_plan"])
            spine.create_workorder(wo_id, ts_id, writer=spec["writer"],
                                   worktree=Path(spec["writable_root"]), base_head=spec["base_head"])
            result["admitted"].append({"requirement_id": rid, "taskspec": ts_id, "workorder": wo_id,
                                       "writer": spec["writer"], "base_head": spec["base_head"]})
        except Exception as exc:  # noqa: BLE001
            result["errors"].append({"requirement_id": rid, "error": f"{type(exc).__name__}: {exc}"})
    with spine.connect() as conn:
        rb = {"requirements": [], "taskspecs": [], "workorders": []}
        for spec in specs(round_dir, base_head):
            rid = spec["requirement_id"]
            ts_id, wo_id = f"TS-{rid.lower()}", f"WO-TS-{rid.lower()}"
            r = conn.execute("select state from requirements where requirement_id=?", (rid,)).fetchone()
            t = conn.execute("select state,owner from taskspecs where taskspec_id=?", (ts_id,)).fetchone()
            w = conn.execute("select state,writer,base_head from workorders where workorder_id=?",
                             (wo_id,)).fetchone()
            rb["requirements"].append({"id": rid, "state": r[0] if r else None})
            rb["taskspecs"].append({"id": ts_id, "state": t[0] if t else None, "owner": t[1] if t else None})
            rb["workorders"].append({"id": wo_id, "state": w[0] if w else None,
                                     "writer": w[1] if w else None, "base_head": w[2] if w else None})
        rb["total_workorders"] = conn.execute("select count(*) from workorders").fetchone()[0]
    result["readback"] = rb
    result["readback_ok"] = (all(x["state"] == "FROZEN" for x in rb["requirements"])
                             and all(x["state"] == "ADMITTED" for x in rb["taskspecs"])
                             and all(x["state"] == "CREATED" for x in rb["workorders"]))
    result["status_after"] = lc.status(args.project_id)
    (args.out / "far3_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"admitted": len(result["admitted"]), "errors": result["errors"],
                      "readback_ok": result["readback_ok"], "base_head": base_head,
                      "total_workorders": rb["total_workorders"]}, ensure_ascii=False, indent=1, default=str))
    return 0 if (not result["errors"] and result["readback_ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
