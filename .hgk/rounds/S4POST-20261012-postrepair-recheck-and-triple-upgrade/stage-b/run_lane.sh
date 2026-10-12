#!/usr/bin/env bash
# Governed lane launcher (v3) - fail-closed, with the round-5 fail-open counterexamples closed.
#
# v1 (round 3): commit harness artifacts before handover; refuse a dirty worktree; log outside the tree.
# v2 (round 4): D1 no fail-open on a missing brief or a failed main-log copy; D2 reject postflight dirt;
#               D3 round-relative output only; F refuse a log dir inside the worktree.
# v3 (round 5) closes five counterexamples an independent officer demonstrated against v2:
#   R1 a failed receipt copy still returned 0                     -> receipt copy is checked and fatal
#   R2 a FAILED git status was read as "clean" (empty output)     -> a nonzero status query is fatal
#   R3 an already staged outside-round file got committed        -> staged paths outside the round are refused
#   R4 (gate-side) see run_lanes_gated.sh
#   R5 (gate-side) see run_lanes_gated.sh
#   A  the manifest was written inside the tree after the clean check, so the handover was dirtied by the
#      launcher itself; it is now written outside the tree and copied in at postflight, like the lane log.
#
# Exit: child's code on full success; 2 dirty/unverifiable preflight; 3 refused input/logdir;
#       4 lane log missing or uncopyable; 5 postflight dirty or unverifiable; 6 receipt or commit failed.
set -u

LANE="${1:-}"; BRIEF="${2:-}"; OUTSUB="${3:-}"
[ -n "$LANE" ] && [ -n "$BRIEF" ] && [ -n "$OUTSUB" ] || { echo "REFUSED[3] usage: run_lane.sh <LANE> <brief> <round-relative-outsub>" >&2; exit 3; }

WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
RELROUND=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
R="$WT/$RELROUND"; S="$R/stage-b"
EMAIL="lane-harness@local.invalid"; NAME="hgk lane harness"
CODEX="${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}"

die() { echo "REFUSED[$1] $2" >&2; echo "REFUSED_${LANE}_DONE"; exit "$1"; }

# R2: a status query that FAILS must never be read as "clean". Counts, or the literal ERR.
status_count() {
  local out rc
  out="$(git status --porcelain 2>/dev/null)"; rc=$?
  [ "$rc" -eq 0 ] || { echo ERR; return; }
  printf '%s\n' "$out" | sed '/^[[:space:]]*$/d' | wc -l | tr -d ' '
}
# R3: refuse to commit if anything outside the round is staged.
staged_outside() { git diff --cached --name-only 2>/dev/null | grep -v "^${RELROUND}/" | grep -v '^[[:space:]]*$'; }
commit_all() {
  git add -A -- "$RELROUND" 2>/dev/null || { echo "GIT_ADD_FAILED" >&2; return 1; }
  local outside; outside="$(staged_outside)"
  if [ -n "$outside" ]; then
    echo "STAGED_OUTSIDE_ROUND_REFUSED: $(printf '%s' "$outside" | tr '\n' ' ')" >&2
    return 1
  fi
  if ! git diff --cached --quiet 2>/dev/null; then
    git -c user.email="$EMAIL" -c user.name="$NAME" commit -q -m "$1" >/dev/null 2>&1 || { echo "GIT_COMMIT_FAILED" >&2; return 1; }
  fi
  return 0
}

[ -f "$S/$BRIEF" ] || die 3 "brief not found: stage-b/$BRIEF"
case "$OUTSUB" in /*|*..*) die 3 "OUTSUB must stay inside the round: $OUTSUB" ;; esac
[ -d "$R" ] || die 3 "round directory not found: $RELROUND"

LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"
mkdir -p "$LOGDIR" || die 3 "cannot create lane log directory: $LOGDIR"
nrm() { { cd "$1" && pwd -P; } 2>/dev/null | tr 'A-Z' 'a-z'; }
WTRES=$(nrm "$WT"); LGRES=$(nrm "$LOGDIR")
[ -n "$WTRES" ] && [ -n "$LGRES" ] || die 3 "cannot resolve worktree/log paths for the containment check"
case "$LGRES" in "$WTRES"|"$WTRES"/*) die 3 "lane log dir resolves inside the worktree: $LGRES" ;; esac

cd "$WT" || die 3 "cannot enter worktree"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TOKEN="${LANE_TOKEN:-$STAMP}"
commit_all "chore(s4post-b): commit harness artifacts before the ${LANE} lane handover" \
  || die 6 "harness preflight commit failed; refusing to hand over"
DIRTY="$(status_count)"
[ "$DIRTY" != "ERR" ] || die 2 "git status failed; cleanliness cannot be established, refusing to launch ${LANE}"
[ "$DIRTY" -eq 0 ] || die 2 "worktree not clean before handover: $DIRTY path(s); refusing to launch ${LANE}"
echo "PREFLIGHT_CLEAN HEAD=$(git rev-parse --short HEAD)"

mkdir -p "$R/$OUTSUB" || die 3 "cannot create round-relative output dir: $OUTSUB"

case "$LANE" in
  AO*) DEF_MODEL="gpt-6.1-sol"; DEF_PROV="openai"; DEF_EFF="medium" ;;
  *)   DEF_MODEL="opencode-go/deepseek-v4.1-flash"; DEF_PROV="opencode-go"; DEF_EFF="high" ;;
esac
MODEL="${LANE_MODEL:-$DEF_MODEL}"; PROV="${LANE_PROVIDER:-$DEF_PROV}"; EFF="${LANE_EFFORT:-$DEF_EFF}"
SANDBOX_MODE="${LANE_SANDBOX:-workspace-write}"

# R5: a slug like "opencode-go/deepseek-v4.1-flash" is a CATALOG ENTRY, not a provider id. The caller
# must state the route; the gate passes the role's route so a writer can never be launched through a
# route the qualification did not exercise.
if [ "${ROUTE_STYLE:-openai}" = "catalog" ]; then
  INV=(-c "model=$MODEL" -c "model_reasoning_effort=\"$EFF\""
       -c "openai_base_url=${ROUTE_BASE_URL:-http://127.0.0.1:10102/v1}"
       -c "model_catalog_json=${ROUTE_CATALOG:?catalog route needs ROUTE_CATALOG}")
else
  INV=(-m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"")
fi

# A: the manifest is written OUTSIDE the worktree and copied in at postflight.
LOG="$LOGDIR/${LANE}_${STAMP}.log"; LOGEXIT="$LOG.exit"; MAN="$LOGDIR/${LANE}_${STAMP}.manifest"
echo "${LANE}_LANE=${STAMP} MODEL=${MODEL} provider=${PROV} reasoning=${EFF} route=${ROUTE_STYLE:-openai} (declared)"
printf 'LANE=%s\nMODEL=%s\nPROVIDER=%s\nEFFORT=%s\nSTAMP=%s\nTOKEN=%s\nWT=%s\nROUTE_STYLE=%s\nSANDBOX=%s\n' \
  "$LANE" "$MODEL" "$PROV" "$EFF" "$STAMP" "$TOKEN" "$WT" "${ROUTE_STYLE:-openai}" "$SANDBOX_MODE" > "$MAN"

timeout 5400 "$CODEX" "${INV[@]}" exec --cd "$WT" --sandbox "$SANDBOX_MODE" --skip-git-repo-check \
  - < "$S/$BRIEF" > "$LOG" 2>&1
CODE=$?
{ [ -f "$LOG" ] && printf 'child_exit=%s\n' "$CODE" > "$LOGEXIT"; } || printf 'child_exit=%s\n' "$CODE" > "$LOGEXIT"
echo "${LANE} exit=${CODE} log=${LOG}"

# D1/R1: never claim or accept a copy that did not happen; a failed receipt copy is fatal.
COPY_OK=0; RECEIPT_OK=0
if [ -f "$LOG" ]; then
  if cp "$LOG" "$S/${LANE}_${STAMP}.log"; then
    COPY_OK=1
    if cp "$LOGEXIT" "$S/${LANE}_${STAMP}.exit" 2>/dev/null; then RECEIPT_OK=1; fi
  fi
fi
if [ "$COPY_OK" -eq 1 ]; then
  MSG="evidence(s4post-b): ${LANE} lane output ${STAMP} (lane log copied in from outside the worktree; child exit ${CODE})"
else
  MSG="evidence(s4post-b): ${LANE} lane METADATA ONLY ${STAMP} - no lane log was copied into the tree (child exit ${CODE}); do not read this as a completed lane"
  echo "POSTFLIGHT_LOG_COPY_FAILED log=$LOG" >&2
fi
[ "$RECEIPT_OK" -eq 1 ] || echo "POSTFLIGHT_RECEIPT_COPY_FAILED receipt=$LOGEXIT" >&2

POSTFAIL=0
commit_all "$MSG" || POSTFAIL=1
DIRTY2="$(status_count)"
[ "$DIRTY2" != "ERR" ] || { echo "POSTFLIGHT_STATUS_FAILED" >&2; POSTFAIL=1; }
if [ "$DIRTY2" != "ERR" ] && [ "$DIRTY2" -ne 0 ]; then
  echo "POSTFLIGHT_DIRTY_REJECTED: $DIRTY2 path(s) still untracked" >&2; POSTFAIL=1
fi

# The receipt attests that everything above passed. It is written last and committed, so the gate can
# test for THIS launch without a wildcard that an older receipt could satisfy.
if [ "$COPY_OK" -eq 1 ] && [ "$RECEIPT_OK" -eq 1 ] && [ "$POSTFAIL" -eq 0 ]; then
  printf 'lane=%s\nstamp=%s\ntoken=%s\nchild_exit=%s\npostflight_dirty=%s\nmodel=%s\nroute=%s\n' \
    "$LANE" "$STAMP" "$TOKEN" "$CODE" "$DIRTY2" "$MODEL" "${ROUTE_STYLE:-openai}" > "$S/${LANE}_${TOKEN}.receipt"
  commit_all "evidence(s4post-b): ${LANE} lane receipt ${TOKEN} (child exit ${CODE})" \
    || { echo "RECEIPT_COMMIT_FAILED" >&2; POSTFAIL=1; }
  echo "RECEIPT_WRITTEN ${LANE}_${TOKEN}.receipt"
fi

echo "POSTFLIGHT:dirty=$DIRTY2 HEAD=$(git rev-parse --short HEAD)"
echo "${LANE}_LANE_DONE"

[ "$COPY_OK" -eq 1 ] || exit 4
[ "$RECEIPT_OK" -eq 1 ] || exit 6
[ "$POSTFAIL" -eq 0 ] || exit 5
exit "$CODE"
