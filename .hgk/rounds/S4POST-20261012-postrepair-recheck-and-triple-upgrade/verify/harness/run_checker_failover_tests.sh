#!/usr/bin/env bash
# Negative tests for the owner-declared checker failover (stage-b/run_checker_lane.sh).
# The point: the failover must fire on exhaustion ONLY. If it fires on any other failure it becomes a
# new fail-open - a model silently swapped in to turn a red lane green.
set -u
WT="${LANE_WT:-C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt}"
REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
# Native git does not translate MSYS-style paths on this host: a clone destination given as
# /tmp/x is created literally as \tmp\x, so the subsequent cd fails. Use a native path for
# anything a native binary must resolve.
LOGD="C:/Users/user/AppData/Local/Temp/fo-tests"; rm -rf "$LOGD"; mkdir -p "$LOGD"
CLONE="$LOGD/c"; E="$LOGD/lanes"; mkdir -p "$E"
export TMPDIR="$E"
pass=0; fail=0
ck(){ if [ "$2" = "$3" ]; then echo "PASS $1 (exit=$3)"; pass=$((pass+1)); else echo "FAIL $1 expected=$3 actual=$2"; fail=$((fail+1)); fi; }
has(){ if grep -q -- "$2" "$3" 2>/dev/null; then echo "PASS $1"; pass=$((pass+1)); else echo "FAIL $1"; fail=$((fail+1)); fi; }
hasnot(){ if grep -q -- "$2" "$3" 2>/dev/null; then echo "FAIL $1 (found: $2)"; fail=$((fail+1)); else echo "PASS $1"; pass=$((pass+1)); fi; }

cd "$WT" || exit 9
git -c safe.directory="$WT" clone -q --no-hardlinks . "$CLONE" >/dev/null 2>&1 || { echo "CLONE_FAILED"; exit 9; }
cd "$CLONE" || exit 9
git checkout -q "$(git -C "$WT" rev-parse HEAD)" 2>/dev/null
git config user.email nt@local.invalid; git config user.name nt
[ -f "$CLONE/$REL/stage-b/run_checker_lane.sh" ] || { echo "not in clone"; exit 9; }

# A stub worker: on its first call it reports the message in $1 and exits 1; on the next it succeeds.
mkstub(){
  cat > "$1" <<'EOS'
#!/usr/bin/env bash
STATE="$FO_STATE"
if [ ! -f "$STATE" ]; then
  : > "$STATE"
  echo "OpenAI Codex v0.162.0-alpha.17.2"
  echo "$FO_MSG"
  echo "exec a succeeded in 12ms:"
  echo "exec b succeeded in 11ms:"
  exit 1
fi
echo "OpenAI Codex v0.162.0-alpha.17.2"
echo "exec a succeeded in 12ms:"
echo "exec b succeeded in 11ms:"
echo "Q1_OK"; echo "Q2_OK"
exit 0
EOS
  chmod +x "$1"
}
STB="$LOGD/stub"; mkstub "$STB"
run(){ FO_STATE="$LOGD/st$1" FO_MSG="$2" CODEX_BIN="$STB" LANE_WT="$CLONE" bash "$CLONE/$REL/stage-b/run_checker_lane.sh" "FO$1" br_fo.md verify/fo$1 2>&1; }

echo "### A1 a provider content-filter kill must NOT be worked around by a model switch"
printf 'x\n' > "$CLONE/$REL/stage-b/br_fo.md"
run A "ERROR: This content was flagged for possible cybersecurity risk." > "$LOGD/A.out" 2>&1
# The primary's own exit code must be propagated: 1 means "failed", which is the point.
ck A1_nonzero_exit "$?" 1
has A1_says_not_exhaustion "CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION" "$LOGD/A.out"
hasnot A1_did_not_fail_over "CHECKER_FAILOVER_START" "$LOGD/A.out"
hasnot A1_no_backup_ok "CHECKER_BACKUP_OK" "$LOGD/A.out"

echo "### A2 a protocol 400 must NOT be worked around by a model switch"
run B "Provider error 400: [invalid_request_error] The reasoning_content in the thinking mode must be passed back to the API." > "$LOGD/B.out" 2>&1
has B2_says_not_exhaustion "CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION" "$LOGD/B.out"
hasnot B2_did_not_fail_over "CHECKER_FAILOVER_START" "$LOGD/B.out"

echo "### A3 an exhaustion signal DOES fail over, and records both models"
run C "ERROR: Selected model is at capacity. Please try a different model." > "$LOGD/C.out" 2>&1
ck A3_exit_zero "$?" 0
has A3_exhaustion_seen "CHECKER_PRIMARY_EXHAUSTED" "$LOGD/C.out"
has A3_failover_started "CHECKER_FAILOVER_START" "$LOGD/C.out"
has A3_backup_ok "CHECKER_BACKUP_OK" "$LOGD/C.out"
has A3_record_names_backup "opencode-go/glm-5.3-flash" "$CLONE/$REL/stage-b/CHECKER_FAILOVER_FOC.md"
has A3_record_names_primary "gpt-6.1-sol" "$CLONE/$REL/stage-b/CHECKER_FAILOVER_FOC.md"
has A3_record_says_identity_changes "changes the checker's identity" "$CLONE/$REL/stage-b/CHECKER_FAILOVER_FOC.md"
hasnot A3_no_record_for_the_killed_lane_unneeded "CHECKER_FAILOVER_START" "$LOGD/A.out"

echo "RESULT pass=$pass fail=$fail"
[ "$fail" -eq 0 ]echo "### A4 a protocol 400 whose text ALSO carries a quota word must NOT fail over (round-10)"
run C "Provider error 400: [invalid_request_error] The reasoning_content in the thinking mode must be passed back. Service at capacity." > "$LOGD/C.out" 2>&1
ck A4_nonzero_exit "$?" 1
has A4_says_not_exhaustion "CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION" "$LOGD/C.out"
has A4_names_the_hard_failure "hard_failure=[" "$LOGD/C.out"
hasnot A4_did_not_fail_over "CHECKER_FAILOVER_START" "$LOGD/C.out"

echo "### A5 a real exhaustion failover must leave its record committed and the tree clean (round-10)"
run D "ERROR: You've hit your usage limit. Upgrade to Pro or try again at 10:37 PM." > "$LOGD/D.out" 2>&1
has A5_failed_over "CHECKER_FAILOVER_START" "$LOGD/D.out"
has A5_backup_ok "CHECKER_BACKUP_OK" "$LOGD/D.out"
REC="$(grep -o 'CHECKER_FAILOVER_RECORD .*' "$LOGD/D.out" | tail -1 | awk '{print $2}')"
if [ -n "$REC" ] && git -C "$CLONE" ls-files --error-unmatch "${REC#$CLONE/}" >/dev/null 2>&1; then echo "PASS A5_record_tracked"; pass=$((pass+1)); else echo "FAIL A5_record_tracked ($REC)"; fail=$((fail+1)); fi
if [ -z "$(git -C "$CLONE" status --porcelain)" ]; then echo "PASS A5_tree_clean"; pass=$((pass+1)); else echo "FAIL A5_tree_clean"; fail=$((fail+1)); fi

echo
echo "RESULT pass=$pass fail=$fail"
[ "$fail" -eq 0 ] || exit 1
