## Why

The R5 S4 candidate (`r5-s4-packreader` @ `0f06eec9`) passed the R4-class P0 repairs but an external
challenge review (2026-10-10) found a narrow, user-visible trust defect plus a set of unclosed evidence
gaps. The blocking one: `pipd doctor` validates `<root>/schemas` only, so an **installed** wheel whose
packaged copy is missing `ArtifactIdentity.schema.json` still prints `verdict=PASS` for a healthy
workspace — a false-positive diagnostic the ordinary user cannot detect. The remaining findings are
subject-binding (`F-R5-02`), wheel tamper semantics (`F-R5-03`), per-atom gate dilution (`F-R5-04`),
the missing TQAEP design positive (`F-R5-05`), SPEC/DEL S4-active coverage (`F-R5-06`), README stage
drift (`F-R5-07`), the unrun symlink negative (`F-R5-08`), the deferred HGK knowledge subset
(`F-R5-09`) and the Human-only license gate (`F-R5-10`).

## What Changes

- **Doctor diagnoses the resolver, not a convention.** `pipd doctor` SHALL report the schema root the CLI
  resolver actually selects (SOURCE / INSTALLED / OVERRIDE), read back the packaged `registry.json`
  exact set of 19 schemas, and typed-FAIL with a non-zero exit when a packaged member is missing even
  though the workspace copy is healthy.
- **One frozen subject.** The round binds every raw receipt to a single immutable candidate tuple
  (commit / tree / product digest / wheel sha) so no R5 attestation is inherited.
- **Tamper semantics are typed.** B4 (RECORD-unchanged / RECORD-adjusted) wheel mutations and B5
  truncation each end in a typed refusal or a typed integrity failure, never a silent PASS.
- **The per-atom gate carries an anti-dilution oracle.** A unique-validated-obligation denominator,
  2/237/801 atom scales, a genuinely long clause and filler/duplicate padding that must not turn an
  over-budget payload green; the historical `343547 > 20000` FAIL stays traceable verbatim.
- **The TQAEP positive path exists.** A legal design-time candidate compiles at
  `ClaimCeiling=TQAEP_DESIGNED`, next to the existing SoD negatives; no receipt string yields
  `INDEPENDENT_PASS`.
- **The README first screen is unambiguous.** Historical R3 snapshot is labelled, `main` is separated
  from `r5-s4-packreader`, `ACCEPTANCE.md` is the current entry, and the
  `LicenseRef-PIPD-Proprietary` no-public-grant position is stated — historical receipts untouched.

## Capabilities

### New Capabilities
- `pipd-s4-doctor-schema-truth`: the diagnostic surface covers the schema resources the CLI actually loads.
- `pipd-s4-perf-gate-antigaming`: the per-atom context gate resists obligation dilution and local overfit.

### Modified Capabilities
- `pipd-s4-usability-repair` (R5 change): the installed-resource, safe-write and export behaviours are
  preserved; only the diagnostic truth, the acceptance matrix and the docs landing change.

## Non-goals

- No full-package rewrite, no second workflow / reducer / Plan IR, no re-activation of `CAND-01..22`.
- No S5 live HGK receiver, S6 GENIE adapter, S7 JIT routing, S8 promotion, and no PRE-W3 claim.
- No push to `main`, no release cut, no public redistribution grant, no `PRODUCTION_VERIFIED`.
- No rewriting of historical FAIL rows, previous AO verdicts or existing attestations.
- No AI prose closing a defect: every claim needs raw evidence with a subject binding.
