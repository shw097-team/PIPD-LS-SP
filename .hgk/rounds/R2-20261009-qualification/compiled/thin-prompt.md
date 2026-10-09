# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-S0S4-CONTINUATION-FAR-R2
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: 在現有 public Repo 與 S0/S1 基線上，以 CONTINUATION 續建 PIPD-LS-SP 至 S0_TO_S4_INDEPENDENT_PRODUCT_DELIVERED：完成可獨立安裝、可執行、可重播、可驗收的 Pre-Implementation & Pre-Dev Lifecycle Engineering Compiler（19 contracts／8 Skills／3 Golden Pilots／5 Web Pack／至少 3 Host projections／13 CLI＋SDK／deterministic compile-validate-explain-dryrun-replay／安裝升級卸載／回退／效能與上下文預算）。
Expected outcome: 同一候選上 S0~S4 全部必要 Gate PASS，並有獨立驗收官判定；S5~S8 僅交付 typed seam 與 Integration Backlog。
ChangeSet: CONTINUATION
Affected domains: src/pipd_ls_sp, schemas, tests, tools, docs, fixtures, dist, openspec, .hgk

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R1 知識庫/工程基座/GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack/ 00_KNOW_INDEX.md §1..19_KP_INDEX_CROSSWALK.md role=NORMATIVE
- R1 知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD_LS/ PIPD_LS_canonical_standard.md#standard_id=PIPD-LIFECYCLE-SPEC role=NORMATIVE
- R1 知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/ PIPD-LS-SP_藍圖.md ; PIPD-LS-SP_PIPD-EC_SGM_總藍圖.md §5.1-5.3 ; PIPD-LS-SP_PIPD-PKG-00..10 role=NORMATIVE
- R2 知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/SKILLS_PLUGIN/ SDLC_PRW_HLPE_SKILLS_PLUGIN_R2.md ; SWOF_ECP_SKILLS_PLUGIN_v2.0.1.md ; SWOF_TQAEP_SKILLS_PLUGIN_v2.0.1.md role=SUPPORT
- R1 知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/ construction-acceptance-prompt-compiler_SKILL.md ; scripts/prompt_contract_compiler.py ; HG-KSEOS使用說明文檔.md §3-10 ; Fabric使用說明文檔.md §2-3 role=NORMATIVE
- R1 C:\Projects\Agent_Workspace\HG-KSEOS ; C:\Projects\Agent_Workspace\Fabric HG-KSEOS/AGENTS.md ; config/hermes.json#HGK-HERMES-BINDING/2 ; var/shared-spine/hg-kseos.db ; Fabric/{control,contracts,assurance} role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 使用者以自然語言即可觸發 lifecycle，取得可供合法 Receiver 接收的施工前契約；任何未閉合項以 typed error 明確呈現，不以檔案存在冒充可用。
Constraints:
- HG-KSEOS 為唯一控制平面；Hermes 為受治理 Runtime／Orchestration Plane
- Knowledge 視圖為 derived/read-only，共用 HGK SharedSpine typed API
- 不得建立第二 WorkOrder／RBWI／Reducer／Task DB／Canonical Plan IR
- 所有一般工程決策由 FAR 自動研究裁決後執行，不因技術歧義反覆詢問使用者
- 寫入權限限 PIPD 產品根目錄內；GitHub 僅更新既有 public Repo，不重建、不 force-push
Non-goals:
- S5 真實 HGK Receiver Shadow／Canary execution
- S6 真實 GENIE Product Compiler
- S7 JIT runtime world-effect factory
- S8 SGM authority cutover
- SWOF 整體工程工廠與 Fabric sealed RP-002／SQP1／Stage-3 修改或 production deployment
Authorized mutations:
- PIPD 產品根目錄內檔案新增／修改／搬移／刪除／重構
- 更新既有公開 Repo shw097-team/PIPD-LS-SP 與單檔驗收證據 MD
- 建立／更新 HGK requirement／taskspec／workorder／checkpoint 與 Kanban 卡
- 執行 FAR 研究並輸出 Gate-1 決策（研究層，非 acceptance）
Forbidden mutations:
- 建立第二 HGK 控制平面／RBWI／Reducer／Task DB
- SharedSpine 原生 SQL 寫入
- PIPD root 外寫入
- Maker 自批獨立驗收
- 公開任何憑證內容
- force-push 覆蓋公開 main
- 把舊候選 checker verdict 轉移到新 HEAD
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_SOURCE_AUTHORITY_FREEZE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_INTENT_REQUIREMENT_ATOM: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_PROFILE_TRIO: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_SEARCH_BEFORE_BUILD_TECH_ADMISSION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_PI_COMPILER: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_PD_BINDER_REPOCONTEXT: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_TASKSPEC_CONSTRUCTION_CONTRACT: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_ECP_TQAEP: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_TRACE_EVIDENCE_CLAIM: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_EIGHT_LOGICAL_SKILLS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_NINETEEN_CONTRACT_FAMILIES: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_DETERMINISTIC_VALIDATORS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_THREE_GOLDEN_PILOTS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_WEB_PACK_5_HOST_PROJECTIONS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_CLI_SDK_13_COMMANDS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_BOUNDED_REPAIR_ROLLBACK: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_KNOWLEDGE_READY_GATE: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CAP_FAR_AUTONOMOUS_RESEARCH: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CAP_HGK_ADMITTED_WORKORDER_EXECUTION: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CAP_TECHNOLOGY_ADMISSION_22: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_THREE_GOLDEN_PILOTS: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_NRTV_JUDGE_CALIBRATION: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_ROLLBACK_READBACK: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_PERF_CONTEXT_BUDGET: ACTIVE_REQUIRED; action=ENABLE; runtime_required=false
- CAP_PORTABLE_RELEASE_INSTALL: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_WEB_PACK_5: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_HOST_PROJECTIONS_3: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_COMPATIBILITY_LOSS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_SKILL_MANAGED_VENDORED_ISOLATION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_CLI_13_COMMANDS_SDK: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_DETERMINISTIC_COMPILER_STATE_MACHINE: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_EXPLAIN_DRYRUN_REPLAY: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_TYPED_ERRORS: ACTIVE_REQUIRED; action=ENABLE; runtime_required=false
- CAP_SECURITY_HOLDOUT_REGRESSION: ACTIVE_REQUIRED; action=ENABLE; runtime_required=true
- CAP_INDEPENDENT_ACCEPTANCE_OFFICER: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
Non-active:
- CAP_HGK_SHADOW_CANARY_RECEIVER: DEFERRED_SOURCE_BACKED; action=DESIGN
- CAP_GENIE_OBJECT_PROJECTION: DEFERRED_SOURCE_BACKED; action=DESIGN
- CAP_JIT_TEAM_ACTIVATION: DEFERRED_SOURCE_BACKED; action=DESIGN
- CAP_EXTERNAL_SAAS: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_EXTRA_VECTOR_KG_STORE: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_MCP_BRIDGE: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_REMOTE_EXECUTION: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_TOOL_MODEL_PROVIDER_SWITCH: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_SGM_CUTOVER: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP_PRODUCTION_DEPLOY: PROHIBITED; action=PROHIBIT
- CAP_FABRIC_SQP1_ESCALATION: PROHIBITED; action=PROHIBIT
- CAP_MAKER_SELF_ACCEPTANCE: PROHIBITED; action=PROHIBIT
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- 已 SI 驗證的 S0 19/19 contract 家族語意（僅可加測不可改語意）
- 已驗證的 S1 genuine vertical slice 行為
- 已發布的歷史 commit（不得改寫）
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_SOURCE_AUTHORITY_FREEZE: verdict=NOT_READY; work=materialize runtime closure for CAP_SOURCE_AUTHORITY_FREEZE in S2..S4 with raw receipts
- CAP_INTENT_REQUIREMENT_ATOM: verdict=NOT_READY; work=materialize runtime closure for CAP_INTENT_REQUIREMENT_ATOM in S2..S4 with raw receipts
- CAP_PI_COMPILER: verdict=NOT_READY; work=materialize runtime closure for CAP_PI_COMPILER in S2..S4 with raw receipts
- CAP_PD_BINDER_REPOCONTEXT: verdict=NOT_READY; work=materialize runtime closure for CAP_PD_BINDER_REPOCONTEXT in S2..S4 with raw receipts
- CAP_TASKSPEC_CONSTRUCTION_CONTRACT: verdict=NOT_READY; work=materialize runtime closure for CAP_TASKSPEC_CONSTRUCTION_CONTRACT in S2..S4 with raw receipts
- CAP_ECP_TQAEP: verdict=NOT_READY; work=materialize runtime closure for CAP_ECP_TQAEP in S2..S4 with raw receipts
- CAP_TRACE_EVIDENCE_CLAIM: verdict=NOT_READY; work=materialize runtime closure for CAP_TRACE_EVIDENCE_CLAIM in S2..S4 with raw receipts
- CAP_EIGHT_LOGICAL_SKILLS: verdict=NOT_READY; work=materialize runtime closure for CAP_EIGHT_LOGICAL_SKILLS in S2..S4 with raw receipts
- CAP_NINETEEN_CONTRACT_FAMILIES: verdict=NOT_READY; work=materialize runtime closure for CAP_NINETEEN_CONTRACT_FAMILIES in S2..S4 with raw receipts
- CAP_DETERMINISTIC_VALIDATORS: verdict=NOT_READY; work=materialize runtime closure for CAP_DETERMINISTIC_VALIDATORS in S2..S4 with raw receipts
- CAP_CLI_SDK_13_COMMANDS: verdict=NOT_READY; work=materialize runtime closure for CAP_CLI_SDK_13_COMMANDS in S2..S4 with raw receipts
- CAP_BOUNDED_REPAIR_ROLLBACK: verdict=NOT_READY; work=materialize runtime closure for CAP_BOUNDED_REPAIR_ROLLBACK in S2..S4 with raw receipts
- CAP_KNOWLEDGE_READY_GATE: verdict=NOT_READY; work=materialize runtime closure for CAP_KNOWLEDGE_READY_GATE in S2..S4 with raw receipts
- CAP_FAR_AUTONOMOUS_RESEARCH: verdict=NOT_READY; work=materialize runtime closure for CAP_FAR_AUTONOMOUS_RESEARCH in S2..S4 with raw receipts
- CAP_HGK_ADMITTED_WORKORDER_EXECUTION: verdict=NOT_READY; work=materialize runtime closure for CAP_HGK_ADMITTED_WORKORDER_EXECUTION in S2..S4 with raw receipts
- CAP_THREE_GOLDEN_PILOTS: verdict=NOT_READY; work=materialize runtime closure for CAP_THREE_GOLDEN_PILOTS in S2..S4 with raw receipts
- CAP_NRTV_JUDGE_CALIBRATION: verdict=NOT_READY; work=materialize runtime closure for CAP_NRTV_JUDGE_CALIBRATION in S2..S4 with raw receipts
- CAP_ROLLBACK_READBACK: verdict=NOT_READY; work=materialize runtime closure for CAP_ROLLBACK_READBACK in S2..S4 with raw receipts
- CAP_PORTABLE_RELEASE_INSTALL: verdict=NOT_READY; work=materialize runtime closure for CAP_PORTABLE_RELEASE_INSTALL in S2..S4 with raw receipts
- CAP_WEB_PACK_5: verdict=NOT_READY; work=materialize runtime closure for CAP_WEB_PACK_5 in S2..S4 with raw receipts
- CAP_HOST_PROJECTIONS_3: verdict=NOT_READY; work=materialize runtime closure for CAP_HOST_PROJECTIONS_3 in S2..S4 with raw receipts
- CAP_CLI_13_COMMANDS_SDK: verdict=NOT_READY; work=materialize runtime closure for CAP_CLI_13_COMMANDS_SDK in S2..S4 with raw receipts
- CAP_DETERMINISTIC_COMPILER_STATE_MACHINE: verdict=NOT_READY; work=materialize runtime closure for CAP_DETERMINISTIC_COMPILER_STATE_MACHINE in S2..S4 with raw receipts
- CAP_EXPLAIN_DRYRUN_REPLAY: verdict=NOT_READY; work=materialize runtime closure for CAP_EXPLAIN_DRYRUN_REPLAY in S2..S4 with raw receipts
- CAP_SECURITY_HOLDOUT_REGRESSION: verdict=NOT_READY; work=materialize runtime closure for CAP_SECURITY_HOLDOUT_REGRESSION in S2..S4 with raw receipts
- CAP_INDEPENDENT_ACCEPTANCE_OFFICER: verdict=NOT_READY; work=materialize runtime closure for CAP_INDEPENDENT_ACCEPTANCE_OFFICER in S2..S4 with raw receipts
Required user journeys:
- J1_NL_SPEC_PACKAGE: 用一句自然語言需求取得綁定來源的 PI 與 PD 施工前契約包 → 一份 PI/PD package（含 source binding、claim ceiling），可在 CLI 以 --json 讀出
- J2_REPO_IMPORT_PD_LATEBINDING: 對真實 Brownfield repo 做 PD late binding → RepoContext（root/head/tracked_files/writable_scope）與 PD 決策
- J3_HGK_HANDOFF: 產出 HGK 相容的 ConstructionContract／ECP／TQAEP（僅契約相容，不冒稱 S5 live ACK） → 可被合法 Receiver 接收的施工前契約三件套
- J4_TEST_REPAIR: 偵測篡改→限縮修補→回歸 → bounded repair 只動 affected edges，rollback pointer 可還原
- J5_CROSS_HOST_EXPORT: 跨 Host 可攜使用（至少三種 Host projection） → 同一候選在多 Host 的 effective-load 與語意一致
- J6_GITHUB_PUBLIC_DELIVERY: 產物在乾淨機器可重裝、GitHub 公開讀回、外部可核證 → public repo 的 commit SHA 與匿名讀回一致
Acceptance predicates:
- ACC-CAP_SOURCE_AUTHORITY_FREEZE subject=CAP_SOURCE_AUTHORITY_FREEZE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_INTENT_REQUIREMENT_ATOM subject=CAP_INTENT_REQUIREMENT_ATOM depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_PROFILE_TRIO subject=CAP_PROFILE_TRIO depth=L2_UNIT_BEHAVIOR
- ACC-CAP_SEARCH_BEFORE_BUILD_TECH_ADMISSION subject=CAP_SEARCH_BEFORE_BUILD_TECH_ADMISSION depth=L2_UNIT_BEHAVIOR
- ACC-CAP_PI_COMPILER subject=CAP_PI_COMPILER depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_PD_BINDER_REPOCONTEXT subject=CAP_PD_BINDER_REPOCONTEXT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_TASKSPEC_CONSTRUCTION_CONTRACT subject=CAP_TASKSPEC_CONSTRUCTION_CONTRACT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_ECP_TQAEP subject=CAP_ECP_TQAEP depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_TRACE_EVIDENCE_CLAIM subject=CAP_TRACE_EVIDENCE_CLAIM depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_EIGHT_LOGICAL_SKILLS subject=CAP_EIGHT_LOGICAL_SKILLS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_NINETEEN_CONTRACT_FAMILIES subject=CAP_NINETEEN_CONTRACT_FAMILIES depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_DETERMINISTIC_VALIDATORS subject=CAP_DETERMINISTIC_VALIDATORS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_THREE_GOLDEN_PILOTS subject=CAP_THREE_GOLDEN_PILOTS depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-CAP_WEB_PACK_5_HOST_PROJECTIONS subject=CAP_WEB_PACK_5_HOST_PROJECTIONS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_CLI_SDK_13_COMMANDS subject=CAP_CLI_SDK_13_COMMANDS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_BOUNDED_REPAIR_ROLLBACK subject=CAP_BOUNDED_REPAIR_ROLLBACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE subject=CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-CAP_KNOWLEDGE_READY_GATE subject=CAP_KNOWLEDGE_READY_GATE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_FAR_AUTONOMOUS_RESEARCH subject=CAP_FAR_AUTONOMOUS_RESEARCH depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_HGK_ADMITTED_WORKORDER_EXECUTION subject=CAP_HGK_ADMITTED_WORKORDER_EXECUTION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_TECHNOLOGY_ADMISSION_22 subject=CAP_TECHNOLOGY_ADMISSION_22 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_THREE_GOLDEN_PILOTS subject=CAP_THREE_GOLDEN_PILOTS depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-CAP_NRTV_JUDGE_CALIBRATION subject=CAP_NRTV_JUDGE_CALIBRATION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_ROLLBACK_READBACK subject=CAP_ROLLBACK_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_PERF_CONTEXT_BUDGET subject=CAP_PERF_CONTEXT_BUDGET depth=L2_UNIT_BEHAVIOR
- ACC-CAP_PORTABLE_RELEASE_INSTALL subject=CAP_PORTABLE_RELEASE_INSTALL depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-CAP_WEB_PACK_5 subject=CAP_WEB_PACK_5 depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_HOST_PROJECTIONS_3 subject=CAP_HOST_PROJECTIONS_3 depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_COMPATIBILITY_LOSS subject=CAP_COMPATIBILITY_LOSS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_SKILL_MANAGED_VENDORED_ISOLATION subject=CAP_SKILL_MANAGED_VENDORED_ISOLATION depth=L2_UNIT_BEHAVIOR
- ACC-CAP_CLI_13_COMMANDS_SDK subject=CAP_CLI_13_COMMANDS_SDK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_DETERMINISTIC_COMPILER_STATE_MACHINE subject=CAP_DETERMINISTIC_COMPILER_STATE_MACHINE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_EXPLAIN_DRYRUN_REPLAY subject=CAP_EXPLAIN_DRYRUN_REPLAY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_TYPED_ERRORS subject=CAP_TYPED_ERRORS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_SECURITY_HOLDOUT_REGRESSION subject=CAP_SECURITY_HOLDOUT_REGRESSION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_INDEPENDENT_ACCEPTANCE_OFFICER subject=CAP_INDEPENDENT_ACCEPTANCE_OFFICER depth=L3_INTEGRATION_RUNTIME
- ACC-J1_NL_SPEC_PACKAGE subject=J1_NL_SPEC_PACKAGE depth=L3_INTEGRATION_RUNTIME
- ACC-J2_REPO_IMPORT_PD_LATEBINDING subject=J2_REPO_IMPORT_PD_LATEBINDING depth=L3_INTEGRATION_RUNTIME
- ACC-J3_HGK_HANDOFF subject=J3_HGK_HANDOFF depth=L3_INTEGRATION_RUNTIME
- ACC-J4_TEST_REPAIR subject=J4_TEST_REPAIR depth=L3_INTEGRATION_RUNTIME
- ACC-J5_CROSS_HOST_EXPORT subject=J5_CROSS_HOST_EXPORT depth=L3_INTEGRATION_RUNTIME
- ACC-J6_GITHUB_PUBLIC_DELIVERY subject=J6_GITHUB_PUBLIC_DELIVERY depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-01-SOURCE-FREEZE subject=REQ-PIPD-01-SOURCE-FREEZE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-02-INTENT-ATOM subject=REQ-PIPD-02-INTENT-ATOM depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-03-PROFILE subject=REQ-PIPD-03-PROFILE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-05-PI-COMPILER subject=REQ-PIPD-05-PI-COMPILER depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-06-PD-BINDER subject=REQ-PIPD-06-PD-BINDER depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-07-CONSTRUCTION-CONTRACT subject=REQ-PIPD-07-CONSTRUCTION-CONTRACT depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-08-ECP-TQAEP subject=REQ-PIPD-08-ECP-TQAEP depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-09-TRACE-EVIDENCE-CLAIM subject=REQ-PIPD-09-TRACE-EVIDENCE-CLAIM depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-10-PORTABLE-RELEASE subject=REQ-PIPD-10-PORTABLE-RELEASE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-11-PUBLICATION-READBACK subject=REQ-PIPD-11-PUBLICATION-READBACK depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-12-GOLDEN-PILOTS subject=REQ-PIPD-12-GOLDEN-PILOTS depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-13-HOST-PROJECTIONS subject=REQ-PIPD-13-HOST-PROJECTIONS depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-14-DETERMINISTIC-COMPILER subject=REQ-PIPD-14-DETERMINISTIC-COMPILER depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-15-SDK subject=REQ-PIPD-15-SDK depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-16-SECURITY-HOLDOUT subject=REQ-PIPD-16-SECURITY-HOLDOUT depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-17-FAR-GOVERNED subject=REQ-PIPD-17-FAR-GOVERNED depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-18-TECH-ADMISSION subject=REQ-PIPD-18-TECH-ADMISSION depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-19-EIGHT-SKILLS subject=REQ-PIPD-19-EIGHT-SKILLS depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-20-EVIDENCE-MD subject=REQ-PIPD-20-EVIDENCE-MD depth=L2_UNIT_BEHAVIOR
- ACC-DEL_PIPD_PRODUCT_TREE subject=DEL_PIPD_PRODUCT_TREE depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_EXTERNAL_ACCEPTANCE_EVIDENCE_MD subject=DEL_EXTERNAL_ACCEPTANCE_EVIDENCE_MD depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_PUBLIC_GITHUB_REPO_PIPD-LS-SP subject=DEL_PUBLIC_GITHUB_REPO_PIPD-LS-SP depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-DEL_SOURCE_MANIFEST_AND_KNOWLEDGE_READBACK subject=DEL_SOURCE_MANIFEST_AND_KNOWLEDGE_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_COMPILER_CONTRACT_PROMPT_RECEIPTS subject=DEL_COMPILER_CONTRACT_PROMPT_RECEIPTS depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_S4_INDEPENDENT_PRODUCT_ACCEPTANCE subject=DEL_S4_INDEPENDENT_PRODUCT_ACCEPTANCE depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_S5_S8_INTEGRATION_BACKLOG subject=DEL_S5_S8_INTEGRATION_BACKLOG depth=L3_INTEGRATION_RUNTIME
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: LICENSE_DECISION, PUBLICATION_AUTHORITY, SCOPE_EXPANSION_BEYOND_PIPD_ROOT, CREDENTIAL_OR_TTL, POLICY_MANDATED_HITL.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: PASS, PARTIAL, FAIL, TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
