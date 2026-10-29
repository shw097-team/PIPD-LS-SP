# GOVERNANCE ROUTING — 誰在什麼時候用哪條路徑（FAR-15 之後）

> 目的：讓下一個 session **不需要人提醒**就知道「這裡要不要口令、口令從哪來、什麼時候可以直接簽」。

## 0. 每個回合的固定前置（不算治理事件，不會彈窗）

```bash
cd /c/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027
python -B owner_preflight.py --ops <本回合宣告的 op> --task <task_id>   # ← 強制第一步（FAR-17）
python -B owner_window.py status      # rc10=WINDOW_READY；rc11=DEDICATED_REQUIRED
python -B writer_lease.py status      # 取不到租約 → 只讀，不要動 shared 檔
```

`owner_preflight.py` 的分類：`NONE`（rc 0，不開窗）／`WINDOW_REQUIRED`（rc 10，當場開窗一次）／
`DEDICATED_REQUIRED`（rc 11，列出清單，窗口不代理）／`UNKNOWN`（rc 14，拒絕猜測）。
每次執行寫 `artifacts/TASK_PREAUTH.json`（最新）＋`TASK_PREAUTH_LOG.jsonl`（追加），由 C115 對帳。

裁決規則（照順序）：

1. `status` 顯示 `usable: true` → **直接跑**，不要停下來問口令。
2. `ABSENT`／`closed` → 只有在**本次真的要簽章**時才需要開窗（見 §2）。
3. 純執行、GWO、G-B、checker、selfcheck、gates、kanban、車道派工 → **不需要任何窗口**。

## 1. 路由表

| 動作 | 路線 | 需要口令？ |
|---|---|---|
| 跑 runner／GWO／G-B／checker／selfcheck／gates／kanban／codex 車道 | 直接執行 | ❌ |
| registry 重簽（新增 route、更新 row sha、rev+1） | **簽章窗口**（`owner_window.py open` 一次，之後 `owner_ceremony.py` 自動走窗口） | 只在**開窗**時一次 |
| row 級簽章（30 列 owner_signature） | 同上（走窗口，不逐列提示；`--load-once` 或窗口） | 同上 |
| `--repass`／`--rotate`／`--secure`／`--seal` | `owner_prompt` → **tkinter 原生視窗**（`OWNER_PROMPT.ps1` 僅為 `HGK_OWNER_UI=ps` 備援） | ✅ 每次（治理事件本體） |
| **Release／SourceFreeze／Policy authority／Trust Anchor** | 一律當場口令，**窗口不代理**；preflight 會回 `DEDICATED_REQUIRED` | ✅ 每次（條文 `04:137` 明列） |
| `owner_enrollment` 變更（換 owner 公鑰＝第二 issuer） | 一律當場口令，窗口會 `REFUSED_ENROLLMENT_CHANGE_IN_WINDOW` | ✅ 每次 |
| Elevated／UserData／Remote Publish effect 超過窗口上限 | 窗口拒絕 `REFUSED_EFFECT_CLASS_ABOVE_WINDOW` | ✅ 每次 |

## 2. 開窗（一次口令，之後連續執行）

```bash
# 由 owner 執行；沒有 TTY 時會自動彈出 OWNER_PROMPT.ps1（遮蔽輸入、不落檔、不進歷史）
python -B owner_window.py open --task <任務代號> --ttl-hours 8 --max-ops 60 \
       --scope registry_row_sign,merkle_root_sign --effect-ceiling REPOSITORY_WRITE
```

- 窗口由 owner key 簽發收據 → `artifacts/OWNER_WINDOW.json`（誰授權、何時到期、上限多少）。
- 每筆簽章寫 `artifacts/SIGNING_LOG.jsonl`（window_id／op／payload sha／decision／ops_used）。
- 關窗：`python -B owner_window.py close`；到期自動關；金鑰只在窗口進程記憶體，關閉即消失。
- 之後簽章若被拒，會回**明確代號**（見 §1），不是靜默降級。

## 3. 口令來源優先序（`owner_prompt.get_secret`）

1. 環境變數（`HGK_OWNER_PASSPHRASE`／`HGK_OWNER_NEW_PASSPHRASE`）— 只用於腳本化/測試，值永不落檔、永不進 argv。
2. 真正的 TTY → `getpass`。
3. **tkinter 原生視窗（主選，FAR-16）** — 同進程、無子進程、口令不出本進程；`OWNER_PROMPT.ps1` 降為備援（`HGK_OWNER_UI=ps` 或 Tk 不可用時）。
4. 視窗彈出／拒絕／關閉時有 `winsound` 提示音（`HGK_OWNER_CHIME=0` 可關；音效不承載任何資訊）。
5. `HGK_NO_UI=1` → 不彈窗，直接 `REFUSED_UI_DISABLED`（無人值守測試用）；`ui_impl`（`env|tty|tkinter|powershell`）會記進窗口與 SIGNING_LOG，由 C113 稽核。

## 4. 硬規則（不要繞）

- 不得把口令寫進檔案、argv、log、commit 或對話。
- 不得把「沒有窗口」當成「檔期阻塞」而上報 `BLOCKED`；正確講法：`NEEDS_OWNER_WINDOW`（可恢復，開窗即續）。
- 不得用 demo key 對 live registry 簽章（`admit.py` 會 `REFUSED_LEGACY_DEMO_PATH_ON_SIGNED_REGISTRY`）。
- 同時要改 `gates.py`／`selfcheck2.py`／`owner_ceremony.py` 等 shared 檔時，先取 writer lease，並在結束時 `release`。
