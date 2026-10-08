#!/usr/bin/env bash
SRC='/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent'
export HERMES_HOME='C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes'
# PIPD-LS-SP governed round: Kanban board + gate DAG (real CLI receipts)
set -u
export PYTHONPATH="$SRC"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$SRC" PYTHONDONTWRITEBYTECODE=1
cd "$SRC" || exit 1
K=(./venv/Scripts/python.exe -B -m hermes_cli.main kanban)
REC="/c/Projects/Agent_Workspace/PIPD/.hgk/kanban"
mkdir -p "$REC"

echo "### boards create"
"${K[@]}" boards create pipd-ls-sp --name "PIPD-LS-SP 2026-10-08 R1" \
  --description "Governed PIPD-LS-SP implementation round under HG-KSEOS" \
  --default-workdir "C:/Projects/Agent_Workspace/PIPD" 2>&1 | tail -5

echo "### switch"
"${K[@]}" boards switch pipd-ls-sp 2>&1 | tail -3
"${K[@]}" boards show 2>&1 | tail -3
