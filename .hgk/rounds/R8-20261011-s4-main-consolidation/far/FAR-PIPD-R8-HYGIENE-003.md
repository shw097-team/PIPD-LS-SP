# FAR-PIPD-R8-HYGIENE-003 — repository hygiene: front page, README, and the branch set

Round `R8-20261011-s4-main-consolidation`. Question: make the repository's default-branch content,
front page and branch set honest and clean.

## 1. The branch set, measured by reachability (not by age)

Deletion is only safe if it loses nothing, so every branch tip was tested for containment in `main` or
the release line, and for how many commits it holds that neither contains.

| remote branch | sha | in `main` | in release line | unique commits |
|---|---|---|---|---|
| `main` | `26beacb` | — | no | 0 |
| `r3-candidate` | `3aebbbc` | **YES** | YES | 0 |
| `r4-candidate` | `cd8a06e` | no | YES | 0 |
| `r5-s4-candidate` | `5094939` | no | YES | 0 |
| `r5-s4-packreader` | `0f06eec` | no | YES | 0 |
| `r5p-post-challenge-repair` | `2efc84e` | no | YES | 0 |
| `r5q-owner-opensource-preview` | `9bd33a1` | no | YES | 0 |
| `r7-del018-successor` | `024d358` | no | YES | 0 |
| **`r5-s4-evidence`** | `2ad1f16` | no | **no** | **1** |
| **`r5-s4-readme`** | `f418153` | no | **no** | **1** |

Tags: `v0.1.0-preview.1` (`cc9bf574`) and `v0.1.0-preview.2` (`8faa64e`) — both immutable, neither moves.

**The table is the finding.** Seven branches are fully contained in the release lineage and become
reachable from `main` the moment the merge lands; deleting them afterwards provably loses nothing. Two
branches are *not* — each carries exactly one commit that survives nowhere else:

- `2ad1f16` — *"r5: publication subject attestation + redacted credential receipt"*: adds
  `.hgk/credentials/CREDENTIAL_RECEIPT.json` and
  `.hgk/rounds/R5-20261009-s4-user-operability/PUBLICATION_SUBJECT_ATTESTATION_R5.json`.
- `f418153` — *"r5: rewrite the README for the S4 repair round"*: a README rewrite (217+/71−).

An "obvious" cleanup that deletes everything except `main` and the newest branch would silently destroy
both. That is the failure mode this study exists to prevent.

## 2. Options

| | Option | Assessment |
|---|---|---|
| **A** | **Merge the release line into `main`; then delete exactly the seven 0-unique, contained branches; keep the two that carry unique history and document why; keep both tags.** | Recommended. Every deletion is provably lossless, and the two exceptions are exceptions *for a stated reason* rather than by oversight. |
| B | Delete every branch except `main` | **Destroys two commits.** Rejected. |
| C | Delete nothing | Leaves seven branches whose only purpose was to be consumed by the release lineage. The repository still reads as an archaeology site. |
| D | Adopt the two unique commits into `main` first, then delete all nine | Attractive in principle and strictly better hygiene, but it imports an R5-era README (`f418153`) that would immediately be superseded by this round's re-derived README, and a credential receipt whose home is a governance ledger rather than the default branch. **Deferred, with the reason recorded** — it is a decision about where round evidence belongs, not a hygiene chore. |

**Adjudication: A.** Lossless deletions proceed; the two history-carrying branches are kept and named.

## 3. Reversibility — stated plainly

- Deleting a **fully contained** branch is reversible: its commits stay reachable through `main`, so
  the ref can be recreated at the same sha indefinitely.
- Deleting a **history-carrying** branch is **not** reversible in practice: once unreachable and
  garbage-collected, that commit is gone from the remote. This is exactly why they are not in scope.
- Tags are never touched. The grant forbids moving or deleting an existing tag, and both tags are
  permanent release identities.

## 4. Front page and README

Handled together with the merge study (`FAR-PIPD-R8-MAIN-002`), because the two are the same problem:
after the lineage lands on `main`, the front page's distinctive claims become false. The hygiene angle
adds one rule — **the page must not describe the repository as a pile of rounds**. A visitor needs
what-it-is, how-to-get-it, what-it-claims; the round archaeology belongs in `docs/` and `.hgk/`, linked
once, not narrated on the front page.

## 5. Files checked for encouragement of an insecure default

`.hgk/credentials/CREDENTIAL_RECEIPT.json` (on `r5-s4-evidence`, not on `main`) is recorded here as a
tracked credential artefact. Whether it is genuinely redacted was **not** verified by this study; it is
flagged for the security pass rather than assumed clean, because a tracked file whose name promises
redaction is exactly the thing that should not be taken on trust.

## 6. Claim ceiling

`REPOSITORY_BRANCH_SET_REDUCED_WITHOUT_HISTORY_LOSS` — scoped to the seven branches listed, at the
commit shas measured. It is not a claim that the repository is free of untracked cruft, that history
contains no secrets, or that any branch removed elsewhere is recoverable.
