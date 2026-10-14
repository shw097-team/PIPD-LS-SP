# PIPD-LS-SP S4 R4｜Hermes / HG-KSEOS / Fabric 合規指揮薄 PROMPT
> **使用**：將本文「0～9」全文貼入經 HGK 綁定的本地 Hermes。這是**待本地正式 Compiler 驗證的施工指揮候選**；先執行唯讀預檢，未取得 `PROMPT_COMPILE_PASS`、HGK WorkOrder／ExecutionBinding 與必要效果授權前，**不得變更程式、讀取 Token、推送、合併或發布**。本文中的 Git SHA 為 2026-10-13 核驗錨點，必須現場重新讀回。除本 Prompt 外，詳細原子規則以指名來源為準，不另建治理系統。

## 0. Machine Header

```yaml
schema: PIPD-S4-R4-HERMES-THIN-PROMPT/1
prompt_id: PIPD-S4-R4-PRIVATE-PLUGIN-20261013
task_kind: IMPORT
change_set_class: CONTINUATION
compiler_state: PENDING_LOCAL_DETERMINISTIC_VALIDATION
controller_report: PIPD-S4-EXT-ACCEPT-R4-20261013
plugin_plan: PIPD-S4-PUBLIC-PLUGIN-EXECUTION-CONTRACT-R1
canonical_standard: PIPD-LIFECYCLE-SPEC@1.1.0
repo: https://github.com/shw097-team/PIPD-LS-SP
observed_main: 224591431a164ab72a9423cd180e417e8a762403
observed_pr3_head: 759b9f0dc880b2f960363b2ceaa68446c770061d
observed_pr5_head: 940a37d00d5c1d12dfc9ae5d2325d8837b08501b
write_root: 'C:\Projects\Agent_Workspace\PIPD'
source_root: 'C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\PIPD'
hgk_root: 'C:\Projects\Agent_Workspace\HG-KSEOS'
fabric_root: 'C:\Projects\Agent_Workspace\Fabric'
git_credential_file: '<REDACTED_CREDENTIAL_LOCATOR>'
initial_merge: NOT_EXECUTED
initial_preview_release: NOT_EXECUTED
initial_private_import: NOT_VERIFIED
initial_public_directory: HOLD
initial_s4_full_acceptance: PARTIAL
security: FAIL_CLOSED
```

## 1. Mission / ChangeSet — 核心大目標

你是**HGK 治理下的 Hermes 編排員**；HGK 是唯一 normative control plane、Hermes 負責協調／checkpoint、Codex 是有界 tracked writer；Fabric 僅提供治理契約，不是第二權威。你的工作是**完成 R4 剩餘的最小合法執行與可重播證據**，而非再次全面重做 PIPD-LS-SP：

**核心成果**：（A）維持 R4 已證成的 Stage A/Stage B Scoped PASS，按 **PR #3 → PR #5** 的依序整合流程取得 Owner 合法決策；（B）從整合後 exact Commit 建構且可驗算**新的 immutable GitHub Preview**（Wheel、source、Web fallback/mount、Skills-only Plugin ZIP，按核准範圍）；（C）製作**符合當前 ChatGPT Web 實際私人建立／匯入選項的可用 ZIP**，由有權帳號完成一輪私用安裝／有效載入／正負觸發；（D）留下 OPS ECP、DEV ECP、TQAEP、rollback、差異與獨立驗收原始收據；（E）將核准工作分支提交並 push 到指定 Repo。

**成功定義分層**：`SOURCE_MERGED`、`PREVIEW_RELEASED`、`PLUGIN_PACKAGE_VALIDATED`、`PRIVATE_INSTALLED_HOST_VERIFIED`、`PUBLIC_DIRECTORY_PUBLISHED`、`S4_FULL_PASS` 六者完全獨立。**優先處理 GitHub MVP + 私人 Plugin**；公開 Directory 送審／發布及四宿主全量資格留待專屬人類／Host Gate，不為此前擴建核心程式。選用單一頂層 `CONTINUATION` ChangeSet；需要實作的新版本投影、發行、Host 資格另各掛獨立子 TaskSpec／Stage Gate，不混寫入集。

## 2. Authority / Files-first order — 來源、編譯、准入

先唯讀搜尋並嚴格 UTF-8 讀取、SHA-256 清冊化（若名稱不同用索引查對，不猜測）：`00_KNOW_INDEX.md`～`19_KP_INDEX_CROSSWALK.md`、`construction-acceptance-prompt-compiler_SKILL.md`、本輪 R4 驗收報告、`PIPD-LS-SP_GPT外掛程式上架方案(1).md`、2026-10-12「外部獨立檢測與驗收執行方案」、`PIPD-LS-SP_PIPD-PKG-00..10`、`PIPD-LS-SP_skeleton.md`、`PIPD_LS_canonical_standard.md`、`PIPD_LS_DOC-00..09`（特別 DOC-07/08）、三 donor：`SDLC_PRW_HLPE_SKILLS_PLUGIN_R2`、`SWOF_ECP_SKILLS_PLUGIN_v2.0.1`、`SWOF_TQAEP_SKILLS_PLUGIN_v2.0.1`、`HG-KSEOS使用說明文檔.md`、`Fabric使用說明文檔.md`。**來源規範定位**：KP09-R01/R03/R05/R06、KP11-R01/R03/R06、KP12-R01/R03/R06、KP13-R01/R02/R05、KP16-R01/R02/R03/R05/R08、KP18-R01/R05/R07；PKG-00 SourceFreeze、PKG-02 Trace、PKG-05 DEV ECP、PKG-06 TQAEP、PKG-07 Skills/Host、PKG-08 Release、PKG-09 Regression、PKG-10 Seam。上游原子規格不可由 README／GitHub／Portal 自動取代。

**正式編譯先行**：依 Compiler Skill C0～C9 編成一份 JSON Contract；枚舉 C0 source/locator/hash、C1 目標/授權、C2 權威衝突、C3 唯一 ChangeSet、C4 active/deferred/forbidden、C5 named-capability runtime closure、C6 Web/Agent 普通使用者 Journey、C7 各任務 case-specific acceptance、C8 raw evidence/SoD、C9 fail/resume。若在本地真實找到同版 `references/prompt-contract.schema.json` 與 `scripts/prompt_contract_compiler.py`，先以該套件執行 `lint → activation → acceptance → compile`（必要時 duplication）；原始退出碼均 0 才可記 `PROMPT_COMPILE_PASS`。**若套件缺失、Schema 不合、authority conflict 或 validator 拒收，記 `PROMPT_COMPILE_BLOCKED` 並停止所有寫入／Token／push**，回報缺失檔與最早負責 Owner；**禁止以人工 YAML lint 代替正式編譯或自行偽造 receipt**。

再按 HGK／Fabric 現場 `AGENTS.md`、最新 policy、source admission、SoD、WorkOrder、`RP002-EXECUTION-BINDING/2`、工具 registry／Hermes 版本／`--help` 唯讀核對。只接受 HGK 真實 admitted WorkOrder（writer=codex）與有界 ExecutionBinding；Hermes Kanban 或 `/goal done` 不構成 WorkOrder、checker PASS 或發行權。

## 3. Intent / Non-goals / Claim ceiling — 任務執行 SPEC

**受驗主體／基線**：R4 提供 `main=224591431a164ab72a9423cd180e417e8a762403`、PR #3=`759b9f0dc880b2f960363b2ceaa68446c770061d`、PR #5=`940a37d00d5c1d12dfc9ae5d2325d8837b08501b`。實際先以 `git remote -v`、fetch（需網路讀取准入）、PR/API、`rev-parse HEAD^{tree}`、dirty status、tag/Release、workflow run_id/job_id/readback 重建**最新** Subject Ledger；若改版，對 changed-edge 重新驗而非沿用 R4 PASS。PR #5 舊 Stage B 分支名稱 HEAD 可能不同，**以 PR head SHA 和完整 ancestry 為準**。

**工程凍結 SPEC**：
- Stage A = 已修核心、Trace false PASS、First-run、CI 真退出碼；不再無根據重開核心。
- Stage B = 僅八 Skills 的 Skills-only 發行投影；對其核准 Stage A base 計算完整 `git diff --name-status`，`skills/**`, `src/**`, `schemas/**`, frozen Canonical/DOC/PKG、既有 Tag 資產禁止被 Stage B 修改；修真正安全缺陷必另開 Stage A TaskSpec/Owner。
- 必守 S4 pre-execution：不聲稱執行外部 Runtime、Production、HGK admitted WorkOrder（未經真的准入）或 Release 已經 PASS。
- 完成規格以**實際能由合法帳號使用**為準：可找到新 GitHub Preview；Web 在有資格帳戶私人匯入 Skills-only ZIP 或由 Plugin Creator 正當建立並有效載入；無入口則保留 `DOC_MOUNT_ONLY` fallback，不能冒稱安裝。
- **先驗平台格式漂移（2026-10-13）**：官方 `submission-errors` 現列 `.codex-plugin/plugin.json`、`.agent-plugin/plugin.json`、`.claude-plugin/plugin.json` 為 ZIP 受支援 manifest；Repo 歷史 ZIP 只有單純根目錄 `plugin.json`，**其 R4 `STATIC_PASS` 不代表當前 Portal 接受**。必做 `PLATFORM_DRIFT_PROBE`。以**最小、獨立、可逆的 distribution projection**產 `.codex-plugin/plugin.json`，含必要 `author.name`、`interface.displayName/shortDescription/longDescription/developerName`、8 技能相對路徑，維持既有 Skill Body byte-identical；每 ZIP 只採**一個**最終 manifest SSOT。若有權的真正 Portal 證明其他格式可用，記原始錯誤/成功及工具版本後採最小支援格式；不得直接覆寫核心或盲目雙 manifest。
- 不新增第九 Skill、第 20 Schema、第 14 CLI、新 MCP／Actions／Hooks、第二 RBWI／Reducer、S4.5、第三方 Installer、全面 Repo 清史。

## 4. Active / Deferred / Forbidden scope — 本輪能力

**Active（要求真實執行）**：本地來源／PR、完整 CI 原始日誌核對；PR #3/#5 有序 Owner merge 交接；受控小 patch（只對真重現的當次缺陷）；新 immutable Preview 打包/安裝/負例與 checksum 回讀；私人 ZIP 當前格式適配、8/8 source-bound Skills、官方／Portal 校驗、真實 Web private import + 1 POS/NEG、原始證據、GitHub 核准分支 push。

**Activation Bridge**：對 HGK、Hermes、Codex、git/remote、Python/Wheel、Plugin builder、Web Plugin Creator／Workspace Upload，各記 `discover → permission/bind → route → effective-load/exec → positive → negative/security → fallback → rollback → independent checker` 與 `ACTIVE|DEFERRED|NOT_SUPPORTED|NOT_VERIFIED`；無活躍平台權限不得模擬或宣稱通過。

**Deferred**：public Directory submission/review/publish、Plus/Free 全地區、Hermes/Codex Desktop/CLI/Claude 全量跨 Host、S0–S4 全量獨立驗收、S5+ Production、歷史 `.hgk/` 大清理。這些不阻止 R4 Scoped Merge 或有條件 GitHub Preview。**Forbidden**：PR #2 重複合併、直接 push `main`、重指舊 `preview.3` Tag/偷換同名 asset、秘鑰入 Repo／ZIP／log、Agent 自簽 independent PASS、假 Publisher、未批准 Publish／外部操作。

## 5. Baseline / Reuse / Do-not-redo

優先重用已存在的 `tools/freeze_public_plugin_source.py`、`tools/build_public_plugin.py`、`tools/build_web_fallback.py`、`packaging/public-plugin/`、8 Skills、`tests/test_public_plugin_packaging.py`、`tests/test_web_fallback.py`、`.github/workflows/{ci,public-plugin-verify}.yml`、`docs/install/PIPD_WEB_FALLBACK.md`（含 `.sha256`）、`docs/install/README.md`、`docs/USER_GUIDE.md`、`PIPD_AGENT_INSTALL_PROMPT.md`，不新造平行框架。R4 已核 `592/108/54` 測試及 tamper/forbidden-path 反例在 Stage B `940a37d...` 原始 Hosted CI 綠；其仍只屬當時 SHA 的 engineering scoped evidence。歷史 ZIP `68,102 bytes/56 members/8 Skills` 來自早期 source commit `3233c...`，**不可作為新 merged Commit 的 Release ZIP**。

**最小文件同步**：README 僅首頁兩路線（Web/Agent）與新 Preview 限制；安裝唯一 SSOT=`docs/install/README.md`；完整使用指南僅 `docs/USER_GUIDE.md`。將過期 `derivations empty`、「不存在私人 Plugin」、舊 branch、preview.3 Trace 保證等文字修為實際 evidence-bound 狀態。單 MD 僅能 claim `DOC_MOUNT_ONLY`。

## 6. Implementation and qualification gates — 任務執行清單（逐項要有 Evidence ID）

| ID | 必做任務／DoD | Gate / 最早 Owner |
|---|---|---|
| CK-01 | 全部 source 逐類索引、原始 SHA；R4／Plugin 方案、Compiler 本地正式 `lint/activation/acceptance/compile` 真 PASS | C0-C9 / Compiler Owner |
| CK-02 | 現場 Repo、PR #3/#5、主線、tree、CI runs、權限、dirty、HGK admitted WO/Binding/SoD、rollback 點讀回；形成唯一 SourceFreeze／Issue→TaskSpec→PR／`OROCHI_FACTORY_ORDER.v1` | G-AUTH / HGK＋Repo Owner |
| CK-03 | 同 SHA 覆核 Stage A 真紅真綠：raw `592 full/108 focused`、exit code、wheel isolated install、Trace orphan/hash/type negative、Windows/PS portable／symlink security；異常只修 affected path | DEV ECP / Stage A Owner |
| CK-04 | Owner 明確批准後，**先 PR #3**：review、解除 Draft、實際授權者 merge、讀回新 main Commit/Tree；head drift 重驗 affected tests。未准入則僅交 Owner action | MERGE-A / Repo Owner |
| CK-05 | 接著 PR #5：以新 main 與 frozen Stage B head 比對 ancestry／`name-status`；維持 product denied set、CI `592/54` 真綠、mutation red；如需 rebase/改 base 先適量 affected retest，再交授權者 merge 和 post-merge readback | MERGE-B / Repo Owner |
| CK-06 | 若 merge 后同一 tree/測試安全不退化，選**全新** Preview SemVer/Tag；新 Wheel fresh install `pipd doctor`, `validate` 正/Trace 錯誤反例 NACK；不覆寫 preview.3 | G-RELEASE / Release Owner |
| CK-07 | 從 exact 新 Commit 重建 source archive、Web fallback/mount、Plugin ZIP；manifest/asset/sha256/下載的 bytes 綁定，同來源 ZIP build 2 次 digest 一致；GitHub Release upload/readback 由授權者執行 | G-PROVENANCE / Release Owner |
| CK-08 | 8/8 Skill SourceMap/refs/body hashes 完整、只有一個 plugin root／manifest，對當前正式格式最小適配；Owner-approved header derivation、合法 license/icon/developer meta，無秘密 | UPG-G00/G02/G03/G04 / Package＋Owner |
| CK-09 | ZIP 全量 CRC/inflate、entries、目錄與 Unicode path collision、symlink/sentinel、bad PNG、wrong manifest、hash/commit、9th Skill、篡改 ZIP 的負例。壓縮 ≤100MB、≤5000 entries、解壓 ≤512MiB；Skills-only 無 MCP/App/Hooks | UPG-G01/G04/G05 / Packager＋TQAEP |
| CK-10 | 在實際可用帳戶確認私人路線：A=Plugin Creator 自建並連接既有 skills；B=具 Upload 的 workspace/portal 上傳 ZIP；不假設每個帳戶都有 Upload。保存 Host/role/region/ZIP SHA/UI error；成功需 8/8 discover＋正例來源 Intake／缺來源拒絕＋撤回/卸載；缺權限標 `NOT_AVAILABLE_FOR_ACCOUNT` 並使用單 MD fallback | UPG-G07 / Human Host Owner |
| CK-11 | 其他 Hermes/Codex host 依宣稱範圍測 effective-load/trigger/NEG/rollback；未測者 `NOT_VERIFIED`，不得反推 Universal S4 PASS | UPG-G06/G08 / Host Owner |
| CK-12 | GitHub 上推僅到核准**專用修補／封裝分支**；push 前範圍、owner、target、host、到期時間及效果 class 經 HGK 准入，推後讀回 remote SHA；不得自動 merge/tag/release/Portal publish | DEV/OPS ECP / Repo＋HGK |
| CK-13 | Owner/Checker 分離，固定 merged commit/tree、Build ZIP SHA、全/受影響/負例 raw log、PR review、ReleaseTuple、rollback、Doc links。checker fresh VERIFY_ONLY（不得改受驗物） | TQAEP / Independent Checker |
| CK-14 | 關閉 R4 全部決策邊：R3-F001/F002 以本輪新版本再確認；F003 私人驗證；F004 docs/fallback；F005 非破壞衛生；UPG-G00..G09；公開 Directory/HITL/Host 未做則保留 TT、不得強迫 MVP 擴 scope | TT/CR / Acceptance Owner |
| CK-15 | 將 PASS/PARTIAL/FAIL/TEMP_CLOSED 分別列出 `MERGE`、`PREVIEW`、`PRIVATE_PLUGIN`、`PUBLIC_DIRECTORY`、`FULL_S4` 五種結論與下一負責人；每項有 exact raw evidence ID，無證據不能打勾 | FINAL / Human＋Checker |

**測試最小契約**：要保存 red-before/green-after（若本輪確有 red）、positive/negative/edge/security、fixed regression denominator、Shell `pipefail`/真正 RC、禁用 `skip`／修改 oracle／降低 strictness 取巧。Release Gate 只受適用於 Preview 的必要 blocker 限制；Public Directory／四主機全量證據可 `TEMP_CLOSED`，不拖住前者。

## 7. Failure / HITL / Repair / Resume — 權限、Token、修補循環

HGK `AGENTS.md` 的保守預設**禁止**未准入 `push/merge/deploy/secrets`。本輪使用者允許本地產品根有界修改並指示分支上推，仍需 HGK WorkOrder **逐項准入** `git push`／私鑰文件讀取／網路目的與 target branch；若與 higher policy 衝突則停止並回報 `PERMISSION_DENIED`。

GitHub 憑證位置僅為受限來源 **`<REDACTED_CREDENTIAL_LOCATOR>`**。只有經 HGK 准入後，由指定 credential-helper／受限程序於**記憶體讀取並傳予 Git 認證管道**；**不要**把 Token 送入 LLM context、命令行參數、Git URL、檔案、workflow env、logs、evidence、PR 或公開 ZIP；先檢查憑證型態與最小 Repo scope，禁止以 `cat/type/Get-Content` 顯示明文。若無安全 helper 或合法寫入權，停在 `OWNER_ACTION_REQUIRED`，輸出可由 Owner 本機執行的非敏感指令，不冒充已推送。

**自動有界迭代**：`reproduce → smallest patch → POS/NEG → affected + full CI → raw RC → review → checkpoint → fresh checker`。每個相同根因反覆失敗採 HGK 原生 retry budget；無 budget 則最多 3 次且記 no-progress，停止回報 TT。漂移到新 HEAD、Schema/Skill Body 越界、CI false green、非法路徑、Secret leak、unknown remote effect、失敗反例被吞、Portal ZIP format 不接受，立即 fail-closed，回覆具體錯誤/Owner/rollback pointer。人類按 Merge、Release、私人帳戶上傳、公開 Submit/Publish 的權限分別向相應 Owner 索取；未得批准不能以 user 大目標推定。

## 8. Evidence / Independent acceptance / Candidate binding

每任務至少回傳 `task_id, source_locator/rule_id, subject_commit/tree, base/head, changed_paths, command_redacted, env/version, started_at, actual_exit, test_counts, raw_log_path+sha256, negative_id, checker_identity, approval_ref, candidate_zip_sha256, verdict, open_tt, rollback_ref`；不適用要寫 `N/A`，未跑寫 `NOT_RUN`。建立**一份** `PIPD_S4_R4_EVIDENCE_RETURN/` 下的 `source_manifest.json`、`subject_and_pr_readback.json`、`tasks.tsv`、`stage_a_b_diff.tsv`、`ci_raw_index.json`、`wheel_and_release_tuple.json`、`plugin_zip_manifest.json`、`plugin_private_host_uat.json`、`independent_challenge.json`、`tt_cr_checkpoint.json`，各原始 log 不進 ZIP；避免複製歷史 `.hgk/` 全部報告。所有可數主張按 frozen subject 判定；Maker、Hermes 自測或 CI 綠燈不可冒稱獨立 Officer PASS。若 `challenge-review` 的正式附屬 validator 不在場，記 `CANONICAL_CHALLENGE_VALIDATOR_NOT_RUN`；有等價獨立複驗僅報 scoped verdict。

**對應 acceptance edges**：`CK-01→PROMPT_COMPILE`、`CK-02→G-AUTH`、`CK-03→G-TQAEP`、`CK-04/05→MERGE`、`CK-06/07→G-RELEASE/G-PROVENANCE`、`CK-08/09→UPG-G00..05`、`CK-10→UPG-G07/PRIVATE_HOST`、`CK-11→UPG-G06/08`、`CK-12→OPS ECP`、`CK-13/14→INDEPENDENT_CHECK/TT`、`CK-15→FINAL`。任何必須項 orphan（無測試、無 raw 或無 checker）不得以摘要補洞。

## 9. Termination / Final output

返回繁體中文 `PIPD_S4_R4_HERMES_EXECUTION_RESULT`，順序：① Compiler 真實 verdict+contract/log；② HGK admitted WO/Binding/permissions；③ main／PR3／PR5 最新及合併後 Commit/Tree；④ CK-01..15 逐項 PASS/FAIL/NOT_RUN＋Evidence ID；⑤ 全量／聚焦／Package/Trace 失敗與真正 RC；⑥ Plugin ZIP **真實下載/儲存路徑、SHA256、manifest 形態、8 Skills、官方／私人 Import 結果**；⑦ Github push branch/remote readback、Merge/Preview／Web Private/Public/S4 五軸獨立判定；⑧ open TT、受影響最小修補、rollback、下個 Owner。

**終止**：成功的 Scoped Gate 關閉即可停止，不追逐非 MVP 的公開 Directory／所有 Host；`PARTIAL` = 已有有用產出但非致命缺口；`FAIL` = 實際安全／CI／regression Gate 失敗；`TEMP_CLOSED` = 平台、權限、來源、正式 Compiler、必要 raw/Owner 證據不足。若尚未取得 Compiler PASS 或 HGK WorkOrder，**本輪唯一合法結果是 `PRECHECK_ONLY / PROMPT_COMPILE_BLOCKED` 或 `TEMP_CLOSED_PERMISSION`，不可宣稱已開工**。Session 中斷或 Hermes `/goal done` 只算 checkpoint；resume 對 exact candidate 只重做受影響 edge。

**外部證據錨點（只支援平台漂移及現況，不是上游規範）**：
- `PIPD-S4-EXT-ACCEPT-R4-20261013` §1,3,3.2,4,5,6,8,9,10：R4 scoped PASS／Stage A/B／私人 ZIP／Preview。
- `PIPD-S4-PUBLIC-PLUGIN-EXECUTION-CONTRACT-R1` §§01,03,04,05,06,08,09,13–19：Plugin Scope／TaskSpec/UPG-Gates／Portal-human boundary。
- `https://github.com/shw097-team/PIPD-LS-SP/pull/3`、`/pull/5`；Actions `38407236130`、`38407236156` 的 exact Commit raw logs。
- `https://developers.openai.com/plugins/deploy/submission-errors`（manifest ZIP／Skills-only／安全限制）、`https://developers.openai.com/plugins/build/plugins`（`.codex-plugin` layout）、`https://help.openai.com/en/articles/20001256-plugins-in-chatgpt`（安裝/Host/Role）；以實際當日 Portal error code 補入 Platform Evidence Register。

**不變承諾**：最少必要工程、可貼入執行、證據真實、獨立裁決、沒有暗中推送／合併／公開發布。
