import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R7-20261014-merge-hygiene-closeout"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R7-20261014-merge-hygiene-closeout")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r7_execute.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"), "--lane","EXECUTE","--prompt",prompt,
   "--round","R7-20261014-merge-hygiene-closeout","--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r7-wt",
   "--force-rank","1","--require-arm","opencode-go/deepseek-v4.1-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject",str(ROUND),
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt",
   "--timeout","1800","--attempt-log-dir",str(VAR/"EXECUTE/attempts"),
   "--json-out",str(VAR/"EXECUTE/dispatch_receipt.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=2000, cwd=str(HGK))
(VAR/"EXECUTE/dispatch.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
wt = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/r7-wt")
print("EXIT=", r.returncode)
print("README_has_section=", "Current state and evidence entry points" in (wt/"README.md").read_text(encoding="utf-8", errors="ignore"))
print("REPO_STATE=", (wt/"docs/REPO_STATE.md").exists(), "| NEXT_SESSION=", (wt/"docs/NEXT_SESSION_START.md").exists())
