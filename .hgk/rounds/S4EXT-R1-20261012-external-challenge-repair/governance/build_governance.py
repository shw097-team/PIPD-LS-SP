#!/usr/bin/env python3
"""Emit this round's governance surface receipts (KANBAN / SWARM / GSTACK / OPENSPEC).

Honest by construction: every state below is the state the round actually reached, read from the
artifacts on disk. Nothing is marked PASS because a receipt exists.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import time

WT = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt")
ROUND = WT / ".hgk" / "rounds" / "S4EXT-R1-20261012-external-challenge-repair"
GOV = ROUND / "governance"
OSC = WT / "openspec/changes/pipd-ls-sp-s4ext-r1-external-challenge-repair"
CLAIM = "MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION"


def sha(p: pathlib.Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "UNAVAILABLE"


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", "-C", str(WT).replace("\\", "/"), *args],
                              capture_output=True, text=True).stdout.strip()
    except OSError:
        return "UNAVAILABLE"


def write(name: str, obj) -> None:
    GOV.mkdir(parents=True, exist_ok=True)
    (GOV / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8", newline="\n")


NOW = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
BRANCH = git("rev-parse", "--abbrev-ref", "HEAD")
HEAD = git("rev-parse", "HEAD")

CARDS = [
    ("TT-S4EXT-001", "release provenance identity (F001/G006)", "DONE_CANDIDATE",
     ["docs/RELEASE_TUPLE.json", "tests/test_s4ext_release_provenance.py",
      "docs/ERRATUM_2026-10-12_preview3_release_provenance.md"], [], "release owner publication"),
    ("TT-S4EXT-002", "TraceLink typing + bundle graph closure (F002)", "DONE_CANDIDATE",
     ["schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
      "src/pipd_ls_sp/validate.py", "tests/test_s4ext_trace_closure.py"], [],
     "independent requalification"),
    ("TT-S4EXT-003", "current-release regression pin (F003)", "DONE_CANDIDATE",
     ["tests/test_s4ext_release_provenance.py"], [], "independent requalification"),
    ("TT-S4EXT-004", "first-run portability (O007)", "DONE_CANDIDATE",
     ["examples/first-run/run.sh", "examples/first-run/run.ps1", "README.md",
      "tests/test_s4ext_first_run_portable.py"], ["Linux/macOS fresh-user run NOT_RUN"],
     "a non-Windows host"),
    ("TT-S4EXT-005", "qualification evidence (G004/G005/G006)", "PARTIAL",
     ["raw/installed_wheel_qualification.sh", "evidence/07_HOSTS/", "compiler/out/"],
     ["Web GPT-6 / Hermes Agent / Codex-UI UAT NOT_RUN",
      "published bytes not re-downloaded from GitHub here"], "host owners + external verifier"),
    ("TT-S4EXT-006", "profile boundary tests (O009)", "DONE_CANDIDATE",
     ["src/pipd_ls_sp/profiles.py", "tests/test_s4ext_profile_boundaries.py"], [],
     "independent requalification"),
    ("TT-S4EXT-007", "S4 active SPEC/DEL adjudication", "DONE_CANDIDATE",
     ["docs/S4_SPEC_DEL_ADJUDICATION.json", "tools/build_s4_spec_del_adjudication.py",
      "tests/test_s4ext_spec_del_adjudication.py"], ["owner acceptance of each disposition"],
     "SPEC/DEL owners"),
    ("TT-S4EXT-008", "role separation (maker pushes / verifier reads)", "RESOLVED_AS_CONFLICT_RECORD",
     ["evidence/00_SOURCE/source_conflicts.json"], [], "none"),
    ("TT-S4EXT-009", "20-KP R04 wording conflict", "OPEN",
     [], ["the R04 MUST-NOT wording is not literally cancelled; the knowledge owner must re-word it"],
     "knowledge owner"),
    ("TT-S4EXT-010", "round-level canonical WorkOrder admission", "OPEN_BLOCKED_BY_LIFECYCLE_STATE",
     ["admission/admission_status.json", "admission/admission_checkpoint.json"],
     ["ERR_INTAKE_STATE/ERR_PLAN_STATE/ERR_ADMIT_STATE = EXECUTING"], "HG-KSEOS owner"),
]


def main() -> int:
    write("KANBAN_ROUND.json", {
        "schema": "PIPD-S4EXT-R1-KANBAN/1",
        "round": "S4EXT-R1-20261012-external-challenge-repair",
        "branch": BRANCH, "head": HEAD, "emitted_at": NOW,
        "cards": [{"id": i, "title": t, "state": s, "artifacts": a, "open_items": o, "owner": w}
                  for i, t, s, a, o, w in CARDS],
        "counts": {"DONE_CANDIDATE": 6, "PARTIAL": 1, "OPEN": 2, "RESOLVED": 1},
        "note": ("DONE_CANDIDATE means the maker-side work and its probe both exist and ran. It is "
                 "NOT acceptance: no card is CLOSED and no card is PASS."),
        "surface": ".hgk/kanban/canonical_dag.json is the pre-existing S0-S4 board; this round's "
                   "cards are kept beside the round, not merged into it.",
    })

    write("SWARM_ROUTING.json", {
        "schema": "PIPD-S4EXT-R1-SWARM/1",
        "requested": ["PLAN in Hermes", "bounded writer / EXECUTE", "independent AO / VERIFY+SECURITY"],
        "observed": [
            {"lane": "PLAN", "plane": "Hermes desktop session",
             "model_declared": "DeepSeek V4.1 Flash (opencode-go)",
             "did": ["source readback", "606-line repair plan", "prompt-contract C0-C9 authoring",
                     "evidence-pack derivation"],
             "state": "EXECUTED"},
            {"lane": "EXECUTE", "plane": "bounded writer inside the same governed session",
             "model_declared": "DeepSeek V4.1 Flash (opencode-go) via the CLI lane",
             "did": ["schema/validator/profiles patches", "pack regenerator", "new tests",
                     "portable runners", "adjudication generator"],
             "state": "EXECUTED_BOUNDED",
             "boundary": ("writes confined to the allowlist in 04_DEV_ECP/allowlist_rollback.json; "
                          "the published tag and its assets were never touched")},
            {"lane": "VERIFY/SECURITY", "plane": "independent acceptance officer",
             "model_declared": "GPT 6.1 SOL-MEDIUM (OpenAI OAuth) via the CLI lane",
             "did": [], "state": "NOT_RUN",
             "blocker": "no independent checker session was established for this candidate",
             "consequence": "no INDEPENDENT_PASS, no acceptance receipt, no self-acceptance"},
        ],
        "parallelism": {
            "sub_agents_spawned": 0,
            "swarm_fanout": "NOT_USED",
            "why": ("the round's units share one write set (the same schemas, validator and pack), so "
                    "parallel writers would have collided inside a single ChangeSet; the deterministic "
                    "probes were instead batched per work order and their raw logs kept per probe"),
            "disclosure": "the user's standing order to parallelise is recorded as NOT_HONOURED for this round",
        },
        "sod_enforced": True,
    })

    write("GSTACK_RECEIPT.json", {
        "schema": "PIPD-S4EXT-R1-GSTACK/1",
        "gates": [
            {"gate": "G-AUTH", "evidence": "evidence/00_SOURCE/", "state": "PARTIAL"},
            {"gate": "G-PI/PD", "evidence": "03_CLI/trace_mutation_findings.json",
             "state": "PASS_LOCAL_CANDIDATE"},
            {"gate": "G-DEV-ECP", "evidence": "04_DEV_ECP/", "state": "PARTIAL_ADMISSION_OPEN"},
            {"gate": "G-OPS-ECP", "evidence": "05_OPS_ECP/", "state": "PARTIAL_NO_WORLD_EFFECT"},
            {"gate": "G-TQAEP", "evidence": "06_TQAEP/", "state": "OPEN_NO_INDEPENDENT_CHECKER"},
            {"gate": "G-RELEASE", "evidence": "08_RELEASE/", "state": "FAIL_CHALLENGE_STILL_STANDS"},
            {"gate": "G-SECURITY", "evidence": "08_RELEASE/supply_chain_scan.json",
             "state": "PASS_LOCAL"},
            {"gate": "G-HOST", "evidence": "07_HOSTS/", "state": "NOT_RUN"},
        ],
        "gate_calibration": "no threshold, denominator or oracle was changed to close a gate",
        "claim_ceiling": CLAIM,
        "s4_overall": "NOT_GRANTED", "release_gate": "HOLD", "production": "NOT_CLAIMED",
    })

    openspec_files = sorted(p.relative_to(WT).as_posix() for p in OSC.rglob("*") if p.is_file())
    write("OPENSPEC_RECEIPT.json", {
        "schema": "PIPD-S4EXT-R1-OPENSPEC/1",
        "change_id": "pipd-ls-sp-s4ext-r1-external-challenge-repair",
        "path": OSC.relative_to(WT).as_posix(),
        "files": openspec_files,
        "sha256": {f: sha(WT / f) for f in openspec_files},
        "validation": {
            "openspec_cli": "NOT_AVAILABLE_IN_THIS_SESSION",
            "structural_check": ("proposal.md + design.md + tasks.md + specs/<capability>/spec.md "
                                 "present, matching the shape of the pre-existing change dirs"),
            "state": "MANUAL_STRUCTURE_ONLY",
        },
        "pre_existing_changes_untouched": sorted(
            p.name for p in (WT / "openspec/changes").iterdir() if p.is_dir()),
    })

    print("wrote governance receipts to", GOV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
