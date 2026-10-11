## 1. Governance surfaces (enabled for this change)

- [x] 1.1 Native prompt compiler executed over the round contract (`lint`, `activation`, `acceptance`,
      `compile`) — all four report `PROMPT_COMPILE_PASS`, `error_count=0`.
- [x] 1.2 HGK typed admission: every R5Q requirement reaches `FROZEN` with a TaskSpec/WorkOrder through
      `admit_requirement` / `checkpoint` (no raw SQL).
- [x] 1.3 KANBAN board `pipd-r5q-20261010` + SWARM graph (root `t_c613d284`, 5 workers, verifier,
      synthesizer) created and read back for the round.
- [x] 1.4 GSTACK route readback recorded against the round's tooling.
- [x] 1.5 This OpenSpec change created.

## 2. Licence landing (owner grant, `Apache-2.0`)

- [x] 2.1 `LICENSE` replaced with the verbatim Apache License 2.0 text; normalised digest compared
      against the canonical ASF text (`cfc7749b…`, exact match).
- [x] 2.2 `NOTICE` created: material-class split, donor-plugin non-assertion, third-party components,
      exclusion policy.
- [x] 2.3 `OWNER_LICENSE_DECISION.yaml`: `decision: Apache-2.0`, with the superseded non-granting record
      preserved verbatim (not back-dated) and explicitly marked as superseded.
- [x] 2.4 `pyproject.toml` declares `license` / `license-files`.
- [x] 2.5 `SBOM.cdx.json`: project `Apache-2.0` at `metadata.licenses`; `jsonschema` corrected to `MIT`;
      licence basis / granted date / NOTICE file added as properties; scope ceiling declared.
- [x] 2.6 `PROVENANCE.md` gains the licence layer.
- [x] 2.7 FAR quick study recorded (FAR-PIPD-R5Q-LICENSE-001) with alternatives, criteria and the
      accepted cost of the choice.
- [x] 2.8 Licence oracle written and green: `LIC-01..LIC-18`, 21/21 checks, including the wheel's own
      RECORD self-manifest and a credential-shape sweep. This is the oracle the R5P crosswalk recorded
      as missing for the licence/SBOM rows.

## 3. Release candidate and distribution

- [x] 3.1 Immutable release candidate commits frozen in an isolated worktree
      (`PIPD-r5q-release-wt`), never merging into `main` or altering the R5P baseline. `main` later
      received one additive README-only pointer commit (`3aebbbce` → `de3a1d9`) so the repository
      front page points at the preview tag, per `TT-R5P-08`.
- [x] 3.2 Wheel rebuilt from `c66be08`; METADATA carries `License-Expression` + `License-File`; the
      licence text, NOTICE **and the owner decision slot** are packed inside the wheel (41 members).
- [x] 3.3 `WHEEL_MANIFEST.json` records `build_input_commit`, a distinct `released_commit` binding, the
      licence and the precise packed/declared licence file sets; the superseded `bb070a6f…` wheel hash is
      not reused.
- [x] 3.4 `SHA256SUMS` regenerated over the wheel and the source archive of the release commit. Both are
      derived artefacts, deliberately not committed, so the manifest cannot depend on its own digest.

## 4. Verification against the actual published bytes

- [x] 4.1 Deterministic suite re-run on the release tree: 311 tests, `OK (skipped=6)`.
- [x] 4.2 Clean venv, no `PYTHONPATH`, outside the repository: install the wheel, `doctor` positive and
      missing-schema typed negative, 19-schema readback.
- [x] 4.3 Design chain `intake → compile-pi → bind-pd → compile-ecp → compile-tqaep`, `validate`, with
      SoD rejection.
- [x] 4.4 `project --dry-run` zero write; `project --out` to disposable scratch (5 Web + 3 Host + IR);
      `export --out` to scratch with recomputed archive / manifest / `SHA256SUMS`.
- [x] 4.5 Licence consistency read out of the installed wheel's METADATA and packaged licences.
- [x] 4.6 UAT matrix: 27 PASS / 2 INFO / 0 FAIL in both modes on the local build, then re-run as
      14 PASS / 1 INFO / 0 FAIL against the wheel **downloaded from the published release**.
- [x] 4.7 Licence oracle re-run against the downloaded published wheel: 21/21.

## 5. Publication and readback

- [x] 5.1 Tag collision checked (no tag and no release existed; lookup returned 404).
- [x] 5.2 Immutable tag `v0.1.0-preview.1` created at the explicit release commit
      `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32`; GitHub **prerelease** `prerelease=true`,
      `draft=false`.
- [x] 5.3 Assets attached: wheel, source archive, `SHA256SUMS`, preview notes — 4/4, HTTP 201.
- [x] 5.4 Independent readback from an anonymous source that never used the local release cache:
      tag → release commit, commit tree, branch tip, prerelease flag, release body disclosures, README
      entry point, and all four assets re-downloaded and re-hashed. 9/9 checks PASS.
- [x] 5.5 Credential hygiene: the PAT was read into process memory and passed to `git` through a
      child-process environment variable consumed by an askpass shim — never in argv, never in a remote
      URL, never in git config, never in a log line, never in the evidence pack or an asset. Secret scan
      over the published tree: 984 files, PASS.

## 6. Independent verification and evidence

- [x] 6.1 Independent non-Maker checker (separate process, read-only) re-derived the decisive claims
      from the published subject: **9/9 PASS, no counterexample**, `PASS_ONLY_THE_ABOVE_CLAIMS`.
      Frozen receipt in `evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json`. Qualification: it ran
      on `deepseek-v4.1-flash` rather than the plan's `GPT 6.1 SOL-MEDIUM` lane.
- [x] 6.2 The lane was re-run on the specified model (`openai-codex/gpt-6.1-sol`, effort medium) as a
      fresh read-only process. It confirmed the corrected entry point (claims 8–11 PASS) and returned
      **`COUNTEREXAMPLE_FOUND`**: 12/12 claims PASS plus **CE-1** (`validate` does not resolve the
      wheel's own schemas the way `doctor` does) and **CE-2** (a bundle from the compilers' own
      unedited stdout is rejected over `_profile_meta`). The maker reproduced both against the
      published wheel bytes; harness frozen in `evidence/ce_repro/`. Both disclosed as limitations
      6/7 on the release body, README and preview notes. **Disposition is the owner's** — each fix
      changes member bytes and needs a superseding release, since published tags are never rewritten.
- [x] 6.3 The receipt-currency reservation is closed: the second receipt **postdates** the entry-point
      correction, and the first receipt's scope is re-stated as the immutable artefact only, with the
      mutable surfaces carried by the timestamped readback (12/12 PASS, quota clean).
- [x] 6.4 Evidence pack (machine-readable) written under the round's `evidence/` root, token-free.
- [ ] 6.5 `CORR-01..08` and the 12 TT rows each carry current truth, owner, disposition and trigger.
- [ ] 6.6 `DEL-018` recorded as `FAIL/EVIDENCE_GAP` with its three uncovered test paths (disclosed in the
      release body, README and preview notes; **not** closed).

## 7. Deferred / kept open (deliberately not closed)

- [ ] 7.1 `DEL-018 RELEASE_MANIFEST@1` full closure (routine packaging follow-up).
- [ ] 7.2 The 10 `S4_ACTIVE_GAP` SPEC/DEL rows.
- [ ] 7.3 The 19 `DEFERRED_BY_INSTRUCTION` rows.
- [ ] 7.4 S5–S8 live execution, PRE-W3, host-native certification, the 22 inactive technologies.
- [ ] 7.5 **CE-1 / CE-2 repair.** `validate` should resolve the wheel's own schemas the way `doctor`
      does; the `PI-PKG` member and `compile-pi`'s `_profile_meta` sidecar should agree. Either change
      moves member bytes, so the repair ships as a **superseding release**, never as a rewrite of
      `v0.1.0-preview.1`. Disposition (repair now vs accept for the preview) is the owner's.
