# R3 PUBLICATION — S4POST 三合一小型升級（FAR 低阻力方案執行輪）

> **這份文件是外部驗收官的入口。** 它說明：要驗什麼、去哪驗、用什麼命令、預期看到什麼、
> 以及**本輪沒有做、也不主張**的事。
> 本文件為候選交付說明，**不是**驗收、不是 PASS、不是發布核准。

## 1. 受驗主體（哪兩個分支、哪個 sha）

| 角色 | 分支 | tip | 內容 |
|---|---|---|---|
| **產品變更集**（建議的受驗主體） | `feat/s4post-triple-upgrade-20261013-r3` | `5df5a3f0f41a15027f06f8a5d9b9c16755cca566` | 產品面（`packaging/`、`tools/`、`tests/`、`docs/install/`、`README.md`、`.github/`）＋本回合的驗收面向文件 |
| **驗證載具與其證據** | `chore/s4post-verification-harness` | `9863c5552190c4100837df7c7dcd182229346d47` | 本回合的載具（`stage-b/`）與其 12 輪中間驗收 bundle（`verify/ao*/`、`verify/harness/`、`checkpoint/`） |
| 前次已發布線 | `feat/s4post-triple-upgrade-20261012-r2` | `9863c555…`（由 `2fc17c0…` **快進**） | 保留原分支名並前移，非強制推送 |

`main` 仍為 `224591431a164ab72a9423cd180e417e8a762403`（**未動**）；三個發布 tag（`v0.1.0-preview.1/2`、`v0.1.1-preview.3`）**未動**。

**為何切成兩個分支（FAR R2）**：先前的變更集相對 `main` 有 **1,239 個變更檔**，其中 **1,119 檔（90%）是本回合自建的驗證載具與中間 bundle**。
治理文件對此有逐字禁令——裁決 §0 總裁定：*「不批准把 CI、Agentic Harness 或風險系統全面擴建」*，且藍圖 INV-01 要求 ONE CHANGESET、A42 要求最小寫入足跡。
切分後**產品變更集為 120 檔**，載具獨立成支。**哪一支是受驗主體屬 owner 裁決**（見 §7 D3）。

## 2. 本輪改了什麼（R1–R8 與四個治理表面）

| 項 | 產出 | 位置 |
|---|---|---|
| FAR 偏離研究 | 對三份治理文件逐條比對，6 項偏離（含對**我自己載具超建**的 DEV-01） | 產品支 `verify/far/FAR_S4POST_DEVIATION_AND_REMEDIES_20261013.md` |
| **R1/R8** 凍結與輪數上限 | 不再擴充驗證軸、不再派 AO13、殘餘 finding 轉 CR/TT；同 round 外部複驗上限 2 輪 | `HARNESS_FREEZE_AND_AO_LOOP_CAP.md` |
| **R2** 變更集切分 | 1,239 → 120 檔；載具獨立分支 | 本文件 §1 |
| **R3** 證據包補齊 | PB-090 缺的 3 欄：`commands`（聚焦 108／全量 572，皆 OK）、`release_assets`、`manifest_sha256` | `evidence/EVIDENCE_RETURN_PACK.json`＋`verify/r3/raw/*` |
| **R4** owner 行動請求 | 4 項 owner 供給、4 項 owner-only 行為、**12 項外部證據**、3 項設計裁決 | `OWNER_ACTION_REQUEST.md` |
| **R5** 最小 CI 首次實跑 | 以 Draft PR 觸發（結果見 §5） | `.github/workflows/public-plugin-verify.yml`（未改） |
| **R6** 證據可重跑＝斷言 | `check_evidence_locators.py`；正向對照 PASS、AO12 bundle **FAIL**（5 個樹外定位，含車道不可讀暫存根與**樹外的正規車道契約**） | `verify/R6_EVIDENCE_RERUNNABILITY.md`、`verify/tools/` |
| **R7** SoD 逐列身分 | producer `user`（SID `…-1000`）／checker `CodexSandboxOffline`（`…-1004`） | `evidence/EVIDENCE_RETURN_PACK.json → sod` |
| KANBAN | 盤 `s4post-r3-remedies`＋SWARM 圖（root `t_fc25bc79`、6 workers、verifier `t_e392ea37`、synthesizer `t_33a81182`） | `kanban/R3_BOARD_EVIDENCE.json` |
| GSTACK | `named_methods.route()` 真實執行；14 項激活不變式**皆為 0** | `surface/GSTACK_R3_ROUTE_READBACK.json` |
| OPENSPEC | 官方 CLI 驗證：`Change 's4post-triple-upgrade' is valid`；tasks.md 新增 R3 段落（未改動既有狀態） | `surface/OPENSPEC_R3_EVIDENCE.json`、`openspec/changes/s4post-triple-upgrade/tasks.md` |
| **HGK admission（typed）** | 本回合 7 項義務以 canonical `ProjectLifecycleController.admit_requirement` 准入至專案 `PIPD-LS-SP-20261008`（`EXECUTING`）：`REQ-PIPD-R3-{FAR-001,EVIDENCE-002,CI-003,SURFACES-004,OWNER-005,PUBLISH-006,VERIFY-007}` → 各 `requirement_state=FROZEN`＋`TS-*`＋`WO-TS-*`，`errors=[]`，checkpoint `CK-20261008-3181EC0D` | `admission/hgk_r3_admission.py`、`admission/r3_admission.json` |

## 3. 驗收命令與預期輸出（在**匿名 clone** 內執行）

```bash
git clone --branch feat/s4post-triple-upgrade-20261013-r3 \
    https://github.com/shw097-team/PIPD-LS-SP.git /tmp/r3 && cd /tmp/r3
python -V                                  # 3.11+
python -m unittest discover -s tests -p 'test_s4ext_*.py' -v
#   預期：Ran 108 tests ... OK              (exit 0)
python -m unittest discover -s tests -t . -v
#   預期：Ran 572 tests in ~210s ... OK (skipped=3)   (exit 0)
python verify/tools/check_evidence_locators.py --root . --search-dir . \
    verify/ao12/EXTERNAL_CHALLENGE_REPORT.md
#   預期：exit 2，verdict FAIL_LOCATORS_NOT_RERUNNABLE（這是 R6 的**負向對照**，FAIL 是正確結果）
python verify/tools/check_evidence_locators.py --root . --search-dir . \
    OWNER_ACTION_REQUEST.md HARNESS_FREEZE_AND_AO_LOOP_CAP.md
#   預期：exit 0，verdict PASS_LOCATORS_IN_TREE
npx --no-install openspec validate s4post-triple-upgrade --strict
#   預期：Change 's4post-triple-upgrade' is valid
```

新發布資產的獨立下載驗算（**不是**只讀 API 的 `digest` 欄位）：

```bash
curl -sL -o /tmp/a.whl https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.3/pipd_ls_sp-0.1.1a3-py3-none-any.whl
sha256sum /tmp/a.whl   # 應等於 Release API 的 digest（本輪已匿名驗過 5/5 相等）
```

## 4. 本輪**沒有**做、也**不主張**

- 未執行：Portal 任何狀態（draft/scan/review/publish）、四主機真實 UAT、`SECURITY_SCAN`、真實 candidate build。
- 未主張：`BUILD_PASS`、`LOCAL_HOST_QUALIFIED`、`PORTAL_APPROVED`、`PUBLISHED`、`PRODUCTION_VERIFIED`、`PIPD_S4_FULL_PASS`。
- 未執行：任何 `main` 推送、force push、tag 異動、merge、已發布資產替換。
- **獨立驗收的最近一次裁決仍是 `FAIL_CHALLENGE`**（AO12，9 項 finding，全部位於本回合自建的驗證載具內），已如實記入證據包 `independent_checker`。
- **Tag → Source → Build → Asset 的可重建性仍為 OPEN**：本輪證明的只是「已發布資產的**下載位元組**等於 API 回報 digest」，不是「可由該 tag 重建出同一資產」。

## 5. 最小 CI 的首次實跑（R5）

- 事實背景（裁決 §3.1 確認）：受驗 5 分支 + 3 tag **全部 0 個 `.github/`**、Actions runs = 0。
- 本輪 workflow 已在分支上，且規格吻合裁決要求：`permissions: contents: read`、SHA 釘選 checkout
  (`11bd71901b…`)、**無** `pull_request_target`、Python 3.11、全量 unittest、fail-closed 負向步驟。
- Draft PR 的嘗試與其原始結果見 §8（**結果後來才補記**，故此處不預寫結論）。

## 6. 已知缺陷與自曝（含我方造成者）

1. **DEV-01（我方）**：本回合變更集 90% 是未經批准的驗證載具擴建——已由 R2 切分修正，並在 FAR 中記為偏離。
2. **車道證據 ACL（我方）**：AO10/11/12 的證據放在車道自己的 temp root，maker 身分**不可讀**；已在 R6 以斷言化工具抓出，尚未修（屬車道 wrapper 設計）。
3. **正規車道契約在樹外**：`~/.agents/skills/fabric-external-independent-challenge-reviewer/**` 未進版控，與裁決抱怨的「參照腳本與模板未掛載」同源（R6 發現 2）。
4. **探針缺陷（我方，兩次）**：以不在 PATH 的 `python` 誤判「缺 jsonschema」；初版 locator 檢查器把散文簡寫當定位造成假紅——兩者都已更正並記錄。
5. **既有 gitlink（非本變更）**：``.hgk/rounds/R2-20261009-qualification/**` 有 4 個 `160000` gitlink（來源 commit `829c17e8…`），在 `main` 即存在；依「凍結樹內缺陷揭露不修」原則**不動**。

## 7. 需 owner 裁決（本文件不代答）

- **D1** 宣告 EXECUTE 模型的補跑 vs 接受為 owner-approved 偏差（`FAR-S4POST-MODEL-DEVIATION-20261012-001` 仍 `not_applied`）。
- **D2** 本輪**單一整合候選**由誰簽（同時解 `FCR-007`／`TT-S4POST-EVIDENCE-06`）。
- **D3** 受驗主體為 §1 的**產品支**或**載具支**（或兩者並驗）。
- **D4** 四項 owner 供給與四項 owner-only 行為（`OWNER_ACTION_REQUEST.md` A/B 節）。

## 8. 附錄：本輪的原始結果與 PR 嘗試

- 測試原始 log：`verify/r3/raw/focused.log`（sha256 `88d8db81…`）、`verify/r3/raw/full.log`（sha256 `185a6177…`）。
- 發布資產下載讀回：`verify/r3/RELEASE_ASSETS_READBACK.json`（5/5 相等）。
- locator 檢查原始 JSON：`verify/tools/LOCATOR_CHECK_R3_POSITIVE.json`、`verify/ao12/LOCATOR_CHECK_AO12.json`。
- GitHub 端（Actions／PR／release）**結果將記於 `R3_PR_ATTEMPT.md`**（同一分支後續提交），避免本文件綁定自身所處的 commit。

## 9. HGK 准入（canonical，typed API）

- 專案：`PIPD-LS-SP-20261008`，lifecycle state `EXECUTING`（可准入），run `RUN-DC744863`。
- 以 `SharedSpine(hgk_root/var/shared-spine/hg-kseos.db, hgk_root/src/hg_kseos/schema.sql)` ＋
  `ProjectLifecycleController.admit_requirement(...)` 准入 **7 項**義務（見上表），每項由 spine 生成
  requirement（`FROZEN`）＋ taskspec ＋ workorder；`errors` 為 **空**；checkpoint 已建立。
- 收據：`admission/r3_admission.json`；腳本：`admission/hgk_r3_admission.py`（照 R9–R11 既有形狀，
  新 id 不動任何既有列）。

**自曝的順序偏差（deviation）**：`REQ-PIPD-R3-SURFACES-004` 的文字要求「工作產物寫入前先跑准入」，
但本回合實際上是在多數產物已寫入**之後**才補跑准入（retroactive admission）。此偏差已記錄，未粉飾；
其後果是准入為事後凍結，而非事前授權。此點需 owner 知悉。
