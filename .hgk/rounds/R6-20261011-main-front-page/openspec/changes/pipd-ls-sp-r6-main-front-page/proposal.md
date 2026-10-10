# Change: rewrite the PIPD-LS-SP front page as current state

- **Change id:** `pipd-ls-sp-r6-main-front-page`
- **Round:** `R6-20261011-main-front-page`
- **Study:** `FAR-PIPD-R6-MAIN-FRONT-PAGE-001`
- **Round type:** `DOCUMENTATION_REPAIR` (front page only)
- **Subject:** `https://github.com/shw097-team/PIPD-LS-SP` default branch `main`,
  `de3a1d9e3a6298fa0dd29fafbf11d850e30c743a` → `12df0554b89f684ffd7941ee76a5d4225713d90e`

## Why

The default branch's front page was an append-only log: an R3 body with a fourteen-line
R5Q banner bolted to the top. It contradicted itself in two places that a first-time
visitor would read as the project's own claims — a `(review candidate)` title directly
above an announcement that a licensed preview exists, and a `No license is granted`
section on a repository that had been granted `Apache-2.0`. It ended on a `## 8.` fragment
with no sections 1–7, containing raw round narration. Ten defects are enumerated with
evidence pointers in the FAR study at `../../far/FAR-PIPD-R6-MAIN-FRONT-PAGE-001.md`.

A default clone of this repository therefore hands the reader the old version, which is
the outcome the earlier front-page pointer was added to prevent. A pointer was not enough;
the page needed to become a state page.

## What changes

| artefact | change |
|---|---|
| `README.md` | rewritten as a current-state page: what the project is, where to get it (the preview tag, explicitly not this branch), a map of the tree as it actually is, corrected claim ceilings, and the published preview's known limitations |
| `docs/FRONT_PAGE_HISTORY.md` | **new**. Holds the sections removed from the front page *verbatim* — the R3 audit-repair status table, the R3 licence paragraph, and the trailing fragment — each with a supersession note |
| everything else | untouched. No source, schema, packaging, `dist/` or tag change |

## What this change does not do

- It does **not** move the repository onto the release line, and does not touch the
  published tag.
- It does **not** publish the R5R defect repair. That repair exists on a separate branch,
  is unpublished, and the new front page says so in its own words.
- It does **not** upgrade any claim. `PARTIAL_CHALLENGE`, the open release-evidence gap,
  the unperformed vulnerability scan, the absent release signature, and the deferred
  stages all remain exactly as they were — they are now *on the front page* instead of
  only in a release note.

## Acceptance

`../workorder/r6_readme_acceptance.py` checks seven criteria mechanically and reports
14 individual checks. Result at the time of this change: **14/14 PASS, exit 0**
(recorded in `../evidence/acceptance_run.txt`).

**Ceiling on that acceptance, stated plainly:** the checker was authored by the same
orchestrator that wrote the page it checks. It is a maker self-check, **not** independent
verification. No `INDEPENDENT_PASS` is claimed for this round.
