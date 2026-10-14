#!/usr/bin/env python3
"""Admit the S4R3X continuation round's obligations into the HG-KSEOS Shared Spine.

Typed SharedSpine API only (register_requirement / transition_requirement /
create_taskspec / create_workorder / checkpoint / completion_sweep), the same methods
the previous PIPD rounds used through lc.admit_requirement.

WHY NOT lc.admit_requirement: that wrapper hardcodes writer="codex" on the workorder it
creates. Most of this round's work was performed by the Hermes orchestration layer, not by a
dispatched codex writer, so admitting through the wrapper would write a FALSE writer into the
canonical spine. The wrapper also swallows a failed create (except InvariantViolation: pass),
so its returned ids are not proof the records exist. This script therefore performs the same
typed sequence itself, records the TRUE writer per obligation, pins the TRUE base head per
obligation (the round spans two product worktrees, so one shared base would be wrong), and then
READS THE CHAIN BACK so the admission is verified rather than asserted.

ORDERING DISCLOSURE (must stay in the record): the F006 repair, the gate-falsifiability work and
the Stage B successor were authored, committed and pushed BEFORE this admission ran. Admission
therefore precedes no part of the implementation; it precedes only this record and any future
verification act. A later admission cannot make an earlier write retroactively admitted, so
those three workorders carry a writer value that says so ("hermes-orchestration-post-hoc") and
their workorders stay in state CREATED, i.e. unverified.

The obligations are named with this round's own prefix (S4R3X-) derived from the round id
S4R3-20261013-ci-truthfulness-and-stageb-writeset; no new workstream number is invented for the
source order, and the mapping is written into the round result.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

POST_HOC = "hermes-orchestration-post-hoc"
CODEX_LANE = "codex-cli-verify-lane"

ROUND_REL = ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"


def obligation_specs(a_wt: str, b_wt: str, a_base: str, b_base: str, lane_root: str) -> list[dict]:
    round_dir = f"{b_wt}/{ROUND_REL}"
    return [
        dict(
            requirement_id="REQ-S4R3X-F006-WHEEL-REGISTRY-001",
            priority="P0", owner="PKG07-OWNER", writer=POST_HOC,
            writable_root=a_wt, base_head=a_base,
            wording=(
                "S4R3X ob-1 (report S4R3-F006, P0): repair the packaging defect at root cause so the "
                "STANDARD build ships the contract registry. A wheel produced by `python -m build` and "
                "installed into a clean environment must report the registry as INSTALLED with all 19 "
                "families resolvable under site-packages, and a clean-environment `doctor` must exit 0. "
                "The fix must hold along the sdist-to-wheel route as well (unpack the sdist, build the "
                "wheel FROM the unpacked sdist). Relaxing the validator, deleting a guard, editing the "
                "oracle or narrowing the denominator is forbidden; the red-before state and the "
                "green-after state must both be shown with raw output."),
            tests=[
                "tools/verify_installed_wheel_registry.py (wheel + install + doctor probe)",
                "tests/test_standard_wheel_schemas.py::InstalledRegistryGateTests",
                "focused negative: resolution must not land inside the checkout",
            ],
            evidence_plan=(
                f"{ROUND_REL}/evidence/12_GATES/F006_RED_GREEN_RECEIPTS.txt plus the hosted CI job "
                "that re-runs the same probe"),
        ),
        dict(
            requirement_id="REQ-S4R3X-GATE-FALSIFIABILITY-002",
            priority="P0", owner="CI-OWNER", writer=POST_HOC,
            writable_root=a_wt, base_head=a_base,
            wording=(
                "S4R3X ob-2 (report S4R3-F001/F002, P0): a gate that exists only inside a hosted "
                "workflow cannot be falsified by the person changing it, and the write-set gate must "
                "measure the change sequence it actually governs. Every new or repaired gate must be "
                "executable locally through a committed harness with a negative test that turns it red, "
                "and the Stage A write-set gate must judge the branch's DECLARED stage and base instead "
                "of the pull-request base. The allowlists must not be widened and the frozen-path refusal "
                "must still refuse."),
            tests=[
                "scripts/run_writeset_gate_locally.py (both stages, positive and negative)",
                ".github/workflows/public-plugin-verify.yml stage-aware write-set step",
                "ci.yml wheel-registry step calling the committed tool rather than an inline assertion",
            ],
            evidence_plan=(
                f"{ROUND_REL}/evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt and "
                f"{ROUND_REL}/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt"),
        ),
        dict(
            requirement_id="REQ-S4R3X-STAGE-B-SUCCESSOR-003",
            priority="P0", owner="PKG07-OWNER", writer=POST_HOC,
            writable_root=b_wt, base_head=b_base,
            wording=(
                "S4R3X ob-3 (report S4R3-F002 consequence): Stage B's head was a SIBLING of the Stage A "
                "repair rather than a descendant of it, so it did not contain the gates that verify it. "
                "Re-pin Stage B onto the repaired Stage A tip, remove the pinned literal base from the "
                "workflow in favour of a ref-resolved base, and close the two Stage B defects recorded "
                "in the earlier acceptance record: an official manifest whose name/version may disagree "
                "with the release bookkeeping it is packaged under, and extension namespaces that are "
                "not on the reviewed list. Both must be refused with a typed error and covered by "
                "negative tests without weakening the existing vendor-schema checks."),
            tests=[
                "tests/test_public_plugin_packaging.py (test_20 identity bind + extension namespace)",
                "focused run of the four S4 suites at the successor head",
            ],
            evidence_plan=(
                f"{ROUND_REL}/evidence/12_GATES/LOCAL_FULL_SUITE_RECEIPTS.txt and the hosted runs for "
                "the successor head"),
        ),
        dict(
            requirement_id="REQ-S4R3X-ADMIT-004",
            priority="P0", owner="DOCS-OWNER", writer=POST_HOC,
            writable_root=round_dir, base_head=b_base,
            wording=(
                "S4R3X ob-4: record this continuation round's admission in the canonical spine through "
                "the typed API, verify the chain by reading it back rather than trusting returned ids, "
                "state the ordering deviation that the admission is late, and keep the round's "
                "coordination artefacts (KANBAN board, SWARM lanes, GSTACK route check, OPENSPEC route "
                "evidence) as FILES on disk - a surface that exists only in narration is not evidence "
                "of one. A task that starts before its admission must be reported as such."),
            tests=[
                "admission read-back: requirement FROZEN, taskspec ADMITTED, workorder CREATED",
                "completion_sweep returns the open edges",
            ],
            evidence_plan=f"{ROUND_REL}/admission/s4r3x_admission.json",
        ),
        dict(
            requirement_id="REQ-S4R3X-VERIFY-005",
            priority="P0", owner="EXTERNAL-VERIFY-LANE", writer=CODEX_LANE,
            writable_root=lane_root, base_head=b_base,
            wording=(
                "S4R3X ob-5: independent check on the CODEX CLI VERIFY lane against the frozen Stage A "
                "and Stage B candidates, by a checker distinct from the maker. The checker must re-derive "
                "its verdict from the raw receipts and must end with an explicit verdict plus the ids it "
                "could not verify; a supplied summary reviewed as text is advisory and is NOT an "
                "acceptance. The verdict is advisory only and no canonical acceptance token may be "
                "derived from it. When the lane cannot serve the checker, the correct record is that no "
                "verdict was produced - never a substituted arm, and never a widened sandbox purely to "
                "obtain a green-looking answer."),
            tests=[
                "lane run against the Stage A and Stage B heads",
                "independent re-derivation of the wheel-registry and write-set gates from the receipts",
            ],
            evidence_plan=f"{ROUND_REL}/evidence/12_GATES/AO_LANE_OUTCOME.json",
        ),
        dict(
            requirement_id="REQ-S4R3X-CLOSURE-006",
            priority="P0", owner="DOCS-OWNER", writer=POST_HOC,
            writable_root=round_dir, base_head=b_base,
            wording=(
                "S4R3X ob-6: close the continuation round with a report that states the claim ceiling, "
                "the items genuinely closed, and every remaining item classified by WHO can close it - "
                "this round, the owner, or an external acceptor. Every side effect (pushes, "
                "canonical-store writes, control-plane reads) is disclosed, the ordering deviation is "
                "carried forward, and merge, release and S4 full pass stay HOLD until a separate "
                "acceptance with a new candidate as its subject and an owner release decision."),
            tests=[
                "round result + checkpoint present and pushed",
                "flags NO_MERGE / NO_PUBLIC_RELEASE / S4_FULL_PASS NOT_GRANTED restated",
            ],
            evidence_plan=f"{ROUND_REL}/ROUND_RESULT_S4R3X.md and {ROUND_REL}/CHECKPOINT_20261013.md",
        ),
    ]


def git_head(path: str) -> str:
    out = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True,
                         text=True, check=True)
    return out.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hgk-root", required=True, type=Path)
    ap.add_argument("--a-worktree", required=True)
    ap.add_argument("--b-worktree", required=True)
    ap.add_argument("--lane-root", required=True)
    ap.add_argument("--project-id", default="PIPD-LS-SP-20261008")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--checkpoint", action="store_true")
    args = ap.parse_args()

    sys.path.insert(0, str(args.hgk_root / "src"))
    from hg_kseos.spine import SharedSpine
    from hg_kseos.lifecycle import ProjectLifecycleController

    a_base = git_head(args.a_worktree)
    b_base = git_head(args.b_worktree)
    specs = obligation_specs(args.a_worktree, args.b_worktree, a_base, b_base, args.lane_root)

    spine = SharedSpine(args.hgk_root / "var/shared-spine/hg-kseos.db",
                        args.hgk_root / "src/hg_kseos/schema.sql")
    lc = ProjectLifecycleController(spine)
    args.out.mkdir(parents=True, exist_ok=True)

    result: dict = {
        "step": "s4r3x_admission", "project_id": args.project_id,
        "ordering_disclosure": (
            "implementation (F006 repair, gate falsifiability, Stage B successor) was authored, committed "
            "and pushed BEFORE this admission; the admission is therefore late and non-retroactive"),
        "bases": {"stage_a_head": a_base, "stage_b_head": b_base},
        "status_before": lc.status(args.project_id), "admitted": [], "errors": [],
    }

    for spec in specs:
        rid = spec["requirement_id"]
        ts_id = f"TS-{rid.lower()}"
        wo_id = f"WO-{ts_id}"
        try:
            spine.register_requirement(
                requirement_id=rid,
                source_locator=f"project:{args.project_id}:late-bound-obligation",
                wording=spec["wording"],
                acceptance_id=f"ACC-{rid}",
                oracle=f"{spec['wording'][:80]} ... materialized + acceptance PASS",
                threshold="EXPLICIT_ORACLE_PASS",
                negative_fixture=f"obligation {rid} without a verified workorder",
                priority=spec["priority"],
                project_id=args.project_id,
            )
            spine.acquire_lease(rid, "lifecycle-planner", f"TK-{rid}", ttl_seconds=300)
            try:
                spine.transition_requirement(
                    rid, "FROZEN", actor="lifecycle-planner", token=f"TK-{rid}",
                    expected_version=0, evidence_ref=f"EV-{rid}",
                    idempotency_key=f"FRZ-{rid}",
                )
            finally:
                spine.release_lease(rid, "lifecycle-planner", f"TK-{rid}")
            spine.create_taskspec(
                taskspec_id=ts_id, requirement_id=rid, objective=spec["wording"],
                owner=spec["owner"], writable_root=Path(spec["writable_root"]),
                permissions={"write_scope": "declared_root_only", "network": "none",
                             "remote_push_merge": "FORBIDDEN",
                             "declared_root": spec["writable_root"]},
                tests=spec["tests"], evidence_plan=spec["evidence_plan"],
            )
            spine.create_workorder(
                wo_id, ts_id, writer=spec["writer"],
                worktree=Path(spec["writable_root"]), base_head=spec["base_head"],
            )
            result["admitted"].append({
                "requirement_id": rid, "taskspec": ts_id, "workorder": wo_id,
                "writer": spec["writer"], "owner": spec["owner"],
                "base_head": spec["base_head"], "writable_root": spec["writable_root"],
            })
        except Exception as exc:  # noqa: BLE001 - recorded, never hidden
            result["errors"].append({"requirement_id": rid,
                                     "error": f"{type(exc).__name__}: {exc}"})

    # --- read the chain back: returned ids are not persistence proof ---
    readback: dict = {"requirements": [], "taskspecs": [], "workorders": []}
    with spine.connect() as conn:
        for spec in specs:
            rid = spec["requirement_id"]
            ts_id = f"TS-{rid.lower()}"
            wo_id = f"WO-{ts_id}"
            r = conn.execute("SELECT state,priority,acceptance_id FROM requirements WHERE requirement_id=?",
                             (rid,)).fetchone()
            t = conn.execute("SELECT state,owner,writable_root FROM taskspecs WHERE taskspec_id=?",
                             (ts_id,)).fetchone()
            w = conn.execute("SELECT state,writer,base_head,worktree FROM workorders WHERE workorder_id=?",
                             (wo_id,)).fetchone()
            a = conn.execute("SELECT verdict FROM acceptances WHERE acceptance_id=?", (f"ACC-{rid}",)).fetchone()
            readback["requirements"].append(
                {"requirement_id": rid, "present": r is not None,
                 "state": r["state"] if r else None, "priority": r["priority"] if r else None,
                 "acceptance": a["verdict"] if a else None})
            readback["taskspecs"].append(
                {"taskspec_id": ts_id, "present": t is not None,
                 "state": t["state"] if t else None, "owner": t["owner"] if t else None,
                 "writable_root": t["writable_root"] if t else None})
            readback["workorders"].append(
                {"workorder_id": wo_id, "present": w is not None,
                 "state": w["state"] if w else None, "writer": w["writer"] if w else None,
                 "base_head": w["base_head"] if w else None,
                 "worktree": w["worktree"] if w else None})
    result["readback"] = readback
    result["readback_ok"] = (
        all(x["state"] == "FROZEN" for x in readback["requirements"])
        and all(x["state"] == "ADMITTED" for x in readback["taskspecs"])
        and all(x["state"] == "CREATED" for x in readback["workorders"])
        and all(x["present"] for x in readback["requirements"] + readback["taskspecs"] + readback["workorders"])
    )

    result["completion_sweep"] = lc.completion_sweep(args.project_id)
    if args.checkpoint:
        try:
            result["checkpoint"] = lc.checkpoint(args.project_id, evidence_refs=[
                f"{ROUND_REL}/admission/s4r3x_admission.json",
                f"{ROUND_REL}/ROUND_RESULT_S4R3X.md",
                f"{ROUND_REL}/CHECKPOINT_20261013.md",
            ])
        except Exception as exc:  # noqa: BLE001
            result["errors"].append({"checkpoint": f"{type(exc).__name__}: {exc}"})
    result["status_after"] = lc.status(args.project_id)

    (args.out / "s4r3x_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps({
        "admitted": len(result["admitted"]), "errors": result["errors"],
        "readback_ok": result["readback_ok"],
        "open_workorders": len(result["completion_sweep"]["auto_local"]),
        "checkpoint": result.get("checkpoint", {}).get("checkpoint_id") if isinstance(result.get("checkpoint"), dict) else None,
    }, ensure_ascii=False, indent=1, default=str))
    return 0 if (not result["errors"] and result["readback_ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
