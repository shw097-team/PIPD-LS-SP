#!/usr/bin/env bash
# Governed CHECKER lane with the owner-declared failover.
#
# Primary checker : gpt-6.1-sol, provider openai (OAuth), route openai, reasoning medium  -- as assigned.
# Backup checker  : opencode-go/glm-5.3-flash, route catalog, per the owner's ruling of 2026-10-12:
#                   "倘若 checker model：GPT 6.1 SOL-MEDIUM(OPEN AI OAuth) 用量耗盡，checker model 就改用
#                    備援：GLM-5.3-Flash(OPENCODE GO)"
#
# Rules this wrapper enforces, so the failover cannot become a convenience:
#   * the backup runs ONLY when the primary lane failed AND its log carries an exhaustion signature
#     (quota / rate limit / 429 / capacity / usage limit). A content-filter kill, a safety flag, a
#     reasoning_content 400, a control-flow bug or any other failure does NOT fail over - it is reported.
#   * every failover is written to stage-b/CHECKER_FAILOVER_<LANE>.md with the primary log path, the
#     matched signature, both models, both stamps and both exit codes. A verdict produced by the backup
#     is a verdict by a DIFFERENT checker model and must disclose that.
#   * no silent retry: one primary attempt, at most one backup attempt.
#
# Exit: 0 only if one of the two attempts succeeded; otherwise the primary's exit code.
set -u
# A caller-seeded start-up file must not be able to widen this.
unset BASH_ENV ENV

LANE="${1:-}"; BRIEF="${2:-}"; OUTSUB="${3:-}"
[ -n "$LANE" ] && [ -n "$BRIEF" ] && [ -n "$OUTSUB" ] || { echo "usage: run_checker_lane.sh <LANE> <brief> <round-relative-outsub>" >&2; exit 3; }

S="$(cd "$(dirname "$0")" && pwd)"
WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"
CATALOG="${ROUTE_CATALOG:-C:/Users/user/.codex/desktop-model-catalog.json}"
BASE_URL="${ROUTE_BASE_URL:-http://127.0.0.1:10102/v1}"

PRIMARY_MODEL="gpt-6.1-sol";           PRIMARY_PROV="openai";     PRIMARY_ROUTE="openai"
BACKUP_MODEL="opencode-go/glm-5.3-flash"; BACKUP_PROV="opencode-go"; BACKUP_ROUTE="catalog"

# Only these signatures may trigger the declared failover.
EXHAUST_RE='quota|rate.?limit|429|too many requests|usage limit|insufficient|at capacity|capacity|exceeded your current'

REC="$S/CHECKER_FAILOVER_${LANE}.md"

attempt() { # $1 model  $2 provider  $3 route  -> runs the governed launcher, prints its stdout
  local model="$1" prov="$2" route="$3"
  if [ "$route" = "catalog" ]; then
    LANE_WT="$WT" LANE_MODEL="$model" LANE_PROVIDER="$prov" ROUTE_STYLE=catalog \
      ROUTE_CATALOG="$CATALOG" ROUTE_BASE_URL="$BASE_URL" \
      bash "$S/run_lane.sh" "$LANE" "$BRIEF" "$OUTSUB"
  else
    LANE_WT="$WT" LANE_MODEL="$model" LANE_PROVIDER="$prov" ROUTE_STYLE=openai \
      bash "$S/run_lane.sh" "$LANE" "$BRIEF" "$OUTSUB"
  fi
}

echo "CHECKER_PRIMARY lane=$LANE model=$PRIMARY_MODEL route=$PRIMARY_ROUTE"
OUT1="$(attempt "$PRIMARY_MODEL" "$PRIMARY_PROV" "$PRIMARY_ROUTE")"; CODE1=$?
printf '%s\n' "$OUT1"
LOG1="$(printf '%s\n' "$OUT1" | sed -n 's/.*log=\([^ ]*\).*/\1/p' | tail -1)"
STAMP1="$(printf '%s\n' "$OUT1" | sed -n 's/^'"$LANE"'_LANE=\([0-9TZ]*\).*/\1/p' | tail -1)"

if [ "$CODE1" -eq 0 ]; then
  echo "CHECKER_PRIMARY_OK lane=$LANE stamp=$STAMP1"
  exit 0
fi

# The primary failed. Decide whether this is the exhaustion the owner's ruling covers.
SIG=""
if [ -n "$LOG1" ] && [ -f "$LOG1" ]; then
  SIG="$(grep -o -i -E "$EXHAUST_RE" "$LOG1" | sort | uniq -c | sort -rn | head -5 | tr '\n' ';' )"
fi
HARD_RE='invalid_request_error|reasoning_content|flagged for possible|cybersecurity|error 400|status 400|400 Bad Request'
HARD=""
[ -n "$LOG1" ] && [ -f "$LOG1" ] && HARD="$(grep -o -i -E "$HARD_RE" "$LOG1" 2>/dev/null | sort -u | tr '\n' ';')"
if [ -n "$HARD" ]; then
  # A protocol failure (an independent officer demonstrated a 400 invalid_request_error beside an
  # incidental quota word) used to switch models and then report success - the "work around a real
  # failure by switching models" the owner's ruling forbids. A hard-failure marker vetoes the switch.
  echo "CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION lane=$LANE exit=$CODE1 hard_failure=[$HARD] signature=[$SIG] - no failover, this is reported not worked around"
  exit "$CODE1"
fi
if [ -z "$SIG" ]; then
  echo "CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION lane=$LANE exit=$CODE1 - no failover, this is reported not worked around"
  exit "$CODE1"
fi

echo "CHECKER_PRIMARY_EXHAUSTED lane=$LANE exit=$CODE1 signature=[$SIG]"
echo "CHECKER_FAILOVER_START lane=$LANE model=$BACKUP_MODEL route=$BACKUP_ROUTE"

OUT2="$(attempt "$BACKUP_MODEL" "$BACKUP_PROV" "$BACKUP_ROUTE")"; CODE2=$?
printf '%s\n' "$OUT2"
LOG2="$(printf '%s\n' "$OUT2" | sed -n 's/.*log=\([^ ]*\).*/\1/p' | tail -1)"
STAMP2="$(printf '%s\n' "$OUT2" | sed -n 's/^'"$LANE"'_LANE=\([0-9TZ]*\).*/\1/p' | tail -1)"

{
  echo "# Checker failover record - $LANE"
  echo
  echo "The owner's ruling of 2026-10-12: if the checker model GPT 6.1 SOL-MEDIUM (OpenAI OAuth) runs out"
  echo "of quota, the checker model switches to the declared backup GLM-5.3-Flash (OPENCODE GO)."
  echo
  echo "| | model | route | stamp | child exit | lane log |"
  echo "|---|---|---|---|---|---|"
  echo "| primary | \`$PRIMARY_MODEL\` | \`$PRIMARY_ROUTE\` | \`$STAMP1\` | $CODE1 | \`$LOG1\` |"
  echo "| backup  | \`$BACKUP_MODEL\` | \`$BACKUP_ROUTE\` | \`$STAMP2\` | $CODE2 | \`$LOG2\` |"
  echo
  echo "Exhaustion signature matched in the primary log: \`$SIG\`"
  echo
  echo "**This changes the checker's identity.** Any verdict produced under the backup was produced by a"
  echo "different model than the assigned checker, and the verdict document must say so. The failover does"
  echo "not transfer, and does not create, any acceptance this round would not otherwise have."
} > "$REC"
# FCR-006: the record was written after the launcher's own postflight, so the wrapper could return
# success while the record stayed untracked. Commit it, then re-read the status, as the launcher does.
# Path spelling matters here: the record path can be an MSYS spelling (/tmp/..) while the worktree is a
# native one (C:/..), and a native git cannot be handed the other spelling. Run git from the record's own
# directory and name it by basename, so no path is translated at all.
RD="$(dirname "$REC")"; RB="$(basename "$REC")"
git -C "$RD" add -- "$RB" 2>/dev/null
if ! git -C "$RD" -c user.email=lane-harness@local.invalid -c user.name="hgk lane harness" commit -q -m "evidence(s4post-b): checker failover record for $LANE" 2>/dev/null; then
  echo "CHECKER_FAILOVER_RECORD_NOT_COMMITTED $RB"; exit 4
fi
DIRT="$(git -C "$RD" status --porcelain)"
if [ -n "$DIRT" ]; then
  echo "CHECKER_FAILOVER_RECORD_DIRTY $(printf '%s' "$DIRT" | tr '\n' ';')"; exit 4
fi
echo "CHECKER_FAILOVER_RECORD $REC"

if [ "$CODE2" -eq 0 ]; then echo "CHECKER_BACKUP_OK lane=$LANE stamp=$STAMP2"; exit 0; fi
echo "CHECKER_BACKUP_FAILED lane=$LANE exit=$CODE2"; exit "$CODE2"
