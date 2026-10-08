#!/usr/bin/env bash
# Independent acceptance lane launcher.
#   * the prompt is read from a file, never from an inline command substitution
#   * stdout/stderr are line-buffered into the verdict log so progress is observable
#   * the model/provider pair is the VERIFY lane, never the maker lane
set -euo pipefail
SRC="/c/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent"
export HERMES_HOME='C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes'
PROMPT="/c/Projects/Agent_Workspace/PIPD/.hgk/ao/ao_s2s4_prompt.md"
LOG="/c/Projects/Agent_Workspace/PIPD/.hgk/ao/ao_s2s4_verdict.log"
cd "$SRC"
echo "[lane] start $(date -u +%FT%TZ) prompt_bytes=$(wc -c < "$PROMPT")" >> "$LOG"
stdbuf -oL -eL ./venv/Scripts/python.exe -u hermes_cli/main.py \
  -z "$(cat "$PROMPT")" -m glm-5.3-flash --provider opencode-go --yolo >> "$LOG" 2>&1
echo "[lane] exit=$? $(date -u +%FT%TZ)" >> "$LOG"
