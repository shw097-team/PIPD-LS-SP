"""Re-establish this session's /goal in the LIVE session DB and prove it landed.

Two facts forced this rewrite:
  * `HERMES_HOME` in this shell had been left pointing at a throwaway WP-20 cell home, so
    goals._get_session_db() opened `wp20/home-iso/state.db` -- a 20 KB file with no goal in it.
  * the earlier "goal set ... subgoals: 10" line printed unconditionally, so it was never proof of a write.
This script therefore loads the goal back and exits non-zero unless the stored bytes come back.
"""
import json
import os
import sqlite3
import sys

HOME = r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes"
os.environ["HERMES_HOME"] = HOME
sys.path.insert(0, os.path.join(HOME, "hermes-agent"))

from hermes_cli import goals as G  # noqa: E402

SESSION_ID = os.environ.get("HERMES_SESSION_ID") or "20261029_204015_f8e085"

SUBGOALS = [
    "S0 [DONE] 四庫現役狀態＋work_queue 讀回；FAR/TT 49 列 reconcile（TT-20=NO_RECORD）",
    "S1 [DONE] WP-FHS-12 root cause（pm.environments @ hermes_bootstrap:527）＋受權 shim 修補＋v3 12 組合矩陣；AO=PARTIAL，天花板收縮",
    "S2 [DONE] WP-FHS-13 C5 先簽後動＋owner 信封授權 sidecar（5/5 claims true）；AO C1–C5 PASS、F2/F3/F4/F6/F7 候選補丁 T1–T5 全過",
    "S3 [ACTIVE] WP-FHS-20：AO 判 PARTIAL 已吸收（F1 軸未綁定、F2 惰性空洞、F3 隔離太薄、F6 未安裝），v3 重跑中：可綁性量測＋plugin 裝/列/移三段＋隔離提前＋cell_id join",
    "S3b [NEXT] Kind 面探測：逐子命令 --help 存證，把 4 項「無面」散文改成 command+exit+sha，再發 scope ruling（5 vs 7 分母）",
    "S4 [DONE] 22 WP DAG 抽查：16/19 PASS 無 evidence_ref → 須重開或補據（WP_DAG_SAMPLING.json）",
    "S5 [PENDING] DEV ECP 逐 ID 施工（RepoContext→WriteSet→Admission→Writer→Diff/Tests→Rollback→Checker）",
    "S6 [PENDING] OPS ECP 32 原 OPS 子契約逐 Host/Effect",
    "S7 [PENDING] TQAEP 12 TestClass／8 OracleType／G00–G14／282 來源身份",
    "S8 [PENDING] Native TPM/Commander/Challenge 三職能與 R15 949／R17 最小閉包",
    "S9 [PENDING] 交付 FINAL_ENGINEERING_REPORT＋四庫 Adoption＋rates（RESUME_CHECKPOINT 已寫）",
]


def main() -> int:
    prior = G.load_goal(SESSION_ID)
    headline, contract = G.parse_contract(
        "R21：以 SBL 為唯一產品工程指揮入口，完成 FHS-MSC_PIPD-LS-PKG HANDOFF-PATCH-v1 中所有"
        "具當期合法 Scope／權限的剩餘工程，並把每個宣稱綁到可重跑 Raw。\n"
        "outcome: FAR-028~056／TT-01~20 逐 ID reconcile；WP-FHS-12／13／20 以具名根因、受控實驗與獨立 AO 收斂；"
        "22 WP DAG 抽查被反證即重開；DEV ECP／OPS ECP 32 子契約／TQAEP 282 依最小閉包逐 ID 施工；"
        "Native TPM／Commander／Challenge 三職能取證；四庫內容級 Adoption 與候選 Patch／PR；"
        "交付 FINAL_ENGINEERING_REPORT＋RESUME_CHECKPOINT＋逐 ID Ledger＋真可用度。\n"
        "verification: 每個 PASS 必須是「檔案＋sha256＋可重跑指令＋Raw 輸出」，主體／PID／Nonce／Epoch／"
        "SourceSHA 綁同次操作；獨立判讀只認不同 principal 的 AO/Checker 收據；作者自測不得當作接受。\n"
        "constraints: 只候選、不動 main、不 force-push、不 merge/tag/release；不冒簽 PASS、不以文件改寫阻斷、"
        "不放寬 TTL/oracle/Permit；owner 動作一律經 owner key 信封（單一 owner==issuer，信封支援一切授權）；"
        "Raw/DB/Key/Token 不上推；受影 A PARK 時其餘 READY 續跑，不增第二 Scheduler／狀態庫。\n"
        "boundaries: 不可取得的 Owner／Host／原始來源條件一律具名 HOLD／PARK／NoFit 並附解除條件；"
        "DeepSeek 模型車道不等於 DeepSeek Harness Host；ChatGPT48 遷移候選不覆寫原 CellID。\n"
        "stop_when: 所有具當期合法授權與有效 Host/Runner 的適用工作已實作且經獨立判讀；"
        "其餘皆有原生具名 PARK/HOLD/NoFit 與可執行解除路徑。"
    )
    contract.boundaries = (contract.boundaries or "") + (
        " ｜ R21 追加：禁止把「標籤」當成「已綁定的實驗軸」；禁以自身 stdout 不變量主張惰性；"
        "禁以推論代替量測（無 command+exit+sha 即 NOT_MEASURED）。")

    state = prior or G.GoalState(goal=headline, status="active")
    state.goal = headline or state.goal
    state.contract = contract
    state.status = "active"
    state.subgoals = SUBGOALS
    G.save_goal(SESSION_ID, state)

    back = G.load_goal(SESSION_ID)
    db = G._get_session_db()
    path = str(getattr(db, "db_path", "") or "")
    ok = bool(back and back.subgoals == SUBGOALS)
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    row = list(con.execute("select key,length(value) from state_meta where key=?", (f"goal:{SESSION_ID}",)))
    print(json.dumps({"session": SESSION_ID, "db": path, "meta_row": row,
                      "readback_subgoals": len(back.subgoals) if back else 0,
                      "readback_status": getattr(back, "status", None),
                      "roundtrip": ok}, ensure_ascii=False, indent=1))
    return 0 if (ok and row) else 6


if __name__ == "__main__":
    raise SystemExit(main())
