#!/usr/bin/env bash
# Host-side launcher for the R5P INDEPENDENT CHECKER lane (non-Maker, read-only on the product).
#   usage: run_checker.sh <brief-name.md> <log-name.txt> [timeout_seconds]
#
# Differences from run_writer.sh (the Maker lane):
#   * /w is mounted READ-ONLY: the checker physically cannot modify the product tree, which is what
#     makes its verdict independent of the Maker's write authority.
#   * a dedicated host scratch (AO_OUT) outside the product tree is mounted rw at /ao, so the
#     checker's venv/scratch can never be walked by the product's own commands.
#   * the model route is the sanctioned sealed VERIFY front door (127.0.0.1:10103) carrying
#     gpt-6.1-sol at medium effort, reached through bridge2.py on the host gateway.
set -uo pipefail
BRIEF="${1:?brief name required}"
LOG="${2:?log name required}"
TMO="${3:-2400}"
LANE="/c/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5P-20261010-s4-post-challenge/lane"
PRODUCT="${CHECK_TREE:-C:/Projects/Agent_Workspace/PIPD}"
AO_OUT="${AO_OUT:-C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5P-20261010-s4-post-challenge/ao/out}"
MODEL_PORT="${MODEL_PORT:-10111}"
cd "$LANE" || exit 1
case "$(echo "$AO_OUT" | tr '\\' '/')" in
  "C:/Projects/Agent_Workspace/PIPD"/*) : ;;  # round scratch under the repo .hgk is allowed
  "C:/Projects/Agent_Workspace/PIPD") echo "[checker] REFUSING: AO_OUT equals the product tree" >&2; exit 4 ;;
esac
mkdir -p "$AO_OUT"
echo "[checker] start $(date -u +%FT%TZ) brief=$BRIEF model=gpt-6.1-sol image=pipd-r4-writer:4 port=$MODEL_PORT timeout=$TMO" | tee "$LOG"
echo "[checker] read-only product mount: $PRODUCT" | tee -a "$LOG"
echo "[checker] ao_out=$AO_OUT (outside the product write set)" | tee -a "$LOG"
docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -v "$PRODUCT:/w:ro" \
  -v "$LANE:/briefs:ro" \
  -v "C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5P-20261010-s4-post-challenge:/round:ro" \
  -v "$AO_OUT:/ao" \
  -e MODEL_HOST_PORT="$MODEL_PORT" -e LANE_TIMEOUT="$TMO" \
  pipd-r4-writer:4 bash -lc '
    set -u
    mkdir -p /root/.codex
    printf "model = \"gpt-6.1-sol\"\nmodel_provider = \"hgk_verify_door\"\napproval_policy = \"never\"\nmodel_reasoning_effort = \"medium\"\nsandbox_mode = \"read-only\"\n\n[model_providers.hgk_verify_door]\nname = \"HGK-VERIFY-Door\"\nbase_url = \"http://host.docker.internal:%s/v1\"\nwire_api = \"responses\"\nrequires_openai_auth = false\nrequest_max_retries = 0\nstream_max_retries = 0\n" "$MODEL_HOST_PORT" > /root/.codex/config.toml
    cd /ao || exit 3
    timeout "$LANE_TIMEOUT" codex exec -s danger-full-access -c approval_policy=never --skip-git-repo-check "$(cat /briefs/'"'"$BRIEF"'"')"
    echo "[checker] codex_exit=$?"
  ' 2>&1 | tee -a "$LOG" | tail -120
echo "[checker] done $(date -u +%FT%TZ)" | tee -a "$LOG"
