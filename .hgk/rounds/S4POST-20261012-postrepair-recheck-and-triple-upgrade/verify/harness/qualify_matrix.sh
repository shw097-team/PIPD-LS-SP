#!/usr/bin/env bash
# Qualification control matrix.
#
# The FAR study could not separate two axes: "the assigned model cannot do a multi-turn
# tool continuation" versus "that reasoning effort cannot", because the operator had
# changed the model AND the effort together and never ran a same-model control. This
# script runs the identical no-write, two-tool-round-trip qualification through the
# identical CLI and endpoint for every combination and records the outcome verbatim.
#
# Read-only sandbox. No writer, no artifact, no repository file is touched.
set -u
WT="${LANE_WT:?LANE_WT must be the delivery worktree}"
S="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b"
BASE="${NT_BASE:-C:/Users/user/AppData/Local/Temp/qual-matrix}"; mkdir -p "$BASE"
BIN="${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}"
BRIEF="$S/GATE_QUALIFICATION_BRIEF.md"
PASS=0; FAIL=0; i=0
run_one() {
  MODEL="$1"; PROV="$2"; EFF="$3"; LABEL="$4"
  SAFE="$(printf %s "$MODEL" | tr -c 'A-Za-z0-9._-' '_')"
  LOG="$BASE/q${i}_${SAFE}_${EFF}.log"
  timeout 900 "$BIN" exec --cd "$WT" --sandbox read-only \
    -m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"" \
    --skip-git-repo-check - < "$BRIEF" > "$LOG" 2>&1
  C=$?
  if [ "$C" -eq 0 ] && grep -q 'Q1_OK' "$LOG" && grep -q 'Q2_OK' "$LOG"; then
    echo "QUALIFY PASS  $LABEL"; PASS=$((PASS+1))
  else
    echo "QUALIFY FAIL  $LABEL  exit=$C"
    grep -m1 -i -E 'error|invalid_request|capacity' "$LOG" | cut -c1-220 | sed 's/^/    first error: /'
    FAIL=$((FAIL+1))
  fi
  echo "    log=$LOG"
  i=$((i+1))
}
echo "### qualification control matrix (read-only, no writer, no artifact)"
run_one "opencode-go/deepseek-v4.1-flash" "opencode-go" "high"    "assignment: assigned model at assigned effort"
run_one "opencode-go/deepseek-v4.1-flash" "opencode-go" "minimal" "effort axis: assigned model at minimal effort"
run_one "opencode-go/deepseek-v4-flash"   "opencode-go" "high"    "model axis: backup model at assigned effort"
run_one "opencode-go/deepseek-v4-flash"   "opencode-go" "minimal" "the shape the backup run actually used"
run_one "gpt-6.1-sol"                     "openai"      "medium"  "control: the checker model that is known to work"
echo
echo "MATRIX pass=$PASS fail=$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
