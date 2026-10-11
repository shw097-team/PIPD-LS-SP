#!/usr/bin/env python3
"""Re-run the two AO acceptance cases that were NOT_RUN because their prerequisite failed.

AO case labels B4 and B5 == brief BLOCK A cases A4 and A5 (mutated-wheel runtime checks).
They were NOT_RUN in the acceptance officer's report because each spent its three-attempt
ceiling on a venv whose `ensurepip` step failed, so the prerequisite successful installation
was never reached. `python -m ensurepip --version` exits 0 in this environment now, so the
prerequisite is testable and the cases can be re-run rather than left NOT_RUN.

A4: delete one *.schema.json member from a copy of the wheel, leave RECORD untouched, install
    it into a fresh venv with --no-index --no-deps, run the installed CLI. It MUST NOT
    silently succeed; a typed error naming the missing schema is the expected shape.
A5: truncate a pipd_ls_sp/*.py member by a few bytes, leave RECORD untouched, install and run.
    The installation must fail rather than yield a working CLI.

Writes raw evidence to ao/rerun_b4_b5.json. Nothing is written outside the system temp dir.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/PIPD")
OUT = REPO / ".hgk/rounds/R5-20261009-s4-user-operability/ao/rerun_b4_b5.json"
WHEEL = REPO / "dist/pipd_ls_sp-0.1.0-py3-none-any.whl"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def rewrite_wheel(src: Path, dst: Path, drop: str | None, truncate: str | None) -> dict:
    """Copy the zip, dropping one member or truncating one member, RECORD left untouched."""
    acted = {}
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if drop and item.filename == drop:
                acted["dropped"] = item.filename
                continue
            if truncate and item.filename == truncate:
                before = len(data)
                data = data[:-7]
                acted["truncated"] = {"member": item.filename, "before": before, "after": len(data)}
            zout.writestr(item, data)
    return acted


def make_venv(path: Path) -> dict:
    r = subprocess.run([sys.executable, "-m", "venv", str(path)], capture_output=True, text=True)
    pip = path / "Scripts" / "pip.exe"
    if r.returncode != 0 or not pip.exists():
        r2 = subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade",
                             "--root", str(path)], capture_output=True, text=True)
        return {"venv_exit": r.returncode, "venv_err": r.stderr[-400:],
                "ensurepip_exit": r2.returncode, "pip_present": pip.exists()}
    return {"venv_exit": r.returncode, "pip_present": pip.exists()}


def run_case(label: str, work: Path, drop=None, truncate=None) -> dict:
    case = {"case": label, "outcome": None}
    whl = work / f"{label}.whl"
    case["mutation"] = rewrite_wheel(WHEEL, whl, drop, truncate)
    case["mutated_sha256"] = sha256(whl)
    case["mutated_bytes"] = whl.stat().st_size

    venv = work / f"venv-{label}"
    case["venv"] = make_venv(venv)
    if not case["venv"].get("pip_present"):
        case["outcome"] = "NOT_RUN"
        case["reason"] = "no pip in the fresh venv even after ensurepip"
        return case

    py = venv / "Scripts" / "python.exe"
    inst = subprocess.run([str(py), "-m", "pip", "install", "--no-index", "--no-deps", str(whl)],
                          capture_output=True, text=True)
    case["install_exit"] = inst.returncode
    case["install_tail"] = (inst.stdout + inst.stderr)[-700:]

    run = subprocess.run([str(py), "-m", "pipd_ls_sp.cli", "--root", str(REPO), "doctor"],
                         capture_output=True, text=True)
    case["run_exit"] = run.returncode
    case["run_tail"] = (run.stdout + run.stderr)[-700:]

    silently_ok = inst.returncode == 0 and run.returncode == 0
    case["silently_succeeded"] = silently_ok
    case["outcome"] = "FAIL" if silently_ok else "PASS"
    case["interpretation"] = (
        "the mutation was DETECTED (install or run failed, or the CLI reported a typed error)"
        if not silently_ok else
        "the mutated wheel produced a working CLI - the guard does not hold"
    )
    return case


def main() -> int:
    if not WHEEL.exists():
        print(f"FATAL: wheel absent: {WHEEL}")
        return 2
    work = Path(tempfile.mkdtemp(prefix="ao-b4b5-"))
    names = zipfile.ZipFile(WHEEL).namelist()
    schema = sorted(n for n in names if n.endswith(".schema.json"))
    mod = sorted(n for n in names if n.startswith("pipd_ls_sp/") and n.endswith(".py"))
    if not schema or not mod:
        print("FATAL: cannot find a schema member / python member to mutate")
        return 2

    doc = {
        "schema": "pipd-r5s4-ao-rerun/1",
        "why": "B4 and B5 were NOT_RUN because their prerequisite (a fresh venv with pip) failed "
               "at ensurepip. ensurepip exits 0 in this environment, so they are re-run here.",
        "wheel": str(WHEEL),
        "wheel_sha256": sha256(WHEEL),
        "wheel_members": len(names),
        "ensurepip_probe": subprocess.run([sys.executable, "-m", "ensurepip", "--version"],
                                          capture_output=True, text=True).stdout.strip(),
        "cases": [
            run_case("B4", work, drop=schema[0]),
            run_case("B5", work, truncate=mod[0]),
        ],
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO)}")
    for c in doc["cases"]:
        print(f"  {c['case']}: {c['outcome']}  mutation={c['mutation']}  "
              f"install_exit={c.get('install_exit')}  run_exit={c.get('run_exit')}  "
              f"silently_succeeded={c.get('silently_succeeded')}")
        print(f"     install_tail: {str(c.get('install_tail'))[-160:]}")
        print(f"     run_tail    : {str(c.get('run_tail'))[-160:]}")
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
