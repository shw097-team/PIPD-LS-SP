# FAR-15 — 簽章窗口（Owner Signing Window）與並行 writer：讓「開頭一次口令」取代「中途卡住」

- 指令：對 (a) F-50 並行 writer、(b) 「另一支程式自建 owner key 並 re-enroll 可偵測不可防」、(c) **每次授權都要使用者臨時提醒才開視窗，否則直接視為阻斷** 三件事做 FAR。
- 裁決順位：**對齊 `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` ＞ Native E2E 自主執行閉環 ＞ 無人值守高自動化 ＞ 高必要性 ＞ 不過度治理／工程化 ＞ 低阻力 ＞ 高效率**。
- 文件核對：`知識庫/…/SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` 與 workspace 副本 `var/R18-FHS-SKELETON-SPINE-20261029/subject` **逐檔 sha 相同**（`04_FABRIC_HGK_CONTROL.md` = `e8fd5317b76bffe1…`、`01_PRODUCT_AUTHORITY_SPINE.md` = `48d3d533b03fb8de…`），故本 FAR 引用行號對兩份都成立。

## 1. 先回答「可不可以開頭先填口令」——條文其實已經允許

| 條文 | 原文 | 意義 |
|---|---|---|
| **`04_FABRIC_HGK_CONTROL.md:137`** | **「Owner 低干預：單一 Human Owner 可在一次 ceremony **批量批准**『可預見、一致 policy epoch、Root、WriteSet、Operation 類別、時限』的**有界許可**；Issuer 為每筆不同 Operation 執行 nonce/lease gating，**不再要求 Owner 逐平凡 read-only probe 重簽**。任何新增 Root、Elevated effect、UserData/Remote Publish、Trust Anchor/**Policy authority**/**Release** 的實質風險提升**仍需專門授權**。」** | **明示**允許「一次批准、有界、有時限、逐筆 nonce」；同時明示哪些升級**不得**被批量涵蓋 |
| `04_FABRIC_HGK_CONTROL.md:81` | 「Owner 授權可**批量涵蓋同一 PlanRevision** 但**每寫 scope 有界**」 | 批量的邊界是 PlanRevision／scope |
| `04_FABRIC_HGK_CONTROL.md:182` | BR1 AUTH_BOUND：exact `(repo/worktree, base_HEAD, readset, writeset, max_attempts, **expiry**, effect_class)`，且「明確記錄來源、授權和拒收器」 | 授權需**明列欄位＋到期＋拒收器** |
| `04_FABRIC_HGK_CONTROL.md:26/54` | 「原 Issuer 才檢 scope/**nonce**/**TTL**」 | 每筆仍要 nonce/TTL 檢查 |
| `04_FABRIC_HGK_CONTROL.md:255` | 「self-signed WO、ECP 當 permit 均拒」 | 自簽仍一律拒 |
| `01_PRODUCT_AUTHORITY_SPINE.md:1432`、`06_FHS_EXECUTE_HERMES_RUNTIME.md:103` | 不得自建第二 Issuer／可自簽第二 queue | 窗口不得成為第二 authority |

**結論**：使用者要的「開頭先填一次、之後連續執行」**不是繞過治理，而是條文第 137 行明列的 Owner 低干預模式**。我目前的「每次臨時開視窗」其實是**比條文更嚴、也更笨**的做法：它不是治理要求，是我把「沒有窗口」實作成「直接阻斷」。

## 2. 現況的三個真缺陷

| 代號 | 缺陷 | 影響 |
|---|---|---|
| **F-50** | 並行 writer 無互斥：兩個 session 可同時改 `gates.py`／`selfcheck2.py`／registry | 互相覆蓋、證據來源不明 |
| **F-51** | 「無口令 → 阻斷」被實作成**硬停**，且 agent 需人提醒才知道有口令機制 | 任務無法自主閉環；使用者必須在場 |
| **F-52** | 結構性殘留：任何程式可自建新 owner key 並 re-enroll（單一 OS principal） | 可偵測不可防；但**可收窄**：把它排除在窗口授權之外 |

## 3. 選項

| 案 | 做法 | 對齊 | 無人值守 | 工程成本 | 判定 |
|---|---|---|---|---|---|
| 甲 | 維持現狀（每次治理事件重新提示） | 達成 | **不可**（中途阻斷） | 0 | 不符需求 |
| **乙** | **Owner Signing Window（簽章窗口）**：開頭一次口令 → 記憶體內簽章代理 → TTL／scope／op 預算／nonce／逐筆 log；**enrollment 變更與 Release/Policy authority 等升級永不在窗口內** | 達成（L137/L81/L182） | **達成** | ~200 行新模組＋ceremony 掛鉤 | **建議** |
| 丙 | 委派簽章憑證（session key + owner-signed grant，registry 帶憑證鏈） | 達成 | 達成 | 需改 registry 驗簽鏈與 schema | 過度工程化 |
| 丁 | 開頭預先簽「整批變更清單」 | 達成 | 僅適用可預見變更 | 低 | 可作乙的補充，不作主案 |
| 戊 | 預簽空白 permit／長 TTL 明文託管 | 不可（重放／可代簽） | 達成 | 低 | **禁止** |

## 4. 裁決：乙（Owner Signing Window）＋ 三條硬不變量 ＋ F-50 單寫者租約

### 4.1 窗口規格（`OwnerSigningWindow@1`）

```json
{
  "window_id": "WIN-<uuid>",
  "task_id": "<本次任務>",
  "opened_at": "...", "expires_at": "...",
  "scope": ["registry_row_sign", "merkle_root_sign"],
  "effect_class_ceiling": "READ_ONLY_PROBE|REPOSITORY_WRITE",
  "max_ops": 40, "ops_used": 0,
  "policy_epoch_at_open": 10,
  "enrollment_sha_at_open": "<sha of owner_enrollment block>",
  "owner_fingerprint": "412b351937be72a1",
  "token_file": "%USERPROFILE%/.hgk-owner/window.token  (ACL: owner only)",
  "log": "artifacts/SIGNING_LOG.jsonl"
}
```

**三條硬不變量（窗口內一律拒絕，必須另行當場輸入口令）**：

1. **`owner_enrollment` 任何變更**（換 owner 公鑰＝自建第二 issuer）→ `REFUSED_ENROLLMENT_CHANGE_IN_WINDOW`。這條同時把 F-52 從「可偵測」收窄成「窗口期內不可為」。
2. **`effect_class` 超過宣告上限**（Elevated／UserData／Remote Publish）→ `REFUSED_EFFECT_CLASS_ABOVE_WINDOW`。
3. **Release／SourceFreeze／Policy authority／Trust Anchor** → `REFUSED_ESCALATION_NEEDS_DEDICATED_AUTH`（條文 L137 明文要求專門授權）。

**窗口到期或 `--close` 後**：金鑰記憶體歸零、token 檔刪除、`window.json` 標 `closed`；此後任何簽章一律 `REFUSED_OWNER_KEY_LOCKED`（回到現行行為）。

**逐筆可稽核**：每次簽章寫 `artifacts/SIGNING_LOG.jsonl`（window_id、op、payload_sha256、decision、ts、ops_used）。owner 事後可一眼看出「這個窗口替我簽了什麼」。

### 4.2 agent 行為規則（不再需要人提醒）

- 任何回合開頭的標準動作：`python owner_window.py status`。
  - `OPEN` 且未過期 → 直接用，**不得**停下來問口令。
  - `ABSENT/EXPIRED` → 只有此時才可以要求開窗，且**一次說清楚**要開多久、多少 op、什麼 scope。
- 這條寫進 `RESUME_HERE.md` 與 `AGENTS.md` 的「治理事件」段落，避免下一個 session 又把它當硬阻斷。

### 4.3 F-50 並行 writer：單寫者租約

- `var/B1-PIPD-PKG-20261027/.writer-lease.json`：`{session_id, pid, started_at, heartbeat_at, owns:[files]}`；以 `O_EXCL` 建立、心跳更新。
- 寫入前先取租約；取不到就**只讀不寫**，並在回報中標 `WRITER_LEASE_HELD_BY:<session>`。
- 本次事件已造成 `gates.py`／`selfcheck2.py`／`owner_ceremony.py` 被兩個 session 先後修改；租約可讓下一次不再靠運氣（本次修補前已快照 `artifacts/f49_snapshot/`）。

## 5. 授權與簽章建議

1. **不需要**新增任何簽章型別或 schema 欄位（九欄 row 不動）；窗口是**獨立 artifact**，registry 只多一個頂層 `signing_window_id` 參照（可選）。
2. 開窗本身**是一次 owner 簽章**：`SigningWindow@1` 由 owner key 簽（`window.open` 內完成），因此「誰授權了這個窗口」本身可驗。
3. 關窗寫 `WINDOW_CLOSED` 事件（含 `ops_used`、`refusals`、`first/last op ts`），作為 owner 的收據。
4. 天花板誠實標註：窗口期內，**持有 token 的本機進程**可在 scope 內代簽；這正是 L137 允許的「有界批量」，但不得敘述成「逐筆 owner 親簽」。

## 6. 建議執行方案

| 步 | 動作 | 驗收 | 時間 |
|---|---|---|---|
| 1 | 寫 `owner_window.py`（open/status/close/revoke、TCP loopback + token、TTL、op 預算、三條硬不變量、SIGNING_LOG） | `open` → `status` 顯示 OPEN；`close` 後簽章 `REFUSED_OWNER_KEY_LOCKED` | 40 分 |
| 2 | `owner_ceremony.py` 掛鉤：有窗口 → 走窗口（不提示）；無 → 現行提示 | 窗口內跑一次 registry 重簽 → rev+1、無提示；關窗後再跑 → 提示/拒絕 | 15 分 |
| 3 | 負例三發：enrollment 變更、effect 超限、Release | 三者皆 `REFUSED_*`，且 `ops_used` 不增 | 15 分 |
| 4 | F-50 租約 `writer_lease.py` ＋ RESUME/AGENTS 規則 | 兩 session 併發測試：第二個寫入被拒並標 `WRITER_LEASE_HELD_BY` | 20 分 |
| 5 | 自檢 C113（窗口不變量）／C114（SIGNING_LOG 完整性） | 110 → 112 全綠 | 15 分 |
| 6 | REPORT／RESUME／kanban | `mission_complete` 不變、attribution 不變 | 10 分 |

**回滾**：新模組與掛鉤皆為加法；`owner_ceremony.py` 保留原提示路徑，刪 `window.json` 即回復現狀。

## 7. 明確不做

- 不做委派簽章憑證（丙案）——需改 registry 驗簽鏈與 schema，屬過度工程化。
- 不做「空白 permit 預簽」或長 TTL 明文託管（戊案）——可重放、可代簽。
- 不把窗口當成 Release／Policy authority／UserData effect 的授權來源（條文 L137 明文禁止）。
- 不為了自動化而放寬 `owner_enrollment` 的變更限制。

## 8. 天花板

- 窗口是「時間＋範圍」的收斂，不是「人不在也能永久簽」。到期即失效，且 escalation 類仍需在場。
- 同使用者進程在簽章瞬間傾印記憶體仍不可防（單一 OS principal）；本設計只降低「靜態託管」與「臨時阻斷」兩個問題。
- 本 FAR 未修改任何 live 檔案；文件引用已對 知識庫 與 workspace 兩份 sha 驗證一致。
