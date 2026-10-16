# 回合任務執行清單 (TASK_CHECKLIST)

**Round**：`PIPD-REPO-HYGIENE-AND-HANDOVER-20261016`｜**紀律**：證據 commit 前必須回填；殘留 `[ ]` = 缺陷。
**狀態碼**：`[ ]` 未開始／`[~]` 進行中／`[x]` 完成／`[-]` NOT_RUN／`[D]` DEFERRED

## Part A — 執行任務（對映 FAR 裁決 execution_plan）

- [x] `T-01` **E0** HGK typed admission（唯一控制平面；不建第二控制平面）
- [x] `T-02` **E0** GSTACK named-method route check（ACTIVE_SELECTED ＋ `route(flow)` ＋ 負向對照）
- [x] `T-03` **E0** OPENSPEC change 建立並 `validate --strict` 通過
- [x] `T-04` **E0** KANBAN gate DAG（E0–E7 依賴鏈）
- [x] `T-05` **E1（R2）** 回收 12 個可還原 worktree（guard：`dirty==0` 且尖端在 origin；使用中者排除）
- [x] `T-06` **E2（R3）** 救援主 clone 6 個未提交檔（新分支 `rescue/r5p-uncommitted-20261016`；不 push、不動原分支）
- [x] `T-07` **E3（R4/R5）** 刪可重生 `_scratch`；`.gitignore` 止漏（僅在可證單一安全前綴時）
- [x] `T-08` **E4（R6）** docs-only 分支：README current-state 節刷新 ＋ 過期車道列更正
- [x] `T-09` **E4（R8）** `ADR-0008` 就地更新（本地衛生清冊）
- [x] `T-10` **E4（R8）** `ADR-0009` 就地更新（SESSION 結案／移交、open TT、rollback、下一步）
- [x] `T-11` **E4** 本地 `_handover` 回合索引（15 目錄 → 1 索引；**不入 repo**）
- [x] `T-12` **E5** 證據包（六件具名＋單一對外 MD）＋ shipped-bytes 清冊 ＋ fresh-extract 自驗
- [x] `T-13` **E5** push 證據分支（唯一遠端寫入）＋ 遠端尖端回讀
- [x] `T-14` **E6** VERIFY 車道（Codex CLI）對凍結封包獨立複驗；裁決逐字入包
- [x] `T-15` **E6** 自檢測／自修補／自驗收：五類反證搜尋 ＋ 缺陷自掃（含自犯缺陷）
- [x] `T-16` **E7** 受 FABRIC & HGK 治理自研究／自學習／自迭代／自進化（FAR-021 五件＋skill＋memory）
- [x] `T-17` Owner 交還包：`OWNER_ACTION_REQUIRED`（docs-only 分支 merge、`.gitignore` 規則是否採用、主 clone 是否切回 main）
- [x] `T-18` SWARM：以子代理並行分擔可離線計算的比對工作（配額耗盡時即刻轉確定性路線）

## Part B — 明確不做（裁決 R10；留痕以免下輪誤認漏做）

- [x] `N-01` 不新增第二控制平面／目錄家族 → **DECLINED_BY_RULING**
- [x] `N-02` 不改 registry／lane POOL 排序 → **DECLINED_BY_RULING**
- [x] `N-03` 不做 `.hgk` 全量遷移 → **DECLINED_BY_RULING**
- [x] `N-04` 不重寫已重構的 README（第二輪重構） → **DECLINED_BY_RULING（R7）**
- [x] `N-05` 不動 `.4` tag/資產／`main`／產品分支／PR 狀態 → **DECLINED_BY_RULING**
- [x] `N-06` 不 merge／不 tag／不 release／不宣稱證據分支 CI → **OWNER_GATE_ONLY**


## 完成註記（證據 commit 前回填）

- `T-01` `ADMISSION_OK`／`WO-TS-20261016-01..05`／checkpoint `CK-20261016-25D7301C`（19 來源）。
- `T-02` GSTACK 六條 flow 全 `CERTIFIED`，負向對照 `NATIVE`（provider 為 null）。
- `T-03` `openspec validate pipd-repo-hygiene-and-handover-20261016 --type change --strict` → **valid**。
- `T-04` KANBAN 板 `repo-hygiene-and-handover-20261016`，E0–E7 依賴鏈 8 閘門（`t_1b226461`…`t_d1f1b773`）。
- `T-05` 29→17（12 回收、1 使用中排除）；`T-06` 救援 `39079c0`（非丟棄）；`T-07` 暫存清除；`.gitignore` 候選**證明不安全故未套用**。
- `T-08`–`T-10` docs-only 分支 `1964561`（3 檔、+119/−10、0 越界）；`T-11` 本地回合索引 `HANDOVER_INDEX.md`。
- `T-12`/`T-13` 封包 9 檔、`bbe855ee…` 已推、遠端==本地；`T-14` 車道裁決逐字入包。
- `T-15` 檢測清單 16/16 回填（見 `DETECTION_CHECKLIST.md`）；`T-16` FAR-021 五件＋skill＋memory；`T-17`/`T-18` 交還包與並行分擔。
