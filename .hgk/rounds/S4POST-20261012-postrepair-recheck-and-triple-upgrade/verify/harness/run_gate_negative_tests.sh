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
# M8: GATE_SKIP_QUALIFY is a testing switch that now needs an owner-visible acknowledgement.
# This is created after S is defined; it was placed earlier once and broke the whole script.
printf 'authorizes_skip_qualification: EXECUTE\nauthorizes_skip_qualification: VERIFY\n' > "$S/GATE_SKIP_QUALIFY_ACK.md"

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
# M9: a qualification must show the CLI header and two real tool executions, not just sentinels.
cat > "$SBQ" <<'EOF'
#!/usr/bin/env bash
echo "OpenAI Codex v0.162.0-alpha.17.2"
echo "exec echo Q1 succeeded in 12ms:"
echo "exec echo Q2 succeeded in 11ms:"
echo Q1_OK
echo Q2_OK
exit 0
EOF
printf '#!/usr/bin/env bash\necho "no qualification"\nexit 9\n' > "$SBQF"
SBARGV="$BASE/stub-argv.sh"
cat > "$SBARGV" <<'EOF'
#!/usr/bin/env bash
echo "$*" >> "${ARGV_LOG:-/dev/null}"
echo "OpenAI Codex v0.162.0-alpha.17.2"
echo "exec echo Q1 succeeded in 12ms:"
echo "exec echo Q2 succeeded in 11ms:"
echo Q1_OK
echo Q2_OK
exit 0
EOF
SBONLY="$BASE/stub-sentinels-only.sh"
cat > "$SBONLY" <<'EOF'
#!/usr/bin/env bash
echo Q1_OK
echo Q2_OK
exit 0
EOF
chmod +x "$SBL" "$SBQ" "$SBQF" "$SBARGV" "$SBONLY"

pass=0; fail=0
ck(){ if [ "$2" = "$3" ]; then echo "PASS $1 (exit=$3)"; pass=$((pass+1)); else echo "FAIL $1 expected=$2 actual=$3"; fail=$((fail+1)); fi; }
has(){ if grep -qF -- "$2" "$3" 2>/dev/null; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }
hasnot(){ if grep -qF -- "$2" "$3" 2>/dev/null; then echo "FAIL $1 (found: $2)"; fail=$((fail+1)); else echo "PASS $1"; pass=$((pass+1)); fi; }
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
has G8_says_refused "REFUSED[3]" "$LOGD/G8.out"
if grep -q "QUALIFICATION_PASSED" "$LOGD/G8.out"; then echo "FAIL G8_claimed_qualified"; fail=$((fail+1)); else echo "PASS G8_did_not_claim_qualified"; pass=$((pass+1)); fi

echo "### G9 the writer must be launched through the route that was qualified (R5)"
ARGV_LOG="$LOGD/g9-argv.txt"; : > "$ARGV_LOG"
OUT=G9; GARGS=(EXECUTE brief_nt_a.md)
# CODEX_BIN too: the writer lane is launched by run_lane.sh, which uses CODEX_BIN, so
# recording only the qualification would leave the writer's argv unchecked.
ck G9_EXECUTE_RUNS 0 "$(gitq GATE_QUALIFY_RUNS=1 GATE_BIN="$SBARGV" CODEX_BIN="$SBARGV" ARGV_LOG="$ARGV_LOG")"
if grep -q 'model=opencode-go/deepseek-v4.1-flash' "$ARGV_LOG"; then echo "PASS G9_child_used_the_catalog_slug"; pass=$((pass+1)); else echo "FAIL G9_child_used_the_catalog_slug"; fail=$((fail+1)); fi
if grep -q 'model_provider' "$ARGV_LOG"; then echo "FAIL G9_child_used_a_provider_id"; fail=$((fail+1)); else echo "PASS G9_child_did_not_use_a_provider_id"; pass=$((pass+1)); fi
if [ "$(grep -c 'model=opencode-go' "$ARGV_LOG")" -ge 2 ]; then echo "PASS G9_qualification_and_writer_agree"; pass=$((pass+1)); else echo "FAIL G9_qualification_and_writer_agree"; fail=$((fail+1)); fi

echo "### G10 a truncated / empty receipt must not satisfy the gate (M6)"
HOOK="$CLONE/.git/hooks/post-commit"
printf '#!/usr/bin/env bash\nfor f in "$(git rev-parse --show-toplevel)"/.hgk/rounds/*/stage-b/*.receipt; do : > "$f"; done\n' > "$HOOK"
chmod +x "$HOOK"
OUT=G10; GARGS=(EXECUTE brief_nt_a.md)
ck G10_EMPTY_RECEIPT_REJECTED 8 "$(gitq GATE_SKIP_QUALIFY=1)"
# A truncated receipt fails the non-empty test, so the gate reports MISSING rather than
# INVALID; both are rejections and the assertion is about the rejection.
has G10_says_receipt_rejected "CHILD_RECEIPT_" "$LOGD/G10.out"
rm -f "$HOOK"

echo "### G11 GATE_SKIP_QUALIFY without an acknowledgement is refused (M8)"
mv "$S/GATE_SKIP_QUALIFY_ACK.md" "$S/GATE_SKIP_QUALIFY_ACK.md.hidden"
OUT=G11; GARGS=(EXECUTE brief_nt_a.md)
ck G11_SKIP_UNAUTHORISED_REFUSED 6 "$(gitq GATE_SKIP_QUALIFY=1)"
has G11_names_the_ack QUALIFICATION_SKIP_UNAUTHORISED "$LOGD/G11.out"
mv "$S/GATE_SKIP_QUALIFY_ACK.md.hidden" "$S/GATE_SKIP_QUALIFY_ACK.md"

echo "### G12 sentinels without tool executions are not a qualification (M9)"
OUT=G12; GARGS=(EXECUTE brief_nt_a.md)
ck G12_SENTINELS_ONLY_REFUSED 7 "$(gitq GATE_QUALIFY_RUNS=1 GATE_BIN="$SBONLY")"
has G12_names_qualification QUALIFICATION_FAILED "$LOGD/G12.out"

echo "### G13 a committed receipt with duplicated conflicting fields is refused (round-8)"
# Round 8 forged a receipt that was committed and left the tree clean, carrying model=wrong,
# qualified=no and BOTH child_exit=0/99 and route=catalog/wrong. The gate returned 0 / LANE_SET_OK.
# The hook below injects the conflicting lines and amends, so the tree stays clean; only the gate's
# own receipt validation can catch it.
HOOK="$CLONE/.git/hooks/post-commit"
# A per-file sentinel, not one global marker: the clone carries receipts from the earlier cases, so a
# global marker was set during the preflight commit (on an OLD receipt) and the current receipt was
# never touched - the gate then correctly returned 0 and the case failed for its own fixture's reason.
printf '#!/usr/bin/env bash\nT="$(git rev-parse --show-toplevel)"\nfor f in "$T"/.hgk/rounds/*/stage-b/*.receipt; do\n  [ -f "$f" ] || continue\n  grep -q "^INJECTED=1$" "$f" && continue\n  printf "child_exit=99\\nroute=wrong\\nmodel=wrong-model\\nqualified=no\\nINJECTED=1\\n" >> "$f"\n  git add "$f"\n  git commit --amend --no-edit -q\ndone\nexit 0\n' > "$HOOK"
chmod +x "$HOOK"
OUT=G13; GARGS=(EXECUTE brief_nt_a.md)
ck G13_CONFLICTING_RECEIPT_REJECTED 8 "$(gitq GATE_SKIP_QUALIFY=1)"
has G13_names_the_receipt CHILD_RECEIPT_INVALID "$LOGD/G13.out"
rm -f "$HOOK"

echo "### G14 owner authorisation is per role, plain-valued and covers the provider axis (round-10)"
# Round 10 demonstrated: `.*` was "named" by any record (BRE match), an EXECUTE-scoped exception
# authorised a VERIFY lane, an unassigned provider bypassed the check, and effort was never checked.
OWNERBAK="$LOGD/owner.bak"; cp "$OWNER" "$OWNERBAK"
OUT=G14a; GARGS=(EXECUTE brief_nt_a.md)
ck G14a_REGEX_MODEL_REFUSED 6 "$(gitq LANE_MODEL='.*' GATE_SKIP_QUALIFY=1)"
has G14a_names_the_axis MODEL_DEVIATION_REQUIRES_OWNER_DECISION "$LOGD/G14a.out"
OUT=G14b; GARGS=(VERIFY brief_nt_a.md)
ck G14b_ROLE_CROSSING_REFUSED 6 "$(gitq LANE_MODEL=opencode-go/deepseek-v4-flash GATE_SKIP_QUALIFY=1)"
has G14b_names_the_axis "axis=model role=VERIFY" "$LOGD/G14b.out"
OUT=G14c; GARGS=(EXECUTE brief_nt_a.md)
ck G14c_PROVIDER_OVERRIDE_REFUSED 6 "$(gitq LANE_PROVIDER=unassigned GATE_SKIP_QUALIFY=1)"
has G14c_names_the_axis "axis=provider" "$LOGD/G14c.out"
OUT=G14d; GARGS=(EXECUTE brief_nt_a.md)
ck G14d_UNDECLARED_EFFORT_REFUSED 6 "$(gitq LANE_EFFORT=minimal GATE_SKIP_QUALIFY=1)"
has G14d_names_the_axis "axis=effort" "$LOGD/G14d.out"
# positive control: the role's own authorised value is still admitted, so the mechanism is a scope and
# not a blanket refusal
OUT=G14e; GARGS=(EXECUTE brief_nt_a.md)
ck G14e_AUTHORISED_VALUE_STILL_RUNS 0 "$(gitq LANE_MODEL=opencode-go/deepseek-v4-flash LANE_EFFORT=none GATE_SKIP_QUALIFY=1)"
has G14e_records_the_axes "axes=[ model effort]" "$LOGD/G14e.out"

echo "### G15 a log directory reached through a Windows junction is refused (round-10)"
# Round 10 showed the lexical pwd -P containment test is defeated by a junction; the gate wrote its
# log INSIDE the worktree and returned 0.
LJ="$LOGD/junction-in"; rm -rf "$LJ"; mkdir -p "$LJ"
JUNC="$LJ/j"; JUNC_PY="${GATE_PY:-python}"
# Create it with an API that does not go through the shell: `cmd //c mklink //J` returned success and
# created nothing here, which made the case pass because the path could not be RESOLVED rather than
# because the containment rule caught a junction - a false PASS.
"$JUNC_PY" - "$JUNC" "$CLONE" <<'EOPY' >/dev/null 2>&1
import os, subprocess, sys
link, target = sys.argv[1], sys.argv[2]
try:
    os.symlink(target, link, target_is_directory=True)
except Exception:
    r = subprocess.run(["cmd", "/c", "mklink", "/J", link.replace("/", "\\"), target.replace("/", "\\")], capture_output=True)
    if r.returncode != 0:
        sys.exit(1)
sys.exit(0 if os.path.isdir(link) else 1)
EOPY
if [ -d "$JUNC" ]; then
  OUT=G15; GARGS=(EXECUTE brief_nt_a.md)
  ck G15_JUNCTION_REFUSED 3 "$(gitq TMPDIR="$JUNC" GATE_SKIP_QUALIFY=1)"
  # The refusal must be the containment rule, not an inability to resolve the path.
  has G15_names_the_containment "inside the worktree" "$LOGD/G15.out"
  hasnot G15_not_a_resolve_failure "cannot resolve worktree/log paths" "$LOGD/G15.out"
  if [ -e "$CLONE/hgk-lanes" ]; then echo "FAIL G15_left_a_dir_in_the_worktree"; fail=$((fail+1)); else echo "PASS G15_left_no_dir_in_the_worktree"; pass=$((pass+1)); fi
else
  echo "SKIP G15_the_junction_could_not_be_created_here (reported, never passed)"
fi

echo "### G16 an unroled lane is refused, so an unassigned model cannot slip through (round-11)"
OUT=G16
env TMPDIR="$LOGD" LANE_WT="$CLONE" CODEX_BIN="$SBL" bash "$S/run_lane.sh" BRIEF_NT_A_ brief_nt_a.md verify/gate-norole >"$LOGD/G16.out" 2>&1; NRC=$?
ck G16_UNROLED_LANE_REFUSED 3 "$NRC"
has G16_names_the_reason "LANE_ROLE is required" "$LOGD/G16.out"

echo "### G17 a resolver that cannot decide must refuse, not proceed (round-11)"
# Round 11 got a gate to qualify while writing through a junction into the clone whenever the OS resolver
# failed: an undecided containment was treated as outside.
cat > "$LOGD/nopy" <<'EOS'
#!/usr/bin/env bash
[ "$1" = "-" ] && { echo "resolver failed" >&2; exit 1; }
exec python "$@"
EOS
chmod +x "$LOGD/nopy"
OUT=G17; GARGS=(EXECUTE brief_nt_a.md)
ck G17_UNDECIDED_CONTAINMENT_REFUSED 3 "$(gitq GATE_PY="$LOGD/nopy" GATE_SKIP_QUALIFY=1)"
has G17_names_the_containment "containment undecided" "$LOGD/G17.out"

echo
echo "RESULT pass=$pass fail=$fail"
[ "$fail" -eq 0 ] || exit 1
