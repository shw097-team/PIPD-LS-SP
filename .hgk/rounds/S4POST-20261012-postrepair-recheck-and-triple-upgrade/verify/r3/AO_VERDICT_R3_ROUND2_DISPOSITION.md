# R8 第 2 輪 — 獨立驗收車道裁決與 maker 處置

> 車道：`fabric-external-independent-challenge-reviewer` 正規車道；CODEX CLI、checker model `gpt-6.1-sol`（provider `openai`、OAuth、reasoning medium）。
> 受驗主體：**`5351c5fadca5`**（tree `3a621e68463e`）；第 1 輪主體 `389d3973`。
> 裁決：**`FAIL_CHALLENGE`** — 10 VERIFIED／3 FAILED／1 INCONCLUSIVE。

## 1. 裁決照刊（逐條，修缺陷不是修裁決）

- **1** `VERIFIED` — Verbatim locator commands from root: negative exit 2 / FAIL_LOCATORS_NOT_RERUNNABLE; positive exit 0 / PASS_LOCATORS_IN_TREE. No path-opening error. Python 3.11.9. Network clone/curl and /tmp/r3 cd deliberately not run.
- **2** `VERIFIED` — {"verdict": "PASS_LOCATORS_IN_TREE", "counts": {"RESOLVES_IN_TREE": 1, "EXTERNAL_ONLY": 0, "UNRESOLVABLE": 0, "SHORTHAND_BARE_NAME": 1}}; exit 0. One actual in-tree locator survives; URL produces no offender.
- **3** `INCONCLUSIVE` — Before and after ordinary status: ?? .ao-r3b/ only. No tracked change or new candidate untracked-non-ignored entry. Bytecode redirected under .ao-r3b to obey write boundary; default fresh-clone creation of three cache directories not independently reproduced.
- **4** `VERIFIED` — focused: committed/disk 3666bce6fc04a84e6e7868715349b34048eaa69ce3e677aadc96e3297cbb41d3; CRLF 88d8db8123e744c2699193bd5c8013fbb62c0fd952d425b779c6f9457488eba7. full: committed/disk 46ff948ae879709b87e17d05c4cdbb4dc3400372b9e2ad8d3128d061353aa7a6; CRLF 185a6177ce2296ca11af42e058f9ee661725c465836a65a
- **5** `FAILED` — DISAGREEMENT: current subject has 9 tracked files containing com.ao3, not 3; all under this round, zero product-side hits. Historical receipt subject 389d3973 really had 3; that does not bind the current subject. Additional files include independent-checker artifacts, not solely maker-authored prose
- **6** `VERIFIED` — Literal workflow allowlist step: main exit 1, stacked exit 1. Main: 4 frozen paths, 27 outside-allowed paths; stacked: 0 frozen paths, 5 outside-allowed paths (.github/workflows/ci.yml and four removed 160000 gitlinks). Base changes frozen-path outcome, not the overall refusal. Outside-allowed membe
- **7** `FAILED` — Spot-checked historical ADJ1 (107 total/22 product/0 schemas/0 src), historical ADJ7 (3 versus current 9), negative/positive locator controls, vendor 1805-byte digest, and ADJ5 findings (9 entries). SELF_ITERATION_AFTER_AO.md cited for 6 -> 3 -> 9 is absent; that full series cannot be re-derived. Re
- **8** `VERIFIED` — 8 unique derivations for 8 skills. Every independently computed SKILL.md disk digest equals source_sha256 and frozen-ledger files entry; per-skill digests in report and measurements.json.
- **9** `VERIFIED` — Both manifests pin the measured vendor schema sha256 0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883 (1805 bytes). No online authenticity assertion.
- **10** `VERIFIED` — Scratch --generate-icons produces assets/icon-128.png sha256=70bfddc3ebd2d6445f54f1a4258f1f0b0b787ee3a629b47900e47c3aa23a16e8, equal to the non-placeholder pin. Original checkout lacks this file; no candidate file was repaired.
- **11** `FAILED` — Exact mandated command exits 2: REFUSED ICON_MISSING: pinned icon is absent or not a regular file: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-r3-verify-r2\packaging\public-plugin\assets\icon-128.png Supplemental scratch generation exits 0: BUILT C:\Users\user\AppData\Local\Temp\ao-r3b-build-4
- **12** `VERIFIED` — OWNER_SUPPLIES_DELIVERED.json explicitly says DERIVED from repository owner, not a verified HUMAN. Human attribution, Portal draft/scan/review/Publish, vendor validator, SemVer/tag/assets, and ratification stay owner-only. Disclosure verified, actual account control/authorization not independently v
- **13** `VERIFIED` — focused exit 0: Ran 108 tests in 23.795s
OK; full exit 0: Ran 572 tests in 182.747s
OK (skipped=4). Offline socket guard, isolated temp/bytecode paths, specified interpreter and clone PYTHONPATH used.
- **14** `VERIFIED` — Stronger-than-evidence statements explicitly identified: R3_CI_FIRST_RUN.md says stacked allowlist violations zero (measured 5); DOC_RECONCILIATION_ERRATUM.md says one com.ao3 file (current 9), rejects public-plugin-verify.yml (guard actually allows it), and says any base red (only two tested); FAR 

## 2. 三項 FAILED 的性質與處置

**關鍵判讀**：三項 FAILED **無一在產品本體**，全部是我自己的文件／標籤。第 1 輪真正影響可執行性的缺陷（§3 不可逐字執行、URL 解析）本輪 **VERIFIED** ✓。

| 裁決 | 實測 | maker 處置 |
|---|---|---|
| **11 FAILED `ICON_MISSING`** | 全新 clone 內**不含 `--generate-icons`** 的建構呼叫 exit 2 拒絕 | **設計使然，非缺陷**（該檔自述 `GENERATED, never committed`）。已寫 `BUILD_INVOCATION_AND_OWNER_DECISION.md`，記錄**精確含生成前置的可重跑呼叫**；檢查器以補充模式獨立得到**同一 sha256 `83e5ce5b…`** ✓。把「無生成模式是否為必要契約」列為 **owner 裁決項**，不自決。|
| **5 FAILED `com.ao3` 3 vs 9** | 檢查器對**當前主體**實測 9 檔；我的 3 是**舊主體**的量 | 檢查器**對**：3 不綁後續主體。已**退掉檔數**，改以**不變式**發布（產品面命中 0；全部命中為本回合自撰紀錄，含檢查器產物）。|
| **7 FAILED 定址／形態** | (a) 引用的 `SELF_ITERATION_AFTER_AO.md` **不存在**；(b) 回執記的工具 sha 與**已提交 blob 不符** | (a) **撤回** 6→3→9 序列主張（不可重推），改引用**確實存在、檢查器自己數過 9 筆**的 `verify/ao12/FINDINGS.json`；(b) 回執改記**兩形態並標籤**（committed blob `05f3fe13…`＝clone 實測；worktree CRLF `3787c377…`）。|
| **14 VERIFIED（附帶發現）** | `R3_CI_FIRST_RUN.md` 寫「允許集外 4」，實測 **5** | 已更正為 5 並具名（`.github/workflows/ci.yml` ＋ 4 筆 gitlink）。|

## 3. 檢查器自陳限制（非缺陷，照刊）

- `not_verified`：`['Default fresh-clone three-cache-directory side effect (write-only-under-.ao-r3b restriction).', 'Network clone, hosted CI, current PR/release state, online vendor-byte identity, release downloads.', 'Verified human publisher, owner account control/authorization/signature, model/provider/SID/on-wire lane identity.', 'Missing SELF_ITERATION_AFTER_AO.md and full 6 -> 3 -> 9 findings series.', 'Portal/vendor validator, host UAT, production/security certification, release/promotion.']`
- 其寫入邊界（僅 `.ao-r3b/`）使 claim 3「全新 clone 三快取目錄副作用」**無法自證** → `INCONCLUSIVE`（誠實，非迴避）。
- 其自述：`Advisory round-2 evidence only; grants no release, no pass, no promotion.`

## 4. R8 上限

本 round 外部複驗 **2／2 已用盡**（第 1 輪 `389d3973`、第 2 輪 `5351c5fadca5`）。**不再發起第 3 輪**，除非 owner 另行下令。

## 5. 天花板（未變）

`BUILD_PASS`／`LOCAL_HOST_QUALIFIED`／`PORTAL_APPROVED`／`PUBLISHED`／`PRODUCTION_VERIFIED`／`PIPD_S4_FULL_PASS` **全部未授予**；發行閘門 **`FAIL-CLOSED / HOLD`**。
