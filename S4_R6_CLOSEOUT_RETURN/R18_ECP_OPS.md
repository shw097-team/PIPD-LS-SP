# OPS_ECP — 維運／發布側執行控制包（具名引用版）

- 建立者：R18（`PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016`），回應稽核列 `ECP-OPS`（原判 `NOT_DONE`）。
- 性質：**引用版**。只收斂既有規則，不新增。每條附 locator；未驗證標 `UNVERIFIED`。

## 1. 遠端寫入的四道閘門（依序，缺一不可）

1. **HGK typed 准入**：`ADMISSION_OK` 且 WorkOrder 覆蓋該次寫入之 effect。本回合為
   `WO-TS-R18-01..05`；locator：`r18/HGK_TYPED_ADMISSION_R18.json`。
2. **產品寫入集閘門**：`public-plugin-verify.yml` 之 `stage-c` 臂對 `git diff --name-only <declared base>...HEAD`
   套正規式白名單；越界即紅。locator：`.github/workflows/public-plugin-verify.yml`、
   `S4_R6_CLOSEOUT_RETURN/R17_RED_GATE_DIAGNOSIS.md`。
3. **只推受控分支**：遠端分支名不得為 `main`；`main` 僅能由 owner 合併推進。
4. **憑證紀律**：PAT 只由受控包裝器讀取，**永不**進入 argv、URL、log、檔案或聊天；推送需
   `-c credential.helper= -c credential.interactive=always -c core.askPass=<wrapper.cmd>`
   （Windows 上 `GIT_ASKPASS` 被忽略）。locator：`far-r17/publish/`、記憶條目。

## 2. 發布側的不可動集合（immutable）

| 資產 | 值 | 驗證方式 |
|---|---|---|
| tag | `v0.1.1-preview.4`（tag object `0618d73c…`） | `git rev-parse v0.1.1-preview.4^{}` 不得變 |
| tag target commit | `cc6c1930…` | `git rev-list -n1 v0.1.1-preview.4` |
| ZIP | `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`，68,357 B | 下載重算 |
| assets | 7 件，摘要與 `SHA256SUMS`（`0f765026…`）相符 | 逐筆 sha256 |

**不得原地替換**已發布資產；更正只能在下次發行。locator：`S4_R6_CLOSEOUT_RETURN/subject_versions.json`、
`release_and_plugin_scope.json`。

## 3. 推送後必須讀回（readback，不是信任）

- 遠端分支 SHA == 本地 HEAD（`git ls-remote`）。
- PR 狀態：`state=open`、非 draft、`mergeable`、變更檔案數與 `+/-` 與本地 `diff --stat` 相符。
- 託管 CI：`verify` 與 `offline-gate` 皆須 `success`（**推送前**先在本地以同一分類器重現閘門，
  避免把紅燈推上去）。locator：`S4_R6_CLOSEOUT_RETURN/PUBLICATION_READBACK.json`。

## 4. 分支模型（為何證據與產品分開）

回合證據**不得**落在產品分支：`stage-c` 白名單明文拒絕回合證據目錄。證據放專用分支
`r6-closeout-evidence-20261016`，產品只留 4 檔。locator：`R17_RED_GATE_DIAGNOSIS.md`。

## 5. 回滾指標（維運側）

- 產品分支舊尖端已保存於證據分支（非破壞性 push 的前置）：`3e1bc6d4…`。
- 若需丟棄產品候選：遠端分支刪除即可，`main` 與 `.4` 不受影響。
- 若誤推：`git push --force-with-lease=<ref>:<exact sha>`（**先**保全舊尖端於另一分支）。

## 6. 必須由 owner 執行者（本回合不得代行）

合併 PR #17／#18；簽核 `TEMP_CLOSED` 為正式 closeout；私有宿主 UPDATE smoke（需人類帳號）；
是否發新 tag／新版；是否調整 lane pool 排序（owner order 2026-10-16，`SOD006-C3`）。
locator：`far-r17/SESSION_CLOSEOUT_AND_HANDOVER.md`、`r18/AUDIT_REQUIREMENTS.tsv`（`OWNER_GATE` 12 列）。

## 7. 已知控制平面缺口（不可由本回合修）

`VERIFY_SECURITY` pool 之 rank-1 為 writer 同模型（依 owner order），故獨立性需**釘選 arm** 取得；
registry 不由量測它的一回合修改（否則摧毀量測）。locator：`far-r17/DEFECT_DOSSIER.md`。

## 8. 天花板

`TEMP_CLOSED` 不得被讀成 `FULL_PASS`；`PUBLIC_DIRECTORY=OUT_OF_SCOPE`、
`S4_FULL_PASS=NOT_GRANTED`、`PRODUCTION=NOT_GRANTED`、`FOUR_HOST_QUALIFIED` 不得出現。
