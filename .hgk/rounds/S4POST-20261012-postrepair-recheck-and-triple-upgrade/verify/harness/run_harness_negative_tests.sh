#!/usr/bin/env bash
# Negative + positive tests for the governed lane launcher (v2).
#
# They reproduce the three defects an independent officer demonstrated against v1
# (round 4, verdict PARTIAL) and assert the repaired behaviour, plus the
# successful-run log-copy branch that officer recorded as NOT_EXECUTED.
#
# Everything runs in an EXTERNAL clone checked out at the delivered HEAD; the
# delivery worktree is never modified. The Codex binary is replaced by a stub so
# the tests are deterministic, instant, and cost no model calls.
set -u
WT="${LANE_WT:?LANE_WT must be the delivery worktree}"
# Native forward-slash path on purpose: git and other native binaries do NOT
# translate MSYS paths, so a bare /tmp/... would land under a literal C:\tmp.
BASE="${NT_BASE:-C:/Users/user/AppData/Local/Temp/nt-launcher}"
CLONE="$BASE/clone"; LOGD="$BASE/logs"
rm -rf "$BASE"; mkdir -p "$LOGD"
SHA="$(git -C "$WT" rev-parse HEAD)" || { echo "HEAD_UNRESOLVED"; exit 9; }
git clone -q --no-hardlinks "$WT" "$CLONE" 2>/dev/null || { echo "CLONE_FAILED"; exit 9; }
git -C "$CLONE" checkout -q "$SHA" || { echo "CHECKOUT_FAILED"; exit 9; }
git -C "$CLONE" config user.email nt@local.invalid; git -C "$CLONE" config user.name nt
REL=".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
L="$CLONE/$REL/stage-b/run_lane.sh"
[ -f "$L" ] || { echo "LAUNCHER_NOT_IN_CLONE"; exit 9; }

STUB="$BASE/stub-codex.sh"
cat > "$STUB" <<'STUBEOF'
#!/usr/bin/env bash
echo "stub lane speaking: argv=$*"
if [ "${STUB_DIRT:-0}" = "1" ]; then printf 'injected dirt\n' > "$NT_WT/NT_POST_DIRT.txt"; fi
if [ "${STUB_ESCAPE:-0}" = "1" ]; then printf 'outside the round\n' > "$NT_WT/outside-the-round.txt"; fi
exit "${STUB_EXIT:-0}"
STUBEOF
chmod +x "$STUB"

pass=0; fail=0
ck() { if [ "$2" = "$3" ]; then echo "PASS $1 (exit=$3)"; pass=$((pass+1)); else echo "FAIL $1 expected=$2 actual=$3"; fail=$((fail+1)); fi; }
cknot() { if [ -e "$2" ]; then echo "FAIL $3 (exists: $2)"; fail=$((fail+1)); else echo "PASS $3"; pass=$((pass+1)); fi; }
ckeq() { if [ -e "$2" ]; then echo "PASS $3"; pass=$((pass+1)); else echo "FAIL $3 (missing: $2)"; fail=$((fail+1)); fi; }
has() { if grep -q "$2" "$3" 2>/dev/null; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }
run() { TMPDIR="$LOGD" LANE_WT="$CLONE" CODEX_BIN="$STUB" STUB_EXIT="${1:-0}" STUB_DIRT="${2:-0}" STUB_ESCAPE="${3:-0}" NT_WT="$CLONE" bash "$L" "$4" "$5" "$6" >"$LOGD/$4.out" 2>&1; echo $?; }

echo "### T1 dirty preflight is refused (v1 passed this; regression guard)"
touch "$CLONE/NT_DIRT.txt"
ck T1_DIRTY_REFUSED 2 "$(run 0 0 0 NT1 brief_nt.md verify/nt)"
grep -q 'REFUSED\[2\]' "$LOGD/NT1.out" && { echo PASS T1_says_refused; pass=$((pass+1)); } || { echo FAIL T1_says_refused; fail=$((fail+1)); }
rm -f "$CLONE/NT_DIRT.txt"

echo "### T2 missing brief: D1a - refuse BEFORE launch, never fail open"
ck T2_MISSING_BRIEF_REFUSED 3 "$(run 0 0 0 NT2 DOES_NOT_EXIST.md verify/nt)"
if ls "$LOGD"/hgk-lanes/NT2_*.log >/dev/null 2>&1; then echo "FAIL T2_no_lane_log_written"; fail=$((fail+1)); else echo "PASS T2_no_lane_log_written"; pass=$((pass+1)); fi
if grep -q 'stub lane speaking' "$LOGD/NT2.out"; then echo "FAIL T2_child_was_launched"; fail=$((fail+1)); else echo "PASS T2_child_never_launched"; pass=$((pass+1)); fi

echo "### T3 successful run: log really copied in, commit says so, no stray root dir (D3)"
ck T3_STUB_SUCCESS 0 "$(run 0 0 0 NT3 brief_nt.md verify/nt)"
ls "$CLONE/$REL/stage-b/" | grep -q '^NT3_.*\.log$' && { echo PASS T3_log_copied_in; pass=$((pass+1)); } || { echo FAIL T3_log_copied_in; fail=$((fail+1)); }
git -C "$CLONE" log -1 --pretty=%B | grep -qi 'copied in from outside' && { echo PASS T3_commit_states_copy; pass=$((pass+1)); } || { echo FAIL T3_commit_states_copy; fail=$((fail+1)); }
cknot "x" "$CLONE/verify" "D3_no_output_dir_at_repo_root"
ckeq x "$CLONE/$REL/verify/nt" "D3_output_dir_is_round_relative"

echo "### T4 postflight dirt is REJECTED, not merely printed (D2)"
ck T4_POSTFLIGHT_DIRT_REJECTED 5 "$(run 0 1 0 NT4 brief_nt.md verify/nt)"
grep -q 'POSTFLIGHT:dirty=1' "$LOGD/NT4.out" && { echo PASS T4_dirt_was_detected; pass=$((pass+1)); } || { echo FAIL T4_dirt_was_detected; fail=$((fail+1)); }
rm -f "$CLONE/NT_POST_DIRT.txt"; git -C "$CLONE" checkout -q -- . 2>/dev/null; rm -f "$CLONE/outside-the-round.txt"

echo "### T5 a non-zero child is propagated, never advertised as success"
ck T5_CHILD_EXIT_PROPAGATED 7 "$(run 7 0 0 NT5 brief_nt.md verify/nt)"
grep -q 'NT5_LANE_DONE' "$LOGD/NT5.out" && { echo PASS T5_lane_reports_done; pass=$((pass+1)); } || { echo FAIL T5_lane_reports_done; fail=$((fail+1)); }

echo "### T6 TMPDIR resolving inside the worktree is refused (F)"
TMPDIR="$CLONE/tmp-inside" LANE_WT="$CLONE" CODEX_BIN="$STUB" bash "$L" NT6 brief_nt.md verify/nt >"$LOGD/NT6.out" 2>&1; c=$?
ck T6_TMPDIR_INSIDE_REFUSED 3 "$c"

echo "### T7 a failed receipt copy is fatal, not a note (R1)"
(
  cp() { local last="${@: -1}"; case "$last" in *.exit) return 23;; *) command cp "$@";; esac; }
  export -f cp
  env TMPDIR="$LOGD" LANE_WT="$CLONE" CODEX_BIN="$STUB" bash "$L" NT7 brief_nt.md verify/nt
) >"$LOGD/T7.out" 2>&1; c=$?
ck T7_RECEIPT_COPY_FATAL 6 "$c"
has T7_names_the_receipt POSTFLIGHT_RECEIPT_COPY_FAILED "$LOGD/T7.out"

echo "### T8 a FAILED git status is not a clean worktree (R2)"
(
  git() { if [ "${1:-}" = "status" ]; then return 128; fi; command git "$@"; }
  export -f git
  env TMPDIR="$LOGD" LANE_WT="$CLONE" CODEX_BIN="$STUB" bash "$L" NT8 brief_nt.md verify/nt
) >"$LOGD/T8.out" 2>&1; c=$?
ck T8_STATUS_FAILURE_REFUSED 2 "$c"
has T8_says_status_failed "git status failed" "$LOGD/T8.out"
if grep -q "stub lane speaking" "$LOGD/T8.out"; then echo "FAIL T8_child_was_launched"; fail=$((fail+1)); else echo "PASS T8_child_never_launched"; pass=$((pass+1)); fi

echo "### T9 an already staged OUTSIDE-round file is refused (R3)"
echo "outside" > "$CLONE/outside-round-fixture.txt"
git -C "$CLONE" add outside-round-fixture.txt
ck T9_STAGED_OUTSIDE_REFUSED 6 "$(run 0 0 0 NT9 brief_nt.md verify/nt)"
has T9_names_the_outside_path STAGED_OUTSIDE_ROUND_REFUSED "$LOGD/NT9.out"
if git -C "$CLONE" log -1 --pretty=%s | grep -q "outside-round-fixture"; then
  echo "FAIL T9_outside_file_was_committed"; fail=$((fail+1))
else echo "PASS T9_outside_file_was_not_committed"; pass=$((pass+1)); fi
git -C "$CLONE" reset -q 2>/dev/null; rm -f "$CLONE/outside-round-fixture.txt"

echo
echo "RESULT pass=$pass fail=$fail"
[ "$fail" -eq 0 ] || exit 1
