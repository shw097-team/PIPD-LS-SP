# HARNESS FREEZE + AO LOOP CAP（FAR R1 / R8）

- 性質：回合**政策宣告**（candidate-side policy artifact），非驗收、非 PASS
- 依據（逐字）：
  - 裁決 §0 總裁定：「**總裁定：須做「最小必要修補＋獨立複驗」，不批准把 CI、Agentic Harness 或風險系統全面擴建。**」
  - 裁決 §10 下一合法動作：「最早 Owner = **Repo/Release Owner**，先簽定一個…**單一整合候選**…CI 與真 Host UAT 隨後走兩條輕量證據路線」
  - 藍圖 A42 `minimal write footprint`＝`DESIGN_CANDIDATE`；INV-01 ONE CHANGESET（單一受控 PR）

## R1 — 驗證載具凍結（自本檔生效）

生效後，**本回合不再**：

1. 新增或擴充驗證軸（現有已演練軸：model／provider／effort／route 四軸；不再加第五軸）。
2. 派遣新的外部複驗車道（**不再派 AO13**）。AO10／AO11／AO12 的 finding 已降為 bounded／
   positive-calibration／INFO 級，且其餘阻斷**全部**屬 owner 閘（見 `OWNER_ACTION_REQUEST.md`）。
3. 以「再修一版載具」回應新 finding。新 finding 一律轉 CR／TT 登記，不在本回合修。

**凍結範圍**：`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/harness/**`、
`run_lane.sh`（載具分支 `stage-b` 內）、`run_lanes_gated.sh`（載具分支 `stage-b` 內）、`run_checker_lane.sh`（載具分支 `stage-b` 內）。

**例外（本回合最後一次載具編輯，明示且可查）**：FAR **R6／R7** 兩項證據管路修正（證據可讀性＋SoD 逐列身分）。
它們是「讓第三方能重跑現有定位」的必要修正，不是新軸；兩者落地後凍結立即生效。凍結生效的 commit 記於本回合 commit。

## R8 — 外部複驗輪數上限（制度化）

- 規則：同一 round 的**外部複驗至多 2 輪**；第 3 輪起，任何 finding 一律**登記為 CR／TT**（帶 owner 類別與
  反例定位），不得再以「載具修補 → 再複驗」的方式在同一 round 內閉環。
- 理由（可查證）：本回合 12 輪複驗的 finding 序列為 6 → 3 → 9，**每一輪都能在自己的載具裡找到新缺陷**
  （含上一輪才加入的 `HTTP 4xx` 429 否決、紀錄範圍主張）——收斂對象是載具，不是治理文件要求的目標；
  而 12 項外部證據缺口的移動量為 **0**。
- 仍**不是**放棄驗收：獨立複驗照做，但對**凍結候選**做，且以「本輪宣告的 scope」為限（裁決 PB-084：
  `PASS_CHALLENGE` 僅針對 declared scope）。

## 已知未閉合（不因凍結而消失，逐項指向其 owner）

| 項目 | 狀態 | Owner |
|---|---|---|
| `FCR-007` / `TT-S4POST-EVIDENCE-06`（Stage-B 綁定未由 owner 簽定） | OPEN | Repo/Release Owner |
| `CR-IDENTITY-BIND`（官方 manifest name/version 未與發行簿記身分綁定） | OPEN | Owner |
| `CR-EXT-UNREVIEWED`（未經審查的 opaque extension namespace 被接受） | OPEN | Owner／Security |
| 四主機 UAT、Portal、SECURITY_SCAN、真實 candidate build | NOT_EXECUTED | 各自 owner（見 `OWNER_ACTION_REQUEST.md` C 表） |
| AO10 `FCR-001..006`（載具軸向缺陷） | 已修並以 G14a–e／G15／G16／G17／A4–A6 覆蓋（118 斷言） | Maker（本回合止） |

## 誠實邊界

凍結是**本回合的自我約束**，其效力來自 owner 是否接受；它不是 HGK admission，也不是外部驗收。
若 owner 要求恢復載具延展，須以新的 owner 指令解除本檔，並在同一 commit 記錄解除理由與範圍。
