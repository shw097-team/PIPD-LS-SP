"""S3d: re-measure the PLUGIN install/list/remove leg without the fake fixture.

What the AO rejected (F6/N1/N2): the old block "installed" a plugin by writing files in Python, the fixture
failed its own `loadable` check, the cited shas existed nowhere, and the before/after lists were byte-identical.

This probe asks the host the question the block claimed to answer, and keeps every byte:
  A  empty home                -> `plugins list`
  B  home + a REAL bundled plugin copied into <home>/plugins/<name>   -> `plugins list`, `validate --json`
  C  same home                 -> `plugins remove <name>` (does removal work without an install record?)
  D  fresh home                -> `plugins install <catalog name>` (does the real install path work offline?)

Each step records argv, rc, stdout bytes, sha256 and the raw file path. Nothing here is a PASS until the two
lists differ AND the name appears only in the expected one; otherwise the honest disposition is recorded.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
WP20 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
SCRATCH = WP20 / "plugin_probe"
OUT = WP20 / "stdout" / "_plugin2"
BIN = r"D:\Hermes-Recovery\live22\bin\hermes.exe"
BUNDLED = (pathlib.Path(os.environ["LOCALAPPDATA"]) / "Packages" / "OpenAI.Codex_2p2nqsd0c76g0" / "LocalCache"
           / "Local" / "hermes" / "hermes-agent" / "plugins" / "disk-cleanup")
PLUGIN_NAME = "disk-cleanup"
TIMEOUT = 120


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(home, args, tag, timeout=TIMEOUT):
    env = dict(os.environ)
    env["HERMES_HOME"] = str(home)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("HERMES_PROFILE", None)
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    try:
        p = subprocess.run([BIN, *args], capture_output=True, text=True, env=env, timeout=timeout,
                           encoding="utf-8", errors="replace")
        rc, out, err = p.returncode, p.stdout or "", p.stderr or ""
        timed_out = False
    except subprocess.TimeoutExpired as e:
        rc, out, err, timed_out = -9, (e.stdout or ""), (e.stderr or ""), True
    blob = out.encode("utf-8")
    f = OUT / f"{tag}.out"
    f.write_text(out, encoding="utf-8", newline="\n")
    (OUT / f"{tag}.err").write_text(err, encoding="utf-8", newline="\n")
    return {"tag": tag, "argv": [BIN, *args], "hermes_home": str(home), "rc": rc, "ms": int((time.time() - t0) * 1000),
            "bytes": len(blob), "sha256": sha(blob), "out_file": str(f.relative_to(ROOT)).replace("\\", "/"),
            "err_tail": err.strip().splitlines()[-2:], "timed_out": timed_out}


def main():
    for d in (SCRATCH, OUT):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    empty, copied = SCRATCH / "home_empty", SCRATCH / "home_copied"
    install_home = SCRATCH / "home_install"
    for h in (empty, copied, install_home):
        h.mkdir(parents=True)

    steps = []
    a1 = run(empty, ["plugins", "list"], "A_list_empty")
    steps.append(a1)

    (copied / "plugins").mkdir(parents=True, exist_ok=True)
    shutil.copytree(BUNDLED, copied / "plugins" / PLUGIN_NAME)
    b1 = run(copied, ["plugins", "list"], "B_list_copied")
    b2 = run(copied, ["plugins", "validate", str(copied / "plugins" / PLUGIN_NAME), "--json"], "B_validate_copied")
    c1 = run(copied, ["plugins", "remove", PLUGIN_NAME], "C_remove_no_record")
    b3 = run(copied, ["plugins", "list"], "C_list_after_remove")
    d1 = run(install_home, ["plugins", "install", PLUGIN_NAME, "--no-deps"], "D_install_catalog", timeout=180)
    d2 = run(install_home, ["plugins", "list"], "D_list_after_install")
    steps += [b1, b2, c1, b3, d1, d2]

    def present(step):
        f = ROOT / step["out_file"]
        return PLUGIN_NAME in f.read_text(encoding="utf-8", errors="replace")

    list_empty, list_copied = a1, b1
    doc = {
        "schema": "FHS.R21.WP20.PLUGIN_PROBE/2",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "binary": BIN, "binary_sha256": sha(pathlib.Path(BIN).read_bytes()),
        "fixture": {"source": str(BUNDLED), "name": PLUGIN_NAME,
                    "copied_sha256_of_manifest": sha((copied / "plugins" / PLUGIN_NAME / "plugin.yaml").read_bytes())
                    if (copied / "plugins" / PLUGIN_NAME / "plugin.yaml").exists() else None},
        "steps": steps,
        "questions": {
            "does_list_see_a_copied_directory": list_copied["sha256"] != list_empty["sha256"] or present(list_copied),
            "is_the_copied_plugin_loadable": None,
            "does_remove_work_without_an_install_record": c1["rc"] == 0,
            "does_catalog_install_work_on_this_host": d1["rc"] == 0,
            "does_the_name_appear_after_install": present(d2),
        },
        "claim_ceiling": ("author-side local probe in throwaway HERMES_HOME directories; no PASS is claimed for the "
                          "plugin cell until a list delta is observed on a real install"),
    }
    vtxt = (ROOT / b2["out_file"]).read_text(encoding="utf-8", errors="replace")
    try:
        vjson = json.loads(vtxt[vtxt.index("{"):vtxt.rindex("}") + 1])
        doc["questions"]["is_the_copied_plugin_loadable"] = bool(vjson.get("ok"))
        doc["validate_detail"] = vjson.get("checks") or vjson.get("problems") or vjson.get("detail")
    except Exception as exc:  # noqa: BLE001
        doc["questions"]["is_the_copied_plugin_loadable"] = f"UNPARSED: {exc}"

    out = WP20 / "PLUGIN_PROBE_V2.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"questions": doc["questions"], "list_empty": list_empty["sha256"][:16],
                      "list_copied": list_copied["sha256"][:16], "install_rc": d1["rc"],
                      "install_err": d1["err_tail"], "sha256": sha(out.read_bytes())[:16]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
