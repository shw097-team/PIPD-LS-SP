#!/usr/bin/env bash
set -u
B="$AO6_SHORT"; W="$B/c"; REL=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
case "$(cygpath -m "$W")" in C:/Users/user/AppData/Local/Temp/a6*/c) ;; *) exit 90;; esac
git -C "$W" reset --hard 239fead8140222660b42819ab2f89784e5322243 >/dev/null
git init -q "$B/smallsub"; git -C "$B/smallsub" config user.name ao6; git -C "$B/smallsub" config user.email ao6@local.invalid
echo initial > "$B/smallsub/file.txt"; git -C "$B/smallsub" add file.txt; git -C "$B/smallsub" commit -qm initial
git -C "$W" -c protocol.file.allow=always submodule add "$B/smallsub" outside-real-submodule
echo SUBMODULE_ADD_EXIT=$?
git -C "$W" commit -qam 'AO6 submodule fixture'
git -C "$W/outside-real-submodule" config user.name ao6; git -C "$W/outside-real-submodule" config user.email ao6@local.invalid
echo changed > "$W/outside-real-submodule/file.txt"; git -C "$W/outside-real-submodule" add file.txt; git -C "$W/outside-real-submodule" commit -qm changed
git -C "$W" add outside-real-submodule
printf 'COMMAND: staged real outside submodule, run_lane.sh REALSUB brief_nt.md verify/ao6\n'
TMPDIR="$B/logs" LANE_WT="$W" CODEX_BIN="$B/stub.sh" AO6_ARGV="$B/evidence/sub-argv.txt" bash "$W/$REL/stage-b/run_lane.sh" REALSUB brief_nt.md verify/ao6
echo REAL_SUBMODULE_EXIT=$?
git -C "$W" status --porcelain