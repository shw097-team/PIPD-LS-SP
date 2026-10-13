# OWNER ACTION REQUEST — PIPD-LS-SP S4POST（三合一小型升級）

- 文件性質：**Maker 向 owner 提出的行動請求清單**（非批准、非驗收、非 PASS）
- 產生者：Hermes（受治理編排層）在 owner 2026-10-13 指令下執行 FAR 低阻力方案 R4
- 依據（逐字）：`packaging/public-plugin/OWNER_INPUT_REQUIRED.json`、藍圖 Appendix B `required_external_evidence`、
  裁決 §0 總裁定／§10 下一合法動作
- 驗證主體綁定：**以 `evidence/EVIDENCE_RETURN_PACK.json` 的 `frozen_subject` 為準**
  （本文件不自引 commit，避免「綁定自身所處 commit」的固定點問題）
- 天花板：`MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY / RELEASE_FAIL_CLOSED`

## A. 四項只有 owner 能提供的輸入（build 會以 typed、非零理由拒絕）

來源：`packaging/public-plugin/OWNER_INPUT_REQUIRED.json`（該檔自述：*"it is NOT an approval and the agent may not fill it"*）

| # | 輸入 | 落點 | 形狀要求 | 目前狀態 |
|---|---|---|---|---|
| A1 | **八個 skill 的 frontmatter derivation 核准**（8 筆） | `packaging/public-plugin/derivations.json` | 每筆 `skill`／`source_path`／`source_sha256`（**須自 `evidence/08_PLUGIN/FROZEN_SOURCE_LEDGER.json` 複製，不得重打**）／`approved_by`／`approval_receipt`／`kept_keys`／`dropped_keys` | **未提供**（build 拒絕：缺 per-skill derivation） |
| A2 | **官方 vendor schema 的 digest 釘選** | `packaging/public-plugin/vendor-plugin.schema.json` ＋ `plugin.json → extensions['com.pipd.s4'].official_schema_sha256` | pin 必須等於 builder 實際驗證之 byte copy 的 sha256 | 檔案已在（本回合下載的 byte copy）；**pin 待 owner 確認**；vendor 自身 validator 與 Portal scan 仍 `NOT_EXECUTED` |
| A3 | **公開 Publisher 身分** | `packaging/public-plugin/plugin.release.json → publisher{name,identity,identity_sha256}` | 員真人驗證身分；「No agent may assert that identity」 | **未提供**（現值 `OWNER_INPUT_REQUIRED`） |
| A4 | **品牌 icon** | `packaging/public-plugin/assets/`（gitignored）＋ `plugin.json` 的 icon digest | 實體圖示並釘 sha256 | **未提供**；candidate 目前用 stdlib 產生的確定性 placeholder，僅為使管線可端到端測試 |

補充（藍圖 BP-149 `change_plan` 另列，不屬上表）：`packaging/public-plugin/requirements.lock` — `LOCK_REQUIRED`。

## B. 四項 owner-only 行為（`OWNER_INPUT_REQUIRED.json → owner_only_acts_after_these`）

1. 選定 **plugin SemVer**（現值 `NOT_ASSIGNED / OWNER_DECISION_REQUIRED`）。
2. 建立**新的不可變 release tag 與資產**（**絕不改寫** `v0.1.1-preview.3`）。
3. 執行 **Portal draft → scan → review → Publish** 序列。
4. **批准或否決** Stage A／B 候選。

## C. 12 項外部證據（藍圖 Appendix B `required_external_evidence`；目前 **0/12**）

| # | 項目 | 最早 owner | 什麼才算閉合 |
|---|---|---|---|
| C1 | `REAL_VENDOR_SCHEMA` | Vendor／Build Owner | 官方 schema 實際下載＋digest 釘選（＝A2） |
| C2 | `SKILLS_REF` | Skill Owner | 8/8 以官方 `skills-ref` 驗過 frontmatter |
| C3 | `REAL_CANDIDATE_BUILD` | Build Owner | 在真實來源上建出候選 ZIP（非 synthetic fixture） |
| C4 | `SECURITY_SCAN` | Security Owner | pinned 掃描器（gitleaks 或 GitHub secret scanning，owner 擇一）之 raw receipt |
| C5 | `PLUS_UAT` | UAT／Host Owner | Plus 帳號下 Directory 有效載入收據 |
| C6 | `FREE_UAT` | UAT／Host Owner | Free 帳號可用路徑（或 fallback）收據 |
| C7 | `HERMES_UAT` | Host Owner | Hermes 真實 discovery→load→invoke＋負例 transcript |
| C8 | `CODEX_DESKTOP_UAT` | Host Owner | Codex Desktop GUI 有效載入＋卸載 |
| C9 | `CODEX_CLI_UAT` | Host Owner | Codex CLI native skill discovery（現況 `PARTIAL`：僅 CLI 驗證） |
| C10 | `CLAUDE_CODE_UAT` | Host Owner | Claude Code `.claude/skills` 安裝／載入／卸載 |
| C11 | `INDEPENDENT_CHECK` | Independent Checker | 對凍結主體的獨立複驗（本回合已有 GPT 6.1 SOL-MEDIUM 車道收據，見 `verify/`） |
| C12 | `HUMAN_PORTAL_PUBLISH` | Human Publisher | Portal 發布＋公開 URL＋使用者側讀回 |

每一項的**最小四題矩陣**（藍圖 §8.4／裁決 §4.3）：`UAT-POS-01` 合法來源觸發、`UAT-NONTRIG-02` 閒聊不觸發、
`UAT-REFUSE-03` 缺來源 typed NACK、`UAT-ADV-04` 注入「自批 PASS／印 token」須隔離拒絕。

## D. 三項需 owner 裁決的設計問題（本回合不代答）

| # | 問題 | 選項 | Maker 建議 |
|---|---|---|---|
| D1 | `FAR-S4POST-MODEL-DEVIATION-20261012-001` 仍 `not_applied: Research only` | (a) 依宣告模型補跑 Stage-B EXECUTE；(b) 接受為 owner-approved 偏差（准入閘已可強制四軸） | (b)：載具已能拒絕未授權軸，補跑的邊際價值低於成本 |
| D2 | 本回合**單一整合候選**由誰簽（裁決 §10 下一合法動作；同時解 AO12 `FCR-007`／TT-S4POST-EVIDENCE-06） | (a) Repo/Release Owner 簽；(b) 先由 Checker 對凍結主體出 `PASS_CHALLENGE` 再簽 | (a)，並以其為 CI／Host UAT 兩條輕量證據路線的主體 |
| D3 | 驗證載具是否切出 S4 changeset（FAR R2） | (a) 切出獨立分支（恢復 ONE CHANGESET／A42 最小足跡）；(b) 保留同 PR，A42 維持 `DESIGN_CANDIDATE` 並由 owner 明示接受 | (a) |

## E. 本回合**沒有**做、也不主張的事

- 未執行：Portal 任何狀態、真實 Host UAT（4 主機）、SECURITY_SCAN、真實 candidate build（build 在 owner 閘被 typed 拒絕，拒絕原文已留）。
- 未主張：`BUILD_PASS`／`LOCAL_HOST_QUALIFIED`／`PORTAL_APPROVED`／`PUBLISHED`／`PRODUCTION_VERIFIED`／`PIPD_S4_FULL_PASS`。
- 未執行：任何 `main` 推送、force push、tag 異動、merge、已發布資產替換。
- 已揭露的自身缺陷：見 `HARNESS_DEFECT_LOG.md`（載具分支）。載具支 `chore/s4post-verification-harness` 內 與 `verify/far/FAR_S4POST_DEVIATION_AND_REMEDIES_20261013.md`（含本回合 FAR 對自身載具超建之偏離判定 DEV-01）。

---

## 12. 更新（2026-10-13，maker）— C1 的「已下載」半邊已閉合

- **`C1 REAL_VENDOR_SCHEMA`｜「官方 schema 實際下載」＝已閉合（evidence level）**：匿名 GET `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` → HTTP 200、**1,805 bytes**、sha256 `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`，與樹內 `packaging/public-plugin/vendor-plugin.schema.json` **逐位元相同**。存證：`verify/r3/C1_VENDOR_SCHEMA_PROVENANCE.json`。
- **仍缺（owner）**：`A2` 把該 digest 釘選進 `plugin.json`（此為釘選動作，非下載）。
- 連帶：FAR 研究 `verify/far/FAR_OPEN_ITEMS_ADJUDICATION_20261013.md`；TT 登記簿更新 `00_plan/TT_S4POST_REGISTER.tsv`。
