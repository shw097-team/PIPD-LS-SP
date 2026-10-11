#!/usr/bin/env bash
# F-R5-08 symlink/TOCTOU negative, run inside the disposable Linux container (root can create
# symlinks; the Windows host cannot - WinError 1314). The product tree is mounted READ-ONLY; every
# write target is a disposable scratch under /sym. Usage: symlink_negative.sh
set -uo pipefail
PY="python3 -B -m pipd_ls_sp.cli"
export PYTHONPATH=/w/src
B=/sym/base
rm -rf "$B"; mkdir -p "$B/outside" "$B/allowed" "$B/work"
CANARY="$B/outside/canary.txt"; echo "CANARY-ORIGINAL" > "$CANARY"
before=$(sha256sum "$CANARY" | cut -d' ' -f1)
echo "{\"case\":\"setup\",\"canary_sha_before\":\"$before\"}"

run() {  # id, expected, argv...
  local id="$1"; shift; local expect="$1"; shift
  local out rc
  out=$(cd "$B/work" && $PY "$@" 2>&1); rc=$?
  printf '{"case":"%s","argv":"%s","exit":%d,"expect":"%s","stdout_tail":"%s"}\n' \
    "$id" "$*" "$rc" "$expect" "$(printf '%s' "$out" | tr -d '\n' | tail -c 320)"
}

# 1. destination is a symlink pointing outside the allowed root
ln -sfn "$B/outside" "$B/link_out"
run "A1_symlink_escape_destination" "refuse UNSAFE_DESTINATION" --root /w project --out "$B/link_out" --allow-root "$B/allowed"

# 2. path traversal through the allowed root
run "A2_traversal_destination" "refuse" --root /w project --out "$B/allowed/../outside/esc" --allow-root "$B/allowed"

# 3. destination inside a symlinked parent (allowed root itself is a symlink)
ln -sfn "$B/outside" "$B/allowed_link"
run "A3_symlinked_allowed_root" "refuse" --root /w project --out "$B/allowed_link/esc" --allow-root "$B/allowed_link"

# 4. TOCTOU: pre-create the destination as a real directory, then swap it for a symlink before the run
mkdir -p "$B/allowed/target"; rm -rf "$B/allowed/target"; ln -sfn "$B/outside" "$B/allowed/target"
run "A4_toctou_swapped_destination" "refuse" --root /w project --out "$B/allowed/target" --allow-root "$B/allowed"

# 5. control: a genuinely safe empty destination DOES publish (proves the resolver discriminates)
run "A5_safe_control" "PASS" --root /w project --out "$B/allowed/safe" --allow-root "$B"

after=$(sha256sum "$CANARY" | cut -d' ' -f1)
leaked=$(find "$B/outside" -type f | wc -l)
printf '{"case":"after","canary_sha_after":"%s","canary_unchanged":%s,"files_under_outside":%d}\n' \
  "$after" "$([ "$before" = "$after" ] && echo true || echo false)" "$leaked"
