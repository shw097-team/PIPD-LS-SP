# CLOSEOUT — FHS-MSC B1 PIPD-LS-PKG（SKELETON SPINE REPAIRED r2-revision2，候選交付）

- 日期：2026-10-29（Asia/Taipei）
- 工作區：`C:\Projects\Agent_Workspace\var\B1-PIPD-PKG-20261027`
- 治理文件：`知識庫/…/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`（與 `var/R18-…/subject` 逐檔 sha 相同）
- **交付等級：本地啟用（LOCAL_ACTIVE）**。`sourcefreeze` 與 `release` 已由 owner 以**專用窗口**簽章（`WIN-ce63de72d674`，scope `sourcefreeze,release`，TTL 1h，2/4 ops）；仍**不是**對外釋出、也不是 native 驗收。

## 1. 已交付且本地可驗

| 項目 | 證據 |
|---|---|
| `PKG_00~08` 工作分解 | `openspec/changes/b1-native-lane-admission/tasks.md` 18/18、`openspec validate` valid |
| 三張 GWO（SBL／HGK／FABRIC） | `artifacts/GWO_SBL_EVIDENCE.json`（11 raws）、`GWO_HGK_EVIDENCE.json`（`readback_sha=c8f317e3…`）、`GWO_FABRIC_EVIDENCE.json`（4 raws、同 sha/epoch） |
| G-B（撤銷／重放） | `artifacts/G_B_EVIDENCE.json` PASS |
| 獨立稽核 | `artifacts/INDEPENDENT_AUDIT.json` PASS（四輪 v1 FAIL→v4 PASS） |
| 閘門 | `G-A 6/6`、`G-B PASS`、`GWO 3/3`、`gates_conjunction PASS`、`mission_complete=true`、`blocker=null` |
| 自檢 | `artifacts/SELFCHECK.json` **113/113** |
| Registry | rev 10、30/30 INSTALLED、`OWNER_SIGNATURE_VERIFIED`、sha256 `d70195751a48f15e…` |
| 簽章能力 | `OwnerSigningWindow@1`（tkinter UI、`winsound` 提示音、TTL／op 預算／三條硬不變量／`SIGNING_LOG`） |
| 任務開頭預授權 | `owner_preflight.py`（rc 0/10/11/14）＋`artifacts/TASK_PREAUTH.json`／`TASK_PREAUTH_LOG.jsonl` |
| 繞道封閉 | `admit.py` legacy demo 動詞對已簽 registry 一律 `REFUSED_LEGACY_DEMO_PATH_ON_SIGNED_REGISTRY`；S2/S3 改指 demo registry |
| 逐列簽章完整性 | `verify_registry()` 逐列驗 `row_body`；ceremony 對缺 sha／缺簽章列 `REFUSED_ROW_UNHASHED_OR_UNSIGNED` |

## 2. 未完成（逐項，含前置條件與可動作者）

| # | 項目 | 現況 | 前置條件 | 可動作者 |
|---|---|---|---|---|
| 1 | `release` / `sourcefreeze` | **`SIGNED`**（owner 專用窗口，`owner_freeze.py`） | 已完成；對外釋出仍未做 | OWNER（已簽） |
| 2 | `ORC-WO-B1-A3-POS` | `EXECUTED_AUTHOR_SIDE`；缺 `persisted_cursor／lease_generation` | Temporal/Redis 屬 `DEFERRED_OWNER_HOLD`（`04:1325`） | OWNER 基礎設施決策 |
| 3 | `ORC-WO-B1-B3-OPS-POS` | `EXECUTED_AUTHOR_SIDE`；缺外部 repo 真 DEV ECP 三件 | 需外部 repo 提供真實 DEV ECP | OWNER |
| 4 | `ORC-WO-B1-C4-POS` | 本輪裁決 **永久 `NOT_GRANTED`**（只收回、不擴張）；local demo grant 與 ledger NEG/SEC 證據保留 | — | 已由 agent 落檔 |
| 5 | `CR-ORACLE-001_OPEN` | `ORACLE_UNBOUND`（`DOC-05:20/667`、`L785`）；27 條 oracle 維持 `NOT_RUN` | 需 OWNER 指定 oracle owner（`10B:451` 只有 `pipd-authority-source` 能建正式 `SourceFreezeManifest`） | OWNER |
| 6 | R1 slot 具名 KB 出處 | 先前量測 31 slot `kb_names_slot=0`，本輪**未能重新推導**（`O5D_PACKET.json` 結構已變），標 `RECORDED_EARLIER_NOT_REDERIVED` | 需重建 slot↔KB 對照 | agent（另立一輪） |
| 7 | AUTHOR_SIDE 三項 | `repo_untouched` **實測為 FALSE**：PIPD 工作樹 **231** 筆未提交（多為既有輪次殘留）→ 標 `MEASURED_DIRTY_TREE`；prestate 為自製 stub → `STUB_PRISTINE_STATE`；CC 綁定為宣告式 → `DECLARATIVE_BINDING` | — | 已量測／標記 |

## 3. 不可消除的限制（不得聲稱已解）

- **F-45**：owner 金鑰在簽章瞬間存在於進程記憶體；同一 OS principal 可傾印。已用 passphrase envelope＋ACL＋窗口收斂，但**不可防**。
- **F-52**：另一支程式可自建 owner key 並重新 enroll；**可偵測（C109/C110/C113）不可防**。窗口期內 `owner_enrollment` 變更一律 `REFUSED_ENROLLMENT_CHANGE_IN_WINDOW`，但窗口外僅能偵測。
- 27 條 oracle 在 `ORACLE_UNBOUND` 下不得補簽。

## 4. 主張上限

| 命題 | 狀態 |
|---|---|
| `PKG_00~08` 的本地工程與證據 | **DELIVERED_AND_LOCALLY_VERIFIED** |
| 獨立稽核 | **PASS**（四輪收斂，稽核者為獨立車道） |
| Native E2E（真 native bundle） | **NOT_CLAIMED**（無外部 DEV ECP／無 native source） |
| Release／SourceFreeze | **SIGNED**（本地啟用授權；非對外釋出） |
| 外部驗收 | **NOT_CLAIMED** |
| 本地啟用 | **ACTIVE**（`artifacts/ACTIVE.json`，rollback = 刪除該檔） |
