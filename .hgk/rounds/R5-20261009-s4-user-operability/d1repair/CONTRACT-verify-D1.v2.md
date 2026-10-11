# VERIFY / SECURITY contract v2 — independent checker (Hermes-native, read-only)

**Role.** Independent Acceptance Officer. Binding: `VERIFY_ONLY`, read-only against the product repo.
**You are not the maker.** You may not repair, improve, reformat, or commit anything. Report only.

**Contract v2 supersedes v1.** v1 contained two specifications that were *the contract author's defect, not
the candidate's*, and one unspecified attribution prerequisite. Those are corrected below and the corrections
are themselves on the record:

- v1-P1 asked for a *literal* pristine clone of `7f13b90` to show the recorded value. Impossible by
  construction: the candidate is **uncommitted**, so a literal clone carries the **pre-fix** tool and must
  disagree. v1-P1 was wrong. v2-P1 states the test in its achievable form (overlay).
- v1-P7 asked you to compare suite counts against a **stale baseline the author wrote from memory** and to
  reproduce a failure cause (`CURRENT_TREE_UNCOVERED`) that v1 mis-described. v1-P7 was wrong. v2-P7 states
  the test in terms of the parent commit and of your own observation.
- v1-P8 required attributing other dirty paths without giving you a pre-run snapshot. v2-P8 supplies it.

---

## 0. Environment facts you must accept as given (verify them, but do not "fix" them)

- Repo: `C:/Projects/Agent_Workspace/PIPD`. Branch `r5-s4-packreader`, HEAD `7f13b90dc06354a0c6b7bd013f83a8cc244bf93d`.
- **The candidate is uncommitted**: the working tree carries the fix. `git status` legitimately shows
  `M tools/perf_budget.py` and `M tests/test_perf_budget.py`.
- Subject under test, pinned by digest (recompute these yourself and refuse if they differ):
  - `tools/perf_budget.py` sha256 `f90c3d8d6061f55b9807c2e8740998f98124b56fbcb5c42397f459c4368ff015` (16180 B)
  - `tests/test_perf_budget.py` sha256 `6c0d21fa8ce6c0a047539d2333973b88a75eea68c82ce031a96381749791d270` (9422 B)
- Writer window was `08:06:04Z`–`08:08:37Z` (the writer only ever touched those two files).
- **The product's own test suite writes into the repo when run in place.** This is a property of the repo,
  not of the candidate. Therefore: **never run the suite in place.** Copy the tree to your scratch dir first.
- Your scratch dir: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/d1repair/independent-checker-v2`
  Create it if absent. **Every write you make goes there or to the verdict path in §3. Nothing else.**

## 1. What you must NOT accept

You must not accept, as evidence, any of: the writer's own report; the maker's claim that a property holds;
any pre-existing `*.json` verdict file; this contract's own assertions. Re-derive from `/C:/Projects/Agent_Workspace/PIPD` (the live tree) or from a copy you make yourself.

## 2. Properties to falsify (9). For each, report `RE_DERIVED`, `DISAGREED` or `UNCERTAIN` + the commands.

**P1 — the recorded value does not move with the checkout (the decisive test of the fix).**
1. Pristine clone: `git clone --no-hardlinks --no-checkout <repo> <scratch>/p1-clone`, then
   `git -C <scratch>/p1-clone checkout --detach 7f13b90dc06354a0c6b7bd013f83a8cc244bf93d`.
   Run `python -B <clone>/tools/perf_budget.py --check`. **Expect the PRE-fix behaviour here** (a bare number,
   no `recorded`/`origin` keys, and `source_of_truth: "UNPROVENANCED"`). This is your control, not a failure.
2. **Overlay**: copy the *working-tree* `tools/perf_budget.py` and `tests/test_perf_budget.py` into the clone
   (overwriting), then run `--check` again **from inside the clone**.
3. Assert: (a) with the overlay, `historical.rows[context_bytes_per_artefact].value` equals the `pi_bytes` in
   `.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json`; (b) the clone's own `measured_now` for that row is
   **different from** `value` if the clone's live measurement differs (report both numbers); (c) the clone and
   the authoring worktree print the **same** `value` while their `measured_now` may differ.
   **This property is the whole point of the fix: the record must be invariant to the checkout.**

**P2 — the live measurement is not discarded.** `measured_now` present on the recorded row, and it equals a
value you recompute independently from the tool's own live path. `DISAGREE` if `measured_now` is missing.

**P3 — the provenance is real.** `origin.file` + `origin.field` actually contain the value: open the named
file, read the named field, and confirm it equals `value`. A provenance label that points at the wrong field
is a `DISAGREE`.

**P4 — no fabricated records.** At least one row with no recorded counterpart has `recorded: false` **and** an
explicit note saying the value is a live measurement, not a recorded one. A row that silently presents a live
number as a record is a `DISAGREE`.

**P5 — the candidate changed no threshold.** Against parent commit `5094939`: every `budgets[*]` value in the
`PROVENANCE`/historical section is byte-identical; `voting_metrics` is exactly `["bytes_per_atom"]`; the
recorded row's `budget` is `20000` and its `verdict` is `FAIL`. Report the diff you used.

**P6 — the regression test genuinely bites.** Run `python -B -m unittest tests.test_perf_budget -v`.
Then, **in a scratch copy only**, perturb the recorded value in `BYTES_PER_ATOM_BASELINE.json` so it no longer
matches the live measurement, and show the suite goes **red**. Confirm the test reads its expectation from the
recorded file rather than hardcoding a literal (show the line). Discard the copy. Never touch the repo's copy.

**P7 — suite delta versus the parent, run in a COPY.** (corrected)
Copy the working tree to `<scratch>/p7-copy` (exclude `.git`, `__pycache__`, `*.pyc`). Run
`python -B -m unittest discover -s tests` **in the copy**. Report exact counts (ran / failures / errors /
skipped) and the names of any failures or errors with their cause.
Then compare test **names** in `tests/test_perf_budget.py` between `5094939` and the working tree:
the change must be **purely additive — 4 added, 0 removed** (v2 expects exactly:
`test_historical_value_is_stable_across_live_measurements`,
`test_historical_value_is_the_recorded_baseline_not_the_measurement`,
`test_no_source_comment_claims_verbatim_preservation_of_the_live_value`,
`test_unrecorded_advisory_metric_says_so_instead_of_fabricating`).
Do **not** compare against any baseline number quoted by the maker: **re-derive the parent side yourself** and
report what you find. Pre-existing failures/errors elsewhere in the suite are expected and must be reported as
pre-existing, with the cause, not attributed to this candidate.

**P8 — write scope, with the snapshot supplied.** (corrected)
Pre-run snapshot, supplied by the maker for your use: at the checker's own start, `git status --porcelain`
already listed ` M .hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` as modified — i.e. it was dirty **before** this
round touched anything. Mechanical corroboration available to you: its content is byte-identical before and
after your run (compare hashes), so **a run that rewrites it writes identical bytes**. The writer window
(`08:06:04Z`–`08:08:37Z`) preceded the first checker start, and the writer's only tracked changes were the two
subject files.
Therefore: `RE_DERIVE` this by listing every non-`.hgk/` tracked path that differs from HEAD and confirming it
is a subset of {`tools/perf_budget.py`, `tests/test_perf_budget.py`}. If any *other* non-`.hgk/` path differs,
that is a `DISAGREE` and you must name it. Paths under `.hgk/` and `openspec/` are round evidence, not product;
list them for the record but do not fail the candidate on them.

**P9 — the two corrected comments describe the code.** Quote the in-source comment(s) that were changed and
judge, against the current code, whether each statement is now true. A comment claiming "preserved verbatim"
about a live measurement is a `DISAGREE`. Note: `source_of_truth: "UNPROVENANCED"` appears on rows; say whether
that is a pre-existing field or something the candidate introduced (check the parent commit).

## 3. Read-only discipline and your verdict

- Do not write, create, delete or chmod anything inside `C:/Projects/Agent_Workspace/PIPD`. If a command you
  were about to run would write there, run it against a copy instead. If you find that you have already
  written there, say so explicitly in your verdict — a disclosed violation is far less damaging than a hidden
  one.
- Write your verdict JSON to exactly:
  `C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5-20261009-s4-user-operability/d1repair/D1_INDEPENDENT_VERDICT_V2.json`
  (this single path under `.hgk/` is the one permitted repo-side write) and **print it in full to stdout**.
- Verdict shape: `{checker:{model,provider,ran_via,independent_of_maker}, subject:{commit,branch,digests},
  properties:[{id,statement,verdict,evidence:{raw_commands:[{command,cwd,exit_code}],raw_output_excerpt}}],
  falsification_attempts:[...], counts:{RE_DERIVED,DISAGREED,UNCERTAIN}, not_verified:[...], claim_ceiling,
  verdict}` where the top-level `verdict` is `ALL_PASS` only if `DISAGREED == 0` **and** `UNCERTAIN == 0`.
- State `claim_ceiling` that grants no promotion, release or external acceptance.
- **Then stop.** Do not attempt repairs.
