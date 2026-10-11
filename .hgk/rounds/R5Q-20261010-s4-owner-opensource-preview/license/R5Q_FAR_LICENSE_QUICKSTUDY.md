# R5Q｜P2 授權落地 FAR 快速研究（License / SPDX / NOTICE / SBOM）

**研究編號：** FAR-PIPD-R5Q-LICENSE-001
**輪次：** `.hgk/rounds/R5Q-20261010-s4-owner-opensource-preview/`
**日期：** 2026-10-10 / Asia-Taipei
**授權依據：** Owner 指示（本輪追加決策）：對「P2：LICENSE、SPDX、NOTICE、SBOM 等授權落地」進行快速 FAR 研究，制定最佳開源工程授權決策與方案並直接執行，無須再索取授權。
**角色分離：** 本研究由 PLAN 角色（Hermes 內執行）產出裁決；落地由 bounded writer 執行；獨立複驗由非 Maker checker 於 P6 進行。Maker 不自簽 Independent PASS。

---

## 1｜研究問題（ResearchRequest）

在下列**已凍結的權利事實**下，為 PIPD-LS-SP 的 S4 Open Source Preview 選定一組**可合法授予、工程上最優、且可被外部複驗**的授權組合，並產出可直接落地的檔案級變更清單：

1. 應選用哪個 SPDX 識別碼作為**整個倉庫的對外授權**？
2. 倉庫內「corpus-derived material」與「agent-authored engineering output」應如何分別處置？
3. `NOTICE`、`SBOM.cdx.json`、`pyproject.toml`、`PROVENANCE.md` 應如何對齊？
4. 哪些風險必須對外揭露、哪些必須設為 Preview 的 stop-ship？

## 2｜已凍結的權利事實（SourceDisposition）

| 事實 | 來源（locator） | 位階 |
|---|---|---|
| 目前 `LICENSE` 為 no-grant；SPDX `LicenseRef-PIPD-Proprietary`；明示「NO LICENCE IS GRANTED」 | `LICENSE` @ `2efc84e` | CURRENT_SOURCE |
| `OWNER_LICENSE_DECISION.yaml` 的 `decision` 目前為非授予值；允許值 `UNSET / LicenseRef-PIPD-Proprietary / MIT / Apache-2.0`；已定義 E1–E4 落地編輯 | `OWNER_LICENSE_DECISION.yaml` @ `2efc84e` | CURRENT_SOURCE |
| **「No third-party source was copied verbatim.」** 三支 donor Skill plugin 僅作 SOURCE reference 盤點，未貼入本樹 | `PROVENANCE.md` @ `2efc84e` | CURRENT_SOURCE |
| 唯一執行期依賴 `jsonschema` 為 **MIT** | `pyproject.toml`；PyPI jsonschema 4.26.0；python-jsonschema 倉庫授權欄 | WEB / PACKAGE |
| 現行 SBOM 把 `jsonschema` 的授權也寫成 `LicenseRef-PIPD-Proprietary`，並無 transitive closure | `SBOM.cdx.json` @ `2efc84e` | CURRENT_SOURCE（**缺陷**） |
| 無 `NOTICE` 檔案 | repo tree @ `2efc84e` | CURRENT_SOURCE |
| 前版外部驗收曾把「未授權」誤判為工程 FAIL，已由 CORRECTED 版撤回 | `PIPD_LS_SP_R5P_S4_External_Challenge_CORRECTED...md` §0.1 | NORMATIVE |
| 技術建議為 `GO_WITH_DISCLOSED_LIMITATIONS`；完整獨立挑戰仍 `PARTIAL_CHALLENGE` | 同上 §0 / §3 | NORMATIVE |

**關鍵判讀：** 本輪不需要處理「他人作品可否轉授權」的舉證問題——倉庫自證未逐字複製第三方來源。剩下的唯一權利問題是**上游 corpus 的衍生敘述**，而該 corpus 是 Owner 自身治理資產；Owner 對其衍生表達得授予授權，僅需在 NOTICE 中如實說明來源分層與 donor 僅為參考。

## 3｜候選方案與評分（Alternatives）

評分準則（1–5，越高越好）：
`A` 可合法授予性 / `B` 專利明確性 / `C` 企業採用摩擦 / `D` 相容性（消費 MIT 依賴、可被 GPLv3 專案採用） / `E` 來源與歸屬揭露機制 / `F` 名稱與商標保護 / `G` 早期 Preview 的簡潔性

| 候選 | A | B | C | D | E | F | G | 合計 | 判讀 |
|---|---|---|---|---|---|---|---|---|---|
| `MIT` | 5 | 2 | 4 | 3 | 2 | 2 | 5 | 23 | 最簡，但**無明示專利授予**、無 NOTICE 機制可承載本倉庫既有的來源分層揭露 |
| **`Apache-2.0`** | 5 | 5 | 5 | 4 | 5 | 5 | 4 | **33** | 明示專利授予（§3）＋NOTICE 機制（§4d）＋商標不授予（§6）；MIT/BSD 依賴可相容消費 |
| `BSD-3-Clause` | 5 | 2 | 4 | 4 | 2 | 3 | 5 | 25 | 同 MIT，加專有名稱條款；仍無專利授予 |
| `MPL-2.0` | 4 | 4 | 3 | 2 | 4 | 3 | 2 | 22 | 檔案級 copyleft，對「要被人嵌進宿主 runtime 的 schema/契約包」造成採用摩擦 |
| `AGPL-3.0` | 4 | 4 | 1 | 1 | 4 | 3 | 1 | 18 | 與 Preview 目標（擴大採用、取得真實使用者回饋）直接衝突 |
| `Apache-2.0 OR MIT` 雙授權 | 4 | 4 | 4 | 3 | 3 | 4 | 2 | 24 | 表面彈性，實際讓下游必須自行判斷，且 NOTICE 義務在 Apache 分支仍存在；對早期 Preview 增加無收益複雜度 |

**外部依據（WEB SUPPORT，不凌駕 Owner 文件）：**
- Apache-2.0 §3 明示專利授予、§4(d) NOTICE 歸屬傳遞、§6 商標與產品名稱不隨授權授予 — `https://www.apache.org/licenses/LICENSE-2.0`；ASF 官方申請說明 `https://apache.org/legal/apply-license.html`（指出 §4d 使歸屬聲明在衍生作品中以 NOTICE 形式存續）。
- MIT 未含明示專利授予，是多數開發者工具改採 Apache-2.0 的常見理由（SiFive 工程討論 `https://forums.sifive.com/t/the-apache-license-is-long-and-needlessly-complex/311`）。
- MIT 與 Apache-2.0 可相容並存；`Apache-2.0` 為目標授權時可消費 MIT 依賴（FOSSA 授權相容表 `https://fossa.com/resources/license-compliance-tools/license-compatibility-checker/apache-2-0-vs-mit/`）。
- `jsonschema` 4.26.0 為 MIT — `https://pypi.org/project/jsonschema/4.26.0/`。

**已知不利事實（必須一併記錄，不得只列優點）：** Apache-2.0 §4(b) 要求被修改檔案攜帶顯著變更通知，較 MIT 增加下游修改者的形式義務；此摩擦在評分 G 反映為 4 分，是本方案唯一的實質代價，接受理由為專利明確性與 NOTICE 揭露機制在**契約／schema 工具**這個產品類別中的權重更高。

## 4｜裁決（Decision）

> **採用 `Apache-2.0` 作為 PIPD-LS-SP 整倉庫對外授權（`decision: Apache-2.0`）。**
> 著作權人：Owner（`shw097-team/PIPD-LS-SP`）。生效時點：本次 release candidate commit 被提交之時；對公眾宣稱已取得開源授權，必須在該 commit 之後。

**權利範圍與分層（與既有 LICENSE 分層一致，不推翻）：**

| material 類 | 授權處置 | 揭露位置 |
|---|---|---|
| agent-authored engineering output（`src/`、`tests/`、`tools/`、`schemas/`、`fixtures/`、`skills/`、`docs/`、`dist/`） | **Apache-2.0 授予** | `LICENSE` §1、`pyproject.toml`、wheel METADATA、SBOM |
| 衍生敘述（源自 Owner 自身治理 corpus 的表達） | **Apache-2.0 授予**，並在 `NOTICE` 說明其來源與為受治理建置產出 | `NOTICE` |
| 三支 donor Skill plugin（SDLC_PRW_HLPE R2、SWOF_ECP v2.0.1、SWOF_TQAEP v2.0.1） | **不在本倉庫內容中**（僅盤點為 SOURCE reference）；不主張任何權利 | `NOTICE`、`PROVENANCE.md` |
| 第三方依賴 | 各自原授權（`jsonschema` = MIT）；記錄於 SBOM，不併入本專案授權 | `SBOM.cdx.json` |

**排除政策（Exclusion Policy）：** 若日後證實任一檔案含第三方權利，該檔案自重證起排除於本授權之外，並以新 release 版本替換；已發布的歷史 tag 與 release 不做破壞性重寫（依 R5Q prompt §7）。

**對外不得聲稱：** 不得聲稱已取得比 Apache-2.0 更寬的授權、不得聲稱 donor plugin 內容屬於本專案、不得聲稱 `G-RELEASE` 全綠或 Production Verified。

## 5｜落地方案（Landing Plan，即 E1–E7）

| ID | 檔案 | 變更 | 驗收方式 |
|---|---|---|---|
| `E1` | `LICENSE` | 以 **Apache License 2.0 全文** 取代 no-grant 本體；保留 corpus-derived / agent-authored 分層段落與 provenance 註記；SPDX 行改為 `Apache-2.0`；移除「NO LICENCE IS GRANTED」狀態語句並保留其歷史指向 | 全文 sha256 與官方 `LICENSE-2.0.txt` 逐字比對 |
| `E2` | `OWNER_LICENSE_DECISION.yaml` | `decision: Apache-2.0`、`decided_utc: 2026-10-10`、`decided_by: owner (instruction: 追加決策，Owner 的開源授權)`、`granted_subject: PIPD-LS-SP`、`rights_scope`、`exclusions`；**新增** `previous_decision` 區塊保留原非授予紀錄與其日期（不倒填、不改寫歷史） | YAML 解析成功；`decision` 值合法；舊值仍在檔內 |
| `E3` | `NOTICE`（**新增**） | 著作權行、專案名、Apache-2.0 引用、來源分層說明、donor plugin 僅為參考之聲明、第三方依賴清單（`jsonschema` MIT） | 檔案存在且在 wheel 與 source archive 內可讀 |
| `E4` | `pyproject.toml` | `license = "Apache-2.0"`、`license-files = ["LICENSE", "NOTICE"]`；維持 `jsonschema>=4.0` | wheel METADATA 含 `License: Apache-2.0` 與 `License-File: LICENSE, NOTICE` |
| `E5` | `SBOM.cdx.json` | metadata 與 component 授權改為 `Apache-2.0`；**修正** `jsonschema` component 誤標為本專案授權的缺陷 → `MIT`；更新 `pipd:licence:basis` | JSON 解析成功；`jsonschema` 授權為 MIT；無 `LicenseRef-PIPD-Proprietary` 殘留 |
| `E6` | `PROVENANCE.md` | 追加授權層（granted by owner、Apache-2.0、生效 commit 佔位） | 與 `NOTICE` 敘述一致 |
| `E7` | `README.md` / `ACCEPTANCE.md` | 首屏指向 Preview tag 而非 R3 `main`；加入授權段落與 Known Limitations 連結 | 首屏不出現「未授權」狀態語句；連結指向 release commit/tag |

**歷史保留（不得倒填）：** `.hgk/rounds/R2-*/**` 內既有的 UNSET 副本、`FAR-PIPD-LICENSE-001` 的 Gate1 收據、以及既有 R3/R4/R5/R5P attestation 一律 byte-identical 保留。

## 6｜殘餘風險與 TT 影響

| 風險 | 等級 | 處置 |
|---|---|---|
| corpus-derived 敘述的作者性主張日後被第三人爭執 | 低（自有 corpus，且未逐字複製第三方） | NOTICE 如實敘明來源；列入 Preview Known Limitations；不主張超出 Owner 可授權範圍 |
| SBOM 無 transitive closure（僅 declared dependency set） | 低 | 維持既有 `pipd:sbom_scope` 聲明；列入 Known Limitations，不偽稱完整 SBOM |
| Apache-2.0 §4(b) 修改檔通知義務造成下游摩擦 | 低 | 於 `NOTICE` 與 Preview Notes 明示 |
| 依賴版本漂移 | 低 | `pipd:licence:recheck_trigger` 記錄 TTL／重新檢查觸發（承 SPEC-026） |

**TT 對映：** `TT-PIPD-LICENSE-001`（source gap：未授權）→ 本輪由 Owner Grant 關閉 **僅就「未授權」這個 source gap 而言**；`TT-R5P-07`（Owner 授權為 HITL 前置）→ 由本輪具名決策記錄滿足。`DEL-019`（SBOM_PROVENANCE_BUNDLE）由 E5/E6 對齊敘述，但**不**因此宣告 release PASS。

## 7｜Claim ceiling

本研究與其落地屬 **candidate-level 工程處置**。對外可聲明的最上限是
`OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED` 且**僅在**實際發布並成功回讀之後；本研究本身不構成 `FULL_S0_S4_INDEPENDENT_PASS`、`G_RELEASE_FULL_PASS` 或 `PRODUCTION_VERIFIED`。

---

**產出者：** Hermes PLAN lane（`deepseek-v4.1-flash` @ `opencode-go`）
**狀態：** `LICENSE_DECISION_RESOLVED_APACHE_2_0`（Owner 委派 FAR 裁決）
