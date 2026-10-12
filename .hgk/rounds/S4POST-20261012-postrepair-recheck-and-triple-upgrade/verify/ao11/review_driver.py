import os,sys,json,hashlib,tempfile,subprocess,pathlib,datetime
ROOT=pathlib.Path.cwd(); REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; OUT=ROOT/REL/'verify/ao11'
SKILL=pathlib.Path('C:/Users/user/.agents/skills/fabric-external-independent-challenge-reviewer')
ENV=os.environ.copy()
for k in list(ENV):
 if k.startswith(('LANE_','GATE_','ROUTE_','CODEX_','STUB_','FO_','NT_','BASH_FUNC_')) or k in ('BASH_ENV','ENV','MSYS_NO_PATHCONV','MSYS2_ARG_CONV_EXCL','TMPDIR'): ENV.pop(k,None)
ENV.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0='*',PYTHONDONTWRITEBYTECODE='1')
BASH='C:/Program Files/Git/usr/bin/bash.exe'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def record(name,args,cwd=None,extra=None):
 e=ENV.copy();e.update(extra or {})
 p=subprocess.run([str(x) for x in args],cwd=cwd or ROOT,env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 raw=p.stdout.decode('utf-8',errors='replace')
 result={'command':[str(x) for x in args],'cwd':str(cwd or ROOT),'environment_overrides':extra or {},'exit_code':p.returncode,'raw_output':raw}
 (OUT/(name+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(name,'exit='+str(p.returncode));print(raw[:2500]);return p.returncode,raw
if sys.argv[1]=='freeze':
 TEMP=pathlib.Path(tempfile.mkdtemp(prefix='ao11-')); (OUT/'temp-location.txt').write_text(str(TEMP))
 old=json.loads((OUT/'EXTERNAL_CHALLENGE_INTAKE.json').read_text());(OUT/'intake-at-dispatch.json').write_text(json.dumps(old,indent=2))
 _,head=record('freeze-head',['git','rev-parse','HEAD']);head=head.strip()
 _,tree=record('freeze-tree',['git','rev-parse',head+'^{tree}'])
 record('freeze-status',['git','status','--porcelain=v1'])
 code,_=record('freeze-archive',['git','archive','--format=tar','--output='+str(TEMP/'candidate.tar'),head]);assert code==0
 code,_=record('freeze-clone',['git','clone','--no-hardlinks','--no-checkout',str(ROOT),str(TEMP/'subject')]);assert code==0
 code,_=record('freeze-checkout',['git','checkout','--detach',head],TEMP/'subject');assert code==0
 dist=ROOT/'dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip';manifest=ROOT/REL/'evidence/EVIDENCE_RETURN_PACK.json'
 freeze={'commit':head,'tree':tree.strip(),'archive_sha256':sha(TEMP/'candidate.tar'),'distribution_sha256':sha(dist),'manifest_sha256':sha(manifest),'temp':str(TEMP),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (OUT/'freeze.json').write_text(json.dumps(freeze,indent=2))
 old['candidate']={'commit':head,'package_sha256':freeze['archive_sha256'],'distribution_digest':freeze['distribution_sha256']};old['evidence_manifest_sha256']=freeze['manifest_sha256'];old['freeze_method']={'package':'git archive --format=tar '+head,'tree':tree.strip(),'temp':str(TEMP),'distribution_semantics':'observed historical ZIP; current Stage-B association unproven'}
 (OUT/'EXTERNAL_CHALLENGE_INTAKE.json').write_text(json.dumps(old,indent=2),encoding='utf-8')
 inventory=[]
 for p in [ROOT/REL/x for x in ['stage-b/ROUND_ASSIGNMENT.json','stage-b/OWNER_DECISION_MODEL_DEVIATION.md','stage-b/run_lane.sh','stage-b/run_lanes_gated.sh','stage-b/run_checker_lane.sh','verify/harness/HARNESS_DEFECT_LOG.md','verify/harness/QUALIFICATION_FINDINGS.md','verify/harness/LAUNCHER_TEST_RESULTS.txt','verify/harness/GATE_NEGATIVE_TEST_RESULTS.txt','verify/harness/CHECKER_FAILOVER_TEST_RESULTS.txt','evidence/EVIDENCE_RETURN_PACK.json','01_subject/FROZEN_SUBJECT.json']]:
  relative=p.relative_to(ROOT).as_posix(); cp=TEMP/'subject'/relative
  inventory.append({'path':relative,'sha256':sha(p),'clone_sha256':sha(cp),'normalized_equal':p.read_bytes().replace(b'\r\n',b'\n')==cp.read_bytes().replace(b'\r\n',b'\n')})
 (OUT/'source-inventory.json').write_text(json.dumps(inventory,indent=2))
 record('skill-self-test',[sys.executable,str(SKILL/'scripts/verify_review_bundle.py'),'--self-test'])
 record('skill-unit-tests',[sys.executable,'-m','unittest','tests/test_verify_review_bundle.py'],SKILL)
 print(json.dumps(freeze,indent=2))
TEMP=pathlib.Path((OUT/'temp-location.txt').read_text());F=json.loads((OUT/'freeze.json').read_text());SUB=TEMP/'subject'
def native(p):return pathlib.Path(p).as_posix()
def fixture(name):
 c=TEMP/name
 rc,_=record(name+'-clone',['git','-c','core.autocrlf=false','clone','--no-hardlinks','--quiet',str(SUB),str(c)]);assert rc==0
 rc,_=record(name+'-checkout',['git','checkout','--detach',F['commit']],c);assert rc==0
 s=c/REL/'stage-b';(s/'challenge-brief.md').write_text('Independent deterministic control-flow fixture. No model call.\n')
 logs=TEMP/(name+'-logs');logs.mkdir()
 return c,s,{'LANE_WT':native(c),'TMPDIR':native(logs),'CODEX_BIN':native(TEMP/'worker-stub.sh'),'GATE_BIN':native(TEMP/'worker-stub.sh'),'GATE_QUALIFY_ONLY':'1','GATE_QUALIFY_RUNS':'1','ROUTE_CATALOG':native(TEMP/'dummy-catalog.json')}
def gate(name,role='VERIFY',extra=None,full=False):
 c,s,e=fixture(name);e.update(extra or {})
 if full:e['GATE_QUALIFY_ONLY']='0'
 rc,raw=record(name,[BASH,str(s/'run_lanes_gated.sh'),role,'challenge-brief.md'],c,e)
 return c,s,e,rc,raw
if sys.argv[1]=='cases':
 (TEMP/'dummy-catalog.json').write_text('{}')
 (TEMP/'worker-stub.sh').write_text('#!/usr/bin/env bash\nprintf "STUB argv: %s\\n" "$*"\necho "OpenAI Codex v-stub"\necho "exec one succeeded in 1ms:"\necho "exec two succeeded in 1ms:"\necho Q1_OK\necho Q2_OK\nexit 0\n',newline='\n')
 for name,role,ex in [('G14a','EXECUTE',{'LANE_MODEL':'.*'}),('G14b','VERIFY',{'LANE_MODEL':'opencode-go/deepseek-v4-flash'}),('G14c','VERIFY',{'LANE_PROVIDER':'foreign-provider'}),('G14d','VERIFY',{'LANE_EFFORT':'high'})]:gate(name,role,ex)
 gate('G14e','EXECUTE',{'LANE_MODEL':'opencode-go/deepseek-v4-flash','LANE_EFFORT':'none'},full=True)
 gate('qualification-stub-positive','VERIFY')
 c,s,e=fixture('junction');target=c/'junction-target';target.mkdir();link=TEMP/'external-junction'
 rc,raw=record('junction-create',['powershell','-NoProfile','-Command',"New-Item -ItemType Junction -Path '"+str(link)+"' -Target '"+str(target)+"' | Select-Object FullName,LinkType,Target"]);assert rc==0
 (link/'landing-probe.txt').write_text('AO11 physical junction positive control\n');assert (target/'landing-probe.txt').read_text()=='AO11 physical junction positive control\n'
 (OUT/'junction-readback.json').write_text(json.dumps({'link':str(link),'target':str(target),'realpath':os.path.realpath(link),'probe_physical_target_exists':(target/'landing-probe.txt').exists(),'probe_sha256':sha(target/'landing-probe.txt')},indent=2))
 e['TMPDIR']=native(link)
 record('G15-gate-junction',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-child-junction',[BASH,str(s/'run_lane.sh'),'AOJ','challenge-brief.md','verify/challenge'],c,e)
 (OUT/'junction-after.json').write_text(json.dumps({'gate_log_files':[str(p) for p in (target/'hgk-lanes').glob('*.log')],'log_directory_created':(target/'hgk-lanes').exists()},indent=2))
 # Native path deliberately maps to the confirmed junction; a resolver failure must not admit a lane.
 e['GATE_PY']=native(TEMP/'resolver-fail.sh');e['LANE_PY']=e['GATE_PY']
 (TEMP/'resolver-fail.sh').write_text('#!/usr/bin/env bash\nif [ "$1" = "-" ]; then exit 97; fi\nexec python "$@"\n',newline='\n')
 record('G15-resolver-failure-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 # Child requires clean preflight; remove only the diagnostic probe in its disposable clone, commit fixture.
 (target/'landing-probe.txt').unlink()
 record('junction-fixture-commit',['git','add','-A'],c)
 record('junction-fixture-commit2',['git','-c','user.email=challenge@local.invalid','-c','user.name=challenger','commit','-qm','external fixture only'],c)
 record('G15-resolver-failure-child',[BASH,str(s/'run_lane.sh'),'AOJR','challenge-brief.md','verify/challenge'],c,e)
 for name,msg in [('A4','Provider error 400: [invalid_request_error] reasoning_content missing; Service at capacity.'),('A5','ERROR: quota exhausted, usage limit reached.'),('protocol-HTTP400','HTTP 400: malformed payload; quota remaining 90 percent.')]:
  c,s,e=fixture(name);e.pop('GATE_QUALIFY_ONLY');e['FO_STATE']=native(TEMP/(name+'-state'));e['FO_MSG']=msg;e['CODEX_BIN']=native(TEMP/'checker-stub.sh')
  (TEMP/'checker-stub.sh').write_text('#!/usr/bin/env bash\nif [ ! -f "$FO_STATE" ]; then : > "$FO_STATE"; echo "$FO_MSG"; exit 1; fi\necho "STUB backup success"\nexit 0\n',newline='\n')
  record(name,[BASH,str(s/'run_checker_lane.sh'),'AO'+name.replace('-',''),'challenge-brief.md','verify/challenge'],c,e)
  record(name+'-status',['git','status','--porcelain=v1'],c)
  record(name+'-record-tracked',['git','ls-files','--error-unmatch',REL+'/stage-b/CHECKER_FAILOVER_AO'+name.replace('-','')+'.md'],c)
  record(name+'-record-commit',['git','log','-1','--format=%H %s','--',REL+'/stage-b/CHECKER_FAILOVER_AO'+name.replace('-','')+'.md'],c)
 c,s,e=fixture('role-omitted');e.update(LANE_MODEL='unassigned-model',LANE_PROVIDER='foreign-provider',LANE_EFFORT='ultra',ROUTE_STYLE='openai');e.pop('GATE_QUALIFY_ONLY')
 record('role-omitted',[BASH,str(s/'run_lane.sh'),'AOOMIT','challenge-brief.md','verify/challenge'],c,e)
def shellpath(p):
 n=native(p);return '/'+n[0].lower()+n[2:]
def fixture2(name):
 c,s,e=fixture(name);e.update(LANE_WT=shellpath(c),TMPDIR=shellpath(TEMP/(name+'-logs')),CODEX_BIN=shellpath(TEMP/'worker-stub.sh'),GATE_BIN=shellpath(TEMP/'worker-stub.sh'))
 return c,s,e
if sys.argv[1]=='retry':
 c,s,e=fixture2('G14e-retry');e.update(LANE_MODEL='opencode-go/deepseek-v4-flash',LANE_EFFORT='none',GATE_QUALIFY_ONLY='0')
 record('G14e-retry',[BASH,str(s/'run_lanes_gated.sh'),'EXECUTE','challenge-brief.md'],c,e)
 c,s,e=fixture2('junction-logdir');target=c/'junction-target';target.mkdir();parent=TEMP/'junction-parent';parent.mkdir();link=parent/'hgk-lanes'
 rc,_=record('junction-logdir-create',['powershell','-NoProfile','-Command',"New-Item -ItemType Junction -Path '"+str(link)+"' -Target '"+str(target)+"' | Format-List FullName,LinkType,Target"]);assert rc==0
 (link/'landing-probe.txt').write_text('physical log destination control\n')
 (OUT/'junction-logdir-readback.json').write_text(json.dumps({'junction':str(link),'os_realpath':os.path.realpath(link),'target':str(target),'physical_probe_exists':(target/'landing-probe.txt').exists(),'physical_probe_sha256':sha(target/'landing-probe.txt')},indent=2))
 (target/'landing-probe.txt').unlink();e['TMPDIR']=shellpath(parent)
 record('G15-logdir-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-logdir-child',[BASH,str(s/'run_lane.sh'),'AOJLOG','challenge-brief.md','verify/challenge'],c,e)
 e.update(GATE_PY=shellpath(TEMP/'resolver-fail.sh'),LANE_PY=shellpath(TEMP/'resolver-fail.sh'))
 record('G15-logdir-resolver-failure-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-logdir-resolver-failure-child',[BASH,str(s/'run_lane.sh'),'AOJFAIL','challenge-brief.md','verify/challenge'],c,e)
 (OUT/'junction-logdir-after.json').write_text(json.dumps({'logs_physically_inside':[str(p) for p in target.glob('*.log')],'hashes':{p.name:sha(p) for p in target.glob('*.log')}},indent=2))
 for name,msg in [('A4-retry','Provider error 400: [invalid_request_error] reasoning_content missing; Service at capacity.'),('A5-retry','ERROR: quota exhausted, usage limit reached.'),('protocol-HTTP400-retry','HTTP 400: malformed payload; quota remaining 90 percent.')]:
  c,s,e=fixture2(name);e.pop('GATE_QUALIFY_ONLY');e.update(FO_STATE=shellpath(TEMP/(name+'-state')),FO_MSG=msg,CODEX_BIN=shellpath(TEMP/'checker-stub.sh'))
  label='AO'+name.replace('-','')
  record(name,[BASH,str(s/'run_checker_lane.sh'),label,'challenge-brief.md','verify/challenge'],c,e)
  record(name+'-status',['git','status','--porcelain=v1'],c)
  record(name+'-record-tracked',['git','ls-files','--error-unmatch',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
  record(name+'-record-commit',['git','log','-1','--format=%H %s','--',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
 c,s,e=fixture2('role-omitted-retry');e.update(LANE_MODEL='unassigned-model',LANE_PROVIDER='foreign-provider',LANE_EFFORT='ultra',ROUTE_STYLE='openai');e.pop('GATE_QUALIFY_ONLY')
 record('role-omitted-retry',[BASH,str(s/'run_lane.sh'),'AOOMIT','challenge-brief.md','verify/challenge'],c,e)
def fixture3(name):
 c,s,e=fixture(name)
 (c/REL/'verify/gate').mkdir(parents=True,exist_ok=True);(c/REL/'verify/challenge').mkdir(parents=True,exist_ok=True)
 (TEMP/(name+'-logs')/'hgk-lanes').mkdir()
 return c,s,e
if sys.argv[1]=='native-retry':
 c,s,e=fixture3('G14e-native');e.update(LANE_MODEL='opencode-go/deepseek-v4-flash',LANE_EFFORT='none',GATE_QUALIFY_ONLY='0')
 record('G14e-native',[BASH,str(s/'run_lanes_gated.sh'),'EXECUTE','challenge-brief.md'],c,e)
 c,s,e=fixture3('junction-native');target=c/'junction-target';target.mkdir();parent=TEMP/'junction-native-parent';parent.mkdir();link=parent/'hgk-lanes'
 rc,_=record('junction-native-create',['powershell','-NoProfile','-Command',"New-Item -ItemType Junction -Path '"+str(link)+"' -Target '"+str(target)+"' | Format-List FullName,LinkType,Target"]);assert rc==0
 (link/'landing-probe.txt').write_text('physical log destination control\n');assert(target/'landing-probe.txt').exists()
 (OUT/'junction-native-readback.json').write_text(json.dumps({'junction':str(link),'os_realpath':os.path.realpath(link),'target':str(target),'physical_probe_exists':(target/'landing-probe.txt').exists(),'physical_probe_sha256':sha(target/'landing-probe.txt')},indent=2))
 (target/'landing-probe.txt').unlink();e['TMPDIR']=native(parent)
 record('G15-native-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-native-child',[BASH,str(s/'run_lane.sh'),'AOJN','challenge-brief.md','verify/challenge'],c,e)
 e.update(GATE_PY=native(TEMP/'resolver-fail.sh'),LANE_PY=native(TEMP/'resolver-fail.sh'))
 record('G15-native-resolver-failure-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-native-resolver-failure-child',[BASH,str(s/'run_lane.sh'),'AOJNF','challenge-brief.md','verify/challenge'],c,e)
 (OUT/'junction-native-after.json').write_text(json.dumps({'logs_physically_inside':[str(p) for p in target.glob('*.log')],'hashes':{p.name:sha(p) for p in target.glob('*.log')}},indent=2))
 for name,msg in [('A4-native','Provider error 400: [invalid_request_error] reasoning_content missing; Service at capacity.'),('A5-native','ERROR: quota exhausted, usage limit reached.'),('protocol-HTTP400-native','HTTP 400: malformed payload; quota remaining 90 percent.')]:
  c,s,e=fixture3(name);e.pop('GATE_QUALIFY_ONLY');e.update(FO_STATE=native(TEMP/(name+'-state')),FO_MSG=msg,CODEX_BIN=native(TEMP/'checker-stub.sh'))
  label='AO'+name.replace('-','')
  record(name,[BASH,str(s/'run_checker_lane.sh'),label,'challenge-brief.md','verify/challenge'],c,e)
  record(name+'-status',['git','status','--porcelain=v1'],c)
  record(name+'-record-tracked',['git','ls-files','--error-unmatch',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
  record(name+'-record-commit',['git','log','-1','--format=%H %s','--',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
 c,s,e=fixture3('role-omitted-native');e.update(LANE_MODEL='unassigned-model',LANE_PROVIDER='foreign-provider',LANE_EFFORT='ultra',ROUTE_STYLE='openai');e.pop('GATE_QUALIFY_ONLY')
 record('role-omitted-native',[BASH,str(s/'run_lane.sh'),'AOOMIT','challenge-brief.md','verify/challenge'],c,e)
def transport():
 shim=TEMP/'path-adapters';shim.mkdir(exist_ok=True)
 for name,binpath in [('mkdir','/usr/bin/mkdir'),('cp','/usr/bin/cp')]:
  (shim/name).write_text('#!/usr/bin/env bash\na=(); for x in "$@"; do case "$x" in [A-Za-z]:/*) x="$(cygpath -u "$x")" ;; esac; a+=("$x"); done\nexec '+binpath+' "${a[@]}"\n',newline='\n')
 return {'PATH':native(shim)+';'+ENV['PATH']}
if sys.argv[1]=='adapted':
 ADAPT=transport()
 # Re-run prepared native fixtures without modifying candidate scripts. The path adapters only
 # translate native C:/ arguments for MSYS mkdir/cp; Git/Python continue receiving native paths.
 for name,role in [('G14e-native','EXECUTE')]:
  c=TEMP/name;s=c/REL/'stage-b';e=json.loads((OUT/(name+'.json')).read_text())['environment_overrides'];e.update(ADAPT)
  record('G14e-adapted',[BASH,str(s/'run_lanes_gated.sh'),role,'challenge-brief.md'],c,e)
 for name,msg in [('A4-adapted','Provider error 400: [invalid_request_error] reasoning_content missing; Service at capacity.'),('A5-adapted','ERROR: quota exhausted, usage limit reached.'),('protocol-HTTP400-adapted','HTTP 400: malformed payload; quota remaining 90 percent.')]:
  c,s,e=fixture3(name);e.pop('GATE_QUALIFY_ONLY');e.update(ADAPT);e.update(FO_STATE=native(TEMP/(name+'-state')),FO_MSG=msg,CODEX_BIN=native(TEMP/'checker-stub.sh'))
  label='AO'+name.replace('-','')
  record(name,[BASH,str(s/'run_checker_lane.sh'),label,'challenge-brief.md','verify/challenge'],c,e)
  record(name+'-status',['git','status','--porcelain=v1'],c)
  record(name+'-record-tracked',['git','ls-files','--error-unmatch',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
  record(name+'-record-commit',['git','log','-1','--format=%H %s','--',REL+'/stage-b/CHECKER_FAILOVER_'+label+'.md'],c)
 c,s,e=fixture3('role-omitted-adapted');e.update(ADAPT);e.update(LANE_MODEL='unassigned-model',LANE_PROVIDER='foreign-provider',LANE_EFFORT='ultra',ROUTE_STYLE='openai');e.pop('GATE_QUALIFY_ONLY')
 record('role-omitted-adapted',[BASH,str(s/'run_lane.sh'),'AOOMIT','challenge-brief.md','verify/challenge'],c,e)
 # Re-run the exact log-directory junction with transport adapter (new lane labels).
 c=TEMP/'junction-native';s=c/REL/'stage-b';e=json.loads((OUT/'G15-native-gate.json').read_text())['environment_overrides'];e.update(ADAPT)
 record('G15-adapted-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-adapted-child',[BASH,str(s/'run_lane.sh'),'AOJAD','challenge-brief.md','verify/challenge'],c,e)
 e.update(GATE_PY=native(TEMP/'resolver-fail.sh'),LANE_PY=native(TEMP/'resolver-fail.sh'))
 record('G15-adapted-resolver-failure-gate',[BASH,str(s/'run_lanes_gated.sh'),'VERIFY','challenge-brief.md'],c,e)
 record('G15-adapted-resolver-failure-child',[BASH,str(s/'run_lane.sh'),'AOJADF','challenge-brief.md','verify/challenge'],c,e)
 target=c/'junction-target';(OUT/'junction-adapted-after.json').write_text(json.dumps({'logs_physically_inside':[str(p) for p in target.glob('*.log')],'hashes':{p.name:sha(p) for p in target.glob('*.log')}},indent=2))
