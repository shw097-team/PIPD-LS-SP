#!/usr/bin/env bash
# FAR candidate independent acceptance lane - Codex CLI, checker model gpt-6.1-sol (medium),
# OpenAI OAuth path (the owner-declared VERIFY/SECURITY lane). Fresh clone, read-only subject.
set -u
SUBJECT="${1:-ad33c0c679ac329a38cb9b0c0127a51211e3e09e}"
REPO=C:/Projects/Agent_Workspace/PIPD
CLONE=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-far-verify-decl
ROUND=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-a-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
LOG="$ROUND/verify/FAR_VERIFY_SUBJECT_${SUBJECT:0:8}_gpt-6.1-sol_medium.log"

rm -rf "$CLONE"
git clone --quiet "$REPO" "$CLONE"
git -C "$CLONE" checkout --quiet "$SUBJECT"
echo "=== lane: clone=$CLONE subject=$(git -C "$CLONE" rev-parse HEAD) tree=$(git -C "$CLONE" rev-parse HEAD^{tree})"
echo "=== head -1 of the brief:"; head -1 "$ROUND/verify/FAR_CHECKER_BRIEF.md"

cd "$CLONE" || exit 2
timeout 2700 "$CB" -c model='gpt-6.1-sol' -c model_reasoning_effort='"medium"' \
  exec --skip-git-repo-check -s danger-full-access - < "$ROUND/verify/FAR_CHECKER_BRIEF.md" \
  > "$LOG" 2>&1
echo "FAR_VERIFY_EXIT=$?"
echo "=== 啟動標頭（模型身分證據）"; grep -m3 -E 'model:|provider:|reasoning effort:' "$LOG" | tr -d '\r'
echo "=== 收據尾"; tail -35 "$LOG" | tr -d '\r'
