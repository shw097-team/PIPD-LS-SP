# FAR-PIPD-R9-DEL018MAIN-003 — DEL-018 on `main`, and why "regenerate" was never going to work

Round `R9-20261011-s4-gap-closure`, obligation `REQ-PIPD-R9-DEL018MAIN-003`.

## 1. The fact pattern

After R8 merged the repaired lineage into `main`, `tools/build_publication_manifest.py --check
--current` reported `paths_total 253, covered 252, uncovered 1`: `docs/FRONT_PAGE_HISTORY.md` had no
disposition. Regenerating with `--write` changed nothing (same 1039 entries), which looked like a
tool defect.

## 2. It was not a tool defect — I had misread the data flow

The entry set does **not** come from the worktree and not from the subject tree. `build_projection()`
iterates **`manifest.items()`** — the **evidence manifest** at `.hgk/artifacts/evidence_manifest.json`,
built by a *different* tool (`tools/build_evidence_manifest.py`), which seals itself against a
**candidate tuple** (repo commit sha, candidate tree sha, stage, policy) and whose `--verify`
**refuses a stale seal**.

Measured before the fix:

- evidence manifest paths: `1039`
- contains `FRONT_PAGE_HISTORY`: `[]` — it was never in the manifest at all
- seal candidate head: `96677835941240d331f9a107b094fcc4cfd89030`
- current head: `f541c3968d8b3fc1d2dfd71bab1b0d56894f05ce`
- `--verify` → **FAIL `REFUSED_STALE_OR_FOREIGN_MANIFEST`**

So there were **two** defects, and only one was about our file: the manifest's seal was **stale by
four rounds** (bound to the R5R execute commit `9667783`), and the manifest had never enumerated a
file that only ever existed on `main`'s line. `--write` was behaving correctly — it can only dispose
of paths the manifest knows about.

## 3. Options

| | option | assessment |
|---|---|---|
| **A** | **Re-seal the evidence manifest from the current tree, then rebuild the projection.** | Recommended and executed. Uses both tools as designed: the seal is *meant* to be rebound per candidate, and the projection tool's own comment says the candidate override exists so that "nothing product-side has to move". |
| B | Hand-add one entry to the projection JSON | Rejected — `--write` would erase it, making the state non-reproducible and the gate dishonest. |
| C | Leave `FAIL(1)` disclosed | Rejected once the owner authorised execution: this was fixable definitional staleness, not a real product risk. |
| D | Move `docs/FRONT_PAGE_HISTORY.md` out of `docs/` so it stops being a product path | Rejected — that is moving the goalposts. The file is legitimate; the manifest was stale. |
| E | Edit `PRODUCT_PREFIXES` or the validator | **Forbidden.** Validators are never edited to fit the tree. |

**Adjudication: A.**

## 4. Result

```
evidence_manifest --seal     -> entries 1085 (was 1039); seal bound to f541c39 / tree 1e11ae1a
evidence_manifest --verify   -> exit 0        (the four-round staleness is gone)
projection --write           -> 1085 entries
projection --check --current -> exit 0, verdict PASS, violations []
                                paths_total 253, covered 253, uncovered_count 0
   docs/FRONT_PAGE_HISTORY.md -> disposition NOT_PUBLISHED, covered: true
```

`NOT_PUBLISHED` is the **correct** disposition: the file is on `main` and deliberately absent from
the published subject, whose bytes are untouched.

## 5. Why this is sanctioned rather than a weakening

The projection's own scope statement says it "covers the published subject commit/tree only; it does
NOT assert coverage of the current worktree". Re-sealing did not loosen the gate — it made the
**evidence base** current so the existing gate could give a truthful answer. The published tag's own
attestation is a separate artefact and was not touched.

## 6. Disclosed side effects

`.hgk/artifacts/evidence_manifest.json` (now 1085 entries), `.hgk/artifacts/evidence_manifest.seal.json`
(rebound to `f541c39` / tree `1e11ae1a`), and `.hgk/ao/pub/PUBLICATION_PROJECTION_MANIFEST.json` were
**rewritten**. This is a release-evidence re-binding for the default branch. **No tag moved, no release
asset changed, no validator edited, no product path moved.**

**Claim ceiling:** `MAIN_DEL018_PASS_WITH_CURRENT_EVIDENCE_SEAL`. This is not `G_RELEASE_FULL_PASS`.
