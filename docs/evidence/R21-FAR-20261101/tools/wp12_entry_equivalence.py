"""WP-FHS-12 entry equivalence, measured with the environment recorded beside every byte count.

Why this exists (AO finding WP12-RS-06/07/08/09): the previous lab claimed four entries were
byte-identical on `status`, but (a) the maker's own raw file held two different 741 B shas, (b) the
product venv forwarder pins HERMES_HOME, and (c) `--version` gains a 22-byte suffix when git is on
PATH. So the matrix below pins and records both knobs and never compares a number to a literal.

Matrix: 4 entries x {HERMES_HOME unset, HERMES_HOME=D:\\Hermes-Recovery\\live22}
                 x {git on PATH, git off PATH}
Only the PATH entry and the entry under test are compared for identity; the product forwarder is
reported separately because it is a different object by construction.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp12"
GIT_CMD = r"C:\Program Files\Git\cmd"

ENTRIES = {
    "A_product_venv_cmd": r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\hermes.cmd",
    "X_recovery_exe": r"D:\Hermes-Recovery\live22\bin\hermes.exe",
    "E_recovery_extless": r"D:\Hermes-Recovery\live22\bin\hermes",
    "P_recovery_cmd": r"D:\Hermes-Recovery\live22\bin\hermes.cmd",
}
PROBES = (["--version"], ["status"], ["--print-runtime-command"])


def run(cmd, env):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, timeout=120, env=env)
    return {"rc": r.returncode, "ms": round((time.time() - t0) * 1000, 1),
            "out_b": len(r.stdout), "out_sha": hashlib.sha256(r.stdout).hexdigest(),
            "err_b": len(r.stderr),
            "err_tail": (r.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-1][:160] if r.stderr else "",
            "out_head": (r.stdout or b"").decode("utf-8", "replace").strip()[:120]}


def base_env(home: str | None, with_git: bool) -> dict:
    keep = ("SystemRoot", "SYSTEMROOT", "windir", "COMSPEC", "PATHEXT", "TEMP", "TMP",
            "USERPROFILE", "APPDATA", "LOCALAPPDATA", "PROGRAMDATA", "NUMBER_OF_PROCESSORS")
    env = {k: os.environ[k] for k in keep if k in os.environ}
    parts = [r"D:\Hermes-Recovery\live22\bin", r"C:\Windows\system32", r"C:\Windows"]
    if with_git:
        parts.append(GIT_CMD)
    env["PATH"] = ";".join(parts)
    if home:
        env["HERMES_HOME"] = home
    return env


rows = {}
for home_tag, home in (("HERMES_HOME_unset", None), ("HERMES_HOME_recovery", r"D:\Hermes-Recovery\live22")):
    for git_tag, git_on in (("git_on_PATH", True), ("git_off_PATH", False)):
        env = base_env(home, git_on)
        where = subprocess.run(["cmd.exe", "/c", "where hermes"], capture_output=True, text=True, env=env)
        rows[f"{home_tag}|{git_tag}"] = {
            "env": {"HERMES_HOME": home, "git_on_PATH": git_on, "PATH": env["PATH"]},
            "where_hermes": (where.stdout or "").strip().splitlines()[:4],
            "probes": {f"{name}::{p[0]}": run([path] + p, env) for name, path in ENTRIES.items() for p in PROBES},
        }

report = {"schema": "FHS.WP12.ENTRY_EQUIVALENCE/2",
          "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "entries": ENTRIES, "rows": rows}

# verdicts are computed, never asserted
checks = {}
for combo, row in rows.items():
    for probe in ("--version", "status", "--print-runtime-command"):
        shas = {n: row["probes"][f"{n}::{probe}"]["out_sha"] for n in ENTRIES}
        rcs = {n: row["probes"][f"{n}::{probe}"]["rc"] for n in ENTRIES}
        # PATH entry vs entry under test = P (what PATH resolves to here) vs X (the launcher it execs)
        checks[f"{combo}::{probe}"] = {
            "P_equals_X": shas["P_recovery_cmd"] == shas["X_recovery_exe"] and rcs["P_recovery_cmd"] == rcs["X_recovery_exe"],
            "X_equals_E": shas["X_recovery_exe"] == shas["E_recovery_extless"],
            "A_equals_X": shas["A_product_venv_cmd"] == shas["X_recovery_exe"],
            "distinct_out_shas": len(set(shas.values())),
            "bytes": {n: row["probes"][f"{n}::{probe}"]["out_b"] for n in ENTRIES},
            "rcs": rcs,
        }

report["checks"] = checks
report["summary"] = {
    "P_equals_X_everywhere": all(v["P_equals_X"] for v in checks.values()),
    "X_equals_E_everywhere": all(v["X_equals_E"] for v in checks.values()),
    "A_equals_X_anywhere": any(v["A_equals_X"] for v in checks.values()),
    "A_equals_X_somewhere_only": any(v["A_equals_X"] for v in checks.values()) and not all(v["A_equals_X"] for v in checks.values()),
    "version_suffix_is_git_conditional": (
        checks["HERMES_HOME_unset|git_on_PATH::--version"]["bytes"]["X_recovery_exe"]
        != checks["HERMES_HOME_unset|git_off_PATH::--version"]["bytes"]["X_recovery_exe"]),
}
(OUT / "ENTRY_EQUIVALENCE_MATRIX.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8", newline="\n")
print(json.dumps(report["summary"], indent=1))
for k, v in checks.items():
    print(f"{k:52} P==X {str(v['P_equals_X']):5} X==E {str(v['X_equals_E']):5} A==X {str(v['A_equals_X']):5} shas {v['distinct_out_shas']} bytes {v['bytes']}")
