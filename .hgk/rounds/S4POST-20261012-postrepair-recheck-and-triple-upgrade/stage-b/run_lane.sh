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

# round-6 M7 hygiene: this script must not depend on shell start-up files a caller can seed.
unset BASH_ENV ENV

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
# R3 + round-6 M2/M3. The old form was
#   git diff --cached --name-only | grep -v "^${RELROUND}/"
# which had two fail-open holes an independent officer demonstrated:
#   * the "." in ".hgk" is a REGEX WILDCARD there, so a staged "Xhgk/rounds/.../outside.txt"
#     read as inside the round and was committed;
#   * a FAILED "git diff --cached --name-only" produced empty output, which read as "nothing
#     is staged outside the round".
# Fixed-string prefix matching via case, and the query's own exit status is checked.
staged_outside() {
  local out rc
  out="$(git diff --cached --name-only 2>/dev/null)"; rc=$?
  [ "$rc" -eq 0 ] || { echo "__STAGED_QUERY_FAILED__"; return; }
  # Two separate holes were demonstrated here, so both are closed explicitly:
  #   * a regex prefix ("^${RELROUND}/") treats the "." in ".hgk" as a wildcard;
  #   * `grep -v -F -- "${RELROUND}/"` fixes that but searches ANYWHERE in the line, so a staged
  #     "prefix/.hgk/rounds/<round>/outside.txt" is admitted and committed while the wrapper
  #     returns 0 (independent officer round 8, smallest counterexample).
  # A case pattern with a QUOTED variable is a literal, ANCHORED prefix match, which is what this
  # check always meant to be. The comment previously claimed "via case" while the code used grep;
  # the code now matches the comment.
  printf '%s\n' "$out" | sed '/^[[:space:]]*$/d' | while IFS= read -r _p; do
    case "$_p" in
      "$RELROUND"/*) ;;
      *) printf '%s\n' "$_p" ;;
    esac
  done
}
commit_all() {
  git add -A -- "$RELROUND" 2>/dev/null || { echo "GIT_ADD_FAILED" >&2; return 1; }
  local outside; outside="$(staged_outside)"
  case "$outside" in
    *__STAGED_QUERY_FAILED__*) echo "STAGED_QUERY_FAILED_REFUSED: the index could not be enumerated" >&2; return 1 ;;
  esac
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
CONTAIN="${LANE_PY:-python}"
INSIDE="$("$CONTAIN" - "$LOGDIR" "$WT" <<'EOPY' 2>/dev/null
import os, sys
d = os.path.realpath(sys.argv[1]); w = os.path.realpath(sys.argv[2])
d = os.path.normcase(d).rstrip(os.sep); w = os.path.normcase(w).rstrip(os.sep)
print("INSIDE" if (d == w or d.startswith(w + os.sep)) else "OUTSIDE")
EOPY
)"
# FCR-004: the lexical comparison above is defeated by a Windows junction. The shell's resolver does not
# resolve one; the OS resolver does, so the containment test is made against realpath as well.
# Fail CLOSED: if the resolver cannot decide, the containment is unproven, and an unproven containment is
# how round 11 got a gate to qualify while writing through a junction into the clone.
case "$INSIDE" in
  INSIDE)  die 3 "lane log dir resolves inside the worktree (realpath): $LOGDIR" ;;
  OUTSIDE) : ;;
  *)       die 3 "containment undecided by the OS resolver: log dir=$LOGDIR worktree=$WT" ;;
esac

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

# round-6 M7: the route must not be trusted from an environment a caller can seed (BASH_ENV).
# When a role is given, the child derives the expected model/effort/route from the assignment
# file itself and refuses any mismatch, so a startup-file override cannot restore the
# "qualified one route, launched another" defect.
LANE_ROLE="${LANE_ROLE:-}"
if [ -n "$LANE_ROLE" ]; then
  AEXP="$(python -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print(r['model'],r['reasoning_effort'],r.get('route',{}).get('style','openai'),r['provider'],r.get('route',{}).get('catalog',''),r.get('route',{}).get('base_url',''))" "$S/ROUND_ASSIGNMENT.json" "$LANE_ROLE" 2>/dev/null)" \
    || die 3 "cannot read the assignment for role $LANE_ROLE"
  [ -n "$AEXP" ] || die 3 "role $LANE_ROLE is not in the assignment"
  read -r A_MODEL A_EFF A_STYLE A_PROV A_CAT A_BASE <<< "$AEXP"
fi

if [ -n "$LANE_ROLE" ]; then
  # A roled lane takes EVERY default from the assignment - model, provider, effort and route. Deriving them
  # from the lane's name instead made the child disagree with the assignment the moment a lane was honest
  # about its role: the checker wrapper states VERIFY and the lane is named FO*, so the name-derived effort
  # (high) contradicted the assigned one (medium) and refused every run.
  DEF_MODEL="$A_MODEL"; DEF_PROV="$A_PROV"; DEF_EFF="$A_EFF"; DEF_STYLE="$A_STYLE"
else
  case "$LANE" in
    AO*) DEF_MODEL="gpt-6.1-sol"; DEF_PROV="openai"; DEF_EFF="medium"; DEF_STYLE="openai" ;;
    *)   DEF_MODEL="opencode-go/deepseek-v4.1-flash"; DEF_PROV="opencode-go"; DEF_EFF="high"; DEF_STYLE="catalog" ;;
  esac
fi
MODEL="${LANE_MODEL:-$DEF_MODEL}"; PROV="${LANE_PROVIDER:-$DEF_PROV}"; EFF="${LANE_EFFORT:-$DEF_EFF}"
STYLE="${ROUTE_STYLE:-${DEF_STYLE:-openai}}"    # an unset caller route follows the assignment
# A governed lane is defined by its role: the role names the only source of truth for the model, provider
# and effort. Without it the check below is skipped entirely, which is how an unassigned model was admitted.
[ -n "$LANE_ROLE" ] || die 3 "LANE_ROLE is required: an unroled lane cannot be checked against the assignment"
SANDBOX_MODE="${LANE_SANDBOX:-workspace-write}"

# R5: a slug like "opencode-go/deepseek-v4.1-flash" is a CATALOG ENTRY, not a provider id. The caller
# must state the route; the gate passes the role's route so a writer can never be launched through a
# route the qualification did not exercise.
if [ -n "$LANE_ROLE" ]; then
  # The child must not simply be told what to use; it derives the expected values and refuses a
  # mismatch. An exception is allowed only when the owner-decision record itself names the exact
  # deviating model or effort, so the gate's authorisation and the child's check cannot disagree.
  OWNERF="$S/OWNER_DECISION_MODEL_DEVIATION.md"
  if [ "$MODEL" = "$A_MODEL" ]; then
    :
  elif ! printf '%s' "$MODEL" | grep -qE '^[A-Za-z0-9._/:+-]+$'; then
    # round 8: "grep -qx "authorizes: $MODEL"" is a BRE, so LANE_MODEL='.*' matched the line and
    # was reported as owner-authorised although no such value exists in the record. A value that is
    # not a plain identifier cannot be an authorised model name, so it is refused before matching.
    die 6 "model is not a plain identifier: env=$MODEL"
  elif [ -f "$OWNERF" ] && grep -Fqx -- "authorizes_model: $LANE_ROLE $MODEL" "$OWNERF"; then
    echo "CHILD_OWNER_AUTHORISED_DEVIATION model=$MODEL assignment=$A_MODEL"
  else
    die 6 "model mismatch with the assignment and not owner-authorised: env=$MODEL assignment=$A_MODEL"
  fi
  if [ "$PROV" = "$A_PROV" ]; then
    :
  elif ! printf '%s' "$PROV" | grep -qE '^[A-Za-z0-9._+-]+$'; then
    die 6 "provider is not a plain identifier: env=$PROV"
  elif [ -f "$OWNERF" ] && grep -Fqx -- "authorizes_provider: $LANE_ROLE $PROV" "$OWNERF"; then
    echo "CHILD_OWNER_AUTHORISED_PROVIDER provider=$PROV assignment=$A_PROV"
  else
    die 6 "provider mismatch with the assignment and not owner-authorised: env=$PROV assignment=$A_PROV"
  fi
  if [ "$EFF" = "$A_EFF" ]; then
    :
  elif ! printf '%s' "$EFF" | grep -qE '^[A-Za-z0-9._+-]+$'; then
    die 6 "effort is not a plain identifier: env=$EFF"
  elif [ -f "$OWNERF" ] && grep -Fqx -- "authorizes_effort: $LANE_ROLE $EFF" "$OWNERF"; then
    echo "CHILD_OWNER_AUTHORISED_EFFORT effort=$EFF assignment_effort=$A_EFF"
  else
    die 6 "effort mismatch with the assignment and not owner-authorised: env=$EFF assignment=$A_EFF"
  fi
  if [ "$STYLE" != "$A_STYLE" ]; then
    # The route is a fourth axis: the owner's checker ruling runs the backup through the catalog route
    # although the VERIFY role is assigned the plain one, so it must be named here like any other axis.
    if [ -f "$OWNERF" ] && grep -Fqx -- "authorizes_route: $LANE_ROLE $STYLE" "$OWNERF"; then
      echo "CHILD_OWNER_AUTHORISED_ROUTE route=$STYLE assignment=$A_STYLE"
    else
      die 6 "route mismatch with the assignment and not owner-authorised: env=$STYLE assignment=$A_STYLE"
    fi
  fi
fi
if [ "$STYLE" = "catalog" ]; then
  INV=(-c "model=$MODEL" -c "model_reasoning_effort=\"$EFF\""
       -c "openai_base_url=${ROUTE_BASE_URL:-${A_BASE:-http://127.0.0.1:10102/v1}}"
       -c "model_catalog_json=${ROUTE_CATALOG:-${A_CAT:?the catalog route needs a catalog}}")
else
  INV=(-m "$MODEL" -c "model_provider=\"$PROV\"" -c "model_reasoning_effort=\"$EFF\"")
fi

# A: the manifest is written OUTSIDE the worktree and copied in at postflight.
LOG="$LOGDIR/${LANE}_${STAMP}.log"; LOGEXIT="$LOG.exit"; MAN="$LOGDIR/${LANE}_${STAMP}.manifest"
echo "${LANE}_LANE=${STAMP} MODEL=${MODEL} provider=${PROV} reasoning=${EFF} route=$STYLE (declared)"
printf 'LANE=%s\nMODEL=%s\nPROVIDER=%s\nEFFORT=%s\nSTAMP=%s\nTOKEN=%s\nWT=%s\nROUTE_STYLE=%s\nSANDBOX=%s\n' \
  "$LANE" "$MODEL" "$PROV" "$EFF" "$STAMP" "$TOKEN" "$WT" "$STYLE" "$SANDBOX_MODE" > "$MAN"

timeout 5400 "$CODEX" "${INV[@]}" exec --cd "$WT" --sandbox "$SANDBOX_MODE" --skip-git-repo-check \
  - < "$S/$BRIEF" > "$LOG" 2>&1
CODE=$?
{ [ -f "$LOG" ] && printf 'child_exit=%s\n' "$CODE" > "$LOGEXIT"; } || printf 'child_exit=%s\n' "$CODE" > "$LOGEXIT"
echo "${LANE} exit=${CODE} log=${LOG}"

# D1/R1: never claim or accept a copy that did not happen; a failed receipt copy is fatal.
COPY_OK=0; RECEIPT_OK=0; MAN_OK=0
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

# round-6 M1: the previous version wrote the manifest outside the worktree and then never
# copied it in, while its documentation claimed a postflight copy. Copy it, and fail if not.
if cp "$MAN" "$S/${LANE}_${STAMP}.manifest" 2>/dev/null; then MAN_OK=1; fi
[ "$MAN_OK" -eq 1 ] || echo "POSTFLIGHT_MANIFEST_COPY_FAILED manifest=$MAN" >&2

POSTFAIL=0
commit_all "$MSG" || POSTFAIL=1

# round-6 M5: a receipt whose write silently failed (for example the destination exists as a
# DIRECTORY) was still announced as written, and round-6 M6 showed the gate must also validate
# the receipt's CONTENT, so this writes a token-tagged body only when the write is verified.
REC="$S/${LANE}_${TOKEN}.receipt"; RECEIPT_WRITE=0
if [ "$COPY_OK" -eq 1 ] && [ "$RECEIPT_OK" -eq 1 ] && [ "$MAN_OK" -eq 1 ]; then
  if [ -e "$REC" ]; then
    echo "RECEIPT_ALREADY_EXISTS_REFUSED $REC" >&2
  elif printf 'lane=%s\nstamp=%s\ntoken=%s\nchild_exit=%s\nmodel=%s\nroute=%s\nqualified=%s\n' \
        "$LANE" "$STAMP" "$TOKEN" "$CODE" "$MODEL" "${ROUTE_STYLE:-openai}" "${QUALIFIED:-no}" > "$REC" \
       && [ -f "$REC" ] && [ -s "$REC" ]; then
    RECEIPT_WRITE=1
    commit_all "evidence(s4post-b): ${LANE} lane receipt ${TOKEN} (child exit ${CODE})" \
      || { echo "RECEIPT_COMMIT_FAILED" >&2; POSTFAIL=1; }
  else
    echo "RECEIPT_WRITE_FAILED $REC" >&2
  fi
fi
[ "$RECEIPT_WRITE" -eq 1 ] || echo "NO_RECEIPT_WRITTEN" >&2

# round-6 M4: the FINAL status query happens AFTER the receipt commit, and only this result is
# reported. Previously the query ran before that commit, so a post-commit hook could leave dirt
# while the wrapper still printed the earlier "dirty=0" and returned 0.
# round 8: the HEAD read is taken FIRST. It was previously the last command to run, so a caller
# who exported a "git" function that writes a file could install dirt AFTER the status query and
# still see POSTFLIGHT:dirty=0 and exit 0. Nothing executable now runs after the query.
HEADV="$(git rev-parse --short HEAD 2>/dev/null)"; [ -n "$HEADV" ] || HEADV=UNKNOWN
DIRTY2="$(status_count)"
[ "$DIRTY2" != "ERR" ] || { echo "POSTFLIGHT_STATUS_FAILED" >&2; POSTFAIL=1; }
if [ "$DIRTY2" != "ERR" ] && [ "$DIRTY2" -ne 0 ]; then
  echo "POSTFLIGHT_DIRTY_REJECTED: $DIRTY2 path(s) still untracked after every commit" >&2; POSTFAIL=1
fi
echo "POSTFLIGHT:dirty=$DIRTY2 HEAD=$HEADV"
echo "${LANE}_LANE_DONE"

[ "$COPY_OK" -eq 1 ] || exit 4
[ "$RECEIPT_OK" -eq 1 ] || exit 6
[ "$MAN_OK" -eq 1 ] || exit 6
[ "$RECEIPT_WRITE" -eq 1 ] || exit 6
[ "$POSTFAIL" -eq 0 ] || exit 5
exit "$CODE"
