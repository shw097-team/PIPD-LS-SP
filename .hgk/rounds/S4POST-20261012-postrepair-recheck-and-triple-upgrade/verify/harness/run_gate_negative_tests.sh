#!/usr/bin/env bash
# Negative tests for the model/effort admission gate (run_lanes_gated.sh).
# External clone only; the Codex binary is replaced by stubs, so nothing is launched
# and no model call is spent.
set -u
WT="${LANE_WT:?LANE_WT must be the delivery worktree}"
BASE="${NT_BASE:-C:/Users/user/AppData/Local/Temp/nt-gate}"; CLONE="$BASE/clone"; LOGD="$BASE/logs"
rm -rf "$BASE"; mkdir -p "$LOGD"
SHA="$(git -C "$WT" rev-parse HEAD)" || { echo HEAD_UNRESOLVED; exit 9; }
git clone -q --no-hardlinks "$WT" "$CLONE" 2>/dev/null || { echo CLONE_FAILED; exit 9; }
git -C "$CLONE" checkout -q "$SHA" || { echo CHECKOUT_FAILED; exit 9; }
git -C "$CLONE" config user.email nt@local.invalid; git -C "$CLONE" config user.name nt
REL=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"; S="$CLONE/$REL/stage-b"
G="$S/run_lanes_gated.sh"; OWNER="$S/OWNER_DECISION_MODEL_DEVIATION.md"
[ -f "$G" ] || { echo GATE_NOT_IN_CLONE; exit 9; }

SBL="$BASE/stub-lane.sh"; SBQ="$BASE/stub-qualify-ok.sh"; SBQF="$BASE/stub-qualify-fail.sh"
cat > "$SBL" <<'EOF'
#!/usr/bin/env bash
echo "stub lane"
if [ "${GATE_STUB_DELETE_LOG:-0}" = "1" ]; then
  L="$(ls -t "${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"/*.log 2>/dev/null | head -1)"; [ -n "$L" ] && rm -f "$L"
fi
n="${LANE_INDEX:-0}"; v=0
for x in ${GATE_STUB_EXITS:-0}; do if [ "$n" -eq 0 ]; then v="$x"; break; fi; n=$((n-1)); done
exit "$v"
EOF
printf '#!/usr/bin/env bash\necho Q1_OK\necho Q2_OK\nexit 0\n' > "$SBQ"
printf '#!/usr/bin/env bash\necho "no qualification"\nexit 9\n' > "$SBQF"
SBARGV="$BASE/stub-argv.sh"
printf '#!/usr/bin/env bash\necho "$*" >> "${ARGV_LOG:-/dev/null}"\necho Q1_OK\necho Q2_OK\nexit 0\n' > "$SBARGV"
chmod +x "$SBL" "$SBQ" "$SBQF" "$SBARGV"

pass=0; fail=0
ck(){ if [ "$2" = "$3" ]; then echo "PASS $1 (exit=$3)"; pass=$((pass+1)); else echo "FAIL $1 expected=$2 actual=$3"; fail=$((fail+1)); fi; }
has(){ if grep -q "$2" "$3" 2>/dev/null; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }
# env, not a bare "$@": the callers pass extra NAME=VALUE assignments and env accepts
# them before the command, whereas a bare expansion tried to execute them (exit 127).
gitq(){ env TMPDIR="$LOGD" LANE_WT="$CLONE" CODEX_BIN="$SBL" GATE_BIN="$SBQ" "$@" \
         bash "$G" "${GARGS[@]}" >"$LOGD/$OUT.out" 2>&1; echo $?; }

echo "### G1 a deviating model with NO owner record is refused, zero writers"
mv "$OWNER" "$OWNER.hidden"
OUT=G1; GARGS=(EXECUTE brief_nt_a.md)
ck G1_DEVIATION_REFUSED 6 "$(gitq LANE_MODEL=opencode-go/deepseek-v4-flash GATE_SKIP_QUALIFY=1)"
has G1_names_the_decision MODEL_DEVIATION_REQUIRES_OWNER_DECISION "$LOGD/G1.out"
has G1_started_no_writer GATE_REFUSED_NO_WRITERS_STARTED "$LOGD/G1.out"
if ls "$S"/BRIEF_NT_A_*.exit >/dev/null 2>&1; then echo "FAIL G1_a_writer_ran"; fail=$((fail+1)); else echo "PASS G1_no_writer_ran"; pass=$((pass+1)); fi
mv "$OWNER.hidden" "$OWNER"

echo "### G2 the SAME deviating model, now named in the owner record, is admitted"
OUT=G2; GARGS=(EXECUTE brief_nt_a.md)
ck G2_AUTHORISED_DEVIATION_RUNS 0 "$(gitq LANE_MODEL=opencode-go/deepseek-v4-flash GATE_SKIP_QUALIFY=1)"
has G2_records_the_deviation OWNER_AUTHORISED_DEVIATION "$LOGD/G2.out"
has G2_lane_set_ok LANE_SET_OK "$LOGD/G2.out"

echo "### G3 a model that cannot survive qualification is refused before any writer"
OUT=G3; GARGS=(EXECUTE brief_nt_a.md)
ck G3_QUALIFICATION_REFUSED 7 "$(gitq GATE_BIN="$SBQF")"
has G3_names_qualification QUALIFICATION_FAILED "$LOGD/G3.out"
has G3_started_no_writer GATE_REFUSED_NO_WRITERS_STARTED "$LOGD/G3.out"

echo "### G4 children exiting 0,1,0 must aggregate to a failed lane set"
OUT=G4; GARGS=(EXECUTE brief_nt_a.md brief_nt_b.md brief_nt_c.md)
ck G4_LANE_SET_FAILED 8 "$(gitq GATE_SKIP_QUALIFY=1 GATE_STUB_EXITS='0 1 0')"
has G4_says_nonzero LANE_SET_FAILED "$LOGD/G4.out"
has G4_counts_the_failure any_child_nonzero=1 "$LOGD/G4.out"

echo "### G5 a child that loses its run receipt is a failure even if it exited 0"
OUT=G5; # Unique brief names: G4 already committed receipts for A/B in the same clone, so an
# inherited receipt would make this assertion vacuous.
GARGS=(EXECUTE brief_nt_d.md brief_nt_e.md)
ck G5_MISSING_RECEIPT_FAILS 8 "$(gitq GATE_SKIP_QUALIFY=1 GATE_STUB_DELETE_LOG=1)"
has G5_names_missing_receipt CHILD_RECEIPT_MISSING "$LOGD/G5.out"

echo "### G6 an unknown role is refused"
OUT=G6; GARGS=(BOGUS_ROLE brief_nt_a.md)
ck G6_UNKNOWN_ROLE_REFUSED 3 "$(gitq GATE_SKIP_QUALIFY=1)"

echo "### G7 the assignment model with a working qualification passes end to end"
OUT=G7; GARGS=(VERIFY brief_nt_a.md)
ck G7_HAPPY_PATH 0 "$(gitq GATE_BIN="$SBQ")"
has G7_qualification_passed QUALIFICATION_PASSED "$LOGD/G7.out"
has G7_no_deviation_notice LANE_SET_OK "$LOGD/G7.out"

echo "### G8 zero qualification attempts must NOT be advertised as a qualified lane (R4)"
OUT=G8; GARGS=(EXECUTE brief_nt_a.md)
ck G8_ZERO_RUNS_REFUSED 3 "$(gitq GATE_QUALIFY_RUNS=0)"
has G8_says_refused "REFUSED\[3\]" "$LOGD/G8.out"
if grep -q "QUALIFICATION_PASSED" "$LOGD/G8.out"; then echo "FAIL G8_claimed_qualified"; fail=$((fail+1)); else echo "PASS G8_did_not_claim_qualified"; pass=$((pass+1)); fi

echo "### G9 the writer must be launched through the route that was qualified (R5)"
ARGV_LOG="$LOGD/g9-argv.txt"; : > "$ARGV_LOG"
OUT=G9; GARGS=(EXECUTE brief_nt_a.md)
ck G9_EXECUTE_RUNS 0 "$(gitq GATE_QUALIFY_RUNS=1 GATE_BIN="$SBARGV" ARGV_LOG="$ARGV_LOG")"
if grep -q 'model=opencode-go/deepseek-v4.1-flash' "$ARGV_LOG"; then echo "PASS G9_child_used_the_catalog_slug"; pass=$((pass+1)); else echo "FAIL G9_child_used_the_catalog_slug"; fail=$((fail+1)); fi
if grep -q 'model_provider' "$ARGV_LOG"; then echo "FAIL G9_child_used_a_provider_id"; fail=$((fail+1)); else echo "PASS G9_child_did_not_use_a_provider_id"; pass=$((pass+1)); fi
if [ "$(grep -c 'model=opencode-go' "$ARGV_LOG")" -ge 2 ]; then echo "PASS G9_qualification_and_writer_agree"; pass=$((pass+1)); else echo "FAIL G9_qualification_and_writer_agree"; fail=$((fail+1)); fi

echo
echo "RESULT pass=$pass fail=$fail"
[ "$fail" -eq 0 ] || exit 1
