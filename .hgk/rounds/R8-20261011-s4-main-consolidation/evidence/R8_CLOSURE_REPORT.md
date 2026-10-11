# R8 CLOSURE REPORT — cross-model verification, main consolidation, repository hygiene

Round `R8-20261011-s4-main-consolidation`. Control plane HG-KSEOS; canonical Hermes as the governed
runtime/orchestration plane; HGK admission run first (5 obligations FROZEN, 0 errors).

## 1. What was asked, and what happened

| item | outcome |
|---|---|
| 1. close the cross-model gap: re-run the same anonymous checks on CODEX CLI's VERIFY lane (`gpt-6.1-sol` / OAuth) | **DONE** — `openai-codex/gpt-6.1-sol`, relay-confirmed. Guard held. See §3. |
| 2. merge `preview.2` into `main`, point the front page at it, add a copy-pasteable quickstart | **DONE** — honest merge commit `cd65692`; README re-derived, not patched; quickstart verified by the cross-model checker. See §4. |
| 3. research + execute repository hygiene (front page, README, branches) | **DONE, in part** — 6 branches retired losslessly; 2 retained because they carry history; PR surface now 0 open. See §5. |
| 4. any new gap → FAR → adjudicate → execute, until an S4-level MVP open-source release closes | **2 new gaps found and adjudicated** (§3.1, §6). The S4 MVP release itself is **not** closed — see §8. |

## 2. Delivery

- `main` advanced `26beacb` → **`07426ef`** by a **normal, non-force push**. The owner grant's
  prohibitions on `force-push` and on rewriting `main` were respected; the default branch was
  advanced by the merge the owner's own instruction asked for.
- Tags **unmoved**: `v0.1.0-preview.1` `cc9bf574`, `v0.1.0-preview.2` `8faa64e`.
- Final remote ref set: `main`, `r7-del018-successor`, `r5-s4-evidence`, `r5-s4-readme`, and the two tags.
- Credential: used only for the authorised push and the branch deletions, passed via a child-process
  environment variable + a `GIT_ASKPASS` shim in `$TMPDIR` (never in argv, a remote URL, `.git/config`
  or a log). Unset and the shim removed immediately afterwards. **Rotation still recommended.**

## 3. The cross-model gap — closed

`verify-codex/INDEPENDENT_ACCEPTANCE_R8_CROSSMODEL.md`. Headline: `ok: true`, `mode: forced_rank`,
`required_arm == served_arm == openai-codex/gpt-6.1-sol`, `usage_provider: openai-p6a1fe3`,
`usage_status: 200`, `reasoning_effort: medium` — a **different model family from PLAN and EXECUTE**,
which is what the R7 subagent receipt could not claim.

Its substantive verdict on the published bytes: refs pinned, release metadata correct, all four
assets independently hashed and matching, the downloaded wheel installed in a clean venv resolving
`mode: INSTALLED` from site-packages with a valid bundle accepted (`exit 0`, `findings: []`) and
undeclared-`trace` bundles for PD-PKG/ECP/TQAEP each **rejected** (`exit 1`, finding names `trace`),
and 9/9 local regression tests passing. **Its overall verdict is `FAIL`, solely because its strict
clean-worktree gate saw the untracked `R8-…` round directory that I created before launching it.**
That is my harness artifact, not a property of the release, and it is reported rather than smoothed.

### 3.1 New gap (found while doing it): `--require-arm` verifies but does not select

`far/FAR-PIPD-R8-DISPATCH-004.md`. The first attempt — with `--require-arm openai-codex/gpt-6.1-sol`
and no rank pin — ran on **rank 1, `opencode-go/deepseek-v4.1-flash`**, i.e. the maker's own model,
and returned `ok: false / ERR_REQUIRED_ARM_NOT_SERVED`. `--require-arm` only refuses when the named
arm is *absent* or *gate-refused*; it never makes it the arm that runs. Adjudicated **A**: pin the
rank (`--force-rank 4 --max-candidates 1`) — caller-side, no control-plane change. Patching the
dispatcher itself is recorded as **candidate option B**, deliberately not taken inside a PIPD round.

**A near-miss worth recording.** I first read the relay usage log, saw three in-window
`gpt-6.1-sol` rows, and concluded the arm *had* run and the dispatcher had mis-attributed it. The
receipt refuted that — those rows came from the earlier four-rank smoke run. Reporting the
mis-attribution would have published a **false exoneration of a real defect.**

## 4. `main` consolidation — and the front page

Merge base was `3aebbbc`; the lines had diverged, so this is an honest merge commit, not a
fast-forward. Exactly **one** conflict, `README.md` — resolved by **re-derivation**, not by picking a
side.

The decisive point is not the merge. It is that `main`'s front page asserted **five things the merge
makes false**: that this branch's wheel was an old R3 build; that Apache-2.0 did not apply here; that
`main` was not the distribution entry point; that installing from here was "the wrong thing to do";
and that the two defects were fixed only off-branch. A patched page would have left all five standing
on the page a visitor reads first. The rewritten page's quickstart was **executed line by line**, and **three of its commands were
wrong on the first draft** (`init` takes no `--root` after the subcommand, `intake` takes `--goal`
plus a `--source` locator that must *exist* and not `--intent`, and `validate` takes `--bundle`).
The page now shows only what was actually run, with the real flag shapes stated.

## 5. Repository hygiene

`far/FAR-PIPD-R8-HYGIENE-003.md`. Branches were judged by **reachability, not age**:

| branch | verdict |
|---|---|
| `r3-candidate`, `r4-candidate`, `r5-s4-candidate`, `r5-s4-packreader`, `r5p-post-challenge-repair`, `r5q-owner-opensource-preview` | **deleted** — each an ancestor of the new `main`, 0 unique commits, therefore lossless |
| `r5-s4-evidence`, `r5-s4-readme` | **kept** — each carries exactly **1 commit that survives nowhere else** |
| `r7-del018-successor` | **kept** — the release lineage, and named throughout the evidence |
| `v0.1.0-preview.1`, `v0.1.0-preview.2` | **untouched** — moving or deleting a published tag is forbidden |

An "obvious" cleanup deleting everything but `main` would have destroyed two commits. PR #1 (head
`r4-candidate`) auto-closed when its head branch was removed; **0 open PRs** remain.

**`docs/FRONT_PAGE_HISTORY.md` was checked, not assumed.** The credential receipt on
`r5-s4-evidence` names a local file carrying a live `providers.opencode-go.apiKey`; that path was
confirmed **never committed** on any ref, and a scan of history found no `apiKey`-style literal —
though only the first 60 revisions were scanned, so that is a bounded clean, not a proof of a clean
history.

## 6. New gap (found by the merge): DEL-018 re-opens on `main` by one path

After the merge the tree has **253** product paths and **252** are covered.
`docs/FRONT_PAGE_HISTORY.md` has no disposition in the release-evidence manifest, whose enumerated
subject predates it (it arrived with R6's front-page rewrite). `--check --current` therefore exits
`1` **on `main`**.

Regeneration does not fix it — `--write` re-emits the same 1039 entries, because the manifest is
built from git objects of the pinned publication subject, not from the worktree.

**Adjudication: disclose, do not paper over.** Extending the manifest's subject is a
**release-evidence** decision and does not belong in a merge/hygiene round, and the validator is not
to be edited to fit the tree. The README's limitation 4 was corrected accordingly: DEL-018 is
**closed for the published subject** (`252/252`) and **`FAIL` by exactly one path on this branch**.

## 7. Side effects of this round, disclosed

New merge commit on `main`; new round directory `.hgk/rounds/R8-20261011-s4-main-consolidation/`;
`main` advanced on the public remote; **6 branches deleted on the public remote** (lossless, and
irreversible only in the sense that the refs are gone — their commits remain reachable from `main`);
PR #1 closed as a consequence; a scratch tree under the Hermes cache holding the checker's venv,
downloaded assets and logs (outside the repo); git identity `Hermes Orchestrator
<hermes-orchestrator@local>` set in the clone; the credential handled once as described in §2.
No tag was created, moved or deleted.

## 8. Claim ceiling — what is still NOT claimed

`MAIN_ADVANCED_TO_THE_REPAIRED_LINEAGE_BY_MERGE_COMMIT` +
`PUBLISHED_PREVIEW2_INDEPENDENTLY_CROSS_MODEL_RE_DERIVED` +
`REPOSITORY_BRANCH_SET_REDUCED_WITHOUT_HISTORY_LOSS`.

**The S4-level MVP open-source release is NOT closed**, and this round does not argue it is. Still
open: no release signature and no builder attestation; no vulnerability scan of this project's own
source and no lock file; `PARTIAL_CHALLENGE` at `28 evidenced / 10 active gaps / 19 deferred`;
`G_RELEASE_FULL_PASS`, `FULL_S0_S4_INDEPENDENT_PASS`, `PRODUCTION_VERIFIED`, `S5_RUNTIME_READY` and
every host certification **not granted**; DEL-018 `FAIL(1)` on `main` as described in §6; and
`--require-arm` still verifies without selecting, unless the caller pins the rank (§3.1).
