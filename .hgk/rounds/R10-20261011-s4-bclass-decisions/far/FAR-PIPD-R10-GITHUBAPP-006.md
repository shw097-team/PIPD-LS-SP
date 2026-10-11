# FAR-PIPD-R10-GITHUBAPP-006 - the four owner steps, EXECUTED

Supersedes the "zero of four steps done" outcome of `FAR-PIPD-R10-GITHUBAPP-005`. All four steps were
completed by driving the browser, each verified by readback from GitHub, and the result was proved
**end to end** by authenticating a real remote git read with a minted App token.

## What was actually created (readback, not narration)

| item | value |
|---|---|
| App name | `HGK-SWOF-ACCEPTANCE-BRIDGE-ORG` |
| **Owned by** | **`@shw097-team`** (the ORGANISATION, not a personal account) |
| **App ID** | **5270497** |
| Client ID | `Iv23liPX0f2yLOOrUrox` |
| Private key | `C:/Users/user/.hgk-creds/hgk-app.private-key.pem`, 1679 B, `openssl rsa -check` -> `RSA key ok`, outside every repo |
| Key fingerprint (public) | `SHA256:/UfJUXyysVMNWq4tCq53IPYUeMw2wdcIcShu6zxlgSo=` |
| **Installation ID** | **170160551**, installed on `@shw097-team` |
| Scope | `install_target=selected`, `repository_ids[]=[1410587331]` -> exactly ONE repository |
| Webhook | **NOT active** (the default is active; it was switched off before creation) |
| Permissions | `Read access to metadata` + `Read and write access to code`; 1 repository permission selected |

## The decisive design fact: the App MUST be owned by the organisation

My operator guide told the owner to register the App under their **personal** settings. Executing it
proved that wrong for this target:

`shw097-team` has a **third-party application access policy set to "Access restricted"**:

> "Only approved applications can access data in this organization. **Applications owned by shw097-team
> always have access.**"

A personal-account App is therefore *never* granted the org's repos. Evidence, in order:

1. A personal App (`hgk-swof-acceptance-bridge-app`, ID 5270409) was created first and its install flow
   offered **only** `Install on your personal account shw097` - the org never appeared.
2. The org-targeted install URL (`.../installations/new/permissions?target_id=261346351&target_type=Organization`)
   returned **Page not found**.
3. The org's own page (`/organizations/shw097-team/settings/apps`) offered **New GitHub App**, and the
   policy text above states the rule.

The fix was to create the App **owned by the organisation**; its install flow then offered
`Install on your organization shw097 team`, and the installation went through on the first try.
**The personal App (5270409) is now redundant and should be deleted along with its key pair.**

## The defect that only appeared once the App existed

Running the broker's App branch for the first time raised:

```
UnboundLocalError: cannot access local variable 'urllib' where it is not associated with a value
  cred_broker.py:79  in mint_app_installation_token()
```

Cause: `mint_app_installation_token()` contained `import urllib.error` **inside its body**, which makes
`urllib` a *local* name for the whole function - so `urllib.request.Request(...)` earlier in the same
function referenced an unbound local. Fixed by moving the import to module scope; the manifest pin was
recomputed (7/7 resolve) and `verify_offline.py` still reports `PASS_OFFLINE_T5_UNPROVEN`.

**Why this matters beyond one line.** Every prior round reported the App source as "implemented" on the
strength of `PASS_OFFLINE_T5_UNPROVEN` and a `selftest.py` whose T5 needs the network and was never
actually run with a real App. The branch was **declared, never executed** - and a declared-but-unexecuted
path is exactly the class of claim this whole exercise exists to catch. It took a real App, a real key
and a real mint to expose a one-line scoping bug in code that had passed offline verification four times.

## End-to-end proof (the point of the whole exercise)

```
cred_broker.py dry-run   -> credential_kind: "app", credential_length: 390,
                            header_would_be_supplied: true, secret_printed: false
cred_broker.py run -- ls-remote https://github.com/shw097-team/PIPD-LS-SP.git main
                         -> stdout "c8d97ec...\trefs/heads/main", stderr "", secret_leaked: false
```

The second command is the proof: a **1-hour installation token minted locally from the org-owned App's
private key authenticated a real read against the target repository**. From here the unattended lane needs
no long-lived credential and **no human renewal** - the whole point of the rotation design.

## Consequential follow-ups (not done in this pass, stated so they are not silently dropped)

1. **Delete the redundant personal App 5270409** (it still has a key pair on GitHub). Its downloaded
   `.pem` was already removed from `Downloads`.
2. **The PAT can now be retired.** The broker prefers the App source, so the PAT
   (`HGK-SWOF-ACCEPTANCE-BRIDGE`) is no longer used. Revoking it is an owner action and closes the R9
   `FAR-PIPD-R9-CREDROT-005` bridge.
3. **Activation is still a separate control-plane round.** The broker works, but nothing in `config/`
   references it (`NON_ACTIVATED_OK`); wiring it into the write lane needs its own admission.
4. The **operator guide has been corrected** on the points execution disproved (org-owned App; the
   install flow; the observed App/installation IDs; the new troubleshooting rows).

## Honest limits

- The four steps were performed **through a browser session that required the owner's password and a 2FA
  code**, both entered by the owner through masked UI prompts. The agent never saw either value. GitHub
  still exposes **no API** for app creation, key generation or installation consent.
- The end-to-end proof is a **read** (`ls-remote`). **No push was performed through the broker** in this
  pass, so "the broker writes correctly" is proven for authentication and read, not for a write.
- The session was logged out mid-flow once and re-authenticated; the timings therefore include two full
  sign-ins.

**Claim ceiling:**
`FOUR_OWNER_STEPS_EXECUTED_AND_READBACK_VERIFIED__ORG_OWNED_APP_REQUIRED_BY_POLICY__DECLARED_BUT_NEVER_EXECUTED_URLLIB_BUG_FOUND_AND_FIXED__APP_TOKEN_AUTHENTICATED_A_REAL_REMOTE_READ`.
