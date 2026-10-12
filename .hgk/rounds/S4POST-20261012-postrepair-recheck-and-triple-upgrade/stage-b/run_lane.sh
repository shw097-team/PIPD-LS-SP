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
  local out rc p
  out="$(git diff --cached --name-only -z 2>/dev/null)"; rc=$?
  [ "$rc" -eq 0 ] || { echo "__STAGED_QUERY_FAILED__"; return; }
  printf '%s' "$out" | tr '\0' '\n' | while IFS= read -r p; do
    [ -z "$p" ] && continue
    case "$p" in
      "$RELROUND"/*) ;;
      *) printf '%s\n' "$p" ;;
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
  AEXP="$(python -c "import json,sys;r=json.load(open(sys.argv[1],encoding='utf-8'))['roles'][sys.argv[2]];print(r['model'],r['reasoning_effort'],r.get('route',{}).get('style','openai'))" "$S/ROUND_ASSIGNMENT.json" "$LANE_ROLE" 2>/dev/null)" \
    || die 3 "cannot read the assignment for role $LANE_ROLE"
  [ -n "$AEXP" ] || die 3 "role $LANE_ROLE is not in the assignment"
  read -r A_MODEL A_EFF A_STYLE <<< "$AEXP"
fi

case "$LANE" in
  AO*) DEF_MODEL="gpt-6.1-sol"; DEF_PROV="openai"; DEF_EFF="medium" ;;
  *)   DEF_MODEL="opencode-go/deepseek-v4.1-flash"; DEF_PROV="opencode-go"; DEF_EFF="high" ;;
esac
MODEL="${LANE_MODEL:-$DEF_MODEL}"; PROV="${LANE_PROVIDER:-$DEF_PROV}"; EFF="${LANE_EFFORT:-$DEF_EFF}"
SANDBOX_MODE="${LANE_SANDBOX:-workspace-write}"

# R5: a slug like "opencode-go/deepseek-v4.1-flash" is a CATALOG ENTRY, not a provider id. The caller
# must state the route; the gate passes the role's route so a writer can never be launched through a
# route the qualification did not exercise.
if [ -n "$LANE_ROLE" ]; then
  [ "$MODEL" = "$A_MODEL" ] || die 6 "model mismatch with the assignment: env=$MODEL assignment=$A_MODEL"
  [ "$EFF" = "$A_EFF" ] || die 6 "effort mismatch with the assignment: env=$EFF assignment=$A_EFF"
  [ "${ROUTE_STYLE:-openai}" = "$A_STYLE" ] || die 6 "route mismatch with the assignment: env=${ROUTE_STYLE:-openai} assignment=$A_STYLE"
fi
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
        "$LANE" "$STAMP" "$TOKEN" "$CODE" "$MODEL" "${ROUTE_STYLE:-openai}" "${QUALIFIED:-yes}" > "$REC" \
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
DIRTY2="$(status_count)"
[ "$DIRTY2" != "ERR" ] || { echo "POSTFLIGHT_STATUS_FAILED" >&2; POSTFAIL=1; }
if [ "$DIRTY2" != "ERR" ] && [ "$DIRTY2" -ne 0 ]; then
  echo "POSTFLIGHT_DIRTY_REJECTED: $DIRTY2 path(s) still untracked after every commit" >&2; POSTFAIL=1
fi
echo "POSTFLIGHT:dirty=$DIRTY2 HEAD=$(git rev-parse --short HEAD)"
echo "${LANE}_LANE_DONE"

[ "$COPY_OK" -eq 1 ] || exit 4
[ "$RECEIPT_OK" -eq 1 ] || exit 6
[ "$MAN_OK" -eq 1 ] || exit 6
[ "$RECEIPT_WRITE" -eq 1 ] || exit 6
[ "$POSTFAIL" -eq 0 ] || exit 5
exit "$CODE"
