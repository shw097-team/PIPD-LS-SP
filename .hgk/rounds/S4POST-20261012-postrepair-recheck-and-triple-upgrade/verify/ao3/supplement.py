from pathlib import Path
import json, shutil, subprocess, sys, zipfile
SUBJECT = Path.cwd()
ROUND = Path('.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade')
OUT = SUBJECT/ROUND/'verify/ao3'
CANDIDATE = Path((OUT/'snapshot-path.txt').read_text())
SCRATCH = Path(json.loads((OUT/'probe-results.json').read_text())['scratch'])
def run(name,command,cwd=CANDIDATE):
    result = subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/(name+'.txt')).write_bytes(f'COMMAND: {subprocess.list2cmdline(command)}\nCWD: {cwd}\nEXIT_CODE: {result.returncode}\nRAW OUTPUT:\n'.encode()+result.stdout)
    print(name,result.returncode,flush=True)
    return result
code = 'from pathlib import Path; import sys; root=Path(sys.argv[1]); selected=sorted(p for p in root.iterdir() if p.name.startswith(("MODEL_DECLARED_","probe_","B1_20261012T101452Z","B2_20261012T101452Z","B3_20261012T101452Z","B1_attempt3_","B2_attempt3_","B3_attempt3_")) and p.is_file()); [(print("FILE:",p.name),print(p.read_text(encoding="utf-8",errors="replace") if p.suffix in (".exit",".txt") or p.name.startswith("probe_") else repr(p.read_text(encoding="utf-8",errors="replace").splitlines()[:12])+repr(p.read_text(encoding="utf-8",errors="replace").splitlines()[-18:]))) for p in selected]'
run('model-summary-retry',[sys.executable,'-c',code,str(ROUND/'stage-b')])
ledger = CANDIDATE/ROUND/'evidence/08_PLUGIN/FROZEN_SOURCE_LEDGER.json'
commit = json.loads(ledger.read_text())['commit']
run('candidate-default-refusal-retry',[sys.executable,str(CANDIDATE/'tools/build_public_plugin.py'),'--source-root',str(CANDIDATE),'--ledger',str(ledger),'--source-commit',commit,'--packaging-root',str(CANDIDATE/'packaging/public-plugin'),'--out-dir',str(SCRATCH/'default-refusal')])
for case in ('name','version','extension'):
    altered = SCRATCH/('judgement-'+case)
    shutil.copytree(SCRATCH/'packaging',altered)
    manifest = json.loads((altered/'plugin.json').read_text())
    if case == 'name':
        manifest['name']='ao3-foreign-package'
    elif case == 'version':
        manifest['version']='999.0.0'
    else:
        manifest['extensions']['com.ao3.unreviewed']={'unreviewed_instruction':'AO3 opaque extension is outside the derivation approval gate'}
    (altered/'plugin.json').write_text(json.dumps(manifest))
    destination = SCRATCH/('judgement-output-'+case)
    result = run('probe-judgement-'+case,[sys.executable,str(CANDIDATE/'tools/build_public_plugin.py'),'--source-root',str(SCRATCH/'source'),'--ledger',str(SCRATCH/'ledger.json'),'--source-commit','c'*40,'--packaging-root',str(altered),'--out-dir',str(destination)])
    if result.returncode==0:
        zip_path = destination/'pipd-ls-sp-public-skills.zip'
        run('probe-judgement-'+case+'-readback',[sys.executable,'-c','import zipfile,sys,json; z=zipfile.ZipFile(sys.argv[1]); m=json.loads(z.read("pipd-ls-sp-public-skills/plugin.json")); r=json.loads(z.read("pipd-ls-sp-public-skills/RELEASE_RECEIPT.json")); print(json.dumps({"manifest":m,"receipt":r},indent=2))',str(zip_path)])
run('doctor-system-python',['C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe','-m','unittest','-v','tests.test_doctor_schema_truth'])
run('snapshot-end-identity',['git','rev-parse','HEAD','HEAD^{tree}'])
run('delivery-end-identity',['git','rev-parse','HEAD','HEAD^{tree}'],SUBJECT)
run('delivery-end-status',['git','status','--porcelain'],SUBJECT)
