# R5Q｜OWNER PREVIEW DECISION PACKET（一頁）

**輪次：** `R5Q-20261010-s4-owner-opensource-preview`
**任務契約：** `PIPD-LS-SP-R5Q-OWNER-OPENSOURCE-PREVIEW-20261010`
**日期：** 2026-10-10 / Asia-Taipei
**裁決狀態：** `RESOLVED_BY_OWNER`（Owner 於本輪追加決策：授予開源授權，並指定由 FAR 制定最佳方案後直接執行）

---

## 1｜受驗主體（精確值，不得以近似值替代）

| 物件 | 精確值 |
|---|---|
| Repo | `https://github.com/shw097-team/PIPD-LS-SP`（public） |
| 工程基線分支 | `r5p-post-challenge-repair` |
| 工程基線 commit / tree | `2efc84eac8e1939092c748d5b389b6dd72267aef` / `e254ea23243e0c767bf79fc647b82341493a231c` |
| 基線 Wheel SHA-256 | `bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76`（38 members） |
| `main` | `3aebbbce948871c07b875ab92acf263d298ecf38`（R3；**不作為 Preview 來源**） |
| Manifest 舊 build identity | `WHEEL_MANIFEST.candidate_head = 7c5bc585…`（**非** release tip，CORR-07） |

新 Preview 的 release commit 與 wheel hash 由授權落地後的凍結產生，**不可能**等於上述基線值。

## 2｜技術判定（本輪不重做）

| 項目 | 值 |
|---|---|
| S4 技術建議 | `S4_OPEN_SOURCE_PREVIEW_TECHNICAL_GO = YES` / `GO_WITH_DISCLOSED_LIMITATIONS` |
| 完整 S0–S4 獨立挑戰 | `PARTIAL_CHALLENGE` |
| 建議動作 | `NO_BROAD_REPAIR`（不啟動 R6） |
| SPEC/DEL 分母 | `28 S4_ACTIVE_EVIDENCED / 10 S4_ACTIVE_GAP / 19 DEFERRED_BY_INSTRUCTION` |

## 3｜Owner 決策（本輪已記錄）

| 決策欄位 | 決定 |
|---|---|
| 決策 | **`APPROVE_LICENSE_AND_PREVIEW`** |
| SPDX 識別碼 | **`Apache-2.0`**（由 FAR-PIPD-R5Q-LICENSE-001 依二階段準則裁決；Owner 委派） |
| 授予範圍 | 全倉庫 agent-authored 工程輸出 + Owner 自有 corpus 之衍生敘述 |
| 排除清單 | 三支 donor Skill plugin 內容（未逐字進入本樹，不主張權利）；未來證實含第三方權利之檔案自重證起排除 |
| 公開行為 | 於 `shw097-team/PIPD-LS-SP` 建立**新的不可變 tag** 與 **prerelease**，指向明確 release commit；**不覆寫 `main`、不 force-push、不移動既有 tag** |
| Tag／Release 命名 | `v0.1.0-preview.1`（發佈前先驗證無碰撞） |
| 既有公開 README／分支修改 | 允許：README 首屏改指向 Preview tag；不重寫歷史段落的既有收據 |
| 憑證 | 由 process-scoped credential broker 於記憶體內使用 Owner PAT；最小權限；不得落任何輸出 |

## 4｜可獲准發布的工件

1. 受 Apache-2.0 涵蓋的 **source archive**（`v0.1.0-preview.1` tag 的 tree）。
2. 對應的 **Wheel**（重建後、含新 SPDX metadata；**非** `bb070a6f` 舊 bytes）。
3. `SHA256SUMS`（wheel + source archive）。
4. `README.md` / `ACCEPTANCE.md` / Preview Notes / Known Limitations。
5. 授權與 SBOM／provenance 摘要（`LICENSE`、`NOTICE`、`SBOM.cdx.json`、`PROVENANCE.md`）。

## 5｜必須對外揭露的 Known Limitations

| 項目 | 揭露內容 |
|---|---|
| `DEL-018 RELEASE_MANIFEST@1` | `tools/build_publication_manifest.py --check --current` **exit 1（維持 FAIL/EVIDENCE_GAP）**；未收錄 `tests/test_git_object_reader.py`、`tests/test_doctor_schema_truth.py`、`tests/test_tqaep_design_positive.py` |
| 完整獨立驗收 | `PARTIAL_CHALLENGE`；不得聲稱 `FULL_S0_S4_INDEPENDENT_PASS` |
| 57-row 分母 | `28/10/19`；`EVIDENCED ≠ PASS` |
| Windows／Host | 未全面認證 symlink/junction/reparse；限定已測環境與 scratch/dry-run（`TT-R5P-01/06`） |
| 完整性自動讀回 | 無 install-time/startup cryptographic readback，僅發行 SHA256 人工核對（`TT-R5P-02`） |
| 發布 Checklist | S5 HGK live、S6 GENIE、S7 JIT、S8 SWOF/SGM、PRE-W3、22 未啟用外部技術 **全部 deferred** |
| Production | `PRODUCTION_VERIFIED = NOT_CLAIMED` |

## 6｜Stop-ship 清單（出現即停止效果操作）

真實可再現的任意路徑刪寫／越權副作用；明文 secret 或 PII 外洩；必要 Schema/CLI 在預定環境無法安裝；核心 `intake → PI → PD → ECP/TQAEP` 普遍不可用；公開物件 hash 不符；散布未經合法授權內容；無有效 Grant 卻宣稱 OSI 授權；偽造 Independent／Release／Production PASS。

## 7｜Restart / Side-effect 揭露

- **本輪會寫入的**：`PIPD` 產品樹（授權／版本／文件最小差異）、`PIPD/dist`（重建產物）、`PIPD/.hgk`（本輪證據樹）、`PIPD/openspec/changes`（本輪 change）、`知識庫/實作相關DOC/PIPD/實作證據`（驗收主檔），以及 GitHub `shw097-team/PIPD-LS-SP` 的新 tag 與 prerelease。
- **本輪不會寫入的**：`HG-KSEOS`、`Fabric`（唯讀取用）、`main` 分支、既有 tag、既有歷史收據。
- **Credential**：`C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt` 僅在程序中讀取；本輪任何輸出皆不含其值。

---

**投遞對象：** 有權 Owner（已裁決）
**本文件自身不是 GitHub Release 頁面，也不是獨立驗收收據。**
