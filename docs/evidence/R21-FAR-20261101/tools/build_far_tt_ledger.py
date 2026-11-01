"""Merge the FAR rows from the reconcile subagent with a locally cited TT table.

FAR rows come from FAR_TT_RECONCILE_SUBAGENT_RAW.json (29/29 carry a file#line pointer; a sample
was spot-read by the author: FAR-054 verify.md#L5 FAIL, FAR-036 #L15 two defects fixed).

TT rows are rebuilt here because the id space claimed by the prompt (TT-01..20) does not exist in any
ledger: R20 recorded TT-R20-1..19, and TT-R20-20 has no row anywhere. Each TT row cites the exact
line where its record lives; no ordinal rename is performed without a record.
"""
import json
import pathlib

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "receipts"
SUB = json.loads((OUT / "FAR_TT_RECONCILE_SUBAGENT_RAW.json").read_text(encoding="utf-8"))

FAR_R20 = "_handover/R20-FHS-20261029/FAR_R20_20261029.md"
CLOSURE = "var/R20-FHS-20261029/CLOSURE_ROUND_REPORT.md"
FARCLOSE = "_handover/R20-FHS-20261029/FAR_CLOSURE_AND_PROMOTION_20261029.md"

# n: (record_line_ref, status_text, classification, reason, unblock)
TT = {
    1: (f"{FAR_R20}#L166", "OPEN", "OPEN_AFFECTED",
        "18/18 stage 列為 ABSENT，無機器工件承載 output contract 實例；量測非缺陷宣告，仍未關閉。",
        "產出可被 reader 消費的 stage 工件後重跑 oracle。"),
    2: (f"{FAR_R20}#L167", "OPEN", "OPEN_AFFECTED",
        "46 個 HOLD cell（CALIBRATION 11／HUMAN_DECISION 11／HUMAN_JUDGE 11／TWO_VERSION 8／PERFORMANCE 5）逐 cell 仍未取得 required_reader。",
        "逐 cell 綁 required_reader 並取得對應 reader 收據。"),
    3: (f"{FAR_R20}#L168", "OPEN", "OPEN_AFFECTED",
        "車道獨立性僅 process-only；三車道同為 deepseek（R15），不得主張模型多樣性。",
        "接入第二家 provider 的 arm 後重測車道獨立性。"),
    4: (f"{FAR_R20}#L169", "MITIGATED", "OPEN_AFFECTED",
        "r2 原始報告作廢後歷史引用仍可能引到 2789/0；以 VOID_R2_REPORT.md 與 PR body 標註緩解，未根除。",
        "在歷史引用處加註 void 指標，或由 owner 決定是否回收舊引用。"),
    5: (f"{FAR_R20}#L170", "OPEN", "OPEN_AFFECTED",
        "repo main 未合併、owner／外部驗收 NOT_RUN；本輪維持候選不動 main。",
        "由 owner 決定是否合併；agent 不得自行 fast-forward。"),
    6: (f"{FAR_R20}#L171", "OPEN（政策）", "OPEN_AFFECTED",
        "指派檔只列 3 個主 arm、未列 fallback；strict 選路設為預設會廢掉文件化後備鏈，屬政策決定。",
        "owner 決定：指派檔列合法 fallback，或把 --require-assigned-arms 設為預設。"),
    7: (f"{FAR_R20}#L172", "OPEN", "OPEN_AFFECTED",
        "--codex-executable 指向不存在檔案會拋未捕捉 FileNotFoundError（既有缺陷）。",
        "改為 typed refusal（ERR_CODEX_EXECUTABLE_MISSING）並加負測。"),
    8: (f"{FAR_R20}#L175", "OPEN", "OPEN_AFFECTED",
        "worktree 有 2 個 collection error（test_native_boundaries.py、test_r6_artifact_scope.py，皆 import test_native_admission）。",
        "修掉 import 路徑後重跑；與本輪改動無關但阻礙全綠宣稱。"),
    9: (f"{FAR_R20}#L174", "OPEN（未綁修補收據）", "OPEN_AFFECTED",
        "pass3–5 的 nonce_present_raw_stdout=false 與其自身 byte-exact stdout 矛盾；closure 改 p7 比對基線 id 集，但無收據把 TT-R20-9 綁到該修補。",
        "重發 p7 收據並在其 subject 明確綁 TT-R20-9。"),
    10: (f"{FAR_R20}#L173", "OPEN", "OPEN_AFFECTED",
         "主機 config/model-lane-assignment.json 在回合中由 rev 35/epoch 34 走到 rev 36/epoch 36，P3 收據記 rev 35。",
         "以 drift 欄位回填或固定指派檔；不得以文件改寫掩蓋。"),
    11: (f"{FARCLOSE}#L112", "FIXED（A8）", "VERIFIED_FIXED",
         "--require-arm 只在呼叫後否決；A8 後選路在 spawn 前以 alias 等價過濾（實測 candidates_before 4→1）。",
         ""),
    12: (f"{CLOSURE}#L26", "REPAIRED", "VERIFIED_FIXED",
         "lane pin 指向主機升級刪除的 codex.exe，每次 dispatch 死於 ERR_LANE_PIN_IDENTITY_INVALID；已改 pin 0ab0e7a8f3779036。",
         ""),
    13: (f"{CLOSURE}#L30", "FIXED", "VERIFIED_FIXED",
         "_producer 在 run_attempt() 內綁定卻在 main() 讀，spawn 前拒絕路徑全部 NameError，61 個綠測轉紅；改為 main() 一次綁定。",
         ""),
    14: (f"{CLOSURE}#L32", "FIXED", "VERIFIED_FIXED",
         "closure 收據斷言了工具內部的區域變數 identity_changed，列紅而工具綠；已改為讀工具輸出。",
         ""),
    15: (f"{CLOSURE}#L42", "OPEN", "OPEN_AFFECTED",
         "2 筆 lineage 刪除未在 subset 重放（owner 決定），仍開。",
         "owner 決定是否重放 lineage 刪除。"),
    16: (f"{CLOSURE}#L42", "OPEN", "OPEN_AFFECTED",
         "repo-wide 74 個既存紅測（6086908 同 id 集、0 新增、14 轉綠），仍開。",
         "另開回合根因處理 74 紅測，或明示接受為既存基線。"),
    17: (f"{CLOSURE}#L34", "FIXED", "VERIFIED_FIXED",
         "A8 後 verdict 用 != 比對 served/required 而選路用 alias 等價，導致正確 arm 在 210.09s 後被拒；已改 arm_served_equivalent() 並宣告 alias 對。",
         ""),
    18: (f"{CLOSURE}#L39", "FIXED", "VERIFIED_FIXED",
         "primary excludes fallbacks 測試被判為 tautology（對污染 mutant 同樣通過）；已改為 runtime invariant。",
         ""),
    19: (f"{CLOSURE}#L39", "FIXED", "VERIFIED_FIXED",
         "與 TT-R20-18 同一 tautology 條目，已一併改為 runtime invariant。",
         ""),
    20: ("NO_RECORD", "NO_RECORD", "OPEN_AFFECTED",
         "分母不符：R20 只留下 TT-R20-1..19（19 筆），任何檔案都沒有 TT-R20-20 的列；prompt 卻以 TT-01～20（20 筆）計。",
         "owner 確認第 20 筆是否存在；否則以 19 為分母修正 prompt／handoff，不得自行補一筆。"),
}

tt_rows = []
for n in range(1, 21):
    ref, status, cls, reason, unblock = TT[n]
    tt_rows.append({"id": f"TT-{n:02d}", "record": f"TT-R20-{n}", "status_in_record": status,
                    "classification": cls, "evidence": ref, "reason": reason,
                    "unblock": unblock, "title": ""})

far_rows = SUB["far"]
counts = {"far": {}, "tt": {}}
for r in far_rows:
    counts["far"][r["classification"]] = counts["far"].get(r["classification"], 0) + 1
for r in tt_rows:
    counts["tt"][r["classification"]] = counts["tt"].get(r["classification"], 0) + 1

ledger = {
    "schema": "FHS.R21.FAR_TT_RECONCILE/1",
    "generated_utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
    "scope": "FAR-028..056 (29) + TT-01..20 (20) = 49 ids",
    "enum": ["VERIFIED_FIXED", "SUPERSEDED", "OPEN_AFFECTED", "HISTORICAL_NOFIT"],
    "provenance": {
        "far_rows": "deleg_4c51e80d (independent subagent, read-only Fabric run dirs), 29/29 with file#line",
        "far_spot_check": [
            "Fabric/fabric-autonomous-research/runs/FAR-20261031-054-RUNTIME-IDENTITY-AND-MAXPATH/lane_output/verify.md#L5 -> 'FAIL — delivered work is incomplete'",
            "Fabric/fabric-autonomous-research/runs/FAR-20261031-036-FHS-MSC-HOST-SURFACES/ResearchSynthesis.md#L15 -> two real defects fixed",
        ],
        "tt_rows": "author-built from R20 records; no rename performed; TT-20 has no record",
        "cited_far_files_exist": True,
    },
    "denominator_findings": [
        "TT: prompt says TT-01..20 (20); R20 wrote TT-R20-1..19 only. TT-20 = NO_RECORD.",
        "FAR: 29 ids all resolve to a run dir or report line.",
    ],
    "counts": {"far_total": len(far_rows), "tt_total": len(tt_rows), **{f"{k}_{c}": v for k, d in counts.items() for c, v in d.items()}},
    "far": far_rows,
    "tt": tt_rows,
}

(OUT / "FAR_TT_RECONCILE.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8", newline="\n")

tsv = ["id\tkind\tclassification\tstatus_in_record\tevidence\treason\tunblock"]
for r in far_rows:
    tsv.append("\t".join([r["id"], "FAR", r["classification"], "", r["evidence"],
                          r["reason"].replace("\t", " "), r.get("unblock", "").replace("\t", " ")]))
for r in tt_rows:
    tsv.append("\t".join([r["id"], "TT", r["classification"], r["status_in_record"], r["evidence"],
                          r["reason"].replace("\t", " "), r["unblock"].replace("\t", " ")]))
(OUT / "FAR_TT_RECONCILE.tsv").write_text("\n".join(tsv) + "\n", encoding="utf-8", newline="\n")

tot = {}
for r in far_rows + tt_rows:
    tot[r["classification"]] = tot.get(r["classification"], 0) + 1
print("rows", len(far_rows) + len(tt_rows), "| totals", tot)
print("far", counts["far"], "| tt", counts["tt"])
print("wrote", OUT / "FAR_TT_RECONCILE.json", (OUT / "FAR_TT_RECONCILE.json").stat().st_size, "B")
