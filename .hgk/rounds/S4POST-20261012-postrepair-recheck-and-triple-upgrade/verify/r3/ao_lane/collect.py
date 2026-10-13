import subprocess
import os
import json
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / '.ao-r3'
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
PYTHON = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)
records = []

def run(label, argv, cwd=ROOT):
    result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (OUT / (label + '.txt')).write_bytes(result.stdout)
    record = {'label': label, 'argv': argv, 'cwd': str(cwd), 'exit': result.returncode, 'output': result.stdout.decode('utf-8', errors='replace')}
    records.append(record)
    (OUT / 'transcript.json').write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
    print(label, 'exit', result.returncode, flush=True)
    return record

run('binding', ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}', 'refs/remotes/origin/main'])
run('python', [PYTHON, '-V'])
run('before-status', ['git', 'status', '--porcelain'])
run('before-ignored', ['git', 'status', '--porcelain', '--ignored'])
run('C1', [PYTHON, '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_s4ext_*.py', '-v'])
run('C2', [PYTHON, '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.'])
run('after-status', ['git', 'status', '--porcelain'])
run('after-ignored', ['git', 'status', '--porcelain', '--ignored'])
run('C5', [PYTHON, 'verify/tools/check_evidence_locators.py', '--root', '.', '--search-dir', '.', 'verify/ao12/EXTERNAL_CHALLENGE_REPORT.md'], ROOT / ROUND)
run('C6', [PYTHON, ROUND + '/verify/tools/check_evidence_locators.py', '--root', '.', '--search-dir', '.', ROUND + '/OWNER_ACTION_REQUEST.md', ROUND + '/HARNESS_FREEZE_AND_AO_LOOP_CAP.md'])
run('C10-head', ['git', 'ls-tree', '-r', 'HEAD'])
run('C10-main', ['git', 'ls-tree', '-r', 'refs/remotes/origin/main'])
