import subprocess
from pathlib import Path
HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
PY = str(HGK/".venv/Scripts/python.exe")
ROUND = Path(r"C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5Y-20261014-gpt-plugin-publication")
VAR = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/R5Y-20261014-gpt-plugin-publication-recheck")
prompt = (ROUND/"scripts/_prompt_ts12_recheck.txt").read_text(encoding="utf-8")
cmd = [PY, str(HGK/"scripts/hgk-lane-dispatch.py"),
   "--lane","VERIFY_SECURITY","--prompt",prompt,
   "--round","R5Y-20261014-gpt-plugin-publication-recheck",
   "--cwd","C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt",
   "--force-rank","4","--require-arm","openai-codex/gpt-6.1-sol","--allow-human-home-transport",
   "--sandbox","danger-full-access","--allow-sandbox-escalation",
   "--guard-subject","C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5Y-20261014-gpt-plugin-publication",
   "--timeout","900",
   "--attempt-log-dir",str(VAR/"attempts"),
   "--json-out",str(VAR/"dispatch_receipt.json")]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200, cwd=str(HGK))
(VAR/"dispatch.log").write_text((r.stdout or "")+"\n---STDERR---\n"+(r.stderr or ""), encoding="utf-8")
print("EXIT=", r.returncode)
v = HGK/"var/R5Y-20261014-gpt-plugin-publication/VERIFY_SECURITY/checker-verdict-recheck.json"
print("VERDICT_FILE=", v.exists())
