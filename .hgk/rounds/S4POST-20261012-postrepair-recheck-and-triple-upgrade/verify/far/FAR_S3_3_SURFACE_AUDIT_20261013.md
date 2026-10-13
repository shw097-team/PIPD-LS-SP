# FAR 附錄 — §3.3 產品面允許集稽核（R3 輪，實測）

- 性質：maker 側稽核證據；非驗收、非 PASS。
- 稽核者：並行子代理，**其每一項 HIGH 皆由 orchestrator 自行重測後才採用**（見「實測」欄）。
- 來源：藍圖 `§3.3` 最小變更樹（13 NEW ＋ 1 MOD ＋ 2 OUT）vs 分支實況。

| # | 條目 | 子代理判定 | orchestrator 實測 | 處置 |
|---|---|---|---|---|
| S1 | `packaging/public-plugin/assets/{logo,composer}.png` | ABSENT（HIGH） | `assets/` 僅有 `.gitignore`、`icon-128.png` → **確認缺席** | 屬 **owner 輸入 A4**（品牌 icon），已列 `OWNER_ACTION_REQUEST` A4 |
| S2 | `packaging/public-plugin/requirements.lock` | ABSENT（HIGH） | 該路徑不存在；repository 根目錄有一份 `requirements.lock`，其自述逐字：「**NOT HASH-PINNED**. Artifact hashes ... are NOT recorded ... `pip install --require-hashes` will therefore **NOT work** against this file」 | 藍圖 BP-149 已列 `LOCK_REQUIRED`；**與 §7.7 的 `--require-hashes -r packaging/public-plugin/requirements.lock` 步驟直接衝突** → 提請 owner |
| S3 | `packaging/public-plugin/plugin.schema.json` | present_wrong_content（HIGH） | 該檔 `title`＝「PIPD public plugin manifest - locally authored subset」、`$id`＝`https://pipd.local/...`；**官方 vendor schema 實體存在**於非允許集檔名 `vendor-plugin.schema.json`（sha256 ＝ `plugin.json` 所釘 `official_schema_sha256`） | 內容**非**缺失；是**允許集檔名與實際官方 schema 檔名不一致**的形狀偏離。官方 schema 已在樹內 → `REAL_VENDOR_SCHEMA` 比先前記錄更接近閉合；digest 釘選仍屬 **owner 輸入 A2** |
| S4 | `packaging/public-plugin/` 額外 5 檔 | 非允許集（MEDIUM） | `OWNER_INPUT_REQUIRED.json`、`plugin.release.json`、`vendor-plugin.schema.json`、`assets/.gitignore`、`assets/icon-128.png` | 屬 builder 的**拒絕閘模板**與 vendor 副本；記錄，不動（避免破壞 fail-closed 閘） |
| S5 | `plugin.json` 內 `OWNER_INPUT_REQUIRED` 佔位 | §7.5 說不可提交（MEDIUM） | 逐字確認 `publisher.*` 與 `icons[0].sha256` 皆為該字串 | 這是**刻意的 fail-closed 佔位**（builder 拒絕到 owner 供給為止）；衝突在於它同時被提交 → 提請 owner 決定命名 |
| S6 | 以 `main` 為 base 時 `src/**`、`schemas/**` 出現在 deny set | MEDIUM | 以**宣告疊層基底 `52542c3`** 重測：`schemas/`、`src/` 寫入 **0 檔** → 屬 Stage-A 疊層，非本升級 | 已於 `R3_CI_FIRST_RUN.md` §3 量化；屬 owner 決策 D3 |
| S7 | 第二個 workflow `ci.yml` | §3.3 deny set 列 Actions（MEDIUM） | 確認 `ci.yml` 為新增 | 該 workflow 正是裁決 §3.1 **明文批准**的最小 CI；與 §3.3 deny set 的字面衝突提請 owner |

## 實測方法
- `git ls-tree` / `ls` 直接列目錄；`json.load` 讀 schema 的 `title`/`$id`/`description`；`read_file` 讀 `requirements.lock` 全文搜尋 `hash` 字樣；
- 疊層基底比對：`git diff --name-only 52542c3..<tip>` 過濾 `^(schemas|src)/`。
- 子代理另回報 19 項 tasks.md 主張之驗證：**17 SUPPORTED、1 CONTRADICTED（R.1）、1 UNSUPPORTED（R3.R5）**，兩者皆為 maker 自身產物缺陷，已於本輪修正（見 `tasks.md` 的 `R3.corrections`）。
