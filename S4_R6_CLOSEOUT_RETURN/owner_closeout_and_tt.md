# S4 Preview MVP — 階段性結案裁決、Owner 簽核請示、殘留 TT 與終止聲明

- round: `PIPD-S4-R6-CLOSEOUT-20261016`
- candidate branch: `fix/s4r6-closeout-doc-identity-and-update-route-20261016`
- candidate commit / tree: `552bbde073806e254f84e95039f05c9767608aa1` / `a95579bf8c1bc77550d1044d12b2de7ed2028ae5`
- base: `origin/main@d3bd5456afbff21a8c8837994a49f57be3e1b97e`
- 產出日：2026-10-16（Asia/Taipei）

---

## 1. 本輪建議（工程建議，非簽核）

| 決策 | 本輪建議 | 依據 |
|---|---|---|
| `S4_PREVIEW_MVP_PHASE` | **`TEMP_CLOSED`（准予階段性結案）** | R5 核心修補已合併、`preview.4` 已發布且資產不變、R6 七個 Finding 中三個非阻斷文件項已在本輪修正 |
| `CORE_REPAIR_R5` | `PASS_SCOPED`（沿用 R6 裁定，未重作） | `main` 之 `requirements.py`／`ClaimCeiling.schema.json`／`test_atomic_requirements.py` 靜態定位命中 |
| `MAIN_INTEGRATION` | `ALREADY_MERGED_PASS` | PR #11/#12/#13/#16 merged（API 讀回） |
| `GITHUB_PREVIEW4_RELEASE` | `PUBLISHED_PASS_SCOPED` | 本輪 fresh HTTPS 讀回：tag object/target/tree 與凍結值一致；7/7 asset metadata 相符；served ZIP 位元組重算 `545e359a…` |
| `PRIVATE_PLUGIN` | `PACKAGE_PASS_ONE_ACCOUNT_INSTALL_DERIVATIVE_OBSERVED`（沿用 R6） | 本輪唯讀複核 ZIP 結構：56 entries／8 `SKILL.md`／單 root／無 traversal／無 MCP/Apps/Hooks |
| `PRIVATE_PLUGIN_SAME_ID_UPDATE` | `DOCUMENTED_NOT_EXECUTED` | 文件路徑已建立；人類帳戶 UI 未執行（見 §3） |
| `NEXT_RELEASE` | `NOT_REQUIRED_TO_CLOSE_PHASE` | `tag..main` = 11 commits 未發布，屬下一次發行 |
| `S4_FULL_PASS` | **`NOT_GRANTED`** | 四宿主未全量資格確認 |
| `HOST_QUALIFIED` | **`NOT_GRANTED`** | 同上 |
| `PRODUCTION_AUTHORIZATION` | **`NOT_GRANTED`** | 同上 |
| `PUBLIC_PLUGIN_DIRECTORY` | **`OUT_OF_SCOPE`** | Owner 決策，非缺陷 |
| `OWNER_FINAL_RATIFICATION` | **`PENDING_ACTUAL_SIGNATURE`** | 需 Owner 真實簽核，代理不得代簽 |

## 2. Owner 簽核請示（需人類決定，代理不得代行）

| # | 請示項 | 選項 | 影響 |
|---|---|---|---|
| O-1 | **本輪候選分支是否合併入 `main`？** | (a) 合併 (b) 暫不合併 (c) 要求修改 | PR 合併是 Owner 的動作；分支已推送且遠端 head 與本地候選一致 |
| O-2 | **是否合併 PR #17？**（1 檔 `ASSET_READBACK`、非 draft、+14/-0、mergeable clean） | (a) 合併 (b) 保留 | R6 已核為 `MERGE_APPROVED_SCOPE_ONLY`；合併仍屬 Owner |
| O-3 | **是否簽核 `S4_PREVIEW_MVP_PHASE = TEMP_CLOSED`？** | (a) 簽核 (b) 維持開放 | 代理僅提出工程建議，不得自簽 |
| O-4 | **是否進行 `R6-PRIVATE-UPDATE-SMOKE`？** | (a) 由 Owner 以有更新權限的帳戶執行 (b) 不做 | 需人類帳戶 UI；代理不得代行 |
| O-5 | **是否發 `R6-NEXT-PREVIEW`（新 Tag）以分發 `main` 後續 11 commits？** | (a) 發行 (b) 不發 | 本輪預設不觸發；若發行須新 Tag / Wheel / ZIP / SHA256SUMS，**不得**改動 `.4` |

## 3. 殘留 TT（Ticket / Task）— 全部為「觸發式」或「已界定不阻斷」

| TT ID | 範圍 | Done When | 觸發條件 | 阻斷本輪結案？ |
|---|---|---|---|---|
| `TT-R6-DOC-ONEPASS` | 兩份文件最小勘誤 + 同 ID UPDATE 路徑 | 候選分支合併、doc-link/identity 檢查綠 | 已由本輪完成候選 | **否**（已交付候選） |
| `TT-R6-PRIVATE-UPDATE-SMOKE` | 人類帳戶執行 1 次 UPDATE + 1 POS + 1 缺來源 NACK | 保存 UI／時間／host／ZIP hash | 僅在承諾「更新」能力時 | 否 |
| `TT-R6-NEXT-PREVIEW-IF-NEEDED` | 把 `main` after PR #13/#16 的修正對外提供 | 新 Tag + Wheel/ZIP/Fallback + SHA256SUMS + served readback | 首次要求分發新主線能力時 | 否 |
| `TT-R6-HOST-SCOPED-UAT` | 每個宣稱宿主最小 POS/NEG/nontrigger/security | 逐宿主 raw 證據 | 下階段品質工作 | 否 |
| `TT-R6-HGK-CNV` | PR #14/#15、CNV 規範與 Model SoD | 由外部 Project Owner 沿自身 route | 他案 | 否 |
| `TT-R6-OD-A` | `KP11-R04 / KP12-R04 / KP16-R04` 的 `MUST NOT` 正規化表歧義（`ORACLE_DISAGREEMENT`） | 上游 Oracle 裁決並更新正規化表 | 下次需引用該表時 | 否 |
| `TT-R6-OD-B` | `preview.4` Release **served** `PIPD_WEB_FALLBACK.md` 的表頭仍寫 `release_id: v0.1.1-preview.3`（本輪新增觀察 `F-R6-08`） | 於新發行重建該文件；**不得**就地替換 `.4` 資產 | 下次發行 | 否 |

## 4. Rollback pointer

- 候選分支：刪除 `fix/s4r6-closeout-doc-identity-and-update-route-20261016`（Owner 授權後）。
- 本地 worktree：`git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt reset --hard d3bd5456afbff21a8c8837994a49f57be3e1b97e`。
- 已發布資產：**任何情況下不得**就地替換 `v0.1.1-preview.4` 的 Tag 或 7 個 asset；如需撤回只透過官方 Release 管理與新版指向。

## 5. 終止聲明

- `TEMP_CLOSED` **不等於** `FULL PASS`。本輪不主張 `S4_FULL_PASS`、`HOST_QUALIFIED`、`PRODUCTION`、`PUBLIC_DIRECTORY` 任何一項。
- 本輪製造者（maker）為 `opencode-go/deepseek-v4.1-flash`（Codex CLI EXECUTE lane）；獨立查核者為
  `openai-codex/gpt-6.1-sol`（Codex CLI VERIFY lane）— **maker ≠ checker，且具模型軸獨立性**。
- 所有計數（CK 項數、測試計數、asset 數）皆由磁碟／API 上的產物導出，非模板數字。
- NOT_RUN 一律記為 `NOT_RUN`，不記為 PASS 或 FAIL。
- Owner 真實簽核前，本文件僅為**工程建議與返包**，非治理裁決。
