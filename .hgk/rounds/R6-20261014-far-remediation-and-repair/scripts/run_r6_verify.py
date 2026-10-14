import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R6-20261014-far-remediation-and-repair"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R6-20261014-far-remediation-and-repair")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r6_verify.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"), "--lane","VERIFY_SECURITY","--prompt",prompt,
   "--round","R6-20261014-far-remediation-and-repair","--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--force-rank","3","--require-arm","opencode-go/glm-5.3-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R6-20261014-far-remediation-and-repair",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt",
   "--timeout","1800","--attempt-log-dir",str(VAR/"VERIFY_SECURITY/attempts"),
   "--json-out",str(VAR/"VERIFY_SECURITY/dispatch_receipt_r6.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=2000, cwd=str(HGK))
(VAR/"VERIFY_SECURITY/dispatch_r6.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
print("EXIT=", r.returncode)
q = VAR/"VERIFY_SECURITY/VERDICT_R6.json"
print("VERDICT_R6=", q.exists())
if q.exists():
    import json as _j; d=_j.loads(q.read_text(encoding="utf-8")); print("overall:", d.get("overall"))
