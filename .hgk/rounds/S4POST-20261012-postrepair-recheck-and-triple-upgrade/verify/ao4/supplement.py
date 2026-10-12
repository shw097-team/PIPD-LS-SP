import json
import os
from pathlib import Path
import subprocess

DELIVERY = Path.cwd()
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
EVIDENCE = DELIVERY / ROUND / 'verify/ao4'
INVENTORY = json.loads((EVIDENCE / 'inventory.json').read_text())
TEMP = Path(INVENTORY['temp'])
TARGET = TEMP / 'harness'
BASH = r'C:\Program Files\Git\usr\bin\bash.exe'
RESULTS = []


def run(name, args, cwd):
    env = os.environ.copy()
    env['LANE_WT'] = TARGET.as_posix()
    env['TMPDIR'] = (TEMP / 'harness-logs').as_posix()
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True,
                            encoding='utf-8', errors='replace', timeout=90)
    record = {'name': name, 'command': args, 'cwd': str(cwd), 'exit_code': result.returncode,
              'stdout': result.stdout, 'stderr': result.stderr}
    RESULTS.append(record)
    text = 'COMMAND: ' + subprocess.list2cmdline(args) + '\nCWD: ' + str(cwd) + '\nEXIT_CODE: ' + str(result.returncode) + '\nRAW STDOUT:\n' + result.stdout + '\nRAW STDERR:\n' + result.stderr
    (EVIDENCE / (name + '.txt')).write_text(text, encoding='utf-8')
    print(text, flush=True)
    return result


run('harness-clone', ['git', 'clone', '--no-hardlinks', '--no-checkout', str(DELIVERY), str(TARGET)], TEMP)
run('harness-checkout', ['git', 'checkout', '--detach', INVENTORY['subject']], TARGET)
run('harness-config-name', ['git', 'config', 'user.name', 'AO4 external probe'], TARGET)
run('harness-config-email', ['git', 'config', 'user.email', 'ao4-probe@local'], TARGET)
run('harness-initial-status', ['git', 'status', '--porcelain'], TARGET)
(TARGET / ROUND / 'stage-b/ao4-harness-fixture.txt').write_text('harness preflight fixture\n', encoding='utf-8')
run('harness-before', ['git', 'status', '--porcelain'], TARGET)
run('harness-missing-brief', [BASH, (TARGET / ROUND / 'stage-b/run_lane.sh').as_posix(), 'AO4_HARNESS', 'AO4_DELIBERATELY_NONEXISTENT_BRIEF.md', 'verify/ao4'], TARGET)
run('harness-probe-history', ['git', 'log', '--reverse', '--format=fuller', '--name-status', INVENTORY['subject'] + '..HEAD'], TARGET)
run('outside-round-diff', ['git', 'diff', '--exit-code', '07681745a436a7d82e85a0aa494d8165acad92a0', INVENTORY['subject'], '--', '.', ':!.hgk/rounds'], DELIVERY)
run('final-status', ['git', 'status', '--porcelain'], DELIVERY)
run('final-identity', ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}'], DELIVERY)
(EVIDENCE / 'supplement-results.json').write_text(json.dumps(RESULTS, indent=2), encoding='utf-8')

