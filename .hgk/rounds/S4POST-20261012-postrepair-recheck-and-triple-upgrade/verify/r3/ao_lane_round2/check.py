import hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
root=Path.cwd(); ao=root/'.ao-r3b'; rnd='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; py='C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe'
env=os.environ.copy(); env.pop('PYTHONDONTWRITEBYTECODE',None)
env.update(PYTHONPATH=str(root)+os.pathsep+str(ao),PYTHONPYCACHEPREFIX=str(ao/'bytecode'),TMP=str(ao/'tmp'),TEMP=str(ao/'tmp'),PYTHONIOENCODING='utf-8')
(ao/'tmp').mkdir(exist_ok=True); data={}; transcript=[]
def run(name,args,environment=env):
    result=subprocess.run(args,cwd=root,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    text=result.stdout.decode('utf-8',errors='replace'); (ao/(name+'.log')).write_bytes(result.stdout)
    record={'command':subprocess.list2cmdline(args),'exit':result.returncode,'output':text}; transcript.append(record); data[name]=record
    (ao/'transcript.json').write_text(json.dumps(transcript,ensure_ascii=False,indent=2),encoding='utf-8')
    (ao/'measurements.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,result.returncode,text[-900:],flush=True); return record
def git(*args): return subprocess.check_output(['git',*args],cwd=root)
def sha(payload): return hashlib.sha256(payload).hexdigest()
def load(path): return json.loads((root/path).read_text(encoding='utf-8'))
data['subject']=git('rev-parse','HEAD').decode().strip(); data['tree']=git('rev-parse','HEAD^{tree}').decode().strip(); data['main']=git('rev-parse','refs/remotes/origin/main').decode().strip()
run('before-status',['git','status','--porcelain']); run('before-ignored',['git','status','--porcelain','--ignored'])
block=(root/rnd/'R3_PUBLICATION.md').read_text(encoding='utf-8')
block=block.split(chr(96)*3+'bash')[1].split(chr(96)*3)[0]; (ao/'publication-section3-verbatim.txt').write_text(block,encoding='utf-8')
commands=re.findall(r'python "\$R/verify/tools/check_evidence_locators.py".*?(?=\n#)',block,re.S)
bashenv=env.copy(); bashenv['PATH']=str(Path(py).parent)+os.pathsep+env['PATH']
for name,command in zip(['locator-negative','locator-positive'],commands): run(name,['C:/Program Files/Git/usr/bin/bash.exe','-c','R='+rnd+'\n'+command],bashenv)
(ao/'url-control.md').write_text('URL in prose https://host.invalid/a/b.json and real path tools/build_public_plugin.py\n',encoding='utf-8')
run('url-control',[py,rnd+'/verify/tools/check_evidence_locators.py','--root','.','--search-dir','.','.ao-r3b/url-control.md'])
pack=load(rnd+'/evidence/EVIDENCE_RETURN_PACK.json'); data['commands_records']=pack['commands']; data['hashes']=[]
for entry in pack['commands']:
    for value in entry.values():
        if isinstance(value,str) and value.endswith('.log'):
            path=value if (root/value).exists() else rnd+'/'+value
            blob=git('cat-file','-p',data['subject']+':'+path); disk=(root/path).read_bytes(); crlf=blob.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
            data['hashes'].append(dict(path=path,bytes=len(blob),blob=sha(blob),disk=sha(disk),crlf=sha(crlf),record=entry))
tracked=git('ls-files','-z').decode().split('\0'); data['com_ao3_files']=[path for path in tracked if path and (root/path).is_file() and b'com.ao3' in (root/path).read_bytes()]
ledgerpath=rnd+'/verify/r3/FROZEN_SOURCE_LEDGER.json'; ledger=load(ledgerpath); data['ledger_commit']=ledger['commit']; data['ledger_keys']=list(ledger); data['derivations']=[]
for entry in load('packaging/public-plugin/derivations.json')['derivations']:
    path='skills/'+entry['skill']+'/SKILL.md'; actual=sha((root/path).read_bytes())
    data['derivations'].append(dict(path=path,actual=actual,recorded=entry['source_sha256'],ledger=ledger['files'][path]))
release=load('packaging/public-plugin/plugin.release.json'); manifest=load('packaging/public-plugin/plugin.json')
data['vendor']=dict(actual=sha((root/'packaging/public-plugin/vendor-plugin.schema.json').read_bytes()),release=release['official_schema_sha256'],manifest=manifest['extensions']['com.pipd.s4']['official_schema_sha256'])
data['icons_before']=[dict(path=entry['path'],exists=(root/'packaging/public-plugin'/entry['path']).exists(),pin=entry['sha256']) for entry in release['icons']]
outside=Path(tempfile.mkdtemp(prefix='ao-r3b-build-',dir=os.environ.get('TEMP'))); data['outside_build_dir']=str(outside)
run('build-exact',[py,'tools/build_public_plugin.py','--source-root','.','--ledger',ledgerpath,'--source-commit',ledger['commit'],'--out-dir',str(outside/'exact')])
copy=ao/'packaging-copy'; shutil.copytree(root/'packaging/public-plugin',copy)
run('build-generated',[py,'tools/build_public_plugin.py','--source-root','.','--ledger',ledgerpath,'--source-commit',ledger['commit'],'--packaging-root',str(copy),'--out-dir',str(outside/'generated'),'--generate-icons'])
data['icons_generated']=[dict(path=entry['path'],pin=entry['sha256'],actual=sha((copy/entry['path']).read_bytes()) if (copy/entry['path']).exists() else None) for entry in release['icons']]
workflow=(root/'.github/workflows/public-plugin-verify.yml').read_text(encoding='utf-8'); allowed=re.search("ALLOWED='([^']+)'",workflow).group(1); denied=re.search("DENIED='([^']+)'",workflow).group(1); data['base_guards']=[]
for base in [data['main'],'52542c395a0f91dc2ba4bd6123acd4cdecd780dc']:
    paths=git('diff','--name-only',base+'...HEAD').decode().splitlines(); frozen=[path for path in paths if re.search(denied,path)]; other=[path for path in paths if not re.search(denied,path) and not re.search(allowed,path)]
    data['base_guards'].append(dict(base=base,changed=len(paths),product_side=len([path for path in paths if not path.startswith('.hgk/')]),schemas=len([path for path in paths if path.startswith('schemas/')]),src=len([path for path in paths if path.startswith('src/')]),frozen=frozen,outside_allowed=other,derived_exit=1 if frozen or other else 0))
run('focused',[py,'-m','unittest','discover','-s','tests','-p','test_s4ext_*.py','-v'])
run('full',[py,'-m','unittest','discover','-s','tests','-t','.','-v'])
run('after-status',['git','status','--porcelain']); run('after-ignored',['git','status','--porcelain','--ignored']); run('tracked-diff',['git','diff','--exit-code'])
print('MEASUREMENTS_COMPLETE',flush=True)
