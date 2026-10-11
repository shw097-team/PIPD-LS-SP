#!/usr/bin/env bash
# VERIFY / SECURITY lane — Independent Acceptance Officer via Codex CLI.
# Owner steer 2026-10-11: checker model = GPT 6.1 SOL-MEDIUM (OpenAI OAuth).
# Non-mutation guard: the frozen checkout's tracked tree must be byte-identical before and after.
set -u

CAND="C:/Projects/Agent_Workspace/PIPD-postrelease-candidate"
WT="C:/Projects/Agent_Workspace/PIPD-postrelease-wt"
ROUND="$WT/.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair"
VDIR="$ROUND/verify"
BRIEF="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/VERIFY_BRIEF.md"
CHECKER_HOME="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/checker-sol"
CODEX="C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe"
mkdir -p "$VDIR"

# --- guard: BEFORE ---
git -C "$CAND" status --porcelain > "$VDIR/MUTATION_BEFORE.txt" 2>&1
git -C "$CAND" rev-parse HEAD > "$VDIR/SUBJECT_COMMIT.txt" 2>&1
git -C "$CAND" rev-parse 'HEAD^{tree}' > "$VDIR/SUBJECT_TREE.txt" 2>&1
git -C "$CAND" status --porcelain > "$VDIR/NONMUTATION_STATUS_before.txt" 2>&1

# Checker runs on the OpenAI OAuth backend: no local relay, no API key in the environment.
unset OPENAI_BASE_URL OPENAI_API_KEY
export CODEX_HOME="$CHECKER_HOME"
export PYTHONDONTWRITEBYTECODE=1

LOG="$VDIR/VERIFY_gpt61sol.exec-$(date -u +%Y%m%dT%H%M%SZ).log"
timeout 3000 "$CODEX" exec --cd "$CAND" --skip-git-repo-check -s danger-full-access - < "$BRIEF" > "$LOG" 2>&1
echo "VERIFY_LANE_EXIT=$?" | tee "$VDIR/VERIFY_LANE_EXIT.txt"

# --- guard: AFTER ---
git -C "$CAND" status --porcelain > "$VDIR/NONMUTATION_STATUS_after.txt" 2>&1
{
  echo "=== NON-MUTATION GUARD (frozen checkout, commit dbe387195d25aca32829f84c051b7bf52b5931eb) ==="
  echo "expected tree: 7606c769e5d1302ebc99cbc2ce8f9a848dd18745"
  echo "actual tree  : $(git -C "$CAND" rev-parse 'HEAD^{tree}')"
  echo "--- status before ---"; cat "$VDIR/NONMUTATION_STATUS_before.txt"
  echo "--- status after ---";  cat "$VDIR/NONMUTATION_STATUS_after.txt"
  if [ ! -s "$VDIR/NONMUTATION_STATUS_after.txt" ] && [ "$(git -C "$CAND" rev-parse 'HEAD^{tree}')" = "7606c769e5d1302ebc99cbc2ce8f9a848dd18745" ]; then
    echo "NON_MUTATION_VERDICT=PASS"
  else
    echo "NON_MUTATION_VERDICT=FAIL"
  fi
} > "$VDIR/NONMUTATION_GUARD.txt" 2>&1
cat "$VDIR/NONMUTATION_GUARD.txt"
echo VERIFY_LANE_DONE
