#!/usr/bin/env bash
# Owner-mandated VERIFY/SECURITY lane — CODEX CLI, checker model gpt-6.1-sol (medium), OpenAI OAuth.
# Fresh clone of the product repo at the FROZEN subject commit; the checker works read-only inside it.
set -u
SUBJECT="389d3973da73e5740f0b4d290bacb92d1e8982f8"
REPO=C:/Projects/Agent_Workspace/PIPD
CLONE=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-r3-verify-decl
ROUND=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
LOG="$ROUND/verify/r3/AO_VERIFY_SUBJECT_389D3973_gpt-6.1-sol_medium.log"

rm -rf "$CLONE"
git clone --quiet "$REPO" "$CLONE"
git -C "$CLONE" checkout --quiet "$SUBJECT"
echo "SUBJECT_EXPECT=$SUBJECT"
echo "SUBJECT_HEAD=$(git -C "$CLONE" rev-parse HEAD)"
echo "SUBJECT_TREE=$(git -C "$CLONE" rev-parse 'HEAD^{tree}')"
echo "PRE_STATUS_LINES=$(git -C "$CLONE" status --porcelain | wc -l)"

cd "$CLONE" || exit 2
timeout 3000 "$CB" -c model='gpt-6.1-sol' \
  -c model_reasoning_effort='medium' \
  -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
  exec --skip-git-repo-check -s danger-full-access - \
  < "$ROUND/verify/r3/R3_CHECKER_BRIEF.md" > "$LOG" 2>&1
echo "LANE_EXIT=$?"

echo "=== model identity evidence (startup header) ==="
grep -m5 -E 'model:|provider:|reasoning effort:|session id:' "$LOG" | tr -d '\r'
echo "=== receipt ==="
if [ -f "$CLONE/.ao-r3/AO_VERDICT.json" ]; then head -c 4000 "$CLONE/.ao-r3/AO_VERDICT.json"; else echo "NO_RECEIPT"; fi
echo ""
echo "=== report headings ==="
if [ -f "$CLONE/.ao-r3/EXTERNAL_CHALLENGE_REPORT.md" ]; then grep -n '^#' "$CLONE/.ao-r3/EXTERNAL_CHALLENGE_REPORT.md" | head -20; else echo "NO_REPORT"; fi
echo "=== log tail ==="
tail -25 "$LOG" | tr -d '\r'
echo LANE_DONE
