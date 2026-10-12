# ACCEPTANCE RECORD - backup-model artifacts as the Stage-B candidate

Owner ruling under execution: whether the EXECUTE lane's artifacts may stand as the Stage-B candidate
**must be decided by an Independent Acceptance Officer (VERIFY/SECURITY)**, and if it passes they are
accepted, with a record kept, plus a FAR root-cause study and a lowest-friction prevention measure.

Lane: `stage-b/AO3_20261012T115506Z.log`, checker `gpt-6.1-sol` / provider `openai` (OAuth) / reasoning
`medium` - the declared VERIFY/SECURITY model. Verdict artifact: `verify/ao3/AO_VERDICT_STAGEB_R3.md`.

## The verdict that this record acts on

**ADJUDICATION B: `ACCEPT_WITH_CONDITIONS`.** In the officer's own framing: the reviewed local Stage-B
artifacts survive independent verification within the stated conditions; the verdict is conditional rather
than unconditional, and the conditions are **not represented as already satisfied**.

## Decision

Read as a pass within its stated conditions, therefore:

**ACCEPTED - the backup-model artifacts stand as the Stage-B candidate, scoped to the three conditions
below.** This is a scoped acceptance, not an unconditional one. The conditions remain OPEN items and each
must be discharged before the corresponding broader claim is made.

Interpretation note, stated so the owner can overrule it: the ruling said "if it passes, accept it". The
verdict is a conditional pass. I have therefore accepted the artifacts but recorded the conditions as
unsatisfied rather than silently promoting this to a clean pass. A reader must not treat this record as an
unconditional acceptance.

## The three conditions, as the officer wrote them

1. **Manifest identity/extension boundary.** Before any owner-filled candidate is treated as
   release-ready, independently check that official `plugin.json` `name` equals the release bookkeeping
   `plugin_id`, that `version` equals the release/receipt version, and that every extension namespace and
   value has been reviewed. The current builder does not enforce these. This Stage-B acceptance covers the
   exact reviewed manifest values only, and must not be extrapolated to operator-edited manifests. A claim
   that the builder fail-closes these inputs would need gates plus negative regression tests plus
   independent re-verification.
2. **Narrowed coverage claim must be retained.** Do not represent the full run as all discovered tests
   passing, nor as host or publication qualification. 19 discovered cases remain unexercised (2 individual
   plus 17 publication-projection cases). Do not create substitute refs or reseal evidence to erase skips.
3. **Model deviation and unresolved attribution must be recorded.** The rerun label was
   `opencode-go/deepseek-v4-flash`, not the originally declared `opencode-go/deepseek-v4.1-flash`, and the
   logs do **not** authenticate the actual upstream model. Before public release a reviewer must
   independently approve the substantive skill/projection decisions and the final publisher inputs rather
   than treating the lane label or synthetic approval fields as provenance or authorization.

## Defects the officer found that the maker's own suite did not

These are new, reproducible, and are the reason the verdict is conditional rather than clean. They are
recorded as open items with a named owner; they are **not** repaired by this record, and no repair has been
attempted:

| ID | Defect | Reproducer / evidence | Owner | Disposition |
|---|---|---|---|---|
| CR-IDENTITY-BIND | The official manifest `name` and `version` are not bound to the release bookkeeping identity. A valid but different official `name` is accepted at exit 0 while the ZIP root and receipt still identify the other plugin; `version 999.0.0` is accepted at exit 0 while the receipt and embedded release remain `0.1.1`. | `verify/ao3/probe-judgement-name*.txt`, `probe-judgement-version*.txt`, `verify/ao3/repro_identity.py` (`IDENTITY_MISMATCH_ACCEPTED: True`) | Package/Builder owner | OPEN - gate plus negative regression tests required before any release-readiness claim |
| CR-EXT-UNREVIEWED | An unreviewed opaque extension namespace (`com.ao3.unreviewed`) is accepted and preserved in the ZIP at exit 0. The locked vendor schema permits arbitrary object-valued namespaces; the owner derivation checks authorize SKILL.md transformations only, not manifest namespaces. | `verify/ao3/probe-judgement-extension.txt` and its readback | Package/Builder owner | OPEN - the delivered template's namespaces were inspected, but future arbitrary extensions are not gated |

Both are **accepted contradictory packaging inputs**, in the officer's phrase - not theoretical concerns.
The officer states no suggestion is supported that the model deviation caused either of them.

## Coverage correction (supersedes earlier round figures)

The officer independently counted the suite and corrected the accounting carried by earlier rounds:

| Figure | Value |
|---|---|
| Cases the loader discovers | **589** (no load errors) |
| Cases unittest reports as run | 572 |
| Successes | 567 |
| Individual skips | 5 |
| setUpModule skip | 1 (17 publication-projection cases never started) |
| Discovered but unexercised | **19** |

So the earlier phrasing "566 passed, 6 skipped" was wrong in both numbers, and `skipped=6` is **not** six
skipped cases. Supplemental system-Python runs later exercised the three pip-blocked cases; they are not a
second full-suite run. The 17 publication-projection cases, the stale-seal readback and the native symlink
case remain unexercised. On this host `O_NOFOLLOW` and `O_NONBLOCK` are **absent** (`False`), so Windows
runs do not exercise those optional POSIX branches; the symlink tests prove the predicate seam's refusal
branch, not real OS link capability.

## Model-deviation record (condition 3, discharged as a record)

| Item | Value |
|---|---|
| Originally declared EXECUTE lane | `opencode-go/deepseek-v4.1-flash` |
| Rerun lane label that produced the candidate | `opencode-go/deepseek-v4-flash` |
| Declared-model lane outcomes | B1/B2/B3 all recorded `.exit` = 1 |
| Actual upstream model | **NOT AUTHENTICATED**. The logs do not establish it. |
| Self-reported identities in the probe logs | `claude (Anthropic)` for one probe, `gpt-5-codex` for another, `unknown` for the checker probe - mutually inconsistent, zero authority |

What the officer found in the failing lanes, verbatim from their tails: **Provider error 400 /
`invalid_request_error`**, with the message **"The reasoning_content in the thinking mode must be passed
back to the API."** Its reading: the evidence supports a **request/history/protocol compatibility failure**
as reported by the upstream error, and does **not** establish that the requested model was nonexistent,
universally unavailable, or incapable of the task. Both DeepSeek-labelled probe logs also show a local
websocket **426 Upgrade Required** at the lane's relay endpoint before producing text.

Consequence for this record: the maker's earlier shorthand ("the declared model aborts on a thinking-mode
adapter bug") is **partly corroborated** - the upstream error does name thinking-mode handling - but the
implication that the model was unavailable or that a different model was therefore required is **not
supported by the evidence**. That causal question is handed to the FAR study, which must not accept the
shorthand either.

The officer also recorded: it declines to convert the deviation into an owner-only veto or into an invented
verified model identity. The deviation is **recorded, not laundered**.

## Claim ceiling of this acceptance

**ACCEPTED, scoped:** the reviewed local Stage-B artifacts survive independent verification within the three
conditions, and the mechanically reproducible parts (exact auxiliary-byte copying, LF-normalised digest
comparison, deterministic ZIP metadata and member order, recomputed hashes, exclusive-member refusals, typed
byte-drift refusals, the exact diff-path guard) were independently exercised and therefore do not depend on
trusting any model label.

**NOT accepted, not granted, not implied:** Portal approval or draft; publication or a public listing; host
qualification on any of the four agent hosts or on Plus/Free accounts; verified human publisher identity;
merge or release permission; production verification; `PIPD_S4_FULL_PASS`; and any claim that the builder
fail-closes arbitrary manifests.

Also not established anywhere in this round: that the vendor's own schema validator accepts the package; that
GitHub Actions has ever run; that a supplied ledger, receipt or digest is self-authenticating; that the
builder is safe against a hostile concurrent filesystem between its existence check and its promotion; and
that CRLF byte-for-byte preservation holds (text is LF-canonicalised before hashing and projection).

## Companion item, separate from this acceptance

The third-round **ADJUDICATION A returned `NOT_CLOSED`** - the delivery handed to that officer was not
clean. That is a handover-hygiene defect of the maker's harness, not of the candidate code: the same officer
independently confirmed that every path in the two closure commits is under `.hgk/rounds/**` and that no
code path changed, so the substantive part of the round-2 closure holds while its cleanliness promise did
not. The structural fix is the governed launcher `stage-b/run_lane.sh` (commit harness artifacts, refuse to
launch against a dirty worktree, write the lane log outside the worktree) and it is being independently
checked in round 4; this record does not claim that fix works.
