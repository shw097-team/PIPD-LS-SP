#!/usr/bin/env bash
# VERIFY round 2 — independent re-verification of candidate 0bc7bb4b (checker = GPT 6.1 SOL-MEDIUM, OpenAI OAuth).
set -u
CAND="C:/Projects/Agent_Workspace/PIPD-postrelease-candidate"
WT="C:/Projects/Agent_Workspace/PIPD-postrelease-wt"
ROUND="$WT/.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair"
VDIR="$ROUND/verify"
mkdir -p "$VDIR" "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/verify2"

git -C "$CAND" status --porcelain > "$VDIR/MUTATION2_BEFORE.txt" 2>&1
git -C "$CAND" rev-parse HEAD              > "$VDIR/SUBJECT2_COMMIT.txt" 2>&1
git -C "$CAND" rev-parse 'HEAD^{tree}'     > "$VDIR/SUBJECT2_TREE.txt" 2>&1

unset OPENAI_BASE_URL OPENAI_API_KEY
export CODEX_HOME="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/checker-sol"
export PYTHONDONTWRITEBYTECODE=1

LOG="$VDIR/VERIFY2_gpt61sol.exec-$(date -u +%Y%m%dT%H%M%SZ).log"
timeout 3300 "C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe" exec \
  --cd "$CAND" --skip-git-repo-check -s danger-full-access - \
  < "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/VERIFY2_BRIEF.md" \
  > "$LOG" 2>&1
echo "VERIFY2_LANE_EXIT=$?" | tee "$VDIR/VERIFY2_LANE_EXIT.txt"

git -C "$CAND" status --porcelain > "$VDIR/MUTATION2_AFTER.txt" 2>&1
{
  echo "=== NON-MUTATION GUARD run 2 (candidate 0bc7bb4b, tree e95e33f008a617faef8881431b27a468f516d409) ==="
  echo "actual tree: $(git -C "$CAND" rev-parse 'HEAD^{tree}')"
  echo "--- status before ---"; cat "$VDIR/MUTATION2_BEFORE.txt"
  echo "--- status after ---";  cat "$VDIR/MUTATION2_AFTER.txt"
  echo "--- delta (files the checker ADDED to the dirty set) ---"
  comm -13 <(sort "$VDIR/MUTATION2_BEFORE.txt") <(sort "$VDIR/MUTATION2_AFTER.txt") || true
} > "$VDIR/NONMUTATION2_GUARD.txt" 2>&1
cat "$VDIR/NONMUTATION2_GUARD.txt"
echo VERIFY2_LANE_DONE
