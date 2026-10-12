unset MSYS_NO_PATHCONV MSYS2_ARG_CONV_EXCL BASH_ENV ENV
export REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade' LANE_WT='/tmp/a8-tej03vas/subject' TMPDIR='/tmp/a8-tej03vas/logs' CODEX_BIN='/tmp/a8-tej03vas/stub.sh' GATE_BIN='/tmp/a8-tej03vas/stub.sh' GATE_QUALIFY_RUNS=1
S="$LANE_WT/$REL/stage-b"; L="$S/run_lane.sh"; G="$S/run_lanes_gated.sh"; OWNER="$S/OWNER_DECISION_MODEL_DEVIATION.md"
mkdir -p "$TMPDIR"; chmod +x "$CODEX_BIN" '/tmp/a8-tej03vas/sentinels.sh'

cp() { case "${@: -1}" in *.manifest) return 23;; *) command cp "$@";; esac; }; export -f cp
 bash "$L" M1FAIL brief_nt.md verify/a8; c=$?; echo SUBJECT_EXIT=$c; command git status --porcelain; exit "$c"
