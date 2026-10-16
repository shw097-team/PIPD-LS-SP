# Checker、Owner 交還、TT 與回復點

**Round** `S4-FINAL-PR18-CLOSEOUT-20261016`｜**STATUS_AS_OF** 2026-10-16 (Asia/Taipei)

## 1. 獨立檢查者的能力與限制（不得誇大）

- 車道：`VERIFY_SECURITY`（`VERIFY_ONLY`，不寫候選、不修補、不建 WorkOrder）。
- **模型軸**：maker 與 checker **同臂**（registry `SOD006-C3`，owner order `OWNER_ORDERED_IN_FORCE`）→
  **模型軸獨立性不存在**；剩下的分離只有「程序／車道／證據路徑」＋不得自我驗收。
- 本回合裁決：**`PARTIAL`**（見 `checker_verdict_s4f.json` 與逐字 `VERDICT_S4F_VERBATIM.txt`）。
  收據為逐字擷取，**不可編輯**。
- 裁決要點：車道沙箱為 **read-only 且外送 TCP 全數被拒**（`WinError 10013`），故 brief 要求的
  live-HTTP 複驗全部為 `UNVERIFIABLE`；車道改以**自身執行的 git 讀取**獨立確認——
  C2 PR #18 四路徑非產品樹（`+465/−23`）、C3 封包 `SHA256SUMS` **8/8 重算相符**且 blob 對分支
  `match=10 diff=0`、C5 ZIP 56 成員／單 root／8 SKILL.md／無逃逸、C6 `main` 未動且兩 PR 皆**未合併**
  （`merge-base --is-ancestor` exit 1）——並明言「可測者**無一虛假宣稱**、多項**無法測**」。
- 車道收據清單（本次運出）：`['lane\\verify_s4f\\logs\\attempt-23372-1792160039-1-stderr.txt', 'lane\\verify_s4f\\logs\\attempt-23372-1792160039-1-stdout.txt', 'lane\\verify_s4f\\run.txt', 'lane\\verify_s4f\\verify_turn.json', 'lane\\verify_s4f\\verify_turn.json.attempts.ndjson']`
- **裁決範圍**：本裁決涵蓋 `219e92ba…` 推送時的**十個**封包檔；其後新增之裁決索引／逐字全文／收據副本
  為**裁決後追加**，已在 `checker_verdict_s4f.json#verdict_scope` 明示。
- 車道並附帶觀測：PIPD 克隆的**本地分支 `main`** 是陳舊獨立 ref（`2245914`，相對 `origin/main` 0 ahead／153 behind），
  屬本地 worktree 產物、**非**受驗遠端主體。

## 2. Owner 交還（`OWNER_ACTION_REQUIRED`，本回合**不代行**）

| # | 動作 | 精確主體 | 完成客觀條件 | 阻擋結案？ |
|---|---|---|---|---|
| 1 | 合併 PR #18 | head `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20` | 於 GitHub 介面合併；合併後回讀新 `main` SHA 與主線 affected checks | 否 |
| 2 | 合併 PR #17 | head `97a01dab95bc53a08b8c372e3c3b04e69a923d7d` | 同次或後續；單檔 readback，不改產品程式 | 否 |
| 3 | 簽認階段結案 | `S4_PREVIEW_MVP_PHASE = TEMP_CLOSED` | 人類簽名或明示「尚未簽」；**未簽不得寫 `OWNER_RATIFIED`** | 否 |
| 4 | 保持 `.4` 不變 | tag object `0618d73c725da0d8c3280f99ef369d13741b5197` → commit `cc6c1930765160697e7e51d6e37735b9220a30db` | 不重打、不換資產、不改 checksum | — |
| 5 | （條件）真實帳號同 ID 更新 smoke | 有上傳權限的帳號 | 1 POS ＋ 1 缺來源 typed NACK ＋ 越權 NEG ＋ 可回滾 | 否 |
| 6 | （觸發式）新版本 | 只在真要分發 `.4` 之後的 `main` 能力時 | 新 immutable tag／Wheel／ZIP／served readback | 否 |

## 3. 未關閉項（TT 登錄）

| TT | 類別 | 內容 | Owner |
|---|---|---|---|
| `TT-S4F-ORACLE-DISAGREEMENT` | ORACLE | KP 個別 R04 極性正規化歷史；回到原始上游語義，不重寫 | Owner |
| `TT-S4F-CHECKER-BASIS` | SoD | maker=checker 同臂；若日後要求模型軸分離，需改 registry（**本回合未改**） | Owner |
| `TT-S4F-HOST-UAT` | HOST | 四宿主同版有效載入＋POS/NEG/越權未做 → `HOST_QUALIFIED` 未授權 | Owner |
| `TT-S4F-SERVED-FALLBACK-HEADER` | DOC | `.4` 內 fallback 表頭仍為 `.3`；下次發版重建 | Owner |
| `TT-S4F-PR14-PR15` | OTHER | CNV/HGK 他案 Draft；**不因本結案提升** | 他案 Owner |

## 4. 回復點（rollback）

- 產品分支與 `main` **未被本回合寫入** → 回復點 = 不需回復。
- 證據分支：由既有尖端 `71e70f747c30bcd42d407fd045261a9669345ddb` 續開；如需回退，丟棄本回合分支即可，產品不受影響。
- 本回合無 merge／tag／release → 無發行層回復動作。
- 若 Owner 已合併 PR #18 而後欲回退：`git revert -m 1 <merge_commit>`（文件/測試/guard 一路徑，無產品程式）。

## 5. 反證搜尋（五類 STOP RULE）

| 類別 | 搜尋方式 | 結果 |
|---|---|---|
| (a) 新鮮安全突破 | ZIP 路徑逃逸／越權／grant 檢查、寫入集負例、privZIP 結構 | **未命中**（見 `private_plugin_status.json`、`pr_and_ci_raw_index.json`） |
| (b) `MUST NOT → MUST` 源條文錯誤 | 對照 canonical/PKG/KP locator 與本回合裁決 | **未命中**（唯一分歧為 KP R04 極性，已列 ORACLE_DISAGREEMENT） |
| (c) Trace False PASS | 追蹤 `docs/install/README.md` 修正與 guard mutation 是否真會 FAIL | **未命中**（guard 於舊文字可重現 FAIL） |
| (d) 供應鏈資產與已宣稱雜湊不符 | 重新下載 `.4` privZIP 逐 byte 計算 | **未命中**（68,357 B／`545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75` 完全相符） |
| (e) 用戶實際收到不可用版本 | 私人帳號真安裝／更新 smoke | **NOT_RUN**（`HOST_OWNER`）→ 因此**不得**主張 (e) 已排除，僅能說未觀測 |
