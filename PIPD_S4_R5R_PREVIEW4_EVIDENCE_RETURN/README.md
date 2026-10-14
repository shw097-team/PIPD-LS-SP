# PIPD-LS-SP — S4 R5R evidence return (`v0.1.1-preview.4`)

**Round** `R5R-20261014-s4-preview4-focused-close` · **subject frozen at**
`f4021aeff9c016cfb14f17e68a0c570ed4e825c5` · **evidence branch from** `main`
(`cc6c1930765160697e7e51d6e37735b9220a30db`)

This directory is the round's return pack for an external acceptance officer. It is **not** an
acceptance: it is the raw material a checker needs, plus an explicit list of what was not done.

## What this round did

One focused semantic repair of the requirement compiler, one bounded claim-shape guard, and one
immutable preview release. Nothing else: no ninth skill, no MCP, no Apps, no Hooks, no `.hgk/`
migration, no history rewrite, no re-pointing of an older tag.

| item | where the evidence is |
|---|---|
| frozen subject, live remote, environment, tool drift | `00_round/R5R_FREEZE.json` |
| contract + compiler receipts + admission note | `00_round/source_and_compiler.json` |
| original vs new main, branch, exact changed paths | `00_round/baseline_and_diff.json` |
| red-before / green-after / full suite / CI counts | `01_tests/*.raw`, `00_round/tests_and_negatives.json` |
| the red gate, its log, and the root cause | `02_ci/ci_public_plugin_verify_failure.log` |
| tag, tree, wheel build input, local digests | `03_release/RELEASE_TUPLE_v0.1.1-preview.4.json` |
| served-byte readback of every release asset | `03_release/asset_readback.json` |
| plugin ZIP structure, determinism, derivation map | `04_package/*.json` |
| the private-host smoke and why it is not a pass | `05_host/`, `00_round/private_host_smoke.json` |
| approvals, checker, rollback, deferred items | `00_round/approvals_checker_tt.json` |

## Verifiable claims (each with a raw artefact)

1. **The release exists and its bytes are what they claim.** `SHA256SUMS` in the release matches the
   locally built assets, and every asset was **re-downloaded from its public URL** and re-hashed:
   `03_release/asset_readback.json` → `all_served_bytes_match_sums: true`.
2. **The repair is real and not an always-green oracle.** With the repairs stashed on the frozen
   subject, 13 of 18 focused cases fail (`01_tests/focused_red_before.raw`); with the repairs in place
   the focused set is green and the full suite is 610 tests (`01_tests/*`).
3. **The mainline gate is green on the frozen candidate.** `ci` and `public-plugin-verify` both
   `success` on `5219dc7e4f9d96701326e864b694658e3601a3b3`; the raw counts are in
   `00_round/tests_and_negatives.json`.
4. **The private plugin ZIP is structurally sound and reproducible.** 56 members, one plugin root,
   one manifest, exactly the eight existing skills, no MCP/Apps/Hooks, built twice from the tag with
   one digest, and a declared derivation map for the eight `SKILL.md` files.
5. **A red gate was diagnosed rather than hidden.** The first run of `public-plugin-verify` failed on
   its write-set step. The log shows the governed range was `Stage A tip...HEAD` (273 paths, of which
   this round wrote 24), i.e. the arm had no declaration for a source-repair round. The workflow was
   amended **in the same pull request** to add a `stage-c` arm; that amendment is disclosed as an
   amendment and is itself subject to review.

## What is NOT claimed

- **No private-host install was performed by this round.** Desktop input needed an interactive consent
  approval; the prompt timed out and the driver's rule is that silence is not consent, so the action was
  not retried. `05_host/` records the attempt, the refusal and what would close the item. This is
  **not** `NOT_SUPPORTED_FOR_ACCOUNT` — the account was never shown to be unentitled.
- **No four-host qualification, no public directory submission, no Developer Identity/KYC, no portal
  review, no `PRODUCTION`, no `S4_FULL_PASS`.** All remain `NOT_GRANTED` / `OUT_OF_SCOPE`.
- **The Codex EXECUTE lane produced no output this round.** It was attempted twice (a stale pinned
  binary path, then an idle child that made no file change in 20 minutes) and is recorded as blocked;
  the bounded write was performed by the orchestrator, and the independent check runs in a distinct
  read-only lane. Maker and checker are not the same process.
- **An OpenAI documentation revision may have moved the plugin manifest convention.** The drift, its
  check time and its URLs are recorded as an open item; it is not resolved by assertion here.

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
