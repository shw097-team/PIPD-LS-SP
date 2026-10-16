"""HGK typed admission for the round PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016.

Mission: PIPD-LS-SP S4 R6 closeout continuation — close the round's own reported delivery defect
(TASK/DETECTION checklists never back-filled) and produce the entry document an external engineering
team needs to continue development, then publish both as evidence.

Own project id (own requirement/taskspec/workorder lineage). The last dash segment is UNIQUE by
construction: plan() derives taskspec ids as TS-<last segment>-NN, so "R18" must not collide.
Successor of the S4R6-CLOSEOUT harness; that predecessor is left byte-unchanged.
Run from a git repository working directory (the controller reads git HEAD from the ambient cwd).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
sys.path.insert(0, ROOT + "/src")
from hg_kseos.cli import spine_for  # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest  # noqa: E402

R6 = Path("C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016")
R18 = R6 / "r18"
WT = Path("C:/Projects/Agent_Workspace/PIPD-S4R6-wt")
ATT = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
FAR17 = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261016-017-s4r6-residual-closure")

PROJECT_ID = "PIPD-S4R6-R18"
TARGET_ROOT = str(WT).replace("\\", "/")

GOAL = (
    "在 HG-KSEOS 唯一控制平面下完成 PIPD-LS-SP S4 R6 結案續行（Continuing ChangeSet）："
    "(a) 關閉本回合自己回報的交付缺陷——回填 TASK_CHECKLIST.md 與 DETECTION_CHECKLIST.md 的狀態與證據欄，"
    "使計畫文件與實際執行一致；"
    "(b) 產出外部工程團隊入口文件 EXTERNAL_ENGINEERING_HANDOVER.md 與機器可讀 ROUND_STATE.json，"
    "涵蓋 repo/分支模型、stage-c 寫入集閘門與本地重現法、lane 模型、可重跑指令、模組地圖與擴充點、open tickets 與 owner gates；"
    "(c) 以 FAR-018 對全部殘留/缺口/阻斷/待 OWNER/候選未落地項目裁決並直接執行本回合有權執行者；"
    "(d) 將產物推至證據分支供外部驗收官驗收與外部工程團隊參照；"
    "(e) 完成受 FABRIC/HGK 治理的自研究/自學習/自迭代/自進化。"
)

CONSTRAINTS = [
    "不得合併 PR #17/#18；不得動 main、不得建 tag、不得發 release；不得替換 v0.1.1-preview.4 之 Tag/Asset。",
    "不得改動 HG-KSEOS 控制平面（另一治理域，需其自身 admission）；其殘留只裁決與列管。",
    "不得重做 R17 已完成者：doc-identity 守門、SSOT 漂移揭露、紅燈診斷、stage-c 具名修正。",
    "新產物不得進入產品分支（stage-c 寫入集不允許回合產物）——一律落於證據分支 r6-closeout-evidence-20261016。",
    "不得宣稱 S4_FULL_PASS／HOST_QUALIFIED／PRODUCTION；私有宿主 UAT 維持 NOT_RUN。",
    "憑證一律不得進入 prompt/stdout/log/.env/remote URL/commit/evidence/模型上下文。",
    "改動僅限本回合批准路徑：S4_R6_CLOSEOUT_RETURN/TASK_CHECKLIST.md、"
    "S4_R6_CLOSEOUT_RETURN/DETECTION_CHECKLIST.md、S4_R6_CLOSEOUT_RETURN/EXTERNAL_ENGINEERING_HANDOVER.md、"
    "S4_R6_CLOSEOUT_RETURN/ROUND_STATE.json、S4_R6_CLOSEOUT_RETURN/r18/**、S4_R6_CLOSEOUT_RETURN/SHA256SUMS、"
    "以及回合根 r18/**（非 repo）。",
]

NON_GOALS = [
    "四宿主全面有效載入資格認證（DEFERRED）。",
    ".hgk/ 整體瘦身與 PR #14/#15 處置（DEFERRED）。",
    "公開 Plugin Directory / KYC / Review / Publish（OUT_OF_SCOPE）。",
    "S5-S8 / Production / HOST_QUALIFIED / S4_FULL_PASS。",
    "R6-NEXT-PREVIEW 新版本發行（本輪預設不觸發）。",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    R18.mkdir(parents=True, exist_ok=True)
    srcs = [
        str(ATT / "S4 R6｜階段結案＋私人 Plugin 指揮薄.md"),
        str(ATT / "PIPD-LS-SP｜S4 R6 修補後外部獨立複驗與階段結案裁決.md"),
        str(Path(ROOT) / "AGENTS.md"),
        str(FAR17 / "VERDICT.json"),
        str(FAR17 / "FINDINGS.tsv"),
        str(R18 / "PLAN_CORE_GOAL_AND_SPEC.md"),
        str(R18 / "TASK_CHECKLIST.md"),
        str(R18 / "DETECTION_CHECKLIST.md"),
        str(R6 / "S4_R6_CLOSEOUT_RETURN" / "R17_RED_GATE_DIAGNOSIS.md"),
        str(R6 / "S4_R6_CLOSEOUT_RETURN" / "R17_MEASUREMENTS.json"),
        str(R6 / "S4_R6_CLOSEOUT_RETURN" / "subject_versions.json"),
        str(R6 / "S4_R6_CLOSEOUT_RETURN" / "RESIDUAL_UNIVERSE.tsv"),
        str(R6 / "S4_R6_CLOSEOUT_RETURN" / "DEFECT_DOSSIER.md"),
        str(R6 / "TASK_CHECKLIST.md"),
        str(R6 / "DETECTION_CHECKLIST.md"),
        str(R6 / "HGK_TYPED_ADMISSION_S4R6.json"),
        str(WT / ".github" / "workflows" / "public-plugin-verify.yml"),
        str(WT / "docs" / "install" / "README.md"),
    ]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        if p.is_file():
            present.append(s)
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            missing.append(s)
    out = R18 / "HGK_TYPED_ADMISSION_R18.json"
    rep = {
        "schema": "PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016/HGK-TYPED-ADMISSION/1",
        "project_id": PROJECT_ID,
        "changeset": "S4R6-R18",
        "sources_present": len(present),
        "sources_missing": missing,
        "source_inventory": inv,
        "steps": [],
    }
    if missing:
        rep["verdict"] = "BLOCKED_SOURCE_MISSING"
        out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"verdict": rep["verdict"], "missing": missing}, ensure_ascii=False))
        return 2
    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=present, constraints=CONSTRAINTS,
                         non_goals=NON_GOALS, target_root=TARGET_ROOT)
    try:
        st = lc.status(PROJECT_ID)
        rep["steps"].append({"step": "start", "result": "ALREADY_EXISTS", "state": st["state"]})
    except Exception:
        st = lc.start(req, project_id=PROJECT_ID)
        rep["steps"].append({"step": "start", "result": "CREATED", "state": st["state"]})
    if lc.status(PROJECT_ID)["state"] == "PROJECT_CREATED":
        env = lc.intake(PROJECT_ID, req)
        rep["steps"].append({"step": "intake", "status": env["status"], "source_count": env["source_count"],
                             "blocking_missing": env["blocking_missing"], "conflicts": env["conflicts"]})
        if env["status"] != "READY":
            rep["verdict"] = "BLOCKED_INTAKE"
            out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"verdict": "BLOCKED_INTAKE", "detail": env}, ensure_ascii=False))
            return 3
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_S4R6R18"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_S4R6R18"),
                           ("DESIGN_READY", "DESIGN_READY_S4R6R18")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": "SKIPPED_FROM_" + cur})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig,
                      evidence_refs=["MAND:PIPD-S4R6-R18-EXTERNAL-HANDOVER-20261016",
                                     "FAR:FAR-20261016-017-s4r6-residual-closure",
                                     "PRODUCT:127ec1ca97c71d0437f5b149a6e7d540d0cb3bba"])
        rep["steps"].append({"step": "transition", "to": to_state, "result": "OK"})
    if lc.status(PROJECT_ID)["state"] == "DESIGN_READY":
        pl = lc.plan(PROJECT_ID)
        rep["steps"].append({"step": "plan", "task_count": pl["task_count"],
                             "titles": [s["title"] for s in pl["plan"]]})
    if lc.status(PROJECT_ID)["state"] == "PLAN_READY":
        rep["steps"].append({"step": "admit_workorders", "result": lc.admit_workorders(PROJECT_ID)})
    rep["final_state"] = lc.status(PROJECT_ID)["state"]
    try:
        rep["denominator"] = lc.denominator(PROJECT_ID)
    except Exception as exc:  # noqa: BLE001
        rep["denominator_error"] = type(exc).__name__ + ": " + str(exc)
    rep["verdict"] = ("ADMISSION_OK" if rep["final_state"] in ("WORKORDERS_ADMITTED", "EXECUTING")
                      else "ADMISSION_STATE_" + rep["final_state"])
    if rep.get("denominator"):
        ck = lc.checkpoint(PROJECT_ID)
        rep["checkpoint"] = ck.get("checkpoint_id") if isinstance(ck, dict) else str(ck)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": rep["verdict"], "final_state": rep["final_state"],
                      "sources_present": rep["sources_present"], "sources_missing": rep["sources_missing"],
                      "steps_tail": rep["steps"][-4:]}, ensure_ascii=False, indent=1))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
