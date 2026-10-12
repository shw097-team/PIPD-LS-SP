#!/usr/bin/env bash
# Second-round independent acceptance lane (VERIFY/SECURITY) on the DECLARED checker model.
# Model: gpt-6.1-sol, provider openai (OAuth), reasoning effort medium - the declared checker model.
# Read-only with respect to the candidate: the brief permits writes only under verify/ao2/.
set -u
WT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
W="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b"
V="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
MODEL="${CHECK_MODEL:-gpt-6.1-sol}"
mkdir -p "$V"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
cd "$WT" || exit 1
echo "AO2_LANE=$STAMP MODEL=$MODEL provider=openai reasoning=medium (declared checker)"
timeout 3000 "$CB" -c model="$MODEL" \
  -c model_reasoning_effort='"medium"' \
  -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
  exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
  < "$W/VERIFIER_AO2_BRIEF.md" > "$W/AO2_${STAMP}.log" 2>&1
echo "$?" > "$W/AO2_${STAMP}.exit"
echo "AO2 exit=$(cat "$W/AO2_${STAMP}.exit") log=$W/AO2_${STAMP}.log"
echo "AO2_LANE_DONE"
