# R6｜FAR 偏差研究與最佳工程裁決（PLAN 車道交付）

- Round：`R6-20261014-far-remediation-and-repair`
- 受研標的：(a) 本 session 對四份上位文件的執行結果；(b) 前次提出之五項最小補強／待裁決事項。
- 上位依據：`PIPD-LS-SP S4 R4｜Hermes HG-KSEOS Fabric 合規指揮薄 PROMPT_2026-10-13`（`CK-01..15`，5×`F0xx`）、`PIPD-LS-SP｜S4 R4 驗收報告_20261013`（**上位裁決**，11×`UPG-*`，5×`F0xx`）、`PIPD-LS-SP_GPT外掛程式上架方案`（`UPG-P01..P04` 全譜）、`PIPD-LS-SP S4｜三合一小型升級藍圖 R2`（`UPG-P01–P04`、`A01–A42`、`F01–F14`、`TR-01–40`）；旁證：`PIPD-S4-EXT-ACCEPT-R3-20261013`（外部獨立複驗，判 `FAIL_CHALLENGE`／`NO_MERGE`／`NO_PUBLIC_RELEASE`）。
- 落地對齊標的：`…/PIPD/PIPD-LS-SP_PIPD-PKG/PIPD-LS-SP_PIPD-PKG-00~PKG-10`（11 檔、逐檔 sha256 已錄於 `01_subject/PKG_INDEX_R6.json`）。
- 方法：Source-Bound／Fail-Closed；偏差分類 D1–D10；每項以「摩擦／可行性／工程必要性／是否過度工程」四軸評分後裁決。

## 0. 評分尺規（避免結論漂移）

- 摩擦：低＝不需新治理核准、不改 gate、不動 main；中＝需 Owner 一次決定；高＝需新機制或跨組件改動。
- 可行性：高＝本輪即可完成且有可重跑證據；中＝需人工／外部；低＝目前不可達。
- 工程必要性：高＝缺它則外部驗收無法開始或結論不可信；中＝顯著提升可驗性；低＝錦上添花。
- 過度工程檢查：凡一次要求「全量 42 原子逐條閉合」「新增第二編譯系統」「為方便放寬 gate」者，一律標為過度並降級為後續 ChangeSet。

## 1. 偏差清單（FAR）

| ID | 上位要求（出處） | 現況（證據） | 偏差 | 影響 | 最小修補 | 摩擦 | 可行 | 必要 | 過度 | 裁決 |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 上位文件為驗收依據；證據須可供外部讀取（PKG-06 TraceGraph/TQAEP、PKG-00 Authority/Source Freeze） | 四份上位文件＋R3 報告僅存在本機知識庫；repo 樹內無 `acceptance_reports/` 或等價路徑（tree 搜尋 0 命中） | 依據不可得 | 外部驗收官無法核對「受驗條文」，只能驗產物 | 把五份文件（含 R3 報告）以其 sha256 清單發佈到**證據分支**的 `acceptance/`；不提 PR、不動 main、不改 gate | 低 | 高 | **高** | 否 | **執行** |
| D2 | 證據須完整可核（PKG-06；R4 報告 §0 原始證據要求） | 遠端 `PIPD_S4_R4_EVIDENCE_RETURN` 僅 3 檔（`EVIDENCE_RETURN_MANIFEST.json`／`tasks.tsv`／`R5X_FINAL_RESULT.md`） | 證據包過薄 | 外部人無法重建 R4 輪次的命令／退出碼／收據 | 補齊 R4 輪次證據（任務表、R5X 結果、CI 摘要、車道收據索引）至證據分支 | 低 | 高 | **高** | 否 | **執行** |
| D3 | 檢查者須有可重跑契約與期望值（PKG-06 Checker／PKG-08 readback） | 無 `VERIFICATION_PROTOCOL`；命令與期望 digest 散落在多份 round 文件 | 驗收程序不透明 | 每次外部驗收都要重新摸索，易得「不可重現」結論 | 新增 `VERIFICATION_PROTOCOL.md`：確切命令、期望 bytes／sha256、判定準則、claim ceiling、不可由 repo 完成項清單 | 低 | 高 | **高** | 否 | **執行** |
| D4 | 交付須有凍結狀態（R4 報告 §10；PKG-08 Release/Human Authority） | `main` 仍 `224591431a16`；PR #8 仍 draft；無新 tag／release | 未交付 | 外部驗收只能在分支上進行，無凍結交付物 | merge／tag／release 為 Owner 決策，不由 agent 自簽 | 中 | 中 | 高 | 否 | **上呈 Owner** |
| D5 | 受治理寫入集不得為便利而放寬（PKG-07 寫入集、AGENTS.md 治理） | `public-plugin-verify` 正面允許清單不含 `docs/acceptance/`；先前已因同因紅燈 | 治理張力 | 若把上位文件塞進 PR 會迫使放寬 gate | **不放寬**；上位文件改由證據分支承載（與 D1 同一手段） | 低 | 高 | 高 | 否（放寬才是過度） | **執行（走證據分支）** |
| D6 | 車道模型須與宣告一致（本次任務指令；PKG-10 整合/Promotion） | PLAN 實跑 `deepseek-v4.1-flash`（宣告為 GLM-5.3-Flash）；EXECUTE 曾 `ERR_REQUIRED_ARM_NOT_SERVED`；VERIFY 於 arm3–arm5 已由 `--force-rank 3` 收據證明為指定臂 | 宣告偏離（PLAN） | 「模型級 SoD」宣稱不成立 | 本輪 PLAN 繼續由本層執行並**如實標示**；VERIFY 一律強制指定臂；把「引擎分離＋收據背書量測」列為可接受的替代上限，或由 Owner 決定改宣告／改池序 | 中 | 高 | 中 | 否 | **執行＋上呈** |
| D7 | 三合一 R2 之 UPG-P01–P04 與 42 原子、F01–F14、TR-01–40（藍圖 §12、Appendix C–E） | UPG-P01/02/03 產物齊；UPG-P04 候選產物有；**無**逐條對照表；R3 外部判 `FAIL_CHALLENGE` | 追溯缺口 | 無法說明「哪些已做、哪些是 Owner／未跑」 | 建立 `UPG_TRACEABILITY_R6.tsv`：逐 UPG／TR／A／F 標記 `DONE／PARTIAL／OWNER／NOT_RUN` 並附證據指標；**不**在本輪施工 42 原子 | 低 | 高 | **高** | 是（若一次做完 42 原子即過度） | **執行（只出對照表）** |
| D8 | UPG-P01 品牌資產（藍圖 Appendix C：`OWNER_BRAND_REQUIRED`） | `packaging/public-plugin/assets/` 僅 `.gitignore`；現用 builder 生成式圖示 | 品牌未定 | 公開上架無法通過 listing 圖像規範 | 由 Owner 供圖；agent 不生成品牌圖（避免冒充） | 中 | 中 | 中 | 否 | **上呈 Owner** |
| D9 | 控制平面須可回寫（PKG-10 HG-KSEOS 整合） | spine `database is locked` 5 次（含 60–180 s busy_timeout）；已落 `SPINE_WRITEBACK_PENDING.md` | 回寫受阻 | spine 帳面未反映 R5Z 結案與本輪 admission | 本輪 admission／結果以**檔案收據**為權威並冪等重試 spine；請 Owner 或 spine owner 清 stale lock | 中 | 中 | 中 | 否 | **執行（檔案權威＋重試）** |
| D10 | 車道臂綁定之池序應使指定臂可被服務（PKG-10；本輪指令） | 池 `lane-route-slots.candidate.json` 對兩車道皆把 `opencode-go/deepseek-v4.1-flash` 排 rank 1 | 池序缺陷 | 未強制 rank 的派工必然服務錯臂，收據恆紅 | 短期：派工一律 `--force-rank`（本輪已用）；長期：改池序＝Owner 治理決定 | 低 | 高 | 高 | 否 | **上呈 Owner（短期已自動緩解）** |

## 2. 最佳工程裁決（Adjudication）

1. **可驗性優先於完備性**：本輪把「外部人可獨立開始驗收」所需的三件事一次做足（D1 依據、D2 證據、D3 程序），全部落在**證據分支**，不動 main、不提 PR、不放寬任何 gate。此為低摩擦且不可逆地提升外部可驗性。
2. **治理不為便利讓路**（D5）：拒絕把上位文件塞進受 gate 管轄的 PR 路徑；允許清單不變更。若 Owner 日後要求上位文件進 main，應以「治理變更」單獨核准，而非順手放寬。
3. **不過度工程**（D7）：三合一 R2 的 42 原子不在本輪逐條施工；本輪只交付**可稽核的對照表**，把「已做／半做／Owner／未跑」說清楚，讓後續 ChangeSet 有工作底稿。
4. **模型級 SoD 以收據為準**（D6/D10）：本輪 VERIFY 仍強制 `--force-rank 3`（指定臂 `opencode-go/glm-5.3-flash`），EXECUTE 強制 `--force-rank 1`（指定臂 `opencode-go/deepseek-v4.1-flash`）；PLAN 模型偏離如實標示，不宣稱模型級隔離。
5. **不代行**（D4/D8）：merge／tag／release／publish、OpenAI 開發者身分、品牌圖、池序變更，一律上呈 Owner，不假冒、不自行點擊。

## 3. 修補／補強執行方案（Tier 化）

- **Tier 1（本輪直接執行，低摩擦、高可行、高必要）**
  1. `D1`：證據分支新增 `PIPD_S4_R6_FAR_AND_ALIGNMENT_RETURN/acceptance/`，內含五份上位文件（`R4_PROMPT`、`R4_REPORT`、`GPT_PLUGIN_PLAN`、`TRIPLE_BLUEPRINT_R2`、`R3_EXT_ACCEPT`）＋`GOVERNING_DOCS_MANIFEST.json`（逐檔 sha256、字元數、來源路徑、抓取時刻）。**唯一修訂**：把憑證定位字串以 `<REDACTED_CREDENTIAL_LOCATOR>` 取代，並在 manifest 中逐檔記錄「redacted lines」計數與理由。
  2. `D2`：`PIPD_S4_R6_FAR_AND_ALIGNMENT_RETURN/R4_EVIDENCE_EXPANDED/`：R4 輪次任務表、R5X 最終結果、CI 摘要、車道收據索引（EXECUTE／VERIFY 收據清單與 sha256）。
  3. `D3`：`VERIFICATION_PROTOCOL.md`：給外部驗收官的最小可重跑流程（見 §4）。
  4. `D7`：`UPG_TRACEABILITY_R6.tsv`：UPG-P01–P04／TR-01–40／A01–A42／F01–F14 的狀態標記。
  5. `PKG_ALIGNMENT_R6.md`：把本輪裁決逐項掛到 PKG-00..10 的領域與條款錨點。
  6. 本報告（`FAR_REPORT_R6.md`）＋`MANIFEST.sha256.json`。
  7. 全數推送至證據分支並遠端讀回驗證。
- **Tier 2（需 Owner；本輪只上呈清單）**：D4 merge／tag／release／publish；D8 品牌圖；D10 池序；D6 PLAN 模型宣告；上位文件是否進 main（治理變更）。
- **Tier 3（背景條件改善後重試）**：D9 spine 回寫（冪等重試）。

## 4. VERIFICATION_PROTOCOL 最小內容（Tier 1 產物規格）

1. 取得證據：`git clone` 後 `git checkout r5z-evidence-return-20261014`（或 API 讀取），驗 `MANIFEST.sha256.json`。
2. 重跑建置：`python tools/freeze_public_plugin_source.py --repo-root . --out ledger.json` → `python tools/build_public_plugin.py --ledger ledger.json --source-commit 062d84ae3e951d02b2ba6bb732359b18799d2864 --packaging-root packaging/public-plugin --out-dir out --generate-icons`；期望 `out/pipd-ls-sp-public-skills.zip` ＝ **68,355 bytes / sha256 `2f9ae010…d199`**。
3. 驗 ZIP 結構：56 entries、8 `SKILL.md`、根 `plugin.json`、七個 camelCase 欄位。
4. 驗 PKG 對齊：以 `PKG_INDEX_R6.json` 的 11 筆 sha256 重算比對。
5. 驗車道收據：`LANE_RECEIPT_VERIFY_arm5.json` 之 `required_arm == served_arm == opencode-go/glm-5.3-flash`、`ok=true`、`subject_mutation.verdict=CLEAN`。
6. 判定準則與上限：`BUILD_PASS != PORTAL_APPROVED != PUBLISHED != HOST_QUALIFIED != S4_PASS`；不可由 repo 完成者＝宿主 UAT、Portal 上架、公開消費者驗證、私人外掛安裝（需帳號）。

## 5. 宣稱上限

本輪為 **candidate 級修補＋可驗性補強**；未 merge／tag／release／publish；未經 OpenAI 審查、未經第三方驗收；三合一 R2 僅交付對照表，不代表其 42 原子已閉合。
