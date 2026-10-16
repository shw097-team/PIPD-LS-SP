"""Assemble the round's evidence packet on the evidence branch and index it by digest.

Run ONLY after the last lane dispatch has exited (a maker write landing inside a guarded subject while a
lane is open voids the lane's window; the same discipline keeps the packet's own digests honest).

Writes into <worktree>/R5R3_PREVIEW4_CLOSEOUT_20261016/ and emits PACK_INDEX.json (path, bytes, sha256).
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys

ROUND = pathlib.Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout")
WT = pathlib.Path("C:/Projects/wt-r5r3-closeout-evidence")
DEST = WT / "R5R3_PREVIEW4_CLOSEOUT_20261016"

COPY = [
    ("ROUND_STATUS_CLOSEOUT.md", "ROUND_STATUS_CLOSEOUT.md"),
    ("ARTIFACT_DATING.md", "ARTIFACT_DATING.md"),
    ("CLAIM_CORRECTIONS_R5R3.md", "CLAIM_CORRECTIONS_R5R3.md"),
    ("CHECKER_VERDICT_WS_C.json", "CHECKER_VERDICT_WS_C.json"),
    ("raw/gstack_readback.json", "gstack_readback_epoch19.json"),
    ("PLAN_CONTRACT_FAR_R5R3.md", "PLAN_CONTRACT_FAR_R5R3.md"),
    ("raw/plan_glm_oneshot.log", "PLAN_DECISION_GLM_raw.log"),
    ("raw/PLAN_DECISION_GLM.json", "PLAN_DECISION_GLM.json"),
    ("TT_DISPOSITIONS.md", "TT_DISPOSITIONS.md"),
    ("OWNER_DECISION_REQUEST.md", "OWNER_DECISION_REQUEST.md"),
    ("PRIVATE_PLUGIN_UPLOAD_RUNBOOK.md", "PRIVATE_PLUGIN_UPLOAD_RUNBOOK.md"),
    ("push_with_pat.sh", "push_with_pat.sh"),
    ("raw/push_dryrun.log", "push_dryrun.log"),
    ("zip_repro_r5r3.py", "zip_repro_r5r3.py"),
    ("probe_control_plane_r5r3.py", "probe_control_plane_r5r3.py"),
    ("raw/control_plane_probe.json", "control_plane_probe.json"),
    ("raw/ROUND_SURFACES.json", "ROUND_SURFACES.json"),
    ("raw/openspec_validate.log", "openspec_validate.log"),
    ("brief_checker_r5r3_round.md", "brief_checker_r5r3_round.md"),
    ("raw/verify_ds_receipt.json", "verify_ds_receipt_attempt1_refused.json"),
    ("raw/verify_ds_checker_attempt2.log", "verify_ds_checker_attempt2.log"),
    ("raw/verify_ds_receipt_attempt2.json", "verify_ds_receipt_attempt2.json"),
    ("raw/pr_open.json", "pr_open.json"),
    ("raw/pr_comment.json", "pr_comment.json"),
    ("PR_BODY_CLOSEOUT.md", "PR_BODY_CLOSEOUT.md"),
    ("PR_COMMENT_CLOSEOUT.md", "PR_COMMENT_CLOSEOUT.md"),
    ("gh_closeout_publish.py", "gh_closeout_publish.py"),
    ("extract_checker_closeout.py", "extract_checker_closeout.py"),
    ("pack_closeout_r5r3.py", "pack_closeout_r5r3.py"),
    ("raw/zip_repro/ZIP_REPRO_R5R3.json", "ZIP_REPRO_R5R3.json"),
    ("raw/zip_repro/ledger.json", "zip_repro/ledger.json"),
]
GLOB = [
    ("raw/zip_repro_r5y/**", "zip_repro_r5y"),
    ("raw/verify_ds*", "verify_ds_logs"),
    ("openspec_change/**", "openspec_change"),
]
FAR_RUN = pathlib.Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/"
                       "FAR-20261016-014-r5r3-closeout-learning")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    written: list[pathlib.Path] = []

    for src_rel, dst_rel in COPY:
        s = ROUND / src_rel
        if not s.is_file():
            print(f"MISSING (declared, not copied): {src_rel}")
            continue
        d = DEST / dst_rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        written.append(d)

    for pattern, dst_dir in GLOB:
        for s in sorted(ROUND.glob(pattern)):
            if not s.is_file():
                continue
            d = DEST / dst_dir / s.name
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
            written.append(d)

    # The round's FAR learning run is kept beside the evidence (it is the round's self-evolution record).
    if FAR_RUN.is_dir():
        for s in sorted(FAR_RUN.glob("*")):
            if s.is_file():
                d = DEST / "far_run" / s.name
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(s, d)
                written.append(d)

    # The checker's extracted verdict, if it produced one.
    v = ROUND / "raw" / "CHECKER_VERDICT_R5R3.json"
    if v.is_file():
        d = DEST / "CHECKER_VERDICT_R5R3.json"
        shutil.copy2(v, d)
        written.append(d)

    index = [{"path": str(p.relative_to(DEST)).replace("\\", "/"), "bytes": p.stat().st_size,
              "sha256": sha256(p)} for p in sorted(written)]
    payload = {"schema": "R5R3-CLOSEOUT-PACK-INDEX/1", "entry_count": len(index), "entries": index}
    (DEST / "PACK_INDEX.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps({"dest": str(DEST).replace("\\", "/"), "files": len(index)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
