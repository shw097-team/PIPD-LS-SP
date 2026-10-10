# Tasks — `pipd-ls-sp-r6-main-front-page`

All tasks are complete. Verification column states what actually backs each one.

| # | task | state | what backs it |
|---|---|---|---|
| 1 | Establish the true remote `main` README (the local `origin/main` ref was stale at `3aebbbc`) | done | `git fetch origin main` → `3aebbbc..de3a1d9`; the pre-fetch text is preserved as `../evidence/original_readme.md` |
| 2 | Map `main`'s real tree (600 files, 20 top-level entries) | done | `git ls-tree -r --name-only origin/main`; skill list from `origin/main:skills`, 13 CLI verbs from `origin/main:src/pipd_ls_sp/cli.py` |
| 3 | Diagnose the front page against that tree | done | 10 defects, each with a line-level evidence pointer, in `../far/FAR-PIPD-R6-MAIN-FRONT-PAGE-001.md` |
| 4 | Compare repair options and choose one | done | same study, §4: option A (banner-only) and B (transplant the 193-line branch README) rejected; option C (rewrite as a state page) selected |
| 5 | Establish what the release page actually offers, from the live page | done | anonymous read of the release asset list → wheel, `SHA256SUMS`, notes, source archive; the published wheel was downloaded and its digest re-derived this session, matching the published `SHA256SUMS` |
| 6 | Distil the open-item ledger so the page states only what is still true | done | `R5Q_NOT_VERIFIED_LEDGER.md` read in full; `DEL-018` still `FAIL/EVIDENCE_GAP`, denominators still `28/10/19`, both preview defects still open, neither fix published |
| 7 | Rewrite `README.md` | done | 188 lines changed on the branch |
| 8 | Preserve the displaced history verbatim rather than deleting it | done | new `docs/FRONT_PAGE_HISTORY.md`; front page links to it |
| 9 | Mechanical acceptance of the rewrite | done | `r6_readme_acceptance.py` → 14/14 PASS, exit 0 (`../evidence/acceptance_run.txt`) |
| 10 | Publish to the default branch | done | fast-forward `de3a1d9..12df055` over HTTPS; token supplied only via child-process environment and a `GIT_ASKPASS` shim |
| 11 | Read the live surface back | done | anonymous `raw.githubusercontent.com` fetch of `main/README.md`, byte-identical to the local file; anonymous `ls-remote` confirms `main = 12df055` and the tag unchanged |

## Not done, and said so on the page

- No independent verification of the rewrite. Criterion 9's checker is the maker's own;
  that is recorded in `../surface/GSTACK_R6_ROUTE_READBACK.json` and in the proposal.
- The sealed EXECUTE lane was not used for the writer work in this round, so there is no
  launcher receipt. Also recorded in the readback.
- The rendered appearance of the page on GitHub was not inspected.

## Ledger effects

None of the following were closed, reduced or re-labelled by this round: the open
release-evidence gap, the `PARTIAL_CHALLENGE` denominator, the deferred stages, the
absent vulnerability scan, the absent release signature, or the two open preview defects.
This round changed a page, and moved some history into a file, and nothing else.
