import json
import os
from pathlib import Path
import subprocess
import tempfile

DELIVERY = Path.cwd()
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
EVIDENCE = DELIVERY / ROUND / 'verify/ao4'
BASE = '07681745a436a7d82e85a0aa494d8165acad92a0'
BASH = r'C:\Program Files\Git\usr\bin\bash.exe'
TEMP = Path(tempfile.mkdtemp(prefix='pipd-ao4-'))
RESULTS = []


def run(name, command, cwd=DELIVERY, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=90)
    record = {'name': name, 'command': command, 'cwd': str(cwd),
              'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    RESULTS.append(record)
    text = ('COMMAND: ' + subprocess.list2cmdline(command) + '\nCWD: ' + str(cwd)
            + '\nEXIT_CODE: ' + str(result.returncode) + '\nRAW STDOUT:\n'
            + result.stdout + '\nRAW STDERR:\n' + result.stderr)
    (EVIDENCE / (name + '.txt')).write_text(text, encoding='utf-8')
    print(text, flush=True)
    return result


run('delivery-start-status', ['git', 'status', '--porcelain'])
subject = run('delivery-identity', ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}']).stdout.splitlines()[0]
run('ancestor', ['git', 'merge-base', '--is-ancestor', BASE, subject])
run('history', ['git', 'log', '--reverse', '--format=commit %H%nparents %P%nsubject %s%n%b',
                '--name-status', '--no-renames', BASE + '..' + subject])
commits = run('commit-list', ['git', 'rev-list', '--reverse', BASE + '..' + subject]).stdout.splitlines()
for index, commit in enumerate(commits, 1):
    run('paths-' + str(index), ['git', 'diff-tree', '--root', '-m', '--no-commit-id',
                              '--name-only', '--no-renames', '-r', commit])
run('harness-trace', ['git', 'show', '--format=fuller', '--no-patch', 'f1dc870'])
run('historical-far-log', ['git', 'show', subject + ':' + ROUND + '/stage-b/FAR_20261012T121718Z.log'])
run('script-numbered', [BASH, '-c', 'nl -ba "$1"', 'ao4',
                       (DELIVERY / ROUND / 'stage-b/run_lane.sh').as_posix()])


def clone(name):
    target = TEMP / name
    result = run(name + '-clone', ['git', 'clone', '--no-hardlinks', '--no-checkout',
                                 str(DELIVERY), str(target)], TEMP)
    if result.returncode:
        raise RuntimeError('clone failed')
    run(name + '-checkout', ['git', 'checkout', '--detach', subject], target)
    run(name + '-config-name', ['git', 'config', 'user.name', 'AO4 external probe'], target)
    run(name + '-config-email', ['git', 'config', 'user.email', 'ao4-probe@local'], target)
    run(name + '-initial-status', ['git', 'status', '--porcelain'], target)
    return target


def environment(target, name):
    env = os.environ.copy()
    env['LANE_WT'] = target.as_posix()
    env['TMPDIR'] = (TEMP / (name + '-logs')).as_posix()
    return env


dirty = clone('dirty')
(dirty / 'ao4-scratch.txt').write_text('untracked refusal fixture\n', encoding='utf-8')
run('dirty-before', ['git', 'status', '--porcelain'], dirty)
run('dirty-refusal', [BASH, (dirty / ROUND / 'stage-b/run_lane.sh').as_posix(),
                      'AO4_DIRTY', 'VERIFIER_AO4_BRIEF.md', 'verify/ao4'],
    dirty, environment(dirty, 'dirty'))
run('dirty-after', ['git', 'status', '--porcelain'], dirty)
run('dirty-head-after', ['git', 'rev-parse', 'HEAD'], dirty)

clean = clone('clean')
run('clean-missing-brief', [BASH, (clean / ROUND / 'stage-b/run_lane.sh').as_posix(),
                          'AO4_MISSING', 'AO4_DELIBERATELY_NONEXISTENT_BRIEF.md', 'verify/ao4'],
    clean, environment(clean, 'clean'))
run('clean-after', ['git', 'status', '--porcelain'], clean)
run('clean-probe-history', ['git', 'log', '--format=fuller', '--name-status', subject + '..HEAD'], clean)

post = clone('postflight')
injection = ('cp() { command cp "$@"; printf "postflight dirt fixture\\n" > "$LANE_WT/ao4-postflight-scratch.txt"; }; '
             'export -f cp; bash "$1" AO4_POST AO4_DELIBERATELY_NONEXISTENT_BRIEF.md verify/ao4')
run('postflight-dirt', [BASH, '-c', injection, 'ao4', (post / ROUND / 'stage-b/run_lane.sh').as_posix()],
    post, environment(post, 'postflight'))
run('postflight-after', ['git', 'status', '--porcelain'], post)

inventory = {'temp': str(TEMP), 'subject': subject, 'commits': commits,
             'dirty_logs': [str(path) for path in (TEMP / 'dirty-logs').rglob('*')],
             'clean_logs': [str(path) for path in (TEMP / 'clean-logs').rglob('*')],
             'clean_root_output_exists': (clean / 'verify/ao4').exists(),
             'clean_round_output_exists': (clean / ROUND / 'verify/ao4').exists()}
(EVIDENCE / 'inventory.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
print(json.dumps(inventory, indent=2), flush=True)
run('delivery-end-status', ['git', 'status', '--porcelain'])
run('delivery-end-identity', ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}'])
(EVIDENCE / 'command-results.json').write_text(json.dumps(RESULTS, indent=2), encoding='utf-8')

