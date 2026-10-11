# FAR-PIPD-R11-FDAEVID-002 — integrating the round's automation use into the team's own evidence surface

Discharges `REQ-PIPD-R11-FDAEVID-002`. The obligation was to integrate, **in the capability team's own
contract form** rather than a format of this round's invention, and to update the Fabric repository with
ONLY the paths this round authored.

## What was produced

| path | role |
|---|---|
| `fabric-desktop-automation/evidence/FDA_R11_CREDENTIAL_AUTOMATION_DISCIPLINE_AND_EVIDENCE.md` | the discipline + embedded raw evidence |
| `fabric-desktop-automation/evidence/FDA_R11_EVIDENCE_SIDECAR.json` | the markdown's own SHA, published out-of-band |

Committed as `463ca0a`, exactly those two paths (`git show --stat` shows 2 files).

## Decision 1 — the artefact deliberately does NOT join the sealed single-evidence series

The team's preflight selects the **LAST sorting member** of the `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE`
prefix for two of its five checks:

- check 2 — the latest must carry no `this_file_sha256`;
- check 4 — `final_subject_root: <40-hex>` in the latest must equal the manifest's `subject_root.git_head`
  and the current checker's subject, on the first 12 characters.

A new file in that series would therefore become the "latest" and **move a sealed, externally accepted
three-way binding** (`be576bebe767`). So the artefact was given a distinct family name and the binding was
left alone.

**Proved by measurement, not asserted:** the preflight was run **before** the addition and **after** it,
and reports `PREFLIGHT: PASS` both times, with `three-way bound: be576bebe767` unchanged. The sealed
corpus is untouched.

**Refused alternatives, with the reason:**
- *Name it into the series so it appears in the external review* — refused: it would hijack two checks
  and move a binding that an external reviewer has already accepted.
- *Regenerate the manifest so the new file joins it* — refused: that rewrites the exact-set counters and
  the `subject_root` of an externally accepted artefact to include material that was never externally
  reviewed. That is manufacturing acceptance, one layer up from `EXISTS != TRUE`.
- *Write it in this round's own format because it is "just" evidence* — refused: the obligation says the
  team's contract, and a locally invented format would not survive the team's own preflight.

## Decision 2 — the sidecar exists because a self-hash is forbidden

The contract forbids the markdown from carrying its own digest. The SHA is therefore published in a
sibling sidecar, committed in the same change as the file it digests, so a reader re-hashes the markdown
and compares. `self_hash_inside_md` is recorded as `false` in the sidecar and was checked mechanically.

## Decision 3 — only this round's paths, in a repository that is 51 entries dirty

The Fabric working tree carried **51 uncommitted entries** from other sessions before this round touched
it, and carries exactly 51 after the commit. Nothing of theirs was swept in; `git add` named the two
paths explicitly. A round that committed "everything to be safe" would have destroyed the ability to
attribute anyone else's work.

## Correction carried into the artefact

A bounded fan-out used for the source survey reported that the credential broker has "exactly ONE file
outside `scripts/cred/`, and it is a Markdown documentation file". Re-measured by the round: **4 paths**,
of which only one is a source referrer; the other three are a FAR-run extraction ledger, a writer
dispatch log, and a **binary false positive inside the SQLite spine file**. The fan-out's conclusion
survived and its count did not, and the count was corrected **before** it entered the artifact.

The same survey flagged a methodology trap that is now recorded as discipline: most of the control
plane's `config/` is **untracked**, so a `git grep` survey reports a confident zero having read almost
nothing. Every zero used here came from a working-tree search and was reproduced independently.

## Residuals

1. Two manifests both declare schema `FDA-EVIDENCE-MANIFEST/3` with different content (54 vs 63 entries,
   different `subject_root`). The preflight reads the bundle copy only; which instance governs NEW work is
   stated nowhere found in-repo. **Not resolved here**; a new artefact currently has to pick one, and this
   round picked the one the checker reads.
2. The externally reviewed series was deliberately **not** extended, so R11 material is not inside it. A
   reader looking for it there will not find it, by design and for the reason in Decision 1.
3. The artefact is submission-ready **as evidence**, not as an acceptance verdict: it extends nothing
   already sealed and claims no new closure of any finding.

**Claim ceiling:**
`ROUND_AUTOMATION_USE_INTEGRATED_IN_THE_TEAM_CONTRACT_FORM__SEALED_THREE-WAY_BINDING_PROVEN_UNMOVED_BY_BEFORE-AND-AFTER_PREFLIGHT__ONLY_AUTHORED_PATHS_COMMITTED`.
