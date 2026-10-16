# PIPD S4 R6 — 任務執行清單（Task Execution Checklist）

> **STATUS_AS_OF: 2026-10-16（R18 回填）。** 本表原於立案時建立，狀態欄在 R6/R17 執行期間未回填，
> 造成「計畫說未開始、證據說已完成」的矛盾。R18 的獨立稽核（`r18/AUDIT_REQUIREMENTS.tsv`，
> 列 `CHECKLIST-CURRENTNESS`）確認為**要求級缺陷**，於此關閉：本次只**填入實際到達的狀態與證據**，
> 未改寫任何一列的語意，亦未刪列。

狀態：`[ ]` 未開始 / `[~]` 進行中 / `[x]` 完成 / `[-]` NOT_RUN / `[D]` DEFERRED / `[o]` OWNER GATE。
「證據 ID」＝`S4_R6_CLOSEOUT_RETURN/` 內的實際檔名，或外部路徑。

## G0 PREP / Compiler
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-01 | 本地 preflight：`git status --porcelain=v1`、`rev-parse HEAD/HEAD^{tree}`、remote URL、worktree 建立於 origin/main | CK-01 | [x] | `source_contract_readback.json`（worktree @ `d3bd545…`，建立時乾淨） |
| T-02 | HGK `doctor`／spine 可用性、`runtime_role_binding_assert.py`、Codex CLI bin 實測 | CK-01 | [x] | lane probe 收據（EXECUTE rank1 `deepseek-v4.1-flash`、VERIFY rank2 `gpt-6.1-sol`）；Codex bin 以 glob 實測解析（舊 pin 已失效） |
| T-03 | 建 `OROCHI_FACTORY_ORDER.v1`（精簡引用版；不改 HGK 既有 WorkOrder） | CK-01 | [x] | `OROCHI_FACTORY_ORDER.v1.json` |
| T-04 | 建 `CONTRACT.json`（C0–C9 對應），跑同版 `lint → activation → acceptance → compile` | CK-01 | [x] | `compiler/compiled/compiler-receipt.json`（4/4 閘門 exit 0） |
| T-05 | Compiler `PROMPT_COMPILE_PASS` 收據（未通過則只回堵點並停止施工） | CK-01 | [x] | `compiler/compiled/compiler-report.json`（首輪 41 errors → 修 contract（未放寬驗證器）→ `PROMPT_COMPILE_PASS`） |

## G1 最小文件修補（EXECUTE = Codex CLI / deepseek-v4.1-flash）
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-06 | `docs/install/README.md` 版號／source commit 混寫勘誤（由實際 mount-pack release provenance 推 pin，不硬填 main） | CK-04 / F-R6-01 | [x] | candidate `552bbde`；`diff_and_tests/candidate_diff.patch` |
| T-07 | `docs/USER_GUIDE.md` 舊 `Merge/release HOLD`、舊 wheel 宣稱之 2–4 句更新；明寫 `.4` 已發布、Full S4 未授予 | CK-05 / F-R6-02 | [x] | 同上；產品分支現況 `127ec1c` |
| T-08 | 安裝 SSOT 補「同 plugin_id 已安裝 → Update／Upload new version；否則備份→同意→卸載→重加；新 ID 為衍生候選非原 ZIP」 | CK-08 / F-R6-03 | [x] | `docs/install/README.md`（產品分支）；`findings_to_task_and_ck.tsv` |
| T-09 | PR #17 一檔 readback 初核（不併 #14/#15） | CK-07 / F-R6-06 | [o] | `findings_to_task_and_ck.tsv`：複驗完成（1 檔 `+14/−0`、non-draft、`mergeable clean`、checks 綠）；**合併屬 OWNER GATE** |
| T-10 | `git diff --check` 乾淨；改動僅限 WorkOrder 批准路徑 | CK-12 | [x] | `diff --check` 空輸出；`R17_MEASUREMENTS.json`；寫入集分類器 `R17_check_write_set.py` → `PASS` |
| T-10b | **（R18 追加）** 修正 `docs/install/README.md:151` 失效對外連結：`](RELEASE_TUPLE.json)` → `](../RELEASE_TUPLE.json)` | CK-04 / F-R6-01 | [x] | R18 產品 commit；稽核列 `DOC-LINK-TARGET`；守門同步擴充為「對外相對連結必須解析得到檔案」 |

## G2 DEV ECP / 回歸
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-11 | doc-link / release-identity 正例：preview.4 tag/body 維持 | CK-02 | [x] | `subject_versions.json`（7/7 assets 摘要相符、tag object 未動） |
| T-12 | 負例：錯 `preview.3` SHA／preview.3 commit 冒充 preview.4 應被發現 | CK-04 | [x] | 守門配對 mutation；獨立 checker 自寫 probe 亦全數被拒（`R17_CHECKER_ESCALATED_VERDICT.txt` C3） |
| T-13 | 負例：same-ID ADD 不被文案誤導為 Update；缺上傳權限正確降級；第九 Skill／跨根修改拒絕 | CK-08/09 | [~] | PARTIAL：文案與 ZIP 結構已量測（56 entries／8 `SKILL.md`／單 root `plugin.json`／無 traversal／無 MCP-Apps-Hooks，`R17_MEASUREMENTS.json`）；**「第九 Skill／跨根修改」缺專屬機械負例** → 列 `TT-R18-01` |
| T-14 | 跑 `tests/test_r5r3_install_route_identity.py` 與適用套件，取 exit code + raw `Ran/OK/FAILED` | CK-03 | [x] | 受影響 44 tests OK；全量 `633 tests / OK (skipped=4) / 174.073s`（`R17_FULL_SUITE_FINAL.txt`） |
| T-14b | **（R18 追加）** 新增 `DEV_ECP` 具名引用版（稽核列 `ECP-DEV` 原判 NOT_DONE） | — | [x] | `r18/ECP_DEV.md` |

## G3 OPS ECP / 分支 Push
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-15 | HGK typed 准入：`allowed_paths`、`network=GitHub`、`effect=branch_push`、`secret_read=指定檔一次性` | CK-01/12 | [~] | PARTIAL：`ADMISSION_OK`、5 WorkOrders 已達成；**但無精確作用域之 ExecutionBinding，且 taskspec 記 `network=false` 而本回合確有 branch push** → 稽核列 `HGK-BINDING`；列 `TT-R18-02`（控制平面項，不在本回合寫入權限內） |
| T-16 | 建隔離修補分支、commit、push（PAT 唯讀讀檔；不回顯）；驗 `origin == shw097-team/PIPD-LS-SP` | CK-12 | [x] | `far-r17/publish/`；產品分支遠端 = `127ec1c`；PAT 全程僅經 askpass 包裝器，未入 argv/URL/log |
| T-17 | 遠端 readback remote SHA／PR URL | CK-12 | [x] | PR #18 @ `127ec1c`（4 檔 `+419/−22`、open／非 draft／`mergeable clean`、`verify` + `offline-gate` 綠） |
| T-17b | **（R18 追加）** 新增 `OPS_ECP` 具名引用版（稽核列 `ECP-OPS` 原判 NOT_DONE） | — | [x] | `r18/ECP_OPS.md` |

## G4 TQAEP / 獨立檢測
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-18 | Maker freeze candidate commit/tree + diff + test logs | CK-03 | [x] | `diff_and_tests/`；`subject_versions.json` |
| T-19 | 非 Maker Checker（Codex CLI gpt-6.1-sol）`VERIFY_ONLY` 於同 hash 重播 doc-link/identity/安全負例 | CK-03/13 | [x] | `checker_verdict.json`（R17 兩次派發）+ `R17_CHECKER_ESCALATED_VERDICT.txt`（`PARTIAL`：C1–C3、C5–C7 PASS，C4 受 guard 邊界限制） |
| T-20 | 無 P0 時保持 R6 `TEMP_CLOSED`，不撤回歷史 `.4` | CK-14 | [x] | `owner_closeout_and_tt.md`（工程建議；**簽核屬 OWNER**） |

## G5 私人 Web route（條件式）
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-21 | 下載入口 + ZIP SHA256（`545e359a…`）於文件與 evidence 揭露 | CK-09 | [x] | `release_and_plugin_scope.json`（68,357 B；獨立 checker 自行下載並重算相符） |
| T-22 | 私人 Host 實測（POS／缺來源 NACK／NEG）——無 UI 權限則如實 `NOT_RUN` | CK-10/11 | [-] | `private_update_uat_redacted.json`：`NOT_RUN`（需具上傳權限的人類帳號，非 agent 可代行） |

## G6 條件新版本
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-23 | `R6-NEXT-PREVIEW`：本輪**預設不觸發**；若觸發須凍結新 main→新 Tag（不得動 `.4`） | CK-06 / F-R6-04 | [D] | `owner_closeout_and_tt.md`（O-5） |

## G7 證據／結案／自演化
| # | 任務 | 對應 | 狀態 | 證據 ID |
|---|---|---|---|---|
| T-24 | 輸出最小 `S4_R6_CLOSEOUT_RETURN/` 八件套 | CK-14 | [x] | 證據包 28 條目 `SHA256SUMS`；fresh clone `28/28 OK` |
| T-25 | Owner closeout + TT：`TEMP_CLOSED ≠ Full PASS`；rollback pointer | CK-14 | [x] | `owner_closeout_and_tt.md`（O-1..O-6 單一動作化） |
| T-26 | FABRIC & HGK 治理下自研究／自學習／自迭代／自進化 | — | [x] | `SELF_EVOLUTION_R6.md/.json`；FAR-016／017／019 |

## R18 追加（本次回填回合）
| # | 任務 | 狀態 | 證據 ID |
|---|---|---|---|
| T-27 | 回填本表與 `DETECTION_CHECKLIST.md` 之狀態／證據欄（稽核列 `CHECKLIST-CURRENTNESS`） | [x] | 本檔 + `DETECTION_CHECKLIST.md` |
| T-28 | 外部工程團隊入口文件 `EXTERNAL_ENGINEERING_HANDOVER.md` + `ROUND_STATE.json` | [x] | 證據分支 `S4_R6_CLOSEOUT_RETURN/` |
| T-29 | `SOURCE_INDEX.json`：KP 20 局 + canonical/DOC/PKG 之 locator+SHA；缺漏或衝突標 `SOURCE_GAP`（稽核列 `SOURCE-INDEX`） | [x] | `r18/SOURCE_INDEX.json` |
| T-30 | 證據包 `checker_verdict.json` 重新綁定至最終候選（稽核列 `PACK-07`） | [x] | `checker_verdict.json`（R18 版） |
| T-31 | 稽核列 `HISTORICAL-RAW-CI`：凍結歷史 raw CI 日誌 | [~] | PARTIAL/`SOURCE_GAP`：憑證對 `actions/jobs/<id>/logs` 回 401 → 以 `SOURCE_GAP` 記錄並附確切原因（`r18/SOURCE_INDEX.json`） |
| T-32 | 稽核列 `HGK-BINDING`：精確作用域 ExecutionBinding | [~] | 承接 T-15；列 `TT-R18-02`，需控制平面自身 admission |

**未回填／未完成之計數（本檔自檢）**：殘留 `[ ]` = **0**。
`[~]` = 4（T-13、T-15、T-31、T-32）；`[-]` = 1（T-22）；`[D]` = 1（T-23）；`[o]` = 1（T-09）。
每一列之證據 ID 皆指向存在之檔案或已記錄之外部狀態；`SOURCE_GAP` 類以其實際限制記錄，不以完成視之。
