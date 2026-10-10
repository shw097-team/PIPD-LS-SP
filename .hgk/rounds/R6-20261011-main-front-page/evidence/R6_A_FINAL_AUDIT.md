# R6-A — final gap/defect audit of the R5R-repaired tree (2026-10-11)

This is the on-disk backing for the R6-A audit. It records what was actually re-run, on which
interpreter, with what output, and what was deliberately **not** concluded.

## What was re-run

Worktree `C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt`, branch `r5r-ce-repair` @
`9667783` (unchanged by this audit).

Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (3.11.9, pip
present, `jsonschema` 4.26.0). This is the interpreter the R5R round itself used.

| # | check | command | result |
|---|---|---|---|
| A1 | full test suite | `python -B -m unittest discover -s tests -t .` | `Ran 321 tests in 115.807s` → **`OK (skipped=3)`**, exit 0, zero `FAIL`/`ERROR` |
| A2 | same suite, Hermes-venv interpreter | same | 321 tests, `OK (skipped=6)` — the 3 extra skips are `pip unavailable in test interpreter`, an artefact of that interpreter, not a product finding |
| A3 | trace-widening counterexample | `python -B .hgk/rounds/R5R-.../maker-e2e/trace_widening_probe.py` | `COUNTEREXAMPLE CLOSED AND CE-2 STILL GREEN: True` |
| A4 | real-install end-to-end | `python -B .hgk/rounds/R5R-.../maker-e2e/maker_e2e.py` | exit 0; real wheel built, installed into a fresh venv, full chain run from a cwd with no `schemas/` and no `--root`; `VERDICT=PASS checked=4 findings=[]`, `schema_source.mode = INSTALLED` |
| A5 | published artefact re-derivation | anonymous download of the release wheel, then local SHA-256 | `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60` — matches the published `SHA256SUMS` and the value recorded in the ledger |

A3's output in detail: with the happy-path bundle untouched (PI-PKG still carries
`_profile_meta`) the verdict is `PASS checked=4 findings=[]`; adding an undeclared `trace` to
PD-PKG / ECP / TQAEP alone (content hashes unchanged) yields `FAIL checked=4` with `SCHEMA`
findings naming `trace` for each of the three. The counterexample the independent checker
raised is therefore closed, and CE-2 remains green.

## What was NOT concluded — the point of this file

**The audit did not certify a zero-defect state, and it must not be cited as doing so.**

Re-running a suite shows the defects that suite covers are absent. The following are all still
open at the project level and were not touched by this audit:

- the published preview still carries the two known defects; the fix exists on this branch and
  **is not published**;
- the release-evidence gap in the publication manifest is still `FAIL` / `EVIDENCE_GAP`;
- the SPEC/DEL denominator is still `28 evidenced / 10 active gaps / 19 deferred`;
- no vulnerability or supply-chain scan has been performed;
- there is no release signature or build attestation;
- the deferred stages, host-native certification and the untested Windows path edges are still
  deferred and untested;
- the registry admission status of the plan and execute lanes remains unproven, and the
  launcher's own receipt states that its transported-model token does not prove backend weights.

**Net**: no open defect was found in the repaired code paths by either the maker or the
independent checker; "no gaps or defects at all" is nevertheless false at the project level.
Those two statements are not interchangeable, and the second one is why the repair was not
published to the default branch.

## A side effect of this audit, and its repair

Running A4 mutated tracked files in the R5R worktree. The diffs were inspected and are **not
semantic**:

- the end-to-end harness builds a throwaway scratch git repo whose commit embeds a timestamp,
  so its head changed (`79570a77…` → `90d7f5d7…`) and every derived value moved with it —
  `content_hash`, `currentness_epoch`, `subject_id` (`PD-87a73906455c03d0` →
  `PD-4d66fe380d7afdce`, `ECP-f919637c887d143d` → `ECP-55acaf010954dbd1`), the idempotency key
  and the `currentness_epoch` bindings;
- the design chain rebound `candidate_head` in `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json`
  to the current HEAD `9667783`;
- `.hgk/artifacts/tqaep_design_tmp/ecp.json` is a scratch artefact;
- the transcript's uv timing lines differ.

The CE-1/CE-2 verdicts did not change. Because R5R is closed and its checker receipts bind to
that tree, the six affected paths were **restored** (`git restore`) rather than committed:
refreshing a frozen round's evidence with timestamp-dependent churn would have broken the
freeze for no informational gain. The worktree is clean and the executed commit is unchanged.
The re-run is reproducible at any time with the commands in the table above.
