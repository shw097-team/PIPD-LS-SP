#!/bin/sh
# Controlled, non-force push of this round's two branches, then a remote readback.
#
# Credential handling. `GIT_ASKPASS` pointing at a .sh helper is known NOT to work with this host's
# git 2.53.0.windows.1 (the previous round hit the same "fatal: unable to get password from user" and
# worked around it by putting the token in the URL). This script avoids both problems: the token is
# read from the owner's file AT RUNTIME by an inline credential helper, so it never enters argv, never
# enters a remote URL, never enters this file and never enters a log. The helper is the only thing that
# touches the file; it answers git's `get` operation and stays silent for store/erase.
#
# `-c credential.helper=` first clears any inherited helper list (this host has a system-level
# `credential.helper manager`), so the system Git Credential Manager cannot take over and open an
# interactive account chooser. GIT_TERMINAL_PROMPT=0 and GCM_INTERACTIVE=never make any such attempt
# fail closed instead of hanging the run.
set -eu

REPO="C:/Projects/Agent_Workspace/PIPD"
TOKEN_FILE="C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt"
BRANCH_A="fix/s4r3-stage-a-ci-truthfulness-20261013"
BRANCH_B="feat/s4r3-stageb-successor-20261013"
REMOTE="origin"

HELPER='!f() { if [ "$1" = get ]; then echo username=shw097-team; printf "password="; tr -d "\r\n" < "'"$TOKEN_FILE"'"; echo; fi; }; f'

push_one() {
  branch="$1"
  wt="$2"
  mode="$3"
  echo "=== pushing ${branch} (from ${wt}, mode=${mode}) ==="
  local_sha="$(git -C "$wt" rev-parse HEAD)"
  case "$mode" in
    ff-only)
      # Stage A only ever gains commits on top of the tip the world already has, so it never needs a
      # rewrite. --force-with-lease is deliberately NOT used here: if this push would not fast-forward,
      # something has happened to the remote that the operator needs to see.
      GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never \
        git -C "$wt" -c credential.helper= -c credential.helper="$HELPER" \
        push "$REMOTE" "HEAD:refs/heads/${branch}"
      ;;
    rewrite-disclosed)
      # Stage B is a DRAFT branch created in this same round. It was already published once as
      # 2363bf6, then rewritten onto the current Stage A tip so that the stack is linear and contains
      # the gates that validate it. The rewrite is disclosed in the pull request body and in the round
      # evidence. --force-with-lease (never a bare --force) so a concurrent remote change aborts the
      # push instead of being silently discarded.
      GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never \
        git -C "$wt" -c credential.helper= -c credential.helper="$HELPER" \
        push --force-with-lease="refs/heads/${branch}" "$REMOTE" "HEAD:refs/heads/${branch}"
      ;;
    *)
      echo "PUSH_MODE_UNDECLARED: ${mode} is not ff-only or rewrite-disclosed" >&2
      return 1
      ;;
  esac
  remote_sha="$(git -C "$wt" ls-remote "$REMOTE" "refs/heads/${branch}" | cut -f1)"
  echo "local  ${local_sha}"
  echo "remote ${remote_sha}"
  if [ "$local_sha" != "$remote_sha" ]; then
    echo "READBACK_MISMATCH: ${branch} local != remote" >&2
    return 1
  fi
  echo "READBACK_OK ${branch}"
}

push_one "$BRANCH_A" "${REPO}/worktrees/s4r3a-wt" ff-only
push_one "$BRANCH_B" "${REPO}/worktrees/s4r3c-wt" rewrite-disclosed

echo "=== frozen refs must be untouched ==="
git -C "$REPO" ls-remote "$REMOTE" refs/heads/main refs/tags/v0.1.1-preview.3
