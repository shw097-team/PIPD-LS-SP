"""FAR: can an external acceptance officer now accept the pushed branch?

Clones the pushed branch into a clean directory (no local refs, no round scratch), then runs what an
external verifier would run, and records raw results. Nothing here writes to the product repo.

Usage: python ops/external_acceptance_dryrun.py
"""

from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

ROUND = pathlib.Path(__file__).resolve().parents[1]
SCRATCH = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch"
)
CLONE = SCRATCH / "r5p-external-clone"
OUT = ROUND / "evidence" / "EXTERNAL_ACCEPTANCE_DRYRUN.json"
REPO = "https://github.com/shw097-team/PIPD-LS-SP.git"
BRANCH = "r5p-post-challenge-repair"
ATTESTED_COMMIT = "194f1774e8e852f954d141c48389a74b0f0e302a"
ATTESTED_TREE = "b1ec0abf4799fdc917aaa23dc75885b302407ee5"
PY = sys.executable

results: dict = {"schema": "PIPD-R5P-EXTERNAL-DRYRUN/1", "as_of": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "repo": REPO, "branch": BRANCH, "clone": str(CLONE), "checks": []}


def run(name: str, cmd: list[str], cwd: pathlib.Path, timeout: int = 900) -> dict:
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        rc, out, err = "TIMEOUT", (exc.stdout or ""), f"timeout after {timeout}s"
    rec = {"name": name, "cmd": cmd, "cwd": str(cwd), "exit": rc, "seconds": round(time.time() - t0, 1),
           "stdout_tail": (out or "")[-1200:], "stderr_tail": (err or "")[-600:]}
    results["checks"].append(rec)
    print(f"[{name}] exit={rc} ({rec['seconds']}s)", flush=True)
    return rec


# 1. clean clone
if CLONE.exists():
    shutil.rmtree(CLONE, ignore_errors=True)
run("clone", ["git", "clone", "--quiet", "--branch", BRANCH, "--single-branch", REPO, str(CLONE)], SCRATCH, 900)

if not (CLONE / ".git").exists():
    results["verdict"] = "CLONE_FAILED"
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    raise SystemExit(1)

head = run("rev-parse", ["git", "rev-parse", "HEAD", "HEAD^{tree}"], CLONE, 60)
results["clone_head"] = head["stdout_tail"].split()

# 2. what evidence can the officer see without the round directory?
tracked = run("evidence_census", ["git", "ls-files"], CLONE, 120)
files = [line for line in tracked["stdout_tail"].splitlines() if line]
results["tracked_file_count"] = len(files)
results["round_evidence_in_repo"] = {
    "hgk_rounds_r5p_present": any("R5P-20261010" in f for f in files),
    "uat_runner_present": [f for f in files if f.endswith("uat_matrix.py")],
    "ao_verdict_files": [f for f in files if "AO_VERDICT" in f],
}
results["checks"][-1]["stdout_tail"] = f"{len(files)} tracked paths (full list not stored)"

# 3. the suite an officer would run
env = dict(os.environ, PYTHONPATH=str(CLONE / "src"))
t0 = time.time()
p = subprocess.run([PY, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                   cwd=str(CLONE), capture_output=True, text=True, env=env, timeout=1800)
tail = (p.stdout + p.stderr)[-800:]
results["checks"].append({"name": "full_suite_clean_clone", "cmd": [PY, "-B", "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                          "cwd": str(CLONE), "exit": p.returncode, "seconds": round(time.time() - t0, 1),
                          "summary": [l for l in tail.splitlines() if l.startswith(("Ran ", "OK", "FAILED", "ERROR"))][-4:],
                          "failures": [l for l in (p.stdout + p.stderr).splitlines() if l.startswith(("FAIL: ", "ERROR: "))],
                          "skips_named": [l for l in (p.stdout + p.stderr).splitlines() if "skipped" in l.lower()][-8:]})
print("[suite]", p.returncode, results["checks"][-1]["summary"], flush=True)

# 4. the publication gates
run("publication_check_current", [PY, "tools/build_publication_manifest.py", "--check", "--current"], CLONE, 900)
run("attestation_verify_r5p", [PY, "tools/publication_attestation.py", "--verify", "--out",
                               ".hgk/ao/pub/PUBLICATION_SUBJECT_ATTESTATION_R5P_POSTCHALLENGE.json",
                               "--expect-commit", ATTESTED_COMMIT, "--expect-tree", ATTESTED_TREE], CLONE, 600)
run("perf_budget_check", [PY, "-B", "tools/perf_budget.py", "--check"], CLONE, 600)

# 5. the user-facing path: install the shipped wheel into a fresh venv and run doctor
venv = SCRATCH / "r5p-external-venv"
if venv.exists():
    shutil.rmtree(venv, ignore_errors=True)
run("venv_create", [PY, "-m", "venv", str(venv)], SCRATCH, 600)
vpy = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
run("wheel_install", [str(vpy), "-m", "pip", "install", "--quiet", "--disable-pip-version-check",
                      str(CLONE / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl")], SCRATCH, 900)
work = SCRATCH / "r5p-external-doctor"; work.mkdir(parents=True, exist_ok=True)
run("doctor_as_installed_user", [str(vpy), "-m", "pipd_ls_sp.cli", "--root", str(work), "doctor"], work, 600)

blocking = [c["name"] for c in results["checks"] if c.get("exit") not in (0, None)]
results["non_zero_checks"] = blocking
results["verdict"] = "EXTERNAL_ACCEPTANCE_READY" if not blocking else "NOT_READY"
OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"verdict": results["verdict"], "non_zero": blocking,
                  "hgk_r5p_in_repo": results["round_evidence_in_repo"]}, ensure_ascii=False, indent=1))
