#!/usr/bin/env bash
# Governed lane launcher (v2) - fail-closed.
#
# v1 repairs (round-3 finding): commit harness artifacts before handover; refuse to
# launch against a dirty worktree; write the lane log OUTSIDE the worktree; copy it
# back and commit only after the run.
#
# v2 repairs three reproducible v1 defects an independent officer demonstrated in
# round 4 (verdict PARTIAL):
#   D1  a missing brief and a failed log copy were masked and the wrapper exited 0
#       while the child had failed. Now: brief is validated BEFORE launch, the copy
#       is checked, the commit message states whether a log was really copied, and
#       the wrapper propagates a nonzero status.
#   D2  postflight dirt was counted and printed but never rejected. Now nonzero.
#   D3  "mkdir -p $WT/$OUTSUB" created the output directory at the REPOSITORY ROOT,
#       outside the round's permitted write set. Now round-relative only.
#   F   TMPDIR was never validated against the worktree. Now a log dir resolving
#       inside the worktree is refused.
#
# Usage: run_lane.sh <LANE> <brief-relative-to-stage-b> <round-relative-out-subdir>
# Exit: child's code on success paths; 2 dirty preflight; 3 refused input/logdir;
#       4 lane log missing/uncopyable; 5 postflight dirt detected.
set -u

LANE="${1:-}"; BRIEF="${2:-}"; OUTSUB="${3:-}"
[ -n "$LANE" ] && [ -n "$BRIEF" ] && [ -n "$OUTSUB" ] || { echo "REFUSED[3] usage: run_lane.sh <LANE> <brief> <round-relative-outsub>" >&2; exit 3; }

WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
RELROUND=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
R="$WT/$RELROUND"; S="$R/stage-b"
EMAIL="lane-harness@local.invalid"; NAME="hgk lane harness"
CODEX="${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}"

die() { echo "REFUSED[$1] $2" >&2; echo "REFUSED_${LANE}_DONE"; exit "$1"; }

# D1/D3: validate inputs before anything is launched or created.
[ -f "$S/$BRIEF" ] || die 3 "brief not found: stage-b/$BRIEF"
case "$OUTSUB" in /*|*..*) die 3 "OUTSUB must stay inside the round: $OUTSUB" ;; esac
[ -d "$R" ] || die 3 "round directory not found: $RELROUND"

# F: the lane log must live outside the worktree; never let TMPDIR put it inside.
LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"
mkdir -p "$LOGDIR" || die 3 "cannot create lane log directory: $LOGDIR"
WTRES=$(cd "$WT" && pwd -W 2>/dev/null || cd "$WT" && pwd)
LGRES=$(cd "$LOGDIR" && pwd -W 2>/dev/null || cd "$LOGDIR" && pwd)
case "$LGRES" in "$WTRES"|"$WTRES"/*) die 3 "lane log dir resolves inside the worktree: $LGRES" ;; esac

cd "$WT" || die 3 "cannot enter worktree"

commit_all() {
  git add -A -- "$RELROUND" 2>/dev/null
  if ! git diff --cached --quiet 2>/dev/null; then
    git -c user.email="$EMAIL" -c user.name="$NAME" commit -q -m "$1" >/dev/null 2>&1 || true
  fi
}

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
commit_all "chore(s4post-b): commit harness artifacts before the ${LANE} lane handover"
DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
[ "$DIRTY" -eq 0 ] || die 2 "worktree not clean before handover: $DIRTY path(s); refusing to launch ${LANE}"
echo "PREFLIGHT_CLEAN HEAD=$(git rev-parse --short HEAD)"

# D3: round-relative only.
mkdir -p "$R/$OUTSUB" || die 3 "cannot create round-relative output dir: $OUTSUB"

case "$LANE" in
  AO*) MODEL="gpt-6.1-sol"; PROV="openai"; EFF="medium" ;;
  *)   MODEL="opencode-go/deepseek-v4.1-flash"; PROV="opencode-go"; EFF="high" ;;
esac
LOG="$LOGDIR/${LANE}_${STAMP}.log"; LOGEXIT="$LOG.exit"
echo "${LANE}_LANE=${STAMP} MODEL=${MODEL} provider=${PROV} reasoning=${EFF} (declared)"
printf 'LANE=%s\nMODEL=%s\nPROVIDER=%s\nEFFORT=%s\nSTAMP=%s\nWT=%s\n' \
  "$LANE" "$MODEL" "$PROV" "$EFF" "$STAMP" "$WT" > "$S/${LANE}_${STAMP}.manifest"

timeout 5400 "$CODEX" exec --cd "$WT" --sandbox workspace-write \
  -m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"" \
  -c "model_supports_reasoning_summaries=true" --skip-git-repo-check \
  - < "$S/$BRIEF" > "$LOG" 2>&1
CODE=$?
echo "$CODE" > "$LOGEXIT"
echo "${LANE} exit=${CODE} log=${LOG}"

# D1: never claim a copy that did not happen.
COPY_OK=0
if [ -f "$LOG" ]; then
  if cp "$LOG" "$S/${LANE}_${STAMP}.log"; then
    COPY_OK=1
    cp "$LOGEXIT" "$S/${LANE}_${STAMP}.exit" 2>/dev/null || true
  fi
fi
if [ "$COPY_OK" -eq 1 ]; then
  MSG="evidence(s4post-b): ${LANE} lane output ${STAMP} (lane log copied in from outside the worktree; child exit ${CODE})"
else
  MSG="evidence(s4post-b): ${LANE} lane METADATA ONLY ${STAMP} - no lane log was copied into the tree (child exit ${CODE}); do not read this as a completed lane"
  echo "POSTFLIGHT_LOG_COPY_FAILED log=$LOG" >&2
fi
commit_all "$MSG"

# D2: detected dirt is a failure, not a note.
DIRTY2=$(git status --porcelain 2>/dev/null | wc -l)
echo "POSTFLIGHT:dirty=$DIRTY2 HEAD=$(git rev-parse --short HEAD)"
echo "${LANE}_LANE_DONE"

# Propagation. Any of these makes the handover untrustworthy even if the child succeeded.
[ "$COPY_OK" -eq 1 ] || exit 4
[ "$DIRTY2" -eq 0 ] || exit 5
exit "$CODE"
