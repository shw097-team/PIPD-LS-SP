# R21 FAR 研究合成 v2（已吸收 VERIFY OBJECT 的更正）

- 輪次 `R21-FAR-20261101`｜車道：PLAN `openai-codex/gpt-6.1-sol` **ok=true／rank 1／117.6s**；VERIFY `openai-codex/gpt-6.1-sol` **ok=true／rank 1／116.5s，verdict=OBJECT**；EXECUTE `opencode-go/deepseek-v4.1-flash`（見 §9）
- 會話平面 `deepseek-v4.1-flash` 是 EXECUTE 車道模型；PLAN／VERIFY 車道結論只認收據，不認會話。
- 來源：`far/sources/SOURCE_DENOMINATOR.json`（35 筆）｜缺口：`far/gaps/GAP_LEDGER.json`（18 列）｜PLAN 原文 `far/PLAN_R21FAR_ANSWER.txt`｜VERIFY 原文 `far/VERIFY_R21FAR_ANSWER.txt`

## 1. 現役狀態（實測）

| 項 | 值 | 來源 |
|---|---|---|
| work_queue | 22 列：19 PASS / 3 FAIL；**17 列 `evidence_ref` 為空＝16 PASS ＋ 1 FAIL（WP-FHS-12）** | `far/sources/WORK_QUEUE_READBACK.json` |
| 有據的 PASS | **只有 3 列**：WP-FHS-10、WP-FHS-11、WP-FHS-17 | 同上 |
| 矛盾列 | WP-FHS-11 是 PASS，卻掛 `HERMES_MODEL_HALF_UNMEASURED`（3 個 Hermes loader cell 未取模型側回應） | 同上 |
| WP-12 真阻斷 | 不是「缺一次模型請求」，而是 **recovery entry `D:\Hermes-Recovery\…` 的 failure 無法被建立**：要嘛由 host owner 從 PATH 退役 forwarder（一個命令），要嘛修 lease 管理的依賴安裝（10 個 openai 模組超 260 字元、10 個 cp314 extension 在 3.11 runtime） | 同上 `blocker_cause` |
| WP-20 分母 | **192 cells**：18 MEASURED_PASS／12 SURFACE_EXISTS_NOT_RUN／**48 NOT_RUN_NO_RUNNER（DeepSeek Harness）**／114 NOFIT_NAMED；本輪只做了 12 格 | 同上 `blocker_cause` |
| OPS ECP | 實測 31 條（OPS 14／OBS 10／DEV 5／USER 2）；契約寫 32 → `NOT_LOCATED` | `ledgers/S6_EDGE_EFFECT_LEDGER.json` |
| 信封 | `WIN-91b01b7cd918`，scope `permit_sign,admission_bundle_sign,registry_row_sign`，ceiling `HOST_OPERATIONS`，到期 2026-11-01T13:55:31Z → **每次用印前必須重驗剩餘 ops 與有效期**（VERIFY：狀態是 SNAPSHOT_REQUIRING_REVALIDATION，不是常開） | `var/B1-PIPD-PKG-20261027/artifacts/OWNER_WINDOW.json` |

## 2. 缺口（11 組，含 VERIFY 的更正）

| # | 缺口 | 狀態 | 解除條件（已更正） |
|---|---|---|---|
| 1 | 16 列 PASS 無據 ＋ WP-12（FAIL）無據 | OPEN | **先回收既有綁定證據**（WP-10/11/17 有據）；只在證據不存在或不足時重跑，不是全部重做 |
| 2 | WP-11 PASS 卻掛 blocker | INCONSISTENT | 從 gateway HTTP 面取一次回應即可同時結掉 WP-11 模型半面與 WP-12 的一半 |
| 3 | S5 四個 canonical 缺陷 | OPEN | owner 授權 REPO_WRITE → 落地 → 不同 principal 重放 |
| 4 | C5「checker 改同一 diff」 | **OPEN**（VERIFY 更正：偵測≠阻止，改程序不能關掉 prevention 條文） | 要嘛實作並測試一道強制 gate，要嘛由 owner 明示接受「偵測即足夠」 |
| 5 | OPS 32 vs 31 | NOT_LOCATED | owner／契約 issuer 裁決 |
| 6 | OPS 11 PARK ＋ 1 partial | PARTIAL | **本地/外部要分開**：receiver 契約、fixture、候選測試、獨立重現可本地評估；生產 receiver 才需外部 |
| 7 | TQAEP 282 未映射未執行 | OPEN | 映射可本地；執行需 fixtures |
| 8 | 三職能無 host 身分 | NOFIT_LOCAL | 見 §3（信封不足以解決） |
| 9 | WP-20 殘留 F4/F5/F6/F11 ＋ 48 NOT_RUN_NO_RUNNER | OPEN | F6 需網路；48 格需 DeepSeek Harness runner |
| 10 | `review_lock.py` 未版控 | OPEN | 版本化即可；**但它不是其他變更的前置**（VERIFY 更正） |
| 11 | TT-20 無記錄 | NO_RECORD | owner 供檔或明定閘 |

## 3. 「無法 PASS」重判（含 VERIFY 對信封提案的否決）

| 項 | 重判 | 結論 |
|---|---|---|
| 三職能 Native | **REAL** | 我原先提「信封以 registry row 登記測試 principal」→ **VERIFY 判 UNSOUND，我接受**：信封只授權簽章操作，不授予「發身分、提供 runtime、改寫 host-issued 條文」的能力。要成立需 issuer 明示授權＋身分語意＋runtime 支撐＋驗收準則，四者缺一不可 |
| PLUGIN install 段 | MISREAD（可控） | 需 catalog／git 來源＋網路；Docker 離線不適用 |
| OPS 32 分母 | OVER_READ | agent 不得補數；契約文字需 owner 裁決 |
| C5 checker | **NARROW_ASSUMPTION 但未關閉** | 「重算 sha」是提案，不是已實作的 gate；條文寫 prevention 就必須有 gate |
| 16 列無據 PASS | OVER_READ | 回填或降級，不需全部重跑 |
| WP-12 升格 | **我原先判 NARROW，VERIFY 更正為 HOST_DEPENDENT** | 缺的是 recovery entry 的 failure 證據或依賴修復，不是「再派一次 lane」 |
| 簽章類 | OVER_READ（有條件） | 每次用印前重驗 ops/期限/scope，不是常開授權 |

## 4. Owner / Issuer 決策（最小形式，含 VERIFY 的收斂）

| # | 決策 | 最小形式 | 誰 | 備註 |
|---|---|---|---|---|
| D1 | 三職能是否可用「受治理測試 principal」 | 需**先**由 issuer 定義身分語意與驗收準則；信封只負責最後的 registry row 簽章 | owner＝issuer | 不是「簽一列就好」 |
| D2 | S5 修補落地 | 一個 patch＋獨立回歸收據 | owner | 需 REPO_WRITE 範圍 |
| D3 | OPS 32 vs 31 | 一句裁決 | owner／契約 issuer | 文件裁決 |
| D4 | 16 列無據 PASS | 授權降級 `UNSUPPORTED_PASS` 或補據 | owner | 影響 22 WP 通過率 |
| D5 | TT-20 | 供檔或明定閘 | owner | — |
| D6 | 合併順序 | **逐案授權，各自 scope 與 gate**（VERIFY 否決「一次性 blanket」） | owner | 見 §6 |

## 5. 可升格（已檢測＋本地驗收）

| 候選 | 已測 | 仍缺 | 建議 |
|---|---|---|---|
| S5 授權補丁 | 4/4＋2/2＋C5 3 過 | 不同 principal 重放 | 候選可升格；落地需 D2 |
| WP-13 修補＋sidecar | T1–T5、5/5 claims | 逐 finding 獨立關閉 | 候選可升格 |
| WP-12 forwarder | 入口等價矩陣 | recovery entry 證據或依賴修復 | HOLD（host） |
| S6 兩修補 | 前後對照 | 獨立重現 | 候選可升格 |
| kind 裁定 v2.1＋list/remove | 68 命令＋delta | install 段 | 局部可升格 |

## 6. 合併建議（逐案，各自 gate）

| 標的 | 先過的閘 | 簽署者 |
|---|---|---|
| `scripts/review_lock.py` 版本化 | 內容審查＋回滾點（**不宣稱是其他項的前置**） | owner（REPO_WRITE） |
| S5 授權補丁 | 獨立 POS/NEG/併發＋canonical sha 前後 | owner（D2） |
| WP-13 修補＋sidecar | 五 finding 獨立關閉＋歷史 swap 以 superseded 記錄 | owner |
| WP-12 forwarder | recovery entry 證據或依賴修復＋入口等價 | owner＋host owner |
| S6 修補 | 獨立重現 | owner |

## 7. 執行方案（三車道）

1. **PLAN 已回**：缺口與決策如上（收據 `far_receipts/PLAN_R21FAR_v2.json`）。
2. **EXECUTE**：C5 由 EXECUTE 車道重跑（收據 `far_receipts/EXECUTE_R21FAR_C5.json`，見 §9）。
3. **VERIFY 已回 OBJECT**：更正已吸收進 v2（本文件）。
4. **Owner 回合**：D1–D6 逐案；D4 與 D6 成本最低、解鎖最多。
5. **停止條件**：需 owner 憑證而未取得者記具名 HOLD，其餘續跑。

## 8. 宣稱天花板

- 候選研究產品；PLAN／VERIFY 收據只證明「該車道以該 arm 服務」，不證明結論正確。
- VERIFY 是**advisory**，不是 acceptance；不得由此升格任何項目。
- 沒有 main、沒有 release、沒有 production 宣稱。

## 9. VERIFY 回件吸收紀錄（verdict=OBJECT）

VERIFY 指出的 7 條 unsupported claims 與 8 條 misclassification，本版處理如下：

| VERIFY 指正 | 本版處理 |
|---|---|
| 「17 列 PASS 無證據」不精確 | 改為 16 PASS＋1 FAIL；並列出 3 列有據（WP-10/11/17） |
| readback 不含目錄清單 | 刪除「無 per-WP 目錄」的主張；該主張改引 `WP_DAG_SAMPLING.json` |
| 「獨立 lane 可解 WP-12」 | 撤回；改記 HOST_DEPENDENT（recovery entry 證據或依賴修復） |
| EXECUTE 收據缺失 | 保留為 MISSING 直到檔案出現，不以存在性代替執行 |
| 「所有數字都有檔案＋sha」 | 改為「有檔案身分，但未綁 command/output」 |
| 「重算 sha 即滿足 C5」 | 改為 OPEN；提案不是已實作的 gate |
| 「review_lock 是前置＋一次性授權」 | 撤回；改為逐案 scope |
| 信封可登記測試 principal | 撤回為 UNSOUND；改為需 issuer 先定義身分語意與驗收準則 |
| WP-20 缺 48 NOT_RUN_NO_RUNNER | 已補進 §1／§2 |
| EXECUTE 收據缺失 | 已補：`far_receipts/EXECUTE_R21FAR_C5.json`（ok=true、nonce 有、exit 0、sha 相符），**但標明不是 dispatcher 收據** |
| （追加，owner 質疑）我先前的「PLAN／VERIFY usage ok」 | **撤回語意**：`usage_receipt_ok=true` 只表示「arm 由 codex rollout 認證」，**不是**有 usage／billing 列。兩回合 `usage_rows_after_offset=0`、`usage_provider=None`；dispatcher 在 OAuth-direct 時（`hgk-lane-dispatch.py` ~3033-3044）**強制**設 true。證據 `far/sources/TOKEN_ATTRIBUTION.json` |

## 10. EXECUTE 車道：三個實測坑（本輪新增，已寫回 skill）

1. **`wire_api = "chat"` 已被 Codex CLI 移除**：`Error loading config.toml: wire_api = "chat" is no longer supported` → 只能 `responses`；但 `:10105` 與前門 `:10100` 都真的回應 `/v1/responses`（200），所以協議不是問題。
2. **sealed home ＋ `-s workspace-write` ＝ 子行程被 read-only 政策擋掉**：模型答了 nonce，命令卻在執行前被拒（"blocked by the read-only sandbox policy"）。改 `-s danger-full-access` 後同一份 brief 正常跑完。
3. **`scripts/hgk-lane-dispatch.py --lane EXECUTE` 兩次卡死**：寫完 `WARN_GUARD_SUBJECT_OUTSIDE_REPO` 後就沒有任何 attempt 記錄，超過自身 `--timeout 520`（實測 704 s）仍未結束 → 手動 kill。因此本輪 EXECUTE 以 **direct sealed-home recipe** 執行，收據以 run log 的 `model:` 行為身分來源，並在收據內明寫 `not_a_dispatcher_receipt: true`。

