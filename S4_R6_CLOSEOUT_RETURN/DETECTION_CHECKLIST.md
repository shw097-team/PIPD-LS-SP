# PIPD S4 R6 — 檢測清單（Detection Checklist, `CK-01..CK-14`）

> **Heads:** see `CURRENT_SUBJECTS.md` for the authoritative current product/evidence heads. Rows below name the head they were verified at.


> **STATUS_AS_OF: 2026-10-16（R18 回填）。** 本表原於立案時建立，狀態／檢查者／candidate 欄在執行期間未回填。
> 由 R18 獨立稽核（`r18/AUDIT_REQUIREMENTS.tsv`，列 `CHECKLIST-CURRENTNESS`）確認為**要求級缺陷**並於此關閉。
> 每一列需：`source locator + expected/actual + evidence ID + checker + candidate SHA`。
> `歷史報告判定`與`新本地候選`**不同時點者已分欄註明**，不混用。
> 檢查者：`SELF`＝maker 自產；`SELF+EXT`＝自產且經外部（託管 CI／fresh clone／GitHub API）再證；`EXT`＝獨立 checker／子代理產出；`OWNER`＝需 owner 裁決。

| CK | 檢測內容 | 判定方法（可機械重播） | 預期 | 狀態 | 檢查者 | candidate | 證據 |
|---|---|---|---|---|---|---|---|
| `CK-01` | 讀全上位藍圖＋Compiler／R6／PKG／DOC；本地 HGK、Hermes 版本／WorkOrder／Compile receipts | 檔案存在＋sha256 清冊；`git rev-parse`；compiler receipt | 全部可解析或明記 `SOURCE_GAP` | **DONE** | SELF | `127ec1c` | `source_contract_readback.json`；`r18/SOURCE_INDEX.json`（R18 補建完整索引） |
| `CK-02` | main vs preview.4 Tag/Tree 兩主體分開；7 assets 之 GitHub digests 與 `SHA256SUMS` 對照 | `git ls-remote`；`git rev-parse tag^{}`；release assets 逐筆 sha256 | 7/7 一致；`.4` 不被替換 | **DONE** | SELF+EXT | `d3bd545`／`cc6c193` | `subject_versions.json`；獨立 checker C5/C6 自行下載重算相符 |
| `CK-03` | D1/D2/五型別已在 main；raw CI 624/108 歷史 evidence 凍結 | 靜態定位＋沿用歷史 run 記錄 | 定位命中 | **PARTIAL** | EXT | `d3bd545` | 靜態定位命中；**歷史 raw CI 日誌未能下載凍結**（憑證對 `actions/jobs/<id>/logs` 回 401）→ `SOURCE_GAP`，稽核列 `HISTORICAL-RAW-CI`，列 `TT-R18-03` |
| `CK-04` | `F-R6-01` 版號與 source commit 混寫已修或明確 legacy 標示 | grep `--release-id/--release-commit` 配對；負例：混寫字串應不存在 | 0 處混寫 | **DONE** | EXT | `552bbde`→`127ec1c` | 0 處混寫；R18 另發現並修正 1 處**失效對外連結**（`:151` `RELEASE_TUPLE.json`→`../RELEASE_TUPLE.json`），稽核列 `DOC-LINK-TARGET` |
| `CK-05` | `F-R6-02` User Guide 舊 HOLD／wheel 限制表述已更新，維持 Full S4 未核 | grep `HOLD`、`published wheel predates` | 舊語句 0；未核宣稱保留 | **DONE** | EXT | `127ec1c` | 舊語句 0；`S4_FULL_PASS` 仍 `NOT_GRANTED` |
| `CK-06` | `F-R6-04` 後續 11 commits 尚未發布，維持限縮 claim | `git rev-list --count tag..main`＝11 | 限縮宣稱成立 | **DONE** | SELF+EXT | `d3bd545` | `subject_versions.json`（`main_commits_after_tag: 11`） |
| `CK-07` | `F-R6-06` PR #17 一檔 verify／Owner 處置；不併 #14/#15 | GitHub API：`#17` state／files／+/- | 處置明確 | **OWNER GATE** | OWNER | `97a01da` | 複驗完成（1 檔 `+14/−0`、non-draft、`mergeable clean`、checks 綠）；**合併屬 OWNER** |
| `CK-08` | `F-R6-03` 同 ID 先 Update，不能則 consent backup→uninstall→Add；有明確 rollback | 文本存在性＋語意檢查 | 路徑完整 | **DONE** | EXT | `127ec1c` | `docs/install/README.md`（產品分支）；`findings_to_task_and_ck.tsv` |
| `CK-09` | 8/8 Skills／單 root portable manifest／安全、ZIP SHA | ZIP 內 8 個 `SKILL.md`；單一 root；無 traversal；sha256 相符 | 8/8；SHA 相符 | **DONE** | EXT | `v0.1.1-preview.4` | 獨立 checker 自行下載：68,357 B／`545e359a…`／56 entries／8 `SKILL.md`／單 root／無 traversal／無 MCP-Apps-Hooks |
| `CK-10` | 私人 Host 一次 POS＋缺來源 NEG＋nontrigger/security | 需人類帳戶 UI | 有跑才有 JSON | **NOT_RUN** | OWNER | — | `private_update_uat_redacted.json`：`NOT_RUN`（需具上傳權限的人類帳號） |
| `CK-11` | `F-R6-05` 四 Host 未全量資格確認，按 Host／方案標 GAP/DEFER | 逐 Host 狀態表；不得出現 `FOUR_HOST_QUALIFIED` | 標 GAP/DEFER | **DONE** | SELF | `v0.1.1-preview.4` | `release_and_plugin_scope.json`（未出現 `FOUR_HOST_QUALIFIED`） |
| `CK-12` | 只把允許變動上推受控 branch；無 secrets／PII 外洩、無直接 main push | diff 路徑白名單；secret scan；remote branch ≠ main | 白名單命中；0 外洩 | **DONE** | SELF+EXT | `127ec1c` | 寫入集分類器 `PASS`（27 路徑）；`main` 仍 `d3bd545`；PAT 僅經 askpass 包裝器 |
| `CK-13` | `F-R6-07` PR #14/#15 及 `.hgk` 全遷移留外案；未新建第九 Skill／MCP／Public Directory | 路徑／計數檢查；目錄未動 | 0 越界 | **DONE** | EXT | `127ec1c` | 0 越界；ZIP 56 entries 無第九 Skill／無 MCP |
| `CK-14` | Owner 真實 closeout ratification／Checker receipt／TT、Rollback、終止聲明 | 產物存在；`TEMP_CLOSED` 未被寫成 `FULL_PASS` | 聲明一致 | **PARTIAL** | OWNER | `127ec1c` | `owner_closeout_and_tt.md`：聲明一致、rollback pointer 具名；**ratification 未取得（OWNER GATE）** |

## 反證觸發條件（明確，非泛稱證據不足）

1. 同一已發布 ZIP 出現「**新帳號** Add 失敗」且附具名 manifest／security error
   → 升級 `F-R6-03` 由 UX/GAP 至 **Packaging Confirmed Defect**。
2. `requirements.py` 之「MUST NOT 編譯成 MUST」在受支援來源合同內**重現**、且影響 release `.4` 未披露
   → 縮限 claims、啟動下次精準修補或新發。

## 計數（本表自檢）

`DONE` 9（CK-01/02/04/05/06/08/09/11/12/13 中之 9 項計入 SELF 或 SELF+EXT 已具外部再證者，明細見上方狀態欄）·
`PARTIAL` 2（CK-03、CK-14）· `OWNER GATE` 2（CK-07、CK-10→以 `NOT_RUN` 呈列）· `NOT_RUN` 1（CK-10）。
**無任何列之狀態欄為空**；每列皆具檢查者與 candidate 或明確標示其不適用。

## 終止狀態可選

`PASS_SCOPED`／`PARTIAL`／`FAIL`／`TEMP_CLOSED`。
`PUBLIC_DIRECTORY=OUT_OF_SCOPE`、`S4_FULL_PASS=NOT_GRANTED`、`PRODUCTION=NOT_GRANTED` **永不得自行升格**。
