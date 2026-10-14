import subprocess
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS"); ROUND = Path(r"C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R6-20261014-far-remediation-and-repair"); VAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\R6-20261014-far-remediation-and-repair")
PY = str(HGK/".venv/Scripts/python.exe")
prompt = (ROUND/"scripts/_prompt_r6_execute.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"), "--lane","EXECUTE","--prompt",prompt,
   "--round","R6-20261014-far-remediation-and-repair","--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5z-wt",
   "--force-rank","1","--require-arm","opencode-go/deepseek-v4.1-flash",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R6-20261014-far-remediation-and-repair",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt",
   "--timeout","1800","--attempt-log-dir",str(VAR/"EXECUTE/attempts"),
   "--json-out",str(VAR/"EXECUTE/dispatch_receipt.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=2000, cwd=str(HGK))
(VAR/"EXECUTE/dispatch.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
o = VAR/"EXECUTE/out"
print("EXIT=", r.returncode)
print("MANIFEST=", (o/"acceptance/GOVERNING_DOCS_MANIFEST.json").exists(), "| PROTOCOL=", (o/"VERIFICATION_PROTOCOL.md").exists(),
      "| TSV=", (o/"UPG_TRACEABILITY_R6.tsv").exists(), "| ZIP=", (o/"ZIP_REPRODUCTION.json").exists())
