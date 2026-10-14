# Adversarial verification — R5R preview.4 focused repair

Subject (frozen): shw097-team/PIPD-LS-SP, `cc6c1930765160697e7e51d6e37735b9220a30db`
(merged from `5219dc7`), tree `7d277a0afaff28b6841836cea3a31ffd0b214d94`, tag `v0.1.1-preview.4`.
Baseline for diffs: `f4021aeff9c016cfb14f17e68a0c570ed4e825c5`.
Method: executed the code (probes in this dir) against the NEW tree and against the pre-change
tree extracted from `f4021ae` (`old_tree/`); ran the project's own suite; read raw CI log.

Note: during the session the shared worktree `r5r-wt` was advanced by a sibling task to
`f3a1254` (branch `r5r-evidence-return-20261014`, an evidence-only commit). The frozen subject
`cc6c193` is an ancestor and the tag still points to it; all checks here are pinned to explicit SHAs.

## Verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | D1 negation surface covers 不允許/不許可/請勿/'should not' | **CONFIRMED** |
| 2 | D1 scope splitting + refusal-by-type | **PARTIAL** (refusal CONFIRMED; "each segment keeps its own scope" REFUTED for same-polarity segments — new merge regression) |
| 3 | D2 token-internal period + real boundary | **PARTIAL** (tokens/spans/binding CONFIRMED; "a real sentence-final period still ends a clause" REFUTED for `X.Y` with no space) |
| 4 | ClaimCeiling schema typing + named findings, no regression | **CONFIRMED** |
| 5 | Version/identity bump + manifest | **CONFIRMED** |
| 6 | 3 tests repointed, not weakened | **CONFIRMED** (but README prose is now self-contradictory) |
| 7 | Workflow stage-c amendment; A/B unchanged | **PARTIAL** (A/B byte-identical CONFIRMED; amendment materially WIDENS; trigger-path gap) |

## Evidence (raw)

### 1 — CONFIRMED
`probe_req.py` / `new_req.json` vs `old_req.json`:
`系統不允許傳送個資。` OLD=MUST NEW=MUST NOT; same for 不許可/請勿/`should not`/`is not allowed to`.
Baseline `系統不得上傳遙測。` MUST NOT in both.

### 2 — PARTIAL
Refusal: `系統必須不得外洩個資。` → OLD 1 atom MUST NOT (guessed); NEW `IntakeInvalid: ambiguous
negation scope`. CONFIRMED.
Mixed comma clause: `系統必須記錄稽核日誌，不得外洩個資。` → OLD **already** 2 atoms MUST/MUST NOT, i.e.
it never collapsed; the new mixed-scope test would pass on OLD and does not pin the repair.
REGression (`probe_adv.py`): comma/以及/`and`-joined **all-negated** obligations now MERGE into one atom:
`系統不得交付遙測資料，不得上傳日誌。` → OLD 2 atoms, NEW **1** atom (statement keeps the comma);
`不得A，不得B，不得C。` → OLD 3, NEW 1; `The system must not log data, must not leak data.` → OLD 2, NEW 1.
This is a silent semantic collapse the module exists to prevent (validate_atoms cannot see a single
atom); no test pins it. Comments claim "today's single-scope behaviour is preserved" — that premise is
factually wrong; the pre-change behaviour was per-segment.

### 3 — PARTIAL
`probe_req.py`: `api.example.com`/`v1.2.3`/`1.25` stay one atom (OLD split 3/3/2); `系統必須記錄日誌.版本必須為 1.2。`
splits correctly. Span round-trip, `clause_id=clause-{start}-{end}`, `source_sha256==sha256(file)`,
stable `req_id` all verified on the D2 token fixture.
Counterexample: an ASCII period flanked by two ASCII alnum chars is treated as internal even when it is
sentence-final with no space: `Do task A.Task B must run.` → NEW **1** atom, OLD 2; `Rate is 5.Use 3.`
→ NEW 1, OLD 2. So "a real sentence-final period still ends a clause" only holds when the period is not
between ASCII alphanumerics.

### 4 — CONFIRMED
`probe_claim.py` / CLI `validate --bundle`:
OLD: `allowed_claims: null` → library `TypeError: 'NoneType' object is not iterable`; undeclared →
`ValueError: 'NOT_A_DECLARED_CLAIM' is not in list`; CLI emitted generic `INPUT_SHAPE_INVALID`, `checked`
absent, exit **2**.
NEW: schema types both lists (array/enum); library returns NAMED findings
(`ClaimCeiling: allowed_claims must be a list of declared claim names (got NoneType)`,
`… entries must be declared claim names (got dict)`, `… names the undeclared claim 'NOT_A_DECLARED_CLAIM'`);
CLI `checked=1`, verdict FAIL, exit **1**. Legal record PASS in both; `pipeline.claim_ceiling(...)` record
still validates with zero findings → no regression.

### 5 — CONFIRMED
`pyproject.toml` / `__init__.py` / `tools/build_dist.py` all `0.1.1a4`. Wheel sha256
`3b59a985…cc0c` == `dist/*.sha256` == `WHEEL_MANIFEST.sha256` == the wheel's real sha256.
`build_input_commit=4754d92…`; all 33 real wheel members hash-match the blobs at **both** `4754d92` and the
frozen subject tree (i.e. the shipped wheel contains the frozen source). `gate_misc` subject tree
`7d277a0afaff28b6841836cea3a31ffd0b214d94` matches the claim.

### 6 — CONFIRMED
`git diff --numstat f4021ae cc6c193` for the three files: 1/1, 3/3, 3/3; every removed line is a literal
substitution (version string / digest / URL) — two `self.assertIn(...)` lines were re-pointed, none dropped.
DEFECT (not in the 7 claims): the README prose the tests assert is self-contradictory —
`v0.1.1-preview.4` is said to "carry the known Trace false-PASS defect" **and** to "supersede it"; and the
"Superseded" row lists `v0.1.1-preview.4` while ending "Use `.4`". Both are the result of replacing
"published `v0.1.1-preview.3`" with "`v0.1.1-preview.4`". The character-presence tests do not catch it.

### 7 — PARTIAL
`sim_stage_c.sh cc6c193` → `WRITE_SET_CLEAN_AGAINST_f4021ae…`, exit 0 (self-tests refuse skills/,
packaging/, `src/other_package/**`, docs/USER_GUIDE.md, tools/build_public_plugin.py; allow the round's
plants). Stages A and B arms extracted from both revisions: **byte-identical**.
Adversarial: the stage-c ALLOWED set (`src/pipd_ls_sp/`, `schemas/`, `tests/`, `fixtures/`, `dist/`,
`pyproject.toml`, `tools/build_dist.py`, `README.md`, `docs/install/`, and the workflow file itself) covers
paths stage-b DENIES (`src/`, `schemas/`, `dist/`) and stage-a largely denies; its DENIED arm is only
`^(skills/|packaging/public-plugin/)`. A future branch can set `STAGE: stage-c` itself, so the arm can
rewrite the compiler, the ClaimCeiling schema, all tests/fixtures, and the workflow that gates it. YES, the
amendment lets a future round write what previous arms refused.
Trigger gap: `on.pull_request.paths` does not list `src/**`, `schemas/**`, `dist/**`, `pyproject.toml`,
`tools/build_dist.py`, `tests/**` (except two files) or `fixtures/**`; a stage-c-only PR would not run the
gate at all. This PR triggered only via the workflow file / README / docs it also touched.
Raw CI evidence (the round's own return pack, branch `r5r-evidence-return`):
`PIPD_S4_R5R_PREVIEW4_EVIDENCE_RETURN/02_ci/ci_public_plugin_verify_failure.log` is a run of PR #11 at
`3cf382b` (pre-amendment, `STAGE: stage-b`) that ended `WRITE_SET_VIOLATION (stage-b base
759b9f0d…)` / `##[error]Process completed with exit code 1`. The pack contains **only** this failing log;
the round's README asserts `public-plugin-verify` is `success` on `5219dc7` but ships no green log.

## Could NOT verify
- The claimed green `public-plugin-verify` run on `5219dc7` (no green log in the pack; GitHub repo is not
  reachable offline from this session).
- The private-host smoke / publication / four-host UAT (out of scope; README already disclaims them).

## Defects found (summary)
1. **D1b merge regression** (silent): same-polarity comma/以及/`and` obligations merge into one atom.
2. **D2 boundary gap**: ASCII `X.Y` (no space) is never a clause boundary, incl. real sentence ends.
3. **D1c over-refusal** (minor): a clean prohibition containing a non-modal positive word
   (`不得使用必須的憑證`, or `required`/`need to`) is refused as ambiguous.
4. **README self-contradiction** introduced by a bad find/replace (preview.4 asserts both that it carries
   and supersedes the Trace defect; preview.4 listed as superseded while told to "use .4").
5. **Workflow stage-c widening + trigger-path gap** (item 7).

## Files produced
`probe_req.py`, `probe_adv.py`, `probe_claim.py`, `check_misc.py`, `sim_stage_c.sh`,
`new_req.json`, `old_req.json`, `adv_new.json`, `adv_old.json`, `new_claim.json`, `old_claim.json`,
`check_misc.json`, `bundle_*.json`, `diff_requirements.txt`, plus extracted trees `old_tree/`, `new_tree/`,
`wheel_x/` and the `a_/b_old/new.txt` arm extracts.
