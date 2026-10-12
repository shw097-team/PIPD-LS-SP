#!/usr/bin/env bash
# S4POST Stage B resumed round, attempt 3: bounded writer lanes on the DECLARED BACKUP model.
# Reason for the substitution (D-03 class): the declared EXECUTE model opencode-go/deepseek-v4.1-flash
# aborts with "The `reasoning_content` in the thinking mode must be passed back to the API"
# (HTTP 400, upstream) once the transcript grows; measured 3/3 lanes in attempt 2 of this round.
# The backup opencode-go/deepseek-v4-flash was probed healthy with a one-line echo before this run.
set -u
WT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
W="$WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
MODEL="${EXEC_MODEL:-opencode-go/deepseek-v4-flash}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
cd "$WT" || exit 1
echo "LANE_SET=$STAMP MODEL=$MODEL (backup; declared model aborts on the thinking-mode adapter bug)"
printf '%s\n' "$MODEL" > "$W/MODEL_DECLARED_$STAMP.txt"

for L in "$@"; do
  (
    timeout 3000 "$CB" -c model="$MODEL" \
      -c model_reasoning_effort='"none"' \
      -c openai_base_url='http://127.0.0.1:10102/v1' \
      -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
      exec --cd "$WT" --skip-git-repo-check -s danger-full-access - \
      < "$W/WRITER_${L}_BRIEF_v2.md" > "$W/${L}_attempt3_${STAMP}.log" 2>&1
    echo "$?" > "$W/${L}_attempt3_${STAMP}.exit"
  ) &
done
wait
for L in "$@"; do echo "$L exit=$(cat "$W/${L}_attempt3_${STAMP}.exit" 2>/dev/null) log=$W/${L}_attempt3_${STAMP}.log"; done
echo "LANES_DONE"
