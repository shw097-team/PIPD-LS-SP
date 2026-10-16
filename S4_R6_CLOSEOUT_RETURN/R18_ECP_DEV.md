# DEV_ECP — 開發側執行控制包（具名引用版）

- 建立者：R18（`PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016`），回應稽核列 `ECP-DEV`（原判 `NOT_DONE`：
  「先建立 OPS/DEV ECP 精簡引用版」）。
- 性質：**引用版（reference edition）**。它不新增規範，只把人已經在別處寫下的東西收斂成一份可引用的
  控制包，供開發者在動任何一行之前先讀。所有事實皆附 locator；未驗證者標 `UNVERIFIED`。

## 1. Subjects（本包描述的主體）

| 角色 | 分支 | commit | tree |
|---|---|---|---|
| 產品候選（本回合產物） | `fix/s4r6-closeout-doc-identity-and-update-route-20261016` | `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20` (見 CURRENT_SUBJECTS.md；`127ec1c` 為 R17 頭，已為歷史) | `62eef9d8059d307ae373de63519a37551fa14854` |
| 回合證據 | `r6-closeout-evidence-20261016` | `0b50d3e` | — |
| 已發布（不可動） | tag `v0.1.1-preview.4` | tag object `0618d73c…` → commit `cc6c1930…` | — |
| 主線（未動） | `main` | `d3bd5456afbff21a8c8837994a49f57be3e1b97e` | `bc8dfc21…` |

locator：`far-r17/SESSION_CLOSEOUT_AND_HANDOVER.md`、`S4_R6_CLOSEOUT_RETURN/subject_versions.json`。

## 2. 本回合的變更（開發者要接的東西）

產品分支相對 `main` 共 4 檔 `+419/−22`，全部落在受治理寫入集內：

1. `docs/install/README.md` — 安裝 SSOT：版號／source commit pin、同 `plugin_id` 更新路徑、
   **以及 R18 追加的失效對外連結修正**（`:151` `](RELEASE_TUPLE.json)` → `](../RELEASE_TUPLE.json)`）。
2. `docs/USER_GUIDE.md` — 舊 `Merge/release HOLD` 與舊 wheel 宣稱更新；明寫 `.4` 已發布、Full S4 未授予。
3. `tests/test_r6_doc_identity_guard.py` — 文件身分守門（含配對 mutation；R18 擴充為對外相對連結亦須解析得到檔案）。
4. `.github/workflows/public-plugin-verify.yml` — `stage-c` 寫入集閘門的**具名修正**（加入 `docs/USER_GUIDE.md`
   單一路徑與同步 planted 清單）。

locator：`S4_R6_CLOSEOUT_RETURN/R17_RED_GATE_DIAGNOSIS.md`、`R17_MEASUREMENTS.json`。

## 3. 重現（read-only，任何人可跑）

```
git -C <repo> fetch origin
git -C <repo> diff --stat origin/main...<product-branch>      # 應為 4 files, +419/-22
python -m unittest discover -s tests -t .                     # 全量；實測 633 tests / OK (skipped=4)
python -m unittest tests.test_r6_doc_identity_guard -v        # 應 9 OK
```

`pytest` 亦可（`621 passed / 20 skipped / 62 subtests`，197.5s）——**兩者分母不同，不可互換引用**。

## 4. 驗證契約（改動前後都必須成立）

- 對外相對連結必須解析到**存在**的檔案（R18 新增此檢查；這是本次抓到 `DOC-LINK-TARGET` 的原因）。
- 文件不得把 `main` 當成已發布版本；`.4` 的 tag object 與 7 assets 摘要不得變。
- 守門的 mutation 反例必須**仍然失敗**（假綠即為缺陷）。
- locator：`tests/test_r6_doc_identity_guard.py`、`r18/`（本回合證據）。

## 5. 回滾（開發側）

產品候選尚未合併，故回滾＝**不要合併**即可；分支可 `git branch -D`。已發布 `.4` 不得原位替換；
若需更正已發布資產，只能在**下一次發行**處理（見 `TT-R6-OD-B`）。

## 6. 未解（開發者接手時要知道的空白）

- `HISTORICAL-RAW-CI`：歷史 `624/108` 的 raw CI 日誌未凍結（憑證 401）→ `TT-R18-03`。
- 「第九 Skill／跨根修改」缺專屬機械負例 → `TT-R18-01`。
- `HGK-BINDING`：本回合的 push 無精確作用域 ExecutionBinding → `TT-R18-02`。

## 7. 天花板

本包描述的是**候選狀態**，不是已驗收狀態。`S4_FULL_PASS`／`HOST_QUALIFIED`／`PRODUCTION` 皆
`NOT_GRANTED`；私有宿主 UAT `NOT_RUN`。合併、簽核、發行與公開目錄皆非開發側可自行完成。
