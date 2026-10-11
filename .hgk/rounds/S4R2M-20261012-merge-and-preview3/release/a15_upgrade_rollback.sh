#!/usr/bin/env bash
# S4R2M M4 oracle A15, part B/C re-run.
# The previous attempt saved the published wheel as `old.whl`; pip rejects a wheel whose filename is
# not a valid distribution filename, so the 0.1.0 baseline and the rollback never happened. That was
# a probe defect, not a product one. This run keeps the real filename and scrubs PYTHONPATH.
set -u
SB="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4r2m-upgrade"
RELDIR="C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/.hgk/rounds/S4R2M-20261012-merge-and-preview3/release"
PY="/c/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
unset PYTHONPATH PYTHONHOME 2>/dev/null
rm -rf "$SB"; mkdir -p "$SB"; cd "$SB"
LOG="$SB/A15_BC.log"; : > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }

OLDW="pipd_ls_sp-0.1.0-py3-none-any.whl"
NEWW="pipd_ls_sp-0.1.1a3-py3-none-any.whl"

say "=== fetch the PUBLISHED 0.1.0 wheel under its real name ==="
curl -fsSL -o "$OLDW" "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2/$OLDW" >>"$LOG" 2>&1
say "downloaded digest: $(sha256sum "$OLDW" | cut -d' ' -f1)"
say "published digest : d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"

$PY -m venv venv >>"$LOG" 2>&1
V="$SB/venv/Scripts/python.exe"

say ""
say "=== B) install 0.1.0, then upgrade to 0.1.1a3 ==="
"$V" -m pip install -q --no-input "$SB/$OLDW" >>"$LOG" 2>&1 && say "install 0.1.0 : OK" || say "install 0.1.0 : FAILED"
say "before upgrade: $("$V" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))" 2>&1)"
"$V" -m pip install -q --no-input --pre -U "$RELDIR/$NEWW" >>"$LOG" 2>&1 && say "upgrade       : OK" || say "upgrade       : FAILED"
say "after upgrade : $("$V" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))" 2>&1)"

say ""
say "=== C) rollback to the pinned 0.1.0 and smoke it ==="
"$V" -m pip install -q --no-input --force-reinstall "$SB/$OLDW" >>"$LOG" 2>&1 && say "rollback      : OK" || say "rollback      : FAILED"
say "after rollback: $("$V" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))" 2>&1)"
"$V" -m pipd_ls_sp.cli doctor >>"$LOG" 2>&1
say "rollback doctor: $(grep -o '"verdict": "[A-Z]*"' "$LOG" | tail -1)"

say ""
say "=== D) upgrade back once more, so the venv ends on the released version ==="
"$V" -m pip install -q --no-input --pre -U "$RELDIR/$NEWW" >>"$LOG" 2>&1
say "final         : $("$V" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))" 2>&1)"
say "A15_BC_DONE"
