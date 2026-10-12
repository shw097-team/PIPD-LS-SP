import os,sys,pathlib,subprocess,json
WT=pathlib.Path.cwd(); REL='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; OUT=WT/REL/'verify/ao8'
BASE=pathlib.Path((OUT/'external-base.txt').read_text()); C=BASE/'subject'; P='/tmp/'+BASE.name
ENV=os.environ.copy()
for k in ['MSYS_NO_PATHCONV','MSYS2_ARG_CONV_EXCL','BASH_ENV','ENV']: ENV.pop(k,None)
ENV['PATH']='C:/Program Files/Git/usr/bin;C:/Program Files/Git/mingw64/bin;'+str(pathlib.Path(sys.executable).parent)+';'+ENV['PATH']
BASH='C:/Program Files/Git/usr/bin/bash.exe'
def run(name,args,env=ENV):
 p=subprocess.run(args,cwd=C,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
 (OUT/(name+'.txt')).write_text('COMMAND: '+json.dumps(args)+'\nCWD: '+str(C)+'\nEXIT_CODE: '+str(p.returncode)+'\nRAW OUTPUT:\n'+p.stdout,encoding='utf-8')
 print(name,p.returncode,p.stdout[-750:],flush=True); return p
for name,file in [('harness-retry','run_harness_negative_tests.sh'),('gate-retry','run_gate_negative_tests.sh')]:
 e=ENV.copy(); e.update(LANE_WT=P+'/subject',NT_BASE=P+'/'+name)
 run(name,[BASH,(C/REL/'verify/harness'/file).as_posix()],e)
STUB='''#!/usr/bin/env bash
echo "stub argv=$*"
echo 'OpenAI Codex vSTUB'
echo 'exec Q1 succeeded in 1ms:'
echo 'exec Q2 succeeded in 1ms:'
echo Q1_OK; echo Q2_OK
if [ "${MAKE_DIR:-0}" = 1 ]; then mkdir -p "$LANE_WT/$REL/stage-b/${CASELANE}_${LANE_TOKEN}.receipt"; fi
exit "${STUB_EXIT:-0}"
'''
(BASE/'stub.sh').write_text(STUB,encoding='utf-8')
(BASE/'sentinels.sh').write_text('#!/usr/bin/env bash\necho Q1_OK; echo Q2_OK\n',encoding='utf-8')
PRE=f'''unset MSYS_NO_PATHCONV MSYS2_ARG_CONV_EXCL BASH_ENV ENV
export REL='{REL}' LANE_WT='{P}/subject' TMPDIR='{P}/logs' CODEX_BIN='{P}/stub.sh' GATE_BIN='{P}/stub.sh' GATE_QUALIFY_RUNS=1
S="$LANE_WT/$REL/stage-b"; L="$S/run_lane.sh"; G="$S/run_lanes_gated.sh"; OWNER="$S/OWNER_DECISION_MODEL_DEVIATION.md"
mkdir -p "$TMPDIR"; chmod +x "$CODEX_BIN" '{P}/sentinels.sh'
'''
def case(name,body):
 # Guard cleanup/reset targets: only the retained external subject clone.
 assert C.resolve().is_relative_to(BASE.resolve()) and not C.resolve().is_relative_to(WT.resolve())
 subprocess.run(['git','reset','--hard','5f776a694b6369d3e0099545c4421da009081a86'],cwd=C,env=ENV,stdout=subprocess.DEVNULL,check=True)
 subprocess.run(['git','clean','-fd'],cwd=C,env=ENV,stdout=subprocess.DEVNULL,check=True)
 hook=C/'.git/hooks/post-commit'
 if hook.exists(): hook.unlink()
 script=PRE+'\n'+body+'\n'
 (OUT/(name+'.sh')).write_text(script,encoding='utf-8')
 run(name,[BASH,(OUT/(name+'.sh')).as_posix()])
def lane(name='PROBE',extra=''):
 return f'{extra} bash "$L" {name} brief_nt.md verify/a8; c=$?; echo SUBJECT_EXIT=$c; command git status --porcelain; exit "$c"'
def gate(extra='',role='EXECUTE'):
 return f'{extra} bash "$G" {role} brief_nt_a.md; c=$?; echo SUBJECT_EXIT=$c; command git status --porcelain; exit "$c"'
case('M1',lane('M1') .replace('command git status','ls "$S"/M1_*.manifest; command git status'))
case('M2','mkdir -p "$LANE_WT/Xhgk/rounds/${REL##*/}"; echo outside > "$LANE_WT/Xhgk/rounds/${REL##*/}/outside.txt"; git add Xhgk\n'+lane('M2'))
case('M3','git() { if [ "${1:-}" = diff ] && [ "${3:-}" = --name-only ]; then return 128; fi; command git "$@"; }; export -f git\n'+lane('M3'))
case('M4','''cat > .git/hooks/post-commit <<'EOF'
#!/usr/bin/env bash
case "$(git log -1 --pretty=%s)" in *receipt*) echo dirt > M4_DIRT.txt;; esac
EOF
chmod +x .git/hooks/post-commit
'''+lane('M4'))
case('M5',lane('M5','MAKE_DIR=1 CASELANE=M5 LANE_TOKEN=fixed'))
case('M6','''cat > .git/hooks/post-commit <<'EOF'
#!/usr/bin/env bash
for f in .hgk/rounds/*/stage-b/BRIEF_NT_A_*.receipt; do printf 'child_exit=99\ntoken=wrong\nroute=wrong\n' > "$f"; done
EOF
chmod +x .git/hooks/post-commit
'''+gate())
startup=BASE/'startup.sh'; startup.write_text('case "$0" in *run_lane.sh) export ROUTE_STYLE=openai;; esac\n',encoding='utf-8')
case('M7',gate(f'BASH_ENV={P}/startup.sh'))
case('M8',gate('GATE_SKIP_QUALIFY=1'))
case('M9',gate(f'GATE_BIN={P}/sentinels.sh'))
case('N-prefix-substring','mkdir -p "prefix/$REL"; echo outside > "prefix/$REL/outside.txt"; git add prefix\n'+lane('PREFIX').replace('command git status','git log -3 --name-only --format=%s; command git status'))
case('N-prefix-rename','mkdir -p "prefix/$REL"; git mv README.md "prefix/$REL/moved.md"\n'+lane('RENAME'))
case('N-prefix-quoted','mkdir -p "prefix/$REL"; echo outside > "prefix/$REL/space name.txt"; git add prefix\n'+lane('QUOTED'))
case('N-owner-regex',gate("LANE_MODEL='.*'"))
case('N-owner-second-line','printf "\\nauthorizes: extra-model\\n" >> "$OWNER"\n'+gate('LANE_MODEL=extra-model'))
case('N-owner-trailing-space','sed -i "s/^authorizes:.*/authorizes: extra-model /" "$OWNER"\n'+gate("LANE_MODEL='extra-model '"))
case('N-owner-other-role',gate('LANE_MODEL=opencode-go/deepseek-v4-flash',role='VERIFY'))
case('N-empty-receipt','''cat > .git/hooks/post-commit <<'EOF'
#!/usr/bin/env bash
case "$(git log -1 --pretty=%s)" in *receipt*) for f in .hgk/rounds/*/stage-b/BRIEF_NT_A_*.receipt; do : > "$f"; done;; esac
EOF
chmod +x .git/hooks/post-commit
'''+gate())
case('N-forged-valid-fields','''cat > .git/hooks/post-commit <<'EOF'
#!/usr/bin/env bash
case "$(git log -1 --pretty=%s)" in *receipt*)
for f in .hgk/rounds/*/stage-b/BRIEF_NT_A_*.receipt; do
sed -i 's/^model=.*/model=wrong-model/;s/^qualified=.*/qualified=no/' "$f"
printf 'child_exit=99\\nroute=wrong\\n' >> "$f"
git add "$f"
done
git -c core.hooksPath=/dev/null -c user.email=a8@local.invalid -c user.name=a8 commit -q -m forged
;; esac
EOF
chmod +x .git/hooks/post-commit
'''+gate().replace('command git status','cat "$S"/BRIEF_NT_A_*.receipt; command git status'))
case('N-after-final-status','''git() {
if [ "${1:-}" = rev-parse ] && [ "${2:-}" = --short ] && ls "$S"/LATE_*.receipt >/dev/null 2>&1; then echo dirt > LATE_DIRT.txt; fi
command git "$@"
}; export -f git
'''+lane('LATE'))
case('N-role-omitted',lane('UNASSIGNED','LANE_MODEL=unassigned LANE_EFFORT=unassigned LANE_PROVIDER=unassigned LANE_SANDBOX=danger-full-access'))
case('N-provider-override',gate('LANE_PROVIDER=unassigned',role='VERIFY'))
case('N-TMPDIR-inside',lane('TMPINSIDE','TMPDIR="$LANE_WT/tmp-inside"'))
case('N-TMPDIR-gate-only',gate('TMPDIR="$LANE_WT/tmp-inside" GATE_QUALIFY_ONLY=1'))
case('N-qualification-forged',gate('GATE_QUALIFY_ONLY=1'))
case('N-startup-initial','''printf 'export GATE_QUALIFY_ONLY=1\\n' > "$TMPDIR/startup-initial.sh"
'''+gate('BASH_ENV="$TMPDIR/startup-initial.sh"'))
