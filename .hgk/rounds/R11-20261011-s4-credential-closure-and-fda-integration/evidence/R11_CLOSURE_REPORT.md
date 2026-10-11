# R11 closure report — credential closure and automation-evidence integration

Round `R11-20261011-s4-credential-closure-and-fda-integration`. Six obligations, admitted through the
typed SharedSpine / ProjectLifecycleController API, FROZEN, zero errors. **The maker does not sign this.**

## 1. What was actually executed

### 1.1 The two remaining owner operations (REQ-PIPD-R11-FDAEXEC-001)

| operation | outcome | readback |
|---|---|---|
| delete the redundant personal-account App (`5270409`) | **DONE** | the account's app list renders exactly `No GitHub Apps`; and on a second, independent surface the app's own page `github.com/apps/hgk-swof-acceptance-bridge-app` returns **Page not found** while `.../hgk-swof-acceptance-bridge-org` still renders - a positive and a negative control on the same surface |
| retire the long-lived PAT | **NO-OP, and that is the finding** | the file's token returns **HTTP 401** and appears in NO token list on `shw097`. There was nothing to revoke. The honest statement is "the bridge was already dead", not "we retired it" |

The risk of the deletion was that it might take the *working* credential with it, so it was verified after
the fact rather than assumed: the organisation-owned App still lists under the organisation, and the API
still reports `app_cred_valid PASS` with `GET /repos/shw097-team/PIPD-LS-SP -> 200`.

**One owner interaction was spent**: one login and one second-factor entry, used for the deletion above.

### 1.2 Evidence integration (REQ-PIPD-R11-FDAEVID-002)

Written into the automation capability team's own evidence folder, in the team's own contract form, plus a
sibling digest sidecar (the contract forbids a self-hash inside the markdown).

**The decisive design choice, and why it is the interesting part of this section.** The team's preflight
selects the **last sorting member** of the `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE` series for two of its five
checks. A new file in that series would have become the "latest" and **moved a sealed, externally accepted
three-way binding** (`be576bebe767`). So the artefact was deliberately given a **different family name**,
and the claim was settled by measurement: the preflight was run **before** the addition and **after** it -
`PREFLIGHT: PASS` both times, binding printed identically both times, and the latest sealed file verified
**byte-identical** across the commit by `git ls-tree` at the commit and at its parent.

Three alternatives were refused, each with its reason recorded in `far/FAR-PIPD-R11-FDAEVID-002.md` -
including "regenerate the manifest so the new file joins it", which would have rewritten the counters and
subject root of an externally accepted artefact to include material no external reviewer saw.

### 1.3 Activation (REQ-PIPD-R11-ACTIVATE-003)

**Not performed, by decision.** The broker's read and write paths are each *exercised* end to end - the
write by a push that actually moved a ref - with the writer **corroborated rather than proven** (it is
referred to elsewhere in this report, and deliberately not upgraded here). It is referenced
**zero times** by the control plane's `config/` - but there is no in-repo consumer to wire it to: the
control plane has **no git remote at all**, and push is **contractually forbidden** by its own `AGENTS.md`.
Activating a credential-bearing push capability into a plane that forbids push would be
permission-widening, not engineering. The deliverable is the decision, the measured call-site survey, and
the enumeration of the activation surfaces (`evidence/BROKER_ACTIVATION_ANALYSIS.md`).

A methodology trap was found and applied: most of `config/` is **untracked**, so a `git grep` survey
reports a confident zero having read almost nothing. Every zero here came from a working-tree search.

## 2. Independent verification (REQ-PIPD-R11-VERIFY-005)

Lane `VERIFY_SECURITY`, forced rank 4, `required_arm = openai-codex/gpt-6.1-sol` (OpenAI OAuth), served
through the relay at `127.0.0.1:10101`; the round ran **no** model other than the declared checker.

**Three dispatches were VOID before one was valid.** They are recorded as VOID, not as failures, and each
root cause was fixed:

| # | receipt | root cause | fixed by |
|---|---|---|---|
| 1 | `ERR_NO_ARM_EMITTED_NONCE` | the brief was passed as a **path**; the child was handed a path as its prompt, was blocked reading it, and honestly returned INCONCLUSIVE | pass the brief's **content** |
| 2 | `EXIT=1` + `PermissionError` traceback | the guard crashed on an unreadable file in the control plane (`relay-supervisor.cooldown.json.lock`) | guard the product subject only - **and disclose that reduction** |
| 3 | `ERR_NO_ARM_EMITTED_NONCE` | the brief never asked for the lane nonce, so a **complete** adversarial verification was voided unread | an explicit `OUTPUT CONTRACT` section in the brief |

All four delivery defects are written up in `far/FAR-PIPD-R11-LANEDISPATCH-003.md`. The third attempt's
verdict is retained as `verify-codex/VOID_ATTEMPT_2_ADVERSARIAL_FINDINGS.json` with
`is_an_acceptance_input: false` - it is not evidence of acceptance, but its findings are why the
corrections below exist, so deleting it would hide the trail.

**Pass 4 was valid**: `ok: true`, `served_arm == required_arm == openai-codex/gpt-6.1-sol`,
`subject_mutation: CLEAN` (4158 files before and after, nothing added, changed or removed), 369.6s.
Verdict **`UNCERTAIN`** - C1-C6 PASS, C7 UNCERTAIN - with six actionable disagreements (section 2.1).

**Pass 5 (on the corrected artefacts) was valid too**: `ok: true`, same arm, `subject_mutation: CLEAN`
(4179 / 4179), 357.6s. It returned **`FAIL`** - and it was right. It confirmed five of the corrections
(C2, C3, C4, C5, C6 explicitly say "Correction CONFIRMED") and then showed that **the provenance fix did
not do what it claimed**: see correction 7 below. That is the whole point of running a second pass on a
correction - a fix is not verified by having been written.

**Pass 6 (on the repaired tree) was valid as well**: `ok: true`, same arm, `subject_mutation: CLEAN`
(4188 / 4188), 387.8s. Verdict **`UNCERTAIN`** - C1-C6 PASS, C7 UNCERTAIN - and it confirmed the repair
explicitly: *"The third-pass repair is complete: no reachable `--no-probe` return still labels PROBED."*
It then raised three smaller items, of which two were real over-claims by the maker's own standard and are
fixed as corrections 8 and 9 below. `C7` stays UNCERTAIN for the same structural reason every time: a
credential-free checker cannot establish the credentialed half of a write claim, and this round never gave
it credentials.

### 2.1 What the valid verdict said, including the parts that went against the maker

Verdict **`UNCERTAIN`** - C1-C6 PASS, C7 UNCERTAIN. It was adversarial, and it was right more than once:

- **It disproved a maker claim.** The claim "a configured-but-unprobed App is refused" is **false**: the
  explicit `--no-probe` flag yields `app_cred_valid: SKIP` and a bare `verdict: OK` over a credential that
  was never proven. Reproduced from the committed source.
- **It then found a second opt-out the maker had not enumerated**: `--metadata-only` never reaches App
  source selection at all and returns `OK` over a file's byte length.
- **It caught a docstring that contradicted its own code** (`run_preflight` claimed a missing getter leaves
  "the gate on the PAT"; the code keeps `effective_source=app` and fails closed).
- **It caught a stale expectation the maker introduced**: `INSTALL_MANIFEST.json` V3 still declared
  `5/5 PASS` while the suite it names records **seven** checks after the T1 split.
- **It refused a self-defeating acceptance rule**: the brief ordered a search for secret-shaped literals
  *using those literals as examples*, so the brief flagged itself. It explicitly called this an
  "acceptance-rule failure, not a secret leak" - and it was right not to inflate it into a finding of
  leakage.
- **It refused to let the write claim stand as proven**: an anonymous `ls-remote` of a **public** repo
  establishes advertised refs only, never writer attribution or credential provenance.
- **It refused to adopt the maker's suite numbers**, because both suites write temporary files and the
  brief had ordered VERIFY_ONLY: it returned `UNCERTAIN` rather than relaying them. What it *did*
  re-derive independently is the pin set - all seven sha256 pins match, from both the working tree and the
  blobs in the commit, mismatch count zero.

### 2.2 The checker's could-not-verify list, quoted

> - The organisation-owned App installation token authenticated the claimed write: no credential-free read
>   can establish writer attribution, and this VERIFY_ONLY run did not acquire credentials or perform any
>   credentialed action.
> - The historical ref transition `1136a69..ae08136` and historical unchanged tags: the present remote
>   advertisement does not establish earlier ref values or when they changed.
> - The narrated provider operations, including personal App deletion, organisation App
>   retention/ownership, the real PAT's HTTP 401, account token-list contents, and the stored credential
>   manager's live credential.
> - The maker's historical before-addition preflight execution: unchanged sealed bytes across the commit
>   and the independently rerun present preflight are established, but a narrated past command execution is
>   not.
> - Historical lane-dispatch execution, served model identity, usage/cost figures, sandbox rejection, and
>   the reported unreadable-lock failure: the requested FAR contents were inspected, but prior executions
>   are not re-derivable from the artefacts.
> - Canonical live admission states and broker activation governance beyond the requested artefact
>   readback: six FROZEN entries are confirmed in the admission JSON, not independently queried from the
>   typed API.

These limits are accepted, and they are the reason for the claim ceiling in section 4. They are also the
honest answer to "why is this not closed": a checker without credentials cannot verify a credentialed
narrative, and this round did not give it credentials.

## 3. What was corrected as a result

1. **Two over-claims in `FAR-PIPD-R11-CREDGATE-001`** - the false refusal claim, and a ceiling
   (`FIXED_AND_REPROVEN`, `CONFIRMED_BY_A_REF_MOVE`) that exceeded what independent checking can support.
   Ceiling lowered to say **corroborated, not proven**, for attribution.
2. **`INSTALL_MANIFEST.json` V3** expectation corrected from `5/5` to `7/7` with the reason.
3. **The control plane now labels an unproven `OK`**: `_verdict()` carries an **additive** field
   `provenance: PROBED | UNPROVEN_BY_REQUEST`. Deliberately additive - no existing key changes value, so
   the documented exit-code contract and every existing reader are untouched - it exists so the two kinds
   of `OK` cannot be confused. The two flags are labelled, not removed: they are legitimate offline
   opt-outs. Manifest re-pinned 7/7; `selftest` 7/7 PASS; `verify_offline` `PASS_OFFLINE_T5_UNPROVEN`.
4. **The `run_preflight` docstring** corrected to match its code.
5. **The evidence artefact's wording** narrowed from a categorical write to `CORROBORATED`, with the
   sidecar re-sealed and the reason for the re-seal recorded in its `revision_history`.
6. **`BOARD_READBACK.json` refreshed**, because the checker correctly flagged that the recorded statuses
   had drifted from the live board. Both snapshots are kept so the drift stays visible.
7. **The provenance fix was itself incomplete, and the second verification pass caught it.** Only the
   function's final return had been given the flag; `run_preflight` has **four** return points. The
   checker's counterexample - configured App + absent PAT + `--no-probe` - still reported
   `provenance: PROBED` while the flag had just skipped the probe: the exact mislabel the field exists to
   prevent, reintroduced by a partial fix. All four returns now carry it, and completeness was proved by
   **enumerating every `_verdict(` call in the function and asserting each one** (4/4), not by spot-check.
   The generalisable lesson is recorded in the FAR: a flag threaded through one return path is not a flag
   threaded through a function.
8. **The provenance FIELD NAME over-claimed, and was replaced by a boolean.** The checker's objection was
   exact: `PROBED` asserted more than it knew - the no-source, invalid-PAT, missing-getter and
   mint-exception paths all returned `PROBED` having made **zero HTTP calls**. The field is now
   `probe_skipped_by_request: true|false`, answering exactly the one question actually known, and nothing
   more. A label must not claim a measurement that was not taken.
9. **A second over-inference was cut out of Finding 2.** That finding called an `Everything up-to-date`
   no-op push proof of "a live write credential" held by the host's credential manager. A no-op sends **no
   ref update**, so it establishes that a credential is *obtainable* and that the command succeeded - not
   that the credential *can write*. The claim was reconciled in the weaker direction, and it also resolved
   an internal contradiction: the same FAR already said correctly that a no-op push proves nothing about
   write permission. What remains is "an uninspected stored credential exists and is usable by git for this
   remote", which is enough to raise as an owner decision and not enough to call a proven write credential.
   This is the round's own rule applied to the round: **name the observation that would be impossible if
   the claim were false, and take that one.**
10. **One correction is impossible by construction, and is therefore disclosed rather than attempted.**
   The false claim also appears in the **commit message of `8ab82ec`**, which is immutable. Amending it
   would mean rewriting history, which the Owner grant forbids (no force-push, no moving published refs).
   So it is left standing and **corrected forward**: by `far/FAR-PIPD-R11-CREDGATE-001.md`, by the
   docstring fix, and by a later commit in the same repository. A checker WILL keep reporting this
   disagreement on every future pass, and that is the correct outcome - the honest answer is "yes, that
   message is wrong; here is the correction, and here is why the message itself cannot be changed", not
   silently rewriting a published commit.

## 3.1 Convergence and the stop criterion, stated up front

The round is **not** chasing a PASS, because the two structural items below can never be a PASS. The
monitoring order is to detect a repeated abnormal block by CLASS and then either intervene or stop, so the
criterion is written down rather than decided in the moment:

1. **`immutable_commit_message_claim`** will be reported on **every** future pass and can never be fixed
   the way a file can: the false sentence lives in an immutable commit message, and amending it means
   rewriting published history, which the Owner grant forbids. The correction is forward-only (the FAR,
   the docstring, later commits). **A checker reporting this again is not progress and will not be
   re-fixed.**
2. **`C7` stays `UNCERTAIN`** for a structural reason: a credential-free checker cannot establish who
   pushed or with which credential, and this round deliberately did not hand it credentials. **More passes
   cannot move it.**

Both are therefore accepted as the terminal state of this round. What a further pass CAN still add is a
new *fixable* defect, and the marginal yield has fallen: pass 4 raised 6 items, pass 5 raised 1 (serious),
pass 6 raised 3 (all minor). One final pass is run on the swept tree, and **if it returns only the two
items above plus already-known corrections, the round stops there** and this ceiling stands.

The recurring parent class was **not** left to the checker to keep finding. It was attacked directly by
sweeping the round's own artefacts for strong-claim words (`proves`, `proof`, `demonstrably`, `guaranteed`,
`definitively`) and auditing each hit. That sweep found **two live instances no checker had yet reported** -
"the broker is proven end to end for read and write" in this report and the same phrase in the OpenSpec
proposal - both contradicting the same documents' own "corroborated, not proven". They are corrected here.
That is the intervention: do not wait for the next alarm to find the class the last three alarms were all
about.

## 4. Claim ceiling

```
SIX_OBLIGATIONS_ADMITTED_FROZEN__TWO_OWNER_OPERATIONS_SETTLED_WITH_READBACK_ONE_BEING_A_HONEST_NO_OP__
ROUND_USE_INTEGRATED_IN_THE_TEAM_CONTRACT_FORM_WITH_THE_SEALED_BINDING_PROVEN_UNMOVED_BY_BEFORE_AND_AFTER__
BROKER_ACTIVATION_DECIDED_NOT_PERFORMED__CREDENTIAL_GATE_LABELS_AN_UNPROVEN_OK_ADDITIVELY__
TWO_OVERCLAIMS_AND_ONE_STALE_EXPECTATION_CORRECTED_AFTER_INDEPENDENT_CHECK__
VERDICT_UNCERTAIN_WITH_THE_UNVERIFIABLE_HALF_NAMED_AND_NOT_CLAIMED
```

Explicitly **NOT** claimed: `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`,
release signing or builder attestation. The maker does not self-accept, and no verdict here is an
acceptance of any subject.

## 5. Open items, by WHO can close them

**Only an external acceptor can close**
- `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`
- release signing / builder attestation
- `DEL-004` (the SPEC registry lives outside this repository)
- the credentialed half of the write claim: **who** pushed, with **which** credential. No credential-free
  read can establish it, and this round deliberately did not hand the checker credentials.

**A control-plane round can close (recorded, not sneaked in)**
- **the dispatcher's guard crashes with a raw traceback on an unreadable path** instead of refusing with a
  typed code. Editing the dispatcher is itself an escalated control-plane operation and deserved its own
  admission, so it was NOT repaired as a side effect of a verification run.
- **the residual gate hole**: a consumer that reads `verdict` and ignores `provenance` still sees a bare
  `OK` on an unproven run.
- **broker activation**, if a decision is ever made that an in-repo push lane should exist.

**The owner can close**
- nothing is outstanding that requires the owner's hands. The deletion is done; the PAT needed no
  revocation. (One further login would re-open the per-session browser automation, but nothing requires it.)

**Disclosed, not closed**
- **the host's credential manager holds a live write credential for the repository**, independent of both
  the dead file and the App. It was identified and **left in place**; rotating it is an owner decision.

## 6. Every side effect of this round

| target | effect |
|---|---|
| `HG-KSEOS` | commits `8ab82ec` (the gate fix), `97cfb5b` (the stale V3 expectation), `d937fc0` (the additive `provenance` field and the docstring) |
| `PIPD-r7-release` | commits `ae08136` (admission + round artefacts), `6f1e5c6` (FARs, activation analysis, brief), `309377b` (over-claim corrections + FAR-003 + rev-2 brief + the VOID verdict), `691ec6c` (both opt-outs enumerated + board readback), plus this closure commit. **No push yet** - see below. |
| `Fabric` | commits `463ca0a` (the evidence artefact + sidecar), `0c1e6bc` (the narrowed claim + re-sealed sidecar). Exactly the round's own paths; the working tree's other entries left as found (49 after, from 51 before this round's later additions). |
| GitHub | **one** personal GitHub App deleted; one login and one second-factor entry by the owner; the organisation App verified intact |
| Hermes | kanban board `pipd-r11-20261011` updated (two cards completed **with `--result` evidence**, because the board refuses an empty completion, plus comments); one skill reference extended with the escalated-checker dispatch traps |
| processes | four verification lane dispatches (three VOID, one valid); no process left running |

**Remote state**: the product repository's `main` now advertises **`adafe58`**, pushed this round through
the broker with the organisation App's installation token (`ae08136..adafe58  main -> main`, exit 0,
`credential_kind: app`, `secret_leaked: false`), and read back **independently of the broker** with every
credential helper blanked - the remote value equals the local head, the working tree is clean and no
helper residue was left in `.git/config`.

One operational defect was found while doing it, and is disclosed rather than tidied away: the first push
attempt **failed** (`error: src refspec main does not match any`) because the broker runs `git` in the
**caller's** working directory, and the caller was the control plane, whose branch is
`codex/hgk-final-closure-002` and which has no remote. Re-running with the product repository as the
working directory succeeded. **The failure was visible and was not reported as success** - which is the
reason the helper is blanked and the readback is done outside the broker rather than trusting its verdict.

Tags are untouched: `v0.1.0-preview.1 = cc9bf574…`, `v0.1.0-preview.2 = 8faa64e5…` (re-read after the push).
