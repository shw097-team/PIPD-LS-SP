# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-R4-R5-CLOSEOUT-CONTINUATION
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: 完成 R4 驗收報告 PIPD-S4-EXT-ACCEPT-R4-20261013 提出的剩餘最小合法執行：平台漂移探測、manifest 最小適配、自凍結 Stage B head 建 2x-deterministic ZIP 候選＋正負例、私人匯入 readiness 套件、release tuple 稿與 10 件式證據包；merge／tag／publish／私人 UI 上傳維持 owner gate。
Expected outcome: 本輪產出 evidence-bound 候選與證據包；PR#3→PR#5 合併、preview tag、私人匯入與公開上架由有權 owner 依 R4 報告執行；任何宣稱不超過其證據。
ChangeSet: CONTINUATION
Affected domains: packaging/public-plugin, docs/install, README.md, .hgk/rounds/R5-20261014-s4-r4-closeout

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP｜S4 R4 驗收報告_20261013-3.md PIPD-LS-SP｜S4 R4 驗收報告_20261013-3.md role=NORMATIVE
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP S4 R4｜Hermes  HG-KSEOS  Fabric 合規指揮薄 PROMPT_2026-10-13-3.md PIPD-LS-SP S4 R4｜Hermes  HG-KSEOS  Fabric 合規指揮薄 PROMPT_2026-10-13-3.md role=NORMATIVE
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_GPT外掛程式上架方案-3.md PIPD-LS-SP_GPT外掛程式上架方案-3.md role=NORMATIVE
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP S4｜三合一小型升級藍圖-6.md PIPD-LS-SP S4｜三合一小型升級藍圖-6.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\PIPD\PIPD-LS-SP_PIPD-PKG\PIPD-LS-SP_PIPD-PKG-00~PKG-10\PIPD-LS-SP_PIPD-PKG-00.md PIPD-LS-SP_PIPD-PKG-00.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\11_EVIDENCE_REQUIREMENT_MATRIX.md 11_EVIDENCE_REQUIREMENT_MATRIX.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\12_EVAL_REGRESSION_LLM_JUDGE.md 12_EVAL_REGRESSION_LLM_JUDGE.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\16_RELEASE_PACKAGING_CHECKSUM_READBACK.md 16_RELEASE_PACKAGING_CHECKSUM_READBACK.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\17_UX_ONBOARDING_NO_BRAIN_FLOW.md 17_UX_ONBOARDING_NO_BRAIN_FLOW.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\工程基座\GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2\KnowledgePack\18_TT_CR_DRIFT_REGISTER.md 18_TT_CR_DRIFT_REGISTER.md role=NORMATIVE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 外部驗收官在 REPO 上可找到：平台漂移證據＋最小 manifest 差異＋兩次等 digest ZIP＋具名反例＋私人匯入 readiness+release tuple 稿＋10 件式證據包；owner gated 項皆有明示 NOT_RUN/NOT_VERIFIED。
Constraints:
- HG-KSEOS 為唯一控制平面；Hermes 為受治理編排面；Fabric 僅提供治理契約。
- 改動面最小：Stage B packaging surface only；不重開核心；不新增第九 Skill；MCP/Actions/Hooks OFF。
- R4 報告主決策：不再修核心邏輯；PR#3→PR#5 順序整合由 Repo Owner 執行。
- merge / tag / release / publish / 私人 UI 上傳一律 owner-gated；agent 只產生 evidence-bound 候選。
- 凍結主體主導：任何 head 改變僅對 affected 差異重驗。
Non-goals:
- 重寫 8 Skill／src／schemas 核心。
- 實作公開 Plugin Directory 上架與四主機全量資格。
- 執行實際 GitHub merge／tag／publish 或私人帳戶 UI 匯入（owner gate）。
- 新增第九 Skill、MCP、Actions、Hooks 或 S4.5。
- 重開已關閉的 R3/R4 findings 或以舊 seal 重新標籤新 commit。
Authorized mutations:
- 本輪 round 目錄（compiler/admission/gates/evidence）
- 受准入分支上的 Stage B packaging 最小投影（plugin manifest 與文件 stub）
- 知識庫實作證據下的 R5X 驗收記錄（另開證據寫入範圍）
Forbidden mutations:
- HG-KSEOS／Fabric 封存控制面（未另取 owner WorkOrder 前不得修改）。
- 已發布歷史 commit／preview.3 資產（不得改寫、不得重指向）。
- 8 個 Skill Body、src／schemas 核心、既有 CI oracle。
- 任何含明文憑證的檔案、commit、manifest、日誌或輸出。
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_R5X_PLATFORM_DRIFT_PROBE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_MANIFEST_MINIMAL_FIT: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_ZIP_BUILD_2X: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_ZIP_NEGATIVES: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_PRIVATE_IMPORT_READINESS: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_RELEASE_TUPLE: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
- CAP_R5X_EVIDENCE_RETURN: ACTIVE_REQUIRED; action=DESIGN; runtime_required=true
Non-active:
- none
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- 8 skills bodies
- src core
- schemas core
- existing release assets
- preview.3 tag assets
- HGK and Fabric frozen subjects
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_R5X_PLATFORM_DRIFT_PROBE: verdict=NOT_READY; work=R4 報告 §5.1/外掛方案 §04.1：PLATFORM_DRIFT_PROBE——fresh-fetch 官方 submission-errors 頁並逐字記錄當日支援的 ZIP manifest 清單（含日期／工具版本）；快取頁面不得決定封裝形態。
- CAP_R5X_MANIFEST_MINIMAL_FIT: verdict=NOT_READY; work=R4 報告 §5.2/外掛方案 §04：manifest 最小適配——portable 根 plugin.json 為唯一 SSOT；新增官方 extensions.com.openai.interface 列示欄位；8 個 Skill Body byte-identical；每 ZIP 僅一個 manifest。
- CAP_R5X_ZIP_BUILD_2X: verdict=NOT_READY; work=R4 報告 §5.2/外掛方案 TS-07：從同一凍結 Stage B head 以 tools/build_public_plugin.py 建 ZIP 兩次，SHA256 相等；56-member 結構、單一根、無第九 Skill。
- CAP_R5X_ZIP_NEGATIVES: verdict=NOT_READY; work=外掛方案 §09 PORTAL-01..03：於 scratch ZIP 副本植入 mcp.json/hooks/.app.json 並驗證 repo 閘門拒絕；每反例記具名拒絕。
- CAP_R5X_PRIVATE_IMPORT_READINESS: verdict=NOT_READY; work=R4 報告 §5.3/外掛方案 TS-10：私人匯入 readiness——plugin_private_host_uat.json 記 route A (Plugin Creator) / route B (workspace upload) 程序與驗收準則；實際 UI 操作為 HumanGate，未執行一律 NOT_VERIFIED。
- CAP_R5X_RELEASE_TUPLE: verdict=NOT_READY; work=R4 報告 §6.2/§10：release tuple 稿——wheel_and_release_tuple.json 含 Owner SemVer 決策欄＋不可變新 tag 規則；preview.3 資產不得重用；實際 tag/publish 為 owner-gated。
- CAP_R5X_EVIDENCE_RETURN: verdict=NOT_READY; work=R4 指揮薄 §8：組裝 PIPD_S4_R4_EVIDENCE_RETURN 10 件式證據包；owner-gated 項顯式 NOT_RUN；所有可數主張綁定凍結主體。
Required user journeys:
- J1_PLATFORM_DRIFT_THEN_BUILD: 在官方當日支援 manifest 形態下從凍結 Stage B head 取得 2x-deterministic ZIP 候選、正負例、私人匯入 readiness、release tuple 稿與 10 件式證據包。 → PLATFORM_DRIFT_PROBE + minimal manifest diff + 2x equal-sha ZIP + named negatives + UAT scaffold + release tuple stub + 10-pack evidence
Acceptance predicates:
- ACC-REQ-R5X-001 subject=REQ-R5X-001 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-002 subject=REQ-R5X-002 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-003 subject=REQ-R5X-003 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-004 subject=REQ-R5X-004 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-005 subject=REQ-R5X-005 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-006 subject=REQ-R5X-006 depth=L2_UNIT_BEHAVIOR
- ACC-REQ-R5X-007 subject=REQ-R5X-007 depth=L2_UNIT_BEHAVIOR
- ACC-PLATFORM_DRIFT_PROBE_JSON subject=PLATFORM_DRIFT_PROBE_JSON depth=L2_UNIT_BEHAVIOR
- ACC-MANIFEST_DIFF_R5X subject=MANIFEST_DIFF_R5X depth=L2_UNIT_BEHAVIOR
- ACC-R5X_PLUGIN_ZIP_X2 subject=R5X_PLUGIN_ZIP_X2 depth=L2_UNIT_BEHAVIOR
- ACC-PORTAL_NEGATIVE_CASES subject=PORTAL_NEGATIVE_CASES depth=L2_UNIT_BEHAVIOR
- ACC-PLUGIN_PRIVATE_HOST_UAT subject=PLUGIN_PRIVATE_HOST_UAT depth=L2_UNIT_BEHAVIOR
- ACC-WHEEL_AND_RELEASE_TUPLE subject=WHEEL_AND_RELEASE_TUPLE depth=L2_UNIT_BEHAVIOR
- ACC-EVIDENCE_RETURN_PACK subject=EVIDENCE_RETURN_PACK depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_PLATFORM_DRIFT_PROBE subject=CAP_R5X_PLATFORM_DRIFT_PROBE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_MANIFEST_MINIMAL_FIT subject=CAP_R5X_MANIFEST_MINIMAL_FIT depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_ZIP_BUILD_2X subject=CAP_R5X_ZIP_BUILD_2X depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_ZIP_NEGATIVES subject=CAP_R5X_ZIP_NEGATIVES depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_PRIVATE_IMPORT_READINESS subject=CAP_R5X_PRIVATE_IMPORT_READINESS depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_RELEASE_TUPLE subject=CAP_R5X_RELEASE_TUPLE depth=L2_UNIT_BEHAVIOR
- ACC-CAP_R5X_EVIDENCE_RETURN subject=CAP_R5X_EVIDENCE_RETURN depth=L2_UNIT_BEHAVIOR
- ACC-J1_PLATFORM_DRIFT_THEN_BUILD subject=J1_PLATFORM_DRIFT_THEN_BUILD depth=L2_UNIT_BEHAVIOR
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: PUBLICATION_APPROVAL, PRIVATE_IMPORT_EXECUTION, RELEASE_TAG_APPROVAL, SCOPE_EXPANSION, CREDENTIAL_GATE.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: R5X_CLOSEOUT_DELIVERED, FAIL, TEMP_CLOSED, NO_WRITES_TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL, BLOCKED_HITL, BLOCKED_EXTERNAL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
