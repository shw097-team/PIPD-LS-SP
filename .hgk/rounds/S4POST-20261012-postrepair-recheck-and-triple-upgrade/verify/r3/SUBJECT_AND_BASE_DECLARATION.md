# ADJ-1 — 受驗主體與 base 的宣告（解 FCR-003／FCR-007 同源爭點）

> 依據：`FAR-OPEN-ITEMS-ADJUDICATION-20261013-001` §2 ADJ-1；owner 2026-10-13 裁決並授權執行。
> 性質：**宣告記錄**（declaration），不是驗收。守衛程式碼**未修改**。

## 1. 宣告

| 項 | 值 |
|---|---|
| **受驗主體** | 分支 `feat/s4post-triple-upgrade-20261013-r3`，受驗 commit **`389d3973da73e5740f0b4d290bacb92d1e8982f8`**（tree `488d12c1a4bef899f6d38543ab50874d79996e3a`） |
| **宣告 base** | **`52542c3`**（Stage-A 修補完成點，即本升級的疊層基底） |
| **載具支（非產品主體）** | `chore/s4post-verification-harness`；`feat/…-20261012-r2` |
| **`main`** | `224591431a164ab72a9423cd180e417e8a762403` — **未動** |
| **本疊層＝兩個變更** | ① Stage-A 修補（已交付，含 `schemas/`、`src/` 修補）② S4POST 三合一小型升級（本次，**`schemas/` 與 `src/` 寫入 0 檔**） |

## 2. 為什麼不是「改守衛」也不是「rebase onto main」

- **改守衛（放寬 base 語意）**：等於鬆綁一道能抓真問題的檢查，屬治理風險，不採。
- **rebase onto main**：高阻力（需重跑整個疊層的複驗），且**結果不會更乾淨**——Stage-A 的 `schemas/`／`src/` 修補本來就必須在樹上，rebase 只會把同一批寫入換個名字放進同一變更集。
- **宣告 base（本方案）**：零程式碼變更、可回溯、且讓「單一變更一小組寫入」這條規則**在正確的粒度上**成立。

## 3. 量測基礎（可重跑）

以宣告基底 `52542c3` 與產品主體比對，逐檔分類：

| 類別 | 結果 |
|---|---|
| `schemas/**` 寫入 | **0 檔** |
| `src/**` 寫入 | **0 檔** |
| 允許集外寫入 | 4 檔 —— 即當時 4 個無 `.gitmodules` URL 的空目錄 gitlink，**已移除**（移除後 `160000` 計數 = 0） |
| 產品面變更總量 | 126 檔（相對未切分工作樹的 1,239 檔縮減約 90%） |

## 4. `public-plugin-verify` 的紅燈如何被解釋（不隱藏）

該 workflow 的審查 base 是 `main`，因此會把 **Stage-A 的 4 個 frozen-path 寫入**算進本次變更集，報出 `UPGRADE_WROTE_OUTSIDE_ALLOWED_SET` ＋ `UPGRADE_WROTE_FROZEN_PATH`。

**但「這只是 base 選錯造成的」是錯的——獨立檢查器以宣告基底重跑該守衛，仍然 exit 1。** 它產出的拒絕清單（`verify/r3/ao_lane/guard-stacked.txt`）顯示，即使以 `52542c3` 為基底，守衛仍拒絕：

- `.github/workflows/ci.yml`（與 `public-plugin-verify.yml`）——該守衛的拒絕集合把 Actions 檔視為不允許；
- 四個 `.hkq/rounds/R2-20261009-*` 的 gitlink 路徑（本次移除的空目錄項目）。

因此正確的敘述是**兩段式**：(a) 就**frozen-path** 而言，以宣告基底重測 = **NONE 寫入**（可重跑，見 §3 對照與 `FAR_MEASUREMENT_RECEIPTS.json` 的 `ADJ1_write_set`）；(b) 但該守衛**同時**拒絕本次獲准新增的 CI 檔與四筆 gitlink 移除，所以它**無論用哪個 base 都會紅**。這是**守衛允許集與裁決 §3.1 明文批准之最小 CI 之間的實質衝突**，不是 base 選錯——處置見 `DOC_RECONCILIATION_ERRATUM.md`（屬 owner 認可的文件對帳項）。
