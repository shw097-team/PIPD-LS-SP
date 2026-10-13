# R3 PUBLICATION — S4POST 三合一小型升級（FAR 低阻力方案執行輪）

> **這份文件是外部驗收官的入口。** 它說明：要驗什麼、去哪驗、用什麼命令、預期看到什麼、
> 以及**本輪沒有做、也不主張**的事。
> 本文件為候選交付說明，**不是**驗收、不是 PASS、不是發布核准。

## 1. 受驗主體（哪兩個分支、哪個 sha）

### 綁定說明（本文件**不**綁定自身所在的 commit）

- **受驗 commit（送驗基準）**：`3ec55572594e`（product 支 `feat/s4post-triple-upgrade-20261013-r3`，於 2026-10-13 送驗時讀取）；
  載具支 `chore/s4post-verification-harness` 同期為 `c7b560022b71`。
- 本文件本身是**其後的證據／文件提交**。一個記錄 `as_of = HEAD` 的檔案**不可能**等於它所處的 commit
  （寫入該值就會改動它該命名的那個 commit）——**此為設計，不是缺陷**。
- 因此：**驗收請綁定你要驗的那個 commit，而非分支 tip**；最新 tip 以 `git log --oneline -1` 取得即可。

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

## 3. 驗收命令與預期輸出（在**匿名 clone** 內執行；可直接複製）

**前提**：**不可**加 `--depth`（4 個 provenance 測試會讀取 tag 與歷史）。

```bash
git clone --branch feat/s4post-triple-upgrade-20261013-r3 \
    https://github.com/shw097-team/PIPD-LS-SP.git /tmp/r3 && cd /tmp/r3
R=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
python -V
python -m unittest discover -s tests -p 'test_s4ext_*.py' -v
#   實測：Ran 108 tests ... OK                                (exit 0)
python -m unittest discover -s tests -t . -v
#   實測：Ran 572 tests ... OK (skipped=3 本機 / 4 獨立第三方環境)  (exit 0)
#   skip 數隨環境而異（第三方多 1 個 skip），非缺陷

cd "$R"
python verify/tools/check_evidence_locators.py --root . --search-dir . \
    verify/ao12/EXTERNAL_CHALLENGE_REPORT.md
#   實測：exit 2 / FAIL_LOCATORS_NOT_RERUNNABLE —— R6 的**負向對照**，FAIL 是正確結果
python "$R/verify/tools/check_evidence_locators.py" --root . --search-dir . \
    "$R/OWNER_ACTION_REQUEST.md" "$R/HARNESS_FREEZE_AND_AO_LOOP_CAP.md"
#   實測（於**產品分支內容**，非含載具的工作樹）：exit 0 / PASS_LOCATORS_IN_TREE
#   兩個 --search-dir 是必要的：這些文件同時引用「回合相對」與「repo 根相對」定位。
#   逐支結果見 verify/tools/LOCATOR_CHECK_R3_POSITIVE.json 的 per_subject 欄位。
#   注意：**不要把本文件（R3_PUBLICATION.md）放進這個對照**——它含 shell 指令，
#   指令中的 URL 與 /tmp 路徑不是檔案定位，檢查器會（正確地）拒絕它們。
cd /tmp/r3
```

**OpenSpec（需本機已安裝 CLI）**：匿名 clone 內沒有 `node_modules`，`npx --no-install openspec`
因此無法解析——本輪的原始驗證輸出已存檔，直接讀取即可：

```bash
cat "$R/surface/OPENSPEC_R3_EVIDENCE.json"   # 內含 `Change 's4post-triple-upgrade' is valid` 原始輸出
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

事實背景（裁決 §3.1 確認）：受驗 5 分支 + 3 tag 全部 **0 個 `.github/`**、Actions runs = **0**。

**本輪實測（非規劃）**：

1. 首次推播後 `ci` 啟動，但在**第 2 步 "Check out the frozen subject" 就失敗**，步驟 3–9 全部 skip → 逐字 log：
   `fatal: No url found for submodule path '.hgk/rounds/R2-20261009-qualification/execute/candidate' in .gitmodules` ＋
   `The process '/usr/bin/git' failed with exit code 128`。
   即 4 個**無 `.gitmodules` 的 gitlink**（`main` 即有，來源 `829c17e8…`）使 `actions/checkout` abort →
   **這條 CI 在此之前從未真正驗過任何東西**。
2. 修補（本輪唯一超出 R1–R8 的動作，已揭露）：移除那 4 個**空目錄** gitlink（磁碟上 0 個項目，不失內容）。
3. 第二次執行在第 7 步失敗：`dist/` 內有兩顆已版控 wheel（`0.1.0`、`0.1.1a3`）→ `pip install dist/*.whl` 觸發
   `ResolutionImpossible`。修補：改為只安裝**剛建出的** wheel（更嚴，非放寬）。
4. **結果：三條分支的 `ci` 全綠（各 13 步、零失敗）**，含全量套件、聚焦套件、wheel 乾淨安裝＋`pipd doctor`、
   來源閘門、**突變負向校準**。逐字與逐步驟見 `R3_CI_FIRST_RUN.md`。
5. Draft PR **#2**：`https://github.com/shw097-team/PIPD-LS-SP/pull/2`（`draft=true`，不請求合併）。
   另一 workflow `public-plugin-verify` 對本 PR 為 **failure**，原因為其審查 base 取 `main` 而本支疊在 Stage-A 上
   （見 `R3_CI_FIRST_RUN.md` §3 的量化），**未改動該守衛語意**，提請 owner（D3）。

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

- 測試原始 log：`verify/r3/raw/focused.log`、`verify/r3/raw/full.log`。**兩種 sha256 皆記錄**（獨立第三方指出差異）：
  **worktree/EOL 形態**（原記錄，含 CRLF）：`88d8db81…` / `185a6177…`；
  **版控 blob 形態**（`.gitattributes` `* text=auto eol=lf` 正規化後，可由 clone 重算）：保留於 `evidence/EVIDENCE_RETURN_PACK.json` 的 `log_sha256_committed_blob`。
- 發布資產下載讀回：`verify/r3/RELEASE_ASSETS_READBACK.json`（5/5 相等）。
- locator 檢查原始 JSON：`verify/tools/LOCATOR_CHECK_R3_POSITIVE.json`、`verify/ao12/LOCATOR_CHECK_AO12.json`。
- **GitHub 端結果**：PR **#2**（draft）＋三條分支 `ci` 全綠＋`public-plugin-verify` 紅（scope），
  逐字 log 與失敗步驟分析見 **`R3_CI_FIRST_RUN.md`**（同輪文件；本文件不與自身 commit 互相綁定）。

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

## 10. §3.3 產品面允許集稽核（並行子代理 + maker 自行重測）

- 7 項條目、其中 3 項 HIGH；**每一項 HIGH 都由 maker 自行重測後才採用**。逐條見
  `verify/far/FAR_S3_3_SURFACE_AUDIT_20261013.md`。
- 摘要：icon 兩檔確實缺席（owner 輸入 A4）；允許集路徑 `packaging/public-plugin/requirements.lock` 缺席，
  而 repository 根目錄那份自述「NOT HASH-PINNED … `--require-hashes` will therefore NOT work」；
  `plugin.schema.json` 內容是**本地撰寫子集**，官方 vendor schema 實體存在於非允許集檔名 `vendor-plugin.schema.json`
  （即官方 schema **已在樹內**，缺的是檔名對位與 digest 釘選 → owner 輸入 A2）。
- 另：`plugin.json` 內 `OWNER_INPUT_REQUIRED` 佔位是 builder 的 fail-closed 設計，但同時被提交 → 提請 owner 決定命名。
