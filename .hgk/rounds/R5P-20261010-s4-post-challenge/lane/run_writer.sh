#!/usr/bin/env bash
# Host-side launcher for the R5P bounded EXECUTE lane (container-enforced write scope).
#   usage: run_writer.sh <brief-name.md> <log-name.txt> [timeout_seconds]
#
# Boundary model (same pattern the R5 round validated):
#   primary = docker mount allowlist: the admitted WriteSet (the PIPD repo) is mounted rw at /w;
#             the brief directory is ro at /briefs; no credentials, no git binary in the image;
#   second  = the sanctioned sealed EXECUTE front door (127.0.0.1:10100) is the ONLY model route,
#             reached through bridge2.py on 0.0.0.0:10110 because the front door binds loopback only
#             and refuses a foreign Host header.
# The image carries codex-cli, python3 + jsonschema, and NO git: an unauthorised remote effect is
# structurally impossible rather than policy-forbidden.
set -uo pipefail
BRIEF="${1:?brief name required}"
LOG="${2:?log name required}"
TMO="${3:-2700}"
LANE="/c/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5P-20261010-s4-post-challenge/lane"
MODEL_PORT="${MODEL_PORT:-10110}"
cd "$LANE" || exit 1
echo "[writer] start $(date -u +%FT%TZ) brief=$BRIEF model=opencode-go/deepseek-v4.1-flash image=pipd-r4-writer:4 port=$MODEL_PORT timeout=$TMO" | tee "$LOG"
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -v "C:/Projects/Agent_Workspace/PIPD:/w" \
  -v "$LANE:/briefs:ro" \
  -e MODEL_HOST_PORT="$MODEL_PORT" -e LANE_TIMEOUT="$TMO" \
  pipd-r4-writer:4 bash -lc '
    set -u
    mkdir -p /root/.codex
    printf "model = \"opencode-go/deepseek-v4.1-flash\"\nmodel_provider = \"hgk_execute_door\"\napproval_policy = \"never\"\nmodel_reasoning_effort = \"medium\"\n\n[model_providers.hgk_execute_door]\nname = \"HGK-EXECUTE-Door\"\nbase_url = \"http://host.docker.internal:%s/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = false\nrequest_max_retries = 0\nstream_max_retries = 0\n" "$MODEL_HOST_PORT" > /root/.codex/config.toml
    cd /w || exit 3
    timeout "$LANE_TIMEOUT" codex exec -s danger-full-access -c approval_policy=never --skip-git-repo-check "$(cat /briefs/'"'"$BRIEF"'"')"
    echo "[writer] codex_exit=$?"
  ' 2>&1 | tee -a "$LOG" | tail -120
echo "[writer] done $(date -u +%FT%TZ)" | tee -a "$LOG"
