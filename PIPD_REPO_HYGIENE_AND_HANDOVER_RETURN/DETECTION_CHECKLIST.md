# 檢測清單 (DETECTION_CHECKLIST) — 已回填

**Round**：`PIPD-REPO-HYGIENE-AND-HANDOVER-20261016`｜**回填時點**：證據 commit 前。
**Checker 欄誠實說明**：PLAN/EXECUTE/VERIFY 同臂（`opencode-go/deepseek-v4.1-flash`，registry `SOD006-C3`）
⇒ **模型軸分離不存在**；下表「獨立」一律指**程序／車道／證據路徑**分離，不指跨模型。
**證據包**：`repo-hygiene-evidence-20261016` @ `bbe855ee860977974d52c645919abc0e0a49c928`。

| ID | 檢測項 | Expected | Actual | 證據 ID / locator | 判定 |
|---|---|---|---|---|---|
| `D-01` | `main` 未被本回合寫入 | `d3bd5456…` | `refs/heads/main` = `d3bd5456afbff21a8c8837994a49f57be3e1b97e`（推前推後同一） | `identities_and_release.json#live_readback`；`independent_verify.json#4` | **VERIFIED** |
| `D-02` | PR #18／#17 未被改變 | head 不變 | `refs/pull/18/head` = `c17aa761…`；`refs/pull/17/head` = `97a01dab…` | 同上 | **VERIFIED** |
| `D-03` | `.4` tag／資產未被觸碰 | tag 物件 `0618d73c…` | `refs/tags/v0.1.1-preview.4` = `0618d73c725da0d8c3280f99ef369d13741b5197`；本回合作業 0 次觸及 release API | `independent_verify.json#4` | **VERIFIED** |
| `D-04` | 產品程式 0 行變更 | `src/`、`schemas/`、`skills/` 皆 0 | 兩分支對 `origin/main` 之差集：`src/schemas/skills` 命中 **0** | `independent_verify.json#2#6` | **VERIFIED** |
| `D-05` | docs 分支恰三檔 | 3 檔 | `README.md`、`docs/adr/ADR-0008-…md`、`docs/adr/ADR-0009-…md`（+119 / −10） | `front_page_change.json`；`independent_verify.json#2` | **VERIFIED** |
| `D-06` | README 不再「以現行語氣」宣告過期車道模型 | 0 命中或標為歷史 | 仍存 2 處 `glm-5.3-flash`（皆為**歷史車道收據原文**，依證據不得改寫），其上方新增 `Lane-arm note (2026-10-16)` 明文標示為歷史並載明現行臂與 SoD 揭露 | `README.md` diff；`independent_verify.json#5` | **PASS_WITH_HISTORICAL_MARKING** |
| `D-07` | README 現況節帶 2026-10-16 事實 | ≥1 且含 PR #18 未合併／`TEMP_CLOSED_RECOMMENDED` | 節標題 `(2026-10-16)`；含 PR #18／#17 表、`TEMP_CLOSED_RECOMMENDED`、S4 final review outcome 表 | `independent_verify.json#5` | **VERIFIED** |
| `D-08` | 首頁 claim ceiling 未被升高 | 仍 `NOT_GRANTED` | `S4_FULL_PASS` 出現處皆伴 `NOT GRANTED`／`NOT_GRANTED`；新增節明列 4 項 `NOT_GRANTED`／`NOT_RUN`／`OUT_OF_SCOPE` | `independent_verify.json#5` | **VERIFIED** |
| `D-09` | worktree 回收守門生效 | 只刪 `dirty==0` ∧ 尖端在 origin | 29 → 17，刪 **12**、跳過 1（使用中者）；**0 個 dirty>0 被刪**；首輪誤取候選集時 9 個 dirty 全被守門拒絕 | `hygiene_actions.json#E1_reclaim`；`#guard_effectiveness` | **VERIFIED** |
| `D-10` | 未提交產品碼為救援非丟棄 | 新分支存在、原分支未動 | `rescue/r5p-uncommitted-20261016` @ `39079c0`；`src/pipd_ls_sp/{cli,pipeline,validate}.py` 等 6 檔入提交；原分支 `r5p-post-challenge-repair` 未被改動、未推；追蹤修改歸零、218 未追蹤原封 | `hygiene_actions.json#E2_rescue_actual` | **VERIFIED** |
| `D-11` | 可重生暫存已清 | 0 項 | `_scratch/verify{,2,3,4,5}` → 0 項 | `hygiene_actions.json#E3_scratch` | **VERIFIED** |
| `D-12` | 未新增目錄家族 | main／docs 候選 0 個新目錄 | main 與 docs 候選皆 0；唯一新目錄為**證據分支**上的封包目錄 `PIPD_REPO_HYGIENE_AND_HANDOVER_RETURN/`（沿用前兩回合封包慣例） | `independent_verify.json#2` | **VERIFIED_WITH_DISCLOSURE** |
| `D-13` | 證據包 shipped-bytes 自驗 | 全符、0 CRLF | 由 `git archive` 取出重算：**mismatches NONE**；`SHA256SUMS` 覆蓋 8 檔（6 具名＋MANIFEST＋far_verdict） | `independent_verify.json#1`（方法與建包不同：自 origin 位元） | **VERIFIED** |
| `D-14` | 遠端尖端 == 本地 | 相等 | 本地 `bbe855ee…` == `refs/heads/repo-hygiene-evidence-20261016`；docs 候選 `1964561…` == 遠端；**該二 push 不觸發任何 CI**（workflow 僅 `pull_request`／`workflow_dispatch`） | `independent_verify.json#1#2` | **VERIFIED** |
| `D-15` | 反證搜尋（不宣稱未搜者） | 逐類交代 | (a) **首頁造假**：無（現況節每項均有遠端可讀 locator）；(b) **職權越界**：無（本回合 0 merge／0 tag／0 release／0 產品寫入）；(c) **自我驗收**：無（裁決由 CODEX CLI 車道獨立出具，且已明示同臂）；(d) **刪除釀損**：無（12 個回收皆尖端在 origin）；(e) **私有宿主 UAT／四宿主 qualification／Production**：**NOT_RUN，本回合不宣稱已排除** | `independent_verify.json`；車道收據 | **VERIFIED (a–d) / NOT_RUN (e)** |
| `D-16` | 自犯缺陷誠實計數 | 逐項列出 | **7 項**（`SID-01`…`SID-07`，見 `hygiene_actions.json#self_inflicted_defects` 與 FAR `DEVIATIONS_ADDENDUM`）：記錄晚寫導致動作無檔、openspec 誤建於 docs worktree、車道 brief 觸發遠端寫入守門 ×2、execute_code 上限中斷車道等待、`$TMPDIR` 路徑未轉譯、admission 段名撞號留下 spine 孤兒、清冊形狀假設 ×2 | 見 FAR `DEVIATIONS_ADDENDUM.md` | **DISCLOSED** |

## 車道裁決（逐字，未編輯）

- 車道：`VERIFY_SECURITY`／engine `codex-cli`／`ok: true`／`used_rank: 1`／`required_arm == served_arm ==
  opencode-go/deepseek-v4.1-flash`／`used_seconds: 524.64`／nonce 已發（`HGK_LANE_NONCE_OK_PIPD-RH-20261016`）。
- **裁決：`INCONCLUSIVE`**；其結語逐字：「…Both keep the round below a full PASS; I found no substance that
  contradicts the writer's core claims.」⇒ **未發現與作者核心宣稱矛盾者**，但**不構成 full PASS**。
- 全文：`lane/verify_rh/VERDICT_LANE_VERBATIM.txt`（含其裁定未能獨立查核之項：WorkOrder/KANBAN id 等
  「一致但無法自提交物查核」）。
