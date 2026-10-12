#!/usr/bin/env bash
# Qualification control matrix - corrected invocation.
#
# Two errors in the first attempt, both mine, are fixed here:
#   * "opencode-go/deepseek-v4.1-flash" is a CATALOG SLUG, not a provider id. Passing it
#     with -c model_provider=<vendor> makes the CLI answer "Model provider not found",
#     which is a harness error; reading that as "the assigned model failed the round trip"
#     would have been a false positive that refused a healthy lane.
#   * the correct shape is the one the writers actually used: -c model=<slug> together with
#     openai_base_url and model_catalog_json, no model_provider.
#
# The FAR study could not separate model from effort because the operator changed both at
# once and kept no same-model control. This matrix runs the identical no-write, two-tool
# round-trip qualification through the identical CLI for every combination.
set -u
WT="${LANE_WT:?LANE_WT must be the delivery worktree}"
BASE="${NT_BASE:-C:/Users/user/AppData/Local/Temp/qual-matrix}"; mkdir -p "$BASE"
BIN="${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}"
BRIEF="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/GATE_QUALIFICATION_BRIEF.md"
CATALOG="C:/Users/user/.codex/desktop-model-catalog.json"
BASEURL="http://127.0.0.1:10102/v1"
PASS=0; FAIL=0; i=0
run_one() {
  STYLE="$1"; MODEL="$2"; PROV="$3"; EFF="$4"; LABEL="$5"
  SAFE="$(printf %s "$MODEL" | tr -c 'A-Za-z0-9._-' '_')"
  LOG="$BASE/q${i}_${SAFE}_${EFF}.log"
  if [ "$STYLE" = "catalog" ]; then
    INV=(-c "model=$MODEL" -c "model_reasoning_effort=\"$EFF\""
         -c "openai_base_url=$BASEURL" -c "model_catalog_json=$CATALOG")
  else
    INV=(-m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"")
  fi
  timeout 900 "$BIN" "${INV[@]}" exec --cd "$WT" --sandbox read-only --skip-git-repo-check \
    - < "$BRIEF" > "$LOG" 2>&1
  C=$?
  if [ "$C" -eq 0 ] && grep -q 'Q1_OK' "$LOG" && grep -q 'Q2_OK' "$LOG"; then
    echo "QUALIFY PASS  [$STYLE] $LABEL"
    PASS=$((PASS+1))
  else
    echo "QUALIFY FAIL  [$STYLE] $LABEL  exit=$C"
    grep -m2 -i -E 'error|invalid_request|capacity|not found' "$LOG" | cut -c1-200 | sed 's/^/    /'
    FAIL=$((FAIL+1))
  fi
  echo "    log=$LOG  bytes=$(wc -c < "$LOG")"
  i=$((i+1))
}
echo "### corrected qualification control matrix (read-only, no writer, no artifact)"
run_one catalog "opencode-go/deepseek-v4.1-flash" opencode-go high    "assignment: assigned model at the assigned effort"
run_one catalog "opencode-go/deepseek-v4.1-flash" opencode-go none    "effort axis: assigned model at the effort the backup run used"
run_one catalog "opencode-go/deepseek-v4-flash"   opencode-go high    "model axis: backup model at the assigned effort"
run_one catalog "opencode-go/deepseek-v4-flash"   opencode-go none    "the exact shape the backup writer lanes ran"
run_one openai  "gpt-6.1-sol"                     openai      medium  "control: the checker model that is known to work"
echo
echo "MATRIX pass=$PASS fail=$FAIL"
