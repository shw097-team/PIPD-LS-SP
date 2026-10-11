# FAR-PIPD-S4R2M-VERGRAM-002 — what to do about the loose `version` string grammar (finding `F04`)

- **Round:** `S4R2M-20261012-merge-and-preview3`
- **Question type:** adjudication of a deferred observation (`S4R2-POST-F04`)
- **Autonomy:** in-round FAR study, executed directly
- **Claim ceiling:** `LOCAL`

## The question

On the frozen subject, the 19 families' generic `version` field is `{type: string, minLength: 1,
maxLength: 64}`. A same-shape fragment test accepts `"broken-version"`, `"  "` and `"999"`. Should this
round tighten the grammar?

## Evidence taken this round

- `schemas/ArtifactIdentity.schema.json` and `schemas/PI-PKG.schema.json` on the frozen subject carry
  exactly that fragment; typed refusals for integer / null / empty are present and working.
- `src/pipd_ls_sp/pipeline.py` `_rec` emits the literal `"1"` for compiler-issued records on this
  subject. That value is *legal current output*.

## Decision

**No grammar change in this round.** The field is a typed, length-bounded string that refuses the wrong
shapes; what is missing is not a validator but a *version contract* — an authority that says which
version model the field expresses.

Adding `^\d+\.\d+\.\d+$` (or any semver-like pattern) now would reject the compiler's own current output
`"1"`, i.e. it would break a positive case in order to close a negative one. That is the exact
inversion the round contract forbids ("a valid compiler record must PASS; never only NEG").

The lowest-resistance, highest-necessity ordering is therefore:

1. Decide the version model from `PKG-01` / `DOC-04`'s version contract (candidates: a bare ordinal
   `"1"`; a dotted `"1.1.0"`; an `ArtifactIdentity@1`-style compound).
2. Identify an **active consumer that actually branches on the version**. If none exists today, the
   grammar is unfalsifiable and tightening it buys nothing but schema drift.
3. Only then add one positive fixture (a real consumer-visible version) and one negative fixture
   (a malformed version the consumer would mis-branch on), plus the minimal enum or pattern.

## Trigger to reopen

Reopen as a `P1` `CONFIRMED_DEFECT` if **either** holds: an external consumer is shown to branch on
`version` and mis-handle a malformed value, **or** a normative source (`PKG-01` / `DOC-04`) is found to
declare a fixed version syntax that the current schema does not enforce. Until then it stays a
`NON_BLOCKING_OBSERVATION` / `EVIDENCE_GAP`, and the report's own instruction not to manufacture five
work orders out of an already-closed mutant set is honoured.

## What this decision does not confer

- It does not claim the version field is semantically verified.
- It does not close `F04`; it records a triggered deferral with an owner and a falsifiable condition.
