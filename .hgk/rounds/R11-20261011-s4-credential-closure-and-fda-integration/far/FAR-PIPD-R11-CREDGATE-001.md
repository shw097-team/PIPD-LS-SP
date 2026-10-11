# FAR-PIPD-R11-CREDGATE-001 — the credential gate required the wrong source

Found by executing, not by reading, in the R11 round. Three findings, one fix, and two corrections to
claims made in the previous round.

## Finding 1 — the file's token is DEAD, and it is not on this account at all

`GET https://api.github.com/user` with the token held in
`C:/Projects/Agent_Workspace/API KEY/Fine-grained personal access tokens.txt` returns **HTTP 401**.

The account's token surfaces contain no such token:
- fine-grained (`/settings/personal-access-tokens`): two entries, both expired;
- classic (`/settings/tokens`): two entries, both expired / never used.

So the artefact the previous round treated as "the credential" is a non-functional string. **The previous
round's claim that pushes were performed "with the PAT" is therefore wrong.** It is corrected here rather
than left standing.

## Finding 2 — what actually authenticates a push on this host is the credential MANAGER

`git config --show-origin --get-all credential.helper` ->
`file:C:/Program Files/Git/etc/gitconfig  manager`, and `git-credential-manager.exe` is present.

Decisive test — with the helper explicitly blanked, three runs of the same push:

| # | credential supplied | result |
|---|---|---|
| 1 | none, helper blanked | **fail**: `could not read Username for 'https://github.com'` (exit 128) |
| 2 | none, helper available | **succeed**: `Everything up-to-date` (exit 0) |
| 3 | broker-supplied App token, helper blanked | **exit 0** (see Finding 3) |

Run 2 is the proof: a push completes with **no token supplied by us**, so the manager's stored
credential is the authenticator in the ordinary path. This has a security consequence worth naming: the
host holds a live write credential for the repository that is independent of both the dead file and the
App, and nothing in this round revokes it.

## Finding 3 — the gate required the FALLBACK, so a dead PAT disabled a healthy App

`cred_preflight.py` had `REQUIRED = ("cred_source_present", "cred_syntax", "cred_api_valid")`, and its
only validity probe was `GET /user` **with the PAT**. The App source was checked for **presence only**
(`app_config_present`), never for validity.

Measured consequence: with a fully configured, working App, the broker reported

```
"cred_api_valid": "FAIL", "detail": "GET /user -> 401"   ->   "verdict": "FAIL_CLOSED", "abort": true
```

and **could not run at all**. The gate also contradicted its own line 32 ("the broker uses the first that
works"): `acquire()` prefers the App and does **not** fall back to the PAT, so the preflight was requiring
a source that the very next function would never consult.

This is the same defect class as the previous round's `urllib` bug, one layer up: a control that had never
been exercised against the configuration it was supposed to govern.

## The fix

The gate resolves the effective source exactly as `acquire()` does and requires **that** source's validity.
The App is probed by minting its installation token and calling the repository endpoint - presence is not
validity, and a configured-but-unprobed App is **refused**, not passed. The PAT bridge is still reported,
but a dead PAT no longer gates a healthy App.

Test fixtures were **realigned, not weakened**. The `absent file => abort` expectations in `selftest.py`
and `verify_offline.py` encoded the superseded PAT-only contract, and they were also **non-hermetic** -
they inherited `HGK_APP_*` from the ambient shell, so their result depended on the environment rather
than on the code. They are split into: T1a (no source at all -> FAIL_CLOSED), T1b (no PAT but App in force
-> not PAT-gated), T1c (configured but unprobed App -> refused), with the App configuration controlled
in-test.

Measured after the fix:

| suite | before | after |
|---|---|---|
| `selftest.py` | 4/5 FAIL | **7/7 PASS** |
| `verify_offline.py` | FAIL | **PASS_OFFLINE_T5_UNPROVEN** |
| manifest pin | n/a | **7/7 resolve** |
| standalone `cred_preflight.py` | FAIL_CLOSED on a dead PAT | **OK, effective_source = app** |

## The write claim, settled the hard way

The App probe reports `GET /repos/shw097-team/PIPD-LS-SP -> 200`, but the same response's
`permissions` block reports **`push: false`** (and `pull: false`), while a token with no push right
obviously cannot have written. **That field is not reliable for installation tokens, and this round does
not rely on it.** The write claim is settled by a push that actually MOVES a ref, with the credential
helper blanked so the manager of Finding 2 cannot supply anything:

```
cred_broker.py run -- push <url> main
  -> exit 0, stderr "1136a69..ae08136  main -> main", credential_kind "app", secret_leaked false
independent git ls-remote (NOT via the broker)
  -> remote main == ae08136 = local head; tags unmoved; working tree clean
```

A no-op push reports `Everything up-to-date` and proves nothing about write permission, because it
sends no authenticated update - the previous round's receipt contained both a real ref move and a no-op,
and only the former is evidence. This FAR relies solely on the ref move.

## What this FAR does NOT claim

- It does not claim the manager's stored credential was revoked or rotated; it was identified and left in
  place, and that residual is disclosed rather than quietly inherited.
- It does not claim the App is "activated"; it is a working capability that nothing calls (see
  `evidence/BROKER_ACTIVATION_ANALYSIS.md`).
- It does not claim the PAT was "retired by revoking it" - there is nothing on this account to revoke.

**Claim ceiling:**
`CREDENTIAL_GATE_REQUIRED_THE_WRONG_SOURCE__FIXED_AND_REPROVEN__APP_TOKEN_WRITE_CONFIRMED_BY_A_REF_MOVE__HOST_MANAGER_CREDENTIAL_IDENTIFIED_AND_LEFT_IN_PLACE`.
