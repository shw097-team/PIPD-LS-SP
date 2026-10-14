#!/usr/bin/env python3
"""Admit FAR round 2 (the F1 allowlist remediation) into the HG-KSEOS Shared Spine.

Typed SharedSpine API only; the base head is read inside this process because `create_workorder`
validates only that base_head is non-empty, so a placeholder passes silently and no update API exists to
correct it afterwards.

The user's order of 2026-10-13 pre-authorises executing this round's recommended remedy, so the
requirement wording records that authorisation AND the two constraints that survive it: no oracle
relaxation, and the stacked invariant must be restored if a candidate head is edited. An authorisation
to act is not an authorisation to relax a check.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROUND_REL = ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
FAR_REL = f"{ROUND_REL}/far-study"


def git_head(path: str) -> str:
    return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def specs(round_dir: str, base_head: str) -> list[dict]:
    exec_wording = (
        "Remediate the S4R3 write-set allowlist finding, executing the remedy the FAR study ranks best. "
        "Constraints that bind regardless of the owner's execution authorisation: (i) no oracle, "
        "threshold, validator, guard, exit code or denominator may be relaxed to reach a green; (ii) a "
        "remedy must be measured against the gate's own governed diff, not argued in prose; (iii) if a "
        "candidate head is edited, the stacked invariant must be restored so that the merge-base of the "
        "Stage B branch and the Stage A branch equals the Stage A head, and the affected receipts must "
        "be re-cut at the new revision; (iv) the round's own claims must be re-verified at the new "
        "revision rather than carried over from the superseded one. Deliver: the recommendation among "
        "keep-and-correct / narrow-by-declaration / declared-deviation, the exact edit per branch copy, "
        "the re-run and re-cut list with what each re-run would falsify, and the DO-NOT list.")
    verify_wording = (
        "Independently audit the FAR round 2 remedy and its receipts as carried in a bundle. The "
        "executor's claims are CLAIMS, not evidence. Judge only the blocks the bundle carries: whether "
        "the edit shown removes the entries it says it removes and adds none, whether the gate's "
        "self-tests still refuse a planted product violation under the new logic, whether the exclusion "
        "is printed where a reviewer can see it, and whether the re-cut receipts name the revision they "
        "were produced at. Name every claim the bundle does not let you settle, and say what block would "
        "settle it. Do not accept a restatement as re-derivation.")
    return [
        dict(requirement_id="REQ-S4R3FAR2-F1-REMEDIATE-001", priority="P1",
             owner="FAR2-REMEDIATE-EXECUTE", writer="codex",
             writable_root=round_dir, base_head=base_head, objective=exec_wording,
             tests=["the remedy's effect is measured against the governed diff, not asserted",
                    "no allowlist entry is added anywhere",
                    "the stacked invariant is measured after any candidate edit"],
             evidence_plan=f"{FAR_REL}/rem2/ plus evidence/12_GATES receipts re-cut at the new revision"),
        dict(requirement_id="REQ-S4R3FAR2-REMEDIATE-VERIFY-002", priority="P1",
             owner="EXTERNAL-VERIFY-LANE", writer="codex-cli-verify-lane",
             writable_root=round_dir, base_head=base_head, objective=verify_wording,
             tests=["the entry-level before/after sets are recomputed from the blocks",
                    "a planted product violation is shown still refused",
                    "each cited receipt is shown to name its revision"],
             evidence_plan=f"{FAR_REL}/rem2/verify/"),
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

    result: dict = {"step": "s4r3_far2_admission", "base_head_at_admission": base_head,
                    "admitted": [], "errors": []}
    for spec in specs(round_dir, base_head):
        rid = spec["requirement_id"]
        ts_id, wo_id = f"TS-{rid.lower()}", f"WO-TS-{rid.lower()}"
        try:
            spine.register_requirement(
                requirement_id=rid, source_locator=f"project:{args.project_id}:far2-remediation-order",
                wording=spec["objective"], acceptance_id=f"ACC-{rid}",
                oracle=f"{spec['objective'][:80]} ... materialized + acceptance PASS",
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture=f"remedy {rid} claimed without a re-cut receipt",
                priority=spec["priority"], project_id=args.project_id)
            spine.acquire_lease(rid, "lifecycle-planner", f"TK-{rid}", ttl_seconds=300)
            try:
                spine.transition_requirement(rid, "FROZEN", actor="lifecycle-planner",
                                             token=f"TK-{rid}", expected_version=0,
                                             evidence_ref=f"EV-{rid}", idempotency_key=f"FRZ-{rid}")
            finally:
                spine.release_lease(rid, "lifecycle-planner", f"TK-{rid}")
            spine.create_taskspec(
                taskspec_id=ts_id, requirement_id=rid, objective=spec["objective"],
                owner=spec["owner"], writable_root=Path(spec["writable_root"]),
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
            rb["taskspecs"].append({"id": ts_id, "state": t[0] if t else None,
                                    "owner": t[1] if t else None})
            rb["workorders"].append({"id": wo_id, "state": w[0] if w else None,
                                     "writer": w[1] if w else None, "base_head": w[2] if w else None})
    result["readback"] = rb
    result["readback_ok"] = (all(x["state"] == "FROZEN" for x in rb["requirements"])
                             and all(x["state"] == "ADMITTED" for x in rb["taskspecs"])
                             and all(x["state"] == "CREATED" for x in rb["workorders"]))
    result["status_after"] = lc.status(args.project_id)
    (args.out / "far2_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"admitted": len(result["admitted"]), "errors": result["errors"],
                      "readback_ok": result["readback_ok"], "base_head": base_head},
                     ensure_ascii=False, indent=1, default=str))
    return 0 if (not result["errors"] and result["readback_ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
