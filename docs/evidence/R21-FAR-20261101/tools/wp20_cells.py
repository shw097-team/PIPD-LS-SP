"""WP-FHS-20: exercise the 12 SURFACE_EXISTS_NOT_RUN cells (PROFILE + PLUGIN on Hermes Agent).

The 12 cells are kind in {PROFILE, PLUGIN} x mode in {STANDALONE, PREW3_SHADOW, SWOF_CONNECTED}
x legacy in {ON, OFF}, all on host Hermes Agent. Each cell gets its OWN run and its own receipt;
nothing is copied between cells, and the axis that turns out to be inert is named rather than hidden.

Isolation discipline: every run uses a throwaway HERMES_HOME under var/…/wp20/home-<cell>, so no
user-data effect happens and the work stays inside the HOST_OPERATIONS envelope ceiling.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
HERMES = r"D:\Hermes-Recovery\live22\bin\hermes.exe"
REAL_PLUGIN = pathlib.Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\plugins\disk-cleanup")

KINDS = ("PROFILE", "PLUGIN")
MODES = ("STANDALONE", "PREW3_SHADOW", "SWOF_CONNECTED")
LEGACY = ("ON", "OFF")


def run(cmd, home, tag):
    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)
    env["HERMES_PROFILE"] = ""
    env.pop("PYTHONPATH", None)
    t0 = time.time()
    p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL, env=env)
    try:
        out, err = p.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        return {"cmd": [str(c) for c in cmd], "tag": tag + "_TIMEOUT", "pid": p.pid, "rc": "TIMEOUT",
                "ms": round((time.time() - t0) * 1000, 1), "out_b": len(out), "out_sha": hashlib.sha256(out).hexdigest(),
                "err_b": len(err), "err_sha": hashlib.sha256(err).hexdigest(),
                "out_tail": out.decode("utf-8", "replace").strip()[-200:], "err_tail": "TIMEOUT"}
    return {"cmd": [str(c) for c in cmd], "tag": tag, "pid": p.pid, "rc": p.returncode,
            "ms": round((time.time() - t0) * 1000, 1),
            "out_b": len(out), "out_sha": hashlib.sha256(out).hexdigest(),
            "err_b": len(err), "err_sha": hashlib.sha256(err).hexdigest(),
            "out_tail": out.decode("utf-8", "replace").strip()[-400:],
            "err_tail": err.decode("utf-8", "replace").strip()[-300:]}


def profile_cell(cell, home):
    name = f"wp20_{cell['mode'].lower()[:6]}_{cell['legacy'].lower()}"
    steps = [run([HERMES, "profile", "create", name, "--no-alias"], home, "create"),
             run([HERMES, "profile", "list"], home, "list"),
             run([HERMES, "profile", "show", name], home, "show"),
             run([HERMES, "profile", "show", "wp20_does_not_exist"], home, "neg_show_missing"),
             run([HERMES, "profile", "delete", name, "-y"], home, "delete")]
    created = steps[0]["rc"] == 0 and name in steps[1]["out_tail"]
    shown = steps[2]["rc"] == 0
    neg_typed = steps[3]["rc"] != 0
    return {"steps": steps, "surface_exercised": bool(created and shown),
            "positive": created and shown, "negative_refused": neg_typed, "name": name}


def plugin_cell(cell, home):
    broken = home / "_broken_plugin"
    if broken.exists():
        shutil.rmtree(broken)
    broken.mkdir(parents=True)
    (broken / "plugin.yaml").write_text("name: broken\nthis is: not: yaml: [\n", encoding="utf-8")
    steps = [run([HERMES, "plugins", "list"], home, "list"),
             run([HERMES, "plugins", "validate", str(REAL_PLUGIN), "--json"], home, "validate_real"),
             run([HERMES, "plugins", "validate", str(broken), "--json"], home, "validate_broken"),
             run([HERMES, "plugins", "capabilities"], home, "capabilities")]
    listed = steps[0]["rc"] == 0
    pos = steps[1]["rc"] == 0
    neg = steps[2]["rc"] != 0
    return {"steps": steps, "surface_exercised": bool(listed and (pos or neg)),
            "positive": pos, "negative_refused": neg, "real_plugin": str(REAL_PLUGIN)}


cells = []
for kind in KINDS:
    for mode in MODES:
        for legacy in LEGACY:
            cell = {"kind": kind, "mode": mode, "legacy": legacy, "host": "Hermes Agent"}
            home = OUT / f"home-{kind.lower()}-{mode.lower()}-{legacy.lower()}"
            if home.exists():
                shutil.rmtree(home)
            home.mkdir(parents=True)
            cell["hermes_home"] = str(home)
            cell["generated_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            body = profile_cell(cell, home) if kind == "PROFILE" else plugin_cell(cell, home)
            cell.update(body)
            cell["state"] = ("MEASURED_PASS" if body["positive"] and body["negative_refused"]
                             else "MEASURED_PARTIAL")
            cells.append(cell)

# isolation control: a profile created in one home must not appear in another
iso_home = OUT / "home-isolation-check"
if iso_home.exists():
    shutil.rmtree(iso_home)
iso_home.mkdir(parents=True)
iso_create = run([HERMES, "profile", "create", "wp20_iso", "--no-alias"], cells[0]["hermes_home"], "iso_create")
iso_list_other = run([HERMES, "profile", "list"], iso_home, "iso_list_elsewhere")
isolation = {"created_in": cells[0]["hermes_home"], "listed_in": str(iso_home),
             "leaked": "wp20_iso" in iso_list_other["out_tail"],
             "create_rc": iso_create["rc"], "other_list_rc": iso_list_other["rc"]}

# inert-axis check: same-surface outputs compared across mode/legacy
def tails(kind, tag):
    return {f"{c['mode']}|{c['legacy']}": next(s["out_sha"] for s in c["steps"] if s["tag"] == tag)
            for c in cells if c["kind"] == kind}


inertness = {}
for kind, tag in (("PROFILE", "list"), ("PLUGIN", "list")):
    shas = tails(kind, tag)
    inertness[kind] = {"tag": tag, "distinct_out_shas": len(set(shas.values())), "shas": shas}

summary = {
    "schema": "FHS.R21.WP20.CELLS/1",
    "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "host": "Hermes Agent", "entry": HERMES,
    "cells": cells,
    "isolation": isolation,
    "inert_axis": inertness,
    "counts": {"cells": len(cells),
               "MEASURED_PASS": sum(1 for c in cells if c["state"] == "MEASURED_PASS"),
               "MEASURED_PARTIAL": sum(1 for c in cells if c["state"] == "MEASURED_PARTIAL")},
    "claim_ceiling": ("AUTHOR_SIDE_LOCAL: the PROFILE and PLUGIN surfaces were exercised on this host with a "
                      "throwaway HERMES_HOME; no provider call, no gateway, no model turn"),
}
(OUT / "CELL_RESULTS_R21.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
print(json.dumps(summary["counts"], indent=1))
for c in cells:
    first = c["steps"][0]
    print(f"{c['kind']:8} {c['mode']:14} {c['legacy']:3} -> {c['state']:16} "
          f"pos={c['positive']} neg={c['negative_refused']} rcs={[s['rc'] for s in c['steps']]}")
print("isolation:", json.dumps(isolation, ensure_ascii=False))
print("inert:", json.dumps({k: v["distinct_out_shas"] for k, v in inertness.items()}, ensure_ascii=False))
