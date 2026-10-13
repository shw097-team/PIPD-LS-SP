import subprocess, os, json, hashlib
from pathlib import Path
ROOT = Path.cwd()
OUT = ROOT / '.ao-r3'
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
records = []
def run(label, args, env=None):
    result = subprocess.run(args, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (OUT/(label+'.txt')).write_bytes(result.stdout)
    records.append({'label':label,'argv':args,'exit':result.returncode,'output':result.stdout.decode('utf-8',errors='replace')})
    print(label, result.returncode, flush=True)
workflow = (ROOT/'.github/workflows/public-plugin-verify.yml').read_text(encoding='utf-8')
part = workflow.split('      - name: Prove the upgrade wrote only inside its allowed set',1)[1].split('      - name:',1)[0]
guard = part.split('        run: |',1)[1]
guard = chr(10).join(line[10:] for line in guard.splitlines() if line.strip())
for label, base in [('guard-stacked','52542c395a0f91dc2ba4bd6123acd4cdecd780dc'),('guard-main','224591431a164ab72a9423cd180e417e8a762403')]:
    env = os.environ.copy()
    env['PR_BASE_SHA'] = base
    env['STACKED_BASE_SHA'] = '52542c395a0f91dc2ba4bd6123acd4cdecd780dc'
    run(label,['C:/Program Files/Git/usr/bin/bash.exe','--noprofile','--norc','-c',guard],env)
run('final-refs',['git','show-ref'])
run('C6-detail',['C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe',ROUND+'/verify/tools/check_evidence_locators.py','--root','.','--search-dir','.','--json-out',str(OUT/'C6-detail.json'),ROUND+'/OWNER_ACTION_REQUEST.md',ROUND+'/HARNESS_FREEZE_AND_AO_LOOP_CAP.md'])
pack = json.loads((ROOT/ROUND/'evidence/EVIDENCE_RETURN_PACK.json').read_text(encoding='utf-8'))
hashes = []
for entry in pack['commands']:
    data = (ROOT/ROUND/entry['raw_log']).read_bytes()
    converted = data.replace(bytes([13,10]),bytes([10])).replace(bytes([10]),bytes([13,10]))
    hashes.append({'path':entry['raw_log'],'synthetic_CRLF_sha256':hashlib.sha256(converted).hexdigest(),'declared_worktree':entry['log_sha256_worktree_eol']})
(OUT/'CRLF-diagnostic.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
(OUT/'supplement-transcript.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(hashes,indent=2))
