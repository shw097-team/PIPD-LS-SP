#!/usr/bin/env bash
# Push the Stage-B candidate to a NEW dedicated branch, because the local branch was rebased onto the
# Stage-A tip and therefore no longer fast-forwards the branch pushed earlier (38f9067d...).
# A force push is forbidden by the round's rules, so the rebased candidate goes to a fresh name.
set -u
cd /c/Projects/Agent_Workspace/PIPD || exit 1
export GIT_ASKPASS="C:/Projects/Agent_Workspace/.git-askpass-shw097-team.sh"
export GIT_TERMINAL_PROMPT=0
OUT=/c/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/09_RELEASE

NEW=feat/s4post-triple-upgrade-20261012-r2
LOCAL=feat/s4post-triple-upgrade-20261012

echo "=== ancestry: is the previously pushed tip an ancestor of the rebased candidate? ==="
if git merge-base --is-ancestor 38f9067d47162c9ecaaa34bb699fbecefb969301 "$LOCAL"; then
  echo "ANCESTOR_YES (fast-forward would be possible)"
else
  echo "ANCESTOR_NO -> fast-forward impossible; a force push would be required and is FORBIDDEN"
fi

echo "=== push rebased candidate to $NEW (no force, no main, no tag) ==="
timeout 300 git -c credential.helper= push --porcelain origin "refs/heads/$LOCAL:refs/heads/$NEW" 2>&1 | tail -8
echo "exit=${PIPESTATUS[0]}"

echo "=== readback ==="
{
  echo "# PUSH_READBACK  round S4POST-20261012"
  echo "# local tips"
  printf '%s %s\n' "$(git rev-parse "$LOCAL")" "$LOCAL"
  printf '%s %s\n' "$(git rev-parse fix/s4post-integration-repair-20261012)" "fix/s4post-integration-repair-20261012"
  printf '%s %s\n' "$(git rev-parse main)" "main"
  echo "# remote refs after push (anonymous read)"
  git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git \
    refs/heads/main refs/heads/fix/s4post-integration-repair-20261012 "refs/heads/$NEW" \
    refs/tags/v0.1.1-preview.3 | sed 's/\t/ /'
} > "$OUT/PUSH_READBACK.txt"
cat "$OUT/PUSH_READBACK.txt"
echo "PUSH_SEQUENCE_DONE"
