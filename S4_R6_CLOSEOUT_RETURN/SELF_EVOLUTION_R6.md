# S4 R6 回合自研究／自學習／自迭代／自進化（受 FABRIC & HGK 治理）

- round: `PIPD-S4-R6-CLOSEOUT-20261016`
- governance: HG-KSEOS = 唯一控制平面；Fabric = 治理契約面；Hermes = 受治理 runner／orchestrator；Codex CLI = tracked writer / checker
- claim ceiling: `LOCAL + PACKAGE`（無 Production、無 `S4_FULL_PASS`、無跨宿主資格）
- 產出時間：2026-10-16（Asia/Taipei）

---

## 1. 自研究（research）— 本回合實際量測到什麼

| # | 研究問題 | 方法（可重跑） | 量測結果 |
|---|---|---|---|
| Q1 | 本交付環境的 compiler 是否真的 BLOCKED？ | 定位同版 bundle 並實際執行四閘門 | **不是 BLOCKED**。指揮薄宣告的 `compiler_verdict_here: PROMPT_COMPILE_BLOCKED` 是**交付環境**（原作者的容器）的狀態，非本機狀態。本機 bundle 齊備，四閘門全 PASS（`lint`/`activation`/`acceptance`/`compile` exit 0）。 |
| Q2 | `preview.4` 的 served 位元組是否仍等於凍結值？ | fresh HTTPS 下載後本地重算 sha256 | 相符：`545e359a…`、68,357 B。此為 R6 因 DNS 不可用而**未能做**的那一步。 |
| Q3 | Release 的伺服文件其 provenance 是否與 tag 自洽？ | 下載 `PIPD_WEB_FALLBACK.md` 並讀其表頭 | **不自洽**（新觀察 `F-R6-08`）：served 文件的表頭寫 `release_id: v0.1.1-preview.3`。served sha 與 repo 內同檔相同，故非傳輸損壞，而是**發行時投影的是上一版的 provenance**。 |
| Q4 | 本機全量測試數是否等於 R6 引用的 CI 數？ | 在候選 HEAD 跑全量 | **不等**：本機 621 passed / 20 skipped / 62 subtests；R6 CI 624 OK / 6 skipped。環境與 skip 集不同，分母不可互換。 |
| Q5 | 車道 pool 的 rank-1 是否等於本回合被授命的分工？ | 讀 `lane-route-slots.candidate.json` 並實探 | **不等**：`VERIFY_SECURITY` rank-1 是 `opencode-go/deepseek-v4.1-flash`，與 EXECUTE **同模型** → 若照 pool 走會違反 SoD。命定的 checker `openai-codex/gpt-6.1-sol` 位於 rank-2，標記 `REACHABLE_VIA_HUMAN_HOME_TRANSPORT`。 |

## 2. 自學習（learning）— 可複用的規則

1. **指揮薄自帶的 verdict 欄位是「產生它的那個環境」的斷言，不是本機事實。** `PROMPT_COMPILE_BLOCKED`
   要先在本機找同版 bundle 實跑再決定；把環境限制當成產品限制會讓整回合空轉。
2. **lane 的 remote-write marker 是 substring 掃描，且片語涵蓋 `publish`。** 任何含 `published` 的
   checker brief 都會被 `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` 擋下。解法不是改寫詞彙規避，而是**在
   brief 內具名本回合已准入的交付類 WorkOrder**（`WO-...` token），讓 gate 的設計條件被真正滿足。
3. **pool ≠ mandate。** 車道 pool 是可達性排序，不是本回合分工；當 mandate 指定的 checker 不在 rank-1，
   必須顯式 `--force-rank` + `--require-arm`，並把「required vs served」寫進收據。**不得**為了讓實測符合
    mandate 去改 registry。
4. **同模型自我查核 = 無 SoD。** 若 writer 與 checker 都由 pool 的 rank-1 服務，該回合的獨立性為零；
   獨立性證據要落在「模型軸」上，而不只是「lane 名稱」上。
5. **本機測試數不能冒充 CI 數。** 分母不同就是不同的證據，只能各自引用。
6. **不可只修被指名的一行。** `F-R6-01` 指名的是一行 `--release-commit`，但同一段落還引用了一個
   **tree 內不存在**的 mount pack；只修指名行會留下一個必然失敗的範例。修復要覆蓋該 identity 的所有欄位。
7. **detector 必須自證非空洞。** 只會 PASS 的檢查沒有證據力；每一條 check 都必須有配對的 mutation
   使其必須 FAIL（本回合 7/7 觸發）。
8. **一個歷史發布的「served 文件」可能帶著上一版的 provenance。** immutable 資產意味著這個瑕疵
   只能在下一次發行修，不能就地覆寫。

## 3. 自迭代（iteration）— 本回合相對前一輪的方法變更

| 前一輪做法 | 本回合做法 | 理由 |
|---|---|---|
| 以 R6 報告的 CI 數字代表本地新改動 | 在候選 HEAD 實跑並分開引用本機數與 CI 數 | 避免以他人分母證成自己的改動 |
| 只重跑既有 helper 作為 checker 證據 | 建立**帶配對 mutation**的 detector，並讓 checker 另行自建對抗案例 | 讓「檢查」本身可被否證 |
| 以 lane 名稱宣告 SoD | 以 `--require-arm` 綁定模型並在收據記 `required vs served` | 讓 SoD 可從收據獨立覆核 |
| 由人手彙整 evidence row | 以產生器從磁碟／API 產物導出計數後落檔 | 消除模板數字與人工漂移 |

## 4. 自進化（evolution）— 建議落地的持久變更

| 目標 | 變更 | 可複用範圍 |
|---|---|---|
| skill `hgk-kanban-and-lane-routing` | 新增：dispatch 前先對 brief 做 marker 預掃；含 `publish`/`push` 等標記者須具名交付類 WorkOrder | 所有跨 lane 交付 |
| skill `hgk-governed-execution` | 新增：pool 與 mandate 分歧時的顯式覆寫程序（`--force-rank` + `--require-arm` + transport 閘門），並在收據記 required/served | 所有 SoD 要求回合 |
| skill `hgk-lifecycle-admission` | 新增：編譯先行規則——薄上的 `PROMPT_COMPILE_BLOCKED` 須先在本機找同版 bundle 實跑否證 | 所有 IMPORT 型指揮薄 |
| 新回合資產 | `r6_doc_identity_check.py`（帶配對 mutation 的文件身分 detector）、`build_evidence_pack.py`（由產物導出計數的證據包產生器） | 後續 docs/identity 守門 |
| OpenSpec | `pipd-s4r6-closeout-doc-identity-and-update-route`（delta spec 三條需求 + 6 個 scenario，`--strict` 有效） | 產品文件契約 |
| FAR | `FAR-20261016-016-pipd-s4r6-closeout-learning` | 治理研究紀錄 |

## 5. 本回合的方法論邊界（誠實揭露）

- 私人 ChatGPT 帳戶 UI 未執行，任何「UI 成功」皆為**歷史**證據沿用，非本回合實測。
- 跨宿主資格、Production、公開目錄皆未授予。
- compiler 產出之 receipt 自帶 `independent_claim`／`production_claim` 欄位，本回合照實引用，未自行升格。
- 本文件為工程自我研究，不是 Owner 裁決。
