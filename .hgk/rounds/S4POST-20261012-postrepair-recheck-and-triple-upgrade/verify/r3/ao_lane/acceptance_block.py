import subprocess, os, json
from pathlib import Path
ROOT = Path.cwd()
OUT = ROOT / '.ao-r3'
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
text = (ROOT / ROUND / 'R3_PUBLICATION.md').read_text(encoding='utf-8')
section = text.split('## 3.',1)[1].split('## 4.',1)[0]
block = section.split(chr(96)*3+'bash',1)[1].split(chr(96)*3,1)[0].strip()
(OUT / 'C4-verbatim-block.txt').write_text(block+chr(10),encoding='utf-8')
steps = []
current = ''
for line in block.splitlines():
    if not line.strip() or line.lstrip().startswith('#'):
        continue
    current += line + chr(10)
    if line.rstrip().endswith(chr(92)):
        continue
    steps.append(current.rstrip())
    current = ''
script = ''
for index, step in enumerate(steps):
    if step.startswith('git clone'):
        script += 'echo C4_STEP_0 NOT_EXECUTED_NO_NETWORK_EXISTING_BOUND_CLONE'+chr(10)
        continue
    script += step+chr(10)
    script += 'echo C4_STEP_'+str(index)+' EXIT=$?'+chr(10)
    script += 'echo C4_CWD=$PWD'+chr(10)
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)
env['PATH'] = 'C:/Users/user/AppData/Local/Programs/Python/Python311;' + env['PATH']
result = subprocess.run(['C:/Program Files/Git/usr/bin/bash.exe','--noprofile','--norc','-c',script],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(OUT/'C4-output.txt').write_bytes(result.stdout)
(OUT/'C4-steps.json').write_text(json.dumps(steps,indent=2,ensure_ascii=False),encoding='utf-8')
print(result.stdout.decode('utf-8',errors='replace')[-9000:])

