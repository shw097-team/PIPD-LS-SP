from pathlib import Path
import json, shutil, subprocess, sys, tempfile, zipfile
OUT = Path(__file__).resolve().parent
CANDIDATE = Path((OUT/'snapshot-path.txt').read_text())
FIXTURE = Path(json.loads((OUT/'probe-results.json').read_text())['scratch'])
SCRATCH = Path(tempfile.mkdtemp(prefix='pipd-ao3-identity-repro-'))
packaging = SCRATCH/'packaging'
shutil.copytree(FIXTURE/'packaging',packaging)
manifest = json.loads((packaging/'plugin.json').read_text())
manifest['version']='999.0.0'
(packaging/'plugin.json').write_text(json.dumps(manifest))
command = [sys.executable,str(CANDIDATE/'tools/build_public_plugin.py'),'--source-root',str(FIXTURE/'source'),'--ledger',str(FIXTURE/'ledger.json'),'--source-commit','c'*40,'--packaging-root',str(packaging),'--out-dir',str(SCRATCH/'output')]
result = subprocess.run(command,cwd=CANDIDATE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print('COMMAND:',subprocess.list2cmdline(command))
print('CWD:',CANDIDATE)
print('BUILDER_EXIT_CODE:',result.returncode)
print(result.stdout.decode())
if result.returncode==0:
    with zipfile.ZipFile(SCRATCH/'output/pipd-ls-sp-public-skills.zip') as archive:
        actual_manifest=json.loads(archive.read('pipd-ls-sp-public-skills/plugin.json'))
        receipt=json.loads(archive.read('pipd-ls-sp-public-skills/RELEASE_RECEIPT.json'))
    print('MANIFEST_VERSION:',actual_manifest['version'])
    print('RECEIPT_VERSION:',receipt['version'])
    print('IDENTITY_MISMATCH_ACCEPTED:',actual_manifest['version']!=receipt['version'])
sys.exit(result.returncode)
