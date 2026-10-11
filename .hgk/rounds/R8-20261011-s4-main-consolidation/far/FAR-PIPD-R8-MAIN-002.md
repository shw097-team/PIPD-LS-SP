# FAR-PIPD-R8-MAIN-002 — bring the repaired lineage to `main`, point the front page at it, add a quickstart

Round `R8-20261011-s4-main-consolidation`. Question: merge the `v0.1.0-preview.2` lineage into `main`,
update the front-page README to point at the successor preview, and ship a copy-pasteable quickstart.

## 1. Facts (measured this round)

| | |
|---|---|
| `main` | `26beacb` — R3-era disclosure line plus R6's rewrite of this page |
| release line | `r7-del018-successor` — `r5q` (owner grant + Apache-2.0 licence) ⊂ `r5r` (CE-1/CE-2 repair) ⊂ `r7` (DEL-018 closure, published `v0.1.0-preview.2`) |
| merge base | `3aebbbc` — the two lines **diverged**; a fast-forward is impossible |
| diverging content | 517 files; `main` uniquely holds the R6 README and `docs/FRONT_PAGE_HISTORY.md`; the release line holds the grant, the repair, the projection and `dist/` |
| README | `main` 9,572 bytes vs release line 18,060 bytes — materially different documents |

**The decisive fact is not the merge; it is that the front page becomes false the moment the merge
lands.** Every distinctive claim on `main`'s current README is a statement about `main` being the
*old* line:

- *"the wheel under `dist/` here is an old R3 build (`ba84115d…`), not the published one"* — false once
  `dist/` carries the repaired wheel (`d6c3e295…`).
- *"the Apache-2.0 grant does not apply to this branch … reads `decision: UNSET`"* — false once the
  grant file merges in.
- *"This branch (`main`) — the R3 snapshot … not the distribution entry point"* — false, and
  self-contradicting: the whole point of the merge is to make it the entry point.
- *"Installing from `main` is the wrong thing to do"* — false.
- The "Start here" pointer targets `v0.1.0-preview.1`, which ships the CE-1/CE-2 defects.

So this task is **not** "edit the README". It is "re-derive it from the merged tree". A patched README
would leave five falsehoods in place on the page a visitor reads first.

## 2. Options

| | Option | Assessment |
|---|---|---|
| **A** | **Merge the release line into `main` (honest merge commit); re-derive the README from the merged tree; add a verified quickstart.** | Recommended. Nothing is rewritten, the tagged commit stays where it is, and each README claim is re-checked against bytes rather than carried over. |
| B | Fast-forward `main` to the release line | **Impossible** — the lines diverged at `3aebbbc`. |
| C | Force `main` to the release tip | **Forbidden** by the owner grant (`overwrite main`, `force-push`) and destroys the R6 README history. |
| D | Rebase the release line onto `main`, then fast-forward | Rewrites the ancestry of the branch that carries the published tag; the tag would still point at an orphaned commit. Buys nothing over A and costs provenance. |
| E | Cherry-pick R6's README onto the release line, fast-forward `main` | The README is the *conflicting* artefact, so this is the merge with the conflict resolved blindly in one direction. Same result as A, less honest about it. |

**Adjudication: A.** It is the only option that is both permitted and truthful, and its cost is one
merge commit.

## 3. Execution plan

1. Merge the release line into `main` with a merge commit (no rebase, no force).
2. Resolve the README **by re-derivation**: take R6's structure (it was purpose-built as a front page)
   and re-check every factual claim against the merged tree — licence state, `dist/` wheel hash, DEL-018
   state, branch role, preview pointer.
3. Replace the `v0.1.0-preview.1` pointer with `v0.1.0-preview.2`, and say plainly why the successor
   exists (preview.1 ships the two defects).
4. **Add a quickstart that is actually verified**: run every command in it against a clean venv with the
   *downloaded* preview.2 wheel, from a cwd with no `schemas/`, and record the real output. A quickstart
   nobody ran is a liability, not documentation.
5. Re-run the DEL-018 check on the merged tree so the evidence surfaces still pass **after** the merge
   (`--check --current` exit 0). A merge that silently re-breaks the projection is the obvious failure
   mode here.
6. Push `main` as a normal (non-force) push. Never move the tags.

## 4. Claim ceiling

`MAIN_ADVANCED_TO_THE_REPAIRED_LINEAGE_BY_MERGE_COMMIT` — publishing capability inherited from the R5Q
grant, which is unchanged by this task. The merge does **not** grant `G_RELEASE_FULL_PASS`,
`PRODUCTION_VERIFIED`, `FULL_S0_S4_INDEPENDENT_PASS` or any host certification, and it does not make
`main` a signed or attested release.

## 5. Known limits to disclose on the page

- `main` will still not be the *published subject*: the immutably published bytes are the tag's, and a
  branch tip is a moving target. The page must say "take the tag, not the branch" even after the merge.
- The wheel is not on PyPI, so `pip install pipd-ls-sp` fails by design; the quickstart must install
  from the downloaded artefact.
