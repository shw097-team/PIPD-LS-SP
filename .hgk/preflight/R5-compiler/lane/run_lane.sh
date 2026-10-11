#!/usr/bin/env bash
# Host-side launcher for the R5 bounded EXECUTE lane (container-enforced write scope).
#   usage: run_lane.sh <brief-name.md> <log-name.txt>
# Mount allowlist IS the primary boundary: only the admitted WriteSet (the PIPD repo) is rw.
set -uo pipefail
BRIEF="$1"
LOG="$2"
LANE="/c/Projects/Agent_Workspace/PIPD/.hgk/preflight/R5-compiler/lane"
MODEL_PORT="${MODEL_PORT:-10100}"
cd "$LANE" || exit 1
echo "[lane] start $(date -u +%FT%TZ) brief=$BRIEF model=opencode-go/deepseek-v4.1-flash image=pipd-r4-writer:4" | tee "$LOG"
docker run --rm --cap-add=NET_ADMIN --add-host=host.docker.internal:host-gateway \
  -v "C:/Projects/Agent_Workspace/PIPD:/w" \
  -v "C:/Users/user/AppData/Local/HG-KSEOS/codex-hermes:/cx:ro" \
  -v "C:/Projects/Agent_Workspace/PIPD/.hgk/preflight/R5-compiler/lane:/briefs:ro" \
  -e MODEL_HOST_PORT="$MODEL_PORT" pipd-r4-writer:4 bash -lc '
    mkdir -p /root/.codex
    printf "model = \"opencode-go/deepseek-v4.1-flash\"\nopenai_base_url = \"http://host.docker.internal:'"$MODEL_PORT"'/v1\"\nmodel_catalog_json = \"/cx/opencodex-catalog.json\"\napproval_policy = \"never\"\n" > /root/.codex/config.toml
    cd /w || exit 3
    timeout 1500 codex exec -s danger-full-access -c approval_policy=never --skip-git-repo-check "$(cat /briefs/'"$BRIEF"')"
    echo "[lane] codex_exit=$?"
  ' 2>&1 | tee -a "$LOG" | tail -60
echo "[lane] done $(date -u +%FT%TZ)" | tee -a "$LOG"
