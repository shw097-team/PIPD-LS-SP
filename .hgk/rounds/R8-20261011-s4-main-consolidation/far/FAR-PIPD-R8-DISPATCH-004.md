# FAR-PIPD-R8-DISPATCH-004 — `--require-arm` verifies an arm but does not *select* it

Round `R8-20261011-s4-main-consolidation`, item 4 (new gap, adjudicated in-round). Discovered while
executing item 1.

## 1. The finding

`hgk-lane-dispatch.py --require-arm openai-codex/gpt-6.1-sol` **does not restrict the run to that
arm.** The candidate list is built unfiltered from the lane's pool and the loop walks it in rank
order, stopping at the **first** arm that satisfies `exit == 0 and nonce_present and
usage_receipt_ok`. `--require-arm` only (a) refuses when the named arm is absent from the pool, and
(b) refuses when the named arm fails the identity gate. It never makes the named arm the one that
runs.

Measuring it, from the run's own receipt:

```
mode                   = pinned_primary
candidates_considered  = [1, 2, 3, 4]          # <- with --require-arm openai-codex/gpt-6.1-sol set
attempts               = [ rank 1, opencode-go/deepseek-v4.1-flash, exit 0, nonce True, usage_ok True ]
used_rank              = 1
served_arm             = opencode-go/deepseek-v4.1-flash
required_arm           = openai-codex/gpt-6.1-sol
code                   = ERR_REQUIRED_ARM_NOT_SERVED
```

One attempt, rank 1, and the loop broke there. Rank 4 — the arm I required — was never invoked.

## 2. Why this matters more than it looks

The receipt is **honest**: it reports `ok: false` and names the mismatch. The danger is elsewhere.

**A verifying role's whole value is that it is not the maker.** Here a run configured to be
cross-model silently executes on rank 1 — and in this stack **rank 1 of `VERIFY_SECURITY` is
`opencode-go/deepseek-v4.1-flash`, the same model that serves PLAN and EXECUTE.** The defect
therefore converts "independent cross-model verification" into "the maker checking itself", while
the *configuration* on record still says `--require-arm openai-codex/gpt-6.1-sol`. An operator who
records the command line and not the receipt would report an independence that never existed.

The post-hoc `ERR_REQUIRED_ARM_NOT_SERVED` is what saves it — and it only exists because
`--require-arm` was set. Without it, a run that served the wrong arm would read as a clean pass.

## 3. Root cause

Two independent code paths, one assumption between them:

| line | behaviour |
|---|---|
| 596–615 | `--require-arm`: refuse if the arm is absent from the pool or fails the gate. **Fail-closed on absence only.** |
| 671–687 | the execution loop: `for i, e in enumerate(entries)` over the **unfiltered** candidate list, `break` on first success. |

Nothing joins them. "The arm survived the gate" is treated as "the arm will run", and it does not.

**A near-miss that must be recorded.** My first reading of the relay usage log found three
`openai-p6a1fe3 / gpt-6.1-sol / status 200 / effort medium` rows inside the run window and I briefly
concluded the arm *had* been served and the dispatcher had mis-attributed it. That was wrong, and
the receipt refuted it: those rows came from the earlier four-rank smoke run, which *does* reach
rank 4. The `attempts` array — one entry, rank 1 — is the authoritative record. Had I reported the
mis-attribution, I would have published a false exoneration of a real defect.

## 4. Options

| | Option | Assessment |
|---|---|---|
| **A** | **Call `--force-rank 4 --max-candidates 1` alongside `--require-arm`.** | Recommended *now*. Caller-side, no control-plane change, immediately effective, and it makes the executed arm explicit. |
| B | Patch the dispatcher so `--require-arm` filters `entries` to the named arm. | The correct long-term fix, but it edits **HG-KSEOS control-plane tooling**. Candidate-only by contract, needs its own admission, and must not ride along inside a PIPD round. |
| C | Rely on the post-hoc `ERR_REQUIRED_ARM_NOT_SERVED`. | Already in place and it does fail closed on *reporting* — but it wastes the whole run and leaves the "did it really run cross-model?" question to be settled by hand, as happened here. |

**Adjudication: A now, B recorded as a candidate tool change, C retained as the backstop.** A
closes the defect for this round without touching the control plane; B is named so the next round
that owns the tooling can implement it deliberately.

## 5. What the corrected invocation must be

```
hgk-lane-dispatch.py --lane VERIFY_SECURITY \
  --require-arm openai-codex/gpt-6.1-sol --force-rank 4 --max-candidates 1 \
  --codex-home C:/Users/user/.codex \
  --sandbox danger-full-access --allow-sandbox-escalation \
  --guard-subject <repo root> --cwd <scratch> --prompt <...>
```

`--max-candidates 1` matters as much as `--force-rank`: without it, exhaustion of rank 4 falls
through to other arms and re-opens the same hole.

## 6. Claim ceiling

`DISPATCH_REQUIRE_ARM_DOES_NOT_SELECT_ARM_MEASURED` — an assertion about the behaviour of
`hgk-lane-dispatch.py` as it stands at this commit, evidenced by a receipt. It is not a claim that
any other lane tool has the same shape, nor that option A is equivalent to option B.
