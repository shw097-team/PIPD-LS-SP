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
validity, and a configured-but-unprobed App is **refused on the default path**, not passed. The PAT bridge
is still reported, but a dead PAT no longer gates a healthy App.

**Correction issued during independent verification (R11, checker `openai-codex/gpt-6.1-sol`).** An
earlier draft of this FAR, and the verification brief built from it, asserted flatly that "a
configured-but-unprobed App is REFUSED". **That assertion is false as written**, and the checker
disproved it by executing the committed source rather than reading it:

```
--no-probe  (an EXPLICIT operator flag, help: "skip the network validity probe")
  effective_source=app, app_cred_valid=SKIP, required=["app_cred_valid"],
  failed_required=[], verdict=OK, abort=false
```

So the exact behaviour is: **the default path refuses** (no getter -> `app_cred_valid: FAIL` ->
`FAIL_CLOSED`), and the **explicit `--no-probe` opt-out** converts the check to `SKIP`, which
`_verdict()` does not count as a FAIL, so the run reports `OK` over a credential that was configured and
**never proven**. That is the same "presence is not validity" class the fix was aimed at, surviving
through a flag, and the code's own comment on the getter-less path says it "refuses to pass on presence
alone" - which is not true of this branch.

**The bypass is bigger than one flag.** The same checker then found a SECOND opt-out, and re-measuring confirms it independently:

| mode | effective source | what is required | verdict | provenance |
|---|---|---|---|---|
| default, getter available | `app` | the App, probed by its own installation token | `OK` only if probed | `PROBED` |
| default, no getter | `app` | `app_cred_valid` | **`FAIL_CLOSED`** | `PROBED` |
| `--no-probe` | `app` | `app_cred_valid: SKIP` -> nothing can FAIL | `OK` over an unproven App | `UNPROVEN_BY_REQUEST` |
| `--metadata-only` | `pat`, and App selection is never reached | `cred_syntax`/`cred_api_valid` both `SKIP` -> existence only | `OK` over a byte length | `UNPROVEN_BY_REQUEST` |

So the gate can be asked, by two explicit flags, to report `OK` while having proven nothing. That is the
presence-is-not-validity class this gate exists to stop, surviving through opt-outs.

Disposition - three parts, each with its reason:

1. **The claim was corrected** (it was mine, and wrong).
2. **An additive field was added** so the two `OK`s can no longer be confused. `_verdict()` now carries
   `"provenance": "PROBED"` or `"UNPROVEN_BY_REQUEST"`. This is deliberately **additive only**: no existing
   key changes value, so `verdict`, `abort`, `failed_required` and the exit-code contract that
   `INSTALL_MANIFEST.json` V3/V4 and external readers encode are untouched. A reader that wants proof now
   has a field to read; a reader that ignores it is no worse off than before. Measured in all four modes
   above; manifest re-pinned 7/7; `selftest` 7/7 PASS; `verify_offline` `PASS_OFFLINE_T5_UNPROVEN`.
3. **The two flags themselves were NOT removed**, and the reason is stated rather than assumed:
   `--no-probe` and `--metadata-only` are explicit, self-describing opt-outs that an offline operator may
   legitimately need, and deleting them would break the documented exit-code contract. They are now
   **labelled** rather than silent. The residual that remains open is only this: a consumer that reads
   `verdict` and ignores `provenance` will still see a bare `OK` on an unproven run.

The docstring of `run_preflight()` was also found to contradict its own code - it said that an absent App
getter leaves "the gate on the PAT", while the code keeps `effective_source=app` and `FAIL_CLOSED`. The
sentence is corrected, and the correction says so.

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
- It does not claim the gate is unconditionally sound: `--no-probe` and `--metadata-only` both yield `OK`
  without proving a credential. They are now labelled by `provenance` rather than silent, but a consumer
  that reads `verdict` and ignores `provenance` still sees a bare `OK` - that is the OPEN residual.
- It does not claim the write's **attribution**. The independent checker established, correctly, that a
  credential-free `ls-remote` of a PUBLIC repository proves only the advertised refs - it cannot show who
  pushed, which credential authenticated, whether the ref moved during this round, or that write
  permission existed. The ref move (`1136a69..ae08136`) is evidence that **something with write access**
  moved the ref while the helper was blanked and the broker supplied the App token; the step from that to
  "the App token did it" is corroboration, not proof, and is labelled as such here.
- It does not claim the suites were independently re-run. The checker refused to execute `selftest.py` and
  `verify_offline.py` because both write temporary files and the brief ordered VERIFY_ONLY - it reported
  `UNCERTAIN` rather than adopting this FAR's numbers. The 7/7 and `PASS_OFFLINE_T5_UNPROVEN` figures below
  remain **maker-reported**; what the checker DID re-derive independently is the manifest pin set (7/7
  resolve, both from the working tree and from the blobs in the commit).

**Claim ceiling:**
`CREDENTIAL_GATE_REQUIRED_THE_WRONG_SOURCE__SOURCE_SELECTION_CORRECTED_AND_REPROVEN_ON_THE_DEFAULT_PATH__APP_TOKEN_WRITE_SHOWN_BY_A_REF_MOVE_WITH_WRITER_ATTRIBUTION_CORROBORATED_NOT_PROVEN__no-probe_OPT_OUT_LEFT_OPEN__SUITE_RESULTS_MAKER_REPORTED__HOST_MANAGER_CREDENTIAL_IDENTIFIED_AND_LEFT_IN_PLACE`.

