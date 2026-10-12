unset MSYS_NO_PATHCONV MSYS2_ARG_CONV_EXCL BASH_ENV ENV
export REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade' LANE_WT='/tmp/a8-tej03vas/subject' TMPDIR='/tmp/a8-tej03vas/logs' CODEX_BIN='/tmp/a8-tej03vas/stub.sh' GATE_BIN='/tmp/a8-tej03vas/stub.sh' GATE_QUALIFY_RUNS=1
S="$LANE_WT/$REL/stage-b"; L="$S/run_lane.sh"; G="$S/run_lanes_gated.sh"; OWNER="$S/OWNER_DECISION_MODEL_DEVIATION.md"
mkdir -p "$TMPDIR"; chmod +x "$CODEX_BIN" '/tmp/a8-tej03vas/sentinels.sh'

git() {
if [ "${1:-}" = rev-parse ] && [ "${2:-}" = --short ] && ls "$S"/LATE_*.receipt >/dev/null 2>&1; then echo dirt > LATE_DIRT.txt; fi
command git "$@"
}; export -f git
 bash "$L" LATE brief_nt.md verify/a8; c=$?; echo SUBJECT_EXIT=$c; command git status --porcelain; exit "$c"
