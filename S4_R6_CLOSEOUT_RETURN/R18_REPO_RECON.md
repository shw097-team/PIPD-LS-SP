# PIPD-LS-SP repository reconnaissance

- Subject checkout: `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`; HEAD `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba`; branch `fix/s4r6-closeout-doc-identity-and-update-route-20261016`. *(output: inventory probe, head and branch; exact invocation and raw output in §8)*
- Read-only reconnaissance; only the requested external `REPO_RECON.md` is authored. Build and publication commands below are quoted, NOT executed; the explicitly requested full unittest suite is executed. *(command: suite invocation in §3; output: inventory probe in §8)*

## 1. Top-level tree at HEAD

- Inventory uses `git ls-tree -r HEAD --name-only`, aggregated in Python; counts below are tracked files recursively under each immediate directory, not directory counts or a disk scan. *(command: inventory probe in §8)*
- `.agents/` — 7 tracked files. *(output: inventory probe, dirs)*
- `.github/` — 2 tracked files. *(output: inventory probe, dirs)*
- `.hermes/` — 6 tracked files. *(output: inventory probe, dirs)*
- `.hgk/` — 1491 tracked files. *(output: inventory probe, dirs)*
- `dist/` — 43 tracked files. *(output: inventory probe, dirs)*
- `docs/` — 22 tracked files. *(output: inventory probe, dirs)*
- `examples/` — 14 tracked files. *(output: inventory probe, dirs)*
- `fixtures/` — 76 tracked files. *(output: inventory probe, dirs)*
- `openspec/` — 54 tracked files. *(output: inventory probe, dirs)*
- `packaging/` — 7 tracked files. *(output: inventory probe, dirs)*
- `schemas/` — 20 tracked files. *(output: inventory probe, dirs)*
- `skills/` — 48 tracked files. *(output: inventory probe, dirs)*
- `src/` — 13 tracked files. *(output: inventory probe, dirs)*
- `tests/` — 55 tracked files. *(output: inventory probe, dirs)*
- `tools/` — 49 tracked files. *(output: inventory probe, dirs)*
- Root files: `.gitattributes`, `.gitignore`, `ACCEPTANCE.md`, `LICENSE`, `MANIFEST.in`, `NOTICE`, `OWNER_LICENSE_DECISION.yaml`, `PREVIEW_NOTES_v0.1.0-preview.1.md`, `PREVIEW_NOTES_v0.1.0-preview.2.md`, `PREVIEW_NOTES_v0.1.1-preview.3.md`, `PREVIEW_NOTES_v0.1.1-preview.4.md`, `PROVENANCE.md`, `README.md`, `SBOM.cdx.json`, `pyproject.toml`, `requirements.lock`, `setup.py`. *(output: inventory probe, roots)*

## 2. Python package and project declarations

- One declared package, `pipd_ls_sp`, under `src/`; package data declares `schemas/*.json`. *(pyproject.toml:46-53)*
- `src/pipd_ls_sp/__init__.py` — 8 physical lines; PIPD-LS-SP: Pre-Implementation & Pre-Dev Lifecycle Skills Plugin. *(output: inventory probe, package; src/pipd_ls_sp/__init__.py:1)*
- `src/pipd_ls_sp/cli.py` — 340 physical lines; `pipd` CLI - exactly the 13 commands of 總藍圖 §5.9.3 (exact-set, no 14th). *(output: inventory probe, package; src/pipd_ls_sp/cli.py:1)*
- `src/pipd_ls_sp/errors.py` — 148 physical lines; Typed failure codes for the 13-command PIPD-EC surface (總藍圖 §5.9.3). *(output: inventory probe, package; src/pipd_ls_sp/errors.py:1)*
- `src/pipd_ls_sp/export_bundle.py` — 241 physical lines; Portable export bundle: deterministic ``<name>.tar.gz`` + manifest + checksums. *(output: inventory probe, package; src/pipd_ls_sp/export_bundle.py:1)*
- `src/pipd_ls_sp/pipeline.py` — 380 physical lines; Deterministic PI -> PD -> ConstructionContract -> ECP/TQAEP pipeline. *(output: inventory probe, package; src/pipd_ls_sp/pipeline.py:1)*
- `src/pipd_ls_sp/profiles.py` — 91 physical lines; Profile trio: LITE / STANDARD / ASSURED over one canonical truth (總藍圖 §7.3 #04). *(output: inventory probe, package; src/pipd_ls_sp/profiles.py:1)*
- `src/pipd_ls_sp/projection.py` — 1836 physical lines; Typed surface projection IR: Web pack + host projections compiled from canonical sources. *(output: inventory probe, package; src/pipd_ls_sp/projection.py:1)*
- `src/pipd_ls_sp/registry.py` — 198 physical lines; Canonical machine-contract registry (exact 19/19, 總藍圖 §7.3). *(output: inventory probe, package; src/pipd_ls_sp/registry.py:1)*
- `src/pipd_ls_sp/repo_context.py` — 228 physical lines; Repository/host probes for PD late binding (R-AUD-009 / CAP_PD_LATE_BINDING). *(output: inventory probe, package; src/pipd_ls_sp/repo_context.py:1)*
- `src/pipd_ls_sp/requirements.py` — 332 physical lines; Clause-bound atomic requirement compiler (R-AUD-005 / CAP_ATOMIC_REQUIREMENT_COMPILER). *(output: inventory probe, package; src/pipd_ls_sp/requirements.py:1)*
- `src/pipd_ls_sp/util.py` — 42 physical lines; Deterministic primitives: canonical JSON, content-addressed ids, hashing. *(output: inventory probe, package; src/pipd_ls_sp/util.py:1)*
- `src/pipd_ls_sp/validate.py` — 294 physical lines; Deterministic validation: schema + semantic invariants over the 19 families. *(output: inventory probe, package; src/pipd_ls_sp/validate.py:1)*
- `src/pipd_ls_sp/workspace.py` — 336 physical lines; Workspace bootstrap, portable export, projection, doctor, diff, repair. *(output: inventory probe, package; src/pipd_ls_sp/workspace.py:1)*
- Distribution name `pipd-ls-sp`; version `0.1.1a4`; Python `>=3.11`; runtime dependency `jsonschema>=4.0`; licence `Apache-2.0`, licence files `LICENSE`, `NOTICE`. *(pyproject.toml:1-8)*
- Console entry point: `pipd = "pipd_ls_sp.cli:main"`. *(pyproject.toml:24-25)*
- Optional `test` dependencies: `pyyaml>=6.0`, `build>=1.2`, `setuptools>=68`, `wheel`; CI installs `python -m pip install -e ".[test]"`. *(pyproject.toml:10-22; .github/workflows/ci.yml:34-45)*
- Build backend `setuptools.build_meta`, build requirement `setuptools>=68`. *(pyproject.toml:27-29)*
- Dedicated unittest/pytest/coverage configuration in pyproject: ABSENT; its only `tool` configuration is `tool.setuptools`. Test discovery is declared in CI instead. *(output: inventory probe, pyproject; .github/workflows/ci.yml:54-56)*

## 3. Test layout, exact CI invocation, and fresh full-suite result

- 51 `tests/test_*.py` modules; `tests/__init__.py` makes the tree importable; three additional corpus files live under `tests/fixtures/quarantine_corpus/`. *(output: inventory probe, tests)*
- Tests span pipeline and atomic requirements, schema/registry, CLI typed refusals, packaging/wheel resources, web/host projections, trace closure, provenance/install documentation guards, security/rollback, performance, evidence tooling, and skill contracts (classification inferred from filenames). *(output: inventory probe, tests)*
- `tests/test_atomic_requirements.py` *(output: inventory probe, tests)*
- `tests/test_ce_repair_regression.py` *(output: inventory probe, tests)*
- `tests/test_claim_ceiling_shape.py` *(output: inventory probe, tests)*
- `tests/test_cli_typed_errors.py` *(output: inventory probe, tests)*
- `tests/test_deny_list_scan.py` *(output: inventory probe, tests)*
- `tests/test_doctor_schema_truth.py` *(output: inventory probe, tests)*
- `tests/test_evidence_manifest.py` *(output: inventory probe, tests)*
- `tests/test_evidence_md_guards.py` *(output: inventory probe, tests)*
- `tests/test_export_bundle.py` *(output: inventory probe, tests)*
- `tests/test_first_run_examples.py` *(output: inventory probe, tests)*
- `tests/test_git_object_reader.py` *(output: inventory probe, tests)*
- `tests/test_host_projection.py` *(output: inventory probe, tests)*
- `tests/test_negative_and_rollback.py` *(output: inventory probe, tests)*
- `tests/test_oracle_disagreement.py` *(output: inventory probe, tests)*
- `tests/test_perf_budget.py` *(output: inventory probe, tests)*
- `tests/test_pi_dedup.py` *(output: inventory probe, tests)*
- `tests/test_postrelease_contract_hardening.py` *(output: inventory probe, tests)*
- `tests/test_postrelease_quickstart.py` *(output: inventory probe, tests)*
- `tests/test_postrelease_selfbootstrap.py` *(output: inventory probe, tests)*
- `tests/test_postrelease_web_mount.py` *(output: inventory probe, tests)*
- `tests/test_preflight_check.py` *(output: inventory probe, tests)*
- `tests/test_project_destination_safety.py` *(output: inventory probe, tests)*
- `tests/test_public_plugin_packaging.py` *(output: inventory probe, tests)*
- `tests/test_publication_projection.py` *(output: inventory probe, tests)*
- `tests/test_quarantine_review.py` *(output: inventory probe, tests)*
- `tests/test_r10_bclass_evidence.py` *(output: inventory probe, tests)*
- `tests/test_r5r3_install_route_identity.py` *(output: inventory probe, tests)*
- `tests/test_r6_doc_identity_guard.py` *(output: inventory probe, tests)*
- `tests/test_round_envelope.py` *(output: inventory probe, tests)*
- `tests/test_round_selfscan.py` *(output: inventory probe, tests)*
- `tests/test_s0_contracts.py` *(output: inventory probe, tests)*
- `tests/test_s1_lite_slice.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_artifact_reproducibility.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_first_run_portable.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_profile_boundaries.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_release_provenance.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_spec_del_adjudication.py` *(output: inventory probe, tests)*
- `tests/test_s4ext_trace_closure.py` *(output: inventory probe, tests)*
- `tests/test_s4r2_affected_only.py` *(output: inventory probe, tests)*
- `tests/test_s4r2m_docs_route.py` *(output: inventory probe, tests)*
- `tests/test_secret_patterns.py` *(output: inventory probe, tests)*
- `tests/test_skill_contracts.py` *(output: inventory probe, tests)*
- `tests/test_spec_del_crosswalk.py` *(output: inventory probe, tests)*
- `tests/test_standard_wheel_schemas.py` *(output: inventory probe, tests)*
- `tests/test_technology_admission.py` *(output: inventory probe, tests)*
- `tests/test_tooling_executes.py` *(output: inventory probe, tests)*
- `tests/test_tqaep_design_positive.py` *(output: inventory probe, tests)*
- `tests/test_tt_summary.py` *(output: inventory probe, tests)*
- `tests/test_web_fallback.py` *(output: inventory probe, tests)*
- `tests/test_web_pack.py` *(output: inventory probe, tests)*
- `tests/test_wheel_distribution.py` *(output: inventory probe, tests)*

Raw excerpt *(.github/workflows/ci.yml:47-56)*

```yaml
47:       - name: Full unittest suite (raw log)
48:         # FALSE-GREEN REPAIR (S4R3-F001): this step previously ran
49:         # `python -m unittest ... 2>&1 | tee full-unittest.log`. A pipeline's exit status is the LAST
50:         # command's, so `tee` succeeded and the step passed while the log itself read
51:         # "FAILED (failures=11, skipped=6)". `set -o pipefail` makes the step carry the suite's own
52:         # exit code, so a red suite is a red job. Do NOT remove it, and do not "fix" a red suite by
53:         # narrowing the denominator or skipping files.
54:         run: |
55:           set -euo pipefail
56:           python -m unittest discover -s tests -t . -v 2>&1 | tee full-unittest.log
```

- The other workflow uses the same full-suite command and pipefail; `-v` plus raw-log piping are CI presentation differences from the requested local run below. *(.github/workflows/public-plugin-verify.yml:385-391)*

Raw excerpt *(command: actual full-suite command)*

```bash
cd C:/Projects/Agent_Workspace/PIPD-S4R6-wt && PYTHONDONTWRITEBYTECODE=1 C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -m unittest discover -s tests -t .
```


Raw excerpt *(command: actual wrapper, process proc_dd31a6e076ff)*

```bash
cd C:/Projects/Agent_Workspace/PIPD-S4R6-wt && PYTHONDONTWRITEBYTECODE=1 C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -m unittest discover -s tests -t .; suite_status=$?; printf '\nSUITE_EXIT_CODE=%s\n' "$suite_status"; git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt status --porcelain; status_code=$?; printf 'STATUS_EXIT_CODE=%s\n' "$status_code"; exit "$suite_status"
```


Raw excerpt *(output: process proc_dd31a6e076ff completed, exit_code=0; exact test-summary/status tail)*

```text
----------------------------------------------------------------------
Ran 633 tests in 180.325s

OK (skipped=4)

SUITE_EXIT_CODE=0
?? openspec/changes/pipd-r18-external-engineering-handover/
STATUS_EXIT_CODE=0
```

- Fresh full suite: 633 tests in 180.325s; `OK (skipped=4)`; process/suite exit code 0. The four skips remain part of the result, not erased into an unqualified all-tests-executed claim. Intermediate `FAIL`/`HIT` strings in fixture output are not the suite verdict. *(output: process proc_dd31a6e076ff, completed test summary)*
- Initial porcelain output was empty. Immediately after the suite the tree was NOT clean: one untracked directory `openspec/changes/pipd-r18-external-engineering-handover/`. A later status read showed the same directory and HEAD remained `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba`. No tracked changes were listed. *(output: initial prerequisite probe; output: process proc_dd31a6e076ff; output: final HEAD/status probe)*
- That directory appeared during the audit interval; three files were observed (`proposal.md`, `tasks.md`, `specs/pipd-round-handover-entry/spec.md`). This child did not create them. Attribution to tests versus a concurrent writer is NOT ESTABLISHED; no cleanup or restore was attempted under the read-only rule. *(output: post-suite path probe below)*
- A non-fatal `ResourceWarning` reports an unclosed file when `build_s4_spec_del_adjudication.py:223` reads `docs/SPEC_DEL_CROSSWALK.json`; unittest nevertheless ended OK. *(output: process proc_dd31a6e076ff; tools/build_s4_spec_del_adjudication.py:223)*


## 4. Build and packaging tooling

- `tools/` has 49 tracked files; descriptions below come from module docstrings / shell headers unless explicitly labelled as a body inference. *(output: inventory probe, tools)*
- `tools/admit_technologies.py` — S0/S1 — materialise the 22 source-designated Technology Admission rulings (PKG-00 §9). *(tools/admit_technologies.py:2)*
- `tools/build_bclass_artifacts.py` — Materialise the two R10 SSOT artefacts that were adjudicated BUILDABLE-FAITHFULLY. *(tools/build_bclass_artifacts.py:2)*
- `tools/build_dist.py` — S3 portable distribution: build a real, standards-shaped wheel + sdist-like bundle, with checksums. *(tools/build_dist.py:2)*
- `tools/build_evidence_manifest.py` — Build, seal and verify the evidence manifest (R-AUD-014 / WO-TS-req-pipd-r3-fw-11). *(tools/build_evidence_manifest.py:2)*
- `tools/build_evidence_md.py` — Assemble the single-file external acceptance evidence MD from the frozen receipts. *(tools/build_evidence_md.py:2)*
- `tools/build_evidence_md_r2.py` — Build the single external acceptance evidence MD for the S0-S4 continuation round. *(tools/build_evidence_md_r2.py:2)*
- `tools/build_mount_pack.py` — WO-S4-WEB-02: build and verify the one versioned Web/ChatGPT mount pack. *(tools/build_mount_pack.py:2)*
- `tools/build_public_plugin.py` — S4POST Stage B: build the deterministic, fail-closed public Skills-only plugin candidate. *(tools/build_public_plugin.py:2)*
- `tools/build_publication_manifest.py` — Publication projection manifest (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-006, R-AUD-014). *(tools/build_publication_manifest.py:2)*
- `tools/build_requirements_lock.py` — Write requirements.lock - the resolved runtime closure of this project, pinned exactly. *(tools/build_requirements_lock.py:2)*
- `tools/build_s4_spec_del_adjudication.py` — TT-S4EXT-007 -- S4-active SPEC/DEL row adjudication (deterministic generator). *(tools/build_s4_spec_del_adjudication.py:2)*
- `tools/build_s5_s8_backlog.py` — S4 -> S5..S8 typed integration seams. *(tools/build_s5_s8_backlog.py:2)*
- `tools/build_spec_del_crosswalk.py` — Build / check the 32 SPEC + 25 DEL crosswalk from live repo objects. *(tools/build_spec_del_crosswalk.py:2)*
- `tools/build_web_fallback.py` — S4POST Stage B: project one frozen Web mount pack into ONE bounded fallback document. *(tools/build_web_fallback.py:2)*
- `tools/cli_smoke.py` — Run all 13 pipd commands end to end and freeze the raw receipts. *(tools/cli_smoke.py:2)*
- `tools/cli_surface_check.py` — Qualify all 13 CLI commands with success and typed-failure paths (header). *(tools/cli_surface_check.py:2)*
- `tools/deny_list_scan.py` — Classify every `danger-full-access` occurrence as a POLICY_MENTION or a WRITER_USAGE (R4 / W9). *(tools/deny_list_scan.py:2)*
- `tools/edge_selfcheck.py` — Local pre-check of the E1..E12 edge probes. *(tools/edge_selfcheck.py:2)*
- `tools/freeze_public_plugin_source.py` — S4POST Stage B: freeze the eight public skill packs into a source ledger. *(tools/freeze_public_plugin_source.py:2)*
- `tools/github_publish.py` — Publish the frozen PIPD-LS-SP candidate to GitHub as a public repo. *(tools/github_publish.py:2)*
- `tools/hgk_admission_driver.py` — Drive the HG-KSEOS normal lifecycle admission chain for PIPD-LS-SP. *(tools/hgk_admission_driver.py:2)*
- `tools/history_secret_scan.py` — Scan BOTH the working tree and the git history for token-like strings (R-AUD-014 / FW-11). *(tools/history_secret_scan.py:2)*
- `tools/host_projection_check.py` — G-S3-HOST gate — FW-06 / R-AUD-004 / R-AUD-015, real semantic checks. *(tools/host_projection_check.py:2)*
- `tools/kanban_canonical_complete.py` — Drive the canonical PIPD-LS-SP board: complete the closed gates with real receipts. *(tools/kanban_canonical_complete.py:2)*
- `tools/kanban_canonical_ids.sh` — Complete the canonical-board gate cards with real CLI receipts. *(tools/kanban_canonical_ids.sh:2)*
- `tools/kanban_complete_early.sh` — Complete the gates whose work is actually finished (ancestors first). *(tools/kanban_complete_early.sh:4)*
- `tools/kanban_complete_s0s1.sh` — ABSENT descriptive header; body claims/completes S0/S1, execution-surface and rollback gate cards (inferred from body). *(tools/kanban_complete_s0s1.sh:9-16)*
- `tools/kanban_dag.sh` — PIPD-LS-SP gate DAG creation + evidence receipts *(tools/kanban_dag.sh:4)*
- `tools/kanban_round.sh` — PIPD-LS-SP governed round: Kanban board + gate DAG (real CLI receipts) *(tools/kanban_round.sh:4)*
- `tools/knowledge_ready_probe.py` — G-KNOWLEDGE-READY probe for PIPD-LS-SP. *(tools/knowledge_ready_probe.py:2)*
- `tools/perf_budget.py` — S2 performance + context budget. Measures real wall-clock work; declares the budget it holds to. *(tools/perf_budget.py:2)*
- `tools/pi_dedup_check.py` — Measure the PI source-clause de-duplication honestly, raw-first (R4 / W5, repaired by W9). *(tools/pi_dedup_check.py:2)*
- `tools/portable_install_check.py` — S3 + R5-DIST-002: real install / self-sufficiency / uninstall lifecycle in an ISOLATED env (L5). *(tools/portable_install_check.py:2)*
- `tools/preflight_check.py` — Preflight check for the PIPD governed lane. *(tools/preflight_check.py:2)*
- `tools/publication_attestation.py` — Immutable publication-subject attestation (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-014). *(tools/publication_attestation.py:2)*
- `tools/quarantine_review.py` — G-KNOWLEDGE-READY — quarantine review path + R3 per-source owner disposition (R-AUD-008). *(tools/quarantine_review.py:2)*
- `tools/registry_reconcile.py` — Single-source reconciliation of schemas/registry.json FROM the schema files. *(tools/registry_reconcile.py:2)*
- `tools/replay_check.py` — S4 replay identity: the same input lock must reproduce the same artefacts byte for byte. *(tools/replay_check.py:2)*
- `tools/round_envelope.py` — S2 verifier envelope: a disposable byte-copy, a per-file snapshot, a three-way delta guard. *(tools/round_envelope.py:2)*
- `tools/round_selfscan.py` — Round self-scan: a credential-shape sweep folded together with the deny-list gate. *(tools/round_selfscan.py:2)*
- `tools/run_golden_pilots.py` — S2 golden pilots — really execute the lifecycle on three profiles. *(tools/run_golden_pilots.py:2)*
- `tools/run_nrtv_judge.py` — S2 NRTV + NEG + SEC + oracle/judge calibration. *(tools/run_nrtv_judge.py:2)*
- `tools/run_r3_qualification.py` — FW-09 (audit finding R-AUD-010): re-qualify the pilots and the 13-command CLI. *(tools/run_r3_qualification.py:2)*
- `tools/run_s1_slice.py` — Run the S1 LITE vertical slice and freeze its artifacts as raw evidence. *(tools/run_s1_slice.py:2)*
- `tools/skill_pack_check.py` — skill_pack_check — discover -> load -> route checker for the 8 PIPD SkillContract packs. *(tools/skill_pack_check.py:2)*
- `tools/tt_summary_check.py` — TT status projection — recompute the TT register summary from `tts[]` only. *(tools/tt_summary_check.py:2)*
- `tools/verify_evidence_digests.py` — Recompute the per-entry sha256 recorded in the evidence manifest against the bytes on disk. *(tools/verify_evidence_digests.py:2)*
- `tools/verify_installed_wheel_registry.py` — Assert that an INSTALLED wheel resolved its OWN packaged contract registry (S4R3-F006). *(tools/verify_installed_wheel_registry.py:2)*
- `tools/web_pack_check.py` — G-S3-WEB gate — FW-05 / R-AUD-003 / R-AUD-015, real semantic checks. *(tools/web_pack_check.py:2)*

### Wheel routes

- Standard CI build installs `build`, builds exactly one wheel in `$RUNNER_TEMP/wheels`, installs it into a new venv, changes out of the source checkout, and runs installed `pipd doctor` / `--help`; a subsequent verifier requires 19 families and rejects source-prefix registry resolution. *(.github/workflows/ci.yml:63-105)*

Raw excerpt *(.github/workflows/ci.yml:74-84)*

```bash
74:           set -euo pipefail
75:           python -m pip install build
76:           rm -rf "$RUNNER_TEMP/wheels" && mkdir -p "$RUNNER_TEMP/wheels"
77:           python -m build --wheel --outdir "$RUNNER_TEMP/wheels"
78:           ls -l "$RUNNER_TEMP/wheels"
79:           python -m venv "$RUNNER_TEMP/wheelvenv"
80:           "$RUNNER_TEMP/wheelvenv/bin/python" -m pip install --upgrade pip
81:           "$RUNNER_TEMP/wheelvenv/bin/python" -m pip install "$RUNNER_TEMP"/wheels/*.whl
82:           cd "$RUNNER_TEMP"
83:           "$RUNNER_TEMP/wheelvenv/bin/pipd" doctor | tee "$GITHUB_WORKSPACE/wheel-doctor.log"
84:           "$RUNNER_TEMP/wheelvenv/bin/pipd" --help | tee "$GITHUB_WORKSPACE/wheel-cli-help.log"
```

- Offline/manual route: `tools/build_dist.py` hand-builds a PEP 427 wheel including the canonical schemas and licence files; its `main()` invokes `build_wheel()` and writes a wheel manifest and checksum. The executable invocation inferred from its main guard is `python tools/build_dist.py` (not run in this read-only audit). *(tools/build_dist.py:2-14; tools/build_dist.py:197-216)*
- The backend build maps the root `schemas/` tree into build output via self-contained `setup.py:build_py`; it refuses missing/undeclared schemas and byte drift, and never mirrors into the source directory; `MANIFEST.in` includes schemas for sdist builds. *(setup.py:15-27; setup.py:120-134; MANIFEST.in:1-7)*

### Public Skills-only plugin ZIP

- `freeze_public_plugin_source.py` produces a ledger; `build_public_plugin.py` requires ledger/source identity, packaging manifests and approved per-skill derivations, and writes a deterministic ZIP candidate outside the repository. `--generate-icons` writes packaging assets, so this option is NOT read-only and was not run. *(tools/freeze_public_plugin_source.py:2; tools/build_public_plugin.py:20-45)*

Raw excerpt *(README.md:64-79)*

```text
64: The plugin ZIP is reproducible. Run from the frozen R5Y worktree at commit
65: `062d84ae3e951d02b2ba6bb732359b18799d2864`:
66: 
67: ```bash
68: python tools/freeze_public_plugin_source.py --repo-root . --out ledger.json
69: python tools/build_public_plugin.py --ledger ledger.json --source-commit 062d84ae3e951d02b2ba6bb732359b18799d2864 \
70:   --packaging-root packaging/public-plugin --out-dir out --generate-icons
71: ```
72: 
73: This reproduces the **historical R5Y build**: `out/pipd-ls-sp-public-skills.zip` — **68,355 bytes**,
74: sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, **56 entries**, **8 `SKILL.md`**
75: — the bytes frozen at `062d84ae3e951d02b2ba6bb732359b18799d2864` and attached to the R5Y evidence return.
76: Those bytes are **superseded as a download**: the artefact a user installs is the `v0.1.1-preview.4`
77: release asset `pipd-ls-sp-public-skills.zip` — **68,357 bytes**, sha256
78: `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`, 56 entries, 8 `SKILL.md`. Two
79: independent builds are byte-identical. A local packager PASS is not portal approval.
```

- The quoted command is explicitly the historical R5Y reproduction at `062d84ae3e951d02b2ba6bb732359b18799d2864`, not a claim that building this HEAD recreates the preview.4 release ZIP. Historical output is 68,355 bytes; documented preview.4 asset is 68,357 bytes. *(README.md:64-79)*
- The local ZIP builder is fail-closed and stdlib-only; `plugin.json` is the official manifest, while `plugin.release.json` bookkeeping is duplicated under `extensions["com.pipd.s4"]` and must agree. Its ceiling is `LOCAL_PACKAGER_PASS_ONLY`, not portal verification/publication. *(tools/build_public_plugin.py:2-18; docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md:47-57)*

## 5. CI workflows and stage-aware write-set classifier


### `.github/workflows/ci.yml`

- Triggers: every `push` and `pull_request`, with no branch/path filters; permission `contents: read`; sole job `offline-gate`, Ubuntu 24.04, Python 3.11, 20-minute timeout. *(.github/workflows/ci.yml:7-32)*
- Preparation steps: check out full history without persisting credentials; set up Python 3.11; install declared `[test]` dependencies and record the resolved environment. *(.github/workflows/ci.yml:23-45)*
- Test steps: full discovery and focused `test_s4ext_*.py` suites, both preserving test failures through `set -euo pipefail` and keeping raw logs. *(.github/workflows/ci.yml:47-61)*
- Packaging steps: build/install the new wheel in isolation, run its CLI, then verify the doctor log resolves the installed package’s own 19-family registry instead of source resources. *(.github/workflows/ci.yml:63-105)*
- Provenance/receipt steps: establish a green provenance suite, tamper with a mount-pack identity and require real identity/byte-binding test failures, restore the fixture, and upload logs even on failure. These mutation steps are described only, NOT replayed by this audit. *(.github/workflows/ci.yml:107-162)*

### `.github/workflows/public-plugin-verify.yml`

- Triggers: path-filtered `pull_request` and unfiltered manual `workflow_dispatch`; sole job `verify`, Ubuntu 24.04, 20-minute timeout, Python 3.11; `contents: read`. PR filters are trigger conditions, NOT the write allowlist. *(.github/workflows/public-plugin-verify.yml:13-15; .github/workflows/public-plugin-verify.yml:17-66)*

Raw excerpt *(.github/workflows/public-plugin-verify.yml:17-44)*

```yaml
17: on:
18:   pull_request:
19:     paths:
20:       - ".github/workflows/public-plugin-verify.yml"
21:       - "README.md"
22:       - "docs/install/**"
23:       - "docs/USER_GUIDE.md"
24:       - "docs/RELEASE_TUPLE.json"
25:       - "packaging/public-plugin/**"
26:       - "tools/freeze_public_plugin_source.py"
27:       - "tools/build_public_plugin.py"
28:       - "tools/build_web_fallback.py"
29:       - "tests/test_public_plugin_packaging.py"
30:       - "tests/test_web_fallback.py"
31:       - "dist/mount/**"
32:       # Source-repair rounds: without these, a PR that only repairs the compiler or the schemas would
33:       # not run this gate at all, so the write-set declaration would be unenforced exactly where it
34:       # matters most.
35:       - "src/**"
36:       - "schemas/**"
37:       - "tests/**"
38:       - "fixtures/**"
39:       - "pyproject.toml"
40:       - "tools/build_dist.py"
41:   workflow_dispatch:
42: 
43: permissions:
44:   contents: read
```

- Preparation/scope steps: full-history checkout without credentials, Python setup, then classify the declared stage’s diff against its own base (not the PR base), require base ancestry, reject traversal and denied/unlisted paths, and exercise planted positive/negative controls. *(.github/workflows/public-plugin-verify.yml:55-68; .github/workflows/public-plugin-verify.yml:201-302)*
- Upgrade steps: byte-compile the three tools, AST-check their and two test modules’ imports against stdlib/own modules, then run `tests.test_public_plugin_packaging` and `tests.test_web_fallback` before installing dependencies. *(.github/workflows/public-plugin-verify.yml:304-370)*
- Project steps: install `.[test]`, record the resolved dependencies, and run the full unittest suite with fail-preserving log capture. The install step’s name says runtime-only, but its actual payload includes test extras. *(.github/workflows/public-plugin-verify.yml:372-391)*
- Negative/receipt steps: require identity-binding failures after pack-document mutation; require `REFUSED MANIFEST_DIGEST_MISMATCH` after copied-pack byte mutation; upload all raw logs even after failure. These mutation/build steps were NOT replayed here. *(.github/workflows/public-plugin-verify.yml:393-517)*

### Declared stage and exact classifier declarations


Raw excerpt *(.github/workflows/public-plugin-verify.yml:122-132)*

```yaml
122:           STAGE: stage-c
123:           # Stage A's declared base: the frozen R3 subject the external acceptance report examined.
124:           STAGE_A_BASE_SHA: e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
125:           # Stage B's declared base: the Stage A tip that Stage B is stacked on. Taken by ref so it
126:           # does not need editing every time the Stage A tip moves; the sha it resolves to is printed
127:           # below and is the value an auditor should cite.
128:           STAGE_B_BASE_REF: fix/s4r3-stage-a-ci-truthfulness-20261013
129:           # Stage C's declared base: the frozen S4-R5 subject, taken as a literal because it is a
130:           # merged main commit and therefore immutable.
131:           STAGE_C_BASE_SHA: f4021aeff9c016cfb14f17e68a0c570ed4e825c5
132:           PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
```


Raw excerpt *(.github/workflows/public-plugin-verify.yml:191-194)*

```bash
191:               ALLOWED='^(src/pipd_ls_sp/|schemas/|tests/|fixtures/|pyproject\.toml$|tools/build_dist\.py$|dist/|README\.md$|docs/install/|docs/USER_GUIDE\.md$|docs/RELEASE_TUPLE\.json$|PREVIEW_NOTES_v0\.1\.1-preview\.4\.md$|\.github/workflows/public-plugin-verify\.yml$)'
192:               DENIED='^(skills/|packaging/public-plugin/)'
193:               REFUSED_PLANTS='skills/pipd-core/SKILL.md packaging/public-plugin/plugin.json src/other_package/thing.py tools/build_public_plugin.py'
194:               ALLOWED_PLANTS='src/pipd_ls_sp/requirements.py schemas/ClaimCeiling.schema.json tests/test_claim_ceiling_shape.py fixtures/REQ-NEG-PHRASES/source.txt dist/pipd_ls_sp-0.1.1a4-py3-none-any.whl README.md docs/install/README.md docs/RELEASE_TUPLE.json docs/USER_GUIDE.md'
```

- The planted-path list variable names are `REFUSED_PLANTS` and `ALLOWED_PLANTS`; traversal examples are a separate inline list. `.hgk/` is excluded by declaration (`EXCLUDED_PREFIXES='^\.hgk/'`), counted and printed, NOT allowed as product scope. *(.github/workflows/public-plugin-verify.yml:193-205; .github/workflows/public-plugin-verify.yml:265-297)*
- The declared arm is `stage-c`, which allows source/schema/dist repairs but denies `skills/` and `packaging/public-plugin/`; do not apply stage-b’s stricter denial of `src/`, `schemas/`, `dist/` to this branch. The file acknowledges stage is branch-declared and its control therefore also depends on review of the amendment. *(.github/workflows/public-plugin-verify.yml:159-175; .github/workflows/public-plugin-verify.yml:191-194)*

## 6. Documentation entry points

- `docs/ERRATUM_2026-10-12_preview3_release_provenance.md` — Preview.3 mount identity defect, source correction and served-asset replacement history. *(docs/ERRATUM_2026-10-12_preview3_release_provenance.md:1-8)*
- `docs/FRONT_PAGE_HISTORY.md` — Preserved historical front-page sections, not a current-state manual. *(docs/FRONT_PAGE_HISTORY.md:1-8)*
- `docs/NORMATIVE_SOURCE_MAP.md` — Derived index of normative source families, identity/digest locators and consumers; external standard remains authoritative. *(docs/NORMATIVE_SOURCE_MAP.md:1-8)*
- `docs/OWNER_ADJUDICATION_R4_2026-10-09.json` — Machine-readable owner rulings for the R4 focused-repair round. *(docs/OWNER_ADJUDICATION_R4_2026-10-09.json:1-8)*
- `docs/OWNER_ADJUDICATION_R4_2026-10-09.md` — Human-readable companion to R4 owner rulings. *(docs/OWNER_ADJUDICATION_R4_2026-10-09.md:1-8)*
- `docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json` — Owner rulings for R5/S4 operability and context-budget definition. *(docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json:1-18)*
- `docs/RELEASE_TUPLE.json` — Release/tag/build-source identities and served-asset digests; see §7. *(docs/RELEASE_TUPLE.json:1-8)*
- `docs/ROUND3_DISCLOSURE.md` — Historical R3 lane, execution and defect disclosures. *(docs/ROUND3_DISCLOSURE.md:1-8)*
- `docs/ROUND_DISCLOSURE.md` — Historical governed-round anomalies, including profile escalation and writer sandbox disclosure. *(docs/ROUND_DISCLOSURE.md:1-8)*
- `docs/S0_CONTRACT_SPEC.md` — Contract-family floor, 19/19 schema identities and single-source reconciliation rules. *(docs/S0_CONTRACT_SPEC.md:1-18; docs/S0_CONTRACT_SPEC.md:63-91)*
- `docs/S4_SPEC_DEL_ADJUDICATION.json` — S4-active SPEC/DEL dispositions, evidence gaps and claim ceiling. *(docs/S4_SPEC_DEL_ADJUDICATION.json:1-8)*
- `docs/SPEC_DEL_CROSSWALK.json` — 32 SPEC + 25 DEL source-to-evidence crosswalk. *(docs/SPEC_DEL_CROSSWALK.json:1-8)*
- `docs/USER_GUIDE.md` — Task-first user manual, linking install/version details to the install SSOT. *(docs/USER_GUIDE.md:1-8)*
- `docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md` — Official root manifest, embedded release bookkeeping, approved derivations and local-validation limits. *(docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md:1-8)*
- `docs/adr/ADR-0007-plugin-distribution-private-first.md` — Private-first distribution decision; public directory remains owner-gated. *(docs/adr/ADR-0007-plugin-distribution-private-first.md:1-8)*
- `docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md` — Historical branch/PR inventory and evidence-preservation/hygiene policy. *(docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md:1-8)*
- `docs/adr/ADR-0009-session-handover-and-next-session-start.md` — Session closeout/start protocol, historical state, owner decisions and reproducibility commands. *(docs/adr/ADR-0009-session-handover-and-next-session-start.md:9-23)*
- `docs/install/ASSET_READBACK_v0.1.1-preview.4.json` — Repository-side record of release-asset downloads/digest comparisons, not itself a release asset. *(docs/install/ASSET_READBACK_v0.1.1-preview.4.json:1-8)*
- `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` — Copy/paste agent install prompt requiring host identity, approval, discovery and load evidence. *(docs/install/PIPD_AGENT_INSTALL_PROMPT.md:1-8)*
- `docs/install/PIPD_WEB_FALLBACK.md` — Single-document `DOC_MOUNT_ONLY` Web fallback; its header retains preview.3 mount provenance. *(docs/install/PIPD_WEB_FALLBACK.md:1-8)*
- `docs/install/PIPD_WEB_FALLBACK.md.sha256` — SHA-256 sidecar for the committed Web fallback document. *(docs/install/PIPD_WEB_FALLBACK.md.sha256:1-8)*
- `docs/install/README.md` — Installation SSOT: Web and Agent routes, pins, ceilings, verification/uninstall/rollback. *(docs/install/README.md:1-8)*
- First six lines of root README follow verbatim (line-number prefix is the inspection output, not file content). *(README.md:1-6)*

Raw excerpt *(README.md:1-6)*

```text
1: # PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin
2: 
3: A governed, contract-first toolkit for the **pre-implementation** stage of a project: it turns a
4: stated intent into a validated chain of machine-readable artefacts — PI → PD →
5: ConstructionContract → ECP / TQAEP — each bound to one of **19 canonical JSON Schema families**,
6: and it refuses to hand you something it cannot check. It ships **8 skills** and a **13-command
```


## 7. `docs/RELEASE_TUPLE.json` schema and release identities

- Schema identifier `PIPD-RELEASE-TUPLE/1`; top-level keys: `schema`, `purpose`, `field_semantics`, `verification_commands`, `releases`, `authority_note`. *(docs/RELEASE_TUPLE.json:1-17; docs/RELEASE_TUPLE.json:84)*
- Observed union of per-release keys (NOT a statement that every entry has every key): `asset_list_source`, `asset_replaced_in_place`, `asset_replacement_record`, `build_source_commit`, `build_source_scope`, `erratum_doc`, `first_shipped_asset_sha256`, `note`, `pack_dir`, `published_asset_name`, `published_asset_sha256`, `release_id`, `release_tag_target`, `served_assets`, `served_assets_coverage`, `stale_identity_in_first_shipped_asset`, `status`, `superseded_candidate_note`, `superseded_candidate_zip`, `tag_object`, `tree`, `zip`. *(output: inventory probe, release_keys; docs/RELEASE_TUPLE.json:18-81)*
- Release entry `v0.1.0-preview.1`. *(docs/RELEASE_TUPLE.json:19)*
- Release entry `v0.1.0-preview.2`. *(docs/RELEASE_TUPLE.json:30)*
- Release entry `v0.1.1-preview.3`. *(docs/RELEASE_TUPLE.json:41)*
- Release entry `v0.1.1-preview.4`. *(docs/RELEASE_TUPLE.json:59)*
- Keep `tag_object`, `release_tag_target`, `build_source_commit`, release-target `tree`, and served `published_asset_sha256` distinct; first two historical tags use the same object/target values, and preview.1 is explicitly `LIGHTWEIGHT_TAG_NO_PACK`. *(docs/RELEASE_TUPLE.json:4-9; docs/RELEASE_TUPLE.json:19-38)*
- Preview.4: tag object `0618d73c725da0d8c3280f99ef369d13741b5197`; release target `cc6c1930765160697e7e51d6e37735b9220a30db`; build source `4754d92cc98c0c02b59bf9700d08c0b7bf452e3d` is scoped ONLY to the wheel, not the plugin ZIP. `pack_dir` and `zip` are deliberately null. *(docs/RELEASE_TUPLE.json:59-80)*
- Preview.4 `served_assets` records all seven assets, including `SHA256SUMS` itself; this is a local record of the download/hash comparison, not a fresh network re-verification performed by this audit. *(docs/RELEASE_TUPLE.json:68-81; docs/install/ASSET_READBACK_v0.1.1-preview.4.json:2-6)*
- Preview.3 records the first-shipped digest, replacement served digest, in-place replacement and erratum; its immutable tag still contains the pre-correction pack, so tag-tree rebuild versus served asset is a documented remaining distinction, not silently equated. *(docs/RELEASE_TUPLE.json:41-56; docs/RELEASE_TUPLE.json:84)*

## 8. Extension points, absences/inconsistencies, and exact raw evidence

- `CONTRIBUTING*` and `AGENTS.md`: ABSENT anywhere in the tracked HEAD inventory; root `AGENTS.md` and parent-level `C:/AGENTS.md`, `C:/Projects/AGENTS.md`, `C:/Projects/Agent_Workspace/AGENTS.md` were also probed and absent. *(output: inventory probe, contributor_files; command: initial prerequisite probe)*
- A dedicated “add a check/test/skill” contributor tutorial in `docs/*.md`: ABSENT in the searched documentation; relevant guidance is fragmented across the concrete sources below. The keyword sweep output is preserved below rather than implying a documented plug-in API. *(command: documentation/header probe below; output: EXTENSION DOC MATCHES)*
- `docs/S0_CONTRACT_SPEC.md` — evolve schemas by tightening required/properties in place, preserve `:1` identity and exact 19-family set, regenerate derived registry through `registry_reconcile.py --write`, check with `--check`; a twentieth family or removal of required fields is refused. *(docs/S0_CONTRACT_SPEC.md:63-91)*
- `docs/ROUND3_DISCLOSURE.md` — historical test-authoring warning: an individual test module failed due to missing `sys.path` bootstrap even though discovery appeared green; tooling checks need regression coverage, not just claims. *(docs/ROUND3_DISCLOSURE.md:80; docs/ROUND3_DISCLOSURE.md:115-143)*
- `docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md` — every portable skill projection requires an approved derivation with matching source digest and approval receipt; projected skill body remains identical; release bookkeeping uses the official manifest’s extension namespace. *(docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md:20-42)*
- Concrete skill/check extension contract (implementation, not a general contributor guide): `tools/skill_pack_check.py` requires input/output schemas, frontmatter/reference validity, POS/NEG/EDGE/SEC cases and routing evidence; exact-eight constraints mean simply adding a ninth skill is deliberately refused. Tests demonstrate the real checker invocation. *(tools/skill_pack_check.py:2-18; tests/test_skill_contracts.py:13-41)*
- Concrete testing pattern (inferred from the executable test): `tests/test_skill_contracts.py` bootstraps `src`, subclasses `unittest.TestCase`, invokes the actual checker in a subprocess and asserts structured results; new `test_*.py` modules are discoverable by CI, but no registration callback mechanism is documented. *(tests/test_skill_contracts.py:9-40; .github/workflows/ci.yml:54-56)*
- `docs/adr/ADR-0009-session-handover-and-next-session-start.md` — require session closeout, checked-in start pack and external checkpoint; treat its state numbers as dated records, not the HEAD identity. *(docs/adr/ADR-0009-session-handover-and-next-session-start.md:2-23)*

### Absences and documentary inconsistencies

- `tools/schema_package_mirror.py`: ABSENT, despite `pyproject.toml` saying `setup.py` invokes that helper; actual mirror is self-contained in `setup.py`. *(output: inventory probe, missing_comment_refs; pyproject.toml:39; setup.py:15-19; setup.py:94-128)*
- `tools/r5q_wheel_license_check.py`: ABSENT, despite a verification reference in a pyproject comment. *(output: inventory probe, missing_comment_refs; pyproject.toml:45)*
- ADR-0009 still records tag/release “not created” and no release for the merged candidate, while the current install SSOT and release tuple record published preview.4. This is dated handover drift, not evidence that preview.4 is absent. *(docs/adr/ADR-0009-session-handover-and-next-session-start.md:34-36; docs/adr/ADR-0009-session-handover-and-next-session-start.md:49; docs/install/README.md:8-16; docs/RELEASE_TUPLE.json:59-81)*
- README claims preview.4 repairs the Trace defects, whereas the user guide explicitly says inheritance by the published wheel is not established by that guide. Preserve that scope distinction; this audit does not resolve released-wheel qualification by inference from source tests. *(README.md:118-122; docs/USER_GUIDE.md:11-18)*
- The fallback header says preview.3 even though the install page is pinned to preview.4. This is explicitly documented and intentional: preview.4 has no mount pack, and the committed fallback retains legacy mount provenance. *(docs/install/PIPD_WEB_FALLBACK.md:4-5; docs/install/README.md:51-59)*
- Probe issue: an attempted read of `tests/test_skill_packs.py` returned file not found; the real tracked skill test is `tests/test_skill_contracts.py`, subsequently read. No path was created or “repaired”. *(output: read_file tests/test_skill_packs.py; tests/test_skill_contracts.py:1-40)*

### Exact invocation and raw inventory output (evidence for §§1–8)


Raw excerpt *(command: inventory probe, executed with exit code 0)*

```bash
python -c 'import ast,collections,json,subprocess,tomllib,re
from pathlib import Path
r=Path("C:/Projects/Agent_Workspace/PIPD-S4R6-wt")
files=subprocess.check_output(["git","-C",str(r),"ls-tree","-r","HEAD","--name-only"],text=True).splitlines()
def lines(p): return (r/p).read_text(encoding="utf-8-sig").splitlines()
def extract(p,start,end): return "\n".join(f"{i}: {x}" for i,x in enumerate(lines(p),1) if start<=i<=end)
tools=[]
for p in files:
 if p.startswith("tools/"):
  text="\n".join(lines(p)); doc=ast.get_docstring(ast.parse(text)) if p.endswith(".py") else None
  purpose=doc.splitlines()[0] if doc else next((x.lstrip("# ") for x in lines(p)[1:8] if x.startswith("#")),"NO DESCRIPTIVE HEADER; body completes S0/S1 gate cards")
  n=next((i for i,x in enumerate(lines(p),1) if purpose in x),1)
  tools.append({"path":p,"purpose":purpose,"line":n})
docs=[{"path":p,"header":" | ".join(x for x in lines(p)[:8] if x)} for p in files if p.startswith("docs/")]
pkg=[]
for p in files:
 if p.startswith("src/pipd_ls_sp/"):
  t="\n".join(lines(p)); doc=ast.get_docstring(ast.parse(t)); pkg.append({"path":p,"lines":len(lines(p)),"purpose":doc.splitlines()[0] if doc else "module (no module docstring)"})
tuple_=json.loads("\n".join(lines("docs/RELEASE_TUPLE.json")))
result={"head":subprocess.check_output(["git","-C",str(r),"rev-parse","HEAD"],text=True).strip(),"branch":subprocess.check_output(["git","-C",str(r),"rev-parse","--abbrev-ref","HEAD"],text=True).strip(),"roots":[p for p in files if "/" not in p],"dirs":dict(sorted(collections.Counter(p.split("/")[0] for p in files if "/" in p).items())),"package":pkg,"pyproject":tomllib.loads("\n".join(lines("pyproject.toml"))),"tests":[p for p in files if p.startswith("tests/")],"tools":tools,"docs":docs,"tuple_keys":list(tuple_),"release_keys":sorted(set().union(*(x.keys() for x in tuple_["releases"]))),"releases":[x["release_id"] for x in tuple_["releases"]],"readme6":extract("README.md",1,6),"ci_run":extract(".github/workflows/ci.yml",47,56),"wheel_run":extract(".github/workflows/ci.yml",74,84),"plugin_run":extract("README.md",64,79),"stage":extract(".github/workflows/public-plugin-verify.yml",122,132),"allow":extract(".github/workflows/public-plugin-verify.yml",191,194),"workflow_steps":{p:[f"{i}: {x.strip()}" for i,x in enumerate(lines(p),1) if "- name:" in x] for p in [".github/workflows/ci.yml",".github/workflows/public-plugin-verify.yml"]},"ci_triggers":extract(".github/workflows/ci.yml",7,12),"plugin_triggers":extract(".github/workflows/public-plugin-verify.yml",17,44),"contributor_files":[p for p in files if Path(p).name.startswith("CONTRIBUTING") or Path(p).name=="AGENTS.md"],"missing_comment_refs":{p:(r/p).exists() for p in ["tools/schema_package_mirror.py","tools/r5q_wheel_license_check.py"]}}
print(json.dumps(result,ensure_ascii=False))'
```


Raw excerpt *(output: inventory probe, raw stdout)*

```json
{"head": "127ec1ca97c71d0437f5b149a6e7d540d0cb3bba", "branch": "fix/s4r6-closeout-doc-identity-and-update-route-20261016", "roots": [".gitattributes", ".gitignore", "ACCEPTANCE.md", "LICENSE", "MANIFEST.in", "NOTICE", "OWNER_LICENSE_DECISION.yaml", "PREVIEW_NOTES_v0.1.0-preview.1.md", "PREVIEW_NOTES_v0.1.0-preview.2.md", "PREVIEW_NOTES_v0.1.1-preview.3.md", "PREVIEW_NOTES_v0.1.1-preview.4.md", "PROVENANCE.md", "README.md", "SBOM.cdx.json", "pyproject.toml", "requirements.lock", "setup.py"], "dirs": {".agents": 7, ".github": 2, ".hermes": 6, ".hgk": 1491, "dist": 43, "docs": 22, "examples": 14, "fixtures": 76, "openspec": 54, "packaging": 7, "schemas": 20, "skills": 48, "src": 13, "tests": 55, "tools": 49}, "package": [{"path": "src/pipd_ls_sp/__init__.py", "lines": 8, "purpose": "PIPD-LS-SP: Pre-Implementation & Pre-Dev Lifecycle Skills Plugin."}, {"path": "src/pipd_ls_sp/cli.py", "lines": 340, "purpose": "`pipd` CLI - exactly the 13 commands of 總藍圖 §5.9.3 (exact-set, no 14th)."}, {"path": "src/pipd_ls_sp/errors.py", "lines": 148, "purpose": "Typed failure codes for the 13-command PIPD-EC surface (總藍圖 §5.9.3)."}, {"path": "src/pipd_ls_sp/export_bundle.py", "lines": 241, "purpose": "Portable export bundle: deterministic ``<name>.tar.gz`` + manifest + checksums."}, {"path": "src/pipd_ls_sp/pipeline.py", "lines": 380, "purpose": "Deterministic PI -> PD -> ConstructionContract -> ECP/TQAEP pipeline."}, {"path": "src/pipd_ls_sp/profiles.py", "lines": 91, "purpose": "Profile trio: LITE / STANDARD / ASSURED over one canonical truth (總藍圖 §7.3 #04)."}, {"path": "src/pipd_ls_sp/projection.py", "lines": 1836, "purpose": "Typed surface projection IR: Web pack + host projections compiled from canonical sources."}, {"path": "src/pipd_ls_sp/registry.py", "lines": 198, "purpose": "Canonical machine-contract registry (exact 19/19, 總藍圖 §7.3)."}, {"path": "src/pipd_ls_sp/repo_context.py", "lines": 228, "purpose": "Repository/host probes for PD late binding (R-AUD-009 / CAP_PD_LATE_BINDING)."}, {"path": "src/pipd_ls_sp/requirements.py", "lines": 332, "purpose": "Clause-bound atomic requirement compiler (R-AUD-005 / CAP_ATOMIC_REQUIREMENT_COMPILER)."}, {"path": "src/pipd_ls_sp/util.py", "lines": 42, "purpose": "Deterministic primitives: canonical JSON, content-addressed ids, hashing."}, {"path": "src/pipd_ls_sp/validate.py", "lines": 294, "purpose": "Deterministic validation: schema + semantic invariants over the 19 families."}, {"path": "src/pipd_ls_sp/workspace.py", "lines": 336, "purpose": "Workspace bootstrap, portable export, projection, doctor, diff, repair."}], "pyproject": {"project": {"name": "pipd-ls-sp", "version": "0.1.1a4", "description": "PIPD-LS-SP Pre-Implementation & Pre-Dev Lifecycle Skills Plugin (HG-KSEOS governed)", "requires-python": ">=3.11", "dependencies": ["jsonschema>=4.0"], "license": "Apache-2.0", "license-files": ["LICENSE", "NOTICE"], "optional-dependencies": {"test": ["pyyaml>=6.0", "build>=1.2", "setuptools>=68", "wheel"]}, "scripts": {"pipd": "pipd_ls_sp.cli:main"}}, "build-system": {"requires": ["setuptools>=68"], "build-backend": "setuptools.build_meta"}, "tool": {"setuptools": {"packages": ["pipd_ls_sp"], "package-dir": {"": "src"}, "package-data": {"pipd_ls_sp": ["schemas/*.json"]}}}}, "tests": ["tests/__init__.py", "tests/fixtures/quarantine_corpus/documented_injection_example.md", "tests/fixtures/quarantine_corpus/identifier_tail.md", "tests/fixtures/quarantine_corpus/malicious_poison.md", "tests/test_atomic_requirements.py", "tests/test_ce_repair_regression.py", "tests/test_claim_ceiling_shape.py", "tests/test_cli_typed_errors.py", "tests/test_deny_list_scan.py", "tests/test_doctor_schema_truth.py", "tests/test_evidence_manifest.py", "tests/test_evidence_md_guards.py", "tests/test_export_bundle.py", "tests/test_first_run_examples.py", "tests/test_git_object_reader.py", "tests/test_host_projection.py", "tests/test_negative_and_rollback.py", "tests/test_oracle_disagreement.py", "tests/test_perf_budget.py", "tests/test_pi_dedup.py", "tests/test_postrelease_contract_hardening.py", "tests/test_postrelease_quickstart.py", "tests/test_postrelease_selfbootstrap.py", "tests/test_postrelease_web_mount.py", "tests/test_preflight_check.py", "tests/test_project_destination_safety.py", "tests/test_public_plugin_packaging.py", "tests/test_publication_projection.py", "tests/test_quarantine_review.py", "tests/test_r10_bclass_evidence.py", "tests/test_r5r3_install_route_identity.py", "tests/test_r6_doc_identity_guard.py", "tests/test_round_envelope.py", "tests/test_round_selfscan.py", "tests/test_s0_contracts.py", "tests/test_s1_lite_slice.py", "tests/test_s4ext_artifact_reproducibility.py", "tests/test_s4ext_first_run_portable.py", "tests/test_s4ext_profile_boundaries.py", "tests/test_s4ext_release_provenance.py", "tests/test_s4ext_spec_del_adjudication.py", "tests/test_s4ext_trace_closure.py", "tests/test_s4r2_affected_only.py", "tests/test_s4r2m_docs_route.py", "tests/test_secret_patterns.py", "tests/test_skill_contracts.py", "tests/test_spec_del_crosswalk.py", "tests/test_standard_wheel_schemas.py", "tests/test_technology_admission.py", "tests/test_tooling_executes.py", "tests/test_tqaep_design_positive.py", "tests/test_tt_summary.py", "tests/test_web_fallback.py", "tests/test_web_pack.py", "tests/test_wheel_distribution.py"], "tools": [{"path": "tools/admit_technologies.py", "purpose": "S0/S1 — materialise the 22 source-designated Technology Admission rulings (PKG-00 §9).", "line": 2}, {"path": "tools/build_bclass_artifacts.py", "purpose": "Materialise the two R10 SSOT artefacts that were adjudicated BUILDABLE-FAITHFULLY.", "line": 2}, {"path": "tools/build_dist.py", "purpose": "S3 portable distribution: build a real, standards-shaped wheel + sdist-like bundle, with checksums.", "line": 2}, {"path": "tools/build_evidence_manifest.py", "purpose": "Build, seal and verify the evidence manifest (R-AUD-014 / WO-TS-req-pipd-r3-fw-11).", "line": 2}, {"path": "tools/build_evidence_md.py", "purpose": "Assemble the single-file external acceptance evidence MD from the frozen receipts.", "line": 2}, {"path": "tools/build_evidence_md_r2.py", "purpose": "Build the single external acceptance evidence MD for the S0-S4 continuation round.", "line": 2}, {"path": "tools/build_mount_pack.py", "purpose": "WO-S4-WEB-02: build and verify the one versioned Web/ChatGPT mount pack.", "line": 2}, {"path": "tools/build_public_plugin.py", "purpose": "S4POST Stage B: build the deterministic, fail-closed public Skills-only plugin candidate.", "line": 2}, {"path": "tools/build_publication_manifest.py", "purpose": "Publication projection manifest (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-006, R-AUD-014).", "line": 2}, {"path": "tools/build_requirements_lock.py", "purpose": "Write requirements.lock - the resolved runtime closure of this project, pinned exactly.", "line": 2}, {"path": "tools/build_s4_spec_del_adjudication.py", "purpose": "TT-S4EXT-007 -- S4-active SPEC/DEL row adjudication (deterministic generator).", "line": 2}, {"path": "tools/build_s5_s8_backlog.py", "purpose": "S4 -> S5..S8 typed integration seams.", "line": 2}, {"path": "tools/build_spec_del_crosswalk.py", "purpose": "Build / check the 32 SPEC + 25 DEL crosswalk from live repo objects.", "line": 2}, {"path": "tools/build_web_fallback.py", "purpose": "S4POST Stage B: project one frozen Web mount pack into ONE bounded fallback document.", "line": 2}, {"path": "tools/cli_smoke.py", "purpose": "Run all 13 pipd commands end to end and freeze the raw receipts.", "line": 2}, {"path": "tools/cli_surface_check.py", "purpose": "S4 CLI surface qualification: exactly 13 commands, each with an exercised SUCCESS path and an", "line": 2}, {"path": "tools/deny_list_scan.py", "purpose": "Classify every `danger-full-access` occurrence as a POLICY_MENTION or a WRITER_USAGE (R4 / W9).", "line": 2}, {"path": "tools/edge_selfcheck.py", "purpose": "Local pre-check of the E1..E12 edge probes.", "line": 2}, {"path": "tools/freeze_public_plugin_source.py", "purpose": "S4POST Stage B: freeze the eight public skill packs into a source ledger.", "line": 2}, {"path": "tools/github_publish.py", "purpose": "Publish the frozen PIPD-LS-SP candidate to GitHub as a public repo.", "line": 2}, {"path": "tools/hgk_admission_driver.py", "purpose": "Drive the HG-KSEOS normal lifecycle admission chain for PIPD-LS-SP.", "line": 2}, {"path": "tools/history_secret_scan.py", "purpose": "Scan BOTH the working tree and the git history for token-like strings (R-AUD-014 / FW-11).", "line": 2}, {"path": "tools/host_projection_check.py", "purpose": "G-S3-HOST gate — FW-06 / R-AUD-004 / R-AUD-015, real semantic checks.", "line": 2}, {"path": "tools/kanban_canonical_complete.py", "purpose": "Drive the canonical PIPD-LS-SP board: complete the closed gates with real receipts.", "line": 2}, {"path": "tools/kanban_canonical_ids.sh", "purpose": "Complete the canonical-board gate cards with real CLI receipts.", "line": 2}, {"path": "tools/kanban_complete_early.sh", "purpose": "Complete the gates whose work is actually finished (ancestors first).", "line": 4}, {"path": "tools/kanban_complete_s0s1.sh", "purpose": "NO DESCRIPTIVE HEADER; body completes S0/S1 gate cards", "line": 1}, {"path": "tools/kanban_dag.sh", "purpose": "PIPD-LS-SP gate DAG creation + evidence receipts", "line": 4}, {"path": "tools/kanban_round.sh", "purpose": "PIPD-LS-SP governed round: Kanban board + gate DAG (real CLI receipts)", "line": 4}, {"path": "tools/knowledge_ready_probe.py", "purpose": "G-KNOWLEDGE-READY probe for PIPD-LS-SP.", "line": 2}, {"path": "tools/perf_budget.py", "purpose": "S2 performance + context budget. Measures real wall-clock work; declares the budget it holds to.", "line": 2}, {"path": "tools/pi_dedup_check.py", "purpose": "Measure the PI source-clause de-duplication honestly, raw-first (R4 / W5, repaired by W9).", "line": 2}, {"path": "tools/portable_install_check.py", "purpose": "S3 + R5-DIST-002: real install / self-sufficiency / uninstall lifecycle in an ISOLATED env (L5).", "line": 2}, {"path": "tools/preflight_check.py", "purpose": "Preflight check for the PIPD governed lane.", "line": 2}, {"path": "tools/publication_attestation.py", "purpose": "Immutable publication-subject attestation (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-014).", "line": 2}, {"path": "tools/quarantine_review.py", "purpose": "G-KNOWLEDGE-READY — quarantine review path + R3 per-source owner disposition (R-AUD-008).", "line": 2}, {"path": "tools/registry_reconcile.py", "purpose": "Single-source reconciliation of schemas/registry.json FROM the schema files.", "line": 2}, {"path": "tools/replay_check.py", "purpose": "S4 replay identity: the same input lock must reproduce the same artefacts byte for byte.", "line": 2}, {"path": "tools/round_envelope.py", "purpose": "S2 verifier envelope: a disposable byte-copy, a per-file snapshot, a three-way delta guard.", "line": 2}, {"path": "tools/round_selfscan.py", "purpose": "Round self-scan: a credential-shape sweep folded together with the deny-list gate.", "line": 2}, {"path": "tools/run_golden_pilots.py", "purpose": "S2 golden pilots — really execute the lifecycle on three profiles.", "line": 2}, {"path": "tools/run_nrtv_judge.py", "purpose": "S2 NRTV + NEG + SEC + oracle/judge calibration.", "line": 2}, {"path": "tools/run_r3_qualification.py", "purpose": "FW-09 (audit finding R-AUD-010): re-qualify the pilots and the 13-command CLI.", "line": 2}, {"path": "tools/run_s1_slice.py", "purpose": "Run the S1 LITE vertical slice and freeze its artifacts as raw evidence.", "line": 2}, {"path": "tools/skill_pack_check.py", "purpose": "skill_pack_check — discover -> load -> route checker for the 8 PIPD SkillContract packs.", "line": 2}, {"path": "tools/tt_summary_check.py", "purpose": "TT status projection — recompute the TT register summary from `tts[]` only.", "line": 2}, {"path": "tools/verify_evidence_digests.py", "purpose": "Recompute the per-entry sha256 recorded in the evidence manifest against the bytes on disk.", "line": 2}, {"path": "tools/verify_installed_wheel_registry.py", "purpose": "Assert that an INSTALLED wheel resolved its OWN packaged contract registry (S4R3-F006).", "line": 2}, {"path": "tools/web_pack_check.py", "purpose": "G-S3-WEB gate — FW-05 / R-AUD-003 / R-AUD-015, real semantic checks.", "line": 2}], "docs": [{"path": "docs/ERRATUM_2026-10-12_preview3_release_provenance.md", "header": "# ERRATUM 1 — v0.1.1-preview.3 Web Mount pack release identity | > **Document ID**：`PIPD-ERRATUM-2026-10-12-PREVIEW3-PROVENANCE` | > **Raised**：2026-10-12 (Asia/Taipei) · **Round**：`S4EXT-R1-20261012-external-challenge-repair` | > **Finding of record**：`F001` of `PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1` (CONFIRMED_DEFECT, P1) | > **Frozen tuple**：`docs/RELEASE_TUPLE.json` · **Status**：`SOURCE_CORRECTED / PUBLISHED_ASSET_REPLACED_IN_PLACE / RELEASE HOLD` | > | > **Reconciled 2026-10-12 (S4POST integration-repair round).** The first version of this banner read"}, {"path": "docs/FRONT_PAGE_HISTORY.md", "header": "# Front-page history moved out of `README.md` (round R6, 2026-10-11) | In round **R6-20261011-main-front-page** the repository front page was rewritten from an | append-only log into a current-state page. Nothing here was deleted — the sections that used to | live on `README.md` and no longer belong on a front page are preserved **verbatim** below, with | their original headings and wording intact. | Two things moved here:"}, {"path": "docs/NORMATIVE_SOURCE_MAP.md", "header": "# NORMATIVE SOURCE MAP (DERIVED INDEX) | > **This file is a DERIVED INDEX. It is NOT a competing master.** | > | > * The external canonical standard `PIPD-LIFECYCLE-SPEC@1.1.0` remains the **single source of | >   truth**. Nothing in this repository restates, supersedes or re-derives its normative content. | > * This index only **points at** source families: where each lives, who owns it, its version, a | >   digest (or an explicit \"not readable here\" marker), and which consumers read it."}, {"path": "docs/OWNER_ADJUDICATION_R4_2026-10-09.json", "header": "{ |   \"schema\": \"PIPD-OWNER-ADJUDICATION/1\", |   \"round\": \"R4-20261009-focused-repair\", |   \"issued\": \"2026-10-09\", |   \"authority\": { |     \"act\": \"owner adjudication + publication authorisation\", |     \"owner_instruction_zh\": \"直接執行研究後的建議最佳工程裁決，並且把相關實作內容和證據更新至 GITHUB REPO，讓外部官進行驗收。\", |     \"basis\": \"PIPD-LS-SP_R4_PLAN_RULINGS_A1A5V7_2026-10-09 (PLAN lane, GPT 6.1 SOL-MEDIUM, CODEX CLI; FAR-style analysis over the supplied local evidence only)\","}, {"path": "docs/OWNER_ADJUDICATION_R4_2026-10-09.md", "header": "# Owner adjudication — R4 focused-repair (2026-10-09) | Machine-readable record: `docs/OWNER_ADJUDICATION_R4_2026-10-09.json` (schema `PIPD-OWNER-ADJUDICATION/1`). | **Authority.** The repository owner directed: *\"直接執行研究後的建議最佳工程裁決，並且把相關實作內容和證據更新至 | GITHUB REPO，讓外部官進行驗收\"* — execute the recommended engineering rulings, and publish the implementation and | evidence to the GitHub repo for external verification."}, {"path": "docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json", "header": "{ |   \"schema\": \"PIPD-OWNER-ADJUDICATION/1\", |   \"round\": \"R5-20261009-s4-user-operability\", |   \"issued\": \"2026-10-10\", |   \"authority\": { |     \"act\": \"owner adjudication executed on the owner's instruction\", |     \"owner_instruction_zh\": \"直接執行FAR研究後建議的裁決\", |     \"basis\": \"知識庫/實作相關DOC/PIPD/實作證據/PIPD-LS-SP_R5_S4_FAR_S2PERF_LICENSE_2026-10-10.md with .hgk/far/FAR-PIPD-R5S4-S2PERF-LICENSE-001/EVIDENCE_S2PERF.json; the FAR study measured the artefact rather than assuming the threshold could be met\","}, {"path": "docs/RELEASE_TUPLE.json", "header": "{ |   \"schema\": \"PIPD-RELEASE-TUPLE/1\", |   \"purpose\": \"Frozen, independently resolvable release identities for the distribution/release surface. TT-S4EXT-001 / F001 exists because a single hand-copied `tag commit` string let the distributed pack name a DIFFERENT release's object than the one it claimed to describe. The two facts are therefore separate fields and must never be collapsed again.\", |   \"field_semantics\": { |     \"tag_object\": \"the annotated tag object sha (git rev-parse <tag>)\", |     \"release_tag_target\": \"the commit the annotated tag dereferences to (git rev-parse <tag>^{commit})\", |     \"build_source_commit\": \"the commit the distributed artifact BYTES were built from; when a release builds more than one artifact this names the one given by that entry's build_source_scope, and it is never a claim about an artifact the scope does not name\", |     \"tree\": \"the tree of release_tag_target (git rev-parse <tag>^{tree})\","}, {"path": "docs/ROUND3_DISCLOSURE.md", "header": "# 本回合揭露（ROUND 3，撰寫於 repo 外，待複驗回收後併入） | ## 1. 模型 SoD 與 lane 指派（現行實測） | | 角色 | lane | provider / model | 實測 | | |---|---|---|---| | | PLANNING（HGK lifecycle / admission） | 主 | openai-codex / `gpt-6.1-sol`（OpenAI OAuth） | 2026-10-08 22:59 遭 HTTP 429，額度 00:26 重置 | | | PLANNING 備援 #1 | 第一備援 | **nvidia / `z-ai/glm-5.3`** | 直連 HTTP 200 `served_as='z-ai/glm-5.3'`；CLI 端到端 `LANE_OK` |"}, {"path": "docs/ROUND_DISCLOSURE.md", "header": "# Round disclosure — PIPD-LS-SP governed round (2026-10-08) | Everything anomalous about this round is listed here on purpose. Nothing below is a | \"known limitation we accepted quietly\". | ## 1. Profile escalation was not requested but was applied | The S1 vertical slice is described as a **LITE** slice. The pipeline **escalated the run to"}, {"path": "docs/S0_CONTRACT_SPEC.md", "header": "# PIPD-LS-SP S0 Canonical Machine Contract Spec — exact 19/19 | Source (NORMATIVE): `PIPD-LS-SP_藍圖.md` §7.3 \"Canonical Machine Contracts — exact 19/19\" | (sha256 6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a for the | canonical standard; the blueprint file digest is recorded in the source manifest). | Bootstrap order (`.pipd` §5.6.1): 01 standard lock, 02 project manifest, 03 schemas/registry, | 04 package index, 05 PI/PD objects, 06 policies/currentness/execution contracts,"}, {"path": "docs/S4_SPEC_DEL_ADJUDICATION.json", "header": "{ |  \"schema\": \"PIPD-S4-SPEC-DEL-ADJUDICATION/1\", |  \"claim_ceiling\": \"MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION\", |  \"subject\": { |   \"baseline_main_commit\": \"0a05f4fde899d5990a8c098e3feaa2d9d1d7e0de\", |   \"crosswalk\": \"docs/SPEC_DEL_CROSSWALK.json\", |   \"crosswalk_schema\": \"PIPD-SPEC-DEL-CROSSWALK/1\", |   \"crosswalk_counts\": {"}, {"path": "docs/SPEC_DEL_CROSSWALK.json", "header": "{ |   \"schema\": \"PIPD-SPEC-DEL-CROSSWALK/1\", |   \"blueprint\": \"PIPD-LS-SP_藍圖.md\", |   \"counts\": { |     \"SPEC\": 32, |     \"DEL\": 25, |     \"total\": 57 |   },"}, {"path": "docs/USER_GUIDE.md", "header": "# PIPD-LS-SP — user guide | **This is the only user guide.** It is task-first: find the row for what you are trying to do and | follow it. It is *not* a second installation document — version pins, hashes, the fetch commands, | uninstall and rollback live in exactly one place, [`docs/install/README.md`](install/README.md), and | this guide links there rather than copying it. | Three ceilings apply to everything below, and no result here can lift them:"}, {"path": "docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md", "header": "# ADR-0001 — The package root manifest is the official Agent Plugins 1.0 manifest | - Status: ACCEPTED (Stage B candidate; nothing is published by this decision) | - Date: 2026-10-12 | - Scope: `packaging/public-plugin/**`, `tools/build_public_plugin.py`, |   `tests/test_public_plugin_packaging.py` | ## Context"}, {"path": "docs/adr/ADR-0007-plugin-distribution-private-first.md", "header": "# ADR-0007 — Plugin distribution: private-first, public directory on hold | - **Status:** accepted 2026-10-14 (owner ruling in chat, executed by the round `R5Z-20261014-session-conformance`) | - **Context:** the plan of record asked for a ChatGPT plugin listing. On 2026-10-14 the agent drove |   `platform.openai.com/plugins` with the desktop tooling and the Portal answered *“You need a verified |   developer identity before you can create or upload a plugin.”* Identity/KYC is a human act and the agent |   must not perform it. The **private** path has no such precondition. | - **Decision:** distribute the Skills-only plugin **privately first**. The candidate ZIP is uploaded through"}, {"path": "docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md", "header": "# ADR-0008 — Repository state and branch/PR hygiene inventory | - **Status**: Accepted (round `R7-20261014-merge-hygiene-closeout`, 2026-10-14) | - **Context**: after PR #8 was merged into `main` under explicit owner authorization, the repository held |   19 branches and six pull requests; the state and what may be cleaned had to be recorded and bound to |   rules so a later session cannot delete a verifiability anchor by accident. | - **Decision**: keep every branch that an evidence pack cites as a frozen subject; close superseded pull |   requests with the ancestry evidence that shows they are already contained; never relax the write-set"}, {"path": "docs/adr/ADR-0009-session-handover-and-next-session-start.md", "header": "## 0. Re-read main before acting | `main` at the time of writing: `fc55591852bc016ae8dc861edf88db0e613b3c6a` (merge of PR #9; PR #8 merged at | `b3a27c1f00c90b010feec7b4da5f420d45edec61`). Any session that starts later must re-read `main` rather than trust | this line: run `git -C <clone> fetch origin && git -C <clone> rev-parse origin/main` first, and treat the evidence | branch (`r5z-evidence-return-20261014`) as the place where the frozen receipts live."}, {"path": "docs/install/ASSET_READBACK_v0.1.1-preview.4.json", "header": "{ |  \"schema\": \"PIPD-LS-SP/asset-readback/1\", |  \"subject_release\": \"v0.1.1-preview.4\", |  \"measured_at\": \"2026-10-16\", |  \"what_this_is\": \"A repository-side verification record, NOT a release asset: every value below was measured by downloading the asset GitHub serves for this release and hashing the bytes locally, then parsing the release's own SHA256SUMS and comparing. It exists so the identity test can cross-check the documented tuple against the served bytes without trusting a maker sidecar.\", |  \"method\": \"per-asset HTTPS download -> sha256 -> compare against the parsed SHA256SUMS entries\", |  \"sha256sums_entries\": [ |   \"PIPD_WEB_FALLBACK.md\","}, {"path": "docs/install/PIPD_AGENT_INSTALL_PROMPT.md", "header": "# PIPD-LS-SP — Agent 安裝提示詞(單一貼上即用) | 這份文件**就是** Agent route 的安裝入口:一整段可複製的提示詞(prompt)。它本身不安裝任何東西、 | 不執行任何指令、不代表任何 acceptance 或發佈狀態——被安裝與被驗證的是 **host**(Hermes Agent / | Codex Desktop (GUI) / Codex CLI / Claude Code),而 host 必須自己證明它的版本、discovery 與生效載入。 | 使用方式:把下面 ```text 區塊**整段**複製,貼進你的 agent host 對話,然後依它的提問回答。全程保留 | 英文識別字(host 名稱、skill 名稱、狀態字如 `NOT_VERIFIED`、`REFUSED`)不要翻譯。"}, {"path": "docs/install/PIPD_WEB_FALLBACK.md", "header": "<!-- PIPD-WEB-FALLBACK/1 DOC_MOUNT_ONLY --> | # PIPD-LS-SP S4 Web fallback — single-document mount (DOC_MOUNT_ONLY) | - release_id: v0.1.1-preview.3 | - release_commit: cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a | - doc_mount_only: true | - member_count: 8 | - size_cap_bytes: 524288"}, {"path": "docs/install/PIPD_WEB_FALLBACK.md.sha256", "header": "c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af *docs/install/PIPD_WEB_FALLBACK.md"}, {"path": "docs/install/README.md", "header": "# PIPD-LS-SP — install (single source of truth) | This page is the **install SSOT**: every other page that mentions installing PIPD-LS-SP either is | this page or points at it. There are **two install routes and only two** — **Web** and **Agent** — | and they have different ceilings. Pick one, read its ceiling, and do not read a green build (or a | copied file) as anything more than what the [states table](#states-that-are-not-the-same) below says. | Version pin for everything on this page: release **`v0.1.1-preview.4`**; its annotated tag object"}], "tuple_keys": ["schema", "purpose", "field_semantics", "verification_commands", "releases", "authority_note"], "release_keys": ["asset_list_source", "asset_replaced_in_place", "asset_replacement_record", "build_source_commit", "build_source_scope", "erratum_doc", "first_shipped_asset_sha256", "note", "pack_dir", "published_asset_name", "published_asset_sha256", "release_id", "release_tag_target", "served_assets", "served_assets_coverage", "stale_identity_in_first_shipped_asset", "status", "superseded_candidate_note", "superseded_candidate_zip", "tag_object", "tree", "zip"], "releases": ["v0.1.0-preview.1", "v0.1.0-preview.2", "v0.1.1-preview.3", "v0.1.1-preview.4"], "readme6": "1: # PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin\n2: \n3: A governed, contract-first toolkit for the **pre-implementation** stage of a project: it turns a\n4: stated intent into a validated chain of machine-readable artefacts — PI → PD →\n5: ConstructionContract → ECP / TQAEP — each bound to one of **19 canonical JSON Schema families**,\n6: and it refuses to hand you something it cannot check. It ships **8 skills** and a **13-command", "ci_run": "47:       - name: Full unittest suite (raw log)\n48:         # FALSE-GREEN REPAIR (S4R3-F001): this step previously ran\n49:         # `python -m unittest ... 2>&1 | tee full-unittest.log`. A pipeline's exit status is the LAST\n50:         # command's, so `tee` succeeded and the step passed while the log itself read\n51:         # \"FAILED (failures=11, skipped=6)\". `set -o pipefail` makes the step carry the suite's own\n52:         # exit code, so a red suite is a red job. Do NOT remove it, and do not \"fix\" a red suite by\n53:         # narrowing the denominator or skipping files.\n54:         run: |\n55:           set -euo pipefail\n56:           python -m unittest discover -s tests -t . -v 2>&1 | tee full-unittest.log", "wheel_run": "74:           set -euo pipefail\n75:           python -m pip install build\n76:           rm -rf \"$RUNNER_TEMP/wheels\" && mkdir -p \"$RUNNER_TEMP/wheels\"\n77:           python -m build --wheel --outdir \"$RUNNER_TEMP/wheels\"\n78:           ls -l \"$RUNNER_TEMP/wheels\"\n79:           python -m venv \"$RUNNER_TEMP/wheelvenv\"\n80:           \"$RUNNER_TEMP/wheelvenv/bin/python\" -m pip install --upgrade pip\n81:           \"$RUNNER_TEMP/wheelvenv/bin/python\" -m pip install \"$RUNNER_TEMP\"/wheels/*.whl\n82:           cd \"$RUNNER_TEMP\"\n83:           \"$RUNNER_TEMP/wheelvenv/bin/pipd\" doctor | tee \"$GITHUB_WORKSPACE/wheel-doctor.log\"\n84:           \"$RUNNER_TEMP/wheelvenv/bin/pipd\" --help | tee \"$GITHUB_WORKSPACE/wheel-cli-help.log\"", "plugin_run": "64: The plugin ZIP is reproducible. Run from the frozen R5Y worktree at commit\n65: `062d84ae3e951d02b2ba6bb732359b18799d2864`:\n66: \n67: ```bash\n68: python tools/freeze_public_plugin_source.py --repo-root . --out ledger.json\n69: python tools/build_public_plugin.py --ledger ledger.json --source-commit 062d84ae3e951d02b2ba6bb732359b18799d2864 \\\n70:   --packaging-root packaging/public-plugin --out-dir out --generate-icons\n71: ```\n72: \n73: This reproduces the **historical R5Y build**: `out/pipd-ls-sp-public-skills.zip` — **68,355 bytes**,\n74: sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, **56 entries**, **8 `SKILL.md`**\n75: — the bytes frozen at `062d84ae3e951d02b2ba6bb732359b18799d2864` and attached to the R5Y evidence return.\n76: Those bytes are **superseded as a download**: the artefact a user installs is the `v0.1.1-preview.4`\n77: release asset `pipd-ls-sp-public-skills.zip` — **68,357 bytes**, sha256\n78: `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`, 56 entries, 8 `SKILL.md`. Two\n79: independent builds are byte-identical. A local packager PASS is not portal approval.", "stage": "122:           STAGE: stage-c\n123:           # Stage A's declared base: the frozen R3 subject the external acceptance report examined.\n124:           STAGE_A_BASE_SHA: e71fee6dd3aa73724baec4e8d9cc72127fbe36ed\n125:           # Stage B's declared base: the Stage A tip that Stage B is stacked on. Taken by ref so it\n126:           # does not need editing every time the Stage A tip moves; the sha it resolves to is printed\n127:           # below and is the value an auditor should cite.\n128:           STAGE_B_BASE_REF: fix/s4r3-stage-a-ci-truthfulness-20261013\n129:           # Stage C's declared base: the frozen S4-R5 subject, taken as a literal because it is a\n130:           # merged main commit and therefore immutable.\n131:           STAGE_C_BASE_SHA: f4021aeff9c016cfb14f17e68a0c570ed4e825c5\n132:           PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}", "allow": "191:               ALLOWED='^(src/pipd_ls_sp/|schemas/|tests/|fixtures/|pyproject\\.toml$|tools/build_dist\\.py$|dist/|README\\.md$|docs/install/|docs/USER_GUIDE\\.md$|docs/RELEASE_TUPLE\\.json$|PREVIEW_NOTES_v0\\.1\\.1-preview\\.4\\.md$|\\.github/workflows/public-plugin-verify\\.yml$)'\n192:               DENIED='^(skills/|packaging/public-plugin/)'\n193:               REFUSED_PLANTS='skills/pipd-core/SKILL.md packaging/public-plugin/plugin.json src/other_package/thing.py tools/build_public_plugin.py'\n194:               ALLOWED_PLANTS='src/pipd_ls_sp/requirements.py schemas/ClaimCeiling.schema.json tests/test_claim_ceiling_shape.py fixtures/REQ-NEG-PHRASES/source.txt dist/pipd_ls_sp-0.1.1a4-py3-none-any.whl README.md docs/install/README.md docs/RELEASE_TUPLE.json docs/USER_GUIDE.md'", "workflow_steps": {".github/workflows/ci.yml": ["23: - name: Check out the frozen subject", "29: - name: Set up Python 3.11", "34: - name: Install (declared dependencies only) and record what was resolved", "47: - name: Full unittest suite (raw log)", "58: - name: Focused S4 repair / closure suites (raw log)", "63: - name: Build the wheel and exercise it in a clean venv with no source on PYTHONPATH", "86: - name: The installed wheel resolves its OWN contract registry (S4R3-F006)", "107: - name: Provenance gate is green before it is tested", "115: - name: Negative — a mutated pack document must make the provenance gate fail", "149: - name: Upload raw logs"], ".github/workflows/public-plugin-verify.yml": ["55: - name: Check out the frozen subject", "63: - name: Set up Python 3.11", "68: - name: Prove the upgrade wrote only inside its allowed set", "304: - name: Compile the three upgrade tools", "313: - name: Assert the upgrade is stdlib-only (no third-party import)", "363: - name: The two new test modules pass with no third-party dependency installed", "372: - name: Install the project's own declared runtime dependency only", "385: - name: Full unittest suite (raw log)", "393: - name: Negative — a mutated pack document must fail the identity binding", "455: - name: Negative — the fallback builder must refuse a pack whose bytes drifted from MANIFEST.sha256", "504: - name: Upload raw logs"]}, "ci_triggers": "7: on:\n8:   push:\n9:   pull_request:\n10: \n11: permissions:\n12:   contents: read", "plugin_triggers": "17: on:\n18:   pull_request:\n19:     paths:\n20:       - \".github/workflows/public-plugin-verify.yml\"\n21:       - \"README.md\"\n22:       - \"docs/install/**\"\n23:       - \"docs/USER_GUIDE.md\"\n24:       - \"docs/RELEASE_TUPLE.json\"\n25:       - \"packaging/public-plugin/**\"\n26:       - \"tools/freeze_public_plugin_source.py\"\n27:       - \"tools/build_public_plugin.py\"\n28:       - \"tools/build_web_fallback.py\"\n29:       - \"tests/test_public_plugin_packaging.py\"\n30:       - \"tests/test_web_fallback.py\"\n31:       - \"dist/mount/**\"\n32:       # Source-repair rounds: without these, a PR that only repairs the compiler or the schemas would\n33:       # not run this gate at all, so the write-set declaration would be unenforced exactly where it\n34:       # matters most.\n35:       - \"src/**\"\n36:       - \"schemas/**\"\n37:       - \"tests/**\"\n38:       - \"fixtures/**\"\n39:       - \"pyproject.toml\"\n40:       - \"tools/build_dist.py\"\n41:   workflow_dispatch:\n42: \n43: permissions:\n44:   contents: read", "contributor_files": [], "missing_comment_refs": {"tools/schema_package_mirror.py": false, "tools/r5q_wheel_license_check.py": false}}
```


### Exact documentation/header search invocation and raw output


Raw excerpt *(command: documentation/header probe, executed with exit code 0)*

```bash
python -c 'import ast,subprocess,re; from pathlib import Path; r=Path("C:/Projects/Agent_Workspace/PIPD-S4R6-wt"); files=subprocess.check_output(["git","-C",str(r),"ls-tree","-r","HEAD","--name-only"],text=True).splitlines(); print("TOOL HEADER PURPOSES");
for p in files:
 if p.startswith("tools/"):
  text=(r/p).read_text(encoding="utf-8-sig"); lines=text.splitlines(); doc=ast.get_docstring(ast.parse(text)) if p.endswith(".py") else None; purpose=doc.splitlines()[0] if doc else next((x.lstrip("# ") for x in lines[1:8] if x.startswith("#")), "NO DESCRIPTIVE HEADER; inspect source"); print(p+": "+purpose)
print("DOCUMENT HEADERS")
for p in files:
 if p.startswith("docs/") and p!="docs/RELEASE_TUPLE.json":
  lines=(r/p).read_text(encoding="utf-8-sig").splitlines(); print(p+": "+" | ".join(f"{i+1}:{x}" for i,x in enumerate(lines[:8]) if x)[:500])
print("EXTENSION DOC MATCHES")
for p in files:
 if (p.startswith("docs/") or p=="README.md") and p.endswith(".md"):
  lines=(r/p).read_text(encoding="utf-8-sig").splitlines()
  for i,x in enumerate(lines):
   if re.search(r"contribut|extend|add.*(check|test|skill)|new.*(check|test|skill)|新增|擴充",x,re.I): print(f"{p}:{i+1}: {x}")' 
```


Raw excerpt *(output: documentation/header probe, raw stdout)*

```text
TOOL HEADER PURPOSES
tools/admit_technologies.py: S0/S1 — materialise the 22 source-designated Technology Admission rulings (PKG-00 §9).
tools/build_bclass_artifacts.py: Materialise the two R10 SSOT artefacts that were adjudicated BUILDABLE-FAITHFULLY.
tools/build_dist.py: S3 portable distribution: build a real, standards-shaped wheel + sdist-like bundle, with checksums.
tools/build_evidence_manifest.py: Build, seal and verify the evidence manifest (R-AUD-014 / WO-TS-req-pipd-r3-fw-11).
tools/build_evidence_md.py: Assemble the single-file external acceptance evidence MD from the frozen receipts.
tools/build_evidence_md_r2.py: Build the single external acceptance evidence MD for the S0-S4 continuation round.
tools/build_mount_pack.py: WO-S4-WEB-02: build and verify the one versioned Web/ChatGPT mount pack.
tools/build_public_plugin.py: S4POST Stage B: build the deterministic, fail-closed public Skills-only plugin candidate.
tools/build_publication_manifest.py: Publication projection manifest (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-006, R-AUD-014).
tools/build_requirements_lock.py: Write requirements.lock - the resolved runtime closure of this project, pinned exactly.
tools/build_s4_spec_del_adjudication.py: TT-S4EXT-007 -- S4-active SPEC/DEL row adjudication (deterministic generator).
tools/build_s5_s8_backlog.py: S4 -> S5..S8 typed integration seams.
tools/build_spec_del_crosswalk.py: Build / check the 32 SPEC + 25 DEL crosswalk from live repo objects.
tools/build_web_fallback.py: S4POST Stage B: project one frozen Web mount pack into ONE bounded fallback document.
tools/cli_smoke.py: Run all 13 pipd commands end to end and freeze the raw receipts.
tools/cli_surface_check.py: S4 CLI surface qualification: exactly 13 commands, each with an exercised SUCCESS path and an
tools/deny_list_scan.py: Classify every `danger-full-access` occurrence as a POLICY_MENTION or a WRITER_USAGE (R4 / W9).
tools/edge_selfcheck.py: Local pre-check of the E1..E12 edge probes.
tools/freeze_public_plugin_source.py: S4POST Stage B: freeze the eight public skill packs into a source ledger.
tools/github_publish.py: Publish the frozen PIPD-LS-SP candidate to GitHub as a public repo.
tools/hgk_admission_driver.py: Drive the HG-KSEOS normal lifecycle admission chain for PIPD-LS-SP.
tools/history_secret_scan.py: Scan BOTH the working tree and the git history for token-like strings (R-AUD-014 / FW-11).
tools/host_projection_check.py: G-S3-HOST gate — FW-06 / R-AUD-004 / R-AUD-015, real semantic checks.
tools/kanban_canonical_complete.py: Drive the canonical PIPD-LS-SP board: complete the closed gates with real receipts.
tools/kanban_canonical_ids.sh: Complete the canonical-board gate cards with real CLI receipts.
tools/kanban_complete_early.sh: Complete the gates whose work is actually finished (ancestors first).
tools/kanban_complete_s0s1.sh: NO DESCRIPTIVE HEADER; inspect source
tools/kanban_dag.sh: PIPD-LS-SP gate DAG creation + evidence receipts
tools/kanban_round.sh: PIPD-LS-SP governed round: Kanban board + gate DAG (real CLI receipts)
tools/knowledge_ready_probe.py: G-KNOWLEDGE-READY probe for PIPD-LS-SP.
tools/perf_budget.py: S2 performance + context budget. Measures real wall-clock work; declares the budget it holds to.
tools/pi_dedup_check.py: Measure the PI source-clause de-duplication honestly, raw-first (R4 / W5, repaired by W9).
tools/portable_install_check.py: S3 + R5-DIST-002: real install / self-sufficiency / uninstall lifecycle in an ISOLATED env (L5).
tools/preflight_check.py: Preflight check for the PIPD governed lane.
tools/publication_attestation.py: Immutable publication-subject attestation (REQ-PIPD-R4-W1 / R3-EXT-01, R-AUD-014).
tools/quarantine_review.py: G-KNOWLEDGE-READY — quarantine review path + R3 per-source owner disposition (R-AUD-008).
tools/registry_reconcile.py: Single-source reconciliation of schemas/registry.json FROM the schema files.
tools/replay_check.py: S4 replay identity: the same input lock must reproduce the same artefacts byte for byte.
tools/round_envelope.py: S2 verifier envelope: a disposable byte-copy, a per-file snapshot, a three-way delta guard.
tools/round_selfscan.py: Round self-scan: a credential-shape sweep folded together with the deny-list gate.
tools/run_golden_pilots.py: S2 golden pilots — really execute the lifecycle on three profiles.
tools/run_nrtv_judge.py: S2 NRTV + NEG + SEC + oracle/judge calibration.
tools/run_r3_qualification.py: FW-09 (audit finding R-AUD-010): re-qualify the pilots and the 13-command CLI.
tools/run_s1_slice.py: Run the S1 LITE vertical slice and freeze its artifacts as raw evidence.
tools/skill_pack_check.py: skill_pack_check — discover -> load -> route checker for the 8 PIPD SkillContract packs.
tools/tt_summary_check.py: TT status projection — recompute the TT register summary from `tts[]` only.
tools/verify_evidence_digests.py: Recompute the per-entry sha256 recorded in the evidence manifest against the bytes on disk.
tools/verify_installed_wheel_registry.py: Assert that an INSTALLED wheel resolved its OWN packaged contract registry (S4R3-F006).
tools/web_pack_check.py: G-S3-WEB gate — FW-05 / R-AUD-003 / R-AUD-015, real semantic checks.
DOCUMENT HEADERS
docs/ERRATUM_2026-10-12_preview3_release_provenance.md: 1:# ERRATUM 1 — v0.1.1-preview.3 Web Mount pack release identity | 3:> **Document ID**：`PIPD-ERRATUM-2026-10-12-PREVIEW3-PROVENANCE` | 4:> **Raised**：2026-10-12 (Asia/Taipei) · **Round**：`S4EXT-R1-20261012-external-challenge-repair` | 5:> **Finding of record**：`F001` of `PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1` (CONFIRMED_DEFECT, P1) | 6:> **Frozen tuple**：`docs/RELEASE_TUPLE.json` · **Status**：`SOURCE_CORRECTED / PUBLISHED_ASSET_REPLACED_IN_PLACE / RELEASE HOLD` | 7:> | 8:> **Reconciled 
docs/FRONT_PAGE_HISTORY.md: 1:# Front-page history moved out of `README.md` (round R6, 2026-10-11) | 3:In round **R6-20261011-main-front-page** the repository front page was rewritten from an | 4:append-only log into a current-state page. Nothing here was deleted — the sections that used to | 5:live on `README.md` and no longer belong on a front page are preserved **verbatim** below, with | 6:their original headings and wording intact. | 8:Two things moved here:
docs/NORMATIVE_SOURCE_MAP.md: 1:# NORMATIVE SOURCE MAP (DERIVED INDEX) | 3:> **This file is a DERIVED INDEX. It is NOT a competing master.** | 4:> | 5:> * The external canonical standard `PIPD-LIFECYCLE-SPEC@1.1.0` remains the **single source of | 6:>   truth**. Nothing in this repository restates, supersedes or re-derives its normative content. | 7:> * This index only **points at** source families: where each lives, who owns it, its version, a | 8:>   digest (or an explicit "not readable here" marker), and which consumers r
docs/OWNER_ADJUDICATION_R4_2026-10-09.json: 1:{ | 2:  "schema": "PIPD-OWNER-ADJUDICATION/1", | 3:  "round": "R4-20261009-focused-repair", | 4:  "issued": "2026-10-09", | 5:  "authority": { | 6:    "act": "owner adjudication + publication authorisation", | 7:    "owner_instruction_zh": "直接執行研究後的建議最佳工程裁決，並且把相關實作內容和證據更新至 GITHUB REPO，讓外部官進行驗收。", | 8:    "basis": "PIPD-LS-SP_R4_PLAN_RULINGS_A1A5V7_2026-10-09 (PLAN lane, GPT 6.1 SOL-MEDIUM, CODEX CLI; FAR-style analysis over the supplied local evidence only)",
docs/OWNER_ADJUDICATION_R4_2026-10-09.md: 1:# Owner adjudication — R4 focused-repair (2026-10-09) | 3:Machine-readable record: `docs/OWNER_ADJUDICATION_R4_2026-10-09.json` (schema `PIPD-OWNER-ADJUDICATION/1`). | 5:**Authority.** The repository owner directed: *"直接執行研究後的建議最佳工程裁決，並且把相關實作內容和證據更新至 | 6:GITHUB REPO，讓外部官進行驗收"* — execute the recommended engineering rulings, and publish the implementation and | 7:evidence to the GitHub repo for external verification.
docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json: 1:{ | 2:  "schema": "PIPD-OWNER-ADJUDICATION/1", | 3:  "round": "R5-20261009-s4-user-operability", | 4:  "issued": "2026-10-10", | 5:  "authority": { | 6:    "act": "owner adjudication executed on the owner's instruction", | 7:    "owner_instruction_zh": "直接執行FAR研究後建議的裁決", | 8:    "basis": "知識庫/實作相關DOC/PIPD/實作證據/PIPD-LS-SP_R5_S4_FAR_S2PERF_LICENSE_2026-10-10.md with .hgk/far/FAR-PIPD-R5S4-S2PERF-LICENSE-001/EVIDENCE_S2PERF.json; the FAR study measured the artefact rather than assuming the thresh
docs/ROUND3_DISCLOSURE.md: 1:# 本回合揭露（ROUND 3，撰寫於 repo 外，待複驗回收後併入） | 3:## 1. 模型 SoD 與 lane 指派（現行實測） | 5:| 角色 | lane | provider / model | 實測 | | 6:|---|---|---|---| | 7:| PLANNING（HGK lifecycle / admission） | 主 | openai-codex / `gpt-6.1-sol`（OpenAI OAuth） | 2026-10-08 22:59 遭 HTTP 429，額度 00:26 重置 | | 8:| PLANNING 備援 #1 | 第一備援 | **nvidia / `z-ai/glm-5.3`** | 直連 HTTP 200 `served_as='z-ai/glm-5.3'`；CLI 端到端 `LANE_OK` |
docs/ROUND_DISCLOSURE.md: 1:# Round disclosure — PIPD-LS-SP governed round (2026-10-08) | 3:Everything anomalous about this round is listed here on purpose. Nothing below is a | 4:"known limitation we accepted quietly". | 6:## 1. Profile escalation was not requested but was applied | 8:The S1 vertical slice is described as a **LITE** slice. The pipeline **escalated the run to
docs/S0_CONTRACT_SPEC.md: 1:# PIPD-LS-SP S0 Canonical Machine Contract Spec — exact 19/19 | 3:Source (NORMATIVE): `PIPD-LS-SP_藍圖.md` §7.3 "Canonical Machine Contracts — exact 19/19" | 4:(sha256 6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a for the | 5:canonical standard; the blueprint file digest is recorded in the source manifest). | 7:Bootstrap order (`.pipd` §5.6.1): 01 standard lock, 02 project manifest, 03 schemas/registry, | 8:04 package index, 05 PI/PD objects, 06 policies/currentness/execution 
docs/S4_SPEC_DEL_ADJUDICATION.json: 1:{ | 2: "schema": "PIPD-S4-SPEC-DEL-ADJUDICATION/1", | 3: "claim_ceiling": "MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION", | 4: "subject": { | 5:  "baseline_main_commit": "0a05f4fde899d5990a8c098e3feaa2d9d1d7e0de", | 6:  "crosswalk": "docs/SPEC_DEL_CROSSWALK.json", | 7:  "crosswalk_schema": "PIPD-SPEC-DEL-CROSSWALK/1", | 8:  "crosswalk_counts": {
docs/SPEC_DEL_CROSSWALK.json: 1:{ | 2:  "schema": "PIPD-SPEC-DEL-CROSSWALK/1", | 3:  "blueprint": "PIPD-LS-SP_藍圖.md", | 4:  "counts": { | 5:    "SPEC": 32, | 6:    "DEL": 25, | 7:    "total": 57 | 8:  },
docs/USER_GUIDE.md: 1:# PIPD-LS-SP — user guide | 3:**This is the only user guide.** It is task-first: find the row for what you are trying to do and | 4:follow it. It is *not* a second installation document — version pins, hashes, the fetch commands, | 5:uninstall and rollback live in exactly one place, [`docs/install/README.md`](install/README.md), and | 6:this guide links there rather than copying it. | 8:Three ceilings apply to everything below, and no result here can lift them:
docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md: 1:# ADR-0001 — The package root manifest is the official Agent Plugins 1.0 manifest | 3:- Status: ACCEPTED (Stage B candidate; nothing is published by this decision) | 4:- Date: 2026-10-12 | 5:- Scope: `packaging/public-plugin/**`, `tools/build_public_plugin.py`, | 6:  `tests/test_public_plugin_packaging.py` | 8:## Context
docs/adr/ADR-0007-plugin-distribution-private-first.md: 1:# ADR-0007 — Plugin distribution: private-first, public directory on hold | 3:- **Status:** accepted 2026-10-14 (owner ruling in chat, executed by the round `R5Z-20261014-session-conformance`) | 4:- **Context:** the plan of record asked for a ChatGPT plugin listing. On 2026-10-14 the agent drove | 5:  `platform.openai.com/plugins` with the desktop tooling and the Portal answered *“You need a verified | 6:  developer identity before you can create or upload a plugin.”* Identity/KYC is a human a
docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md: 1:# ADR-0008 — Repository state and branch/PR hygiene inventory | 3:- **Status**: Accepted (round `R7-20261014-merge-hygiene-closeout`, 2026-10-14) | 4:- **Context**: after PR #8 was merged into `main` under explicit owner authorization, the repository held | 5:  19 branches and six pull requests; the state and what may be cleaned had to be recorded and bound to | 6:  rules so a later session cannot delete a verifiability anchor by accident. | 7:- **Decision**: keep every branch that an evidence
docs/adr/ADR-0009-session-handover-and-next-session-start.md: 2:## 0. Re-read main before acting | 4:`main` at the time of writing: `fc55591852bc016ae8dc861edf88db0e613b3c6a` (merge of PR #9; PR #8 merged at | 5:`b3a27c1f00c90b010feec7b4da5f420d45edec61`). Any session that starts later must re-read `main` rather than trust | 6:this line: run `git -C <clone> fetch origin && git -C <clone> rev-parse origin/main` first, and treat the evidence | 7:branch (`r5z-evidence-return-20261014`) as the place where the frozen receipts live.
docs/install/ASSET_READBACK_v0.1.1-preview.4.json: 1:{ | 2: "schema": "PIPD-LS-SP/asset-readback/1", | 3: "subject_release": "v0.1.1-preview.4", | 4: "measured_at": "2026-10-16", | 5: "what_this_is": "A repository-side verification record, NOT a release asset: every value below was measured by downloading the asset GitHub serves for this release and hashing the bytes locally, then parsing the release's own SHA256SUMS and comparing. It exists so the identity test can cross-check the documented tuple against the served bytes without trusting a mak
docs/install/PIPD_AGENT_INSTALL_PROMPT.md: 1:# PIPD-LS-SP — Agent 安裝提示詞(單一貼上即用) | 3:這份文件**就是** Agent route 的安裝入口:一整段可複製的提示詞(prompt)。它本身不安裝任何東西、 | 4:不執行任何指令、不代表任何 acceptance 或發佈狀態——被安裝與被驗證的是 **host**(Hermes Agent / | 5:Codex Desktop (GUI) / Codex CLI / Claude Code),而 host 必須自己證明它的版本、discovery 與生效載入。 | 7:使用方式:把下面 ```text 區塊**整段**複製,貼進你的 agent host 對話,然後依它的提問回答。全程保留 | 8:英文識別字(host 名稱、skill 名稱、狀態字如 `NOT_VERIFIED`、`REFUSED`)不要翻譯。
docs/install/PIPD_WEB_FALLBACK.md: 1:<!-- PIPD-WEB-FALLBACK/1 DOC_MOUNT_ONLY --> | 2:# PIPD-LS-SP S4 Web fallback — single-document mount (DOC_MOUNT_ONLY) | 4:- release_id: v0.1.1-preview.3 | 5:- release_commit: cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a | 6:- doc_mount_only: true | 7:- member_count: 8 | 8:- size_cap_bytes: 524288
docs/install/PIPD_WEB_FALLBACK.md.sha256: 1:c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af *docs/install/PIPD_WEB_FALLBACK.md
docs/install/README.md: 1:# PIPD-LS-SP — install (single source of truth) | 3:This page is the **install SSOT**: every other page that mentions installing PIPD-LS-SP either is | 4:this page or points at it. There are **two install routes and only two** — **Web** and **Agent** — | 5:and they have different ceilings. Pick one, read its ceiling, and do not read a green build (or a | 6:copied file) as anything more than what the [states table](#states-that-are-not-the-same) below says. | 8:Version pin for everything on thi
EXTENSION DOC MATCHES
docs/ROUND3_DISCLOSURE.md:70: 3. 新增 `tests/test_secret_patterns.py`：**六個樣式全部釘住**（原本只有 `github_pat_` 被間接測到，其餘五個無測試，會靜默腐化）+ 加寬不得變成濫配 + 不得命中普通散文。測試數 **22 → 26**。
docs/ROUND3_DISCLOSURE.md:72: 5. **`history_secret_scan.json` 重生**：原版記錄的是被 supersede 的樣式名稱（kernel 內 module 快取所致），與其宣稱的 revision 不符 → 改為獨立子行程新鮮 import，並新增 `source_sha256` 與 `worktree_files_scanned`。此為**我方產物的正確性缺陷，自行揭露**。
docs/ROUND3_DISCLOSURE.md:80: - **A2（NOT_REPRODUCED）**：新增的 `tests/test_secret_patterns.py` **缺 `sys.path` bootstrap**，`python -m unittest tests.test_secret_patterns -v` 直接以 `ModuleNotFoundError` 失敗；只因 discovery 時字母序較前的測試檔改了 `sys.path` 才「看起來會過」。**這正是我先前指出的測試腐化類別，我自己犯了。**
docs/ROUND3_DISCLOSURE.md:87: 2. `history_secret_scan.py` 欄位改名為 `source_revision_scanned`，並新增 `candidate_binding` 明示語意：「描述該來源 revision；本檔由後續的 evidence-only commit 提交，且其 `src/ tests/ schemas/` 與該 revision 相同」。
docs/ROUND3_DISCLOSURE.md:115: 2. 新增 `tests/test_tooling_executes.py`（**守門測試**，3 項）：
docs/ROUND3_DISCLOSURE.md:136: 1. 新增 `_tracked_file_count(root)`：若有可用的 git checkout 則以 `git ls-files` 計數（名副其實），否則退回「排除 `.git`/`__pycache__` 的樹內檔案數」。實測 `170 == git ls-files 170`。
docs/ROUND3_DISCLOSURE.md:143: **累積模式（值得記錄）**：本回合的兩個最嚴重缺陷（`read_text` 的 `newline`、`.git` 計數）**都不是被獨立驗收抓到的**，而是「獨立驗收的附註」或「我方事後重跑」才浮現。共同根因是同一類：**我用來做證據的工具本身缺乏回歸測試**。目前已以 `tests/test_tooling_executes.py`（5 項）建立守門，並實測其有效性；但 `run_s1_slice.py`、`history_secret_scan.py`、`build_evidence_md.py`、`build_evidence_manifest.py`、`github_publish.py` 仍未被測試釘住 —— 此結構性缺口記入 TT，不宣稱已解。
docs/ROUND3_DISCLOSURE.md:172: - 本輪新增 2 列：`TT-ORACLE-DISAGREEMENT-KP-R04`（OPEN，待授權來源 ratify）、`TT-PRE-W3-CROSS-PROJECT`（**TEMP_CLOSED**，獨立關閉、不從 S0–S4 證據推導，HITL owner：SWOF GENIE PRE-W3 owner）。真實分母 17：1 CLOSED / 4 PARTIAL / 9 OPEN / 2 OPEN_OWNER_GATE / 1 TEMP_CLOSED。
docs/adr/ADR-0007-plugin-distribution-private-first.md:9:   ChatGPT (`Plugins → Add → Upload plugin archive`), installed, and its skills invoked from a chat. The public
docs/install/PIPD_AGENT_INSTALL_PROMPT.md:54:   哪些新增、哪些覆寫、哪些衝突。
docs/install/PIPD_WEB_FALLBACK.md:106: > authority, a new skill and not a second source of truth.
docs/install/PIPD_WEB_FALLBACK.md:306: This pack's `SKILL.md` is a **dispatcher over these eight skills** — it adds none. Each skill below
```


### Post-suite path probe


Raw excerpt *(command: post-suite path probe, exit code 0)*

```bash
git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt status --porcelain && python -c 'from pathlib import Path; import datetime; r=Path("C:/Projects/Agent_Workspace/PIPD-S4R6-wt"); p=r/"openspec/changes/pipd-r18-external-engineering-handover"; print("UNTRACKED_PATH_EXISTS",p.exists()); [(print(str(f.relative_to(r)).replace(chr(92),"/"),"bytes="+str(f.stat().st_size),"mtime="+datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat())) for f in sorted(p.rglob("*")) if f.is_file()]; print("DOCS_REPO_STATE_EXISTS",(r/"docs/REPO_STATE.md").exists())'
```


Raw excerpt *(output: post-suite path probe)*

```text
?? openspec/changes/pipd-r18-external-engineering-handover/
UNTRACKED_PATH_EXISTS True
openspec/changes/pipd-r18-external-engineering-handover/proposal.md bytes=2593 mtime=2026-10-16T11:43:15.403082+00:00
openspec/changes/pipd-r18-external-engineering-handover/specs/pipd-round-handover-entry/spec.md bytes=3941 mtime=2026-10-16T11:43:37.965186+00:00
openspec/changes/pipd-r18-external-engineering-handover/tasks.md bytes=2153 mtime=2026-10-16T11:43:15.445164+00:00
DOCS_REPO_STATE_EXISTS False
```


### Initial prerequisite/clean-status probe


Raw excerpt *(command: initial prerequisite probe, exit code 0)*

```bash
python -c 'from pathlib import Path; paths=[Path("C:/AGENTS.md"),Path("C:/Projects/AGENTS.md"),Path("C:/Projects/Agent_Workspace/AGENTS.md"),Path("C:/Projects/Agent_Workspace/PIPD-S4R6-wt/AGENTS.md")]; [(print("=== "+str(p)+" ==="),print(p.read_text(encoding="utf-8") if p.exists() else "ABSENT")) for p in paths]' && git -C "C:/Projects/Agent_Workspace/PIPD-S4R6-wt" rev-parse HEAD && git -C "C:/Projects/Agent_Workspace/PIPD-S4R6-wt" status --porcelain
```


Raw excerpt *(output: initial prerequisite probe; no porcelain lines followed HEAD)*

```text
=== C:\AGENTS.md ===
ABSENT
=== C:\Projects\AGENTS.md ===
ABSENT
=== C:\Projects\Agent_Workspace\AGENTS.md ===
ABSENT
=== C:\Projects\Agent_Workspace\PIPD-S4R6-wt\AGENTS.md ===
ABSENT
127ec1ca97c71d0437f5b149a6e7d540d0cb3bba
```


### Final HEAD/status probe


Raw excerpt *(command: final HEAD/status probe, exit code 0)*

```bash
git -C "C:/Projects/Agent_Workspace/PIPD-S4R6-wt" rev-parse HEAD && git -C "C:/Projects/Agent_Workspace/PIPD-S4R6-wt" status --porcelain
```


Raw excerpt *(output: final HEAD/status probe)*

```text
127ec1ca97c71d0437f5b149a6e7d540d0cb3bba
?? openspec/changes/pipd-r18-external-engineering-handover/
```

- Additional broken documentary reference: `docs/REPO_STATE.md` is ABSENT at this checkout, although ADR-0009 lists it as the repository hygiene inventory; the existing inventory document is ADR-0008. *(output: post-suite path probe; docs/adr/ADR-0009-session-handover-and-next-session-start.md:71; docs/adr/ADR-0008-repository-state-and-hygiene-inventory.md:1)*
