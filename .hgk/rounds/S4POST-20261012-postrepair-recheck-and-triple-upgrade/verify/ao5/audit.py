import os, pathlib, subprocess, json, sys
D=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt')
BASE=pathlib.Path(sys.argv[1]); REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; E=D/REL/'verify/ao5'; E.mkdir(parents=True,exist_ok=True)
BASH=r'C:/Program Files/Git/usr/bin/bash.exe'; HEAD='c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d'
results={}
def run(name,args,cwd=D,env=None):
 p=subprocess.run([str(x) for x in args],cwd=str(cwd),env=env,capture_output=True)
 out=p.stdout.decode('utf-8','replace'); err=p.stderr.decode('utf-8','replace')
 rec={'command':[str(x) for x in args],'cwd':str(cwd),'exit':p.returncode,'stdout':out,'stderr':err}
 results[name]=rec
 (E/(name+'.txt')).write_text('COMMAND: '+subprocess.list2cmdline(rec['command'])+'\nCWD: '+str(cwd)+'\nEXIT_CODE: '+str(p.returncode)+'\nSTDOUT:\n'+out+'\nSTDERR:\n'+err,encoding='utf-8')
 print(name,'EXIT_CODE='+str(p.returncode),flush=True)
 return rec
# The first observation was made before this driver or evidence directory existed.
(E/'first-observation.txt').write_text('COMMAND: git rev-parse HEAD; git rev-parse \'HEAD^{tree}\'; git status --porcelain; Get-Location\nTOOL_EXIT_CODE: 0 (grouped PowerShell; individual native exits not separately captured)\nRAW OUTPUT:\nc93a41fb07ced91519bdb17e9cb1536bb1a5ac1d\nd8fe6480f5107bcb01a045783c36b2cd536662c3\n?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest\n\nPath\n----\nC:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\n',encoding='utf-8')
for n,a in [('delivery-head',['git','rev-parse','HEAD']),('delivery-tree',['git','rev-parse','HEAD^{tree}']),('delivery-status',['git','status','--porcelain']),('delivery-index',['git','diff','--cached','--name-status']),('delivery-tracked',['git','diff','--name-status'])]:run(n,a)
files=['verify/ao3/AO_VERDICT_STAGEB_R3.md','verify/ao4/AO_VERDICT_HANDOVER_R4.md','stage-b/run_lane.sh','stage-b/run_lanes_gated.sh','stage-b/ROUND_ASSIGNMENT.json','stage-b/OWNER_DECISION_MODEL_DEVIATION.md','verify/harness/run_harness_negative_tests.sh','verify/harness/run_gate_negative_tests.sh','verify/harness/HARNESS_DEFECT_LOG.md','verify/harness/QUALIFICATION_FINDINGS.md']
run('required-source-read',[sys.executable,'-c','import pathlib,sys\nfor x in sys.argv[1:]:\n print("FILE: "+x); print(pathlib.Path(x).read_text(encoding="utf-8"))',*[D/REL/x for x in files]])
C=BASE/'candidate2'
def msys(p):
 return '/tmp/'+pathlib.Path(p).relative_to(BASE.parent).as_posix()
run('clone',['git','-c','safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt','clone','--no-hardlinks','--no-checkout',D,C],BASE)
run('checkout',['git','checkout','--detach',HEAD],C)
run('clone-tree',['git','rev-parse','HEAD^{tree}'],C); run('clone-clean',['git','status','--porcelain'],C)
run('clone-email',['git','config','user.email','ao5@local.invalid'],C);run('clone-name',['git','config','user.name','AO5 external probe'],C)
L=C/REL/'stage-b/run_lane.sh'; G=C/REL/'stage-b/run_lanes_gated.sh'
ST=BASE/'stub.sh'
ST.write_text('''#!/usr/bin/env bash
printf 'CHILD_LAUNCHED\\n' >> "$MARKER"
printf 'STUB argv=%s\\n' "$*"
if [ "${MAKE_DIRT:-0}" = 1 ]; then printf dirt > "$LANE_WT/AO5_POST_DIRT"; fi
if [ "${DELETE_LOG:-0}" = 1 ]; then rm -f "$TMPDIR"/hgk-lanes/*.log; fi
exit "${CHILD_EXIT:-0}"
''',encoding='utf-8',newline='\n')
Q=BASE/'qual.sh'; Q.write_text('#!/usr/bin/env bash\nprintf "QUAL_LAUNCHED\\n" >> "$QMARKER"\nprintf "Q1_OK\\nQ2_OK\\nQUAL argv=%s\\n" "$*"\nexit 0\n',encoding='utf-8',newline='\n')
run('stub-executable',[BASH,'-c','chmod +x "$1" "$2"','ao5',ST.as_posix(),Q.as_posix()],BASE)
def reset(n):
 run(n+'-reset',['git','reset','--hard',HEAD],C)
 run(n+'-clean',['git','clean','-fd'],C)
def env(n,**extra):
 e=os.environ.copy();e.pop('MSYS_NO_PATHCONV',None);e.pop('MSYS2_ARG_CONV_EXCL',None)
 for k in ['ROUTE_STYLE','ROUTE_CATALOG','GATE_SKIP_QUALIFY','GATE_QUALIFY_ONLY','GATE_QUALIFY_RUNS','LANE_MODEL','LANE_PROVIDER','LANE_EFFORT','GIT_INDEX_FILE']:e.pop(k,None)
 e.update(LANE_WT=msys(C),TMPDIR=msys(BASE/(n+'-logs')),CODEX_BIN=msys(ST),MARKER=msys(BASE/(n+'-child.marker')),QMARKER=msys(BASE/(n+'-qual.marker')),GATE_BIN=msys(Q),GATE_PY=sys.executable.replace('\\','/'))
 e.update(extra);return e
def lane(n,ee=None,brief='brief_nt.md',out='verify/ao5-probe',shell=None):
 ee=ee or env(n)
 args=[BASH,L.as_posix(),'AO5_'+n.upper(),brief,out] if shell is None else [BASH,'-c',shell,'ao5',L.as_posix(),'AO5_'+n.upper(),brief,out]
 rec=run(n,args,C,ee)
 readback='import pathlib,json,sys; c=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); r=sys.argv[3]; n=sys.argv[4]; print(json.dumps({"child_marker":(b/(n+"-child.marker")).read_text() if (b/(n+"-child.marker")).exists() else None,"external_logs":[str(x) for x in (b/(n+"-logs")).rglob("*") if x.is_file()],"root_output_exists":(c/"verify/ao5-probe").exists(),"round_output_exists":(c/r/"verify/ao5-probe").exists(),"lane_exit_files":[str(x) for x in (c/r/"stage-b").glob("AO5_"+n.upper()+"_*.exit")]},indent=2))'
 run(n+'-inventory',[sys.executable,'-c',readback,C,BASE,REL,n],C);run(n+'-status',['git','status','--porcelain'],C);return rec
reset('dirty');(C/'AO5_ROOT_DIRT').write_text('dirt');lane('dirty')
reset('missing');lane('missing',brief='AO5_DOES_NOT_EXIST.md')
reset('post');lane('post',env('post',MAKE_DIRT='1'))
reset('output');lane('output')
reset('inside');lane('inside',env('inside',TMPDIR=msys(C/'tmp-inside')))
reset('child7');lane('child7',env('child7',CHILD_EXIT='7'))
reset('copyfail');lane('copyfail',env('copyfail',DELETE_LOG='1'));run('copyfail-message',['git','log','-1','--format=%B'],C)
reset('receiptfail');lane('receiptfail',shell='cp() { case "$1" in *.exit) echo "AO5_INJECTED_EXIT_COPY_FAILURE" >&2; return 23;; *) command cp "$@";; esac; }; export -f cp; bash "$@"')
reset('staged');(C/'AO5_OUTSIDE_STAGED').write_text('outside round staged fixture');run('staged-add',['git','add','AO5_OUTSIDE_STAGED'],C);run('staged-before',['git','status','--porcelain'],C);lane('staged');run('staged-history',['git','log','--format=commit %H%nsubject %s','--name-status',HEAD+'..HEAD'],C)
reset('qzero');ee=env('qzero',GATE_QUALIFY_RUNS='0');run('qzero',[BASH,G.as_posix(),'VERIFY','brief_nt.md'],C,ee)
run('qzero-markers',[sys.executable,'-c','import pathlib,sys\nfor x in sys.argv[1:]:\n p=pathlib.Path(x); print(str(p)+" exists="+str(p.exists())); print(p.read_text() if p.exists() else "")',BASE/'qzero-child.marker',BASE/'qzero-qual.marker'],C)
reset('route');ee=env('route');run('route',[BASH,G.as_posix(),'EXECUTE','brief_nt.md'],C,ee)
run('route-logs',[sys.executable,'-c','import pathlib,sys\nfor x in pathlib.Path(sys.argv[1]).rglob("*.log"):\n print("FILE: "+str(x));print(x.read_text())',BASE/'route-logs'],C)
# Requested harness checks ONLY, not product suite. Their recursive deletion is restricted
# to fresh, unique, verified system-temp descendants that do not yet exist.
for n,s in [('harness-tests','run_harness_negative_tests.sh'),('gate-tests','run_gate_negative_tests.sh')]:
 target=BASE/(n+'-retry'); assert target.resolve().is_relative_to(BASE.resolve()) and not target.exists()
 ee=env(n);ee.update(LANE_WT=C.as_posix(),NT_BASE=msys(target))
 reset(n)
 run(n,[BASH,(C/REL/'verify/harness'/s).as_posix()],C,ee)
 run(n+'-raw-case-logs',[sys.executable,'-c','import pathlib,sys\nfor x in pathlib.Path(sys.argv[1]).glob("logs/*.out"):\n print("FILE: "+str(x)); print(x.read_text())',target],BASE)
for n,a in [('delivery-end-head',['git','rev-parse','HEAD']),('delivery-end-tree',['git','rev-parse','HEAD^{tree}']),('delivery-end-status',['git','status','--porcelain']),('delivery-end-index',['git','diff','--cached','--name-status']),('delivery-end-tracked',['git','diff','--name-status'])]:run(n,a)
(E/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
(E/'temp-location.txt').write_text(str(BASE),encoding='utf-8')
print('EVIDENCE='+str(E));print('TEMP='+str(BASE))

