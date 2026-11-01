"""Set this session's /goal + subgoals for the R21 FAR/TT + Native E2E mission."""
import os
import sys
from datetime import datetime, timezone

HOME = os.environ.get("HERMES_HOME") or r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes"
sys.path.insert(0, os.path.join(HOME, "hermes-agent"))

from hermes_cli import goals as G  # noqa: E402

SESSION_ID = os.environ.get("HERMES_SESSION_ID") or "20261029_204015_f8e085"

headline, contract = G.parse_contract(
    "R21：以 SBL 為唯一產品工程指揮入口，完成 FHS-MSC_PIPD-LS-PKG HANDOFF-PATCH-v1 中所有"
    "具當期合法 Scope／權限的剩餘工程，並把每個宣稱綁到可重跑 Raw。\n"
    "outcome: FAR-028~056 與 TT-01~20 逐 ID reconcile（VERIFIED_FIXED／SUPERSEDED／OPEN_AFFECTED／"
    "HISTORICAL_NOFIT）；把 work_queue 尚餘的 WP-FHS-12／13／20 以具名根因、受控實驗與獨立 AO 重坐收斂；"
    "22 WP DAG 依 Done／Claim Ceiling 抽查，被反證者重開；DEV ECP／OPS ECP 32 子契約／TQAEP 12 類 8 Oracle "
    "G00–G14 282 依最小適用閉包逐 ID 施工；Native TPM／Commander／Challenge 三職能各自取證；四庫內容級 "
    "Adoption 清單與候選 Patch／PR；交付 FINAL_ENGINEERING_REPORT＋RESUME_CHECKPOINT＋逐 ID Ledger＋真可用度。\n"
    "verification: 每個 PASS 必須是「檔案＋sha256＋可重跑指令＋Raw 輸出」，且項目主體／PID／Nonce／Epoch／"
    "SourceSHA 綁同次操作；獨立判讀只認不同 principal 的 AO/Checker 收據；作者側自測不得當作接受。\n"
    "constraints: 只候選、不動 main、不 force-push、不 merge/tag/release；不冒簽 PASS、不以文件改寫阻斷、"
    "不放寬 TTL/oracle/Permit；owner 動作一律經 owner key 信封；Raw/DB/Key/Token 不上推；"
    "受影 A PARK 時其餘 READY 續跑，不增第二 Scheduler／狀態庫。\n"
    "boundaries: 不可取得的 Owner／Host／原始來源條件一律具名 HOLD／PARK／NoFit 並附解除條件；"
    "DeepSeek 模型車道不等於 DeepSeek Harness Host；ChatGPT48 遷移候選不覆寫原 CellID。\n"
    "stop_when: 所有具當期合法授權與有效 Host/Runner 的適用工作已實作且經獨立判讀；其餘皆有原生具名 "
    "PARK/HOLD/NoFit 與可執行解除路徑。"
)

state = G.GoalState(goal=headline or "FHS-MSC R21 FAR/TT + Native E2E", status="active")
state.contract = contract
state.created_at = datetime.now(timezone.utc).timestamp()
state.subgoals = [
    "S0 四庫現役狀態（main/branch/worktree/loaded）與 FAR/TT 逐 ID reconcile",
    "S1 WP-FHS-12：PATH forwarder 根因＋A/B/C 受控實驗＋AO clause 2 重坐",
    "S2 WP-FHS-13：grant-bound ABI swap 在 ABI fixture 重跑＋C5 重坐",
    "S3 WP-FHS-20：12 格現存 surface 實跑（Hermes PROFILE/PLUGIN）＋7 Kind 具名處置",
    "S4 22 WP DAG：19 PASS 抽查原 Receiver/Effect，被反證即重開",
    "S5 DEV ECP：逐 ID 施工（RepoContext→WriteSet→Admission→Writer→Diff/Tests→Rollback→Checker）",
    "S6 OPS ECP：32 原 OPS 子契約逐 Host/Effect",
    "S7 TQAEP：12 TestClass／8 OracleType／G00–G14／282 來源身份",
    "S8 Native TPM/Commander/Challenge 三職能與 R15 949／R17 最小適用閉包",
    "S9 交付：FINAL_ENGINEERING_REPORT＋RESUME_CHECKPOINT＋逐 ID Ledger＋四庫 Adoption＋rates",
]
G.save_goal(SESSION_ID, state)
print("goal set for", SESSION_ID, "| subgoals:", len(state.subgoals))
