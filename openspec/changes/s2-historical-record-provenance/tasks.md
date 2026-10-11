# Tasks

> Status legend: `[x]` = done and re-verified. `[~]` = done as far as the local candidate allows, residue
> named. `[ ]` = not done.
>
> **This change is a CANDIDATE. Every task below is `[ ]` — nothing in it has been implemented, and no
> claim beyond `CANDIDATE_ONLY` is made or inherited.**

## WO-S2-RECORD-001 — separate recorded history from live measurement (`tools/perf_budget.py`)
- [ ] 1.1 Add `RECORDED_ARTIFACT = ROOT / ".hgk" / "artifacts" / "s2" / "PERF_BUDGET.json"`; load it once, tolerantly (absent/unreadable → no recorded values)
- [ ] 1.2 Rebuild the `historical` block from the recorded file, not from `advisory`; for each advisory metric `m` emit `value` = recorded `rows[metric=m].value`, `recorded: true`, `origin` = {`file`, `field`}
- [ ] 1.3 Carry `measured_now` on every historical row, populated from the live advisory measurement, kept in a field disjoint from `value`
- [ ] 1.4 No-recorded-value path: `recorded: false`, `value: null`, `origin: null`, `note: "NO_RECORDED_VALUE ..."`; `measured_now` still populated; never invent a value
- [ ] 1.5 `verdict`/`exceeded` on the historical row come from the RECORDED verdict (never recomputed from live data); `budget` comes from the unchanged `PROVENANCE` map
- [ ] 1.6 Cross-check: the preserved `context_bytes_per_artefact` recorded value must equal `pi_bytes` in `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`; a mismatch is reported, not swallowed
- [ ] 1.7 Prove no deciding value changed: `PROVENANCE` budgets, `REGRESSION_TOLERANCE_PCT`, `_verdict`, and `voting_metrics` are byte-identical to before

## WO-S2-RECORD-002 — regression test bound to the recorded files
- [ ] 2.1 `tests/test_perf_budget_records.py`: read the expected recorded value from `.hgk/artifacts/s2/PERF_BUDGET.json` **at test time** and assert the printed `historical` `value` equals it
- [ ] 2.2 Assert the printed recorded value also equals `pi_bytes` in `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`, read at test time
- [ ] 2.3 Negative-by-construction: the test source contains no literal recorded number (grep-checkable); it fails if either file is edited independently of the printed value
- [ ] 2.4 Assert `recorded` is a bool, `origin.file`/`origin.field` are non-empty when `recorded` is true, and `measured_now` is a distinct field on every historical row
- [ ] 2.5 Absent-file case: point the loader at a missing path and assert every historical row is `recorded: false` with a null `value` and a `NO_RECORDED_VALUE` note — no invention
- [ ] 2.6 Guard: assert `res["voting_metrics"] == ["bytes_per_atom"]` and every brief budget value is unchanged

## WO-S2-RECORD-003 — falsifiability and claims
- [ ] 3.1 Adversarial check: perturb the live measurement (or the recorded file) and confirm the printed `value` stays the recorded one while `measured_now` moves, and that 2.1/2.2 go red
- [ ] 3.2 Adversarial check: confirm no new field is emitted with a live number in a recorded slot, on any advisory metric
- [ ] 3.3 Keep `ClaimCeiling = CANDIDATE_ONLY`; record that this change is proposed, not accepted, and that a green `openspec validate --strict` proves only well-formedness

## Evidence
- [ ] 4.1 Attach the `--check` report before/after and its SHA-256
- [ ] 4.2 Attach the regression-test run output (raw), showing it reads the files at test time
- [ ] 4.3 Attach `openspec validate s2-historical-record-provenance --strict` raw output with exit code
