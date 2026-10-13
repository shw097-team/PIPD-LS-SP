# R6 — 證據「第三方可重跑」已成為可執行斷言（非承諾）

- 性質：FAR 低阻力方案 **R6** 的落地與量測；Maker 側證據，非驗收
- 觸發的事實（實測，非推論）：AO10／AO11／AO12 的逐案證據放在車道自己的
  `%LOCALAPPDATA%\Temp\<lane>-*` 暫存根，**maker 身分（`user`, SID `…-1000`）連列目錄都被拒**
  （`ls: Permission denied`；`icacls` 回 `0 files processed, 1 error`）。
  因此報告中指向該根的定位**對第三方不可重跑**——即使報告本身可讀。

## 工具（新增、可重跑、有正負對照）

`verify/tools/check_evidence_locators.py`

把每個「路徑形」定位歸類並以 typed 非零碼拒絕：

| 類別 | 意義 | 是否 offеndер |
|---|---|---|
| `RESOLVES_IN_TREE` | 解析到 `--root`（或 `--search-dir`）之下的真實檔案 | 否 |
| `EXTERNAL_ONLY` | 存在，但在 `--root` 之外 | **是** |
| `UNRESOLVABLE` | 形如路徑但在所有搜尋根下都不存在 | **是** |
| `SHORTHAND_BARE_NAME` | 無路徑分隔的裸檔名（如 `` `plugin.json` `` 之類散文簡寫） | 否（只計數） |

（`SHORTHAND_BARE_NAME` 這一類是**檢查器自身第一版的缺陷**修出來的：初版把散文簡寫算成 offender，
導致正向對照假紅。依「自己的探針錯了，探針就是 finding」原則，記為探針缺陷並修正精度。）

## 量測（raw）

```
# 正向對照：本回合 R3 產物（必須乾淨）
python verify/tools/check_evidence_locators.py --root <repo> --search-dir <round> \
    OWNER_ACTION_REQUEST.md HARNESS_FREEZE_AND_AO_LOOP_CAP.md
exit=0  {"verdict":"PASS_LOCATORS_IN_TREE",
         "counts":{"RESOLVES_IN_TREE":11,"EXTERNAL_ONLY":0,"UNRESOLVABLE":0,"SHORTHAND_BARE_NAME":13}}

# 負向對照：AO12 的正規車道報告（應被拒）
python verify/tools/check_evidence_locators.py --root <repo> --search-dir <round> \
    verify/ao12/EXTERNAL_CHALLENGE_REPORT.md
exit=2  {"verdict":"FAIL_LOCATORS_NOT_RERUNNABLE",
         "counts":{"RESOLVES_IN_TREE":13,"EXTERNAL_ONLY":5,"UNRESOLVABLE":25,"SHORTHAND_BARE_NAME":54}}
```

逐條 JSON：`verify/tools/LOCATOR_CHECK_R3_POSITIVE.json`、`verify/ao12/LOCATOR_CHECK_AO12.json`。

## 兩項結構性發現（機器斷言，非敘述）

1. **車道暫存根在樹外且不可讀** → 任何引用它的 finding 都不可由第三方重跑。
2. **正規車道契約本身在樹外**：報告引用的
   `~/.agents/skills/fabric-external-independent-challenge-reviewer/**`（SKILL.md、`scripts/verify_review_bundle.py`、`tests`）
   全部解析為 `EXTERNAL_ONLY`。
   這與裁決自陳「其參照腳本與模板未掛載」**同源**：該車道的 canonical 契約與 validator 沒有進版控，
   所以**任何人都無法在 repo 內獨立重建報告所宣稱遵循的契約**。

## 低阻力修法（兩條，均可小成本落地）

| # | 修法 | 效果 | 成本 |
|---|---|---|---|
| R6-a | 車道退出前**在樹內**放置 bundle（AO12 已如此做，`verify/ao12/` 9 檔可讀 ✓），並由 wrapper 以本檢查器斷言「所有引用定位皆解析於樹內」，不符即 typed 非零碼 | 消除第 1 類發現 | 低（本檢查器即為其斷言核心） |
| R6-b | 把正規車道契約以**釘選 digest 的方式 vendored 進樹**（或記錄可重現的下載定位） | 消除第 2 類發現；同時關閉裁決的「validator 未掛載」 | 中（需 owner 同意 vendoring 第三方契約） |

## 殘餘（不主張已閉合）

- 檢查器是**啟發式**：它不判斷語義正確性，只判斷定位可解析性。
- `SHORTHAND_BARE_NAME` 不判為 offender，因此**惡意或疏漏的裸檔名引用不會被本工具抓住**。
- 本工具未接進任何自動閘門（無 consumer）；現階段是 **DETECTION，不是 prevention**——
  要成為控制，須由車道 wrapper 在退出前呼叫它並以其退出碼阻斷 promote。
