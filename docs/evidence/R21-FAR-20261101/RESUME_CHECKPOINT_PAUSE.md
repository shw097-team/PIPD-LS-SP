# R21 暫停檢查點（owner 要求關機）

- 產生時間：2026-11-01T16:25Z 前後（台北 2026-11-02 00:25）
- 狀態：**PAUSED_BY_OWNER**（不是完成、不是失敗；沒有任何 PASS 被追認）
- 工作區：`C:\Projects\Agent_Workspace`；R21 根：`var/FHS-R21-FAR-TT-20261101/`
- 本輪未動 `main`、未 push、未 merge/tag/release、canonical 檔 0 byte 改動。
- **2026-11-01 追加**：AO `deleg_0361E484` 回件 PARTIAL（8 關閉／3 殘留／F11 從缺），WP-20 有 4 條宣稱撤回 → 見 `AO_RETURN_AND_CORRECTIONS.md`。

## 1. 一句話狀態

S0／S1／S2／S4／S6 已完成並有收據；S3／S3b 完成量測但**未經獨立驗收**；**S5 進行中：5 條 REPO_WRITE edge 中 A8／B3／B4 已實跑並各有缺陷＋候選補丁，B5 已量測為 `SP_HOST_LOAD_UNPROVEN`，C5 未做**；S7／S8／S9 未開始。

## 2. 里程碑狀態

| 階段 | 狀態 | 產物 |
|---|---|---|
| S0 四庫＋work_queue＋FAR/TT reconcile | DONE | `receipts/FAR_TT_RECONCILE.json` 49 列（11／14／18／6）＋TT-20 `NO_RECORD`；work_queue 19 PASS / 3 FAIL |
| S1 WP-FHS-12 | DONE（AO=PARTIAL） | `wp12/*`；preimage `a9d680b0…`／postimage `d5c83a8f…`；天花板 `PATH_ENTRY_EQUIVALENCE_VERSION_AND_DISPATCH` |
| S2 WP-FHS-13 | DONE | `wp13/C5_UNDER_ENVELOPE.json`（5/5 claims true）＋sidecar `3d769aee…`；grant `294e915b…` |
| S3 WP-FHS-20 | DONE（量測） | `wp20/CELL_RESULTS_V3_1.json`：12/12 cell_id、隔離可區辨、軸 `NOT_BINDABLE_ON_HOST`；天花板 `AUTHOR_SIDE_LOCAL_SURFACE_SMOKE` |
| S3b Kind 面裁定 | DONE（量測） | `wp20/KIND_SURFACE_RULING.json`：69 動詞、4 有安裝面／1 有面無安裝器／3 無面；「7」「5」兩個分母皆撤回 |
| S3c 獨立 AO | **未回** | `deleg_0361e484`／`sa-0-7da6a885`；無收據不得算完成 |
| S4 22 WP DAG 抽查 | DONE | `receipts/WP_DAG_SAMPLING.json`：3 cited／16 `NO_EVIDENCE_REOPEN`／1 artifact-only |
| S5 DEV ECP | **ACTIVE（3/5 edge）** | 見 §3 |
| S6 OPS ECP | DONE（部分） | `s6/S6_CLOSURE.{json,md}`：2 缺陷補丁／1 partial／11 PARK；31 edge（OPS 14／OBS 10／DEV 5／USER 2） |
| S7 TQAEP 282 | PENDING | `ledgers/S5_S7_INVENTORY.json` 已機讀 282/282 帶 `case_sha256` |
| S8 三職能＋R15/R17 | PENDING | `s5/B5_PROBE.json` 已量測 SP host 不可得 |
| S9 最終交付 | PENDING | — |

## 3. S5 逐 edge（本輪新增，全部可重跑）

| edge | 條文 POS/NEG | 實測 | 收據 |
|---|---|---|---|
| `A8` NATIVE_HOTPATH | exact hotpath＋rollback pointer＋獨立回歸／unbounded 或無 red reproducer | POS PASS、rollback PASS（還原 byte-identical）、scope-escape PASS、**preimage 不符被接受（缺陷）**；補丁後 `GRANT_PREIMAGE_MISMATCH_ENTRY` | `s5/A8_CASES.json` |
| `B3-DEV` SBL_TO_NATIVE | DEV≠OPS／第二 issuer 或共享收據 | **同 grant 二次使用被接受**、**`host_operation` grant 授權 repo write 被接受**、第二 issuer 被拒（verifier rc=3） | `s5/B3_CASES.json`＋`s5/B3_PATCH_TEST.json` 4/4 |
| `B4-DEV` ECP_SELECTOR | 一 WO 一 active ECP／未知 class | canonical 兩者都接受；`candidate_selector` 兩者都拒（`ECP_MULTIPLE_ACTIVE`、`GRANT_EFFECT_MISMATCH`） | `s5/B4_CASES.json` |
| `B5-DEV` THREE_SP | 三個真 host-issued 身分／缺 host 呼叫 | `SP_HOST_LOAD_UNPROVEN`：6 個候選執行檔皆無、0 筆 host 呼叫收據、3 份角色 skill 是 BRIEF 非身分 | `s5/B5_PROBE.json` |
| `C5` CODEX_MINPATCH | allowlist 內＋窄回滾／checker 改同一 diff 或無 red test | **未做**（下一步） | — |

### 候選補丁（canonical 未動）

| 檔 | 作用的缺陷 | sha256 前 16 | bytes |
|---|---|---|---|
| `s5/patch/hotswap.b3.patch` | preimage 未讀＋效果混用＋收據重用 | `04b5244968518955` | 6,868 |
| `s5/patch/hotswap.selector.patch` | 上述＋同 subject 第二個 live ECP | `e2a8fa289efe5ecc` | 7,652 |
| `s5/patch/PIPD/tools/hotswap_b3.py` | 可執行副本（需 `PIPD/src` 同層才 import 得到 `pipd_ls_sp`） | `4b5fe035f90f1f4e` | 18,663 |
| `s5/patch/PIPD/tools/hotswap_selector.py` | 同上＋selector | `03b08c73cd530a64` | 19,410 |

B3／B4 的補丁測試都以「coverage 必須 true」為 PASS 前提；v1 中以路徑不符造成的假拒絕已作廢（`s5/B3_CASES.json` 記 `supersedes`）。

## 4. 開機後第一件事（照這個順序）

```bash
cd C:/Projects/Agent_Workspace && unset HERMES_HOME

python var/FHS-R21-FAR-TT-20261101/tools/s5_b4_cases.py        # 最便宜，先確認環境沒漂移
python var/FHS-R21-FAR-TT-20261101/tools/s5_b3_patch_v2.py     # 補丁 4/4 證明
python var/FHS-R21-FAR-TT-20261101/tools/s5_a8_hotpath_cases_v2.py
python var/FHS-R21-FAR-TT-20261101/tools/s5_b5_probe.py
```

**做 C5 之前先補一件事**：`s5/A8_NEG2_PATCH.json` 當時是 inline 執行、**沒有落檔**；重跑 A8 後請把它寫成檔案，否則 A8 的 patched 對照只有 stdout、沒有收據。

## 5. 開機後的下一步（S5 → S7）

1. **C5（CODEX_MINPATCH）**：POS＝allowlist 外 0 改動＋窄回滾；NEG＝checker 改同一 diff 或無 red test → `UNBOUNDED_PATCH_OR_REGRESSION`。可用 writeset 覆蓋檢查當 allowlist 證據、用 patch sha 前後比對當 checker 未改動證據。完成後把 5 條 edge 併成 `s5/S5_CLOSURE.{json,md}`。
2. **S7 TQAEP**：`ledgers/S5_S7_INVENTORY.json` 已有 282 案＋282 `case_sha256`；需 case→TestClass/OracleType/G00–G14 映射（12 TestClass／8 OracleType）。
3. **S8**：B5 已量到 SP host 不可得 → 三職能以 `NoFit`／`PARK` 具名交付，不補數。
4. **S3c AO** 若仍未回：重派或記 `AO_UNRETURNED`，不得以本地自測替代。

## 6. 阻斷與天花板（照原樣保留，未放寬）

- `OPS ECP 32 子契約`：正文不存在，實測 31 條出口 → `NOT_LOCATED`，不補數。
- 11 條 OPS edge `PARK_NO_IMPLEMENTATION`（每條需該 domain 具簽 receiver＋該 edge oracle）。
- 22 WP DAG：16 列 PASS 無 `evidence_ref` → `NO_EVIDENCE_REOPEN`。
- WP-12／13／20 的 work_queue 仍 **FAIL**；未經原 Checker 不得改列。
- `s5/B5_PROBE.json`：三職能無 host 身分（`SP_HOST_LOAD_UNPROVEN`），解除條件＝在會發身分的 host 上跑並留 command+exit+sha。
- `scripts/review_lock.py` 未版控；`TT-20` 無記錄；設定漂移 TT-R20-10 刻意不回填。
- F1（不同 issuer 憑證）已由 owner 更正為「單一 owner == issuer」，改以信封 sidecar 解決，不再是 HOLD。

## 7. Owner 信封（關機即失效）

- window `WIN-91b01b7cd918`，task `FHS-MSC-R21-NATIVE-E2E-20261101`，scope `permit_sign,admission_bundle_sign,registry_row_sign`，ceiling `HOST_OPERATIONS`，max_ops 40，`opened_at` 2026-11-01T13:55:31Z，`expires_at` 1793541331（台北 2026-11-01 21:55）。
- broker `proc_779bee03f526`（pid 19616、listener `127.0.0.1:1654`）仍 running；**關機後需重開信封**（`owner_window.py open …`），舊 window 不可沿用。
- 本輪沒有任何 op 需要用印（ops 3/40 起算，之後未再動用）。

## 8. 已知陷阱（本輪實際踩過，開機後務必沿用）

1. `HERMES_HOME` 被 shell 遺留污染 → 一律 `unset HERMES_HOME` 再跑。
2. 複製 fixture 帶 `__pycache__` → 舊 .pyc 讓 NEG 以「錯的理由」拒絕（A8 首跑）。每次 swap 前清 bytecode 並斷言身分。
3. 相對路徑 → grant writeset 的絕對路徑對不上，得出假的 `WRITESET_EXCLUDES`。一律絕對路徑。
4. hotswap 副本放在 `PIPD/` 套件樹外 → `ModuleNotFoundError: pipd_ls_sp`。副本需 `PIPD/tools/` ＋ `PIPD/src/` 同層。
5. selector 的 ledger row 沒寫 `subject` → 守衛惰性（跑了但永不觸發）。B4 因此重跑一次才得到真結果。
6. `python - <<'PYEOF'` 內含 `\n` 的字串會被吃掉 → 含跳脫的程式碼一律用 `write_file`／`patch`，別用 heredoc。

## 9. 檔案指紋（sha256 前 16／bytes）

| 檔 | sha256 | bytes |
|---|---|---|
| `s5/A8_CASES.json` | `d23636b4ced3319c` | 3,208 |
| `s5/B3_CASES.json` | `0ff6a2949e59731a` | 3,624 |
| `s5/B3_PATCH_TEST.json` | `a04d1b4b224ed495` | 2,040 |
| `s5/B4_CASES.json` | `356830001f82d79f` | 2,611 |
| `s5/B5_PROBE.json` | `f1ea29f03e8849e0` | 2,398 |
| `s6/S6_CLOSURE.json` | `ded23f11960ecf0f` | 7,869 |
| `ledgers/S5_S7_INVENTORY.json` | `ebe11a0070981bc7` | 6,126 |
| `ledgers/S6_EDGE_EFFECT_LEDGER.json` | `1b37b6aca682090d` | 18,532 |
| `ledgers/S6_OPS_EDGE_PLAN.json` | `476390d8845008cb` | 30,847 |
| `wp20/CELL_RESULTS_V3_1.json` | `904966220b93bf7e` | 37,700 |
| `wp20/KIND_SURFACE_RULING.json` | `c0f85cd01a7f8b19` | 5,787 |
| `wp13/C5_UNDER_ENVELOPE.json` | `8735274fb44ecbe0` | 2,346 |

工具（`var/FHS-R21-FAR-TT-20261101/tools/`）：`s5_a8_hotpath_cases_v2.py`、`s5_b3_cases_v2.py`、`s5_b3_patch_v2.py`、`s5_b4_cases.py`、`s5_b5_probe.py`、`wp20_cells_v3.py`、`wp20_kind_surface_probe.py`、`wp20_kind_ruling.py`、`build_s5_s7_inventory.py`、`build_s6_closure.py`、`update_goal_r21.py`。

## 10. 宣稱天花板

- 本輪所有結果都是 **作者端本地量測**（AUTHOR_SIDE），沒有獨立 principal 判讀 → **不得**標 `PASS_ACCEPTED`／`NATIVE_COMPLETE`。
- 所有補丁只在副本上驗證；canonical `PIPD/tools/hotswap.py`、`HG-KSEOS/scripts/issue_grant.py`、`work_queue.py` 皆未改動。
- 沒有 push、沒有 PR、沒有 merge／tag／release。
