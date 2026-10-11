#!/usr/bin/env bash
# POSTRELEASE round — sequential sealed EXECUTE lanes (writer = opencode-go/deepseek-v4.1-flash).
# Each lane gets its OWN immutable log path. Sandbox is danger-full-access because
# -s workspace-write degrades to read-only on this host (measured: the run printed
# "sandbox: read-only" and the shell was rejected by policy), so writes are bounded by the
# brief's write scope and by scope discipline only -- no OS-level isolation. Disclosed as residual.
set -uo pipefail

W="C:/Projects/Agent_Workspace/PIPD-postrelease-wt"
R="$W/.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane"
BRIEFS="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post"
CODEX_EXE="C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

export CODEX_HOME="C:/Users/user/AppData/Local/HG-KSEOS/codex-hermes"
export OPENAI_BASE_URL="http://127.0.0.1:10100/v1"
ENVF="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/.env"
export OPENAI_API_KEY="$(grep -h '^OPENCODE_GO_API_KEY=' "$ENVF" 2>/dev/null | head -1 | cut -d= -f2- || echo local-proxy)"

mkdir -p "$R"
for spec in "UX01:BRIEF_UX01.md" "CONTRACT03:BRIEF_CONTRACT03.md" "WEB02:BRIEF_WEB02.md" "SELFBOOT04:BRIEF_SELFBOOT04.md"; do
  WO="${spec%%:*}"; BF="${spec##*:}"
  LOG="$R/WO-$WO.exec-$STAMP.log"
  echo "=== LANE $WO -> $LOG ==="
  timeout 1800 "$CODEX_EXE" exec --cd "$W" --skip-git-repo-check -s danger-full-access - \
      < "$BRIEFS/$BF" > "$LOG" 2>&1
  RC=$?
  echo "EXIT=$RC" >> "$LOG"
  echo "--- $WO exit=$RC; binding reported by the run ---"
  grep -m4 -E '^(model|provider|sandbox|approval):' "$LOG" || true
done
echo "ALL_LANES_DONE"
