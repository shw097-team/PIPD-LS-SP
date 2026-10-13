# ADJ-6／ADJ-7 — 治理文件與實作現實的對帳（owner 授權的 erratum 記錄）

> 依據：`FAR-OPEN-ITEMS-ADJUDICATION-20261013-001` §2 ADJ-6、ADJ-7；owner 2026-10-13 裁決並授權執行。
> 性質：**candidate erratum**。**未修改** owner 的藍圖正本（不在寫手授權範圍）；此處只記錄「何者為準、理由、以及下一版應改什麼」。

## 1. `ci.yml` 與 §3.3 deny-set「Actions」的衝突 → **§3.1 為準**

- 事實：裁決 **§3.1 明文批准**「一個最小 GitHub Actions workflow」，且該節位於 §3.3 之後。
- 判定：治理文件**後節優先**，故 `.github/workflows/ci.yml` 的建立**屬已批准動作**；§3.3 的 deny-set 中「Actions」字樣對本變更而言**已被 §3.1 supersede**。
- 附帶事實（實測）：該 workflow **原本從未真正執行過**——`.gitmodules` 缺 URL 的 4 個空目錄 gitlink 使 `actions/checkout` 在第 2 步 `exit 128`，步驟 3–9 全 skip。移除後三支分支才首次取得全綠 13 步。

## 2. §7.7 的 `--require-hashes -r …requirements.lock` → **照寫不可能通過**

- 事實（實測）：已核准的 CI **不使用**該步驟（以 `pyproject.toml` 安裝，唯一依賴為 `jsonschema>=4.0`）；而 `requirements.lock` 檔內自述逐字為
  「NOT HASH-PINNED … `--require-hashes` will therefore NOT work」。
- **追加實測（更強）**：允許集路徑名 `packaging/public-plugin/requirements.lock` 在本受驗主體**根本不存在**——
  `git show 389d3973:packaging/public-plugin/requirements.lock` → `fatal: path … does not exist`。
  即 §7.7 引用的是一個**在產品主體缺席的路徑**（存在的是 repo 根目錄那份未釘雜湊的檔）。
- 判定：此步驟與實作現實**直接衝突**，屬**文件缺陷**。建議下一版二擇一：
  (i) 改寫該步驟為實際執行路徑（`pyproject.toml` ＋ 釘 Python 版本），或 (ii) 由 owner 產出真正 hash-pinned 的 lock 並置於允許集路徑。
- **S4 不新增 hash-pin 工作流**（避免為對齊文件而擴建，見裁決 §0）。

## 3. `tools/*` 5 檔在允許集外 → **在範圍內**

- 理由：§3.1 所批准的最小 CI 必須執行 build／freeze 工具（`tools/build_public_plugin.py`、`tools/freeze_public_plugin_source.py` 等）。批准 CI 即批准其執行所必需的最小工具集。
- **獨立檢查器補正（重要）**：以**宣告基底**重跑守衛**仍然 exit 1**。它產出的拒絕清單（`verify/r3/ao_lane_round2/guard-stacked.log`）顯示拒絕項**恰為 5 項**：`.github/workflows/ci.yml` 以及四筆 `.hgk/rounds/R2-20261009-qualification/**` 的 gitlink 路徑。**不含** `public-plugin-verify.yml`——該檔在守衛的允許集內（第 11 步 `ALLOWED` 正則逐字可見），故紅燈與它無關。
  → 故**不得**把紅燈敘述為「僅因 base 選錯」。正確敘述：frozen-path 寫入＝**NONE**（以宣告基底實測），但該守衛**結構上拒絕**本次獲准新增的 CI 檔與四筆 gitlink 移除，**任何 base 皆紅**。這是守衛允許集與 §3.1 批准之最小 CI 的實質衝突，需在下一版治理文件中解決（本輪不動守衛）。

## 4. `plugin.schema.json` 槽位內容錯位（ADJ-6c）→ **S4 只做文件映射**

- 事實（實測）：官方 vendor schema 實體**存在**於 `packaging/public-plugin/vendor-plugin.schema.json`，且與線上官方文件 **1,805 B／sha256 `0a4aad95…` 逐位元相同**；而允許集路徑名所指向的 `plugin.schema.json` 標題自述為「locally authored subset」。
- 判定：這是**檔名對位**問題，不是「官方 schema 未取得」。改名需同步 builder 常數（屬 code churn），故 **S4 只記錄映射**：

| 允許集路徑名 | 實際內容 | 狀態 |
|---|---|---|
| `packaging/public-plugin/plugin.schema.json` | 本地撰寫的 subset（自述） | 保留；下一變更改名為 `plugin.subset.schema.json` |
| `packaging/public-plugin/vendor-plugin.schema.json` | **官方文件原始位元**（sha256 已與線上比對相符） | 下一變更改名為 `plugin.schema.json` |

## 5. `com.ao3.*` 未審查命名空間（ADJ-7）→ **移出產品受驗範圍**

- 事實（實測）：對**產品主體全樹**掃描 `com.ao3`，命中 **1 檔**，且該檔為**本回合的紀錄文件**（`ACCEPTANCE_RECORD_STAGEB.md`）；`packaging/`、`tools/`、`tests/`、`docs/install/`、`dist/web/` **0 命中**。
- 判定：`CR-EXT-UNREVIEWED` 的標的**不是產品主體**，歸為**載具／格式層 CR**。這不是關閉一個 CR，而是把它歸到正確的標的。
