# FAR-PIPD-R6-MAIN-FRONT-PAGE-001 — main 主頁 README 現況研究與重構方案

- 輪次：`R6-20261011-main-front-page`
- 研究編號：`FAR-PIPD-R6-MAIN-FRONT-PAGE-001`
- 對象：`https://github.com/shw097-team/PIPD-LS-SP` 的預設分支 `main`（`README.md`）
- 受驗主體：`main` = `de3a1d9e3a6298fa0dd29fafbf11d850e30c743a`（2026-10-10 抓取，遠端實測）
- 性質：**純文件研究 + 主頁重構**。不修產品程式、不改 wheel、不移動 tag、不 force-push。

## 0. 方法與取證

| 來源 | 取法 | 事實 |
|---|---|---|
| `main` 的 `README.md` | `git show origin/main:README.md`（fetch 後）→ 71 行 / 5,359 bytes | 見 §1 |
| `main` 的檔案樹 | `git ls-tree -r --name-only origin/main` | **600 個檔案** |
| `main` 根目錄 | `git ls-tree --name-only origin/main` | 20 個頂層項目（見 §2） |
| `main` 的授權檔 | `git show origin/main:LICENSE`、`OWNER_LICENSE_DECISION.yaml` | `LICENSE` = 非授與「licence position」；`decision: UNSET` |
| 已發布 preview | 遠端 tag `v0.1.0-preview.1` = `cc9bf574…`（`git ls-remote` 實測） | Apache-2.0；wheel `c450dbef…` |
| 比對：`r5q` 分支 README | `git show 9bd33a1:README.md` → 193 行 / 18,060 bytes | 見 §3 |
| 申請人決策/殘留台帳 | `R5Q_NOT_VERIFIED_LEDGER.md`（202 行，實讀） | 見 §4 |

**取證限制（明示）**：`main` 的 README 以本機 clone 的 `origin/main` 讀取；該 ref 在 fetch 前曾**過期**停在 `3aebbbc`，本文所有判斷均在 `git fetch origin main`（`3aebbbc..de3a1d9`）之後重讀。未以匿名 HTTP 重新下載驗證渲染結果，故「渲染外觀」類判斷止於 Markdown 語意層。

## 1. 現況：main 主頁是什麼

`main` = **R3 線**（`3aebbbc` "publish the S0-S4 destructive-audit repair candidate"），其後**只有一個 commit**：`de3a1d9`（14 行、只動 `README.md`，於頁首插入指向 preview tag 的 banner）。

因此今日 `main` 的主頁 = **R3 內容 + 一頂 14 行 banner 帽**。

## 2. main 的實際樹（banner 與 R3 內文都沒說的部分）

20 個頂層項目 / 600 檔：

```
.agents  .gitattributes  .gitignore  .hermes  .hgk
LICENSE  OWNER_LICENSE_DECISION.yaml  PROVENANCE.md  README.md  SBOM.cdx.json
dist  docs  fixtures  openspec  pyproject.toml
schemas  skills  src  tests  tools
```

- `skills/` — **8 個已發布 skill**：`pipd-route-intake`、`pipd-profile-tailor`、`pipd-pi-compile`、`pipd-pd-bind`、`pipd-execution-contract`、`pipd-assurance-tqaep`、`pipd-authority-source`、`pipd-package-project`（每個含 `SKILL.md`／`references/`／`schemas/`／`tests/cases.yaml`）
- `schemas/` — 20 檔 = 19 契約 family + `registry.json`
- `src/pipd_ls_sp/` — 12 個模組；`cli.py` 提供 **13 個指令**：`init` `intake` `profile` `compile-pi` `bind-pd` `compile-ecp` `compile-tqaep` `validate` `doctor` `project` `export` `diff` `repair`
- `tests/` — 19 檔（R5R 分支為 32 檔）
- `dist/` — `WHEEL_MANIFEST.json`、`pipd_ls_sp-0.1.0-py3-none-any.whl`、`.sha256`、`web/`（含 host packs 與 OPTIONAL_SITE_UI）
- `docs/` — 3 檔：`S0_CONTRACT_SPEC.md`、`ROUND_DISCLOSURE.md`、`ROUND3_DISCLOSURE.md`
- `.hgk/` — `admission` `ao` `artifacts` `codex` `far` `kanban` `knowledge` `preflight` `rounds` `surfaces`
- `pyproject.toml` — `name = "pipd-ls-sp"`、`version = "0.1.0"`、`requires-python = ">=3.11"`、**無 license 欄位**
- **不存在**：`NOTICE`、`ACCEPTANCE.md`、`PREVIEW_NOTES_v0.1.0-preview.1.md`（三者皆為 R5Q 產物，只在 release 線）
- `dist/` 內的 wheel sha256 = `ba84115dfc5efa0f7c2240d137c2868a9469a9b5680cbd6cff833c1943630dfa`，**≠** 已發布 preview 的 `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60` → main 的 `dist/` 是 **R3 時代的舊 wheel**

## 3. 診斷：現行主頁的 10 項缺陷

每項均附實測依據。

| # | 缺陷 | 依據 |
|---|---|---|
| D1 | **H1 標題宣告錯誤事項**。首行寫 `(review candidate)`，而其下 banner 已宣告 owner 授權的 Apache-2.0 preview 存在。訪客第一眼看到的是已被超越的狀態詞。 | L1 vs L3–8 |
| D2 | **授權自相矛盾且未調和**。banner 說 preview 是 Apache-2.0；本文 §License 說 `No license is granted`。banner **未**聲明「main 本身」未授權，故讀者無法得知矛盾何者適用於當前分支。 | L6 vs L65–66 |
| D3 | **banner 以 blockquote 承載標題與結構**。14 行 `>` 區塊被當成主視覺，內文重複其資訊；區塊引用在 GitHub 上渲染為灰底引言，語意上不該是主導航。 | L3–15 |
| D4 | **claim ceiling 表達已不實**（且對 main 自身亦不實）：`INDEPENDENT_PASS` 稱「pending an independent acceptance officer receipt」，但 R5Q/R5R 已有獨立收據；`PUBLICATION_APPROVED` 稱「no license is declared in the source corpus」，但 owner grant 已存在。 | L42–43 |
| D5 | **與所在分支自我矛盾**。「`S0` and `S1` are the only stages reached. S2–S8 are not implemented.」但 main 自身的建置提交標題即為 "the S0-S4 … candidate"，樹內含 8 skills / 13 指令。 | L47 vs `3aebbbc` 標題 |
| D6 | **頁尾懸空編號章節**。`## 8. Correction of a wording overclaim (round 2 finding)` 出現在 `## License` 之後，**沒有 1–7**，內容是輪次內部工作敘述（"README.md previously implied…"）。輪次過程外洩到門面。 | L69–71 |
| D7 | **無真實樹狀圖**。「What is in this tree」漏列 `skills/`（8 個已發布 skill）、`dist/`（wheel ＋ web packs）、`.hgk/`、`openspec/`、`fixtures/`——即訪客最需要的一半。 | L23–30 vs §2 |
| D8 | **完全沒有安裝／quickstart**。`dist/` 明明有 wheel，主頁卻沒有一個可照做的起點。 | 全文 |
| D9 | **指向凍結的 R3 快照數**。單元測試列指向 `.hgk/artifacts/STATUS_R3.json#tests`，讀者無法自行重跑得到該數。 | L55 |
| D10 | **殘留已過期的授權缺口代號**。§License 引 `TT-PIPD-LICENSE-001` 作為結論，該項已被 R5Q owner grant 超越，卻無任何 supersede 註記。 | L66 |

**根因（單一）**：此頁是**按時間追加的日誌**，不是門面。R3 內文 → 加 R4 → 疊 R5Q → 疊 banner，每層都追加、都不改上層；`r5q` 分支的 193 行版本把同一病症展示得更完整（3 層 `supersedes` 串、§License 與頁首相反、同一 D6 懸空章節）。main 版只是層數較少的同一病症。

## 4. 重構方案（比較與選定）

| 方案 | 做法 | 評估 |
|---|---|---|
| A 維持 banner | 只修 banner 措辭 | 不改根因；D4–D10 全留 |
| B 平移 r5q 版 | 把 193 行版本搬到 main | **不可**：它描述 release 線的事實（`NOTICE`、`ACCEPTANCE.md`、Apache-2.0 為樹內狀態），main 上**這些檔案不存在**，會直接造成假陳述 |
| **C 以現況重寫為門面（選定）** | 依 main **實際**樹重寫；產品入口指向 tag；歷史外移 | 一次解決 D1–D10；事實皆可對 `main` 樹驗證 |

**選 C。** 理由：D1–D10 的共同根因是「門面被當成日誌」，只有重寫成**狀態頁**才處理根因；且 C 是唯一能在不假陳述 main 的前提下，同時服務「訪客要安裝」與「main 是 R3 快照」兩個事實的方案。

### 選定設計（目標結構）

1. **標題 + 一句是什麼**（H1 不得出現 `review candidate`）
2. **狀態框（≤8 行，非引言）**：這個分支是什麼、散布入口在 tag、main 自身的授權狀態
3. **這是什麼** — 取自 `docs/S0_CONTRACT_SPEC.md` 的定位，2–4 句
4. **取得與使用** — preview tag、wheel、安裝、13 指令、可重跑命令
5. **樹狀圖** — 涵蓋 §2 全部 20 個頂層項目
6. **Claim ceiling** — 修正後分「已授予 / 未宣稱」兩欄，並列 preview 已知限制
7. **歷史與證據在哪** — 指向 `.hgk/`、`docs/`、tag
8. 移除懸空 §8

### 驗收判準（可機械檢查）

- AC1 H1 不含 `review candidate`，且不再與內文宣告矛盾
- AC2 全文**不出現**未調和的 `No license is granted` 作為 main 的結論；main 自身的授權狀態被明示
- AC3 樹狀圖涵蓋 20 個頂層項目中實際存在者（≥ 全部實際項）
- AC4 每條對外連結（tag、release、授權檔）皆指向**實際存在**的目標
- AC5 引用的每個樹內路徑皆存在於 `main`（以腳本逐一 `git cat-file -e`）
- AC6 不清除任何既有歷史資訊，而是**外移**到 `docs/` 並在門面留指標
- AC7 不出現任何未經本輪驗證的升級（尤其：不得暗示 R5R 修補已交付使用者）

## 5. 必須寫入的誠實揭露（不可省）

1. **main 自身未授權**：`LICENSE` 為非授與文本、`OWNER_LICENSE_DECISION.yaml` 的 `decision: UNSET`；Apache-2.0 只在 release commit／tag 生效。
2. **main 的 `dist/` wheel 不是發布版**（sha 不同），不得被當成安裝來源。
3. **已發布 preview 仍帶兩個已知缺陷**（`validate` 的 schema 解析；四編譯器原始 stdout 之 bundle 被 `_profile_meta` 拒收）。
4. **這兩缺陷的修補已完成且經獨立複驗，但尚未發布**——主頁不得暗示使用者已取得修補。
5. **既有天花板照抄不升級**：`DEL-018` FAIL/EVIDENCE_GAP；`PARTIAL_CHALLENGE` 28/10/19；無 CVE／供應鏈掃描；無 attestation／release signature；S5–S8、host-native、PRE-W3 未認證；`PRODUCTION_VERIFIED` 未宣稱。

## 6. 本研究的未做事項

未以匿名 HTTP 下載驗證 GitHub 渲染後外觀；未重跑產品套件（此為文件輪）；未查核 `dist/web/` 內 20 餘檔的內容正確性；未評估 `main` 上 `3aebbbc` 之前的歷史是否另需整理。以上不影響 §3 的診斷（皆為檔案層事實）與 §4 的選定方案。
