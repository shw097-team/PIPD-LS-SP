# Design — S4EXT-R1

## D1. Release identity: two fields, never one word

The defect was a *naming* defect with a data consequence: one phrase, "the `v0.1.1-preview.3` tag
commit", was used for two different facts — where the pack was **built from** and what the tag
**points at**. Every check in the repository compared documents against each other, so all eight
agreed and all eight were wrong.

Decision: `docs/RELEASE_TUPLE.json` (`PIPD-RELEASE-TUPLE/1`) becomes the single source of the two
fields, and the pack generator reads it. A document that wants to mention the previous identity must
mark the line as a disclosure (`erratum`, `previously published`, `superseded`, `lineage`), so the
verifier can distinguish "corrected" from "still wrong".

The published asset is immutable. Rewriting it would destroy the audit trail that makes the erratum
meaningful, so the correction is a *new* file plus a document that says exactly what was published
and what changed. Only the release owner may publish either.

## D2. Trace closure: reuse the engine that already exists

`pipeline.trace_closure()` already computed exactly the predicate the challenge wanted (missing
endpoint, `bad_hashes`, closure reached). The defect was that `validate_bundle()` never called it, and
that the schema accepted `{}` for the seven endpoint properties. So the change is:

* schema: type the endpoints (non-blank id, 64-hex hash, family enum, no extra keys);
* validator: call the existing closure and report a **three-valued** outcome —
  `FULL` (the chain closed), `SCHEMA_ONLY` (no edges in this bundle: the honest statement for a
  partial bundle), `FAILED` (edges present but not closable, or a hash mismatch);
* verdict: `FAILED` ⇒ `verdict = FAIL` and a non-zero CLI exit. `SCHEMA_ONLY` never claims closure.

The nested `PI-PKG.trace.items` repeats the endpoint constraints **inline** rather than `$ref`-ing the
`TraceLink` `$id`: the pinned validator does not resolve that URN, and a remote `$ref` would let the
resolver drift. A drift test asserts the two constraint sets stay equal.

Deliberately unchanged: `version` stays `string 1..64` with the legal value `"1"`; no 20th family; no
second trace engine.

## D3. Portability: derive, don't pin

`run.sh` / `run.ps1` compute the repository root from `BASH_SOURCE` / `$PSScriptRoot`, put the scratch
workspace under the platform temp dir, prefer an installed `pipd` (no `PYTHONPATH` at all) and fall
back to `$ROOT/src`. Preconditions run before any work and fail closed with a typed reason. Every
native invocation is followed by an exit-code check on Windows (`$LASTEXITCODE`), and the script's
success line (`FIRST_RUN_OK`) is printed only when the refusal step also behaved.

## D4. The 57-row adjudication is generated, not written

A hand-written adjudication drifts from the crosswalk and invites the very upgrade it is supposed to
prevent. The generator reads the crosswalk, requires an explicit disposition for every non-`EVIDENCED`
row (an un-answered row is a hard error, not a default), and emits a document whose test re-derives it
and refuses any status upgrade. `EVIDENCED` is deliberately left alone: it is a candidate evidence
path, not an acceptance.

## D5. Why the scope stops here

The report's §5 table is the boundary: provenance truth, current-release pinning, endpoint typing and
closure, first-run portability and profile boundary tests were approved; SemVer enforcement, a 12-axis
risk engine, `subject_id` UUID enforcement and S5–S8 activation were not. Nothing in this change
reaches past that table, and no row of the crosswalk is marked closed.
