# R21 結案與移交（FHS-MSC_PIPD-LS-PKG FAR/TT Native E2E）

- 輪次：`R21-FAR-20261101`｜結案時間：2026-11-01（台北）
- 車道：PLAN `openai-codex/gpt-6.1-sol`（OAuth）｜EXECUTE `opencode-go/deepseek-v4.1-flash`（Codex CLI，前門 10100）｜VERIFY `openai-codex/gpt-6.1-sol`（verdict **OBJECT**，已吸收）
- Owner 信封：`WIN-759646a93af5` OPEN，scope `permit_sign,admission_bundle_sign,registry_row_sign,merkle_root_sign`，ceiling `REPOSITORY_WRITE`，ops **3/120**
- 宣稱天花板：**候選證據**。無獨立驗收、無 main 集成、無 release。

## 1. 本輪實際完成（可重算）

| # | 產出 | 位置 | 驗證 |
|---|---|---|---|
| 1 | FAR 研究產品（缺口 18 列／來源 35 檔／Claim+Fit+Rejected 帳本／RunReceipt） | `far/`＋`far/research-product/` | 合成 sha `8753efe7…`（v2 後再修一次，見 LAYER_AUDIT） |
| 2 | 三車道收據 | `far_receipts/{PLAN_R21FAR_v2,EXECUTE_R21FAR_C5,VERIFY_R21FAR}.json` | PLAN ok/rank1／EXECUTE exit0／VERIFY OBJECT |
| 3 | 收據語意缺陷（D7）＋候選補丁 | `patches/hgk-lane-dispatch.usage-semantics/` | **9/9**（T1–T9），canonical `524cfd83…` 未動 |
| 4 | S5 hotswap 修補落地（候選分支） | `PIPD/tools/hotswap.py` | sha **`4b5fe035…`**＝通過 4/4 的測試版本 |
| 5 | 逐列證據審計 v2 | `wp_evidence/CANDIDATE_BINDINGS_V2.json` | family-level 綁定否決；有據 PASS＝**3** |
| 6 | Owner 裁定 ×2（簽章） | `rulings/OWNER_RULING_R21_{D4,D3_D5_W2}.json`＋`.signature.json` | broker 簽發，payload sha 相符 |
| 7 | 證據／實作上推 | 分支 `candidate/r21-far-20261101` | `a448e54` → `be93a56`，PR **#22** |

## 2. 判定變更（先前宣稱 → 現在）

| 項 | 先前 | 現在 | 依據 |
|---|---|---|---|
| 22 列隊列通過率 | 19 PASS | **有據 PASS 只有 3**（WP-10/11/17），16 列改列 `UNSUPPORTED_PASS` | 審計 v2＋D4 簽署 |
| PLAN/VERIFY「usage ok」 | 有計費 | **只有 arm 認證，沒有 usage 列**（OAuth-direct 不寫 ledger，dispatcher 強制 true） | `far/sources/TOKEN_ATTRIBUTION.json` |
| `review_lock.py` 未版控 | 阻斷項 | **撤回**：`git ls-files` 證明已版控 | D3/D5/W2 裁定 |
| OPS 分母 | 32 | **實測 31**；第 32 條 `NOT_LOCATED_IN_SOURCE` | 同上 |
| EXECUTE 車道 | 卡死 | 直連 sealed-home 配方可跑（`-s danger-full-access`） | `EXECUTE_R21FAR_C5_RUN.log` |

## 3. 層別審計（可棄層／候選層檢查）

| 層 | 內容 | 狀態 |
|---|---|---|
| L0 canonical | `HG-KSEOS/scripts/hgk-lane-dispatch.py`（`524cfd83…`）、`PIPD/tools/hotswap.py` on main（`f9468f40…`） | **未動** |
| L1 candidate | 分支 `candidate/r21-far-20261101`＋PR #22，含證據 456 對位元相同檔 | 已保存 |
| L2 disposable | `var/FHS-R21-FAR-TT-20261101`（wp20 probe homes 5 GB、s6 raw logs 1.5 GB） | 可重建；發現 JSON 已進 L1 |
| L3 host | `~/.hgk-owner/{window.json,owner.key.enc}` | 只留主機，永不進 repo |

**發現並已修**：s5/、s6/、ledgers/、wp12/、wp13/、receipts/、39/46 支工具、兩份 owner 簽章，原本**只存在於可棄層**（`var/`）。本輪已 83 檔補拷＋全量比對（456 對位元相同、**0 缺口**），明細見 `LAYER_AUDIT.json`。

**仍待 owner 決定**：
- M3：D7 修補只針對 canonical 腳本但仍是候選 → 需 merge 決策。
- M4：hotswap 修補在候選分支，main 未動。
- M5：selector 修補與已落地修補在 `bind_grant` 簽名衝突，`ECP_MULTIPLE_ACTIVE` 仍未強制。
- M6：兩份治理裁定目前放在產品 repo（PIPD-LS-SP），是否改放 HG-KSEOS 由 owner 定。

## 4. 未完成項目（逐條可續）

| ID | 項目 | 阻斷性質 | 下一步 |
|---|---|---|---|
| W3b | selector rebase | 技術 | 以 b3 版本為底重放 SELECTOR_BLOCK，重跑 6/6 |
| W4 | WP-13 F2/F3/F4/F6/F7 逐 finding 關閉 | 技術 | 以 `wp13/*` 為底逐條獨立重現 |
| W5 | WP-12 recovery entry | **HOST** | 退役 forwarder 或修 lease 依賴（10 模組超長路徑／10 cp314 ext） |
| W6 | S6 兩修補獨立重現 | 技術 | `s6/patch/*` 前後對照 |
| W8 | WP-20 F11／SIMPLE_AGENT／plugin install | 部分需網路 | F11 寫出或記 `NEVER_STATED`；install 需 catalog/git 來源 |
| W10 | TQAEP 282 映射 | 技術 | 以 `case_sha256` 逐筆對應 |
| W11 | 三職能 SP | **ISSUER 語意** | 信封不足以發身分（VERIFY 判定）；需 issuer 明定身分語意與驗收準則，否則具名 HOLD |

## 5. 續跑指令（四行）

```bash
cd C:/Projects/Agent_Workspace && unset HERMES_HOME
python var/FHS-R21-FAR-TT-20261101/tools/far_build_gap_ledger.py && python var/FHS-R21-FAR-TT-20261101/tools/far_build_product.py
python var/FHS-R21-FAR-TT-20261101/tools/w7_evidence_audit_v2.py
PYTHONPATH=C:/Projects/Agent_Workspace/HG-KSEOS/src python var/FHS-R21-FAR-TT-20261101/tools/test_d7_semantics.py
```

## 6. 不可宣稱

- 未經獨立 Checker／Publisher 判定前，不得宣稱 Native Complete／Independent Accepted／Main Integrated／Released。
- 16 列 `UNSUPPORTED_PASS` 在補據或重跑前，不得再被引用為通過。
- `ECP_MULTIPLE_ACTIVE` 目前**未強制**。
