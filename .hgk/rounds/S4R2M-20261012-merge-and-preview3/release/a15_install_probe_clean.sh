#!/usr/bin/env bash
# S4R2M M4 oracle A15, re-run with a SCRUBBED environment.
# The first attempt inherited PYTHONPATH from the orchestrator shell, so `pipd` resolved schemas from
# the candidate worktree instead of the installed distribution. That measurement is void; this one
# starts from a clean env and records everything to a log.
set -u
SB="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4r2m-release-clean"
RELDIR="C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/.hgk/rounds/S4R2M-20261012-merge-and-preview3/release"
PY="/c/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
rm -rf "$SB"; mkdir -p "$SB"
LOG="$SB/A15.log"; : > "$LOG"

# scrub every variable that could point the import system at a checkout
unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PIPD_SCHEMAS_DIR 2>/dev/null

say() { echo "$@" | tee -a "$LOG"; }

cd "$SB"
say "=== A) fresh venv, install the BUILT wheel; nothing on PYTHONPATH ==="
$PY -m venv venv-a >>"$LOG" 2>&1
VA="$SB/venv-a/Scripts/python.exe"
"$VA" -m pip install -q --no-input "$RELDIR/pipd_ls_sp-0.1.1a3-py3-none-any.whl" >>"$LOG" 2>&1
say "installed version : $("$VA" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))")"
say "module location   : $("$VA" -c "import pipd_ls_sp,os;print(os.path.dirname(pipd_ls_sp.__file__))")"
say "PYTHONPATH=[${PYTHONPATH:-<unset>}]"
say "--- pipd doctor (schema_source must be INSTALLED) ---"
"$VA" -m pipd_ls_sp.cli doctor 2>&1 | tee -a "$LOG" | grep -E "schema_source|\"schemas_dir\"|verdict" | head -6
say "--- command surface ---"
"$VA" -m pipd_ls_sp.cli --help >>"$LOG" 2>&1
say "commands advertised: $(grep -o '13 commands' "$LOG" | head -1)"

say ""
say "=== B) upgrade from the PUBLISHED 0.1.0 wheel to 0.1.1a3 ==="
$PY -m venv venv-b >>"$LOG" 2>&1
VB="$SB/venv-b/Scripts/python.exe"
curl -fsSL -o old.whl "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2/pipd_ls_sp-0.1.0-py3-none-any.whl" >>"$LOG" 2>&1
say "downloaded 0.1.0 digest: $(sha256sum old.whl | cut -d' ' -f1)"
say "                    published: d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
"$VB" -m pip install -q --no-input ./old.whl >>"$LOG" 2>&1
say "before upgrade: $("$VB" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))")"
"$VB" -m pip install -q --no-input --pre -U "$RELDIR/pipd_ls_sp-0.1.1a3-py3-none-any.whl" >>"$LOG" 2>&1
say "after upgrade : $("$VB" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))")"

say ""
say "=== C) rollback to the pinned 0.1.0, doctor still works ==="
"$VB" -m pip install -q --no-input --force-reinstall ./old.whl >>"$LOG" 2>&1
say "after rollback: $("$VB" -c "import importlib.metadata as m;print(m.version('pipd-ls-sp'))")"
"$VB" -m pipd_ls_sp.cli doctor >>"$LOG" 2>&1
say "rollback doctor verdict: $(grep -o '\"verdict\": \"[A-Z]*\"' "$LOG" | tail -1)"

say ""
say "=== D) schema_source truth in the installed venv (no checkout reachable) ==="
"$VA" -c "import pipd_ls_sp,os;print('pkg dir:',os.path.dirname(pipd_ls_sp.__file__))" | tee -a "$LOG"
"$VA" -m pipd_ls_sp.cli doctor 2>&1 | grep -A3 '"schema_source"' | head -6 | tee -a "$LOG"
say "A15_CLEAN_DONE"
