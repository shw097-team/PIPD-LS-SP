#!/usr/bin/env bash
# S4POST Stage B resumed round: three parallel bounded writer lanes on the DECLARED model.
set -u
WT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
W="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
MODEL="${EXEC_MODEL:-opencode-go/deepseek-v4.1-flash}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
cd "$WT" || exit 1
echo "LANE_SET=$STAMP MODEL=$MODEL"
echo "$MODEL" > "$W/MODEL_DECLARED_$STAMP.txt"

for L in B1 B2 B3; do
  (
    timeout 2700 "$CB" -c model="$MODEL" -c openai_base_url='http://127.0.0.1:10102/v1' \
      -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
      exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
      < "$W/WRITER_${L}_BRIEF_v2.md" > "$W/${L}_${STAMP}.log" 2>&1
    echo "$?" > "$W/${L}_${STAMP}.exit"
  ) &
done
wait
for L in B1 B2 B3; do echo "$L exit=$(cat "$W/${L}_${STAMP}.exit" 2>/dev/null) log=$W/${L}_${STAMP}.log"; done
echo "LANES_DONE"
