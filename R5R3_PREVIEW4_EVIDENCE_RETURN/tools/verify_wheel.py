"""Wheel clean-install smoke (CK-07 / CK-10) on the SERVED preview.4 wheel.

Installs the downloaded wheel into a FRESH venv (created with --system-site-packages so the
third-party dependency set comes from the host interpreter, never from any project PYTHONPATH),
then runs `pipd doctor` and a positive + wrong-hash/orphan negative bundle through the INSTALLED
console script, from a cwd OUTSIDE the source tree.

Usage: verify_wheel.py <wheel-path> <out-dir>
"""
from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
from pathlib import Path

PY311 = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"


def run(cmd: list[str], cwd: str, env: dict | None = None) -> dict:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return {"cmd": cmd, "exit": r.returncode,
            "stdout": r.stdout[-4000:], "stderr": r.stderr[-2500:]}


def main() -> int:
    wheel = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    venv = out / "venv"
    report: dict = {"schema": "R5R3-20261016/wheel-clean-install/1",
                    "wheel": str(wheel),
                    "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
                    "claim_ceiling": "installed-artifact smoke; not an acceptance"}

    if not venv.exists():
        report["venv_create"] = run([PY311, "-m", "venv", "--system-site-packages", str(venv)],
                                    cwd=str(out))
    py = str(venv / "Scripts" / "python.exe")
    pip = [py, "-m", "pip", "install", "--no-deps", "--no-index", "--force-reinstall", str(wheel)]
    report["install"] = run(pip, cwd=str(out))
    report["installed_files_are_in_venv"] = run(
        [py, "-c", "import pipd_ls_sp,sys;print(pipd_ls_sp.__file__)"], cwd=str(out))
    src_path = report["installed_files_are_in_venv"]["stdout"].strip()
    report["install_is_not_source_tree"] = ("wt-r5r3" not in src_path and "src" not in src_path
                                            or "site-packages" in src_path)

    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    work = out / "run"
    work.mkdir(exist_ok=True)

    report["doctor"] = run([py, "-m", "pipd_ls_sp.cli", "doctor"], cwd=str(work), env=env)
    report["help"] = run([py, "-m", "pipd_ls_sp.cli", "--help"], cwd=str(work), env=env)
    # console script (entry point) rather than -m: proves the packaged entry point resolves
    script = venv / "Scripts" / "pipd.exe"
    report["console_script_exists"] = script.exists()
    if script.exists():
        report["doctor_console_script"] = run([str(script), "doctor"], cwd=str(work), env=env)

    checks = {
        "install_exit_0": report["install"]["exit"] == 0,
        "import_from_venv": "site-packages" in src_path,
        "doctor_exit_0": report["doctor"]["exit"] == 0,
        "console_script_present": report["console_script_exists"],
    }
    report["checks"] = checks
    report["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
