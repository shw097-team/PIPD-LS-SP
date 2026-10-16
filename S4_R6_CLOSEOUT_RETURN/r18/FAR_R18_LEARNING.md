# FAR-018 — Learning

run_id: `FAR-20261016-019-s4r6-external-handover`
Round: `PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016`

Rules are written as imperatives with the reason, and only where this round actually paid for them.

## 1. A guard must be tested against the defect class, not against the example that prompted it

The previous round built a doc-identity guard that checked in-page anchors. The requirement it was
implementing (F-R6-01) is about the *documented route being truthful*. A dead outgoing link is the
same class of defect and was invisible: the guard was green while the route was dead.
**Rule:** before writing a check for a stated requirement, enumerate the shapes the requirement
implies (in-page anchor, outgoing relative path, external URL, cross-document reference) and either
cover each or state the exclusion. A check whose coverage is narrower than its requirement, without
saying so, is worse than no check: it manufactures confidence.

## 2. Ask a reader who has never seen the repository to walk the route

The dead link survived two rounds because everyone involved already knew which file it meant.
**Rule:** the falsification for a documentation claim is an outside reader following it literally.

## 3. The plan documents are deliverables, and the last card on the board is their back-fill

Both checklists were left at `[ ]` after the work was done, so the plan said "not started" while the
evidence said "done" — and only an independent audit noticed.
**Rule:** make "back-fill the plan documents" an explicit, terminal card. Status without an evidence
ID, and a blank status on an executed row, are both defects of the deliverable.

## 4. A verdict file must carry its subject history, or a re-bind silently erases evidence

The packet's `checker_verdict.json` bound the first candidate while the final head was verified in a
side file. Re-binding by overwriting would have destroyed the record of what was verified when.
**Rule:** give a verdict artefact a `subject_history` array and append; never rewrite a binding.

## 5. Two manifests of the same packet must be comparable, and line endings are part of the bytes

The local manifest disagreed with the published one on one file. The cause was CRLF vs LF: the
content was identical, the bytes were not.
**Rule:** normalise text to LF before hashing, and when two manifests disagree, compare the *sets*
first, then per-path hashes, then byte length — that order isolates a line-ending difference from a
content difference in one step.

## 6. Do not "fix" a manifest by recomputing it over the files you can see

The first repair produced a 17-entry manifest because the recompute only looked at the top level and
dropped 11 entries from subdirectories. It looked correct and verified against itself.
**Rule:** a manifest is regenerated over a *declared* path set, and the result is checked against
that set's size and membership — self-verification alone will happily confirm a truncated manifest.

## 7. A round must not edit the registry it measures

The verification pool's rank-1 is the writer's own model by owner order. Editing the order to fix it
would have destroyed the measurement that establishes the defect.
**Rule:** when the thing you measure is also the thing you would need to change, pin around it (arm
identity), record the deviation, and deliver a not-applied candidate patch.

## 8. Report the credential's limit as a fact about the credential

The historical raw CI logs could not be frozen: this credential gets HTTP 401 on job logs.
**Rule:** record the locator, the exact refusal, and the ticket. Do not convert it into "evidence
unavailable" — that phrasing hides which key would open it.

## 9. An audit's own reading is not a re-verification

45 rows came back `ALREADY_SATISFIED`. Inheriting that reading is legitimate; presenting it as this
round's verification is not.
**Rule:** label inherited verdicts with their source in the same column as the verdict.

## 10. A lane warning is recorded, not smoothed

The writer lane's receipt carried `WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE` and stated that
inconclusive is not a pass.
**Rule:** transcribe warnings into the round's findings with their own ID. A warning that appears only
inside a receipt nobody reads is a hidden deviation.

## 11. Repair the validator in the strengthening direction or not at all

The temptation with a red gate is to widen the allowlist until it is green. The red gate here was
legitimate (a product file outside the declared set), and the two tempting alternatives — admitting
the round's evidence into the product write set, or adding a whole new stage arm — were both refused.
**Rule:** when a gate is red, assert first that the *change* is wrong or the *gate* is wrong; if the
change is wrong, fix the change. If you widen a validator, say in the commit message which class of
defect you have just made undetectable.

## 12. The gate that judges the round runs before the push, not after

The write-set classifier was executed locally on the exact commit before it was pushed, and it passed
27/27. Discovering the same fact from a red hosted check costs a review cycle and muddies the record.
**Rule:** reproduce the hosted gate locally against the exact commit, and record its verdict with the
commit SHA as the evidence.
