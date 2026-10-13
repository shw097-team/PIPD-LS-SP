# FAR — S4POST 三合一小型升級：偏離研究與低阻力方案

- 研究編號：`FAR-S4POST-DEVIATION-20261013-001`
- 受研對象：`feat/s4post-triple-upgrade-20261012-r2`（本地 HEAD 於研究時點）、回合目錄 `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/`
- 方法：三份治理文件逐條抽取（子代理全文抽取：藍圖 314 條、指揮薄＋裁決 171 條）→ 與實作面實際證據逐條比對（git diff 統計、檔案存在性、workflow 內容、bundle 欄位）
- 本報告為 **探索／設計候選**，非驗收；不改變任何 Gate 狀態
- 天花板（不變）：`BUILD_PASS` / `LOCAL_HOST_QUALIFIED` / `PORTAL_APPROVED` / `PUBLISHED` / `PRODUCTION_VERIFIED` / `PIPD_S4_FULL_PASS` **全部未授予**；公開發行閘門 **FAIL-CLOSED / HOLD**

## 0. 一句話結論

> 產品面（三合一 21 檔）**在 allowlist 內且與條文多數吻合**；但本回合 **98.2% 的變更檔是「外部獨立複驗」衍生的自製驗證載具**，而治理文件對此事有**逐字禁令**（裁決 §0 總裁定：*「不批准把 CI、Agentic Harness 或風險系統全面擴建」*）。真正的 12 項外部證據缺口，**12 輪複驗的移動量為 0**——因為它們全部是 owner／外部主體閘，不是載具能修的。

## 1. 逐條偏離矩陣

| # | 文件條文（逐字，附定位） | 實作現況（實測） | 判定 |
|---|---|---|---|
| DEV-01 | 裁決 §0 總裁定：**「總裁定：須做『最小必要修補＋獨立複驗』，不批准把 CI、Agentic Harness 或風險系統全面擴建。」** | 自 Stage-A tip 起 **1,150 變更檔 → 1,129 檔（98.2%）** 在 `.hgk/rounds/**`：准入閘門 `run_lanes_gated.sh`、派遣器 `run_lane.sh`／`run_checker_lane.sh`、三套負向測試（38+52+27＝118 斷言）、12 輪 AO 車道與證據 | **偏離（重大）** |
| DEV-02 | 指揮薄 §7：「**准入順序不可跳**：SourceFreeze／Requirement → TaskSpec → `OROCHI_FACTORY_ORDER.v1` → HGK SharedSpine 原生 **WorkOrder admission** → typed **ExecutionBinding** → deterministic route → **Hermes Kanban**（必要時限權 Swarm）→ Codex writer → local tests → checkpoint」；同節：「Kanban/LLM 摘要不取得權威；HGK admission `REFUSED_BY_LIFECYCLE_STATE` 不是 PASS」 | 本回合以**自製 shell 車道**取代上列控制鏈：無 HGK WorkOrder admission、無 ExecutionBinding、無 Kanban 盤。`KANBAN`／`SWARM`／`GSTACK` 產物在 repo 中**只屬其他回合**（POSTRELEASE-20261011、R10、R11），本回合無自己的 | **偏離（重大）** |
| DEV-03 | 藍圖 INV-01 ONE CHANGESET（**「單一受控 PR」**）＋A42 `minimal write footprint`（§3.3 §5.1）＋BP-023 最小變更檔案樹（13 檔） | 產品面 21 檔**符合** PA-030 allowlist；但同一分支另夾 1,129 檔載具／證據，佔本次 diff **98.2%** | **偏離（中）** |
| DEV-04 | 裁決 §9 Evidence Return Pack 欄位：`schema`,`frozen_subject`,`manifest_sha256`,`release_assets`,`commands`,`host_uat`,`nonmutation`,`independent_checker`,`owner_ratification` | `evidence/EVIDENCE_RETURN_PACK.json` **存在**且具 13 個頂層鍵；**缺 `manifest_sha256`、`release_assets`、`commands`** 三欄 | **部分合規** |
| DEV-05 | 藍圖 INV-10／指揮薄 PA-069（每列需 `checker distinct identity`）／PA-071（外部 Checker 在**獨立隔離 runner** `VERIFY_ONLY`） | 車道身分與 repo 擁有者 SID **不同**（`…-1004` vs `…-1000`）✓，但**逐列未記錄 checker identity 欄位**；且 AO10／AO11／AO12 的證據 root 連**列目錄都被拒**（`ls: Permission denied`、`icacls` 0 processed）→ 定位**對第三方不可重跑** | **偏離（中）** |
| DEV-06 | 裁決 §2：**「絕不可用『原分支上的 PASS』宣告最新版 `main` 或新的發布資產通過；不能直接 merge 修補分支」**；§10 下一合法動作：Owner 先簽**單一整合候選** | 本回合 Stage-B 綁定仍指向 `2fc17c0`／其後 `a5b461c`，**未由 Owner 簽定整合候選**（即 AO12 `FCR-007`／裁決 TT-S4POST-EVIDENCE-06） | **未閉合（owner 閘）** |

## 2. owner／外部主體閘（非 Maker 可解）

藍圖 Appendix B `required_external_evidence` 12 項，**目前 0/12**：
`REAL_VENDOR_SCHEMA`、`SKILLS_REF`、`REAL_CANDIDATE_BUILD`、`SECURITY_SCAN`、`PLUS_UAT`、`FREE_UAT`、`HERMES_UAT`、`CODEX_DESKTOP_UAT`、`CODEX_CLI_UAT`、`CLAUDE_CODE_UAT`、`INDEPENDENT_CHECK`、`HUMAN_PORTAL_PUBLISH`。

對照條文與實測：

| 條文 | 期望 | 實測 |
|---|---|---|
| 裁決 PB-044／PB-057 | 四主機 UAT（Web GPT-6／Hermes／Codex UI／Codex CLI） | 3 `NOT_RUN`、1 `PARTIAL`（現況不變） |
| 裁決 PB-005／PB-034 | 受驗 5 分支＋3 tag 皆 0 `.github/`、Actions runs＝0 | 不變（本分支的 workflow **未經 GitHub 實跑**） |
| 裁決 PB-007／PB-030 | Release `HOLD`；公開 Wheel `e8ca…` `FAIL_CHALLENGE` | 不變 |
| 裁決 PB-039 | `ROUTE_OUT_MINIMAL_CI`：僅批准**一個**最小 read-only workflow | 我方新增 1 個（吻合），但未跑 |
| 藍圖 BP-149 | `packaging/public-plugin/assets/logo.png`、`composer.png`、`requirements.lock` 分別為 `OWNER_BRAND_REQUIRED`／`LOCK_REQUIRED` | **三者皆 MISSING**（設計上就該缺＝owner 輸入） |
| 藍圖 BP-025／BP-149 | `dist/install/PIPD_WEB_FALLBACK.md`（generated, bounded, source stamped） | **不存在**（`REAL_ASSET_NOT_EXECUTED`：產生器在、未對真實來源產出） |

> 上述檔案缺項**不是 Maker 缺陷**——藍圖本身把它們標為 owner 閘/未執行。重點是：**載具修補對它們的邊際貢獻為零。**

## 3. 合規項（可驗證的正面清單，避免只報壞消息）

| 條文 | 驗證方式 | 結果 |
|---|---|---|
| 藍圖 INV-03 ZERO CORE WRITES | 本 changeset 未觸 `skills/**`、`src/**`、根 schemas | **成立** |
| 藍圖 INV-02 ONE SOURCE（8 Skills） | `skills/` 目錄 8 項、未增減 | **成立** |
| 藍圖 INV-06 MCP/Apps/Actions/Hooks OFF | 未新增 backend／MCP／輪詢工具 | **成立** |
| 藍圖 INV-07／指揮薄 PA-028 FAIL-CLOSED EVIDENCE | 12 輪從未把 `BUILD_PASS`／`PUBLISHED` 升格 | **成立** |
| 裁決 PB-034／PB-050 最小 CI 規格 | 實讀 `public-plugin-verify.yml`：含 `contents: read`、**無** `pull_request_target`、checkout 釘 `11bd71901b…`、有 `python-version`、有 `unittest` | **吻合條文** |
| 指揮薄 PA-075 終止產物 | `ROUND_RESULT.md`＝`# S4POST_AND_UPGRADE_RESULT`，§1–§12 含 gate／未閉合／終止狀態 | **已存在** |
| 指揮薄 PA-007／PA-033 禁則 | 未推 `main`、未 force、未動 tag、未 merge；每次 push 後遠端 SHA 回讀＝本地 HEAD | **成立** |
| 指揮薄 PA-060 憑證 | token 由 GIT_ASKPASS helper 讀取、未 echo、未入 log／commit／remote | **成立** |
| 藍圖 §3.3 最小樹 | 13/13 產品檔路徑存在（除三個 owner 閘檔） | **成立** |

## 4. 低阻力最佳工程方案（R1–R8）

排序＝投報率；每項標「成本／風險／依據」。

| ID | 動作 | 成本 | 風險 | 依據 | 可驗收證據 |
|---|---|---|---|---|---|
| **R2**（最高） | **把驗證載具切出 S4 changeset**：新分支 `chore/s4post-verification-harness` 承載 `.hgk/rounds/**` 載具與 AO 證據；S4 PR 分支只留 21 檔產品面＋`ROUND_RESULT.md`／`EVIDENCE_RETURN_PACK.json` 作指標 | 一次 rebase（低） | 低（需 owner 許可改分支拓撲） | 藍圖 INV-01＋A42；裁決 PB-008 | `git diff --name-only <base>..<s4>` 僅 21–23 檔 |
| **R3** | **補 Evidence Return Pack 三欄**：`manifest_sha256`、`release_assets`（未下載者**保留欄位**填 `NOT_EXECUTED`）、`commands` | 0.5 h | 無 | 裁決 PB-090、PB-091（樣例填值≠實測） | 欄位齊備且未跑者標 `NOT_EXECUTED` |
| **R4** | **12 項外部缺口升為一封 owner 行動請求** `OWNER_ACTION_REQUEST.md`：4 項 owner 輸入（PNG×2、`requirements.lock`、derivations 核准）、Publisher 身分、四主機 UAT 窗口、**單一整合候選簽定** | 1 h | 無 | 裁決 PB-096；藍圖 BP-148 | 一份可勾選清單，指向 `OWNER_INPUT_REQUIRED.json` |
| **R5** | **開 Draft PR 讓最小 CI 真的跑**（workflow 已在分支上，權限最小、SHA 已釘） | 低（憑證已具） | 低；GitHub 端紅燈＝新資訊，不影響本地已驗項 | 指揮薄 PA-062；裁決 PB-005／PB-034 | Actions run 的 checkrun＋raw log／exit code |
| **R6** | **修車道證據 ACL**：車道退出前把證據打包進 repo 可讀位置（或放行 ACL） | 3 行 | 無 | 裁決 PA-069／PA-071 | 第三方可讀＝同一路徑可重跑 |
| **R7** | **SoD 身分欄位化**：每列 EvidenceRow 加 `producer_identity`／`checker_identity`（兩者 SID 已不同，只差記錄） | 0.5 h | 無 | 藍圖 INV-10、指揮薄 PA-069 | 逐列具名，不再只有程序聲明 |
| **R1** | **凍結載具、停止擴建**：`.hgk/rounds/.../verify/**` 與三套負向測試宣告 frozen；**不再派遣 AO13**；不再新增軸；殘餘 finding 轉 CR／TT | 0 | 無 | 裁決 PB-008 逐字 | 新增 commit 數＝0；AO 車道不再啟動 |
| **R8** | **AO 迴圈上限制度化**：同一 round 至多 2 輪外部複驗，其後 finding 一律轉 CR／TT | 0 | 無 | 裁決 PB-008；AO10／11／12 邊際 finding 已降為 bounded／positive-calibration／INFO | 寫入 skill 或回合政策檔 |

### 4.1 建議執行序

1. **R1（立即，0 成本）** → 停止無界迴圈。
2. **R3＋R4（1.5 h，零風險）** → 把交付表面補齊、把缺口交還 owner。
3. **R2（一次 rebase，需 owner 許可）** → 恢復 ONE CHANGESET／最小足跡。
4. **R5（開 Draft PR）** → 讓唯一可自行取得的外部證據（CI checkrun）落地。
5. **R6＋R7（半天）** → 讓後續任何外部驗收官真的可用。

### 4.2 我建議**不要**做（逐字對齊禁則）

- 不再新增驗證軸、不做「全模型 × 所有提供者 × 所有 OS 的暴力矩陣」（裁決 PB-086）
- 不導入第二套 CI 服務、不做 12 軸自動風險裁定器、不強制 SemVer、不進 S5–S8（裁決 PB-040／PB-086、指揮薄 PA-026）
- 不新增第九 Skill／第 20 schema family／第 14 CLI（PA-026）
- 不自行 merge／發 tag／發布／替換已發布資產（PA-033、裁決 PB-029）

## 5. 需 owner 裁決（本報告不代答）

1. `FAR-S4POST-MODEL-DEVIATION-20261012-001` 的 `not_applied: Research only`：宣告 EXECUTE 模型是否需補跑，或接受為 owner-approved 偏差（載具閘已可強制四軸）。
2. 本回合 Stage-B 綁定的「單一整合候選」由誰簽（裁決 PB-096）——這同時是 AO12 `FCR-007`。
3. 驗證載具是否依 R2 切出分支；若 owner 選擇保留在同一 PR，則 A42 的判定維持 `DESIGN_CANDIDATE` 並需 owner 明示接受。

## 6. 誠實的邊際價值判讀

12 輪外部複驗的 finding 序列 6 → 3 → 9，**每一輪都在我的載具裡找到新缺陷**（含我自己上一輪才加的 429 否決、紀錄範圍主張）。這證明載具品質在提升，但也證明：**這條迴圈收斂的對象是「我自己造的載具」，不是治理文件要求的目標**。在 R1 生效前，第 13 輪的可預期產出仍是「載具的新缺陷」，而 12 項外部證據缺口的移動量仍會是 0。
