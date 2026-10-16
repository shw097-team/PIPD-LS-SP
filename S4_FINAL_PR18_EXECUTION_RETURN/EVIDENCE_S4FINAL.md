# S4 FINAL 回合 — 外部驗收證據（單一 MD）

**Round** `PIPD-S4-FINAL-PR18-CLOSEOUT-20261016`｜**Report** `PIPD-LS-SP-S4-EXTERNAL-FINAL-20261016`
**契約** `PIPD-S4-FINAL-PR18-CLOSEOUT-20261016`｜**Host TaskKind** `IMPORT`｜**ChangeSet** `CONTINUATION`（單一）
**凍結主體**：`main` `d3bd5456afbff21a8c8837994a49f57be3e1b97e`｜PR #18 `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20`｜PR #17 `97a01dab95bc53a08b8c372e3c3b04e69a923d7d`｜tag object `0618d73c725da0d8c3280f99ef369d13741b5197` → commit `cc6c1930765160697e7e51d6e37735b9220a30db`

## 1. 本回合做了什麼（一句話）

在 HGK 唯一控制平面下，**只讀**核實已發布主體的真實身分與真實 CI，產出可稽證據包，並把「合併 PR #18/#17」與「`S4_PREVIEW_MVP_PHASE=TEMP_CLOSED` 正式簽認」以 `OWNER_ACTION_REQUIRED` 交還 Owner；**未開新一輪核心修補、未 merge／tag／release、未改動 `.4` 任何資產**。

## 2. Gate 結果

| Gate | 結果 |
|---|---|
| G0 唯讀前置＋Compiler | `PROMPT_COMPILE_PASS`（lint／activation／acceptance／compile 全 exit 0；contract_sha256 見 `sources_compiler_admission.json`） |
| G0 HGK admission | `ADMISSION_OK`（18/18 來源；WorkOrders `WO-TS-PR18-01..05`；checkpoint `CK-PR18-A2FBBBB0`） |
| G0 GSTACK／OpenSpec | 路由 `CERTIFIED`（plan-eng-review／cso／qa／review）＋負向對照 `NATIVE`；OpenSpec change strict 有效 |
| G1 PR #18 | 精確核對**完成**；**合併 = `OWNER_ACTION_REQUIRED`** |
| G2 PR #17 | 精確核對**完成**；**合併 = `OWNER_ACTION_REQUIRED`** |
| G3 最小修補例外 | **未觸發**（STOP RULE：五類反證未命中） |
| G4 受控傳輸 | push ×1（scoped evidence 分支）；憑證未外洩（見 `AUTHORIZATION_MANIFEST.md`） |
| G5 私人 ZIP／UAT | 結構**位元組級驗證通過**；真帳號 smoke = `NOT_RUN`（`HOST_OWNER`） |
| G6 TQAEP／獨立驗收 | 見 `checker_and_owner_closeout.md`（同模型軸限制明示） |
| G7 新 Preview | **未觸發**；`.4` 為 `IMMUTABLE_HISTORICAL_RELEASE` |

## 3. 驗收聲明上限（Claim ceiling）

`MAIN_CORE_PASS_SCOPED`／`.4 = PUBLISHED_PASS_SCOPED`／`PRIVATE_ZIP_FORMAT_PASS / ONE_ACCOUNT_PARTIAL`／
`S4_PREVIEW_MVP_PHASE = TEMP_CLOSED_RECOMMENDED`（**Owner 未簽前不得寫 `OWNER_RATIFIED`**）。
`S4_FULL_PASS` = `NOT_GRANTED`；`HOST_QUALIFIED` = `NOT_GRANTED`；`PRODUCTION` = `NOT_GRANTED`；`PUBLIC_DIRECTORY` = `OUT_OF_SCOPE`。

## 4. 非聲明（Non-claims）

- 不聲稱模型軸獨立驗收（maker=checker 同臂）。
- 不聲稱四宿主同版有效載入。
- 不聲稱 `.4` 已包含 tag 之後 `main` 的 11 個 commit。
- 不聲稱任何私人帳號的「一鍵更新」已實測。
- 不聲稱本輪新增任何產品修補（STOP RULE）。

## 5. 讀者入口

1. `identities_and_release.json` — 凍結身分逐欄 expected/actual
2. `pr_and_ci_raw_index.json` — 四組測試分母與原始 job log 行
3. `private_plugin_status.json` — privZIP 位元組級結構與更新路徑
4. `findings_tasks_checklist.tsv` — 逐項 finding／CK 處置
5. `sources_compiler_admission.json` — 來源、Compiler、admission、路由
6. `checker_and_owner_closeout.md` — checker 限制、Owner 交還、TT、回復點

**STOP**：未命中五類反證 → 依 STOP RULE 不再開 S4 核心修補輪；剩餘品質工作列後續觸發式 TT。
