## 1. Governance surfaces (enabled for this change)

- [x] 1.1 Native prompt compiler executed over the round contract (`lint`, `activation`, `acceptance`,
      `compile`) — all four report `PROMPT_COMPILE_PASS`, `error_count=0`.
- [x] 1.2 HGK typed admission: every R5Q requirement reaches `FROZEN` with a TaskSpec/WorkOrder through
      `admit_requirement` / `checkpoint` (no raw SQL).
- [ ] 1.3 KANBAN board + SWARM graph created and read back for the round.
- [ ] 1.4 GSTACK route readback recorded.
- [ ] 1.5 This OpenSpec change created.

## 2. Licence landing (owner grant, `Apache-2.0`)

- [x] 2.1 `LICENSE` replaced with the verbatim Apache License 2.0 text; hash compared against the
      canonical ASF text.
- [x] 2.2 `NOTICE` created: material-class split, donor-plugin non-assertion, third-party components,
      exclusion policy.
- [x] 2.3 `OWNER_LICENSE_DECISION.yaml`: `decision: Apache-2.0`, with the superseded non-granting record
      preserved verbatim (not back-dated).
- [x] 2.4 `pyproject.toml` declares `license` / `license-files`.
- [x] 2.5 `SBOM.cdx.json`: project `Apache-2.0`; `jsonschema` corrected to `MIT`; licence basis updated.
- [x] 2.6 `PROVENANCE.md` gains the licence layer.
- [x] 2.7 FAR quick study recorded (FAR-PIPD-R5Q-LICENSE-001) with alternatives, criteria and the
      accepted cost of the choice.

## 3. Release candidate and distribution

- [ ] 3.1 Immutable release candidate commit frozen in an isolated worktree.
- [ ] 3.2 Wheel rebuilt from that commit; METADATA carries `License-Expression` + `License-File`; the
      licence text and NOTICE are packed inside the wheel.
- [ ] 3.3 `WHEEL_MANIFEST.json` records `build_input_commit`, a distinct released-commit binding, the
      licence and the licence files; the superseded wheel hash is not reused.
- [ ] 3.4 `SHA256SUMS` regenerated over the wheel and the source archive.

## 4. Verification against the actual published bytes

- [ ] 4.1 Deterministic suite re-run on the release tree.
- [ ] 4.2 Clean venv, no `PYTHONPATH`, outside the repository: install the wheel, `doctor` positive and
      missing-schema typed negative, 19-schema readback.
- [ ] 4.3 Design chain `intake → compile-pi → bind-pd → compile-ecp → compile-tqaep`, `validate`.
- [ ] 4.4 `project --dry-run` zero write; `project --out` to disposable scratch (5 Web + 3 Host + IR);
      `export --out` to scratch with recomputed archive / manifest / `SHA256SUMS`.
- [ ] 4.5 Licence consistency read out of the installed wheel's METADATA and packaged licences.

## 5. Publication and readback

- [ ] 5.1 Tag collision checked (no tag existed).
- [ ] 5.2 Immutable tag + GitHub prerelease created against the explicit release commit.
- [ ] 5.3 Assets attached (source archive, wheel, `SHA256SUMS`, preview notes).
- [ ] 5.4 Independent readback of repo / tag / commit / tree / release / assets and asset download hashes
      from a source that never used the local release cache.
- [ ] 5.5 Credential hygiene proven: no token value in argv, stdout, logs, evidence, prompt, git config or
      any asset.

## 6. Independent verification and evidence

- [ ] 6.1 Independent non-Maker checker (separate process, read-only) re-derives the decisive claims from
      the published subject.
- [ ] 6.2 Evidence pack (machine-readable) and human-readable master written under the private evidence
      root, token-free.
- [ ] 6.3 `CORR-01..08` and the 12 TT rows each carry current truth, owner, disposition and trigger.
- [ ] 6.4 `DEL-018` recorded as `FAIL/EVIDENCE_GAP` with its three uncovered test paths.

## 7. Deferred / kept open (deliberately not closed)

- [ ] 7.1 `DEL-018 RELEASE_MANIFEST@1` full closure (routine packaging follow-up).
- [ ] 7.2 The 10 `S4_ACTIVE_GAP` SPEC/DEL rows.
- [ ] 7.3 The 19 `DEFERRED_BY_INSTRUCTION` rows.
- [ ] 7.4 S5–S8 live execution, PRE-W3, host-native certification, the 22 inactive technologies.
