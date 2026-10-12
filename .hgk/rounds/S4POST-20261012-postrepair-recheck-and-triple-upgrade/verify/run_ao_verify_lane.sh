#!/usr/bin/env bash
# S4POST stage-A independent acceptance lane.
# Fresh clone of the product repo at the frozen subject; the checker works read-only inside it.
set -u
SUBJECT=f3c80ec5f97fd6163192491efaae184a773b421c
REPO=C:/Projects/Agent_Workspace/PIPD
CLONE=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-a-verify-decl
ROUND=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-a-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
LOG="$ROUND/verify/AO_VERIFY_SUBJECT_F3C80EC_gpt-6.1-sol_medium.log"

rm -rf "$CLONE"
git clone --quiet "$REPO" "$CLONE"
if [ ! -d "$CLONE/.git" ]; then echo "CLONE_EXIT=1"; exit 1; fi
git -C "$CLONE" checkout --quiet "$SUBJECT" || { echo "CHECKOUT_EXIT=1"; exit 1; }

echo "CLONE_EXIT=0"
echo "EXPECT_COMMIT=$SUBJECT"
echo "ACTUAL_COMMIT=$(git -C "$CLONE" rev-parse HEAD)"
echo "ACTUAL_TREE=$(git -C "$CLONE" rev-parse 'HEAD^{tree}')"
git -C "$CLONE" status --porcelain > "$ROUND/verify/pre_status.txt" || true
echo "PRE_STATUS_LINES=$(wc -l < "$ROUND/verify/pre_status.txt")"

cd "$CLONE" || exit 1
"$CB" -c model='gpt-6.1-sol' \
      -c model_reasoning_effort='medium' \
      -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
      exec --skip-git-repo-check -s danger-full-access - \
      < "$ROUND/verify/AO_VERIFY_BRIEF_v3.md" > "$LOG" 2>&1
echo "VERIFY_LANE_EXIT=$?"

git -C "$CLONE" status --porcelain | grep -v '^?? .ao/' > "$ROUND/verify/post_status.txt" || true
echo "POST_STATUS_LINES=$(wc -l < "$ROUND/verify/post_status.txt")"
if [ -s "$ROUND/verify/pre_status.txt" ] || [ -s "$ROUND/verify/post_status.txt" ]; then
  echo "NON_MUTATION_VERDICT=REVIEW_TRACKED_CHANGES"
else
  echo "NON_MUTATION_VERDICT=PASS"
fi
echo "=== receipt ==="
head -c 3000 "$CLONE/.ao/AO_VERDICT.json" 2>/dev/null || echo "NO_RECEIPT"
echo ""
echo "=== log tail ==="
tail -12 "$LOG"
