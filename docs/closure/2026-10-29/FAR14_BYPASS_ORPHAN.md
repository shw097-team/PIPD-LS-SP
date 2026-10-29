# FAR-14 — F-49 繞道孤兒：admit.py 的 demo 簽章動詞與「第二簽章路徑」

- 指令：對「admit.py 仍留 init-keys／sign-canary（第二簽章路徑）＋無檢查禁止另建 owner key 並 re-enroll」做 FAR。
- 裁決順位：**對齊 `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` ＞ Native E2E 閉環 ＞ 無人值守 ＞ 高必要性 ＞ 不過度治理／不過度工程化 ＞ 低阻力 ＞ 高效率**。
- 治理文件位置：`var/R18-FHS-SKELETON-SPINE-20261029/subject/`（`01_BODY/` 已解壓，含 84 entries；zip 同名 13.3 MB）。

## 1. 條文對照（先確認這是不是規格問題）

| 條文 | 原文 | 對 F-49 的意義 |
|---|---|---|
| `01_BODY/01_PRODUCT_AUTHORITY_SPINE.md:1432` | NEG「**非原 Owner 自建第二 Issuer**」 | 「另建一把可簽的 key」本身即為條文列名的 NEG |
| `01_BODY/04_FABRIC_HGK_CONTROL.md:132` | 「只有**真受保護 HGK Issuer** 可發原生 WorkOrder/Permit/ExecutionAdmission，PLAN/TPM/Codex **不得自己簽**」；NEG「任意字段／過期批准→NACK，**不借 demo key**」 | **明文禁止借用 demo key**，`sign-canary` 正是此形狀 |
| `01_BODY/04_FABRIC_HGK_CONTROL.md:98` | 「未授權 principal **無法直接修改** active pointer／loader cache」 | 任何直接寫 registry 的路徑都違反此不變量 |
| `01_BODY/06_FHS_EXECUTE_HERMES_RUNTIME.md:103` | 「不建立…或**可自簽第二 queue**」 | 第二簽章路徑＝第二 authority |
| `01_BODY/02_PIPD_LIFECYCLE_AND_TPM.md:28`、`07_ACCEPTANCE_CHALLENGE.md:129`、`09_SBL_DOC00_13_FULL_UPGRADE.md:375` | 「Maker 輸入 receipt 字串不能自簽」→ `SELF_ACCEPTANCE_DENY`／`DOMAIN_U15_2_VIOLATION` | demo 自簽一旦被當成驗收即為 domain violation |
| `01_BODY/09A_R15_949_ORIGINAL_ATOMS.md:9386` | R15-854「HGK Native **single issuer**」 | 單一 issuer 是原產品原子要求 |

**結論**：F-49 不是衛生問題，是**條文明列的 NEG 形狀**（借用 demo key／自建第二簽章路徑）。我先前說「風險高」需要按量測修正如下。

## 2. 量測（在副本上做，不動 live）

把 `admission/` 整份複製到隔離目錄（`REG` 是相對檔案位置，所以副本自成一體），在副本上跑 legacy 動詞：

| 步 | 觀測 |
|---|---|
| 起始 | `rev 10`、`OWNER_SIGNATURE_VERIFIED`、owner `d42c654cd1afba80` |
| `python admit.py init-keys` | **rc = 0**；輸出 `OWNER-DEMO-DEMO-277c07267c161976`、`ISSUER-DEMO-8e993b8e505c23bf`；`owner_enrollment` 被覆寫為 `status: DEMO_KEY_NOT_OWNER` |
| 覆寫後 `verify_registry` | `REFUSED_OWNER_KEY_NOT_ENROLLED` |
| 覆寫後 `verify-and-run` | **rc = 6**、`REFUSED_OWNER_KEY_NOT_ENROLLED` |

三點判讀：

1. **偽造可驗簽的 owner 簽章：不可行（低）**——merkle root 覆蓋 enrollments，換鑰就使整個 root 失效，且重簽需要 owner 口令。
2. **破壞已簽 registry：可行（高）**——`init-keys` 直接覆寫檔案，rev 與 merkle 都對不上；恢復必須 owner 口令重簽。
3. **可達性：高**——`admission/run_s2_s3.py:49,55` 仍直接呼叫 `init-keys`／`sign-canary`，而它的 `REG` 指向 **live registry**（`admission/registry/runner-registry.json`）。任何人重跑 S2/S3 就會觸發第 2 點，且**在無人值守下無法自行恢復**（口令不在 agent 手上）。

→ 修正後的嚴重度：**偽造 = 低、破壞 = 高、可達性 = 高**。這是「可用性＋治理」缺陷，不是「可偽造驗收」缺陷。

## 3. 選項

| 案 | 做法 | 對齊 | 可重現 | 成本 | 判定 |
|---|---|---|---|---|---|
| 甲 | 直接刪 `init-keys`／`sign-canary` | 達成 | **斷**（S2/S3 無法重跑） | 5 分 | 不可 |
| 乙 | 守衛：目標 registry 已有 `owner_signature` 時回 `REFUSED_LEGACY_DEMO_PATH_ON_SIGNED_REGISTRY`（rc 6） | 達成 | 保（僅 unsigned demo registry 可用） | 10 分 | 可行 |
| **丙** | **乙 ＋ `HGK_REGISTRY_PATH` 覆寫，`run_s2_s3.py` 指向 demo registry 副本** | 達成 | 保（S2/S3 永遠在 demo 副本上跑） | 20 分 | **建議** |
| 丁 | 丙 ＋ 兩個自檢（C110 靜態：admit 以外不得用 `owner-demo.key` 對 live registry 簽；C112：S2/S3 目標必須是 demo registry） | 達成＋防回歸 | 保 | 30 分 | **建議（併入丙）** |
| 戊 | 另建 demo 沙箱框架／第二 registry service | 達成 | 保 | 100+ 分 | 過度工程化 |

## 4. 裁決：丙＋丁（守衛、路徑覆寫、兩項自檢）

理由（按順位）：

1. **對齊**：把 demo 簽章路徑限制在「未被 owner 簽過的 registry」＝條文「不借 demo key」「single issuer」的實作化。
2. **Native 閉環**：不動 30 列 registry、不動 runner、不動 GWO/G-B 證據；`verify-and-run` 行為不變。
3. **無人值守**：修補**不需要** owner 口令（純程式與 demo 路徑變更）；同時消除「重跑 driver 就 bricked、只能等 owner」的 HARD blocker 風險。
4. **不過度治理／工程化**：不加服務、不加 principal、不改 schema、不新增簽章型別。
5. **低阻力／高效率**：一次改動＋兩項自檢；S2/S3 仍可重跑且天花板自動標成 `DEMO_KEY_NOT_OWNER`。

## 5. 授權與簽章建議

- **不需要新的 owner 簽章**：本次修補不產生新 registry rev、不改 enrollment、不改 merkle root。
- **需要一次 owner 可見的變更紀錄**：`FAR14` ＋ `REPORT` 段落 ＋ 自檢 C110/C112 的 evidence，屬「作者側候選」，天花板 `AUTHOR_SIDE_REPAIR_CANDIDATE`。
- 若未來要**把 demo key 從 `admission/keys/` 移除**，那會影響 S2/S3 重現，屬另一個決策，需 owner 同意；本輪不做。

## 6. 執行方案（步驟／驗收／回滾）

| 步 | 動作 | 驗收 | 時間 |
|---|---|---|---|
| 0 | **先解決 F-50**：確認另一個 writer 是否仍在跑（live registry 已被非本 session 於 15:02:55 重簽為 rev 10；`owner_ceremony.py` 13:00、`selfcheck2.py` 13:15、`gates.py` 14:57 有外部修改） | 取 sha256 快照；若他方仍在寫，暫停本修補或交由他方接手 | 5 分 |
| 1 | `admit.py`：`REG = Path(os.environ.get("HGK_REGISTRY_PATH") or (HERE/"registry"/"runner-registry.json"))` | 預設行為不變 | 5 分 |
| 2 | `admit.py`：`init-keys`／`sign-canary` 前置守衛（偵測 `owner_signature` 存在 → rc 6 拒絕） | 在 live 副本上跑兩支動詞 → rc 6 `REFUSED_LEGACY_DEMO_PATH_ON_SIGNED_REGISTRY` | 5 分 |
| 3 | `run_s2_s3.py`：改指向 `demo/registry/runner-registry.json`（首次自動建立空白 demo registry） | 跑 S2/S3 → 產出證據，且 **live registry sha 不變** | 10 分 |
| 4 | `selfcheck2.py`：C110（靜態掃 `owner-demo.key` 對 live 的簽章呼叫）、C112（S2/S3 目標非 live） | 自檢 108 → 110，全綠 | 10 分 |
| 5 | 重跑 `gates.py`／`sync_state.py`；更新 REPORT／RESUME | `mission_complete` 不變、attribution 不變 | 5 分 |
| 回滾 | 保留 `admit.py.bak`、`run_s2_s3.py.bak`；live registry 全程唯讀，故無需 registry 回滾 | 回滾後自檢恢復 108 | — |

## 7. 明確不做

- 不刪 S2/S3 的歷史證據（既有 `artifacts/` 保留，只標 `DEMO_KEY_SIGNED` 天花板）。
- 不動 30 列 registry、不重簽、不換 owner key。
- 不引入第二個 registry service／demo 框架。
- 不把 demo key 當作任何驗收依據（C110 會擋）。

## 8. 天花板

- 修補後「另一支程式自建新 owner key 並 re-enroll」仍**可偵測、不可防**（單一 OS principal）：這需要第二 principal 或 HSM，且與本包無關，故列為已知殘留，不假稱已解。
- 本 FAR 的所有量測都在副本上完成；live registry 於本輪全程未被本 session 修改。

## 9. 附帶發現（F-50，必須先處理）

- live `runner-registry.json`：**rev 10**、`signed_at 2026-10-28T15:02:55`、merkle `dae3590f…`、owner 指紋未變（`d42c654c…`）、30/30 `INSTALLED`、驗簽通過——**不是本 session 所為**（本 session 最後狀態是 11:40 的 rev 9）。
- `owner_ceremony.py`（13:00）、`selfcheck2.py`（13:15）、`gates.py`（14:57）與新檔 `sync_gates_into_state.py`（12:08）皆有外部修改；`gates.py` 已多出 `sandbox_conjunction` 欄位。
- `RESUME_HERE.md` 仍停在 11:41 → 交接資訊已落後。
- 判讀：**有另一個 writer（另一個 session）在同一工作區推進**，且它持有口令（能簽 rev 10）。在 F-49 動手前必須先確認它是否仍在寫，否則會互相覆蓋（這正是 `canonical-change-landing` 記載的教訓）。
