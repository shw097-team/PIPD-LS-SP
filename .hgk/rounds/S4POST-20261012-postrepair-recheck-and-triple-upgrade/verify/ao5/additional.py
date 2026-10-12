import pathlib,os,subprocess,json,sys,shutil
B=pathlib.Path(sys.argv[1]);D=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt');R='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade';E=D/R/'verify/ao5';C=B/'candidate2';bh=r'C:/Program Files/Git/usr/bin/bash.exe';res=json.loads((E/'results.json').read_text());ev=os.environ.copy();ev.pop('MSYS_NO_PATHCONV',None);ev.pop('MSYS2_ARG_CONV_EXCL',None);ms=lambda p:'/tmp/'+pathlib.Path(p).relative_to(B.parent).as_posix()
def run(n,args,cwd=C,env=None):
 p=subprocess.run([str(a) for a in args],cwd=cwd,env=env,capture_output=True);o=p.stdout.decode('utf-8','replace');er=p.stderr.decode('utf-8','replace');res[n]={'command':[str(a) for a in args],'cwd':str(cwd),'exit':p.returncode,'stdout':o,'stderr':er};(E/(n+'.txt')).write_text('COMMAND: '+subprocess.list2cmdline([str(a) for a in args])+'\nCWD: '+str(cwd)+'\nEXIT_CODE: '+str(p.returncode)+'\nSTDOUT:\n'+o+'\nSTDERR:\n'+er,encoding='utf-8');print(n,p.returncode)
run('output2-reset',['git','reset','--hard','c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d']);run('output2-clean',['git','clean','-fd'])
cmd='import pathlib,json,sys; c=pathlib.Path(sys.argv[1]);print(json.dumps(sorted(p.name for p in c.iterdir() if p.is_dir())))'
run('output2-root-before',[sys.executable,'-c',cmd,C]);ee=ev.copy();ee.update(LANE_WT=ms(C),TMPDIR=ms(B/'output2-logs'),CODEX_BIN=ms(B/'stub.sh'),MARKER=ms(B/'output2-child.marker'))
run('output2',[bh,(C/R/'stage-b/run_lane.sh').as_posix(),'AO5_OUTPUT2','brief_nt.md','verify/ao5-probe'],env=ee);run('output2-root-after',[sys.executable,'-c',cmd,C])
run('statusfail-reset',['git','reset','--hard','c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d']);run('statusfail-clean',['git','clean','-fd'])
ee=ev.copy();ee.update(LANE_WT=ms(C),TMPDIR=ms(B/'statusfail-logs'),CODEX_BIN=ms(B/'stub.sh'),MARKER=ms(B/'statusfail-child.marker'),FAILMARKER=ms(B/'statusfail-failure.marker'))
shell='git() { if [ "$1" = status ]; then printf "GIT_STATUS_RETURN=128\\n" >> "$FAILMARKER"; return 128; fi; command git "$@"; }; export -f git; bash "$@"'
run('statusfail',[bh,'-c',shell,'ao5',(C/R/'stage-b/run_lane.sh').as_posix(),'AO5_STATUSFAIL','brief_nt.md','verify/ao5-probe'],env=ee)
run('statusfail-readback',[sys.executable,'-c','import pathlib,sys;b=pathlib.Path(sys.argv[1]);print((b/"statusfail-failure.marker").read_text());print((b/"statusfail-child.marker").read_text())',B])
# Store exact tested stub source and reproducible environment definition (no secrets).
run('stub-source',[sys.executable,'-c','import pathlib,sys\nfor x in sys.argv[1:]:\n print("FILE: "+x);print(pathlib.Path(x).read_text())',B/'stub.sh',B/'qual.sh'])
run('environment-contract',[sys.executable,'-c','import os,sys;print("INITIAL_MSYS_NO_PATHCONV="+os.environ.get("MSYS_NO_PATHCONV","<unset>"));print("INITIAL_MSYS2_ARG_CONV_EXCL="+os.environ.get("MSYS2_ARG_CONV_EXCL","<unset>"));print("TEMP="+os.environ["TEMP"]);print("PYTHON="+sys.executable)'])
(E/'results.json').write_text(json.dumps(res,indent=2),encoding='utf-8');shutil.copy2(B/'additional.py',E/'additional.py')
