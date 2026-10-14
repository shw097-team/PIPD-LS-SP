#!/usr/bin/env python3
"""Admit the FAR decision-and-handover round into the HG-KSEOS Shared Spine.

Typed SharedSpine API only, and the base head is read INSIDE this process: `create_workorder`
validates only that base_head is non-empty, so a placeholder passes silently and no update API
exists to correct it afterwards.

Two TaskSpec/WorkOrder pairs, because one WorkOrder binds exactly one TaskSpec and the round both
executes and verifies:
  EXECUTE  writer `codex`                 - the bounded writer that assembles the study draft
  VERIFY   writer `codex-cli-verify-lane` - the independent checker, a distinct identity

DELIBERATE WORDING CHOICE: an earlier admitted requirement in this project
(REQ-S4R3X-GATE-FALSIFIABILITY-002) states that the write-set allowlists "must not be widened".
That obligation is now MEASURED as violated, so this requirement is written to require the study to
REPORT that deviation with its exact delta rather than to restate the unverified claim. Admission
records must not carry a claim the same round has already falsified.
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
    wording = (
        "FAR decision study on the S4 R3 round's current state, its pending owner decisions, and what "
        "may be handed to an external acceptance officer. The study must: (i) report the MEASURED "
        "allowlist deviation against the already-admitted obligation "
        "REQ-S4R3X-GATE-FALSIFIABILITY-002, with the exact added entries and the fact that the "
        "obligation's own wording forbids widening - classified as a requirement violation, not a "
        "documentation gap; (ii) enumerate every pending decision with its owner and what unblocks it; "
        "(iii) separate items that are owner inputs or external-subject work from defects of this "
        "round; (iv) rank remedies by action, cost, risk, the clause restored and the artifact that "
        "would verify it, preferring options that need no engineering; and (v) close with the "
        "marginal-value read: how many of the governing documents' required-external-evidence items "
        "moved across the rounds under study. Constraints: low friction, high engineering necessity, "
        "not over-engineered, aligned to the task core (the R3 prompt, the external acceptance report, "
        "the upstream blueprint), and directly usable by an external acceptance officer. The study may "
        "not relax any oracle, threshold, validator or denominator, and may not merge, release or tag.")
    return [
        dict(
            requirement_id="REQ-S4R3FAR-DECISION-STUDY-001",
            priority="P1", owner="FAR-STUDY-EXECUTE", writer="codex",
            writable_root=round_dir, base_head=base_head,
            objective=wording,
            tests=[
                "the study's every factual claim binds to a receipt already in the round's evidence tree",
                "the allowlist delta is recomputed by the study, not quoted from prose",
                "each remedy names the artifact that would verify it",
            ],
            evidence_plan=f"{FAR_REL}/ plus the round's existing evidence/12_GATES receipts",
        ),
        dict(
            requirement_id="REQ-S4R3FAR-DECISION-VERIFY-002",
            priority="P1", owner="EXTERNAL-VERIFY-LANE", writer="codex-cli-verify-lane",
            writable_root=round_dir, base_head=base_head,
            objective=(
                "Independently verify the FAR decision study. The executor's study and every receipt "
                "it cites are CLAIMS, not evidence. Re-derive: the allowlist delta from the two "
                "committed revisions; the state of each admission row the study cites; and the "
                "existence of every artifact path the study cites. Refuse to accept any claim whose "
                "receipt the study does not carry. Report per-claim verdicts and name every claim you "
                "could not re-derive."),
            tests=[
                "recompute the allowlist set-diff from the committed workflow revisions",
                "resolve every cited artifact path and report unresolved ones",
                "read the admission rows back from the spine read-only",
            ],
            evidence_plan=f"{FAR_REL}/verify/",
        ),
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
    plan = specs(round_dir, base_head)

    spine = SharedSpine(args.hgk_root / "var/shared-spine/hg-kseos.db",
                        args.hgk_root / "src/hg_kseos/schema.sql")
    lc = ProjectLifecycleController(spine)
    args.out.mkdir(parents=True, exist_ok=True)

    result: dict = {"step": "s4r3_far_admission", "project_id": args.project_id,
                    "base_head_at_admission": base_head, "status_before": lc.status(args.project_id),
                    "admitted": [], "errors": []}
    for spec in plan:
        rid = spec["requirement_id"]
        ts_id = f"TS-{rid.lower()}"
        wo_id = f"WO-{ts_id}"
        try:
            spine.register_requirement(
                requirement_id=rid,
                source_locator=f"project:{args.project_id}:far-decision-study-order",
                wording=spec["objective"], acceptance_id=f"ACC-{rid}",
                oracle=f"{spec['objective'][:80]} ... materialized + acceptance PASS",
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture=f"study {rid} without a verified workorder",
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
                                       "writer": spec["writer"], "owner": spec["owner"],
                                       "base_head": spec["base_head"]})
        except Exception as exc:  # noqa: BLE001 - recorded, never hidden
            result["errors"].append({"requirement_id": rid, "error": f"{type(exc).__name__}: {exc}"})

    readback: dict = {"requirements": [], "taskspecs": [], "workorders": []}
    with spine.connect() as conn:
        for spec in plan:
            rid = spec["requirement_id"]
            ts_id = f"TS-{rid.lower()}"
            wo_id = f"WO-{ts_id}"
            r = conn.execute("SELECT state,priority,acceptance_id FROM requirements WHERE requirement_id=?",
                             (rid,)).fetchone()
            t = conn.execute("SELECT state,owner,base_head FROM taskspecs WHERE taskspec_id=?",
                             (ts_id,)).fetchone() if _has_col(conn, "taskspecs", "base_head") else \
                conn.execute("SELECT state,owner FROM taskspecs WHERE taskspec_id=?", (ts_id,)).fetchone()
            w = conn.execute("SELECT state,writer,base_head,worktree FROM workorders WHERE workorder_id=?",
                             (wo_id,)).fetchone()
            a = conn.execute("SELECT verdict FROM acceptances WHERE acceptance_id=?",
                             (f"ACC-{rid}",)).fetchone()
            readback["requirements"].append({"requirement_id": rid, "present": r is not None,
                                             "state": r["state"] if r else None,
                                             "priority": r["priority"] if r else None,
                                             "acceptance": a["verdict"] if a else None})
            readback["taskspecs"].append({"taskspec_id": ts_id, "present": t is not None,
                                          "state": t["state"] if t else None,
                                          "owner": t["owner"] if t else None})
            readback["workorders"].append({"workorder_id": wo_id, "present": w is not None,
                                           "state": w["state"] if w else None,
                                           "writer": w["writer"] if w else None,
                                           "base_head": w["base_head"] if w else None})
    result["readback"] = readback
    result["readback_ok"] = (
        all(x["state"] == "FROZEN" for x in readback["requirements"])
        and all(x["state"] == "ADMITTED" for x in readback["taskspecs"])
        and all(x["state"] == "CREATED" for x in readback["workorders"])
        and all(x["present"] for x in readback["requirements"] + readback["taskspecs"]
                + readback["workorders"]))
    result["status_after"] = lc.status(args.project_id)
    (args.out / "far_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({"admitted": len(result["admitted"]), "errors": result["errors"],
                      "readback_ok": result["readback_ok"],
                      "base_head": base_head}, ensure_ascii=False, indent=1, default=str))
    return 0 if (not result["errors"] and result["readback_ok"]) else 1


def _has_col(conn, table: str, col: str) -> bool:
    return any(r[1] == col for r in conn.execute(f"pragma table_info({table})"))


if __name__ == "__main__":
    raise SystemExit(main())
