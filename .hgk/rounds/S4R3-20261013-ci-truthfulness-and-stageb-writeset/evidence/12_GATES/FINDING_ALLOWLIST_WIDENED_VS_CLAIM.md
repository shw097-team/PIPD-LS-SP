# Finding: the write-set allowlist WAS widened, and the round claimed it was not

Status: OPEN, owner decision required. Self-caught while producing the C3 baseline diff that the
verification lane had asked for three times.

## The claim, as this round stated it

Every C3 prompt sent to the verification lane asserted: "the write-set gate judges the branch's
DECLARED stage and base rather than the pull-request base; **the allowlists were NOT widened** and the
frozen-path refusals still refuse." The workflow's own inline comment says the same thing: "This
change widens NEITHER allowlist".

## What the evidence shows

Baseline diff, mechanical, in `C3_ALLOWLIST_BASELINE_DIFF.txt`:

| stage | vs the frozen R3 subject (e71fee6d) |
|---|---|
| stage-b | **+2 entries**: `docs/USER_GUIDE.md`, `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` |
| stage-b DENIED | unchanged: skills/, src/, schemas/, dist/ |
| stage-a | a new stage; its DENIED set **omits `src/`** (files there are still refused by the allowlist) |

## Why this matters

1. The statement the round has been putting to a verifier is contradicted by the round's own commit
   history. A verifier that had taken it at face value would have accepted an unverified claim about
   the governed write set.
2. The second addition puts the round's own evidence directory inside the governed set of a gate whose
   job is to judge what the round writes. The gate would not object to writes under
   `.hgk/rounds/S4R3-.../`, including writes to its own receipts.
3. `docs/USER_GUIDE.md` is a scope extension in its own right, even if a defensible one.

## What is NOT claimed here

Not claimed: that either addition was made to buy a green run. Both have ordinary explanations
(Stage B ships docs; the round commits evidence and the gate would otherwise reject it). The defect is
the ASSERTION, not a proven motive. Also not claimed: that any frozen path became writable for
stage-b - the denial set is unchanged.

## Remediation options (owner's choice, low friction)

1. **Correct the statement and keep the sets** (smallest change): amend the workflow comment and the
   round's C3 wording to enumerate the two additions and their justification, and stop asserting
   "neither allowlist was widened". No candidate head changes.
2. **Narrow the round-directory entry**: replace `.hgk/rounds/S4R3-.../` with the specific evidence
   paths the gate must tolerate, so the gate does not permit arbitrary writes under its own receipts
   directory. This edits the Stage A head, so it invalidates the audited head and needs a new
   verification round.
3. **Split the governance question from the repair**: keep the sets, record the two additions as a
   declared, reviewed deviation, and let the external acceptance officer judge them as part of C3
   rather than as a hidden widening.

## Ceiling

This finding rests on committed revisions and a mechanical set-diff. It is not an acceptance, and it
does not change any flag. `NO_MERGE`, `NO_PUBLIC_RELEASE` and `S4_FULL_PASS NOT_GRANTED` still hold.
