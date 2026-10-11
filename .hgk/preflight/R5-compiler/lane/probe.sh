#!/usr/bin/env bash
# R5 lane probe: identity, egress admission, mount-allowlist negative matrix, model + codex route.
# Runs INSIDE the writer container. Prints one machine-readable line per probe.
set -uo pipefail

MODEL_PORT="${MODEL_HOST_PORT:-10100}"
echo "[probe] whoami=$(id -un) cwd=$(pwd) python=$(python3 -V 2>&1)"
echo "[probe] image_tools codex=$(codex --version 2>&1) git=$(command -v git || echo ABSENT)"

mkdir -p /root/.codex
cat > /root/.codex/config.toml <<EOF
model = "opencode-go/deepseek-v4.1-flash"
openai_base_url = "http://host.docker.internal:${MODEL_PORT}/v1"
model_catalog_json = "/cx/opencodex-catalog.json"
approval_policy = "never"
EOF
echo "[probe] codex_config_written=1"

python3 - <<'PY'
try:
    import jsonschema
    print("[probe] jsonschema=%s" % jsonschema.__version__)
except Exception as exc:
    print("[probe] jsonschema=ABSENT(%s)" % exc)
PY

# ---- negative matrix -------------------------------------------------------
mkdir -p /w/.hgk/r5-lane-probe
echo "admitted-$(date -u +%s)" > /w/.hgk/r5-lane-probe/admitted.txt && echo "[probe] admitted_write=SUCCEEDED" || echo "[probe] admitted_write=FAILED"

if (echo x > /cx/escape.txt) 2>/dev/null; then echo "[probe] ro_mount_write=SUCCEEDED_UNEXPECTED"; else echo "[probe] ro_mount_write=DENIED"; fi

if (echo x > /w-escape/escape.txt) 2>/dev/null; then echo "[probe] unmounted_write=SUCCEEDED_UNEXPECTED"; else echo "[probe] unmounted_write=DENIED"; fi

ln -sfn /cx /w/.hgk/r5-lane-probe/symlink-escape 2>/dev/null
if (echo x > /w/.hgk/r5-lane-probe/symlink-escape/via-link.txt) 2>/dev/null; then echo "[probe] symlink_escape=SUCCEEDED_UNEXPECTED"; else echo "[probe] symlink_escape=DENIED"; fi
rm -f /w/.hgk/r5-lane-probe/symlink-escape

if (echo x > /nonexistent-host-dir/probe.txt) 2>/dev/null; then echo "[probe] foreign_abs_write=SUCCEEDED_UNEXPECTED"; else echo "[probe] foreign_abs_write=DENIED"; fi

if [ -e "/run/secrets" ] || [ -e "/root/.ssh" ]; then echo "[probe] secret_path=PRESENT_UNEXPECTED"; else echo "[probe] secret_path=ABSENT"; fi

# ---- egress ---------------------------------------------------------------
EG=$(curl -s -o /dev/null -w '%{http_code}' --max-time 6 http://example.com 2>/dev/null || echo TIMEOUT)
echo "[probe] egress_external=${EG:-TIMEOUT}"
MEG=$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 "http://host.docker.internal:${MODEL_PORT}/v1/models" || echo FAIL)
echo "[probe] model_endpoint=${MEG}"

# ---- codex lane call ------------------------------------------------------
cd /w || exit 3
OUT=$(timeout 240 codex exec -s workspace-write --skip-git-repo-check \
        "Reply with exactly the token CODEX_R5_LANE_OK and nothing else." 2>&1)
echo "[probe] codex_exit=$?"
if printf '%s' "$OUT" | grep -q "CODEX_R5_LANE_OK"; then echo "[probe] lane_codex=CODEX_R5_LANE_OK"; else echo "[probe] lane_codex=NO_TOKEN"; fi
printf '%s\n' "$OUT" | tail -5
exit 0
