# PIPD-LS-SP GPT Plugin — R5Y evidence return

**Round** `R5Y-20261014-gpt-plugin-publication` · **Contract** `PIPD-S4-PUBLIC-PLUGIN-EXECUTION-CONTRACT-R1`
**Control plane** HG-KSEOS (admitting project `PIPD-LS-SP-20261008`) · **Orchestration plane** Hermes (this run)
**Desktop/screen-control layer** FDA (cua-driver) — used for every UI action recorded in `09_ui_fda/`

## Claim ceiling (read this first)
`A PORTAL_SUBMIT_READY` ≠ `B PUBLIC_PUBLISHED` ≠ `C PUBLIC_CONSUMER_VERIFIED`.
This pack claims **A = candidate-only, locally verified**. Nothing here is Portal approval, review approval or publication.
No cell reads PASS without a real command, exit code and raw log; anything unproven is `NOT_RUN`/`EVIDENCE_GAP` in `06_verification/NOT_RUN_REGISTER.json`.

## Frozen subject
- branch `feat/s4r5y-plugin-publication-20261014` @ `062d84ae3e951d02b2ba6bb732359b18799d2864` (draft PR #6 → `main` `224591431a164ab72a9423cd180e417e8a762403`)
- candidate ZIP `pipd-ls-sp-public-skills.zip` — 68,355 bytes, sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, built twice byte-identically (56 members, 8 skills, single root)

## What is proven here
| # | claim | evidence |
|---|---|---|
| 1 | deterministic packaging, 2× identical | `04_package/build/build-a|build-b`, `plugin_zip_sha256.txt` |
| 2 | manifest delta = listing metadata only | `02_implementation/MANIFEST_DIFF.json` (1 file, M) |
| 3 | 8 skill bodies unchanged vs Stage B | `git diff --stat 940a37d HEAD -- skills/` empty (checker check C) |
| 4 | local suite green | `03_tests/full_unittest.stdout.log` 589 passed / 20 skipped |
| 5 | hosted CI green on the frozen head | `03_tests/ci_run_ids_jobs_exit_counts.json` (ci + public-plugin-verify) |
| 6 | Portal-mirror negatives | `08_release/NEGATIVE_CASES.json` |
| 7 | no false publish claim in docs | `00_authority/DOC_LINK_AUDIT.json` |
| 8 | independent challenge | `05_challenge/` (checker lane, maker ≠ checker) |
| 9 | Portal identity gate captured live | `09_ui_fda/portal_identity_gate.png` + `FDA_UI_ACTION_LOG.json` |

## What is NOT done (owner / external)
`07_acceptance/OWNER_ACTION_REQUIRED.json`: identity verification (TS-13), draft upload (TS-14), submit (TS-15), OpenAI review (TS-16), publish + unrelated-user install (TS-17).
TS-13 is a **hard Portal precondition** — the Portal itself refused with “You need a verified developer identity before you can create or upload a plugin.”

## Verification recipe
1. `git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git refs/heads/feat/s4r5y-plugin-publication-20261014` → must equal the frozen head.
2. `sha256sum 04_package/build/build-*/pipd-ls-sp-public-skills.zip` → must equal the pinned hash.
3. Anonymous `GET /repos/shw097-team/PIPD-LS-SP/actions/runs?head_sha=<head>` → ci + public-plugin-verify = success.
