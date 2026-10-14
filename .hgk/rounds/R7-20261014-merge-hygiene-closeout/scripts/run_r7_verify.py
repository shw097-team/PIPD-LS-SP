import subprocess, json
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R7-20261014-merge-hygiene-closeout"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R7-20261014-merge-hygiene-closeout")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r7_verify.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"), "--lane","VERIFY_SECURITY","--prompt",prompt,
   "--round","R7-20261014-merge-hygiene-closeout","--cwd",str(ROUND),
   "--force-rank","3","--require-arm","opencode-go/glm-5.3-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject",str(ROUND),
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r7-wt",
   "--timeout","1800","--attempt-log-dir",str(VAR/"VERIFY_SECURITY/attempts"),
   "--json-out",str(VAR/"VERIFY_SECURITY/dispatch_receipt_r7.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=2000, cwd=str(HGK))
(VAR/"VERIFY_SECURITY/dispatch_r7.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
q = VAR/"VERIFY_SECURITY/VERDICT_R7.json"
print("EXIT=", r.returncode, "| VERDICT_R7=", q.exists())
if q.exists(): print("overall:", json.loads(q.read_text(encoding="utf-8")).get("overall"))
