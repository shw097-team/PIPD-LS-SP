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

if [ "${GATE_SKIP_QUALIFY:-0}" = "1" ]; then
  echo "QUALIFICATION_SKIPPED_BY_ENV (testing switch; a lane admitted this way is NOT qualified)"
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
    if [ "$QC" -ne 0 ] || ! grep -q 'Q1_OK' "$QLOG" || ! grep -q 'Q2_OK' "$QLOG"; then
      echo "QUALIFICATION_FAILED model=$REQ_MODEL effort=$REQ_EFF attempt=$((k+1))/$RUNS exit=$QC log=$QLOG"
      echo "GATE_REFUSED_NO_WRITERS_STARTED"; exit 7
    fi
    echo "  qualification attempt $((k+1))/$RUNS PASS"
    k=$((k+1))
  done
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
  LANE_TOKEN="$TOKEN" LANE_INDEX="$i" LANE_MODEL="$REQ_MODEL" LANE_PROVIDER="$REQ_PROV" LANE_EFFORT="$REQ_EFF" \
    LANE_SANDBOX="${LANE_SANDBOX:-workspace-write}" ROUTE_STYLE="$ROLE_STYLE" ROUTE_CATALOG="$ROUTE_CATALOG" \
    ROUTE_BASE_URL="$ROUTE_BASE_URL" GATE_STUB_EXITS="${GATE_STUB_EXITS:-}" \
    bash "$S/run_lane.sh" "$LANE" "$B" "$OUTSUB"
  C=$?
  echo "CHILD lane=$LANE index=$i exit=$C"
  [ "$C" -eq 0 ] || FAILED=1
  # The receipt is per launch, so an older receipt cannot satisfy this check.
  if [ ! -f "$S/${LANE}_${TOKEN}.receipt" ]; then echo "CHILD_RECEIPT_MISSING lane=$LANE token=$TOKEN"; MISSING=1; fi
  i=$((i+1))
done

if [ "$FAILED" -ne 0 ] || [ "$MISSING" -ne 0 ]; then
  echo "LANE_SET_FAILED children_ok=$((i-FAILED)) any_child_nonzero=$FAILED missing_receipt=$MISSING model=$REQ_MODEL effort=$REQ_EFF"
  exit 8
fi
echo "LANE_SET_OK lanes=$i model=$REQ_MODEL effort=$REQ_EFF route=$ROLE_STYLE"
