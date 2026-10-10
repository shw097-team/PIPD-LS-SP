# R5R｜CE-1／CE-2 修補 FAR 快速研究（CE-1/CE-2 Repair Quickstudy）

- 輪次：`R5R-20261010-s4-ce-repair-and-codex-verify`
- 研究編號：`FAR-PIPD-R5R-CE-REPAIR-001`
- 受理：`REQ-PIPD-R5R-FAR-001` / `WO-R5R-FAR-001`
- 上游：R5Q 第二輪獨立驗收（指定 lane）回報 `COUNTEREXAMPLE_FOUND`，CE-1／CE-2 已由 maker 對發布 wheel 位元複現
- 本文角色：**研究與決策**；實際修補由 EXECUTE lane（CODEX CLI）執行，獨立驗證由 VERIFY lane（CODEX CLI，`gpt-6.1-sol`）執行

---

## 1｜研究問題

在不改動已發布 `v0.1.0-preview.1`（不回寫 tag、不重建既有 wheel）的前提下，選出**最低阻力**且對得起產品語意的工程修補，使：

- **CE-1**：安裝後的 `validate` 能像同環境的 `doctor` 一樣解析 wheel 自帶的 schemas；
- **CE-2**：四個 compiler **未經修改的 stdout** 組成的 bundle 能被 `validate` 接受。

## 2｜根因（實讀原始碼，非推測）

### CE-1

| 位置 | 事實 |
|---|---|
| `src/pipd_ls_sp/cli.py:39` | 全域 `--root` 的預設值是 `Path.cwd()` |
| `src/pipd_ls_sp/cli.py:166` | `validate` 呼叫 `validate.validate_bundle(bundle, root / "schemas")` —— schema 目錄**只**由 `--root` 決定 |
| `src/pipd_ls_sp/cli.py:171` | `doctor` 走 `workspace.doctor(root)` |
| `src/pipd_ls_sp/registry.py:82-115` | `doctor` 用的解析鏈是 `OVERRIDE` → `INSTALLED` → `SOURCE`，取**第一個含 `registry.json`** 者 |

→ 兩個指令對「schemas 在哪」有**兩套不同的規則**。`doctor` 問 registry，`validate` 直接看 cwd。使用者在別的目錄執行時，`doctor` 綠燈、`validate` 找不到檔案。

### CE-2

| 位置 | 事實 |
|---|---|
| `src/pipd_ls_sp/pipeline.py:164` | `pi["_profile_meta"] = profile_meta  # non-record sidecar, stripped before validation` |
| `src/pipd_ls_sp/validate.py:48` | `_body_hash` 確實**有**把 `_profile_meta` 排除（連同 `subject_id`/`version`/`content_hash`/`schema_version`/`trace`） |
| `src/pipd_ls_sp/validate.py:27-35` | `validate_record` 對**原樣**的 record 做 JSON Schema 檢查，**沒有**套用那一份排除清單 |
| `schemas/PI-PKG.schema.json` | `additionalProperties: false`，`properties` 只有 7 個宣告欄位 |
| `src/pipd_ls_sp/pipeline.py:26-29` | 專案自身慣例的明文：欄位須留在已宣告欄位**內**，「never as a new top-level key and never by editing the schema」 |

→ `validate_bundle` **違反了它自己程式碼裡宣稱的行為**（"stripped before validation"）。這不是 schema 的錯，也不是 compile-pi 輸出「錯」，是驗證端漏套用自家已宣告的 sidecar 清單。

## 3｜候選方案與判詞

### CE-1

| 代號 | 方案 | 判詞 |
|---|---|---|
| **A1** | `validate` 改用 registry 的解析鏈，並把 `--root/schemas`（當其含 `registry.json` 時）**插在最前面** | **採用**。workspace 模式（工作區自帶 schemas 優先）保持不變；安裝模式得到與 `doctor` 一致的行為；零 schema 變更 |
| A2 | 只補文件，要求使用者傳 `--root` | 只消除驚訝，不消除缺陷；R5Q 已如此揭露過，本輪目的正是修掉它 |
| A3 | 把 `--root` 預設改成套件目錄 | 會**破壞** workspace 模式：工作區自己的 schemas 必須優先 |
| A4 | 讓 CLI 自帶 schemas 而不依賴路徑 | 不改變「兩套規則」的事實 |

### CE-2

| 代號 | 方案 | 判詞 |
|---|---|---|
| **B1** | `validate` 在 schema 檢查前套用**同一份**已宣告的非記錄 sidecar 清單 | **採用**。這正是 `pipeline.py:164` 註解已宣告的行為；不動 schema、不動產物內容、不動 wheel 內的 schema 集合 |
| B2 | 讓 `compile-pi` 不再輸出 `_profile_meta` | 會**弄壞** `tools/run_s1_slice.py:71-72`（讀 `pi["_profile_meta"]["profile"]`），並把 profile 升級紀錄從產物中移除 |
| B3 | 在 `PI-PKG.schema.json` 加上 `_profile_meta` | 改動 S0 canonical schema＝契約變更，且連帶改動 wheel 內 schema 集合；同時違反專案自身慣例（見 `pipeline.py:26-29`） |
| B4 | 讓 `validate` 容忍所有未知欄位 | 等於對全部 19 個家族放寬契約——代價遠大於缺陷本身 |

## 4｜裁決

**採 A1 + B1**，並加一項**消除同類**的結構性要求：

> 把「非記錄 sidecar 清單」抽成**單一真實來源**（一個常數／一個函式），由 `validate._body_hash`、`validate.validate_record` 與 `pipeline._rec` **共同引用**。CE-2 之所以發生，正是因為同一份清單在兩個地方各寫一次、其中一處漏了。

理由：兩者都是**驗證端的行為與自家已宣告語意不一致**，不是演算法錯誤。最小修補＝讓驗證端照它已經寫下的規則做。這也讓 R5Q 已公開揭露的限制 6／7 從「使用者必須知道的怪癖」變成「已修復」。

**代價與邊界：**
- 修補改變 `src/` → 出廠 wheel 位元會變 → **必須**以**後繼 release** 交付，不得回寫 `v0.1.0-preview.1`（owner grant：published tags are never rewritten, a superseding release is issued instead）。
- 本輪**不**發布新 tag；發布與否另由 owner 決定（見 §6）。
- 已發布 wheel `c450dbef…` 的行為**不會**因此改變；本輪交付的是「下一顆」的正確性與其獨立驗證。

## 5｜回歸要求（不接受「修好了」這種說法）

每個修補都要有**先失敗、後通過**的證據：

1. 對**修補前**的樹執行新測試 → 必須失敗（CE-1：cwd 無 `schemas/` 時 exit 2；CE-2：原始 stdout bundle 被拒）。
2. 對**修補後**的樹執行同一測試 → 必須通過。
3. 既有 311 測試維持全綠。

另需一個**端到端**檢查：以安裝後的 wheel、在**非 repo 目錄**、用**未經手改**的四段 compiler 輸出跑 `validate`，須 `verdict=PASS`。

## 6｜殘餘（本輪不關閉）

- 已發布 `v0.1.0-preview.1` 的 wheel 仍帶舊行為；其公開頁面文字已於 R5Q 揭露，本輪修補後需更新為「已在下一版修復」。
- `DEL-018 RELEASE_MANIFEST@1` 仍 `FAIL/EVIDENCE_GAP`。
- 是否發布 `v0.1.0-preview.2`（或下一個實質版本）**屬 owner 的發布決定**，不在本研究授權內。
- 本輪不變更 S0 schema 契約、不變更 19 家族集合、不變更任何 claim ceiling。

## Sources

- `src/pipd_ls_sp/cli.py`、`validate.py`、`pipeline.py`、`registry.py`、`workspace.py`（本次實讀）
- `schemas/PI-PKG.schema.json`、`schemas/registry.json`
- `tools/run_s1_slice.py`
- R5Q：`evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json`、`evidence/ce_repro/`、`evidence/R5Q_FINAL_REPORT.md` §6.3
- Owner grant：`OWNER_LICENSE_DECISION.yaml`（`exclusions`: superseding release, never a rewrite）
