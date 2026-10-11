# FAR｜PIPD-LS-SP R5 S4「全部缺口可閉合性」快速研究報告

- **FAR ID**：`FAR-PIPD-R5S4-GAPCLOSURE-001`
- **研究問題**：我方是否有可能（或需使用者／Owner 額外做什麼、授權什麼）才能**完全解決並關閉目前全部缺口與缺陷**，使外部驗收官有機會進行 **「S4 級」驗收**？或「S4 級」對我方**根本不可能**達成？
- **方法**：以現場 machine truth 直接量測（網路可達性、GitHub 匿名讀取、object store 血緣比對、位元組雜湊比對、cli 閘門機制讀回）。**未使用任何憑證**。
- **產出時間**：2026-10-10T06:0x Z（見檔尾 sidecar）
- **前提事實**：本報告的所有量測皆為本回合首次執行；執行期間**從未**對 GitHub 做過任何讀回。

---

## 0. 結論（先講）

> **不是不可能。** 技術性缺口被**一個零憑證的廉價動作**支配——`git fetch` + 一個 15 檔的 commit——它本該是第 0 步。
> **但「我方能自己關掉全部」是假的**：有三件事在結構上不屬於我方的權限範圍——**遠端寫入、授權／公開發行範圍、以及「獨立驗收」這個動作本身**。
> 因此正確答案是：**工程剩餘量很小，瓶頸是 Owner 的四項決定。**

---

## 1. 決定性發現（全部現場量測）

### F1. GitHub repo 是**公開可匿名讀取**的，且遠端分支齊全

```
$ git ls-remote https://github.com/shw097-team/PIPD-LS-SP
3aebbbce948871c07b875ab92acf263d298ecf38  HEAD
3aebbbce948871c07b875ab92acf263d298ecf38  refs/heads/main
3aebbbce948871c07b875ab92acf263d298ecf38  refs/heads/r3-candidate
cd8a06e4c066a40398a4012b7b3908ac11408a2b  refs/heads/r4-candidate      ← 外部受驗主體在此
cd8a06e4c066a40398a4012b7b3908ac11408a2b  refs/pull/1/head
0289573195c32172a67aa424319e244b0316df95  refs/pull/1/merge
```

`api.github.com/repos/shw097-team/PIPD-LS-SP` → **HTTP 200**（公開）。`github.com` → **200**（可達）。

**→ 缺口 G1（R5 指令 §2.1-3 要求的 GitHub 讀回從未執行）本來就是「**零憑證即可完成**」。它不是授權阻斷，是流程失誤。**（R5 指令本身也寫明：「若只需只讀 GitHub 操作，優先使用既有授權連線，**不需觸碰 PAT**」。）

### F2. `r4-candidate` 只比 `main` 多 **2 個 commit**，但本機歷史裡**完全沒有**

```
cd8a06e r4: disclose INCIDENT-02 (same path-defect class, orchestration side)
3039148 r4: focused-repair candidate — hardening tooling, evidence, owner adjudication
3aebbbc r3: publish the S0-S4 destructive-audit repair candidate

$ git diff --stat 3aebbbc origin/r4-candidate
135 files changed, 48977 insertions(+), 133 deletions(-)
```

本機 object store：**只有** `master@7c5bc58`、`r3-candidate@3aebbbc`；`r4-candidate` 與 `cd8a06e` **不存在**。

### F3. 但本機工作樹的 R4 內容與 `cd8a06e` **逐位元組相同**

| 檔案 | 本機 sha256(前16) | `cd8a06e` 內 | 判定 |
|---|---|---|---|
| `tests/test_round_envelope.py` | `907763d3c75883fa` | `907763d3c75883fa` | **IDENTICAL** |
| `tools/round_envelope.py` | `d8a24cb565ff5112` | `d8a24cb565ff5112` | **IDENTICAL** |
| `tools/preflight_check.py` | `ab193f06ef533566` | `ab193f06ef533566` | **IDENTICAL** |
| `tests/test_tt_summary.py` | `1010ea1f837310cc` | `1010ea1f837310cc` | **IDENTICAL** |
| `src/pipd_ls_sp/requirements.py` | `1ac3a64c655d93e0` | `1ac3a64c655d93e0` | **IDENTICAL** |
| `tests/test_deny_list_scan.py` | `ddc4d3bb8c6279e8` | `ddc4d3bb8c6279e8` | **IDENTICAL** |

**→ 工作樹 = R4 候選內容（在磁碟上）＋ 本回合 R5 差異；但歷史 = R3 線。**
也就是說：**內容正確，卻無法被綁定（content-correct but unbindable）**。
這就是為何所有 publication／attestation 註定失敗：**沒有任何東西把磁碟上的位元組綁到那個受稽核的 commit**。

### F4. R5 差異在 `cd8a06e` 之上只有 **15 個檔案**

```
src/   (6) cli.py  errors.py  export_bundle.py(NEW)  projection.py  registry.py  workspace.py
tools/ (5) build_dist.py  cli_smoke.py  cli_surface_check.py  perf_budget.py  portable_install_check.py
tests/ (4) test_export_bundle.py  test_perf_budget.py  test_project_destination_safety.py  test_wheel_distribution.py
```
（另有重建的 `dist/*`、`pyproject.toml`、`OWNER_LICENSE_DECISION.yaml`、`docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json`）

**→ 一個 15 檔的 commit，即可把「不可綁定」轉為「可綁定」。**

### F5. 發行閘門的機制已釐清

```
$ python tools/build_publication_manifest.py --help
  --commit COMMIT   published subject commit (default: resolve r3-candidate)
  --check           verify the projection; non-zero on violation
  --current         with --check: also FAIL while any current worktree product path is UNCOVERED
```
閘門需要的是**一個已 commit 的主體**；`--current` 之所以 FAIL，是因為現行工作樹的產品路徑**沒被任何 manifest 覆蓋**。

### F6. `__pycache__` 不構成風險
`git status --porcelain | grep -c __pycache__` → **0**（已被 ignore）。

---

## 2. 缺口可閉合性矩陣（本報告的核心）

| # | 缺口 | 我方能閉合？ | 需要什麼 |
|---|---|---|---|
| **G1** | GitHub 來源讀回（§2.1-3） | **可以，完全可，且零憑證** | `git fetch origin r4-candidate` |
| **G2** | 血緣綁定到受稽核的 `cd8a06e` | **可以** | 以 `cd8a06e` 為基底開分支，commit 上述 15 檔 |
| **G3** | 發行投影 manifest／attestation | **本機可** | 先有 G2 的 commit，再 `--write` → `--check` |
| **G4** | **推上 GitHub 供外部驗收官看** | **不行 — Owner 動作** | Owner 授權遠端寫入 **＋** 具 `contents:write` 的憑證，**或由 Owner 自己推** |
| **G5** | 授權／公開發行範圍 | **不行 — Owner 裁定** | Owner 決定（現值 `LicenseRef-PIPD-Proprietary`＝**非授予性**） |
| **G6** | **UAT 的「非 Maker 獨立 Checker」** | **不行 — 不可自派** | Owner 指派獨立檢查者（真人，或一個 **harness 非 Maker 所撰**的獨立運作車道） |
| **G7** | S2 閾值 provenance | **已由 Owner 完成**（2026-10-10） | —（契約重新定義；artefact 未變） |
| **G8** | `WO-HGK-ORCH-007` MSYS 路徑安全 | **有條件** | 僅當 S4 真的走該 orchestration；否則列 S5 前置 |
| **G9** | `F-R4-TRACE-08`／`F-R4-GOV-09` | **依設計 deferred** | Owner 決定是否納入範圍 |
| **G10** | **「S4 級 PASS」本身** | **不行 — 依構造如此** | 那是**檢查者在凍結主體上的作為**；Maker 不可能產出自己的驗收 |

---

## 3. 對「是否根本不可能」的直接回答

**分兩層，必須分開講：**

1. **「本機技術缺口全部關閉」→ 完全辦得到，且成本低。**
   剩餘工程 ≈ ① fetch（秒級）② 以 `cd8a06e` 為基底 commit 15 檔 ③ 重生 publication manifest ④ 在凍結 tuple 上重跑檢查者。
   這四步裡**沒有一項需要本回合目前缺的任何東西**。

2. **「我方自行完成 S4 級驗收」→ 結構上不可能，且不應嘗試。**
   依 R5 指令 §9，`PASS` 的定義是「**有權獨立 Checker** 對同一 frozen subject 確認」。Maker 產出自己的 `PASS` 正是本回合全程禁止的**自簽**。此外 G4／G5 是 Owner 的權利，不是能力問題。

> **所以：不是「不可能辦到」，而是「有 4 件事必須由 Owner 做或授權，其餘我方可以自己收掉」。**

---

## 4. Owner 最小行動清單（建議）

| 序 | Owner 需做／授權 | 為什麼不能由我方代替 | 若不做，後果 |
|---|---|---|---|
| **A1** | 確認「可匿名讀取公開 repo」即為 §2.1-3 的可接受來源（或明示需要 PAT 身分） | 來源適格性是規範判斷 | G1 無法在報告中被標為已閉合 |
| **A2** | 授權一個**可寫入的推送目標**（既有 `r4-candidate` 的安全工作分支，或新修補 PR 分支）**＋** 具 `contents:write` 的憑證；**或由 Owner 自行 push** | 遠端寫入與憑證使用是 Owner 的權利；我方未被授予 | G4 永遠不成立 → 外部驗收官**在 GitHub 上無物可驗** |
| **A3** | 裁定**授權與公開發行範圍** | 授權決定權屬 Owner | G5 不成立；即使推上去也不能公開 |
| **A4** | **指派一位非 Maker 的獨立檢查者**（並確認其 harness 非 Maker 所撰），對凍結 tuple 執行 S4 安全負例／wheel 資源／export／UAT-00～12 | **Maker 不得自簽**；指派權在 Owner | `INDEPENDENT_PASS` 永久不成立 → §9 的 `PASS` 不可達 |

**（可選）A5**：若希望 `F-R4-TRACE-08`／`GOV-09` 於本輪閉合，需 Owner 明確納入範圍；否則它們依設計維持 `deferred`。

---

## 5. 本報告的證據與限度

**已量測（可重跑）**
- 網路可達性：`api.github.com` 200、`github.com` 200
- 匿名 `git ls-remote`：欄位如上（**未使用任何憑證**）
- 匿名 `git clone` 至 scratch（**產品樹外**）：`C:\...\hermes\cache\scratch\far-r5s4-lineage\repo`
- 血緣：`rev-list --count 3aebbbc..origin/r4-candidate` = 2；`diff --stat` = 135 files / +48977
- 位元組比對：6 檔 IDENTICAL（見 F3 表）
- 差異範圍：15 檔（排除 `__pycache__`，且以 `--ignore-cr-at-eol` 消除換行雜訊）

**未做（明確聲明）**
- **未**修改產品 repo：**未** fetch 進 `C:\Projects\Agent_Workspace\PIPD`、**未** commit、**未** push
- **未**讀取、**未**使用任何 PAT／secret
- **未**進行任何遠端寫入
- `git status` 仍為 78 項 dirty（與本報告開始前一致）

**本報告不得被引用為**
- 發行授權、外部驗收、或 `INDEPENDENT_PASS` 的依據
- 「缺口已閉合」的證明——本報告證明的是**可閉合性**，不是**已閉合**

**宣稱上限**：`FEASIBILITY_ONLY`。本回合產品宣稱上限不變：`S4_REPAIR_CANDIDATE_LOCAL_TESTED`。
