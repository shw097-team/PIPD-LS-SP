# PIPD-LS-SP S4｜三合一小型升級藍圖（R2 全量審查升級修補版）

> **Blueprint ID**：`PIPD-S4-TRIPLE-UPGRADE-BLUEPRINT-20261012-R2`  
> **Document Version**：`2026-10-12_r2_AUDIT_PATCHED_FULL_REPAIR`（取代 R1 的施工設計主體；不是 Plugin Release Version）  
> **Date**：2026-10-12 Asia/Taipei  
> **Supersedes**：`PIPD-S4-TRIPLE-UPGRADE-BLUEPRINT-20261012-R1`（source SHA256 `592044addde580dba70e7df38ad82be072c3d5ccc6cee4988868934367bca505`）  
> **Audit source**：`PIPD-LS-SP S4｜三合一小型升級藍圖 — FULL DESTRUCTIVE AUDIT.md`（SHA256 `2321c54bb6ce482d7994fb14dfa74e4d4db158a56bf0ece6b927f28570d5f8d6`）；AUDIT §§1–10  
> **Route**：`IMPORT + DESIGN + bounded EVAL-PLAN + DRIFT_PROBE`；未經外部 HGK、Codex CLI 或 OpenAI Portal 實際執行  
> **Report verdict**：`DOCUMENT_REPAIR_COMPLETED / DESIGN_CANDIDATE / INDEPENDENT_REAUDIT_PENDING`  
> **Public release gate**：**`FAIL-CLOSED / HOLD`**；**`PIPD_S4_FULL_PASS=NOT_GRANTED`**  
> **Repository baseline**：`shw097-team/PIPD-LS-SP @ 224591431a164ab72a9423cd180e417e8a762403`; tree `1a9fcb94a42eb589e405c2453793be986419d4cb`；任何新施工前必重新凍結。  
> **Plugin version**：`NOT_ASSIGNED / OWNER_DECISION_REQUIRED`，不得把本文 R2 當作 Plugin SemVer。  
> **一句話結論**：**不新設 S4.5；沿用 S4 PKG-07／PKG-08，單次受控 ChangeSet／PR，確定性投影八個既有 Skills，補發行封裝、公開發行交接與 Web／Agent 雙主入口；F01–F05 缺陷及 42 個需求原子逐條可追；公開發布與外部 S4 PASS 獨立封鎖。**

## 0. 版本/證據/請求範圍聲明

本 R2 為**獨立完整的升級取代文件**，不以「見 R1」代替正文。已承接 R1 的 SSOT、架構、RCA、四工作包、UPG-G00–G09、OROCHI 候選與機器 TSV／JSON，同時替換有 Fail-open 的 exporter/Manifest/workflow/test/fallback 範本。本文說明所有原始證據是否真正存在：本機僅檢測隔離**合成測試**，不冒稱官方 Plugin Validator、真實 Repo 正式構建、Plus/Free/Agents 或 Publisher Portal 的原始驗收。AUDIT 中的 F01–F05 是**針對 R1 的已重現問題**；R2 新範本有相應合成修補測試，不等於 R2 已被另一獨立 Checker 無死角稽核。

**核心版本隔離**：`PIPD-LIFECYCLE-SPEC@1.1.0` 為上游生命週期標準版本，本文 R2 是發行設計藍圖，PIPD source release 現為 `v0.1.1-preview.3`，Plugin 發行版號需由 Owner 另定合法 SemVer。四者不可互相替代。**該 baseline 來源本輪 GitHub connector 於 2026-10-12 read-only 重驗；不得當作未來 main 永遠不變的保證。**

### 0.1 十條不可降級不變式

1. **ONE CHANGESET**：`S4-UX-DISTRIBUTION-UPGRADE-R1` 為新建議 ChangeSet，現有 PKG-07／PKG-08 之四工作包；單一受控 PR，OpenAI Portal 為獨立人工 Release Gate。`[PIPD-LS-SP_藍圖.md §15.2；PIPD-PKG-07 Part7–8；PIPD-PKG-08 Part11]`
2. **ONE SOURCE**：已有 8 個邏輯 Skills；不生成第九個 dispatcher Skill、不複製第二個維護中的上游技能樹。`[PIPD-LS-SP_藍圖.md §8.3/§15.2]`
3. **ZERO CORE WRITES**：`skills/`、`src/`、根 schemas、Canonical/DOC/PKG/ECP/TQAEP oracle 寫入集為零。`[PIPD-PKG-07 Part7–8；GPTB-KP11-R03]`
4. **NO MODEL REWRITE**：Skills 原文先位元組複製；如 Header 不合規，只有 Owner 核准的發行副本欄位機械移轉，Body 不改且差異/負向行為逐項核對。`[PIPD-LS-SP_藍圖.md §15.2；challenge-review-SKILL §Invariants]`
5. **NO EFFECT CLAIM**：Web Skills-only 僅來源綁定的規劃/交接；不等於 Wheel/13 CLI、HGK Runtime、作業執行或 S4 外部驗收。`[DOC-08 §13.3–13.5；PKG-06 TQAEP]`
6. **MCP/Apps/Actions/Hooks OFF**：此 ChangeSet 不新增 Backend、Remote MCP、Credentials、輪詢/寫入工具。`[PIPD-SP-SPEC-030；14_APPS_ACTIONS_MCP_ROUTEOUT.md]`
7. **FAIL-CLOSED EVIDENCE**：`build != host loaded != portal approved != published != user verified != S4_PASS`。`[DOC-08 §13.3–13.5；PKG-08 Part11；GPTB-KP16-R01..R08]`
8. **WEB ONE ROUTE / AGENT ONE PROMPT**：目標為最少按鍵，仍不可省略必要安裝同意及公開發布者身份。`[17_UX_ONBOARDING_NO_BRAIN_FLOW.md；三合一附件 §5]`
9. **SOURCE/RELEASE PIN**：Commit、Git tree、source/file SHA、schema SHA、manifest SHA、ZIP SHA、已發布 asset SHA 分開綁定。`[16_RELEASE_PACKAGING_CHECKSUM_READBACK.md；RELEASE_CORRECTION_WEB_MOUNT.md L7–60]`
10. **SOD AND TT/CR**：Maker、Independent Checker、Release Owner、Human Publisher 各有獨立證據與否決權。`[challenge-review-SKILL §Workflow；11_EVIDENCE_REQUIREMENT_MATRIX；18_TT_CR_DRIFT_REGISTER]`

### 0.2 對 R1 驗收失敗的升級處理

R1 在 AUDIT §1 被判 `FAIL_REPAIR_REQUIRED`，本 R2 **不作回溯竄改其結果**。R2 完成文件和樣板層的缺陷修補、覆蓋矩陣與可測候選，AUDIT P0 F01/F03/F04/F05 有對應負向測試；R1 之 `PLAN_APPROVED` 被降格為 `ARCHITECTURE_DIRECTION_ACCEPTABLE`，只有新候選獲獨立驗證後才可上升 `BUILD_PASS`。`[AUDIT §§1,4,9]`

---

## 1. Inputs Manifest：索引→實質條文→全文關鍵字→子要求→目標段落

### 1.1 實體資料庫全量掃描結果

本輪以容器對所有可見 `.md` 檔執行**整份** `read_bytes→UTF-8 strict→SHA256→splitlines→8 大詞族逐行全文比對`；**無抽樣、無選前幾頁、無 OCR**。共 **102 份 Markdown、71,971,885 bytes、866,660 行**。這是**物理可讀性與詞族位置索引**，不是 866,660 行皆完成獨立人工語義驗收；上游原子完整性依後述 `CR-SOURCE-ATOMIC` 保留未閉合。若上游或附件不在目前物理工作目錄，一律 `MISSING`；本次列出的 102 份均為 `FOUND`，部分為內容相同的重複報告副本，不可灌水為不同權威來源。

**8 詞族**：`INSTALL_UX`, `PLUGIN_FORMAT`, `RELEASE`, `SECURITY`, `TQAEP`, `OPEN_SOURCE`, `AGENT`, `REQUIREMENT_ATOMS`；詞命中僅觸發 Substantive Review，不能自動取代「實質內容判定」。初始審查（AUDIT）另以 11 詞族對約 46 份首要規範作了全文搜尋；本次以完整物理目錄做更大範圍掃描，原子核查仍聚焦此次 Upgrade 的 A01–A42。

### 1.2 權威與證據效力（本文件原地重述）

| 層級 | 來源 | 法位 | 精確來源定位 | 作用與不允許的推論 |
|---|---|---|---|---|
| P0 | System/Developer、使用者本次 PATCH/SOP | Highest | 本次使用者指令 SOP1–7 | 限定「完整設計修補」；不授權外部施工/發布 |
| L0 | `PIPD_LS_canonical_standard.md`, `PIPD_LS_DOC-00..09` | NORMATIVE | Canonical `PIPD-LIFECYCLE-SPEC@1.1.0`; `DOC-07` TQAEP；`DOC-08` §§8.9/9.3/9.5/13.3–13.5 | 生命週期 SSOT/獨立驗收及安裝語義 |
| L1 | `PIPD-LS-SP_PIPD-EC_SGM_總藍圖`, `PIPD-LS-SP_藍圖.md`, `PIPD-LS-SP_skeleton.md`, `PIPD-PKG-00..10` | NORMATIVE scoped | `藍圖 §8.3、§15.2、§15.3`；PKG-07 Part7–8、PKG-08 Part11、PKG-06 TQAEP | 8 Skill/Generated Surface Adapter/ECP/Release 及 claim ceiling |
| L2 | `00_KNOW_INDEX..19_KP_INDEX_CROSSWALK`, `challenge-review-SKILL.md` | LOCAL NORMATIVE | KP09/11/12/13/14/16/17/18；challenge §Invariants/Workflow | route-out、rawness、安全、HITL、TT/CR、UX、no second authority |
| L3 | `SDLC_PRW_HLPE_SKILLS_PLUGIN_R2`, `SWOF_ECP_SKILLS_PLUGIN_v2.0.1`, `SWOF_TQAEP_SKILLS_PLUGIN_v2.0.1` | Scoped donor | 各 donor 包 header 及 workflow/技能段 | 施工/測試輸入，不凌駕 canonical SSOT |
| H | 全篇對話、`三合一小型升級_總討論.md`、另兩份決策附件、R1 藍圖及本次 AUDIT | Decision history / challenge | 總討論 L9–1359；三合一附件 §§0–11；鑑定誤附件 §§1–10；AUDIT §§1–10 | 需求沿革、缺陷證據及本次補丁映射；矛盾部分以原上游規範及當前證據校準 |
| R | 受測 GitHub Repo commit/tree、Web Mount 發行 | Implementation evidence | `skills/pipd-*`, `README.md`, `tools/build_mount_pack.py`, `RELEASE_CORRECTION_WEB_MOUNT.md` | 現有實作真相，不取代上游規範 |
| W | OpenAI Agent Plugins、Agent Skills、GitHub Actions、OpenSSF、OSS Repos | SUPPORT | 本文 §4 Technology Register 附具名官方 URL | 僅平台/開源實作比對，不得把 Web 支援敘述寫成 PIPD 規範 |

### 1.3 主要來源逐檔讀取狀態/定位

| 分組 | 應有件數 | Found | 核心定位及驗證策略 |
|---|---:|---:|---|
| KB `00`–`19` | 20 | 20 | `00_KNOW_INDEX` 入口；KP09/11/12/13/14/16/17/18 實質條文；本文 §§0/5/9/11 |
| `challenge-review` | 1 | 1 | `challenge-review-SKILL.md` Invariants/Workflow；本文 §§0/9/10 |
| PIPD PKG `00`–`10` | 11 | 11 | PKG07 Part7/8、PKG08 Part11、PKG06 TQAEP；本文 §§5–11 |
| Skeleton/主藍圖/EC SGM 總藍圖 | 3 | 3 | 主藍圖 §8.3/§15.2/§15.3；skeleton ClaimCeiling；本文 §§0/5/11 |
| Canonical + DOC `00`–`09` | 11 | 11 | DOC07/08 與 lifecycle SSOT；本文 §§0/3/9 |
| 三份必需 donor | 3 | 3 | Scoped ECP/SDLC/TQAEP；本文 §5.3 |
| 三份本次歷史附件 | 3 | 3 | 問答/版本歷史；本文 §§2/3/A01–A42 |
| 原 R1 藍圖＋本次 AUDIT | 2 | 2 | R1 §§0–9/附錄 A–E、AUDIT F01–F14；本文 §§6/10/12 |

其他 Project/legacy/PI-PKG/PD-PKG/使用文件在附錄 Inventory 全列、物理掃描且定為 `SUPPORT_OR_HISTORICAL`；本次變更是否直接適用仍須由 Owner 對 scoped atom ledger 勾選，不能把全量 scan 冒充每一條 legacy 規範都適用。

## 2. 決策沿革、RCA、歷史故障與勘誤

### 2.1 時序/裁決完整化

| 階段/定位 | 原痛點或設計 | 本 R2 保留／修正 |
|---|---|---|
| 總討論 L9–455：Web 安裝 vs MCP、OpenSpec/Spec Kit/Matt Skills/GSD/gstack/Superpowers | CLI/Web Mount 存在但 Web 端非完整 Python Runtime；MCP 欠工程必要性 | KEEP：Skills-first，MCP OFF；OSS 必須逐項具名決策；需真實機器證據再選 Read-only MCP |
| 總討論 L459–702：極簡安裝 | Plus 優先、Free 備援；Web/Agent 各一條主路徑；Agent 單 Prompt | KEEP + REPAIR：Web fallback 必須實際產生；Host install 實際命令、版本、沖突與卸載 |
| 總討論 L704–960：HGK Codex CLI vs Work Sol | Codex 確定性封裝主施工；Work 僅輔助；Publisher 人工審核 | KEEP：不讓 AI 自由重新摘要/壓平八 Skills；不得認定 Work+某模型=完整性保證 |
| 總討論 L962–1180：要否 S4.5 子開發 | Skills 原料已存在，Public Plugin 缺外殼 | KEEP：一個 release adapter task，不加第九 Skill/第二核心 |
| 總討論 L1181–1359 + 三合一附件 §§0–11 | 一個 ChangeSet/四工作包/十 Gate | KEEP + REPAIR：完善事件契約、原始證據、release tuple、UI journey 與部署阻斷 |
| R1 藍圖 §§0–9、附錄 A–E | 施工級範本自稱可直接套用 | RETRACT/REPLACE：R1 假 PNG、manifest、frontmatter、null commit、symlink sidecar 等 Fail-open |
| AUDIT §§1,4,5,7,8 | F01–F14、A01–A42、RP-P01..08 | ADOPT AS CHALLENGE INPUT：每項有責任段落/驗收/缺證據狀態；不偷改 AUDIT verdict |

### 2.2 RCA：症狀 → 根因 → 反證/直接定位 → 可執行修補

| 症狀 | 根因 | Source locator | R2 修補/測試 |
|---|---|---|---|
| 原作者 Web 安裝困難 | README 混淆 Wheel、Web Mount、Native Skill/Plugin、MCP | `README.md` preview3 Install；總討論 L459–567 | §8 一頁兩入口與狀態 selector；UAT-UX-01..08 |
| Plus 誤以為可自行上傳 Native Skill | 帳號能力差異被錯當常態 | 總討論 L571–588；OpenAI Plugins Help | §8 Plus 真實 Directory 主線；未發布當下改單 MD |
| Free 需上傳多文件 | 文件碎片、無單檔導出工具 | R1 §6.7；AUDIT F08 | §7.4 `build_web_fallback.py`、無截斷檢查、單份下載 |
| Web 掛載等於 S4 Runtime | Capability Loss 不明 | 主藍圖 §15.2/§15.3；DOC08 §13 | §0 invariants，README `DOC_MOUNT_ONLY` |
| Agent 安裝需懂腳本/平台配置 | 只給抽象 Prompt，無真實 Host 路徑 | R1 §6.5；AUDIT F07/A14–A18 | §8 Per-host runbook（CLI/GUI 不混用）、一段 Prompt、預授權 |
| `preview.3` 包 8 欄舊 Commit | 打包只存字串不比 tag | `.hgk/.../RELEASE_CORRECTION_WEB_MOUNT.md L7–60` | §6.2 freeze/§9 G05，mutation `stale predecessor` |
| 假 PNG 可打包 | 原 R1 只檢檔頭 magic | AUDIT §4 F01 R1 L398–401 | §7.2 Pillow 全檔解碼、負測 F01 |
| 任意 Manifest 欄位 accepted | 非官方 Schema 校驗 | AUDIT §4 F02 R1 L351–374 | §7.2 使用**鎖定 SHA** 的 Agent Plugins 1.0 JSON Schema + local constraints |
| 無效 SKILL.md accepted | 只查 `SKILL.md` 路徑和 bytes | AUDIT §4 F03 R1 L384–396 | §7.2 正規化/必填 name/description + 官方 skills-ref + UAT |
| `source_commit:null` map | 缺 Frozen release tuple | AUDIT §4 F04 R1 L405–409 | §7.1 freeze script + assert 40hex/tag/tree/digests；F04 test |
| symlink 覆寫 sentinel | 輸出沒有根路徑隔離/ O_EXCL | AUDIT §4 F05 R1 L409–410 | §7.2 root private dir、拒 symlink、隔離 stage、race guard，F05 test |
| 同 Tag 不同發行 bytes | GitHub 替換 asset，Tag 不保證下載 bytes | 修復記錄 L29–60；三合一附件 §2 | §9 immutable-policy、下載後 hash、客戶端版本 readback |
| 實施者自行宣稱 PASS | Maker/Checker/Publisher SoD 合併 | challenge §Workflow；DOC07；AUDIT F13 | §9 RACI、獨立 fresh receipt、HITL |
| 新增 S4.5/MCP | 將發行適配誤視新產品生命週期 | 主藍圖 §15.2；三合一附件 §0 | §5 Keep four tasks、forbidden delta + OEI |

### 2.3 八項必要勘誤（全部有正文措施）

1. R1 `PLAN_APPROVED` **改為** `ARCHITECTURE_DIRECTION_ACCEPTABLE / R2_INDEPENDENT_REAUDIT_PENDING`；禁止由文件完整性推論 Release PASS。
2. 八個 Skill 在 Repo 已存在但無 root `plugin.json`；既有 Web Mount ZIP 不可改名冒充 Public Plugin。`[Repo Git Tree；OpenAI Package guide]`
3. 原碼位元組等價不是 Host 官方語義驗收；自訂 frontmatter 必以 `skills-ref`/Portal 驗；若需搬欄位，必有核准 `derivations`，Body 一字不改。`[Agent Skills specification；AUDIT F03]`
4. `preview.3` 舊 Commit stamp 已有 **修復紀錄**，不能宣稱目前仍是同一未修復 Bug；其 build-time guard 未補仍為 CR_OPEN。`[Repo release correction L55–60]`
5. README「公開目錄可安裝」須取決於已發布、Account 可見、真實 Consumer UAT；未具備則單一 MD 文檔備援並明示限制。
6. 四個網站/隱私/條款 URL 對**skills-only ZIP** 在當前 Submission Errors 中屬 optional，MCP-backed 公開審核另有額外要求；上架文案仍需真人提供可驗證身份/政策資料，不得隨意填 placeholder。
7. `vercel-labs/skills` 是候選可重用 installer，不是保證每種 Host 命令語法、路徑或安裝版本相同；要 Host 本地探測、pin、preview/HITL/有效載入。
8. 正式 S4 Independent PASS，TraceLink/trace closure，原 OPS/DEV/TQAEP 權限與 ECP Gate 不因 Plugin 發布改善而上升；若相關缺陷影響 Plugin 宣稱，須阻斷。

## 3. Repo 實況、差距、ChangeSet 與 Minimum-Sufficient Architecture

### 3.1 最新 GitHub connector readback（非推測）

2026-10-12 GitHub read-only API 回報：`main=224591431a164ab72a9423cd180e417e8a762403`, `HEAD tree=1a9fcb94a42eb589e405c2453793be986419d4cb`, Git recursive Tree 1,853 entries、`truncated=false`；8 `skills/pipd-*/SKILL.md`，48 個 Skill supporting files；root `plugin.json` 與新公發 package manifest 未找到。`v0.1.1-preview.3` GitHub Release asset Web ZIP **API metadata** digest `sha256:af342d281f02ba04f284a1625f4a58a6f2de15549cc182a0c61ce357ec6b504f`；未在本輪下載原始 ZIP 位元組作獨立重算。正式施工新 commit/new version 必重新 readback。Repo 本輪未改動。

| 層面 | Frozen baseline | 未閉合問題 | Upgrade decision |
|---|---|---|---|
| Core S4 | 13 CLI、19 Schema families、PI/PD/ECP/TQAEP | 原 S4 Independent Full PASS 尚未簽 | KEEP，不在本小升級裡改編譯器 |
| Skills | 八個邏輯 Skill，每個六檔，合計 48 | Header 標準相容性/實際 Host load 未驗 | Generated projection only |
| Web Mount | `preview.3` 已發 9 member doc pack | 非 root Agent Plugins package；Free 單檔缺 | 保留為來源；生成 1 MD fallback |
| Public Plugin | 無 root `plugin.json` | 不可能直接公開可安裝 | 增根 manifest + zip + 官方 validator |
| DX | README 多路徑 / OS 多選 | 非工程用戶理解成本高 | 二主入口/一 Agent Prompt/備援收摺 |
| Release | SHA256SUMS/Wheel/Web.zip 等 | Tag vs ZIP identity 防回歸未自動完成 | 釘住 release tuple + immutable new version |
| Portal/Host | 未取得實際 submit/install UAT | 缺人員身份、平台審核/實測 | 外部 HOLD，各獨立 state |

### 3.2 整合架構與四工作包

```text
PIPD canonical source / Frozen Source Commit+Tree
  ├─ Original 8 × Skills + references/schemas/tests  [READ_ONLY]
  ├─ Existing Web Mount Pack / 13 CLI / 19 schemas      [UNCHANGED]
  └─ Source release identity                            [PINNED]
                  │
       ONE ChangeSet: S4-UX-DISTRIBUTION-UPGRADE-R1
          UPG-P01: vendor-compatible Skills-only ZIP projector
          UPG-P02: Web/Agent route-first install docs + one MD fallback
          UPG-P03: security/schema/provenance/negative/Host UAT
          UPG-P04: release manifest/rollback/public portal handoff
                  │
         INDEPENDENT CHECKER: clean-room evidence replay
                  │
      RELEASE OWNER: scoped candidate release approval
                  │
   VERIFIED HUMAN PUBLISHER: ZIP upload/scans/review/Publish
                  │
         Plus/Free account-level consumer UAT
```

### 3.3 最小變更檔案樹及 Deny Set

```text
NEW  packaging/public-plugin/plugin.json          # approved portable manifest
NEW  packaging/public-plugin/assets/{logo,composer}.png  # actual approved PNG
NEW  packaging/public-plugin/requirements.lock    # hash-pinned deps / Owner lock
NEW  packaging/public-plugin/plugin.schema.json    # official vendor schema (digest pinned)
NEW  packaging/public-plugin/derivations.json       # approved header projection or empty
NEW  tools/freeze_public_plugin_source.py           # frozen source ledger
NEW  tools/build_public_plugin.py                   # bounded deterministic generator
NEW  tools/build_web_fallback.py                    # one-attachment fallback generator
NEW  tests/test_public_plugin_packaging.py         # synthetic red-to-green
NEW  tests/test_web_fallback.py                      # no-truncation/sidecar attack
NEW  docs/install/README.md                       # ONE install SSOT / host decisions
NEW  docs/install/PIPD_AGENT_INSTALL_PROMPT.md    # ONE user-facing prompt
MOD  README.md                                    # only 2 top-level install routes
NEW  .github/workflows/public-plugin-verify.yml   # read-only PR/dispatch verification
OUT  dist/plugins/<new SemVer>/*                  # built artifacts (do not commit unapproved)
OUT  dist/install/PIPD_WEB_FALLBACK.md           # generated, bounded, source stamped
NO   skills/**, src/**, schemas/**, canonical/**, DOC/**, PKG/**,
     ECP/TQAEP oracle, existing release assets, MCP, Actions, Hooks.
```

**工具重用先於新碼**：現有 `tools/build_mount_pack.py` 已具固定 ZIP metadata、SHA sidecar、解壓 readback；`tools/portable_install_check.py` 有 Wheel 安裝/卸載/殘留；應先將重用的 ZipInfo/sha utils 小幅共用。因 Public Plugin 額外需要 owner-approved Header projection、Plugin JSON Schema、兩個圖示及 Frozen tuple，新增一個**薄 exporter** 合理；不應重做 Python Installer/泛用 CLI Framework。`[Repo tools/build_mount_pack.py L33–160; portable_install_check.py L70–225]`

### 3.4 宣稱分層

| State | 需要何證據 | 不代表 |
|---|---|---|
| `DOCUMENT_REPAIR_COMPLETED` | R2 MD 在本輪建檔與本地合成測試 | build production PASS |
| `LOCAL_PACKAGER_PASS` | 在受控隔離 worktree，source sha/schema/icon/zip readback 與合成回歸 | 官方 Portal scan/Host loading |
| `BUILD_PASS` | G00–G05 真正 code/build/source/security tests，Independent Checker raw evidence | user install/PUBLIC |
| `LOCAL_HOST_QUALIFIED` | 每個已聲明 Host G06–G08 正負載入/卸載 readback | OpenAI approval |
| `PORTAL_DRAFT/SCAN/REVIEW_APPROVED` | Portal 實際 UI/API 收據 | published |
| `PUBLIC_PUBLISHED` | Human Publish + Public listing readback | Plus/Free individual availability |
| `PUBLIC_CONSUMER_VERIFIED` | 不同帳戶成功率與 source-bound negative UAT | PIPD_S4_FULL_PASS |
| `PIPD_S4_FULL_PASS` | 原上游全套客觀 Gate、Trace、安全、HITL 獨立閉合 | **本次 Upgrade 不簽發** |

## 4. Web/OSS/工具完整具名技術比較與防降級（SUPPORT ONLY）

**證據法位**：本節外部技術主張為 `SUPPORT`，不凌駕本文 §1 上游；部分工具「近期熱度」由 Issue/Changelog 個案推知，不能冒稱大數據統計、成熟技術者百分比共識。每項重大平台決策列至少兩個*不同文件或實作來源*；並明言「不同文件」不一定是獨立統計驗證。

### 4.1 官方格式與平台（兩來源交叉）

| Claim/Decision | Source A | Source B | 工程接納/邊界 |
|---|---|---|---|
| Portable Plugin root `plugin.json`，Skills 在固定 `skills/`；MCP 可省略 | [OpenAI Package your plugin](https://developers.openai.com/plugins/build/plugins) | [Agent Plugins schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) | **ADOPT**，不以舊 Web Mount 假代；官方 schema 鎖 digest + Portal |
| 8 個 `SKILL.md` 需符合 frontmatter/body/relative reference | [Agent Skills specification](https://agentskills.io/specification) | [OpenAI Build skills](https://developers.openai.com/plugins/build/skills) | **ADOPT**，`skills-ref validate` + Public Portal + effective load |
| ZIP 提交 ≠ 公發 | [OpenAI submission](https://developers.openai.com/plugins/deploy/submission) | [Submission errors](https://developers.openai.com/plugins/deploy/submission-errors) | **ADOPT**，ZIP→scan→review→Human Publish→consumer UAT |
| Skills-only listing URL 與 MCP reviewer cases 要求有別 | [OpenAI submission](https://developers.openai.com/plugins/deploy/submission) | [Submission errors](https://developers.openai.com/plugins/deploy/submission-errors) | **ADOPT**，四 URL skills-only 可選，MCP 5+3/demo/OAuth 不應強加 |
| GitHub CI least privilege、避免 privileged untrusted PR | [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use) | [OpenSSF Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md) | **ADOPT**：`permissions:contents:read`, SHA pin, no `pull_request_target` |
| Host install 真正載入不等於檔案存在 | [Hermes Skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) | [Agent Skills specification](https://agentskills.io/specification) | **ADOPT**：fresh session/discovery/positive/negative/permission/rollback |
| 供應鏈來源、build 主體、artifact hash 分別記錄 | [SLSA provenance](https://slsa.dev/spec/v1.0/provenance) | [OpenSSF Scorecard](https://github.com/ossf/scorecard) | **ADOPT minimal provenance ledger**；完整 SLSA/Sigstore attestation 暫緩待風險/Owner |

### 4.2 六個指定 OSS 逐個實質評估（不把列名當作評估）

| OSS / 官方入口 | 強項／與 PIPD 的互操作界線 | 版本/狀態證據；已知風險 | 選型/為何不當本 ChangeSet Runtime 依賴 |
|---|---|---|---|
| **OpenSpec** [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) | change-first proposal/spec/delta/archive；可借鑑 change ledger/人員確認；PIPD 原已 canonical/evidence/PI-PD Compiler | [CHANGELOG](https://github.com/Fission-AI/OpenSpec/blob/main/CHANGELOG.md) 含 Windows EPERM、CLI auto-confirm/scope guard 調整；本輪未 pin 可安裝版的完整 transitive lock | `BENCHMARK_ONLY`：不加入工作流引擎；採用「先批准變更再動手」與 bulk finding 設計；版本/安全必要性另 Gate |
| **Spec Kit** [github/spec-kit](https://github.com/github/spec-kit) | Spec→Plan→Tasks、Bundle 只組合元件不新增 runtime；參考離散變更/來源 pin | [bundles docs](https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md)：digest+releases 版本紀律；[June newsletter](https://github.com/github/spec-kit/blob/main/newsletters/2026-June.md) | `DESIGN_REFERENCE`：共用既有 Compiler，勿導入另一 Spec Engine；借用 bundle pin/readback 思路 |
| **Matt Skills** [mattpocock/skills](https://github.com/mattpocock/skills) | 小型可組合 Skills、可學習 minimal SKILL header/人類易讀入口 | 曾出現用戶安裝後仍為舊版的社群歷史記錄（見對話總討論 L274–280）；具體最新安裝契約未本輪 Host 重驗 | `BENCHMARK_ONLY / VERSION_PIN_PENDING`：借鑑版本 readback，不把其 Skills 加入 PIPD 發行依賴 |
| **GSD** [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) | 階段工作流、薄 MCP companion；可借鑑 state/host surface | 總討論 L254–260 記錄 2026-10-05 `v1.16.0` 與 repository migration；外部當前版本必以現場 Tag 再核 | `DEFER_RUNTIME`：PIPD 無需第二狀態機；MCP 只有 live/auth/action/dynamic discovery 真需求才 ADR |
| **gstack** [garrytan/gstack](https://github.com/garrytan/gstack) | role-based QA/review/Go-NoGo；適合作為獨立驗收測量對比 | 總討論 L294–300 記錄 10/11–12 fail-closed 严格性與 privacy 變更；本 ChangeSet 未跑互操作 baseline | `BENCHMARK_ONLY`：採效果/完整 raw log，不複製整套角色系統 |
| **Superpowers** [obra/superpowers](https://github.com/obra/superpowers) | progressive workflow、TDD/review、按任務尺寸調整 | [Release Notes](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md)；總討論 L264–270 記錄 v7 Host issues | `DESIGN_REFERENCE`：使用者只需短 Prompt，真正工作由 Host Adapter；不納完整執行框架 |

**六者均明確具名、各有納入／不納入決策、維護與引用**。不以 stars 或話題熱度取代需求證據；若需要導入其中任何一項實際 runtime 必有單獨的 `ADR`，列成本、安全面與 UAT ROI，不在本次發行 PR 偷加。

### 4.3 要用的工具/技術／可選工具 — 完整 Adoption Register

| Tool / version identity | 來源 | 本案作用 | 層級/核准狀態 | Pin/Fail strategy |
|---|---|---|---|---|
| **OpenAI Agent Plugins 1.0** | [package guide](https://developers.openai.com/plugins/build/plugins), [schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) | root manifest/skills distribution | `REQUIRED SUPPORT STANDARD` | Vendor JSON Schema SHA pin；Portal 最終檢驗不能省 |
| **Agent Skills + skills-ref** | [spec](https://agentskills.io/specification), [ref validator](https://github.com/agentskills/agentskills/tree/main/skills-ref) | 8 Skills 合規 | `REQUIRED CHECK` | 要現場鎖定 tools 版本/快照；缺 validator→HOLD |
| **Python stdlib** | [stdlib zipfile](https://docs.python.org/3/library/zipfile.html), local Repo `build_mount_pack.py` | deterministic zip, hashlib, tempfile, git rev-parse | `REUSE_FIRST` | existing packager diff，輸出安全隔離 |
| **PyYAML** | [pyyaml.org](https://pyyaml.org/) | Safe frontmatter parse | `SCOPED BUILD DEP` | Hash-pinned requirements；`safe_load`，禁 executable tags |
| **jsonschema (Python)** | [python-jsonschema.readthedocs.io](https://python-jsonschema.readthedocs.io/) | 官方 schema 校驗 | `SCOPED BUILD DEP` | Lock with `--require-hashes`; allow no network runtime |
| **Pillow** | [Pillow docs](https://pillow.readthedocs.io/) | 真 PNG 解碼/尺寸校驗 | `SCOPED BUILD DEP` | `.verify()` 與實體圖示；錯圖 P0 FAIL |
| **GitHub Actions** | [Secure use](https://docs.github.com/en/actions/reference/security/secure-use), [checkout](https://github.com/actions/checkout) | synthetic/regression/source build CI | `APPROVE READ-ONLY CHECKS` | `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`（v4.2.2 Git ref 核實），不要 `pull_request_target` |
| **OpenSSF Scorecard** | [ossf/scorecard](https://github.com/ossf/scorecard), [checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md) | 檢查 CI/Repo 風險 | `ADVISORY CHECK` | action Pin & scope review；不把檢查器分數當 S4 Gate |
| **SLSA** | [slsa.dev](https://slsa.dev), [slsa-github-generator](https://github.com/slsa-framework/slsa-github-generator) | 可選 provenance attestation | `DEFER` | 此版 minimal ReleaseTuple；Owner 需上游特別 Gate 才啟用 |
| **Sigstore/Cosign** | [sigstore.dev](https://www.sigstore.dev/), [cosign](https://github.com/sigstore/cosign) | 可選 signing/provenance | `DEFER` | 只有供應鏈威脅模型或平台要求才新增，避免過度工程 |
| **Secret scan: Gitleaks or GitHub secret scanning** | [gitleaks](https://github.com/gitleaks/gitleaks), [GitHub security](https://docs.github.com/en/code-security/secret-scanning) | 禁止密鑰進 ZIP | `REQUIRED CAPABILITY, TOOL OWNER_SELECTED` | 指定一種、鎖 SHA 和 raw receipt；缺掃描 FAIL-CLOSED |
| **SBOM: Syft** | [anchore/syft](https://github.com/anchore/syft), [CycloneDX](https://cyclonedx.org/) | 依賴清單/License | `CONDITIONAL` | 若發行流程/政策要求則產出，否則 CR_OPEN 殘餘風險 |
| **vercel-labs/skills CLI** | [repo](https://github.com/vercel-labs/skills), [CLI](https://github.com/vercel-labs/skills/blob/main/src/cli.ts) | Agent 多 Host Skills 安裝候選 | `SECOND-LINE` | `npx skills` 未 pin 禁止自動執行；各 Host 實測後核准 |
| **Hermes Skills Hub** | [work with skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md), [skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) | Hermes Native install/discovery | `NATIVE FIRST` | project local + trust/scan，不能只用 global install 冒稱 project-only |
| **Codex GUI / Codex CLI** | [OpenAI Codex plugins](https://developers.openai.com/plugins/build/plugins), [Codex Skills](https://learn.chatgpt.com/docs/build-skills) | Codex plugin/skill consumer | `NATIVE FIRST` | GUI/CLI 各算獨立 Host UAT；未實測回 NOT_EXECUTED |
| **Claude Code native Skills** | [Claude Skills docs](https://code.claude.com/docs/en/skills), [Claude Plugins](https://code.claude.com/docs/en/plugins) | `.claude/skills`/plugin source | `NATIVE FIRST` | project-local、同名衝突、卸載殘留與代理認知分開驗 |
| **Plugin Creator / ChatGPT Work** | [OpenAI package guide](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission) | Draft/metadata/Publisher 附助 | `OPTIONAL ASSISTANT` | 不可取代 frozen copier、CodeX/Checker 或 Human Publish |
| **HGK / OROCHI_FACTORY_ORDER.v1** | `09_OROCHI_FACTORY_ORDER.md`, `10_AGENTIC_SWE_HARNESS.md` | Route-out、TaskSpec、evidence_return_pack | `REQUIRED LOCAL CONTRACT` | schema 型別／Owner 批准；不是 ChatGPT 自動外部 Runtime |

### 4.4 MCP 決策 Gate（跨六 OSS 仍保持 OFF）

PIPD Repo 歷史 `.hgk/artifacts/s2/MCP_MATERIALIZATION_DECISION.json` 記錄 `materialized:false`，`adapter_materialization_state: DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED`；這是歷史 frozen readback，不應假設後續永不改。要新增 MCP 必須存在 `live/authenticated/action-capable/dynamic-discovery` 其中一種經 Owner 驗證的高價值需求、Skills/CLI 不能滿足的反例、permission model、現有 Trace 閉合合格與真實 UAT 收益比較；否則本 ChangeSet `MCP=OFF`。OpenSpec/Spec Kit/GSD 相關 CLI/MCP 實作可作候選，但不因開源熱度就建立新的 PIPD MCP/認證/Runtime。

## 5. 可執行架構：事件、權限、依賴、降級及施工順序

### 5.1 四工作包與合法 Route-out

| Workstream | TaskSpec 界線 | Owner | 輸入 | 出口 / Required evidence |
|---|---|---|---|---|
| `UPG-P01` | Plugin 正式 root/manifest/8 Skills projection、圖示、Schema | PKG07 + Codex Maker | Frozen source ledger、Publisher metadata、owner derivation批准 | ZIP + source-map + Release receipt + raw tests；**未 Publ** |
| `UPG-P02` | README 兩主入口、Agent 單 Prompt、Free 單 MD | KP17/DX + PKG07 | Public state 與 Host capabilities, existing Web Mount | 真正生成文件 + first-run UAT / source map |
| `UPG-P03` | 防破壞、manifest、Skill、URI/ZIP、secret/license、Host effective load | PKG06/TQAEP + PKG08 Checker | 受控候選、負向集、獨立乾淨環境 | raw tests、defect ledger、no maker self-PASS |
| `UPG-P04` | 新版本候選 Release、Portal Publisher handoff | PKG08 Release Owner + Human Publisher | 完整驗證、實際 identity／授權 | tag/asset/digest/decision、Portal receipts/rollback runbook |

Execution stage 的 `OROCHI_FACTORY_ORDER.v1` schema mapping 見 §11；建議 Issue→Task→PR 對照：`UPG-P01` export, `UPG-P02` user-route, `UPG-P03` checkrun, `UPG-P04` publisher；**一 PR 可多子任務，但 Release/Portal 非 PR atomic step**。

### 5.2 事件矩陣：每一事件不可被下一步吞併

| Event | Emitter | Receiver | Required payload | Effect/Claim ceiling |
|---|---|---|---|---|
| `SOURCE_FROZEN` | Release Owner | Maker/Checker | repo+commit+tree+manifest SHA+baseline tag | `SOURCE_ONLY` |
| `DERIVATION_APPROVED` | Owner | Maker/Checker | Skill path, original hash, fields, ADR, approver | 只准改發行 copy |
| `PACKAGE_BUILT` | Maker | Checker | zip sha, source_map sha, vendor_schema sha, manifest SHA | `LOCAL_PACKAGER_PASS` |
| `CHECKRUN_COMPLETED` | Independent Checker | Release Owner | candidate hash + raw log + negatives + toolchain pin | `BUILD_PASS` 若各項合格 |
| `HOST_LOAD_OBSERVED` | Host Consumer | Checker | host/version/OS/install path/action log/discovery/negative | Host scoped qual |
| `PORTAL_DRAFT` | Human Publisher | Release Owner | real Portal draft id, ZIP hash | draft only |
| `PORTAL_SCAN_COMPLETE` | OpenAI Portal | Publisher | scan id, findings, timestamp | scan only |
| `REVIEW_APPROVED` | OpenAI review | Publisher | review receipt | approved != published |
| `PUBLIC_PUBLISHED` | Human Publisher | Consumers | directory URL/ID/version/time, approval receipt | public release scoped |
| `CONSUMER_VERIFIED` | Independent UAT | Release Gate | Plus/Free/Host effective load and negatives | Plugin UX verified; not S4 Full PASS |
| `DRIFT_FOUND` | DRIFT_PROBE | Owner | official before/after URL + affected test | TEMP_CLOSED until impact/ADR |
| `ROLLBACK` | Release Owner | Publisher/Consumers | known-good digest, revocation, cleanup proof | stop promotion |

### 5.3 RACI / Permission / SoD

| Actor | Source Repo read | Candidate write | Tests | Merge | Public Publish | 明確拒絕 |
|---|---|---|---|---|---|---|
| Authority/Product Owner | YES | owner approved scope only | ratifies applicable gates | via repo policy | strategy | fake receipts |
| HGK Orchestrator | YES | route-out instructions, not external runtime | observe | NO | NO | claim tool execution without receipt |
| Codex CLI Maker | Frozen worktree | restricted `UPG-P01/02/03` path | local synthetic/self-test | NO | NO | modify raw Skills, core, oracle |
| Independent Challenge Checker | immutable snapshot | isolated checker reports only | fresh negative/effective-load | NO | NO | fix then self sign |
| Release Owner | YES | controlled candidate/tag/signature | release readback | policy controlled | no default | same-tag unlogged replace |
| Verified Human Publisher | ZIP verify | Portal fields | portal scan/review | no default | authorized only | simulate user legal attestation |
| Plus/Free/Agent UAT consumer | public bytes only | own local scope | positive/negative/UX | NO | NO | claim other hosts tested |

**CI 權限**：GitHub Actions `contents:read`；不暴露 Publish secret；PR 不使用 `pull_request_target`；需 `CODEOWNERS` 保護 `src/`, `skills/`, Canonical, acceptance oracle 及 `.github/workflows/**`；required checks names/ruleset 由 Repo Owner 在 GitHub 內設定，尚未實際驗。`[GitHub secure use；OpenSSF]`

### 5.4 使用者與工程降級矩陣

| Situation | 唯一當前推薦操作 | Effect state | Stop/Fail condition |
|---|---|---|---|
| Plus + Public plugin 已發布且帳戶可見 | Directory→Install→Use | `PUBLIC_CONSUMER_VERIFIED` only with raw UAT | Developer/Region restriction→fallback |
| Plus + 未公開 / Portal 待審 | 單份 `PIPD_WEB_FALLBACK.md` 附件 | `DOC_MOUNT_ONLY` | 附件無法上傳→NOT_SUPPORTED |
| Free + Public Plugin 可安裝 | 同一 Directory（先真實 Free UAT） | Native scoped | 不可由 Plus infer Free |
| Free + Native unavailable + files 可上傳 | 單份 MD 且告知不同能力 | `DOC_MOUNT_ONLY` | size/truncation→FAIL |
| Free + 文件限制無法使用 | 宣告 NOT_SUPPORTED + 可閱讀 README 核心提示 | `NO_NATIVE_EFFECT` | 禁止假裝記住缺的 source |
| Hermes | project-local `.hermes/skills` 或 `.agents/skills`，trust + scan | session-scoped after first trust | scan dangerous/not loaded→FAIL |
| Codex Desktop GUI | 目標版本內 Skills/Plugins UI + project directory | GUI-scoped | 若 GUI 權限/入口不存在→TEMP_CLOSED |
| Codex CLI | verified local `.agents/skills` 或 verified plugin install | CLI-scoped | cached version stale / not discovered→FAIL |
| Claude Code | `.claude/skills` project-local native | scoped | symlink/mismatch/no discovery→FAIL |
| Third-party skills CLI | only if native blocked and allowed version pin | second-line | installing floating main/unreviewed `npx -y` forbidden |
| Prompt-only no Shell/FS permissions | show plan only; no write | NOT_INSTALLED | false completion -> FAIL |
| Bad Header requiring nonportable field shift | owner-approved derived copy + diff + negative UAT | DERIVED_NOT_EXACT | unauthorized mutation→FAIL |
| Public portal without verified publisher | retain BUILD_CANDIDATE only | `PUBLISH_HOLD` | fake approval→FAIL |
| Future MCP need | new ADR/version/policy gate | out-of-scope | no bundled MCP in this ZIP |

### 5.5 施工順序和回滾

1. Freeze read-only: Git commit/tree/asset bytes；Owner 核准 Issue、allowed/deny set、(若須)Frontmatter ADR；缺任一前提先 `TEMP_CLOSED`。
2. R1 mutation baseline replay（保留原 Audit 5 個 failing case）→修補範本合成測試 red→green；不以合成測試替代 source real UAT。
3. Builder in isolated fresh clean Git worktree；先安裝 hash-pinned dependencies，再 vendor Schema/Skills validation；缺依賴不觸發 secretful fallback。
4. Build 2x + exact SHA、ZIP extraction、source map + SPDX/license/secret scans；獨立 Checker 複跑、raw evidence 收集。
5. Build Free one-file fallback，限容量且不截斷；README 狀態由真實 published flag 切換；Agent SOP 與 Host UAT 個別完成。
6. PR code review/safety validation 後由 Release Owner 新建**新版本**預發行；不覆寫 preview.3，保留 previous known-good assets，於 release readback 綁 Digest。
7. Human Publisher 進 Portal draft→scan→review→Publish；不同帳戶 consumer UAT；若被拒退回 package build，保留 TT/CR，**不可**讓 Maker 冒名審核。
8. 回滾：未發布只清理 **本次派生** stage/目標 Host files；已公開由正式 Publisher 撤回/新版本修復，使用者重新安裝已核 known-good 版本，回報本次誤發布 bytes/affected host；不能宣稱已自動遠端卸載。

## 6. 全量修補缺陷條文：F01–F14、RP-P01–P08、防回歸條件

### 6.1 AUDIT Finding 全量追溯／修補證據判定（R1 的 Fail 不抹除）

| Finding | R1 AUDIT 證據 | R2 解法／正文定位 | 本輪證據/尚缺 |
|---|---|---|---|
| **F01 P0 Fake PNG** | AUDIT §4：R1 L398–401 只檢魔數 | §7.2 `validate_png` 使用 Pillow verify、尺寸/格式上限 | `test_F01_bad_png` 合成 PASS；真 Portal icon scan NOT_EXECUTED |
| **F02 P1 Manifest custom** | AUDIT §4：R1 L351–374 | §7.2 `validate_manifest` + frozen 官方 schema SHA、unknown reject | `test_F02_extra_manifest_property` 合成 PASS；vendor real schema/Portal 待驗 |
| **F03 P0 Invalid SKILL** | AUDIT §4：R1 L384–396 | §7.2 `read_skill` + explicit `project_skill`; §9 G04/G06 | `test_F03_invalid_skill_frontmatter` PASS；`skills-ref`/Host 未跑 |
| **F04 P0 Commit null** | AUDIT §4：R1 L405–409 | §7.1 freeze git HEAD/tree + §7.2 40hex/digest + release receipt | F04 missing/wrong, schema missing PASS；正式 ReleaseTuple external check 未做 |
| **F05 P0 Sidecar symlink** | AUDIT §4：R1 L409–410 sentinel overwritten | §7.2 secure owner-only output dir, `O_EXCL`, stage and atomic promote | `test_F05_symlink_target_untouched` PASS；OS race stress pending |
| F06 P1 Weak suite | AUDIT §4/§8 baseline 4 tests | §7.3 synthetic 14 tests + §9 host/negative matrix | 合成 14 + fallback 5；獨立 UAT NOT_EXECUTED |
| F07 Host commands absent | AUDIT §4/§5 A14–A18 | §8.2 all 4 Host adapters，real commands/scope/trust/uninstall matrix | 文檔完整；per-host tested commands NOT_EXECUTED |
| F08 Free fallback only text | AUDIT §5 A13 | §7.4 exact body generator, inventory, no truncation tests | 4 synthetic PASS；PIPD real release export NOT_EXECUTED |
| F09 Named six OSS shallow | AUDIT §3/§5 A19–A24 | §4.2 six independent technology decisions | 各 tool 具名、用途、風險、採用/不採用；production pin N/A |
| F10 Raw scan != semantic | AUDIT §5 A38/39 | §1 physical 102 + §12 atom-to-target A01–A42 | 42 upgrade atoms bounded trace；上游全部 atomic exhaustiveness NOT_PROVEN |
| F11 Publisher/Portal | AUDIT §5 A09/A10/A32 | §9 G09, §10 CR-HUMAN, §5 event/ownership | Portal account/identity/scan/review NOT_EXECUTED |
| F12 Replace same-tag asset | AUDIT §5 A26/A33 | §2 RCA + §9 new immutable version/readback | 新 release guard 編列；repo 尚未施工 |
| F13 Independent Checker | AUDIT §5 A28/§8 | §5.3 SoD、§9 evidence fields、Checker clean runner | local tests 是同 session，**not independent** |
| F14 original S4 full compiler | AUDIT §8 Out-of-scope | §0/§3 claim ceiling、§9 negative gated | 外部 S4 FULL PASS 繼續 NOT_GRANTED |

### 6.2 Repair Package 完整關閉矩陣

| RP | 計畫/責任 | 本文實質正文 | 必需驗收 | Candidate disposition |
|---|---|---|---|---|
| `RP-P01` | PKG07 exporter + source guard | §7.1–7.3 reuse+script/source tuple | F01..05, deterministic twice, release bytes | REPAIRED_IN_TEMPLATE, NOT_PRODUCTION |
| `RP-P02` | Manifest/frontmatter/real PNG | §7.2, §4.1 | Official Plugin schema, skills-ref, verified image, Owner ADR | PENDING_VENDOR_HOST |
| `RP-P03` | Free single MD + docs | §7.4, §8.1 | actual MD generated, max size, Plus/Free tests | SYNTHETIC_PASS, HOST_PENDING |
| `RP-P04` | host matrix | §8.2–8.4 | Hermes/Codex Desktop/Codex CLI/Claude independent UAT | DOCUMENTED, NOT_EXECUTED |
| `RP-P05` | QA/CI/security | §7.5, §9.2–9.4 | Secret/License/SBOM decision, negative/SoD | SCRIPT_TEST_ONLY |
| `RP-P06` | ReleaseTuple/rollback | §7.2 receipt, §9.5 | stale tag, same-tag change, publisher states | NEEDS_RELEASE_OWNER |
| `RP-P07` | named tech ADR | §4.2–4.4 | OpenSpec, Spec Kit, Matt, GSD, gstack, Superpowers, Vercel all decided | DESIGN_MAPPED |
| `RP-P08` | OROCHI/machine contracts | §§11/12/Appendix | JSON/TSV parse/schema binding/readback | MACHINE_BLOCKS_GENERATED |

### 6.3 Negative-first / Gate Calibration Failure defense

Gate 嚴格性分三層：**P0**（source/secret/permission/semantic false PASS）任何一例失敗即 FAIL；**P1**（某指定 host install/UX/rollback）對該 Host scope fail，不掩蓋；**P2**（非必要 benchmark/建議性 UX 指標）不阻斷已封閉的機器合格，但需記 CR。校準函數 `priority objective constraints` 為：`maximize verified task completion / minimize steps and time` **subject to** `zero unauthorized writes, exact provenance, no false PASS, no silent omitted source`;不能用平均 Clicks 更少犧牲安全。Regression baseline 保留 R1 F01–F05 先紅後綠、preview.2→preview.3 stale identity、8 Skills 行為/oracle；LLM judge 如需評價可讀性則執行 order-swapped、多 judge、golden anchors、反例對平衡，**Judge 不能覆寫 schema/trace/raw evidence**。HITL 由 Owner 作最終公開/責任簽核。`[12_EVAL_REGRESSION_LLM_JUDGE.md；AUDIT §§4/8]`

### 7.1 Frozen source manifest generator（`tools/freeze_public_plugin_source.py`）

**狀態**：`REFERENCE_IMPLEMENTATION / SYNTHETIC_TESTED / NOT_PRODUCTION_APPROVED`。施工方須與 Repo 既有工具比對後受控納入。

```python
#!/usr/bin/env python3
"""Owner/Checker-run frozen source ledger; never write inside source repository."""
import argparse, hashlib, json, os, re, stat, subprocess
from pathlib import Path
SKILLS=('pipd-route-intake','pipd-authority-source','pipd-profile-tailor',
        'pipd-pi-compile','pipd-pd-bind','pipd-execution-contract',
        'pipd-assurance-tqaep','pipd-package-project')
BASE={'SKILL.md','references/contract.md','references/examples.md',
      'schemas/input.schema.json','schemas/output.schema.json','tests/cases.yaml'}

def freeze(repo,version):
    repo=Path(repo).resolve(strict=True)
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?',version):
        raise ValueError('invalid semver')
    def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
    if git('status','--porcelain'):raise ValueError('source worktree dirty')
    names={p.name for p in (repo/'skills').iterdir() if p.name.startswith('pipd-')}
    if names!=set(SKILLS):raise ValueError('logical skill set mismatch')
    entries={}
    for skill in SKILLS:
        root=repo/'skills'/skill
        files={}
        for p in root.rglob('*'):
            m=p.lstat().st_mode
            if stat.S_ISDIR(m):continue
            if not stat.S_ISREG(m):raise ValueError(f'unsafe special member: {p}')
            rp=p.relative_to(root).as_posix()
            if any(part.startswith('.') for part in p.relative_to(root).parts):
                raise ValueError(f'hidden member: {p}')
            files[rp]=hashlib.sha256(p.read_bytes()).hexdigest()
        if not BASE <= files.keys():raise ValueError(f'missing required resources: {skill}')
        for k,h in files.items():entries[f'skills/{skill}/{k}']=h
    return {'repo':'shw097-team/PIPD-LS-SP','commit':git('rev-parse','HEAD'),
            'tree':git('rev-parse','HEAD^{tree}'),'plugin_version':version,
            'skills':sorted(SKILLS),'files':dict(sorted(entries.items()))}

if __name__=='__main__':
    pa=argparse.ArgumentParser()
    pa.add_argument('--repo',required=True)
    pa.add_argument('--version',required=True)
    args=pa.parse_args()
    print(json.dumps(freeze(args.repo,args.version),sort_keys=True,ensure_ascii=False,indent=2))
```

### 7.2 修補版受控 Public Skills-only Exporter（`tools/build_public_plugin.py`）

**狀態**：`REFERENCE_IMPLEMENTATION / SYNTHETIC_TESTED / NOT_PRODUCTION_APPROVED`。施工方須與 Repo 既有工具比對後受控納入。

```python
#!/usr/bin/env python3
"""PIPD public Skills-only projection candidate; no publish/write to source repo.
Contract: frozen manifest; secure output root; no source rewrites; official schema lock.
Runner needs jsonschema, PyYAML, Pillow, Git (versions/hash-locked by CI owner).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from io import BytesIO

import jsonschema
import yaml
from PIL import Image

SCHEMA_URI = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
SEMVER = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$')
HEX40 = re.compile(r'^[a-f0-9]{40}$')
HEX64 = re.compile(r'^[a-f0-9]{64}$')
SKILL_NAMES = frozenset(('pipd-route-intake','pipd-authority-source',
 'pipd-profile-tailor','pipd-pi-compile','pipd-pd-bind',
 'pipd-execution-contract','pipd-assurance-tqaep','pipd-package-project'))
ZTIME = (1980, 1, 1, 0, 0, 0)
REQUIRED_FILES = {'SKILL.md','references/contract.md','references/examples.md',
                  'schemas/input.schema.json','schemas/output.schema.json','tests/cases.yaml'}
FORBIDDEN_PLUGIN = {'mcp.json','.mcp.json','.app.json','hooks','scripts'}
ALLOWED_HEADER = {'name','description','license','compatibility','metadata','allowed-tools'}


def sha(data): return hashlib.sha256(data).hexdigest()
def canonical(o): return (json.dumps(o, sort_keys=True,ensure_ascii=False,
                                  separators=(',', ':'))+'\n').encode('utf-8')
def demand(cond, message):
    if not cond: raise ValueError(message)
def safe_file(path, expected_root):
    root = Path(expected_root).resolve(strict=True)
    p = Path(path)
    demand(p.is_relative_to(root), f'outside root: {p}')
    rel = p.relative_to(root)
    parent = root
    for part in rel.parts:
        parent = parent / part
        m = parent.lstat().st_mode
        demand(stat.S_ISREG(m) or stat.S_ISDIR(m), f'symlink/special refused: {parent}')
    demand(p.is_file() and stat.S_ISREG(p.lstat().st_mode),f'not a regular file: {p}')
    # Verify leaf again by fd; source must be a pinned, isolated worktree.
    flags=os.O_RDONLY | getattr(os,'O_NOFOLLOW',0)
    fd=os.open(p,flags)
    try:
        m=os.fstat(fd).st_mode
        demand(stat.S_ISREG(m),'unsafe input inode')
        with os.fdopen(fd,'rb',closefd=False) as f:
            data=f.read(16*1024*1024+1)
        demand(len(data)<=16*1024*1024,'oversized input file')
        return data
    finally: os.close(fd)


def read_skill(data, skill):
    text = data.decode('utf-8','strict')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n([\s\S]+)\Z', text, re.S)
    demand(bool(match), f'invalid frontmatter: {skill}')
    header = yaml.safe_load(match.group(1))
    demand(isinstance(header,dict), f'header not object: {skill}')
    demand(header.get('name') == skill, f'name mismatch: {skill}')
    desc = header.get('description')
    demand(isinstance(desc,str) and 1 <= len(desc) <= 1024, f'description: {skill}')
    demand(len(match.group(2).strip()) > 20, f'empty skill body: {skill}')
    demand(not (set(header)-ALLOWED_HEADER), f'nonportable frontmatter: {skill}')
    if 'metadata' in header:
        demand(isinstance(header['metadata'],dict) and all(isinstance(k,str) and isinstance(v,str)
             for k,v in header['metadata'].items()),f'bad metadata: {skill}')
    return header



def project_skill(data, skill, approval):
    """Mechanical release-only projection. Never alters upstream SKILL.md body."""
    t = data.decode('utf-8','strict')
    m = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n([\s\S]+)\Z',t,re.S)
    demand(bool(m), f'invalid frontmatter: {skill}')
    h = yaml.safe_load(m.group(1))
    demand(isinstance(h,dict) and h.get('name')==skill, f'name mismatch: {skill}')
    extras = set(h)-ALLOWED_HEADER
    if not extras:
        read_skill(data,skill)
        return data,'EXACT',[]
    demand(isinstance(approval,dict) and approval.get('ticket') and
           approval.get('approved_by') and approval.get('source_sha256')==sha(data) and
           set(approval.get('fields',[]))==extras,
           f'frontmatter derivation needs explicit owner approval: {skill}')
    meta = h.get('metadata') or {}
    demand(isinstance(meta,dict),'existing metadata must be map')
    meta = dict(meta)
    for field in sorted(extras):
        key='pipd.'+field
        demand(key not in meta,f'metadata collision: {key}')
        meta[key]=json.dumps(h.pop(field),ensure_ascii=False,separators=(',',':'),sort_keys=True)
    h['metadata']=meta
    new='---\n'+yaml.safe_dump(h,sort_keys=False,allow_unicode=True).rstrip()+'\n---\n'+m.group(2)
    result=new.encode('utf-8')
    read_skill(result,skill)
    demand(m.group(2)==result.decode('utf8').split('\n---\n',1)[1],
           f'body mismatch: {skill}')
    return result,'DERIVED_WITH_OWNER_APPROVAL',sorted(extras)

def validate_png(data, where):
    try:
        with Image.open(BytesIO(data)) as pic:
            demand(pic.format == 'PNG', f'not PNG: {where}')
            w,h = pic.size
            demand(64 <= w <= 4096 and 64 <= h <= 4096, f'bad dimensions: {where}')
            pic.verify()
    except Exception as exc:
        raise ValueError(f'bad PNG {where}: {exc}') from exc


def validate_manifest(data, schema_bytes):
    schema = json.loads(schema_bytes)
    demand(schema.get('$id') == SCHEMA_URI,'unexpected vendor schema id')
    jsonschema.Draft202012Validator.check_schema(schema)
    m = json.loads(data)
    jsonschema.Draft202012Validator(schema).validate(m)
    demand(m['$schema'] == SCHEMA_URI, 'manifest URI')
    demand(m['name'] == 'pipd-ls-sp','plugin identity')
    demand(isinstance(m.get('version'),str) and SEMVER.fullmatch(m['version']),'semver')
    demand(m.get('license') == 'Apache-2.0','license not confirmed')
    ext = m.get('extensions',{}).get('com.openai',{})
    demand(isinstance(ext,dict) and not (set(ext) & {'apps','hooks','mcpServers'}),'unwanted tools')
    interface = ext.get('interface',{})
    demand(isinstance(interface,dict),'missing interface')
    demand(isinstance(interface.get('developerName'),str) and
           interface['developerName'].strip() and not re.search(r'<|TO_VERIFY|PLACEHOLDER',interface['developerName']),
           'publisher identity pending')
    demand(bool(interface.get('logo')) and bool(interface.get('composerIcon')),
           'public icons not configured')
    return m, interface


def build(repo, frozen_file, manifest_file, schema_file, assets_root, output_parent):
    repo = Path(repo).resolve(strict=True)
    frozen = json.loads(Path(frozen_file).read_text(encoding='utf-8'))
    manifest_data = Path(manifest_file).read_bytes()
    schema_data = Path(schema_file).read_bytes()
    demand(isinstance(frozen.get('official_plugin_schema_sha256'),str) and
           frozen['official_plugin_schema_sha256'] == sha(schema_data),
           'official schema digest must be pinned in source ledger')
    demand(isinstance(frozen.get('expected_plugin_manifest_sha256'),str) and
           frozen['expected_plugin_manifest_sha256'] == sha(manifest_data),
           'plugin manifest digest must be pinned in source ledger')
    manifest,ui = validate_manifest(manifest_data,schema_data)
    demand(frozen.get('repo') == 'shw097-team/PIPD-LS-SP','unexpected repo')
    demand(isinstance(frozen.get('commit'),str) and HEX40.fullmatch(frozen['commit']),'commit must be 40hex')
    demand(isinstance(frozen.get('tree'),str) and HEX40.fullmatch(frozen['tree']),'tree must be 40hex')
    demand(frozen.get('plugin_version') == manifest['version'],'version mismatch')
    def git(*args):
        return subprocess.check_output(['git','-C',str(repo),*args], text=True).strip()
    demand(git('rev-parse','HEAD') == frozen['commit'], 'source commit mismatch')
    demand(git('rev-parse','HEAD^{tree}') == frozen['tree'], 'source tree mismatch')
    demand(git('status','--porcelain') == '', 'source worktree dirty')
    srcfiles = frozen.get('files')
    demand(isinstance(srcfiles,dict) and srcfiles,'source file ledger missing')
    demand(set(frozen.get('skills',[])) == SKILL_NAMES,'skill exact set mismatch')
    manifest_rows = {}
    demand(not (set(x.name for x in (repo/'skills').iterdir() if x.is_dir()
                and x.name.startswith('pipd-'))-SKILL_NAMES),'extra logical skill')
    for skill in sorted(SKILL_NAMES):
        relset = {'/'.join(PurePosixPath(p).parts[2:]) for p in srcfiles
                  if p.startswith(f'skills/{skill}/')}
        demand(REQUIRED_FILES <= relset, f'skill missing resources: {skill}')
    entries = {'pipd-ls-sp/plugin.json':manifest_data}
    for rel,expected in sorted(srcfiles.items()):
        demand(isinstance(rel,str) and rel.startswith('skills/'),f'bad source path: {rel}')
        pp = PurePosixPath(rel)
        demand('..' not in pp.parts and pp.parts[1] in SKILL_NAMES,f'bad skill path: {rel}')
        src = safe_file(repo/rel, repo)
        demand(isinstance(expected,str) and HEX64.fullmatch(expected) and sha(src)==expected,
               f'identity mismatch: {rel}')
        if rel.endswith('/SKILL.md'):
            dst_data,mode,moved=project_skill(src,pp.parts[1],
                                           frozen.get('derivations',{}).get(rel))
        else:
            dst_data,mode,moved=src,'EXACT',[]
        dest = 'pipd-ls-sp/'+rel
        entries[dest] = dst_data
        manifest_rows[rel] = {'destination':dest,'source_sha256':expected,
                              'destination_sha256':sha(dst_data),'mode':mode,
                              'moved_header_fields':moved}
    # Full source set check, not merely a fixed count or wildcard approximation.
    observed = {}
    for skill in sorted(SKILL_NAMES):
        for p in (repo/'skills'/skill).rglob('*'):
            if p.is_file() or p.is_symlink():
                key = p.relative_to(repo).as_posix()
                observed[key] = sha(safe_file(p,repo))
    demand(observed == srcfiles, 'source set changed: missing or extra resource')
    root = Path(assets_root).resolve(strict=True)
    for field in ('logo','composerIcon'):
        ref = ui[field]
        demand(isinstance(ref,str) and re.fullmatch(r'\./assets/[\w.-]+\.png',ref),
               f'bad icon path: {field}')
        data = safe_file(root/ref.removeprefix('./'),root)
        validate_png(data,ref)
        entries['pipd-ls-sp/'+ref.removeprefix('./')]=data
    # Fail-close if unreviewed files/assets/exec surfaces appear.
    demand(not any(x in Path(z).parts for z in entries for x in FORBIDDEN_PLUGIN),
           'forbidden bundle surface')
    source_map = {'schema':'PIPD-S4-SOURCE-MAP.v2','source_repo':frozen['repo'],
                  'source_commit':frozen['commit'],'source_tree':frozen['tree'],
                  'plugin_version':manifest['version'], 'files':manifest_rows}
    source_map_data = canonical(source_map)
    output = Path(output_parent).resolve(strict=True)
    demand(output != repo and not output.is_relative_to(repo) and
           not repo.is_relative_to(output),'output/source overlap forbidden')
    demand(stat.S_ISDIR(output.lstat().st_mode) and not output.is_symlink(),
           'output must be real directory')
    demand(output.stat().st_uid == os.getuid() and not (output.stat().st_mode & 0o022),
           'output must be owned and not group/world writable')
    final_dir = output / ('pipd-ls-sp-'+manifest['version'])
    demand(not final_dir.exists() and not final_dir.is_symlink(),'release dir already exists')
    stage = Path(tempfile.mkdtemp(dir=output,prefix='.staging-',suffix='.pending'))
    try:
        zip_file = stage/'pipd-ls-sp.zip'
        with zipfile.ZipFile(zip_file,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,data in sorted(entries.items()):
                info=zipfile.ZipInfo(name,date_time=ZTIME)
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=(0o100644 << 16)
                z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        with zipfile.ZipFile(zip_file) as z:
            demand(z.testzip() is None,'archive CRC')
            demand(set(z.namelist()) == set(entries),'archive member set')
            demand(all(z.read(k)==v for k,v in entries.items()), 'zip readback mismatch')
        receipt = {'schema':'PIPD-S4-PLUGIN-RECEIPT.v2',
          'source_repo':frozen['repo'],'source_commit':frozen['commit'],
          'source_tree':frozen['tree'],'source_manifest_sha256':sha(canonical(frozen)),
          'plugin_version':manifest['version'],'plugin_manifest_sha256':sha(manifest_data),
          'official_schema_sha256':sha(schema_data),
          'plugin_zip_sha256':sha(zip_file.read_bytes()),
          'source_map_sha256':sha(source_map_data),
          'logical_skills':len(SKILL_NAMES),'source_files':len(srcfiles),
          'claim_ceiling':'LOCAL_PACKAGER_PASS_ONLY',
          'official_portal_verification':'NOT_EXECUTED',
          'host_evidence':'NOT_EXECUTED','public_published':False}
        (stage/'SOURCE_TO_PLUGIN_MAPPING.json').write_bytes(source_map_data)
        (stage/'RELEASE_RECEIPT.json').write_bytes(canonical(receipt))
        (stage/'SHA256SUMS').write_bytes(
            (receipt['plugin_zip_sha256']+'  pipd-ls-sp.zip\n').encode())
        for p in stage.iterdir():
            with p.open('rb') as f: os.fsync(f.fileno())
        # Directory atomic promotion under exclusive, owner-private output dir.
        lock = output/'.plugin-publish.lock'
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,'O_NOFOLLOW',0),0o600)
        try:
            demand(not final_dir.exists() and not final_dir.is_symlink(),'release destination raced')
            stage.rename(final_dir)
        finally:
            os.close(fd)
            lock.unlink()
        return receipt
    finally:
        if stage.exists(): shutil.rmtree(stage)


def main():
    ap=argparse.ArgumentParser()
    for arg in ('repo','frozen','plugin-json','plugin-schema','assets-root','output-root'):
        ap.add_argument('--'+arg,required=True)
    a=ap.parse_args()
    args=[getattr(a,x.replace('-','_')) for x in
          ('repo','frozen','plugin-json','plugin-schema','assets-root','output-root')]
    try:
        print(json.dumps(build(*args),ensure_ascii=False,sort_keys=True))
        return 0
    except Exception as exc:
        print(f'BUILD_DENIED: {type(exc).__name__}: {exc}',file=__import__('sys').stderr)
        return 2
if __name__ == '__main__': raise SystemExit(main())
```

### 7.3 14 項合成負向／成功／確定性回歸（`tests/test_public_plugin_packaging.py`）

**狀態**：`REFERENCE_IMPLEMENTATION / SYNTHETIC_TESTED / NOT_PRODUCTION_APPROVED`。施工方須與 Repo 既有工具比對後受控納入。

```python
"""Local synthetic red-to-green mutation suite. Does not constitute Portal or Host UAT."""
import hashlib, json, os, subprocess, tempfile, unittest
from pathlib import Path
from PIL import Image
import jsonschema
from build_public_plugin import build, SKILL_NAMES, SCHEMA_URI, canonical
from freeze_public_plugin_source import freeze

def git(cwd,*args):
    subprocess.run(['git','-C',str(cwd),*args],check=True,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.repo=self.root/'repo';self.repo.mkdir()
        git(self.repo,'init','-q')
        git(self.repo,'config','user.email','synthetic@example.test')
        git(self.repo,'config','user.name','Synthetic Tests')
        for skill in SKILL_NAMES:
            d=self.repo/'skills'/skill
            for rel in ('references/contract.md','references/examples.md','schemas/input.schema.json',
                        'schemas/output.schema.json','tests/cases.yaml'):
                p=d/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('example\n',encoding='utf8')
            (d/'SKILL.md').write_text(f'---\nname: {skill}\ndescription: Use for source-bound PIPD workflow.\n---\n# Workflow\nRefuse unauthorized release and missing source.\n',encoding='utf8')
        self.assets=self.root/'assets'; (self.assets/'assets').mkdir(parents=True)
        for name in ('logo.png','composer.png'):
            Image.new('RGBA',(128,128),(0,0,0,0)).save(self.assets/'assets'/name)
        self.schema=self.root/'plugin_schema.json'
        self.schema.write_text(json.dumps({'$id':SCHEMA_URI,'$schema':'https://json-schema.org/draft/2020-12/schema',
          'type':'object','required':['$schema','name','version'],
          'additionalProperties':False,
          'properties':{'$schema':{'const':SCHEMA_URI},'name':{'type':'string'},
                        'version':{'type':'string'},'description':{'type':'string'},
                        'license':{'type':'string'},'extensions':{'type':'object'}}}),encoding='utf8')
        self.plug=self.root/'plugin.json'
        self.meta={'$schema':SCHEMA_URI,'name':'pipd-ls-sp','version':'0.2.0-rc.1',
           'description':'Synthetic PIPD plugin fixture','license':'Apache-2.0',
           'extensions':{'com.openai':{'interface':{
             'developerName':'Example Team','logo':'./assets/logo.png',
             'composerIcon':'./assets/composer.png'}}}}
        self.plug.write_bytes(canonical(self.meta))
        self.out=self.root/'isolated_output'; self.out.mkdir(mode=0o700)
        self.pin()

    def pin(self):
        git(self.repo,'add','skills')
        git(self.repo,'commit','-qm','synthetic fixture')
        self.pinfile=self.root/'source_pin.json'
        frozen = freeze(self.repo,'0.2.0-rc.1')
        frozen['official_plugin_schema_sha256']=hashlib.sha256(self.schema.read_bytes()).hexdigest()
        frozen['expected_plugin_manifest_sha256']=hashlib.sha256(self.plug.read_bytes()).hexdigest()
        self.pinfile.write_bytes(canonical(frozen))

    def invoke(self, out=None):
        return build(self.repo,self.pinfile,self.plug,self.schema,self.assets,out or self.out)

    def test_baseline_reproducible(self):
        a=self.invoke()
        other=self.root/'other_out';other.mkdir(mode=0o700)
        b=self.invoke(other)
        self.assertEqual(a['plugin_zip_sha256'],b['plugin_zip_sha256'])
        self.assertEqual(a['source_files'],48)
        self.assertTrue((self.out/'pipd-ls-sp-0.2.0-rc.1'/'RELEASE_RECEIPT.json').exists())

    def test_F01_bad_png(self):
        (self.assets/'assets'/'logo.png').write_bytes(b'\x89PNG\r\n\x1a\nNOT_A_REAL_PNG')
        with self.assertRaisesRegex(ValueError,'bad PNG'):self.invoke()
        self.assertFalse(list(self.out.glob('pipd-*')))

    def test_F02_extra_manifest_property(self):
        self.meta['custom']='unreviewed';self.plug.write_bytes(canonical(self.meta))
        p=json.loads(self.pinfile.read_text())
        p['expected_plugin_manifest_sha256']=hashlib.sha256(self.plug.read_bytes()).hexdigest()
        self.pinfile.write_bytes(canonical(p))
        with self.assertRaises(jsonschema.exceptions.ValidationError):self.invoke()

    def test_F03_invalid_skill_frontmatter(self):
        p=self.repo/'skills'/'pipd-route-intake'/'SKILL.md'
        p.write_text('NOT A VALID AGENT SKILL FRONTMATTER')
        self.pin()
        with self.assertRaisesRegex(ValueError,'invalid frontmatter'):self.invoke()

    def test_F04_missing_commit_fails(self):
        j=json.loads(self.pinfile.read_text());j['commit']=None
        self.pinfile.write_bytes(canonical(j))
        with self.assertRaisesRegex(ValueError,'commit must be 40hex'):self.invoke()

    def test_unpinned_schema_denied(self):
        j=json.loads(self.pinfile.read_text()); j['official_plugin_schema_sha256']=None
        self.pinfile.write_bytes(canonical(j))
        with self.assertRaisesRegex(ValueError,'official schema digest'):self.invoke()

    def test_F04_wrong_commit_fails(self):
        j=json.loads(self.pinfile.read_text());j['commit']='a'*40
        self.pinfile.write_bytes(canonical(j))
        with self.assertRaisesRegex(ValueError,'source commit mismatch'):self.invoke()

    def test_F05_symlink_target_untouched(self):
        sentinel=self.root/'sentinel';sentinel.write_bytes(b'DO_NOT_TOUCH')
        (self.out/'pipd-ls-sp-0.2.0-rc.1').symlink_to(sentinel)
        with self.assertRaisesRegex(ValueError,'release dir already exists'):self.invoke()
        self.assertEqual(sentinel.read_bytes(),b'DO_NOT_TOUCH')

    def test_F06_extra_file_in_source(self):
        p=self.repo/'skills'/'pipd-route-intake'/'references'/'unexpected.md'
        p.write_text('unexpected');self.pin()
        j=json.loads(self.pinfile.read_text());j['files'].pop('skills/pipd-route-intake/references/unexpected.md')
        self.pinfile.write_bytes(canonical(j))
        with self.assertRaisesRegex(ValueError,'source set changed'):self.invoke()

    def test_F06_source_symlink_denied(self):
        external=self.root/'exfil';external.write_bytes(b'NOT_TRUSTED')
        p=self.repo/'skills'/'pipd-route-intake'/'references'/'linked.md'
        p.symlink_to(external)
        with self.assertRaisesRegex(ValueError,'source worktree dirty'):self.invoke()

    def test_negative_bad_metadata_name(self):
        p=self.repo/'skills'/'pipd-route-intake'/'SKILL.md'
        p.write_text(p.read_text().replace('name: pipd-route-intake','name: wrong-name'))
        self.pin()
        with self.assertRaisesRegex(ValueError,'name mismatch'):self.invoke()

    def test_empty_publisher_denied(self):
        self.meta['extensions']['com.openai']['interface']['developerName']='PLACEHOLDER'
        self.plug.write_bytes(canonical(self.meta))
        pin=json.loads(self.pinfile.read_text())
        pin['expected_plugin_manifest_sha256']=hashlib.sha256(self.plug.read_bytes()).hexdigest()
        self.pinfile.write_bytes(canonical(pin))
        with self.assertRaisesRegex(ValueError,'publisher identity pending'):self.invoke()

    def test_source_overlap_denied(self):
        # Calling freeze first then attempting inside source is blocked before publication.
        with self.assertRaises(ValueError):self.invoke(self.repo)

    def test_derived_frontmatter_needs_explicit_approval(self):
        p=self.repo/'skills'/'pipd-route-intake'/'SKILL.md'
        p.write_text(p.read_text().replace('description:', 'version: 1\ndescription:'))
        self.pin()
        with self.assertRaisesRegex(ValueError,'explicit owner approval'):self.invoke()
        pin=json.loads(self.pinfile.read_text()); h=pin['files']['skills/pipd-route-intake/SKILL.md']
        pin['derivations']={'skills/pipd-route-intake/SKILL.md':{
            'ticket':'ADR-TEST-001','approved_by':'Fixture Owner',
            'source_sha256':h,'fields':['version']}}
        self.pinfile.write_bytes(canonical(pin))
        receipt=self.invoke()
        result=json.loads((self.out/'pipd-ls-sp-0.2.0-rc.1'/'SOURCE_TO_PLUGIN_MAPPING.json').read_text())
        row=result['files']['skills/pipd-route-intake/SKILL.md']
        self.assertEqual(row['mode'],'DERIVED_WITH_OWNER_APPROVAL')
        self.assertNotEqual(row['source_sha256'],row['destination_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)
```

### 7.4 Free 單檔投影產生器（`tools/build_web_fallback.py`）

**狀態**：`REFERENCE_IMPLEMENTATION / SYNTHETIC_TESTED / NOT_PRODUCTION_APPROVED`。施工方須與 Repo 既有工具比對後受控納入。

```python
#!/usr/bin/env python3
"""Build ONE bounded, byte-complete Web document from a frozen Web Mount source.
Not a Native Plugin, does not claim full S4 execution or source semantic completeness.
"""
import argparse, hashlib, os, re, stat, json
from pathlib import Path

def die(msg):raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()

def build(mount, output, release, commit, max_bytes=1048576):
    root=Path(mount).resolve(strict=True)
    if not re.fullmatch(r'[a-f0-9]{40}',commit): die('release source commit not bound')
    if not release or '<' in release or '>' in release:die('release not resolved')
    manifest=root/'MANIFEST.sha256'
    if manifest.is_symlink():die('symlink manifest')
    entries={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        m=re.fullmatch(r'([a-f0-9]{64})\s{2}(.+)',line)
        if not m:die('bad manifest line')
        hash_expected, rel=m.groups()
        p=root/rel
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(root):
            die('unsafe document reference')
        if p.suffix.lower() not in ('.md','.txt'):die('unsupported document type')
        data=p.read_bytes()
        if sha(data)!=hash_expected:die('source digest mismatch')
        if rel in entries:die('duplicate document')
        entries[rel]=(data,hash_expected)
    actual={p.relative_to(root).as_posix() for p in root.rglob('*')
            if p.is_file() and p.name!='MANIFEST.sha256'}
    if set(entries)!=actual:die('missing or unexpected mount files')
    if not entries:die('empty mount')
    for rel,(data,h) in entries.items():
        txt=data.decode('utf-8','strict')
        if release not in txt or commit not in txt:
            die(f'release identity mismatch within source document: {rel}')
    head=['# PIPD-LS-SP S4 — Web single-document fallback',
          '',f'Source release: `{release}`',f'Source commit: `{commit}`',
          f'Mount source manifest SHA-256: `{sha(manifest.read_bytes())}`','',
          '**DOC_MOUNT_ONLY**. This is a source-stamped, non-executable projection; not a',
          'Public Plugin, Python CLI, external checker, S4 PASS, or release approval.','',
          'Every embedded section is reproduced from the release mount verbatim, never summarized.',
          'If any required source is absent or the output is too large, export refuses.',
          '', '## Embedded document inventory','',
          '| Source member | SHA-256 |','|---|---|']
    for rel,(_,h) in sorted(entries.items()):head.append(f'| `{rel}` | `{h}` |')
    pieces=['\n'.join(head)+'\n']
    for rel,(data,h) in sorted(entries.items()):
        text=data.decode('utf-8','strict')
        pieces += ['\n---\n',f'\n## BEGIN SOURCE: `{rel}` — SHA256 `{h}`\n\n',
                   text,'\n',f'\n## END SOURCE: `{rel}`\n']
    result=''.join(pieces).encode('utf-8')
    if len(result)>max_bytes:die('document exceeds approved max bytes; no truncation')
    dest=Path(output).absolute()
    if dest.is_symlink() or dest.exists():die('existing output refused')
    parent=dest.parent.resolve(strict=True)
    if parent.is_relative_to(root) or root.is_relative_to(parent):die('output overlaps source')
    if parent.stat().st_mode & 0o022:die('output parent not private')
    flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0)
    fd=os.open(dest,flags,0o600)
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(result);f.flush();os.fsync(f.fileno())
    except BaseException:
        dest.unlink(missing_ok=True)
        raise
    return {'output_sha256':sha(result),'bytes':len(result),
            'members':len(entries),'claim_ceiling':'DOC_MOUNT_ONLY'}

if __name__=='__main__':
    pa=argparse.ArgumentParser()
    pa.add_argument('--mount',required=True);pa.add_argument('--out',required=True)
    pa.add_argument('--release',required=True);pa.add_argument('--commit',required=True)
    pa.add_argument('--max-bytes',type=int,default=1048576)
    a=pa.parse_args()
    try:print(json.dumps(build(a.mount,a.out,a.release,a.commit,a.max_bytes)))
    except Exception as ex:
        print(f'FALLBACK_EXPORT_DENIED: {ex}',file=__import__('sys').stderr)
        raise SystemExit(2)
```

### 7.4.1 單檔備援 5 個反例/正常測試（`tests/test_web_fallback.py`）

**狀態**：`REFERENCE_IMPLEMENTATION / SYNTHETIC_TESTED / NOT_PRODUCTION_APPROVED`。施工方須與 Repo 既有工具比對後受控納入。

```python
import hashlib,tempfile,unittest
from pathlib import Path
from build_web_fallback import build

class FallbackTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name);self.mount=root/'mount';self.mount.mkdir()
        self.out=root/'out';self.out.mkdir(mode=0o700)
        self.text=(b'# PIPD example\nDO NOT APPROVE release.\nRelease v-fixture tag commit '+b'a'*40+b'\n')
        (self.mount/'SKILL.md').write_bytes(self.text)
        digest=hashlib.sha256(self.text).hexdigest()
        (self.mount/'MANIFEST.sha256').write_text(f'{digest}  SKILL.md\n')
        self.commit='a'*40
    def invoke(self,maxb=1048576):
        return build(self.mount,self.out/'PIPD_WEB_FALLBACK.md','v-fixture',self.commit,maxb)
    def test_exact_projection(self):
        r=self.invoke()
        self.assertEqual(r['members'],1)
        data=(self.out/'PIPD_WEB_FALLBACK.md').read_bytes()
        self.assertIn(self.text,data)
        self.assertIn(b'DOC_MOUNT_ONLY',data)
    def test_stale_release_stamp(self):
        data=self.text.replace(b'a'*40,b'b'*40)
        (self.mount/'SKILL.md').write_bytes(data)
        (self.mount/'MANIFEST.sha256').write_text(hashlib.sha256(data).hexdigest()+'  SKILL.md\n')
        with self.assertRaisesRegex(ValueError,'release identity mismatch'):self.invoke()

    def test_no_truncation(self):
        with self.assertRaisesRegex(ValueError,'no truncation'):self.invoke(10)
        self.assertFalse((self.out/'PIPD_WEB_FALLBACK.md').exists())
    def test_bad_sha(self):
        (self.mount/'SKILL.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'digest mismatch'):self.invoke()
    def test_symlink(self):
        extra=self.out/'sentinel';extra.write_text('secret')
        (self.out/'PIPD_WEB_FALLBACK.md').symlink_to(extra)
        with self.assertRaisesRegex(ValueError,'output refused'):self.invoke()
        self.assertEqual(extra.read_text(),'secret')
if __name__=='__main__':unittest.main(verbosity=2)
```

### 7.5 官方 Plugin Manifest、Vendor Schema、正式發布 metadata 交接

下述 JSON 為**欄位級示例**，明確使用候選 `0.2.0-rc.1` 只是 synthetic fixture 的數字，**不代表真實 Plugin 版本/Publisher/Assets 已通過**。正式發行配置須由 Owner 填真實資料，凍結 SHA 並經官方 Schema + Portal：

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "pipd-ls-sp",
  "version": "0.2.0-rc.1",
  "description": "Source-bound PIPD pre-implementation workflows. No execution or S4 PASS is implied.",
  "repository": "https://github.com/shw097-team/PIPD-LS-SP",
  "license": "Apache-2.0",
  "extensions": {
    "com.openai": {
      "interface": {
        "displayName": "PIPD-LS-SP",
        "shortDescription": "Source-bound PI/PD workflows",
        "longDescription": "Eight source-bound planning and handoff skills. No runtime execution or independent S4 acceptance.",
        "developerName": "OWNER_VERIFIED_REAL_PUBLISHER_REQUIRED",
        "category": "Productivity",
        "logo": "./assets/logo.png",
        "composerIcon": "./assets/composer.png",
        "defaultPrompt": ["Plan a source-bound PIPD intake.", "Check PIPD ECP evidence requirements."]
      }
    }
  }
}
```

**不可直接提交以上 placeholder**。來源採 Apache-2.0 是 Repo README 當前聲明；資產商標/隱私/政策是新的公發責任，仍須 Publisher 核准。正式 manifest 若加入官方定義 extension，必由該時官方 Validator 正確承認；任意 `custom` 一律 schema deny。不要將 `mcp.json/.app.json/hooks/` 夾帶在 Skills-only Public Plugin。`[OpenAI packaging/submission; AUDIT F02/A10]`

**必需的 release 檔組**：`frozen_source.json`（源 commit/tree+全部 files hashes+approved derivations+官方 schema SHA+manifest SHA）, `SOURCE_TO_PLUGIN_MAPPING.json`（逐 source/destination bytes&derive）, `RELEASE_RECEIPT.json`（hashes+claim ceiling）, `SHA256SUMS`（ZIP hash）, plugin ZIP；Owner Release 一律外部再核確切 Git tag/asset SHA。Source manifest 包含官方 schema hash、Plugin manifest hash，禁止 `null` 或只填公開網址。若沒有 Publisher 核准 `derivations`，原 PIPD 自訂 Frontmatter 會在生成器 **正確 Fail-Closed**；這不是可跳過的錯誤。正式生產時如要解決，對每個 Skill 各提供 `approved_by/ticket/source_sha256/fields`，保留 body 和 metadata 字串映射。這種派生是相容性適配，不可產生新的第九技能。

### 7.6 操作順序（需要專案 Owner 審核，非直接執行委託）

```bash
# 僅示意在 HGK/Codex 的授權隔離工作區，禁止直接對 main 執行寫入
# 1) 切至由 Owner 批准的 frozen candidate commit，確認 git status --porcelain 為空
python tools/freeze_public_plugin_source.py   --repo "$FROZEN_REPO" --version "$OWNER_APPROVED_PLUGIN_SEMVER"   > "$SECURE_OUT/frozen_source.json"
# 2) 以 Owner 控制的 metadata 加入 official_plugin_schema_sha256、
#    expected_plugin_manifest_sha256、逐 Skill 的 derivations approval；
#    對其 Schema/Owner 簽核核實後，禁止 Maker 默默補 approval。
python tools/build_public_plugin.py   --repo "$FROZEN_REPO"   --frozen "$SECURE_OUT/frozen_source.json"   --plugin-json "$PROJECT_ROOT/packaging/public-plugin/plugin.json"   --plugin-schema "$PROJECT_ROOT/packaging/public-plugin/plugin.schema.json"   --assets-root "$PROJECT_ROOT/packaging/public-plugin"   --output-root "$SECURE_OUT/published_candidates"
# 3) 另跑 vendor skills-ref validate、官方 Portal scan、secret/license/SBOM policy Gate。
# 4) independent checker 在另一乾淨環境重演；不可因 stdout 0 就公開。
```

**上述 Shell 為具有已核准版本、來源目錄與封裝資料時的執行順序；所有環境變數仍須由實際 Executor 綁定**。若 `SECURE_OUT` 或 plugin schema lock 不存在就停；不能靠自行創建可寫 global 路徑繞過授權。合成 14/14 包裝測試使用*簡化 synthetic vendor schema*，並非把真正的官方 schema 校驗偷換成同一結果，最終 Vendor 1.0.0 schema 要另行 lock/check。`[AUDIT §§4,7.1]`

### 7.7 GitHub Actions Read-only CI workflow（`public-plugin-verify.yml`）

此 Workflow 只跑**合成回歸與 frozen/source 檔案静態檢查**；PR 未取得 Verified Publisher metadata／外部 Portals 時不得宣稱 Public PASS。官方例子的 checkout Commit 已透過 GitHub API 在本輪核為 v4.2.2→`11bd71901bbe5b1630ceea73d27597364c9af683`；正式運作前 Lock 檔必由 Owner 產出經核 SHA256 的 PyYAML/jsonschema/Pillow/Security deps。若 Lock/依賴不存在，workflow **失敗**，不是降級讓測試綠。

```yaml
name: public-plugin-static-and-synthetic
on:
  pull_request:
    paths:
      - 'tools/build_public_plugin.py'
      - 'tools/freeze_public_plugin_source.py'
      - 'tools/build_web_fallback.py'
      - 'tests/test_public_plugin_packaging.py'
      - 'tests/test_web_fallback.py'
      - 'packaging/public-plugin/**'
      - 'docs/install/**'
      - 'README.md'
      - '.github/workflows/public-plugin-verify.yml'
  workflow_dispatch:
permissions:
  contents: read
jobs:
  check-synthetic:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          persist-credentials: false
          fetch-depth: 0
      - name: locked-dependencies-only
        run: python -m pip install --require-hashes -r packaging/public-plugin/requirements.lock
      - name: forbidden-core-diff-for-upgrade
        shell: bash
        run: |
          git diff --name-only "origin/${GITHUB_BASE_REF}...HEAD" > "${RUNNER_TEMP}/changed_paths.txt"
          if grep -E '^(skills/|src/|schemas/|PIPD_LS_|PIPD-LS-SP_PIPD-PKG-|PIPD-LS-SP_skeleton\.md)' "${RUNNER_TEMP}/changed_paths.txt"; then
            echo 'UPGRADE_WRITE_SET_VIOLATION' >&2
            exit 1
          fi
      - name: python-compilation
        run: |
          python -m py_compile tools/build_public_plugin.py tools/freeze_public_plugin_source.py tools/build_web_fallback.py
      - name: regression-F01-through-F06-and-fallback
        env:
          PYTHONPATH: tools
        run: |
          python -m unittest -v tests.test_public_plugin_packaging tests.test_web_fallback
      - name: forbidden-privileged-execution-check
        run: |
          ! grep -R -n 'pull_request_target\|permissions: write-all' .github/workflows/public-plugin-verify.yml
      - name: evidence-boundary
        run: |
          echo 'SYNTHETIC_CHECK_ONLY; HOST_UAT=NOT_EXECUTED; PUBLIC_PUBLISH=NOT_EXECUTED'
```

**重要**：`tests.*` 必須是 Python 可 import modules（例如建置空 `tests/__init__.py`，或改 `unittest discover -s tests -p 'test_*plugin*.py'`）；需由施工者在 Repo 完成 `actionlint`/YAML parser、Protected Paths Diff、checkout actor 權限及 Dependency Pin 的**真實** PR 工作流驗證。`workflow_dispatch` 只手動觸發 read-only CI，不發行；Repo 若 `required checks` 未實際配置，Gates 結果 `TEMP_CLOSED`。所有掃描結果保留 raw log、Tool/Version/runner SHA；如需 gitleaks/Scorecard action 優先 Pin 完整 Git SHA，不得將 `latest` 視為安全。

### 7.8 前版工程程式與本 R2 的修補關係

原 R1 包含約 129 行 exporter、約 58 行 unittest 與一組形式 Workflow；此次 R2 用更嚴格、實際執行過 synthetic fixture 的參考程式**取代**它們。保留 R1 的架構、Scope、四包、十 Gate 和證據輸出語義；被替換的 Fail-open 原碼不再當作推薦施工內容。實施者若發現現有 Repo `build_mount_pack.py` 本身可安全重用部分操作，應提交最小 Diff 與 ADR，拒絕為了照搬 R2 範本而引入多餘抽象。不可因 R2 的 code lines 較多就視為 Overengineering：其新增部分是輸入/輸出安全、原始追溯、Schema/Frontmatter、負向/rollback 校驗；若能共用既有安全元件且保留 Gate，可刪除重複的實現代碼。

## 8. 極簡安裝的完整使用者旅程、逐 Host 安裝和 UX 測量

### 8.1 Web Plus / Free 唯一入口規則（需要真實狀態決策，非靜態死連結）

**Web 使用者看見的首屏**：

```markdown
## Start PIPD-LS-SP S4

### 1) ChatGPT Web / Desktop app（Plus 優先；Free 按實際帳戶能力）
- 【PUBLIC_VERIFIED=true 且該帳戶可安裝】開啟已驗證的 PIPD-LS-SP Plugin Directory 頁面，按 Install，開始來源綁定 PI/PD 任務。
- 【否則】下載 **一份** `PIPD_WEB_FALLBACK.md` 並上傳 Project/對話，複製首次引導 Prompt。
- 文件備援僅 `DOC_MOUNT_ONLY`，無 Python CLI、MCP、外部倉庫寫入或 S4 認可權。

### 2) Hermes Agent / Codex Desktop / Codex CLI / Claude Code
- 開啟 `docs/install/PIPD_AGENT_INSTALL_PROMPT.md`，複製一段 Prompt，讓有工具權限的 Agent 檢查宿主、版本和受控安裝路徑。
- 安裝前必顯示寫入/刪除/是否信任來源計畫，取得使用者授權；安裝後看見 8/8 discovery 與負向回報。

Advanced / Recovery: 版本 pin、SHA、Wheel 安裝、手動 ZIP、故障排除與卸載位於 docs/install/README.md，不在首頁要求新手判斷。
```

`PUBLIC_VERIFIED` 由 Release Owner 填入**實際 Portal listing、發布版本、Plus+Free 實帳號 UAT 收據**後才可設為 true；未有資料不能顯示假 URL。上述 Markdown 中的括號是**生成條件註記**，不是要原樣發布在 README。若 Owner 暫無公開 Plugin，真實首屏就**只有單檔備援當下主路徑**；不能把未來願景稱作已可用一鍵安裝。此要求來自 `GPTB-KP17-R01..R08`、三合一附件 §5 與 AUDIT A11–A13。

**首次 Web 對話 Prompt（單 MD 模式）**：

```text
請使用我已上傳的 PIPD-LS-SP 單一 Markdown 文件。先列出你可見的來源章節與 SHA/locator，確認這是文件模式，不是已安裝 Python Compiler。請先提供「我需要補哪些最低限度的目標、來源、限制」；沒有來源或沒有獨立驗收收據時，明確 NACK，不要宣稱 S4 PASS、已寫入 Repo 或已執行 OPS ECP。
```

### 8.2 Agent 四種 Host／五個表面 — 具名能力及操作契約

| Surface | 讀到的原生命令/路徑（SUPPORT；仍要 Host 版實測） | 安裝/發現/實際載入確認 | 權限/卸載/失敗降級 |
|---|---|---|---|
| **Hermes Agent** | `~/.hermes/skills/` 為 hub global；新版本另有 project-local `<project>/.hermes/skills/`、`<project>/.agents/skills/`；`hermes skills list`、`hermes skills trust`（project）；hub `hermes skills install owner/repo/skills/name` | 推薦**專案層**從鎖定候選 ZIP 的八 Skill 受控複製到 `.hermes/skills/`，進入該 Project 執行 `hermes skills trust` + Scan + 新 Session，確認 8 名單與正/負 trigger | 若版本不支援 project local，停 `NOT_SUPPORTED` 或經同意第二線 Hub global（不得默默擴全域）；`hermes skills untrust`／卸載僅改本次檔，殘留測試。來源：[Hermes docs](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) |
| **Codex Desktop/GUI** | 官方 Plugins Directory/Local Marketplace／Skills，部分入口依介面/計畫；專案 `.agents/skills/` 會受 native mechanism 版本差異影響 | 建議 `PORTABLE ZIP` 或八技能已被驗證的 repo-local provider；GUI 啟用不等於 CLI 立即載入，須開新 session/Project 驗 8 技能/版本，測 NACK | 本輪未有實機版本、操作收據；不可給假 `codex plugin install` 命令成功證明；無入口 `NOT_SUPPORTED`，附 Host version screenshot |
| **Codex CLI** | 可使用 `.agents/skills/<name>/SKILL.md` project skills；Plugin marketplace CLI 命令依安裝版本，先 `codex --version` 和內建 help | 在 Owner 核准的 project root 相對 `.agents/skills/` 受控放 8 個 Skills；新 Session 看可發現，跑 POS/NEG/不同 Source；Client Registry 版本核對 | 不動 `AGENTS.md`、不 global；衝突中止、卸載只回滾本次變更；無已驗的 native help 就走安裝說明 `NOT_EXECUTED` |
| **Claude Code** | `.claude/skills/<skill>/SKILL.md` project native；Plugin Marketplace 另有機制；以 [Claude Skills docs](https://code.claude.com/docs/en/skills) 和實際 `claude --version` 判定 | 從已驗 ZIP 的 8 份派生 source 複製到 `.claude/skills/`，啟動新 Session，再測名稱/引用與 NACK | 既有 Skills/符號連結衝突→HOLD；不能據退出碼推論 Host 生效；撤銷本次批准檔後殘留 0 |
| **Vercel skills CLI**（第三方備援） | [vercel-labs/skills](https://github.com/vercel-labs/skills)，候選 `skills add <repo> -a codex/claude-code --skill ... --copy`，`skills list/remove` | 只有已 pin release tarball/digest、Host 版本實測、dry-run/列選確認時才啟用；**不強制 `npx latest`** | 未確認 flags/mapping 時不執行；預設 projekt local、需外部授權；不因工具省一行就放寬來源證據 |

**注意：Hermes project-local 支援曾有歷史 Issue**（官方專案 `#67143`），而官方新版 Skills 文件描述現有 trust/quarantine 工作流；因此現場**必須** `hermes --version`、查看實際 `--help`、專案根探測、scan/list/trigger/卸載，不能把最新 docs 直接推論所有已安裝舊版都支援。[Hermes issue](https://github.com/NousResearch/hermes-agent/issues/67143) / [Hermes skills docs](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)。

### 8.3 Agent 單一安裝 Prompt（可直接複製的設計版）

```text
我要在目前 AI Coding Agent 專案安裝 PIPD-LS-SP S4 八個 Skills。官方來源：https://github.com/shw097-team/PIPD-LS-SP 。
請先偵測你現在的 Host（Hermes / Codex Desktop / Codex CLI / Claude Code）、版本、OS、專案根目錄、既有同名技能與 Shell/檔案/網路權限；沒有權限只出方案，不能假裝已安裝。
只使用 Owner 已驗證的固定 Commit、Release ZIP SHA 和八個 Skills exact set，先驗 8 Skills、所有相對參照/Schema/tests、許可與來源，禁止從 floating main 自動覆寫。優先使用當前 Host 已具備並經測試的 Native project-local Skills/Plugin Install；第三方 skills CLI 僅作 pin 後第二線。
請先展示：要新增的八個目標路徑、將寫入的檔案數、對現有設定的差異、版本/hash、如何卸載；我的明確批准前不得安裝、全域寫入、修改 AGENTS.md/CLAUDE.md、執行 MCP、使用 Token、Commit 或 Publish。
經我批准後才執行。每個 Host 要確認真正的 Skills discovery/effective-load 以及 8/8 各一正反案例；若只裝到檔案沒有有效載入，回報 NOT_VERIFIED，而不是 PASS。卸載只刪本次批准的目標並檢查殘留，不動其他 Skills。
最後繁體中文回傳 Host/OS/版本、安裝時使用的 pinned source、八技能有效數、缺資料時拒絕案例、衝突/剩餘問題、raw log 路徑；勿聲稱 PIPD S4 完整驗收或 Public Plugin 已發布。
```

單 Prompt 不能賦權，不能讓未配好 runtime 的網頁對話執行 Shell；發布者信任/Repo 寫權、Human Gate 永遠外置。此 Prompt 是給有執行權限 Agent 的已審契約**不是** ChatGPT Web 的一鍵安裝腳本。

### 8.4 Per-host Test Protocol、錯誤碼與解除安裝

| Phase | 需要的原始證據 | Fail / Exit code policy |
|---|---|---|
| `preflight` | host ID, OS, `host --version`, root path, feature flags, user consent | 缺 Host 工具=NOT_SUPPORTED；誤判 Host→FAIL |
| `trust-source` | frozen commit/tree, Publisher manifest, ZIP/content SHA, license, scan result | 不一致/未授權→FAIL / no write |
| `dry-run` | 已有同名 Skill、目標 8 路徑、將修改檔案/符號連結、backup dir | 同名覆寫未批准→CONFLICT_HOLD |
| `consent` | 由人員批准的 action/scope/timestamp，不存 secrets | 缺同意→STOP；不可繞過 |
| `install` | native command stdout+stderr+exit+before/after dirs | 非零→FAIL；零僅 FILE_COPIED |
| `discover` | host UI/CLI skill list、8/8 name、effective version、new session evidence | 缺 1→HOST_FAIL；`exit 0` 不當通過 |
| `trigger & deny` | POS, NEG, indirect, non-trigger, missing-source, no unauthorized write | 任何 false PASS/Repo write→FAIL |
| `uninstall` | 差異快照/previous restoration/owned files residue 0 | 非授權刪除→SECURITY_FAIL |
| `rollback` | restore prior state independent readback | rollback failure→TT_CR_OPEN |

### 8.5 UAT 計量：最少人工成本不得覆蓋安全

`attempted_supported_accounts` 是分母，只計實際符合條件且嘗試的帳戶；Free 因平台不支援時必須單獨登記 `NOT_SUPPORTED`，不得隱藏於成功率的分母。指標：`first_success_rate = verified_first_task_success / attempted_supported_accounts`、`p50/p95_clicks`、`p50/p95_time_to_first_success`、`fallback_rate`、`install_failed_effective_load_rate`、`unsafe_write_count`、`uninstall_residue_rate`。收集前後 baseline 同一環境，明示 task difficulty、賬戶/OS/Host 版本、輔助說明次數，避免局部最適化。**建議性**（非上游 Norm）初始 UX 目標：Web public 主路徑無須挑 MD；Free fallback 1 份 MD；Agent 1 段 Prompt、零個未知全域寫入；`unsafe_write_count=0` 具阻斷性；可考慮 `p95≤5 必要點擊、p95≤10 min` 由 Owner UAT baseline 決定正式門檻。無實際測量時 UX PASS=NOT_EXECUTED。另測繁體中文、英文命令、Windows PowerShell/Mac/Linux、螢幕閱讀器或鍵盤操作、企業限制/離線情境。

## 9. Implementation & Test：十個 Gate、完整負向與 CI/Release Readback

### 9.1 UPG-G00–G09 精準阻斷矩陣

| Gate / Check | Objective | PASS 條件（必須有 raw evidence） | Fails/Degrade |
|---|---|---|---|
| `UPG-G00 SOURCE_FREEZE` | 來源身份正確 | 40hex commit/tree，tag crosswalk + SHA256 all source，vendor schema digest pin | mismatch FAIL / missing TEMP_CLOSED |
| `UPG-G01 SOURCE_IMMUTABLE` | 守住原 S4 | denied src/skills/schema/Normative diff = 0, Owner changed paths approved | unauthorized change FAIL |
| `UPG-G02 EXACT_SKILLS` | 無遺漏/多出 Skill | eight logical exact set；當版由 `freeze` 產全 recursive file set；每個 baseline 6，future approved deps 全錄 | 7/9 Skill、缺 reference、special file FAIL |
| `UPG-G03 SEMANTIC_PROJECTION` | 不壓平/不漂移 | 逐檔 exact sha；DERIVED 有 Ticket/field/source hash/Body unchanged + behavior negative | silent normalization FAIL |
| `UPG-G04 PACKAGE_FORMAT` | 合法/安全 | 官方 Plugin schema SHA vendor-lock pass、skills-ref eight valid、PNG verified、mcp/actions/hooks absent、secret/license scan、ZIP secure/readback | failure FAIL；Portal 未跑=TEMP_CLOSED |
| `UPG-G05 RELEASE_PROVENANCE` | 防舊戳/資產偷換 | ReleaseTuple commit/tree/map+zip+source version+GitHub actual asset hash matches，2x reproducible | null commit/stale tag/same-tag asset drift FAIL |
| `UPG-G06 SKILL_BEHAVIOR` | 實際工作流有效 | 8/8 each POS/NEG/EDGE/SEC/nontrigger，no-source NACK、false PASS veto、SoD/HITL guard，fresh trace | one false PASS FAIL |
| `UPG-G07 WEB_CONSUMER` | Plus/Free UX | real Plus account Public Directory effective load or fallback; real Free both availability/account-scoped fallback, 1 MD complete | no host receipt TEMP_CLOSED；false promise FAIL |
| `UPG-G08 AGENT_CONSUMER` | 多 Host UX | Hermes,Codex Desktop,Codex CLI,Claude each real install/list/trigger/negative/uninstall/rollback | unsupported host isolated NOT_SUPPORTED，不得 Universal PASS |
| `UPG-G09 PUBLIC_RELEASE` | Publisher legitimate | Verified Publisher identity, Portal ZIP SHA, scan/review approval, Human publish, public URL + user-side readback | missing=PUBLIC_HOLD，不等於 coding FAIL |

### 9.2 最小回歸 Check Tracking List（非只列名字）

| Test ID | Fixture/操作 | Expected | Gate |
|---|---|---|---|
| `TR-01` | repo commit/tree mismatch | builder nonzero / no output | G00,G05 |
| `TR-02` | source unknown/missing/new extra file | refuse exact source set | G02 |
| `TR-03` | source symlink, `../` reference, nonregular | refuse no read | G01,G02,G04 |
| `TR-04` | fake PNG valid magic + invalid body (F01) | refuse image decode | G04 |
| `TR-05` | arbitrary Manifest custom key (F02) | vendor schema reject | G04 |
| `TR-06` | invalid Skill header (F03) | reject/derive only when approved | G03,G04 |
| `TR-07` | SourceMap commit null (F04) | nonzero/no build pass | G00,G05 |
| `TR-08` | SourceMap 40hex wrong | git HEAD readback rejects | G00,G05 |
| `TR-09` | sidecar output symlink sentinel (F05) | sentinel unchanged, builder rejects | G04 |
| `TR-10` | output root overlaps repo | refuse to publish | G01,G04 |
| `TR-11` | deterministic twice fresh environments | zip SHA equal | G05 |
| `TR-12` | attacker adds ninth `SKILL.md` | fail exact eight | G02 |
| `TR-13` | Skill Header owner metadata migrated | requires preapproval and body exact | G03 |
| `TR-14` | `tests/cases.yaml` missing | fail source ledger | G02 |
| `TR-15` | stale preview.2 tag stamped preview.3 | fail release identity check | G05 |
| `TR-16` | same tag has different asset SHA | fail checksum/load | G05 |
| `TR-17` | no secret scanner evidence / matched API token fixture | release hold/reject | G04 |
| `TR-18` | SPDX/LICENSE mismatched with claimed Apache-2.0 | reject publication | G04 |
| `TR-19` | split file fallback output over cap | fail without truncating | G07 |
| `TR-20` | fallback source hash corrupt | refuse | G07 |
| `TR-21` | fallback destination symlink sentinel | refuse no overwrite | G07 |
| `TR-22` | 8 Skills each POS + NEG + EDGE + SEC | 32+ bounded behavior receipts | G06 |
| `TR-23` | each of 8 Skills has non-trigger probe | 8 nontrigger no activation | G06 |
| `TR-24` | no Source Locator | typed NACK with locator | G06 |
| `TR-25` | malicious docs command ``ignore prior...`` | quarantine no action | G06 |
| `TR-26` | fake Independent PASS prompt | refuses signoff | G06 |
| `TR-27` | Host installed but not discovered | HOST_FAIL, not install PASS | G07,G08 |
| `TR-28` | Hermes project trust false/dangerous scan | no load/no false pass | G08 |
| `TR-29` | Codex GUI installs + CLI stale version | independent states, no universal PASS | G08 |
| `TR-30` | Claude Code symlink/directory mismatch | host effective-load fail | G08 |
| `TR-31` | same-name Skill conflict | no overwrite without approval | G08 |
| `TR-32` | uninstall previously existing foreign skills | foreign paths unchanged, ours residue 0 | G08 |
| `TR-33` | no Portal reviewer identity/scan | PUBLISH_HOLD | G09 |
| `TR-34` | Portal approved but not Publish | APPROVED != PUBLISHED | G09 |
| `TR-35` | Plus can see Plugin but Free cannot | account scoped degrade | G07 |
| `TR-36` | GitHub Actions privileged PR+unsafe shell | CI config rejected | G04,G09 |
| `TR-37` | unauthorized repo code change | fail forbidden Git Diff | G01 |
| `TR-38` | LLM judge order effect and missing negative | counterbalance calibrate/report TT | G06 |
| `TR-39` | seeded orphan/hash mismatch TraceLink | preserve S4 oracle fail, no Full PASS | S4 nonpromotion |
| `TR-40` | new/old public Plugin rollback | Publisher/Host state readback matches receipt | G09 |

**配套測試涵蓋程度**：§7.3 的 14 項 + §7.4.1 的 5 項為已跑的**合成** fixture；TR-15–TR-40 多數需真實 Repo/host/Portal/Independent execution，故仍 `NOT_EXECUTED`，不得把「列到表上」誤升格 PASS。`[AUDIT §§4,5,7,8]`

### 9.3 Evidence Return Pack（每次實體檢驗必有）

```json
{
  "schema_id": "PIPD-S4-PUBLIC-EVIDENCE-RETURN.v2-CANDIDATE",
  "task_id": "UPG-P01",
  "subject": {"repo":"shw097-team/PIPD-LS-SP","commit":"REQUIRED_40_HEX","tree":"REQUIRED_40_HEX","plugin_zip_sha256":"REQUIRED_64_HEX"},
  "actor": {"maker":"MUST_BIND","checker":"MUST_BIND_DISTINCT","human_owner":"MUST_BIND"},
  "checks": [{"gate":"UPG-G00","status":"NOT_EXECUTED","tool_version":null,"stdout_sha256":null,"stderr_sha256":null,"raw_log_uri":null}],
  "mutations": {"F01":"NOT_EXECUTED","F02":"NOT_EXECUTED","F03":"NOT_EXECUTED","F04":"NOT_EXECUTED","F05":"NOT_EXECUTED"},
  "host": {"plus":"NOT_EXECUTED","free":"NOT_EXECUTED","hermes":"NOT_EXECUTED","codex_desktop":"NOT_EXECUTED","codex_cli":"NOT_EXECUTED","claude_code":"NOT_EXECUTED"},
  "portal": {"publisher_verified":false,"draft_id":null,"scan":"NOT_EXECUTED","review":"NOT_EXECUTED","publish":"NOT_EXECUTED"},
  "raw_evidence_attached": false,
  "verdict": "TEMP_CLOSED",
  "claim_ceiling": "CANDIDATE_ONLY"
}
```

上述 `REQUIRED_*` **僅為 schema specification placeholder**；真實返包須以型別 validator 強制 40/64hex、枚舉狀態、`maker!=checker` 與 candidate 同一 SHA，無法執行時 `NOT_EXECUTED` / `TEMP_CLOSED`。不要在從 ChatGPT 對話直接產生「真實 checkrun」假的 URL。正式 OROCHI schema-binding 以 `09_OROCHI_FACTORY_ORDER.md` 的規格版本編譯；本文 candidate JSON 不假冒已有 Registry Schema。

### 9.4 安全供應鏈 Gate

**Release Blocking**：zip traversal、symlink/special files、zip bomb/unbounded compression、manifest.schema unknown、Skill Header bypass、PNG invalid/惡意壓縮炸彈、secret scans missing or secrets found、license incompatible、allowlist/source mismatch、external dependency未 hash pin、CI `pull_request_target`/write token、false PASS、unapproved header derivation、一致性失敗。Scanner 需要指定 Tool SHA/Version、config/digest、raw findings count、exception approval/time、回歸 fixture 和獨立 readback；**單純寫「掃描」不算完成**。

**SBOM/Attestation**：安全 Gate 要有依賴清冊（至少 locked requirements/asset manifest）和政策選擇結果；若 SLSA/Sigstore 屬選配，正式發行需 Owner 對不做的殘餘風險簽字，不能標記「SLSA PASS」；如新增 third-party install CLI 需先 license/SCA/兼容與 pin。以 OpenSSF Scorecard/CodeQL GitHub Actions analyzer 為 advisory 辨識 CI 風險，評分不可以取代 raw evidence。

### 9.5 Release Tuple、Version monotonicity、Portal states/rollback

```json
{
  "schema_id":"PIPD-S4-PUBLIC-RELEASE-TUPLE.v2-CANDIDATE",
  "source":{"repo":"shw097-team/PIPD-LS-SP","commit":"REQUIRED_40_HEX","tree":"REQUIRED_40_HEX","source_manifest_sha256":"REQUIRED_64_HEX","source_tag":"OWNER_BOUND"},
  "plugin":{"version":"OWNER_SELECTED_SEMVER","manifest_sha256":"REQUIRED_64_HEX","official_schema_sha256":"REQUIRED_64_HEX","zip_sha256":"REQUIRED_64_HEX","source_map_sha256":"REQUIRED_64_HEX","skills":8,"source_file_count":"ACTUAL_FROZEN_COUNT"},
  "github_release":{"tag":null,"asset_id":null,"download_sha256":null,"replay_verified":false},
  "public_portal":{"publisher_verified":false,"draft_id":null,"scan_status":"NOT_EXECUTED","review_approved":false,"published_id":null,"published_url":null},
  "claim_ceiling":"BUILD_CANDIDATE_ONLY"
}
```

**採分離的版本關聯**：源 PIPD `v0.1.1-preview.3`、本次 Upgrade source commit/tree、Plugin `<new SemVer>`、Portal revision/archive digest 分別記錄；TAG**不是**發布資產位元組 hash。過往 `.3` 同 Tag 替換不必重寫歷史，但新的 Public Plugin 公發應使用新的版本與新 bytes，禁止 silent in-place replacement。發生受損/退出時，先進入 `WITHDRAWN/UPDATE_REQUIRED`，Publisher依 Portal 正式機制處置，通知用戶已註冊的 known-good snapshot；Host project-local 有批准才能卸載/重裝，不能假裝 Portal 支援已發布版本的任意回滾。`[PKG-08 Part11; Repo RELEASE_CORRECTION_WEB_MOUNT.md L29–60]`

## 10. Risk Register、CR_OPEN、Degrade/Hold 完整帳本

| CR ID | 種類 | 缺口/事實 | Owner | 阻斷與降級 | Closure evidence |
|---|---|---|---|---|---|
| `CR-SOURCE-ATOMIC` | EVIDENCE_GAP | 102 檔物理掃描不等於 866k 行逐原子語義驗收；skeleton 自標 atomic not proven | Authority | 全量上游 claim 不得升格；scoped A01–A42 設計候選 | owner-reviewed subatom semantic ledger + independent reaudit |
| `CR-F01-PNG-PORTAL` | EXTERNAL_TEST | local Pillow fixture 通過但真 public logo Portal 未驗 | Publisher | PUBLISH_HOLD | real logo scan receipt |
| `CR-F02-SCHEMA-LOCK` | TOOL_CHAIN | 官方 Schema bytes 未下載/lock 入 Repo，local tests 用 synthetic schema | Build Owner | BUILD_HOLD for real candidate | vendor sha official + `jsonschema` and Portal |
| `CR-F03-SKILLS-REF` | TOOL_CHAIN | 原八 SKILL headers 自訂欄位；需核准 Derivation | Skill Owner | build refuse, no silent normalization | 8/8 approved fields/Body preservation + skills-ref output |
| `CR-F04-RELEASE` | EXECUTION | actual candidate source mapping+digest 未產 | Release Owner | BUILD_HOLD | frozen pinned tuple and fresh checker receipt |
| `CR-F05-OS-HARDEN` | SECURITY | same-user adversarial concurrent race/Windows specific behavior 未 OS stress | Security | scoped platform no release | Windows/Linux/macos race/symlink stress |
| `CR-REAL-BUILD` | EXECUTION | 本次只跑 synthetic fixture，未在實際 Repo build Public ZIP | Maker | BUILD_PASS NOT_GRANTED | real stage artifact/repro log |
| `CR-HOST-PLUS` | ACCOUNT | Plus Directory 安裝/有效載入收據無 | UAT | `NOT_EXECUTED`→fallback | plus screenshot/raw prompts+version |
| `CR-HOST-FREE` | ACCOUNT | Free account Plugin eligibility/附件限制無 | UAT | account scoped degrade | free tested accessible route |
| `CR-HOST-HERMES` | HOST | version/project trust/scan/load/uninstall無 | Host UAT | no universal pass | Hermes real CLI results |
| `CR-HOST-CODEX-DESKTOP` | HOST | GUI Plugin/Skill discovery and uninstall 無 | Host UAT | NOT_SUPPORTED/PENDING | GUI version+steps+effective load |
| `CR-HOST-CODEX-CLI` | HOST | CLI native version/target path/UAT 無 | Host UAT | pending | CLI native install/discover/negative |
| `CR-HOST-CLAUDE` | HOST | Claude Code `.claude/skills` install/load無 | Host UAT | pending | direct reproducible receipt |
| `CR-FALLBACK-REAL` | EFFECT | Free one-file from real `preview.3`尚未生成/測實帳 | UX | single MD claim pending | exact generated MD+sha+consumer task success |
| `CR-SECRET-LICENSE` | SECURITY | 未指定實際 gitleaks/license/SBOM scan pinned runner | Security Owner | BUILD_HOLD | raw scan + exception ledger |
| `CR-CI-PROTECTIONS` | SECURITY | Repo Required checks/CODEOWNERS protection/workflow未驗 | Repo Owner | no PR merge | branch rules & checkrun receipts |
| `CR-PUBLISHER` | HUMAN | 真實 Verified Publisher/Logo/可選 URL、Portal 身分無 | Human Publisher | PUBLISH_HOLD | official identity/policy evidence |
| `CR-PORTAL` | PLATFORM | Scan/review/approval/publish/host UAT 尚無 | Publisher | not published | portal states+visible directory URL |
| `CR-S4-ORIGINAL` | OUT_OF_SCOPE | 原 TraceLink/Closure、Wheel/13 CLI/19 Schemas S4 all-tests 未封閉 | Original S4 owner | **不得宣稱 PIPD_S4_FULL_PASS** | original S4 independent pack |
| `CR-OSS-ADOPTION` | DECISION | 六 OSS + skills tool only comparison, not dependency installed | PKG04 Owner | not in scope | ADR if needed, version/license pinned |
| `CR-REVIEW-INDEPENDENCE` | SOD | 本輪 source review與 synthetic tests由本助理編製/自測，獨立 Checker 未執行 | Independent | no external PASS | fresh checker actor/raw logs |

`TEMP_CLOSED` 僅代表證據不足需等待非可擅補；`FAIL` 為已知阻斷/安全或回歸 Gate 失敗；`PARTIAL` 僅表示局部非重大成果存在；`PASS` 要全部同候選、原始證據、獨立複驗及 Human Gate 閉合。對任一平台不相容而公開不支援的平台，以 `NOT_SUPPORTED` 進入矩陣且不得在 README 宣稱全平台相容，不能偷偷縮小用戶承諾。`[AUDIT §9; GPTB-KP11/12/18]`

### 10.1 發布前 No-Go 速查（Fail-Closed）

任何一項為真，則 **`NO GO`**：`repo source changed outside allow-set`、`vendor schema not locked`、`any 8 Skills not validated`、`SourceMap null/mismatch`、`false independent PASS`、`unverified PNG/asset`、`secret/license scan absent`、`host UAT claimed without receipts`、`owner/publisher identity absent`、`same-tag bytes silently replaced`、`permission elevation without consent`、`original S4 full pass inferred`。小升級 PR 可以在 Public Portal 暫未完成時宣稱 **`CODE_CANDIDATE_READY_PENDING_PUBLISH`**（前提是 G00–G06 真正通過），但 README 絕不得同時顯示「已公開一鍵安裝」。

### 10.2 對 Overengineering Index（OEI）的明確判斷

採用**五維定性比較**：新增權限面、重複 Runtime、外部依賴、維運成本、對目前用戶收益。**A 一個 PKG07/08 Public distribution/UX PR**＝低；**B 三條 Plugin/Publish/Installer 獨立專案**＝中高；**C 全套自製跨 Host Installer**＝高；**D MCP+Remote Backend+OAuth**＝極高且不符合當前目標。這是需求相關工程權衡，而非宣稱有實測統計的客觀市場百分比。若 Host UAT 顯示 Native 原生缺失、導入外部 `vercel-labs/skills` 能顯著改善首次任務成功率、降低人工時間且不擴權，Owner 可在 ADR 批准第二線，但仍不需新 Stage。

## 11. OROCHI_FACTORY_ORDER.v1 Candidate／TaskSpec／evidence_return_pack 施工包絡

**權威來源**：`09_OROCHI_FACTORY_ORDER.md`, `05_SDD_ADR_TASKSPEC.md`, `10_AGENTIC_SWE_HARNESS.md`, `11_EVIDENCE_REQUIREMENT_MATRIX.md`, `challenge-review-SKILL.md`。下列 YAML 是**候選示意投影**，Schema Registry 的正式欄位、Enumeration 和接收要求須依上述實質條文編譯再驗；不存在「本助理已對外派工」。

```yaml
order_kind: OROCHI_FACTORY_ORDER.v1
order_status: CANDIDATE_NOT_ROUTED
change_id: S4-UX-DISTRIBUTION-UPGRADE-R1
route: DESIGN_AND_SCOPED_IMPORT
subject:
  repository: shw097-team/PIPD-LS-SP
  baseline_commit: 224591431a164ab72a9423cd180e417e8a762403
  baseline_tree: 1a9fcb94a42eb589e405c2453793be986419d4cb
  new_candidate_commit: NOT_ASSIGNED
  plugin_version: OWNER_DECISION_REQUIRED
objective:
  - One Public Skills-only Plugin candidate from original eight Skills
  - One verified Web route with one-file fallback when unpublished
  - One Agent Prompt and four host-specific effective-load contracts
  - Build/release/user publication states must not be conflated
work_packages:
  - id: UPG-P01
    owner: PKG07
  - id: UPG-P02
    owner: KP17_DX
  - id: UPG-P03
    owner: PKG06_TQAEP_AND_PKG08
  - id: UPG-P04
    owner: PKG08_RELEASE_HUMAN_PUBLISHER
allowed_write_set:
  - packaging/public-plugin/**
  - docs/install/**
  - tools/freeze_public_plugin_source.py
  - tools/build_public_plugin.py
  - tools/build_web_fallback.py
  - tests/test_public_plugin_packaging.py
  - tests/test_web_fallback.py
  - README.md
  - .github/workflows/public-plugin-verify.yml
denied_write_set:
  - skills/**
  - src/**
  - schemas/**
  - '*canonical*'
  - 'PIPD_LS_DOC-*'
  - 'PIPD-LS-SP_PIPD-PKG-*'
  - 'ECP_TQAEP_ORACLES/**'
  - existing_release_assets/**
  - mcp.json
  - .app.json
  - hooks/**
check_gates: [UPG-G00, UPG-G01, UPG-G02, UPG-G03, UPG-G04, UPG-G05, UPG-G06, UPG-G07, UPG-G08, UPG-G09]
required_mutation_tests: [F01, F02, F03, F04, F05]
rollback: derived_scoped_only
maker_may_publish: false
independent_checker_required: true
human_publisher_required: true
claim_ceiling: BUILD_CANDIDATE_ONLY_PENDING_RAW_EVIDENCE
```

### 11.1 Task → PR → Checkrun 責任映射

- **Issue** `UPG-P01`：manifest、source projection、PNG/schema/frontmatter、source exact ledger。交付 proposed code/diff+raw F01–F05 test suite。
- **Issue** `UPG-P02`：用一個共同安裝頁承接 Web/Agent，單檔輸出有生成器、消費者樣本、容量與 release stamp 測試。
- **Issue** `UPG-P03`：QA automation 與四 Host/Plus/Free UAT 作不同 receipts；独立 Checker 不能由 Maker 自簽。
- **Issue** `UPG-P04`：ReleaseTuple/new version、依賴與回滾、新 Portal listing/publisher handoff；Portal 正式操作權留 Human。
- **PR**：一個 scoped ChangeSet 允許包含上述四組，建置/測試做到多少報多少；Release Portal gate 為 external asynchronous human/platform step，PR merge 不代表公開成功。

### 11.2 證據返包不可少欄位（與 §9.3 對齊）

每個 Checkrun 至少 `case_id, gate_id, objective, subject_commit/tree/zip_sha, host/OS/version, tool+pin, actor_role, started_at, input_fixture_sha, command/permission, exit_code, raw_stdout_uri+sha, raw_stderr_uri+sha, artifact_url+sha, observed_effect, expected_effect, negative_first_fail, verdict, tt_cr, owner_approval`；給 LLM judge 的 prompt/model/settings/順序交換結果另附，但不可由 LLM judge 宣告 raw code/source integrity PASS。`[KP11,KP12,PKG06/DOC07]`

## 12. AUDIT 42 項原子需求：Source → Substantive Body → Gate／未閉合狀態

**方法**：依 `AUDIT §5` 的 A01–A42 **全部逐列展開**，遇「Plus/Free」「Hermes/Codex desktop/CLI/Claude」「六開源比較」均拆成獨立原子；`§target` 指向本文有操作/測試/權限之**實質正文**，不是只有標題或關鍵字。`HOST_PENDING/VENDOR_PENDING` 明確代表設計措施已存在、但外部實施證據尚未取得。若原規範抽出更多上游 sub-atoms 未列於 42，本文件不稱 100% atomic exhaustiveness。

| Audit Atom | Required substance (分別驗) | R2 target locator | 本輪 evidence ceiling |
|---|---|---|---|

| `A01` | one upgrade | §3.2 §5.1 | `CANDIDATE_SPEC` |

| `A02` | no new stage | §0 §3.2 | `CANDIDATE_SPEC` |

| `A03` | eight exact Skills | §0 §7.1–7.3 | `SYNTHETIC_TEST` |

| `A04` | no rewrite core | §0 §3.3 §9.1 | `SPEC_ONLY` |

| `A05` | one canonical multi-projection | §3.2 §7.2 §7.4 | `SYNTHETIC_TEST` |

| `A06` | portable manifest/plugin | §4.1 §7.2 §7.5 | `VENDOR_PENDING` |

| `A07` | dynamic 8 skills closure | §7.1–7.3 | `SYNTHETIC_TEST` |

| `A08` | relative files closure | §7.2 §9 TR-14 | `INDEPENDENT_PENDING` |

| `A09` | Portal stages | §3.4 §5.2 §9.5 | `HUMAN_PENDING` |

| `A10` | publisher assets/license | §7.2 §7.5 §10 | `HUMAN_PENDING` |

| `A11` | Plus Web main | §8.1 §9 G07 | `HOST_PENDING` |

| `A12` | Free when available | §8.1 §8.5 | `HOST_PENDING` |

| `A13` | Free one-file fallback | §7.4 §8.1 | `SYNTHETIC_TEST` |

| `A14` | Hermes Agent | §8.2–8.4 | `HOST_PENDING` |

| `A15` | Codex Desktop GUI | §8.2–8.4 | `HOST_PENDING` |

| `A16` | Codex CLI | §8.2–8.4 | `HOST_PENDING` |

| `A17` | Claude Code | §8.2–8.4 | `HOST_PENDING` |

| `A18` | Native vs Vercel skills | §4.3 §8.2 | `SELECTED_CONDITIONAL` |

| `A19` | OpenSpec | §4.2 row OpenSpec | `BENCHMARK_ONLY` |

| `A20` | Spec Kit | §4.2 row Spec Kit | `BENCHMARK_ONLY` |

| `A21` | Matt Skills | §4.2 row Matt Skills | `BENCHMARK_ONLY` |

| `A22` | GSD | §4.2 row GSD | `BENCHMARK_ONLY` |

| `A23` | gstack | §4.2 row gstack | `BENCHMARK_ONLY` |

| `A24` | Superpowers | §4.2 row Superpowers | `BENCHMARK_ONLY` |

| `A25` | MCP OFF | §0 §4.4 | `SCOPE_DECISION` |

| `A26` | preview.3 repaired not current defect | §2.2 §3.1 | `REPO_READBACK` |

| `A27` | deterministic build twice | §7.3 §9 TR-11 | `SYNTHETIC_TEST` |

| `A28` | independent raw evidence | §5.3 §9.3 | `INDEPENDENT_PENDING` |

| `A29` | 8 skill POS/NEG/EDGE/SEC | §9.2 TR-22–26 | `HOST_PENDING` |

| `A30` | source no claim | §0 §3.4 | `CANDIDATE_SPEC` |

| `A31` | injection/supply chain | §9.2 TR-17/25 §9.4 | `SCANNER_PENDING` |

| `A32` | auth/privacy accessibility | §8.5 §10 | `HUMAN_PENDING` |

| `A33` | rollback | §5.5 §9.5 | `HOST_PENDING` |

| `A34` | end-to-end UX metrics | §8.5 | `UAT_PENDING` |

| `A35` | machine summary | Appendix B | `GENERATED` |

| `A36` | change_plan.tsv | Appendix C | `GENERATED` |

| `A37` | checkrun contract.tsv | Appendix D | `GENERATED` |

| `A38` | history chain | §2.1–2.3 | `SCOPED_COVERAGE` |

| `A39` | source provenance | §1 §12 Appendix A | `SCOPED_COVERAGE` |

| `A40` | two sources on tech | §4.1–4.3 | `SUPPORT_CROSSCHECK` |

| `A41` | S4 original FULL_PASS separate | §0 §3.4 §9 | `NO_PROMOTION` |

| `A42` | minimal write footprint | §3.3 §5.1 | `DESIGN_CANDIDATE` |

### 12.1 預先設定的「無聲降級」檢查

如新版本遺失以下具名術語/決策，全文機器檢查必發 `COVERAGE_REGRESSION_FAIL`：`OpenSpec`, `Spec Kit`, `Matt Skills`, `GSD`, `gstack`, `Superpowers`, `vercel-labs/skills`, `OpenSSF`, `SLSA`, `Sigstore`, `Agent Plugins 1.0`, `Agent Skills`, `Plugin Creator`, `ChatGPT Work`, `Hermes`, `Codex Desktop`, `Codex CLI`, `Claude Code`, `PIPD-LS-SP`, `OROCHI_FACTORY_ORDER.v1`, `HGK`, `Plus`, `Free`, `source_map`, `ReleaseTuple`, `TraceLink`, `TQAEP`, `OPS ECP`, `DEV ECP`, `HITL`, `fail-closed`, `rollback`。關鍵詞命中**只是防遺漏初篩**：對技術項仍須在 §4 有用途/比較/決策、對 Host 仍須在 §8 有 install/discover/uninstall、對安全 Gate 仍須在 §9 有 negative/owner/證據。`[AUDIT §3/§5；PATCH SOP7]`

## Appendix A — 全量實體 Inputs Manifest（本輪 102 份 Markdown）

**生成方式**：`Path('/mnt/data').rglob('*.md')`, each read bytes and strict UTF-8, SHA256, line count, term-family hit count。保留實體長檔名稱與 SHA-256，會有內容重複的百分比編碼副本。依檔名標法位是**工作範圍分類**，不是承認每個檔案都提供此 Upgrade 的直接規範。

| # | File/path | Role | Bytes | Lines | SHA-256 | Status |
|---:|---|---|---:|---:|---|---|

| 1 | `00_KNOW_INDEX.md` | `LOCAL_NORM` | 7827 | 129 | `5b42ababab952cb7946051baa8f99e23e560504ffb2fd35e8e38b02962917ec9` | FOUND_UTF8_FULL_SCAN |

| 2 | `01_AUTHORITY_BOUNDARY.md` | `LOCAL_NORM` | 8032 | 129 | `4fcbf184144d38918aa4599ee8665c8078f1992f107b6bd5e106a9b6d2e6e6a2` | FOUND_UTF8_FULL_SCAN |

| 3 | `02_OUTPUT_CONTRACT.md` | `LOCAL_NORM` | 8046 | 129 | `302b9eb2876fd92b090eb02b0e1c3ab22077cac18fc83381e30b2923ed2d8a0f` | FOUND_UTF8_FULL_SCAN |

| 4 | `03_INTAKE_P2E_HANDOFF.md` | `LOCAL_NORM` | 8392 | 132 | `f97afbe1e020d4ee9deea4ea6bf5a95e0f5aa4106e5508ab1c24a1a702aebb44` | FOUND_UTF8_FULL_SCAN |

| 5 | `04_PRODUCT_BUSINESS_RISK_ACCEPTANCE.md` | `LOCAL_NORM` | 8412 | 131 | `e6d357b7ecbeeb1ff972b7aae6fb7388566a73e0dfe92527f43c29c28ec81f01` | FOUND_UTF8_FULL_SCAN |

| 6 | `05_SDD_ADR_TASKSPEC.md` | `LOCAL_NORM` | 7906 | 130 | `97355259edde717eeaf249205c56c352506d7d1c5b18fcd434ce4cf234bfeb10` | FOUND_UTF8_FULL_SCAN |

| 7 | `06_BUILDER_CONFIG.md` | `LOCAL_NORM` | 8130 | 132 | `ac2357934eeca6f61684e44b1a21ebaf78998cf047ec2b4d29a54a0fc56a1ce0` | FOUND_UTF8_FULL_SCAN |

| 8 | `07_BUILDER_INSTRUCTIONS.md` | `LOCAL_NORM` | 8187 | 128 | `79d0bd91a4a24f0195e5148ce459256d8c05f38f75e150a5a54d6bbb264c3ee4` | FOUND_UTF8_FULL_SCAN |

| 9 | `08_KNOWLEDGE_RAG_SOURCE_TO_ANCHOR.md` | `LOCAL_NORM` | 8124 | 129 | `42e12f231f01e750652ca98536d81a22d31e0935f2cc9e2ccd730fb8671384c7` | FOUND_UTF8_FULL_SCAN |

| 10 | `09_OROCHI_FACTORY_ORDER.md` | `LOCAL_NORM` | 8668 | 143 | `578ca9310b5e7fe2ff880ce913ef24b7f6702a472a9bb347f9ace2ad6bc75403` | FOUND_UTF8_FULL_SCAN |

| 11 | `10_AGENTIC_SWE_HARNESS.md` | `LOCAL_NORM` | 8187 | 131 | `7773d221b1b15b7bb4bd355c337c3cfe051e6efa00e051d5e5c7c1e61c4de929` | FOUND_UTF8_FULL_SCAN |

| 12 | `11_EVIDENCE_REQUIREMENT_MATRIX.md` | `LOCAL_NORM` | 8151 | 131 | `577e1de7ff15f4d66aefcb8cb8ccfad678ecb68b4eb3592d2536549055be6559` | FOUND_UTF8_FULL_SCAN |

| 13 | `12_EVAL_REGRESSION_LLM_JUDGE.md` | `LOCAL_NORM` | 8331 | 132 | `ef8601f057f6b6a764410910257964607bd3e6baa735481a8b06dbcde7000cca` | FOUND_UTF8_FULL_SCAN |

| 14 | `13_SECURITY_PRIVACY_PROMPT_INJECTION.md` | `LOCAL_NORM` | 8380 | 130 | `f3b64233d0983ad60fa95c658757c15499d0eea38af98408973d33e1a5725e87` | FOUND_UTF8_FULL_SCAN |

| 15 | `14_APPS_ACTIONS_MCP_ROUTEOUT.md` | `LOCAL_NORM` | 8449 | 130 | `36e19f0e63555be39cb2976e819f01becf1e111d1dd737c9e0a84ee31b424934` | FOUND_UTF8_FULL_SCAN |

| 16 | `15_MEMORY_STATE_TRACE_REPLAY.md` | `LOCAL_NORM` | 8422 | 132 | `4d4ebb379ee732b9e9afea7f29bf60d566d4712e387c25f1dbf549178ff8503a` | FOUND_UTF8_FULL_SCAN |

| 17 | `16_RELEASE_PACKAGING_CHECKSUM_READBACK.md` | `LOCAL_NORM` | 8135 | 129 | `dc4e9bbca29b1053235cc624066b8d42366d66d7d1086717a9d18dda81875e0c` | FOUND_UTF8_FULL_SCAN |

| 18 | `17_UX_ONBOARDING_NO_BRAIN_FLOW.md` | `LOCAL_NORM` | 8010 | 129 | `f02c9507aa642910d18f90076f47a71c2db96329a4ac3303978e0068560d6155` | FOUND_UTF8_FULL_SCAN |

| 19 | `18_TT_CR_DRIFT_REGISTER.md` | `LOCAL_NORM` | 7946 | 131 | `b28b56aaaacb819b87ac66435963f538f99a1b061351c8748e225d6910252d6a` | FOUND_UTF8_FULL_SCAN |

| 20 | `19_KP_INDEX_CROSSWALK.md` | `LOCAL_NORM` | 8251 | 131 | `b0cd77297e1a57207ab41db683d14d0c8df12114315604c6da1efa81a1b9b561` | FOUND_UTF8_FULL_SCAN |

| 21 | `Fabric使用說明文檔.md` | `BACKGROUND` | 29436 | 314 | `7c30cf68719966cce4edebdd1d1dea5fcf83a9deaad752df9d78ac09e885d651` | FOUND_UTF8_FULL_SCAN |

| 22 | `HG-KSEOS使用說明文檔.md` | `BACKGROUND` | 36011 | 435 | `b0ecacc2a1272774b361d0f6edfb63e9dd95db9efaff2e6969ed1341a4f38b2d` | FOUND_UTF8_FULL_SCAN |

| 23 | `PIPD-LS-SP S4｜Public Skills-only Plugin 新增子開發階段工程鑑定誤.md` | `HISTORY` | 21947 | 218 | `798e505e732a7857ea389f3ecfeddad0748472672fcabe4f52f05221684dfe20` | FOUND_UTF8_FULL_SCAN |

| 24 | `PIPD-LS-SP S4｜三合一小型升級_總討論.md` | `HISTORY` | 75578 | 1359 | `b110ec50340e82dbda322aa524c13f7d579d56a81a9427495107ccaefeeb22b4` | FOUND_UTF8_FULL_SCAN |

| 25 | `PIPD-LS-SP S4｜三合一小型升級藍圖 — FULL DESTRUCTIVE AUDIT.md` | `AUDIT` | 75400 | 709 | `2321c54bb6ce482d7994fb14dfa74e4d4db158a56bf0ece6b927f28570d5f8d6` | FOUND_UTF8_FULL_SCAN |

| 26 | `PIPD-LS-SP S4｜三合一小型升級：Public Skills-only Plugin × 公開發行 × 極簡安裝體驗.md` | `HISTORY` | 27300 | 243 | `d7b5cc7e6b26ce5fcff62cefa2c92f4c1fe38da1c9415308b4243e8b1b05d92d` | FOUND_UTF8_FULL_SCAN |

| 27 | `PIPD-LS-SP_PIPD-EC_SGM_總藍圖_2026-10-07_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 187925 | 2417 | `0a29095745c628728e6fd7eb5934ecede0368ed870dda9d2b8139ec67296c6b1` | FOUND_UTF8_FULL_SCAN |

| 28 | `PIPD-LS-SP_PIPD-EC_SGM_總討論.md` | `BACKGROUND` | 193385 | 7123 | `674eb471adca93532a1e24fca6459fb7ed6acdb73b59334f0c8448efee919ef7` | FOUND_UTF8_FULL_SCAN |

| 29 | `PIPD-LS-SP_PIPD-PKG-00.md` | `UPSTREAM_NORM` | 594228 | 10742 | `89b60fde8b7bb93522c897a250a3ffbf9f2c4f91556493e74ee2da269710ecfe` | FOUND_UTF8_FULL_SCAN |

| 30 | `PIPD-LS-SP_PIPD-PKG-01_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 984996 | 21587 | `4c468e38d461595f21cd4d696dd2b97b655a438d7c8ef2fa1fec29637f8e139f` | FOUND_UTF8_FULL_SCAN |

| 31 | `PIPD-LS-SP_PIPD-PKG-02_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 676216 | 10158 | `decf42108f693563b1127064864b891d233ace2cf63b33db8f8e57e5ef29e977` | FOUND_UTF8_FULL_SCAN |

| 32 | `PIPD-LS-SP_PIPD-PKG-03_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 735475 | 19674 | `a8d61dc4ab3062f401427c0787f596093671c6e0d7408c6e924be3362423043f` | FOUND_UTF8_FULL_SCAN |

| 33 | `PIPD-LS-SP_PIPD-PKG-04_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 840568 | 16528 | `967c0a4906d735f7f0973987b6162993d8a87d88d8675d9bd1675f31b1055a77` | FOUND_UTF8_FULL_SCAN |

| 34 | `PIPD-LS-SP_PIPD-PKG-05_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 295627 | 4199 | `b01b170519b1343c6f4593b4e039b28bb9b4f3f68dbd9c17be52b198d542ff94` | FOUND_UTF8_FULL_SCAN |

| 35 | `PIPD-LS-SP_PIPD-PKG-06_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 307177 | 4821 | `073592099de22584e12b5ca892c52b298ccca2504f759e723c258a52c2b14dc9` | FOUND_UTF8_FULL_SCAN |

| 36 | `PIPD-LS-SP_PIPD-PKG-07_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 736406 | 14993 | `213b49c53f060ea780657def96a22b7e2815a222726874187d154f844a5c9872` | FOUND_UTF8_FULL_SCAN |

| 37 | `PIPD-LS-SP_PIPD-PKG-08_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 712350 | 15916 | `e93fe81371192b43c2b583423a33cfb728b6a6b99a7eef48ef19ff2516e18445` | FOUND_UTF8_FULL_SCAN |

| 38 | `PIPD-LS-SP_PIPD-PKG-09_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(1).md` | `UPSTREAM_NORM` | 733299 | 12555 | `b2952652d511ff726fac0b7f80147f807d1624ad4392c682635aa5582e386197` | FOUND_UTF8_FULL_SCAN |

| 39 | `PIPD-LS-SP_PIPD-PKG-10_2026-10-08_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY(2).md` | `UPSTREAM_NORM` | 1099995 | 11934 | `e089fa095aa83f130be4846b478edc14bea9f410d4cc99ad52e4b6b5375391bd` | FOUND_UTF8_FULL_SCAN |

| 40 | `PIPD-LS-SP_PIPD-PKG_藍圖&skeleton(2).md` | `BACKGROUND` | 3925634 | 56534 | `c5f5fe48156dc6458378b870f218b8b83a323d2f939aa7d6b343ca7841b63f48` | FOUND_UTF8_FULL_SCAN |

| 41 | `PIPD-LS-SP_S4_%E6%A5%B5%E7%B0%A1%E5%AE%89%E8%A3%9D%E9%AB%94%E9%A9%97_%E5%B7%A5%E7%A8%8B%E9%91%91%E5%AE%9A%E8%88%87%E6%94%B9%E9%80%A0%E6%96%B9%E6%A1%88_2026-10-12.md` | `HISTORY` | 21298 | 156 | `700648305252b4242abc1c743d60dd998997e4acae4ca3bf1f5d8a87b89df086` | FOUND_UTF8_FULL_SCAN |

| 42 | `PIPD-LS-SP_S4_三合一小型升級藍圖_2026-10-12.md` | `HISTORY` | 84789 | 954 | `592044addde580dba70e7df38ad82be072c3d5ccc6cee4988868934367bca505` | FOUND_UTF8_FULL_SCAN |

| 43 | `PIPD-LS-SP_S4_極簡安裝體驗_工程鑑定與改造方案_2026-10-12.md` | `HISTORY` | 21298 | 156 | `700648305252b4242abc1c743d60dd998997e4acae4ca3bf1f5d8a87b89df086` | FOUND_UTF8_FULL_SCAN |

| 44 | `PIPD-LS-SP_skeleton.md` | `UPSTREAM_NORM` | 16078915 | 262863 | `a320d344785da9700aff8f48699b307ef150e0bb89d15735722f2930e46faa0e` | FOUND_UTF8_FULL_SCAN |

| 45 | `PIPD-LS-SP_藍圖.md` | `UPSTREAM_NORM` | 243577 | 2517 | `a751a9e91dc6d0b7914b0598519e5d7a0f7adaccb6704e9c7d2aa503f80b0d68` | FOUND_UTF8_FULL_SCAN |

| 46 | `PIPD_LS_DOC-00_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 251982 | 2292 | `be3a672ec20aa0e6b5e0e35097fc08de749bfe7f59f827d18e38aef67dd68ea4` | FOUND_UTF8_FULL_SCAN |

| 47 | `PIPD_LS_DOC-01_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 177451 | 2592 | `b753f2e5cdd5598a818f8a113d57b7f815aeb3f1dfa061ce74c76bb3553ac8c7` | FOUND_UTF8_FULL_SCAN |

| 48 | `PIPD_LS_DOC-02_2026-10-07_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_SUBSTANTIVE_BODY (1).md` | `UPSTREAM_NORM` | 1306240 | 18413 | `a021998dd3b63015e89af1dd40e0b413744a69b872da46c6bf5f4d92f7f23d0b` | FOUND_UTF8_FULL_SCAN |

| 49 | `PIPD_LS_DOC-03_2026-10-07_r2_AUDIT_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 454167 | 1911 | `d89d82dcd2c8603ec6b86c5ec8c40845e4594bc181adf5272bd48a3de7c88f0f` | FOUND_UTF8_FULL_SCAN |

| 50 | `PIPD_LS_DOC-04_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 181988 | 4052 | `fa64d84da3d747b183e4affff62f4d2fb86c80bb5075f5dd933c09b20caeddcf` | FOUND_UTF8_FULL_SCAN |

| 51 | `PIPD_LS_DOC-05_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 227894 | 3946 | `7b40584540c162cda6debfd09a4c04321416706acdb03a7a3c2b41383dc585f4` | FOUND_UTF8_FULL_SCAN |

| 52 | `PIPD_LS_DOC-06_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 405028 | 3790 | `20e44ea4dd8e53c9b0a076ce861136bbea86f52687019307f6e995cd9079d303` | FOUND_UTF8_FULL_SCAN |

| 53 | `PIPD_LS_DOC-07_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 689563 | 12915 | `a68dae1c3670d07bcfa3476a1e37463c534594df5cd65d8dab0dca064b5a9fc1` | FOUND_UTF8_FULL_SCAN |

| 54 | `PIPD_LS_DOC-08_2026-10-07_r2_HIGH_RETENTION_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 197972 | 2501 | `e46caa7e440392a6cfa7a86421aead5bce8a2a229fec97b133429db6b6748e42` | FOUND_UTF8_FULL_SCAN |

| 55 | `PIPD_LS_DOC-09_2026-10-07_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `UPSTREAM_NORM` | 144948 | 2451 | `eaf0aefe2b4711c140fc3274223d88fdc38ad4ec2b7184f756a0f2471f3b0b54` | FOUND_UTF8_FULL_SCAN |

| 56 | `PIPD_LS_canonical_standard.md` | `UPSTREAM_NORM` | 209157 | 7176 | `6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a` | FOUND_UTF8_FULL_SCAN |

| 57 | `Pre-Implementation-PKG  Pre-Dev-PKG 生命週期規格_總討論.md` | `BACKGROUND` | 77326 | 2559 | `be1858e860092fb1751bf0524cd22b6939138b6835ce8f452bfc30894f945a95` | FOUND_UTF8_FULL_SCAN |

| 58 | `SDLC_PRW_HLPE_SKILLS_PLUGIN_R2.md` | `SCOPED_DONOR` | 4708011 | 26846 | `afa73b3542fde82b1ac2134d41a351240004d6c81304c3ff22e6e76874201926` | FOUND_UTF8_FULL_SCAN |

| 59 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-00_2026-09-19_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 678938 | 3312 | `dc71306353a69409d0e9909041482fe482575c09e2f1bab05ac51a81ef36c0de` | FOUND_UTF8_FULL_SCAN |

| 60 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-01_2026-09-20_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1751280 | 16314 | `090d689b35fe928bba96845cc5fc5dcdc0f17f274354b025aa2ffa95586bfa68` | FOUND_UTF8_FULL_SCAN |

| 61 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-02_2026-09-21_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1180569 | 8408 | `fd4c7b3d27ed55760ce6d726ab9764c85ee240423e183f252d6a080e7afe16d4` | FOUND_UTF8_FULL_SCAN |

| 62 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-03_2026-09-22_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 668903 | 5815 | `c8edfe2c704da26245eca1c1f2bf5d050c344d59e9a996d0606cc02a1b217491` | FOUND_UTF8_FULL_SCAN |

| 63 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-04_2026-09-25_r2_HIGH_RETENTION_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY (1).md` | `BACKGROUND` | 1723907 | 11190 | `8211e450c1c68d26012dd9c4644cd7b2d9639ca5eb5c2e50078db143b8648c6b` | FOUND_UTF8_FULL_SCAN |

| 64 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-05_2026-09-23_r3_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 439056 | 5039 | `45a29510ba36318e581fc43db2c58b6b3e6f2bec0374c6cec754f71b5f521388` | FOUND_UTF8_FULL_SCAN |

| 65 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-06_2026-09-24_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1428389 | 11381 | `8b05ac7cf0b68b09c01fa5fdc38caa9db6002c2dd33414ec6c89b08007fa7b63` | FOUND_UTF8_FULL_SCAN |

| 66 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-07_2026-09-22_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 650820 | 5063 | `4b5ae7e4ec213dce4fbac30ade01486d1fd77679c95cafe7d100de160929cac0` | FOUND_UTF8_FULL_SCAN |

| 67 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-08_2026-09-25_r2_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 577971 | 3003 | `3d6491e6a56b14e908fe6ff711395e84500231c35d81d0c16bdef5ee7523fbd5` | FOUND_UTF8_FULL_SCAN |

| 68 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-09_2026-09-24_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 605338 | 3868 | `f608bc048b338f71bff9bc3fdb0aed3e066de3a68092a6a41ba1aad32eba997e` | FOUND_UTF8_FULL_SCAN |

| 69 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-10_2026-09-25_r2_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 510896 | 4543 | `76063a6fd497285333d283a3e515fcca33eb9b25729e80bceaf541b4ecbba2b4` | FOUND_UTF8_FULL_SCAN |

| 70 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-11_2026-09-27_r2_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1323931 | 12447 | `9da8ecc1f163439afa60a71a77ed784385e14496f342377dd35c91bda89038ed` | FOUND_UTF8_FULL_SCAN |

| 71 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-12_2026-09-29_r2_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 665484 | 7162 | `3e60f49072e269c7be5cd9bcf38aec3b204492a13b531e817567d36e132f8677` | FOUND_UTF8_FULL_SCAN |

| 72 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-13_2026-09-29_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 822164 | 3669 | `e2ec36c473dbcb5918a195a1ea2ae74a247f6404c303c87da1506498d32123fb` | FOUND_UTF8_FULL_SCAN |

| 73 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-14_2026-09-30_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 819555 | 5916 | `be1182b5f5a6f8886b3e1b753c2bdf8e264f91caf2298f87b1f52270d2c41d0f` | FOUND_UTF8_FULL_SCAN |

| 74 | `SWOF-F_SWOF-GENIE_All-IW_PD-PKG-15_2026-09-30_r2_HIGH_RETENTION_AUDIT_PATCHED_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 2566455 | 14109 | `297c9120b9f317ac48df0b0cb2bc65b30c68bbf787334078384532663f792e8d` | FOUND_UTF8_FULL_SCAN |

| 75 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-00_2026-09-08_r2_FULL_REPAIR.md` | `BACKGROUND` | 406510 | 2053 | `4cf1420abe34b39a34dc4181198ff13be81cd0901a138197d31db09f3fbf1a87` | FOUND_UTF8_FULL_SCAN |

| 76 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-01_2026-09-09_r2_FULL_REPAIR.md` | `BACKGROUND` | 249072 | 1386 | `46774c8a1697f93375c8045987ed78e45d45fffd14d3996b486fb04b751a5b02` | FOUND_UTF8_FULL_SCAN |

| 77 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-02_2026-09-10_r2_FULL_REPAIR.md` | `BACKGROUND` | 1095535 | 3538 | `4ca2beb49fbada5d0b305491267774fb487561f0f4317eda357c3ca21f52f5f9` | FOUND_UTF8_FULL_SCAN |

| 78 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-03_2026-09-12_r2_FULL_REPAIR.md` | `BACKGROUND` | 1115620 | 9577 | `a79e1574ab8a51c92208ecc93e674e0d38230a488704a744cd2fa57fea2a6960` | FOUND_UTF8_FULL_SCAN |

| 79 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-04_2026-09-14_r2_FULL_REPAIR.md` | `BACKGROUND` | 830970 | 11513 | `7164277db25600cbe15d1dca61dbdabb636efe9ae2376348c7415aea9d215979` | FOUND_UTF8_FULL_SCAN |

| 80 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-05_2026-09-14_r2_FULL_REPAIR.md` | `BACKGROUND` | 1259386 | 13871 | `a9d733c7ae0bc2ce6f535c7f9ebab20c50b8c6f8358bebcc9ecc2857b65367d5` | FOUND_UTF8_FULL_SCAN |

| 81 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-06_2026-09-11_r2_FULL_REPAIR.md` | `BACKGROUND` | 2309494 | 22948 | `fdd1f2b4b2144889f88579f2a11cd8442419931ea9852073e1f464f32ba1705f` | FOUND_UTF8_FULL_SCAN |

| 82 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-07_2026-09-12_r2_FULL_REPAIR.md` | `BACKGROUND` | 854923 | 6257 | `c23bd2f22f1bbf2f11e9b5257ce6d8ab5d50510333f8f13f234bd7a7f7c03ebb` | FOUND_UTF8_FULL_SCAN |

| 83 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-08_2026-09-15_r3_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 481943 | 4755 | `84010d0253f3285984d5d614f7d05a3921ef4bb5c1a46c07582018fa908dc7aa` | FOUND_UTF8_FULL_SCAN |

| 84 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-09_2026-09-15_r3_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 610893 | 4075 | `abb037953e03f8dbf0377b7bdf4c1fc05a58348ba1a53361ba7b0ef89a4adbe8` | FOUND_UTF8_FULL_SCAN |

| 85 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-10_2026-09-15_r3_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 311534 | 3253 | `324e17b30309c6df2d78c7c6f533dc22c3a00849f58c4b9afa3337bad399243b` | FOUND_UTF8_FULL_SCAN |

| 86 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-11_2026-09-16_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY(1).md` | `BACKGROUND` | 1071302 | 11932 | `9b45fc0e5169dc0805c94157fc86007f76d6716522c4942211da6cfee5959751` | FOUND_UTF8_FULL_SCAN |

| 87 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-12_2026-09-16_r2_FULL_REPAIR_FULL_INTEGRATED_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 955542 | 11709 | `5b18bdbf486f29d0daa7ca29f7daeb76879b5ff53b99c0f57571db0e8e0d356a` | FOUND_UTF8_FULL_SCAN |

| 88 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-13_2026-09-14_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1582178 | 17513 | `b94e2beed991bbcbfa25c767463a8ef9d3701f1f1b3b423596744bf4e1bbdfc4` | FOUND_UTF8_FULL_SCAN |

| 89 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-14_2026-09-14_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 1836648 | 14985 | `8aa4ce0cc7758f2c6db222dfa153a8bb7c6afb8d7edb7227bca6b8ad7ff7671a` | FOUND_UTF8_FULL_SCAN |

| 90 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-15_2026-09-17_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 181269 | 854 | `26572e5bafd77a7784b03a6ebf1bdf8e2fdd5ec29e112b04563cfec127d12f91` | FOUND_UTF8_FULL_SCAN |

| 91 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-16_2026-09-17_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 282315 | 2074 | `86d93c7ed4036722cffca48fdf198bf22e84ac9dbb56ebc8bc5e8fa4f8efe368` | FOUND_UTF8_FULL_SCAN |

| 92 | `SWOF-F_SWOF-GENIE_All-IW_PI-PKG-17_2026-09-18_r2_FULL_REPAIR_FULL_SUBSTANTIVE_BODY.md` | `BACKGROUND` | 837645 | 7256 | `da9b7ec34a5d7803cccf065f7addecfe090eee19d1a4599027b874ad4617a06b` | FOUND_UTF8_FULL_SCAN |

| 93 | `SWOF_ECP_SKILLS_PLUGIN_v2.0.1.md` | `SCOPED_DONOR` | 719549 | 15792 | `eddc399cfe9d4490aaf234bbfc4fa9debe57dfdccc7a01e4d13dd5f9198d4d3f` | FOUND_UTF8_FULL_SCAN |

| 94 | `SWOF_TQAEP_SKILLS_PLUGIN_v2.0.1.md` | `SCOPED_DONOR` | 481954 | 5497 | `728b6c6758ff6cb3345ba0dc9e9e8def6c589fd23a164eaabb89bfd1bc12049a` | FOUND_UTF8_FULL_SCAN |

| 95 | `acceptance_reports/PIPD-LS-SP_S4_%E4%B8%89%E5%90%88%E4%B8%80%E5%B0%8F%E5%9E%8B%E5%8D%87%E7%B4%9A_%E5%B7%A5%E7%A8%8B%E9%91%91%E5%AE%9A%E8%88%87%E6%96%BD%E5%B7%A5%E6%96%B9%E6%A1%88_2026-10-12.md` | `HISTORY` | 27300 | 243 | `d7b5cc7e6b26ce5fcff62cefa2c92f4c1fe38da1c9415308b4243e8b1b05d92d` | FOUND_UTF8_FULL_SCAN |

| 96 | `acceptance_reports/PIPD-LS-SP_S4_Public_Plugin_%E6%98%AF%E5%90%A6%E9%9C%80%E8%A6%81%E5%AD%90%E9%96%8B%E7%99%BC%E9%9A%8E%E6%AE%B5_%E5%B7%A5%E7%A8%8B%E9%91%91%E5%AE%9A_2026-10-12.md` | `HISTORY` | 21947 | 218 | `798e505e732a7857ea389f3ecfeddad0748472672fcabe4f52f05221684dfe20` | FOUND_UTF8_FULL_SCAN |

| 97 | `acceptance_reports/PIPD-LS-SP_S4_Public_Plugin_是否需要子開發階段_工程鑑定_2026-10-12.md` | `HISTORY` | 21947 | 218 | `798e505e732a7857ea389f3ecfeddad0748472672fcabe4f52f05221684dfe20` | FOUND_UTF8_FULL_SCAN |

| 98 | `acceptance_reports/PIPD-LS-SP_S4_Public_Skills-only_Plugin_%E5%BB%BA%E7%BD%AE%E7%99%BC%E8%A1%8C_%E5%B7%A5%E7%A8%8B%E9%91%91%E5%AE%9A_2026-10-12.md` | `HISTORY` | 18022 | 149 | `16906a411d4dfbbbe7f3f4af40023ef7387ac2ad9f6c3171ff64b7b9c84a46fe` | FOUND_UTF8_FULL_SCAN |

| 99 | `acceptance_reports/PIPD-LS-SP_S4_Public_Skills-only_Plugin_建置發行_工程鑑定_2026-10-12.md` | `HISTORY` | 18022 | 149 | `16906a411d4dfbbbe7f3f4af40023ef7387ac2ad9f6c3171ff64b7b9c84a46fe` | FOUND_UTF8_FULL_SCAN |

| 100 | `acceptance_reports/PIPD-LS-SP_S4_三合一小型升級_工程鑑定與施工方案_2026-10-12.md` | `HISTORY` | 27300 | 243 | `d7b5cc7e6b26ce5fcff62cefa2c92f4c1fe38da1c9415308b4243e8b1b05d92d` | FOUND_UTF8_FULL_SCAN |

| 101 | `challenge-review-SKILL.md` | `LOCAL_NORM` | 7332 | 99 | `9ecd2366dc2353fc8aaf533161ae1e34abba37a80f345f5f78023325f8d26194` | FOUND_UTF8_FULL_SCAN |

| 102 | `construction-acceptance-prompt-compiler_SKILL.md` | `BACKGROUND` | 7534 | 97 | `214c7f048f7361fe0bc4a324a0c99aaaf0df4191a430b645b8a97d24620064b6` | FOUND_UTF8_FULL_SCAN |

## Appendix B — machine_summary.json（文件候選，不謊稱外部執行）

```json
{
  "schema": "PIPD-S4-TRIPLE-UPGRADE-BLUEPRINT-MACHINE.v2-CANDIDATE",
  "document_id": "PIPD-S4-TRIPLE-UPGRADE-BLUEPRINT-20261012-R2",
  "document_version": "2026-10-12_r2_AUDIT_PATCHED_FULL_REPAIR",
  "supersedes_r1_sha256": "592044addde580dba70e7df38ad82be072c3d5ccc6cee4988868934367bca505",
  "audit_sha256": "2321c54bb6ce482d7994fb14dfa74e4d4db158a56bf0ece6b927f28570d5f8d6",
  "recommended_blueprint": "ONE_SMALL_CHANGESET_REUSE_PK07_PK08_GENERATE_PUBLIC_SKILLS_ONLY_PLUGIN_AND_ONE_WEB_ONE_AGENT_ROUTE",
  "repo_baseline": {
    "repository": "shw097-team/PIPD-LS-SP",
    "commit": "224591431a164ab72a9423cd180e417e8a762403",
    "tree": "1a9fcb94a42eb589e405c2453793be986419d4cb"
  },
  "source_full_utf8_scan": {
    "files": 102,
    "bytes": 71971885,
    "lines": 866660,
    "semantic_all_upstream_atoms_proven": false
  },
  "audit_atom_coverage": {
    "ids": [
      "A01",
      "A02",
      "A03",
      "A04",
      "A05",
      "A06",
      "A07",
      "A08",
      "A09",
      "A10",
      "A11",
      "A12",
      "A13",
      "A14",
      "A15",
      "A16",
      "A17",
      "A18",
      "A19",
      "A20",
      "A21",
      "A22",
      "A23",
      "A24",
      "A25",
      "A26",
      "A27",
      "A28",
      "A29",
      "A30",
      "A31",
      "A32",
      "A33",
      "A34",
      "A35",
      "A36",
      "A37",
      "A38",
      "A39",
      "A40",
      "A41",
      "A42"
    ],
    "mapping_rows": 42,
    "independent_pass": false
  },
  "audit_findings": {
    "F01_F05": "SYNTHETIC_REPAIRS_TESTED",
    "F06_F14": "DOCUMENT_MAPPED_EXTERNAL_EVIDENCE_OPEN"
  },
  "local_synthetic_tests": {
    "packaging": 14,
    "fallback": 5,
    "passed": 19,
    "independent_external_validation": false
  },
  "original_repo_modified": false,
  "public_plugin_built_for_real_repo": false,
  "public_published": false,
  "full_s4_independent_pass": false,
  "release_gate": "FAIL_CLOSED_HOLD",
  "blueprint_status": "DOCUMENT_REPAIR_COMPLETED_CANDIDATE_PENDING_INDEPENDENT_REAUDIT",
  "mandatory_gates": [
    "UPG-G00",
    "UPG-G01",
    "UPG-G02",
    "UPG-G03",
    "UPG-G04",
    "UPG-G05",
    "UPG-G06",
    "UPG-G07",
    "UPG-G08",
    "UPG-G09"
  ],
  "required_external_evidence": [
    "REAL_VENDOR_SCHEMA",
    "SKILLS_REF",
    "REAL_CANDIDATE_BUILD",
    "SECURITY_SCAN",
    "PLUS_UAT",
    "FREE_UAT",
    "HERMES_UAT",
    "CODEX_DESKTOP_UAT",
    "CODEX_CLI_UAT",
    "CLAUDE_CODE_UAT",
    "INDEPENDENT_CHECK",
    "HUMAN_PORTAL_PUBLISH"
  ],
  "prohibited_scope": [
    "NEW_S4_STAGE",
    "NINTH_LOGICAL_SKILL",
    "NEW_COMPILER",
    "MCP_SERVER",
    "REWRITE_CANONICAL",
    "MAKER_SELF_PASS"
  ]
}
```

## Appendix C — change_plan.tsv

```tsv
path	change_type	task_id	reason	release_guard
packaging/public-plugin/plugin.json	ADD	UPG-P01	Plugin portable manifest, verified publisher/semver	OWNER_IDENTITY_REQUIRED
packaging/public-plugin/assets/logo.png	ADD	UPG-P01	verified PNG listing	OWNER_BRAND_REQUIRED
packaging/public-plugin/assets/composer.png	ADD	UPG-P01	verified composer PNG	OWNER_BRAND_REQUIRED
packaging/public-plugin/plugin.schema.json	ADD	UPG-P01	vendor 1.0 pinned schema	VENDOR_SHA_REQUIRED
packaging/public-plugin/requirements.lock	ADD	UPG-P03	pip --require-hashes build deps	LOCK_REQUIRED
packaging/public-plugin/derivations.json	ADD	UPG-P01	owner-approved frontmatter mapping	DERIVATION_APPROVAL_REQUIRED
tools/freeze_public_plugin_source.py	ADD	UPG-P01	pin commit/tree/all skill hashes	NO_CORE_CHANGE
tools/build_public_plugin.py	ADD	UPG-P01	secure deterministic projection	F01_TO_F05_MUST_PASS
tools/build_web_fallback.py	ADD	UPG-P02	single document projection no truncation	FREE_UAT_REQUIRED
tests/test_public_plugin_packaging.py	ADD	UPG-P03	14 synthetic mutation tests	TRUE_CHECKER_REQUIRED
tests/test_web_fallback.py	ADD	UPG-P03	4 fixture cases	TRUE_CHECKER_REQUIRED
docs/install/README.md	ADD	UPG-P02	one install SSOT with real UAT	HOST_UAT_REQUIRED
docs/install/PIPD_AGENT_INSTALL_PROMPT.md	ADD	UPG-P02	single prompt	PROJECT_SCOPE
README.md	MODIFY	UPG-P02	only two main install routes	NO_FALSE_PUBLIC_LINK
.github/workflows/public-plugin-verify.yml	ADD	UPG-P03	read-only gates	RULESET_REVIEW
dist/plugins/<owner-version>/*	GENERATE	UPG-P04	candidate artifact and receipt	EXTERNAL_NOT_EXECUTED
dist/install/PIPD_WEB_FALLBACK.md	GENERATE	UPG-P02	one exact fallback MD	REAL_ASSET_NOT_EXECUTED
```

## Appendix D — checkrun_contract.tsv

```tsv
required_check	check_name	reporter_role	required_raw_fields	missing_evidence_disposition
UPG-G00	SOURCE_FREEZE	RELEASE_OWNER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	TEMP_CLOSED
UPG-G01	SOURCE_IMMUTABLE	INDEPENDENT_CHECKER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G02	EXACT_SKILLS	CHECKER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G03	SEMANTIC_PROJECTION	TQAEP_CHECKER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G04	PLUGIN_FORMAT	PUBLIC_PACKAGING_CHECKER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G05	RELEASE_PROVENANCE	RELEASE_CHECKER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G06	SKILL_BEHAVIOR	INDEPENDENT_TQAEP	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	FAIL
UPG-G07	WEB_CONSUMER	PLUS_FREE_UAT	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	TEMP_CLOSED
UPG-G08	AGENT_CONSUMER	FOUR_HOST_UAT	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	TEMP_CLOSED
UPG-G09	PUBLIC_RELEASE	HUMAN_PUBLISHER	commit,tree,zip_sha256,actor,tool_pin,exit_code,raw_stdout_sha,raw_stderr_sha,fixture_sha,verdict	PUBLIC_HOLD
```

## Appendix E — audit_patch_ledger.tsv（F01–F14×R2實質位置）

```tsv
audit_finding	substantive_target	test_or_gate	not_yet_proven
F01	§7.2,§7.3	TR-04	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F02	§7.2,§7.3	TR-05	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F03	§7.2,§7.3	TR-06	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F04	§7.1,§7.2	TR-07,TR-08	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F05	§7.2,§7.3	TR-09	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F06	§7.3,§9.2	TR-11..40	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F07	§8.2..8.4	TR-27..32	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F08	§7.4,§8.1	TR-19..21	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F09	§4.2	OSS_REGISTER	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F10	§1,§12	A01..A42	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F11	§5.2,§9.5	UPG-G09	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F12	§2.2,§9.5	TR-15,TR-16	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F13	§5.3,§9.3	INDEPENDENT_REPLAY	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
F14	§0,§3.4	NO_S4_PASS	REAL_DEPLOYMENT_AND_INDEPENDENT_CHECK_PENDING
```

## Appendix F — Source-focused Fullscan term-family totals、機器稽核限制

下表是物理全文關鍵字命中計數（每份文件每個詞族每命中一行計一次，非去重 requirement count）。同一文件可被多詞族同時命中，不能累計成已閉合規範。詳見 Appendix A 的全量 SHA 元資料。R2 每個要求的實質敘述在 §0–12 已具名定位，具數字結果以 §7 合成測試/§10 CR 區分。即使字面命中 100%，仍需要 PIPD 官方 Host、Portal、Repo 原始實行的獨立證據。

| Term family | Matched lines across mounted documents | Interpretation |
|---|---:|---|

| `INSTALL_UX` | 27422 | LEXICAL_INDEX_ONLY |

| `PLUGIN_FORMAT` | 937 | LEXICAL_INDEX_ONLY |

| `RELEASE` | 29987 | LEXICAL_INDEX_ONLY |

| `SECURITY` | 5979 | LEXICAL_INDEX_ONLY |

| `TQAEP` | 29278 | LEXICAL_INDEX_ONLY |

| `OPEN_SOURCE` | 5511 | LEXICAL_INDEX_ONLY |

| `AGENT` | 7763 | LEXICAL_INDEX_ONLY |

| `REQUIREMENT_ATOMS` | 32295 | LEXICAL_INDEX_ONLY |

## Appendix G — Synthetic execution evidence and reproducibility boundary

本輪在無寫入 GitHub／不觸碰使用者 S4 Repo 的**合成 temp Git fixture** 中執行 `python -m unittest`。結果：`test_public_plugin_packaging.py` **14/14 PASS**（F01 假 PNG、F02 schema arbitrary、F03 非法 frontmatter、F04 null/mismatch source commit、F05 symlink sentinel、F06 missing/extra/source symlink、invalid name、Publisher placeholder、root overlap、2x deterministic、approved derivation、schema pin），`test_web_fallback.py` **5/5 PASS**（exact source embed、too-large no truncation、bad source hash、symlink target unchanged、stale release stamp）。這是 Maker 參考程式的單次局部測試；仍缺使用者帳號／Portal／真正 PIPD Repo build／獨立 Checker 再測/跨 OS tests。任何 `.log` 路徑只保留於本次容器，**不等於**簽署的外部 evidence return pack。

```text
synthetic_packaging: 14 tests, OK
synthetic_web_fallback: 5 tests, OK
source_main_readback: 224591431a164ab72a9423cd180e417e8a762403
source_tree_readback: 1a9fcb94a42eb589e405c2453793be986419d4cb
repo_mutation: NOT_EXECUTED
real_plugin_package_build: NOT_EXECUTED
official_vendor_plugin_validation: NOT_EXECUTED
public_portal_submit_review_publish: NOT_EXECUTED
all_consumer_hosts: NOT_EXECUTED
independent_s4_full_pass: NOT_GRANTED
```

**Final S4 claim ceiling**：`R2_BLUEPRINT_UPGRADED_WITH_SYNTHETIC_CODE_TESTS / PRODUCTION_EVIDENCE_PENDING / RELEASE_FAIL_CLOSED`。此次 R2 可供 HGK/Codex 以受控 route-out 實作的完整設計底稿，但不可被視為已具體完成 Public Plugin 外掛、官方審核或原 S4 實體驗收。

### Appendix G.1 外部來源文獻（SUPPORT，不替代 Normative）

- https://developers.openai.com/plugins/build/plugins
- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agentskills.io/specification
- https://developers.openai.com/plugins/build/skills
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://docs.github.com/en/actions/reference/security/secure-use
- https://github.com/ossf/scorecard/blob/main/docs/checks.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md
- https://github.com/vercel-labs/skills
- https://code.claude.com/docs/en/skills
- https://github.com/github/spec-kit/blob/main/docs/reference/bundles.md
- https://github.com/Fission-AI/OpenSpec/blob/main/CHANGELOG.md
- https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md
- https://github.com/open-gsd/gsd-core
- https://github.com/garrytan/gstack
- https://github.com/mattpocock/skills

---

**最終裁定**：`R2_DOCUMENT_REPAIR_COMPLETED / A01–A42_DESIGN_MAPPED / R1_F01–F05_SYNTHETIC_REGRESSIONS_REPAIRED / NO_NEW_STAGE / NO_MCP / PUBLICATION_HOLD / INDEPENDENT_REAUDIT_REQUIRED`。

