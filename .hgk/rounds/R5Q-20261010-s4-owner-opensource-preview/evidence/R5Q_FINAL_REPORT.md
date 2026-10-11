# R5Q — Owner-Authorised S4 Open Source Preview: master evidence

**Round:** `R5Q-20261010-s4-owner-opensource-preview`
**Contract:** `PIPD-LS-SP-R5Q-OWNER-OPENSOURCE-PREVIEW-20261010`
**Date:** 2026-10-10 (Asia/Taipei)
**ChangeSet:** `CONTINUATION` of `r5p-post-challenge-repair` — affected-only publication,
documentation and packaging changes. No new R6, no PI/PD redesign, no schema/Skill/CLI rewriting.

---

## 1. Claim ceiling — read this before anything else

| Claim | State |
|---|---|
| `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED` | **CLAIMED** — real public tag + prerelease, read back from an anonymous source |
| `S4_OPEN_SOURCE_PREVIEW_TECHNICAL_GO` | `YES` / `GO_WITH_DISCLOSED_LIMITATIONS` (from R5P S0–S4) |
| `PARTIAL_CHALLENGE` | **MAINTAINED** — 57-row base stays `28 evidenced / 10 active gaps / 19 deferred` |
| `DEL-018 RELEASE_MANIFEST@1` | **`FAIL / EVIDENCE_GAP`** — open, disclosed, not closed |
| `FULL_S0_S4_INDEPENDENT_PASS` | `NOT_GRANTED` |
| `G_RELEASE_FULL_PASS` | `NOT_GRANTED` |
| `PRODUCTION_VERIFIED` | `NOT_CLAIMED` |
| Independent acceptance by a non-maker checker | **RECEIVED**, and superseded by a stricter run — first receipt `PASS_ONLY_THE_ABOVE_CLAIMS` (9/9); second run on the specified model lane **`COUNTEREXAMPLE_FOUND`** (12/12 claims PASS, 2 non-stop-ship defects). See §6.1, §6.3 |

Nothing in this round upgrades the R5P technical GO into a full-gate pass. The independent checker
returned §6.1, so the maker-side results in §4 are now corroborated from outside — for the immutable
released artefact only, and on a different model lane than the plan named.

## 2. Identity chain (no reused hashes)

| Role | Value |
|---|---|
| Review baseline | `r5p-post-challenge-repair` @ `2efc84eac8e1939092c748d5b389b6dd72267aef` (tree `e254ea23243e0c767bf79fc647b82341493a231c`) |
| Superseded review wheel | `bb070a6f…` — **never reused, never re-labelled** |
| Frozen candidate head | `7c5bc585c7d889cd338da853be4efc4b8f07d3b2` (deliberately not the release tip) |
| Wheel build-input commit | `c66be0806155eeae3c997a905885ede1e661571f` |
| **Release commit** | `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32` |
| Release tree | `da39a1effe8cb2d73fb63ba45b5ae73685ee93e6` |
| Wheel SHA256 | `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60` |
| Source archive SHA256 | `8faaaa5a171c3ba62e5483e2418854936965015ef976dfb92a74cffa569659b0` |

Commit sequence in the isolated worktree `PIPD-r5q-release-wt` (branch `r5q-owner-opensource-preview`):

| Commit | What it does |
|---|---|
| `f4e1b58` | Licence landing across `LICENSE` / `NOTICE` / `OWNER_LICENSE_DECISION.yaml` / `pyproject.toml` / `SBOM.cdx.json` / `PROVENANCE.md` / `README.md` / `ACCEPTANCE.md` / `build_dist.py` |
| `c66be08` | Ships the licence basis inside the wheel; replaces the over-claiming `licence_files` field with three precise fields; adds the licence oracle |
| `74af152` | Release-candidate wheel + acceptance evidence (UAT matrix, oracle, suite log) |
| `c53e147` | Publication driver + preview release notes |
| `95e8cf2` | Publisher resolves the release identity from the repository instead of a literal |
| `89c1c5c` | Release body becomes a rendered template (a committed literal would be stale on write) |
| `cc9bf574` | Derived release assets kept out of the tree — stops the manifest depending on its own digest |

The R3 line was **not rewritten**: no force-push, no existing tag moved or deleted, no second
repository, and no merge of the release branch into `main`. `main` was advanced **only** by an
additive README-only pointer commit (`3aebbbce` → `de3a1d9`) so the repository front page stops
advertising the pre-grant R3 state; the R3 content itself is preserved byte-for-byte below that
one commit (see §11).

## 3. What the licence landing actually changed

- **Chosen licence: `Apache-2.0`** (study `FAR-PIPD-R5Q-LICENSE-001`), selected over MIT / BSD-3 /
  MPL-2.0 / AGPL-3 / dual-licensing on explicit patent grant (§3), the NOTICE attribution mechanism
  (§4(d)) this repository needs for its provenance split, trademark non-grant (§6), and compatibility
  with its MIT dependency. Accepted cost: §4(b) adds a modified-file notice obligation downstream.
- `OWNER_LICENSE_DECISION.yaml` is the **single source of truth** for the SPDX id. The wheel reads the
  id from it, and now ships the file itself, so a consumer can audit the derivation instead of taking
  the conclusion on faith.
- The prior non-granting record (`LicenseRef-PIPD-Proprietary`) is preserved verbatim in
  `previous_decision` and marked superseded — history is retained, not rewritten or back-dated.
- SBOM: root licence at `metadata.licenses` = `Apache-2.0`, plus `pipd:licence:basis`,
  `pipd:licence:granted_utc`, `pipd:licence:notice_file`. The single dependency keeps its own `MIT` —
  the project's licence is not asserted over upstream code. A top-level scope property states that the
  SBOM covers the declared dependency set only and does **not** compute a transitive closure.

## 4. Verification performed, against which bytes

| Check | Local build (`c450dbef…`) | Wheel downloaded from the release |
|---|---|---|
| Deterministic suite | 311 tests, `OK (skipped=6)` | — (source-tree check) |
| UAT matrix | 27 PASS / 2 INFO / 0 FAIL (source + install modes) | 14 PASS / 1 INFO / 0 FAIL (install mode) |
| Licence oracle | 21/21 | 21/21 |
| Secret scan | PASS, 984 files | — |

The UAT modes are labelled in the receipts. The clean-venv install used `uv pip install --python`
after `python -m venv`'s `ensurepip` bootstrap failed **in the background-process context on this
host**; the receipt records the installer path taken (`uv_pip_online_index`) rather than hiding it.
That is an environment workaround, not a product finding.

Notable UAT coverage: `doctor` positive and a missing-schema typed negative; the full design chain
with SoD rejection; `project --dry-run` proving zero writes; `project --out` to disposable scratch
(5 Web + 3 Host + IR); `export --out` with archive, manifest and `SHA256SUMS` recomputed; the wheel's
own install → uninstall → reinstall cycle with an empty residue check; a large-input run (801 atoms).

## 5. Publication

- **Repo:** https://github.com/shw097-team/PIPD-LS-SP (public)
- **Tag:** `v0.1.0-preview.1` → `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32`
- **Release:** https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1 — id `409035298`, `prerelease=true`, `draft=false`
- **Branch pushed:** `r5q-owner-opensource-preview` (new branch)
- **Assets (4/4, HTTP 201):** wheel, source archive, `SHA256SUMS`, `PREVIEW_NOTES_v0.1.0-preview.1.md`

Readback (anonymous GitHub API + fresh asset downloads, no token, no local release cache) — 9/9:

`repo_public` ✓ · `tag_exists_and_targets_release_commit` ✓ · `commit_tree_matches` ✓ ·
`branch_points_at_release_commit` ✓ · `release_is_prerelease` ✓ · `release_not_draft` ✓ ·
`release_body_discloses_limitations` ✓ · `all_assets_download_and_match` ✓ · `readme_at_tag_points_to_tag` ✓

One 404 on the first readback was a GitHub edge-cache replay of the pre-publication tag lookup; the
raw endpoint returned 200 with the correct SHA and the re-run passed. Recorded here rather than
quietly discarded, because a readback that only passes on the second attempt is worth knowing about.

## 6. Independent verification — two runs, the second stricter

### 6.1 Independent non-Maker checker

A separate read-only process (own context, own tool session, no participation in the build) re-derived
every decisive claim from the **published** subject alone: anonymous download plus its own `git clone`
— it read no local wheel and no local evidence file. Result: **9/9 PASS, zero stop-ship
counterexamples**, verdict `PASS_ONLY_THE_ABOVE_CLAIMS`. Frozen receipt:
`evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json`.

What it independently confirmed: tag → `cc9bf574` with tree `da39a1ef` (via its own clone, not just the
API); wheel `c450dbef…` agreeing across asset digest, release body and `SHA256SUMS`, with all 40 RECORD
rows verifying; the licence packed inside the wheel and byte-identical to the repository copy; a
clean-venv install whose `doctor` reports `INSTALLED` and whose 19 schemas pass Draft2020-12 checks;
the design chain running green; typed non-zero negatives when the installed schema set is
corrupted or missing; the claim ceiling stated without inflation; and destination safety proven with a
canary — including that `--allow-replace` preserves the old tree as a backup rather than deleting it.
Its `validate` result was green **only with an explicit `--root` and a bundle whose PI-PKG member had
had its `_profile_meta` sidecar removed**; §6.3 records what the second run found when neither
condition was supplied, and the maker reproduced both.

**Two qualifications on this receipt, both material.**

1. **Model lane deviation.** The round's model plan assigned VERIFY/SECURITY to a checker on
   `GPT 6.1 SOL-MEDIUM` via the CODEX CLI. Neither `codex` nor `gh` is installed on this host
   (`opencodex 2.11.0` exists but is not the `codex` CLI), so the VERIFY lane ran as an independent
   Hermes subagent process on `deepseek-v4.1-flash`. It is genuinely independent in *process* terms —
   separate context, separate session, read-only mandate, no access to the maker's reasoning — but it
   is **not** the model the plan named. Strict model SoD would require re-running this lane on the
   specified checker model.
2. **It predates the entry-point correction.** The checker ran before §11's fix changed two *mutable*
   surfaces: the front-page README on `main` and the live release body. Its assertions about those
   surfaces still hold (the body still discloses the limitations and the licence; the README still
   marks the claim ceiling), and the immutable artefact it actually verified — tag, commit, tree,
   wheel bytes — is untouched by the fix. The fix itself is covered by the round's own anonymous
   readback, not by this receipt.

Explicitly **not** verified by it: the full test suite; the 57-row SPEC/DEL base row by row; S5–S8
runtime, host-native or Windows symlink/junction behaviour; cryptographic provenance (no attestation
or signature exists — SHA-256 only); a full CVE / supply-chain scan; and `validate` without a
`schemas/` surface.

### 6.2 Evidence pack

Machine-readable, token-free, written under the round's `evidence/` root.

### 6.3 Second independent run, on the model lane the plan named — COUNTEREXAMPLE_FOUND

`§6.1`'s checker ran as a Hermes subagent on `deepseek-v4.1-flash`, not the `GPT 6.1 SOL-MEDIUM` lane
the round's model plan specified. That deviation was reported, not smoothed over, and the lane was
re-run on the specified model (`openai-codex/gpt-6.1-sol`, `reasoning_overrides` = medium) as a fresh
read-only process with its own context and tool session.

That run returned **`COUNTEREXAMPLE_FOUND`**, not a clean pass. All twelve of its claims passed, and
it independently confirmed the corrected entry point (claims 8–11: `main` advanced `3aebbbce` →
`de3a1d9` with a 14-line README-only diff, R3 still an ancestor, no `not touched` wording left in the
live body, and the re-uploaded preview notes matching the branch byte-for-byte). But it also found
two reproducible, **non-stop-ship** defects:

| | finding | reproduced by the maker against the published wheel |
|---|---|---|
| CE-1 | `validate` does not resolve the wheel's own schemas the way `doctor` does | from a cwd with no `schemas/` and no `--root`: exit **2**, `INPUT_SHAPE_INVALID`, `FileNotFoundError: <cwd>/schemas/PI-PKG.schema.json` — while `doctor` in the **same venv** exits 0 with `schema_source.mode = INSTALLED` |
| CE-2 | a bundle assembled from the compilers' own unedited stdout is rejected | four unmodified compiler outputs → exit **1**, `checked=4`, `PI-PKG/: Additional properties are not allowed ('_profile_meta' was unexpected)`; deleting only that sidecar → exit **0**, `checked=4`, `findings=[]` |

Both were reproduced independently by the maker — a clean venv from the wheel downloaded off the
release, the four commands run with their real exit codes, the raw bundle assembled by hand. The
harness, the wheel it ran against and the raw results are frozen in `evidence/ce_repro/`.

**Why this is not a stop-ship and why the call is not the maker's to make.** Install, licence
packaging inside the wheel, `doctor`, the CLI, and every artefact hash are unaffected. But the owner
grant's stop-ship list contains *"core intake → PI → PD → ECP/TQAEP chain broadly unusable"*, and a
tool that rejects its own unedited output is on that boundary. The maker therefore **did not** rule it
cosmetic, and **did not** repair it: either repair changes member bytes, which would require a
superseding release, and published tags are never rewritten. Both are disclosed as limitations 6 and
7 on the release body, README and preview notes, and the disposition — repair in a superseding
release, or accept for the preview — is left to the owner.

**Consequence for §4.** The maker-side UAT row claiming the design chain plus `validate` was green is
**true only under an undocumented pair of conditions** (explicit `--root`; `_profile_meta` stripped).
That qualification was missing before this run and is the reason the claim read stronger than the
evidence.

## 7. Credential handling (disclosed)

The owner's fine-grained PAT appeared in this round as a chat attachment. It was **not** needed to read
anything (the repository is public) and was used once, for the authorised push, tag and release.

Mechanism: the value was read into process memory and handed to `git` through a child-process
environment variable consumed by a generated askpass shim that contains no secret. It therefore never
entered argv, a remote URL, git config, a log line, the evidence pack or any uploaded asset. A
credential-shape sweep (8 patterns, including GitHub PAT/`ghp_`/`gho_`, AWS, Slack, bearer, PEM
private-key and OpenAI key shapes) runs inside the licence oracle and additionally covers the wheel's
METADATA and packaged files: clean.

**Standing caution:** a secret pasted into a chat transcript should be treated as exposed. Rotating this
PAT is advisable; the publication does not depend on it any more.

## 8. Side effects of this round (complete list)

| Effect | Where |
|---|---|
| New branch pushed | `shw097-team/PIPD-LS-SP` — `r5q-owner-opensource-preview` |
| New immutable tag | `shw097-team/PIPD-LS-SP` — `v0.1.0-preview.1` |
| New prerelease + 4 assets | GitHub Releases, id `409035298` |
| New kanban board | Hermes `kanban.db` — `pipd-r5q-20261010` |
| New SWARM graph | root `t_c613d284`, 5 workers, verifier, synthesizer |
| Local worktree | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt` (branch `r5q-owner-opensource-preview`) |
| `main` | advanced by **one additive README-only pointer commit**: `3aebbbce` (R3) → `de3a1d9`; no force-push, no rewrite |
| Existing tags / R5P baseline | **unchanged** |

## 9. Open items and the shortest recovery path

1. **The two counter-examples (CE-1, CE-2) are open.** Each needs a member-byte change, so the
   repair path is a superseding release, not a rewrite of `v0.1.0-preview.1`. Disposition is the
   owner's: repair, or accept for the preview. Disclosed on every public surface either way.
3. **Independent acceptance — RECEIVED, with qualifications.** See §6.1: 9/9 claims, no counterexample,
   `PASS_ONLY_THE_ABOVE_CLAIMS`. Two caveats are recorded there and matter: the checker ran on
   `deepseek-v4.1-flash` rather than the plan's `GPT 6.1 SOL-MEDIUM` lane (no `codex`/`gh` on this
   host), and it predates the §11 entry-point correction.
3. **`DEL-018 RELEASE_MANIFEST@1` — `FAIL/EVIDENCE_GAP`.** `tools/build_publication_manifest.py
   --check --current` exits 1. Uncovered paths: `tests/test_git_object_reader.py`,
   `tests/test_doctor_schema_truth.py`, `tests/test_tqaep_design_positive.py`. Disclosed in the
   release body, README and preview notes.
4. **`CORR-01..08` / 12 TT rows** — the dispositions that this round touched are recorded in the
   tasks file; the rows untouched by publication keep their R5P gaps.
5. **Deferred, unchanged:** the 10 `S4_ACTIVE_GAP` rows, the 19 `DEFERRED_BY_INSTRUCTION` rows,
   S5–S8 live execution, PRE-W3, host-native certification, the 22 inactive technologies, and
   Windows symlink/junction behaviour beyond the tested scope.

To withdraw the preview: the tag is immutable by policy, so issue a superseding release with a
deprecation notice rather than moving or deleting `v0.1.0-preview.1`.

## 10. Evidence inventory (this round)

| Artefact | Purpose |
|---|---|
| `compiler/R5Q.CONTRACT.json`, `compiler/R5Q.*.raw.txt`, `compiler/out/` | prompt compiler contract + four raw verdicts |
| `admission/r5q_admission.json` | HGK typed admission (7/7 FROZEN) |
| `preflight/R5Q_PREFLIGHT.json` | read-only round preflight |
| `license/R5Q_FAR_LICENSE_QUICKSTUDY.md` | FAR study behind the licence choice |
| `owner/OWNER_PREVIEW_DECISION_PACKET.md`, `owner/OWNER_LICENSE_GRANT_R5Q.json` | the owner's decision and grant |
| `tools/r5q_license_oracle.py` | executable licence claims (21 checks) |
| `tools/r5q_publish.py` | preflight / publish / readback driver |
| `uat/uat_matrix_r5q.py`, `uat/out/`, `uat/out2/` | UAT harness + both runs |
| `evidence/R5Q_LICENCE_ORACLE.json`, `…_PUBLISHED.json` | oracle on local build and on published bytes |
| `evidence/R5Q_PUBLICATION_PREFLIGHT.json`, `R5Q_PUBLICATION.json`, `R5Q_PUBLICATION_READBACK.json` | publish + anonymous readback |
| `evidence/R5Q_SECRET_SCAN.json` | credential sweep over the published tree |
| `evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json` | non-Maker checker's frozen receipt (9/9, no counterexample) |
| `evidence/ce_repro/` | maker's reproduction of CE-1/CE-2: harness, the wheel it ran against, raw exit codes |
| `evidence/R5Q_NOT_VERIFIED_LEDGER.md` | the 7-item `what_i_did_not_verify` list classified; 2 must stay open |
| `license/R5Q_FAR_RECEIPT_CURRENCY_STUDY.md` | FAR study on closing the receipt-currency reservation |
| `release/RELEASE_BODY.md`, `release/.gitignore` | rendered release notes template; derived assets excluded |

## 11. Correction made after review — the entry point was pointing at the wrong thing

**What was wrong.** The publication left the repository front page advertising the pre-grant R3
state: `main`'s `README.md` mentioned neither `v0.1.0-preview.1`, nor "preview", nor `Apache-2.0`.
Anyone landing on the repository saw a version with no licence and no download pointer — which is
precisely what the acceptance report forbids (`main = 3aebbbce / R3`: "documentation and download
entry points must point at the new Preview tag/commit, to avoid a default clone of the old
version"; `TT-R5P-08`: "pin the correct branch/tag at the top of the release front page, keep the
historical positioning").

**Why the round's own readback did not catch it.** The check was `readme_at_tag_points_to_tag`: it
read `README.md` **at the tag**, which did point at the tag, and passed. It never read the README
on the **default branch** — the one a visitor actually lands on. A check that only inspects the
artefact you already believe is correct cannot find a gap in the entry point.

**Fix.** One additive, README-only commit on `main` (`3aebbbce` → `de3a1d9`), pushed as a normal
forward push — no force, no merge of the release branch, no other file touched. It pins a banner
naming tag `v0.1.0-preview.1`, its `Apache-2.0` grant and the release page, and marks everything
below as the R3 historical snapshot, as `TT-R5P-08` requires.

**Checks added so this class of gap fails loudly next time:**

| New readback check | What it enforces |
|---|---|
| `front_page_readme_points_to_tag` | the **default branch** README names the release tag |
| `front_page_readme_marks_itself_snapshot` | historical narrative is labelled as history, not current |
| `default_branch_not_rewritten` | the front-page commit still sits on the R3 line — advancement, never a rewrite |
| `release_commit_reachable_from_branch_tip` | replaces `branch_points_at_release_commit`, which asserted the branch tip *equals* the release commit — an invariant that publication evidence commits necessarily break |

The final readback is **12/12 PASS**.

**Statement-level consequence, disclosed.** Every surface that said "`main` was not touched" was
made false by this fix. The release body (live, re-published via the API), `README.md`,
`ACCEPTANCE.md`, the preview-notes asset, the OpenSpec tasks/proposal and this report were all
corrected rather than left stale. The immutable tag `v0.1.0-preview.1` still points at
`cc9bf574`, whose tree predates this fix — that is expected for an immutable release pointer, and
is why the corrected statements live on the mutable surfaces. The published wheel is unaffected:
its bytes, hash and contents are identical (`c450dbef…`).
