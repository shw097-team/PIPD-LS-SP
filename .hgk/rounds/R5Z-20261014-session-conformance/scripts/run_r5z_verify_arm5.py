import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R5Z-20261014-session-conformance"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R5Z-20261014-session-conformance")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r5z_verify_arm5.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"),
   "--lane","VERIFY_SECURITY","--prompt",prompt,
   "--round","R5Z-20261014-session-conformance-arm5",
   "--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--force-rank","3","--require-arm","opencode-go/glm-5.3-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5Z-20261014-session-conformance",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt",
   "--timeout","1500",
   "--attempt-log-dir",str(VAR/"VERIFY_SECURITY/attempts_arm5"),
   "--json-out",str(VAR/"VERIFY_SECURITY/dispatch_receipt_arm5.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(HGK))
(VAR/"VERIFY_SECURITY/dispatch_arm5.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
print("EXIT=", r.returncode)
from pathlib import Path as P
print("ARM5_VERDICT=", (VAR/"VERIFY_SECURITY/arm5/VERDICT_ARM5.json").exists())
