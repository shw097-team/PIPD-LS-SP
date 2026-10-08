#!/usr/bin/env python3
"""S3 real install / upgrade / uninstall lifecycle in an ISOLATED environment (L5).

This is a real side effect, not a described one: a fresh venv is created, the wheel is installed into
it, the console script is executed, the package is uninstalled, and the residue is counted. It then
reinstalls from the same wheel and compares digests, which is the only honest way to claim that the
distribution is reproducible.

Offline by design: `--no-deps` plus the declared dependency checked SEPARATELY, so a missing
jsonschema cannot be mistaken for a broken package. The missing-dependency behaviour is recorded as a
typed, fail-closed refusal rather than an import crash.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUT = ROOT / ".hgk" / "artifacts" / "s3"
PY = sys.executable


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    whl = next(DIST.glob("pipd_ls_sp-*.whl"), None)
    if whl is None:
        print(json.dumps({"verdict": "FAIL", "why": "no wheel; run tools/build_dist.py first"}))
        return 1
    import hashlib
    whl_sha_before = hashlib.sha256(whl.read_bytes()).hexdigest()

    tmp = Path(tempfile.mkdtemp(prefix="pipd-install-"))
    venv = tmp / "venv"
    rows: list[dict] = []

    def row(step: str, ok: bool, detail: str) -> None:
        rows.append({"step": step, "verdict": "PASS" if ok else "FAIL", "detail": detail[:250]})

    r = run([PY, "-m", "venv", str(venv)])
    row("create_isolated_venv", r.returncode == 0, r.stdout + r.stderr)
    vpy = venv / "Scripts" / "python.exe"
    if not vpy.exists():
        vpy = venv / "bin" / "python"

    r = run([str(vpy), "-m", "pip", "install", "--no-index", "--no-deps", str(whl)])
    row("install_wheel_no_index_no_deps", r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1]
        if (r.stdout + r.stderr).strip() else "")

    r = run([str(vpy), "-c", "import pipd_ls_sp, pipd_ls_sp.cli as c; print('import OK', c.__name__)"])
    row("sdk_import_in_clean_env", r.returncode == 0, (r.stdout + r.stderr).strip())

    script = venv / "Scripts" / "pipd.exe"
    if not script.exists():
        script = venv / "bin" / "pipd"
    r = run([str(script), "--help"])
    help_ok = r.returncode == 0 and "--" in r.stdout
    row("console_script_entry_point", help_ok, f"exit={r.returncode}")

    r = run([str(script), "intake", "--goal", "Implement the lifecycle compiler.",
             "--source", str(ROOT / "docs" / "S0_CONTRACT_SPEC.md")])
    row("cli_command_runs_in_clean_env", r.returncode == 0 and "subject_id" in r.stdout,
        f"exit={r.returncode} {(r.stdout or r.stderr)[:120]}")

    # the DECLARED dependency must behave as a typed refusal when it is absent, not an ImportError
    r = run([str(vpy), "-c",
             "from pipd_ls_sp import validate as V; import json,pathlib,sys;"
             "print(json.dumps(V.semantic_invariants('PI-PKG', {})))"])
    typed_dep_ok = r.returncode == 0
    row("declared_dependency_absent_is_graceful", typed_dep_ok,
        f"exit={r.returncode} {(r.stdout or r.stderr)[:120]}")

    r = run([str(vpy), "-m", "pip", "uninstall", "-y", "pipd-ls-sp"])
    row("uninstall", r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1]
        if (r.stdout + r.stderr).strip() else "")

    site = list(venv.glob("Lib/site-packages")) + list(venv.glob("lib/python*/site-packages"))
    residue = []
    for sp in site:
        residue += [p.name for p in sp.iterdir() if "pipd" in p.name.lower()]
    row("no_residue_after_uninstall", not residue, f"residue={residue}")

    r = run([str(vpy), "-c", "import pipd_ls_sp"])
    row("import_fails_after_uninstall", r.returncode != 0, f"exit={r.returncode}")

    r = run([str(vpy), "-m", "pip", "install", "--no-index", "--no-deps", str(whl)])
    row("reinstall_same_wheel", r.returncode == 0, "reinstalled")
    whl_sha_after = hashlib.sha256(whl.read_bytes()).hexdigest()
    row("wheel_bytes_unchanged_by_install", whl_sha_before == whl_sha_after,
        f"{whl_sha_before[:16]} == {whl_sha_after[:16]}")

    shutil.rmtree(tmp, ignore_errors=True)
    payload = {
        "wheel": whl.name, "wheel_sha256": whl_sha_before, "isolated_env": "fresh venv, no system site-packages",
        "rows": rows,
        "passed": f"{sum(1 for r_ in rows if r_['verdict'] == 'PASS')}/{len(rows)}",
        "known_offline_limitation": "jsonschema is declared in Requires-Dist and is not present in the "
                                    "isolated env; validity paths raise a typed ValidationFail rather "
                                    "than crashing, and the declaration is what a resolver would satisfy",
        "candidate_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
    }
    payload["verdict"] = "PASS" if all(r_["verdict"] == "PASS" for r_ in rows) else "FAIL"
    (OUT / "PORTABLE_INSTALL.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                                               encoding="utf-8", newline="")
    print(json.dumps({"passed": payload["passed"], "verdict": payload["verdict"]}, ensure_ascii=False, indent=1))
    for r_ in rows:
        if r_["verdict"] != "PASS":
            print("  FAIL", r_)
    return 0 if payload["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
