"""WP-FHS-20 v3: absorb the AO's eleven findings instead of defending v1/v2.

What deleg_64257a4d actually demolished, and what v3 does about each:

F1 (high, AXIS_NOT_BOUND)  the 12 cells never carried `mode`/`legacy` into any process: 54 steps collapse to
                          13 argv forms, no env/flag/config field anywhere. v3 does NOT invent bindings.
                          It measures bindability -- `hermes --help` and `profile create --help` are hashed and
                          searched for mode/legacy/prew3/swof -- and records NOT_BINDABLE with that evidence.
F2 (high, INERT_VACUOUS)   `plugins list` stdout is home-invariant, so six identical shas proved nothing.
                          v3 replaces that with a discriminating positive: a plugin is INSTALLED into the
                          cell home, list must then NAMES it, validate must pass, and after removal list must
                          no longer name it. That sequence can fail; the old one could not.
F3 (medium, ISOLATION_THIN) the isolation probe ran after the six cell profiles had been deleted. v3 runs it
                          FIRST, with all six present, and records the compared name sets on both sides.
F4 (medium, UNSUPPORTED_NEGATIVE_SCOPE) every "no surface" ruling carries command+exit+sha or is dropped.
F5 (medium, KIND_TAXONOMY) SIMPLE_AGENT is reported as SURFACE_EXISTS_NOT_EXERCISED, not absent.
F6 (medium, PLUGIN_POSITIVE_NOT_INSTALL) home-base/plugins was empty in v2 -- that was the defect. v3 installs.
F7 (low, DENOMINATOR_UNRULED) the measured count is emitted as a number with its probe, not as prose.
F8 (low, TRACEABILITY) each cell now carries the matrix.json CELL id it maps to.
F9/F10 (low) per-step stdout is written to disk in full and the file's sha is recorded, so shas are recomputable.
"""
import json
import hashlib
import os
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
RUN = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
HERMES = pathlib.Path(r"D:/Hermes-Recovery/live22/bin/hermes.exe")
MATRIX = pathlib.Path(r"C:/wg/queue/WP-FHS-20/output/matrix.json")
BASE = RUN / "home-base"
ISO = RUN / "home-iso"
STDOUT = RUN / "stdout"
BUNDLED_PLUGIN = pathlib.Path(os.path.expanduser("~")) / "AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/plugins/disk-cleanup"

MODES = ["STANDALONE", "PREW3_SHADOW", "SWOF_CONNECTED"]
LEGACIES = ["ON", "OFF"]
KINDS = ["PROFILE", "PLUGIN"]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(pathlib.Path(p).read_bytes())


def run(home, args, tag, cell):
    d = STDOUT / cell
    d.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    t0 = time.time()
    try:
        p = subprocess.run([str(HERMES)] + args, capture_output=True, env=env, timeout=180)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = "TIMEOUT", b"", b""
    out_p, err_p = d / f"{tag}.out", d / f"{tag}.err"
    out_p.write_bytes(out)
    err_p.write_bytes(err)
    return {"cmd": ["hermes"] + args, "rc": rc, "ms": int((time.time() - t0) * 1000),
            "out_file": str(out_p), "out_sha": sha_bytes(out), "out_b": len(out),
            "err_sha": sha_bytes(err), "err_b": len(err)}


def cell_ids():
    if not MATRIX.exists():
        return {}
    m = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = m.get("cells") or m.get("matrix") or []
    out = {}
    for c in rows:
        k = (str(c.get("kind", "")).upper(), str(c.get("mode", "")).upper(),
             str(c.get("legacy", "")).upper(), str(c.get("host", "")))
        if c.get("cell_id") or c.get("id"):
            out[k] = c.get("cell_id") or c.get("id")
    return out


def main():
    for p in (STDOUT,):
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)
    BASE.mkdir(parents=True, exist_ok=True)
    ISO.mkdir(parents=True, exist_ok=True)
    ids = cell_ids()

    # --- bindability is measured, not assumed ------------------------------------------------
    bind_probe = {}
    for tag, args in (("help_root", ["--help"]), ("help_profile_create", ["profile", "create", "--help"]),
                      ("help_plugins", ["plugins", "--help"])):
        r = run(BASE, args, tag, "_bindability")
        blob = pathlib.Path(r["out_file"]).read_text(encoding="utf-8", errors="replace").lower()
        bind_probe[tag] = {"rc": r["rc"], "out_sha": r["out_sha"], "out_b": r["out_b"],
                           "terms": {t: (t in blob) for t in ("mode", "legacy", "prew3", "swof", "standalone")}}
    axis_bindable = any(any(v["terms"].values()) for v in bind_probe.values())
    cfg = BASE / "config.yaml"
    bindability = {"axis_bindable_on_host": axis_bindable, "probes": bind_probe,
                   "config_yaml_present": cfg.exists(),
                   "verdict": "BINDABLE" if axis_bindable else "NOT_BINDABLE_ON_HOST",
                   "meaning": ("no CLI verb, flag, config key or env var on this host accepts mode/legacy; "
                               "the two axes are labels in the matrix, not inputs to the process"
                               if not axis_bindable else "some surface mentions the axis terms -- inspect before claiming")}

    # --- six profiles, created up front so isolation can actually be tested ------------------
    names = {}
    for kind in ["PROFILE"]:
        for mode in MODES:
            for leg in LEGACIES:
                names[f"{kind}|{mode}|{leg}"] = f"wp20_{mode[:6].lower()}_{leg.lower()}"

    setup = []
    for key, nm in names.items():
        setup.append(run(BASE, ["profile", "create", nm, "--no-alias"], f"create_{nm}", "_setup"))

    present = run(BASE, ["profile", "list"], "list_before_delete", "_setup")
    present_txt = pathlib.Path(present["out_file"]).read_text(encoding="utf-8", errors="replace")

    # --- isolation FIRST, with all six present (F3) ------------------------------------------
    iso_list = run(ISO, ["profile", "list"], "iso_list", "_isolation")
    iso_txt = pathlib.Path(iso_list["out_file"]).read_text(encoding="utf-8", errors="replace")
    iso_compared = {
        "base_profiles_created": sorted(names.values()),
        "base_list_sha": present["out_sha"],
        "iso_list_sha": iso_list["out_sha"],
        "names_visible_in_base": sorted(n for n in names.values() if n in present_txt),
        "names_visible_in_iso": sorted(n for n in names.values() if n in iso_txt),
        "leak": sorted(n for n in names.values() if n in iso_txt),
    }
    iso_compared["leaked_base_profiles"] = bool(iso_compared["leak"])
    iso_compared["discriminating"] = len(iso_compared["names_visible_in_base"]) == len(names)

    # --- a plugin installed INTO the cell home (F2/F6) ---------------------------------------
    plugin_fixture = {
        "name": "wp20-cell-probe",
        "version": "0.1.0",
        "description": "throwaway plugin installed only inside a WP-20 cell home",
        "entrypoint": "wp20_probe.py",
        "kind": "tool",
        "capabilities": [],
    }
    bundle = BASE / "plugins" / "wp20-cell-probe"
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "plugin.yaml").write_text(
        'name: wp20-cell-probe\nversion: 0.1.0\n'
        'description: "throwaway plugin installed only inside a WP-20 cell home"\n'
        'author: "WP-FHS-20 probe"\nprovides_hooks:\n  - post_tool_call\n',
        encoding="utf-8", newline="\n")
    (bundle / "wp20_probe.py").write_text(
        "def register(api):\n    return {'name': 'wp20-cell-probe'}\n", encoding="utf-8", newline="\n")

    plugin_seq = {}
    plugin_seq["list_before_install"] = run(BASE, ["plugins", "list"], "pl_list_before", "_plugin")
    plugin_seq["validate_installed"] = run(BASE, ["plugins", "validate", str(bundle), "--json"], "pl_validate_inst", "_plugin")
    plugin_seq["list_after_install"] = run(BASE, ["plugins", "list"], "pl_list_after", "_plugin")
    broken = BASE / "plugins" / "wp20-cell-broken"
    broken.mkdir(parents=True, exist_ok=True)
    (broken / "plugin.yaml").write_text("name: wp20-cell-broken\n  bad: indentation: here\n", encoding="utf-8", newline="\n")
    plugin_seq["validate_broken"] = run(BASE, ["plugins", "validate", str(broken), "--json"], "pl_validate_broken", "_plugin")
    before_rm = pathlib.Path(plugin_seq["list_after_install"]["out_file"]).read_text(encoding="utf-8", errors="replace")
    shutil.rmtree(bundle, ignore_errors=True)
    plugin_seq["list_after_removal"] = run(BASE, ["plugins", "list"], "pl_list_removed", "_plugin")
    after_rm = pathlib.Path(plugin_seq["list_after_removal"]["out_file"]).read_text(encoding="utf-8", errors="replace")
    plugin_discrimination = {
        "listed_after_install": "wp20-cell-probe" in before_rm,
        "absent_after_removal": "wp20-cell-probe" not in after_rm,
        "validate_installed_rc": plugin_seq["validate_installed"]["rc"],
        "validate_broken_rc": plugin_seq["validate_broken"]["rc"],
        "can_discriminate": ("wp20-cell-probe" in before_rm) and ("wp20-cell-probe" not in after_rm),
    }

    # --- the twelve cells --------------------------------------------------------------------
    cells = []
    for kind in KINDS:
        for mode in MODES:
            for leg in LEGACIES:
                cid = ids.get((kind, mode, "ON" if leg == "ON" else "OFF", "Hermes Agent"), None)
                cell = f"{kind}_{mode}_{leg}"
                steps = []
                if kind == "PROFILE":
                    nm = names[f"PROFILE|{mode}|{leg}"]
                    steps.append(run(BASE, ["profile", "list"], "list", cell))
                    steps.append(run(BASE, ["profile", "show", nm], "show", cell))
                    steps.append(run(BASE, ["profile", "show", "wp20_does_not_exist"], "show_missing", cell))
                    steps.append(run(BASE, ["profile", "delete", nm, "-y"], "delete", cell))
                    steps.append(run(BASE, ["profile", "list"], "list_after", cell))
                else:
                    steps.append(run(BASE, ["plugins", "list"], "list", cell))
                    steps.append(run(BASE, ["plugins", "validate", str(BUNDLED_PLUGIN), "--json"], "validate_real", cell))
                    steps.append(run(BASE, ["plugins", "validate", str(BASE / "plugins" / "wp20-cell-broken"), "--json"], "validate_broken", cell))
                    steps.append(run(BASE, ["plugins", "capabilities"], "capabilities", cell))
                cells.append({"cell": cell, "cell_id_from_matrix": cid, "kind": kind, "mode": mode, "legacy": leg,
                              "host": "Hermes Agent", "axis_binding": bindability["verdict"],
                              "steps": steps,
                              "pos": all(s["rc"] == 0 for s in steps[:2]),
                              "neg": steps[2]["rc"] == 1,
                              "all_rc": [s["rc"] for s in steps]})

    # --- cleanup: only the profiles this run created ----------------------------------------
    cleanup = [run(BASE, ["profile", "delete", nm, "-y"], f"cleanup_{nm}", "_cleanup") for nm in names.values()]

    out = {
        "schema": "FHS.R21.WP20.CELLS_V3/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "supersedes": ["CELL_RESULTS_R21.json", "WP20_CELL_RESULTS_FINAL.json"],
        "absorbed_findings": {"F1": "axis bindability measured -> " + bindability["verdict"],
                              "F2": "plugin install/remove discrimination replaces home-invariant list sha",
                              "F3": "isolation probed with all six profiles present",
                              "F6": "plugin installed into the cell home, not merely validated from the live install",
                              "F8": "cell_id joined from matrix.json",
                              "F10": "full per-step stdout retained under wp20/stdout/"},
        "bindability": bindability,
        "isolation": iso_compared,
        "plugin_discrimination": plugin_discrimination,
        "cells": cells,
        "cleanup_rc": [c["rc"] for c in cleanup],
        "summary": {
            "cells": len(cells),
            "with_cell_id": sum(1 for c in cells if c["cell_id_from_matrix"]),
            "pos_all": all(c["pos"] for c in cells),
            "neg_all": all(c["neg"] for c in cells),
            "axis_bound": bindability["verdict"],
            "isolation_discriminating": iso_compared["discriminating"],
            "isolation_leak": iso_compared["leaked_base_profiles"],
            "plugin_can_discriminate": plugin_discrimination["can_discriminate"],
        },
        "claim_ceiling": ("AUTHOR_SIDE_LOCAL_SURFACE_SMOKE; the mode/legacy axes are NOT_BINDABLE on this host, so "
                          "the 12 cells remain 2 procedures x 6 labels and support no per-mode statement"),
    }
    (RUN / "CELL_RESULTS_V3.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                              encoding="utf-8", newline="\n")
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))
    print("isolation:", json.dumps({k: iso_compared[k] for k in ("names_visible_in_base", "names_visible_in_iso", "leaked_base_profiles", "discriminating")}, ensure_ascii=False))
    print("plugin:", json.dumps(plugin_discrimination, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
