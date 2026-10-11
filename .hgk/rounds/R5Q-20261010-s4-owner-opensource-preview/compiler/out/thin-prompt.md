# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-R5Q-OWNER-OPENSOURCE-PREVIEW-20261010
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Execute the owner-authorised S4 open-source preview release of PIPD-LS-SP: land the owner's Apache-2.0 grant across every license surface, freeze a new immutable release candidate, rebuild and verify the distribution, publish a GitHub prerelease bound to the explicit commit, read it back externally, obtain an independent non-Maker preview verdict and return one evidence pack that keeps DEL-018 and the deferred stages honestly open.
Expected outcome: 一般使用者能在明確的 Preview tag 取得合法授權涵蓋的 source 與可核對 Wheel，在乾淨 venv 依說明安裝，執行 doctor 與 intake→PI→PD→ECP/TQAEP 設計鏈，安全地 project --dry-run／scratch --out 與 export，並清楚知道版本、限制與回報方式。
ChangeSet: CONTINUATION
Affected domains: LICENSE, OWNER_LICENSE_DECISION.yaml, NOTICE, pyproject.toml, SBOM.cdx.json, PROVENANCE.md, README.md, ACCEPTANCE.md, dist, .hgk

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\PROMPT\PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\PROMPT\PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\驗收報告\PIPD_LS_SP_R5P_S0-S4_External_Challenge_CORRECTED_OWNER_OpenSource_Preview_GO_2026-10-10.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\驗收報告\PIPD_LS_SP_R5P_S0-S4_External_Challenge_CORRECTED_OWNER_OpenSource_Preview_GO_2026-10-10.md role=NORMATIVE
- R1 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R5_POST_CHALLENGE_S4_EXTERNAL_EVIDENCE.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R5_POST_CHALLENGE_S4_EXTERNAL_EVIDENCE.md role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/知識庫 C:/Projects/Agent_Workspace/知識庫 role=NORMATIVE
- R1 https://github.com/shw097-team/PIPD-LS-SP@2efc84eac8e1939092c748d5b389b6dd72267aef https://github.com/shw097-team/PIPD-LS-SP@2efc84eac8e1939092c748d5b389b6dd72267aef role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/Fabric C:/Projects/Agent_Workspace/Fabric role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/PIPD@2efc84eac8e1939092c748d5b389b6dd72267aef C:/Projects/Agent_Workspace/PIPD@2efc84eac8e1939092c748d5b389b6dd72267aef role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 使用者只需要 Preview tag、wheel/source 檔案、SHA256 與 Python/jsonschema 版本；不需要知道 WorkOrder、ExecutionBinding 或 provider 識別。
Constraints:
- CONTINUATION：只做 affected-only 的發布／文件／封裝修正，不重做 19 Schema／8 Skills／13 CLI。
- 原生 Prompt Compiler 必須真正執行；FAIL 或 bundle 缺失即 PROMPT_COMPILE_BLOCKED，只准唯讀預檢。
- claim 互不繼承：LOCAL_TESTED ≠ INDEPENDENT_ACCEPTED ≠ RELEASED ≠ PRODUCTION_VERIFIED。
- 新產品二進位不可沿用 bb070a6f 舊 hash；manifest 必須區分 build_input_commit 與 released_commit。
- 12 TT 與 CORR-01..08 逐一保留 current/closure/deferred、owner、原始證據或限制、重新觸發條件。
- DEL-018 維持 FAIL/EVIDENCE_GAP 並在 Preview Notes 明示。
Non-goals:
- 不啟動 R6 大修、不刷新全部 57 個 SPEC/DEL 成 PASS、不修好 22 個未啟用外部技術。
- 不部署 HGK live S5、GENIE S6、JIT S7、SWOF/SGM S8、PRE-W3。
- 不覆寫 main、不 force-push、不修改或移動既有 tag。
- 不建立第二個 Repo、不建立第二套 norm authority。
- 不把 DEL-018 的 exit 1 抹成 PASS，也不為此擴張成新工單。
- 不以 Maker 自簽取代獨立驗收，不宣稱 G_RELEASE_FULL_PASS 或 PRODUCTION_VERIFIED。
Authorized mutations:
- PIPD 產品樹發布相關最小差異：LICENSE、OWNER_LICENSE_DECISION.yaml、NOTICE（新增）、pyproject.toml、SBOM.cdx.json、PROVENANCE.md、README.md、ACCEPTANCE.md 之授權／版本／限制段落。
- PIPD dist/ 重建產物：wheel、*.sha256、SHA256SUMS、WHEEL_MANIFEST.json、source archive。
- PIPD .hgk 證據樹：rounds/R5Q-*（preflight、compiler、admission、license、release、uat、ao、evidence）、kanban、gstack、openspec 變更。
- PIPD openspec/changes 下本輪 change。
- 知識庫 實作相關DOC/PIPD/實作證據 下本輪驗收主檔與 FAR 記錄（不含 Token）。
- GitHub shw097-team/PIPD-LS-SP：新增 release 分支/tag 與 prerelease（不得覆寫 main 或既有 tag）。
Forbidden mutations:
- 不得讀出 PAT 明文，或把 PAT 寫進 repo URL／logs／stdout／prompt／Manifest／evidence／commit。
- 不得覆寫 main、force-push 或修改既有 tag。
- 不得在真 repo/home/cwd/來源祖先執行危險 --out 負例或刪除性試驗。
- 不得把 corpus/donor 材料自動改用 OSI 授權或宣稱擁有其權利。
- 不得 Maker 自簽 Independent／Release／Production PASS，或直接改 HGK/Fabric controls 以繞過 Gate。
- 不得以 Fabric/Hermes 自建第二 norm authority。
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_R5Q_OWNER_LICENSE_GRANT: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_RELEASE_CANDIDATE_FREEZE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_WHEEL_REBUILD_MANIFEST: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_CLEAN_INSTALL_UAT: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_CREDENTIAL_BROKER: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_GITHUB_PRERELEASE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_RELEASE_READBACK: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5Q_SURFACE_ENABLEMENT: ACTIVE_SELECTED; action=QUALIFY; runtime_required=false
- CAP_R5Q_EVIDENCE_PACK: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
Non-active:
- CAP_R5Q_DEL018_GAP_HONEST: DEFERRED_SOURCE_BACKED; action=DESIGN
- CAP_R5Q_S5_S8_SEAMS: DEFERRED_SOURCE_BACKED; action=DESIGN
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- 19 schema 結構與 registry exact set
- 8 個 SkillContract 與 5 份 Web MD 分母
- 13 CLI 名稱與 3 Golden Pilot fixture
- R5 已修的 project --out 安全 resolver 與 export --out 實體輸出
- R5P 已修的 doctor schema truth 與 TQAEP design positive
- 已發布的 GitHub 歷史、既有 tag 與 R3/R4/R5/R5P attestation
- HG-KSEOS／Fabric 封存控制面
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_R5Q_OWNER_LICENSE_GRANT: verdict=NOT_READY; work=WO-R5Q-LICENSE-001: one owner grant that makes LICENSE / SPDX / NOTICE / SBOM / provenance agree on the same identifier
- CAP_R5Q_RELEASE_CANDIDATE_FREEZE: verdict=NOT_READY; work=WO-R5Q-REBUILD-002: an immutable release candidate commit that is NOT the review commit, with build_input/released identity split
- CAP_R5Q_WHEEL_REBUILD_MANIFEST: verdict=NOT_READY; work=WO-R5Q-UAT-003: the shipped wheel carries the granted license metadata and a recomputed hash that is not the old one
- CAP_R5Q_CLEAN_INSTALL_UAT: verdict=NOT_READY; work=WO-R5Q-CREDENTIAL-004: the ACTUAL released wheel bytes pass an ordinary-user install and command chain outside the repo
- CAP_R5Q_CREDENTIAL_BROKER: verdict=NOT_READY; work=WO-R5Q-GITHUB-005: the token is used in memory only; no secret reaches argv, stdout, logs, evidence or any public asset
- CAP_R5Q_GITHUB_PRERELEASE: verdict=NOT_READY; work=WO-R5Q-AO-006: a new immutable tag resolves to the explicit release commit and the release is marked prerelease
- CAP_R5Q_RELEASE_READBACK: verdict=NOT_READY; work=WO-R5Q-DOC-007: an independent readback of repo/tag/commit/tree/release/assets and asset download hashes
- CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY: verdict=NOT_READY; work=a non-Maker checker issues a bounded preview receipt; no FULL independent PASS is manufactured
- CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE: verdict=NOT_READY; work=the public notes name DEL-018, the 12 TT disposition rows and the 28/10/19 denominator without washing them to CLOSED
- CAP_R5Q_EVIDENCE_PACK: verdict=NOT_READY; work=one machine-readable pack plus one human-readable master under the private evidence root, token-free
Required user journeys:
- J1_OWNER_GRANT_LANDING: The owner's grant is recorded once and every license surface in the tree and the wheel agrees with it. → all five surfaces carry the same SPDX identifier and the scope split is stated
- J2_CLEAN_INSTALL_USER_PATH: An ordinary user in a clean venv outside the repository installs the published wheel and runs the documented chain without touching the source checkout. → per-command stdout/stderr/exit plus artifact hashes, mode labelled SOURCE or INSTALLED
- J3_PREVIEW_DOWNLOAD: A third party downloads the preview assets from the release page and verifies them against the published checksums. → asset names, sizes and sha256 are listed next to the checksum file contents
- J4_KNOWN_LIMITATIONS: A reader of the release notes can tell exactly what is not claimed by this preview. → the notes name the deferred stages and the un-certified host surface
- J5_INDEPENDENT_PREVIEW_VERIFY: A checker that did not author the release reproduces the decisive claims from the published bytes. → the verdict names what it re-derived and what it could not
Acceptance predicates:
- ACC-CAP_R5Q_OWNER_LICENSE_GRANT subject=CAP_R5Q_OWNER_LICENSE_GRANT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_RELEASE_CANDIDATE_FREEZE subject=CAP_R5Q_RELEASE_CANDIDATE_FREEZE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_WHEEL_REBUILD_MANIFEST subject=CAP_R5Q_WHEEL_REBUILD_MANIFEST depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_CLEAN_INSTALL_UAT subject=CAP_R5Q_CLEAN_INSTALL_UAT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_CREDENTIAL_BROKER subject=CAP_R5Q_CREDENTIAL_BROKER depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_GITHUB_PRERELEASE subject=CAP_R5Q_GITHUB_PRERELEASE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_RELEASE_READBACK subject=CAP_R5Q_RELEASE_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY subject=CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE subject=CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_SURFACE_ENABLEMENT subject=CAP_R5Q_SURFACE_ENABLEMENT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_EVIDENCE_PACK subject=CAP_R5Q_EVIDENCE_PACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5Q_DEL018_GAP_HONEST subject=CAP_R5Q_DEL018_GAP_HONEST depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5Q_S5_S8_SEAMS subject=CAP_R5Q_S5_S8_SEAMS depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R5Q-LIC-001 subject=REQ-PIPD-R5Q-LIC-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-PKG-002 subject=REQ-PIPD-R5Q-PKG-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-UAT-003 subject=REQ-PIPD-R5Q-UAT-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-CRED-004 subject=REQ-PIPD-R5Q-CRED-004 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-PUB-005 subject=REQ-PIPD-R5Q-PUB-005 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-AO-006 subject=REQ-PIPD-R5Q-AO-006 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5Q-DOC-007 subject=REQ-PIPD-R5Q-DOC-007 depth=L3_INTEGRATION_RUNTIME
- ACC-J1_OWNER_GRANT_LANDING subject=J1_OWNER_GRANT_LANDING depth=L3_INTEGRATION_RUNTIME
- ACC-J2_CLEAN_INSTALL_USER_PATH subject=J2_CLEAN_INSTALL_USER_PATH depth=L3_INTEGRATION_RUNTIME
- ACC-J3_PREVIEW_DOWNLOAD subject=J3_PREVIEW_DOWNLOAD depth=L3_INTEGRATION_RUNTIME
- ACC-J4_KNOWN_LIMITATIONS subject=J4_KNOWN_LIMITATIONS depth=L3_INTEGRATION_RUNTIME
- ACC-J5_INDEPENDENT_PREVIEW_VERIFY subject=J5_INDEPENDENT_PREVIEW_VERIFY depth=L3_INTEGRATION_RUNTIME
- ACC-PROMPT_COMPILER_READBACK subject=PROMPT_COMPILER_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-HGK_ADMISSION_READBACK subject=HGK_ADMISSION_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-OWNER_PREVIEW_DECISION_PACKET subject=OWNER_PREVIEW_DECISION_PACKET depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_LICENSE_DECISION_FAR subject=R5Q_LICENSE_DECISION_FAR depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_RELEASE_CANDIDATE_TUPLE subject=R5Q_RELEASE_CANDIDATE_TUPLE depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_DISTRIBUTION_TUPLE subject=R5Q_DISTRIBUTION_TUPLE depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_CLEAN_INSTALL_UAT_MATRIX subject=R5Q_CLEAN_INSTALL_UAT_MATRIX depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_GITHUB_PRERELEASE_READBACK subject=R5Q_GITHUB_PRERELEASE_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_INDEPENDENT_AO_VERDICT subject=R5Q_INDEPENDENT_AO_VERDICT depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_EVIDENCE_PACK subject=R5Q_EVIDENCE_PACK depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_EVIDENCE_MASTER_MD subject=R5Q_EVIDENCE_MASTER_MD depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_KANBAN_SWARM_RECEIPT subject=R5Q_KANBAN_SWARM_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_GSTACK_ROUTE_READBACK subject=R5Q_GSTACK_ROUTE_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-R5Q_OPENSPEC_CHANGE subject=R5Q_OPENSPEC_CHANGE depth=L1_SCHEMA_CONTRACT
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: LICENSE_DECISION, PUBLICATION_APPROVAL, CREDENTIAL_GATE, PERF_THRESHOLD_RATIFICATION, ORACLE_POLARITY, SCOPE_EXPANSION.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED, PREVIEW_TECHNICAL_GO_OWNER_DECISION_PENDING, RELEASE_POLICY_BLOCKED, STOP_SHIP, BLOCKED_CREDENTIAL, BLOCKED_HITL, FAIL.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
