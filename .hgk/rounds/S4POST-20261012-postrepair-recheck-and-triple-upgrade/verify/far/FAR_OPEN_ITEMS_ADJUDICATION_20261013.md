# FAR — 未閉合與待裁決項目：裁決建議與執行方案

- **研究編號**：`FAR-OPEN-ITEMS-ADJUDICATION-20261013-001`
- **性質**：決策研究（candidate 文件）— **非驗收、非 PASS、非批准**
- **範圍**：只涵蓋「需要裁決」或「仍未閉合」的項目；已完成者不重述
- **方法**：每一條建議都先有**今日實測**的事實基礎（探測輸出見各條「基礎」欄），再給建議、阻力、必要性
- **判準**（依裁決 §0／§8 逐字）：低阻力、高度工程必要性、**不過度工程化**

---

## 1. 結論摘要（一句一項）

| ID | 待決事項 | 建議裁決 | 誰 | 阻力 | 必要性 |
|---|---|---|---|---|---|
| ADJ-1 | 受驗主體與其 base（＝FCR-007 同源） | 主體＝**產品支 vs 宣告疊層基底 `52542c3`**；疊層記為**兩個變更**；**不動守衛**，只把 base 寫進 PR／記錄 | Owner 一行 | 極低 | **高** |
| ADJ-2 | 單一整合候選由誰簽 | Owner 以**既有機制**簽一筆 10 行 JSON（commit＋tree＋仍缺供給） | Owner | 極低 | **高** |
| ADJ-3 | 宣告模型 vs 實際路線之偏差 | **記錄，不修**（逐車道路線已記、SoD 身分層已成立） | Owner 認可 | 零 | 中 |
| ADJ-4 | `R3.VERIFY-007` 指定車道未跑 | **跑一次**、scoped、**裁決照刊（含 FAIL）** | Agent 執行 | 低 | **高** |
| ADJ-5 | 載具缺陷 FCR-003/004/005/006/009/010 | **凍結維持**；轉 CR/TT；**把自建載具移出「驗收依據」**，改用 CI＋指定車道 | Agent＋Owner 認可 | 零 | **最高** |
| ADJ-6 | §3.3 允許集／deny-set 四項張力 | (a)(d) **明文 supersession 記錄**；(b) 在範圍內；(c) **S4 只做文件映射**，改名留待下輪 | Owner 認可 | 極低 | 中高 |
| ADJ-7 | `com.ao3.*` 未審查命名空間 | **移出產品受驗範圍**（產品面 0 命中） | CR owner | 零 | 中 |
| ADJ-8 | TT 登記簿陳舊（CI-04 仍 OPEN） | **更正狀態**（同欄位，不改 schema）— 已於本輪執行 | Agent | 零 | 低 |

---

## 2. 逐項建議與基礎

### ADJ-1 受驗主體與其 base（連帶解 FCR-007）
- **基礎（今日實測）**：以宣告疊層基底 `52542c3` 比對本升級，`schemas/`＋`src/` 寫入 = **0 檔**、允許集外僅 4 檔（即當時那 4 個無 `.gitmodules` 的 gitlink，**已移除**）；以 `main` 為 base 比對才會計入 Stage-A 的 4 個 frozen-path 寫入。`public-plugin-verify` 紅即源於此 base 選擇。
- **建議**：受驗主體＝產品支 `feat/s4post-triple-upgrade-20261013-r3`，**base 宣告為 `52542c3`**；並把本疊層明文化為**兩個變更**（Stage-A 修補＝已交付；S4POST 升級＝本次）。守衛語意**不改**（改守衛＝鬆綁風險），紅燈保留並在 PR／記錄中說明。
- **不做**：rebase onto `main`（高阻力，且仍會把 Stage-A 的 schema/src 修補納入同一變更集）、改 `public-plugin-verify` 的 base 邏輯。

### ADJ-2 單一整合候選簽署
- **基礎**：`OWNER_INPUT_REQUIRED.json`＋`plugin.release.json` 已提供 owner 供給的機制與模板；缺的不是格式而是**簽署動作**。裁決 §10 明文「最早 Owner = Repo/Release Owner，先簽定單一整合候選」。
- **建議**：owner 簽一筆最小記錄：`{commit, tree, signed_at, supplies_still_missing:[A1..A4], note}`，放在既有 `evidence/10_OWNER/`。**不新增 CLI、不新增格式**。

### ADJ-3 模型偏差（D1）
- **基礎**：每一條車道都記錄了 route；SoD 以**不同 SID** 成立（producer `…-1000`／checker `…-1004`）。偏差屬**申報欄位**性質。
- **建議**：**記錄為 owner-approved deviation**，寫入證據包 `sod`／裁決區塊。
- **不做**：把 `deepseek-v4.1-flash` 加入 `opencode-go.preserveReasoningContentModels`＋on-wire replay——未授權，且 S4 不需要（屬 S5+ 或供應方層級）。

### ADJ-4 指定車道（R3.VERIFY-007）
- **基礎**：owner 逐字指定「Independent Acceptance Officer／VERIFY／SECURITY，轉交 CODEX CLI，checker model：GPT 6.1 SOL-MEDIUM」；該車道尚未執行，是本輪**唯一未閉合**義務。
- **建議**：對已凍結主體**跑一次**、範圍明確、**裁決照刊（可能是 `FAIL_CHALLENGE`）**；依 R8「同回合外部複驗至多 2 次」。若 FAIL，finding 一律轉 CR/TT，**不重開載具**。

### ADJ-5 載具缺陷（最重要的「不過度工程化」建議）
- **基礎**：findings 序列 **6 → 3 → 9**（不收斂），且**每一輪的新缺陷都落在我自己前一輪的修補裡**；同時，真正的外部產出（CI 首次實跑、資產下載讀回、C1 schema 比對）都不是靠載具修出來的。裁決 §0 逐字：「**不批准把 CI、Agentic Harness 或風險系統全面擴建**」。
- **建議**：①凍結維持（不再擴軸、不派 AO13）；②FCR-003/004/005/006/009/010 轉 CR/TT；③**把自建載具移出「驗收依據」的角色**——驗收改以**產品 CI（現已 hosted 全綠）**＋**指定車道**為閘門。
- **理由**：載具缺陷的修補邊際價值趨近於零（修好的是量測工具，不是產品），而每輪修補都會製造新缺陷。把閘門換成「產品 CI＋外部車道」既提升證據強度，也終止迴圈。

### ADJ-6 §3.3 允許集／deny-set 四項張力
- (a) **第二個 workflow `ci.yml`**：裁決 §3.1 **明文批准**一個最小 Actions workflow，其位置在 §3.3 之後 → **後者為準（supersession）**，記錄即可，不刪 workflow。
- (b) **`tools/*` 5 檔在允許集外**：該 CI 執行所需（build/freeze），屬**在範圍內**。
- (c) **`plugin.schema.json` 槽位內容錯位**：官方 vendor schema 實體**存在**於 `vendor-plugin.schema.json` 且**與線上官方文件 byte 相同**（見 §3 C1）→ 那是**檔名對位**問題。S4 建議：**只做文件映射＋TT**；改名留待下一次變更（改名需同步 builder 常數，屬 code churn）。
- (d) **`requirements.lock`**：已核准的 CI **完全不用它**（用 `pyproject.toml`），且根目錄那份自述「NOT HASH-PINNED…`--require-hashes` will NOT work」→ §7.7 的步驟**照寫不可能通過**。建議：**改 §7.7 文字**（文件 erratum），或把 `LOCK_REQUIRED` 留作 owner 輸入；兩者選一，不要為此新增 hash-pin 工作流。

### ADJ-7 `com.ao3.*`（CR-EXT-UNREVIEWED）
- **基礎**：產品支全樹掃描，`com.ao3` 僅出現於**本回合一份紀錄文件**，`packaging/`、`tools/`、`tests/`、`docs/install/`、`dist/web/` **0 命中**。
- **建議**：**移出產品受驗範圍**，保留為載具／格式 CR。這不是「關掉一個 CR」，而是把它歸到正確的標的。

### ADJ-8 TT 登記簿陳舊
- **基礎**：`00_plan/TT_S4POST_REGISTER.tsv` 的 `TT-S4POST-CI-04` 仍 `OPEN`，但 CI 已 hosted 全綠；登記簿缺本輪新增事項。
- **建議**：同欄位更新狀態＋追加 7 列（本輪已執行）。

---

## 3. 12 項外部證據的重新分類（今日新事實）

| 類 | 項目 | 依據 |
|---|---|---|
| **已可收斂（agent，本輪已做）** | `C1 REAL_VENDOR_SCHEMA` | 官方 URL 200、1,805 B、sha256 `0a4aad95…` **＝樹內 `vendor-plugin.schema.json`**（逐位元相同）。**只剩 A2 的 digest 釘選**屬 owner |
| **agent 可嘗試（有界）** | `C4 SECURITY_SCAN`（工具可用性待探）、`C7 HERMES_UAT`、`C9 CODEX_CLI_UAT`（已 PARTIAL）、`C10 CLAUDE_CODE_UAT`（若已安裝）、`C11 INDEPENDENT_CHECK`（＝ADJ-4） | 主機／工具在本機可得性不同，逐項需先探測；**能做則做，不能則記 NOT_SUPPORTED** |
| **owner 嚴格必要** | `C3 REAL_CANDIDATE_BUILD`（需 A1–A4）、`C5/C6 PLUS/FREE_UAT`（帳號）、`C8 CODEX_DESKTOP_UAT`、`C12 HUMAN_PORTAL_PUBLISH` | 需要 owner 的帳號／身分／簽核 |
| **明確不建議做** | 全模型×全 provider×全 OS 矩陣、第二套 CI、12 軸風險裁定器、為對齊而簽第二個 tag、S5–S8 提前 | 逐字對齊裁決 §8「立即不批准」 |

---

## 4. 執行方案（依阻力排序）

| 序 | 動作 | 成本 | 可逆 | 誰 |
|---|---|---|---|---|
| **R-1** | `C1` 存證落盤、TT 登記簿更正與擴充、本報告落盤並推送 | 已完成（本輪） | 完全可逆 | agent |
| **R-2** | ADJ-4：跑指定車道**一次**，裁決照刊 | 一個車道回合 | 可逆（純讀） | agent（需你一句 go） |
| **R-3** | ADJ-1/2/3：你各一行即可解鎖（base 宣告、簽候選、接受模型偏差記錄） | 3 行 | 可逆 | owner |
| **R-4** | ADJ-6(a)(d)：supersession 與 §7.7 文字 erratum | 2 段文字 | 可逆 | owner 認可 |
| **R-5** | （下一變更）schema 槽位改名、lock hash-pin、載具 CR 的正式處置 | 下一輪 | — | 下一輪 |

**建議執行序**：R-1（已完成）→ R-2 → R-3 → R-4 → R-5。

---

## 5. 宣稱天花板（未變）

`BUILD_PASS`／`LOCAL_HOST_QUALIFIED`／`PORTAL_APPROVED`／`PUBLISHED`／`PRODUCTION_VERIFIED`／`PIPD_S4_FULL_PASS`
**全部 NOT GRANTED**；發行閘門 **`FAIL-CLOSED / HOLD`**；獨立驗收最近裁決仍 **`FAIL_CHALLENGE`**（AO12）。
本報告為 maker 研究，**不構成**任何驗收、批准或發布。
