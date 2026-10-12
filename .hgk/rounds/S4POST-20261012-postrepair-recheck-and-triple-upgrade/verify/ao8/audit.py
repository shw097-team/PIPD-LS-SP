import os, subprocess, pathlib, tempfile, json, hashlib, sys
WT=pathlib.Path.cwd()
REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
OUT=WT/REL/'verify/ao8'
BASE=pathlib.Path(tempfile.mkdtemp(prefix='a8-',dir=os.environ['TEMP']))
ENV=os.environ.copy()
for k in ['MSYS_NO_PATHCONV','MSYS2_ARG_CONV_EXCL','BASH_ENV','ENV']: ENV.pop(k,None)
ENV['PATH']='C:/Program Files/Git/usr/bin;C:/Program Files/Git/mingw64/bin;'+str(pathlib.Path(sys.executable).parent)+';'+ENV['PATH']
BASH='C:/Program Files/Git/usr/bin/bash.exe'
SAFE='safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt'
def run(name,args,cwd=WT,env=None):
 p=subprocess.run(args,cwd=cwd,env=env or ENV,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 s='COMMAND: '+json.dumps(args)+'\nCWD: '+str(cwd)+'\nEXIT_CODE: '+str(p.returncode)+'\nRAW OUTPUT:\n'+p.stdout
 (OUT/(name+'.txt')).write_text(s,encoding='utf-8')
 print(name,p.returncode,p.stdout[-450:],flush=True)
 return p
(OUT/'initial.txt').write_text('Before creating anything:\nHEAD 5f776a694b6369d3e0099545c4421da009081a86\nTREE 9eb9e957cfa4b1949640154e1fa7733e05cc0f91\nstatus --porcelain: ZERO BYTES; observed untracked paths NONE\nRepeated with command-scoped safe.directory=delivery path: HEAD_EXIT=0 TREE_EXIT=0 STATUS_EXIT=0\nInitial combined command exit=1 because rg unavailable; Get-ChildItem found no AGENTS.md.\n',encoding='utf-8')
(OUT/'external-base.txt').write_text(str(BASE),encoding='utf-8')
run('clone-plain',['git','clone','--no-hardlinks',str(WT),str(BASE/'plain')])
run('clone-safe',['git','-c',SAFE,'clone','--no-hardlinks',str(WT),str(BASE/'subject')])
C=BASE/'subject'
run('clone-identity',['git','rev-parse','HEAD','HEAD^{tree}'],C)
run('clone-status',['git','status','--porcelain'],C)
# Test scripts use their own external clones; safe exception remains process scoped.
e=ENV.copy(); e.update(LANE_WT=C.as_posix())
for name,file in [('harness-suite','run_harness_negative_tests.sh'),('gate-suite','run_gate_negative_tests.sh')]:
 e['NT_BASE']=(BASE/name).as_posix()
 run(name,[BASH,(C/REL/'verify/harness'/file).as_posix()],C,e)
