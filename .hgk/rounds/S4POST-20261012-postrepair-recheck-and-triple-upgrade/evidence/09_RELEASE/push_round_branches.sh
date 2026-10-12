#!/usr/bin/env bash
# Push the round's two dedicated branches. Never main, never a tag, never force.
# The token is read by the GIT_ASKPASS helper from the owner-provided file; it is never echoed,
# never placed in argv, and never written to a log. Credential Manager is disabled for these pushes
# so the only credential path is the askpass helper.
set -u
cd /c/Projects/Agent_Workspace/PIPD || exit 1
export GIT_ASKPASS="C:/Projects/Agent_Workspace/.git-askpass-shw097-team.sh"
export GIT_TERMINAL_PROMPT=0
OUT=/c/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/09_RELEASE
mkdir -p "$OUT"

for b in fix/s4post-integration-repair-20261012 feat/s4post-triple-upgrade-20261012; do
  echo "=== push $b ==="
  timeout 300 git -c credential.helper= push --porcelain origin "refs/heads/$b:refs/heads/$b" 2>&1 | tail -8
  echo "exit=${PIPESTATUS[0]}"
done

echo "=== readback: ls-remote ==="
git ls-remote origin refs/heads/main refs/heads/fix/s4post-integration-repair-20261012 \
  refs/heads/feat/s4post-triple-upgrade-20261012 refs/tags/v0.1.1-preview.3 | sed 's/\t/ /' > "$OUT/PUSH_READBACK.txt"
cat "$OUT/PUSH_READBACK.txt"
echo "=== local tips ==="
for b in fix/s4post-integration-repair-20261012 feat/s4post-triple-upgrade-20261012 main; do
  printf '%s %s\n' "$(git rev-parse "$b")" "$b" >> "$OUT/PUSH_READBACK.txt"
done
tail -4 "$OUT/PUSH_READBACK.txt"
echo "PUSH_SEQUENCE_DONE"
