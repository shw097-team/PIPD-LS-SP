# R7 independent acceptance — verdict, ceiling, and what the ceiling costs

## Provenance (read this before the verdict)

| | |
|---|---|
| Task | `deleg_cf1e8980` / `sa-0-6920edcf`, completed 2026-10-11 09:10:04, duration 280 s |
| Isolation | separate Hermes context — the checker never saw the maker's reasoning |
| **Model / provider** | **`deepseek-v4.1-flash` / `opencode-go`** |
| Intended model | `gpt-6.1-sol` (medium) on the OpenAI OAuth route, via the CODEX CLI VERIFY lane |

**Caveat that matters more than the verdict: this is NOT cross-model verification.** The child
inherited the parent's model, which is the **same model family as the planner and the maker**. Every
other independence property holds — separate context, no access to the maker's conclusions, every
value re-executed from the published bytes — but common-mode error is **not** controlled for. A
checker that shares the maker's model can fail the same way the maker does and still agree. Treat a
PASS here as *independently re-derived*, **not** as *cross-model corroborated*.

The result message was not delivered to the parent; this record was recovered from the child's
transcript (`delegation/live/deleg_cf1e8980/task-0.log`), which preserves its full output.

## Verdict

**PASS** — in the checker's own words: *"Verified, from anonymously-read published bytes only, that
release v0.1.0-preview.2 of shw097-team/PIPD-LS-SP is internally consistent in the respects checked
and that the shipped wheel carries both claimed repairs."*

## Checks it re-derived itself

| # | Check | Observed |
|---|---|---|
| 1 | Anonymous ref resolution | `main` = `26beacb`; `refs/tags/v0.1.0-preview.2` = `8faa64e`; `refs/tags/v0.1.0-preview.1` = `cc9bf574` (unmoved) |
| 2 | Release metadata | `prerelease: True`, `draft: False`, `target_commitish: 8faa64e…`, `body_len 3491`, body contains `G_RELEASE_FULL_PASS` and `Known limitations` |
| 3 | Assets, downloaded anonymously | wheel `d6c3e295…` OK; `PREVIEW_NOTES_v0.1.0-preview.2.md` `31b68010…` OK; source zip `4d24d1ec…` OK; `SHA256SUMS` self-consistent (`verify` → all OK) |
| 4 | **CE-1 on the shipped bytes** | clean venv outside the repo; **cwd has no `schemas/`**, no `--root`; `pipd.exe validate --bundle bundle_ce1.json` → `checked: 4`, `findings: []`, `schema_source.mode = INSTALLED` |
| 5 | **trace-widening closed on the shipped bytes** | bundle with an undeclared top-level `trace` on PD-PKG / ECP / TQAEP → **EXIT=1**, findings name `trace` per contract (`Additional properties are not allowed ('trace' was unexpected)`); also confirmed `trace` is **not** in `NON_RECORD_SIDECARS` and **is** in `HASH_EXCLUDED_FIELDS` inside the installed package |
| 6 | Corroboration | the repo's own `test_ce_repair_regression.py` — 9 tests pass; `git status` clean afterwards (repo untouched) |

Checks 4 and 5 are the ones that matter: they were performed on the **downloaded release wheel**,
from a directory with no schema tree, which is exactly the condition under which the pre-repair build
failed. The defect is demonstrably absent from the published bytes.

## What the checker said it could NOT verify (its own ceiling, quoted)

- It did **not** prove the wheel was built from the source commit named in the release body.
- It did **not** audit the tag's tree or the source archive contents.
- It did **not** test the preview.1 wheel's contents (only that its ref did not move).

## Additional limits the maker adds (not in the checker's list)

- **Common-mode risk** — same model as the maker (see Provenance).
- **No external signature** was verified, because none exists on this release.
- The checker could not run the **full** suite: its venv had no `pytest`, so it ran the R5R
  regression module directly (9 tests) rather than the whole 321-test suite. The full suite result for
  this tree is not independently reproduced here.
- **Nothing about `main`** was verified beyond its ref hash; `main` and the release line diverged and
  DEL-018's closure exists only on the release line.

## Resulting claim ceiling for the round

`R7_LOCALLY_VERIFIED_AND_INDEPENDENTLY_RE_DERIVED_SAME_MODEL_CANDIDATE_PUBLISHED`.

Not claimed: cross-model corroboration, `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`,
`PRODUCTION_VERIFIED`.
