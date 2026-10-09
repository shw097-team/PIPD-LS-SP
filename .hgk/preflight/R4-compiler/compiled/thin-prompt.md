# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-R4-FOCUSED-REPAIR-20261009
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: 在 PIPD 上完成 R4 定向修補：處置 R3-EXT-01..10 與 R-AUD-001..015，在單一 frozen published candidate 上取得可獨立複驗的證據，並分離 local 與 publication 兩份 manifest。
Expected outcome: 每個適用的 R3-EXT/R-AUD 條目都有具體閉環證據或明確 owner/TEMP_CLOSED 狀態；不宣稱 15/15 完成，不偽造 PASS。
ChangeSet: NARROW_REPAIR
Affected domains: tools, src/pipd_ls_sp, tests, .hgk, docs, fixtures

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/PIPD-LS-SP_HERMES_R4_FOCUSED_REPAIR_PROMPT_2026-10-09.md C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/PIPD-LS-SP_HERMES_R4_FOCUSED_REPAIR_PROMPT_2026-10-09.md | R4 §0-#9 W1..W8 and the terminal output contract role=NORMATIVE
- R0 C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/PIPD_LS_SP_R3_Post_Repair_External_Challenge_Acceptance_2026-10-09.md C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/PIPD_LS_SP_R3_Post_Repair_External_Challenge_Acceptance_2026-10-09.md | R3-EXT-01..10, R-AUD-001..015, SPEC 32, DEL 25, CAND 22, Gate calibration role=NORMATIVE
- R1 C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/實作證據/PIPD-LS-SP_S0-S4_AUDIT_REPAIR_EVIDENCE_2026-10-09.md C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/實作證據/PIPD-LS-SP_S0-S4_AUDIT_REPAIR_EVIDENCE_2026-10-09.md | current bytes; the reviewer's claimed sha256 e6bbd32d7047bc71e1f43a312c8b5845a719de5367c6aeb4f874c0a61cd1f4f3 is NOT reproduced by any local revision role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/知識庫 C:/Projects/Agent_Workspace/知識庫 | PIPD-LS-SP_藍圖 §19.1/§19.2/§25/§26; PIPD_LS_DOC-08 §7.3; PKG-00..10; canonical standard role=NORMATIVE
- R1 https://github.com/shw097-team/PIPD-LS-SP@3aebbbce948871c07b875ab92acf263d298ecf38 https://github.com/shw097-team/PIPD-LS-SP@3aebbbce948871c07b875ab92acf263d298ecf38 | observed public main 3aebbbce948871c07b875ab92acf263d298ecf38, tree 1a7dc57f9403202c32d1bc01deb1925ac1f6412e (remote source: no local file digest applies) role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS | AGENTS.md, SharedSpine, WorkOrder/ExecutionBinding, policies, lane registry role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/Fabric C:/Projects/Agent_Workspace/Fabric | Fabric governance contract surface (policy read-only in this round) role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2 C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2 | local HEAD 7c5bc585c7d889cd338da853be4efc4b8f07d3b2, tree b2d5faf52a1b7b37f85c0a83162cbaaa896edb37; R3 candidate 10cb3d31fcbd54fffe64152f4b17085866d0d75e, tree bba26ad0634e46169270e81109f9db22c967602a role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 使用者以自然語言即可觸發 lifecycle 並取得綁來源的 PI/PD 契約；8 Skills、5 Web、3 Host、13 CLI 的失敗一律以 typed error 呈現，不以檔案存在或非空 JSON 冒充可用。
Constraints:
- HG-KSEOS 為唯一控制平面；Hermes 為受治理編排面；Fabric 僅契約面。
- NARROW_REPAIR：保留 R3 已有的 19 schemas／8 skills／5 web／3 host／atomic PI-PD／13 CLI／3 GP，不得全域重寫。
- W2 優先：任何 writer 必須具 OS/container 強制 write scope；做不到則 NO WRITES/TEMP_CLOSED。
- 禁止 danger-full-access 或其他僅憑 PROMPT 聲明限制的無隔離 writer。
- 不得改驗收閾值湊 PASS、不得刪 requirement、不得改測試成永遠真。
- claim 互不繼承：CODE_CHANGED / SCHEMA_VALID / TEST_EXECUTED / FIXTURE_MOCK_QUALIFIED / LIVE_HOST_EFFECTIVE_LOAD / LOCAL_QUALIFIED / INDEPENDENT_PASS / HUMAN_RATIFIED / PUBLICATION_APPROVED / RELEASED / PRODUCTION_VERIFIED。
- PAT 只在必要時使用，明文不得進入 argv／日誌／commit／manifest／聊天。
Non-goals:
- 重寫 R3 的 19 schemas／8 Skills／5 Web／3 Host／atomic PI-PD 主幹。
- 施工 S5～S8、PRE-W3、live HGK/GENIE canary。
- 公開 130 MB 歷史 DB 或 1,074 份不公開原始執行快照。
- 自動批准 license／release／publication 或關閉 owner gate。
- force-push、改寫已發布歷史、以舊 seal 重新標籤新 commit。
Authorized mutations:
- PIPD 產品樹的最小必要修補（src/tools/tests/schemas/skills/docs/dist/fixtures）。
- PIPD .hgk 證據樹（收據、manifest、TT、ledger）。
- 知識庫 實作證據 目錄下的 R4 驗收主檔（另開證據寫入 scope）。
- 合規 GitHub PR／分支推送（owner 已授權 PAT；非 release 權限）。
Forbidden mutations:
- HG-KSEOS／Fabric 封存控制面（未另取 owner WorkOrder）。
- 已發布的歷史 commit（不得改寫、不得 force-push）。
- PRE-W3 跨專案 frozen subject。
- 任何 OS 層不可強制的 writer 執行。
- 任何含明文憑證的檔案、commit、manifest、日誌或輸出。
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_W1_PUBLICATION_PROJECTION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_W2_HOST_ENFORCED_WRITESET: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_W3_TT_SUMMARY_PROJECTION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_W4_TECH_GATE_SCOPE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_W5_PERF_PROVENANCE_ECONOMY: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_W6_KNOWLEDGE_REINGEST: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_W7_SPEC_DEL_CROSSWALK: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_W8_FRESH_CHALLENGE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_S0_CONTRACT_SCHEMAS_19: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_SKILL_CONTRACTS_8: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_WEB_PACK_5: ACTIVE_SELECTED; action=DESIGN; runtime_required=false
- CAP_HOST_PROJECTION_MOCK_3: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_CLI_13: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_GOLDEN_PILOTS_3: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_TECH_DISPOSITIONS_22: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_ROLLBACK_DRILL: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
Non-active:
- CAP_OWNER_LICENSE_GATE: STANDBY; action=NONE
- CAP_PRE_W3_SEPARATE: NOT_APPLICABLE_SOURCE_BACKED; action=NONE
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- R3 已確證的 19 schema 結構（TechnologyAdmission required 14/14、$id :1、closed object）
- R3 已存在的 8 個 SkillContract 六件式與 5 份 Web MD 分母
- R3 已存在的 13 CLI 名稱與 3 Golden Pilot fixture
- 已發布的 GitHub 歷史（3aebbbc 及其祖先）
- HG-KSEOS／Fabric 封存控制面
- PRE-W3 跨專案 frozen subject
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_W1_PUBLICATION_PROJECTION: verdict=NOT_READY; work=W1: 分離 local(1667) 與 publication projection manifest，逐項 disposition，並以 sidecar 綁定 published tuple
- CAP_W2_HOST_ENFORCED_WRITESET: verdict=NOT_READY; work=W2: OS/container 強制 writable-roots、spawn guard、effect admission；負例（outside-root/junction/escape/remote write）必須 REFUSE
- CAP_W8_FRESH_CHALLENGE: verdict=NOT_READY; work=W8: 在單一 frozen published candidate 上由獨立 checker 重跑全部分母並留 raw evidence
Required user journeys:
- J1_NL_TO_PI_PD: 以自然語言複合／否定需求取得綁來源的 PI/PD 契約包 → 含 per-clause atom、source binding、claim ceiling 的 PI/PD
- J2_EXISTING_REPO_TO_PD: 在既有 repo 上取得真實 currentness 綁定的 PD → PD 綁 host-derived HEAD/dirty/tracked/epoch
- J3_PUBLICATION_REVIEW: 外部 reviewer 能在公開 repo 上取得可驗證 artefact 與證據 → 分離的 publication projection manifest 與 sidecar attestation
- J4_TECH_AND_PERF_GATES: 消費者不會被頂層 PASS 誤導，且效能閘有可裁定的閾值來源 → 分欄的 consistency/hard-gate 輸出與 provenance 化的效能指標
Acceptance predicates:
- ACC-CAP_W1_PUBLICATION_PROJECTION subject=CAP_W1_PUBLICATION_PROJECTION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_W2_HOST_ENFORCED_WRITESET subject=CAP_W2_HOST_ENFORCED_WRITESET depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_W3_TT_SUMMARY_PROJECTION subject=CAP_W3_TT_SUMMARY_PROJECTION depth=L2_UNIT_BEHAVIOR
- ACC-CAP_W4_TECH_GATE_SCOPE subject=CAP_W4_TECH_GATE_SCOPE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_W5_PERF_PROVENANCE_ECONOMY subject=CAP_W5_PERF_PROVENANCE_ECONOMY depth=L2_UNIT_BEHAVIOR
- ACC-CAP_W6_KNOWLEDGE_REINGEST subject=CAP_W6_KNOWLEDGE_REINGEST depth=L2_UNIT_BEHAVIOR
- ACC-CAP_W7_SPEC_DEL_CROSSWALK subject=CAP_W7_SPEC_DEL_CROSSWALK depth=L2_UNIT_BEHAVIOR
- ACC-CAP_W8_FRESH_CHALLENGE subject=CAP_W8_FRESH_CHALLENGE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S0_CONTRACT_SCHEMAS_19 subject=CAP_S0_CONTRACT_SCHEMAS_19 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_SKILL_CONTRACTS_8 subject=CAP_SKILL_CONTRACTS_8 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_WEB_PACK_5 subject=CAP_WEB_PACK_5 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_HOST_PROJECTION_MOCK_3 subject=CAP_HOST_PROJECTION_MOCK_3 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_CLI_13 subject=CAP_CLI_13 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_GOLDEN_PILOTS_3 subject=CAP_GOLDEN_PILOTS_3 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_TECH_DISPOSITIONS_22 subject=CAP_TECH_DISPOSITIONS_22 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_ROLLBACK_DRILL subject=CAP_ROLLBACK_DRILL depth=L2_UNIT_BEHAVIOR
- ACC-CAP_OWNER_LICENSE_GATE subject=CAP_OWNER_LICENSE_GATE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_PRE_W3_SEPARATE subject=CAP_PRE_W3_SEPARATE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W1 subject=REQ-PIPD-R4-W1 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W2 subject=REQ-PIPD-R4-W2 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W3 subject=REQ-PIPD-R4-W3 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W4 subject=REQ-PIPD-R4-W4 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W5 subject=REQ-PIPD-R4-W5 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W6 subject=REQ-PIPD-R4-W6 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W7 subject=REQ-PIPD-R4-W7 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R4-W8 subject=REQ-PIPD-R4-W8 depth=L2_UNIT_BEHAVIOR
- ACC-HGK_WORKORDER_READBACK subject=HGK_WORKORDER_READBACK depth=L2_UNIT_BEHAVIOR
- ACC-R4_FINDING_LEDGER subject=R4_FINDING_LEDGER depth=L2_UNIT_BEHAVIOR
- ACC-R4_QUALIFICATION_MATRIX subject=R4_QUALIFICATION_MATRIX depth=L2_UNIT_BEHAVIOR
- ACC-PUBLICATION_PROJECTION_MANIFEST subject=PUBLICATION_PROJECTION_MANIFEST depth=L2_UNIT_BEHAVIOR
- ACC-PUBLICATION_SUBJECT_ATTESTATION subject=PUBLICATION_SUBJECT_ATTESTATION depth=L2_UNIT_BEHAVIOR
- ACC-R4_EXTERNAL_ACCEPTANCE_EVIDENCE.md subject=R4_EXTERNAL_ACCEPTANCE_EVIDENCE.md depth=L2_UNIT_BEHAVIOR
- ACC-PROMPT_COMPILER_RECEIPTS subject=PROMPT_COMPILER_RECEIPTS depth=L2_UNIT_BEHAVIOR
- ACC-J1_NL_TO_PI_PD subject=J1_NL_TO_PI_PD depth=L2_UNIT_BEHAVIOR
- ACC-J2_EXISTING_REPO_TO_PD subject=J2_EXISTING_REPO_TO_PD depth=L2_UNIT_BEHAVIOR
- ACC-J3_PUBLICATION_REVIEW subject=J3_PUBLICATION_REVIEW depth=L2_UNIT_BEHAVIOR
- ACC-J4_TECH_AND_PERF_GATES subject=J4_TECH_AND_PERF_GATES depth=L2_UNIT_BEHAVIOR
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: LICENSE_DECISION, PUBLICATION_APPROVAL, ORACLE_POLARITY, PERF_THRESHOLD_RATIFICATION, SCOPE_EXPANSION, PRE_W3_OWNER.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: R4_FOCUSED_REPAIR_DELIVERED, FAIL, TEMP_CLOSED_PRE_W3, BLOCKED_HITL, BLOCKED_EXTERNAL, NO_WRITES_TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
