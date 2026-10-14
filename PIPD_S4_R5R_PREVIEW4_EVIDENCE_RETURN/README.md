# PIPD-LS-SP — S4 R5R evidence return (`v0.1.1-preview.4` + the verdict follow-up)

**Round** `R5R-20261014-s4-preview4-focused-close` · **subject frozen at**
`f4021aeff9c016cfb14f17e68a0c570ed4e825c5` · **evidence branch built on** `main`
`dba4b19456777d3b597fdf71480f6423dd974243`

This directory is the round's return pack for an external acceptance officer. It is **not** an
acceptance: it is the raw material a checker needs, plus an explicit list of what was not done and of
what was found wrong with the first attempt.

## Read this first: three things the first version of this pack got wrong

1. **The release shipped without its `SHA256SUMS` asset.** The generator builds the checksum list over
   every asset *except the list itself*, and the upload loop then used that same list. The release notes
   and the README tell the reader to fetch `SHA256SUMS`; that request returned 404, so the documented
   verify route was broken for this tag. Found by this round's own served-byte readback and independently
   re-found by the wheel clean-install lane. Fixed by attaching the file to the existing release.
   → `00_round/release_corrections.json`
2. **That file was then written with CRLF endings**, so `sha256sum -c` folded a `\r` into every file name
   and reported all six entries unreadable. Re-emitted with LF (the script refuses on any digest drift),
   the asset replaced, the readback re-run, and the documented reader command confirmed. → same file.
3. **The CI story was one-sided.** The pack shipped the failing gate log but not the green one, and left
   out an intermediate red full-suite run. Both green logs, the failing log and the intermediate red are
   now here. → `02_ci/`, `01_tests/`, `00_round/tests_and_negatives.json`

## The independent verdict, and what was done about it

An adversarial re-derivation in a separate read-only lane (different process and different checker than
the writer) confirmed the negation-surface widening, the ClaimCeiling typing and named findings, the
identity bump, and that the three repointed tests were not weakened. It returned three claims as
**PARTIAL** and found four defects. Full text: `05_check/VERDICT.md`.

| defect | what it was | disposition |
|---|---|---|
| D1b | same-polarity obligations joined by a comma / `以及` / `and` **merged into one atom** (`不得A，不得B` → 1, was 2) — an obligation folded into another atom's text is invisible to `validate_atoms` | **fixed** on `main` (PR #13), pinned by four new tests |
| D2 | a period between two alphanumerics was never a boundary, so a sentence end typed without a space (`Do task A.Task B must run.`) stopped splitting | **fixed** on `main` |
| D1c | a prohibition whose object merely contains a modal word (`不得使用必須的憑證`) was refused as ambiguous | **fixed** on `main` |
| GATE | the `stage-c` write-set arm can be widened by self-declaration, and its trigger paths omitted `src/**`, `schemas/**`, `tests/**`, `fixtures/**`, `pyproject.toml`, `tools/build_dist.py`, so a source-only PR would not run the gate at all | trigger paths **fixed**; the widening cannot be removed by construction and is stated in the file as an open item |

The fixes are in PR #13, merged as `dba4b194`, with `ci` **614 tests OK (skipped=6)** and
`public-plugin-verify` reporting `WRITE_SET_CLEAN_AGAINST_f4021ae…` on that head. The released tag still
carries the pre-fix behaviour: **a release note must not claim `v0.1.1-preview.4` is free of D1b/D2.**

## What this round did

One focused semantic repair of the requirement compiler, one bounded claim-shape guard, one immutable
preview release, and then the corrections the independent verdict forced. Nothing else: no ninth skill,
no MCP, no Apps, no Hooks, no `.hgk/` migration, no history rewrite, no re-pointing of an older tag.

| item | where the evidence is |
|---|---|
| frozen subject, live remote, environment, tool drift | `00_round/R5R_FREEZE.json` |
| contract + compiler receipts + admission note | `00_round/source_and_compiler.json` |
| original vs current main, the three merges, exact changed paths | `00_round/baseline_and_diff.json` |
| red-before / fixed / green, incl. the intermediate red | `01_tests/*`, `00_round/tests_and_negatives.json` |
| CI: the failure, the diagnosis, both green runs | `02_ci/` |
| tag, tree, wheel build input, local digests | `03_release/RELEASE_TUPLE_v0.1.1-preview.4.json` |
| served-byte readback of every asset | `03_release/asset_readback.json` |
| the two post-publication asset corrections | `00_round/release_corrections.json` |
| plugin ZIP structure, determinism, derivation map | `04_package/*.json` |
| the independent adversarial verdict and its probes | `05_check/` |
| the re-check brief dispatched for the fix | `06_verify2/` |
| the private-host smoke and why it is not a pass | `05_host/`, `00_round/private_host_smoke.json` |
| approvals, checker, rollback, open items | `00_round/approvals_checker_tt.json` |

## Verifiable claims (each with a raw artefact)

1. **The release exists and its bytes are what they claim.** `SHA256SUMS` in the release matches the
   locally built assets, and every asset was re-downloaded from its public URL and re-hashed:
   `03_release/asset_readback.json` → `all_served_bytes_match_sums: true`.
2. **The repair is real, and so is the first version's regression.** With the repairs stashed on the
   frozen subject, 13 of 18 focused cases fail. The first version then merged same-polarity obligations
   (`05_check/adv_old.json` vs `adv_new.json`: 2 atoms → 1); the follow-up restores one atom per segment
   and pins it. Full suite on the fixed head: 614 tests OK.
3. **The mainline gate is green on the current head.** `02_ci/`: `ci` 614 OK; `public-plugin-verify`
   write-set clean with its own refusal self-tests firing; the earlier failure log is kept for comparison.
4. **The private plugin ZIP is structurally sound and reproducible.** 56 members, one plugin root, one
   manifest, exactly the eight existing skills, no MCP/Apps/Hooks, built twice from the tag with one
   digest. One honest limit: the eight `SKILL.md` members are **derived** (frontmatter reduced to
   `name`+`description`), so they cannot be cross-checked against the frozen ledger's source hashes — the
   other 40 members are byte-identical, and the derivation is declared in `SOURCE_TO_PLUGIN_MAPPING.json`.
5. **A red gate was diagnosed rather than hidden.** The first `public-plugin-verify` failure measured the
   range `Stage A tip...HEAD` (273 paths, of which this round wrote 24); that arm had no declaration for a
   source-repair round. The workflow was amended **in the same pull request** with a `stage-c` arm, and the
   amendment is itself subject to review — with its limit written into the file.

## What is NOT claimed

- **No private-host install was performed by this round.** Desktop input needed an interactive consent
  approval; the prompt timed out and the driver's rule is that silence is not consent, so the action was
  not retried. `05_host/` records the attempt, the refusal and what would close the item. This is **not**
  `NOT_SUPPORTED_FOR_ACCOUNT` — the account was never shown to be unentitled.
- **No four-host qualification, no public directory submission, no Developer Identity/KYC, no portal
  review, no `PRODUCTION`, no `S4_FULL_PASS`.** All remain `NOT_GRANTED` / `OUT_OF_SCOPE`.
- **The Codex EXECUTE lane produced no output this round.** It was attempted twice (a stale pinned binary
  path, then an idle child that made no file change in 20 minutes) and is recorded as blocked; the
  bounded write was performed in the orchestrator lane and the checks ran in distinct read-only lanes.
  Maker and checker are not the same process or model.
- **The follow-up fix is in no release.** Publishing a further preview needs a fresh owner authorization.
- **An OpenAI documentation revision may have moved the plugin manifest convention.** The drift, its check
  time and its URLs are recorded as an open item; it is not resolved by assertion here.

## How to check the release yourself

```bash
BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.4
curl -fsSLO "$BASE/SHA256SUMS"
curl -fsSLO "$BASE/pipd_ls_sp-0.1.1a4-py3-none-any.whl"
grep '  pipd_ls_sp-0.1.1a4-py3-none-any.whl$' SHA256SUMS | sha256sum -c -
```

Rollback: the previous preview (`v0.1.1-preview.3`) is untouched and still downloadable; the tag
`v0.1.1-preview.4` is immutable and will not be re-pointed. A defect is corrected by a new preview,
never by rewriting this one.
