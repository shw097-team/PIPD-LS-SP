import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R5Z-20261014-session-conformance"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r5z_verify_arm3.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"),
   "--lane","VERIFY_SECURITY","--prompt",prompt,
   "--round","R5Z-20261014-session-conformance-arm3",
   "--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--force-rank","3","--require-arm","opencode-go/glm-5.3-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5Z-20261014-session-conformance",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--timeout","1800",
   "--attempt-log-dir",str(VAR/"VERIFY_SECURITY/attempts_arm3"),
   "--json-out",str(VAR/"VERIFY_SECURITY/dispatch_receipt_arm3.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=2100, cwd=str(HGK))
(VAR/"VERIFY_SECURITY/dispatch_arm3.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
print("EXIT=", r.returncode); print("ARM3_VERDICT=", (VAR/"VERIFY_SECURITY/VERDICT_ARM3.json").exists())
