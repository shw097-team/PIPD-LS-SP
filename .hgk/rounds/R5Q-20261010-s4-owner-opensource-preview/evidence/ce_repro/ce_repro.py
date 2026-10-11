"""Independent re-derivation of CE-1 / CE-2 against the PUBLISHED wheel.

Everything here is built from the release asset itself; no local evidence file is trusted.
Run with:  python ce_repro.py
"""
import json
import pathlib
import subprocess
import sys

SC = pathlib.Path(__file__).resolve().parent
V = SC / "venv" / "Scripts" / "python.exe"
DL = SC / "dl"
WORK = SC / "mywork"
REPO = SC / "myrepo"

results = []


def run(label, argv, cwd, env=None):
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    results.append((label, p.returncode, p.stdout[:600], p.stderr[:300]))
    print(f"--- {label}  exit={p.returncode}")
    print("    stdout:", p.stdout[:400].replace("\n", " ")[:400])
    if p.stderr.strip():
        print("    stderr:", p.stderr[:200].replace("\n", " "))
    return p


def cli(*args, cwd=WORK, root=None):
    argv = [str(V), "-m", "pipd_ls_sp.cli"]
    if root:
        argv += ["--root", str(root)]
    argv += list(args)
    return argv


WORK.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- CE-1 ------
# A user who pip-installs the wheel and runs validate from their own directory.
# There is no schemas/ under that cwd; doctor in the SAME environment resolves INSTALLED.
print("\n########## CE-1: validate from a foreign cwd, no --root ##########")
run("CE-1 doctor (no --root)", cli("doctor", cwd=SC), cwd=SC)

# Build a bundle first so the failure is about schema resolution, not a missing file.
notes = DL / "PREVIEW_NOTES_v0.1.0-preview.1.md"
p = run("intake --source <published preview notes>",
        cli("intake", "--goal", "independent re-derivation of the published preview contract",
            "--source", str(notes), "--constraint", "design-only", cwd=WORK), cwd=WORK)
if p.returncode != 0:
    sys.exit("intake failed; cannot proceed")
intent = WORK / "intent.json"
intent.write_text(p.stdout, encoding="utf-8")

p = run("compile-pi", cli("compile-pi", "--intent", str(intent), cwd=WORK), cwd=WORK)
pi = WORK / "pi.json"
pi.write_text(p.stdout, encoding="utf-8")

p = run("bind-pd --repo-root <clean git repo>",
        cli("bind-pd", "--pi", str(pi), "--repo-root", str(REPO), cwd=WORK), cwd=WORK)
pd = WORK / "pd.json"
pd.write_text(p.stdout, encoding="utf-8")

p = run("compile-ecp", cli("compile-ecp", "--pd", str(pd), "--pi", str(pi), cwd=WORK), cwd=WORK)
ecp = WORK / "ecp.json"
ecp.write_text(p.stdout, encoding="utf-8")

p = run("compile-tqaep", cli("compile-tqaep", "--pi", str(pi), "--ecp", str(ecp),
                             "--maker", "preview-author",
                             "--checker", "independent-design-checker",
                             "--checker-receipt", "DESIGN_ONLY_NOT_RUNTIME_ACCEPTANCE",
                             cwd=WORK), cwd=WORK)
tqaep = WORK / "tqaep.json"
tqaep.write_text(p.stdout, encoding="utf-8")

# Bundle exactly as the compilers emitted it — no hand editing.
raw = WORK / "bundle_raw.json"
raw.write_text(json.dumps({k: json.loads(f.read_text(encoding="utf-8")) for k, f in
                           (("PI-PKG", pi), ("PD-PKG", pd), ("ECP", ecp), ("TQAEP", tqaep))},
                          indent=1), encoding="utf-8")

run("CE-1 validate --bundle (NO --root), cwd has no schemas/",
    cli("validate", "--bundle", str(raw), cwd=WORK), cwd=WORK)

# ---------------------------------------------------------------- CE-2 ------
# Same bundle, now pointing --root at the INSTALLED package so schema resolution succeeds.
print("\n########## CE-2: same raw bundle, --root at the installed package ##########")
site = SC / "venv" / "Lib" / "site-packages" / "pipd_ls_sp"
run("CE-2 validate --bundle <raw bundle> --root <installed pkg>",
    cli("validate", "--bundle", str(raw), cwd=WORK, root=site), cwd=WORK)

# Control: drop only the _profile_meta sidecar and re-validate.
b = json.loads(raw.read_text(encoding="utf-8"))
removed = b["PI-PKG"].pop("_profile_meta", None)
ctl = WORK / "bundle_control.json"
ctl.write_text(json.dumps(b, indent=1), encoding="utf-8")
run("CE-2 CONTROL validate --bundle <bundle minus _profile_meta> --root <installed pkg>",
    cli("validate", "--bundle", str(ctl), cwd=WORK, root=site), cwd=WORK)

print("\n########## summary ##########")
for label, code, out, err in results:
    print(f"  exit={code:<3} {label}")
pathlib.Path(SC / "ce_repro.json").write_text(
    json.dumps([{"label": l, "exit": c, "stdout": o, "stderr": e} for l, c, o, e in results],
               indent=1), encoding="utf-8")
print("\nremoved sidecar was:", json.dumps(removed)[:200])
