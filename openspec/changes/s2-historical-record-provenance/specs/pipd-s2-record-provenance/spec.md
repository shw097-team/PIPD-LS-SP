# pipd-s2-record-provenance

## ADDED Requirements

### Requirement: The budget report separates the recorded value from the live measurement
The `perf_budget` report SHALL present, for every non-voting (advisory) metric, a `historical` row whose
`value` is the RECORDED value read from a committed file, together with an `origin` naming the file and
field the recorded value came from, a `recorded` boolean, and a separate `measured_now` field carrying the
live measurement of the current process.

#### Scenario: A recorded value is re-emitted, not re-measured
- **WHEN** the committed artifact `.hgk/artifacts/s2/PERF_BUDGET.json` contains a row for
  `context_bytes_per_artefact`
- **THEN** the `historical` row for that metric reports `value` equal to the recorded value in that file,
  `recorded` true, and an `origin` naming that file and the field it was read from

#### Scenario: The live number is preserved under its own field
- **WHEN** any `--check` run produces the report
- **THEN** the live measurement of every advisory metric appears in `measured_now` and never stands in for
  the recorded `value`

#### Scenario: A metric with no recorded value says so
- **WHEN** the recorded artifact is absent, unreadable, or lacks a row for a metric
- **THEN** that row reports `recorded` false, a null `value`, a null `origin` and a `NO_RECORDED_VALUE`
  note, while `measured_now` still carries the live number — and no value is invented to fill the slot

### Requirement: Recording provenance changes no threshold and no voter
The change SHALL NOT alter any budget, any numeric threshold, the regression tolerance, or the set of
voting metrics.

#### Scenario: Budgets are unchanged
- **WHEN** the provenance map is read after the change
- **THEN** the budgets remain `compile_chain_ms` 2000, `validate_19_contracts_ms` 3000, `cli_cold_start_ms`
  6000, `context_bytes_per_artefact` 20000 and `bytes_per_atom` 2000, and the regression tolerance remains
  10.0

#### Scenario: The voting set is unchanged
- **WHEN** a `--check` run reports its `voting_metrics`
- **THEN** the list is exactly `["bytes_per_atom"]`

#### Scenario: The preserved FAIL stays visible and cannot be rewritten
- **WHEN** the recorded `context_bytes_per_artefact` value exceeds its unchanged 20000 budget
- **THEN** the `historical` row reports the RECORDED verdict `FAIL` and `exceeded` true, and no live
  reading of the current process can change that recorded verdict

### Requirement: A regression test binds the printed recorded value to the recorded files
The test suite SHALL assert that the `historical` block's recorded value equals the value read from the
recorded files at test time, and SHALL NOT hard-code that value in the test source.

#### Scenario: The recorded value is read, not literal
- **WHEN** the regression test runs
- **THEN** it reads the expected value from the recorded artifact at test time and its source contains no
  literal recorded number

#### Scenario: The printed value matches both recorded files
- **WHEN** the historical block reports the recorded value for `context_bytes_per_artefact`
- **THEN** that value equals both the row value in `.hgk/artifacts/s2/PERF_BUDGET.json` and `pi_bytes` in
  `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`, each read at test time

#### Scenario: A drifted live measurement is caught
- **WHEN** the live measurement differs from the recorded value
- **THEN** `measured_now` shows the new number while the recorded `value` is unchanged, so the divergence
  is visible and the regression test can detect it
