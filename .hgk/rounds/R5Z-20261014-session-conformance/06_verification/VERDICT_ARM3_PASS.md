## R5Z-20261014-session-conformance ~ VERIFY_SECURITY arm3

- arm3: True
- attempt: 3
- engine: codex-cli
- self_reported_arm: opencode-go/glm-5.3-flash
- subject_sha256: a431ac09342d5e55dc88004d540fb59d08d2cdd20deb2c923788290c75d4f0ba
- overall: PASS
- unresolved_locators: []

### Regression spot-checks

- PKG 11/11 sha256 recompute: PASS (11/11)
- ZIP rebuilt at 062d84a -> 68355 bytes, sha256 2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199
- ZIP structure: 56 entries, 8 SKILL.md, root plugin.json: ['pipd-ls-sp-public-skills/plugin.json']
- camelCase fields: all seven present (missing: [])

### Item-by-item checks

- 1.1_pkg_alignment_round_root: PASS
- 1.2_r5x_final_result_axes: PASS
- 1.3_pat_path_exists: PASS
- 1.4_branch_commit_blob: PASS
- 1.5_branch_3f2f095_ancestor: PASS
- 2_locators: PASS
- 3_regression: None
- 4_files_created: PASS

### Versioned subject states

- attempt1_initial: 557f98828696ad616ec4db4ea66a6d2dc98a18561d9d6a43b32589d92b10a7ee (original required sha256; elapsed during lane activity; setup persists in read_probe.py log.)
- attempt2_recheck: 62f8e5390b7729036dc6a2484276cf07fa2ad2adaea2a9dd769384cbb9b08f09 (snapshot the earlier full recheck was performed against.)
- attempt3_final: a431ac09342d5e55dc88004d540fb59d08d2cdd20deb2c923788290c75d4f0ba (current arm3 check basis; concurrently appended by the revising maker between the run's start and end.)

### Files created under arm3 (anti-mutation)

- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\annotate.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\api_heads.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\api_heads_out.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\auth_probe.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\build_locators_final.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\c\pipd-ls-sp-public-skills.zip
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\c\pipd-ls-sp-public-skills.zip.sha256
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\c\RELEASE_RECEIPT.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\c\SOURCE_TO_PLUGIN_MAPPING.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\fetch_heads.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\inspect_heads.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\locator_sweep.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\locator_sweep.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\locator_sweep_final.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\pat_probe.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\ratelimit_probe.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\read_citations.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\read_probe.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\scope_probe.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\subject_lines.txt
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\subject_rescan.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\subject_rescan2.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\subject_tail.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\VERDICT_ARM3.json
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\VERDICT_ARM3.md
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\write_final_verdict.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\write_verdict.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\write_verdict_v3.py
- C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance\VERIFY_SECURITY\arm3\zip_inspect.py

### Scope limitations

- Subject was concurrently revised by the lane's maker during this check; tracked via the versioned_subject_states table.
- Authenticated-API remote head probe under item 1.5 could not run with the PAT on file (404); the check local-ancestor check was completed, but the API head printout is not asserted in this verdict.
- The authenticating PAT granted /user (200) but denied /repos/shw097-team/PIPD-LS-SP (404), consistent with a fine-grained repo-scoped token whose authorized repo is outside the verifier's environment.

**Arm binding:** the dispatcher receipt is the binding evidence for the served arm; my self-report is advisory only.

