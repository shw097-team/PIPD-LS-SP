# BOUNDED WRITER BRIEF — WO-S4-CAL-003 / WO-S4-TQAEP-004 / WO-DOC-STATUS-005 (R5P round, EXECUTE lane)

You are the **bounded Codex writer** for three small Work Orders of the R5P post-challenge S4 focused
repair. Orchestrator: Hermes (PLAN). Control plane: HG-KSEOS. Model route: opencode-go/deepseek-v4.1-flash
through the sanctioned sealed EXECUTE front door. Claim ceiling of everything you produce:
**CANDIDATE / LOCAL_TESTED only**.

## Execution environment

> **Do NOT run `python3 -B -m unittest discover -s tests -t .`.** Inside this container that full suite
> takes ~25 minutes (Windows bind mount) and a previous lane was killed by its own timeout doing exactly
> that. The orchestrator runs the full suite on the host. Run ONLY the specific test modules you touch,
> and keep individual commands under ~3 minutes.

- You run INSIDE a disposable Linux container; the mount allowlist is the write-scope boundary.
- The product repo is mounted read-write at `/w` — your ONLY writable tree. There is **no git**.
- `python3` (with `jsonschema`), `pip` and `venv` are available. The package is NOT installed:
  export `PYTHONPATH=/w/src` for every python invocation and use cwd `/w`.
  CLI module entry point: `python3 -B -m pipd_ls_sp.cli <command>`.
- Use `python3` only. Do not attempt network access.

## Write scope (HARD)

Allowed to modify/create ONLY:
- `tools/perf_budget.py`
- `tests/test_perf_budget.py`
- `src/pipd_ls_sp/pipeline.py` (TQAEP only)
- `src/pipd_ls_sp/cli.py` (only if required for the TQAEP reporting or a `--check` exit code)
- `README.md` (first screen only — see WO-DOC)
- `tests/test_tqaep_design_positive.py` (new file, optional)

**`schemas/` must NOT change** (the 19-contract structure is frozen) and the packaged schema set must stay
exactly 19. `dist/`, `tools/build_dist.py`, `src/pipd_ls_sp/workspace.py`, `src/pipd_ls_sp/registry.py`
and `tests/test_wheel_distribution.py` belong to a DIFFERENT Work Order — do not touch them.

---

## WO-S4-CAL-003 — per-atom gate anti-dilution (`F-R5-04`, P1)

Current state: `tools/perf_budget.py` already carries per-row provenance, makes `PER_ATOM_BYTES(2000)`
(`bytes_per_atom`) the only voting row, demotes the absolute `context_bytes_per_artefact` row and the
three timing rows to ADVISORY, and preserves the historical `343547 > 20000` FAIL via a frozen baseline
file. **Keep all of that**: do not change any threshold, do not change which row votes, do not touch the
owner's ruling.

Add an **anti-dilution oracle**:

1. A **unique validated obligation denominator**: count distinct obligation atoms by canonical identity
   (e.g. the atom's `subject_id`, or its canonical JSON when the id is absent) and report BOTH
   `atoms` (raw) and `unique_obligations`, with an explicit `dedup_rule` string. The voting rate must be
   computed against the denominator you can defend; state which one you used and why in the row.
2. A **padding-invariance test**: given an over-budget payload, appending N duplicate/filler atoms must
   NOT bring `bytes_per_atom` (or whatever rate votes) at or below the budget. Implement it as a real
   assertion over the module's own computation, not a comment.
3. **Scale fixtures**: exercise 2, 237 and 801 unique obligations, and a single genuinely long clause
   (e.g. a syntactically valid multi-thousand-character clause), reporting per-scale numbers. A
   `p95`/`max` per-atom statistic is welcome in addition to the mean — if you add one, mark clearly
   whether it votes (it must NOT silently replace the owner's mean-based row).
4. **Separate the two quantities** the challenge calls out: serialized/disk bytes vs the bytes that would
   actually enter a model context. If the product cannot compute the second, say so explicitly and mark
   that row `UNPROVENANCED`/advisory rather than inventing a number.
5. Tests in `tests/test_perf_budget.py` covering: the unique-obligation computation, the padding
   invariance, the scales 2/237/801, and that the historical FAIL row is still present and unchanged.

Acceptance evidence to run and paste: `PYTHONPATH=/w/src python3 -B -m unittest tests.test_perf_budget -v`
and `PYTHONPATH=/w/src python3 -B tools/perf_budget.py --check` (report its exit code and the JSON verdict
block compactly). Do NOT run the whole `tests/` directory.

---

## WO-S4-TQAEP-004 — design-time TQAEP positive (`F-R5-05`, P1)

Current state: `pipeline.compile_tqaep()` refuses `maker == checker` (case/whitespace-insensitive) and an
empty or `SELF_ATTESTED` receipt, but it then emits
`acceptance = [{"case": "INDEPENDENT_CASE_PASS", ...}]` — i.e. a **receipt string is presented as if it
were independent verification**. UAT-03 therefore only ever exercises the refusal path.

Required change (keep it minimal and honest):

1. Introduce a design-time ceiling constant, e.g. `TQAEP_DESIGN_CEILING = "TQAEP_DESIGNED"`, and carry it
   in the TQAEP record's `acceptance` entries — **the record's key set must stay schema-conformant**
   (`schemas/TQAEP.schema.json` has `additionalProperties: false`; do not add a new top-level key and do
   NOT edit the schema).
2. The acceptance entry for a design-time candidate must NOT claim `INDEPENDENT_CASE_PASS`. Use a
   design-time status naming exactly what was established (a distinct checker identity was supplied and
   recorded), plus explicit fields such as `independent_acceptance: "NOT_GRANTED"` and
   `independent_proof_requires: "S5_LIVE_RUNTIME_CHECKER"`, and `claim_ceiling: TQAEP_DESIGN_CEILING`.
3. Keep the existing typed refusals (`TQ_SOD` for maker==checker / missing / SELF_ATTESTED, `TQ_TRACE` for
   missing trace, `TQ_ORACLE` for an oracleless test). Refusal codes and `exit != 0` must not change.
4. Add a test (new file is fine) proving: (a) a legal design-time call with `--maker A --checker B
   --checker-receipt <non-empty non-SELF_ATTESTED>` exits 0, the artifact carries
   `claim_ceiling == "TQAEP_DESIGNED"` and contains **no** `INDEPENDENT_CASE_PASS` anywhere;
   (b) the three negatives still exit non-zero with their typed codes; (c) no code path can turn a
   receipt string into an `INDEPENDENT_PASS` token (assert on the artifact contents).

Acceptance evidence to run and paste: the new test(s) plus a live CLI demonstration of the positive and of
one negative (`python3 -B -m pipd_ls_sp.cli compile-tqaep ...` with the real flags you discovered).

---

## WO-DOC-STATUS-005 — README first screen (`F-R5-07`, P2)

The README's opening still tells a reader that `S0` and `S1` are the only stages reached and that
`S2–S8 are not implemented` in a way that reads as the *current* product state, while later sections and
`ACCEPTANCE.md` describe the R5 S4 candidate. A reviewer who reads only the first screen is misled.

Required change — **the smallest possible edit, first screen only**:

1. Label that historical statement explicitly as the **historical R3 snapshot** (keep the original text as
   history — do not delete or rewrite historical receipts/numbering).
2. State which branch is current for review (`r5-s4-packreader`) and that `main` is still the R3 state.
3. Point at `ACCEPTANCE.md` as the current acceptance entry point and note the candidate ceiling
   (`S4 candidate, internal evaluation`, `LicenseRef-PIPD-Proprietary`, **no public-use grant**).
4. Do not touch the R3 audit-repair history section, the claim table's semantics, or any numbers.

Be precise about what is claimed vs not: do not upgrade any claim level.

---

## Output contract

Finish with a single fenced JSON block named `WO_CALTQAEPDOC_RECEIPT`:

```json
{"work_orders": ["WO-S4-CAL-003", "WO-S4-TQAEP-004", "WO-DOC-STATUS-005"],
 "files_changed": ["..."],
 "perf": {"check_exit": 0, "voting_row": "...", "denominator": "...", "padding_invariance_test": "PASS",
          "scales": {"2": 0, "237": 0, "801": 0}, "historical_fail_preserved": true},
 "tqaep": {"positive_exit": 0, "claim_ceiling": "TQAEP_DESIGNED", "independent_case_pass_present": false,
           "negatives": {"self_attested": 2, "maker_eq_checker": 2, "missing_receipt": 2}},
 "readme": {"first_screen_labels_historical": true, "names_current_branch": true, "license_position_stated": true},
 "targeted_test_modules": {"tests.test_perf_budget": "OK", "tqaep": "OK"},
 "not_done": ["anything you could not do, with the exact command and error"],
 "claim_ceiling": "CANDIDATE_ONLY"}
```

Never invent output; if something cannot be done, put the exact command and error in `not_done`.
