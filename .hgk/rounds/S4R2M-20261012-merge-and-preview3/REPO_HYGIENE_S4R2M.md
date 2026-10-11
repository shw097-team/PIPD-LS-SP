# REPO_HYGIENE_S4R2M — default branch, branches and worktrees

**Round** `S4R2M-20261012-merge-and-preview3` · **date** 2026-10-12 (Asia/Taipei)
**Scope** owner instruction: bring `main` and its README fully up to the latest released state, and
tidy the repository's branch/worktree surface.

## 1. `main` — now the latest released line

| step | from | to |
|---|---|---|
| M3 integration (owner-approved fast-forward) | `4445db5a…` | `dfa52053…` |
| release + round record | `dfa52053…` | `18990da…` |
| round acceptance record (officer verdict, report, A15 logs) | `18990da…` | `f8c61aa…` |
| `.gitignore` hygiene (see §4) | `f8c61aa…` | **`82f4ae5…`** |

Every step was a fast-forward; no merge commit, no rewrite, no force.

`main`'s `README.md` now names `v0.1.1-preview.3` as the installable preview, links its release page,
marks `.1` and `.2` superseded, and carries the new wheel name and digest in the bash, PowerShell and
one-line install blocks. Verified by reading the file back out of `origin/main`, not from the working
copy.

## 2. Branches — before / after

**Remote, deleted** (both fully contained in `main`, short-lived by the project's own convention):

| branch | why safe |
|---|---|
| `release/s4r2m-preview3` | this round's release branch; the tag `v0.1.1-preview.3` keeps its commit reachable |
| `r7-del018-successor` | fully merged into `main` before this round |

**Remote, kept deliberately:**

| branch | why kept |
|---|---|
| `main` | default branch |
| `s4-r2-affected-only-20261011` | fully merged, but the 2026-10-11 acceptance report links to `tree/s4-r2-affected-only-20261011`; deleting it would 404 that reference |
| `r5-s4-evidence`, `r5-s4-readme` | **not** fully merged — each still holds a commit that `main` does not. Deleting them would drop content, so they are left in place for their round's owner |

**Local, deleted** (content already in `main`): `postrelease-narrow-repair-20261011`, `r3-candidate`,
`r5-s4-candidate`, `r5-s4-packreader`, `release/s4r2m-preview3`,
`s4r2m-merge-and-preview3-20261012`, `r5r-ce-repair`, `r6-main-readme`.

**Local, kept:** `main`, `master` (old pre-r3 lineage, not merged — left alone rather than judged),
`r5-s4-evidence`, `r5-s4-readme` (as above), `r5p-post-challenge-repair` (the primary checkout's
branch, see §5), `r5q-owner-opensource-preview` (its worktree holds uncommitted files), and
`s4-r2-affected-only-20261011`.

## 3. Worktrees — before / after

Removed after confirming each was clean **and** that its commit was reachable from a ref:
`worktrees/main-readme-wt`, `worktrees/r5r-repair-wt`, `worktrees/postrelease-candidate`,
`worktrees/r2-candidate`. Kept: `worktrees/s4r2m-merge-wt` (this round), `worktrees/r5q-release-wt`
(refused removal — it has uncommitted files, see §5), the primary checkout, `PIPD-postrelease-wt`.

`worktrees/main-readme-wt`'s branch `r6-main-readme` was reported as `<origin/main: behind 94>` before
removal — a stale checkout of the pre-repair README, which is exactly what this round supersedes.

## 4. What the `.gitignore` fix actually prevents

`main` had **no** rule excluding credential material or the in-repo `worktrees/` directory. The
credential file this project uses sits one level above the checkout, so a plain `git add -A` from the
repository root could have staged it into a **public** repository. That is an exposure path, not a
tidiness preference. The default branch now excludes `API KEY/`, `Fine-grained personal access
tokens*.txt`, `*.credentials.json`, `worktrees/`, `_handover/`, `_control/` and `CHECKPOINT_*.md`.
Verified: `git show origin/main:.gitignore` carries the rule, and no credential path is tracked or
staged.

## 5. Left alone, deliberately — and why

These are **not** oversights. Each would have required a judgement about someone else's unfinished
work, which this round is not entitled to make:

- **Primary checkout is on `r5p-post-challenge-repair`, not `main`, and is dirty.** Uncommitted:
  `.gitignore` (its content is now on `main`, but the local file still differs from its own branch),
  `PUBLICATION_PROJECTION_EQUIVALENCE.json` (+7 lines recording a `second_evidence_commit` binding),
  and a large set of untracked round scratch (`R5`/`R5P`/`R5Q` `ao/out/**`, lane logs, a 345 KB
  `tqaep_design_tmp/`, a knowledge `.db`, an `opencodex-config` backup). All dated 2026-10-10 or
  earlier — none created by this round. Committing another round's evidence under this round's
  authorship, or discarding it, are both wrong; the owner should decide. Switching the primary to
  `main` was **not** done, because the switch would carry those files across branches.
- **`worktrees/r5q-release-wt`** holds a modified `TECHNOLOGY_ADMISSIONS.json` and an untracked
  `tqaep_design_tmp/`. Removal was refused by git and not forced.
- **`PIPD-postrelease-wt`** likewise refused removal for modified/untracked content; not forced.
- **Tracked-but-ignored files**: `.hgk/ao/ao_verdict.log` and
  `.hgk/rounds/R2-20261009-qualification/pause-model-switch-20261009/CHECKPOINT_FINAL.md` are tracked
  *and* matched by `.gitignore`. `git rm --cached` would tidy this, but both are historical evidence;
  left for the owner.
- **Four mode-160000 gitlink entries** under `.hgk/rounds/R2-20261009-qualification/**` are recorded
  as submodule commits with no `.gitmodules` companion. They are historical round records; removing
  them would edit sealed evidence, so they are reported, not touched.
- **Four ~5.9 MB entries** under the same R2 round (`semcheck`, `regression-candidate`,
  `pristine-candidate`, `execute/candidate`) are the largest tracked paths in the repository. Left
  in place — they are sealed round evidence.

## 6. Final state

| item | value |
|---|---|
| `main` | `82f4ae5c4ecea0f71a04ec557aa3dea82b0820ba` |
| `README.md` on `main` | points at `v0.1.1-preview.3`, wheel `pipd_ls_sp-0.1.1a3-py3-none-any.whl` |
| tag `v0.1.1-preview.3` | `e94cc7f9…` → peels to `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a` |
| release | published, prerelease, 5 assets, **anonymous readback verified, all digests match** |
| remote branches | `main`, `s4-r2-affected-only-20261011`, `r5-s4-evidence`, `r5-s4-readme` |
| local branches | `main`, `master`, `r5-s4-evidence`, `r5-s4-readme`, `r5p-post-challenge-repair`, `r5q-owner-opensource-preview`, `s4-r2-affected-only-20261011` |
| worktrees | primary, `s4r2m-merge-wt`, `r5q-release-wt`, `PIPD-postrelease-wt` |

Nothing in this pass touched a published asset, an existing tag, or the content of a sealed round.
