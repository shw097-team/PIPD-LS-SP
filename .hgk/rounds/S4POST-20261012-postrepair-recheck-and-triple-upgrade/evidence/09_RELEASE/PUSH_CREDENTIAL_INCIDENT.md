# Push-credential incident: an interactive account chooser appeared although a token was supplied

## Symptom

A push of the Stage-B branch stopped on a Git Credential Manager window asking which GitHub account
to use, even though the push was run with the owner-supplied fine-grained token exposed through a
`GIT_ASKPASS` helper. A push that needs no account choice is the whole point of supplying the token.

## Cause

Git asks the **configured credential helpers first**; `GIT_ASKPASS` is only the fallback used when no
helper can answer. This host has a system-wide setting:

```
file:C:/Program Files/Git/etc/gitconfig   credential.helper = manager
```

`manager` is Git Credential Manager. Because the environment already carried a working credential,
the earlier pushes in this round were answered from GCM's cache and looked fine. When that cache no
longer covered the request, GCM went interactive and opened its account chooser — and the token
helper was never consulted at all. Nothing was wrong with the token or its scope.

## Fix, applied and verified

Run the push with the inherited helper list cleared, so the token helper is the only thing that can
answer, and make GCM non-interactive as a second line:

```sh
GIT_ASKPASS=<owner token helper> \
GIT_TERMINAL_PROMPT=0 \
GCM_INTERACTIVE=never \
git -c credential.helper= push origin HEAD:refs/heads/<round branch>
```

`-c credential.helper=` (empty value) resets the helper list for that one invocation; it does not edit
any config. The push then completed with no window:

| Check | Value |
|---|---|
| remote `refs/heads/feat/s4post-triple-upgrade-20261012-r2` | `07681745a436a7d82e85a0aa494d816acad92a0` |
| local `HEAD` | `07681745a436a7d82e85a0aa494d816acad92a0` |
| `main` | untouched (`224591431a164ab72a9423cd180e417e8a762403`) |
| any tag | untouched |
| force | not used |

The token value itself never reached the command line, the logs, the remote URL or this file.

## Standing rule for the rest of the round

Every push sets the four variables above, and every push passes `-c credential.helper=`.

Correction, recorded because the first draft of this note got it wrong: the round's own scripts —
`evidence/09_RELEASE/push_round_branches.sh` and `push_stage_b_new_branch.sh` — **already** carried
`git -c credential.helper= push`. That is why the two branch pushes they performed completed silently.
The window appeared on an **ad-hoc** push issued by hand from the shell, which omitted that flag and
therefore fell through to the system helper. The scripts are correct as written; the ad-hoc
invocation was the defect, and it will not be repeated. An interactive prompt on an unattended push
is a governance problem, not a convenience one: it blocks a lane that must run without a human.
