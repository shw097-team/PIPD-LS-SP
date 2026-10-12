#!/usr/bin/env bash
# S4EXT-R1 / TT-S4EXT-005 + G006 -- installed-wheel qualification in an ISOLATED virtualenv.
#
# Proves the published wheel works as an installed distribution, with NO PYTHONPATH pointing at the
# source tree, and records every exit code. Not a substitute for an external verifier re-running it
# from the downloaded asset bytes; it is the local, replayable half of that evidence.
#
# Replay:  bash .hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw/installed_wheel_qualification.sh
set -u

WT="C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt"
RAW="$WT/.hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw"
PY311="${PYTHON311:-C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe}"
WHEEL="$WT/dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"
WORK="${PIPD_QUAL_WORK:-C:/Users/user/AppData/Local/Temp/pipd-s4ext-r1-qual}"
VENV="$WORK/venv"
PY="$VENV/Scripts/python.exe"
CLI="$VENV/Scripts/pipd.exe"
CTX="$WORK/ctx"
ART="$WORK/art"

rm -rf "$WORK"
mkdir -p "$WORK" "$CTX" "$ART"; rc=$?
echo "workspace=$WORK (removed and recreated; rc=$rc)"

step() {  # step <label> <logfile> <cmd...>
  local label="$1" logf="$2"; shift 2
  echo "### $label" >> "$logf"
  echo "\$ $*" >> "$logf"
  "$@" >> "$logf" 2>&1
  local rc=$?
  echo "exit_code=$rc" >> "$logf"
  echo "$label exit=$rc"
  return $rc
}

# ---------------------------------------------------------------- 1. install
L="$RAW/QUAL_01_install.raw.log"
: > "$L"
echo "host_uname=$(uname -s) shell=$BASH_VERSION" >> "$L"
echo "python311=$PY311" >> "$L"
sha256sum "$WHEEL" >> "$L" 2>&1
step "venv_create" "$L" "$PY311" -m venv "$VENV"
step "pip_install_wheel" "$L" "$PY" -m pip install --disable-pip-version-check "$WHEEL"
step "pip_show" "$L" "$PY" -m pip show pipd-ls-sp
step "import_location" "$L" "$PY" -c "import pipd_ls_sp,json;print(json.dumps({'pkg':pipd_ls_sp.__file__}))"
step "no_pythonpath_set" "$L" env -u PYTHONPATH bash -c "echo PYTHONPATH=\${PYTHONPATH:-<unset>}"

# ---------------------------------------------------------------- 2. doctor + surface
L="$RAW/QUAL_02_doctor_and_surface.raw.log"
: > "$L"
step "doctor" "$L" "$CLI" doctor
step "help" "$L" "$CLI" --help
for c in init intake profile compile-pi bind-pd compile-ecp compile-tqaep validate doctor project export diff repair; do
  step "help_$c" "$L" "$CLI" "$c" --help
done

# ---------------------------------------------------------------- 3. schemas delivered by the wheel
L="$RAW/QUAL_03_installed_schemas.raw.log"
: > "$L"
step "installed_schema_family_count" "$L" "$PY" -c "
import pathlib, pipd_ls_sp, json
root = pathlib.Path(pipd_ls_sp.__file__).parent
p = sorted(root.rglob('*.schema.json'))
print(json.dumps({'count': len(p), 'names': [x.name for x in p]}, indent=1))
"

# ---------------------------------------------------------------- 4. the chain, installed CLI only
L="$RAW/QUAL_04_installed_chain.raw.log"
: > "$L"
step "init" "$L" "$CLI" --root "$ART" init
step "intake" "$L" bash -c "'$CLI' --root '$ART' intake --goal 'Compile this example clause source into a validated PI to PD to ECP to TQAEP chain.' --source '$WT/examples/first-run/source.txt' --constraint 'candidate-only, no release' --non-goal 'no upstream document bodies copied' > '$ART/intent.card.json'"
step "compile_pi" "$L" bash -c "'$CLI' --root '$ART' compile-pi --intent '$ART/intent.card.json' --profile LITE > '$ART/pi.json'"
step "bind_pd" "$L" bash -c "'$CLI' --root '$ART' bind-pd --pi '$ART/pi.json' --repo-root '$CTX' > '$ART/pd.json'"
step "compile_ecp" "$L" bash -c "'$CLI' --root '$ART' compile-ecp --pd '$ART/pd.json' --pi '$ART/pi.json' > '$ART/ecp.json'"
step "compile_tqaep" "$L" bash -c "'$CLI' --root '$ART' compile-tqaep --pi '$ART/pi.json' --ecp '$ART/ecp.json' --maker HERMES-MAKER --checker GLM-5.3-FLASH-AO-LANE --checker-receipt deleg_example/lane-C > '$ART/tqaep.json'"
step "assemble" "$L" bash -c "'$PY' '$WT/examples/first-run/assemble_bundle.py' '$ART/pi.json' '$ART/pd.json' '$ART/ecp.json' '$ART/tqaep.json' > '$ART/bundle.json'"
step "validate_bundle" "$L" bash -c "'$CLI' --root '$ART' validate --bundle '$ART/bundle.json' > '$ART/validate.json'; cat '$ART/validate.json'"

# ---------------------------------------------------------------- 5. refusal (negative, must be non-zero)
L="$RAW/QUAL_05_refusal.raw.log"
: > "$L"
step "refusal_missing_source" "$L" "$CLI" --root "$ART" intake --goal "nope" --source "$WT/examples/first-run/does-not-exist.txt"
step "refusal_no_artifact_written" "$L" bash -c "test ! -e '$ART/nope.json' && echo 'no artefact written for the refused intake'"
step "bad_bundle_refused" "$L" bash -c "'$CLI' --root '$ART' validate --bundle '$WT/does-not-exist-bundle.json'"

# ---------------------------------------------------------------- 6. digests of what was verified
L="$RAW/QUAL_06_digests.raw.log"
: > "$L"
step "wheel_and_assets" "$L" bash -c "sha256sum '$WHEEL' '$WT/dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip' '$WT/dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3-erratum1.zip'"
step "artefact_digests" "$L" bash -c "sha256sum '$ART'/intent.card.json '$ART'/pi.json '$ART'/pd.json '$ART'/ecp.json '$ART'/tqaep.json '$ART'/bundle.json"
step "validate_json" "$L" cat "$ART/validate.json"

echo "DONE rc-collection complete; logs in $RAW"
