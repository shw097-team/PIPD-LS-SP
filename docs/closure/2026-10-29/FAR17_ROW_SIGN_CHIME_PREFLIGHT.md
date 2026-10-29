# FAR-17 — F-53 的真因、口令視窗音效、任務開頭強制預授權

裁決順位：對齊 `SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` ＞ Native E2E 閉環 ＞ 無人值守 ＞ 高必要性 ＞ 不過度治理／工程化 ＞ 低阻力 ＞ 高效率。

## 一、F-53：我上一輪的描述不精確，實測後改判

### 1.1 量測（可重跑）

```
live      rows 30  signed 30  gen_rows 18   gen_exe 存在 → sha256 有值
scratch2  rows 30  signed 12  gen_rows 18   gen_exe 不存在 → sha256 = null
```

`owner_ceremony.py:427-430`：

```python
for row in rows:
    if row.get("status") == "INSTALLED" and row.get("sha256"):     # ← 靜默跳過沒有 sha 的列
        … row["owner_signature"] = …
```

`admission/owner_merkle.py:73` `verify_registry()`：只驗 `owner_signature`（root）＋ `merkle_root` 相符＋ root 簽章可驗；
**完全不檢查每一列是否帶簽章**。

### 1.2 所以真正的缺陷是兩個，不是一個

| 代號 | 缺陷 | 為什麼會發生 | 嚴重度 |
|---|---|---|---|
| **F-53a** | ceremony 對 `INSTALLED` 但 `sha256` 空白的列**靜默不簽**，也不拒絕 | workspace 缺 `admission/runners/generic_route_runner.py` → `gen_sha=None` → 21 行條件不成立 | 中：會產出「INSTALLED 但沒有 owner 簽章」的列 |
| **F-53b** | `verify_registry()` 只驗 root，**不驗逐列簽章** | 設計成 merkle-root-only | 低—中：root 仍能抓「改內容」（leaves 變→root 變），抓不到「本來就沒簽」 |

修正我先前的說法：**不是「ceremony 只簽 12 列」**，而是「沒有 sha 的列被跳過」。live 的 30 列齊全是因為 live 有 `generic_route_runner.py`。

### 1.3 裁決

| 案 | 做法 | 判定 |
|---|---|---|
| 甲 | 只寫文件 | 否：狀態可再現 |
| 乙 | ceremony 遇 `INSTALLED` 但缺 sha／缺簽章 → typed refuse `REFUSED_ROW_UNHASHED_OR_UNSIGNED`（6 行） | 可，但不夠 |
| **丙** | **乙 ＋ `verify_registry()` 逐列驗簽**（每一列須有 `owner_signature.value` 且以 enrolled owner key 對 `row_body` 驗過，否則 `REFUSED_ROW_SIGNATURE_MISSING/INVALID`）；`demo:true` 的 registry 豁免（demo 本來就不簽） | **採用** |
| 丁 | 丙 ＋ 逐列 `key_id` ＋ 輪替歷史鑰驗證 | 過度工程化（目前只有一把 owner key，輪替已由 `--rotate` 產生新 rev） |

成本：乙 6 行、丙 ~35 行；驗證 30 列成本可忽略（Ed25519 驗簽微秒級）。
對 live 的影響：**live 30/30 已簽且有 sha → 直接通過**；scratch/demo 會被 乙 擋（正確行為），demo registry 以 `demo:true` 豁免丙。

**授權／簽章需求：不需要任何新 owner 簽章**（不改 30 列內容、不改 enrollment、不產生新 rev）。

---

## 二、口令視窗音效

### 2.1 量測（本機）

| 方案 | 延遲 | 依賴 | 備註 |
|---|---|---|---|
| `winsound.MessageBeep(MB_ICONEXCLAMATION)` | **0.00 s** | Python 內建（Windows） | 用系統音效配置，不會吵 |
| `winsound.PlaySound("SystemExclamation", SND_ALIAS\|SND_ASYNC)` | 0.07 s | 內建 | 非阻塞，可換系統音 |
| `winsound.Beep(880,120)` | 0.12 s | 內建 | 阻塞 120ms，音調固定 |
| Hermes TTS（`text_to_speech`） | 秒級＋網路 | edge/雲端 | 過度：一個提示音不需要語音合成 |
| PowerShell `[console]::beep` | 需起進程 | 額外進程 | 與 FAR-16 已移除的轉手相同問題 |

### 2.2 裁決

**乙：`winsound` 進程內提示音，預設開、可用 `HGK_OWNER_CHIME=0` 關閉。**

- 開窗：`MessageBeep(MB_ICONEXCLAMATION)` ＋ `PlaySound("SystemExclamation", ASYNC)`（雙保險，其中一個被系統設定靜音仍有另一個）。
- 拒絕／驗證失敗：`MessageBeep(MB_ICONHAND)`（不同音，讓你不必看螢幕也知道被拒）。
- 關窗／到期：`MessageBeep(MB_OK)`。
- 全部 async／非阻塞，不影響 TTL 與簽章路徑；`winsound` 匯入失敗則靜默略過（音效不是治理條件）。
- **不得**用音效傳遞任何資訊（不編碼口令、不編碼結果），只是提示。

---

## 三、任務開頭強制預授權（preflight）

### 3.1 條文依據

`04_FABRIC_HGK_CONTROL.md:137`「一次 ceremony 批量批准**可預見**、一致 policy epoch、Root、WriteSet、Operation 類別、**時限**的有界許可」；`:182` BR1 AUTH_BOUND 要求 exact tuple（含 `expiry`、`effect_class`）＋明確拒收器。
→ **「可預見」正是任務開頭要做的事**：先宣告，再開窗。這不是新治理，是把已有的閘門提前到 T0。

### 3.2 設計：`owner_preflight.py`

```bash
python -B owner_preflight.py --ops registry_resign,new_route --ttl-hours 8 --max-ops 60
```

| 分類 | 觸發 op | 行為 |
|---|---|---|
| `NONE` | 讀取／GWO／checker／selfcheck／gates／kanban／codex 車道 | 直接放行，**不開窗** |
| `WINDOW_REQUIRED` | `registry_resign`、`new_route`、`row_resign`、`route_revoke` | **當場開窗一次**（tkinter、有音效），等 `usable:true` 才回 0 |
| `DEDICATED_REQUIRED` | `release`、`sourcefreeze`、`policy_authority`、`trust_anchor`、`owner_enrollment_change`、`userdata_effect` | 印出清單並回 11；**窗口不代理**，該項仍需當場授權 |

輸出 `artifacts/TASK_PREAUTH.json`：`task_id`、`ops`、`classification`、`window_id`、`expires_at`、`max_ops`、`effect_ceiling`、`dedicated_required[]`、`decided_at`。
退出碼：`0=NONE`／`10=WINDOW_READY`／`11=DEDICATED_REQUIRED`／`12=WINDOW_FAILED`／`13=WINDOW_TIMEOUT`。

**強制點**：`GOVERNANCE_ROUTING.md` 的回合前置改成三步（preflight → lease → 執行）；新增自檢 **C115**：
- 每次有窗口簽章的回合，必須存在同 `task_id` 的 `TASK_PREAUTH.json`；
- `SIGNING_LOG` 的 op 必須落在 preflight 宣告的 `ops` 內（不得事後長出未宣告的 op）；
- `dedicated_required` 清單中的 op 不得在 `SIGNING_LOG` 出現 `ALLOW`。

### 3.3 為什麼不是過度治理

- 一個指令、一次口令、零新授權主體；所有欄位都已在條文 AUTH_BOUND 裡。
- 沒有 preflight 就只能靠 agent「記得先開窗」——那正是這一輪之前的失敗模式（F-51）。
- 可無人值守：preflight 在無人值守時帶 `--ops` 直接跑；若需要窗口而無人輸入 → 回 13 並清楚標 `NEEDS_OWNER_WINDOW`，不是假裝 BLOCKED。

---

## 四、建議執行方案

| 步 | 動作 | 驗收 | 時間 |
|---|---|---|---|
| 1 | F-53a：ceremony 遇 `INSTALLED` 缺 sha／缺簽章 → `REFUSED_ROW_UNHASHED_OR_UNSIGNED`；demo 豁免 | scratch2 重跑：18 列無 sha → **typed refuse**；live 不受影響 | 15 分 |
| 2 | F-53b：`verify_registry()` 逐列驗簽（`REFUSED_ROW_SIGNATURE_MISSING/INVALID`）；`demo:true` 豁免 | live 仍 `OWNER_SIGNATURE_VERIFIED`；把一列簽章改成 `00…` → 立即 `REFUSED_ROW_SIGNATURE_INVALID` | 25 分 |
| 3 | 音效：`owner_prompt` 內 `_chime()`；開窗／拒絕／關閉三種；`HGK_OWNER_CHIME=0` 可關 | 開窗聽到提示音；錯口令聽到警示音；無 GUI 時不出聲 | 10 分 |
| 4 | `owner_preflight.py` ＋ `TASK_PREAUTH.json` | 三類各跑一次：NONE→0、WINDOW→10 且窗口 usable、DEDICATED→11 且列出清單 | 30 分 |
| 5 | C115（preflight 與 SIGNING_LOG 對帳）＋ 文件三步前置 | selfcheck 112 → 113 全綠 | 15 分 |
| 6 | 真鑰驗證：preflight 用現役窗口（不再問口令）跑一次 `registry_resign` 宣告 → 零提示完成 | `TASK_PREAUTH.json` 與 SIGNING_LOG 對得上 | 10 分 |

**回滾**：全部加法；`HGK_OWNER_CHIME=0` 關音效；preflight 不跑則行為與現在相同（但 C115 會紅，這正是要的）。

## 五、天花板

- 丙案讓「未簽列」無法再被當成正常狀態，但**不阻止**有人直接用別的工具改寫 registry 檔案（單一 OS principal 的固有限制，只能偵測）。
- 音效可被系統靜音；它不是治理證據。
- preflight 的分類依「宣告」而來；宣告不實仍會在 C115 被 SIGNING_LOG 對帳抓出來，但無法阻止 agent 在宣告外**嘗試**（會被窗口 scope 拒絕）。

---

## 六、執行結果（2026-10-29，實跑）

| 步 | 結果 |
|---|---|
| 1 F-53a | scratch2 ceremony → `REFUSED_ROW_UNHASHED_OR_UNSIGNED`，count=18、`nothing was written`、rc=4 |
| 2 F-53b | live → `OWNER_SIGNATURE_VERIFIED`；scratch2 → `REFUSED_ROW_SIGNATURE_MISSING:OWNER_REGISTERED::immutable_evidence`；改簽章 → `REFUSED_REGISTRY_ROOT_MISMATCH` |
| 3 音效 | `_chime()` 三態實呼；延遲 0.00–0.12 s；`HGK_OWNER_CHIME=0` 靜音 |
| 4 preflight | NONE rc 0／WINDOW rc 10（沿用 `WIN-98bc50531cba`）／DEDICATED rc 11（`release`）／UNKNOWN rc 14 |
| 5 自檢 | **113/113**（新增 C115 preflight 對帳）；gates 全綠 |
| 6 真鑰 | 現役窗口 `WIN-98bc50531cba`（tkinter、fp `412b3519…`）被 preflight 直接沿用，**未再彈窗** |

未變：live registry `d70195751a48f15e`、`mission_complete=true`、`release/sourcefreeze = NOT_RUN`。
