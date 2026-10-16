#!/usr/bin/env bash
# Durable PAT credential mechanism for this repo (TT-R5R3-01 remediation).
#
# Why this exists: the per-invocation workaround was remembering three -c flags by hand, and the naive
# variants fail on this host (GIT_ASKPASS is ignored because the credential manager sets
# credential.interactive=false). This wrapper encodes the working shape ONCE.
#
# The token itself is read from the owner's key file at the moment of use and is never placed in argv,
# in the environment, in git config, or in any log produced by this script. Only the file PATH appears.
#
# Usage:  bash push_with_pat.sh push origin <branch>          # real push
#         bash push_with_pat.sh push --dry-run origin <ref>   # credential proof, updates no ref
set -euo pipefail

TOKEN_FILE="${PIPD_PAT_FILE:-C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt}"

if [ ! -r "$TOKEN_FILE" ]; then
  echo "ERR_PAT_FILE_UNREADABLE: $TOKEN_FILE" >&2
  exit 2
fi

exec git \
  -c credential.helper= \
  -c credential.interactive=always \
  -c "credential.helper=!f(){ echo username=x-access-token; printf 'password=%s\n' \"\$(tr -d '\r\n' < '$TOKEN_FILE')\"; }; f" \
  "$@"
