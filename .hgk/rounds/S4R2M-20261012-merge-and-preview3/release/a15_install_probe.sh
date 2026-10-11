#!/usr/bin/env bash
# S4R2M Gate M4 oracle A15 — install, upgrade, rollback from BUILT bytes, outside any checkout.
set -u
SB="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4r2m-release"
RELDIR="C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/.hgk/rounds/S4R2M-20261012-merge-and-preview3/release"
PY="/c/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
rm -rf "$SB"; mkdir -p "$SB"
cd "$SB"

echo "=== A) fresh venv, install the BUILT wheel (no source checkout on PYTHONPATH) ==="
unset PYTHONPATH
$PY -m venv venv-a >/dev/null 2>&1
VPY="$SB/venv-a/Scripts/python.exe"
"$VPY" -m pip install -q --no-input "$RELDIR/pipd_ls_sp-0.1.1a3-py3-none-any.whl" 2>&1 | tail -3
echo "installed version: $("$VPY" -c "import importlib.metadata as m; print(m.version('pipd-ls-sp'))")"
echo "module location  : $("$VPY" -c "import pipd_ls_sp,os; print(os.path.dirname(pipd_ls_sp.__file__))")"
echo "--- pipd doctor ---"
"$VPY" -m pipd_ls_sp.cli doctor 2>&1 | tail -12
echo "--- pipd --help : command count ---"
"$VPY" -m pipd_ls_sp.cli --help 2>&1 | head -5 | tail -2

echo
echo "=== B) upgrade path: install the PUBLISHED 0.1.0 wheel, then upgrade to 0.1.1a3 ==="
$PY -m venv venv-b >/dev/null 2>&1
VPY2="$SB/venv-b/Scripts/python.exe"
curl -fsSL -o old.whl "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2/pipd_ls_sp-0.1.0-py3-none-any.whl"
echo "old wheel sha256: $(sha256sum old.whl | cut -d' ' -f1)"
echo "  (published digest d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f)"
"$VPY2" -m pip install -q --no-input ./old.whl 2>&1 | tail -2
echo "before upgrade: $("$VPY2" -c "import importlib.metadata as m; print(m.version('pipd-ls-sp'))")"
"$VPY2" -m pip install -q --no-input --pre -U "$RELDIR/pipd_ls_sp-0.1.1a3-py3-none-any.whl" 2>&1 | tail -2
echo "after upgrade : $("$VPY2" -c "import importlib.metadata as m; print(m.version('pipd-ls-sp'))")"

echo
echo "=== C) rollback smoke: pinned 0.1.0 again, doctor still works ==="
"$VPY2" -m pip install -q --no-input --force-reinstall ./old.whl 2>&1 | tail -2
echo "after rollback: $("$VPY2" -c "import importlib.metadata as m; print(m.version('pipd-ls-sp'))")"
"$VPY2" -m pipd_ls_sp.cli doctor 2>&1 | tail -4
echo A15_DONE
