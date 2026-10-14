# PIPD-LS-SP S4 修補後外部獨立複驗暨三合一小型升級實作驗收

**Report ID**：`PIPD-S4-EXT-ACCEPT-R3-20261013`  
**日期**：2026-10-13，Asia/Taipei  
**Repository**：https://github.com/shw097-team/PIPD-LS-SP  
**角色**：External Independent Challenge Reviewer；讀取／證據分析／報告，不是 Maker、Repo Owner、Release Owner、Portal Publisher。  
**方法**：Source-Bound、Subject-Frozen、Clean-Room 意圖、Negative-First、Raw-Evidence-First、Fail-Closed。  
**正式結論**：**`FAIL_CHALLENGE`（目前 R3 候選之 S4/升級合併 Gate）／`TEMP_CLOSED`（跨宿主、公開 Portal 與完整 S4 簽收）／`NO_MERGE`／`NO_PUBLIC_RELEASE`**。

> 此份 Markdown 為本次新的外部獨立工程驗收報告，不是 `challenge-review` 技能所規定、由其內附 canonical validator 產生的 `EXTERNAL_CHALLENGE_REPORT.json` 與其 digest-bound Markdown 雙檔包。因技能所引用的 `references/`、`scripts/`、`assets/` 未在本次輸入形成可執行的同一完整套件，故本報告不冒稱通過該工具的 bundle validator。

---

## 0. 執行範圍、實際完成與限制

### 0.1 本輪確實完成

1. 對本地已掛載 Markdown 以嚴格 UTF-8 完整讀入並重算 SHA-256；共 **93 份** Markdown 可讀，含 `00`–`19` 20 份 KP、`challenge-review-SKILL.md`、11 份 `PIPD-PKG-00..10`、`PIPD-LS-SP_skeleton.md`、`PIPD_LS_canonical_standard.md`、`PIPD_LS_DOC-00..09`、主藍圖、上一輪外部報告及新上傳的三合一 R2 藍圖。讀取所有位元組／建立清冊 **不等於對巨量上游所有原子條文逐一語義驗收**。獨立全檔位元組清冊：`session_input_inventory_2026-10-13.json`。
2. 用使用者指定之 GitHub 連接器重新列舉 `main`、**11 個分支**、**3 個發行 Tag**、發行資產、PR #2、Git Tree、R3 檔案、CI Workflows、實際 Workflow jobs 及其 raw log。各涉及的 GitHub Git Tree 回傳 `truncated=false`。
3. 以 GitHub 比較 API核對 `main...R3` 的 Git 歷史和變更清單，並直接檢視 R3 的 README、`docs/install`、Plugin 封裝、Schema、tests、CI 與獨立 checker 收據。
4. 從 GitHub Actions **原始 Job 日誌**重建最新兩個 Workflow 的結果與實際測試結尾，不依賴綠色 UI badge。
5. 核對三合一 R2 藍圖 A01–A42、F01–F14、UPG-P01–P04、UPG-G00–G09、TR-01–40 的適用性、要求與證據上限；檢核前輪 F001–F003、G004–G006、O007–O009 是否可結案。

### 0.2 未實際完成／不得推論為 PASS

- 本執行容器無法解析 `github.com`（`git ls-remote` 回報 `Could not resolve host: github.com`），所以**沒有**獨立 clone R3 程式、在此容器執行 Python 全量測試、直接下載 ZIP/Wheel byte-by-byte hash、做乾淨環境釋出版重建。GitHub Job 的原始日誌是本輪獨立檢視的遠端執行資料，非本驗收官親自 rerun。
- **沒有**實際操作 Web GPT-6 Plus/Free、Hermes Agent Native Skill、Codex Desktop、Codex CLI Native Skill discovery、Claude Code、OpenAI Plugin Portal 的正式實裝/上架。Repo 既有 UAT 收據只在被檢視之 exact subject/scope 生效。
- 沒有修改候選、Source、Schema、測試、Oracle、Evidence Pack、Workflow、PR、Tag 或 Release；不具備合併、上架及 Production 授權。

### 0.3 權威順序與設計上限

- **上游**：`PIPD-LIFECYCLE-SPEC@1.1.0`（`PIPD_LS_canonical_standard.md`）、DOC-00..09（特別是 DOC-07 TQAEP、DOC-08 權限／宿主／發行）；主藍圖 `PIPD-LS-SP_藍圖.md §8.3、§15.2、§15.3`、EC/SGM 總藍圖；PKG-00..10（特別 PKG-06、PKG-07 Part7–8、PKG-08 Part11）。
- **地方契約**：`00_KNOW_INDEX..19_KP_INDEX_CROSSWALK`；`challenge-review-SKILL.md §Invariants, §Workflow, §Safety and permissions`。證據 `GPTB-KP11-R01/R03/R06/R08`、回歸 `GPTB-KP12-R01/R03/R06/R07`、發行 `GPTB-KP16-R01/R02/R03/R05/R07/R08`、UX `GPTB-KP17-R01/R02/R05/R08`、TT `GPTB-KP18-R01/R05/R07/R08`。
- **本輪三合一範圍**：上傳 `PIPD-LS-SP S4｜三合一小型升級藍圖(1).md`，ID `PIPD-S4-TRIPLE-UPGRADE-BLUEPRINT-20261012-R2`，§§0.1/3.2/3.3/5.1/6/8/9/10/11/12；**不新設 S4.5**、不創第九 Skill、不新加 MCP/Actions/Hooks、不把 build、host load、portal、published、S4 Full PASS 混為一談。
- **歷史受驗**：`acceptance_reports/PIPD-LS-SP_S4_修補後外部獨立複驗與MVP必要性裁決_2026-10-12.md`，SHA-256 `2ceecbad26e5189637faa104cbeb443087ae8c35a398dce72aaecf0e81a9bf39`。歷史結果是挑戰輸入，不自動帶入最新 R3。

---

## 1. Frozen subject 與 GitHub 現況

| Item | 2026-10-13 GitHub 讀回 | 驗收解釋 |
|---|---|---|
| default `main` | `224591431a164ab72a9423cd180e417e8a762403` | 已公開的既有主線，不是 R3 |
| `main` Git tree | `1a9fcb94a42eb589e405c2453793be986419d4cb` | Git commit API tree |
| R3 `feat/s4post-triple-upgrade-20261013-r3` | `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` | 本輪最新候選 |
| R3 Git tree | `2875287352529ee92277d7dc4f37cd12ffc977c7` | 由 Git commit API 核對，不以 recursive-tree URL 顯示值冒充 tree SHA |
| R2 `feat/s4post-triple-upgrade-20261012-r2` | `d3bb4e92f00b256f1ba6abeaba7049113c00cedb` | 歷史分支，勿合併當前 R3 主題 |
| 舊修補分支 | `eef951acdfe0e2b4d93dde7732d264441d9bd674` | 歷史 F001/F002 修補分支 |
| 主線 vs R3 | `ahead_by=94, behind_by=0`, **217 files changed** | Git 歷史可 fast-forward ≠ Gate PASS |
| Draft PR #2 | https://github.com/shw097-team/PIPD-LS-SP/pull/2 | `draft=true`、`mergeable=true`、`merged=false`；42,513 additions，34 deletions |
| 目前 Releases | `v0.1.0-preview.1`、`.2`、`v0.1.1-preview.3` | 沒有 R3 的新 Public Plugin 發行 |
| 最新 Preview Wheel | `pipd_ls_sp-0.1.1a3-py3-none-any.whl`, digest `e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec` | 已發布的舊 Wheel，不是 R3 修補 Wheel |

R3 tree 有 `.github/workflows/ci.yml`、`.github/workflows/public-plugin-verify.yml`、`packaging/public-plugin/`、`docs/install/README.md`、`docs/install/PIPD_AGENT_INSTALL_PROMPT.md`、三個 exporter/freeze 工具、二個新測試模組。**先前「所有分支都沒 CI」的歷史判斷已失效**；`main` 仍無上述兩個 workflow，但 R3 已有。

**GitHub PR #2 body 自述**：仍是 Draft／Candidate，最新獨立裁定 `FAIL_CHALLENGE`，不要直接 merge 到 main。此種自限和本輪 raw CI 結果一致。Branch 可技術上合併不表示准予合併。

### 1.1 公開 Preview 的 F001/F002 追蹤

- **F001 Web Mount stamp**：目前 `main` 八份 Mount 文件皆已改以正確 preview.3 Tag Commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a` 標示，GitHub 發行資產 metadata Web ZIP SHA-256 `af342d281f02ba04f284a1625f4a58a6f2de15549cc182a0c61ce357ec6b504f`。但 Tag tree 保留舊檔、伺服器後續曾在同 Tag 重新上傳，現行安裝文件亦明示 Tag 原始內容與目前 served bytes 不能從同一原始 Tag tree 再現。**現有宣告不等於未修復舊戳；新 immutable release 的來源/資產閉合仍待 Owner。**
- **F002 Trace false PASS**：R3 source `schemas/TraceLink.schema.json`、`schemas/PI-PKG.schema.json` 與 `src/pipd_ls_sp/validate.py` 包含修補，測試 `tests/test_s4ext_trace_closure.py` 存在且 R3 CI log 大量案例通過。但 preview.3 已發布 Wheel 仍是前一版 byte identity，**不繼承新 source 修補**。發布前須重建新 Wheel、套件安裝後執行 legal/wrong-type/orphan/wrong-hash 正反例；絕不可重貼舊版 digest 冒充 R3 發行。
- **F003/Profiles**：R3 有 release provenance、profiles 邊界測試；本輪不建議全面收緊 `version`/`subject_id`、全面更換 Schema 或重做 profile engine；只處理實際 red case 與影響範圍回歸。

---

## 2. 本輪獨立關鍵發現：CI「綠燈」與原始測試矛盾

### `S4R3-F001` — `CONFIRMED_DEFECT`，P0，S4 Gate-blocking

**查驗主體**：R3 `e71fee6d...`；GitHub Actions `ci` run `38341318079`，Job `115112781888`。  
**原始入口**：https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38341318079  
**Workflow source**：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/.github/workflows/ci.yml

GitHub API 此 Job 的 `conclusion=success`，但 Job 原始 log 明載：

```
Ran 572 tests in 48.136s
FAILED (failures=11, skipped=6)
...
Ran 108 tests in 6.665s
FAILED (failures=2)
```

`ci.yml` 的「Full unittest suite」與「Focused S4 repair / closure suites」使用 `python -m unittest ... 2>&1 | tee <log>`，在相應步驟未啟用 Bash `pipefail` 或顯式保存第一個程序 RC；pipe 的退出碼取自 `tee`，成功寫日誌掩蓋測試失敗。這是具可定位 source、log、job verdict 的 **False-Green CI / Gate Calibration Failure**；不是單純 flaky warning。

**至少 11 個失敗的類別**（均見上述 run raw log，非我們自行執行）：

- `tests/test_negative_and_rollback.py`: Windows 形式 `C:/Windows/system32/x.dll` 未觸發預期 `RepairScopeFail`；這需要跨平台路徑威脅模型實測，不可直接忽略。
- `tests/test_s4ext_first_run_portable.py`: `run.sh` 不是 executable；PowerShell `run.ps1` 從外部 CWD 執行 `Cannot bind argument to parameter 'Path' because it is null.`；**直接碰觸新使用者的 First-run UX**。
- `tests/test_skill_contracts.py`：多個測試原本要求 typed refusal，但實際得到 `TOOL_MISSING / PyYAML is required to load tests/cases.yaml`；顯示 runner 依賴與真正檢測的拒絕目的混淆。`pyproject.toml` 宣告 runtime 依賴 `jsonschema>=4.0`，未宣告 PyYAML。應決定 PyYAML 是 test-only 依賴、改用 stdlib fixture、或實際 runtime 依賴；以清晰閉合的最小路徑處理，不能跳過負例。
- `tests/test_tooling_executes.py`: CLI smoke fail；須看 trace 和 environment 後最小修補。
- `tests/test_web_fallback.py`: symlink destination 負例測試出現 `a refused build must not leave a destination behind` 之 assertion failure；需釐清 symlink `exists()` 跟 `lexists`／`is_symlink()` 語意及 sentinel byte 保護，不得只以修改 expected code 讓其綠燈。

**最小必要修補**：將 CI 流程中每個真測試 step 使用 `set -euo pipefail`，或 `PIPESTATUS[0]`／明確 shell exit 捕捉，將實際失敗的測試與失敗 Job 顯示紅燈。針對反例／刻意期待 nonzero 的 mutation steps 另保留正反 first-fail 的確認，避免把預期拒絕變成無法通過的 CI。於同一 fresh runner 重跑全量＋聚焦 suite、Wheel isolated install、負例，並核對 `test exit == job conclusion`。**禁止藉降低測試嚴格性、只跑 subset、skip failing files 或更改驗收 oracle 解除阻塞。**

**Owner**：CI/DEV/TQAEP Owner。**Retest**：`ci` workflow same frozen Commit 的完整測試 raw log、RC、status，外加 injected negative control「讓一個測試刻意失敗→Job 必須失敗」。**Affected regression**：全量 Suite／Quickstart／Skills 型別拒絕／Windows 路徑／symlink 安全／Trace closure。

### `S4R3-F002` — `CONFIRMED_DEFECT`，P0，三合一 Upgrade Gate-blocking

**查驗主體**：R3 `e71fee6d...`；`public-plugin-verify` run `38341318074`，Job `115112712475`，**`conclusion=failure`**。  
**原始入口**：https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38341318074  
**Workflow source**：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/.github/workflows/public-plugin-verify.yml

首個變更範圍 Gate 對 `main` 計算：

```
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/verify_evidence_digests.py
WRITE_SET_VIOLATION (base 224591431a164ab72a9423cd180e417e8a762403)
Process completed with exit code 1
```

後續「三個工具 Python 編譯」、「stdlib-only」、「兩個新 Test Module」、「全量 unittest」、「Release identity negative」、「fallback byte drift negative」均 `skipped`。故**不能稱 R3 三合一在 GitHub Hosted CI 已整套通過**。

根因有兩層：1) 目前 PR 把 Stage A / 修補、Stage B 三合一和大量 `evidence/.hgk` 變更堆在一個跨 94 Commits 的差異；2) Stage B allowlist 只准三合一的窄 paths，對 `main` 的較廣差異天然拒絕。較早獨立 checker 也查到改用宣告 stacked base 仍有 `.github/workflows/ci.yml` 和 4 個 gitlink 移除等 **5 個**違反項，故不得把原因簡化成「改 base 即全綠」。

**最小必要修補**：依核准 Stage A→Stage B 的責任邊界，分開合併前「修補性來源差異」與「三合一發行投影差異」兩套 allowlist／base，並在 PR 中列出精確 `diff --name-status`。可透過兩個有順序、各自可驗證的 PR（原藍圖 ONE CHANGESET 下的受控分段），或由 Owner 重新批准一個完整的 integrated allowlist + 純淨 candidate branch；**不可為求綠燈直接把任意 `tools/**`、`src/**`、`schemas/**` 加入三合一 UPG-G01 允許集**。修完仍需 fresh independent check。

**Owner**：Repo Owner + Stage A Repair Owner + PKG07/08 Upgrade Owner。**Retest**：兩個 Base 分別重建 affected diff，Stage B `zero core writes`，全部 CI 步驟實跑且為綠、負向新增 forbidden path 確實被拒。

### `S4R3-F003` — `EVIDENCE_GAP`，P1，Public Plugin／Host

目前 `packaging/public-plugin/` 有正式形狀的 manifest、vendor-schema pin、八個 `derivations.json` 與 Owner Supplies 記錄，`tools/build_public_plugin.py` 有 stdlib-only exporter、typed refusal、測試。R3 紀錄一項本地組包 `BUILT`，可見 synthetic / local checker 進步；然而:

- 原 checkout **沒有**實際批准的品牌 PNG（gitignored），須先 `--generate-icons` 才有本地測試圖示；不含此 flag 的指定建構命令由獨立 checker `REFUSED ICON_MISSING`。此前置條件必寫入單一官方 Runbook。生成占位圖≠真人批准商標。
- R3 `OWNER_SUPPLIES_DELIVERED.json` 明示 publisher identity 來自 Repo Owner 資料推導，**非真實人類 Portal publisher 驗證**。官方 vendor validator、Portal Scan／Review／Publish、新 Plugin release tag、Plus/Free 實帳號載入均 `NOT_EXECUTED`。
- 先前 R3 官方驗收車道對 `389d3973...`、`5351c5...` 均為 `FAIL_CHALLENGE`；其後 Maker 對文字/量測的更正不能回寫前述裁定，最新 `e71fee6d...` 亦沒有獨立新 PASS 加本輪完整 Gate 封閉。
- R3 現有功能正常與否不能只由自編 `validate_subset()` 推定 vendor/Portal 相容性；必跑被釘選且獨立確認的官方 Validator、正負例及 Portal scan。

**Owner**：PKG07 Build / Human Publisher / Host UAT。**Disposition**：本地候選可續驗，公開發行 `HOLD`；不准發行已裝備完成宣稱。

### `S4R3-F004` — `EVIDENCE_GAP`，P1，README / First-run

R3 README 已放兩條 Route，新增 `docs/install/README.md`（170 行）與單一 Agent Prompt（86 行）且公開承認沒有 Directory Listing。這是**實質實作**，而非紙上規劃。但 `README.md` 仍約 **366 行**，前段說 `docs/install/README.md` 是唯一安裝 SSOT，後段仍重複 Shell／PowerShell 長版指令、Wheel 及過往版本，初學者會同時看到 Web、Agent、CLI、Web Mount 的多個實作入口；其中 `preview.3` 曾被簡寫為「Use .3」，但其 Wheel 已知 Trace false PASS。應按真實最新可用能力精準標示 Preview、已知缺陷和使用情境，不以一句版本推薦遮蓋危險。

R3 docs 說 Web 當下可下載「單一 `PIPD_WEB_FALLBACK.md`」，但 Git Tree **未發現可直接下載的成品 `PIPD_WEB_FALLBACK.md`**；僅有 generator `tools/build_web_fallback.py` 和手動 build 指令。對「沒有 Shell 的 Web 新手」目前仍缺一個**實際可取得的單檔入口**。

**Owner**：DX/PKG07；**Disposition**：需同步 README/UI 與可用產物，見 §5。

### `S4R3-F005` — `NON_BLOCKING_OBSERVATION`／範圍式 Hygiene

本輪 R3 Git Tree 靜態計數：**1,638 個 blob，約 64,956,563 bytes**（Git Tree metadata size）；其中 `.hgk/` **1,226 個 blob，約 61,822,185 bytes**，佔顯示 blob 大小約 **95.18%**。`dist/` 約 41 個檔，含舊版本 Wheel/ZIP。未見 `.github/CODEOWNERS`、`CODEOWNERS`、`CONTRIBUTING.md`、`SECURITY.md`、`CHANGELOG.md` 或明確獨立 user guide。這不是聲稱所有檔案都是垃圾，更不能刪掉 checker raw evidence；但產品入口與數十 MB 的歷史證據長期混雜增加 clone 成本、版本溯源與新使用者負擔。

另 PR #2 有 `42,513 additions/34 deletions` 且將 Stage A 安全修補、S4 core typed trace、Stage B 派生封裝與 round evidence 聚合於同一 PR。建議清理**將來的發行界線與檔案布局**，不要回溯砍除現有歷史證據以製造一個看起來乾淨的 PASS。

---

## 3. 原三合一藍圖實作後十 Gate 獨立裁定

來源：新上傳 R2 Blueprint §§0.1、3.3、6、9.1、9.2、10.1。狀態若檔案存在而沒有本輪執行測試，不得由存在推論功能通過。

| Gate | R3 觀察 | 判定／原因 |
|---|---|---|
| UPG-G00 SOURCE_FREEZE | commit/tree 可固定；source/frozen ledger exists，歷史來源層次清晰 | `PARTIAL`：完整正式 candidate tuple/new release 未封閉 |
| UPG-G01 SOURCE_IMMUTABLE | R3 有 217 個相對 main 變更，含 `src/`、`schemas/`、`skills` 未見列入；workflow blocked | **`FAIL`**：Stage B vs Stage A 分層未解釋清楚，正向 allowlist Gate fail |
| UPG-G02 EXACT_SKILLS | 原始 8 Skills，每個 6 檔，derivations 八份 | `PARTIAL`：Repo/source 數與歷史 checker 可見；正式 bundle完整驗收仍欠 |
| UPG-G03 SEMANTIC_PROJECTION | 專用 exporter、derivations、逐檔 SHA；歷史 checker 正向 | `PARTIAL`：R3 host behavior / official skill validator 未證 |
| UPG-G04 PACKAGE_FORMAT | vendor-schema byte pin、tests、PNG generator；published public plugin 無 | `TEMP_CLOSED`：正式 vendor/Portal scan、品牌圖核准缺；workflow未跑完 |
| UPG-G05 RELEASE_PROVENANCE | 歷史 F001 已做更正；R3 source freeze 及 release tools 存在 | `TEMP_CLOSED`：新不可變 release/asset byte independent readback 缺 |
| UPG-G06 SKILL_BEHAVIOR | Codex CLI 歷史 4 probes 有部分正向，且模型替代／transport 不一致 | `PARTIAL`：非 8/8 per-host POS/NEG/EDGE/SEC+nontrigger |
| UPG-G07 WEB_CONSUMER | 目前是文件備援，沒有 Public Listing；單 MD 成品未提供 | `TEMP_CLOSED`：Plus/Free 真實可用性、文件完成上傳、第一任務成功缺 |
| UPG-G08 AGENT_CONSUMER | Hermes、Codex Desktop GUI、Codex CLI、Claude 安裝 Prompt 有；Host UAT 紀錄不完整 | `TEMP_CLOSED`：4 Host 各自 discovery/permission/rollback 無完整 fresh receipt |
| UPG-G09 PUBLIC_RELEASE | portal developer human、review、Publish state 未完成 | **`HOLD`**：禁止從 Build 推導已發行 |

**MVP 工程結論**：三合一的 *source/design/build 工具層* 已明顯向前進展；因存在實際 CI 失敗、False-Green 及 Host／Portal 缺口，不具正式 BUILD_PASS、PUBLIC_PUBLISHED、S4_FULL_PASS。

---

## 4. 四項指定決策：高度必要性 + 避免 Overengineering

### 4.1「是否可以將目前分支整合進 MAIN？」

**裁定：`CONDITIONAL_APPROVAL_OF_INTEGRATION_STRATEGY / CURRENT_MERGE_NO_GO`。**

- 技術面：PR #2 `mergeable=true` 且 R3 比 main ahead 94/behind 0，**不是**強制解讀為 Merge Gate 通過。
- 品質面：F001 CI False-Green、F002 Public-plugin verifier Red，現階段 `NO_MERGE`。R3 開發者和 PR 文字本身亦仍承認 `FAIL_CHALLENGE`、`HOLD`。
- 建議：**不要把全部 11 個分支逐一合併**；多數是過去修補、證據及實驗分支。Owner 先建立唯一經授權 integrated candidate identity，分離 Stage A 安全/核心修補與 Stage B Public distribution 允許集；可受控合併成一個 final PR 或按先後順序兩個 PR，各自全量/負向驗收。歷史分支標記 superseded，未獲 Owner 許可不刪。
- 必要放行先決：一個清楚來源 commit/tree、Stage A/B diffs、沒有 forbidden writes、真紅真綠 CI、必要 positive/negative、checker readback、PR reviews、owner/HITL。Merge 後必再依新 main commit 重演；不能拿 merge 前 checker PASS 充數。

### 4.2「是否要完整更新 REPO 主頁 README？」

**裁定：`YES_MINIMUM_INFORMATION_ARCHITECTURE_REWRITE`（P1，高價值）**。

- `README.md` 現有 366 行；首屏兩條 Route 和真實 claim-ceiling 值得保留。欠缺的是**唯一主導航**：保留五區塊——專案做/不做什麼、狀態與已知 Preview 限制、Web／Agent 兩張單一路徑、CLI advanced、Validation/License/Contribute；Shell 詳解移至 `docs/install/README.md`，不重複第二份安裝 SSOT。
- 主頁不要同時鼓勵 `preview.3` 無條件使用又隱藏 published Wheel F002：應顯著註明已知 trace false PASS、修補僅位於候選，公開安裝使用限制。
- 所有連結必指向真實存在的檔案；Public Plugin Directory URL 在未刊登前不得為可安裝 CTA；Web 下載 `PIPD_WEB_FALLBACK.md` 只有成品/asset 存在且驗 SHA 後才可表示「一鍵下載」。
- 完整更新是**架構/用字層**而非重寫核心功能、規範、八個 Skill 或長篇宣傳。快速開始由實機 UAT 支持前不可貼 `Verified 4-host` Badge。

### 4.3「是否要另外增加『完整使用說明』？」

**裁定：`YES_ONE_GUIDE_ONLY`（P1，高價值、非發布 Portal 的取代品）**。

`docs/install/README.md` 是「安裝 SSOT」而不是端到端操作手冊；`README.md` 應是入口而非手冊；`examples/first-run/README.md` 是樣板，不能取代各 Host 使用者工作流。新增**一份**建議 `docs/USER_GUIDE.md` 或 `docs/usage/README.md`（由 Owner 選一，不要兩份同步維護），內容按任務含：

1. Web GPT-6：下載已驗的 ONE MD / 附件授權 / source locator / 缺 source typed NACK；明示 `DOC_MOUNT_ONLY`。
2. Hermes：Host/version 探測→專案 scoped install/trust→8/8 discovery→正負 trigger→rollback。
3. Codex Desktop／Codex CLI：分別的 GUI/CLI effective-load 探針；不把 Wheel `pipd doctor` 冒充 Native Skill discovery。
4. CLI/Wheel：僅以已發布、雜湊匹配的 Wheel 走 `pipd doctor`、最小合法 source→PI→PD→ECP/TQAEP→validate；針對 published F002 明示不能把 `validate PASS` 當完整 Trace 合格。
5. JSON output、常見 typed refusals、版本 pin、離線/Windows/macOS/Linux、rollback/uninstall、範例輸出及限制。

新文件不得複製安裝命令而成為第二 SSOT；頁面指向 `docs/install/README.md` 的版本化步驟。交付 DoD：README→User Guide→Install SSOT→實際 Test Fixture 四級導航無死連結，新用戶可跟同一個 `first-run` 範例得到正例與已預期拒絕；Plus/Free/Host 有清楚 `NOT_SUPPORTED/NOT_VERIFIED` 而非假 PASS。

### 4.4「是否要對 REPO 進行最終發布前的 REPO 衛生整理？」

**裁定：`YES_SCOPED_PRE_RELEASE_HYGIENE`（P1；不准歷史改寫或壓平 raw evidence）**。

**必需**：刪除／隔離**本次新產生**的未授權臨時檔、垃圾快取、祕鑰與敏感資訊；檢查 gitlinks/submodule 清單、Git LFS／large binaries、相對連結、`.gitattributes` 的 EOL、授權宣告及 Wheel/LICENSE/NOTICE 一致性、驗收記錄 SHA／subject 追溯；對 GitHub workflow 配置最小 `contents:read`、不使用 privileged untrusted PR、不暴露 publish secret；測試結果不可 False-Green；Owner 核對 GitHub required checks／保護規則（rulesets API 本輪回傳 0，不排除另有尚未核實的 branch protection 設定）。

**高價值但可延後到準備對外收 PR 時**：`CONTRIBUTING.md`、`SECURITY.md`/漏洞通報管道、`CODEOWNERS`、簡版 Release/Changelog 入口；沒有這些本身不是所有 MVP/S4 功能失敗的證據。若正式 Public Plugin 牽涉外部使用者資安回報，最小 SECURITY policy 有較高必要性。

**歷史證據處理**：R3 約 64.96 MB Git Tree blob size，其中 `.hgk/` 61.82 MB、95.18%；這是明確可觀察的 DX/Repo 肥大。建議往後採 `source-in-repo` + `append-only evidence archive` + digest/locator handoff 的政策，不要此刻無批准刪除 raw log、原始負例、驗收 oracle 或重寫歷史換取小體積；既有證據應 archive + manifest + readback，避免新開源審查因「整理」而失去可追溯性。`dist` 歷史版也同理，不覆寫任何 Tag 或 asset。

**不放行的過度工程**：新 MCP/Remote backend/OAuth、第二個 Installer Framework、多個重複 User Manual、額外第九 Skill、完整自建 Portal、重製所有 Schema、破壞性 git-filter-repo 清史、單為 CI 綠燈改掉真失敗 Oracle。

---

## 5. 三合一驗收工作包回讀（UPG-P01..04）

| Package | 本次 R3 實作 | 必要缺口／Owner |
|---|---|---|
| **UPG-P01** Public Plugin Source Projection | `packaging/public-plugin/plugin.json`, `plugin.release.json`, vendor bytes pin, 8 derivations, `freeze_public_plugin_source.py`, `build_public_plugin.py`; existing 8 Skills exact set | Human publisher/商標/Official validator/real ZIP/G00–05 independent proof；PKG07 Owner |
| **UPG-P02** Minimal Web/Agent onboarding | README 2-route、`docs/install/README.md`, `PIPD_AGENT_INSTALL_PROMPT.md`, `build_web_fallback.py` | 真正可下載 Web ONE MD、可複製 CLI/Host task、Windows first-run red → green；DX Owner |
| **UPG-P03** Independent safety/testing | 兩份新 tests、兩 Workflow、Runner negative，歷史 AO R3 Round1/2 verdict | 本輪 CI False-Green + public-plugin-verifier fail；缺 full independent checker、Host 8/8 behavior；TQAEP Owner |
| **UPG-P04** Release／Portal／Rollback | Manifest, ReleaseTuple, manifest/sha 與 human hold 說明 | 新 Immutable preview、GitHub asset readback、Portal Scan/Publish/HITL/Plus&Free UAT，Release Owner + Publisher |

### 5.1 嚴格採納 R2 的五個最高風險負例

- **F01** fake PNG valid magic but bad image body：須完整解碼/結構驗證；僅看 signature=FAIL。
- **F02** unofficial Manifest extra-property：正式 vendor JSON Schema 固定 digest、未核准欄位拒絕；本地 subset 不能取代官方相容性證明。
- **F03** Invalid SKILL header／派生：8/8 元始 body 必 byte-preserved；Header 派生需 Owner 授權、前後映射及獨立正負行為 UAT。
- **F04** missing/null/wrong commit/tree：fail closed，SourceMap 和 ZIP Receipt 不得省略 Subject identity。
- **F05** symlink/hardlink sentinel overwrite：輸出隔離、`O_EXCL`、不觸碰外部 sentinel；和本輪 web fallback failing test 一起復測。

**實質上限**：R2 Blueprint §7.3 的 14 synthetic + §7.4.1 的 5 synthetic 是藍圖樣板聲明，不是最新 R3 這 19 項都已由本官獨立跑過。R3 自己有較多測試，然而 Hosted CI 紅燈及 RC masking 禁止由 test count 推 PASS。

---

## 6. 最小修補順序（Issue → TaskSpec → Evidence Return → Next Verdict）

| Priority | Finding / 最早責任 Owner | Smallest legal repair | Required focused retest / raw evidence |
|---|---|---|---|
| **P0** | `S4R3-F001` CI Owner + TQAEP | CI shell 加 `pipefail` 或保存 unittest 退出碼；修復 11 個及 2 個測試失敗的真因 | 新 run exact SHA／完整 stdout/stderr/exit/log；故意測試 FAIL→CI 必紅，真修後全量綠 |
| **P0** | `S4R3-F002` Repo+Stage A/Stage B Owners | 重組 PR 寫入集/兩階段 base；保留真正禁止寫集 | `public-plugin-verify` 全步驟實跑；兩個 base 下 allowlist negative，且禁止新增 src/schema |
| **P1** | `S4R3-F003` PKG07、Release/Publisher | 把正式 Icons、Vendor validation、Owner human identity、實際 Build preflight 清楚綁定；新的發行版本 | ZIP 2x deterministic、schema/image/full decode、F01–05 negative、download/readback；Portal 另列 |
| **P1** | `S4R3-F004` DX Owner | 產生可用 Web 單 MD / 指定下載位置，README 維持兩主入口，新增唯一 User Guide | 外部新用戶 copy-paste journey、broken link、PowerShell/Bash、Plus/Free 分開 |
| **P1** | `S4R3-F005` Repo Owner | 不破壞式 repo hygiene、Review owner policies、evidence archival policy | Git status clean、掃描、license、large files、source/release mapping、rollback |
| **P1** | `S4R3-HOST` Host UAT Owner | 四宿主各 POS/NEG/EDGE/SEC/non-trigger、missing-source NACK、uninstall | Host name/version/OS/source+SHA/discovery/permission/raw prompts/transcripts/negative/HITL；代換模型另標 |
| **P1** | `S4R3-RELEASE` Release Owner | 新 immutable candidate Release + human Portal | new tag/commit/tree/bytes/SHA/asset_id，portal draft→scan→review→publish 原始收據 |

**不批准**：現在直接 merge PR #2、force-push/重寫公開 Tag、為了測試綠燈刪除 Security negative、只新增一個大而空泛的「完整文件」、沒有真 Host 功能卻標 Universal S4。

### 6.1 允許／禁止寫入集（路由候選，須 Owner ratify）

```yaml
change: S4POST-R3_MINIMUM_REPAIR_ROUTEOUT
status: CANDIDATE_NOT_EXECUTED
primary_repo: shw097-team/PIPD-LS-SP
current_main: 224591431a164ab72a9423cd180e417e8a762403
candidate_r3: e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
route: IMPORT + EVAL + ACCEPTANCE_ROUTEOUT
stage_a:
  purpose: "S4 trace/first-run/CI correctness, individually reviewed"
  allowed_paths: "Explicit owner-approved patch paths only; not a generic src/** wildcard"
stage_b:
  purpose: "UPG-P01..P04 public Skills-only distribution"
  allowed_paths:
    - "packaging/public-plugin/**"
    - "tools/freeze_public_plugin_source.py"
    - "tools/build_public_plugin.py"
    - "tools/build_web_fallback.py"
    - "tests/test_public_plugin_packaging.py"
    - "tests/test_web_fallback.py"
    - "docs/install/**"
    - "docs/USER_GUIDE.md (single Owner-selected path)"
    - "README.md"
    - ".github/workflows/public-plugin-verify.yml"
  denied_paths:
    - "skills/**"
    - "src/**"
    - "schemas/**"
    - "PIPD_LS_canonical_standard.md"
    - "PIPD_LS_DOC-**"
    - "PIPD-LS-SP_PIPD-PKG-**"
    - "existing tagged release bytes"
    - "ECP/TQAEP acceptance oracles"
    - "MCP/actions/hooks/credentials"
merge: HOLD
release: HOLD
checker_role: INDEPENDENT_READ_ONLY
human_approval: REQUIRED
```

**注意**：一個 Stage A 為了修真正實作而修改 `src/**/schemas/**`，與 Stage B **ZERO CORE WRITES** 不矛盾，前提是不同 TaskSpec/Owner/基準/證據獨立分開；若把二者混成一個 diffless 「三合一」變更，就無法認證 UPG-G01。

### 6.2 精簡 Evidence Return Pack（不製造 PASS 收據）

```json
{
  "schema_id": "PIPD-S4-R3-EXT-REVERIFY-CANDIDATE/1",
  "status": "PENDING_NEW_SUBJECT",
  "subject": {"repo": "shw097-team/PIPD-LS-SP", "commit": null, "tree": null, "zip_sha256": null},
  "checker": {"identity": "MUST_BIND_DISTINCT_FROM_MAKER", "readonly": true},
  "gates": ["G-AUTH", "G-PI_PD", "G-DEV_ECP", "G-OPS_ECP", "G-TQAEP", "G-RELEASE", "UPG-G00", "UPG-G01", "UPG-G02", "UPG-G03", "UPG-G04", "UPG-G05", "UPG-G06", "UPG-G07", "UPG-G08", "UPG-G09"],
  "minimum_raw": ["git_tree_and_changed_paths", "workflow_log_and_exit_code", "entire_test_output", "affected_negative_tests", "wheel_install_and_cli", "zip_2x_and_sha", "host_discovery_and_behavior", "human_owner_ratification"],
  "owner_human_approval": "NOT_RECEIVED_FOR_THIS_NEW_SUBJECT",
  "public_release_approval": false,
  "S4_FULL_PASS": false
}
```

這裡的 `null` 是**未建立下一個新受驗 Subject** 的明確佔位，而不是合法可交給 production release 的 frozen tuple。下一個候選缺 commit/tree/hash 時應 `TEMP_CLOSED`，不得由 Executor 自填想像值。

---

## 7. Gate Calibration 防失守檢查

| 控制 | 本輪觀察 | 修正與驗收門檻 |
|---|---|---|
| Objective mismatch | 未經 Host 安裝卻宣稱易用／可安裝 | 實際首次成功任務與退出碼、不是 file count |
| Strictness drift | `unittest` 11/2 紅仍 CI 綠 | P0 修正 RC，獨立故障注入 |
| Local overfit | R3 本機 Windows 572 OK，但 hosted Linux 572 有 11 Fail | 至少 Linux+Windows，macOS 按真宣稱 scope；不用本地分母代替 CI |
| Missing negative | Skill 結構驗證不能代表行為拒絕 | 8 Skills × POS/NEG/EDGE/SEC/nontrigger；主機分開 |
| Regression baseline | R2 F01–F05、preview.3 F001/F002、script portable、Trace | red-before/green-after，保留反例源 |
| Raw evidence | GitHub 綠 Badge vs 原始 FAIL | 原始日誌和退出碼有最終優先權 |
| LLM judge balancing | Host 是否遵守越權靠模型判斷 | paired prompts/order-swapped、golden anchors、HITL；不覆蓋 Schema FAIL |
| Separation of duties | Maker 及 checker 歷史有不同 commit/verdict | 釘 exact subject，另獨立 read-only verifier，新版本另驗 |
| TT/CR | 既有 57 rows 含 evidence gaps/design-only，Host/Portal open | 未有 evidence 前不得消除原缺口、不得整批標 PASS |
| Release fail-closed | Public Plugin Portal/Publisher 未證 | `NO_PUBLIC_RELEASE`；撤銷/回復由 Owner + Publisher |

---

## 8. 最終外部驗收矩陣與適當的聲明上限

| 驗收面向 | 本輪 Verdict | 能支持的最強聲明 |
|---|---|---|
| 本地 20 KP + challenge + 11 PKG + skeleton + Canonical/DOC 上游讀取 | **PASS (physical read only)** | `SESSION_SOURCE_READABLE`，非 100% atomic semantic audit |
| Repo HEAD/PR/branch/release 綁定 | **PASS (direct GitHub metadata)** | 凍結於 R3 `e71fee6d...`/tree `28752873...` |
| S4 core source Trace 關閉能力 | **PARTIAL** | source 修補可見；CI full red、publish Wheel 未升級 |
| DEV/OPS ECP | **PARTIAL/TEMP_CLOSED** | 存契約/歷史 receipts，不是世界執行准入 |
| TQAEP / CI truthfulness | **FAIL_CHALLENGE** | `ci` 假綠；不能出 S4 PASS |
| 三合一 UPG-G01 / Hosted CI | **FAIL_CHALLENGE** | `public-plugin-verify` 紅且後續未跑 |
| 三合一 Builder/Schema/Icons | **PARTIAL/TEMP_CLOSED** | 本地候選及歷史來源，無正式 vendor + Portal |
| README / DX | **PARTIAL** | 兩入口可見，首次任務及下載單檔未封閉 |
| 四 Agent Host / Web GPT-6 真實 UAT | **TEMP_CLOSED** | `NOT_VERIFIED`；舊 Codex CLI 部分正負例不得替代四 Host |
| Public Plugin Publish / Human ratification | **TEMP_CLOSED** | 尚未取得必要真人 Publisher／Portal receipts |
| 目前 PR #2 merge | **FAIL / NO_MERGE** | 數據可 merged 不等於 quality mergeable |
| `S4_FULL_PASS` | **NOT_GRANTED** | 新受驗 Subject 全部 Gate 關閉後再另審 |

### 最終裁定

**`FAIL_CHALLENGE`：R3 現有候選的 Gate 資料存在可重現的 CI False-Green 與失敗 Workflow，不能合併至 `main`，不能進入正式公開發行。**

**`TEMP_CLOSED`：四宿主真實使用、Vendor/Portal、Human ratification、完整 S4 External PASS 因未具備可重播原始證據而保留，不把缺證據臆測成產品錯誤。**

**高度工程必要的後續只有**：修復 CI 真紅真綠、把 Stage A/B base/diff 切清並全量重驗、關閉真實 First-run/Trace／typed refusal 失敗、產出一個可用 Web 備援與一份使用指南、建新不可變 release tuple＋真實 Host/Publisher 收據。其餘大型工具、第二 Control Plane、非必要深度清理、套件版本擴大，**不批准**。

---

## 9. 直接可追溯證據與權威 Locator

- 原 R2 升級藍圖（本地）：`PIPD-LS-SP S4｜三合一小型升級藍圖(1).md`，SHA-256 `aca367e7d4aad7d44245c56c2ec3c9f164fc07852904078358b3be2ece01c2b4`，§§0.1、3.2、3.3、5.1、6.1–6.3、8.1–8.5、9.1–9.5、10.1–10.2、11、12、Appendix A。
- Challenge reviewer：`challenge-review-SKILL.md §Invariants 1–10, §Workflow 1–5`；SHA-256 `9ecd2366dc2353fc8aaf533161ae1e34abba37a80f345f5f78023325f8d26194`。
- 規範落點：`11_EVIDENCE_REQUIREMENT_MATRIX.md#evidence-matrix-rules`; `12_EVAL_REGRESSION_LLM_JUDGE.md#eval-regression-judge-rules`; `16_RELEASE_PACKAGING_CHECKSUM_READBACK.md#release-packaging-rules`; `17_UX_ONBOARDING_NO_BRAIN_FLOW.md#ux-onboarding-rules`; `18_TT_CR_DRIFT_REGISTER.md#tt-cr-drift-rules`; PKG-06 TQAEP、PKG-07 Part7–8、PKG-08 Part11、Canonical DOC-07、DOC-08。
- GitHub Repo：https://github.com/shw097-team/PIPD-LS-SP
- R3 subject：https://github.com/shw097-team/PIPD-LS-SP/commit/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
- Draft PR #2：https://github.com/shw097-team/PIPD-LS-SP/pull/2
- `ci` source：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/.github/workflows/ci.yml
- `ci` run raw Job：https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38341318079 （Job `115112781888`）
- `public-plugin-verify` source：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/.github/workflows/public-plugin-verify.yml
- `public-plugin-verify` run raw Job：https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38341318074 （Job `115112712475`）
- R3 安裝 SSOT：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/docs/install/README.md
- R3 入口 README：https://github.com/shw097-team/PIPD-LS-SP/blob/e71fee6dd3aa73724baec4e8d9cc72127fbe36ed/README.md
- R3 host UAT（歷史部分證據）：`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/uat/UAT_RESULTS.md`；局部 Codex CLI 正反案例，不具四 host 全量證據。
- R3 第 1／2 獨立車道結果：`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/ao_lane/AO_VERDICT.json`、`.../ao_lane_round2/AO_VERDICT.json`；均 `FAIL_CHALLENGE`，且受驗 commit 不同於最新 `e71fee6d...`。
- R3 本地 Owner supplies 限制：`.../verify/r3/OWNER_SUPPLIES_DELIVERED.json`；`build` 不等於 Portal／Human／Published。

### 本次輸出不構成

`EXTERNAL_CHALLENGE_REPORT` 官方雙檔 validator PASS／Repo Merge Approval／GitHub Required Check Configuration／Public Plugin Portal Review／四宿主有效載入確認／S4 全套實施結案／正式發布、部署或 Production Acceptance。

**END — no candidate mutation; repair routed to earliest owner.**
