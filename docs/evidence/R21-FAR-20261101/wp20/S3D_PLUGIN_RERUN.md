# S3d：PLUGIN leg 重測（取代被撤回的 plugin_real_install 區塊）

## 為什麼重跑

AO `deleg_0361E484` 的 F6／N1／N2：舊區塊用 Python 寫檔假裝安裝、fixture 自己 `{"ok": false}`、引用的 sha 在磁碟上不存在、before/after 位元相同。那一整塊已撤回（見 `AO_0361E484_RETURN.md`、`CORRECTION_LEDGER.json`）。

## 這次怎麼量

三間獨立的 `HERMES_HOME`（`wp20/plugin_probe/home_empty`、`home_copied`、`home_install`），同一支 binary `D:\Hermes-Recovery\live22\bin\hermes.exe`，每一步留 argv／rc／stdout 原文／sha256：

| 步 | 動作 | rc | stdout sha256 前 16 |
|---|---|---|---|
| A | 空 home `plugins list` | 0 | `6fefec6697229249` |
| B | 複製**真實** bundled `disk-cleanup` 到 `<home>/plugins/` 後 `plugins list` | 0 | `33ea8969c563e9b6` |
| B2 | `plugins validate <home>/plugins/disk-cleanup --json` | 0 | `ok: true` |
| C | `plugins remove disk-cleanup`（無 install record） | 0 | — |
| C2 | 移除後 `plugins list` | 0 | `6fefec6697229249`（＝A，位元相同） |
| D | `plugins install disk-cleanup --no-deps` | **1** | — |
| D2 | 安裝後 `plugins list` | 0 | 同 A |

## 量到什麼

1. **`plugins list` 對 home 有反應**：B 與 A 的差異只有一行——
   `│ disk-cleanup │ not enabled │ 2.0.0 │ … │ bundled │` → `… │ user │`，外加一行 `provenance: manual`。
   所以「清單看不到使用者放的 plugin」這個舊說法**不成立**，而「清單可區辨」這次是**用 delta 證的**。
2. **fixture 這次是真的可載入**：`plugins validate --json` → `ok: true`（舊的 fixture 是 `ok: false`＋`nothing to load`）。
3. **移除後回到基線**：C2 與 A **位元相同**（`6fefec66…`）。
4. **catalog 安裝沒做成**：`plugins install disk-cleanup` → rc=1，訊息是
   `Error: 'disk-cleanup' is not in the Hermes plugin catalog and is not a Git URL or owner/repo shorthand.`
   因它是 bundled plugin。真正的 `install` 需要 catalog 名稱／git URL／owner-repo（要網路＋依賴 bootstrap），本次**沒有**執行。

## 我自己在中途又抓到的第二個假測試

第一版把判斷寫成「清單輸出裡是否出現 plugin 名稱」——**空 home 本來就把 `disk-cleanup` 列為 bundled**，所以那個測試永遠為真、不可能失敗。已改成 delta 比對（sha 與逐行 diff），並把這件事寫進 `PLUGIN_PROBE_V2.json` 的 `corrections`。

## 處置

`F6 install leg` = **PARTIAL_MEASURED**：

- 已量到：list 可區辨 user 複本、validate 可載入、remove 回到基線。
- 未量到：真正的 `hermes plugins install <catalog|git|owner/repo>`（需網路＋依賴 bootstrap）→ `NOT_EXERCISED_BY_CATALOG`。
- 因此**不得**再說「install／list／remove 三段可區辨」；能說的是「list 與 remove 兩段已量測，install 段未行使」。

## 檔案

- `wp20/PLUGIN_PROBE_V2.json`（sha `f01efb109aaff069…`，含 `corrections` 區塊）
- `wp20/stdout/_plugin2/{A_list_empty,B_list_copied,B_validate_copied,C_remove_no_record,C_list_after_remove,D_install_catalog,D_list_after_install}.{out,err}`
- 工具：`tools/wp20_plugin_install_probe.py`
