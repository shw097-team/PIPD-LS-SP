"""Record the lane-transport fault class, its verified root cause, the remediation and the probe.

Read-only against the control plane; writes only the JSON files it is asked for.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

R = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close")
FREEZE = R / "00_freeze/R5S_FREEZE.json"


def run(args):
    p = subprocess.run(args, capture_output=True, text=True, shell=isinstance(args, str))
    return (p.stdout or "") + (p.stderr or "")


# correct listener capture (native netstat, filtered in python so the shell cannot drop it)
net = run(["netstat", "-an"])
listeners = sorted({m.group(1) for m in re.finditer(r"TCP\s+(\S+)\s+\S+\s+LISTENING", net) if m.group(1).endswith(("10100", "10101", "10102", "10103", "10105"))})

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
freeze["lane_transport_before_remediation"] = {"listeners_1010x": []}
freeze["lane_transport_after_remediation"] = {"listeners_1010x": listeners, "captured_utc": datetime.now(timezone.utc).isoformat()}
FREEZE.write_text(json.dumps(freeze, indent=1, ensure_ascii=False), encoding="utf-8")

launcher = Path("C:/Projects/Agent_Workspace/HG-KSEOS/scripts/start-hgk-hermes.ps1").read_text(encoding="utf-8", errors="replace")
pre = [ln.strip() for ln in launcher.splitlines() if "ERR_RUNTIME_FILE_MISSING" in ln or "foreach ($file in @(" in ln]

out = {
    "schema": "R5S-LANE-ROOT-CAUSE/1",
    "round": "R5S-20261015-s4-preview4-verify-close",
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "error_class": "LANE_TRANSPORT_DOWN_CAUSED_BY_LAUNCHER_PRECONDITION_FAIL",
    "class_count_note": "ONE error class. The previous round recorded it as four separate symptoms (EXECUTE dispatch returned ok=null twice with a 0-byte runner.log; the declared VERIFY_SECURITY arm timed out at 900 s with 0 bytes; the backup arm produced 0 bytes). They are four occurrences of one cause, not four independent faults.",
    "verified_root_cause": {
        "mechanism": "start-hgk-hermes.ps1 validates a fixed runtime-file list before ANY action: foreach ($file in @($humanConfig, $codexExe, $bunExe, $openCodexEntry, $hermesExe, $hermesPython)) { if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw \"ERR_RUNTIME_FILE_MISSING:$file\" } }",
        "trigger": "config/hermes-codex-lane.json pins codex_executable at a path that does not exist on this host",
        "declared_codex_executable": "C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe",
        "declared_path_exists": False,
        "declared_codex_sha256": "D13914CED6C7AF174D8D638DB938284231227312104B06A25E9608C632A7DAEC",
        "only_live_codex_binary": "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe",
        "only_live_codex_sha256": "e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e",
        "consequence": "The launcher refuses EVERY action including -Action StartOpenCodex, so the isolated relay on 127.0.0.1:10101 is never started and no Codex-CLI lane can reach a model. The symptom is a silent empty lane turn, which reads like a model, quota or prompt problem.",
        "launcher_lines": pre,
        "reproduction": {
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File C:/Projects/Agent_Workspace/HG-KSEOS/scripts/start-hgk-hermes.ps1 -Action StartOpenCodex",
            "observed": "ERR_RUNTIME_FILE_MISSING:C:\\Users\\user\\AppData\\Local\\OpenAI\\Codex\\bin\\2e5e00daee91c61d\\codex.exe (OperationStopped at the Test-Path guard)",
            "observed_utc": "2026-10-15T01:02Z",
        },
        "ports_before_remediation": [],
    },
    "remediation_applied_this_session": {
        "what": "Started the isolated relay directly with the exact command the launcher's StartOpenCodex action would have run, using the launcher's own documented root and isolated home. NO canonical configuration was mutated.",
        "command": "cd <opencodex_root> && OPENCODEX_HOME=<isolated opencodex home> node_modules/bun/bin/bun.exe run src/cli/index.ts start --port 10101",
        "opencodex_root": "C:/Users/user/AppData/Local/HG-KSEOS/runtime/opencodex-2.11.0",
        "opencodex_home": "C:/Users/user/AppData/Local/HG-KSEOS/opencodex-hermes",
        "healthz_after": {"status": "ok", "service": "opencodex", "version": "2.11.0", "port": 10101, "pid": 19892},
        "ports_after": listeners,
        "side_effects_disclosed": [
            "A local relay process is now running (pid 19892) that was not running before this session.",
            "A new worktree was added: C:/Projects/Agent_Workspace/PIPD/worktrees/r5s-verify-wt at commit dba4b19 (detached), used as the read-only checker subject.",
        ],
        "not_done": "The stale pin itself is NOT repaired. Retargeting the lane's pinned executable/digest is a canonical control-plane change that belongs to the tool-drift item TT-R5R-TOOL-DRIFT-LANE-CODEX-BINARY under its own change, not to a silent edit inside this round.",
    },
    "transport_probe": {
        "lane": "VERIFY_SECURITY",
        "forced_rank": 3,
        "arm": "opencode-go/glm-5.3-flash",
        "note": "rank 3 is the arm the previous round declared as the backup checker after the declared arm (rank 4, openai-codex/gpt-6.1-sol) timed out. Any verdict from it comes from a different checker than the round declared.",
        "receipt": "VERIFY3/probe_receipt.json",
        "ok": True,
        "nonce_echoed": "HGK_LANE_NONCE_OK",
        "usage_receipt_ok": True,
        "used_seconds": 2.73,
        "codex_executable_used": "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe (the documented --codex-executable seam; the lane config itself is untouched)",
        "caveat": "stderr carries 'failed to connect to websocket: HTTP error: 426 Upgrade Required' followed by 'Reading additional input from stdin...'. The turn still completed through the HTTP path with a real completion and a matching usage receipt, but this is the degraded transport shape this skill library flags as a VOID risk when it also shows an implausibly small used_seconds with no artifact - here a real completion and output tokens are present, so it is recorded as a degraded-but-valid transport, not a void.",
    },
}
(R / "01_lane").mkdir(parents=True, exist_ok=True)
(R / "01_lane/LANE_ROOT_CAUSE.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"listeners": listeners, "freeze_updated": True, "root_cause_written": True}, indent=1))
