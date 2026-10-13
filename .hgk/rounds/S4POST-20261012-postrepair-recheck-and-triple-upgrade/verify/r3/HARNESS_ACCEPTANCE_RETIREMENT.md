# ADJ-5 — 自建載具從「驗收依據」退場（CR/TT 轉列）

> 依據：`FAR-OPEN-ITEMS-ADJUDICATION-20261013-001` §2 ADJ-5；owner 於 2026-10-13 裁決並授權執行 FAR 建議。
> 性質：**candidate 記錄**，不構成驗收、不構成批准。

## 1. 退場決定

自本記錄起，**自建 stage-b 驗收載具不再作為任何「通過／不通過」的依據**。它的產出（FCR 系列、守衛列印、lane log）仍保留為**歷史紀錄**，但：

- 不得用來支撐任何 PASS 或 FAIL 的對外主張；
- 不得因它紅燈而再開啟修補輪（**R1 凍結維持**）；
- 任何新發現一律**轉 CR/TT**，不新增 AO 輪次（R8：同回合外部複驗 ≤2 次）。

## 2. 取而代之的閘門（二條，皆為外部可重跑）

| 閘門 | 內容 | 現況 |
|---|---|---|
| **G1 產品 CI** | `.github/workflows/ci.yml`（hosted runner；checkout→安裝→全量套件→聚焦套件→wheel＋乾淨 venv→`pipd doctor`→來源閘門→突變負向校準→上傳 log） | 三支分支 **`ci` = passing**（13 步全 success） |
| **G2 指定獨立車道** | owner 指定：CODEX CLI／checker model `gpt-6.1-sol`（OpenAI OAuth, medium），對**凍結 commit** 驗收 | 已於本輪對 `389d3973…` 執行（見 `verify/r3/AO_VERIFY_SUBJECT_389D3973_gpt-6.1-sol_medium.log`） |

`public-plugin-verify` 仍紅，**照實揭露**（其 base＝`main` 而本主體疊在 Stage-A 之上）；此為 **base 語意**問題，見 `SUBJECT_AND_BASE_DECLARATION.md`。

## 3. CR/TT 轉列

| 原 finding | 轉列 | 處置 |
|---|---|---|
| `FCR-003`（Stage-B 綁定／單一整合候選） | **TT-S4POST-R3-SUBJECT-08** | owner 宣告主體與 base 後關閉 |
| `FCR-004`（containment 邊界副作用：目錄先建後拒） | CR（載具類） | **不在 S4 修**；載具已退場，影響面僅量測工具 |
| `FCR-005`（重開項） | CR（載具類） | 同上 |
| `FCR-006`（wrapper 狀態查詢被視為乾淨＝偽通過類） | CR（載具類） | 同上；閘門已由 G1/G2 取代，偽通過不再能影響對外主張 |
| `FCR-007`（OPEN） | **TT-S4POST-R3-SUBJECT-08** | 與 FCR-003 同源，由主體宣告一併關閉 |
| `FCR-009`（429 被 4xx 正則誤否決＝正向校準失敗） | CR（載具類） | 同上 |
| `FCR-010`（重開項） | CR（載具類） | 同上 |

## 4. 為什麼這不是「關掉紅燈」

紅燈的**數量與位置全部保留可查**（`verify/ao12/FINDINGS.json` 未動）。改變的是**它是否能對外產生效力**：一個自身缺陷邊際不減、且每輪修補都會引入新缺陷的量測工具（本回合成績：findings **6→3→9**，且新缺陷全部落在前一輪修補之內），作為閘門只會**降低**證據強度。真正的閘門因此換成「hosted CI ＋ owner 指定的外部車道」——兩者都不由 maker 控制。
