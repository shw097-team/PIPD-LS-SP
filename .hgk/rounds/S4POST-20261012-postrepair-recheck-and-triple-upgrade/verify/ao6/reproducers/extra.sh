#!/usr/bin/env bash
set -u
BASE="$(cd "$(dirname "$0")" && pwd -P)"; WT="$BASE/c"
case "$(cygpath -m "$WT")" in C:/Users/user/AppData/Local/Temp/a6*/c) ;; *) exit 90;; esac
REL=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
S="$WT/$REL/stage-b"; L="$S/run_lane.sh"; G="$S/run_lanes_gated.sh"
export LANE_WT="$WT" TMPDIR="$BASE/logs" CODEX_BIN="$BASE/stub.sh" GATE_BIN="$BASE/stub.sh" GATE_QUALIFY_RUNS=1 AO6_ARGV="$BASE/evidence/extra-argv.txt"
reset_subject(){ rm -f "$WT/.git/hooks/post-commit" "$WT/.git/info/exclude"; git -C "$WT" reset --hard 239fead8140222660b42819ab2f89784e5322243 >/dev/null; git -C "$WT" clean -fdx >/dev/null; }
run_case(){ local id="$1"; shift; echo "COMMAND[$id]: $*"; "$@" > "$BASE/evidence/$id.txt" 2>&1; local rc=$?; cat "$BASE/evidence/$id.txt"; echo "EXIT[$id]=$rc"; git -C "$WT" status --porcelain; echo STATUS_EXIT=$?; }
reset_subject
mkdir -p "$WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
echo outside > "$WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt"; git -C "$WT" add Xhgk
run_case REGEX_PROOF bash "$L" ALIAS2 brief_nt.md verify/ao6
git -C "$WT" log -3 --name-only --pretty=oneline
reset_subject
(
git(){ if [ "${1:-}" = diff ] && [ "${2:-}" = --cached ] && [ "${3:-}" = --name-only ]; then echo INJECT_STAGED_QUERY_EXIT_128 >&2; return 128; fi; command git "$@"; }; export -f git
echo outside > "$WT/outside.txt"; command git -C "$WT" add outside.txt
run_case STAGED_QUERY_FAILURE bash "$L" QUERY brief_nt.md verify/ao6
command git -C "$WT" log -3 --name-only --pretty=oneline
)
reset_subject
printf '\nAO6_ignored_staged.txt\n' >> "$WT/.gitignore"; git -C "$WT" add .gitignore; git -C "$WT" commit -qm 'AO6 ignore fixture'
echo hidden > "$WT/AO6_ignored_staged.txt"; git -C "$WT" add -f AO6_ignored_staged.txt
run_case GITIGNORE_ENTRY bash "$L" IGNORE2 brief_nt.md verify/ao6
reset_subject
cat > "$BASE/route-env.sh" <<'EOF'
case "$0" in */run_lane.sh) export ROUTE_STYLE=openai ROUTE_BASE_URL=http://bad.invalid ROUTE_CATALOG=bad.json;; esac
EOF
: > "$AO6_ARGV"
run_case BASH_ENV_ROUTE env BASH_ENV="$BASE/route-env.sh" bash "$G" EXECUTE brief_nt_a.md
cat "$AO6_ARGV"
reset_subject
# Receipt file exists before launch, then printf write fails after redirection truncates it.
old="$S/BRIEF_NT_A__20000101T000000Z-0.receipt"
printf 'OLDER RECEIPT child_exit=99 route=wrong\n' > "$old"; git -C "$WT" add "$REL"; git -C "$WT" commit -qm 'AO6 old receipt fixture'
echo OLD_BEFORE; wc -c "$old"; cat "$old"
(
date(){ echo 20000101T000000Z; }; export -f date
printf(){ case "${1:-}" in lane=%s*) echo INJECT_RECEIPT_WRITE_FAILURE >&2; return 1;; *) builtin printf "$@";; esac; }; export -f printf
run_case EMPTY_OLD_RECEIPT bash "$G" EXECUTE brief_nt_a.md
)
echo OLD_AFTER; wc -c "$old"; cat "$old"
reset_subject
# Older receipt with DIFFERENT token must not rescue a missing current receipt.
printf OLD > "$S/BRIEF_NT_A__OLDER.receipt"; git -C "$WT" add "$REL"; git -C "$WT" commit -qm 'AO6 different-token fixture'
cat > "$BASE/delete-log.sh" <<'EOF'
#!/usr/bin/env bash
ls -t "$TMPDIR"/hgk-lanes/BRIEF_NT_A__*.log | head -1 | xargs rm -f
echo stub; exit 0
EOF
chmod +x "$BASE/delete-log.sh"
run_case DIFFERENT_TOKEN env CODEX_BIN="$BASE/delete-log.sh" bash "$G" EXECUTE brief_nt_a.md
reset_subject