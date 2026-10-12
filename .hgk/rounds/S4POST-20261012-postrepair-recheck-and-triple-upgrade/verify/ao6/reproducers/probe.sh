#!/usr/bin/env bash
set -u
BASE="$(cd "$(dirname "$0")" && pwd -P)"
WT="$BASE/c"
case "$(cygpath -m "$WT")" in C:/Users/user/AppData/Local/Temp/a6*/c) ;; *) exit 90;; esac
REL=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
S="$WT/$REL/stage-b"; L="$S/run_lane.sh"; G="$S/run_lanes_gated.sh"
SHA=239fead8140222660b42819ab2f89784e5322243
mkdir -p "$BASE/evidence" "$BASE/logs"
export LANE_WT="$WT" TMPDIR="$BASE/logs" CODEX_BIN="$BASE/stub.sh" GATE_BIN="$BASE/stub.sh" GATE_QUALIFY_RUNS=1
cat > "$BASE/stub.sh" <<'EOF'
#!/usr/bin/env bash
printf 'STUB argv=%s\n' "$*" >> "$AO6_ARGV"
echo Q1_OK; echo Q2_OK
exit 0
EOF
chmod +x "$BASE/stub.sh"
export AO6_ARGV="$BASE/evidence/argv.txt"
reset_subject() {
  rm -f "$WT/.git/hooks/post-commit" "$WT/.git/info/exclude"
  git -C "$WT" reset --hard "$SHA" >/dev/null
  git -C "$WT" clean -fdx >/dev/null
}
run_case() {
  local id="$1"; shift
  echo "COMMAND[$id]: $*"
  "$@" > "$BASE/evidence/$id.txt" 2>&1; local rc=$?
  cat "$BASE/evidence/$id.txt"
  echo "EXIT[$id]=$rc"
  git -C "$WT" status --porcelain
  echo "STATUS_EXIT[$id]=$?"
}
reset_subject
(
cp(){ case "${@: -1}" in *.exit) echo INJECT_CP_EXIT_23 >&2; return 23;; *) command cp "$@";; esac; }; export -f cp
run_case R1 bash "$L" R1 brief_nt.md verify/ao6
)
reset_subject
(
git(){ if [ "${1:-}" = status ]; then echo INJECT_STATUS_EXIT_128 >&2; return 128; fi; command git "$@"; }; export -f git
run_case R2 bash "$L" R2 brief_nt.md verify/ao6
)
reset_subject
printf outside > "$WT/outside.txt"; git -C "$WT" add outside.txt
run_case R3 bash "$L" R3 brief_nt.md verify/ao6
reset_subject
run_case R4 env GATE_QUALIFY_RUNS=0 bash "$G" EXECUTE brief_nt_a.md
reset_subject
: > "$AO6_ARGV"
run_case R5 env ROUTE_STYLE=openai ROUTE_BASE_URL=http://bad.invalid ROUTE_CATALOG=bad.json bash "$G" EXECUTE brief_nt_a.md
cat "$AO6_ARGV"
reset_subject
cat > "$WT/.git/hooks/post-commit" <<'EOF'
#!/usr/bin/env bash
case "$(git log -1 --pretty=%s)" in *'lane receipt'*) echo hook-dirt > AO6_HOOK_DIRT.txt;; esac
EOF
chmod +x "$WT/.git/hooks/post-commit"
run_case SECOND_COMMIT bash "$L" SECOND brief_nt.md verify/ao6
reset_subject
mkdir -p "$WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
printf outside > "$WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt"
git -C "$WT" add Xhgk
run_case REGEX_ALIAS bash "$L" ALIAS brief_nt.md verify/ao6
 git -C "$WT" log -2 --name-only --pretty=oneline
reset_subject
printf outside > "$WT/outside.txt"; git -C "$WT" add ./outside.txt
run_case DOT_ALIAS bash "$L" DOT brief_nt.md verify/ao6
reset_subject
mkdir -p "$WT/CASEPATH"; printf case > "$WT/CASEPATH/outside.txt"; git -C "$WT" add casepath/outside.txt
run_case CASE_VARIANT bash "$L" CASE brief_nt.md verify/ao6
reset_subject
printf outside.txt > "$WT/.git/info/exclude"; printf ignored > "$WT/outside.txt"; git -C "$WT" add -f outside.txt
run_case IGNORED_STAGED bash "$L" IGNORE brief_nt.md verify/ao6
reset_subject
# Minimal synthetic gitlink: tests staged submodule path treatment, not recursive submodule execution.
git -C "$WT" update-index --add --cacheinfo "160000,$SHA,outside-submodule"
run_case SUBMODULE_GITLINK bash "$L" SUB brief_nt.md verify/ao6
reset_subject
printf 'AO6_IGNORED.txt\n' > "$WT/.git/info/exclude"; printf hidden > "$WT/AO6_IGNORED.txt"
run_case IGNORED_DIRT bash "$L" HIDDEN brief_nt.md verify/ao6
 git -C "$WT" status --porcelain --ignored | head -5
reset_subject
# Freeze wall-clock token to reproduce an older same-token receipt (token has no nonce/pid).
old="$S/BRIEF_NT_A__20000101T000000Z-0.receipt"
printf 'lane=BRIEF_NT_A_\nstamp=OLD\ntoken=20000101T000000Z-0\nchild_exit=99\npostflight_dirty=99\nroute=OLD\n' > "$old"
git -C "$WT" add "$REL"; git -C "$WT" commit -qm 'AO6 older receipt fixture'
git hash-object "$old"
(
date(){ echo 20000101T000000Z; }; export -f date
printf(){ case "${1:-}" in lane=%s*) echo INJECT_RECEIPT_WRITE_FAILURE >&2; return 1;; *) builtin printf "$@";; esac; }; export -f printf
run_case OLD_RECEIPT bash "$G" EXECUTE brief_nt_a.md
)
cat "$old"; git hash-object "$old"
reset_subject
cat > "$WT/.git/hooks/post-commit" <<'EOF'
#!/usr/bin/env bash
case "$(git log -1 --pretty=%s)" in *'lane receipt'*)
for r in .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/*.receipt; do
 case "$r" in *BRIEF_NT_A__*) printf 'FORGED child_exit=99 token=wrong route=wrong\n' > "$r";; esac
done;; esac
EOF
chmod +x "$WT/.git/hooks/post-commit"
run_case FORGED_RECEIPT bash "$G" EXECUTE brief_nt_a.md
find "$S" -name 'BRIEF_NT_A__*.receipt' -exec cat '{}' \;
reset_subject
run_case MANIFEST bash "$L" MANIFEST brief_nt.md verify/ao6
find "$BASE/logs" -name 'MANIFEST_*.manifest' -print
find "$S" -name 'MANIFEST_*.manifest' -print
reset_subject
run_case SKIP_QUALIFY env GATE_SKIP_QUALIFY=1 bash "$G" EXECUTE brief_nt_a.md
reset_subject
run_case FILTER_ONLY env GATE_QUALIFY_ONLY=1 bash "$G" EXECUTE brief_nt_a.md