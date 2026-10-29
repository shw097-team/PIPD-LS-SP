# FAR-18 — 最終結案、上推 REPO、移交（七項殘留的裁決）

裁決順位：對齊 `SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` ＞ Native E2E 閉環 ＞ 無人值守 ＞ 高必要性 ＞ 不過度治理／工程化 ＞ 低阻力 ＞ 高效率。

## 0. 先量測，再裁決（本輪實測）

| 事實 | 量測 |
|---|---|
| `ORC-WO-B1-A3-POS` | `BLOCKED_CLASSIFICATION.json` 已是 **`EXECUTED_AUTHOR_SIDE`**；缺的是 `persisted_cursor／lease_generation`，`who_can_solve = OWNER（Temporal/Redis 為 DEFERRED_OWNER_HOLD）` |
| `ORC-WO-B1-B3-OPS-POS` | 同上 **`EXECUTED_AUTHOR_SIDE`**；缺真實 DEV handoff 三件（`sbl_entry／candidate／dev_diff`），`who_can_solve = OWNER`（外部 repo 無真 DEV ECP） |
| `ORC-WO-B1-C4-POS` | `OWNER_ACTION_REQUIRED`；`owner grant (principal/scope/ttl)`；ledger 的 NEG/SEC 已執行 |
| `CR-ORACLE-001` | `DOC-05:20/667` 衝突未解、`L785 ORACLE_AUTHORITY_UNRESOLVED`；`pipd-authority-source` 才能建正式 `SourceFreezeManifest`（`10B_B1_PI27_PD31.md:451`） |
| `Release／SourceFreeze` | 需「原 Owner 簽章＋native 證據後重新 freeze」；本輪 GWO／G-B／audit 均已 PASS |
| 現役簽章窗口 | `WIN-98bc50531cba`，scope 僅 `registry_row_sign,merkle_root_sign`，ops 1/60 —— **依 FAR-15 硬不變量，它簽不了 freeze/release** |
| PIPD repo | 分支 `rescue/r5p-uncommitted-20261016`；`b1/closure-20261028` = `5c8f203`；工作樹有未提交變更（`tasks.md`、`TECHNOLOGY_ADMISSIONS.json`、`.b1_evidence/` 等） |

## 1. 七項裁決

| # | 項目 | 裁決 | 誰能做 | 成本 | 判定依據 |
|---|---|---|---|---|---|
| 1 | A3 QUEUE_WO | **維持 `EXECUTED_AUTHOR_SIDE`，不列為 agent 缺陷**；真 durable queue（Temporal/Redis）依 `04:1325 DEFERRED_OWNER_HOLD` **不由 agent 自建** | OWNER（基礎設施決策） | 0（本輪） | 條文已把 Temporal/Redis 列為 owner hold；agent 自建＝第二 scheduler，違 `06:103` |
| 2 | B3-OPS SBL_TO_NATIVE | **同上**；缺的是**外部 repo 的真 DEV ECP**，不是本候選缺能力 | OWNER（提供外部 ECP） | 0（本輪） | 外部 repo 無 DEV ECP → 依 FAR-10 只做 L1，不得假稱 native |
| 3 | C4 EXTERNAL_GRANT | **永久 `NOT_GRANTED`（裁決丁）** | agent 可記錄（**只會收回權限，不會擴張**） | 10 分 | 外部租戶 grant 無真實需求；保留 local demo grant 與 ledger NEG/SEC 證據 |
| 4 | CR-ORACLE-001 | **維持 `ORACLE_UNBOUND`，不自任 oracle owner**；27 條 oracle 保持 `NOT_RUN`，並在結案書明列為「文件層未決」 | OWNER（指定 oracle owner） | 0 | `DOC-05:20/667`；自任 owner＝自簽 oracle，違 `02:28`／`09:375` |
| 5 | R1 31 slot 無 KB 具名出處 | **維持 `DELIVERED_ONLY` 天花板**，不補造引用；把 31 個 slot 逐 ID 列成「待補出處」清單 | agent（列清單）＋OWNER（若要真引用需 KB 授權範圍） | 30 分 | 憑空補 `file#line` 就是偽造證據；寧可掛天花板 |
| 6 | AUTHOR_SIDE 三項殘留 | **可量測的先量測、不可量測的維持宣告式並在結案書標 `DECLARATIVE_NOT_MEASURED`**：<br>· `repo_untouched` → 實測 `git status` 對照<br>· prestate 自製 stub → 標 `STUB_PRISTINE_STATE`<br>· CC 綁定宣告式 → 標 `DECLARATIVE_BINDING` | agent | 20 分 | 三項都不影響 native 說服力，但不得冒稱已量測 |
| 7 | F-45／F-52 天花板 | **寫進結案書的「不可消除限制」**，並在 `RECOVERY.md`／`GOVERNANCE_ROUTING.md` 交叉引用 | agent | 10 分 | 單一 OS principal 的固有限制；聲稱已解就是造假 |

**總結**：七項之中，**只有 3 號（C4）可由本輪直接裁決落地**；1／2／4 是 **OWNER 決策/資源**，5／6／7 是 **誠實天花板**。沒有任何一項可以靠再寫程式變成「已完成」。

## 2. Release / SourceFreeze：唯一需要新簽章的一步

`04:137` 明列 Release 屬「仍需專門授權」；FAR-15 的窗口因此**永久拒絕** `release/sourcefreeze`。要結案必須做一次**專用授權**：

| 方案 | 做法 | 判定 |
|---|---|---|
| 甲 | 維持 `NOT_RUN` | 誠實但不結案 |
| **乙** | **專用窗口**：`owner_window.py open --task CLOSEOUT --scope sourcefreeze,release --allow-dedicated sourcefreeze,release --ttl-hours 1 --max-ops 4`。scope 明列、TTL 1 小時、上限 4 次、每次簽章都進 `SIGNING_LOG`，`DEDICATED_AUTHORISATION=explicit` 記在窗口與收據 | **建議** |
| 丙 | 放寬現役窗口 allowlist | **否**：等於讓一般 registry 窗口可以簽 release |
| 丁 | 用 env 口令直接跑 ceremony | 否：繞過窗口＝回到 F-51 的失敗模式 |

乙案仍是「專門授權」——差別只在授權**用視窗明示**而不是臨時打指令；條文只要求「專門」，沒要求「不能用 UI」。

## 3. 上推 REPO（不 force、不推 main）

| 步 | 動作 | 驗收 |
|---|---|---|
| 1 | 在 PIPD 建 `b1/closure-20261029`（自 `b1/closure-20261028` `5c8f203`） | 分支存在、base 可追 |
| 2 | 只加 `docs/closure/2026-10-29/`（`CLOSEOUT.md`、`HANDOVER.json`、`FAR14–18`、`GATES.json`、`SELFCHECK.json`、`TASK_PREAUTH.json`、`OWNER_WINDOW.json`、`BLOCKED_CLASSIFICATION.json`） | 檔案清單與 sha 記在 `HANDOVER.json` |
| 3 | commit（訊息含 `claim_ceiling` 與 `release=NOT_RUN`／`=SIGNED` 實況） | `git show --stat` |
| 4 | push 到 `origin b1/closure-20261029`（PAT wrapper、**永不 force**） | `git ls-remote` 的 sha == 本地 HEAD |
| 5 | 不動 `main`、不動別的 session 的分支 | `git branch -r` 前後對照 |

## 4. 移交（下一個 SESSION 不需重新推導）

`HANDOVER.json` 必須包含：機器可讀狀態（gates／selfcheck／window／lease／blocked／repo）、**未完成項與各自的前置條件**、**唯一需要 owner 的兩件事**（C4 已裁決→僅記錄；freeze/release 需專用簽章）、以及「哪些主張不能說」（release 未簽前不得說已釋出）。

## 5. 建議執行方案（三波）

| 波 | 內容 | 需要簽章 | 時間 |
|---|---|---|---|
| **A** | C4 永久 `NOT_GRANTED` 落檔；A3/B3-OPS 分類覆核；R1 31 slot 逐 ID 清單；AUTHOR_SIDE 三項標記；`CLOSEOUT.md`＋`HANDOVER.json`；selfcheck／gates 重跑 | ❌ | 60 分 |
| **B** | 專用窗口（乙案）簽 `SourceFreezeManifest` → `RELEASE_RECEIPT`；gates 的 `release_status`／`sourcefreeze_status` 由 `NOT_RUN` 轉 `SIGNED` | ✅ **一次**（你輸入一次口令） | 25 分 |
| **C** | PIPD 建分支、commit、push、`ls-remote` 驗證；更新 `HANDOVER.json` 的 repo 段 | ❌（用既有 PAT） | 20 分 |

**若你不想現在簽 B**：A＋C 可先完成，結案書會明寫 `release_status=NOT_RUN (owner signature pending)`，push 的 commit 訊息也照實寫——不會把未簽講成已釋出。

## 6. 天花板（寫進結案書）

- `release`／`sourcefreeze` 未簽前，本交付只能稱 **候選交付（candidate delivery）**。
- 27 條 oracle 在 `ORACLE_UNBOUND` 下維持 `NOT_RUN`，不得以任何自建 owner 身分補簽。
- F-45（同 principal 記憶體）與 F-52（他人自建 owner key 可偵測不可防）**不會消失**。
- `repo_untouched` 若無真 prestate，只能標 `DECLARATIVE`，不得寫成「實測未變更」。
