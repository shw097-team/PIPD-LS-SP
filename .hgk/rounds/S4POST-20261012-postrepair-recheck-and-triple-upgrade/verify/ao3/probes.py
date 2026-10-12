from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
SUBJECT = Path.cwd()
ROUND = Path('.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade')
OUT = SUBJECT / ROUND / 'verify/ao3'
CANDIDATE = Path((OUT / 'snapshot-path.txt').read_text())
SCRATCH = Path(tempfile.mkdtemp(prefix='pipd-ao3-probes-'))
sys.path.insert(0, str(CANDIDATE / 'tools'))
import build_public_plugin as builder
import freeze_public_plugin_source as freezer
RESULTS = {}
def digest(data):
    return hashlib.sha256(data).hexdigest()
def run(name, command, cwd=CANDIDATE, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    header = f'COMMAND: {subprocess.list2cmdline(command)}\nCWD: {cwd}\nEXIT_CODE: {result.returncode}\nRAW OUTPUT:\n'
    (OUT / (name + '.txt')).write_bytes(header.encode() + result.stdout)
    RESULTS[name] = {'command':command,'cwd':str(cwd),'exit':result.returncode,'stdout':result.stdout.decode(errors='replace')}
    return result
source = SCRATCH / 'source'
for name in freezer.EXPECTED_SKILLS:
    folder = source / 'skills' / name
    folder.mkdir(parents=True)
    (folder / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Independent AO3 fixture.\nowner: synthetic-owner\n---\n# AO3 {name}\nBody sentinel: do not transform.\n', encoding='utf-8', newline='\n')
    (folder / 'references').mkdir()
    (folder / 'references/ao3.txt').write_bytes(b'AO3 auxiliary payload\x00\xff')
ledger = freezer.freeze(source, require_git=False, commit_override='c'*40, tree_override='d'*40)
ledger_path = SCRATCH / 'ledger.json'
ledger_path.write_bytes(builder.canonical_json_bytes(ledger))
packaging = SCRATCH / 'packaging'
shutil.copytree(CANDIDATE / 'packaging/public-plugin', packaging)
icon = builder.png_icon_bytes()
(packaging / 'assets').mkdir(exist_ok=True)
(packaging / 'assets/icon-128.png').write_bytes(icon)
release = json.loads((packaging / 'plugin.release.json').read_text())
release['publisher'] = {'name':'AO3 SYNTHETIC NOT A PUBLISHER','identity':'ao3@example.invalid','identity_sha256':'f'*64}
release['icons'][0]['sha256'] = digest(icon)
manifest = json.loads((packaging / 'plugin.json').read_text())
manifest['extensions'][builder.RELEASE_EXTENSION_KEY] = release
derivations = {'schema':'PIPD-PUBLIC-PLUGIN-DERIVATIONS/1','derivations':[]}
for name in freezer.EXPECTED_SKILLS:
    rel = f'skills/{name}/SKILL.md'
    derivations['derivations'].append({'skill':name,'source_path':rel,'source_sha256':ledger['files'][rel],'kept_keys':['name','description'],'dropped_keys':['owner'],'approved_by':'ao3@example.invalid','approval_receipt':'AO3-SYNTHETIC-NO-HUMAN-APPROVAL'})
for name, value in [('plugin.json',manifest),('plugin.release.json',release),('derivations.json',derivations)]:
    (packaging / name).write_bytes(builder.canonical_json_bytes(value))
def build(name, destination, packaging_root=packaging, source_root=source):
    return run(name, [sys.executable,str(CANDIDATE / 'tools/build_public_plugin.py'),'--source-root',str(source_root),'--ledger',str(ledger_path),'--source-commit','c'*40,'--packaging-root',str(packaging_root),'--out-dir',str(destination)])
build('probe-control', SCRATCH / 'control')
build('probe-rebuild', SCRATCH / 'rebuild')
file_names = ['pipd-ls-sp-public-skills.zip','pipd-ls-sp-public-skills.zip.sha256','SOURCE_TO_PLUGIN_MAPPING.json','RELEASE_RECEIPT.json']
comparison = {name:{'first':digest((SCRATCH/'control'/name).read_bytes()),'second':digest((SCRATCH/'rebuild'/name).read_bytes()),'equal':(SCRATCH/'control'/name).read_bytes()==(SCRATCH/'rebuild'/name).read_bytes()} for name in file_names}
projection = []
with zipfile.ZipFile(SCRATCH/'control'/file_names[0]) as archive:
    for name in freezer.EXPECTED_SKILLS:
        rel = f'pipd-ls-sp-public-skills/skills/{name}/SKILL.md'
        actual = archive.read(rel)
        expected = f'---\nname: {name}\ndescription: Independent AO3 fixture.\n---\n# AO3 {name}\nBody sentinel: do not transform.\n'.encode()
        projection.append({'member':rel,'equal_expected_bytes':actual==expected,'sha256':digest(actual)})
        auxiliary = f'pipd-ls-sp-public-skills/skills/{name}/references/ao3.txt'
        projection.append({'member':auxiliary,'equal_expected_bytes':archive.read(auxiliary)==b'AO3 auxiliary payload\x00\xff'})
    inventory = archive.namelist()
collisions = []
for mode in ('regular','hardlink'):
    for index, member in enumerate(file_names):
        destination = SCRATCH / f'collision-{mode}-{index}'
        destination.mkdir()
        sentinel = SCRATCH / f'sentinel-{mode}-{index}'
        sentinel.write_bytes(b'AO3_EXTERNAL_DO_NOT_TOUCH\x00\xfe')
        seeded = destination/member
        if mode == 'hardlink':
            os.link(sentinel, seeded)
        else:
            seeded.write_bytes(sentinel.read_bytes())
        before = digest(sentinel.read_bytes())
        result = build(f'probe-collision-{mode}-{index}',destination)
        collisions.append({'mode':mode,'member':member,'samefile':os.path.samefile(sentinel,seeded),'exit':result.returncode,'sentinel_unchanged':digest(sentinel.read_bytes())==before,'seed_unchanged':seeded.read_bytes()==sentinel.read_bytes(),'remaining_members':sorted(path.name for path in destination.iterdir())})
build('probe-output-overlap',source/'ao3-output')
build('probe-output-dist',source/'dist'/'ao3-output')
for case in ('missing-owner','unknown-manifest','bad-vendor','missing-derivation'):
    altered = SCRATCH / ('packaging-'+case)
    shutil.copytree(packaging,altered)
    if case == 'missing-owner':
        value = json.loads((altered/'plugin.release.json').read_text())
        value['publisher']['name']='OWNER_INPUT_REQUIRED'
        (altered/'plugin.release.json').write_bytes(builder.canonical_json_bytes(value))
    elif case == 'unknown-manifest':
        value = json.loads((altered/'plugin.json').read_text())
        value['unreviewed']='AO3'
        (altered/'plugin.json').write_bytes(builder.canonical_json_bytes(value))
    elif case == 'bad-vendor':
        with (altered/'vendor-plugin.schema.json').open('ab') as stream:
            stream.write(b' ')
    else:
        (altered/'derivations.json').write_text('{"schema":"PIPD-PUBLIC-PLUGIN-DERIVATIONS/1","derivations":[]}')
    build('probe-refusal-'+case,SCRATCH/('output-'+case),altered)
member_path = source/'skills'/freezer.EXPECTED_SKILLS[0]/'SKILL.md'
original = member_path.read_bytes()
member_path.write_bytes(original+b'UNREVIEWED DRIFT')
build('probe-source-drift',SCRATCH/'drift-output')
member_path.write_bytes(original)
extra = source/'skills'/'unreviewed-ninth'
extra.mkdir()
build('probe-ninth-skill',SCRATCH/'ninth-output')
extra.rmdir()
pack = CANDIDATE/'dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3'
release_commit = 'cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a'
def fallback(name, mount, destination, extra_args=None):
    return run(name,[sys.executable,str(CANDIDATE/'tools/build_web_fallback.py'),'--mount-pack',str(mount),'--release-id','v0.1.1-preview.3','--release-commit',release_commit,'--out',str(destination)]+(extra_args or []))
fallback('probe-web-control',pack,SCRATCH/'web1.md')
fallback('probe-web-rebuild',pack,SCRATCH/'web2.md')
web_comparison = {'first':digest((SCRATCH/'web1.md').read_bytes()),'second':digest((SCRATCH/'web2.md').read_bytes()),'equal':(SCRATCH/'web1.md').read_bytes()==(SCRATCH/'web2.md').read_bytes()}
web_sentinel = SCRATCH/'web-sentinel'
web_sentinel.write_bytes(b'AO3 WEB SENTINEL')
os.link(web_sentinel,SCRATCH/'web-linked.md')
fallback('probe-web-hardlink',pack,SCRATCH/'web-linked.md')
web_comparison['hardlink_unchanged'] = web_sentinel.read_bytes()==b'AO3 WEB SENTINEL'
fallback('probe-web-preseeded',pack,SCRATCH/'web1.md')
fallback('probe-web-size',pack,SCRATCH/'web-too-small.md',['--size-cap','1'])
for case in ('drift','extra','traversal'):
    altered = SCRATCH/('web-'+case)
    shutil.copytree(pack,altered)
    if case == 'drift':
        with (altered/'SKILL.md').open('ab') as stream:
            stream.write(b'UNREVIEWED DRIFT')
    elif case == 'extra':
        (altered/'unreviewed.txt').write_bytes(b'UNREVIEWED')
    else:
        with (altered/'MANIFEST.sha256').open('a') as stream:
            stream.write('0'*64+'  ../escape.md\n')
    fallback('probe-web-'+case,altered,SCRATCH/('web-result-'+case+'.md'))
guard_environment = os.environ.copy()
guard_environment.update({'PR_BASE_SHA':'','STACKED_BASE_SHA':'52542c395a0f91dc2ba4bd6123acd4cdecd780dc'})
for case,path in [('frozen','dist/ao3.txt'),('outside','docs/ao3-unallowed.md'),('allowed','docs/install/ao3.md'),('unresolved',None)]:
    if path is None:
        env = guard_environment.copy()
        env['STACKED_BASE_SHA']='0'*40
        run('probe-guard-'+case,['C:/Program Files/Git/bin/bash.exe',str(OUT/'guard-extracted.sh')],env=env)
    else:
        shell = 'git() { if [ "$1" = diff ]; then printf "%s\n" '+path+'; else command git "$@"; fi; }; export -f git; bash "$1"'
        run('probe-guard-'+case,['C:/Program Files/Git/bin/bash.exe','-c',shell,'ao3',str(OUT/'guard-extracted.sh')],env=guard_environment)
summary = {'scratch':str(SCRATCH),'fixture':'independently authored; no candidate test helper used; synthetic approval is not human authority','determinism':comparison,'projection':projection,'inventory':inventory,'collisions':collisions,'web':web_comparison,'commands':RESULTS}
(OUT/'probe-results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
