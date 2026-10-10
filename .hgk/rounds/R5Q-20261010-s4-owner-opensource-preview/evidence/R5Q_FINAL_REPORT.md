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
| Independent acceptance by a non-maker checker | **PENDING** — dispatched this round, receipt not yet issued |

Nothing in this round upgrades the R5P technical GO into a full-gate pass. A maker-side PASS in this
document is an unconfirmed claim until §8 returns.

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

`main` was **not** touched (it still points at the older R3 line); no force-push; no existing tag was
moved or deleted; no second repository was created.

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

## 6. Credential handling (disclosed)

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

## 7. Side effects of this round (complete list)

| Effect | Where |
|---|---|
| New branch pushed | `shw097-team/PIPD-LS-SP` — `r5q-owner-opensource-preview` |
| New immutable tag | `shw097-team/PIPD-LS-SP` — `v0.1.0-preview.1` |
| New prerelease + 4 assets | GitHub Releases, id `409035298` |
| New kanban board | Hermes `kanban.db` — `pipd-r5q-20261010` |
| New SWARM graph | root `t_c613d284`, 5 workers, verifier, synthesizer |
| Local worktree | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt` (branch `r5q-owner-opensource-preview`) |
| `main` / existing tags / R5P baseline | **unchanged** |

## 8. Open items and the shortest recovery path

1. **Independent acceptance receipt — pending.** Dispatched to a separate read-only process; it has
   the published tag, commit and wheel as its only subjects and was told not to touch anything.
   Until it returns, the maker-side results in §4 are unconfirmed.
2. **`DEL-018 RELEASE_MANIFEST@1` — `FAIL/EVIDENCE_GAP`.** `tools/build_publication_manifest.py
   --check --current` exits 1. Uncovered paths: `tests/test_git_object_reader.py`,
   `tests/test_doctor_schema_truth.py`, `tests/test_tqaep_design_positive.py`. Disclosed in the
   release body, README and preview notes.
3. **`CORR-01..08` / 12 TT rows** — the dispositions that this round touched are recorded in the
   tasks file; the rows untouched by publication keep their R5P gaps.
4. **Deferred, unchanged:** the 10 `S4_ACTIVE_GAP` rows, the 19 `DEFERRED_BY_INSTRUCTION` rows,
   S5–S8 live execution, PRE-W3, host-native certification, the 22 inactive technologies, and
   Windows symlink/junction behaviour beyond the tested scope.

To withdraw the preview: the tag is immutable by policy, so issue a superseding release with a
deprecation notice rather than moving or deleting `v0.1.0-preview.1`.

## 9. Evidence inventory (this round)

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
| `release/RELEASE_BODY.md`, `release/.gitignore` | rendered release notes template; derived assets excluded |
