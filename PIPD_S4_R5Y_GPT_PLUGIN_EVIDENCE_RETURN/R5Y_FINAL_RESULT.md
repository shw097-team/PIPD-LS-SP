# PIPD-LS-SP GPT 外掛程式上架方案 — R5Y 執行結果（終局報告）

**輪次** `R5Y-20261014-gpt-plugin-publication` ｜ **契約** `PIPD-S4-PUBLIC-PLUGIN-EXECUTION-CONTRACT-R1`
**唯一控制平面** HG-KSEOS（准入 project `PIPD-LS-SP-20261008`；1 requirement FROZEN ＋ 18 TaskSpec ＋ 18 WorkOrder）
**受治理 Runtime／Orchestration Plane** 本輪 Hermes（PLAN lane）｜ **桌面／螢幕控制層** FDA（cua-driver）
**證據包** `PIPD/PIPD_S4_R5Y_GPT_PLUGIN_EVIDENCE_RETURN/`（69 檔）｜ **輪目錄** `PIPD/.hgk/rounds/R5Y-20261014-gpt-plugin-publication/`

## 一、五軸判定（嚴禁跨階躍升）

| 軸 | 判定 | 依據 |
|---|---|---|
| A 建置候選（BUILD_CANDIDATE） | **PASS**（含獨立複核） | ZIP 2× byte-identical `2f9ae010…d199`（68,355 B／56 成員／8 skills／單一根）；本機 589 passed／20 skipped；hosted `ci` 與 `public-plugin-verify` 皆 success |
| B 私人外掛（PRIVATE） | **PASS（自有帳號）** | 外掛建立→安裝→對話 `@pipd-route-intake` 調用成功，技能 body 生效且 fail-closed 規則被執行 |
| C 公開目錄提交（PORTAL_SUBMIT_READY） | **HOLD（外部硬阻斷）** | Portal 實機回 `Complete identity verification`：「You need a verified developer identity before you can create or upload a plugin.」 |
| D 公開發佈（PUBLIC_PUBLISHED） | **NOT_RUN** | 需 Owner 發佈決議＋外部審查；本輪未執行 |
| E 公開消費者驗證（PUBLIC_CONSUMER_VERIFIED） | **NOT_RUN** | 需不特定第三方在目錄搜尋→安裝→調用 |

## 二、已完成（附證據）

1. **TS-00 凍結**：`main 2245914…`／Stage A `759b9f0…`／Stage B `c52c219…`／PR #3/#4/#5（全 open draft）／tags preview.1–3；本輪分支 `feat/s4r5y-plugin-publication-20261014` @ `062d84ae…`（PR #6 draft）。
2. **TS-04 manifest 官方 listing 適配**：僅動 `packaging/public-plugin/plugin.json`（1 檔 M）；新增 `com.openai.interface` 的 `category=Developer Tools`／`capabilities` 三項／`defaultPrompt` 三則／`displayName`／`shortDescription`／`longDescription`／`developerName` ＋ `com.openai.onboardingSkill`；**8 個 SKILL.md body 與 Stage B byte-identical**。
3. **TS-07 決定性打包**：build-a／build-b 兩次相等；結構負例 PORTAL-01..03c（.codex-plugin／mcp.json／hooks／.app.json 植入）全部被結構審計抓出。
4. **TS-10 託管 CI 真實結果**：head `062d84ae…` 上 `ci` 與 `public-plugin-verify` 皆 success（含 dispatch 與 PR 事件），無 failed／skipped 步驟。
5. **TS-11 安全與技能行為**：`skill_pack_check --all` 8 packs × 7 cases（POS/NEG/EDGE/SEC）全過、`routes_verified`；secret scan 50 檔零發現；typed refusal 負例。
6. **TS-12 獨立複核（maker≠checker）**：arm B `openai-codex/gpt-6.1-sol`（CODEX CLI）。**attempt 1** 具名檢查 A–H 全 PASS，但整體 **FAIL**——`verify_only_guard` 偵測稽核窗口內受稽核檔被寫動（`01_subject/SOURCE_SCOPE_MATRIX_BY_SKILL.json`），屬程序瑕疵；開 `R5Y-TT-001` → 凍結後 **bounded recheck（attempt 2）PASS**：A–I 全 PASS、`verify_only_guard` status PASS、`audited_artifacts_modified=false`、inventory sha256 前後一致。
7. **FDA 桌面控制（真實 UI 動作）**：全部走 cua-driver；background 優先，Chromium 丟棄 posted keystroke 時取得結構化 `background_unavailable` 才升 foreground（僅一次，Return 鍵）；原生檔案對話框以 UIA `set_value`＋`Invoke` 純消息完成（零滑鼠、零焦點）。

## 三、私人外掛路徑（本輪新增可交付）

- 路徑：`chatgpt.com/plugins` → 側欄「外掛程式」→「新增」→「上傳外掛程式封存檔」→ 原生對話框選 `pipd-ls-sp-public-skills.zip` → 「新增外掛程式」→ 「安裝外掛程式」→ 「設定」。
- 產物：`https://chatgpt.com/plugins/Plugin_5ba168f715b8819190ccbe33a4a926b0`
- 已安裝清單確認：`chatgpt.com/settings/plugins-settings` → 「已安裝的外掛程式」列出 `PIPD-LS-SP Public Skills — Source-bound PIPD lifecycle skills`（副標即 manifest `shortDescription`）。
- 詳情頁渲染確認：類別 `Developer Tools`、功能三項、開發者、版本 `0.1.1`、**技能 8** 全列、`longDescription` 全文 ⇒ 官方 listing 欄位確實在 ChatGPT 端生效。
- 功能驗證：對話 `https://chatgpt.com/c/6acef5b8-56d0-83e8-80bb-38d3f78606d7` 中 `@pipd-route-intake` 被讀取，助理依 SKILL.md 拒絕空白目標與零來源定位器 ⇒ 技能本體生效且 fail-closed 行為正確。

## 四、未完成（誠實列出）

| 項 | 狀態 | 阻斷 |
|---|---|---|
| TS-13 開發者身分驗證 | NOT_RUN | Portal 硬性前置；屬人類 KYC，agent 不得代行（未點 Continue、未輸入任何身分資料） |
| TS-14 公開目錄 Draft／上傳 | NOT_RUN | 被 TS-13 阻斷（私人路徑已另完成） |
| TS-15 提交審查 | NOT_RUN | 同上＋Publisher 政策具結 |
| TS-16 審查通過（OpenAI） | NOT_RUN | 外部機關 |
| TS-17 公開發佈＋不特定第三方安裝調用 | NOT_RUN | Owner 發佈決議＋第三方 |
| TS-05／TS-06 殘項 | 部分 | 本輪專屬 owner 再簽名；品牌圖為 generator 產物，需 owner 供圖或明示核准 |

## 五、如何獨立驗證

1. `git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git refs/heads/feat/s4r5y-plugin-publication-20261014` → `062d84ae3e951d02b2ba6bb732359b18799d2864`
2. `sha256sum 04_package/build/build-*/pipd-ls-sp-public-skills.zip` → `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`
3. 匿名 `GET /repos/shw097-team/PIPD-LS-SP/actions/runs?head_sha=062d84ae…` → `ci`、`public-plugin-verify` 皆 success
4. 私人外掛：登入同一帳號開 `chatgpt.com/settings/plugins-settings` 應見已安裝項；`09_ui_fda/` 有逐動 log、樹狀 dump 與截圖

## 六、claim ceiling

本輪只主張 **A 候選級＋B 私人路徑（自有帳號）**。**不主張**：公開目錄已提交、已審查通過、已發佈、任何第三方已可搜尋安裝。未取得證據者一律 `NOT_RUN`／`EVIDENCE_GAP`，無任何 PASS 由推論填補。
