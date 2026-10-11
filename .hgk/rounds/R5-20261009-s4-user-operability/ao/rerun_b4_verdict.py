#!/usr/bin/env python3
"""B4 (brief A4) verdict, probe v3 - third attempt, and the first one that is sound.

What went wrong twice, both preserved as evidence rather than hidden:
  v1 (rerun_b4_b5_v1_falsepass.json): the mutated wheel was named `B4.whl`; pip rejects that on the
     FILENAME alone, so the install failed for an unrelated reason and both cases logged a false PASS.
  v2 (rerun_b4_b5.json): named the wheel correctly, but the probe command for B4 was `doctor`.
     src/pipd_ls_sp/cli.py contains ZERO references to load_registry / load_schema /
     _resolve_schemas_dir, so `doctor` cannot observe a missing schema at all. The "silently
     succeeded" reading was therefore about the probe, not the product.
  v2-probe (rerun_b4_probe.json, conclusion VOID): that probe passed `--root` twice and omitted
     required options, so all three commands exited 2 on argparse usage errors. Its "CONCLUSION"
     line is wrong and is retracted.

This version asks the question directly, through the API that actually resolves schemas:

  registry.load_registry()  ->  for each family, raises ValidationFail
                                "schema file missing for the contract" if the .schema.json is absent
  registry.load_schema(name) -> reads the file directly

The probe (a) drops the member and repairs RECORD so the INSTALL SUCCEEDS, (b) proves from inside
the installed package that the victim file really is gone while registry.json still lists the
family, then (c) calls the two APIs and captures the exception type and message.

Writes ao/rerun_b4_verdict.json. Nothing is written outside the system temp dir.
"""
import base64
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/PIPD")
OUT = REPO / ".hgk/rounds/R5-20261009-s4-user-operability/ao/rerun_b4_verdict.json"
WHEEL = REPO / "dist/pipd_ls_sp-0.1.0-py3-none-any.whl"
VALID_NAME = "pipd_ls_sp-0.1.0-py3-none-any.whl"
VICTIM_FAMILY = "ArtifactIdentity"

INNER = r'''
import importlib.resources as R, json, traceback
out = {}
pkg = R.files("pipd_ls_sp")
sd = pkg / "schemas"
victim = sd / ("__VICTIM__.schema.json")
out["schemas_dir"] = str(sd)
out["victim_present_in_installed_package"] = victim.is_file()
try:
    reg = json.loads((sd / "registry.json").read_text())
    fights = [f["contract"] for f in reg.get("families", [])]
    out["registry_family_count"] = len(fights)
    out["registry_still_lists_victim"] = "__VICTIM__" in fights
except Exception as e:
    out["registry_read_error"] = repr(e)

try:
    import pipd_ls_sp.registry as REG
    d = REG.load_registry()
    out["load_registry"] = {"raised": False, "families": len(d.get("families", []))}
except Exception as e:
    out["load_registry"] = {"raised": True, "type": type(e).__name__, "message": str(e)[:300]}

try:
    REG.load_schema("__VICTIM__")
    out["load_schema_victim"] = {"raised": False}
except Exception as e:
    out["load_schema_victim"] = {"raised": True, "type": type(e).__name__, "message": str(e)[:300]}

print(json.dumps(out))
'''


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def rec_hash(d: bytes) -> str:
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(d).digest()).decode().rstrip("=")


def build(dst: Path, drop: str) -> dict:
    members = []
    with zipfile.ZipFile(WHEEL) as z:
        for i in z.infolist():
            members.append([i.filename, z.read(i.filename)])
    acted = {}
    for m in members:
        if m[0] == drop:
            acted["dropped"] = m[0]
            m[1] = None
    members = [m for m in members if m[1] is not None]
    rec = next((m for m in members if m[0].endswith(".dist-info/RECORD")), None)
    rows = list(csv.reader(io.StringIO(rec[1].decode("utf-8", "replace"))))
    kept = []
    for r in rows:
        if r and r[0] == drop:
            acted["record_row_removed"] = r[0]
            continue
        kept.append(r)
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(kept)
    rec[1] = buf.getvalue().encode()
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in members:
            z.writestr(n, d)
    return acted


def main() -> int:
    names = zipfile.ZipFile(WHEEL).namelist()
    victim = next(n for n in names if n.endswith(f"/{VICTIM_FAMILY}.schema.json"))
    work = Path(tempfile.mkdtemp(prefix="b4v-"))
    whl = work / VALID_NAME
    mutation = build(whl, victim)

    venv = work / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], capture_output=True, text=True)
    py = venv / "Scripts" / "python.exe"
    inst = subprocess.run([str(py), "-m", "pip", "install", "--no-index", "--no-deps", str(whl)],
                          capture_output=True, text=True)

    inner = work / "inner.py"
    inner.write_text(INNER.replace("__VICTIM__", VICTIM_FAMILY), encoding="utf-8", newline="\n")
    # cwd = work, which is empty: nothing can be borrowed from the repository working tree.
    probe = subprocess.run([str(py), str(inner)], capture_output=True, text=True, cwd=str(work))

    inner_out = {}
    if probe.stdout.strip():
        try:
            inner_out = json.loads(probe.stdout.strip().splitlines()[-1])
        except Exception:
            inner_out = {"unparsed": probe.stdout[-400:]}

    lr = inner_out.get("load_registry") or {}
    ls = inner_out.get("load_schema_victim") or {}
    guard_held = bool(lr.get("raised")) and VICTIM_FAMILY in str(lr.get("message", ""))
    doc = {
        "schema": "pipd-r5s4-ao-b4verdict/3",
        "question": "with a schema member missing from the INSTALLED package, does the code that "
                    "resolves schemas refuse, and does it name the family?",
        "victim_member": victim,
        "mutation": mutation,
        "install_exit": inst.returncode,
        "installed_package_state": inner_out,
        "inner_stderr_tail": probe.stderr[-300:],
        "guard_held": guard_held,
        "verdict": "PASS" if guard_held else "FAIL",
        "interpretation": (
            "the schema resolver refuses with a typed error naming the family when the member is "
            "absent from the installed package - the brief's A4 requirement is satisfied by "
            "registry.load_registry(), NOT by `doctor`"
            if guard_held else
            "the schema resolver did not refuse with a typed error naming the family"
        ),
        "scope_note": "This does NOT verify that any CLI subcommand surfaces that error to a user; "
                      "`doctor` provably cannot, because it never opens the schema set.",
        "retractions": {
            "rerun_b4_b5_v1_falsepass.json": "false PASS - invalid wheel filename, mutation never exercised",
            "rerun_b4_probe.json": "CONCLUSION line is VOID - argparse usage errors, no schema resolution reached",
        },
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO)}")
    print(f"  victim={victim}  install_exit={inst.returncode}  mutation={mutation}")
    print(f"  victim absent from installed package : {inner_out.get('victim_present_in_installed_package')}")
    print(f"  registry still lists the family      : {inner_out.get('registry_still_lists_victim')} "
          f"(families={inner_out.get('registry_family_count')})")
    print(f"  load_registry() -> {lr}")
    print(f"  load_schema(victim) -> {ls}")
    print(f"  GUARD HELD = {guard_held}  ->  verdict {doc['verdict']}")
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
