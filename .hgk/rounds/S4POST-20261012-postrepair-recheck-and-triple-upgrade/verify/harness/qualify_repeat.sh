#!/usr/bin/env bash
# Repeat the qualification N times for one configuration and report the pass rate.
#
# A single qualification is a sample, not a property. The assigned model at the assigned
# effort both passed and failed in this round with an identical configuration, so the
# original failure is intermittent and only a rate describes it honestly.
#
# Usage: qualify_repeat.sh <model> <provider> <effort> <n> <label>
set -u
WT="${LANE_WT:?LANE_WT must be the delivery worktree}"
MODEL="$1"; PROV="$2"; EFF="$3"; N="$4"; LABEL="$5"
BASE="${NT_BASE:-C:/Users/user/AppData/Local/Temp/qual-repeat}"; mkdir -p "$BASE"
BIN="${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}"
BRIEF="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/GATE_QUALIFICATION_BRIEF.md"
CATALOG="C:/Users/user/.codex/desktop-model-catalog.json"
STYLE="${STYLE:-catalog}"
SAFE="$(printf %s "$MODEL" | tr -c 'A-Za-z0-9._-' '_')"
p=0; f=0
for k in $(seq 1 "$N"); do
  LOG="$BASE/r_${SAFE}_${EFF}_${k}.log"
  if [ "$STYLE" = "catalog" ]; then
    INV=(-c "model=$MODEL" -c "model_reasoning_effort=\"$EFF\""
         -c "openai_base_url=http://127.0.0.1:10102/v1" -c "model_catalog_json=$CATALOG")
  else
    INV=(-m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"")
  fi
  timeout 600 "$BIN" "${INV[@]}" exec --cd "$WT" --sandbox read-only --skip-git-repo-check \
    - < "$BRIEF" > "$LOG" 2>&1
  C=$?
  if [ "$C" -eq 0 ] && grep -q 'Q1_OK' "$LOG" && grep -q 'Q2_OK' "$LOG"; then
    echo "  run $k PASS"; p=$((p+1))
  else
    # Take the TERMINAL error, not the first match in the file: the relay's benign
    # 426 websocket warning always precedes the real failure, so a first-match
    # extraction labels every failure "426", which is wrong and was wrong here.
    RSN="$(grep -o -i -E 'reasoning_content|at capacity|Model provider .* not found' "$LOG" | tail -1)"
    [ -n "$RSN" ] || RSN="$(grep -o -i -E '426 Upgrade Required|429|400' "$LOG" | tail -1)"
    [ -n "$RSN" ] || RSN="undetermined (see $LOG)"
    echo "  run $k FAIL exit=$C reason=${RSN:-unknown}"; f=$((f+1))
  fi
done
echo "RATE [$STYLE] $LABEL :: pass=$p fail=$f of $N"
