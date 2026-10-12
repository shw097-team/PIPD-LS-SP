#!/usr/bin/env bash
# FAR research lane on the declared checker model (research must not be done by the maker lane it studies).
# Model: gpt-6.1-sol, provider openai (OAuth), reasoning effort medium.
# Read-only wrt the candidate: writes only under the round's verify/far/.
set -u
WT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
R="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
W="$R/stage-b"
V="$R/verify/far"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
MODEL="${CHECK_MODEL:-gpt-6.1-sol}"
mkdir -p "$V"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
cd "$WT" || exit 1
echo "FAR_LANE=$STAMP MODEL=$MODEL provider=openai reasoning=medium (declared checker; research lane)"
timeout 3000 "$CB" -c model="$MODEL" \
  -c model_reasoning_effort='"medium"' \
  -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
  exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
  < "$W/FAR_BRIEF_MODEL_DEVIATION.md" > "$W/FAR_${STAMP}.log" 2>&1
echo "$?" > "$W/FAR_${STAMP}.exit"
echo "FAR exit=$(cat "$W/FAR_${STAMP}.exit") log=$W/FAR_${STAMP}.log"
echo "FAR_LANE_DONE"
