import pathlib,subprocess,hashlib,json,os,sys
src=(pathlib.Path.cwd()/'.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao8/probes.py').read_text()
exec(src.split('for name,file in')[0])
exec(src[src.index("STUB='''"):src.index("case('M1'")])
case('M1-copy-failure','cp() { case "${@: -1}" in *.manifest) return 23;; *) command cp "$@";; esac; }; export -f cp\n'+lane('M1FAIL'))
case('M7-direct-mismatch',lane('M7FAIL','LANE_ROLE=EXECUTE LANE_MODEL=opencode-go/deepseek-v4.1-flash LANE_EFFORT=high ROUTE_STYLE=openai'))
# Reader override is demonstrated only against stubs in qualify-only mode.
fake=BASE/'reader.sh'
fake.write_text('''#!/usr/bin/env bash
case "$2" in
 *"print(r['model'],r['provider']"*) echo 'fake-model fake-provider fake-effort';;
 *"get('style'"*) echo openai;;
 *"get('catalog'"*) echo unused;;
 *"get('base_url'"*) echo http://127.0.0.1:9/v1;;
esac
exit 0
''',encoding='utf-8')
case('N-GATE-PY-override',f'chmod +x {P}/reader.sh\n'+gate(f'GATE_PY={P}/reader.sh GATE_QUALIFY_ONLY=1'))
safe='safe.directory='+WT.as_posix()
def delivery(name,args):
 p=subprocess.run(args,cwd=WT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 (OUT/(name+'.txt')).write_text('COMMAND: '+json.dumps(args)+'\nCWD: '+str(WT)+'\nEXIT_CODE: '+str(p.returncode)+'\nRAW OUTPUT:\n'+p.stdout,encoding='utf-8')
 print(name,p.returncode,p.stdout,flush=True)
 return p
delivery('delivery-end-head',['git','-c',safe,'rev-parse','HEAD','HEAD^{tree}'])
delivery('delivery-end-status',['git','-c',safe,'status','--porcelain'])
delivery('historical-AO7-receipt',['git','-c',safe,'show','5f776a694b6369d3e0099545c4421da009081a86:'+REL+'/stage-b/AO7_20261012T135739Z.receipt'])
rows=[]
for f in ['stage-b/run_lane.sh','stage-b/run_lanes_gated.sh','verify/harness/run_harness_negative_tests.sh','verify/harness/run_gate_negative_tests.sh']:
 b=subprocess.check_output(['git','-c',safe,'show','5f776a694b6369d3e0099545c4421da009081a86:'+REL+'/'+f],cwd=WT,env=ENV)
 snap=(OUT/'source-snapshots'/pathlib.Path(f).name).read_bytes()
 current=(WT/REL/f).read_bytes()
 rows.append(f+' initial_SHA256='+hashlib.sha256(b).hexdigest()+' snapshot_matches_initial='+str(b==snap)+' current_matches_initial='+str(b==current))
(OUT/'source-identity-check.txt').write_text('COMMAND: git show initial-HEAD:<each named source>; compare SHA256 and bytes with inspected snapshot and current file\nEXIT_CODE: 0\nRAW OUTPUT:\n'+'\n'.join(rows)+'\n',encoding='utf-8')
print('\n'.join(rows),flush=True)
