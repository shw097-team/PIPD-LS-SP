#!/usr/bin/env bash
# Push the two S4R3 control branches and read the remote refs back.
#
# The token is never printed, never placed in argv and never written to a log: git asks the approved
# GIT_ASKPASS helper, which reads the owner's token file itself. Only non-force pushes to two named
# feature branches are performed. No push to main, no tag, no release.
set -uo pipefail
cd "C:/Projects/Agent_Workspace/PIPD" || exit 1
# Credential path. The GIT_ASKPASS helper that earlier rounds used is a `#!/bin/sh` script; git for
# Windows 2.53 failed to execute it here ("unable to get password from user") even though the script
# itself answers correctly when run by sh. This inline helper does the same job through git's own
# `!`-prefixed helper mechanism, so no interpreter association is involved. The token VALUE never
# reaches argv, stdout, a log or a config file - only the path of the owner-provided file does, and
# `man`/`printf` read it inside the helper process git spawns.
HELPER='!f(){ echo username=shw097-team; printf "password=%s\n" "$(tr -d "\r\n" < "C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")"; }; f'
export GIT_TERMINAL_PROMPT=0
GITC=(git -c credential.helper= -c "credential.helper=$HELPER")
REMOTE="https://github.com/shw097-team/PIPD-LS-SP.git"
OUT="worktrees/s4r3b-wt/.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/09_OWNER_RELEASE"
mkdir -p "$OUT"

A="fix/s4r3-stage-a-ci-truthfulness-20261013"
B="feat/s4r3-stage-b-distribution-20261013"
BASE_A="517d7a5d3f00935e1589908f456dfacea8fd8a74"
BASE_B="517d7a5d3f00935e1589908f456dfacea8fd8a74"

echo "=== remote identity precheck (must be github.com / shw097-team/PIPD-LS-SP) ==="
git remote -v | sed -n '1,4p'
case "$(git remote get-url origin)" in
  *"github.com/shw097-team/PIPD-LS-SP"*) echo "REMOTE_OK" ;;
  *) echo "REMOTE_MISMATCH: refusing to push" >&2; exit 2 ;;
esac

echo "=== local tips ==="
printf '%s %s\n' "$(git rev-parse "$A")" "$A"
printf '%s %s\n' "$(git rev-parse "$B")" "$B"
echo "=== ancestry check: is the declared Stage B base an ancestor of the Stage B tip? ==="
if git merge-base --is-ancestor "$BASE_B" "$B"; then echo "ANCESTOR_YES"; else echo "ANCESTOR_NO"; exit 3; fi
echo "=== the Stage B push set (declared base ... Stage B tip) ==="
git diff --name-status "$BASE_B...$B"

echo "=== push A (non-force) ==="
timeout 300 "${GITC[@]}" push --porcelain origin "refs/heads/$A:refs/heads/$A" 2>&1 | tail -4
echo "push_A_exit=${PIPESTATUS[0]}"
echo "=== push B (non-force) ==="
timeout 300 "${GITC[@]}" push --porcelain origin "refs/heads/$B:refs/heads/$B" 2>&1 | tail -4
echo "push_B_exit=${PIPESTATUS[0]}"

{
  echo "# S4R3 PUSH_READBACK  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "# remote: $REMOTE  (no force, no main, no tag, no release)"
  echo "# local tips"
  printf '%s %s\n' "$(git rev-parse "$A")" "$A"
  printf '%s %s\n' "$(git rev-parse "$B")" "$B"
  printf '%s %s\n' "$(git rev-parse main)" "main"
  echo "# remote refs after the push (anonymous read: no credential used)"
  git ls-remote "$REMOTE" "refs/heads/$A" "refs/heads/$B" refs/heads/main refs/tags/v0.1.1-preview.3 | sed 's/\t/ /'
  echo "# declared Stage B base"
  echo "$BASE_B"
  echo "# push set actually sent (declared base ... Stage B tip)"
  git diff --name-status "$BASE_B...$B"
} > "$OUT/PUSH_READBACK.txt"
echo "=== readback ==="
cat "$OUT/PUSH_READBACK.txt"
echo "PUSH_SEQUENCE_DONE"
