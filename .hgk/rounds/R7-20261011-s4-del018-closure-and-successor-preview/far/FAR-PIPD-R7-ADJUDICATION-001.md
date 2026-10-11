# FAR-PIPD-R7-ADJUDICATION-001 — the three candidate paths

Round `R7-20261011-s4-del018-closure-and-successor-preview`. Study of the adjudication the owner
left open at the end of R6: *fix DEL-018 first / open a successor release that delivers the repair /
do a security scan and attestation first*. This is a study over facts established in-round, not a
restatement of the earlier reports.

## 1. What the three paths are actually asking

| Path | What it really is | Blast radius |
|---|---|---|
| **A - fix DEL-018** | `RELEASE_MANIFEST@1` has failed since the R3 crosswalk. It is an **evidence-surface** failure, not a runtime defect. | Evidence files only. No product byte. |
| **B - successor release** | `v0.1.0-preview.1` ships the CE-1/CE-2 defects. The repaired wheel exists only in a worktree. Delivering it needs a **new** immutable tag, because the grant forbids moving the old one. | A new tag, new release, new assets. |
| **C - security scan + attestation** | Prove the candidate is free of secret/PII exposure and known dependency vulnerabilities, and attach a publication attestation. | Evidence only, unless it finds something. |

The R5Q round deliberately refused to repair DEL-018 ("stays exit 1 and is disclosed, not repaired as
an excuse to expand scope"), while the ledger that R5Q itself wrote says DEL-018 is *"正式 Gate 前必
修"* — mandatory before a formal gate. So the scope refusal was a deferral, not a determination that
the gap is acceptable. That is the tension this study resolves.

## 2. Facts established in-round (each with its evidence)

**F1 — DEL-018's failure depends on where you run it, and the on-record description is incomplete.**
`tools/build_publication_manifest.py` resolves `GIT_DIR = ROOT/".git"` and reads `refs/heads/*` and
`packed-refs` itself. In a **linked worktree** `.git` is a gitfile, so the tool dies with
`cannot resolve ref 'r5-s4-candidate' in ...\PIPD-r5q-release-wt\.git` — an *earlier and different*
failure than the one on record. Run in a primary-form checkout it reproduces the documented verdict.
Evidence: `execute/del018_check.json`, and the `preconditions` note in §5.

**F2 — the real content gap is 4 product paths, not 3.** On the R7 base (`9667783`) the uncovered set
is `tests/test_ce_repair_regression.py`, `tests/test_doctor_schema_truth.py`,
`tests/test_git_object_reader.py`, `tests/test_tqaep_design_positive.py` — 252 product paths, 248
covered. The fourth arrived with the R5R round's own regression test, so any figure quoted from
before R5R is stale.

**F3 — the prescribed minimal repair is a pure regeneration, and it works.**
`build_evidence_manifest.py --seal` → `build_publication_manifest.py --write` → `--check --current`
exits **0**, 252/252 covered, 0 violations. Three evidence files move; nothing product-side.

**F4 — but a passing check is not by itself evidence of repair.** The regeneration *shrinks* the
manifest (1916 → 1039 entries). A manifest that simply covers less would also pass. Measured: all
1085 dropped entries are stale `.hgk/` round artifacts that no longer exist in the tree, **0** are
product paths, and the 206 additions include exactly the 4 uncovered tests. So the closure is
staleness removal, not a coverage trade. `workorder/r7_del018_proof.py` asserts this mechanically.

**F5 — the successor release needs no merge.** `r5q-owner-opensource-preview` (`9bd33a1`) **is an
ancestor of** `r5r-ce-repair` (`9667783`); the repair branch already carries every R5Q artefact. A
successor can be cut straight from the repair line. This is what makes path B cheap.

**F6 — path B is already inside the grant that exists.** `OWNER_LICENSE_GRANT_R5Q.json` grants
`action: create_new_immutable_tag_and_prerelease` with `target: explicit release commit (never the
default branch)`, `prerelease: true`, and forbids only *overwrite main / force-push / move or delete
an existing tag / create a second repository*. `OWNER_LICENSE_DECISION.yaml`'s exclusions state it
outright: *"already published tags are not rewritten, **a superseding release is issued instead**"*.
So publishing a successor does **not** require a new owner act — it requires executing one already
granted.

**F7 — attestation is available natively; the default sidecar is stale.** `tools/publication_attestation.py`
builds and verifies a subject attestation from local git objects, so no cosign/sigstore identity is
needed. However `--verify` with default expectations **FAILS**: the default sidecar attests commit
`3aebbbc`/tree `1a7dc57f` (`generated_at 2026-10-09`, checker `INDEPENDENT_ACCEPTANCE_OFFICER_R3`)
while the pinned published subject is `f4f0a02`/`49082394`. This is a **newly surfaced** stale
evidence surface — it is not in the R5Q not-verified ledger.

**F8 — the factory scans are clean; no third-party scanner is installed.** `history_secret_scan.py`
over 2339 objects and the worktree: **0 hits, CLEAN/CLEAN**. `deny_list_scan.py`: **PASS**, 0 writer
usages inside the R4 scope (45 occurrences are 34 policy mentions + 11 log lines under `.hgk/`).
`pip-audit`, `osv-scanner`, `cosign`, `syft`, `grype`, `trivy` are **all absent**; `gpg` is present
but there is no signing identity. The declared dependency closure is a single entry
(`jsonschema>=4.0`), so a scanner is cheap to add but must be installed.

**F9 — the published wheel is already the repaired build.** The committed wheel is
`d6c3e295…` with `build_input_commit 1ab17d1`, and the `validate.py` inside it carries
`NON_RECORD_SIDECARS`. So R7 has to *release*, not rebuild — which removes the largest source of
risk (a reproducible-build divergence) from path B.

## 3. Friction, honestly assessed

| Path | Blocked by | Blocked by an owner act? |
|---|---|---|
| A | nothing — proven working (F3/F4) | no |
| B | nothing new — grant covers it (F6) | **no** |
| C (attestation) | nothing — native tooling (F7) | no |
| C (dependency scan) | a scanner must be installed; network required | no |
| C (signature/attestation *by an external identity*) | no signing identity on this host | **yes** — properly deferred |

## 4. Adjudication

**Order A → C → B, and publish the successor.**

- **A first** because it is free, it is the one item the project's own ledger calls mandatory before a
  formal gate, and doing it *before* the release means the published artefact carries the closure
  rather than deferring it again.
- **C before B** because a scan finding changes what the release may claim. Scanning after publishing
  would force either a re-release or an unpublishable claim.
- **B last**, so the tag carries A's closure and C's outcome together.
- **C's signature/attestation limb is deferred, not faked.** No signing identity exists on this host;
  inventing one would be an agent self-attestation, which is exactly the thing the governance forbids.
  It is recorded as an open item with the reason.
- **Path A must not be "fixed" by loosening the check.** The check is not edited; the evidence is
  regenerated. The non-lossy assertion exists precisely so that a convenient pass cannot be mistaken
  for a repair (F4).

### Why not the other orders

- *C first, alone*: leaves the user's actual problem (the preview they can download is defective)
  untouched for another round. The scan is cheap but it is not the deliverable.
- *B first*: publishes a tag whose DEL-018 status would have to be re-disclosed as still failing, and
  any scan finding would then attach to a tag that already exists. Both bad.
- *A only*: this is the state the owner already rejected — a repaired line that nobody can obtain.

## 5. Execution plan and its outcome

| Step | Status | Evidence |
|---|---|---|
| Admit the R7 obligations through the typed SharedSpine API | done | `admission/r7_admission.json` (6 requirements FROZEN, 0 errors) |
| Run in a primary-form checkout, disclose the two tool preconditions | done | `execute/del018_check.json` |
| A: regenerate manifest + seal + projection | done | commit `64b9955` |
| A: prove the closure is not a coverage cut | done, PASS 4/4 | `evidence/DEL018_CLOSURE_PROOF.json` |
| C: history secret scan | done, PASS | `evidence/scan_history_secret.json` |
| C: deny-list scan | done, PASS | `evidence/scan_deny_list.json` |
| C: dependency vulnerability scan | see the closure report | `evidence/scan_dependency.json` |
| C: attestation verification | done — **FAIL, surfaced as new** | `evidence/scan_attestation_verify.json` |
| B: stage assets and bind the release commit | done | `release/STAGED.json` |
| B: publish tag + prerelease | done, PUBLISHED | `release/PUBLISH_RECEIPT.json` |
| B: anonymous read-back of the published bytes | done, PASS | `release/READBACK.json` |
| Independent acceptance on the published bytes | separate checker, not the maker | `verify-codex/` |

### Two preconditions of the release-evidence toolchain (disclosed, not hidden)

The round runs in `C:/Projects/Agent_Workspace/PIPD-r7-release`, a **normal clone** rather than a
linked worktree, because `build_publication_manifest.py` cannot run in a worktree (F1) and requires
the local ref `r5-s4-candidate` to exist. Both are undocumented preconditions of the tool. They are
recorded rather than patched around: editing the tool would change a product byte and re-open the
build-reproducibility question for a purely cosmetic gain.

## 6. Claim ceiling for this study

`R7_ADJUDICATION_IS_A_RECOMMENDATION_EXECUTED_BY_THE_MAKER` — the adjudication is the maker's, and
the maker cannot accept its own work. The successor release is published on the owner's **existing**
grant, not on a new owner act; if the owner regards a fresh grant as required for each tag, that is
an owner decision this round did not take. Nothing here grants `G_RELEASE_FULL_PASS`,
`PRODUCTION_VERIFIED`, `FULL_S0_S4_INDEPENDENT_PASS` or any host certification.
