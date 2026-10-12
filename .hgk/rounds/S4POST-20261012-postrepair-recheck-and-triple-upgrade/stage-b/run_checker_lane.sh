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
# `HTTP 400` and `malformed payload` added: round 11 demonstrated a hard failure spelled that way beside an
# incidental quota word, which the previous pattern missed and which then switched models and "succeeded".
HARD_RE='invalid_request_error|reasoning_content|flagged for possible|cybersecurity|HTTP 4[0-9][0-9]|error 4[0-9][0-9]|status 4[0-9][0-9]|malformed payload'

# Every wrapper outcome leaves a tracked record, so a successful wrapper can never return 0 with an
# untracked artefact: the failover record and the no-failover record both go through this.
# Path spelling matters: the record can be an MSYS spelling (/tmp/..) while the worktree is native (C:/..),
# and a native git cannot be handed the other spelling. Run git from the record's own directory and name it
# by basename, and normalise the directory itself.
commit_record() { # $1 file, $2 message
  local f="$1" d b
  d="$(dirname "$f")"; b="$(basename "$f")"
  command -v cygpath >/dev/null 2>&1 && d="$(cygpath -m "$d")"
  git -C "$d" add -- "$b" 2>/dev/null
  if ! git -C "$d" -c user.email=lane-harness@local.invalid -c user.name="hgk lane harness" commit -q -m "$2" 2>/dev/null; then
    echo "CHECKER_RECORD_NOT_COMMITTED $b"; return 1
  fi
  if [ -n "$(git -C "$d" status --porcelain)" ]; then
    echo "CHECKER_RECORD_DIRTY $b"; return 1
  fi
  echo "CHECKER_RECORD_COMMITTED $b"; return 0
}

REC="$S/CHECKER_FAILOVER_${LANE}.md"

attempt() { # $1 model  $2 provider  $3 route  -> runs the governed launcher, prints its stdout
  local model="$1" prov="$2" route="$3"
  if [ "$route" = "catalog" ]; then
    LANE_WT="$WT" LANE_ROLE=VERIFY LANE_MODEL="$model" LANE_PROVIDER="$prov" ROUTE_STYLE=catalog \
      ROUTE_CATALOG="$CATALOG" ROUTE_BASE_URL="$BASE_URL" \
      bash "$S/run_lane.sh" "$LANE" "$BRIEF" "$OUTSUB"
  else
    LANE_WT="$WT" LANE_ROLE=VERIFY LANE_MODEL="$model" LANE_PROVIDER="$prov" ROUTE_STYLE=openai \
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
# The classification must read the PROVIDER's own error channel, not the whole log. Round 11 was a review
# lane reading the very sources that quote a 400 and a content-filter notice, so every marker a
# whole-log matcher saw came from a quotation, not from the lane's own call - and the same weakness makes
# a genuine exhaustion unreachable in a lane that quotes quota text. Read the error lines; if the log has
# none, fall back to its last 80 lines, where a terminal provider failure lands.
ERRVIEW=""
if [ -n "$LOG1" ] && [ -f "$LOG1" ]; then
  ERRVIEW="$(mktemp)"
  grep -E '^(ERROR|error:|stream error|Codex error)' "$LOG1" > "$ERRVIEW" 2>/dev/null
  [ -s "$ERRVIEW" ] || tail -n 80 "$LOG1" > "$ERRVIEW"
fi
SIG=""
if [ -n "$ERRVIEW" ]; then
  SIG="$(grep -o -i -E "$EXHAUST_RE" "$ERRVIEW" | sort | uniq -c | sort -rn | head -5 | tr '\n' ';' )"
fi
HARD=""
[ -n "$ERRVIEW" ] && HARD="$(grep -o -i -E "$HARD_RE" "$ERRVIEW" 2>/dev/null | sort -u | tr '\n' ';')"
if [ -n "$HARD" ]; then
  # A protocol failure (an independent officer demonstrated a 400 invalid_request_error beside an
  # incidental quota word) used to switch models and then report success - the "work around a real
  # failure by switching models" the owner's ruling forbids. A hard-failure marker vetoes the switch.
  RECNF="$S/CHECKER_NOFAILOVER_${LANE}.md"
  { echo "# Checker failover NOT applied - $LANE"; echo
    echo "The primary lane failed and the failure was classified as NOT exhaustion, so no model was switched."
    echo
    echo "- lane: $LANE  primary exit: $CODE1  stamp: ${STAMP1:-unknown}"
    echo "- hard-failure markers: [$HARD]"
    echo "- exhaustion-looking markers: [$SIG]"
    echo "- classified from the provider error channel of: $LOG1 (fallback: its last 80 lines)"
  } > "$RECNF"
  commit_record "$RECNF" "evidence(s4post-b): checker no-failover record for $LANE" || exit 4
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
commit_record "$REC" "evidence(s4post-b): checker failover record for $LANE" || exit 4
echo "CHECKER_FAILOVER_RECORD $REC"

if [ "$CODE2" -eq 0 ]; then echo "CHECKER_BACKUP_OK lane=$LANE stamp=$STAMP2"; exit 0; fi
echo "CHECKER_BACKUP_FAILED lane=$LANE exit=$CODE2"; exit "$CODE2"
