# Design — S2 historical-record provenance

## Context

`tools/perf_budget.py` carries two kinds of number through one `_row()` helper: the numeric budgets
unchanged since R4, and the provenance rows added in R5 S4 (the owner re-specified the deciding metric as
the scale-invariant rate `bytes_per_atom` and demoted the four originals to ADVISORY). The four advisory
rows keep their historical verdicts, and the report reprints them in a `historical` block whose comment
promises the recorded FAIL is "preserved verbatim and is still emitted".

The block is populated from the live advisory rows (`for r in advisory`), and `advisory` is derived from
`rows`, which were built by measuring this process. So the "historical" block is a live measurement wearing
a recorded label. The bug is a provenance bug, not an arithmetic one: nothing is mis-computed, but a claim
of preserved record is made by code that keeps no record.

## Decision 1 — a recorded source is read, and its fields are named

The `historical` block is rebuilt from a RECORDED source read at runtime:

```
RECORDED_ARTIFACT = ROOT / ".hgk" / "artifacts" / "s2" / "PERF_BUDGET.json"
```

For each advisory metric `m`, the recorded value is the `value` of the row in that file whose `metric == m`.
`origin` is emitted as the file plus the field it was read from:

```json
"origin": {"file": ".hgk/artifacts/s2/PERF_BUDGET.json",
           "field": "rows[metric=context_bytes_per_artefact].value"}
```

The baseline file `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json` is the frozen record of the PI byte
size (`pi_bytes` = 343547); the preserved `context_bytes_per_artefact` value must agree with it. This is a
cross-check, not a second writer — `--check` still writes nothing, and the recorded artifact is only
rewritten by a non-check run, exactly as today.

## Decision 2 — the live number keeps its own name

Every advisory metric carries `measured_now`: the value measured by this process, under its own key, next
to the recorded `value`. The two can never be confused because they never share a field. When the recorded
artifact is absent, unreadable, or missing the metric, the row reports `recorded: false`, `value: null`,
`origin: null` and a `NO_RECORDED_VALUE` note — and still reports `measured_now`. Nothing is invented to
fill the recorded slot.

Shape of one historical row after the change:

```json
{
  "metric": "context_bytes_per_artefact",
  "value": 343547,
  "recorded": true,
  "origin": {"file": ".hgk/artifacts/s2/PERF_BUDGET.json",
             "field": "rows[metric=context_bytes_per_artefact].value"},
  "measured_now": 343547,
  "budget": 20000,
  "verdict": "FAIL",
  "exceeded": true,
  "source_of_truth": "UNPROVENANCED"
}
```

`verdict` is the RECORDED verdict from the origin file and MUST NOT be recomputed from live data, so no
new run can rewrite the recorded FAIL. `budget` is read from the unchanged `PROVENANCE` map.

## Decision 3 — the test binds to the file, not to a constant

The regression test computes the expected value at test time:

```python
recorded = json.loads((ROOT / ".hgk/artifacts/s2/PERF_BUDGET.json").read_text())["rows"]  # find metric
baseline = json.loads((ROOT / ".hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json").read_text())["pi_bytes"]
printed  = historical_row("context_bytes_per_artefact")["value"]
assert printed == recorded_value(m) == baseline
```

The test source contains **no literal recorded number**, so it cannot pass by echoing a frozen constant;
it fails the moment the printed recorded value drifts from either file. This is the falsifiable core: an
adversarial checker can change the printed value, or the file, and watch the test go red.

## Decision 4 — nothing that decides moves

`PROVENANCE` budgets, the `REGRESSION_TOLERANCE_PCT` (10.0), the `_verdict` fail-closed logic and the
`voting` flags are untouched. The split only changes how the `historical` block is *sourced*; it changes
no verdict and no voter. `voting_metrics` remains exactly `["bytes_per_atom"]`.

## Risks and their mitigations

| Risk | Mitigation |
|---|---|
| The tool reading its own committed output looks circular | The record is a committed, git-tracked artifact; `--check` never writes it, so the read is of a frozen prior state, which is precisely what "preserved" means |
| A missing or corrupt recorded file silently degrades to a live number | `recorded: false` + `NO_RECORDED_VALUE` note is explicit and null-valued; the test asserts the recorded path when the file is present |
| The `context_bytes_per_artefact` recorded value and the baseline `pi_bytes` diverge on some corpus | that divergence is a real inconsistency the cross-check is designed to surface, not to hide |
| A reader mistakes the currently-latent state for correctness | the proposal states plainly that the live and recorded values coincide today and the defect is structural |

## Out of scope

The `bytes_per_atom` rate, its frozen baseline and the regression guard; any threshold change; any
`src/`, `schemas/` or other `tools/` file; the S2 lossless-dedup refactor (`S2_LOSSLESS_DEDUP =
DEFER_AS_REFACTOR`); and any claim of acceptance, release or independent verification.
