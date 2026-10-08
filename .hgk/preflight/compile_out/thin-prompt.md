# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-ROUTEOUT-2026-10-08-R1
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Implement the PIPD-LS-SP Pre-Implementation & Pre-Dev Lifecycle Skills Plugin under HG-KSEOS governance: compile vague user intent into source-bound, traceable, profile-aware, evidence-ready, receiver-ready PI->PD->ConstructionContract->ECP/TQAEP/Handoff artifacts, with HGK admission, Kanban/Swarm/GSTACK/OpenSpec/Codex execution surfaces, deterministic validators, and independent acceptance.
Expected outcome: A real, runnable PIPD-LS-SP product tree at C:\Projects\Agent_Workspace\PIPD with source-bound artifacts, tests, evidence, and a single external-acceptance MD; honest stage reporting S0..S8.
ChangeSet: NEW_IMPLEMENTATION
Affected domains: PIPD-LS-SP product tree (PI/PD lifecycle plugin), Host Skills + CLI/SDK surfaces, HGK typed receiver seam, GENIE/JIT-SGM seams, public deliverable + evidence

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
Expected experience: An ordinary user can trigger the lifecycle with natural language and receive a compiled spec package without knowing internal Skill, WorkOrder, Agent or Provider names.
Constraints:
- HG-KSEOS is the only normative control plane; Hermes is the governed runtime/orchestration plane; Codex is the bounded writer.
- Only C:\Projects\Agent_Workspace\PIPD is the product mutation root; HG-KSEOS/Fabric control code is not mutated.
- Every durable mutation rides an admitted HGK WorkOrder with baseline + rollback pointer.
- Claim levels PROMPT_COMPILE_PASS / HGK_ADMITTED / RUNTIME_READY / LOCAL_QUALIFIED / INDEPENDENT_PASS / PUBLICATION_APPROVED / RELEASED / PRODUCTION_VERIFIED are kept separate.
- No secret values are written to chat, argv, logs, git history or evidence.
Non-goals:
- No second HGK control plane, scheduler, reducer, Canonical Plan IR, Task DB or release authority.
- No copying of Fabric authority or enabling Apps/Actions/MCP/external providers without admission.
- No unbounded self-evolution, no self-issued INDEPENDENT_PASS or PRODUCTION_PASS.
- No claiming runtime/effect PASS from docs, schemas, README or green CI.
- No inheriting a previous Stage PASS into a new Stage.
Authorized mutations:
- Create/modify/rename/restructure files under C:\Projects\Agent_Workspace\PIPD (product target root).
- Write run receipts, checkpoints and evidence under C:\Projects\Agent_Workspace\PIPD\.hgk\.
- Create and update candidate git repository and, after local qualification + independent gate, push to the candidate GitHub repo.
- Write the mandated single-file external acceptance evidence MD under 知識庫/實作相關DOC/PIPD/實作證據/.
Forbidden mutations:
- Any write to HG-KSEOS src/config or Fabric control/contracts/assurance.
- Any SQL write to the SharedSpine DB outside the typed API.
- Any publication of secrets, private corpora or raw sensitive local evidence.
- Any production deployment or Stage-3/Fabric SQP1 escalation.
Claim ceiling: LOCAL

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
- CAP_EIGHT_LOGICAL_SKILLS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_NINETEEN_CONTRACT_FAMILIES: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_DETERMINISTIC_VALIDATORS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_THREE_GOLDEN_PILOTS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_WEB_PACK_5_HOST_PROJECTIONS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_CLI_SDK_13_COMMANDS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_HGK_SHADOW_CANARY_RECEIVER: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_GENIE_OBJECT_PROJECTION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_JIT_TEAM_ACTIVATION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_BOUNDED_REPAIR_ROLLBACK: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
Non-active:
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
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- HG-KSEOS src/config/Fabric control code
- RP-002 Stage-1/2/3 sealed scope
- Fabric SQP1/Stage-3
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_SOURCE_AUTHORITY_FREEZE: verdict=NOT_READY; work=materialize SourceManifest+KnowledgeIndexReadback
- CAP_INTENT_REQUIREMENT_ATOM: verdict=NOT_READY; work=materialize RequirementAtom schema + validator
- CAP_PI_COMPILER: verdict=NOT_READY; work=build PI compiler vertical slice (intent->PI)
- CAP_PD_BINDER_REPOCONTEXT: verdict=NOT_READY; work=build PD binder / RepoContext late-binding
- CAP_TASKSPEC_CONSTRUCTION_CONTRACT: verdict=NOT_READY; work=build TaskSpecSeed + ConstructionContract emitter
- CAP_ECP_TQAEP: verdict=NOT_READY; work=build ECP/TQAEP emitter with donor adapters
- CAP_TRACE_EVIDENCE_CLAIM: verdict=NOT_READY; work=build trace/evidence/claim registry + readback
- CAP_NINETEEN_CONTRACT_FAMILIES: verdict=NOT_READY; work=materialize 19 typed machine contracts + schema validators
- CAP_DETERMINISTIC_VALIDATORS: verdict=NOT_READY; work=materialize deterministic validator suite + NEG cases
- CAP_CLI_SDK_13_COMMANDS: verdict=NOT_READY; work=implement 13 CLI/SDK commands with dry-run/explain
- CAP_BOUNDED_REPAIR_ROLLBACK: verdict=NOT_READY; work=implement bounded repair + rollback drill harness
Required user journeys:
- J1_NL_SPEC_PACKAGE: 用自然語言描述需求即可取得可追溯規格包 → 從自由文字編譯出 PI 規格包
- J2_REPO_IMPORT_PD_LATEBINDING: 匯入既有 Repo 並做 PD late-binding → 掃描既有 Repo 產生 RepoContext
- J3_HGK_HANDOFF: 把規格包交接給 HGK typed receiver → 輸出 ECP/TQAEP 與 handoff 物件
- J4_TEST_REPAIR: 測試失敗後受控修補與重測 → detect->bound->repair->focused retest
- J5_CROSS_HOST_EXPORT: 跨 Host 匯出 5-file Web Pack / Host projections → 產生 5/5 Web Pack
- J6_GITHUB_PUBLIC_DELIVERY: 公開發布候選 Repo 與證據 → 建立/更新 public repo 並讀回 visibility
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
- ACC-CAP_EIGHT_LOGICAL_SKILLS subject=CAP_EIGHT_LOGICAL_SKILLS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_NINETEEN_CONTRACT_FAMILIES subject=CAP_NINETEEN_CONTRACT_FAMILIES depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_DETERMINISTIC_VALIDATORS subject=CAP_DETERMINISTIC_VALIDATORS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_THREE_GOLDEN_PILOTS subject=CAP_THREE_GOLDEN_PILOTS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_WEB_PACK_5_HOST_PROJECTIONS subject=CAP_WEB_PACK_5_HOST_PROJECTIONS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_CLI_SDK_13_COMMANDS subject=CAP_CLI_SDK_13_COMMANDS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_HGK_SHADOW_CANARY_RECEIVER subject=CAP_HGK_SHADOW_CANARY_RECEIVER depth=L2_UNIT_BEHAVIOR
- ACC-CAP_GENIE_OBJECT_PROJECTION subject=CAP_GENIE_OBJECT_PROJECTION depth=L2_UNIT_BEHAVIOR
- ACC-CAP_JIT_TEAM_ACTIVATION subject=CAP_JIT_TEAM_ACTIVATION depth=L2_UNIT_BEHAVIOR
- ACC-CAP_BOUNDED_REPAIR_ROLLBACK subject=CAP_BOUNDED_REPAIR_ROLLBACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE subject=CAP_PUBLIC_ARTIFACT_ACCEPTANCE_EVIDENCE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-01-SOURCE-FREEZE subject=REQ-PIPD-01-SOURCE-FREEZE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-02-INTENT-ATOM subject=REQ-PIPD-02-INTENT-ATOM depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-03-PROFILE subject=REQ-PIPD-03-PROFILE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-05-PI-COMPILER subject=REQ-PIPD-05-PI-COMPILER depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-06-PD-BINDER subject=REQ-PIPD-06-PD-BINDER depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-07-CONSTRUCTION-CONTRACT subject=REQ-PIPD-07-CONSTRUCTION-CONTRACT depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-08-ECP-TQAEP subject=REQ-PIPD-08-ECP-TQAEP depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-09-TRACE-EVIDENCE-CLAIM subject=REQ-PIPD-09-TRACE-EVIDENCE-CLAIM depth=L2_UNIT_BEHAVIOR
- ACC-J1_NL_SPEC_PACKAGE subject=J1_NL_SPEC_PACKAGE depth=L3_INTEGRATION_RUNTIME
- ACC-J2_REPO_IMPORT_PD_LATEBINDING subject=J2_REPO_IMPORT_PD_LATEBINDING depth=L3_INTEGRATION_RUNTIME
- ACC-J3_HGK_HANDOFF subject=J3_HGK_HANDOFF depth=L3_INTEGRATION_RUNTIME
- ACC-J4_TEST_REPAIR subject=J4_TEST_REPAIR depth=L3_INTEGRATION_RUNTIME
- ACC-J5_CROSS_HOST_EXPORT subject=J5_CROSS_HOST_EXPORT depth=L3_INTEGRATION_RUNTIME
- ACC-J6_GITHUB_PUBLIC_DELIVERY subject=J6_GITHUB_PUBLIC_DELIVERY depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_PIPD_PRODUCT_TREE subject=DEL_PIPD_PRODUCT_TREE depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_EXTERNAL_ACCEPTANCE_EVIDENCE_MD subject=DEL_EXTERNAL_ACCEPTANCE_EVIDENCE_MD depth=L2_UNIT_BEHAVIOR
- ACC-DEL_PUBLIC_GITHUB_REPO_PIPD-LS-SP subject=DEL_PUBLIC_GITHUB_REPO_PIPD-LS-SP depth=L1_SCHEMA_CONTRACT
- ACC-DEL_SOURCE_MANIFEST_AND_KNOWLEDGE_READBACK subject=DEL_SOURCE_MANIFEST_AND_KNOWLEDGE_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-DEL_COMPILER_CONTRACT_PROMPT_RECEIPTS subject=DEL_COMPILER_CONTRACT_PROMPT_RECEIPTS depth=L2_UNIT_BEHAVIOR
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: GITHUB_AUTH, SCOPE_EXPANSION, SEALED_GOVERNANCE_CHANGE, PROVIDER_ACTIVATION, PUBLICATION_VISIBILITY.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: PASS, PARTIAL, FAIL, TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above LOCAL.
