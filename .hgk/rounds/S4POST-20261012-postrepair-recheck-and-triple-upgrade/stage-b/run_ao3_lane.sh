#!/usr/bin/env bash
# Third-round independent acceptance lane (VERIFY/SECURITY) on the DECLARED checker model.
# Model: gpt-6.1-sol, provider openai (OAuth), reasoning effort medium - the declared checker model.
# Read-only wrt the candidate: the brief permits writes only under the round's verify/ao3/.
set -u
WT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
R="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
W="$R/stage-b"
V="$R/verify/ao3"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
MODEL="${CHECK_MODEL:-gpt-6.1-sol}"
mkdir -p "$V"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
cd "$WT" || exit 1
echo "AO3_LANE=$STAMP MODEL=$MODEL provider=openai reasoning=medium (declared checker)"
timeout 3000 "$CB" -c model="$MODEL" \
  -c model_reasoning_effort='"medium"' \
  -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
  exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
  < "$W/VERIFIER_AO3_BRIEF.md" > "$W/AO3_${STAMP}.log" 2>&1
echo "$?" > "$W/AO3_${STAMP}.exit"
echo "AO3 exit=$(cat "$W/AO3_${STAMP}.exit") log=$W/AO3_${STAMP}.log"
echo "AO3_LANE_DONE"
