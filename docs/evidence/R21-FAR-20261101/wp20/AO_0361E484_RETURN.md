# AO deleg_0361E484 回件（S3c）：WP-20 v3.1 ＋ Kind 裁定的獨立重坐

- 回件時間：2026-11-01 15:34Z 派出、25m07s 完成（`deleg_0361e484`，34 api calls）
- 判定：**PARTIAL** — 8 條關閉、3 條殘留、1 條（F11）從未被寫出
- 這份文件只做兩件事：記錄 AO 說了什麼，以及**我自己用命令重測了哪幾條**。沒有把 AO 的敘述當成已驗事實。

## 1. AO 的處置清單

| finding | AO 判定 | 依據（AO 指出的位置） |
|---|---|---|
| F1 軸可綁性 | CLOSED（撤回 BINDABLE，非子字串誤判） | 69 份 help 全掃，`standalone/prew3/swof` 0 命中；`legacy` 只出現在 `migrate-legacy` |
| F2 plugin 惰性 | CLOSED IN SUBSTANCE（測試現在可以失敗） | 保留的 `pl_list_before/removed` 對照可見 user-source plugin 進出 |
| F3 隔離太薄 | CLOSED | mtime 15:20:47 base 6 profile → 15:20:51 iso 只剩 default，之後才第一次 delete |
| F7 分母算術 | CLOSED（算術） | 4＋1＋3＝8 kinds，與 `WP20_KIND_SCOPE.json` 一致；「7」「5」皆撤回 |
| F8 cell_id join | CLOSED | 12/12 對上 `C:/wg/queue/WP-FHS-20/output/matrix.json` |
| F9 PID 混用 | CLOSED | `CELL_RESULTS_V3_1.json` 無 `pid` 字樣 |
| F10 證據可重算 | CLOSED（僅 54 個 cell step） | 54/54 out_file＋sha＋bytes 全對；**輔助區塊不在此列** |
| F4 三種無面 | **REMAINS** | 兩個負面處置仍是散文＋null sha；PROFILE 引文其實是 generator 的 `or` 預設字串 |
| F5 SIMPLE_AGENT | **REMAINS** | 5 份是 opencodex 路由 subagent，未證明是 SIMPLE_AGENT 種類或可載入 |
| F6 未安裝 | **REMAINS** | 安裝的 fixture 自己 `{"ok": false}`（`nothing to load`），`validate_installed_rc=1` 卻仍輸出 `can_discriminate=true` |
| F11 | **NOT DISCHARGED** | 11 條裡有一條從未被寫出：`wp20_cells_v3.py` 與 `AO_64257A4D_ABSORPTION.md` 只列到 F10 |

## 2. 我獨立重測的 4 條（AO 的新發現，不採信也不否認，先量）

### N1 引用的 sha 在磁碟上不存在 — **CONFIRMED**

```
$ sha256sum stdout/_plugin/pl_list_before.out stdout/_plugin/pl_list_after.out stdout/_plugin/pl_list_removed.out
0b8391377785a90e…  pl_list_before.out
0b8391377785a90e…  pl_list_after.out      ← 與 before 位元相同
d9dc9435ad82c37f…  pl_list_removed.out
$ grep -rl "9d1c54ec0d9eab29" .
./CELL_RESULTS_V3_1.json                  ← 只出現在 JSON 自己裡面
```

結論：`CELL_RESULTS_V3_1.json` 的 `plugin_real_install` 區塊所引 `9d1c54ec…/107669 B` **沒有任何檔案可對應**，且保留的 before/after 位元相同（安裝什麼都沒改變）。**這一塊的宣稱撤回。**

### N3「69 個動詞」不是主機的命令集 — **CONFIRMED（數字修正）**

```
$ # root_help.txt 解析 vs KIND_SURFACE_PROBE.json
root_help verbs: 68 | probed: 69
unprobed: ['browser', 'codex-runtime', 'migrate', 'profile']
probed-not-command: ['branches', 'firewall', 'schemas', 'server', 'settings']
```

AO 說 69 vs 69（5 個替換），我量到的是 **68 vs 69**：4 個真命令沒探、5 個不是命令的被探。兩邊都證明同一件事——**動詞數是湊巧相同**。分母撤回，改由 root_help 解析。

### N4 `gateway install` 打臉 AGENT_OS／AI_SYSTEM 的「無面」 — **CONFIRMED**

```
$ grep -nE "^\s+install\b" kind_surface_probe/gateway_help.txt
16:    install             Install gateway as a systemd/launchd background
$ # KIND_SURFACE_PROBE.json 的 install_capable_verbs（18 個）
['acp','bundles','computer-use','curator','egress','gateway','lsp','mcp','memory','pets','plugins','security','send','setup','skills','tools','uninstall','update']
```

`gateway install` 是 OS 服務安裝器，且在探測自己的 `install_capable_verbs` 裡；裁定卻引 `acp` 說「69 個動詞沒有一個安裝作業系統 runtime」。**AGENT_OS／AI_SYSTEM 的 `NO_SURFACE` 撤回，待重判。**

### F11 從未被寫出 — **CONFIRMED**

```
$ grep -o "F[0-9]\+" wp20/AO_64257A4D_ABSORPTION.md | sort -u | tr '\n' ' '
F1 F2 F3 F4 F5 F6 F7 F8 F9 F10
```

11 條裡只有 10 條有文字，F11 沒有正文、沒有吸收記錄、沒有反證。最多只能聲稱 10 條，其中 7 條關閉。

## 3. 立即撤回的宣稱

1. **「plugin 安裝／列出／移除三段可區辨」** → 撤回。引用的 sha 不存在，保留的 before/after 位元相同，安裝的 fixture 連自己的 `loadable` 檢查都沒過。
2. **「69 個動詞逐一 `--help` 存證」** → 撤回分母。改為「root_help 解析出的 68 個命令」，並另行記錄 5 個非命令項。
3. **AGENT_OS／AI_SYSTEM／GENIE 的 `NO_SURFACE`** → 撤回，待以 root_help 分母重判（`gateway install` 必須列入）。
4. **SIMPLE_AGENT** → 維持 `UNCLASSIFIED`；5 份檔案是 opencodex 路由 subagent，不構成 SIMPLE_AGENT 證據。
5. **AO 11 條全吸收** → 改為「10 條有文字，7 條關閉、3 條殘留；F11 從缺」。

## 4. 已開始的補救

- `tools/wp20_kind_reprobe.py`：改以 `root_help.txt` 解析出的命令集重探（同一支 binary `D:\Hermes-Recovery\live22\bin\hermes.exe`），逐命令留 rc／bytes／sha／help 原文，並把「舊探測多探／漏探」寫進 `KIND_SURFACE_PROBE_V2.json`。
- 待做：plugin 安裝區塊以「保留 stdout ＋ 每步 rc／sha」重跑（安裝必須用 `hermes plugins install`，不得用 Python 寫檔假裝安裝）；SIMPLE_AGENT 的分類要嘛量到載入、要嘛標 `UNCLASSIFIED`。

## 5. 天花板

AO 的判定本身也是 self-report；本文件只採用「我用命令重測過」的那 4 條（N1／N3／N4／F11）。其餘 N2／N5–N8 與 F4／F5／F6 的細節尚未逐條重測，一律記為 **AO_REPORTED_UNVERIFIED**，不得當成已確認缺陷，也不得當成已排除。
