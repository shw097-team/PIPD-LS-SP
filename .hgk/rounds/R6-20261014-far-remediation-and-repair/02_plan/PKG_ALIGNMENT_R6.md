# R6｜落地對齊：本輪裁決 ↔ PKG-00..10

- 對齊標的：`…/PIPD/PIPD-LS-SP_PIPD-PKG/PIPD-LS-SP_PIPD-PKG-00~PKG-10`（11 檔，逐檔 sha256 見 `01_subject/PKG_INDEX_R6.json`，本輪以實體檔案重算）。
- 對齊層級聲明：**領域級 + 具名條款錨點**（H2／條款 ID）。**不宣稱** 7.5 MB 條文之逐條語義閉合；凡未逐條核對者一律標 `ANCHOR_ONLY`。

| 本輪項目 | PKG | 領域（H1） | 具名錨點（實體存在） | 對齊狀態 |
|---|---|---|---|---|
| FAR 方法與權威排序（上位文件為依據） | 00 | Constitution, Authority & Source Freeze | `## 0.1 成品的法位、裁決及限制`、`## 0.2 適用權威的分域排序` | ANCHOR_ONLY（領域對齊） |
| 證據參照／round 狀態物件 | 01 | Lifecycle, Canonical Objects & Schemas | `## 3. Lifecycle State & Gate Contract`、`## 4. PI / PD / P Normative Clause Crosswalk` | ANCHOR_ONLY |
| 需求登錄（`REQ-R6-FAR-REMEDIATION-001`）與前置編譯 | 02 | Intake, Requirements & Pre-Implementation Compiler | `## PART 0｜Executive Construction Contract`、`## 02-D00-H2-1｜Task-kind route into intake` | 已落 spine＋檔案收據 |
| 凍結來源與 repo context（commit／tree） | 03 | Pre-Dev Binder, RepoContext & Late-Bound Resolution | H1（領域） | 已記錄凍結 commit `062d84a…`／README 分支 `9643495` |
| 車道 provider／模型准入（`--force-rank`、必要臂） | 04 | Search-Before-Build & Technology / Provider Admission | H1（領域） | 已落收據（arm3/4/5、EXECUTE r6） |
| 派工契約與接收者交接（收據格式） | 05 | Pre-Execution Contract, ECP & Receiver Handoff | H1（領域） | 已落 `dispatch_receipt*.json`＋`LANE_RECEIPT_VERIFY_*` |
| FAR 證據規則、claim ceiling、驗收程序 | 06 | Traceability, TQAEP, Evidence & Claim Assurance | `## PART 0 — Authority、Full-Corpus SOP、Baseline & 修補法位`、`## PART 3 — SourceClause/Atom 全量直接分母` | 本輪交付 `FAR_REPORT_R6.md`＋`VERIFICATION_PROTOCOL.md` |
| skills-only 投影與安裝入口（UPG-P01／P02） | 07 | Skills, Multi-Surface Projection & Distribution | H1（領域） | 產物實體存在；`PARTIAL`（品牌／UAT 未閉合） |
| CI／發行／供應鏈／可觀測（D2、D4） | 08 | CI, Release, Supply Chain & Observability | `SDLC Release/Handoff — readback and rollback`、`08-D03-H1`、`SC-08-002+004+007 supply-chain truth separation`、`CR-08-003`（SLSA 自稱 vs 實證） | 證據補齊本輪執行；merge／tag／release 仍屬 Owner |
| 偏差修補與再資格化路徑（TT-001／TT-004／TT-005） | 09 | Evolution, Migration & Requalification | H1（領域） | TT-004／005 CLOSED；TT-001 OPEN（Owner） |
| 控制平面綁定、spine 回寫、車道路由 | 10 | HG-KSEOS, GENIE, JIT & SGM Integration / Promotion | H1（領域） | admission 已入 spine；車道臂綁定以收據證明；池序改善屬 Owner |

## 未閉合與後續（不在本輪施工）

- `UPG_TRACEABILITY_R6.tsv` 標記為 `NOT_RUN` 之 `TR-01..40`／`A01..A42`／`F01..F14`：屬未來 ChangeSet `S4-UX-DISTRIBUTION-UPGRADE-R1`，須另立受控 PR 與獨立驗收。
- 上位文件是否併入 `main`：屬治理變更（動到 `public-plugin-verify` 正面允許清單），未經核准不作。
- 品牌資產、發行版號、Portal 交接、開發者身分：Owner／Human Gate。
