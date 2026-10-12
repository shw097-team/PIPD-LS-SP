#!/usr/bin/env bash
# Governed lane-set launcher with a fail-closed model/effort admission gate (v2).
#
# Prevention for the FAR finding: the EXECUTE lanes produced candidates on a model other than the
# assigned one, and nothing in the harness refused it.
#   1. the per-role model AND effort assignment is immutable (ROUND_ASSIGNMENT.json);
#   2. a differing model/effort is REFUSED unless an owner-decision record names that exact model;
#   3. the lane must survive GATE_QUALIFY_RUNS consecutive two-tool round trips through the SAME route,
#      model and effort the writers will use - a single pass proves little when the fault is intermittent;
#   4. child exits and per-launch receipts are aggregated; any failure fails the lane set.
#
# Round-5 repairs (independent officer, ADJUDICATION B "still fails open"):
#   R4 GATE_QUALIFY_RUNS=0 printed QUALIFICATION_PASSED with zero attempts -> the count must be a
#      positive integer or the gate refuses;
#   R5 the gate qualified EXECUTE through the catalog route but launched the writers through the default
#      route, i.e. it validated one lane and started another -> the role's route is now exported to the
#      children, and a test asserts the child's argv.
#
# Exit: 3 refused usage/input; 6 model deviation without an owner decision; 7 qualification failed;
#       8 the lane set had a failing child or a missing/failed receipt.
set -u

unset BASH_ENV ENV   # round-6 M7: do not inherit a caller-seeded shell start-up file

ROLE="${1:-}"; [ -n "$ROLE" ] || { echo "REFUSED[3] usage: run_lanes_gated.sh <EXECUTE|VERIFY> <brief>..." >&2; exit 3; }
shift
[ "$#" -ge 1 ] || { echo "REFUSED[3] no briefs given" >&2; exit 3; }

WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
RELROUND=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
R="$WT/$RELROUND"; S="$R/stage-b"
ASSIGN="$S/ROUND_ASSIGNMENT.json"; OWNERFILE="$S/OWNER_DECISION_MODEL_DEVIATION.md"
LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"
# round 8: the launcher refused a log dir inside the worktree but the GATE did not, so a
# qualify-only run wrote qualification logs into the tree and still returned 0, and the mkdir
# had already created an empty in-tree directory that git does not report. Same rule, before mkdir.
nrmg() { { cd "$1" && pwd -P; } 2>/dev/null | tr 'A-Z' 'a-z'; }
WTRES="$(nrmg "$WT")"; LGRES="$(nrmg "$(dirname "$LOGDIR")")"
[ -n "$WTRES" ] && [ -n "$LGRES" ] || { echo "REFUSED[3] cannot resolve worktree/log paths for the containment check" >&2; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3; }
case "$LGRES" in "$WTRES"|"$WTRES"/*) echo "REFUSED[3] gate log dir resolves inside the worktree: $LGRES" >&2; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3 ;; esac
mkdir -p "$LOGDIR"
OUTSUB="${GATE_OUTSUB:-verify/gate}"
PDF="${GATE_PY:-python}"

[ -f "$ASSIGN" ] || { echo "REFUSED[3] assignment missing: ROUND_ASSIGNMENT.json" >&2; exit 3; }
read_role() { "$PDF" -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print($1)" "$ASSIGN" "$ROLE" 2>/dev/null; }
READ="$( "$PDF" -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print(r['model'],r['provider'],r['reasoning_effort'])" "$ASSIGN" "$ROLE" 2>/dev/null )"
[ -n "$READ" ] || { echo "REFUSED[3] role $ROLE is not in the assignment" >&2; exit 3; }
read -r A_MODEL A_PROV A_EFF <<< "$READ"
ROLE_STYLE="$(read_role "r.get('route',{}).get('style','openai')")"; ROLE_STYLE="${ROLE_STYLE:-openai}"
ROUTE_CATALOG="$(read_role "r.get('route',{}).get('catalog','C:/Users/user/.codex/desktop-model-catalog.json')")"
ROUTE_BASE_URL="$(read_role "r.get('route',{}).get('base_url','http://127.0.0.1:10102/v1')")"
echo "ASSIGNMENT role=$ROLE model=$A_MODEL provider=$A_PROV effort=$A_EFF route=$ROLE_STYLE"

REQ_MODEL="${LANE_MODEL:-$A_MODEL}"; REQ_PROV="${LANE_PROVIDER:-$A_PROV}"; REQ_EFF="${LANE_EFFORT:-$A_EFF}"
DEVIATED=0
[ "$REQ_MODEL" = "$A_MODEL" ] || DEVIATED=1
[ "$REQ_EFF" = "$A_EFF" ] || DEVIATED=1
if [ "$DEVIATED" -eq 1 ]; then
  if [ ! -f "$OWNERFILE" ]; then
    echo "MODEL_DEVIATION_REQUIRES_OWNER_DECISION requested=$REQ_MODEL/$REQ_EFF assigned=$A_MODEL/$A_EFF owner_record=MISSING"
    echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 6
  fi
  if ! grep -qx "authorizes: $REQ_MODEL" "$OWNERFILE"; then
    echo "MODEL_DEVIATION_REQUIRES_OWNER_DECISION requested=$REQ_MODEL is not named in the owner decision record"
    echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 6
  fi
  echo "OWNER_AUTHORISED_DEVIATION model=$REQ_MODEL effort=$REQ_EFF assigned=$A_MODEL/$A_EFF record=OWNER_DECISION_MODEL_DEVIATION.md"
fi

BIN="${GATE_BIN:-${CODEX_BIN:-/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe}}"
route_inv() {
  if [ "$ROLE_STYLE" = "catalog" ]; then
    printf '%s\n' -c "model=$REQ_MODEL" -c "model_reasoning_effort=\"$REQ_EFF\"" \
      -c "openai_base_url=$ROUTE_BASE_URL" -c "model_catalog_json=$ROUTE_CATALOG"
  else
    printf '%s\n' -m "$REQ_MODEL" -c "model_provider=\"$REQ_PROV\"" -c "model_reasoning_effort=\"$REQ_EFF\""
  fi
}
mapfile -t QINV < <(route_inv)

SKIP_ACK="$S/GATE_SKIP_QUALIFY_ACK.md"
if [ "${GATE_SKIP_QUALIFY:-0}" = "1" ]; then
  # round-6 M8: this was an exposed bypass - any caller could set it and admit a writer with no
  # qualification at all. It now needs an owner-visible acknowledgement file, and every lane
  # admitted this way is recorded as unqualified.
  if [ ! -f "$SKIP_ACK" ] || ! grep -q "^authorizes_skip_qualification: $ROLE$" "$SKIP_ACK"; then
    echo "QUALIFICATION_SKIP_UNAUTHORISED: GATE_SKIP_QUALIFY=1 needs GATE_SKIP_QUALIFY_ACK.md naming role $ROLE"
    echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 6
  fi
  QUALIFIED="no"; SKIPPED_UNQUALIFIED=1
  echo "QUALIFICATION_SKIPPED_BY_ENV (authorised testing switch; a lane admitted this way is NOT qualified and the receipt records qualified=$QUALIFIED)"
else
  # R4: a configurable count is an input and must be validated.
  RUNS="${GATE_QUALIFY_RUNS:-3}"
  case "$RUNS" in ''|*[!0-9]*) echo "REFUSED[3] GATE_QUALIFY_RUNS must be a positive integer, got: $RUNS"; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3 ;; esac
  [ "$RUNS" -ge 1 ] || { echo "REFUSED[3] GATE_QUALIFY_RUNS must be >= 1, got: $RUNS"; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3; }
  QSAFE="$(printf %s "$REQ_MODEL" | tr -c 'A-Za-z0-9._-' '_')"
  echo "QUALIFICATION_ROUTE style=$ROLE_STYLE model=$REQ_MODEL effort=$REQ_EFF consecutive_runs_required=$RUNS"
  k=0
  while [ "$k" -lt "$RUNS" ]; do
    QLOG="$LOGDIR/qual-$(date -u +%Y%m%dT%H%M%SZ)-$$-${ROLE}-r$((k+1))-${QSAFE}.log"
    timeout 900 "$BIN" "${QINV[@]}" exec --cd "$WT" --sandbox read-only --skip-git-repo-check \
      - < "$S/GATE_QUALIFICATION_BRIEF.md" > "$QLOG" 2>&1
    QC=$?
    # round-6 M9: the sentinels alone are just strings - a stub that prints them passed the
    # gate without performing a single tool call. Require the CLI header and at least TWO
    # successful tool executions as well. Ceiling, stated plainly: any transcript-based check
    # can still be produced by a stub, so this raises the bar and does not prove provenance.
    TOOLLINES="$(grep -c ' succeeded in ' "$QLOG" 2>/dev/null | tr -d ' ')"
    if [ "$QC" -ne 0 ] || ! grep -q 'Q1_OK' "$QLOG" || ! grep -q 'Q2_OK' "$QLOG" \
       || ! grep -q 'OpenAI Codex v' "$QLOG" || [ "${TOOLLINES:-0}" -lt 2 ]; then
      echo "QUALIFICATION_FAILED model=$REQ_MODEL effort=$REQ_EFF attempt=$((k+1))/$RUNS exit=$QC tool_execs=${TOOLLINES:-0} log=$QLOG"
      echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 7
    fi
    echo "  qualification attempt $((k+1))/$RUNS PASS"
    k=$((k+1))
  done
  QUALIFIED="yes"
  echo "QUALIFICATION_PASSED model=$REQ_MODEL effort=$REQ_EFF consecutive_runs=$RUNS route=$ROLE_STYLE"
fi

if [ "${GATE_QUALIFY_ONLY:-0}" = "1" ]; then
  echo "GATE_QUALIFICATION_ONLY_OK role=$ROLE model=$REQ_MODEL effort=$REQ_EFF"
  exit 0
fi

GATE_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
i=0; FAILED=0; MISSING=0
for B in "$@"; do
  [ -f "$S/$B" ] || { echo "REFUSED[3] brief not found: stage-b/$B" >&2; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3; }
  LANE="$(basename "$B" .md | tr 'a-z' 'A-Z' | tr -c 'A-Z0-9' '_' | cut -c1-14)"
  TOKEN="${GATE_STAMP}-${i}"
  # R5: the child is launched through the SAME route the qualification exercised.
  LANE_TOKEN="$TOKEN" LANE_INDEX="$i" LANE_ROLE="$ROLE" LANE_GATED=1 QUALIFIED="${QUALIFIED:-no}" \
    LANE_MODEL="$REQ_MODEL" LANE_PROVIDER="$REQ_PROV" LANE_EFFORT="$REQ_EFF" \
    LANE_SANDBOX="${LANE_SANDBOX:-workspace-write}" ROUTE_STYLE="$ROLE_STYLE" ROUTE_CATALOG="$ROUTE_CATALOG" \
    ROUTE_BASE_URL="$ROUTE_BASE_URL" GATE_STUB_EXITS="${GATE_STUB_EXITS:-}" \
    env -u BASH_ENV -u ENV bash "$S/run_lane.sh" "$LANE" "$B" "$OUTSUB"
  C=$?
  echo "CHILD lane=$LANE index=$i exit=$C"
  [ "$C" -eq 0 ] || FAILED=1
  # round-6 M6: existence alone was enough, so an EMPTY file or a forged, wrong-token,
  # wrong-route receipt with child_exit=99 satisfied the gate. The content is validated now.
  RCP="$S/${LANE}_${TOKEN}.receipt"
  if [ ! -f "$RCP" ] || [ ! -s "$RCP" ]; then
    echo "CHILD_RECEIPT_MISSING lane=$LANE token=$TOKEN (absent, or not a non-empty regular file)"; MISSING=1
  else
    # Exactly one line per key, carrying the expected value. Matching a line at all was not
    # enough: a duplicated conflicting line, a wrong model and a wrong qualification were all
    # accepted. Flag order is deliberate; see the guard false-positive note in HARNESS_DEFECT_LOG.
    RJ=""
    one_key() { n="$(grep -c "^$1=" "$RCP")"; [ "$n" -eq 1 ] && grep -Fqx "$1=$2" "$RCP"; }
    one_key token "$TOKEN"      || RJ="$RJ token"
    one_key lane "$LANE"        || RJ="$RJ lane"
    one_key child_exit 0        || RJ="$RJ child_exit"
    one_key route "$ROLE_STYLE" || RJ="$RJ route"
    one_key model "$REQ_MODEL"  || RJ="$RJ model"
    if [ "${SKIPPED_UNQUALIFIED:-0}" = "1" ]; then
      one_key qualified no  || RJ="$RJ qualification"
    else
      one_key qualified yes || RJ="$RJ qualification"
    fi
    if [ -n "$RJ" ]; then
      echo "CHILD_RECEIPT_INVALID lane=$LANE token=$TOKEN failed:$RJ"; MISSING=1
    fi
  fi
  i=$((i+1))
done

if [ "$FAILED" -ne 0 ] || [ "$MISSING" -ne 0 ]; then
  echo "LANE_SET_FAILED children_ok=$((i-FAILED)) any_child_nonzero=$FAILED missing_receipt=$MISSING model=$REQ_MODEL effort=$REQ_EFF"
  exit 8
fi
echo "LANE_SET_OK lanes=$i model=$REQ_MODEL effort=$REQ_EFF route=$ROLE_STYLE"
