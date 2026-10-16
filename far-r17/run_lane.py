"""Generic HGK lane dispatch runner.

usage: run_lane.py <lane> <brief.md> <out.json> <logdir> <cwd> <rank> <arm> [extra flags]

Keeps the brief out of argv-quoting hell: --prompt is one argv token, so the brief text is passed
programmatically. No credential ever touches this file.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
CODEX = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/e78bad9887fa50cf/codex.exe"

lane, brief_p, out_p, logdir, cwd, rank, arm = sys.argv[1:8]
extra = sys.argv[8:]

brief = Path(brief_p)
cmd = [
    str(HGK / ".venv/Scripts/python.exe"), str(HGK / "scripts/hgk-lane-dispatch.py"),
    "--lane", lane,
    "--prompt", brief.read_text(encoding="utf-8"),
    "--brief", str(brief),
    "--codex-executable", CODEX,
    "--cwd", cwd,
    "--require-arm", arm,
    "--force-rank", str(rank),
    "--json-out", out_p,
    "--attempt-log-dir", logdir,
    "--timeout", "1500",
    *extra,
]
r = subprocess.run(cmd, cwd=str(HGK), capture_output=True, text=True, timeout=1800)
print("runner_exit", r.returncode)
try:
    d = json.loads(r.stdout[r.stdout.index("{"):])
    print(json.dumps({k: d.get(k) for k in ("ok", "code", "used_rank", "used_transport_model",
                                            "used_seconds", "usage_receipt_ok", "required_arm",
                                            "sandbox", "say", "detail")},
                     ensure_ascii=False, indent=1))
    for a in (d.get("attempts") or []):
        print("attempt", a.get("rank"), a.get("model"), "exit", a.get("exit"),
              "nonce", a.get("nonce_present"))
        print("STDOUT_TAIL")
        print((a.get("stdout_tail") or "")[-7000:])
        print("END_STDOUT_TAIL")
except Exception as exc:  # noqa: BLE001
    print("parse_fail", exc)
    print((r.stdout or "")[-4000:])
print("stderr_tail", (r.stderr or "")[-800:])
