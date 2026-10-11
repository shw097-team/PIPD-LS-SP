# S4R2M 回合總結報告 — 條件式合併與 Preview.3 閘門

**回合**：`S4R2M-20261012-merge-and-preview3`
**控制平面**：HG-KSEOS（唯一 normative/control plane）；Hermes = 受治理 orchestration runtime
**執行日期**：2026-10-12（Asia/Taipei）
**狀態**：`MERGE_READY_HITL_PENDING`（除外部驗收／Owner 授權外，可做事項已全部完成）

---

## 0. 六個 Gate 的實測狀態（不得互相折抵）

| Gate | 實測狀態 | 證據 |
|---|---|---|
| `PROMPT_COMPILE_PASS` | **PASS**（native，本回合新編，非移植舊收據） | `compiler/S4R2M.*.receipt.json`；0 errors；duplication 0.0166 / 0.0047 |
| HGK Admission | **PASS** | 4 Requirement → 4 TaskSpec → 4 WorkOrder；`admission/S4R2M_ADMISSION_READBACK.json` |
| Maker Test | **DONE**（= candidate evidence，不等於驗收） | `verify/M2_ISOLATED_REGRESSION.json`：9 模組 107 tests OK |
| Checker Verdict | **PARTIAL**（`non_mutation PASS`） | `verify/VERIFY_RECEIPT_OFFICER.json` |
| Merge | **NOT_MERGED**（`MERGE_READY_HITL_PENDING`） | `evidence/M3_READINESS.json` |
| Release / Production | **NOT_PUBLISHED / NOT_CLAIMED** | `preview.3` 不存在 |

新增第 7 個必述狀態：**KANBAN / SWARM / GSTACK / OPENSPEC 已啟用**（`kanban/`），14 條 named-method activation invariant 全部 0 違反。

---

## 1. 主體 tuple（不得混同）

| 角色 | commit | tree |
|---|---|---|
| base（遠端 `s4-r2` 頂端，未動） | `3f6c7dc52b73cfcba03dccbe576ade75bec1890d` | `de2c8541d22d0ac5046e3cfda5a4368dfced7bd5` |
| **C** 受驗產品變更 | `58a1f334464675081d0573476d70e2165143bdd8` | `c9d96316ea7717ab8cb74f0858dd6f05d0ec7db4` |
| **E** 凍結證據受驗主體（Officer 實測） | `dfa52053d34535d63a8157e0a70584c43f175eed` | `b427f0312d74c3491f4076e48ecae8884bbc5038` |
| 遠端 `main` | `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7` | `13edaa8ec8775506015310d1c60c977ff5d09e9c` |
| 公開 `v0.1.0-preview.2` | `8faa64e581e8c25f5ec355475e29561847da3ead` | 未動 |
| frozen checker product | `7c00b64960d86fc1e94848c9955c512a3626a85f` | 未動 |

`main` 為 C 的祖先 → 整合形狀為 **fast-forward**，不產生 merge commit、不改寫歷史。

---

## 2. M1 / M2 / M3 / M4 逐項處置

| WO | 狀態 | 實測結果 |
|---|---|---|
| `WO-S4R2M-DOC-CAL-01`（M1） | **DONE** | README 新增 `## Choose your path: CLI or Skills`（置於 Start here 與 Quickstart 之間）；`--root` 敘述改為與 `cli.py` 一致；新增可執行正例 ×3 與拒絕例 ×1；新增 `tests/test_s4r2m_docs_route.py` |
| `WO-S4R2M-FOCUSED-VERIFY-02`（M2） | **DONE** | 於**位元等價可寫 clone** 跑 9 模組 107 tests 全 OK；exact-set 19 schemas + registry / 8 skills / 13 CLI；受驗主體位元前後一致 |
| `WO-S4R2M-MAIN-INTEGRATION-03`（M3） | **READY / BLOCKED（owner gate）** | 憑證路線已實證可用；未經 Owner 批准不得前進（見 §4） |
| `WO-S4R2M-PREVIEW3-OPTIONAL-04`（M4） | **NOT_SELECTED（owner gate）** | 版本策略已裁決並實測（見 §5），未建任何 tag / 未發任何 asset |

---

## 3. M2 隔離回歸的具名 Oracle 結果

| Oracle | 觀測 |
|---|---|
| C1 主體身分 | `dfa52053` / `b427f031`；`git status` 乾淨 |
| C2 非變異 | 受驗主體 1399 tracked files + 4 gitlinks，前後 digest 相同 |
| C3（F01 分流） | `README.md:26` 明示 wheel 與 chat-host skill pack 為兩個不同 artefact |
| C4（F02 `--root`） | 文句與 `cli.py:39/69` parser 事實一致 |
| C5 執行正負例 | 真 exit `0, 0, 0, 2` |
| C6 exact-set | 19 canonical schemas / 8 skills / 13 CLI |
| C7 受影響 suite | 9 模組、107 tests、`OK`、無 skip |
| C8 ProfileBinding 負例 | 7 項全拒且具 field 命名；合法 record 通過 |
| C9 diff 範圍 | 僅 `README.md` + `openspec/**` + `.hgk/**`；`src/**`、`schemas/**`、`dist/**` 未動 |
| C10 claim 邊界 | **INCONCLUSIVE** — Officer 對既有 claim-ceiling 表（`README.md:247`）保留判斷；該行早於本回合存在，且已正確限縮（`G-RELEASE_FULL_PASS is NOT granted`） |

**Officer 提出的唯一 disagreement（已修正，未塗銷）**：merge 記錄原寫「1341 files」，與凍結主體 `dfa52053`（1399 files）不符。兩者量測不同主體（M2 在 `58a1f334`，早於證據 commit），已於 `MERGE_DECISION_S4R2M.md` 改為明確綁定各自主體。

---

## 4. M3 — 為何停在 Owner Gate，以及已備妥的單一動作

**憑證路線（實測，未外洩任何值）**：

| 檢查 | 結果 |
|---|---|
| broker 預設來源（`Fine-grained personal access tokens.txt`） | `GET /user` → **401**（與 R11 歷史一致，已死） |
| `HGK_CRED_FILE` 指向較新的 owner 憑證 | broker `preflight` → **OK**，`cred_api_valid PASS`（login=`shw097`） |
| repo / ref 讀取 | `200` / `200`；`git ls-remote` exit 0 |
| **寫入能力（不變異驗證）** | `git push --dry-run` **exit 0**，回報 `4445db5..3f6c7dc HEAD -> main`；**遠端 ref 確認未變** |

→ 憑證具備寫入能力，且 `main` 具備 fast-forward 條件。**唯一缺件是 Owner 批准。**

裁定依據（FAR `FAR-PIPD-S4R2M-RELGRANT-003.md`）：既有 R5Q 授權的 `action` 為 `create_new_immutable_tag_and_prerelease`，**未列舉「推進 main」**；且本回合 governing prompt 明載 `human_gate: REQUIRED_FOR_MAIN_INTEGRATION_AND_PUBLIC_RELEASE`。故本回合不自清此閘門。

**Owner 若批准，將執行的完整命令**：
```
HGK_CRED_FILE=<live credential path> python HG-KSEOS/scripts/cred/cred_broker.py run -- push origin main
```
批准後續動作：讀回 `refs/heads/main`、確認 `.2` tag 仍指向 `8faa64e5…`、確認 release asset 清單未變。

---

## 5. M4 — 版本策略已裁決（未發行）

實測（真 `packaging.version.Version`）：

| 候選 | 相對已發布 `0.1.0` |
|---|---|
| `0.1.0a3` / `0.1.0b3` / `0.1.0rc3` | **LESS**（不可宣稱自然升級） |
| `0.1.0.post1` | GREATER（語義不符：內容已變更） |
| `0.1.1a3` | **GREATER** ✓ |

**裁決：`0.1.1a3` / tag `v0.1.1-preview.3`**（FAR `FAR-PIPD-S4R2M-VERCHOICE-004.md`）。已發布 wheel 名稱實測為 `pipd_ls_sp-0.1.0-py3-none-any.whl`，.1/.2 同名 → 不改版名會延續同名不同 bytes 的歧義。

**未建 tag、未產 wheel、未發布。** 發布後仍只可宣稱 `SCOPED_PREVIEW`。

---

## 6. 8 項 Finding 與 10 項 TT 的處置

| Finding | 處置 |
|---|---|
| `F01` CLI/Skills 分流 | **CLOSED_IN_ROUND**（M1 + Officer C3） |
| `F02` `--root` 措辭 | **CLOSED_IN_ROUND**（M1 + Officer C4/C5） |
| `F03` 未併入 main / 未出新 Wheel | **PARTIAL**：M3 待 Owner；M4 未選 |
| `F04` version grammar | **DEFERRED_WITH_TRIGGER**（FAR `VERGRAM-002`；現行合法輸出為 `"1"`，不得套 semver regex） |
| `F05` 法位差／未在唯讀主體跑 suite | **CLOSED_IN_ROUND**（位元等價 clone + 前後 digest 比對） |
| `F06` native web load | **NOT_RUN**（README 已如實標示未實測） |
| `F07` 12-axis risk | **CLAIM_BOUND_UNCHANGED**（`NOT_ASSESSED` 維持誠實） |
| `F08` S5+ | **OUT_OF_SCOPE** |

TT：`01` 歷史保留；`02` **有遠端新證據**（舊 PAT 401、新憑證可用）；`03` 另開 full gate；`04` 視 M4；`05` `NOT_RUN`；`06` `ALREADY_CLOSED_NO_REDO`（4 mutants 仍被拒、合法 record 仍通過）；`07` OUT_OF_SCOPE；`08` 遠端分支可讀（本回合未 push）；`09` **CLOSED**；`10` 以方法解決。

**本回合新增 TT**：`TT-S4R2M-CREDSRC-01`（broker 預設來源指向已死憑證，需改指向 live 憑證或移除以避免誤導）、`TT-S4R2M-MAINGATE-02`、`TT-S4R2M-NATIVEWEB-03`、`TT-S4R2M-VERGRAM-04`。

---

## 7. 本回合自我修補紀錄（誠實揭露）

1. **Officer 第一次執行判定 `INCONCLUSIVE` / `non_mutation FAIL`**：原因是編排在 checker 執行途中改了 `openspec/.../tasks.md`，且該次修改**提前把 6.6 勾成完成**——在沒有任何 Officer verdict 之前自行宣告獨立驗收完成。該收據保留為 `VERIFY_RECEIPT_OFFICER_RUN1_INVALIDATED.json`（**不是 verdict**），勾選已回退，主體重新凍結為乾淨 commit 後重跑。
2. **第一次 mutant probe 失敗**：`validate_record` 需要 `Path` 而我傳 `str` → `TypeError`。這是**探針缺陷**，非產品缺陷；已修正重跑，產品未動（記載於 `M2_PROFILE_MUTANTS.json`）。
3. **Officer 抓到我自己的文件不一致**（1341 vs 1399 files），已修正並保留其 disagreement 原文。

---

## 8. 不得宣稱事項（Claim Ceiling，全部維持）

`FULL_S0_S4_INDEPENDENT_PASS = NOT_GRANTED`；
`G_RELEASE_FULL_PASS = NOT_GRANTED`；
`PRODUCTION_VERIFIED = NOT_CLAIMED`；
`S5_RUNTIME_READY = NOT_CLAIMED`；
`WEB_NATIVE_EFFECTIVE_LOAD = NOT_RUN`；
`S4R2_INDEPENDENT_CHECKER = PARTIAL`（**不是** FULL PASS，也**不是** FAIL）；
`v0.1.0-preview.2` 維持公開 `GO_WITH_LIMITATIONS`。

**本回合未 push、未 merge、未建 tag、未發 Release、未改任何公開 asset。**

---

## 9. Owner 下一步（兩個獨立決策，可只做第一個）

1. **M3**：是否批准把 `main` fast-forward 至 `dfa52053`（或僅產品 commit `58a1f334`）。
2. **M4**：是否選擇發行 `v0.1.1-preview.3`（若選，版本策略已定，施工順序見 FAR `VERCHOICE-004` §5）。

未批准則本回合以此結束狀態封存；candidate 與全部證據保存在 `s4r2m-merge-wt`，rollback 指標見 `CANDIDATE_TUPLE.json`。
