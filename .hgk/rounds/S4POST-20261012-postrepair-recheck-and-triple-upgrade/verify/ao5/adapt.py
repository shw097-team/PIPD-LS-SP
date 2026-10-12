import pathlib,sys,shutil
base=pathlib.Path(sys.argv[1]); e=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao5'); old=e/'host-initial';old.mkdir(exist_ok=True)
for x in list(e.iterdir()):
 if x.is_file():shutil.copy2(x,old/x.name)
p=base/'audit.py';s=p.read_text(encoding='utf-8-sig');s=s.replace("C=BASE/'candidate'","C=BASE/'candidate2'\ndef msys(p):\n return '/tmp/'+pathlib.Path(p).relative_to(BASE.parent).as_posix()")
s=s.replace("e=os.environ.copy()","e=os.environ.copy();e.pop('MSYS_NO_PATHCONV',None);e.pop('MSYS2_ARG_CONV_EXCL',None)")
s=s.replace("LANE_WT=C.as_posix(),TMPDIR=(BASE/(n+'-logs')).as_posix(),CODEX_BIN=ST.as_posix(),MARKER=(BASE/(n+'-child.marker')).as_posix(),QMARKER=(BASE/(n+'-qual.marker')).as_posix(),GATE_BIN=Q.as_posix()", "LANE_WT=msys(C),TMPDIR=msys(BASE/(n+'-logs')),CODEX_BIN=msys(ST),MARKER=msys(BASE/(n+'-child.marker')),QMARKER=msys(BASE/(n+'-qual.marker')),GATE_BIN=msys(Q)")
s=s.replace("TMPDIR=(C/'tmp-inside').as_posix()", "TMPDIR=msys(C/'tmp-inside')")
s=s.replace("target=BASE/n", "target=BASE/(n+'-retry')")
s=s.replace("NT_BASE=target.as_posix()", "NT_BASE=msys(target)")
s=s.replace("ee['MARKER'],ee['QMARKER']", "BASE/'qzero-child.marker',BASE/'qzero-qual.marker'")
p.write_text(s,encoding='utf-8')
