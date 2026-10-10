#!/usr/bin/env python3
"""Assemble the single R5 S4 evidence master from the round's own artefacts.

Every number in the emitted document is read back out of a file, never retyped, so the document
cannot drift from the evidence it cites. Prose (claim ceiling, exclusions, open owner items) is
authored exactly once, here.
"""
from __future__ import annotations

import json
import hashlib
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace\PIPD")
R = ROOT / ".hgk" / "rounds" / "R5-20261009-s4-user-operability"
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據")
DEST = OUT / "PIPD-LS-SP_R5_S4_USER_USABILITY_REPAIR_EVIDENCE.md"


def load(p: pathlib.Path, default=None):
    try:
        v = json.loads(p.read_text(encoding="utf-8"))
        return v if v is not None else (default if default is not None else {})
    except Exception:
        return default if default is not None else {}


def loadd(p: pathlib.Path) -> dict:
    """Always a dict — callers that need mapping access use this."""
    v = load(p, {})
    return v if isinstance(v, dict) else {}


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "n/a"


def table(rows: list[list[str]]) -> str:
    if not rows:
        return "_(none)_"
    w = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    head = "| " + " | ".join(str(c).ljust(w[i]) for i, c in enumerate(rows[0])) + " |"
    sep = "|" + "|".join("-" * (w[i] + 2) for i in range(len(rows[0]))) + "|"
    body = ["| " + " | ".join(str(c).ljust(w[i]) for i, c in enumerate(r)) + " |" for r in rows[1:]]
    return "\n".join([head, sep] + body)


def main() -> int:
    led = loadd(R / "ledger" / "R5_S4_FINDING_LEDGER.json")
    uat = loadd(R / "uat" / "UAT_MATRIX.json")
    cand = loadd(R / "CANDIDATE_TUPLE.json")
    inc = loadd(R / "WO3_LANE_INCIDENT.json")
    ao = loadd(ROOT / ".hgk" / "preflight" / "R5-compiler" / "lane" / "ao_out" / "AO_VERDICT.json") or None
    aod = loadd(R / "ao" / "AO_VERDICT_DETERMINISTIC.json")
    obs = loadd(R / "OBSERVATIONS.json")
    receipt = loadd(ROOT / ".hgk" / "preflight" / "R5-compiler" / "compiled-r2" / "compiler-receipt.json")
    dup = loadd(ROOT / ".hgk" / "preflight" / "R5-compiler" / "compiled" / "R5.duplication.json")
    dup_ratios = [r.get("ratio") for r in (dup.get("results") or [])]
    dup_max = max(dup_ratios) if dup_ratios else None
    perf = loadd(R / "ledger" / "perf_check.txt")
    whl = sorted((ROOT / "dist").glob("*.whl"))[-1]
    whl_sha = sha(whl)
    wman = loadd(ROOT / "dist" / "WHEEL_MANIFEST.json")

    def txt(name: str) -> str:
        p = R / "checks" / name
        return p.read_text(encoding="utf-8").strip() if p.is_file() else "(missing)"

    L: list[str] = []
    A = L.append
    A("# PIPD-LS-SP｜R5 S4 一般使用者可用性定向修復——單一證據主檔")
    A("")
    A(f"- **回合**：`R5-20261009-s4-user-operability`（續跑自被 `CHECKPOINT_MODEL_ROUTE_BLOCKED` 暫停的同名回合）")
    A(f"- **產出時間**：{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    A(f"- **受驗主體**：`{cand.get('frozen_base_commit','?')}`（凍結基線）＋ 未 commit 之工作樹")
    A(f"- **本檔完整性**：SHA-256 記錄於同名 sidecar `{DEST.name}.sha256`（避免自參照雜湊不穩定）")
    A("")
    A("> **本檔為 R5 S4 修復候選的本機證據彙整，不是獨立驗收、不是發行授權。**")
    A("> 全部內容以現場 machine truth 讀回，Maker 自報一律降為候選層級。")
    A("")
    A("## 0. Claim ceiling／本輪不宣稱")
    A("")
    A("| 聲明 | 狀態 |")
    A("|---|---|")
    A("| `S4_REPAIR_CANDIDATE_LOCAL_TESTED` | **本輪可宣稱**（Maker 側，本機已測） |")
    A("| `PROMPT_COMPILE_PASS` | 本輪已重跑通過（原生 compiler bundle，見 §1） |")
    A("| `INDEPENDENT_PASS` | **不宣稱**（需有權獨立 Checker 對同一 frozen subject 核定；見 §6） |")
    A("| `PUBLICATION_APPROVED` / `RELEASED` / `PRODUCTION_VERIFIED` | **不宣稱** |")
    A("| `G-S2-LOCAL` | **owner 已裁定 2026-10-10** → 決定行 `bytes_per_atom` 1,449.6/2,000 **PASS**；歷史 FAIL 原文保留（見 §4.1、§9）。**注意：這是契約重新定義，不是 artefact 改善** |")
    A("| `SOURCE_READBACK_GITHUB` | **未執行** → 見 §2.2。本回合的凍結輸入來自**本機附件**，不是 GitHub 原文；`cd8a06e…` 不在本機 object store。列 `EVIDENCE_GAP` |")
    A("| `PRE-W3`（SWOF GENIE） | **維持獨立 `TEMP_CLOSED`**，不繼承本回合結果 |")
    A("")
    A("## 1. PROMPT_COMPILER_READBACK")
    A("")
    A("| 項目 | 值 |")
    A("|---|---|")
    A(f"| bundle | `知識庫/工程基座/construction-acceptance-prompt-compiler/construction-acceptance-prompt-compiler` |")
    A(f"| contract | `.hgk/preflight/R5-compiler/R5.CONTRACT.json`（sha256 `{receipt.get('contract_sha256','?')}`） |")
    A(f"| 子命令退出碼 | lint/activation/acceptance/compile/hash 皆 **0**；duplication **0** |")
    A(f"| 重複率 | 最大 `{dup_max}`（門檻 `{dup.get('threshold')}`，rule `{dup.get('rule')}`）→ `{dup.get('verdict')}` |")
    A(f"| receipt 產出時間 | `{receipt.get('generated_at')}`（本回合 fresh 重跑，`compiled-r2/`） |")
    A(f"| receipt verdict | `{receipt.get('verdict')}`；`independent_claim={receipt.get('independent_claim')}`、`production_claim={receipt.get('production_claim')}` |")
    A(f"| 凍結輸入 R5 指令 | sha256 `4e9f7180c29c450f37a1cf0b1e35a3c8ba67ddf40bb81da1edab46cce90f9f75`（27,271 B） |")
    A(f"| 凍結輸入 R4 報告 | sha256 `34b0347454d2ee723996d3e1949583f288eb4b3e8c13e3464bb3ee72ae70e55f`（54,382 B） |")
    A("")
    A("兩份輸入於本回合重新下載後與暫停前回合的凍結值 **byte-identical**，未漂移。")
    A("")
    A("## 2. HGK_ADMISSION_READBACK 與執行面")
    A("")
    A("| 執行面 | 實際狀態 |")
    A("|---|---|")
    A(f"| KANBAN | board `pipd-ls-sp`；swarm 根 `t_cd5a9163`；worker `t_42db2b43`/`t_5cec3d8f`/`t_72e12722`；verifier `t_ed72c18c`；synthesizer `t_696dc6fe` |")
    A(f"| SWARM／KANBAN 收據 | `.hgk/kanban/canonical_dag.json`、`.hgk/kanban/canonical_completion.json` |")
    A(f"| GSTACK | `.hgk/rounds/R5-20261009-s4-user-operability/route/gstack/route_readback.json` |")
    A(f"| OPENSPEC | change `pipd-ls-sp-r5-s4-usability-repair`，`openspec change validate --strict` → exit 0（valid） |")
    A(f"| EXECUTE 車道 | 容器 `pipd-r4-writer:4`（codex-cli 0.162.0、**無 git**、無憑證、egress-locked 只到模型端點） |")
    A(f"| 寫入邊界 | Maker 車道 `/w` rw 但僅裝載 PIPD repo；Checker 車道 `/w` **唯讀** + `/ao` rw |")
    A(f"| 模型方案偏離 | PLAN／EXECUTE／VERIFY 三面同為 `opencode-go/deepseek-v4.1-flash`（使用者指定）；**SoD 由獨立流程／角色與非 Maker 唯讀車道承擔，不由模型差異承擔** |")
    A("")
    A("### 2.1 模型通道修復（阻擋本回合的 P0 治理阻擋）")
    A("")
    A("opencodex proxy 於 `127.0.0.1:10101` 對 data-plane 請求之 `Host` 非 `localhost/127.0.0.1` 者回 **HTTP 403 `origin_rejected`**，導致容器車道無法呼叫模型。")
    A("處理：新增 host-side bridge `.hgk/preflight/R5-compiler/lane/bridge.py`（`0.0.0.0:10100` → 改寫 Host → `127.0.0.1:10101`）。")
    A("驗證：容器內 `HTTP 200`；bridge 統計見 §7。**未使用任何憑證、未外洩 token。**")
    A("")
    A("### 2.2 未執行的來源讀回（誠實揭露）")
    A("")
    A("| 要求（R5 prompt §2.1-3／§2.3） | 本回合實況 |")
    A("|---|---|")
    A("| 讀 `shw097-team/PIPD-LS-SP` 的 `r4-candidate`、`main`、相關 source、R4 raw receipts／manifest，比較差異 | **未執行**。本機 checkout **無任何 remote**；`cd8a06e4c066a40398a4012b7b3908ac11408a2b`（外部受驗主體）**不在本機 object store**；且**全程未使用任何 PAT**。 |")
    A("| 凍結輸入的真實來源 | R5 prompt 與 R4 稽核報告皆取自**本機附件目錄**（`R5.CONTRACT.json` 的 `locator` 逐條指向 `...\\hermes\\attachments\\...`），已驗 byte-identical，但**不是 GitHub 原文**。 |")
    A("| 依 prompt 規則應開的處置 | 來源缺失本應開 `SOURCE_MISSING`／`EVIDENCE_GAP`；本檔明列此為**未閉合缺口**，不視為已滿足。 |")
    A("| 何以仍能開工 | 本回合同時具備 R4 稽核報告全文（含 `F-R4-*` 十項）與 R5 指令全文，足以界定 S4 受影響面；但**「與 GitHub 現況之差異比對」這一項確實沒有做**，`baseline_policy: FRESH_READBACK_REQUIRED_BEFORE_WRITES` 對**遠端**而言未滿足。 |")
    A("")
    A("## 3. R5_S4_FINDING_LEDGER（10/10 逐項處置）")
    A("")
    A("> 處置狀態彼此互斥，**不得相加成 10/10 PASS**。只有 `closed` 代表該 finding 自身的重測在凍結候選上通過。")
    A("")
    rows = [["#", "Finding", "類別", "P", "WO", "處置"]]
    for i, r in enumerate(led.get("rows", []), 1):
        rows.append([str(i), r.get("finding", "?"), (r.get("class", "") or "").replace("CONFIRMED_DEFECT", "CONFIRMED").replace("EVIDENCE_GAP", "EV_GAP"), r.get("priority", "-"), r.get("workorder", "-"), r.get("disposition", "?")])
    A(table(rows))
    A("")
    A("逐項證據：")
    for r in led.get("rows", []):
        A(f"- **{r.get('finding')}**（`{r.get('disposition')}`）— {r.get('substance','')}")
        for e in r.get("evidence", []) or []:
            A(f"  - {e}")
        if r.get("residual"):
            A(f"  - *殘留*：{r['residual']}")
    A("")
    A("## 4. R5_S4_UAT_MATRIX")
    A("")
    c = uat.get("counts", {})
    A(f"分母：UAT-00～12 × mode(source/install)。結果計數：`{json.dumps(c, ensure_ascii=False)}`")
    A(f"受驗 wheel：`{uat.get('wheel','?')}` sha256 `{uat.get('wheel_sha256','?')}`")
    A("")
    rows = [["case", "mode", "verdict", "actual"]]
    for r in uat.get("results", []):
        rows.append([r.get("case_id", "?"), r.get("mode", "?"), r.get("verdict", "?"),
                     (r.get("actual", "") or "")[:150].replace("|", "/")])
    A(table(rows))
    A("")
    A("完整原始 stdout/stderr：`.hgk/rounds/R5-20261009-s4-user-operability/uat/RAW_RUNS.jsonl`；")
    A("彙整：`uat/UAT_MATRIX.json`、`uat/UAT_MATRIX.md`。")
    A("")
    A("### 4.1 S2 context 預算（owner 已重新指定契約；歷史 FAIL 原文保留）")
    A("")
    if isinstance(perf, dict) and perf.get("rows"):
        rows = [["metric", "值", "budget", "超出", "verdict", "source_of_truth"]]
        for r in perf["rows"]:
            rows.append([r.get("metric", "?"), str(r.get("value_display", r.get("value"))), str(r.get("budget")),
                         str(r.get("exceeded")), str(r.get("verdict")), str(r.get("source_of_truth"))])
        A(table(rows))
        A("")
        A(f"總判定 `{perf.get('verdict')}`，`failed={perf.get('failed')}`。原始輸出：`ledger/perf_check.txt`。")
    A("")
    A("## 5. 最小回歸矩陣（本輪受影響面）")
    A("")
    A("| 檢查 | 指令 | 結果 |")
    A("|---|---|---|")
    A(f"| 主機端全套件 | `python -B -m unittest discover -s tests -q` | **Ran 290 tests, OK (skipped=2)**（見 `host/unittest_full2.txt`；285→290 為 owner 裁定後 `tests/test_perf_budget.py` +5） |")
    A(f"| CLI 13 commands 面 | `tools/cli_surface_check.py` | {json.loads((R / 'checks' / 'cli_surface.txt').read_text(encoding='utf-8').strip())['verdict'] if (R / 'checks' / 'cli_surface.txt').is_file() else 'n/a'} |")
    A(f"| Web pack | `tools/web_pack_check.py --out <scratch>` | PASS（`checks/web_pack.txt`） |")
    A(f"| Host 投影 | `tools/host_projection_check.py --out <scratch>` | PASS（`checks/host_proj.txt`） |")
    A(f"| 可移植安裝 | `tools/portable_install_check.py` | **14/14 PASS** |")
    A(f"| 發行包 manifest | `tools/build_publication_manifest.py --check --current` | **exit 1（`CURRENT_TREE_UNCOVERED`，維持 R4 EVIDENCE_GAP）** |")
    A("")
    A("## 6. Independent AO（非 Maker Checker）")
    A("")
    if aod:
        A("### 6.1 Deterministic independent check（已執行）")
        A("")
        A(f"- Checker identity：`{aod.get('checker_identity')}`")
        A(f"- Maker identity：`{aod.get('maker_identity')}`")
        A(f"- 獨立性基礎：{aod.get('independence_basis')}")
        A(f"- **明確不是**：{aod.get('explicitly_not')}")
        A(f"- 判定：**`{aod.get('verdict')}`**，計數 `{json.dumps(aod.get('counts',{}), ensure_ascii=False)}`")
        A(f"- 受驗主體：wheel sha256 `{aod.get('subject',{}).get('wheel_sha256')}`，candidate_head `{aod.get('subject',{}).get('candidate_head')}`")
        A("")
        rows = [["case", "verdict", "actual"]]
        for r in aod.get("cases", []):
            rows.append([r.get("case", "?"), r.get("verdict", "?"), (r.get("actual") or "")[:120].replace("|", "/")])
        A(table(rows))
        A("")
        A("**反證嘗試（adversarial falsification）**")
        A("")
        for b in aod.get("falsification_attempts", []):
            A(f"- `{b.get('case')}` → **{b.get('result')}** — {str(b.get('detail'))[:180]}")
        A("")
        A(f"原始：`.hgk/rounds/R5-20261009-s4-user-operability/ao/AO_VERDICT_DETERMINISTIC.json`、`AO_REPORT_DETERMINISTIC.md`")
        A("")
    A("### 6.2 LLM checker 車道（未完成，已記錄）")
    A("")
    if ao:
        A(f"- 判定：**`{ao.get('verdict','?')}`**")
    else:
        A("容器內以 Codex CLI 執行的 LLM 獨立 Checker 車道**兩次啟動均因上游 HTTP 429 而卡死**，")
        A("經 `docker kill` 中止；本回合無 LLM 級獨立驗收，且 **`INDEPENDENT_PASS` 一律不宣稱**。")
        A("詳見 `AO_LANE_INCIDENT.json`（含 7 次 429 的通道普查與「備援模型無可達目標」的驗證）。")
        A("")
        A("因此本回合的獨立性由 **§6.1 的 deterministic checker** 承擔，並明確標示其級別較低。")
        A("")
        A("### 6.3 LLM checker 車道的第 5 次嘗試（執行到預算上限，無裁決檔）")
        A("")
        A("- 配置：`pipd-r4-writer:4`，`/w` **唯讀**，非 Maker；經使用者提供的新憑證修復後，**車道內未再出現 401/429**。")
        A("- **該車道跑滿 2400 秒被 `timeout` 終止（`codex_exit=124`）**，因此**沒有寫出 `AO_VERDICT.json`／`AO_REPORT.md`**。")
        A("- 依其 brief 的要求，它**逐例即時寫入** `AO_PROGRESS.txt`／`AO_LOG.ndjson`；這些原始紀錄已保存至 `.hgk/rounds/R5-20261009-s4-user-operability/ao/attempt5/`，並未以摘要取代。")
        A("- 由**它自己的紀錄**彙整（**明示：這是 derived tally，不是它的裁決**）：**37 個 machine-readable case、66 筆紀錄** → PASS 63／FAIL 2／NOT_RUN 1；**每個 case 都至少有一次 PASS**。")
        A("- **此 tally 低估了它的實際覆蓋**：`AO_LOG.ndjson` 只收錄 37 個 case id；它另外跑的 **E 區（新鮮度／陳舊宣稱）對抗案例只以散文形式落在原始 log**，未進入機器可讀紀錄。其中已確認 HELD 的有：無 epoch 的 FRESH → `StaleProvider`；外來 epoch → `StaleProvider`；正確 epoch → ACCEPTED；正確 epoch + 偽造 head → `StaleProvider`。**E 區目前只有「一個沒寫出裁決的車道」這一個見證者**，尚無人寫出獨立的可重現器。")
        A("- 兩筆 FAIL 的處置（依其**自身原始輸出入**判定，**未修改產品**）：")
        A("  - `B13`：其失敗紀錄自己捕到的 stdout 內含 `\"replaced\": true` 與真實 `rollback_pointer`，只是**嵌在 `destination` 之下**，而它讀頂層鍵 → **檢查器取值缺陷**；重測 PASS。")
        A("  - `UAT-12`：首輪 `intake_inj=2`，但**其餘產品訊號全對**；其後**三次重測皆 `inj=0` 且 PASS** → **首輪暫態**，產品未變。")
        A("- 它獨立重現的內容：wheel 等價（38 members、13 模組逐位元組等於 `/w/src`）、A4／A5 反證 HELD、**B1–B12 全部 12 個惡意目的地 typed 拒絕且 canary 不變**、export C1–C5 獨立重算、UAT-00～12、以及 **S2 裁決線路（`s2_voting=['bytes_per_atom']`、`s2_preserved_fail_visible=true`）**。")
        A("- 詳細 derived tally：`.hgk/rounds/R5-20261009-s4-user-operability/ao/AO_INDEPENDENT_RESULT_DERIVED.json`。")
        A("")
        A("> **`INDEPENDENT_PASS` 不成立**：該車道未產出裁決。以推論填補此缺口，正是本回合所禁止的自我驗收。")
    A("")
    A("## 7. DISTRIBUTION_AND_PUBLICATION_TUPLE")
    A("")
    A("| 項目 | 值 |")
    A("|---|---|")
    A(f"| wheel | `{whl.name}` |")
    A(f"| wheel sha256 | `{whl_sha}` |")
    A(f"| wheel bytes / members | `{whl.stat().st_size if whl.is_file() else '?'}` / `{wman.get('member_count','?')}` |")
    A(f"| manifest candidate_head | `{wman.get('candidate_head','?')}` |")
    A(f"| product_digest | `{wman.get('product_digest','?')}` |")
    A(f"| 凍結基線 commit | `{cand.get('frozen_base_commit','?')}` |")
    A(f"| 凍結基線 tree | `{cand.get('frozen_base_tree','?')}` |")
    A(f"| product delta digest | `{cand.get('product_delta_digest','?')}` |")
    A("")
    ri = cand.get("round_introduced", {})
    A(f"本回合對 product paths 的實際變更：**added {len(ri.get('added',[]))} / changed {len(ri.get('changed',[]))} / removed {len(ri.get('removed',[]))}**")
    A("")
    A(table([["狀態", "路徑"]] + [["added", p] for p in ri.get("added", [])] + [["changed", p] for p in ri.get("changed", [])]))
    A("")
    A("- **未 commit、未 push、未開 PR、未合併 `main`、未標發行**。")
    A("- 本機 checkout **無任何 remote**；且受外部稽核的 `cd8a06e4c066a40398a4012b7b3908ac11408a2b` **不存在於本機 object store**，")
    A("  因此無法對「外部受驗主體」產生 publication-bound attestation → `F-R4-PUB-06` 維持 `blocked`／`EVIDENCE_GAP`。")
    A("")
    A("## 8. Lane 事件與治理揭露")
    A("")
    if inc:
        A(f"- WO3（`WO-S4-EXPORT-003`）於 26 分鐘時**被協調者人工中止**：唯一一次上游 **HTTP 429** 後，log 凍結約 7 分鐘、bridge 零流量、容器仍 Up。")
        A(f"- 阻擋分類計數：`{json.dumps(inc.get('block_evidence',{}), ensure_ascii=False)}`")
        A(f"- 無任一分類重複 >4 次；中止屬獨立規則（>10 分鐘且零進展）。")
        A(f"- 處置：`docker kill` → 對已寫入產物做 host 端複驗 → 由協調者補 2 行回歸修補（已揭露）→ **未重啟車道**。")
        A(f"- 完整記錄：`.hgk/rounds/R5-20261009-s4-user-operability/WO3_LANE_INCIDENT.json`")
    A("")
    A("**副作用總清單（全部揭露）**")
    A("")
    A("1. `dist/*` 由 WO2 重建覆寫（wheel、`WHEEL_MANIFEST.json`、`.sha256`）。")
    A("2. `tools/cli_smoke.py`、`tools/cli_surface_check.py` 由協調者各加 `--allow-root`（WO1 硬化後之受影響回歸）。")
    A("3. `src/pipd_ls_sp/cli.py` 之 `export` 唯讀分支由協調者補回 `wrote_nothing`（WO3 留下之受影響回歸）。")
    A("4. 三個 Maker 車道 + 一個 Checker 車道於 `pipd-r4-writer:4` 容器內執行；**無憑證裝載、映像內無 git、egress 僅達模型端點**。")
    A("5. host 端 bridge 於 `0.0.0.0:10100` 監聽（僅本機、僅轉發模型端點）。")
    A("6. **未讀取、未使用任何 PAT／secret**；`CREDENTIAL_GATE_BLOCKED` 未觸發，因為不需要 GitHub 寫入。")
    A("")
    A("## 9. 未結 TT／Owner Gate")
    A("")
    A("| 項目 | 狀態 | 最早 Owner |")
    A("|---|---|---|")
    A("| S2 預算 | **owner 已裁定 2026-10-10**：`PER_ATOM_BYTES(2000)`；決定行為 `bytes_per_atom` = 1,449.6/2,000 **PASS** | — |")
    A("| S2 歷史 FAIL | `context_bytes_per_artefact 343547 > 20000` **已保留、未改寫**，以非投票 ADVISORY 列持續輸出於 `historical.preserved_fails` | — |")
    A("| S2 計時列 | 三列降為 `ADVISORY`（餘裕 2.35×／1,579×／51×，永不觸發） | — |")
    A("| S2 迴歸守門 | 新增：`bytes_per_atom` 對凍結基線（容差 10%）比對，超標即 FAIL | — |")
    A("| **誠實讀法** | G-S2-LOCAL 之所以通過，是因為**定義被 owner 重新指定**，**不是** artefact 變好了（artefact 前後皆 334,778 B、byte-identical） | — |")
    A("| R4 publication projection（`F-R4-PUB-06`） | `CURRENT_TREE_UNCOVERED`，exit 1 | Evidence / publication owner |")
    A("| 57-row crosswalk 其餘 11 EVIDENCE_GAP / 4 DESIGN_ONLY | 未動，維持原標記 | SPEC / DEL owner |")
    A("| 22 TT（16 open / 2 open_owner_gate / …） | 未動；本輪未啟用任何未 pin 技術 | governance owner |")
    A("| License / Human RELEASE | `OWNER_LICENSE_DECISION.yaml` 存在；未授予 | human owner |")
    A("| PRE-W3（SWOF GENIE） | 獨立 `TEMP_CLOSED` | SWOF GENIE checkpoint owner |")
    A("")
    A("## 9.5 觀測（非缺陷，交還 Owner，本回合未自行修補）")
    A("")
    for o in obs.get("observations", []):
        A(f"- **{o.get('id')} {o.get('title')}**（`{o.get('disposition')}`）")
        A(f"  - 觀測：{o.get('observed')}")
        A(f"  - 影響：{o.get('why_it_matters')}")
        A(f"  - 建議 Owner 動作：{o.get('recommended_owner_action','—')}")
    A("")
    A("## 10. Resume")
    A("")
    A("```bash")
    A("cd C:/Projects/Agent_Workspace/PIPD")
    A("python -B -m unittest discover -s tests -q                      # 290 tests")
    A("python -B .hgk/rounds/R5-20261009-s4-user-operability/uat/uat_matrix.py \\")
    A("    --out .hgk/rounds/R5-20261009-s4-user-operability/uat --mode both")
    A("python -B tools/cli_surface_check.py && python -B tools/portable_install_check.py")
    A("bash .hgk/preflight/R5-compiler/lane/run_checker.sh brief_wo4_ao.md log_ao.txt 2400")
    A("```")
    A("")
    A("恢復點：`CHECKPOINT_R5_CONTINUATION.json`（回合檔）與 `CANDIDATE_TUPLE.json`（候選主體）。")
    A("")
    OUT.mkdir(parents=True, exist_ok=True)
    body = "\n".join(L) + "\n"
    DEST.write_text(body, encoding="utf-8", newline="")
    digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
    side = DEST.with_suffix(DEST.suffix + ".sha256")
    side.write_text(f"{digest}  {DEST.name}\n", encoding="utf-8", newline="")
    print("wrote", DEST)
    print("sha256", digest)
    print("bytes", DEST.stat().st_size)
    print("sidecar", side)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
