# R7｜FAR：待裁決事項 × REPO 完整更新／MERGE／衛生 × 結案移交（PLAN 車道交付）

- Round：`R7-20261014-merge-hygiene-closeout`；授權來源：用戶本輪直接授權「FAR 提出最佳工程裁決＋執行方案後直接執行，執行到本 session 可完整結案」。
- 上位依據：R4 指揮薄 PROMPT、R4 驗收報告（上位裁決）、三合一 R2 藍圖、GPT 外掛上架方案、PKG-00..10。
- 方法：Source-Bound／Fail-Closed；每項以「摩擦／可行性／工程必要性／是否過度工程」評分。

## 1. 全部待裁決事項 → 裁決

| # | 待裁決事項 | 事實 | 裁決 | 摩擦／可行／必要／過度 |
|---|---|---|---|---|
| O1 | merge／tag／release／publish | main=`22459143`、6 個 draft PR；用戶本輪直接授權「完整更新、MERGE」 | **merge 執行**（本輪）；**tag／release 留待版本決策**（建議 `v0.2.0-preview.1` 或 `v0.1.1-preview.4`，由 Owner 定）；**portal publish 維持 HOLD**（開發者身分＝HumanGate） | 低／高／高／否 |
| O2 | 五份上位文件是否續留公開證據分支 | 本輪前已發佈（僅憑證定位字串遮蔽）；用戶再次指示「推到 REPO 供外部驗收」 | **維持**，並在 main README 標示入口與撤回機制 | 低／高／高／否 |
| O3 | 車道池序（臂綁定） | 池 rank1 為 `deepseek-v4.1-flash`，指定臂在 rank3 | 本輪一律 `--force-rank`；池序變更留 Owner（附一行修補建議） | 低／高／高／否 |
| O4 | `R5Z-TT-001` PLAN 模型宣告偏離 | PLAN 實跑 `deepseek-v4.1-flash`，宣告為 `glm-5.3-flash` | **以「引擎分離＋收據背書量測」結案並文件化**（宣稱上限明示於 README 與 closeout）；Owner 可改宣告／改池序推翻 | 低／高／中／否 |
| O5 | 品牌資產（logo／composer 圖） | `assets/` 僅 `.gitignore` | 維持 Owner 供圖；**不由 agent 生成品牌圖** | 中／中／中／否 |
| O6 | OpenAI 開發者身分驗證 | Portal 自回需驗證身分 | **HOLD，不代行** | 中／中／高／否 |
| O7 | 三合一 R2 之 42 原子／UPG-P04 交接 | 藍圖自載 `DESIGN_CANDIDATE`；`UPG_TRACEABILITY_R6.tsv` 已逐列標記 | **不在本輪施工**；以追溯表＋REPO 現況文件記錄，留待 ChangeSet `S4-UX-DISTRIBUTION-UPGRADE-R1` | 低／高／中／是（若現在做） |
| O8 | 上位文件是否併入 main（治理變更） | `public-plugin-verify` 正面允許清單不含 `docs/acceptance/` | **不放寬 gate**；上位文件留在證據分支，main 只放 README 入口連結 | 低／高／高／是（若放寬） |

## 2. REPO 完整更新／MERGE 裁決

**事實（權威量測）**
- `main`＝`224591431a16`，1439 blobs，**無** `packaging/`、`tools/build_public_plugin.py`、`docs/install/`、`.github/workflows/`。
- 開啟中 PR 6 筆（皆 draft）：#8（+72933/-46，493 檔，CI＋gate 綠，含 `ADR-0007`）／#6（+72886，492 檔，綠）／#5（250 檔，綠）／#3（247 檔，綠）／#4（`dirty`）／#2（`unstable`，gate **failure**）。
- 祖先關係：`main` 是 #8 的祖先；`#3`、`#5`、`#6`、R5X(`e00ab7b6`) 皆為 #8 的祖先；`#2` 非。

**裁決**
1. **合併 #8 → main**：零衝突（可快進／merge commit），一次帶入 Stage A/B、R5Y 封裝與 R5Z README＋ADR-0007 全鏈。
2. **關閉 #6／#5／#4／#3／#2**：前四者「已被 #8 包含」並附祖先證據；#2「CI gate `public-plugin-verify` failure」；#4「`dirty` 且被 #5 取代」。
3. **不刪除任何分支**：多條分支是證據包所引用的凍結受審主體（如 `062d84ae`），刪除將破壞可驗性；改以 `docs/REPO_STATE.md` 清冊化（用途／凍結指標／可否清理）。
4. **README／主頁完整升級**：新增「現況與證據入口」章（證據分支、R6 pack、`VERIFICATION_PROTOCOL.md`、PKG-00..10 對齊、車道車據、宣稱上限、私人外掛路線、私有/公開 gate 狀態）。
5. **工程衛生**：`.gitignore` 補強（`__pycache__`、`*.pyc`、暫存）；確認無追蹤垃圾與無憑證；main 首次 CI 運轉結論留檔。
6. **驗證**：合併後以 VERIFY 車道（強制 rank3 `glm-5.3-flash`）對「已合併 main」做獨立複核（樹內容、README 宣稱與實況一致、無憑證、CI 結論、PR 關閉理由正確）。

## 3. 結案／移交裁決

- 產出 `07_acceptance/SESSION_CLOSEOUT_R7.md`（最終結案）＋`_handover/CHECKPOINT_R7_FINAL_20261014.md`。
- 於 REPO 新增 `docs/NEXT_SESSION_START.md`：**新 session 起點**（本輪狀態、未完成 gate、Owner 待決、入口文件、可重跑命令、車道派工模板）。
- spine：R7 admission／result、TT 最終狀態、checkpoint、evidence_refs。
- 推送：證據分支（R7 pack）；main 由 PR 合併路徑更新。

## 4. 宣稱上限

本輪為 **Owner 授權下之 merge＋文件／衛生升級＋結案**；未 tag／release、未上架 Portal、未經 OpenAI 審查或第三方驗收；`BUILD_PASS != PORTAL_APPROVED != PUBLISHED != HOST_QUALIFIED != S4_PASS`。合併後之 main 屬「已合併候選態」，其獨立複核僅涵蓋本輪列明之檢查項。
