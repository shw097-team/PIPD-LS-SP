# PIPD-LS-SP｜S4 R4 修補後外部獨立複驗、三合一升級與私人 Plugin ZIP 裁決

**報告識別**：`PIPD-S4-EXT-ACCEPT-R4-20261013`  
**重驗日期**：2026-10-13，Asia/Taipei  
**受驗 Repo**：<https://github.com/shw097-team/PIPD-LS-SP>  
**驗收身分**：External Independent Challenge Reviewer；唯讀取證、交叉反證、合併／發行工程決策建議；非代行 Repo Owner／Human Ratifier／Portal。  
**核心原則**：MVP 開源、低阻力、必要修補、反過度工程；證據與聲明上限分離。  
**摘要裁決**：**`SCOPED PASS / MERGE-RECOMMENDED-NOW`（Stage A＋Stage B 工程候選）**；**`PARTIAL`（S0–S4 跨宿主最終驗收）**；**`ZIP_STATIC_COMPATIBLE / PRIVATE_IMPORT_NOT_VERIFIED`**；**`PREVIEW_RELEASE_CONDITIONAL`**；**`PUBLIC_DIRECTORY_HOLD`**；**`TEMP_CLOSED`（本階段剩餘非 P0 工程事項）**。

> 本報告是本輪直接重取 GitHub 受驗候選、GitHub Actions 原始日誌及 OpenAI 官方 ZIP 規格後形成的外部挑戰報告，不是 Maker 自簽收據；也**不是** `challenge-review-SKILL.md` 附屬 canonical validator 產生的 JSON＋digest-bound Markdown 雙檔包。未取得完整技能 references/scripts/assets 同一套件，因此不冒稱此一形式資格檢查已通過。此報告不執行 GitHub merge、tag、publish、Portal 上傳或使用者帳戶私人安裝。

---

## 1. 本輪決策先行：必須給出實際可用裁決

| 對象 | 本輪裁決 | **立刻要做／不用再做** | 不可聲稱 |
|---|---|---|---|
| **Stage A / PR #3** | **工程合併建議 `PASS`，准進主線整合程序** | 以目前 SHA 固定執行順序，PR #3 先合併；不要求再開修補輪 | 不是 Production、不是 S4 Full PASS |
| **Stage B / PR #5** | **工程合併建議 `PASS`，接續 PR #3 合併** | PR #3 成功後，以 PR #5 對應最新 head 及 `main` 重新比對，已有相同 head 的雙工作流成功紀錄；無重大漂移可合併 | 不是 Web 帳戶上傳成功／公共上架 |
| **GitHub 下一版 Open-source Preview** | **下一次發布作業有條件放行，不需要新核心開發** | **一次**不可變 Tag＋重新建置＋ZIP/Wheel SHA-256＋ReleaseTuple＋最小安裝 Smoke；成功即可發布新的 preview | 不得重寫 preview.3 Tag/同名資產，不能當 Stable/S4 Full PASS |
| **ChatGPT Web 私人 Skills-only Plugin ZIP** | **結構相容候選：`STATIC_PASS`；實際安裝：`NOT_VERIFIED`** | 如帳戶有權限，直接試現有候選 ZIP；一次 Portal/私人上傳＋8 技能觸發 Smoke；若受帳戶限制即記 `NOT_AVAILABLE_FOR_ACCOUNT`，改 Plugin Creator／MD fallback | 不得把 ZIP 內檔案存在解讀為已安裝／有效載入 |
| **公開 OpenAI Plugin Directory** | **`HOLD`（獨立發行渠道）** | 開源 S4 MVP **不必等**公共上架；日後另完成 verified publisher、Portal scan/review、publish、回讀 | 未完成公共審核絕不能說 `PUBLIC_DIRECTORY_PUBLISHED` |
| **S0–S4 四主機全量終驗** | **`PARTIAL`＋本階段 `TEMP_CLOSED`** | 不再因低風險表單、備註、單點格式而返工；真正各宿主可用性以首次實際使用收據閉合 | 不授予 Universal 8/8 Host Qualified、S4 Full PASS |

**主決策**：**此刻不需要再修核心邏輯，應進入有順序的 PR #3→PR #5 技術合併；待一次不可變 Preview 打包與最小手動 Web 會話測試後，開放可辨識限制的預覽使用。** 把完整公共 Directory、四 Host 覆蓋率、形式化 Evidence Pack 的尾端治理移至後續階段。實際 GitHub 按鈕由授權持有人操作；本報告給出工程放行**建議**，不是偽稱有人已實際按下 Merge。

**例外阻斷**：若合併前任何 head 改變了 `src/`、`skills/`、`schemas/`、測試 Oracle、Workflow security 或 ZIP builder，則這項對舊 SHA 的 scoped PASS **不自動繼承**，只需對改動差異跑 affected regression；不是無限重跑 S0–S4。

---

## 2. Authority／掛載／檢查方法與聲明分層

本地 `/mnt/data` 已嚴格 UTF-8 逐檔讀入核對，並生成同目錄 `input_inventory_2026-10-13_recheck.json`：

- `00_KNOW_INDEX.md` 至 `19_KP_INDEX_CROSSWALK.md`：**20/20**；
- `PIPD-LS-SP_PIPD-PKG-00..10`：**11/11**；
- `PIPD_LS_DOC-00..09`：**10/10**；
- `PIPD-LS-SP_skeleton.md`：**1/1**；`PIPD_LS_canonical_standard.md`：**1/1**；
- `challenge-review-SKILL.md`：**1/1**；
- `PIPD-LS-SP S4｜三合一小型升級藍圖(1).md`：**1/1**；
- 既有 2026-10-12 S0–S4 外部工程方案、2026-10-12 S4 修補後驗收報告、2026-10-13 R3 完整驗收報告：均作為**歷史 challenge／回歸 baseline**，非新候選的預設判決。

位元組核對及關鍵章節擷取不等於巨量 PKG／DOC 每一行完成獨立語義再審；本輪為與修補／發布直接相關之 scoped acceptance。

**Authority**：system/developer → 本輪 user task → 上游 canonical／PKG r2／skeleton／DOC → GPT B KP／`challenge-review` → 受驗 Repo bytes／CI raw → 現行官方 Web 支援（僅判 platform drift）。核心定位如下：

| 範圍 | 規範 locator／rule ID | 本輪使用情境 |
|---|---|---|
| Evidence rawness | `11_EVIDENCE_REQUIREMENT_MATRIX.md`，`GPTB-KP11-R01/R03/R06/R07` | Workflow **raw log** 優先於自述 `green` |
| 防 Gate Calibration | `12_EVAL_REGRESSION_LLM_JUDGE.md`，`GPTB-KP12-R01/R03/R06/R07` | 真測試數、負例、退出碼、affected regression |
| 發行物身分 | `16_RELEASE_PACKAGING_CHECKSUM_READBACK.md`，`GPTB-KP16-R01/R02/R03/R05/R08` | SHA-256、readback、新 immutable preview |
| UX | `17_UX_ONBOARDING_NO_BRAIN_FLOW.md`；三合一 R2 `§8.1–8.5` | Web 1 MD、Agent 1 prompt、host 實際觸發 |
| 開放項處理 | `18_TT_CR_DRIFT_REGISTER.md`，`GPTB-KP18-R01/R02/R05/R07/R08`；PKG-06 DOC-05 `TT_CLOSURE_WITHOUT_CHECKER` | 阻斷與後置項分離，不用 Maker 自稱 CLOSED |
| 挑戰技能 | `challenge-review-SKILL.md` `§Invariants`、`§Workflow 1–5`、`§Safety and permissions` | exact subject；確認正負例；只寫外部驗收產物 |
| 三合一契約 | 三合一藍圖 R2 `§3.2`、`§5.1`、`§9.1 UPG-G00–G09`、`§9.2 TR-01..`、`§10` | 四工作包／十 Gate／MVP 反過度工程 |
| 上游 stage claims | `PIPD_LS_canonical_standard.md`、`PIPD_LS_DOC-07/08`、PKG-07/08/10 | 否決產品工程 PASS→公開上架／四宿主 qualification 的跳級宣稱 |

**重要判準**：Repo 檔案是受驗對象，其內「NO_MERGE」「CHECK_PENDING」「LOCAL_PACKAGER_PASS_ONLY」屬於作者／Maker 自限與工作流狀態，必須尊重**實際法定授權**，但不能阻止本輪受委託的獨立驗收官依新證據做出不同的**工程放行建議**。本報告不冒稱已取得實際人的 Ratification Token 或 external runtime promotion。

---

## 3. Frozen GitHub Subject：上一輪與本輪的新事實

**GitHub connector 2026-10-13 直接取證**：

| 實體 | 確切 Git SHA | 狀態 |
|---|---|---|
| `main` | `224591431a164ab72a9423cd180e417e8a762403` | 未前進 |
| Stage A | `759b9f0dc880b2f960363b2ceaa68446c770061d` | Draft PR #3，target `main` |
| Stage B **最新** | `940a37d00d5c1d12dfc9ae5d2325d8837b08501b` | Draft PR #5，target Stage A |
| 舊 R3 | `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` | Draft PR #2，保留歷史，不要作為新 release head |
| 歷史公開發行 | `v0.1.1-preview.3` | **舊版**，不可冒稱含新修補 |

- GitHub Compare `main...Stage A`：`ahead_by=104`、`behind_by=0`；包含大量歷史累積變更（247 changed files），**不是**單一補丁。
- `Stage A...Stage B`：`ahead_by=25`、`behind_by=0`；Stage B **繼承** Stage A，不需要重複 cherry-pick。GitHub Compare `main...Stage B`：`ahead_by=129`、`behind_by=0`（GitHub changed-files 回傳受 300 筆上限影響，不可把它當完整路徑清冊）。
- PR #3 <https://github.com/shw097-team/PIPD-LS-SP/pull/3> 與 PR #5 <https://github.com/shw097-team/PIPD-LS-SP/pull/5> 均 `draft=true`, `mergeable=true`, `merged=false`。`mergeable` 是 GitHub 的衝突判定，不是安全驗收。
- 相同時點的 public release list 沒有新 Preview Tag；因此此次**沒有**實際新發布。

### 3.1 最新 Hosted CI 真正結尾（不是 Badge）

**同一受驗 SHA**：Stage B `940a37d00d5c1d12dfc9ae5d2325d8837b08501b`。

| GitHub run | Job ID | 真正原始測試／證據 | 結論 |
|---|---|---|---|
| [`ci` 38407236130](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38407236130) | `115329930528` | `Ran 592 tests ... OK (skipped=6)`；聚焦 `Ran 108 tests ... OK`；wheel clean venv；installed registry；provenance mutation refusal | `success`，**與實際測試一致** |
| [`public-plugin-verify` 38407236156](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38407236156) | `115329930743` | 變更路徑 Gate `WRITE_SET_CLEAN_AGAINST_759b9f0...`；`Ran 54 tests ... OK (skipped=1)`；全量 `Ran 592 tests ... OK (skipped=6)`；`MUTATION_REFUSED_ON_IDENTITY_BINDING`；`BYTE_DRIFT_REFUSED_ON_MANIFEST_BINDING` | `success`，後續步驟未被跳過 |
| 同 head push [`ci` 38407227631](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38407227631) | `115329903654` | 同候選另一觸發方式完成全部重要步驟 | `success` |
| Stage A [`ci` 38398212337](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38398212337) | `115298761473` | 有效測試／wheel install／mutation 步驟全部完成 | `success` |
| Stage A [`public-plugin-verify` 38398212422](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38398212422) | `115298764509` | write-set／工具／測試／負例全部完成 | `success` |

CI 在完整套件輸出中另有 **47 tests、2 failures／1 errors** 字串，它是**被測工具的故意紅燈對照／fixture 記錄**，不能當作最新全量 suite 故障；最新 suite 的最終結果明示 592 OK，且 Job 與 step 退出碼匹配。這一區分是防止 gate overfit/false positive 的必要校準。

### 3.2 對 R3 五項 Finding 的逐項裁決

| 上輪 ID | 上輪問題 | 本輪證據 | **R4 工程結案裁決** |
|---|---|---|---|
| `S4R3-F001` | CI `tee` 吞錯、572/11 failures＋108/2 failures 假綠 | `ci.yml` 每個測試 pipeline 使用 `set -euo pipefail`；592/108 OK；獨立真失敗對照及 raw logs | **阻斷解除，工程層 `PASS`** |
| `S4R3-F002` | public-plugin write-set 首關紅燈，後續全部 skip | 新 Stage B 基底為 Stage A；allowlist refusal selftests 與完整流程 `success`，raw `WRITE_SET_CLEAN` | **阻斷解除，工程層 `PASS`** |
| `S4R3-F003` | Plugin／Host 真實發布與載入不足 | 既有 ZIP 實體＋新 GitHub 正負例；未獲真人 private upload / public portal receipts | **ZIP 靜態兼容；宿主 `NOT_VERIFIED`，不得阻止 Repo 工程合併** |
| `S4R3-F004` | Web fallback／README／First-run 文件缺口 | `docs/install/PIPD_WEB_FALLBACK.md`＋ `.sha256` 已上 Repo；`docs/USER_GUIDE.md` 已新增；README 已設導航 | **基本交付 `PASS`；狀態敘述殘留屬 P2 文案同步，不再加阻斷** |
| `S4R3-F005` | Repo 衛生／過多歷史 evidence | Stage B tree 既有 `.hgk/` 1,491 個 blob，約 63.5MB，總 blob bytes 約 66.8MB | **維持歸檔與敏感資料最低檢查；非核心合併 Gate** |

**補充新發現**：`docs/install/README.md` 仍稱 `derivations.json` 空、Publisher／icon 尚不存在，但 Stage B 候選實際 `packaging/public-plugin/derivations.json` 已有 8 筆，manifest 亦有 publisher digest/icon pin，舊文件屬**明顯過期宣稱**；`README.md` 的「Verification entry point」仍指舊 R3 branch。此乃 `NON_BLOCKING_OBSERVATION`，下一次 release docs 同步修正即可；不能不當提升為產品邏輯阻斷。

---

## 4. 三合一 R2 藍圖：UPG-P01–P04／UPG-G00–G09

### 4.1 四工作包

| 包 | 規劃目標 | 現行受驗證據 | 裁定 |
|---|---|---|---|
| P01 | 來源凍結、exact 8 Skills、審計派生 | `tools/freeze_public_plugin_source.py`、8 筆 derivations、source ledger；54 項相關 suite | **scoped PASS** |
| P02 | OpenAI Skills-only Plugin ZIP 封裝 | `tools/build_public_plugin.py`、portable `plugin.json`、實體 56 成員 ZIP、source/receipt；Portal 未試 | **local/structural PASS；不等於 installed** |
| P03 | ChatGPT Web Free／Plus 單檔備援 | `tools/build_web_fallback.py`，`docs/install/PIPD_WEB_FALLBACK.md` 42,145 bytes + sha256、負向 MANIFEST tamper | **document deliverable PASS；real account 未驗** |
| P04 | 安裝 SSOT／四 Agent 宿主入口／Read-only CI | `docs/install/README.md`、`PIPD_AGENT_INSTALL_PROMPT.md`、`docs/USER_GUIDE.md`、2 工作流全部新綠 | **Repo 工作包 PASS；四 Host qualification 未驗** |

### 4.2 十 Gate（嚴格限定可聲稱的層次）

| Gate | 結果 | 何者真的關閉／何者留待下一階段 |
|---|---|---|
| `UPG-G00 SOURCE_FREEZE` | `PASS_SCOPED` | Stage A / Stage B commits、對照 refs 固定；尚無**新的** immutable release |
| `UPG-G01 SOURCE_IMMUTABLE` | `PASS_SCOPED` | Stage B vs Stage A product write-set allowlist 綠；`.hgk/` 為明示 exclude、非准予任意改產品 |
| `UPG-G02 EXACT_SKILLS` | `PASS_SCOPED` | ZIP 中 8 個 `SKILL.md`；凍結來源導出、54 tests |
| `UPG-G03 SEMANTIC_PROJECTION` | `PASS_SCOPED` | builder/source ledger 8 derivations＋tests；非實際 OpenAI host semantic effective-load |
| `UPG-G04 PACKAGE_FORMAT` | **`STATIC_PASS / PORTAL_UNTESTED`** | ZIP 根 `plugin.json` 是官方明列支援之 portable 格式；路徑與目錄結構可驗；Portal scanner 未執行 |
| `UPG-G05 RELEASE_PROVENANCE` | `PASS_CANDIDATE / NEW_RELEASE_OPEN` | old preview.3 immutable tag 跟 served asset rebuild 不一致的歷史 caveat 尚在；不得復用它發布新修補 |
| `UPG-G06 SKILL_BEHAVIOR` | `PASS_DETERMINISTIC / HOST_OPEN` | 測試負例、資料來源、Refusal 與 592 suite 成功；不得代替 8×4 host-trigger |
| `UPG-G07 WEB_CONSUMER` | `FALLBACK_READY / PRIVATE_INSTALL_UNTESTED` | 1 MD 可手動 Knowledge mount；私人 Plugin ZIP 可測，但帳戶 UI/權限尚無真實紀錄 |
| `UPG-G08 AGENT_CONSUMER` | `INSTALL_CONTRACT_READY / HOST_UNTESTED` | Hermes、Codex GUI、Codex CLI 的單段安裝提示詞已到位；每 Host 原生 discovery/8-of-8 裝載不由 CI 證明 |
| `UPG-G09 PUBLIC_RELEASE` | **`HOLD_PUBLIC_DIRECTORY`** | 公共 Plugin Directory 需另外 verified publisher＋Portal scan/review＋publish；不阻擋 GitHub 開源 Preview／私人使用 |

### 4.3 不得恢復的過度工程選項

- 不新增第九 Skill，不上 MCP／Actions／Hooks，不新增 S4.5，不把 web single-document fallback 轉成必跑 server。
- 不要求同一輪四 Host×所有 OS×所有供應商模型全覆蓋才可**合併原始碼**；高風險權限／越界行為仍應 fail-closed。
- 不要為修飾 Maker 的過時摘要再建立第二套 Oracle 或多一級證據治理；非阻斷文件在下一次 Release Docs patch 同步即可。

---

## 5. ChatGPT Web 私人 Plugin：OpenAI 2026-10-13 官方規格核對

### 5.1 官方來源與平台漂移（SUPPORT，而非上游 Norm）

1. **OpenAI Help: Plugins in ChatGPT** — <https://help.openai.com/en/articles/20001256-plugins-in-chatgpt>：個人 Plugin 可由 **Plugin Creator** 建立／使用；在有上傳選項與必要權限的 ChatGPT Web 工作區，可於 Admin console → Plugins → Add → **Upload plugin** 上傳 ZIP；私人／workspace sharing 與公開 directory publication 是不同動作。
2. **OpenAI Developers: Submit plugin** — <https://developers.openai.com/plugins/deploy/submission>：可建立 Skills-only Plugin，私用與公共審核不同；Portal 上傳 ZIP 的受支援原始 manifest 包括 Agent Plugins portable `plugin.json` 與 `.codex-plugin/plugin.json`；公共出版才需要 Portal 流程。
3. **OpenAI Developers: Submission errors** — <https://developers.openai.com/plugins/deploy/submission-errors>：ZIP 要求：一個清楚 plugin root；根 `plugin.json`／`.codex-plugin/plugin.json` 等支援格式；至少一份 `skills/<name>/SKILL.md`；ZIP 不超過 **100 MB**、不超過 **5,000 entries**、解開不超過 **512 MiB**；禁止 `../`、絕對路徑、路徑碰撞、unsupported types。
4. **OpenAI Developers: Package your plugin** — <https://developers.openai.com/plugins/build/plugins>：Codex-style 以 `.codex-plugin/plugin.json` 為主要入口；**但 portable Agent Plugins manifest 仍是 submission-errors 明列的 ZIP 支援格式**。不要將兩種格式混為一談。
5. **OpenAI Developers: Plugin architecture／Build skills** — <https://developers.openai.com/plugins/concepts/plugins>、<https://developers.openai.com/plugins/build/skills>：Skills-only 不需 MCP，指令與 live tool 層須分離。
6. **OpenAI API Agents environment.plugins** — <https://developers.openai.com/api/docs/guides/agents-api/tools/plugins>：API sandbox 的 ZIP **一個 plugin folder 包 `.codex-plugin/plugin.json`**，此為**不同產品表面**，不能拿來否定 ChatGPT Web Portal 支援的 portable ZIP。

> **規格漂移裁定 `ADOPT`**：上輪 Repo 文件把 Web Route 限定為「一份 MD，因無 Public Directory listing 所以不能從 Directory 安裝」，對 **Public Directory** 仍正確；若誤讀成「Web GPT 不能有私人 ZIP Plugin」，則依最新 OpenAI 文件**不正確**。私人、workspace、公開與 API sandbox 四種渠道必須拆開寫。

### 5.2 GitHub 實體 ZIP 的獨立結構盤點

**本輪實際取得 GitHub Repo 某一份既有封裝**，不是只看 Builder 名稱：

- Path：`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/08_PLUGIN/BUILD_AFTER_SUPPLIES/pipd-ls-sp-public-skills.zip`
- GitHub ref：`940a37d00d5c1d12dfc9ae5d2325d8837b08501b`；歷史封裝 receipt 的**凍結 source commit**：`3233c817cc0a8fcd3f80f49219f219544235d25a`，**不是** latest Stage B HEAD（不可錯誤宣稱同一個 build-source commit）。
- GitHub file connector 回傳 base64，經本輪在記憶體中解碼 **ZIP central directory**：**68,102 bytes**、**56 entries**、**唯一頂層目錄 `pipd-ls-sp-public-skills/`**、manifest `pipd-ls-sp-public-skills/plugin.json`、**8/8 `skills/<name>/SKILL.md`**。
- 8 Skill 名稱：`pipd-assurance-tqaep`、`pipd-authority-source`、`pipd-execution-contract`、`pipd-package-project`、`pipd-pd-bind`、`pipd-pi-compile`、`pipd-profile-tailor`、`pipd-route-intake`。
- 所有 enumerated member paths 均未見 `/` 絕對路徑、`../`、反斜線或 `//`；列表未見 MCP/App/Hook 配置檔。
- Source JSON `packaging/public-plugin/plugin.json` 提供 `$schema=https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`、合法 SemVer `0.1.1`、name、description、license、source、vendor schema digest、8 技能結構；相關 CI package tests 綠。
- Receipt `RELEASE_RECEIPT.json` 宣告 56 entries、`LOCAL_PACKAGER_PASS_ONLY`、`official_portal_verification: NOT_EXECUTED`；旁檔 SHA256 宣告 `83e5ce5b4b3ac85e1be4842e16132c5450d2ae6074406a210debdc8a05bb4d87`。**本輪解析的是中央目錄與官方錯誤契約的結構符合性；未執行完整 ZIP inflate/CRC、逐檔 digest／Portal 官方掃描，也未替第三方帳戶上傳，故不能宣稱官方校驗已完整 PASS**。

**封裝 verdict**：`STRUCTURAL_FORMAT_PASS`；`OFFICIAL_PORTAL_VALIDATION_NOT_EXECUTED`；`PRIVATE_IMPORT_NOT_EXECUTED`。此 ZIP 在結構上**可作為私人上傳測試候選**，不需等待公共 listing；但最新 Branch 的逐位元組可發布 ZIP 仍應於下一次 release packaging 產出在明確下載路徑，不依賴 `.hgk/` 深層歷史資料夾。

**最小相容性改善（P2，不阻擋合併）**：`extensions.com.openai.interface` 目前只有 `display_name`（snake_case）。OpenAI 現行 listing field 是 `displayName`（camelCase）。建議在下一次 ZIP 小版本產製前提供官方預期字段／metadata，讓私人頁面顯示正常；不能以此未提供就自稱因 YAML/JSON 完全不相容。若 Portal 直接接受並正常顯示，記 warning 即可。

### 5.3 私人使用與其他表面的真正可行程度

| 路線 | 現在可做 | 仍需一個真實操作才能 `PASS` | Release blocking? |
|---|---|---|---|
| **Web GPT-6，Plugin Creator** | 個人可透過 Creator 建立 Skills-only Plugin；通常本地建立後即可個人使用 | 有資格帳戶建立→在 Personal／Installed 顯示→一次正觸發與負觸發 | **不阻擋 Repo Merge** |
| **Web GPT-6，私人 ZIP 上傳** | ZIP 結構相容；有 Upload 權限的 workspace owner/admin 可試 | UI 真正接受 ZIP→Install→8 Skills discovery＋至少 1 正/負觸發 | **不阻擋 Repo Merge** |
| **Web GPT-6，Knowledge / MD** | Repo `docs/install/PIPD_WEB_FALLBACK.md` 已存在，可單檔掛載 | 手動 mount＋內容讀取／引用；**天花板 `DOC_MOUNT_ONLY`** | 可以當立刻可用的降級路線 |
| **Hermes Agent** | 一段安裝提示詞＋8 技能源碼 | 真實 Hermes 版本/OS 原生 discovery/trigger/uninstall 日誌 | 留下 host-qualified open item |
| **Codex Desktop** | 同一安裝提示詞 | 真實 Codex GUI host discovery/trigger/uninstall | 留下 host-qualified open item |
| **Codex CLI** | 安裝提示詞＋已有局部 UAT 歷史資料 | 最新 SHA 的 host-specific 實際發現、有效載入、負向測試 | 留下 host-qualified open item |
| **OpenAI API `environment.plugins`** | 可另建 `.codex-plugin/plugin.json` 包 | API-specific sandbox ZIP 格式，不等同 Web Portal | **不列入本次 MVP** |

**帳戶限制**：無法在本次唯讀驗收中取得使用者 ChatGPT Web 的 Upload 權限、Workspace role 或私人 Plugin 頁面，因此不能保證每位使用者都看得到 Upload；平台支持的能力≠本帳戶 entitlement。私人 Plugin 的創建／使用並**不必**先申請公開 Directory 審核。

---

## 6. 本次最重要的高 CP 值分流決策

### 6.1 建議現在合併，不再等待多輪「Maker 小瑕疵修補」

**推薦的單次整合操作**：

1. 審核 `main=224591431...`、PR #3 head `759b9f0...`，確認 GitHub 同 SHA 必要 CI check 仍綠，先由授權操作者將 **PR #3** 從 Draft 轉入合併／Reviewer signoff；合併到 `main`。
2. 將 **PR #5** 的原 Stack base 從 Stage A 分支轉向更新後的 `main`（或在 Stage A 正常合併的 Git Graph 上重新確認差異），**只按 Stage B product paths 做 affected check**；若 head 未改，沿用本輪 green raw receipts；之後合併 PR #5。
3. 不以原 PR #2 再推一遍舊 R3；不要把 `Stage B` 在 `Stage A` 之前直接合併。

技術批准理由：原 P0 出口碼與 Write-set 重大缺陷有 **同候選遠端 raw、負向對照與固定來源碼**；Stage A 後 Stage B 為嚴格後繼。未發現新 P0 阻斷。PR #3/#5 `draft` 是行政／流程狀態，不是程式錯誤；需合法 Repo 權限完成操作，但**不要求再開一輪核心程式修補**。

### 6.2 下一版 Preview 發行：只做一次真正 Release Tuple，不擴建治理

**下一個小版本 `preview.4` 或 Owner 合法選定新版本**，絕不可挪用／重貼現有 preview.3 的 Tag／資產，必要之單次 release checklist：

- 固定合併後 `main` **40-hex commit/tree**；封裝 wheel、web mount／fallback、可上傳 Plugin ZIP 的 Build Subject 分別寫清來源及 version，不把歷史 `3233...` 與 release commit 混淆。
- 產出 Manifest SHA-256，獨立 readback 已上傳的 GitHub Release 資產 digest；Wheel 在乾淨 venv `pipd doctor/validate` 的 **Trace wrong hash/orphan negative** 不得 false PASS；ZIP 再驗 8 Skills＋portable manifest＋秘密掃描。
- README 主頁只留**一段**新 Preview 推薦版本與 Download；`docs/install/README.md` 作唯一安裝 SSOT，`docs/USER_GUIDE.md` 作唯一完整手冊；修復「Owner inputs 未提供／Web private plugin 不可用」的過時語句，加入「私人 ZIP 具上傳權限才可使用」說明。
- 產出新版本 Release Notes：明示 `Preview/No full S4 host qualification`，公開 Plugin Directory 仍未發布。保留上一版 readback 與 rollback 指向。

只要四項皆成功，**驗收官建議准予新的 GitHub 開源 MVP Preview 發布**，不必等 GitHub 所有歷史 `.hgk/` 清空、公共 Portal 上架或四 Host UAT 100%。不能把此建議說成有人已上傳或發布。

### 6.3 `TEMP_CLOSED` 的明確邊界

本輪建議將以下項目移到**下一使用者驗收／公開 Plugin 發行階段**：四 Host 完整 8/8 行為覆蓋、所有 OS UX 指標、公共 Portal 審核／Human verified publisher、ZIP metadata cosmetic 欄位、原始歷史證據檔案整理。只要沒有新觀測的危險路徑／假 PASS／重大安全退化，它們不再阻礙原始碼 merge 或**標示 Preview 的有限發行**。

**不允許階段性結案的例外**：CI 再次 False-Green，新的正式發行資產 digest 跟 manifest 不一致，8 Skill 實際少載且被宣稱已載，越權寫入／注入致 S4 自簽 PASS，或新 Wheel Trace false PASS。這些如重現就立刻 `FAIL/REOPEN`，只做 affected-only 修補。

---

## 7. 實作修補之後，現在還高度必要的東西有多少？

| 選項 | 風險／效益 | 本輪強制程度 | 工程判定 |
|---|---|---|---|
| 追加 CI/核心程式邏輯修補 | 已有 592/108 綠與負例 | **不再要求**，除非出現新可重現阻斷 | `STOP_REPAIR` |
| Stage A→Stage B 順序合併 | 直接讓使用者拿到已修的源碼 | **現在必要** | `APPROVE_STAGED_MERGE` |
| 完整重寫 README | 目前已有長 README + 新導航 | 不必要 | 做 1 次版本／入口／限制小 patch 即可 |
| 新增完整使用手冊 | `docs/USER_GUIDE.md` 已存在 | 不必要 | `DONE_AS_DELIVERABLE` |
| Web 單檔備援 | 42,145 bytes MD + sha256 已存在 | 不必要再開發 | `DONE_AS_DELIVERABLE` |
| 私人 Plugin ZIP | 結構具備，未做 Web 真實 Import | **一次**真實帳戶測試 | `ONE_SMOKE_TEST_ONLY` |
| 重新封版 Preview | 目前新程式只在 branches | **下一發行前必要** | `ONE_RELEASE_PACK` |
| 大掃除 `.hgk/`／重寫歷史 | 高風險破壞證據，低即時效益 | **不要** | 只做 release surface 與秘密掃描 |
| 公開 Plugin 上架 | 需要 Portal／真人身分 | 開源 MVP 不依賴 | `DEFER` |
| MCP／Hooks／9th Skill | 無必要用戶需求 | **禁止擴張** | `OUT_OF_SCOPE` |

**MVP 目標函數**：最低操作步驟、可重現原始碼、不中斷安全 invariant、使用者能找到安裝入口、拒絕虛假 PASS。**不是**「將每份歷史報告消除所有文字矛盾」或「在四個 host 上完全相同的功能環境」。

---

## 8. Evidence quality、Negative-first、Gate Calibration

| 檢驗 | Evidence | 是否與結果綁定 |
|---|---|---|
| 重大 P0 CI False-Green | 先前 572/11 failures 假綠（R3 原始 log） vs 新 592 OK＋`pipefail`＋job success | 是；受驗新 SHA `940a37d...` |
| Write-set guard 實驗 | Stage B `WRITE_SET_CLEAN_AGAINST_759b9f...` 且 guard selftest 對 forbidden src/skills/schema/dist 進行 planted negative | 是；新 workflow 與 Job log |
| Trace／provenance 竄改 | 18 tests OK（正）；變更 stamp 的 negative 回傳 `MUTATION_REFUSED_ON_IDENTITY_BINDING` | 是；新 Job |
| Web fallback 內容竄改 | 先成功，後變更成員 digest，typed `REFUSED MANIFEST_DIGEST_MISMATCH` | 是；新 Job |
| wheel install | clean venv 不使用 checkout PYTHONPATH，讀出 package registry 19 families | 是；最新 `ci` 觀測 |
| Plugin ZIP 靜態安全 | 實體 central directory：1 root、56 entries、8 skill、無 `../`／MCP/hook | **歷史 ZIP**；不冒充新 HEAD 當次建構 |
| 完整 OpenAI ZIP 校驗 | 此輪未跑 Portal ZIP scan，也未完整解壓/CRC 驗證 | `NOT_EXECUTED` |
| Web GPT-6 私人安裝 | 無帳戶 UI／組織權限及真實 Upload receipt | `NOT_VERIFIED` |
| Hermes/Codex host-specific | Repo installer spec；真實四 host effective-load 全量不足 | `NOT_VERIFIED` |
| 獨立官資格 | GitHub 原始 Job 再解讀，未進行獨立 clone 重跑；非 official checker bundle | **限定 scoped challenge，不升格 Formal Full PASS** |

**對常見誤判的警告**：`BUILD_PASS`≠`PORTAL_VALIDATED`≠`PRIVATE_INSTALLED`≠`HOST_QUALIFIED`≠`PUBLISHED`≠`S4_FULL_PASS`；`572 red` 是 R3 舊 Commit，不可用來否決新 `592 green`；`no Portal listing` 不等於「私人 ZIP Plugin 根本不存在」；單純 Maker 註明 `NO_MERGE` 不等於獨立驗收官必須永遠拒絕給工程建議。

---

## 9. 具體最小 Issue→Task→Evidence Return 契約

這是**下一步執行者的出入契約**，非此回合已代行的 Repo 操作；不建立多餘 issue 結構。

| 單元 | Earliest Owner | 工作（最大寫入範圍） | 必要返包 | 一次驗收終止條件 |
|---|---|---|---|---|
| `R4-MERGE-A` | Repo Maintainer | PR #3 Draft→main；不額外改核心 | 合併前/後 SHA、CI head/status、merge commit | 同候選 green；成功即可 stop |
| `R4-MERGE-B` | Repo Maintainer | PR #5 base 調整＋合併；**只做 affected-diff** | diff list、PR SHA、both workflows 對應 green、merge commit | Stage B 無新 denied product path；即可 stop |
| `R4-RELEASE-1` | Release Maintainer | 新 preview tag／wheel／Mount ZIP／公開 release files／docs 限定 patch | Release Tuple、SHA256SUMS、asset readback、wheel clean venv＋Trace negative、rollback pointer | 1 次成功即可 release preview |
| `R4-WEB-PRIVATE-1` | 具權限實際用戶／Workspace Admin | 現有 ZIP 或新 Release ZIP 私人 Upload；如無權限改用 Creator | upload receipt／錯誤碼、可見 plugin、8 skills discover、至少 POS/NEG | 已可私用即 stop；受限則 `NOT_AVAILABLE` 而非修產品 |
| `R4-HOST-1` | 各 Host Owner | 依現有單段 prompt 原生 install/discover/trigger/uninstall | 各 Host/OS/version、8/8 與 POS/NEG transcript | 個別 host pass，不影響其他 host 的 Preview 使用 |
| `R4-PUBLIC-1` | Public Plugin Publisher | 新公共 Directory 申請，獨立於 OSS Release | verified identity、Portal submit/check/review、served ZIP digest、publish proof | `PUBLIC_DIRECTORY_PUBLISHED` 才能宣稱公共上架 |

**安全寫入界線**：本報告不授權任何代理繞過 Maker/Checker SoD；必要之 `PR merge`／`tag`／`public Publish` 仍須真實授權維護者在相應平台操作。若有新的發行風險，僅對當次變動設定 TT，而非把舊 R3 形式性 open items 全部重新歸零回頭跑。

---

## 10. 下一版 Preview 的一次性放行／失敗標準（無模糊地帶）

**建議允許 GitHub 開源 Preview 發行的充分條件**（非公共 Directory）**全部同時成立**：

1. 本輪已驗修補真的位於新 `main`；tag 指向那個 commit；來源跟 Tag object／tree 及 release version 一致。
2. 新 Wheel fresh-install 在 Linux 預覽 runner `pipd doctor` 與 Trace false PASS 負例符合預期；不需要再引入新的語義 feature。
3. 新 release artifacts（Wheel、Source、Web fallback/ZIP／如有附 Plugin ZIP）皆由該版宣告的 pinned source 建立、SHA256 readback 跟 GitHub served assets 一致，**不用原地覆寫舊 Tag**。
4. 使用者首頁與唯一安裝 SSOT 指向新 Preview 且明寫 `S4_HOST_QUALIFICATION_PARTIAL`、`PUBLIC_PLUGIN_NOT_PUBLISHED`、Web fallback 天花板；Owner 預覽發行授權存在。

若上述任一條失敗，**僅該 Preview Release Gate `HOLD`**，工程 Merge PASS 不須回滾（除非出現安全 P0）。若四條達成，建議 **`PREVIEW_RELEASE_PASS`**，單輪結案；其他 Portal/全 Host 狀態可標記階段性 `TEMP_CLOSED`。

---

## 11. R4 最終判定（四維度，不混為一個 PASS）

```yaml
report_id: PIPD-S4-EXT-ACCEPT-R4-20261013
repo: https://github.com/shw097-team/PIPD-LS-SP
main_commit: 224591431a164ab72a9423cd180e417e8a762403
stage_a_commit: 759b9f0dc880b2f960363b2ceaa68446c770061d
stage_b_commit: 940a37d00d5c1d12dfc9ae5d2325d8837b08501b
stage_a_scoped_engineering: PASS
stage_b_scoped_engineering: PASS
critical_r3_findings:
  S4R3-F001: REPAIRED_IN_CANDIDATE
  S4R3-F002: REPAIRED_IN_CANDIDATE
merge_recommendation: APPROVE_STAGED_NOW_PR3_THEN_PR5
merge_executed: false
next_github_preview: CONDITIONALLY_APPROVED_ON_ONE_RELEASE_PACK
public_directory: HOLD_SEPARATE_CHANNEL
web_private_plugin_zip: STATIC_FORMAT_PASS_IMPORT_NOT_VERIFIED
web_fallback: DOC_MOUNT_ONLY_READY
hermes_codex_gui_cli_native_hosts: NOT_UNIVERSALLY_VERIFIED
full_s0_s4_acceptance: PARTIAL
this_phase_noncritical_remaining_work: TEMP_CLOSED
repair_more_core_code: NOT_RECOMMENDED_WITHOUT_NEW_P0
user_account_private_upload: NOT_TESTED
human_ratification: NOT_CLAIMED
production_pass: NOT_GRANTED
```

**結論白話版**：**這次可以准予 Stage A＋Stage B 工程合併**，不應再用無限證據細節攔住 MVP；合併順序必須是 PR #3 然後 PR #5。**下一次只做一包可追溯 Preview release，不做下一輪「更大修補」**。ChatGPT Web 私人 Plugin ZIP 的結構已可當測試候選；現在可由有權限的帳戶測試私人上傳，無需等待公開目錄。但**真實 Web 裝載、四 Host 有效載入、公開 Plugin Directory 與正式 S4 Full PASS 均未被實際完成**，僅能作分開的條件性／階段性閉合。

---

## 12. 證據索引（可直接點選並重跑的 URL）

### GitHub frozen subjects／PR

- Stage A PR #3：<https://github.com/shw097-team/PIPD-LS-SP/pull/3>
- Stage B PR #5：<https://github.com/shw097-team/PIPD-LS-SP/pull/5>
- `ci` source：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/.github/workflows/ci.yml>
- `public-plugin-verify` source：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/.github/workflows/public-plugin-verify.yml>
- `plugin.json` portable manifest：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/packaging/public-plugin/plugin.json>
- `README`：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/README.md>
- User Guide：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/docs/USER_GUIDE.md>
- MD fallback：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/docs/install/PIPD_WEB_FALLBACK.md>
- 獨立結構分析的歷史 ZIP：<https://github.com/shw097-team/PIPD-LS-SP/blob/940a37d00d5c1d12dfc9ae5d2325d8837b08501b/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/08_PLUGIN/BUILD_AFTER_SUPPLIES/pipd-ls-sp-public-skills.zip>

### GitHub raw hosted execution

- <https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38407236130> — `ci` SHA `940a37d...`
- <https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38407236156> — `public-plugin-verify` SHA `940a37d...`
- <https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38398212337> — Stage A `ci`
- <https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38398212422> — Stage A `public-plugin-verify`

### Current OpenAI public official documentation, verified 2026-10-13

- <https://help.openai.com/en/articles/20001256-plugins-in-chatgpt> — private plugin / upload permissions / Plugin Creator
- <https://developers.openai.com/plugins/deploy/submission-errors> — ZIP manifests, root constraints, limits
- <https://developers.openai.com/plugins/deploy/submission> — private/public flow, upload/review/publish
- <https://developers.openai.com/plugins/build/plugins> — `.codex-plugin` developer package and paths
- <https://developers.openai.com/api/docs/guides/agents-api/tools/plugins> — API environment.plugins distinct format

### 本地上游基準（物理存在與逐檔 SHA 清冊）

- `/mnt/data/00_KNOW_INDEX.md`…`19_KP_INDEX_CROSSWALK.md`
- `/mnt/data/challenge-review-SKILL.md`
- `/mnt/data/PIPD-LS-SP_PIPD-PKG-00..10`
- `/mnt/data/PIPD-LS-SP_skeleton.md`、`/mnt/data/PIPD_LS_canonical_standard.md`
- `/mnt/data/PIPD_LS_DOC-00..09`
- `/mnt/data/PIPD-LS-SP S4｜三合一小型升級藍圖(1).md`
- `/mnt/data/acceptance_reports/PIPD-LS-SP_S4_R3_三合一升級_外部獨立複驗與MAIN整合裁決_2026-10-13.md`
- `/mnt/data/acceptance_reports/input_inventory_2026-10-13_recheck.json`

**報告結束。** 本報告不在受驗 Repo 寫入；未建立、人為背書、合併、簽章、發行、上架任何資產。唯一接受的法律／帳戶授權仍由相應維護者與 Plugin Portal 控制。
