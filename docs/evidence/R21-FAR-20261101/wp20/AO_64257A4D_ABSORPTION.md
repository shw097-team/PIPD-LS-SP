# WP-FHS-20 — AO `deleg_64257a4d` 判讀吸收（PARTIAL）

generated_utc: 2026-11-01T07:20:56Z
verdict: **PARTIAL** · claim_ceiling_recommendation: `AUTHOR_SIDE_LOCAL_SURFACE_SMOKE`（不得把 MEASURED_PASS/12-of-12 當成解除 WP-FHS-20 的依據）

## 我接受的核心否證
**F1（high）軸從未綁定**：54 個 step 正規化後只剩 13 種 argv、2 套程序；step 記錄裡沒有 env/flag/config 欄位；
`home-base` 沒有 `config.yaml`，也搜不到 PREW3/SWOF/STANDALONE。→ 我那 12 格其實是「2 支程序 × 6 個標籤」，
不能支撐任何「模式不影響」或「模式已驗」的陳述。**這是我 v2 的實質缺陷，不是文件問題。**

**F2（high）PLUGIN 惰性無資訊量**：`plugins list` 在三個不同 `HERMES_HOME` 下輸出完全相同（107,390 B、
sha `7470ddb1…`），所以「六格同 sha」在任何軸值下都會成立 —— 舊設計不可能失敗。

**F3（medium）隔離負對照太薄**：探測跑在六個 profile 已被刪除之後，唯一可泄漏的只剩 `wp20_bootstrap`；
且只存 `out_tail` + 自稱的 `leaked_base_profiles=false`，沒有可比對的名稱集合。

**F6（medium）從未真的安裝 plugin**：`home-base/plugins` 是空的，被驗的是活安裝路徑下的內建 `disk-cleanup`。

其餘：F4 四項「無面」只有 GENIE 有命令；F5 SIMPLE_AGENT 有 5 份定義（分類未裁）；F7 分母（5 vs 7）未裁；
F8 無 cell_id 無法 join；F9 PID 重用；F10 只留 tail、sha 不可自驗。

## 逐條處置（v3 已按此改寫並重跑）
| finding | v3 動作 |
|---|---|
| F1 | **不發明綁定**。改量測可綁性：`hermes --help`／`profile create --help`／`plugins --help` 三份輸出落檔＋sha，逐字搜 mode/legacy/prew3/swof/standalone，得 `axis_bindable_on_host` 與 `verdict` |
| F2 | 改成**可失敗**的序列：把 plugin 真的裝進 cell home → `plugins list` 必須**出現名字** → 驗證通過 → 移除後 list **不得再出現** |
| F3 | 隔離探測**提前**到六個 profile 都還在時，並記錄雙邊名稱集合（`names_visible_in_base` / `names_visible_in_iso` / `discriminating`） |
| F4 | 每個「無面」判定都附 command+exit+sha，否則降級 `NOT_MEASURED` |
| F5 | SIMPLE_AGENT 改 `SURFACE_EXISTS_NOT_EXERCISED`（5 份 `~/.claude/agents/*.md`） |
| F6 | plugin 真的寫入 `home-base/plugins/`，`list_before_install` / `list_after_install` / `list_after_removal` 三段 |
| F7 | 分母以數字＋探測輸出呈現，另發 scope ruling（見 `RULING_WP20_KIND_SCOPE.md`） |
| F8 | 由 `matrix.json` 以 (kind,mode,legacy,host="Hermes Agent") join 出 `cell_id_from_matrix` |
| F9 | 不以 PID 單獨識別 step，收據改以 cell+tag+out_sha |
| F10 | 每個 step 的完整 stdout/stderr 落 `wp20/stdout/<cell>/<tag>.out` 與 `.err`，sha 可重算 |

## 保留的否證（AO 要求，不接受翻案）
- 不得把 12 格當成「12 個可區辨的 cell」。`axis_binding=NOT_BINDABLE_ON_HOST` 時，它們是 2×6 重複。
- 不得以 `plugins list` 的 sha 一致性主張惰性。
- 未做任何 provider／gateway／model turn，與 WP-FHS-12 的 RUNTIME_PATH_UNRESOLVED 無關。

## 檔案
- 吸收前：`CELL_RESULTS_R21.json` sha `598dc54b3f97bfa082aa7f2e92e9e8e0fcd080d97444cb3528bad4efe16ca064`
- 吸收後：`CELL_RESULTS_V3.json`（本次產生）、`AO_64257A4D_ABSORPTION.md`（本檔）
