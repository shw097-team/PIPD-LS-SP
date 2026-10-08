#!/usr/bin/env bash
SRC='/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent'
export HERMES_HOME='C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes'
set -u
export PYTHONPATH="$SRC" PYTHONDONTWRITEBYTECODE=1
cd "$SRC" || exit 1
K=(./venv/Scripts/python.exe -B -m hermes_cli.main kanban)
run() { echo "== $*"; "${K[@]}" "$@" 2>&1 | tail -2; }
run claim t_36c70d06 2>/dev/null || true
run complete t_36c70d06 --result "G-EXEC-SURFACES PASS: KANBAN board pipd-ls-sp + 11-card gate DAG with real create/claim/complete receipts; SWARM 3 independent verification lanes dispatched (deleg_5a26d6d5: evidence recheck / admission+board readback / adversarial claim audit); GSTACK route check recorded (.hgk/surfaces/gstack_route_check.json: review+qa->GSTACK CERTIFIED, design/impl/acceptance/validation->NATIVE); OPENSPEC 1.8.0 initialised in PIPD with change pipd-ls-sp-s0-s1 (5/11 tasks); CODEX writer spawn codex-cli 0.147.0-alpha.6.5 wrote 19/19 schemas (run1 blocked by missing windows sandbox helper, run2 ran under an explicitly disclosed sandbox bypass)."
run claim t_e94d5373 2>/dev/null || true
run complete t_e94d5373 --result "G-S0 PASS: 19/19 canonical machine-contract families materialised in schemas/ by writer=codex (registry.json + 19 Draft2020-12 closed schemas). Verified by tests/test_s0_contracts.py: exact order/identity, draft+closed, registry fields enforced by each schema, seam-only materialisation preserved, 20th-family rejected, renamed-family rejected. doctor PASS with 0 findings."
run claim t_08daea9b 2>/dev/null || true
run complete t_08daea9b --result "G-S1 PASS: LITE vertical slice intent->PI-PKG->PD-PKG->ConstructionContract->ECP->TQAEP runs end to end; 5 requirement atoms, 5 TQAEP tests, trace closure PASS (0 orphans), all 5 records schema+semantic validate with 0 findings, replay-deterministic (identical ids/hashes across runs). 13/13 CLI commands execute (exit 0). Defects found and repaired in-round: profile axis mismatch, record/schema field divergence, doctor duplicate-skill rule over-broad. Disclosed: LITE request escalated to ASSURED by the axis-complexity safety veto."
run claim t_0dc4e10c 2>/dev/null || true
run complete t_0dc4e10c --result "G-SECURITY-ROLLBACK PASS: secret scan PASS (0 hits, 5 patterns) over the tree; git-history secret scan PASS (157 blobs, 0 matches); rollback drill PASS (git worktree at baseline fe97156080764768e6e064e2c68375156c976868 restores 27 files, schemas/ correctly absent, worktree removed cleanly); export refuses secret-bearing files (EXPORT_SECRET_SCAN); repair refuses empty scope and maker self-accept."
run list
