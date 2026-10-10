# R5R — CE-1／CE-2 修補＋CODEX CLI 獨立驗收｜輪次總結報告

- 輪次：`R5R-20261010-s4-ce-repair-and-codex-verify`
- 契約：`PIPD-LS-SP-R5R-CE-REPAIR-20261010`
- 控制平面：HG-KSEOS（唯一）；canonical Hermes 為受治理 Runtime／Orchestration Plane
- 分支：`r5r-ce-repair`（worktree `PIPD-r5r-repair-wt`）
- HGK admission：6/6 FROZEN、0 error、checkpoint `CK-20261008-3927763C`
- 收據 commit：見 `git log r5r-ce-repair`

---

## 0. 一句話結論

CE-1／CE-2 **兩者皆已修補並在真實 wheel 安裝上端到端證明**，過程中另發現並修掉**第三個同類站點**與**一條驗收官抓到的放寬**；獨立驗收官第一輪判 **FAIL**、第二輪重驗 **PASS（6/6）**。**修補後的 wheel 未發布**，`v0.1.0-preview.1` 未被改寫。

---

## 1. 模型方案實際落地（含偏離，逐項揭露）

| 車道 | 本輪要求 | 實際使用 | 與 registry 一致性 |
|---|---|---|---|
| PLAN | DeepSeek V4.1 Flash（OPENCODE GO），在 Hermes 內 | `opencode-go/deepseek-v4.1-flash` | **偏離**：registry 宣告 PLAN＝`openai-codex/gpt-6.1-sol`；`global_overrides_permitted: false`。屬**操作者指定偏離**，不得引用為 registry 合規路線 |
| EXECUTE | CODEX CLI，`opencode-go/deepseek-v4.1-flash` | 同左，經 **受制裁啟動器** `start-hgk-hermes.ps1 -Action Write` | 一致。直接呼叫 `codex.exe` 會被 policy 擋（`CreateProcess` 全拒）；啟動器的 Write 閘門對 OAuth 路線 fail-closed（`ERR_EXECUTE_OAUTH_BOUNDED_WRITER_ADMISSION_REQUIRED`），故 writer 只能是制裁配對 |
| VERIFY／SECURITY | CODEX CLI，GPT 6.1 SOL-MEDIUM（OpenAI OAuth） | `openai-codex/gpt-6.1-sol`、effort medium、**獨立 CODEX_HOME**（非 EXECUTE lane 的） | registry 的 `VERIFY_SECURITY` **arm B**，`automatic_selection: false`＝僅可由操作者選取；本輪即操作者指定，非自動挑選 |

`maker_checker_distinct_model`：maker＝`deepseek-v4.1-flash`、checker＝`gpt-6.1-sol`，**互異且滿足**。

registry 的拒絕條款「arm B 檢查 **PLAN 製物**時必須被拒」**未觸發**：受檢物由 EXECUTE lane 依 bounded work order 產出，PLAN 只寫 work order 與 FAR，未寫受檢程式碼。此為可查核主張，非假定。

---

## 2. FAR 研究結論（`far/R5R_FAR_CE_REPAIR_QUICKSTUDY.md`）

**CE-1**（`validate --bundle` 在無 `schemas/` 的 cwd、無 `--root` 時 exit 2）
根因：`cli.py` 的 `--root` 預設 `Path.cwd()`，`validate` 無條件吃 `<root>/schemas`；`doctor` 走 registry 解析鏈（OVERRIDE→INSTALLED→SOURCE）。兩者對「schemas 在哪」不一致。
**採 A1**：`validate` 改走 registry 解析鏈，`<root>/schemas` 僅在**真的含 `registry.json`** 時優先（回報為 `WORKSPACE`）；解析不到則具名 fail-closed。
否決 A2（只補文件）、A3（`--root` 改指套件目錄，會破壞 workspace 模式）、A4（不改變事實）。

**CE-2**（四編譯器原始 stdout 組成的 bundle 被 `validate` 拒收）
根因：`pipeline` 以註解宣告 `_profile_meta` 為「non-record sidecar, stripped before validation」，`_body_hash` 確實剝離，但 `validate_record` 對**未剝離**的原件做 schema 檢查，而 `PI-PKG` 為 `additionalProperties: false` → 工具拒絕自己的輸出。
**採 B1**：在 schema 檢查前剝離真正非記錄的 sidecar（此即程式自己宣稱的行為），並將清單收為單一定義。
否決 B2（停止輸出 `_profile_meta`，會斷 `run_s1_slice.py` 的讀取並使升級紀錄消失）、B3（改動 canonical schema＝契約變更且違反 repo 自訂慣例）、B4（全面容忍未知鍵＝削弱所有 family 的契約）。

---

## 3. 實際修補（全部由 EXECUTE lane 產出，PLAN 逐次自審後才入 commit）

1. **CE-1**：`registry.resolve_for_validate(root)`；`validate` 回報 `schema_source{mode,path,tried}`，解析不到時具名 `SCHEMA_RESOLUTION` fail-closed。
2. **CE-2**：sidecar 清單單一定義，`_seal`／`_body_hash`／`validate_record` 共用；schema 檢查跑剝離後副本。
3. **同類第三站（PLAN 的 E2E 探針抓到）**：`workspace.init_workspace` 在剛建立**空的** `<root>/schemas` 後就拿它 `load_registry` → `pipd init` 在任何新／安裝態 root 必失敗。改走同一解析鏈並回報來源。`projection.py` 的 `root/schemas/registry.json` 讀取**刻意不動**（其契約是從指定 canonical tree 載入物件），已寫明 out-of-scope。
4. **驗收官反例 `CE-CODEX-TRACE-WIDENING`（第一輪 FAIL 的那一條）**：原修補把「雜湊排除集合」與「schema 檢查剝離集合」混為一談。只有 `PI-PKG` 宣告 `trace`，其餘三個契約不宣告 → `additionalProperties: false` 不再觸發，未宣告的 `trace` 被靜默接受。拆為 `HASH_EXCLUDED_FIELDS`（雜湊用）與 `NON_RECORD_SIDECARS`（僅 `_profile_meta`，schema 檢查唯一剝離集合），`trace` 恢復受各契約 schema 強制。
5. **`tracked_files` 啟發式（本輪自己造成的）**：本輪提交證據使追蹤檔數由 `9bd33a1` 的 **996** 增至 `afb29d0` 的 **1015**，觸發 `assertLess(n, 1000)`。改為直接斷言「無任何追蹤路徑屬版本控制機制」（真正意圖），保留寬鬆 25,000 上限，並新增測試證明守衛確實會觸發。EXECUTE lane 曾誤判此失敗為「既有且無關」，**該判定已量測推翻並在紀錄中更正**。

---

## 4. 證據（可獨立複核）

| 項目 | 結果 | 位置 |
|---|---|---|
| 完整測試套件 | **321 tests, OK (skipped=3)** | `execute/full_suite.txt` |
| RED（修補前） | CE-1：exit 2 `FileNotFoundError: <cwd>/schemas/PI-PKG.schema.json`；CE-2：exit 1 `PI-PKG/: Additional properties are not allowed ('_profile_meta' was unexpected)` | `execute/red_state.txt` |
| GREEN（修補後） | 同名測試全綠 | `execute/green_state.txt` |
| Maker E2E（真實安裝） | 乾淨 venv、**cwd 無 `schemas/`、不傳 `--root`**：`doctor`／`init`／`intake`／`compile-pi`／`bind-pd`／`compile-ecp`／`compile-tqaep` 全 exit 0；`validate` → `verdict=PASS checked=4 findings=[]`，且 PI-PKG 仍帶 `_profile_meta` | `maker-e2e/maker_e2e_transcript.txt` |
| 反例複現（PLAN 自跑） | 對 PD-PKG／ECP／TQAEP 各加未宣告 `trace` → 三者皆被指名 `trace` 擋下；未動 bundle 仍 PASS | `maker-e2e/trace_widening_probe.py` |
| 受測物 | `pipd_ls_sp-0.1.0-py3-none-any.whl` sha256 `d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f`，41 members，`build_input_commit` `1ab17d1` | `dist/WHEEL_MANIFEST.json` |

---

## 5. 獨立驗收（CODEX CLI，`gpt-6.1-sol`／OpenAI OAuth／medium／獨立 CODEX_HOME）

**第一輪 — `VERDICT: FAIL`**（`verify-codex/verdict.json`）
- Claims 1–7、9 **PASS**：wheel 真的裝進乾淨 venv 且 `doctor` exit 0；安裝態真的跑完整設計鏈（含 checker 自建 scratch git repo 供 `bind-pd`，自撰輸入）；CE-1 成立且帶 `registry.json` 的 `--root` 仍優先；CE-2 成立；三種篡改仍 fail-closed（缺 required identity、junk key、body 改而未重簽 `content_hash`）；`v0.1.0-preview.1` 仍指向 `cc9bf574…` 且 wheel 仍為 `c450dbef…`；新 `.git` 守衛比它取代的尺寸上限更強。
- Claim 8 **FAIL**，反例 `CE-CODEX-TRACE-WIDENING`。checker 以**已發布 wheel 的 validator** 直接對照，故為比較性證據而非臆測。

**第二輪 — `VERDICT: PASS`（6/6，零反例）**（`verify-codex-2/verdict.json`）
- 重用自己先前的 byte-level fixtures；額外測 15 種 `trace` 值變體（`null`／`[]`／`false`／`""`／`{}` 等）**全部被拒且指名 `trace`**；並確認已發布 wheel 對同批紀錄亦有相同 findings。
- 讀新 wheel 內 `validate.py`／`pipeline.py`／`registry.py` 原始碼，確認 19 個打包 schema 與已發布**逐位元相同**，並確認 `_profile_meta` 容忍**不是** PI-PKG 特例。
- 主動揭露一項未變更的既有寬鬆：PI-PKG 的 `trace` schema 為 `{}`，故物件形 `trace` 在新舊 validator 皆通過——**非**本輪造成的放寬。
- 明示 `checker_lane_disclosure`：同一 checker 車道、未參與建置、僅就上述 claims 重驗。

**⚠ 天花板**：第二輪是**同一 checker 車道重驗自己的反例**，非全新驗收官。這是反例關閉的正規做法，但**不構成**新的獨立 officer 意義。

---

## 6. 真實可行性（使用者要求「順便驗證實際安裝、執行的真實可行性並記錄」）

**結論：可以，但有落差。** checker 以非建置者身分，確實完成了安裝與全鏈執行。其自述落差：
- wheel **不含 README／quickstart**；`--help` 只列旗標。
- 需自行推得：`--source` 必須是**存在的檔案路徑**（非任意標籤）；編譯器把 JSON **印到 stdout**，須自行存檔並按契約 family 包成 bundle；`bind-pd` 需**已提交**的 git repo；`compile-tqaep` 需**互異的 maker/checker** 加**非空 receipt**。
- 型別化錯誤碼在 `--source`／receipt 兩處幫上了忙；package 內文件未提供端到端 quickstart。

**已記錄，未於本輪修補**（屬交付物文件化問題，非本輪修補範圍）。

---

## 7. 申報天花板（明確不主張）

- ❌ **修補未交付使用者**：wheel 仍 `0.1.0`、**未發布**；`v0.1.0-preview.1` 未被改寫。已發布的 preview 仍**帶著它當時出貨的 CE-1／CE-2 缺陷**。交付需在**新的 Owner grant** 下開後繼 release。
- ❌ **「writer 跑在 deepseek-v4.1-flash」不可升級為「後端權重已驗證」**：啟動器自身的回條就載明 `transported_model: "opencode-go/"` 且 `transported_model_is_backend_weights_proof: false`。本輪對 writer 模型的主張天花板僅止於「車道被釘在該制裁配對、前門如此回報、transport 如此承載」。**無任何後端權重證明**。四趟回條原文存於 `execute/launcher_receipts.json`（四趟的 gate 來源雜湊、codex 執行檔雜湊、human config 雜湊完全一致）。
- ❌ **checker 車道沒有對應的啟動器回條**：因啟動器的 Write 對 OAuth 路線 fail-closed，checker 是直接以自己的 CODEX_HOME 呼叫（它不是 writer）。其來源證明是 CLI 自身輸出與 `verify-codex/`、`verify-codex-2/` 內的 JSONL 與 verdict.json。此不對稱已載明，避免被誤讀為 checker 亦受啟動器認證。
- ❌ 未進行**安全性審查**（`cso`／`hgk-security` 角色未行使）：無供應鏈／相依／CVE 掃描。
- ❌ registry 中 PLAN 與 EXECUTE 的 `admission_status` 仍為 **UNPROVEN**。
- ❌ `DEL-018 RELEASE_MANIFEST@1` 仍 FAIL／EVIDENCE_GAP；`PARTIAL_CHALLENGE` 維持 28/10/19；`FULL_S0_S4_INDEPENDENT_PASS`／`G_RELEASE_FULL_PASS`／`PRODUCTION_VERIFIED` 未授予。
- ❌ 未進行 S5–S8 live execution／host-native 認證／其他平台驗證。
- ✅ 授予的天花板：**`R5R_CE_REPAIR_LOCALLY_VERIFIED_AND_INDEPENDENTLY_RE_VERIFIED_CANDIDATE_ONLY`**。

---

## 8. 副作用與已揭露事項

1. 四次 bounded-writer lane 執行，經受制裁 EXECUTE 前門，模型釘死 `opencode-go/deepseek-v4.1-flash`；日誌於 `%LOCALAPPDATA%/HG-KSEOS/logs/codex-write-*.log`。
2. 兩次獨立 checker 執行，**各自獨立的 CODEX_HOME**（非 EXECUTE lane 的），原生 OpenAI OAuth。
3. writer lane 曾從**本機離線 wheelhouse** 對 repo 的 Python 3.11 解譯器安裝 `jsonschema`（否則 `validate` 路徑無法被測試），已於其 SUMMARY 自述。
4. 僅在分支 `r5r-ce-repair` 產生 commit；**`main` 未被觸碰**、**既有 tag 未被觸碰**。
5. 追蹤檔案 `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` 曾兩度被執行設計鏈弄髒，**兩次皆已還原**，未進入任何 commit。
6. **無背景程序遺留**；`v0.1.0-preview.1` 未做任何寫入。

---

## 9. 治理表面

- **KANBAN**：board `pipd-r5r-20261010`；swarm root `t_c9975958`（5 workers＋verifier＋synthesizer）。
- **SWARM**：EXECUTE lane 與 VERIFY lane 為**真正不同模型**的並行車道，checker 第一輪即產出 maker 未見的反例。
- **GSTACK**：`surface/GSTACK_R5R_ROUTE_READBACK.json` — registry `HGK-LANE-ROUTING-REGISTRY/1` epoch 15（status CANDIDATE）、逐 flow 的 `route(flow)` 證據、兩條**已申報路線偏離**、四條 `hard_deny` 舉證。本機**無** `gstack` 執行檔，`authority_ceiling: NO_ADOPT_CONTROL_PLANE`。
- **OPENSPEC**：`openspec/changes/pipd-ls-sp-r5r-ce-repair-and-codex-verify`（`openspec validate` → valid），tasks 逐項附證據指標。
- **CODEX**：sealed lane 作為 tracked writer，僅經 work order 寫入，不自驗、不自收。

---

## 10. 建議的下一步（皆需 Owner 裁決）

1. 在**新的 Owner grant** 下開後繼 release（如 `v0.1.0-preview.2`），把本修補交付使用者；**嚴禁**移動或改寫 `v0.1.0-preview.1`。preview notes 應載明：已發布版本仍帶 CE-1／CE-2，本版才修。
2. 針對**重新可重現建置**單獨開輪次：本機重建 sha 與已發布 sha 不一致（`e49d38e5` vs `c450dbef`），本輪未處理。`dist/` 為 tracked，值得一併檢視是否應改為建置產物不入庫。
3. 針對**套件內文件**開小輪次：wheel 內補 quickstart，載明 `--source` 需存在的檔案、編譯器輸出須自行按契約 family 包成 bundle、`bind-pd` 需已提交 repo、`compile-tqaep` 需互異 maker/checker＋非空 receipt。
4. 為 `cso`／`hgk-security` 角色補一次**安全性審查**輪次。
5. registry PLAN 路線偏離與 arm B 的選取，建議在 registry 內補記（本輪已於 GSTACK 讀回申報，但 registry 本身未動）。
