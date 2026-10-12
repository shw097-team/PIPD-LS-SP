import pathlib,subprocess,sys,json,re,shutil
B=pathlib.Path(sys.argv[1]);D=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt');R='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade';E=D/R/'verify/ao5';report=E/'AO_VERDICT_HANDOVER_R5.md';logs=[]
def capture(n,a):
 p=subprocess.run([str(x) for x in a],cwd=D,capture_output=True);o=p.stdout.decode('utf-8','replace');er=p.stderr.decode('utf-8','replace');t='COMMAND: '+subprocess.list2cmdline([str(x) for x in a])+'\nCWD: '+str(D)+'\nEXIT_CODE: '+str(p.returncode)+'\nSTDOUT:\n'+o+'\nSTDERR:\n'+er;(E/(n+'.txt')).write_text(t,encoding='utf-8');return p.returncode,t,o
code,t,o=capture('maker-documents-read',[sys.executable,'-c','import pathlib,sys\nfor x in sys.argv[1:]:\n print("FILE: "+x);print(pathlib.Path(x).read_text(encoding="utf-8"))',D/R/'verify/harness/HARNESS_DEFECT_LOG.md',D/R/'verify/harness/QUALIFICATION_FINDINGS.md']);assert code==0
addition='\n## Verbatim maker-document readback\n\nThe unsupported-claim inventory above refers to these original assertions; they are quoted as claims, not accepted as facts.\n\n```text\n'+t+'\n```\n'
for n,args in [('report-end-head',['git','rev-parse','HEAD']),('report-end-tree',['git','rev-parse','HEAD^{tree}']),('report-end-status',['git','status','--porcelain']),('report-end-index',['git','diff','--cached','--name-status']),('report-end-tracked',['git','diff','--name-status'])]:
 c,t,o=capture(n,args);assert c==0
 if n.endswith('head'):assert o.strip()=='c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d'
 if n.endswith('tree'):assert o.strip()=='d8fe6480f5107bcb01a045783c36b2cd536662c3'
 if n.endswith('index') or n.endswith('tracked'):assert not o.strip()
 if n.endswith('status'):assert set(o.splitlines())=={'?? '+R+'/stage-b/AO5_20261012T130513Z.manifest','?? '+R+'/verify/ao5/'}
 logs.append(t)
addition+='\n## Post-report delivery readback\n\nThese observations were collected after report creation.\n\n'+''.join('```text\n'+t+'\n```\n\n' for t in logs)
with report.open('a',encoding='utf-8') as f:f.write(addition)
shutil.copy2(B/'write_report.py',E/'write_report.py');shutil.copy2(B/'finalize.py',E/'finalize.py')
s=report.read_text();res=json.loads((E/'results.json').read_text());assert 'RESULT pass=15 fail=0' in res['harness-tests-final']['stdout'];assert 'RESULT pass=19 fail=0' in res['gate-tests-final']['stdout'];assert res['harness-tests-final']['exit']==res['gate-tests-final']['exit']==0
assert all(res[n]['exit']==v for n,v in [('dirty',2),('missing',3),('post',5),('output',0),('inside',3),('child7',7),('copyfail',4),('receipt2',0),('statusfail',0),('qzero',0)])
assert s.count('```')%2==0
for name in re.findall(r'Evidence: `([^`]+\.txt)`',s):assert (E/name).is_file(),name
checks='EXIT_CODE: 0\nReport fences balanced; cited raw evidence files present; required probe exits match recorded results; test counts verified; delivery HEAD/tree unchanged; tracked/index diffs empty; status contains only pre-existing manifest plus allowed officer evidence.\n'
(E/'report-validation.txt').write_text(checks,encoding='utf-8');print(checks)
