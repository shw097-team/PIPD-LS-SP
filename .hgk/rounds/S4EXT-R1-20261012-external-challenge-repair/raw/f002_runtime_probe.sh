#!/usr/bin/env bash
# S4EXT-R1 / TT-S4EXT-002 + F002 -- the runtime escalation probe.
#
# The external report graded F002 "CONFIRMED_DEFECT (Schema-level), pending a real CLI counterexample"
# and explicitly said it had NOT run `pipd validate` from the published wheel. This script closes that
# gap from the local side: the SAME tampered bundle is fed to
#
#   (A) the PUBLISHED installed wheel (pipd_ls_sp-0.1.1a3, sha256 e8ca509d...) -- the subject whose
#       bytes were published, and
#   (B) the REPAIRED candidate source tree,
#
# so the defect's grade and the repair's effect are both observed, not asserted.
set -u
WT="C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt"
RAW="$WT/.hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw"
WORK="C:/Users/user/AppData/Local/Temp/pipd-s4ext-r1-qual"
VENVPY="$WORK/venv/Scripts/python.exe"
VENVCLI="$WORK/venv/Scripts/pipd.exe"
ART="$WORK/art"
L="$RAW/QUAL_07_f002_runtime_probe.raw.log"
: > "$L"

echo "### building the tampered bundles from the honest artefacts" >> "$L"
"$VENVPY" - "$ART" >> "$L" 2>&1 <<'PY'
import json, pathlib, sys
art = pathlib.Path(sys.argv[1])
good = json.loads((art / "pi.json").read_text(encoding="utf-8"))
trace = good.get("trace")
assert isinstance(trace, list) and trace, f"no trace array in pi.json: {list(good)}"
print("pi trace entries:", len(trace))
print("trace[0] keys:", sorted(trace[0]))

# bad 1: wrong TYPES on the endpoints (still an object with every required key present)
bad_types = json.loads(json.dumps(good))
bad_types["trace"][0]["from_hash"] = 12345
bad_types["trace"][0]["to_id"] = {"not": "a string"}
# bad 2: an endpoint id that is a well-formed string but present nowhere in the bundle (orphan)
bad_orphan = json.loads(json.dumps(good))
bad_orphan["trace"][0]["to_id"] = "PI-0000000000000000"
# bad 3: a syntactically valid 64-hex hash that is simply wrong
bad_hash = json.loads(json.dumps(good))
bad_hash["trace"][0]["from_hash"] = "0" * 64

for name, doc in (("pi_bad_types.json", bad_types), ("pi_bad_orphan.json", bad_orphan),
                  ("pi_bad_hash.json", bad_hash)):
    (art / name).write_text(json.dumps(doc, indent=1), encoding="utf-8")
    bundle = {
        "PI-PKG": doc,
        "PD-PKG": json.loads((art / "pd.json").read_text(encoding="utf-8")),
        "ECP": json.loads((art / "ecp.json").read_text(encoding="utf-8")),
        "TQAEP": json.loads((art / "tqaep.json").read_text(encoding="utf-8")),
    }
    (art / name.replace("pi_", "bundle_")).write_text(json.dumps(bundle, indent=1), encoding="utf-8")
print("wrote tampered bundles:", sorted(p.name for p in art.glob("bundle_*.json")))
PY

probe() {  # probe <label> <cli-invocation...>
  local label="$1"; shift
  echo "### $label" >> "$L"
  echo "\$ $*" >> "$L"
  "$@" >> "$L" 2>&1
  echo "exit_code=$?" >> "$L"
}

echo "=== (A) PUBLISHED installed wheel $("$VENVPY" -m pip show pipd-ls-sp | grep -i ^version) ===" >> "$L"
probe "A_good_bundle"          "$VENVCLI" --root "$ART" validate --bundle "$ART/bundle.json"
probe "A_bad_types_bundle"     "$VENVCLI" --root "$ART" validate --bundle "$ART/bundle_bad_types.json"
probe "A_bad_orphan_bundle"    "$VENVCLI" --root "$ART" validate --bundle "$ART/bundle_bad_orphan.json"
probe "A_bad_hash_bundle"      "$VENVCLI" --root "$ART" validate --bundle "$ART/bundle_bad_hash.json"

echo "=== (B) REPAIRED candidate source tree ===" >> "$L"
CAND() { PYTHONPATH="$WT/src" "$VENVPY" -B -m pipd_ls_sp.cli "$@"; }
probe "B_good_bundle"          bash -c "PYTHONPATH='$WT/src' '$VENVPY' -B -m pipd_ls_sp.cli --root '$ART' validate --bundle '$ART/bundle.json'"
probe "B_bad_types_bundle"     bash -c "PYTHONPATH='$WT/src' '$VENVPY' -B -m pipd_ls_sp.cli --root '$ART' validate --bundle '$ART/bundle_bad_types.json'"
probe "B_bad_orphan_bundle"    bash -c "PYTHONPATH='$WT/src' '$VENVPY' -B -m pipd_ls_sp.cli --root '$ART' validate --bundle '$ART/bundle_bad_orphan.json'"
probe "B_bad_hash_bundle"      bash -c "PYTHONPATH='$WT/src' '$VENVPY' -B -m pipd_ls_sp.cli --root '$ART' validate --bundle '$ART/bundle_bad_hash.json'"

echo "DONE -- see $L"
