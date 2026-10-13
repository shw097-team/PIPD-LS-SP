# R5 — 最小 CI 的**首次真實執行**（含根因、修補與未閉合項）

- 性質：maker 側的執行紀錄與故障分析；**不是**產品驗收、**不是** CI 綠燈宣告
- 前置事實（裁決 §3.1 的觀察）：受驗 5 分支 + 3 tag 全部 0 個 `.github/`、Actions runs = 0
- 本輪：Draft PR **#2** `https://github.com/shw097-team/PIPD-LS-SP/pull/2`（draft=true，不請求合併）

## 1. 為什麼「有 workflow」卻「從未驗過任何東西」

`ci` workflow 一直在分支上（`main` 仍為 0 個 `.github/`），但**所有**推播觸發的執行都在第 2 步就失敗，
功能步驟全被 skip。逐字根因（run `38331055903`，job `offline-gate`，log `2_Check out the frozen subject.txt`）：

```
[command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' ..."
fatal: No url found for submodule path '.hgk/rounds/R2-20261009-qualification/execute/candidate' in .gitmodules
##[error]The process '/usr/bin/git' failed with exit code 128
```

`actions/checkout` 在移除 auth header 時會跑 `git submodule foreach`；而 repo 內有 **4 個 mode-160000
gitlink**（`main` 即有，來源 commit `829c17e87855cd7a1c88bfad1f51f1fdd1fafa5e`）**沒有任何 `.gitmodules`**，
因此 checkout 直接 abort。

**修補**（本輪，超出 FAR R1–R8 清單，理由：它是唯一讓「已核准的最小 CI」無法執行的原因，且不新增任何 CI 軸）：

```
fix(repo): drop four unresolvable gitlink entries so actions/checkout can run (CI unblock)
```

那 4 個路徑在磁碟上是**空目錄（0 項）**，移除索引項不失任何內容；`main` 未動。

## 2. 修補後：CI 第一次真正執行（run `38331455392`，sha `8e5c719`）

| 步驟 | 結果 |
|---|---|
| 2 Check out the frozen subject | **success**（修補前 failure）|
| 3 Set up Python 3.11 | success |
| 4 Install (declared dependencies only) | success |
| 5 **Full unittest suite** | **success** |
| 6 **Focused S4 repair/closure suites** | **success** |
| 7 Build wheel + clean venv + `pipd doctor` | **failure** |
| 8 Provenance gate is green before it is tested | skipped |
| 9 Negative — mutated pack must fail the gate | skipped |

**這是有紀錄以來第一次**：該 workflow 的完整與聚焦套件在主辦 runner 上實際跑完且通過。
仍**不主張**任何產品正確性——步驟 8/9（來源閘門與其負向校準）**尚未被執行過**。

## 3. 步驟 7 的第二個真因（已修）

```
ERROR: Cannot install pipd-ls-sp 0.1.0 (from .../dist/pipd_ls_sp-0.1.0-py3-none-any.whl) and
pipd-ls-sp 0.1.1a3 (from .../dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl) because these package
versions have conflicting dependencies.  →  ERROR: ResolutionImpossible
```

`dist/` **被版控**且同時存有兩顆 wheel（`0.1.0` 與 `0.1.1a3`，各自的 `.sha256` 與 `WHEEL_MANIFEST.json`），
而該步驟用 `pip install dist/*.whl`。**修法（採更嚴而非更鬆）**：建置到私有目錄並**只安裝剛建出的那顆**
（`python -m build --wheel --outdir "$RUNNER_TEMP/wheels"`），`dist/` 完全不動——
既修正受驗主體，也讓此步驟真正檢驗新產物。

## 4. `public-plugin-verify` 的紅燈：**兩種 scope 的機器量測**（owner 決策用）

該 job 的正向允許清單步驟（"Prove the upgrade wrote only inside its allowed set"）在 run `38331461433` 失敗。
以**它自己的 regex** 在兩種 base 下重跑該判定：

| base | 變更檔 | 允許集外 | frozen-path 寫入 |
|---|---|---|---|
| `main` `2245914…`（**PR 時的預設**） | 126 | 長清單（含 `docs/`、`tools/`） | **4**：`schemas/PI-PKG.schema.json`、`schemas/TraceLink.schema.json`、`src/pipd_ls_sp/profiles.py`、`src/pipd_ls_sp/validate.py` |
| `52542c3…`（workflow 自宣告的 **STACKED_BASE_SHA** ＝ Stage-A 疊層底） | 99 | **4**，且正是本輪剛移除的那 4 個 gitlink | **NONE** |

**結論（雙向都對 owner 有用）**：
1. **本升級自身**在 `schemas/`、`src/` 的寫入為 **0**——`INV-03 ZERO CORE WRITES` 由本回合自己的守衛取得機器證據，
   不再只是 maker 的主張。
2. 那 4 個 frozen-path 寫入屬 **Stage-A 疊層**（`fix/s4post-integration-repair-20261012` 的合法修補），
   只有在「以 `main` 為 base」時才被計入 → **受驗主體（升級 vs 整個疊層）就是 owner 要裁決的 D3**。
3. 修補 gitlink 後，在宣告 scope 內的**允許集違規歸零**。

## 5. 未閉合 / 不主張

- 步驟 8（來源閘門）與 9（突變負向）**從未執行過**；`ci` 現階段為紅（步驟 7 待新一輪驗證）。
- `public-plugin-verify` 在 PR-to-main 下為紅，其成因是 **scope 選擇**，已上表量化，**未**改動該守衛的語意。
- 未主張：`BUILD_PASS`、`LOCAL_HOST_QUALIFIED`、`PORTAL_APPROVED`、`PUBLISHED`、`PRODUCTION_VERIFIED`、`PIPD_S4_FULL_PASS`。
- 本輪對 `main` 無任何寫入；`dist/` 未動；三個 tag 未動。
