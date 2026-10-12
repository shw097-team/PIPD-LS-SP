import pathlib, hashlib, re
src=(pathlib.Path.cwd()/'.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao8/probes.py').read_text()
exec(src.split('for name,file in')[0])
exec(src[src.index("STUB='''"):src.index("case('M1'")])
case('N-owner-trailing-control','sed -i "s/^authorizes:.*/authorizes: extra-model /" "$OWNER"\n'+gate('LANE_MODEL=extra-model'))
case('N-owner-effort-regex',lane('EFFREGEX',"LANE_ROLE=EXECUTE LANE_MODEL=opencode-go/deepseek-v4.1-flash LANE_EFFORT='.*' ROUTE_STYLE=catalog ROUTE_CATALOG=unused"))
case('N-route-address',lane('ADDRESS','LANE_ROLE=EXECUTE LANE_MODEL=opencode-go/deepseek-v4.1-flash LANE_EFFORT=high ROUTE_STYLE=catalog ROUTE_BASE_URL=http://127.0.0.1:9/v1 ROUTE_CATALOG=unassigned'))
case('N-prefix-tab','mkdir -p "prefix/$REL"; echo outside > "prefix/$REL/"$\'tab\\tname.txt\'; git add prefix; git diff --cached --name-only\n'+lane('TAB').replace('command git status','git log -3 --name-only --format=%s; command git status'))
case('N-failed-child-receipt',lane('FAILCHILD','STUB_EXIT=7').replace('command git status','cat "$S"/FAILCHILD_*.receipt; command git status'))
case('N-authorised-skip','printf "authorizes_skip_qualification: EXECUTE\\n" > "$S/GATE_SKIP_QUALIFY_ACK.md"\n'+gate('GATE_SKIP_QUALIFY=1').replace('command git status','cat "$S"/BRIEF_NT_A_*.receipt; command git status'))
# Attempt a real filesystem symlink; do not treat an MSYS emulated copy as one.
assert C.resolve().is_relative_to(BASE.resolve())
subprocess.run(['git','reset','--hard','5f776a694b6369d3e0099545c4421da009081a86'],cwd=C,env=ENV,stdout=subprocess.DEVNULL,check=True)
subprocess.run(['git','clean','-fd'],cwd=C,env=ENV,stdout=subprocess.DEVNULL,check=True)
owner=C/REL/'stage-b/OWNER_DECISION_MODEL_DEVIATION.md'; target=BASE/'linked-owner.md'
target.write_text('authorizes: linked-model\n',encoding='utf-8'); owner.unlink()
try:
 owner.symlink_to(target)
 (OUT/'symlink-setup.txt').write_text('COMMAND: pathlib.Path.symlink_to(external owner file)\nEXIT_CODE: 0\nRAW OUTPUT:\n'+str(owner)+' -> '+str(target)+'\n')
 script=PRE+'\n'+gate('LANE_MODEL=linked-model')+'\n'
 (OUT/'N-owner-symlink.sh').write_text(script,encoding='utf-8')
 run('N-owner-symlink',[BASH,(OUT/'N-owner-symlink.sh').as_posix()])
except OSError as e:
 (OUT/'symlink-setup.txt').write_text('COMMAND: pathlib.Path.symlink_to(external owner file)\nEXIT_CODE: setup exception; launcher NOT_EXECUTED\nRAW OUTPUT:\n'+str(e)+'\n',encoding='utf-8')
 print('SYMLINK_SETUP',str(e),flush=True)
# Retain exact inspected launcher/test bytes, with hashes; do not copy broad legacy logs.
files=['stage-b/run_lane.sh','stage-b/run_lanes_gated.sh','verify/harness/run_harness_negative_tests.sh','verify/harness/run_gate_negative_tests.sh']
snap=OUT/'source-snapshots'; snap.mkdir(exist_ok=True)
hashes=[]
for f in files:
 b=(WT/REL/f).read_bytes(); (snap/pathlib.Path(f).name).write_bytes(b)
 hashes.append(f+' SHA256='+hashlib.sha256(b).hexdigest())
(OUT/'source-hashes.txt').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
# Stub output only: tie M7 to writer argv and M1 to manifest byte equality.
for n in ['M1','M7','N-role-omitted','N-provider-override','N-route-address']:
 text=(OUT/(n+'.txt')).read_text()
 m=re.search(r'log=(/tmp/[^\s]+\.log)',text)
 if m:
  native=BASE/pathlib.PurePosixPath(m[1]).relative_to(P)
  run(n+'-worker-log',[BASH,'-c','cat "$1"','officer',m[1]])
  if n=='M1':
   ext=native.with_suffix('.manifest'); delivery=C/REL/'stage-b'/ext.name
   # Clone was reset between probes; use the committed copy captured by its commit from transcript.
   h=re.search(r'POSTFLIGHT:dirty=0 HEAD=([0-9a-f]+)',text).group(1)
   run('M1-manifest-readback',['git','show',h+':'+REL+'/stage-b/'+ext.name])
   run('M1-manifest-external',[BASH,'-c','cat "$1"','officer',m[1][:-4]+'.manifest'])
