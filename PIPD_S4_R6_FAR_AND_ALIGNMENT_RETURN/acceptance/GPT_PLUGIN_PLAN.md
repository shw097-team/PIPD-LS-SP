# PIPD-LS-SP S4｜三合一小型升級：Public Skills-only Plugin × 公開發行 × 極簡安裝體驗

> **Report ID** `PIPD-S4-ONE-UPGRADE-EXTERNAL-ASSESSMENT-20261012-R1`  
> **任務** `IMPORT/DRIFT_PROBE + DESIGN + EVAL-PLAN`（僅唯讀鑑定／建議 Route-out；不是實體施工）  
> **日期** 2026-10-12（Asia/Taipei）  
> **Repo** https://github.com/shw097-team/PIPD-LS-SP  
> **最新 main** `224591431a164ab72a9423cd180e417e8a762403`；**Git Tree** `1a9fcb94a42eb589e405c2453793be986419d4cb`  
> **已發布版本** `v0.1.1-preview.3`；**候選公開 Plugin** 尚未實體化、尚未審核發布  
> **Claim ceiling** `DESIGN_AND_STATIC_REPO_EVIDENCE_READY / NO_REPO_MUTATION / NO_S4_FULL_PASS / PUBLIC_PLUGIN_NOT_PUBLISHED`

## 0. Executive adjudication：合併是正確選擇，但不能把建置和公開發行視為同一個 Gate

**主決策：APPROVE — ONE SMALL UPGRADE CHANGESET，NO NEW DEVELOPMENT STAGE。**

將前三輪工作（A 公開 Skills-only Plugin、B 候選包建置與公開交接、C Web/Agent 極簡安裝）合成一次**既有 S4 PKG-07／PKG-08 領域的發行與 UX 升級**，不新增 S4.5、Product Plane、邏輯第九 Skill、CLI 指令、MCP／認證服務，也不重寫 PIPD 上游規範或現有 Compiler。合理的工作單位為：**一個變更契約、一次受控施工分支／PR、一組差異與驗收資料、一次新版本發行候選；OpenAI Public Portal 提交及 Publish 另需獨立的 Human Publisher Gate**。

> 建議 ChangeSet 名稱：`S4-UX-DISTRIBUTION-UPGRADE-R1`。這是本報告**新建議識別碼**，不是上游既有 rule／審批號。

| 分項 | 是否已具備 | 本輪最小新增事項 | 判斷 |
|---|---|---|---|
| 8 logical Skills / source | 是，8×6＝48 檔案 | 鎖定來源，複製到 Plugin `skills/` | **零核心重做** |
| 現有 Web Mount | 是，9 成員發行目錄 | 保留既有 ZIP 為人工掛載 fallback | **不得偽裝成 Public Plugin** |
| Public plugin manifest + ZIP | 目前 Repo 缺 `plugin.json` | 依官方 Agent Plugins 1.0 產生、檢查和打包 | **必要小適配** |
| Web 安裝主入口 | Public Directory 尚未發布 | README 導向已審核的 Public Plugin；未發布前要誠實標待上架 | **文件＋真實主機驗證** |
| Plus/Free fallback | 文件掛載已有 | 可選單一 Markdown projection，以機械產生、完整來源回指 | **可合併的低成本改善** |
| Agent 安裝 | Skill 原始目錄已有；主機各異 | 一份官方安裝 Prompt＋小型 Host 適配／驗證規則 | **不建自製 Installer 平台** |
| Release/Checksum/HITL | 既有 S4 設計及部分實作 | 公開 Plugin build-time ReleaseTuple、檔案雜湊、安裝 readback | **強制補回歸** |
| OpenAI Public review | 未執行 | 發布者 listing／政策／審核／Publish | **非純 PR 任務；獨立 Gate** |

**需要被糾正的想法**：Plugin 已有一切核心素材，但**不是現有 `PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip` 更名後就能正式公開**。官方要求正式 manifest、單一根目錄、Skill 存放路徑與 publishing metadata，Web 文件模式和可安裝 Public Plugin 需分別驗證；Skill 包不在 Web 執行 Python Wheel，也不賦予 HGK WorkOrder 或驗收簽核權。

## 1. 上游 SOURCE／權威／責任範圍

**本輪依據**：`00_KNOW_INDEX.md`～`19_KP_INDEX_CROSSWALK.md`、`challenge-review-SKILL.md`；`PIPD-LS-SP_PIPD-PKG-00..10`；`PIPD-LS-SP_skeleton.md`、`PIPD-LS-SP_藍圖.md`、`PIPD-LS-SP_PIPD-EC_SGM_總藍圖`；`PIPD_LS_canonical_standard.md` 與 `PIPD_LS_DOC-00..09`；必用 donor `SDLC_PRW_HLPE_SKILLS_PLUGIN_R2`、`SWOF_ECP_SKILLS_PLUGIN_v2.0.1`、`SWOF_TQAEP_SKILLS_PLUGIN_v2.0.1`；前三份先行研究報告，均為研究依據而非發行許可。文件中 PIPD-LIFECYCLE-SPEC@1.1.0 保持生命週期 SSOT，不受外部 Plugin 格式反向改寫。

**具體 Locator/ID**：

- `PIPD-LS-SP_藍圖.md` **§8.3 / PIPD-SP-SK-01..08**：8/8 SkillContract；**§15.2**：`One Canonical Source → Generated Surface Adapters`、Web `UPLOAD_MOUNT`／Coding Agent `HOST_ADAPTER`／Hermes `HGK_RUNTIME_SURFACE`；**PIPD-SP-SPEC-030**：MCP 依 live/auth/action/dynamic discovery need 啟用。
- `PIPD_LS_DOC-08` **§8.9、§9、§13.3–13.5**：Full Plugin 是有條件的 multi-Skill 發行與安裝介面；`DESIGN_SELECTED ≠ INSTALLED ≠ ENABLED ≠ EXECUTED ≠ VERIFIED ≠ RELEASED`；要求 pin/hash、license、Host Bind、enable/disable、卸載與殘留掃描。
- `PIPD-LS-SP_PIPD-PKG-07` **Part 7 `07-D04-H2-1` / Part 8 `07-D05-H2-1`**：跨主機觸發／非觸發 parity、Web no-effects、8 Skills exact set、安裝衝突與 owner path 保護。
- `PIPD-LS-SP_PIPD-PKG-08` **Part 11 J00–J10**：Freeze、Dependencies、Schema、Semantic、Secret、SCA、SBOM、Build、Attestation、Independent Qualification、Release Candidate；不因設計包存在便宣稱 Repo runner 已按全部 Job 執行。
- `GPTB-KP16-R01..08`（`16_RELEASE_PACKAGING_CHECKSUM_READBACK.md`）：逐發行 Manifest、SHA-256、包裝後 readback、candidate vs production 分離與 TT/CR；`GPTB-KP11-R01/03/05/06/07/08` 原始證據、審核者身份、工具 provenance；`GPTB-KP17-R01..08` 任務導向的新手 UX；KP14 Apps/Actions/MCP 權限關閉與外部 route-out；`challenge-review-SKILL.md` §Invariants/§Workflow：read-only independent checker、原始證據優先、fail-closed。
- 上游 `DOC-07`/`PKG-06`（TQAEP）維持 maker/checker/批准分權；任何 Public Plugin packaging PASS 不會自動升級 S4 Runtime Full PASS，更不構成 Production Release 或 S5 HGK Execution Admission。

**上游文件較廣，不代表該工作要重跑全部 11-PKG 從頭製作。** 應做 `affected-only + mandatory regressions`，所有新接收對象均以 precise source/subject 綁定。

## 2. 現行 Repo 最新狀態與差距（本輪唯讀重新核實）

- `main` Commit `224591431a164ab72a9423cd180e417e8a762403`（2026-10-12 03:39:21Z）；tree `1a9fcb94a42eb589e405c2453793be986419d4cb`，GitHub recursive tree 未截斷；**8 `skills/pipd-*/SKILL.md`、合計48份 Skill 文件**；正式 `plugin.json` 未發現，現行 Web Mount 發行目錄為 **9 個檔案**。
- 最新公開 Preview **`v0.1.1-preview.3`**；Web Mount ZIP API 遠端 digest `sha256:af342d281f02ba04f284a1625f4a58a6f2de15549cc182a0c61ce357ec6b504f`。此為 GitHub **asset metadata**，本輪並未下載 ZIP 後獨立重算每個位元組。
- `main` 近期已修正 Web Mount 八份內容先前誤填 `preview.2` commit 的 provenance，包含已記錄的 Replace 歷程。**不能繼續聲稱這是現行 ZIP 的未修正缺陷**；但是自動 `release_tag_commit == actual_tag_commit` Gate 尚待工程補全，須加回歸防止再發。
- GitHub 目前沒有可直接宣稱 Public Plugin 上架、Plus/Free 有效載入、Codex/Hermes/Claude 全主機安裝 UAT 都 PASS 的實測證據；不能把 Release ZIP 或 README 當作等效收據。

**選版規則**：本次施工不應直接修改或重寫已發行的 `preview.3`；Owner 選定**新** release candidate commit/tag，依那個候選的 wheel、Skills source、Plugin ZIP 綁定同一 source identity。若 public package 發行獨立版本，需有 canonical `source_release_ref+commit+tree+manifest` crosswalk。**對以往替換過 GitHub release asset 的情況，Tag pin 與下載後 asset SHA 必須同時記錄**。不得假定發布 URL 永久對應某個 bytes。

## 3. 一次小型升級的 Minimum-Sufficient Architecture

核心保留：8 logical skills、19 PIPD contract schemas、13 CLI、PI/PD/DEV ECP/OPS ECP/TQAEP、Canonical Standard、HGK control plane、既有 Web Mount fallback。**只新增衍生發行表面與驗收。**

```text
PIPD S4 frozen source commit (唯一內容真相)
  ├─ skills/pipd-* (8×6 files，無重寫)
  ├─ 已有 Web Mount (保留人工附檔備援)
  ├─ release / source identity
  │
  └─ ONE small controlled upgrade (one ChangeSet / one PR)
       ├─ PUBLIC PLUGIN projection: root plugin.json + skills/* + assets/*
       ├─ AGENT install route: one maintained prompt / thin host guidance
       ├─ WEB user route: README one public plugin link + one-file fallback
       └─ deterministic package checks + skill behavior UAT contract
                   |
                   v
        package + source/destination SHA manifest + raw test logs
                   |
                   v
        INDEPENDENT CHECKER (與 Maker 分離)
                   |
                   v
        Human Publisher / Public Portal (submission and Publish are distinct)
```

**最小發行檔案規則**（作為新生成物而非修改源碼）：

```text
pipd-ls-sp/                 # 發行包唯一根；必須符合官方檢驗
  plugin.json                # Agent Plugins 1.0 公開 manifest
  skills/
    pipd-route-intake/      # 從凍結來源精確複製6檔
    pipd-authority-source/
    pipd-profile-tailor/
    pipd-pi-compile/
    pipd-pd-bind/
    pipd-execution-contract/
    pipd-assurance-tqaep/
    pipd-package-project/
  assets/                    # approved public listing icon 等，必要時建立
  # NO mcp.json, .app.json, Actions, hooks, Python runtime, extra 9th domain skill
```

正式 `plugin.json` 必須遵守 `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` 與 OpenAI 当前 public submission metadata；release manifest version 為合法 SemVer、DisplayName／ShortDescription 字元數核對、Verified Publisher 提供真實身份與網站／支援／Privacy／Terms URLs。八個既有 Skill 的 `SKILL.md` 有自訂 frontmatter；**先跑真實 Validator**，若不接受就對**發行副本**做最小可機械重演的欄位映射，保留原文及 Diff、測試 trigger／refusal，禁止偷改上游業務規範。

**和上游位置關係**：`PKG-07` 負責 Skills/Compatibility/Distribution，`PKG-08` 負責 Packaging/Release/Readback；README／Quickstart 是 `KP17` 投影，外部驗收仍由既有 TQAEP/Challenge Reviewer 執行。**一個 ChangeSet 可以含多個 Task，但不增加 lifecycle Phase/Authority。**

## 4. 一次 PR 內的四個工作包（不能轉成四個獨立產品線）

| Task ID（新建議） | 責任 Owner | Allowed write-set 建議 | 必要輸出 | 明確禁止 |
|---|---|---|---|---|
| `UPG-P01-PACKAGE` | PKG07 / HGK→Codex maker | `packaging/public-plugin/`, 新建 dist build 暫存 | root manifest、8 Skills immutable copy、plugin ZIP、source-to-distribution mapping | 改寫 `skills/`、`src/`、根 Schema、Canonical DOC |
| `UPG-P02-ONBOARD` | DX / PKG07 | `README.md`、`docs/install/` 或一份單獨安裝說明；**只選一組單一來源** | Web 主路徑＋Free fallback；Agent 單一 Prompt，安裝/更新/卸載指引 | 五套手工同步 README、憑空承諾「一鍵自動批准」 |
| `UPG-P03-CHECKS` | QA / PKG08 | 一組精簡 build/verify scripts/tests／Manifest schema | frozen SHA parity、archive validation、negative mutation、Host UAT plan/receipts | 新 Test Engine 或修改既有 S4 gate 使其容易通過 |
| `UPG-P04-RELEASE-HANDOFF` | PKG08 / Release Owner | `release/` 或 `dist/` versioned output、提交材料 | version/digest/TT/CR/roll-back、Public listing draft、獨立驗證包 | 改舊 Tag、上傳 Public Portal、冒用 Verified identity |

**更省事的代碼布局**：若 Repo 已有 `tools/build_mount_pack.py` 和 `tools/portable_install_check.py`，先評估能否用**薄型函式**延伸生成 `dist/plugins/pipd-ls-sp-<version>.zip`；若封裝格式差太多，才增加 1 個明確的 `build_public_plugin.py` + 1 個 `test_public_plugin_packaging.py`，不能為了命名一致做新的抽象平台。`packaging/public-plugin/` 可只保留 root `plugin.json` 模板及展示素材；不要在 Git 再複製 48 份 Skills 原始碼造成兩套需人工維護的版本。**ZIP 產物打包時自現有 source 複製。**

**Publish 不必與 Repo PR 原子提交**：PR/候選 release 作 machine close，Public Portal 所需身份、政策、Scan、Review、Publish 是外部真實流程，應由 Publisher 成果回饋後更新受控發行紀錄，不得把等待 OpenAI 審查視為工程必然失敗，也不能在待審狀態顯示「已公開安裝」。

## 5. 整合後的使用者最少阻力體驗

**README 首屏只保留兩個主要入口**，一般使用者不看到 `pip`, `npm`, `.agents`, `.claude`, ZIP checksum 的冗長選擇；進階頁面保存供校驗和備援。

| 使用者 | 唯一推薦主路徑（目標） | 允許的 fallback | 驗收真相 |
|---|---|---|---|
| ChatGPT Plus | 公開 Plugin Directory → PIPD-LS-SP → Install → 開始設計 | Project／Conversation 單一 `PIPD_WEB_FALLBACK.md` | 需真實 Plus 帳戶實測 discover/install/activate，不承諾所有方案權限相同 |
| ChatGPT Free | 同一公開 Plugin **在該帳戶可用時**直接 Install | 單一 MD 附件，文件模式 | 不支援帳戶標 `NOT_SUPPORTED`，不能顯示虛假安裝成功 |
| Hermes/Codex/Codex CLI/Claude | 貼官方單一 Prompt，Agent 依**目前宿主真正能使用的**原生 Installer 執行 | 進階受控 CLI／手動文件指引 | 安裝前需要審核計畫／必要授權；驗八技能實際 load 與負向拒絕 |

**一段 Prompt** 是使用者體驗方案，不是允許 Agent 跳過權限門檻、在無 Shell Host 中假裝安裝。主路徑不可直接自動執行從 Repo 下載的未稽核 shell script；只可呼叫選定且 pin/version 的本機原生安裝器或帶已審腳本。禁止默默覆寫既有 Skill/`AGENTS.md`、全域 Registry、Secrets 與其他 Plugin。請以單一 Host capability table 判斷需要的讀檔、網路、寫入與 consent，無能力採 `NOT_SUPPORTED`。使用者只需理解**安裝的目的**和**必要授權**。

**公開 listing／安裝文件的版本型別不得混淆**：`source release v0.1.1-preview.3` 是目前現況；新的 Public Plugin 若首次發布，需有自己的 SemVer + exact source mapping；不能預先宣稱 Public Plugin 已上架。若未發布，README 首屏應顯示「公開上架待審」，主線仍使用最短可用的單一 MD fallback，避免引導死連結。方案切換由發行狀態驅動，不由模型隨意選。

**UX 衡量方式（建議目標，不取代上游 gate）**：Web 已上架後不要求使用者選擇一份份 MD；Free fallback 只附 1 MD；Agent 操作者只貼一段 Prompt 並批准必要寫入；所謂 0 人工步驟**不包括法定／安全授權**。以新手 UAT 原始錄影／步驟記錄統計「選擇數、錯誤率、首次任務成功率、真正生效時間、卸載殘留」，不以宣稱「一鍵」當 PASS。

## 6. 必要 Gate：兩層完整性、八個 Skill 行為與跨主機 UAT

| Gate | 必要直接證據／檢驗 | Negative mutation／Fail condition | Owner |
|---|---|---|---|
| `UPG-G00` Source freeze | Commit/tree、source SHA、release asset raw hash、build environment | floating `main`、錯發布 tuple | Release/Independent |
| `UPG-G01` Source immutability | 施工前後 `skills/src/schemas/上游文件` hash/diff 皆無意外變化 | 改源檔、壓縮 DOC/refusal | Independent |
| `UPG-G02` Plugin exact set | 8/8 expected Skills，**48/48原始支援檔**；Manifest+ZIP 結構 | 第九邏輯 Skill、缺單一 reference、symlink/path traversal | Maker+Checker |
| `UPG-G03` Semantic mapping | 每個 source path/hash→dist path/hash；derived diff ledger＋批准 | 靜默簡化/刪除 Source Locator/SoD/NACK | Independent/TQAEP |
| `UPG-G04` Official package | Agent Plugins 1.0 manifest、相容 frontmatter、無 MCP/apps/hooks、version/listing、scan | Plugin root 錯、manifest key 不合法、秘鑰滲漏 | Pack/Portal |
| `UPG-G05` Release regression | 新版 manifest、SHA-256、zip 解壓 readback、release commit 一致；刻意舊版 tag 攻擊 | ZIP 內舊 provenance、tag/digest 不匹配 | Release/Checker |
| `UPG-G06` Skill behavior | 八個 Skill 各 1+ 真正正向與反例、直接/間接觸發與非觸發、missing-source typed NACK、false PASS veto | 被壓成泛用助手、拒絕失靈、產生假 repo commit/pass | TQAEP/Checker |
| `UPG-G07` Web consumer | Plus 真實 discover/install/active & conversation；Free 可用性實測／MD fallback | 只上傳 ZIP 就稱「已安裝」、文字冒稱 Python Runtime | Consumer UAT |
| `UPG-G08` Agent consumer | Hermes/Codex CLI/Codex/Claude 真實 discovery/load、positive/negative、install/uninstall/conflict | Installer exit0 但 Host load 無效；覆寫既有設定 | Host qualification |
| `UPG-G09` Submission/PUBLISH | 真實發布者身份、Listing URLs/Logo/Privacy/Terms、Portal scan、Approval、Publish、外部安裝 readback | Draft 或 Private 被稱 Public；Human click 被假簽 | Human Publisher/Independent |

**保留原本 S4 測試與安全 Gate**，此 PR 只增加受影響的 packaging/consumer 閘門，不能為了縮小人工步驟而刪除 fail-closed、秘密掃描、控制面、HITL 或獨立 checker。既有 S4 靜態缺陷（例如 TraceLink Schema/closure）若對**Plugin 的宣稱能力**有安全影響，應在 CapabilityLoss 和 known gaps 中公開；不要以建立新的 Public 包「順便修」出額外不可審差異，也不得宣稱八 Skills 等於完整 Runtime Compiler。

**封閉條件要分清**：

- `BUILD_PASS`：候選 ZIP、Manifest、檔案／語義映射、機器負向測試、發行 Readback 完成。
- `PLUGIN_LOCAL_QUALIFIED`：真實受支援 Host effective-load＋負向測試合格，由獨立 Checker 審定。
- `PUBLIC_PUBLISHED`：Portal 已批准並由 Human Publish、真實用戶可安裝確認。
- `PIPD_S4_FULL_PASS`：**不因前三者成立而自動成立**，其原本獨立 S4 Gate 必須另閉合。

`TEMP_CLOSED`：沒有正本數據或尚在審查；`PARTIAL`：局部有效但非阻斷剩餘；`FAIL`：出現阻斷的 Schema/Source/安全/反向使用者失效。缺證據不可假通過。

## 7. RACI／SoD／合法 Route-out / ECP 契約

| Actor | 建置 | 修改公開 metadata | 獨立驗證 | 真實發行 | 禁止 |
|---|---|---|---|---|---|
| Product/Authority Owner | 確認名義需求／限制 | 核對產品宣稱 | 決定 applicability | 核准發行策略 | 直接偽造 raw evidence |
| HGK＋Codex Maker | 隔離工作區 package、PR、logs、hash | Draft/提案 | 自測僅 Maker Evidence | **無權代替 Owner Publish** | 修改 SSOT/Oracle/Checker verdict |
| Independent Challenge | 唯讀 source、fresh verifier、反例測試 | 查錯 | 完成 bounded independent report | 無 | 修碼後自簽 PASS |
| Release Owner | 版本、Manifest、供應鏈、rollback | listing 經驗證 | 發行 readback | 管理受控 release | 默默換舊 tag 或掩蓋失敗日誌 |
| Human Publisher | 核實身分、Terms/Privacy、國家/區域、商務 | 核准 | 參閱驗收收據 | Portal Submit/Publish | 把尚未審核說成 Published |

**外部施工包輸入（推薦 `OROCHI_FACTORY_ORDER.v1` 包絡，但此處是候選，不冒充已路由）**：`task_kind=DESIGN/IMPORT output route-out`、`change_class=UPGRADE`、`source_freeze={commit,tree,tag,sha}`, `objective=one install primary path each Web/Agent`, `allow_write_set`, `deny_write_set`, `acceptance_ids=UPG-G00..09`, `negative_cases`, `raw_evidence_required`, `rollback`, `release_claim_ceiling`, `human_gates`。Maker 可先提出 `Issue → TaskSpec → PR`，自動建置只在授權 worktree，返回候選 `evidence_return_pack`。本對話**未向 HGK/OROCHI/Codex 真正派工**。

**建議能直接貼給 HGK 的施工摘要**：

> 使用 frozen PIPD-LS-SP S4 Repo source，將既有 8 Skills 製成 Public Skills-only Plugin 與單一 Agent/Web 安裝入口。僅一個 S4 `UPGRADE` ChangeSet、一條 PR、Release／Host UAT 受控工作。先列 `source manifest + impact diff + allowed write-set`，不得改原始 Skills、19 Schema、13 CLI、上游 SPEC、Oracle/Gates、不得啟用 Apps/Actions/MCP/Hooks 或自行公開發布。使用確定性複製＋官方 Agent Plugins 格式，證明 48/48 source/destination、8/8 trigger/NACK、ReleaseTuple、ZIP、安全及 Plus/Free/Agent effective-load；只更新 README 主入口、備援一檔、Agent 一段 Prompt。回傳原始 logs、diff、SHA256、TT/CR、rollback 和 Owner 批准要求，由獨立 Checker 評估；未驗證時 fail-closed。

## 8. 發布安全／平台最新規則（屬支援資料，非上游權威）

**OpenAI 官方 Plugin docs**（2026-10-12 檢索）：

- `https://developers.openai.com/plugins/build/plugins`：portable root `plugin.json`、固定 `skills/`、無 MCP 時無需 `mcp.json`、可在 Codex/HGK 之外建構 ZIP；Skills-only 不需要新的主機運行服務。
- `https://developers.openai.com/plugins/build/skills`：直接／間接／缺輸入／非觸發／邊界測試，從 Skill 目標決定如何編排；Skill instructions 不代表 MCP Tool。
- `https://developers.openai.com/plugins/deploy/submission`：ZIP upload→scan/check→submit→approve→publish 的**多 Gate**；可在原始 Repo 建置 ZIP，不必在 ChatGPT UI 重寫原碼。**目前官方明言「已發行 Skills-only Plugin 不支援之後直接新增 MCP」**，故本次保持純 Skills-only，未來如需 MCP，另做 Provider/Security/產品演進 ADR；不能偷塞空 MCP 後端預留。
- `https://developers.openai.com/plugins/deploy/submission-errors`：ZIP plugin root、skill 合法性、禁止 Skills-only 加入 MCP/app 設定、manifest validation。
- `https://developers.openai.com/plugins/plugin-guidelines`：Skills-only 也須具有效 listing metadata，公開資格依 Portal 判定。發布準備手冊另要求四個可驗證 Listing URLs（產品、支援、隱私、條款）。先按保守原則備妥，若 Public Portal 本次某類別不要求，以 Portal readback 為準，不應靠臆測減免。

**勘誤三點**：

1. **不需要三條新子開發線**。所需新工作是 S4 既有 PKG07/08 一個發行升級 PR；Public submission 是 **release/human gate**，不是 Coding Stage。
2. **「八 Skills 已有」≠「Public Plugin 已存在」**，也不等於 Skills-only Web 端能執行 Python CLI。
3. 前一輪針對 4 Listing URLs「Skills-only 可選」和準備規範「四項要齊」的說法有分歧。本報告為降低 Submit 失敗採 **四 URL 都預備且驗證；最終以 Public Portal 實際版型與檢查 readback 為準**；不因此新增法律網站開發工程線，缺正式政策則可在提交前保持 `PUBLISH_HOLD`。

## 9. 升級成功的實際產品路徑、Overengineering Index 與 No-Go

| 選項 | 主要收益 | 額外工程風險 | OEI（定性） | 裁定 |
|---|---|---|---|---|
| **A. 一個 S4 Distribution/UX PR** | 使用者入口一致、單一來源、少重工 | 官方格式／host/UAT 審查 | **低** | **採納** |
| B. 三個獨立安裝／Plugin／公開發布專案 | 每線可單獨排程 | Manifest、SSOT、文件、驗收重複 | 中高 | **不採納** |
| C. 為了安裝重造跨主機 Installer Framework | 運作或可自訂 | 新 dependency/unsafe shell/maintenance | 高 | **不採納** |
| D. 累加 MCP、Remote backend、OAuth | 動態工具可用 | 安全／提供者／政策／Hosting 面擴大 | 極高 | **此輪不採納** |

OEI 以新 Runtime、新 Authority、重複實作、外部權限面及維護負擔作啟發式評估，**不是量測的市場指數**。若要再次擴 scope，先要求有真實使用者痛點、明確正向收益、與現有安裝能力無法達成的 counterexample，再走 ADR／ChangeSet；不能因平台流行而加層。

### 明確的停工與拆案條件

- 官方 Plugin Validator 不接受某個 Skill 核心 contract，且最小發行副本適配會改變上游 SoD／拒絕條件 → **TEMP_CLOSED**，開相容性 TT，不能直接刪詞通過。
- 需寫新的 Backend／MCP／Actions、要求真實 GitHub 憑證、Remote Code Execution、或新增 Python Compiler 能力 → **超出本次小升級**，另案 Decision；不硬併。
- 任一必要 Host 的版本或 Native Skill 安裝能力缺乏 → 標 `NOT_SUPPORTED`、採已驗 fallback；不混成跨宿主 Universal PASS。
- 未有 verified developer/Policy URL/Portal 權限 → **code pack 可以 ready，PUBLIC_PUBLISHED 仍 HOLD**；不以沒有 Portal 權限否決已完成的局部工程，但也不對外宣稱可公開下載。
- 任一既有核心 Schema／Trace 或發行已知負向案例仍未閉合 → 在相關使用者聲明標示 capability ceiling / blocked gate，不趁此次「安裝 UX PR」暗修 Core Compiler。

## 10. 驗收結果與後續邊界

**本輪已完成**：三份前案整合；現有上游 locator crosswalk；GitHub main/發行 metadata/8 Skills/48 source/現有9檔 Web Mount/manifest absence 的 read-only 核對；官方 Public Plugin 格式與 submission Gate 查證；單次小升級施工與驗收契約；建議停工／拆案規則。

**本輪未執行**：在遠端 Repo 寫入、Codex CLI build、Public Plugin ZIP 產物、Host install/UAT、Portal 上傳／審查／上架、S4 全部 Runtime tests、Human Ratification。舊 S4 PASS/FAIL 現況不能由本方案覆寫。

```yaml
report_kind: EXTERNAL_ENGINEERING_ADJUDICATION
scope: PIPD_LS_SP_S4_DISTRIBUTION_AND_ONBOARDING
change_class: UPGRADE
recommendation: ONE_SMALL_CHANGESET_ONE_REVIEWED_PR
new_substage: NOT_REQUIRED
reuse_existing_skills: 8_OF_8
new_compiler_or_mcp: NOT_ALLOWED_IN_SCOPE
public_plugin_artifact: NOT_YET_BUILT
public_submission: NOT_EXECUTED
consumer_uat: NOT_EXECUTED
build_approvable: SUBJECT_TO_OWNER_SCOPE_AUTHORIZATION
independent_checker: REQUIRED
human_publisher: REQUIRED_FOR_PUBLICATION
full_s4_acceptance: NOT_INFERRED
claim_ceiling: DESIGN_READY_STATIC_EVIDENCE_ONLY
```

## 11. 溯源連結

- PIPD Repo：`https://github.com/shw097-team/PIPD-LS-SP/tree/224591431a164ab72a9423cd180e417e8a762403`
- Public Preview：`https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.1-preview.3`
- 舊版 Web Mount readback：`https://github.com/shw097-team/PIPD-LS-SP/blob/224591431a164ab72a9423cd180e417e8a762403/dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3/README_MOUNT.md`
- Source map：`PIPD-LS-SP_藍圖.md` §8.3、§15.2；`PIPD_LS_DOC-08` §8.9、§13.3、§13.5；`PIPD-LS-SP_PIPD-PKG-07` Part 7–8；`PIPD-LS-SP_PIPD-PKG-08` Part 11；`GPTB-KP11/14/16/17/18`；`challenge-review-SKILL.md` §Invariants、§Workflow；`PIPD_LS_canonical_standard.md`、DOC-00..09。
- 前案：`PIPD-LS-SP_S4_極簡安裝體驗_工程鑑定與改造方案_2026-10-12.md`；`PIPD-LS-SP_S4_Public_Skills-only_Plugin_建置發行_工程鑑定_2026-10-12.md`；`PIPD-LS-SP_S4_Public_Plugin_是否需要子開發階段_工程鑑定_2026-10-12.md`。
- OpenAI 2026 平台核對：`https://developers.openai.com/plugins/build/plugins`、`https://developers.openai.com/plugins/build/skills`、`https://developers.openai.com/plugins/deploy/submission`、`https://developers.openai.com/plugins/deploy/submission-errors`、`https://developers.openai.com/plugins/plugin-guidelines`。

**最終裁定：`APPROVE_SMALL_UPGRADE_AS_PLAN / NO_NEW_SUBSTAGE / PUBLICATION_HUMAN_GATE / NOT_IMPLEMENTED_THIS_TURN`。**
