# R5S 回合狀態｜PIPD-LS-SP S4 續辦：preview.4 已發布後的 delta-only 驗證與車道修復

```yaml
schema: R5S-ROUND-STATUS/1
round: R5S-20261015-s4-preview4-verify-close
as_of: 2026-10-15 (+08)
predecessor: R5R-20261014-s4-preview4-focused-close
contract: PIPD-S4-R5-PREVIEW4-PRIVATE-PLUGIN-ROUTEOUT/1（如附件，未重編譯）
subject_repo: https://github.com/shw097-team/PIPD-LS-SP
frozen_subject:
  main_commit: dba4b19456777d3b597fdf71480f6423dd974243
  main_tree: d00175d5aef6e031d282bb018f9a538184c48681
  release: v0.1.1-preview.4（annotated tag 0618d73c… → commit cc6c1930…, 7 assets, 非 draft, prerelease）
  evidence_branch: r5r-evidence-return-20261014 @ 389d9b5a2ffcc2959a3b3ee2c3e67ca644ef9db4
  open_pull_requests: 0
compiler_verdict: PROMPT_COMPILE_NOT_RUN_THIS_SESSION（前回合 R5R 已產生 compiler receipts；本回合依 delta-only 規則未重編譯）
hgk_admission: ADMITTED_READ_WRITE_SCOPED（沿用前回合 WorkOrder/ExecutionBinding；本回合只新增唯讀驗證、隔離 worktree 與本回合 var/ 產物）
claim_ceiling: S4_PREVIEW_MVP_PHASE_TEMP_CLOSED（scoped, temporary）
not_granted: [S4_FULL_PASS, FOUR_HOST_QUALIFICATION, PUBLIC_DIRECTORY, PRODUCTION]
```

## 0. 一句話

`preview.4` 已發布且本回合再次以匿名下載重算全部 7 個資產的 SHA-256（與 GitHub digest 及 `SHA256SUMS` 三方一致）；前一回合把車道全滅誤判成四個獨立症狀的那個錯誤，本回合找到**單一根因**並修復傳輸，並用修好的車道對「已合併、未發布、未複核」的 D1/D2 修補啟動獨立複核；私人 Host 上傳仍是 `HOST_UPLOAD_REJECTED`（未解決、未宣稱安裝）。

## 1. 本回合實際做過的事（含揭露的副作用）

| # | 動作 | 產物 | 揭露 |
|---|---|---|---|
| 1 | delta-only 凍結（重讀 remote main/tags/releases/PR/CI、lane pin、codex 二進位） | `00_freeze/R5S_FREEZE.json` | 無寫入 repo |
| 2 | 車道全滅的**單一根因**定位：launcher 前置檔檢 `ERR_RUNTIME_FILE_MISSING` 因 `config/hermes-codex-lane.json` 的 `codex_executable` pin 指向不存在的 `…\bin\2e5e00daee91c61d\codex.exe`，導致**任何** action（含 `StartOpenCodex`）都中止 ⇒ 10101 relay 從未啟動 ⇒ 所有 Codex 車道回空 | `01_lane/LANE_ROOT_CAUSE.json` | 無設定變更 |
| 3 | 修復傳輸（**未動 canonical 設定**）：以 launcher 自己會下的同一條指令直接啟動隔離 relay | relay pid 19892；`10101` LISTENING；healthz ok | **副作用**：本機多了一個先前沒有的 relay 程序 |
| 4 | 傳輸探針：`VERIFY_SECURITY` rank 3 = `opencode-go/glm-5.3-flash`，`ok=true`、nonce 回聲、usage receipt ok | `VERIFY3/probe_receipt.json` | 該 arm 是前回合宣告的備援 checker，非原宣告 arm（標示為不同 checker） |
| 5 | 獨立複核車道（唯讀、`force-rank 3`、subject = 新 worktree `r5s-verify-wt@dba4b19`） | `VERIFY3/dispatch_receipt.json`、`VERIFY3/verdict_stdout.txt` | **副作用**：新增 worktree `PIPD/worktrees/r5s-verify-wt`（detached） |
| 6 | 匿名 served-byte 重讀：7 資產下載重算 sha256，對 GitHub digest 與 `SHA256SUMS` 三方比對；ZIP 從**下載位元組**再驗（56 members / 1 root / 1 manifest / 8 skills / CRC 全通過 / 無 MCP·Hooks·Apps / 無路徑逃逸），並二次下載確認同 bytes | `03_release/asset_readback_r5s.json` | 無 |
| 7 | 上游對齊（知識庫**唯讀**）：11 份 `PIPD-PKG-00~10` 的 bytes/sha256 盤點 | `landing/UPSTREAM_ALIGNMENT.json` | 未對知識庫做任何寫入 |
| 8 | 看板：`t_562cdedf` 補記最新 host 狀態；修復 DAG 邊 `t_562cdedf → t_d8dab532`（揭露三項自檢） | 看板註記 | 邊的變更已揭露 |

## 2. 車道錯誤的分類（依 CLASS 計數，不按 session 累加）

- **CLASS A `LANE_TRANSPORT_DOWN_CAUSED_BY_LAUNCHER_PRECONDITION_FAIL`**：前回合 4 次（EXECUTE 兩次 `ok=null`＋0 byte runner.log；宣告的 VERIFY_SECURITY arm TIMEOUT 900s 0 bytes；備援 arm 0 bytes），本回合再確認 1 次（修復前 1010x 無 listener）。**同一類、5 次觀測、一個根因**。處置：已修復傳輸並以探針證明（`ok=true`），未以重試掩蓋。
- **CLASS B `HOST_UPLOAD_REJECTED`**：1 次（私人 Host 伺服器端拒絕，客戶端無錯誤碼/回應主體/request id）。未解決；兩顆判別用 ZIP（variant-a 56 members、variant-b 548 bytes）已備，各需一次受同意的人工上傳。

## 3. CK-01..15

| CK | 狀態 | 依據 |
|---|---|---|
| CK-01 Compiler 收據＋HGK 准入 | PASS（前回合） | `.hgk/preflight/R5R-compiler/out/compiler-receipt.json`、`R5R.CONTRACT.json`、`R5R_FREEZE.json.compiler_receipt_sha256` |
| CK-02 凍結最新 main/tag/PR/CI | PASS（本回合再凍結） | `00_freeze/R5S_FREEZE.json`：main `dba4b19`、tree `d00175d5`、無 open PR、preview.4 已發布 |
| CK-03 D1 否定面/scope | PASS（在 main） | `src/pipd_ls_sp/requirements.py` 的 NEGATION/POSITIVE_MODAL/逐段 scope；`tests/test_atomic_requirements.py` 新回歸 |
| CK-04 D2 切句 | PASS（在 main） | `_is_clause_terminator()`：ASCII 字母數字夾住且後接大寫才視為句尾 |
| CK-05 TYPE5 五型別 | PASS（同 PR 完成，非 DEFER） | `schemas/ClaimCeiling.schema.json` + `validate.py` |
| CK-06 allowlist/diff/rollback | PASS | 只動 `src/pipd_ls_sp/`、`schemas/`、`tests/`、`docs/`、`.github/workflows/`；rollback 指向 preview.3 |
| CK-07 全量/聚焦/Trace/wheel clean venv/CI | PASS | 614 tests OK（skipped=4）本地；CI run 38581970291 / public-plugin-verify 38581970365 success；wheelcheck 6/6 typed negatives |
| CK-08 安全負例/假 PASS | PASS | 見前回合 pack；本回合未新增越權行為 |
| CK-09 有界 PR＋合併後 main SHA 讀回 | PASS | PR #11/#12/#13 merged → main `dba4b19`（本回合重讀） |
| CK-10 Tag 指向綠燈 main、四類身分對齊 | PASS（含揭露） | preview.4 tag → `cc6c193`；**揭露：該 tag 早於 PR #12/#13，故 D1b/D2 修補不在任何 release 內** |
| CK-11 ZIP 8/8 Skills、單根、單 manifest、CRC | PASS（本回合從下載位元組複驗） | `asset_readback_r5s.json.plugin_zip_inspection_from_downloaded_bytes` |
| CK-12 served assets SHA256 vs SUMS/ReleaseTuple | PASS（本回合獨立重做） | 7/7 與 GitHub digest 及 `SHA256SUMS`（6 條、無 CRLF）一致 |
| CK-13 README/Install SSOT/User Guide | PASS（前回合） | 前回合 repoint 與 docs 修正；本回合未改文檔 |
| CK-14 私人 Host smoke | **NOT_RUN / BLOCKED（HOST_UPLOAD_REJECTED）** | 見 §4；**不得記為 PASS** |
| CK-15 獨立複核綁定／Owner 發布追認／TT-CR／階段結案 | PASS（有界） | 獨立 checker 在凍結候選 `f4021ae` 上給出四項缺陷；三項已修並合併（PR #13 → main `dba4b19`）；**修補本身的獨立複核已於本回合在 `dba4b19` 上完成**：兩個 checker 車道各 9/9 案例 `CONFIRMED`（見 §4）。Owner 對 preview.4 的發布追認已由已發布的 release 體現；`preview.5` 與私人 Host 仍為 OPEN |

## 4. 獨立複核結果（本回合新完成）

| 來源 | arm | 結果 | 憑據 |
|---|---|---|---|
| VERIFY/SECURITY 車道 attempt 2 | `opencode-go/glm-5.3-flash`（宣告的備援） | 9/9 案例 `CONFIRMED`；附帶說明其套件 rc=1 | `VERIFY3/checker_verdict_armA_raw.txt` |
| VERIFY/SECURITY 車道 attempt 5 | `openai-codex/gpt-6.1-sol`（**宣告的 checker arm**） | 9/9 案例 `CONFIRMED`，附實際 atom 數與極性 | `VERIFY3/checker_verdict_armB2_raw.txt` |
| Orchestrator 量測（同凍結 commit） | 本 orchestrator 的獨立程序 | 11/11 案例 `CONFIRMED`；受測套件 `Ran 35 tests … OK` rc=0 | `VERIFY3/orchestrator_measurement_r5s.json` |

**套件離散已解釋（非受測缺陷）**：兩個車道內的 `unittest` 都回 rc=1（13 errors）；宣告 arm 自己給出原因為 `tempfile.TemporaryDirectory: FileNotFoundError`（唯讀沙箱沒有可用暫存目錄）。本機以**兩個不同直譯器**（pinned `Python311`、Hermes venv）在同一凍結 worktree 各跑一次皆 `Ran 35 tests … OK` rc=0。

**仍未取得**：車道內**套件層級**的綠燈（唯讀沙箱結構上做不到）。此點以「本機两次綠 + 車道逐案例綠」表達，不假冒成「車道全套件綠」。

## 5. 車道與模型一致性（owner 直接提問的答覆，附憑據）

宣告安排 vs 實際服務：

| 角色 | 宣告 | 本回合實際 | 一致性 |
|---|---|---|---|
| PLAN / Orchestrator | `openai-codex/gpt-6.1-sol`（OpenAI OAuth，Hermes 內） | 本 session 服務模型 `deepseek-v4.1-flash`（opencode-go） | **NOT_CONFORMANT**（session 模型是 operator 層設定；未經授權不代改） |
| EXECUTE（bounded writer） | CODEX CLI `opencode-go/deepseek-v4.1-flash` | **本回合未派出 writer 車道**（delta-only，無需產品原始碼寫入；本回合寫入皆為回合證據） | **NOT_EXERCISED**（揭露，不當成功） |
| VERIFY / SECURITY | CODEX CLI checker `openai-codex/gpt-6.1-sol` | 前兩次 pin rank 3（備援 `glm-5.3-flash`），第 3、5 次 pin rank 4（宣告 arm） | **PARTIAL：宣告 arm 已於第三次派出並產出實質 verdict** |

**為何先前看不到 gpt-6.1-sol 的 token 消耗**：本回合前段兩次都 pin rank 3，前一回合唯一的 rank 4 派出是 0 byte timeout；期間該 arm 沒有任何流量。本回合 09:27（attempt 3）與 09:37–09:38（attempt 5）才首次出現該 arm 的列：

- 帳本：`%LOCALAPPDATA%/HG-KSEOS/opencodex-hermes/usage.jsonl`，近 6 小時：`opencode-go/glm-5.3-flash` 107 列、`opencode-go/deepseek-v4.1-flash` 11 列、**`openai-p6a1fe3/gpt-6.1-sol` 10 列**（09:27:11–09:27:26、09:37:31–09:38:23）。
- token 數取自各次 lane 自己的 `turn.completed`：attempt 3 = 41,886 in / 773 out；attempt 5 = 127,492 in / 2,232 out（該 provider 的帳本列不含 token 欄位）。

**已重用既有車道**（未另造基礎設施）：`scripts/hgk-lane-dispatch.py`、`config/lane-route-slots.candidate.json` 的既有排序池、前回合的 `GIT_ASKPASS` 憑證模式、`--codex-executable` 官方覆寫縫、以及 launcher 自己會下的 relay 啟動指令。

**未能照用既有設定之處**：`config/hermes-codex-lane.json` 的 `codex_executable` pin 指向不存在的 `…/bin/2e5e00daee91c61d/codex.exe`，launcher 在任何 action（含 `StartOpenCodex`）之前就 `ERR_RUNTIME_FILE_MISSING` 中止 ⇒ relay 從未啟動 ⇒ 車道全空。**未改動該 pin**（屬 control-plane 變更，留給工具漂移條目），改走官方覆寫縫。

## 6. 未結項與需要 Owner 決定的兩件事

1. **`preview.5` 授權**：`v0.1.1-preview.4` 不可變、且其 tag 指向 `cc6c193`（早於 PR #12/#13），因此 **D1b/D2 修補已在 main、但不在任何 release 內**。發布下一版 preview 需要新的 Owner 授權（preview.4 的授權已用完）。**本回合不自行發布。**
2. **私人 Host smoke**：`HOST_UPLOAD_REJECTED`（UI 存在且可用、伺服器端兩次拒絕位元組相同的封存檔，原因未定）。兩顆判別 ZIP（variant-a / variant-b 548 bytes）已備，各需**一次受同意的人工上傳**；或由 Owner 自行上傳並記錄九步 UI log。**不宣稱安裝成功、也不記為 `NOT_SUPPORTED_FOR_ACCOUNT`。**
3. 其餘：車道 pin 修復（工具漂移）、platform manifest drift、web mount pack、`.hgk/` 倉庫衛生（皆 P2，依 TT/CR 保留）。

