# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-R5-S4-USER-OPERABILITY-FOCUSED-REPAIR
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: 在 PIPD 上執行 R5 S4 一般使用者可用性定向修補：處置 R4 外部挑戰報告的 F-R4-S4-01..04 / F-R4-S2-05 / F-R4-PUB-06 / F-R4-HARNESS-07 / F-R4-TRACE-08 / F-R4-GOV-09 / F-R4-RELEASE-10，先修安全的 pipd project --out、與 R5 source 等價的可安裝 wheel、真正落地的 pipd export --out，再於隔離工作區跑 UAT-00..12 正反例與 replay。
Expected outcome: 一般使用者不需知道內部 Skill/WorkOrder/Provider 名稱即可完成 Intent -> RequirementAtom -> Profile -> PI -> PD -> ConstructionContract -> ECP/TQAEP -> validate -> Web/Host projections -> portable export，且 pipd 永不因任意 --out 毀損工作樹、永不以舊 wheel 當現行安裝件；未閉合項以 typed blocker 或 owner gate 誠實回報，不宣稱 10/10 PASS。
ChangeSet: NARROW_REPAIR
Affected domains: src/pipd_ls_sp, tools, tests, dist, schemas, .hgk, pyproject.toml

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_R5_S4_USER_USABILITY_FOCUSED_REPAIR_PROMPT_2026-10-09.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_R5_S4_USER_USABILITY_FOCUSED_REPAIR_PROMPT_2026-10-09.md role=NORMATIVE
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_R4_S4_User_Usability_PostRepair_External_Acceptance_2026-10-09.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_R4_S4_User_Usability_PostRepair_External_Acceptance_2026-10-09.md role=NORMATIVE
- R1 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R4_FOCUSED_REPAIR_EVIDENCE_2026-10-09.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R4_FOCUSED_REPAIR_EVIDENCE_2026-10-09.md role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/知識庫 C:/Projects/Agent_Workspace/知識庫 role=NORMATIVE
- R1 https://github.com/shw097-team/PIPD-LS-SP@cd8a06e4c066a40398a4012b7b3908ac11408a2b https://github.com/shw097-team/PIPD-LS-SP@cd8a06e4c066a40398a4012b7b3908ac11408a2b role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/Fabric C:/Projects/Agent_Workspace/Fabric role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2 C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2 role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 13 個 CLI 子命令的成功/拒絕/副作用皆有 typed 輸出與可重算雜湊；危險目的地一律 typed UNSAFE_DESTINATION 且 exit != 0；fresh venv 安裝後 19 schemas 實際可載；export --dry-run 零寫入。
Constraints:
- HG-KSEOS 為唯一控制平面；Hermes 為受治理編排面；Fabric 僅契約面。
- NARROW_REPAIR：保留 19 schemas／8 skills／5 web／3 host mock／13 CLI／3 GP／clause-bound PI/PD 主幹，不得全域重寫，不推進 S5～S8。
- 任何 writer 必須具 OS/container 強制 write scope；做不到則 NO_WRITES/TEMP_CLOSED。
- 禁止 danger-full-access 或其他僅憑 PROMPT 聲明限制的無隔離 writer。
- 不得改驗收閾值湊 PASS、不得刪 requirement、不得改測試成永遠真；S2 perf FAIL 不得抹去。
- 危險 destination 反例只在 disposable scratch/mock workspace 執行，嚴禁對含重要資料的真目錄執行。
- claim 互不繼承：CODE_CHANGED / SCHEMA_VALID / TEST_EXECUTED / FIXTURE_MOCK_QUALIFIED / LOCAL_QUALIFIED / INDEPENDENT_PASS / HUMAN_RATIFIED / PUBLICATION_APPROVED / RELEASED / PRODUCTION_VERIFIED。
- PAT 只在必要時由 credentialed handler 使用，明文不得進入 argv／日誌／commit／manifest／聊天。
Non-goals:
- 重寫 19 schemas／8 Skills／5 Web／3 Host／13 CLI 的既有可行核心。
- 實作 S5 receiver live、S6 GENIE、S7 JIT、S8 SGM promotion、PRE-W3。
- 修滿 22 個未 active 技術的 source pins 或清洗 153/160 全域 knowledge。
- 自動批准 license／release／publication 或關閉任何 owner gate。
- force-push、改寫已發布歷史、以 R3/R4 舊 seal 重新標籤新 commit。
Authorized mutations:
- PIPD 產品樹的最小必要修補（src/pipd_ls_sp、tools、tests、schemas、dist、pyproject.toml、fixtures）。
- PIPD .hgk 證據樹（preflight 契約/收據、rounds、admission、lane raw logs）。
- 知識庫 實作相關DOC/PIPD/實作證據 下的 R5 驗收主檔（另開證據寫入 scope）。
Forbidden mutations:
- HG-KSEOS／Fabric 封存控制面（未另取 owner WorkOrder 前不得修改）。
- 已發布的歷史 commit（不得改寫、不得 force-push）。
- PRE-W3 跨專案 frozen subject。
- 任何 OS 層不可強制的 writer 執行。
- 任何含明文憑證的檔案、commit、manifest、日誌或輸出。
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_R5_PROJECT_DEST_SAFETY: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5_WHEEL_EQUIVALENCE: ACTIVE_REQUIRED; action=INSTALL; runtime_required=true
- CAP_R5_EXPORT_EFFECT: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5_FRESH_USER_UAT: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_R5_WRITESET_ENFORCEMENT: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CAP_R5_PERF_PROVENANCE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_R5_PUBLICATION_TUPLE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_R5_NATIVE_ORCH_PATH: ACTIVE_SELECTED; action=QUALIFY; runtime_required=false
- CAP_R5_OWNER_LICENSE_GATE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP_R5_SCHEMAS_19: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_SKILLS_8: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_WEB_5: ACTIVE_SELECTED; action=DESIGN; runtime_required=false
- CAP_R5_HOST_3: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_CLI_13_USERPATH: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_GOLDEN_PILOTS_3: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_TECH_DISPOSITIONS_22: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
- CAP_R5_ROLLBACK_DRILL: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=false
Non-active:
- CAP_R5_PRE_W3_SEPARATE: NOT_APPLICABLE_SOURCE_BACKED; action=NONE
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- 19 schema 結構（TechnologyAdmission required 14/14、closed object）
- 8 個 SkillContract 與 5 份 Web MD 分母
- 13 CLI 名稱與 3 Golden Pilot fixture
- clause-bound RequirementAtom / negation / compound 既有行為
- 已發布的 GitHub 歷史與 R3/R4 attestation
- HG-KSEOS／Fabric 封存控制面與 PRE-W3 跨專案 frozen subject
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_R5_PROJECT_DEST_SAFETY: verdict=NOT_READY; work=WO-S4-DEST-001: 統一 OutputDestination Resolver，拒絕早於任何 create/delete/replace；staging + atomic publish；dry-run 零副作用
- CAP_R5_WHEEL_EQUIVALENCE: verdict=NOT_READY; work=WO-S4-DIST-002: 由 frozen candidate 重建 deterministic wheel，含 requirements/repo_context/projection 與 19 schemas 資源；install-safe resource lookup
- CAP_R5_EXPORT_EFFECT: verdict=NOT_READY; work=WO-S4-EXPORT-003: export --out 實體落檔 archive+manifest+checksums；--dry-run 零寫入；secret-scan FAIL 零 artifact
- CAP_R5_FRESH_USER_UAT: verdict=NOT_READY; work=WO-S4-UAT-004: 以新 wheel 與 source import 分別跑 UAT-00..12，紀錄 raw stdout/exit/canary hash/replay
- CAP_R5_WRITESET_ENFORCEMENT: verdict=NOT_READY; work=container lane (pipd-r4-writer) 負例矩陣：admitted 成功、outside-root/unmounted/symlink 拒絕、secret 不存在、egress DROP
Required user journeys:
- J1_FRESH_INSTALL_TO_VALIDATE: 從乾淨 venv 安裝 R5 wheel 後，pipd doctor/validate 能載入 19 schemas 並正確拒絕壞 bundle → pipd 指向 site-packages 安裝；19/19 schema 可定位；empty/wrong-owner/orphan trace 為 typed FAIL
- J2_PROJECT_SAFE_WRITE: 以 pipd project 產生 5 Web + 3 Host + IR，且任何危險 --out 都被拒絕且不觸碰工作樹 → 正常 scratch 目的地 5/5、3/3、IR 寫入且 hash 可重算；危險目的地 typed UNSAFE_DESTINATION exit != 0 且 canary 不變
- J3_PORTABLE_EXPORT: pipd export --out 產出可獨立解包的 portable 交付（archive+manifest+checksums） → 指定路徑出現 archive 與 manifest；外部可解包並重算 sha256；dry-run 無任何檔案
- J4_FULL_S4_CHAIN: 同一 frozen source 完成 intake -> compile-pi -> bind-pd -> compile-ecp/tqaep -> validate 全鏈，並在兩個 fresh process 重播一致 → clause-bound RequirementAtom、profile 行為、PD currentness、TQAEP maker!=checker 皆 typed；兩次 replay 正規化 hash 相同
Acceptance predicates:
- ACC-CAP_R5_PROJECT_DEST_SAFETY subject=CAP_R5_PROJECT_DEST_SAFETY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5_WHEEL_EQUIVALENCE subject=CAP_R5_WHEEL_EQUIVALENCE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5_EXPORT_EFFECT subject=CAP_R5_EXPORT_EFFECT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5_FRESH_USER_UAT subject=CAP_R5_FRESH_USER_UAT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5_WRITESET_ENFORCEMENT subject=CAP_R5_WRITESET_ENFORCEMENT depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_R5_PERF_PROVENANCE subject=CAP_R5_PERF_PROVENANCE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_PUBLICATION_TUPLE subject=CAP_R5_PUBLICATION_TUPLE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_NATIVE_ORCH_PATH subject=CAP_R5_NATIVE_ORCH_PATH depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_OWNER_LICENSE_GATE subject=CAP_R5_OWNER_LICENSE_GATE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_SCHEMAS_19 subject=CAP_R5_SCHEMAS_19 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_SKILLS_8 subject=CAP_R5_SKILLS_8 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_WEB_5 subject=CAP_R5_WEB_5 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_HOST_3 subject=CAP_R5_HOST_3 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_CLI_13_USERPATH subject=CAP_R5_CLI_13_USERPATH depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_GOLDEN_PILOTS_3 subject=CAP_R5_GOLDEN_PILOTS_3 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_TECH_DISPOSITIONS_22 subject=CAP_R5_TECH_DISPOSITIONS_22 depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_ROLLBACK_DRILL subject=CAP_R5_ROLLBACK_DRILL depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5_PRE_W3_SEPARATE subject=CAP_R5_PRE_W3_SEPARATE depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R5-DEST-001 subject=REQ-PIPD-R5-DEST-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5-DIST-002 subject=REQ-PIPD-R5-DIST-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5-EXPORT-003 subject=REQ-PIPD-R5-EXPORT-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5-UAT-004 subject=REQ-PIPD-R5-UAT-004 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-PIPD-R5-PERF-005 subject=REQ-PIPD-R5-PERF-005 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R5-PUBLISH-006 subject=REQ-PIPD-R5-PUBLISH-006 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-PIPD-R5-ORCH-007 subject=REQ-PIPD-R5-ORCH-007 depth=L2_UNIT_BEHAVIOR
- ACC-PROMPT_COMPILER_READBACK subject=PROMPT_COMPILER_READBACK depth=L2_UNIT_BEHAVIOR
- ACC-HGK_ADMISSION_READBACK subject=HGK_ADMISSION_READBACK depth=L2_UNIT_BEHAVIOR
- ACC-R5_S4_FINDING_LEDGER subject=R5_S4_FINDING_LEDGER depth=L2_UNIT_BEHAVIOR
- ACC-R5_S4_UAT_MATRIX subject=R5_S4_UAT_MATRIX depth=L2_UNIT_BEHAVIOR
- ACC-DISTRIBUTION_AND_PUBLICATION_TUPLE subject=DISTRIBUTION_AND_PUBLICATION_TUPLE depth=L2_UNIT_BEHAVIOR
- ACC-R5_S4_EVIDENCE_MASTER_MD subject=R5_S4_EVIDENCE_MASTER_MD depth=L2_UNIT_BEHAVIOR
- ACC-J1_FRESH_INSTALL_TO_VALIDATE subject=J1_FRESH_INSTALL_TO_VALIDATE depth=L3_INTEGRATION_RUNTIME
- ACC-J2_PROJECT_SAFE_WRITE subject=J2_PROJECT_SAFE_WRITE depth=L3_INTEGRATION_RUNTIME
- ACC-J3_PORTABLE_EXPORT subject=J3_PORTABLE_EXPORT depth=L3_INTEGRATION_RUNTIME
- ACC-J4_FULL_S4_CHAIN subject=J4_FULL_S4_CHAIN depth=L3_INTEGRATION_RUNTIME
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: LICENSE_DECISION, PUBLICATION_APPROVAL, PERF_THRESHOLD_RATIFICATION, ORACLE_POLARITY, SCOPE_EXPANSION, PRE_W3_OWNER, CREDENTIAL_GATE.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: R5_S4_USER_OPERABILITY_DELIVERED, FAIL, TEMP_CLOSED_PRE_W3, BLOCKED_HITL, BLOCKED_EXTERNAL, NO_WRITES_TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
