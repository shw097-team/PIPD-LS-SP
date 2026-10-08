#!/usr/bin/env bash
SRC='/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent'
export HERMES_HOME='C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes'
# Complete the gates whose work is actually finished (ancestors first).
set -u
export PYTHONPATH="$SRC" PYTHONDONTWRITEBYTECODE=1
cd "$SRC" || exit 1
K=(./venv/Scripts/python.exe -B -m hermes_cli.main kanban)
REC="/c/Projects/Agent_Workspace/PIPD/.hgk/kanban"
{ echo "C0=t_cbbdb372"; echo "G1=t_0b92731d"; echo "G2=t_7e7214f7"; echo "G3=t_b6090a8a";
  echo "G4=t_36c70d06"; echo "G5=t_e94d5373"; echo "G6=t_08daea9b"; echo "G7=t_0dc4e10c";
  echo "G8=t_1d8e0b3d"; echo "G9=t_36fbffdb"; echo "G10=t_d67fd1fc"; } > "$REC/dag_ids.txt"

run() { echo "== $*"; "${K[@]}" "$@" 2>&1 | tail -3; }
run claim t_cbbdb372 --json 2>/dev/null || run claim t_cbbdb372
run complete t_cbbdb372 --result "PREFLIGHT_DONE: 160 source files hashed across 6 families (0 drift); HGK doctor PASS (schema v3, sqlite 3.53.1); compiler bundle located; spine backup BACKUP_READBACK_PASS sha256=54f89956...; PIPD root empty -> NEW_IMPLEMENTATION."
run claim t_0b92731d 2>/dev/null || true
run complete t_0b92731d --result "G-KNOWLEDGE-READY PASS: 6/6 families present, 0 drift, 153 docs promoted into derived FTS5 view, POS 7/7 HIT, NEG 2/2 ABSTAIN, NRTV 3/3 PASS, revoked namespace excluded; 7 source files quarantined by HGK sanitation (disclosed)."
run claim t_7e7214f7 2>/dev/null || true
run complete t_7e7214f7 --result "G-PROMPT-COMPILE PASS: lint/activation/acceptance/compile all PROMPT_COMPILE_PASS; contract_sha256=90bfa61d045b2367f183d2f23510037cd3e35291ec5223e40ca98dea78115a5a; thin-prompt 13880 chars."
run claim t_b6090a8a 2>/dev/null || true
run complete t_b6090a8a --result "G-HGK-ADMISSION PASS: project PIPD-LS-SP-20261008 SOURCE_DISCOVERY->SOURCE_ADMISSION->INTENT_BOUND->REQUIREMENTS_READY->DESIGN_READY->PLAN_READY->WORKORDERS_ADMITTED->EXECUTING; 48 sources admitted; 6 TaskSpecs; 6 WorkOrders WO-TS-20261008-01..06."
run list
