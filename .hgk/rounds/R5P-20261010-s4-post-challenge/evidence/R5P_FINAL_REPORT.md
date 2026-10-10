# R5P 終止報告（§9 固定順序）— PIPD-LS-SP R5 外部挑戰後 S4 最小封口修補

**round**：`.hgk/rounds/R5P-20261010-s4-post-challenge/`　**日期**：2026-10-10

## 1. 編譯 / 准入

- `PROMPT_COMPILE_PASS`（真實原生 receipt）：`compiler/R5P.lint.raw.txt`、`R5P.activation.raw.txt`、
  `R5P.acceptance.raw.txt`、`R5P.compile.raw.txt` 四者皆 `verdict=PROMPT_COMPILE_PASS`、`error_count=0`；
  `task_id=PIPD-LS-SP-HERMES-R5P-POST-CHALLENGE-S4-FOCUSED-REPAIR`，
  `contract_sha256=d24353122a4bf9a570f64f84c2fb85453d558ab31996431346e4b098c5e43113`。
  （該收據之 `claim_ceiling` 欄位為 `EXTERNAL_ACCEPTANCE`，係沿用 R5 契約形狀；本輪操作上限仍為
  `CANDIDATE_ONLY`，見 INC-R5P-06。）
- HGK admission readback：`admission/r5p_admission.json` — 5 個 requirement 皆 `FROZEN` 並取得
  `taskspec`／`workorder`（DIG-00{1}、AO-002、CAL-003、TQAEP-004、DOC-005），經 typed
  SharedSpine/ProjectLifecycleController 過渡，無 raw SQL；checkpoint `CK-20261008-DD900DB9`。

## 2. R5_S4_REPAIR_STATUS

- baseline：`0f06eec96386b7349db8b41ac6cf9c7455d326f1` / tree `1f7564282fd708fab2ddeadbbbe4e424a3c564be`
- 新主體：`194f1774e8e852f954d141c48389a74b0f0e302a` / tree `b1ec0abf4799fdc917aaa23dc75885b302407ee5`
- 修改路徑：18 條（見外部證據主檔 §2）
- WO 判定：DIAG-001 **PASS(candidate)**、AO-002 **PASS（四輪獨立，分布於 commit 鏈）**、
  CAL-003 **PASS(candidate)**、TQAEP-004 **PASS(candidate)**、DOC-005 **PASS(candidate)**
- F-R5-01～10 逐項：見外部證據主檔 §4（3 項 PARTIAL→TT，2 項 DEFERRED，5 項 CLOSED）

## 3. S4_USER_OPERABILITY_RESULT

- source + install：13 CLI 正反例與 UAT-00～12 之 PASS 證據為 `uat/out2`（27 PASS / 2 INFO / 0 FAIL，
  綁 wheel `bb070a6f…`）。`uat/out3` 之 5 FAIL 為 round scratch 汙染（root 內 dangling symlink，
  INC 已揭露），非產品回歸，且**未被計入任何 PASS**。
- perf Gate：分母已改為內容定址之 validated obligation；三種灌水攻擊皆測得超標 FAIL；歷史
  `343547 > 20000` 保留為非投票列（`evidence/perf_budget_check.json`）。
- Maker 未自封 Independent PASS：獨立判定一律引自 `ao/out/AO_VERDICT*.json`。

## 4. 綁定與位置

- branch `r5p-post-challenge-repair`（**本機候選，未推送**；`main` 仍為 R3）
- wheel sha256 `bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76`（38 members）
- bound product digest `6120cf3775ae522fbabb550f12b39bb6b682d88d8dabc8b247ec093f41775c0e`（288 檔）
- 外部單一證據主檔：`C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R5_POST_CHALLENGE_S4_EXTERNAL_EVIDENCE.md`
- 不可公開 raw 之索引：`evidence/EVIDENCE_RETURN_PACK.json`
- resume 指令：見 `CHECKPOINT_R5P.json` 之 `resume_commands`
- TT/HITL：`evidence/TT_REGISTER_R5P.json`（7 項 open，owner 逐一具名）

## 5. 終局與分流

S4 定向修補**停止**。S5（HGK live receiver/SharedSpine）、S6（GENIE adapter/host parity）、
S7（JIT routing）、S8（release/promotion/HITL）與 licence 全部維持 deferred，未自行升權。
claim ceiling `CANDIDATE_ONLY`；`HUMAN_RATIFIED / RELEASED / PRODUCTION_VERIFIED` 一律**未**繼承。
