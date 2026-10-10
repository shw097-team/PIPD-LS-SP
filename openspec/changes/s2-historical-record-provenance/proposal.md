# S2 historical-record provenance — separate the RECORDED value from the LIVE measurement in `tools/perf_budget.py`

**Status: CANDIDATE — not accepted, not released, not independently verified.** Claim ceiling
`CANDIDATE_ONLY` (see *Claims*). This document proposes a contract change; it does not claim the change
is made.

## Why

`tools/perf_budget.py` prints a `historical` block whose stated contract, in the module comment at lines
32–33, is that

> the historical 343,547 > 20,000 FAIL is preserved verbatim and is still emitted in the `historical` block.

It is not. The block is assembled from the **live** advisory rows in the same process:

```python
"rows": [{"metric": r["metric"], "value": r["value"], "budget": r["budget"],
          "verdict": r["verdict"], ...} for r in advisory],
```

`r["value"]` is the number measured a few lines earlier in this run, never a value read from any
committed record. There is no `343547` literal in the file — `grep` finds `343,547` only *inside that
comment* — and no code path reads `.hgk/artifacts/s2/PERF_BUDGET.json`; the file is only ever **written**
(line 260). The `historical` block labelled "preserved verbatim" therefore re-emits the LIVE measurement.

Consequence: any change to the corpus (`docs/S0_CONTRACT_SPEC.md`), the compiler, or the schema set moves
the live number, and the block silently reports the new number as though it were the recorded one. The
recorded FAIL that owner ruling `S2_HISTORICAL_FAIL: PRESERVE` requires to "stay visible" becomes a
moving target that no reader can distinguish from a faithful replay.

## Evidence (verified on the frozen candidate, HEAD `7f13b90d`)

| Fact | Source | Value |
|---|---|---|
| Recorded historical value (the number that must stay visible) | `.hgk/artifacts/s2/PERF_BUDGET.json` → row `context_bytes_per_artefact` → `value` | `343547`, `verdict` `FAIL`, `exceeded` true |
| Frozen recorded PI size | `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json` → `pi_bytes` | `343547` |
| Recorded companion readings | committed row `sizes` | `pd` **2447** |
| Live companion reading | five `--check` runs | `pd` **1385** |
| Live PI size this tree | five `--check` runs × five `PYTHONHASHSEED` values | **343547** every time |

The recorded `sizes.pd` (2447) and the live `sizes.pd` (1385) differ, which proves the block reproduces
**today's** measurement rather than the recorded one. On this frozen tree the LIVE PI size happens to
equal the recorded 343547, so the defect is currently **latent and invisible**; it becomes visible the
moment the corpus or compiler moves.

**Honest reproduction note.** I could not reproduce the run-to-run variance I was told to expect
(366299, then 365351): on this frozen tree the live value is stable at 343547 across every run and every
hash seed tried. The defect is confirmed **structurally** — by reading the construction of the
`historical` block and by the recorded-vs-live companion drift — not by that variance. Stating this
openly matters, because the latent state is exactly what makes the block look correct.

## What changes

- **Recorded history and live measurement become separate fields.** The `historical` block is rebuilt
  from a RECORDED source, not from the live rows:
  - the historical row's `value` is the **recorded** value, read from a committed file;
  - `origin` names the file and field the recorded value came from (e.g.
    `{"file": ".hgk/artifacts/s2/PERF_BUDGET.json", "field": "rows[metric=context_bytes_per_artefact].value"}`);
  - `recorded` is a boolean;
  - the live number is preserved, clearly separated, as **`measured_now`**.
- **No recorded value is invented.** When the recorded artifact is absent, unreadable, or lacks a row for
  a metric, that row reports `recorded: false`, a null `value`, a null `origin` and a
  `NO_RECORDED_VALUE` note, while `measured_now` still carries the live number.
- **Nothing that decides is touched.** Every budget and numeric threshold is unchanged; the regression
  tolerance stays 10.0; `voting_metrics` stays exactly `["bytes_per_atom"]`; the recorded FAIL stays
  visible.
- **A regression test binds the printed value to the recorded file.** It reads the expected value from
  the recorded artifact (and the frozen `pi_bytes` from the baseline file) at test time and asserts the
  printed recorded value equals it — never a hard-coded literal.

## Design notes / non-goals

No change to `src/`, `schemas/`, `fixtures/`, or any other tool. No threshold is raised or lowered; no
row changes which verdict it votes. This is not a re-litigation of the owner ruling
`S2_BUDGET_DEFINITION = PER_ATOM_BYTES(2000)` or `S2_HISTORICAL_FAIL = PRESERVE`; it makes the *record*
those rulings depend on actually faithful. The `bytes_per_atom` row, its baseline and the regression
guard are out of scope.

## Claims

Claim ceiling: `CANDIDATE_ONLY`. This change is **proposed, unimplemented and unverified**. A green
`openspec validate --strict` attests only that this proposal is well-formed, not that any test passes or
that the defect is fixed. `S4_REPAIR_CANDIDATE_LOCAL_TESTED`, `INDEPENDENT_PASS`, `RUNTIME_READY`,
`PUBLICATION_APPROVED`, `RELEASED` and `PRODUCTION_VERIFIED` do not inherit and are not claimed.
