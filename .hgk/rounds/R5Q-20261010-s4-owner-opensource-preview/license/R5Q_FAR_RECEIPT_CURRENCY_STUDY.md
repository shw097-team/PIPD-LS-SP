# R5Q｜證據時效保留 FAR 快速研究（Receipt Currency / Mutable Entry Points）

**研究編號：** `FAR-PIPD-R5Q-RECEIPT-CURRENCY-001`（本次研究識別碼，非新增 Gate／TT）  
**輪次：** `R5Q-20261010-s4-owner-opensource-preview`  
**研究日期：** 2026-10-10；現場回讀截至 `2026-10-10T15:58:09Z`（UTC，臺北為 2026-10-10 23:58:09）  
**授權與施工上限：** 只建立本研究文件；不修改任何既有檔案，不執行 git，不 push，不修改 GitHub，不執行實際 VERIFY／發布／撤回。  
**角色分離：** 本文是 PLAN/FAR 建議，不是 Independent PASS；實際關閉須另由符合原契約的非 Maker Checker 發出新收據。

---

## 1｜研究問題（ResearchRequest）

第一份收據於 `2026-10-10T15:40:56Z` 發出，早於 main 的 README-only 入口更正，以及 live release body／PREVIEW_NOTES 資產更正。要消除的是「以較早收據代表更正後公開狀態」的證據鏈缺口，不是要重造已驗證的產品。

**裁決先行：採 A——同一 preview.1 主體、指定模型的獨立 VERIFY 重跑，新增可變公開入口與全部上傳資產的覆蓋；以新收據及 append-only supersession index 取代舊收據的『當前驗收入口』地位。保留舊收據原 bytes。** 不建立新 tag，不重建 wheel，不改 main，不再重傳產品資產。這是能關閉本保留的最低阻力方案；只寫本文或改一個狀態標籤不能關閉。

另有一項必須先面對的反證：主報告 §11 稱最終 readback `12/12 PASS`，但本次讀到的指定 `R5Q_PUBLICATION_READBACK.json` 是 `FAIL`，不是該 PASS。不得把報告當成原始收據。本方案必須產生一份新的、可重推導的 raw readback 和獨立收據，而非沿用該檔案。

## 2｜已凍結事實與來源處置（SourceDisposition）

### 2.1 本地治理文件（全文已讀）

下列 `ROUND` 均為 `C:/Projects/Agent_Workspace/PIPD-r5q-release-wt/.hgk/rounds/R5Q-20261010-s4-owner-opensource-preview`。

| Locator | 本次取用的事實／規範 | 位階 |
|---|---|---|
| `ROUND/evidence/R5Q_FINAL_REPORT.md` §6.1、§11 | 原收據兩項 qualification：模型 lane deviation、早於入口更正；更正是 additive main README 及 live body／notes；tag／wheel 未變 | 輪次主張，須以 raw 證據校核 |
| `ROUND/evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT.json` `issued_at_utc`、`claims`、`scope_note` | `15:40:56Z`、9/9 PASS、`PASS_ONLY_THE_ABOVE_CLAIMS`；模型 `deepseek-v4.1-flash`；immutable subject 有精確 commit/tree/wheel SHA | 歷史原始收據 |
| `ROUND/license/R5Q_FAR_LICENSE_QUICKSTUDY.md` §3–7 | 沿用候選比較、反證、裁決、落地步驟、殘餘風險及 claim ceiling 結構；不重開授權選型 | 既有 FAR 決策 |
| `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/PIPD/PROMPT/PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md` §4、§5、P5/P6、§7、§8 | 禁覆寫 main／force-push／改既有 tag；禁止第二 repo；只能 affected-only、Maker 不自簽；歷史證據不可倒填；公開後須獨立重讀 | 治理約束 |
| `ROUND/compiler/R5Q.CONTRACT.json` `independent_checker`（搜尋定位） | `GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER` | 本輪指定 checker 身分；不等同已證明可用的模型 wire id |
| `ROUND/evidence/R5Q_PUBLICATION_READBACK.json` L3、L53–85、L107–121 | `read_at=15:44:15Z`；notes 下載 `6334 B / 3f4ebba3…` 不符 expected `a46daaf3…`；README/API 403；`all_assets_match=false`；`verdict=FAIL` | 本次實讀的原始反證 |
| `ROUND/tools/r5q_publish.py` L66–118、L121–158 | 已有 `RateLimited` 類別、raw-file fallback；readback 工具亦有 local git 使用，不能在本次「不動 git」研究中直接執行 | 工具定位，不當獨立驗收 |

原獨立收據檔 SHA256：`1eb524c3154335971bece8ed844b07308ffd9967ff762b7413364f11142c5322`。本次讀到的 raw readback 檔 SHA256：`e994e253e678a00d70085e552b66816f11a8310fba9e4a16ed56a4d697e2d215`。上述值由實際讀檔運算，不是複製報告。

### 2.2 GitHub 真實現場（匿名 GET、fresh download，非本地 release cache）

匿名 REST API 實際回 `403: rate limit exceeded`；加唯一 query 後仍為 403。改讀 GitHub HTML、raw CDN、commit patch、release download，沒有取用 PAT。commit HTML 的兩次查讀為 406，未把它當 PASS。以下是成功取得的現場，不能擴張成全部 API metadata 已驗：

| 主體 | 現場結果 | 支持／邊界 |
|---|---|---|
| Repo 前台 | HTML embedded data：`defaultBranch=main`、`currentOid=de3a1d9e3a6298fa0dd29fafbf11d850e30c743a` | 實讀公開前台。[6] |
| `main/README.md` | `5359 B`；SHA256 `43c96a7610b49f44a49e4637fd9ab0871133c969749efce9e4a19a05dc4d6a6d`；首屏指 preview tag、Apache-2.0、release page；其下標 R3 historical snapshot，禁止預設從 main 安裝 | TT-R5P-08 的可見入口已更正。[1] |
| 指定更正 commit patch | Date `2026-10-10 23:41:22 +0800`；只一個 `README.md` diff，14 insertions | patch 支持 README-only；author date 不是 server push timestamp，也不能單憑 patch 證明父 commit／無歷史改寫。[3] |
| tag 的 GitHub tree 頁 | `currentOid=cc9bf574c3b3f0f44ea615b5c67ae40d74efee32` | 本次重新看到 tag 指向 release commit；tree SHA 仍需下一位 checker 讀 git object。release body 所列 tree 並非獨立 object 證明。[7] |
| live release body | 已把 main 描述改成 R3 content preserved、只 advanced by pointer commit；仍標 prerelease、Apache-2.0、DEL-018 FAIL、PARTIAL_CHALLENGE、NOT GRANTED ceilings | 已觀察更正正文；API `updated_at`／`draft=false`／release id 本次無法 fresh 確認。[5] |
| wheel fresh download | `252618 B`；SHA256 `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60` | 與原收據／SHA256SUMS／GitHub asset 顯示 digest 一致，未變。[8][10][4] |
| source.zip fresh download | `3654658 B`；SHA256 `8faaaa5a171c3ba62e5483e2418854936965015ef976dfb92a74cffa569659b0` | 與主報告／SHA256SUMS／asset 顯示 digest 一致，未變。[9][10][4] |
| SHA256SUMS fresh download | `205 B`；SHA256 `d32cdefb112665c92bb0e252906ec8cba654d0a87acdf0e43f3beccae2535b50` | 只列 wheel、source.zip；兩列均實際重新計算通過，未把 notes 偽裝為此檔已覆蓋。[10] |
| 更正後 notes fresh download | `6495 B`；SHA256 `a46daaf3692454cdfead909191e0f9a7bf0ebeb2c497739b179c7171ff3eabc4`；說明 main 是 R3 line plus pointer | 已匹配 raw readback 的 expected，但不匹配該 raw 檔記錄的舊 downloaded bytes。asset 列顯示時間 `2026-10-10T15:44:09Z`；不冒稱此 HTML 時間就是 API `updated_at`。[11][4] |

**時間順序的可靠表達：** 原收據 `15:40:56Z` → main patch 記錄 `15:41:22Z` → notes 現場顯示 `15:44:09Z` → 舊 raw readback 記錄 `15:44:15Z` → 本次現場 fresh downloads `15:56–15:58Z`。live body 更正的精確 server timestamp 本次未取得。原收據／§11 已明示先驗後改，且新 notes 顯示時間確實晚於原收據；本次不猜 API `updated_at`，也不從 commit author date 推論 push 時刻。

**獨立反證：** 實際解開 fresh source.zip（記憶體內、不落地）後，其中 `.hgk/rounds/R5Q-20261010-s4-owner-opensource-preview/release/RELEASE_BODY.md` 仍寫 main **not touched**；archive 內 notes 說 main 是 R3 snapshot，live uploaded notes 則已改成 R3 plus pointer。這是已凍結 source 與後改 mutable 說明的歷史差異，不能聲稱「所有舊產物都已內含更正文」。[9][11]

## 3｜保留的精確範圍（FitGap / Invalidation）

| 原 claims / 新入口 | 時效影響 | 正確處置 |
|---|---|---|
| claim 1：tag → commit → tree | 入口更正不改上述 objects；本次 tag 頁重讀一致，但未重新取得 tree object | 不使原 immutable PASS 因 README 改字而失效；新 checker 仍讀 object 核實未漂移 |
| claim 2：prerelease、limitations、licence | 正文被改，原收據不證明新正文 bytes；局部性質可能仍成立 | 新 receipt 綁 release id、flags、body SHA、讀取時刻與內容條件；不能只覆述舊 PASS |
| claim 3：wheel/source hash 三方一致 | wheel/source/SHA256SUMS 未變；notes 重傳不在舊 checksum 兩列內 | 新下载全部 4 個上傳資產，notes 另綁 asset id/digest／bytes；明列輪替 notes 的歷史身份 |
| claims 4–7：wheel licence、安裝、schema、design、typed negatives | README/body/notes 不改 wheel bytes，沒有因果 invalidation | 新指定模型重跑原限定 VERIFY 可同時移除模型保留；不重建產品、不跑完整 57 rows／全 suite |
| claim 8：claim ceiling | 讀取位置必須區分 tag README、main README、live body、live notes；不能同名 README 混為一談 | 檢查現行首屏指 preview，歷史 no-grant 等舊段落有 snapshot framing；只要求含界定區的限制，不要求把全部歷史字串刪掉 |
| claim 9：no stop-ship counterexample | 舊產品安全測試是舊觀測；新入口差異不等於安全缺陷 | 維持原場景／負例邊界，再做當期限定安全驗證；不推出全安全認證 |
| 新項：default branch README／additive ancestry | 原 9 claims 沒有證明 main 首屏正確；讀 tag README 過關不能代替它；本次也實讀 tag README，但它是另一個受驗位置。[2] | 本次最關鍵增項：default branch lookup → pinned main SHA → README bytes；父 commit 及 README-only diff → R3 lineage |

**完全不因這次更正改變的主體：** release tag／release commit／release tree（依更正機制與歷史證據；本次 tree fresh object 待補）、wheel bytes 及其封裝 licence/schema/code、source.zip bytes。可變的是 branch tip／main README、release body、notes asset identity/bytes。GitHub 上傳資產不能因「附在 immutable tag 下」就推論平台保證 immutable；此次 notes 替換本身即反例。[4][11]

**不能借此關閉：** `DEL-018 FAIL/EVIDENCE_GAP`、`PARTIAL_CHALLENGE`／`28/10/19`、Windows／host-native／S5–S8／PRE-W3、無 signature/attestation、完整 CVE scan 等。收據時效是 scope 問題，不是 product full-gate 問題。

## 4｜候選方案與判詞（Alternatives / RejectedAlternativeLedger）

成本是規劃估計，不是已測工時；以一位 bounded executor 加一位獨立 checker、現有授權與現場可讀為前提。模型安裝／OAuth／配額阻斷無法給有限保證。不要用無來源的加總分數假裝精準。

| 候選 | 1. 關閉時效保留？ | 2. 治理合規／碰觸物件 | 3. 可稽核性 | 4. 消費者實害 | 5. 工時與成本（估計） | 6. 新未收斂狀態 | 判詞 |
|---|---|---|---|---|---|---|---|
| **A 指定模型重跑 VERIFY＋擴及現行入口／資產＋supersession** | **可**，但只有在所有最後更正後實際採樣、發新收據且無再漂移時；本研究尚未執行 | 不須更動 main/tag/commit/tree/wheel；只追加 evidence/index。不得回寫舊 JSON。若需公告另走 bounded admission | 最強且最短：old digest → change boundary → fresh observations → new receipt → append-only index | 不增加版本／安裝身份；仍有 archive 內歷史說明，需明示不是現行平台狀態 | 約 30–90 分鐘的 readback＋限定 clean-install VERIFY＋封存；若嚴格 CODEX lane 不可用則 BLOCKED，不偷換 | 只增加一個 successor 收據鏈；固定一個 current pointer，原 receipt 是 HISTORY | **首選：最低『有效關閉』阻力** |
| **B 新 tag preview.2＋新 prerelease、immutable source 內含更正文** | 新版本仍須發布後獨立驗收；只發 tag 不會關閉。新 receipt 能驗新版本，但 preview.1 的時間缺口只能標 retired/historical，不能倒填 | 保留 preview.1、不 force-push、不改 main／不建 repo 時可合規；新 commit/tree/source 肯定變。wheel 是否改依 packaging，不可假裝必定沿用 | 可形成雙版本完整鏈，但新增 identity/build/manifest／checksum／入口轉向及新驗收 | 優點是新 source 可攜更正文；代價是兩份 preview 並行、舊下載仍存在。若沿用同 wheel version/name 增混淆 | 約半天起：版本界定、source/release metadata、可能 rebuild、發布和獨立驗收；超出 A | 多一 tag、release、資產套組、維護／retirement 規則 | **合規備選；只有要求 immutable 包內亦要更正時才值得採用** |
| **C 撤回／deprecate 舊 release 並重發** | 改 status 或重發不能代替新 receipt；只能停止拿舊入口當 current，仍須 B/A 式新驗收 | Owner-authorised **deprecation notice＋superseding release** 可合規；刪 tag／移 tag 明確不合規；刪 release／資產再同名重發會破壞原證據入口，不採 | deprecate 保留原 bytes 可稽核；delete/recreate 同名會斷 release id／asset id／URL 連續性 | 消費者可能失去既有下載或把同名替代誤當原版；比 README 更正本身傷害大 | 不少於 B，再加公告與撤回風險核准，約半天至一天以上 | 舊版 retired、新版待驗、失效下載等多重狀態 | **目前無新 stop-ship，比例失衡；不採破壞性撤回** |
| **D 不動作，只在報告註記** | **否**；揭露等於接受保留，不等於時效 closure | 不碰主體，合規，但不能宣稱關閉 | 有誠實註記，沒有 post-correction independent readback | 沒新增 byte 混淆，仍無現行入口獨立收據；archive/notes 差異無新證據鏈 | 幾分鐘，零發布成本 | 原保留及模型偏離持續存在 | **只可作阻斷期間 checkpoint，不是修正方案** |

**為何不是 B：** 本保留的壞掉之處是 measurement 晚於／早於 correction 的關係。新 tag 把受驗主體換成另一個，仍然要付 A 的 fresh VERIFY 成本，且新增不可變身份；不修復舊 receipt 的時間順序。若 Owner 額外要求「離線 source 對 current platform 狀態也不得留歷史陳述」，那是不同驗收要求，此時選 B，不能將它混成 A 已承諾的 closure。

## 5｜裁決與可驗收的關閉定義（Decision）

**採 A，狀態 `RECOMMENDED_PENDING_INDEPENDENT_EXECUTION`。** 本文不是 `CLOSED`。

關閉判準必須全部成立：

1. 新 Checker 確實是非 Maker、不同 context/process，依 original contract 使用 `GPT 6.1 SOL-MEDIUM`／CODEX CLI／OpenAI OAuth；保存 requested 與實際 served model、effort、CLI/version、session id 與完整原始事件。若擬改用 Hermes／opencodex，先取得有權角色的明示偏離處置，不能稱原 lane 已遵守。
2. 原 9 claims 在原 immutable subject 重新驗；增加 default-branch README、additive main ancestry／README-only diff、live body、更正 notes 與 4 上傳資產身份／hash 覆蓋。可拆分 claims，但固定分母由實際清單生成，不預造「9/9＋3=12/12」結論。
3. 對可變主體記錄 `observed_at_utc`、main SHA、README SHA、release id／body SHA／API 實際提供的時間欄位（不假定 release 有 `updated_at`）、每個 asset id／`updated_at`／size／digest／實際 download SHA。API timestamps 是輔證；真正閉合依 byte-bound observations。
4. 在全部入口更正完成後開始採樣，驗收結束再 fresh read 相同 fingerprint，期間沒有 mutable subject drift；`issued_at_utc` 晚於最後成功採樣和已知最後 correction。GitHub release 不必然提供 body 修改時間；沒有該欄位不構成 FAIL，以更正完成證據、fresh body bytes 與觀測時刻定界。若必需的身份／flags／asset metadata 因 API 403 仍不可得，不能猜值或簽無條件現況 PASS。[12]
5. 新收據只給 `PASS_ONLY_THE_ABOVE_CLAIMS`／具體失敗／`INCONCLUSIVE`；歷史 raw readback FAIL 保留且有後繼觀測解釋。不得把舊 FAIL 改成 PASS。
6. 追加 supersession index，列 old/new receipt path＋sha256、superseded scope、successor claims、current pointer、mutable fingerprint、claim ceiling。**superseded 僅是 current acceptance pointer 被接替；不撤銷舊收據對未變 immutable bytes 的歷史效力。**

這是關閉而不是遮蔽：新獨立 evidence 可直接讀新 subject、時序及 hashes；遇失敗真的保留 FAIL／INCONCLUSIVE；舊 receipt／raw 403／notes mismatch 都保留。若只有 Maker 的 fresh hashes 或新模型名稱標籤，仍不符合條件。

## 6｜落地方案（Landing Plan / 指令層級）

以下是**後續取得 bounded admission 的 executor/checker runbook**，本研究沒有執行。寫入只准 fresh scratch 與新 evidence 檔；產品 repo 無 commit/push、main/tag 不動。不要以 `r5q_publish.py --publish` 重發，也不要不指定 release SHA 執行其 HEAD-default 模式。

### E1｜先確認指定 lane，缺件就停

```bash
command -v codex || exit 2
codex --version
codex exec --help
```

本次實測 `gh=None`、`codex=None`、`opencodex` 存在；與主報告 qualification 一致。因此上述命令在本 host 目前會停，不能把換名字的 CLI 當已滿足 CODEX 契約。最低阻力是調度**已合規的 verifier host/session**；若需要新增安裝／登入，另經准入完成，不屬本研究授權。

由原 ExecutionBinding／有權治理方提供 `VERIFY_MODEL`（真實 wire id）及 `VERIFY_PROFILE`（原指定 medium/OAuth route），先測服務可用並驗 served model。文件的顯示名稱不是已查證的 wire id，本研究不憑空指定 `gpt-*` token，也不讀憑證或替 verifier 寫 config。

### E2｜獨立取得 bytes、git object 及 main ancestry

以下只讓**後續 checker**在新的 scratch clone 使用 git，不是對既有工作樹操作；本次研究連唯讀 git 也未執行。`VERIFY_ROOT` 須由 runner 分配唯一且准入的 scratch 根；不可覆蓋舊 attempt。

```bash
: "${VERIFY_ROOT:?require an admitted fresh scratch path}"
mkdir -p "$VERIFY_ROOT"
git clone --no-checkout https://github.com/shw097-team/PIPD-LS-SP.git "$VERIFY_ROOT/source"
git -C "$VERIFY_ROOT/source" rev-parse 'refs/tags/v0.1.0-preview.1^{commit}'
git -C "$VERIFY_ROOT/source" rev-parse 'cc9bf574c3b3f0f44ea615b5c67ae40d74efee32^{tree}'
git -C "$VERIFY_ROOT/source" rev-parse refs/remotes/origin/main
git -C "$VERIFY_ROOT/source" show -s --format='%H %P %cI' de3a1d9e3a6298fa0dd29fafbf11d850e30c743a
git -C "$VERIFY_ROOT/source" diff-tree --no-commit-id --name-status -r de3a1d9e3a6298fa0dd29fafbf11d850e30c743a
git -C "$VERIFY_ROOT/source" merge-base --is-ancestor 3aebbbce948871c07b875ab92acf263d298ecf38 de3a1d9e3a6298fa0dd29fafbf11d850e30c743a
git -C "$VERIFY_ROOT/source" checkout --detach cc9bf574c3b3f0f44ea615b5c67ae40d74efee32
```

須 assert tag commit／tree 等於 §2 的完整值；main 當期 tip 等於被採樣 SHA；更正 commit 只有 README.md 且父鏈保留 R3；main 漂移立即列差異，不將新 tip 默認接受。這證明**當前 lineage**；沒有 server audit log 就不宣稱已證明歷史上從未發生任何 force-push。

從 GitHub REST GET 下列 endpoints，保存 response 原 bytes、HTTP status、headers 及本地時間；拒絕 403／404／error body 偽裝成 metadata。release/asset API 欄位及查讀路徑以官方文件為準。[12]

```text
GET /repos/shw097-team/PIPD-LS-SP
GET /repos/shw097-team/PIPD-LS-SP/git/ref/tags/v0.1.0-preview.1
GET /repos/shw097-team/PIPD-LS-SP/git/commits/cc9bf574c3b3f0f44ea615b5c67ae40d74efee32
GET /repos/shw097-team/PIPD-LS-SP/commits/main
GET /repos/shw097-team/PIPD-LS-SP/releases/tags/v0.1.0-preview.1
```

用第一個 response 的 `default_branch` 決定 front-page ref，先固定 SHA，再讀 `raw.githubusercontent.com/.../{main_sha}/README.md`；另外讀 tag README，避免再次只驗 tag。四個 upload 資產的精確下載 URL 見 Sources [8]–[11]。不要把 GitHub 自動生成的 zip/tar.gz 計成四個 uploaded assets；本次 asset HTML 顯示 6 entries，實際是 4 uploads＋2 autogenerated archives。[4]

可執行的 fresh-download/checksum 命令（在 Git Bash 的原生 Windows 路徑根內）：

```bash
python - "$VERIFY_ROOT" <<'PY'
import pathlib,sys,urllib.request,hashlib,json,datetime
root=pathlib.Path(sys.argv[1]); out=root/'download-attempt'; out.mkdir(exist_ok=False)
base='https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/'
names=['pipd_ls_sp-0.1.0-py3-none-any.whl','pipd-ls-sp-v0.1.0-preview.1-source.zip','SHA256SUMS','PREVIEW_NOTES_v0.1.0-preview.1.md']
rows=[]
for name in names:
    request=urllib.request.Request(base+name,headers={'User-Agent':'R5Q-independent-verify'})
    with urllib.request.urlopen(request,timeout=120) as response:
        data=response.read(); headers=dict(response.headers); status=response.status
    (out/name).write_bytes(data)
    rows.append({'name':name,'url':base+name,'http_status':status,'bytes':len(data),
                 'sha256':hashlib.sha256(data).hexdigest(),'headers':headers,
                 'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
for line in (out/'SHA256SUMS').read_text().splitlines():
    sha,name=line.split()
    assert hashlib.sha256((out/name).read_bytes()).hexdigest()==sha,(name,'mismatch')
(root/'download-observations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
PY
```

這段是 byte observation，**不是**獨立驗收 oracle；Checker 還必須比對原 immutable expectations、API digests 及正文。notes hash 必須由新 receipt 明列，不任意修改舊 SHA256SUMS。下載失败保留 stdout/stderr/exit，重新嘗試使用新 attempt 名稱，不覆寫。

### E3｜指定 checker 的最小重驗與完整輸出

由 admitted runner 事先建立 `VERIFY_TASK.md`（本節條件即任務內容），輸入只給公開 subject、既有 receipt 的 expected claims/identity，不給 Maker 推理當 evidence。要求 raw stdout/stderr/exit、counterexamples、not_verified、before/after fingerprints，以及原 9 claims 加入口增項的逐項 verdict。

官方 CLI 支持 `exec`、`--model`、`--profile`、`--sandbox`、`--json`、`--output-last-message` 與 stdin prompt；本機版本 `--help` 必須先核實旗標。[13]

```bash
: "${VERIFY_MODEL:?require the admitted model wire id}"
: "${VERIFY_PROFILE:?require the admitted medium/OAuth profile}"
# VERIFY_TASK.md 必須已由准入 runner 放在 fresh VERIFY_ROOT。
cd "$VERIFY_ROOT/source" || exit 2
codex exec --model "$VERIFY_MODEL" --profile "$VERIFY_PROFILE" \
  --sandbox read-only --json \
  --output-last-message "$VERIFY_ROOT/R5Q_INDEPENDENT_VERIFICATION_RECEIPT_POST_ENTRY_CORRECTION.json" \
  - < "$VERIFY_ROOT/VERIFY_TASK.md" \
  > "$VERIFY_ROOT/verify.events.jsonl" 2> "$VERIFY_ROOT/verify.stderr.txt"
rc=$?
printf '%s\n' "$rc" > "$VERIFY_ROOT/verify.exit.txt"
```

`read-only` sandbox 可能無法做 fresh venv install／scratch negatives 或 network；若遭拒，**不得宣告 PASS、不得自行切 danger-full-access**。由准入 runner 把安裝／負例放到已授權的 disposable sandbox，讓 checker 獨立驅動或獨立重推導其 raw 證據；若只能讀 Maker 的轉述，該 claim 是 `INCONCLUSIVE`。所有寫入只在 scratch；後續 copy 到 evidence 的動作由 admitted executor 做，不把自己當 acceptance signer。

至少重跑：wheel RECORD、licence 對 tag repo 的 byte compare、clean venv 無 PYTHONPATH／repo cwd、doctor／19 schemas、design chain／validate、schema corruption/missing typed negatives、已允許 scratch 的 destination canary。command 細節使用發布 tag 的 `ACCEPTANCE.md` 與既有 UAT 說明，不重創另一套 CLI／core pipeline。完整 311 suite／57-row challenge／production 不在本輪。

API rate limit 可用公開 HTML/CDN 作輔證，如本研究所做；但新收據若要求精確 release/asset id、API 實際提供的 timestamps 而未拿到，保持 `INCONCLUSIVE_API_METADATA`，等 quota reset 或使用 Owner 明許的 readonly credential broker；不讀原 PAT 檔、不把 secrets 放 argv/logs。

### E4｜封存、supersede、檢查 closure

新增（非覆寫）兩個證據目標，名稱為本研究的**建議**而非既存檔案：

- `ROUND/evidence/R5Q_INDEPENDENT_VERIFICATION_RECEIPT_POST_ENTRY_CORRECTION.json`
- `ROUND/evidence/R5Q_RECEIPT_SUPERSESSION_INDEX.json`

index 明確列 `old_receipt_sha256`（§2 值）、`new_receipt_sha256`（實算）、`superseded_for=CURRENT_PUBLIC_ENTRY_ACCEPTANCE`、`retained_for=HISTORICAL_IMMUTABLE_ARTIFACT_ACCEPTANCE`、新 `current_receipt`、最後 correction evidence、subject before/after fingerprint、兩項原 qualification 的逐項 closure／未閉合理由。所有 JSON 用 serializer，不手填假 timestamps／新 hash。

封存前再次 GET main SHA、release body／flags／updated_at／assets，重新下載 notes，與 checker 的最後採樣比較。若不一致，在新 attempt 做 affected-only 再驗，不能為舊收據後補一個發文時刻。先做一切需納入範圍的正文更改，再驗；不要驗後改 live body 再聲稱收據仍 fresh。若要公開新收據，可在 Owner 准入範圍發布獨立 evidence link／append-only evidence branch，不動本次產品 subject；若更新 subject body 本身，必須再驗新正文。

重算收據與原檔 hashes，檢查 old receipt／raw FAIL bytes 與 study 基準相同；保存鏈與完整 checker event log。index 通過 schema/semantic checks且新收據所有適用 claims PASS，才由有權接收角色將**本時效保留**標為 CLOSED。這不是 HGK Full Release Gate 的關閉。

## 7｜殘餘風險、反證與 TT 影響（Residual / Claim Ceiling）

| 項目 | 採 A 後處置 |
|---|---|
| 本文尚未執行 VERIFY | **目前仍 OPEN**。本次 fresh downloads 是研究證據，不是所選 lane 的 closure receipt |
| CODEX CLI／指定 route 可用性 | 本 host `codex` 未安裝，wire id/medium/OAuth served evidence 未查證；調度合規既有 lane 或另核准配置。若替代仍偏離，時效或可單獨閉合，但模型 qualification 不得一併消失 |
| 主報告 12/12 與指定 raw FAIL 矛盾 | 新觀測可以證明目前 bytes 一致，不能證明當年那一個 raw 檔是 PASS；保留歷史矛盾並由新 index 連到 fresh receipt。若獨立 checker 無法確認，不關閉 |
| 凍結 source 內 `main not touched`／舊 notes | **歷史封裝文字不更正**；新 receipt 明示與 live 說明屬不同 as-of subject。這是歷史說明殘留，不是 wheel bytes 缺陷。離線只讀 archive 的人仍可能把舊敘述誤當平台現狀；A 不承諾消除此風險，要求消除則 B |
| live body 尚稱 independent acceptance pending | 本次看到的保守舊敘述與已收到第一份 qualified receipt 的報告不完全同步；不冒稱已移除。[5] 若 Owner 要公開摘要一致，先作 bounded/as-of disclosure，再列入新 VERIFY；單一私有 index 不解決公眾發現新 receipt 的問題 |
| future mutable drift／TOCTOU | closure 只代表 receipt observation window，不保證永遠現況。main tip、body digest、asset id/digest 任一變更即重啟 affected-only verification；不設無限 fresh 承諾 |
| immutable tag／source 仍有歷史不同文字 | old tag 不回寫；不能因 tag 不動就保證 release/asset 平台 immutable。未取得 server audit log／cryptographic attestation 不宣稱供應鏈完整認證 |
| 原 full-gate/DEL/TT gaps | `DEL-018` 仍 FAIL；`PARTIAL_CHALLENGE`、28/10/19 與所有 deferred unchanged。對 TT-R5P-08／09／14 只補公開入口、受驗身份及明確 SHA 的局部證據，不大量把 TT CLOSED |

**本保留能否完全關閉？** 對「第一份 receipt 早於入口更正，沒有獨立證據覆蓋當期可變入口」這個精確命題，A 在 §5 全部滿足後可以完全關閉。對「所有歷史 zip/tag 文件是否改成現況」及「未來可變頁面永遠 fresh」，A 不關閉也不應承諾；前者如另列 acceptance 則改採 B，後者任何 release 都需 drift trigger。

**成本裁決：** A 避開授權重選、產品重建、新 tag／release、main 再寫、輪替資產，仍真正支付一次合規獨立觀測及 receipt chain 的必要成本。D 更便宜卻没有 closure；B/C 要付同樣的獨立驗收再加發布成本，因此不是最低有效阻力。

**本次寫入清單／施工誠實度：** 產品工作樹僅新增本研究 MD。引用登錄簿是 Hermes scratch 的研究工具暫存；未修改既有 evidence、report、contract 或 Skill；未執行 git／push／Owner Grant／HGK admission／board／SWARM／native FAR harness／獨立 VERIFY。這是依既有 license quickstudy 格式做 bounded FAR synthesis，不自稱完整 FAR runtime 三來源或治理 Gate 通過。API 403、commit HTML 406、缺 `gh/codex`、tree fresh object 未取得均已保留邊界。

**狀態：** `RECOMMENDED_A / RECEIPT_CURRENCY_CLOSURE_PENDING`；可對外最高仍為 Owner-authorised preview with disclosed limitations，不是 `FULL_S0_S4_INDEPENDENT_PASS`、`G_RELEASE_FULL_PASS` 或 `PRODUCTION_VERIFIED`。

---

## Sources

[1] https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP/main/README.md
[2] https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP/v0.1.0-preview.1/README.md
[3] https://github.com/shw097-team/PIPD-LS-SP/commit/de3a1d9e3a6298fa0dd29fafbf11d850e30c743a.patch
[4] https://github.com/shw097-team/PIPD-LS-SP/releases/expanded_assets/v0.1.0-preview.1
[5] https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1
[6] https://github.com/shw097-team/PIPD-LS-SP
[7] https://github.com/shw097-team/PIPD-LS-SP/tree/v0.1.0-preview.1
[8] https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/pipd_ls_sp-0.1.0-py3-none-any.whl
[9] https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/pipd-ls-sp-v0.1.0-preview.1-source.zip
[10] https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/SHA256SUMS
[11] https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/PREVIEW_NOTES_v0.1.0-preview.1.md
[12] https://docs.github.com/en/rest/releases/releases
[13] https://developers.openai.com/codex/cli/reference
