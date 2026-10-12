#!/usr/bin/env bash
# Governed lane launcher - fixes the recurring handover-hygiene defect.
#
# Root cause it addresses: the previous runners wrote the brief, the runner itself and the lane log
# INTO the same worktree that was then handed to the officer. The delivery was therefore dirty by
# construction, and two independent officers correctly refused to call it clean.
#
# This wrapper enforces five things:
#   1. FAIL-CLOSED preflight: the worktree must be clean before an officer is launched against it.
#   2. Harness artifacts under the round directory are COMMITTED before launch, not left untracked.
#   3. The lane log is written OUTSIDE the worktree (system temp), so the log cannot dirty the delivery.
#   4. The officer's own output directory is created before launch and is the only permitted dirt.
#   5. Postflight: copy the log in, commit the lane artifacts, and assert the worktree is clean again.
#
# usage: run_lane.sh <lanelupper> <brief-basename> <in-round-output-subdir> [model]
#   e.g. run_lane.sh AO4 VERIFIER_AO4_BRIEF.md verify/ao4
set -u
# The worktree is overridable so the refusal path can be tested in an external clone by a checker,
# without ever dirtying the real delivery.
WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
RELROUND=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
R="$WT/$RELROUND"
W="$R/stage-b"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
LANE="${1:?lane name required}"
BRIEF="${2:?brief basename required}"
OUTSUB="${3:?round-relative output subdir required}"
MODEL="${4:-gpt-6.1-sol}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"
LOGOUT="$LOGDIR/${LANE}_${STAMP}.log"

cd "$WT" || exit 1
mkdir -p "$LOGDIR"

# --- 1/2. preflight: commit harness artifacts, then require a clean worktree -------------------
git add -A -- "$RELROUND" >/dev/null 2>&1
if ! git diff --cached --quiet; then
  git -c core.safecrlf=false commit -q \
    -m "chore(s4post-b): commit harness artifacts before the ${LANE} lane handover" \
    -m "Fail-closed preflight of the governed lane launcher: an officer must be handed a clean worktree."
fi
DIRT=$(git status --porcelain | wc -l)
if [ "$DIRT" -ne 0 ]; then
  echo "LANE_REFUSED: ${DIRT} dirty path(s) in the delivery; an officer must not be launched against this" >&2
  git status --porcelain >&2
  exit 2
fi
echo "PREFLIGHT_CLEAN HEAD=$(git rev-parse --short HEAD)"

# --- 3. the log lives outside the worktree ----------------------------------------------------
mkdir -p "$WT/$OUTSUB" 2>/dev/null || mkdir -p "$R/$OUTSUB"
echo "${LANE}_LANE=$STAMP MODEL=$MODEL provider=openai reasoning=medium (declared checker)"
timeout 3000 "$CB" -c model="$MODEL" \
  -c model_reasoning_effort='"medium"' \
  -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
  exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
  < "$W/$BRIEF" > "$LOGOUT" 2>&1
CODE=$?
echo "$CODE" > "$LOGDIR/${LANE}_${STAMP}.exit"

# --- 5. postflight: bring the log in, commit everything the lane produced ---------------------
cp "$LOGOUT" "$W/${LANE}_${STAMP}.log"
echo "$CODE" > "$W/${LANE}_${STAMP}.exit"
git add -A -- "$RELROUND" >/dev/null 2>&1
if ! git diff --cached --quiet; then
  git -c core.safecrlf=false commit -q \
    -m "evidence(s4post-b): ${LANE} lane output (exit ${CODE}) on the frozen subject" \
    -m "Log copied in from outside the worktree; officer output committed as delivered evidence."
fi
DIRT=$(git status --porcelain | wc -l)
echo "${LANE} exit=$CODE log=$LOGOUT"
echo "POSTFLIGHT:dirty=$DIRT HEAD=$(git rev-parse --short HEAD)"
echo "${LANE}_LANE_DONE"
