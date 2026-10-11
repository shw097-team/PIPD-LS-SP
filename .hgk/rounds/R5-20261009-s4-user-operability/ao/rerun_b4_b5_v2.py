#!/usr/bin/env python3
"""Re-run the two AO acceptance cases that were NOT_RUN because their prerequisite failed.

AO labels B4 and B5 == brief BLOCK A cases A4 and A5 (mutated-wheel runtime checks).

CORRECTION OF THE FIRST ATTEMPT (v1 kept alongside, not deleted): v1 wrote the mutated wheels as
`B4.whl` / `B5.whl`. pip rejects those on the FILENAME before looking inside, so the install failed
for a reason that has nothing to do with the mutation and both cases reported a false PASS. This
version keeps a valid wheel filename, records INVALID instead of PASS when pip refuses the file, and
runs every case in two variants so the interpretation cannot be faked:

  variant "record_untouched" - exactly the brief's wording: RECORD left as-is.
  variant "record_fixed"     - RECORD repaired so the install SUCCEEDS, which is the only way to
                               test the *runtime* guard the brief asks about.

A case is PASS only when the mutation is actually detected. `silently_succeeded` (install AND run
both exit 0) is FAIL. A `not_a_valid_wheel` install error is INVALID, never PASS.

Writes ao/rerun_b4_b5.json. Nothing is written outside the system temp dir.
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
OUT = REPO / ".hgk/rounds/R5-20261009-s4-user-operability/ao/rerun_b4_b5.json"
WHEEL = REPO / "dist/pipd_ls_sp-0.1.0-py3-none-any.whl"
VALID_NAME = "pipd_ls_sp-0.1.0-py3-none-any.whl"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def record_hash(data: bytes) -> str:
    d = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
    return f"sha256={d}"


def build_mutated(src: Path, dst: Path, drop, truncate, fix_record: bool) -> dict:
    members = []
    with zipfile.ZipFile(src) as zin:
        for item in zin.infolist():
            members.append([item.filename, zin.read(item.filename)])

    acted = {}
    for m in members:
        if drop and m[0] == drop:
            acted["dropped"] = m[0]
            m[1] = None
        elif truncate and m[0] == truncate:
            before = len(m[1])
            m[1] = m[1][:-7]
            acted["truncated"] = {"member": m[0], "before": before, "after": len(m[1])}

    members = [m for m in members if m[1] is not None]

    if fix_record:
        rec = next((m for m in members if m[0].endswith(".dist-info/RECORD")), None)
        if rec:
            rows = list(csv.reader(io.StringIO(rec[1].decode("utf-8", "replace"))))
            by_name = {m[0]: m[1] for m in members}
            fixed = []
            for row in rows:
                if not row:
                    continue
                path = row[0]
                if drop and path == drop:
                    acted["record_row_removed"] = path
                    continue
                if path in by_name and len(row) >= 3 and row[1].startswith("sha256="):
                    data = by_name[path]
                    new_h = record_hash(data)
                    if new_h != row[1]:
                        acted.setdefault("record_rows_repaired", []).append(path)
                        row = [row[0], new_h, str(len(data))]
                fixed.append(row)
            buf = io.StringIO()
            csv.writer(buf, lineterminator="\n").writerows(fixed)
            rec[1] = buf.getvalue().encode()

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in members:
            zout.writestr(name, data)
    return acted


def run_case(case: str, variant: str, work: Path, drop=None, truncate=None) -> dict:
    out = {"case": case, "variant": variant}
    d = work / f"{case}-{variant}"
    d.mkdir(parents=True, exist_ok=True)
    whl = d / VALID_NAME
    out["mutation"] = build_mutated(WHEEL, whl, drop, truncate, variant == "record_fixed")
    out["mutated_sha256"] = sha256(whl)
    out["mutated_bytes"] = whl.stat().st_size

    venv = d / "venv"
    r = subprocess.run([sys.executable, "-m", "venv", str(venv)], capture_output=True, text=True)
    pip = venv / "Scripts" / "pip.exe"
    out["venv"] = {"exit": r.returncode, "pip_present": pip.exists()}
    if not pip.exists():
        out["outcome"] = "NOT_RUN"
        out["reason"] = "no pip in the fresh venv"
        return out

    py = venv / "Scripts" / "python.exe"
    inst = subprocess.run([str(py), "-m", "pip", "install", "--no-index", "--no-deps", str(whl)],
                          capture_output=True, text=True)
    blob = inst.stdout + inst.stderr
    out["install_exit"] = inst.returncode
    out["install_tail"] = blob[-600:]
    if "is not a valid wheel filename" in blob:
        out["outcome"] = "INVALID"
        out["reason"] = "pip rejected the filename, so the mutation was never exercised"
        return out

    run = subprocess.run([str(py), "-m", "pipd_ls_sp.cli", "--root", str(REPO), "doctor"],
                         capture_output=True, text=True)
    out["run_exit"] = run.returncode
    out["run_tail"] = (run.stdout + run.stderr)[-600:]
    out["install_succeeded"] = inst.returncode == 0

    silently = inst.returncode == 0 and run.returncode == 0
    out["silently_succeeded"] = silently
    if silently:
        out["outcome"] = "FAIL"
        out["interpretation"] = "the mutated wheel produced a working CLI - the guard does not hold"
    else:
        det = []
        if inst.returncode != 0:
            det.append("installation refused")
        if run.returncode != 0:
            det.append("installed CLI refused to run")
        out["outcome"] = "PASS"
        out["detected_by"] = det
        out["interpretation"] = "mutation detected: " + " and ".join(det)
    return out


def main() -> int:
    if not WHEEL.exists():
        print(f"FATAL: wheel absent: {WHEEL}")
        return 2
    names = zipfile.ZipFile(WHEEL).namelist()
    schema = sorted(n for n in names if n.endswith(".schema.json"))
    mod = sorted(n for n in names if n.startswith("pipd_ls_sp/") and n.endswith(".py"))
    if not schema or not mod:
        print("FATAL: nothing to mutate")
        return 2

    work = Path(tempfile.mkdtemp(prefix="ao-b4b5-"))
    doc = {
        "schema": "pipd-r5s4-ao-rerun/2",
        "why": "B4/B5 were NOT_RUN because their prerequisite (a fresh venv with pip) failed at "
               "ensurepip. ensurepip exits 0 here, so they are re-run.",
        "v1_correction": "The first attempt produced false PASSes: the mutated wheel was named "
                         "B4.whl / B5.whl and pip rejects that on the filename alone, so the "
                         "mutation was never exercised. v1 is kept as rerun_b4_b5_v1_falsepass.json.",
        "wheel": str(WHEEL),
        "wheel_sha256": sha256(WHEEL),
        "wheel_members": len(names),
        "ensurepip_probe": subprocess.run([sys.executable, "-m", "ensurepip", "--version"],
                                          capture_output=True, text=True).stdout.strip(),
        "cases": [],
    }
    for case, kw in (("B4", {"drop": schema[0]}), ("B5", {"truncate": mod[0]})):
        for variant in ("record_untouched", "record_fixed"):
            doc["cases"].append(run_case(case, variant, work, **kw))

    OUT.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(REPO)}")
    for c in doc["cases"]:
        print(f"  {c['case']}/{c['variant']}: {c['outcome']}  mutation={json.dumps(c.get('mutation'))[:120]}")
        print(f"     install_exit={c.get('install_exit')} run_exit={c.get('run_exit')} "
              f"silently={c.get('silently_succeeded')} | {str(c.get('interpretation') or c.get('reason'))[:110]}")
        if c.get("run_tail"):
            print(f"     run_tail: {str(c['run_tail'])[-220:]}")
    shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
