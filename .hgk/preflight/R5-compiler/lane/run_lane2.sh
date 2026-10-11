#!/usr/bin/env bash
# Host-side launcher for the R5 bounded EXECUTE lane (container-enforced write scope).
#   usage: run_lane2.sh <brief-name.md> <log-name.txt> [timeout_seconds]
#
# Boundary model (unchanged from the prior round's validated pattern):
#   primary  = docker mount allowlist: only the admitted WriteSet (the PIPD repo) is rw;
#              /cx is ro, /briefs is ro, no credentials, no git binary in the image;
#   second   = lane-entry.sh egress lock inside the image (loopback + host gateway only),
#              which self-verifies by probing the model endpoint and degrades loudly if it
#              cannot reach it.
# Model route: opencodex proxy (host loopback 127.0.0.1:10101) fronted by bridge.py on
# 0.0.0.0:10100, because the proxy refuses data-plane requests whose Host header is not
# localhost/127.0.0.1. The bridge rewrites Host. Verified: HTTP 200 from inside the container.
set -uo pipefail
BRIEF="${1:?brief name required}"
LOG="${2:?log name required}"
TMO="${3:-1800}"
LANE="/c/Projects/Agent_Workspace/PIPD/.hgk/preflight/R5-compiler/lane"
MODEL_PORT="${MODEL_PORT:-10100}"
cd "$LANE" || exit 1
echo "[lane] start $(date -u +%FT%TZ) brief=$BRIEF model=opencode-go/deepseek-v4.1-flash image=pipd-r4-writer:4 port=$MODEL_PORT timeout=$TMO" | tee "$LOG"
docker run --rm --cap-add=NET_ADMIN \
  --add-host=host.docker.internal:host-gateway \
  -v "C:/Projects/Agent_Workspace/PIPD:/w" \
  -v "C:/Users/user/AppData/Local/HG-KSEOS/codex-hermes:/cx:ro" \
  -v "C:/Projects/Agent_Workspace/PIPD/.hgk/preflight/R5-compiler/lane:/briefs:ro" \
  -e MODEL_HOST_PORT="$MODEL_PORT" -e LANE_TIMEOUT="$TMO" \
  -e PIPD_PROJECT_ALLOWED_ROOTS="/w/dist" \
  pipd-r4-writer:4 bash -lc '
    set -u
    mkdir -p /root/.codex
    printf "model = \"opencode-go/deepseek-v4.1-flash\"\nopenai_base_url = \"http://host.docker.internal:%s/v1\"\nmodel_catalog_json = \"/cx/opencodex-catalog.json\"\napproval_policy = \"never\"\n" "$MODEL_HOST_PORT" > /root/.codex/config.toml
    cd /w || exit 3
    timeout "$LANE_TIMEOUT" codex exec -s danger-full-access -c approval_policy=never --skip-git-repo-check "$(cat /briefs/"'"$BRIEF"'")"
    echo "[lane] codex_exit=$?"
  ' 2>&1 | tee -a "$LOG" | tail -100
echo "[lane] done $(date -u +%FT%TZ)" | tee -a "$LOG"
