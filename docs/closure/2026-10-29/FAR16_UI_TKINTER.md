# FAR-16 — 口令 UI：PowerShell ＋ loopback 換成 in-process tkinter

- 指令：對「把 `owner_prompt.py` 的 UI 分支從 PowerShell（+loopback 回傳）換成同一支 tkinter `prompt_passphrase`」做 FAR，裁決順位：對齊 `SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` ＞ Native E2E 閉環 ＞ 無人值守 ＞ 高必要性 ＞ 不過度治理／工程化 ＞ 低阻力 ＞ 高效率。
- 前提事實（已量測，非推論）：另一 SESSION 的 UI 是 `var/R18-FHS-SKELETON-SPINE-20261029/tools/owner_delegation.py:65` 的 `prompt_passphrase()`，**tkinter（Tk 8.6）native modal**，49 行；我目前的是 `OWNER_PROMPT.ps1`（83 行）＋`owner_prompt.py` loopback 段（82 行）＋UI 呼叫段（24 行）＝**189 行**。

## 1. 量測（本機，2026-10-29）

| 測項 | 方法 | 結果 |
|---|---|---|
| tkinter 在「無 console 的背景進程」能否顯示 | 背景啟動 Tk 視窗，另一進程 `EnumWindows` 列舉 | **可見**：`HGK-TK-PROBE`（前景視窗 18 個中含它） |
| Tk 版本 | `import tkinter` | **8.6** |
| 真實使用者能否輸入 | 以另一 SESSION 的原函式叫窗，你當場輸入 | **entered: True**（未取值、未記錄） |
| 現行 PowerShell 路徑的必要環節 | 讀碼 | PS 進程 → HTTP POST → `_Intake` → 佇列 → 主進程（**口令跨 3 段、其中一段是 TCP loopback 明文 JSON**） |
| 程式量 | `wc -l` | PS 路線 **189 行** vs tkinter **約 55 行**（含 fallback） |
| 引用點 | grep | `GOVERNANCE_ROUTING.md`／`owner_prompt.py`／`post_repass.py`／`REPORT.md`／`RESUME_HERE.md`（5 處需同步） |

## 2. 兩條路線的實質差異

| 面向 | 甲 PowerShell＋loopback（現況） | 乙 tkinter in-process |
|---|---|---|
| 口令經過 | PS 記憶體 → **TCP 127.0.0.1 明文 JSON** → Python | **只在同一進程記憶體**，無 socket、無序列化 |
| 額外進程 | 1 支 PowerShell（`-ExecutionPolicy Bypass`） | 0 |
| 依賴 | `powershell.exe`、HTTP server、token 檔 | Python 內建 Tk（已實測可用） |
| 遮蔽輸入 | `Read-Host -AsSecureString` | `Entry(show="•")` |
| 失敗模式 | PS 被政策封鎖／路徑改動 → 靜默等 300s | Tk 不可用 → 立即 `REFUSED_UI_DISABLED`（可 fallback） |
| 跨 session 一致性 | 只有本 session 這樣做 | 與另一 SESSION 同一個視覺與互動（你要的） |
| 程式量 | 189 行 | ~55 行（淨減 ~130） |
| 已驗證程度 | 真鑰成功 2 次 | 真鑰輸入 1 次（只是叫窗，未接簽章） |

**關鍵判讀**：PowerShell 版把口令送過一次 loopback 明文 JSON。同機的其他進程若已取得本使用者權限，本來就能讀信封與記憶體，所以這**不構成新的越權**；但它是「可避免的暴露面」——in-process tkinter 把它整段刪掉，且同時滿足「與另一 SESSION 一致」這個你明確要求過的點。

## 3. 選項

| 案 | 做法 | 判定 |
|---|---|---|
| 甲 | 維持 PowerShell＋loopback | 可用、已驗證，但多 1 進程、口令跨 socket、與另一 SESSION 不一致 |
| **乙** | **tkinter 為主，PowerShell 保留為 `HGK_OWNER_UI=ps` 備援** | **建議** |
| 丙 | 純 tkinter，直接刪 PS | 少 20 行，但失去「Tk 在某環境失效時」的退路；不留退路要再改一次碼 |
| 丁 | Hermes preview HTML 表單 | **否**：值需經 `data-hermes-send` 回一個 user turn，等於口令進對話與模型上下文；違反「永不進對話」 |
| 戊 | 直接讀 OS 憑證管理員（Windows Credential Manager） | 過度工程化：多一層依賴，且與現有 envelope 重複 |

## 4. 裁決：乙

- **UI 主選＝tkinter**（復刻另一 SESSION 的 `prompt_passphrase`，含 confirm 欄、最少 12 字、Topmost、Enter／Esc）。
- **備援＝`HGK_OWNER_UI=ps`**：僅在 Tk 初始化失敗（`tk.TclError`）或明確指定時使用既有 PowerShell 路徑；`HGK_NO_UI=1` 仍為硬關閉（無人值守／測試）。
- 三條硬不變量、`OwnerSigningWindow@1` 的 scope／TTL／op 預算、C113／C114 **一律不動**——本次只換「口令怎麼進來」，不動「誰能簽」。
- 新增一筆可稽核欄位：`ui_impl` 記在 `window.json`／`SIGNING_LOG`（`tkinter|powershell|env|tty`），C113 加驗它在白名單內。

**授權／簽章建議**：本次**不需要任何新 owner 簽章**。它不產生 rev、不變 enrollment、不動 registry；現役窗口 `WIN-6a96eaaf9df1`（ops 1/60）不受影響。

## 5. 建議執行方案

| 步 | 動作 | 驗收 | 時間 |
|---|---|---|---|
| 1 | `owner_prompt.py`：新增 `_tk_secret()`（復刻 49 行版，加 confirm／錯誤標籤），`get_secret()` 路由改 `env → TTY → tkinter → PowerShell（僅 HGK_OWNER_UI=ps 或 Tk 失敗）` | `HGK_NO_UI=1` 仍 `REFUSED_UI_DISABLED` | 20 分 |
| 2 | `window.json`／`SIGNING_LOG` 增 `ui_impl`；`cmd_open` 傳入 | 開窗證據可看出走哪條 | 10 分 |
| 3 | 文件同步 5 處（`GOVERNANCE_ROUTING.md`／`RESUME_HERE.md`／`REPORT`／`post_repass.py` 註解／`FAR-16`） | grep 不再宣稱 PS 為主選 | 10 分 |
| 4 | **scratch 假鑰**全鏈：開窗→31 簽→三負例→預算→關窗 | 與 FAR-15 同表全綠，且 `ui_impl=env`（測試） | 20 分 |
| 5 | tkinter 實窗（假鑰，`HGK_OWNER_UI=tk` 強制）手動按一次 | 視窗出現、輸入後 `ui_impl=tkinter` | 5 分 |
| 6 | selfcheck C113 加 `ui_impl` 白名單；跑 112/112（+1 = 113 若另立 C115） | 全綠 | 10 分 |

**回滾**：`owner_prompt.py` 保留 PS 分支；一行 `HGK_OWNER_UI=ps` 即回到今日已驗證路徑。

## 6. 天花板

- 同一個 OS principal 在輸入那一刻傾印記憶體仍拿得到口令——換 UI 不會改變這點。
- tkinter 需要互動桌面工作階段；headless／cron 一律走 `HGK_NO_UI` 或 env，**不會**因為換 UI 而變成可無人輸入。
- 本次不改變「誰有權簽」：Release／SourceFreeze／Policy authority／Trust Anchor／owner_enrollment 仍須當場授權。
