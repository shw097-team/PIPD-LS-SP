# EXECUTE WorkOrder — bounded writer (Codex CLI)

**Writer**: Codex CLI, sealed lane, provider/model = `opencode-go/deepseek-v4.1-flash`.
**Role**: bounded WRITER. You implement exactly the change below. You do NOT verify it, do NOT
accept it, and do NOT claim it works. An independent checker runs afterwards and is entitled to
call your work wrong.

## Repository

`C:\Projects\Agent_Workspace\PIPD` — you are ALREADY checked out at branch
`r5-s4-packreader` @ `7f13b90`. **Your shell starts at a drive root, not the repo: `cd` to an
absolute path first, every time.**

## Defect (confirmed, with evidence)

`tools/perf_budget.py` writes a `historical` block whose prose claims the recorded
FAIL is preserved verbatim:

```
# line ~32-33 (comment):
#   The historical 343,547 > 20,000 FAIL is preserved verbatim and is still emitted
#   in the `historical` block.
# line ~244-248 (the block):
"historical": {
    "note": "measured and printed but non-voting; the recorded verdicts are preserved "
            "verbatim and must never be rewritten",
    "rows": [{"metric": r["metric"], "value": r["value"], ...} for r in advisory],
```

But `r["value"]` is a **live re-measurement** — the row is built at line ~203 as
`rows.append(_row("context_bytes_per_artefact", worst, sizes=sizes))`, where `worst` is the
largest artefact measured **on this machine, right now**. Measured consequences:

| run | `historical.rows[context_bytes_per_artefact].value` |
|---|---|
| the committed artifact `.hgk/artifacts/s2/PERF_BUDGET.json` | **343547** |
| `python -B tools/perf_budget.py --check` (AO's run) | **366299** |
| `python -B tools/perf_budget.py --check` (my run) | **365351** |

So the "historical" record is **non-deterministic and host-dependent**, which contradicts both the
comment above and the owner adjudication `S2_HISTORICAL_FAIL: PRESERVE`
(`docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json`). An independent checker flagged this
(AO verdict D1 = BROKE).

## The recorded value exists — use it, do not invent it

`.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json` is a frozen, recorded artifact:

```json
{ "bytes_per_atom": 1449.57, "atoms": 237, "pi_bytes": 343547,
  "tolerance_pct": 10.0, "frozen_head": "7c5bc585c7d889cd338da853be4efc4b8f07d3b2" }
```

`pi_bytes = 343547` **is** the recorded historical value. Load it; never hard-code it as a literal
in your diff, and never recompute it.

## Required change (exactly this, nothing wider)

1. **Split recorded history from live measurement.** In the `historical` block:
   - `value` MUST become the **RECORDED** value when a recorded baseline supplies one for that
     metric (for `context_bytes_per_artefact` it is `pi_bytes` from
     `BYTES_PER_ATOM_BASELINE.json`).
   - Add `measured_now` carrying the live measurement that used to sit in `value`, so nothing is
     lost.
   - Add `origin` naming where the recorded value came from, e.g.
     `{"file": ".hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json", "field": "pi_bytes"}`.
   - Add `"recorded": true|false` per row.
   - If the baseline file is absent or has no field for that metric, keep `value` = the live
     measurement, set `recorded: false` and add a `note` saying no recorded value was available.
     **Do not fabricate a recorded value, and do not silently fall back without saying so.**
   - The row `verdict` for a recorded row must be computed from the RECORDED value against the
     unchanged budget, so `343547 > 20000` still reads `FAIL`. Budgets are NOT to be changed.
2. **Fix the two false comments** (the module header ~line 32-33 and the `historical.note` string) so
   they describe what the code now actually does.
3. **Do NOT change**: any threshold/budget, `voting_metrics` (must stay exactly `["bytes_per_atom"]`),
   the advisory set, `overall_verdict`, `--freeze-baseline`, or the `adjudication` block.
   Do NOT touch `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`.
4. **Add the regression test** to `tests/test_perf_budget.py` (append a new `unittest.TestCase`
   class; touch nothing existing):
   - assert that running the tool and parsing its output yields
     `historical.rows[<context_bytes_per_artefact>].value == <the value read from the baseline file>`
     (read the expectation FROM the baseline file at test time — do not hard-code 343547);
   - assert `verdict == "FAIL"` and `budget == 20000`;
   - assert the value is STABLE: it does not depend on the live measurement (assert `measured_now`
     is present and may differ, while `value` is the recorded one);
   - assert the module's own comment no longer claims verbatim preservation of a number the code
     does not emit — i.e. assert the source of `tools/perf_budget.py` contains no line claiming
     "343,547" is "preserved verbatim" while `value` is measured. Keep this as a targeted assertion
     on the two corrected strings, not a broad grep.
   Exit code 0 on pass, non-zero on failure, `unittest` style (the repo runs
   `python -B -m unittest discover -s tests`).

## Hard rules

- **Write-set**: `tools/perf_budget.py` and `tests/test_perf_budget.py` ONLY. Touching any other
  file is a scope violation. Do not `git add`, do not commit, do not push, do not create branches.
- Interpreter: use `python -B` (bare `python` on this host is the sanctioned interpreter for this
  repo; `PYTHONPATH=C:/Projects/Agent_Workspace/PIPD/src` and `PYTHONDONTWRITEBYTECODE=1`).
- Prove your own change runs: execute `python -B tools/perf_budget.py --check` and
  `python -B -m unittest tests.test_perf_budget -v` and paste the **raw** command output (exit
  codes included) into your final report. Truncation is fine; rewriting is not.
- **You may not report success without pasted raw evidence.** If something does not work, say exactly
  what did not work — a truthful BLOCKED is a good result, a fabricated PASS is not.

## Final report (required shape)

1. `git diff --stat` for your two files.
2. Raw output of `python -B tools/perf_budget.py --check` showing the `historical` block.
3. Raw output of the test run with the pass count.
4. Any file you touched and did NOT mention above (should be: none).
