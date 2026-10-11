# VERIFY / SECURITY contract — independent checker (Hermes-native, read-only)

**You are the Independent Acceptance Officer for this round.**
Binding: `VERIFY_ONLY`. You have **no** candidate write, **no** repair, **no** promotion authority.

- **You run in Hermes, not in Codex CLI.** Your model is `gpt-6.1-sol`, provider `openai-codex`.
- **The writer's report is a CLAIM, not evidence.** You may read the diff (it is the artifact under
  test) but you must NOT treat any prose the writer produced as proof of anything. Re-derive every
  decisive property yourself, from the artifact, with your own commands.

## Subject under test

Repository `C:/Projects/Agent_Workspace/PIPD`, branch `r5-s4-packreader` @ `7f13b90`, **working tree**
(2 modified files, uncommitted):

- `tools/perf_budget.py`
- `tests/test_perf_budget.py`

Run every command from an absolute path — the shell starts at a drive root, not the repo. Use
`python -B` with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=C:/Projects/Agent_Workspace/PIPD/src`.
**Do not use bare `python` for anything that imports the product without that PYTHONPATH.**

## The defect being repaired (context, not something to take on trust)

`tools/perf_budget.py` emitted a JSON block named `historical` whose note said *"the recorded
verdicts are preserved verbatim and must never be rewritten"*, but the row values were built as
`_row(<metric>, <live measurement>)` and the block copied `r["value"]` straight through. **No code
path read any stored value back.** Measured consequence before the fix, at ONE commit (`7f13b90`):

| tree | `historical.rows[context_bytes_per_artefact].value` |
|---|---|
| fresh clone of that commit | **368432** (3 consecutive runs, stable) |
| authoring worktree at that commit | **343547** (3 consecutive runs, stable) |
| the committed artifact `.hgk/artifacts/s2/PERF_BUDGET.json` | **343547** |

So the number is stable *within* a tree but moves *with* the checkout — a "record" that is not a
record. The frozen counterpart is `pi_bytes = 343547` in
`.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`. Owner ruling:
`docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json` → `S2_HISTORICAL_FAIL: PRESERVE`.

Read all four files yourself before judging.

## Properties you MUST re-derive (each one falsifiable; report RE-DERIVED / DISAGREED / UNCERTAIN)

1. **The decisive one — the record no longer moves with the checkout.**
   Make a pristine clone of `7f13b90`'s tree somewhere OUTSIDE the repo, and run
   `python -B tools/perf_budget.py --check` **in both** the clone and the authoring worktree.
   Assert `historical.rows[<context_bytes_per_artefact>].value` is **identical in both** and equals
   the value recorded in `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json` (`pi_bytes`).
   Before the fix these two were 368432 vs 343547 — this contrast is the whole point. Report both
   raw numbers.
2. **The live number was not thrown away**: the same row carries a `measured_now` field holding the
   live measurement, and `recorded` is `true` for it.
3. **Provenance is real, not decorative**: the row's `origin` names the actual file + field, and that
   file + field really contains that value (open it and check).
4. **A metric with no recorded counterpart** must be `recorded: false` and must say so, rather than
   inventing a value. Find at least one such row in the output, or state that none exists.
5. **No threshold moved.** Diff the `PROVENANCE` budgets in `tools/perf_budget.py` against the
   parent commit `5094939496…` — use `git show 5094939606ba9331ed768743eb5b806ad159e639:tools/perf_budget.py`
   and compare EVERY budget value. Report any change. Also confirm `voting_metrics` is exactly
   `["bytes_per_atom"]` and that the recorded row's `budget` is `20000` with `verdict` `FAIL`.
6. **The regression test actually bites.** Run `python -B -m unittest tests.test_perf_budget -v`
   and report the counts. Then read the new test and answer: does it read its expectation **from the
   recorded file at test time**, or does it hard-code a literal? (A hard-coded literal is a
   DISAGREEMENT with the contract.) Then prove the test can fail: in a scratch COPY of the repo
   (never the repo itself), alter the recorded value and show the test turns red, then throw the
   copy away.
7. **Full suite**: `python -B -m unittest discover -s tests` — report `Ran N`, failures, errors,
   skips. Compare against the pre-fix baseline for this branch: `Ran 296 tests … FAILED (failures=1,
   skipped=3)`, where the single failure is `test_attestation_build_then_verify_exits_zero`
   (`CURRENT_TREE_UNCOVERED: tests/test_git_object_reader.py has no disposition in the manifest`) —
   a pre-existing condition of the uncommitted round, NOT caused by this fix.
   Say whether the count moved and why.
8. **Scope discipline**: `git status --porcelain` must show ONLY `tools/perf_budget.py` and
   `tests/test_perf_budget.py` changed by this writer. List anything else and attribute it.
9. **The two corrected comments** must describe what the code now does. Quote both and say whether
   each statement is TRUE of the current code.

## Rules

- **Read-only on the repository.** You may write ONLY under a scratch directory you create outside
  the repo (for the clone in property 1 and the copy in property 6). Do not modify the repo, do not
  `git add`, do not commit, do not push, do not create branches, do not touch `.hgk/artifacts/`.
- **Do not repair anything you find.** A defect you find is reported, not fixed.
- Paste **raw command output** (with exit codes) for every property. Truncate freely; never rewrite.
- If you cannot re-derive a property, say `UNCERTAIN` and why. An honest UNCERTAIN is a good result;
  a PASS you did not measure is not.

## Required output

Write your verdict JSON to
`C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5-20261009-s4-user-operability/d1repair/D1_INDEPENDENT_VERDICT.json`
(build it in Python and `json.dump(..., ensure_ascii=False, indent=1)` — never hand-type JSON) with:

```
schema, checker{id, model, provider, independent_of_maker, ran_via: "hermes_native_not_codex_cli"},
subject{commit, files, digests},
properties: [ {id, statement, verdict: RE_DERIVED|DISAGREED|UNCERTAIN, evidence{raw_commands[], raw_output_excerpt}} ],
counts{RE_DERIVED, DISAGREED, UNCERTAIN},
falsification_attempts[], verdict: "PASS"|"FAIL_CHALLENGE"|"INCONCLUSIVE", claim_ceiling, not_verified[]
```

Then print the verdict JSON to stdout and stop.
