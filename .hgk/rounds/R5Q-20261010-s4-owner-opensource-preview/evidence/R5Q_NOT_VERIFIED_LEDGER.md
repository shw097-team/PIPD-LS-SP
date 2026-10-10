# R5Q「未驗清單」分類與關閉判定台帳

## 0. 裁定與適用範圍

**不是所有「未驗」都需要關閉。** 原始 7 項不是 7 個已確認產品缺陷，也不是新的全量施工清單。依本輪契約，完整獨立測試、57 列全驗、S5–S8、host-native、Windows 全面認證不得因限定 Preview 已發布而標成已驗。簽章／attestation、完整 CVE 掃描及專屬錯誤訊息的補強，不能自動升格為本次發布阻斷。

本文件辨認出：

- **必須維持開啟的宣稱邊界：** 原驗收官沒有重跑完整套件、沒有逐列全驗；10 個 active evidence gaps 與 19 個 deferred 列；S5–S8／PRE-W3／host-native／未驗 Windows 邊角；沒有密碼學 provenance 或完整 CVE 掃描證據。維持開啟不代表永遠不能補驗，而是本輪不能用文件把它們洗成 CLOSED/PASS。
- **必須處置的文件／使用者路徑缺口：** `validate` 的 workspace-local `schemas/` 前提未在本次核讀的公開入口明示；公開 release body 仍說限定獨立驗收 pending，但本地 R5Q 已有獨立收據。後者是狀態敘述不同步，不是 wheel 的功能缺陷。
- **必須保留 FAIL 的既有發行證據缺口：** `DEL-018 RELEASE_MANIFEST@1`。它不是可丟棄的註記；然而契約明確容許本期披露後延後修補。正式 manifest／全 Gate PASS 前必須修，**不是已發布 Preview 的立即 stop-ship**。
- **目前沒有依這 7 項成立的新 stop-ship 產品缺陷。** 「沒有驗」不能推出「一定壞」；本文件亦未證明「一定安全」。若出現 P4／驗收報告 §7.3 的真實反例，立即另走最小 `NARROW_REPAIR`，不能拿 Preview 邊界免責。[P §6 P4、§7；A §7.3、§8]

**受驗身分（來自 R5Q 文件與收據，非本輪重新驗 wheel）：** tag `v0.1.0-preview.1`；release commit `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32`；wheel SHA-256 `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60`；Apache-2.0。最高狀態仍為 `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`；`FULL_S0_S4_INDEPENDENT_PASS`、`G_RELEASE_FULL_PASS` 未授予，`PRODUCTION_VERIFIED` 不宣稱。[F §1–2；R `/subject`、`/claim_ceiling`]

**時間與方法：** 本輪唯讀檢視於 2026-10-10（Asia/Taipei），工具實測時間 `2026-10-10T23:55:40.919938+08:00` 起。本文件是分類與來源稽核，不是新的獨立驗收或 Stage promotion；未執行產品完整套件、安裝 wheel 或缺 schemas 的 CLI 負例。只新增本文件，不修產品、不改既有報告或收據、不操作 git、不 push、不改 GitHub。

## 1. 證據索引與定位規則

以下縮寫均指本輪實際讀取的文件；`L` 為讀檔工具回傳的 1-based 行號。公開 surface 可變，故除行號外另給章節／項目標題。

| 代碼 | 精確來源 | 主要定位 |
|---|---|---|
| F | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/.hgk/rounds/R5Q-20261010-s4-owner-opensource-preview/evidence/R5Q_FINAL_REPORT.md` | §1 claim ceiling；§4 測試；§6.1 checker 邊界；§9 open items；§11 入口修正 |
| R | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/.hgk/rounds/R5Q-20261010-s4-owner-opensource-preview/evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json` | `/claims`、`/not_verified`、`/scope_note`、`/claim_ceiling`；L42–52 |
| P | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/PROMPT/PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md` | §3–5；§6 P3/P4/P6；§8.1 CORR；§8.2 TT |
| A | `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/驗收報告/PIPD_LS_SP_R5P_S0-S4_External_Challenge_CORRECTED_OWNER_OpenSource_Preview_GO_2026-10-10.md` | §0；§5–6；§8–9；§13；附錄 A/B |
| D | 公開 tag `v0.1.0-preview.1` 的 `README.md`，匿名 raw 下載 | 頁首 Preview 警示；`Claim ceiling`；`Preview known limitations` 段落 |
| N | GitHub release asset `PREVIEW_NOTES_v0.1.0-preview.1.md`，匿名實際下載；另讀本地同名檔 | §2；§3 Known limitations #1–8；尾端 Claim ceiling |
| B | GitHub `v0.1.0-preview.1` 的 live release body，公開 release 網頁 | `Install`；`Licence and rights` 的 Third-party 段落；`Known limitations` #1–5；`What this release does not claim` 及其 pending 段落（匿名 HTMLParser 擷取） |
| M | 公開 `main/README.md`，匿名 raw 下載 | 頁首 banner（R3 snapshot，不是安裝入口）與 release 導引 |
| C | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/src/pipd_ls_sp/cli.py` | L39 root；L63–64 validate；L66–73 `--out type=Path`；L164–169 schema 參數；L298–322 typed envelopes |
| V | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/src/pipd_ls_sp/validate.py` | L27–35；L130–148 |
| G | `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/src/pipd_ls_sp/registry.py` | L82–127 resolver；L165–167 explicit schemas_dir |

公開定位（URL 以程式碼形式保留，避免把本地 template 當 live body）：

- B：`https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1`
- D：`https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP/v0.1.0-preview.1/README.md`
- M：`https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP/main/README.md`
- N：`https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/PREVIEW_NOTES_v0.1.0-preview.1.md`

**取證限制：** 匿名 GitHub API 的 release 查詢回 `HTTP 403: rate limit exceeded`；改以公開 release 網頁讀 body 成功，D/M/N 的匿名下載亦成功。B 以匿名 HTML 讀取並擷取 markdown-body；本輪不據頁面上的資產表重宣稱全部下載或重新驗全部 hashes。本地 `release/RELEASE_BODY.md` 是含 `{{TAG}}` 等標記的 template，不能單憑它證明公開揭露；本地 `release/` 下沒有 Preview Notes，實際 notes 位於 repo root，且本輪已讀公開 asset。

## 2. 分類語義與原清單補正

| 類別 | 本文件的判準 | 處置 |
|---|---|---|
| 缺陷 | 已確認違反適用要求的產品行為，或已確認公開文件缺漏／失真 | 應修；另標是立即阻斷、文件修正，或明准延後的證據修補 |
| 宣稱邊界 | 未驗／未授予／明令 deferred 的狀態 | 保留原收據；不得靠刪字或改標籤假關閉 |
| 可選增強 | 本期限定 Preview 不以其為必要條件的新增保障 | 可另排，不把缺少保障等同反例 |
| 方法論註記 | 記錄誰驗了什麼、分支／訊息是否命中 | 保留事實；不作新的產品 Gate |

A §1.2（L51）明確把 `EvidenceGap` 與 `Defect` 分開。以下仍使用使用者要求的四類，但每項的「未驗」與其背後「可修機制」分列，避免把類別混成單一 P0。

原說明稱欄位為 `what_i_did_not_verify`，實際 R5Q JSON 的 key 是 **`not_verified`**（R L42–50），含 7 個 entries；兩者指的是同一清單，不能在稽核時捏造另一個 key。第 3 項應拆成 3a S5–S8、3b host-native、3c Windows 路徑邊角；第 4 項應分離「release provenance 簽章／attestation」與「安裝／啟動自動 integrity readback」，不能以 TT-R5P-02 後者的揭露冒稱前者也完整揭露。第 2 項則應分 28 evidenced、10 active gaps、19 deferred 與混合 Stage 的 S4 seam；不能把 57 列全 deferred，或把 28 evidenced 改成 28 independent PASS。[P §5、§8.1 CORR-04/05；A 附錄 A/B]

## 3. 原始 7 項逐條裁定

### NV-01｜未重跑 repository 完整測試套件

- **主要分類：方法論註記＋宣稱邊界。** 可選增強是由適格獨立 checker 另跑全套；現有「未重跑」不是產品缺陷。
- **依據：** R `/not_verified/0`；P §5 L89 要求先做差異與 affected-only 測試，不因授權／文件變更重做整條工程流程；P §6 P6 L127 明定最小 clean-install 與使用者 smoke。A §0 L19–20、§4 L106–111 區分候選 suite 收據與獨立全驗。
- **判讀：** F §4 L79 記錄 round suite `311 tests, OK (skipped=6)`，不等於 R 的 checker 也跑過。這兩句可同時真實；不得改寫為「整個 round 沒跑測試」，也不得把 maker 的 suite 搬成 checker 的全量 PASS。
- **公開揭露：** N §2 的 deterministic suite 列明為 run in the round；N §3 #2 與尾端 ceiling 明示非 full independent acceptance；D 頁首與 `Preview known limitations` 明示 `PARTIAL_CHALLENGE`；B 的 `What this release does not claim` 不授 full PASS。**「這位 checker 沒重跑全套」在上述公開入口未逐字列出**，但其導出的必要宣稱邊界已揭露，不能說整份 7 條已逐項公開。
- **最小動作／wheel：** 無必修程式動作。若後續全驗，建立新 checker 收據，綁定 exact subject、command、environment、skips、raw log；不覆寫 R 歷史。只補證據不改 wheel。
- **狀態：** `KEEP_ORIGINAL_NOT_VERIFIED / NON_BLOCKING`。

### NV-02｜57 列 SPEC/DEL 未逐列稽核

- **主要分類：宣稱邊界；適用子集可能有證據義務，並非 57 個缺陷。**
- **依據：** P §5 L91 保留 `28 S4_ACTIVE_EVIDENCED / 10 S4_ACTIVE_GAP / 19 DEFERRED_BY_INSTRUCTION` 且 `EVIDENCED ≠ PASS`；P §8.1 CORR-04 L168 明定只驗實際影響 Preview 發布及使用者路徑的適用行；CORR-05 L169 不准把 S4 design seam 一起延後。A §6 TT-R5P-03、§9 CORR-04/05、附錄 A/B 保留逐列責任。
- **必須保留：** 28 是 evidence mapping，不是獨立驗完；10 gaps 不可一刀切全關，也不可一刀切當全阻斷；19 deferred 按指示保留。F §9 L195 使用「Deferred」總括 10 active gaps 與 19 deferred，語義不夠精確；本台帳以 P 與 A 的分類校準，不把 10 active gaps 改成 19 deferred 的同類。
- **真正必做：** 如某行影響必要安裝、安全、授權、當期核心 CLI 或設計 seam，依 CORR-04/05 取得 focused evidence，或保留明確 gap 並判定 user impact。只有真實適用要求違反成立才開修；不能靠這條總述認定所有適用行均已驗，也不能因 checker 沒逐列全驗否定已成立 Preview GO。
- **公開揭露：** B `Known limitations` #2 明列分母及現用子集；D `Preview known limitations` 同列 `28/10/19`；N §3 #2 明列三分類與 `EVIDENCED ≠ PASS`。**已如實揭露整體邊界，未證明每一列 individually closed。**
- **最小動作／wheel：** 查用戶適用行→規範 locator→POS/NEG/raw→exact subject，僅補缺少且確實適用的證據；單純 mapping／測試不改 wheel，若發現功能缺陷才最小程式修補並另版 wheel。
- **狀態：** `KEEP_PARTIAL_CHALLENGE / APPLICABLE_ROWS_ONLY`。

### NV-03｜S5–S8／host-native／Windows symlink/junction/reparse 未驗

| 子項 | 分類與依據 | 公開具體位置 | 本期處置 |
|---|---|---|---|
| NV-03a S5–S8 live、PRE-W3、22 inactive technologies | **宣稱邊界／DEFERRED_BY_INSTRUCTION**。P §3 L68、§4 L80、CORR-08；A §9 CORR-08、§11 W06 | D 頁首及 `Preview known limitations`；N §3 #6；B `Known limitations` #4–5 | 維持 deferred；不執行或假核發 live 認證 |
| NV-03b 全 host-native certification | **宣稱邊界**。P §6 P3 L114 禁止誇稱；A §3 G-S1-SKILLS／G-S3-HOST 區分 projection/mock 與 native | D 頁首；N §3 #6；B `Known limitations` #4 | 只聲明已證 projection/design 範圍，不能把 3 Host packs 的存在當 native PASS |
| NV-03c Windows 全面 symlink/junction/reparse 與 dangling symlink | **宣稱邊界＋非阻斷觀察**。P CORR-06、TT-R5P-01/06；A §6 TT-R5P-01/06 | D `Preview known limitations`；N §3 #3（含 scratch/dry-run 與破壞性反例回報）；B `Known limitations` #4 | 保留未認證邊角；遇真實破壞性反例才 stop-ship，不靠 fail-stop abort 推論資料毀損 |

- **最小動作／wheel：** 現況沒有全量必修。若要擴大認證，另由 Stage/platform Owner 授權 scoped sandbox 正負例、fresh checker 與新收據；若確有 destination safety 缺陷，修該 guard 並重驗 canary／rollback／已測路徑，新 wheel 必須另版，不改原 tag。
- **核心回答：** 本輪把此條無證據關成「Windows／Host／S5 live 已驗」會直接違反 P L114、L128、A §13 的禁止聲明。後來合法補驗不是永遠被禁止；禁止的是**本輪越界施工與無證據升級**。
- **狀態：** `MUST_STAY_OPEN_IN_THIS_ROUND`。

### NV-04｜沒有 attestation/signature；只有手動 SHA-256

- **主要分類：宣稱邊界；新增簽章／可驗 provenance 為可選增強。** 不能把 hashing 本身稱為沒有密碼學演算法；真正未證的是作者／建置來源的可驗認證鏈。
- **依據：** R `/not_verified/3` 明記 no attestation or signature；P §4 ACTIVE 使用 SHA256、readback，§6 P3/P5 要求精確 build/release/wheel binding；A §6 TT-R5P-02 允許下載後人工 checksum 作最低 Preview 保障，§5.2 禁止全量 provenance gate 全綠。A 附錄 B `DEL-019` 仍為 G，不因有檔名叫 PROVENANCE 或工具叫 attestation 就推論有 release signature。
- **公開揭露：** D `Preview known limitations`、N §3 #4 **已明示沒有 install-time/startup cryptographic readback，僅手動 SHA-256**；B `Verify the bytes before you trust them` 提供 hash 流程。**這不等同公開明言 release「沒有 attestation/signature」；本輪核讀的三入口未見該完整句。** 一般 manual hash 邊界已揭露，release provenance 層的否定尚非逐字完整揭露。
- **最小動作／wheel：** 非阻斷的文件增強：在 mutable notes/body 加「未提供 release signature／build attestation，SHA-256 僅供下載一致性核對，不構成來源認證」。若真的做增強，以 external attestation 綁定目前 digest、公開 verifier/identity/trust policy，再由 checker 驗；不得倒填為當時即有。外部簽章可不改 wheel；若新增 runtime auto-check 程式，才需新 wheel 與 focused 回歸。
- **狀態：** `KEEP_UNSIGNED_PROVENANCE_BOUNDARY / OPTIONAL_HARDENING`，不是新 stop-ship。

### NV-05｜未做完整 CVE／供應鏈弱點掃描

- **主要分類：方法論註記＋宣稱邊界；完整掃描為可選增強。** secret-pattern clean 與 destination canary 不等於完整供應鏈無弱點。
- **依據：** R `/not_verified/4` 及 claim 9；P §4 ACTIVE／§6 P4 列 Secret Scan、主要安全 negatives 與真實 stop-ship，沒有把「完整 CVE 掃描完成」列為 Preview 必達；A §11 W06 限 active corpus/tech 與 secret scan，§8 不許無 real counterexample 的全面返工。這是對**本次契約**的適用性判讀，不是對其他 release policy 的通用豁免。
- **公開揭露：** B `Licence and rights` 的 third-party/SBOM 段落明示 declared dependency set 非 transitive closure；D/N 沒有「完整 CVE 掃描已完成」的聲明。**未見在 D/N/B 明言「完整 CVE／供應鏈掃描未做」；SBOM scope 與 CVE coverage 也不是同一概念。** 因而不能宣稱逐項揭露已完整；也不能憑未逐字寫而認定軟體存在 CVE。
- **最小動作／wheel：** 可追加明確 coverage 註記；若後續掃描，記錄 exact wheel/source、resolved dependency closure、scanner/database 時間、 findings 與可達性／影響，由安全 Owner 判斷修補。掃描本身不改 wheel；confirmed applicable vulnerability 需要依機制修補，若變更打包程式／相依條件則新 wheel。未知缺口不能直接標安全 PASS。
- **狀態：** `NOT_SCANNED_FULLY / OPTIONAL_SCAN`。只在真實可利用／契約必達安全反例成立後升級，不自動阻斷。

### NV-06｜無 workspace-local schemas 時的 validate 行為未驗

- **主要分類：方法論註記／證據缺口；另有應修的公開使用前提缺漏。** 這項位於 S4 CLI user path，不能像 S5–S8 一樣整體排除；但目前不足以核定「已確認 installed wheel validate 功能壞」。
- **依據：** P §6 P3 L113 要求乾淨安裝後 `validate`，L114 要求清晰使用者說明；P §8.1 CORR-04 要求適用 user path；A §7.3 列必要 CLI／核心鏈不可用的 stop-ship，§8 則要求 real counterexample。R claim 6 的 PASS 僅覆蓋實際測試條件，不能擴張為任意 root 都成立。
- **已確認的 source 行為：** C L164–166 始終向 `validate_bundle` 傳 `root / "schemas"`；V L143→L29 呼叫 `load_schema`；G L165–167 在 explicit schemas_dir 有值時不走 packaged/source resolver。故僅因 doctor 能報 `INSTALLED`，不能推出 validate 在無 local schemas 的任意 root 自足。此為本地 source inspection，**未重新綁定並執行發布 wheel 的該負例**。
- **公開揭露：** D `Preview known limitations`、N §2 的 validate covered 與 §3、B `Install`／limitations **未明列 `validate` 需要 root 下 `schemas/` 的使用前提**。B 對 installed 自足的描述與 N 的 validate covered 應避免被讀成所有 root 的保證。這不是可援用為已揭露的 Stage 邊界。
- **必須最小處置：** 發布／文件 Owner 先明示已驗 workspace 模型、`--root` 必須含對應 schema surface、doctor 的 installed schema-source 不等同 validate 的解析路徑；取得發布 wheel 的 focused 正負例（有 schemas／無 schemas／missing/corrupt schema，記錄 stdout/stderr/exit，禁止假 PASS）。不須重跑全部 57 列。
- **若確認功能缺陷：** 先確認 normative contract 是否要求 schema-less root 的 installed validate 成功。若要求，最小程式修補是讓無 local schema 的合法 installed 模式使用受驗 resolver，並保留 explicit/local damaged schema 的 typed FAIL；加 focused 回歸。若不要求且有 typed refusal，文件補正與測試即可，不應臆造新功能。無 schemas 的未測狀態不能先寫成已通過或已確認 stop-ship。
- **wheel 影響：** 補公開前提與測試不改已發布 wheel；改 C 的 schema resolution 則影響 wheel 內 CLI，須另版重包、重算 hashes、新獨立 smoke，不可覆寫 `v0.1.0-preview.1`。
- **狀態：** `REQUIRED_DOCUMENTATION_DISPOSITION / FOCUSED_EVIDENCE_OPEN`；目前不核發全功能 defect 或 stop-ship verdict。

### NV-07｜MSYS 專屬 guard 訊息未命中，但仍 fail-closed

- **主要分類：方法論註記；專屬診斷可選增強，非已確認安全缺陷。**
- **依據：** R `/not_verified/6` 明記仍 fail-closed、not a security gap；R claim 9 記錄 MSYS 等 unsafe destinations exit 2、canary intact；C L66/L73 的 `type=Path` 支持 argparse 先轉 Path 的解釋。P §6 P4 與 A §7.3 的 stop-ship 謂詞是任意刪寫／越權，不是特定 message 字串有沒有命中。
- **公開揭露：** D/N 的 Windows 範圍限制已涵蓋未全面認證；但未見 D/N/B 逐字寫 MSYS 專屬 message 的分支深度。此微觀方法註記沒有必須對一般使用者逐分支揭露的本輪條款，不能當成揭露缺陷。
- **最小動作／wheel：** 可選擇先保留原始 `--out` token，於 Path 正規化前產生一致 typed message，或僅補 unit branch coverage。必須保留 fail-closed 與 canary 不變，不得為命中訊息移除其他 guard。只加測試不改 wheel；改 CLI parse／guard 則新 wheel 與 project/export 負例回歸。
- **狀態：** `NON_BLOCKING_METHOD_NOTE`。收據不回寫成「專屬分支已驗」。

## 4. 清單遺漏：不得被 7 項總括吞掉的事項

### SUP-01｜DEL-018 是實際發行證據缺口，但允許延後

**分類：既有證據覆蓋失敗（非已確認產品功能缺陷）；正式 Gate 前必修，本期合法披露後可延後。** F §9 L189–192、P §6 P4 L118、A §5.1–5.3／附錄 B `DEL-018` 都明定 `--check --current` exit 1，漏 `tests/test_git_object_reader.py`、`tests/test_doctor_schema_truth.py`、`tests/test_tqaep_design_positive.py`。

公開 B `Known limitations` #1、D `Preview known limitations`、N §3 #1 均已明列。最小修補是依 A §5.3 更新 evidence manifest/seal、重建 publication projection、綁定新 commit/tree、`--check --current` exit 0、focused readback；不為此重寫 19 schemas／8 skills／13 CLI。不改 runtime/member 時 wheel bytes 可不變，但 release identity／外部 evidence 必須正確重新綁定。本輪不執行修補，不發 DEL-018 PASS。若 HGK policy 不准例外，只能真正的 Policy Owner 路由或停 `RELEASE_POLICY_BLOCKED`，不能改 Gate。[P §4 CONDITIONAL/DEFERRED、§6 P4]

### SUP-02｜checker lane 不符原計畫

**分類：方法論註記＋流程資格證據邊界。** F §6.1 L132–138 明定原計畫是 `GPT 6.1 SOL-MEDIUM` via CODEX CLI，實際 R `/evaluator/model` 為 `deepseek-v4.1-flash`。不要把 process independence 冒稱 planned-model SoD 已滿足。若要聲明嚴格 model SoD 合規，須指定模型 checker 新唯讀收據；補驗不改 wheel。本輪核讀 D/N/B 未見該模型偏離的明確揭露；可以後續公開受限驗收摘要揭露，不因此自封 full pass。

### SUP-03｜mutable 入口修正不在原收據範圍內；live body pending 已不同步

**分類：前半為正確宣稱邊界；後半為應修的公開文件狀態缺陷。** R `/scope_note`（L51）及 F §6.1 L139–144 說 checker 在 §11 的 `main README`／live body 修正之前執行；修正由 round 自己 anonymous readback 覆核，不是該 checker 重驗。F §11 L249 記錄後續 `12/12 PASS`，這不會自動變成 independent checker 12/12。

本輪實讀 B 的 `What this release does not claim` 後段仍說 independent acceptance pending；但 F §1 L22、§6.1 及 R `/overall` 已有 `PASS_ONLY_THE_ABOVE_CLAIMS`。**若發布 Owner 採用這份現存收據，live body 的 pending 需同步更正**：改成收到 immutable-subject-only 限定收據，並寫清模型偏離、未驗 7 項及 mutable 修正未含在原收據中；或明確說 pending 指哪一項後續補驗，不再混稱所有 independent acceptance 都未收到。這是事實同步，不能藉此升成 FULL PASS。

最小修補僅 mutable release body／受影響公開說明；修改後匿名 readback exact surface。**不影響 wheel、不可修改原 R 或移動 tag。** 本輪不代為修改，故仍列 `OPEN_DOCUMENTATION_FIX`。M 頁首已明確指 Preview tag，N §3 #8 亦已揭露 main 為 R3 plus banner，不能再把入口修正本身列為尚未執行的缺陷。

## 5. 關閉／保留／增強的決策矩陣

| ID／集合 | 現在必須修或補處置？ | 現在必須保持開啟？ | 何時才可合法關閉 | wheel 影響 |
|---|---|---|---|---|
| NV-01 | 不要求獨立全套重跑 | 原 checker 的未重跑事實、FULL PASS 邊界 | 新受綁定的合法全套收據；歷史不改 | 純測試無 |
| NV-02 | 只處置真正適用 Preview 行與混合 S4 seam | 10 gaps、19 deferred、非 57/57 邊界 | 每項適用條款之證據或合法 stage 處置 | 依真實修補 |
| NV-03a/b/c | 無反例不展開全量施工；限制需保留公開 | 是，本輪未授 Stage/native/全面 Windows | 另案有權 Owner + scoped tests + 合格驗收 | 驗證本身無 |
| NV-04 | 不要求簽章；可加 release unsigned 註記 | 無 provenance 認證事實 | 真實 attestation/signature + verifier 證據 | external signature 無 |
| NV-05 | 不要求完整 CVE scan；可加 coverage 註記 | 無完整 scan verdict | exact subject／dependency closure／時效掃描與裁定 | scan 無 |
| NV-06 | **要補公開 validate 前提與 focused 處置；不先當功能已壞** | 缺 schemas 負例未驗狀態 | 文件明確 + 發布 wheel focused evidence；若真缺陷則修後回歸 | 文件無，程式修正有 |
| NV-07 | 專屬訊息可選改善 | 未命中特定分支的歷史事實 | 新訊息／分支測試收據，不倒填 | 只測試無，改程式有 |
| SUP-01 DEL-018 | **正式 Gate 前必修；本期准延後** | `FAIL/EVIDENCE_GAP` | reseal/rebind + current-check exit 0 + appropriate checker | evidence-only 可無 |
| SUP-02 model lane | 要聲明 planned SoD 時必補 | model mismatch 邊界 | 指定 lane 新驗；不刪原偏離 | 無 |
| SUP-03 mutable/pending | **公開 pending 狀態要更正；mutable independence 不假關閉** | 原收據不涵蓋後續 mutable 修正 | 更正並 readback；要獨立驗 mutable 再取新收據 | 無 |

### 必須保持開啟的精確含義

1. 保留歷史 R `not_verified` 七項，不用新文件改它曾經驗過的範圍。
2. 本輪維持 `PARTIAL_CHALLENGE`、`DEL-018 FAIL/EVIDENCE_GAP`、10 active gaps、19 deferred；不能只因 Owner 已授權就把它們 CLOSED。[P §6 P6 L128、§8.2 L191]
3. 維持 `FULL_S0_S4_INDEPENDENT_PASS=NOT_GRANTED`、`G_RELEASE_FULL_PASS=NOT_GRANTED`、`PRODUCTION_VERIFIED=NOT_CLAIMED`，以及 Windows／host-native／S5 live 不受認證的邊界。[P §3、§6 P3；A §13]
4. **不能關掉邊界來假裝達標；可以在合法後續範圍真正補證，再另發新判定。** 本輪文件修正關的是失真／缺漏，不是 Stage 義務或獨立驗收 Gate。

### 必須關閉與非阻斷的精確含義

- **必須處置的當期文件問題：** NV-06 的使用前提不明；SUP-03 的 pending 狀態不同步。採最小公開文件修正、exact readback，不用重包 wheel 或重做 S4 架構。NV-06 的 focused evidence 尚開，不能藉本文件給它 PASS。
- **不是立即發布阻斷但正式 closure 前必修：** SUP-01 DEL-018。既有 FAIL 真實保留，正式 Gate 不得跨越；Owner Preview 例外不是把失敗變成成功。
- **真正產品 stop-ship 必須修：** 任意資料刪寫／越權／秘密外洩／必要 schema 或 CLI 在預定支援環境不可用／核心鏈普遍不可用／公開 hash 不符／有效授權或 Human/independent/Production 身分偽造。這些是 P P4 與 A §7.3 的觸發條件，**本輪沒有因 7 條未驗總述而證成其中一個新反例**。
- **可選增強：** 獨立全套、57-row 全量 oracle、合法後續 native/windows sandbox 全驗、外部簽章／attestation、auto-integrity、完整 CVE 掃描、MSYS 專屬診斷。若未來契約／發布政策明定為 mandatory，須重新校準；不能將本輪非阻斷當作永遠免驗。

## 6. 本文件完成與未做事項

已實讀四份指定文件、公開 main/tag README、公開 Preview Notes asset、live release body，以及 validate/schema resolution 相關 source；逐項區分缺陷、宣稱邊界、可選增強、方法論註記，補列 DEL-018、checker lane 與 mutable/pending 邊界。所有公開揭露判斷均限定本輪實讀的 D/N/B/M；未聲稱搜尋整個 GitHub 後證明任何句子絕對不存在。

本文件不執行 closure，不新增產品 PASS、不修既有文檔、不重跑套件、不操作 git、不發布或撤回 release。**最終裁定：`NOT_ALL_NOT_VERIFIED_ITEMS_REQUIRE_CLOSURE`；保留正確邊界，修正必要公開說明，證據／Stage 的真正關閉留給合法的新驗收。**
