#!/usr/bin/env bash
# Governed lane-set launcher with a fail-closed model/effort admission gate.
#
# Implements the prevention the FAR study asked for after the EXECUTE lane produced
# candidates on a model other than the one the owner assigned:
#   1. the per-role model AND effort assignment is immutable (ROUND_ASSIGNMENT.json);
#   2. a requested model/effort that differs is REFUSED unless an owner-decision record
#      names that exact model - no automatic substitution, no retry-on-failure;
#   3. a same-configuration qualification must first survive TWO tool round trips
#      through the identical CLI/endpoint/model/effort with no write permission, because
#      that multi-turn continuation is precisely what failed;
#   4. child exits are aggregated, and a child without its run receipt is a failure.
# The gate never relabels an artifact and never claims to authenticate the upstream model.
#
# Usage: run_lanes_gated.sh <EXECUTE|VERIFY> <brief> [brief ...]
# Exit: 3 usage/input refused; 6 model deviation without owner decision; 7 qualification
#       failed; 8 the lane set had a failing child or a missing receipt.
set -u

ROLE="${1:-}"; [ -n "$ROLE" ] || { echo "REFUSED[3] usage: run_lanes_gated.sh <EXECUTE|VERIFY> <brief>..." >&2; exit 3; }
shift
[ "$#" -ge 1 ] || { echo "REFUSED[3] no briefs given" >&2; exit 3; }

WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
RELROUND=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
R="$WT/$RELROUND"; S="$R/stage-b"
ASSIGN="$S/ROUND_ASSIGNMENT.json"; OWNERFILE="$S/OWNER_DECISION_MODEL_DEVIATION.md"
LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"; mkdir -p "$LOGDIR"
OUTSUB="${GATE_OUTSUB:-verify/gate}"
PDF="${GATE_PY:-python}"

[ -f "$ASSIGN" ] || { echo "REFUSED[3] assignment missing: ROUND_ASSIGNMENT.json" >&2; exit 3; }
READ="$( "$PDF" -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print(r['model'],r['provider'],r['reasoning_effort'])" "$ASSIGN" "$ROLE" 2>/dev/null )" \
  || { echo "REFUSED[3] cannot read the assignment for role $ROLE" >&2; exit 3; }
[ -n "$READ" ] || { echo "REFUSED[3] role $ROLE is not in the assignment" >&2; exit 3; }
read -r A_MODEL A_PROV A_EFF <<< "$READ"
echo "ASSIGNMENT role=$ROLE model=$A_MODEL provider=$A_PROV effort=$A_EFF"

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
if [ "${GATE_SKIP_QUALIFY:-0}" = "1" ]; then
  echo "QUALIFICATION_SKIPPED_BY_ENV"
else
  # Two qualifications in the same second collided on one path and the second overwrote
# the first, destroying the evidence of the first one. Role, sanitised model and pid now
# make the name unique; keep the log even when the gate refuses.
QSAFE="$(printf %s "$REQ_MODEL" | tr -c "A-Za-z0-9._-" "_")"
  QLOG="$LOGDIR/qual-$(date -u +%Y%m%dT%H%M%SZ)-$$-${ROLE}-${QSAFE}.log"
  # Same route as the writers: a catalog slug is not a provider id. Qualifying through a
  # different route would test a different lane than the one about to be trusted.
  ROLE_STYLE="$( "$PDF" -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print(r.get('route',{}).get('style','openai'))" "$ASSIGN" "$ROLE" 2>/dev/null )"
  if [ "$ROLE_STYLE" = "catalog" ]; then
    QINV=(-c "model=$REQ_MODEL" -c "model_reasoning_effort=\"$REQ_EFF\""
          -c "openai_base_url=${ROUTE_BASE_URL:-http://127.0.0.1:10102/v1}"
          -c "model_catalog_json=${ROUTE_CATALOG:-C:/Users/user/.codex/desktop-model-catalog.json}")
  else
    QINV=(-m "$REQ_MODEL" -c "model_provider=\"$REQ_PROV\"" -c "model_reasoning_effort=\"$REQ_EFF\"")
  fi
  echo "QUALIFICATION_ROUTE style=$ROLE_STYLE model=$REQ_MODEL effort=$REQ_EFF"
  # The failure this gate exists to catch is INTERMITTENT: the assigned model completed
  # both tool calls and was then rejected at the next request with the thinking-replay
  # 400 on a 479-token transcript, on roughly half of attempts. One pass is therefore
  # not a qualification. Require RUNS consecutive passes, and say so in the record.
  RUNS="${GATE_QUALIFY_RUNS:-3}"; k=0
  while [ "$k" -lt "$RUNS" ]; do
    QLOG="$LOGDIR/qual-$(date -u +%Y%m%dT%H%M%SZ)-$$-${ROLE}-r$((k+1))-${QSAFE}.log"
    timeout 900 "$BIN" "${QINV[@]}" exec --cd "$WT" --sandbox read-only --skip-git-repo-check \
      - < "$S/GATE_QUALIFICATION_BRIEF.md" > "$QLOG" 2>&1
    QC=$?
    if [ "$QC" -ne 0 ] || ! grep -q 'Q1_OK' "$QLOG" || ! grep -q 'Q2_OK' "$QLOG"; then
      echo "QUALIFICATION_FAILED model=$REQ_MODEL effort=$REQ_EFF attempt=$((k+1))/$RUNS exit=$QC log=$QLOG"
      echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 7
    fi
    echo "  qualification attempt $((k+1))/$RUNS PASS"
    k=$((k+1))
  done
  echo "QUALIFICATION_PASSED model=$REQ_MODEL effort=$REQ_EFF (consecutive_runs=$RUNS, two tool round trips each)"
fi

# A dry gate: prove the lane is usable BEFORE any writer is assigned to it. No child runs.
if [ "${GATE_QUALIFY_ONLY:-0}" = "1" ]; then
  echo "GATE_QUALIFICATION_ONLY_OK role=$ROLE model=$REQ_MODEL effort=$REQ_EFF"
  exit 0
fi

i=0; FAILED=0; MISSING=0
for B in "$@"; do
  [ -f "$S/$B" ] || { echo "REFUSED[3] brief not found: stage-b/$B" >&2; echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 3; }
  LANE="$(basename "$B" .md | tr 'a-z' 'A-Z' | tr -c 'A-Z0-9' '_' | cut -c1-14)"
  LANE_INDEX="$i" LANE_MODEL="$REQ_MODEL" LANE_PROVIDER="$REQ_PROV" LANE_EFFORT="$REQ_EFF" \
    LANE_SANDBOX="${LANE_SANDBOX:-workspace-write}" GATE_STUB_EXITS="${GATE_STUB_EXITS:-}" \
    bash "$S/run_lane.sh" "$LANE" "$B" "$OUTSUB"
  C=$?
  echo "CHILD lane=$LANE index=$i exit=$C"
  [ "$C" -eq 0 ] || FAILED=1
  if ! ls "$S/${LANE}"_*.exit >/dev/null 2>&1; then echo "CHILD_RECEIPT_MISSING lane=$LANE"; MISSING=1; fi
  i=$((i+1))
done

if [ "$FAILED" -ne 0 ] || [ "$MISSING" -ne 0 ]; then
  echo "LANE_SET_FAILED children_ok=$((i-FAILED)) any_child_nonzero=$FAILED missing_receipt=$MISSING model=$REQ_MODEL effort=$REQ_EFF"
  exit 8
fi
echo "LANE_SET_OK lanes=$i model=$REQ_MODEL effort=$REQ_EFF"
