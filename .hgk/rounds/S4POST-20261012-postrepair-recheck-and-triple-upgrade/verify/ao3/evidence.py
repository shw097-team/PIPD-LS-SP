from pathlib import Path
import hashlib, json, os, subprocess, sys
SUBJECT = Path.cwd()
ROUND = Path('.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade')
OUT = SUBJECT/ROUND/'verify/ao3'
CANDIDATE = Path((OUT/'snapshot-path.txt').read_text())
def run(name,command,cwd=CANDIDATE):
    result = subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/(name+'.txt')).write_bytes(f'COMMAND: {subprocess.list2cmdline(command)}\nCWD: {cwd}\nEXIT_CODE: {result.returncode}\nRAW OUTPUT:\n'.encode()+result.stdout)
    print(name,result.returncode,flush=True)
    return result
paths = ['tools/build_public_plugin.py','tools/build_web_fallback.py','tools/freeze_public_plugin_source.py','.github/workflows/public-plugin-verify.yml','tests/test_public_plugin_packaging.py','tests/test_web_fallback.py','docs/install/README.md',str(ROUND/'AO2_HANDOVER_CLOSURE.md'),str(ROUND/'verify/ao2/LOCATION_NOTE.md')]
run('reviewed-source',[sys.executable,'-c','from pathlib import Path; import sys; [(print("FILE:",p),print(Path(p).read_text(encoding="utf-8",errors="replace"))) for p in sys.argv[1:]]']+paths)
run('code-unchanged-since-r2',['git','diff','--exit-code','07681745a436a7d82e85a0aa494d8165acad92a0','HEAD','--','.',':(exclude).hgk/rounds/**'])
run('delivery-tracked-diff',['git','diff','--exit-code'],SUBJECT)
run('delivery-index-diff',['git','diff','--cached','--exit-code'],SUBJECT)
run('original-root-tracked',['git','ls-tree','-r','--name-only','07681745a436a7d82e85a0aa494d8165acad92a0','verify/'])
run('original-root-status',[sys.executable,'-c','from pathlib import Path; import sys; root=Path(sys.argv[1]); print("exists",root.exists()); print("files",sorted(str(p) for p in root.rglob("*") if p.is_file()) if root.exists() else [])',str(SUBJECT/'verify')])
hash_code = 'from pathlib import Path; import hashlib,subprocess,sys,json; root=Path(sys.argv[1]); rows=[]; files=sorted(p for p in root.iterdir() if p.is_file()); print("COUNT",len(files)); print("OFFICER_COUNT_EXCLUDING_LOCATION_NOTE",len([p for p in files if p.name!="LOCATION_NOTE.md"])); [(rows.append({"name":p.name,"current_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"first_commit_sha256":hashlib.sha256(subprocess.check_output(["git","show","4807c111b6077fbe8f82d9edf1abc62a797f079d:"+p.as_posix()])).hexdigest()})) for p in files]; print(json.dumps(rows,indent=2)); print("CURRENT_EQUALS_FIRST_COMMIT",all(row["current_sha256"]==row["first_commit_sha256"] for row in rows)); print("This compares after-relocation states; no independently retained pre-move bytes are present here.")'
run('ao2-hashes',[sys.executable,'-c',hash_code,str(ROUND/'verify/ao2')])
model_code = 'from pathlib import Path; import sys; root=Path(sys.argv[1]); selected=sorted(p for p in root.iterdir() if p.name.startswith(("MODEL_DECLARED_","probe_","B1_20261012T101452Z","B2_20261012T101452Z","B3_20261012T101452Z","B1_attempt3_","B2_attempt3_","B3_attempt3_")) and p.is_file()); [(print("FILE:",p.name),print(p.read_text(encoding="utf-8",errors="replace") if p.suffix in (".exit",".txt") or p.name.startswith("probe_") else "HEAD:\n"+"\n".join(p.read_text(encoding="utf-8",errors="replace").splitlines()[:12])+"\nTAIL:\n"+"\n".join(p.read_text(encoding="utf-8",errors="replace").splitlines()[-18:]))) for p in selected]'
run('model-summary',[sys.executable,'-c',model_code,str(ROUND/'stage-b')])
run('candidate-default-refusal',[sys.executable,str(CANDIDATE/'tools/build_public_plugin.py'),'--source-root',str(CANDIDATE),'--ledger',str(CANDIDATE/'packaging/public-plugin/SOURCE_FREEZE_LEDGER.json'),'--source-commit','52542c395a0f91dc2ba4bd6123acd4cdecd780dc','--packaging-root',str(CANDIDATE/'packaging/public-plugin'),'--out-dir',str(CANDIDATE.parent/'default-refusal')])
system_python = 'C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
run('system-interpreter',[system_python,'-c','import sys,os; print(sys.executable); print(sys.version); print(os.getcwd())'])
run('system-pip',[system_python,'-m','pip','--version'])
run('wheel-system-python',[system_python,'-m','unittest','-v','tests.test_wheel_distribution','tests.test_first_run_examples'])
run('delivery-status-final',['git','status','--porcelain'],SUBJECT)
