# Tasks

> Status legend: `[x]` = done and re-verified against the frozen candidate by the orchestrator, not merely
> claimed by the writer lane. `[~]` = done as far as the local candidate allows, with the residue named.
> `[ ]` = not done.
>
> Denominator: the ten findings `F-R5-01..10` of the R5 post-challenge report (2026-10-10). The route-out
> Work Orders are `WO-S4-DIAG-001`, `WO-S4-AO-002`, `WO-S4-CAL-003`, `WO-S4-TQAEP-004`, `WO-DOC-STATUS-005`.

## WO-S4-DIAG-001 — doctor diagnoses the schema root the CLI uses (`F-R5-01`, P0)
- [ ] 1.1 `registry.describe_schemas_source()` returns the resolved schema directory plus its mode
      (`OVERRIDE` / `INSTALLED` / `SOURCE`) and the candidate list actually tried.
- [ ] 1.2 `workspace.doctor(root)` reports `schema_source{ mode, path, tried }` and validates the exact
      packaged set (`registry.json` + 19 `<Family>.schema.json`) at that root: count, parseability,
      `$schema` draft, `$id` presence and registry-required-fields enforcement.
- [ ] 1.3 An installed wheel missing a packaged schema member yields `verdict=FAIL`, a finding naming the
      missing family, and CLI exit 1 — never a silent fallback to the workspace copy.
- [ ] 1.4 A healthy source tree and a healthy install both report 19/19 PASS with the mode named.
- [ ] 1.5 Affected regression: doctor/validate/install/export UAT rows and `tests/test_wheel_distribution.py`.

## WO-S4-AO-002 — independent re-derivation on the new frozen subject (`F-R5-02`, P0)
- [ ] 2.1 Publish a new immutable candidate tuple (commit / tree / product digest / wheel sha) and use it
      for every raw receipt of this round.
- [ ] 2.2 A non-Maker checker runs from a fresh process against the read-only candidate and re-derives the
      UAT matrix and the 13-command surface in source and installed modes.
- [ ] 2.3 The checker records its own identity, model route and transport, and returns
      PASS / PARTIAL / FAIL with named NOT_RUN rows rather than a coverage claim.
- [ ] 2.4 No R5 (`5094939…`, `d1aad3e…`) attestation is reused as this round's receipt.

## WO-S4-CAL-003 — per-atom gate anti-dilution (`F-R5-04`, P1)
- [ ] 3.1 The gate computes and prints a **unique validated obligation** denominator (dedup by canonical
      atom identity) alongside the raw atom count.
- [ ] 3.2 Fixtures at 2 / 237 / 801 unique obligations, plus a genuinely long single clause.
- [ ] 3.3 An adversarial payload padded with filler / duplicate atoms must not pass an over-budget gate;
      the padding-invariance is a test, not a claim.
- [ ] 3.4 The historical `343547 > 20000` FAIL remains verbatim in the historical section and the owner's
      `PER_ATOM_BYTES(2000)` objective is unchanged.

## WO-S4-TQAEP-004 — TQAEP design-time positive (`F-R5-05`, P1)
- [ ] 4.1 UAT-03 carries a legal design-time candidate compiling to `ClaimCeiling = TQAEP_DESIGNED`.
- [ ] 4.2 The SoD negatives (missing receipt / `SELF_ATTESTED` / maker == checker alias) still refuse
      typed.
- [ ] 4.3 The produced artifact is a design contract; no `INDEPENDENT_PASS` is derivable from a receipt
      string and the checker identity fields stay distinct.

## WO-DOC-STATUS-005 — README status landing (`F-R5-07`, P2)
- [ ] 5.1 The README first screen labels the historical R3 snapshot and names the current branch.
- [ ] 5.2 `main` vs `r5-s4-packreader` is stated explicitly, with `ACCEPTANCE.md` as the current entry.
- [ ] 5.3 The `LicenseRef-PIPD-Proprietary` internal-evaluation / no-public-grant position is visible on
      the first screen; historical receipts are not rewritten.

## Cross-cutting
- [ ] 6.1 Native prompt-contract compiler receipts present (`PROMPT_COMPILE_PASS`, contract / prompt /
      compiler sha256) for this round's contract.
- [ ] 6.2 HGK admission readback: five `REQ-PIPD-R5P-*` requirements FROZEN with TaskSpec + WorkOrder.
- [ ] 6.3 Kanban board + SWARM graph created and read back; GSTACK route readback recorded; OpenSpec change
      validates.
- [ ] 6.4 `F-R5-01..10` disposition table with per-finding close condition and honest NOT_RUN rows.
- [ ] 6.5 Evidence pack: baseline/new sha, wheel sha, per-case raw stdout/stderr/exit, checker identity.
