# FAR 第二輪：四項 owner 未關項的研究與裁決建議

**Request:** `FAR-PIPD-S4EXT-OWNER-OPEN-002` ｜ **主體:** S4EXT-R1 輪結束時刻意交還 owner 的四項
**裁決者:** Hermes 受治理編排者（PLAN 車道） ｜ **反方:** `deleg_7ba46965`（fresh-context、read-only）

> 本文件是研究與裁決**建議**。它不重開驗收官 `PASS_CHALLENGE` 的裁定、不抬升任何 claim ceiling、不宣稱發行或生產狀態，且**未改動任何 tracked 證據位元組、seal 或已發布 digest**。

---

## 一、這一輪先修正了我自己的草案

反方推翻了草案的三根支柱；我逐項獨立複算後**全部採納**。這是本輪最重要的產出：

| 草案主張 | 反方 | 我的獨立複算 | 結論 |
|---|---|---|---|
| 「6 筆 digest 在任何單一 revision 都解釋不了，manifest 混雜 ≥3 個 revision」 | **FALSIFIED** | 加上 CRLF 基準後 **UNEXPLAINED = 0**（`disk 1041 + blob@cand 38 + CRLF(blob@cand) 5 + CRLF(disk) 1`） | **撤回** |
| 「14 檔非祖先、含 `f541c396`」 | **FALSIFIED** | 實為 **21 檔／3 個 sibling 頭**；`f541c396` **是** HEAD 與 main 的祖先 | **更正** |
| 「把不變式改成 resolves-only」 | **FALSIFIED** | 該工具**本就** report-only（改動是 no-op）；唯一硬約束 T4 **現正通過**，改它＝降級 | **否決** |

我的錯在**基準取錯**：我只測了「磁碟內容正規化為 LF」，而 manifest 實際雜湊的是**封印當下的工作樹位元組**（CRLF；且有一個檔當時尚未提交，5 分鐘後才入 `846f5ee`）。因此那 44 筆**全部**由「seal 的 as-of ＋ 行尾基準」解釋，**沒有任何一筆是真漂移**。

---

## 二、四項裁決建議（低阻力 & 高工程必要性）

### TT-020／TT-021｜digest 校驗 → **ADOPT `F-020-A-BASIS` + 文件性 `F-020-B-SEAL-SEMANTICS`**

**現況缺陷不是「44 筆過期」，而是「警報無法區分三種完全不同的情況」**：良性 epoch 漂移、行尾差異、與證據檔被替換，在讀者眼前長得一模一樣；而 `crosswalk_digest` 又直接折入這些未重算的值。

- **改法**：讓驗證器**具基準感知**（五基準：工作樹位元組／sealed candidate 的 blob／該 blob 的 CRLF 形／工作樹 CRLF 形／工作樹 LF 形），逐筆歸類為 `MATCH_WORKTREE`／`EXPLAINED_AT_SEALED_CANDIDATE`／`EXPLAINED_BY_EOL_BASIS`／`UNEXPLAINED_DRIFT`；`--strict` **只在 `UNEXPLAINED_DRIFT > 0`** 失敗。順修 docstring 的過時數字（41 → 44）。
- **今日實測效果**：44 筆 stale → **0 筆未解釋**。
- **阻力 LOW**：只動一個工具檔＋測試；manifest、seal、`crosswalk_digest` **全不動**，故無消費者需重新對帳。
- **必要性 HIGH**：讓警報**只代表一件事**。
- **否決**：re-seal（下一個 commit 就再度過期；且改動 tracked 檔、seal sha 與 `crosswalk_digest`，四個消費者正是對著那些位元組對帳）；修剪條目（摧毀快照完整性）。
- **文件性修正**：seal 的 `candidate` 命名的是**封印當下的工作樹狀態**（HEAD `f541c396` ＋ 一個未提交檔、工作樹 CRLF），不是精確的 commit 快照——1 筆條目比該 commit 晚約 5 分鐘。

### TT-024｜非祖先的 `candidate_head` → **ADOPT `F-024-A-KEEP-REPORT-ONLY`**

- **事實更正**：**21/56**（非 14）非祖先，全屬 **r2/r3 兄弟線**（`7c5bc585×8`、`10cb3d31×5`、`db229911×8`，皆 2026-10-09）＝**跨線生成識別，屬已知類別、非缺陷**。
- **改法**：不變式**維持 report-only**（現狀）；更正標籤與敘述；**保留** T4（唯一硬約束，且它通過）；若日後要更強訊號，用**嚴格更強**的 report-only 檢查：**「記錄的 revision 可解析，且其樹在該路徑上含該位元組」**（生成可重現性）。
- **阻力 LOW／必要性 MEDIUM**：移除一類假警報，且不削弱唯一被強制的斷言。
- **否決**：resolves-only（嚴格更弱，連「樹裡沒有該路徑」的 commit 都接受）；把 ancestry 全面改為致命（會否決 21 筆正當識別，且任何 rebase／squash／shallow clone 都會誤殺）。

### TT-023｜EXECUTE 車道 → **ADOPT `F-023-A-PROBE-AND-RECORD`**

- **事實**：宣示模型在本機 adapter 下**第一輪工具呼叫後即 400**（`reasoning_content`），且**乾淨失敗、不留半成品**；catalog **不提供**可用旗標（deepseek 各條目皆空）→ 資格**只能實測**。
- **改法**：長跑前先做**兩輪工具呼叫探針**並把 `model_eligibility_probe` 寫入車道收據；車道 config 釘住已驗證模型；**declared vs actual 一律成欄記錄**（既有做法正式化）；adapter 缺陷（須回傳 `reasoning_content`）**上報外部 owner**。
- **阻力 LOW／必要性 HIGH**：每次未預測的失敗都耗掉一整趟 writer run，並**誘發靜默替換**。
- **否決**：改 EXECUTE 模型家族（改動宣示 SoD，且在 sibling 可用時無必要）；在本 repo 修 adapter（對外部契約的無主 fork）。

---

## 三、淨規則變動 = **0**

四項採納項**全部**是 report-only 增補或文件更正：**沒有任何 tracked 證據位元組、seal、已發布 digest 或驗收規則被改動，也沒有任何規則被放寬**。沿用上一輪原則：**改工具、不打折規則**；並新增一條：**警報必須只代表一件事**——若一個檢查分不出「良性 epoch 漂移」與「真實損毀」，**有缺陷的是檢查，不是資料**。

## 四、請 owner 裁定

1. 追認 `F-020-A-BASIS` ＋ `F-020-B-SEAL-SEMANTICS`（TT-020／TT-021）
2. 追認 `F-024-A-KEEP-REPORT-ONLY`（TT-024）
3. 追認 `F-023-A-PROBE-AND-RECORD`，並把 adapter 缺陷轉外部（TT-023）

**實作註記**：三項採納都是**有界 writer 工作**（一個工具檔、一段 docstring、一份 schema/reader 註記）。本**研究未執行**它們——任何實作都會**依構造作廢**現行的驗收收據，故須自成一個 commit 並重跑獨立驗收。

## 五、揭露的殘餘風險

- CRLF／工作樹的解讀是對 44 筆殘差**最佳擬合**的解釋，**非已證事實**（無封印當下的工作樹存檔可查）。
- adapter 上報在 owner 回覆前**沒有 in-repo 證據路徑**；期間車道必須維持「替代並宣告」。
- 沒有任何消費者重算逐筆 digest（反方 F8），故「更正後沒人會發現」的正確說法是 **none known**，不是 **none**。
