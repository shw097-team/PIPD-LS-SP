"""WP-FHS-20 v2: the 12 PROFILE/PLUGIN cells, one bootstrap instead of twelve.

v1 died twice for environmental reasons worth recording rather than hiding:
  * `hermes profile delete` blocks on a confirmation prompt unless `-y` is passed (child inherited stdin);
  * creating the first profile in a fresh HERMES_HOME makes the CLI bootstrap an install environment
    (`installs/<id>/environments/<id>/venv/...`), which is minutes of work and leaves a deep tree that
    plain shutil.rmtree cannot remove on Windows.
So v2 bootstraps ONE base home and runs each cell against it with its own profile name, giving every cell
its own run and receipt without paying bootstrap six times. Isolation is still measured, on a second home.
"""
import hashlib
import json
import os
import pathlib
import shutil
import stat
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
HERMES = r"D:\Hermes-Recovery\live22\bin\hermes.exe"
REAL_PLUGIN = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\plugins\disk-cleanup")
MODES = ("STANDALONE", "PREW3_SHADOW", "SWOF_CONNECTED")
LEGACY = ("ON", "OFF")


def safe_rm(p: pathlib.Path):
    if not p.exists():
        return
    def onerr(func, path, exc):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass
    shutil.rmtree(str(p), onerror=onerr)
    if p.exists():  # long-path fallback
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(p)], capture_output=True)


def run(cmd, home, tag, timeout=180):
    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)
    env.pop("HERMES_PROFILE", None)
    env.pop("PYTHONPATH", None)
    t0 = time.time()
    p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL, env=env)
    try:
        out, err = p.communicate(timeout=timeout)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        rc = "TIMEOUT"
    return {"cmd": [str(c) for c in cmd], "tag": tag, "pid": p.pid, "rc": rc,
            "ms": round((time.time() - t0) * 1000, 1),
            "out_b": len(out), "out_sha": hashlib.sha256(out).hexdigest(),
            "err_b": len(err), "err_sha": hashlib.sha256(err).hexdigest(),
            "out_tail": out.decode("utf-8", "replace").strip()[-400:],
            "err_tail": err.decode("utf-8", "replace").strip()[-300:]}


OUT.mkdir(parents=True, exist_ok=True)
safe_rm(OUT / "home-smoke")
base = OUT / "home-base"
base.mkdir(parents=True, exist_ok=True)

bootstrap = run([HERMES, "profile", "create", "wp20_bootstrap", "--no-alias", "--no-skills"], base, "bootstrap", timeout=600)

cells = []
for kind in ("PROFILE", "PLUGIN"):
    for mode in MODES:
        for legacy in LEGACY:
            cell = {"kind": kind, "mode": mode, "legacy": legacy, "host": "Hermes Agent",
                    "hermes_home": str(base), "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            if kind == "PROFILE":
                name = f"wp20_{mode.lower()[:6]}_{legacy.lower()}"
                steps = [run([HERMES, "profile", "create", name, "--no-alias", "--no-skills"], base, "create"),
                         run([HERMES, "profile", "list"], base, "list"),
                         run([HERMES, "profile", "show", name], base, "show"),
                         run([HERMES, "profile", "show", "wp20_does_not_exist"], base, "neg_show_missing"),
                         run([HERMES, "profile", "delete", name, "-y"], base, "delete")]
                created = steps[0]["rc"] == 0 and name in steps[1]["out_tail"]
                cell.update(name=name, steps=steps, positive=bool(created and steps[2]["rc"] == 0),
                            negative_refused=steps[3]["rc"] != 0)
            else:
                broken = OUT / f"_broken_plugin_{mode.lower()}_{legacy.lower()}"
                safe_rm(broken)
                broken.mkdir(parents=True)
                (broken / "plugin.yaml").write_text("name: broken\nthis is: not: yaml: [\n", encoding="utf-8")
                steps = [run([HERMES, "plugins", "list"], base, "list"),
                         run([HERMES, "plugins", "validate", str(REAL_PLUGIN), "--json"], base, "validate_real", timeout=240),
                         run([HERMES, "plugins", "validate", str(broken), "--json"], base, "validate_broken"),
                         run([HERMES, "plugins", "capabilities"], base, "capabilities")]
                cell.update(steps=steps, positive=steps[1]["rc"] == 0, negative_refused=steps[2]["rc"] != 0,
                            real_plugin=str(REAL_PLUGIN))
            cell["surface_exercised"] = bool(cell["positive"] or cell["negative_refused"])
            cell["state"] = ("MEASURED_PASS" if (cell["positive"] and cell["negative_refused"])
                             else "MEASURED_PARTIAL")
            cells.append(cell)

iso = OUT / "home-iso"
iso.mkdir(parents=True, exist_ok=True)
iso_list = run([HERMES, "profile", "list"], iso, "iso_list", timeout=600)
isolation = {"home": str(iso), "rc": iso_list["rc"],
             "leaked_base_profiles": any(n in iso_list["out_tail"] for n in
                                         ("wp20_bootstrap", "wp20_stand", "wp20_prew3", "wp20_swof")),
             "out_tail": iso_list["out_tail"][-200:]}

def shas(kind, tag):
    return {f"{c['mode']}|{c['legacy']}": next((s["out_sha"] for s in c["steps"] if s["tag"] == tag), None)
            for c in cells if c["kind"] == kind}

inert = {k: {"tag": t, "distinct_out_shas": len(set(v for v in shas(k, t).values() if v)), "shas": shas(k, t)}
         for k, t in (("PROFILE", "list"), ("PLUGIN", "list"))}

summary = {"schema": "FHS.R21.WP20.CELLS/2",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "host": "Hermes Agent", "entry": HERMES, "bootstrap": bootstrap,
           "cells": cells, "isolation": isolation, "inert_axis": inert,
           "counts": {"cells": len(cells),
                      "MEASURED_PASS": sum(1 for c in cells if c["state"] == "MEASURED_PASS"),
                      "MEASURED_PARTIAL": sum(1 for c in cells if c["state"] == "MEASURED_PARTIAL")},
           "claim_ceiling": ("AUTHOR_SIDE_LOCAL: PROFILE and PLUGIN surfaces exercised on this host in a throwaway "
                             "HERMES_HOME; no provider call, no gateway, no model turn")}
(OUT / "CELL_RESULTS_R21.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
print(json.dumps(summary["counts"], indent=1))
for c in cells:
    print(f"{c['kind']:8} {c['mode']:14} {c['legacy']:3} {c['state']:16} pos={c['positive']} neg={c['negative_refused']} "
          f"rcs={[s['rc'] for s in c['steps']]}")
print("isolation:", json.dumps(isolation, ensure_ascii=False)[:200])
print("inert:", {k: v["distinct_out_shas"] for k, v in inert.items()})
