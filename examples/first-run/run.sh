#!/usr/bin/env bash
# PIPD-LS-SP first run — portable, self-locating, no developer paths.
#
# Runs the whole chain in ONE command on any checkout:
#     preconditions -> doctor -> intake -> compile-pi -> bind-pd -> compile-ecp
#     -> compile-tqaep -> assemble -> validate -> refusal check
#
# Every path is derived from this script's own location; the scratch workspace is created
# outside the checkout. Nothing here depends on the author's machine, on an exported
# PYTHONPATH, or on a hard-coded interpreter path: set PYTHON=<interpreter> to override the
# auto-detection. Exit 0 means every POSITIVE step exited 0 AND the NEGATIVE step refused with a
# non-zero exit code; a missing precondition exits 3 with a typed reason on stderr.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"

fail() { echo "PRECONDITION_FAIL: $*" >&2; exit 3; }

# Native tools (python, git, ...) do NOT translate MSYS paths such as /c/... ; hand them
# Windows-style forward-slash paths. cygpath -m is the portable way to produce one.
npath() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s' "$1"; fi
}

# ---------------------------------------------------------------- preconditions
PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then PY="$candidate"; break; fi
  done
fi
[ -n "$PY" ] || fail "no python3/python on PATH (set PYTHON=<interpreter>)"

"$PY" - <<'PYEOF' || fail "Python >= 3.11 with the 'jsonschema' package is required"
import sys
if sys.version_info < (3, 11):
    raise SystemExit(f"python >= 3.11 required, found {sys.version.split()[0]}")
try:
    import jsonschema  # noqa: F401
except ImportError:
    raise SystemExit("jsonschema is not importable (pip install 'jsonschema>=4.0')")
PYEOF

# Prefer an installed distribution (no PYTHONPATH at all); otherwise use THIS checkout's src/.
SRC_ROOT="$(npath "$ROOT")"
if command -v pipd >/dev/null 2>&1; then
  MODE="installed"
  cli() { pipd "$@"; }
elif [ -f "$ROOT/src/pipd_ls_sp/cli.py" ]; then
  MODE="source ($SRC_ROOT/src)"
  export PYTHONPATH="$SRC_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
  cli() { "$PY" -B -m pipd_ls_sp.cli "$@"; }
else
  fail "no installed 'pipd' and no src/pipd_ls_sp/cli.py under $ROOT"
fi

ART="${PIPD_FIRST_RUN_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/pipd-first-run.XXXXXX")}"
ART_N="$(npath "$ART")"          # native form handed to the interpreter
CTX="$ART_N/ctx"                 # the read-only directory bind-pd probes (empty => stable digests)
mkdir -p "$CTX"
SRC="$SRC_ROOT/examples/first-run/source.txt"
[ -f "$ROOT/examples/first-run/source.txt" ] || fail "fixture missing: $SRC"

echo "checkout : $ROOT"
echo "runner   : $MODE"
echo "workspace: $ART"
echo

step() { echo "--- $*"; }

step "doctor"
cli --root "$ART_N" doctor

step "intake"
cli --root "$ART_N" init >/dev/null
cli --root "$ART_N" intake \
  --goal "Compile this example clause source into a validated PI to PD to ECP to TQAEP chain." \
  --source "$SRC" \
  --constraint "candidate-only, no release" \
  --non-goal "no upstream document bodies copied" \
  > "$ART/intent.card.json"

step "compile-pi"
cli --root "$ART_N" compile-pi --intent "$ART_N/intent.card.json" --profile LITE > "$ART/pi.json"

step "bind-pd"
cli --root "$ART_N" bind-pd --pi "$ART_N/pi.json" --repo-root "$CTX" > "$ART/pd.json"

step "compile-ecp"
cli --root "$ART_N" compile-ecp --pd "$ART_N/pd.json" --pi "$ART_N/pi.json" > "$ART/ecp.json"

step "compile-tqaep"
cli --root "$ART_N" compile-tqaep --pi "$ART_N/pi.json" --ecp "$ART_N/ecp.json" \
  --maker HERMES-MAKER --checker GLM-5.3-FLASH-AO-LANE --checker-receipt deleg_example/lane-C \
  > "$ART/tqaep.json"

step "assemble (no CLI verb exists for this; the helper only re-serialises the four records)"
"$PY" "$(npath "$HERE/assemble_bundle.py")" \
  "$ART_N/pi.json" "$ART_N/pd.json" "$ART_N/ecp.json" "$ART_N/tqaep.json" > "$ART/bundle.json"

step "validate"
cli --root "$ART_N" validate --bundle "$ART_N/bundle.json"

step "negative: a source locator that does not exist must be refused, non-zero, with no artefact"
set +e
cli --root "$ART_N" intake --goal "must be refused" \
  --source "$SRC_ROOT/examples/first-run/missing.txt" \
  > "$ART/refusal.json" 2>"$ART/refusal.stderr"
REFUSAL_RC=$?
set -e
echo "refusal exit code: $REFUSAL_RC"
if [ "$REFUSAL_RC" -eq 0 ]; then
  echo "REFUSAL_FAIL: a missing source locator exited 0" >&2
  exit 1
fi
cat "$ART/refusal.json"

echo
echo "FIRST_RUN_OK: every positive step exited 0 and the refusal exited $REFUSAL_RC"
echo "artefacts under: $ART"
