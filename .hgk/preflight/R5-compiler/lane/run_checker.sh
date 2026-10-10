#!/usr/bin/env bash
# Host-side launcher for the R5 INDEPENDENT CHECKER lane (non-Maker / read-only on the product).
#   usage: run_checker.sh <brief-name.md> <log-name.txt> [timeout_seconds]
#
# Difference from run_lane2.sh (the Maker lane):
#   * /w is mounted READ-ONLY. The checker physically cannot modify the product tree,
#     which is what makes its verdict independent of the Maker's write authority.
#   * a dedicated host scratch (AO_OUT) is mounted rw at /ao so every artefact the checker
#     produces is readable from the host afterwards.
#   * AO_OUT lives OUTSIDE the product tree, deliberately. An earlier revision put it at
#     $LANE/ao_out (inside the repo) and the checker's own venv then broke the product's own
#     walkers - `pipd doctor` and `pipd export` died with WinError 1920 on
#     ao_out/venv/lib64 - so the verifier's artefacts looked like product failures. That is the
#     same class of defect as the R4 "verifier and subject in the same tree" incidents. The
#     guard below refuses to start rather than silently reintroducing it.
#   * no PIPD_PROJECT_ALLOWED_ROOTS is injected: the checker must pass --allow-root explicitly.
set -uo pipefail
BRIEF="${1:?brief name required}"
LOG="${2:?log name required}"
TMO="${3:-1800}"
LANE="/c/Projects/Agent_Workspace/PIPD/.hgk/preflight/R5-compiler/lane"
PRODUCT="C:/Projects/Agent_Workspace/PIPD"
AO_OUT="${AO_OUT:-C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/r5-ao-lane}"
MODEL_PORT="${MODEL_PORT:-10100}"
cd "$LANE" || exit 1

# Guard: the checker's writable scratch must not sit inside the tree it is judging.
case "$(echo "$AO_OUT" | tr '\\' '/')" in
  "$PRODUCT"|"$PRODUCT"/*)
    echo "[checker] REFUSING to start: AO_OUT ($AO_OUT) is inside the product tree ($PRODUCT)." >&2
    echo "[checker] The checker's venv/scratch would be copied and walked by the product's own" >&2
    echo "[checker] commands and would be misread as product failures. Move AO_OUT outside." >&2
    exit 4 ;;
esac

mkdir -p "$AO_OUT"
echo "[checker] start $(date -u +%FT%TZ) brief=$BRIEF image=pipd-r4-writer:4 port=$MODEL_PORT timeout=$TMO" | tee "$LOG"
echo "[checker] ao_out (outside the product tree)=$AO_OUT" | tee -a "$LOG"
docker run --rm --cap-add=NET_ADMIN \
  --add-host=host.docker.internal:host-gateway \
  -v "C:/Projects/Agent_Workspace/PIPD:/w:ro" \
  -v "C:/Users/user/AppData/Local/HG-KSEOS/codex-hermes:/cx:ro" \
  -v "$LANE:/briefs:ro" \
  -v "$AO_OUT:/ao" \
  -e MODEL_HOST_PORT="$MODEL_PORT" -e LANE_TIMEOUT="$TMO" \
  pipd-r4-writer:4 bash -lc '
    set -u
    mkdir -p /root/.codex
    printf "model = \"opencode-go/deepseek-v4.1-flash\"\nopenai_base_url = \"http://host.docker.internal:%s/v1\"\nmodel_catalog_json = \"/cx/opencodex-catalog.json\"\napproval_policy = \"never\"\n" "$MODEL_HOST_PORT" > /root/.codex/config.toml
    cd /ao || exit 3
    timeout "$LANE_TIMEOUT" codex exec -s danger-full-access -c approval_policy=never --skip-git-repo-check "$(cat /briefs/"'"$BRIEF"'")"
    echo "[checker] codex_exit=$?"
  ' 2>&1 | tee -a "$LOG" | tail -100
echo "[checker] done $(date -u +%FT%TZ)" | tee -a "$LOG"
