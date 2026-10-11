#!/usr/bin/env bash
# VERIFY (S4-R2) — independent re-verification of candidate 7c00b649.
# Checker = GPT 6.1 SOL-MEDIUM via OpenAI OAuth (~/.codex auth.json), NOT the EXECUTE lane's relay.
set -u
CAND="C:/Projects/Agent_Workspace/PIPD-r2-candidate"
WT="C:/Projects/Agent_Workspace/PIPD-postrelease-wt"
ROUND="$WT/.hgk/rounds/S4R2-20261011-affected-only"
VDIR="$ROUND/verify"
SB="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4r2"
mkdir -p "$VDIR" "$SB"

git -C "$CAND" status --porcelain > "$VDIR/MUTATION_BEFORE.txt" 2>&1
git -C "$CAND" rev-parse HEAD          > "$VDIR/SUBJECT_COMMIT.txt" 2>&1
git -C "$CAND" rev-parse 'HEAD^{tree}' > "$VDIR/SUBJECT_TREE.txt" 2>&1

# The checker home must be an OpenAI-OAuth home. Build it from ~/.codex auth.json if absent.
CH="$SB/checker-sol"
if [ ! -f "$CH/auth.json" ]; then
  mkdir -p "$CH"
  cp "/c/Users/user/.codex/auth.json" "$CH/auth.json"
  cat > "$CH/config.toml" <<'EOF'
model = "gpt-6.1-sol"
model_provider = "openai"
model_reasoning_effort = "medium"
EOF
fi
unset OPENAI_BASE_URL OPENAI_API_KEY OPENCODE_GO_API_KEY
export CODEX_HOME="$CH"
export PYTHONDONTWRITEBYTECODE=1

LOG="$VDIR/VERIFY.exec-$(date -u +%Y%m%dT%H%M%SZ).log"
timeout 3300 "C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe" exec \
  --cd "$CAND" --skip-git-repo-check -s danger-full-access - \
  < "$VDIR/VERIFY_BRIEF.md" > "$LOG" 2>&1
echo "VERIFY_LANE_EXIT=$?" | tee "$VDIR/VERIFY_LANE_EXIT.txt"

git -C "$CAND" status --porcelain > "$VDIR/MUTATION_AFTER.txt" 2>&1
{
  echo "=== NON-MUTATION GUARD (candidate 7c00b64960d86fc1e94848c9955c512a3626a85f, tree b08b961061f510d1eb78a944307ecaa446d68eed) ==="
  echo "actual tree: $(git -C "$CAND" rev-parse 'HEAD^{tree}')"
  echo "--- status before ---"; cat "$VDIR/MUTATION_BEFORE.txt"
  echo "--- status after ---";  cat "$VDIR/MUTATION_AFTER.txt"
  echo "--- delta (files the checker ADDED to the dirty set) ---"
  comm -13 <(sort "$VDIR/MUTATION_BEFORE.txt") <(sort "$VDIR/MUTATION_AFTER.txt") || true
} > "$VDIR/NONMUTATION_GUARD.txt" 2>&1
cat "$VDIR/NONMUTATION_GUARD.txt"
echo VERIFY_LANE_DONE
