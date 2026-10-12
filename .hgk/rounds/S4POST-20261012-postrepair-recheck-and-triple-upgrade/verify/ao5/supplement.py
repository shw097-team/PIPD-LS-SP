import pathlib,subprocess,os,sys,json,shutil
BASE=pathlib.Path(sys.argv[1]); D=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt'); REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; E=D/REL/'verify/ao5'; C=BASE/'candidate2'; BASH=r'C:/Program Files/Git/usr/bin/bash.exe'
results=json.loads((E/'results.json').read_text())
def run(n,a,cwd=C,ee=None):
 p=subprocess.run([str(x) for x in a],cwd=cwd,env=ee,capture_output=True);o=p.stdout.decode('utf-8','replace');er=p.stderr.decode('utf-8','replace');results[n]={'command':[str(x) for x in a],'cwd':str(cwd),'exit':p.returncode,'stdout':o,'stderr':er};(E/(n+'.txt')).write_text('COMMAND: '+subprocess.list2cmdline([str(x) for x in a])+'\nCWD: '+str(cwd)+'\nEXIT_CODE: '+str(p.returncode)+'\nSTDOUT:\n'+o+'\nSTDERR:\n'+er,encoding='utf-8');print(n,'EXIT_CODE='+str(p.returncode));return p.returncode
ee=os.environ.copy();ee.pop('MSYS_NO_PATHCONV',None);ee.pop('MSYS2_ARG_CONV_EXCL',None)
k=int(ee.get('GIT_CONFIG_COUNT','0'));ee.update(GIT_CONFIG_COUNT=str(k+1));ee['GIT_CONFIG_KEY_'+str(k)]='core.longpaths';ee['GIT_CONFIG_VALUE_'+str(k)]='true'
ms=lambda p:'/tmp/'+pathlib.Path(p).relative_to(BASE.parent).as_posix()
run('path-diagnostic',[BASH,'-c','git clone --no-hardlinks "$1" "$2"; c=$?; echo CLONE_EXIT=$c; exit "$c"','ao5',C.as_posix(),ms(BASE/'path-diagnostic-clone')],BASE,dict(os.environ,MSYS_NO_PATHCONV='',MSYS2_ARG_CONV_EXCL=''))
for n,script in [('harness-tests-final','run_harness_negative_tests.sh'),('gate-tests-final','run_gate_negative_tests.sh')]:
 target=BASE.parent/('a5'+('h' if n.startswith('harness') else 'g')+BASE.name[-8:]);assert target.resolve().is_relative_to(BASE.parent.resolve()) and not target.exists()
 ev=ee.copy();ev.update(LANE_WT=C.as_posix(),NT_BASE=ms(target))
 run(n,[BASH,(C/REL/'verify/harness'/script).as_posix()],C,ev)
 run(n+'-case-logs',[sys.executable,'-c','import pathlib,sys\nfor p in pathlib.Path(sys.argv[1]).glob("logs/*.out"):\n print("FILE: "+str(p));print(p.read_text())',target],BASE)
# Independent masked receipt copy, with an external failure marker.
HEAD='c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d';run('receipt2-reset',['git','reset','--hard',HEAD]);run('receipt2-clean',['git','clean','-fd'])
ev=ee.copy();ev.update(LANE_WT=ms(C),TMPDIR=ms(BASE/'receipt2-logs'),CODEX_BIN=ms(BASE/'stub.sh'),MARKER=ms(BASE/'receipt2-child.marker'),FAILMARKER=ms(BASE/'receipt2-failure.marker'))
shell='cp() { case "$1" in *.exit) printf "EXIT_COPY_RETURN=23\\n" >> "$FAILMARKER"; return 23;; *) command cp "$@";; esac; }; export -f cp; bash "$@"'
run('receipt2',[BASH,'-c',shell,'ao5',(C/REL/'stage-b/run_lane.sh').as_posix(),'AO5_RECEIPT2','brief_nt.md','verify/ao5-probe'],C,ev)
run('receipt2-readback',[sys.executable,'-c','import pathlib,sys\nb=pathlib.Path(sys.argv[1]);s=pathlib.Path(sys.argv[2]);print((b/"receipt2-failure.marker").read_text());print("child_marker="+(b/"receipt2-child.marker").read_text());print("receipts="+repr([str(p) for p in s.glob("AO5_RECEIPT2_*.exit")]))',BASE,C/REL/'stage-b'])
run('receipt2-history',['git','log','-1','--format=%B','--name-status'])
for n,a in [('final-delivery-head',['git','rev-parse','HEAD']),('final-delivery-tree',['git','rev-parse','HEAD^{tree}']),('final-delivery-status',['git','status','--porcelain']),('final-delivery-index',['git','diff','--cached','--name-status']),('final-delivery-tracked',['git','diff','--name-status'])]:run(n,a,D)
(E/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for f in ['audit.py','adapt.py','supplement.py']:
 if (BASE/f).exists():shutil.copy2(BASE/f,E/f)
