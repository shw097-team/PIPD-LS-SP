# S4 FINAL closeout — evidence branch README

**Branch**：`s4-final-closeout-evidence-20261016`（本回合唯一遠端寫入；由既有證據尖端
`71e70f747c30bcd42d407fd045261a9669345ddb` 續開）
**Round**：`PIPD-S4-FINAL-PR18-CLOSEOUT-20261016`｜**ChangeSet**：`CONTINUATION`（單一）｜**Host TaskKind**：`IMPORT`

## 這是什麼

本回合以 **只讀** 方式核實已發布主體（`main`、PR #18、PR #17、`v0.1.1-preview.4`）的真實身分與真實
CI 原始日誌，並把「合併 PR #18／#17」與「`S4_PREVIEW_MVP_PHASE=TEMP_CLOSED` 正式簽認」交還 Owner。
本目錄是給外部驗收官的**輕量證據包**；上游長篇規範與產品程式不在此複製。

## 本分支**沒有**做什麼（非聲明）

- 沒有 merge、沒有 tag、沒有 release、沒有改動 `.4` 任何資產或 checksum。
- 沒有寫入產品分支 `fix/s4r6-closeout-doc-identity-and-update-route-20261016`、沒有寫入 `main`。
- **沒有產生任何 CI 執行**：本 repo 的 `public-plugin-verify` 工作流僅由 `pull_request` 與
  `workflow_dispatch` 觸發，**push 分支不會觸發**；因此本分支不附帶、也不聲稱任何 CI 結果。
  其中所有 CI 數字都是對**既有** hosted run 的原始日誌讀回（見 `pr_and_ci_raw_index.json`）。
- 沒有模型軸獨立驗收：maker 與 checker 同臂（registry `SOD006-C3`，owner order）。

## 讀者入口（建議順序）

1. `EVIDENCE_S4FINAL.md` — 單一入口：做了什麼、Gate 結果、聲明上限、非聲明、STOP RULE
2. `identities_and_release.json` — 凍結身分逐欄 expected/actual（13/13 相符）
3. `pr_and_ci_raw_index.json` — 四組互不可換的測試分母與原始 job log 行
4. `private_plugin_status.json` — 私人 ZIP 位元組級結構、同 ID 更新路徑、fallback 歷史事實
5. `findings_tasks_checklist.tsv` — F-R6-01..07、F-FINAL-08/09、FINAL-F01..06、CK-01..15 逐列處置
6. `sources_compiler_admission.json` — 來源清冊、Compiler 四命令收據、HGK admission、GSTACK 路由
7. `checker_and_owner_closeout.md` — checker 限制、Owner 交還清單、TT 登錄、回復點、五類反證搜尋
8. `MANIFEST.json` / `SHA256SUMS` — 檔案清冊與雜湊

## 完整性驗證方式

```bash
sha256sum -c SHA256SUMS      # 於本目錄內執行；應全部 OK
```

`SHA256SUMS` 與 `MANIFEST.json` 於最後一次封包變更後重算（任何在本目錄後續新增的檔案都會被重新納入）。
若本目錄在裁決之後被追加過任何檔案（例如車道收據），以 `MANIFEST.json` 的 `files` 清單為準。
