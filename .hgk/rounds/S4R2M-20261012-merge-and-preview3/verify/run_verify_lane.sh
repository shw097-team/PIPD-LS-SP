#!/usr/bin/env bash
# S4R2M VERIFY lane — Independent Acceptance Officer.
# Checker = GPT 6.1 SOL (medium) via OpenAI OAuth (~/.codex/auth.json), NOT the EXECUTE lane's
# opencode-go relay. The relay env is unset so the checker cannot silently run as the maker's model.
set -u

SUBJ="C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt"
R="$SUBJ/.hgk/rounds/S4R2M-20261012-merge-and-preview3"
VDIR="$R/verify"
SB="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4r2m-verify"
mkdir -p "$VDIR" "$SB"

git -C "$SUBJ" status --porcelain            > "$VDIR/SUBJECT_STATUS_before.txt" 2>&1
git -C "$SUBJ" rev-parse HEAD                > "$VDIR/SUBJECT_COMMIT.txt" 2>&1
git -C "$SUBJ" rev-parse 'HEAD^{tree}'       > "$VDIR/SUBJECT_TREE.txt" 2>&1

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

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$VDIR/VERIFY.exec-$STAMP.log"
echo "== VERIFY lane start $STAMP ==" > "$LOG"
timeout 3300 "C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe" exec \
  --cd "$SUBJ" --skip-git-repo-check -s danger-full-access - \
  < "$VDIR/VERIFY_BRIEF.md" >> "$LOG" 2>&1
RC=$?
echo "VERIFY_LANE_EXIT=$RC" | tee "$VDIR/VERIFY_LANE_EXIT.txt" >> "$LOG"

git -C "$SUBJ" status --porcelain > "$VDIR/SUBJECT_STATUS_after.txt" 2>&1
{
  echo "=== NON-MUTATION GUARD (subject 58a1f334464675081d0573476d70e2165143bdd8, tree c9d96316ea7717ab8cb74f0858dd6f05d0ec7db4) ==="
  echo "actual HEAD: $(git -C "$SUBJ" rev-parse HEAD)"
  echo "actual tree: $(git -C "$SUBJ" rev-parse 'HEAD^{tree}')"
  echo "--- files the checker ADDED to the dirty set ---"
  comm -13 <(sort "$VDIR/SUBJECT_STATUS_before.txt") <(sort "$VDIR/SUBJECT_STATUS_after.txt") || true
} > "$VDIR/NONMUTATION_GUARD.txt" 2>&1
cat "$VDIR/NONMUTATION_GUARD.txt"
echo VERIFY_LANE_DONE
