import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
PY = str(HGK/".venv/Scripts/python.exe")
ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R5Z-20261014-session-conformance")
VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance")
prompt = (ROUND/"scripts/_prompt_r5z_execute_rebuild.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"),
   "--lane","EXECUTE","--prompt",prompt,
   "--round","R5Z-20261014-session-conformance",
   "--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--require-arm","opencode-go/deepseek-v4.1-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5Z-20261014-session-conformance",
   "--timeout","1500",
   "--attempt-log-dir",str(VAR/"EXECUTE/attempts"),
   "--json-out",str(VAR/"EXECUTE/dispatch_receipt.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(HGK))
(VAR/"EXECUTE/dispatch.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
print("EXIT=", r.returncode)
print("RECEIPT=", (VAR/"EXECUTE/EXECUTE_REBUILD_RECEIPT.json").exists())
print("DISPATCH=", (VAR/"EXECUTE/dispatch_receipt.json").exists())
