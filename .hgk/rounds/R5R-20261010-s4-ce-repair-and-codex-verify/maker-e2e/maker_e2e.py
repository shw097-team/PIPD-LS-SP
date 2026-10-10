"""R5R maker-side end-to-end probe (CE-1 / CE-2), run against a REAL wheel install.

Maker-side only: this is the PLAN's own check before the round is handed to the independent
CODEX CLI checker. It must exercise the installed distribution, from a cwd that has no
`schemas/` directory and with no `--root` argument, so CE-1 is tested for real.
"""

import json
import os
import pathlib
import shutil
import subprocess
import sys

ROUND = pathlib.Path(__file__).resolve().parents[1]
WORK = ROUND / "maker-e2e"
WHEEL = pathlib.Path(
    "C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt/dist/pipd_ls_sp-0.1.0-py3-none-any.whl")
SCRATCH = pathlib.Path(os.environ["TMPDIR"]) / "r5r-maker-e2e"
UV = shutil.which("uv") or "uv"

log_lines = []


def log(msg=""):
    print(msg, flush=True)
    log_lines.append(str(msg))


def run(cmd, cwd, env=None, label=""):
    e = dict(os.environ)
    e.pop("PYTHONPATH", None)
    e.pop("HERMES_HOME", None)
    e["PYTHONUTF8"] = "1"
    if env:
        e.update(env)
    p = subprocess.run(cmd, cwd=str(cwd), env=e, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    log(f"$ {' '.join(str(c) for c in cmd)}   (cwd={cwd})")
    log(f"  exit={p.returncode}")
    if p.stdout.strip():
        log("  stdout: " + p.stdout.strip()[:1500])
    if p.stderr.strip():
        log("  stderr: " + p.stderr.strip()[:800])
    return p


log(f"wheel   : {WHEEL}")
log(f"exists  : {WHEEL.is_file()}")
log(f"sha256  : {__import__('hashlib').sha256(WHEEL.read_bytes()).hexdigest()}")
log()

# ---------------------------------------------------------------- clean venv
if SCRATCH.exists():
    shutil.rmtree(SCRATCH, ignore_errors=True)
(VENV := SCRATCH / "venv").parent.mkdir(parents=True, exist_ok=True)
run([UV, "venv", str(VENV), "--python", "3.11"], cwd=SCRATCH, label="venv")
PY = VENV / "Scripts" / "python.exe"
PIPD = VENV / "Scripts" / "pipd.exe"
run([UV, "pip", "install", "--python", str(PY), str(WHEEL)], cwd=SCRATCH)
run([PY, "-c", "import pipd_ls_sp,sys;print('import ok', pipd_ls_sp.__file__)"], cwd=SCRATCH)

# ---------------------------------------------------------------- cwd with NO schemas/
RUN = SCRATCH / "run"
RUN.mkdir(parents=True, exist_ok=True)
log()
log(f"run dir : {RUN}")
log(f"has schemas/ ? {(RUN / 'schemas').exists()}   (must be False for CE-1)")

# a scratch git repo for bind-pd
REPO = SCRATCH / "repo"
REPO.mkdir(parents=True, exist_ok=True)
run(["git", "init", "-q"], cwd=REPO)
(REPO / "README.md").write_text("# scratch repo for bind-pd\n", encoding="utf-8")
run(["git", "add", "-A"], cwd=REPO)
run(["git", "-c", "user.email=r5r@local", "-c", "user.name=r5r", "commit", "-q", "-m", "init"], cwd=REPO)
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True,
                      text=True).stdout.strip()
log(f"scratch repo head: {head}")

# ---------------------------------------------------------------- CE-1: doctor
log()
log("=== 1. doctor (from the schemas-less cwd, no --root) ===")
run([str(PIPD), "doctor"], cwd=RUN)

# ---------------------------------------------------------------- chain
log()
log("=== 2. chain ===")
run([str(PIPD), "init"], cwd=RUN)

SRC = RUN / "source_clause.md"
SRC.write_text("# R5R maker E2E source clause\n\n"
               "The installed distribution must expose doctor, intake, compile-pi, bind-pd,\n"
               "compile-ecp, compile-tqaep and validate, and validate must reach a verdict\n"
               "without any schemas/ directory in the working directory.\n", encoding="utf-8")
p = run([str(PIPD), "intake", "--goal",
         "R5R maker E2E: prove the installed distribution runs the full design chain",
         "--source", str(SRC)], cwd=RUN, label="intake")
intent = WORK / "intent.json"
try:
    intent.write_text(json.dumps(json.loads(p.stdout), ensure_ascii=False, indent=1),
                      encoding="utf-8")
    log(f"intent card written: {intent}")
except Exception:
    intent = None
    log("intake did not emit a JSON card on stdout")


def emit(name, argv, cwd=RUN):
    """Run a chain step; return (exit, parsed-json-or-None)."""
    p = run([str(PIPD)] + argv, cwd=cwd, label=name)
    try:
        return p.returncode, json.loads(p.stdout)
    except Exception:
        return p.returncode, None


if intent is not None:
    rc, pi = emit("compile-pi", ["compile-pi", "--intent", str(intent)])
    if isinstance(pi, dict):
        (WORK / "pi.json").write_text(json.dumps(pi, ensure_ascii=False, indent=1), encoding="utf-8")
        rc, pd = emit("bind-pd", ["bind-pd", "--pi", str(WORK / "pi.json"),
                                 "--repo-root", str(REPO), "--head", head])
        if isinstance(pd, dict):
            (WORK / "pd.json").write_text(json.dumps(pd, ensure_ascii=False, indent=1), encoding="utf-8")
            rc, ecp = emit("compile-ecp", ["compile-ecp", "--pd", str(WORK / "pd.json"),
                                           "--pi", str(WORK / "pi.json")])
            if isinstance(ecp, dict):
                (WORK / "ecp.json").write_text(json.dumps(ecp, ensure_ascii=False, indent=1),
                                               encoding="utf-8")
                rc, tq = emit("compile-tqaep", ["compile-tqaep", "--pi", str(WORK / "pi.json"),
                                                "--ecp", str(WORK / "ecp.json"),
                                                "--maker", "R5R-E2E-MAKER-SMOKE",
                                                "--checker", "R5R-E2E-SMOKE-CHECKER",
                                                "--checker-receipt",
                                                "E2E-SMOKE-PLACEHOLDER-NOT-INDEPENDENT-VERIFICATION"])
                if isinstance(tq, dict):
                    (WORK / "tqaep.json").write_text(json.dumps(tq, ensure_ascii=False, indent=1),
                                                     encoding="utf-8")

# ---------------------------------------------------------------- CE-2: raw-stdout bundle
log()
log("=== 3. CE-2: bundle assembled from the compilers' own stdout, unedited ===")
members = {}
for name in ("pi", "pd", "ecp", "tqaep"):
    f = WORK / f"{name}.json"
    if f.is_file():
        members[name] = json.loads(f.read_text(encoding="utf-8"))
        log(f"  {name}: keys={sorted(members[name].keys())[:6]}"
            f"  _profile_meta present={'_profile_meta' in members[name]}")

BUNDLE = {"PI-PKG": members.get("pi"), "PD-PKG": members.get("pd"),
          "ECP": members.get("ecp"), "TQAEP": members.get("tqaep")}
BUNDLE = {k: v for k, v in BUNDLE.items() if isinstance(v, dict)}
(WORK / "bundle_raw.json").write_text(json.dumps(BUNDLE, ensure_ascii=False, indent=1),
                                      encoding="utf-8")
log(f"  bundle contracts: {sorted(BUNDLE)}")
log(f"  PI-PKG still carries _profile_meta: {'_profile_meta' in (BUNDLE.get('PI-PKG') or {})}")

p = run([str(PIPD), "validate", "--bundle", str(WORK / "bundle_raw.json")], cwd=RUN, label="validate")
verdict = None
try:
    verdict = json.loads(p.stdout)
except Exception:
    pass
if isinstance(verdict, dict):
    log(f"  VERDICT={verdict.get('verdict')}  checked={verdict.get('checked')}  "
        f"findings={verdict.get('findings')}")
    log(f"  schema_source={json.dumps(verdict.get('schema_source'), ensure_ascii=False)}")

(WORK / "maker_e2e_transcript.txt").write_text("\n".join(log_lines), encoding="utf-8")
print("\nwrote", WORK / "maker_e2e_transcript.txt")
