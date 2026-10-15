"""R5S independent-case measurement on the FROZEN commit dba4b19 (orchestrator measurement).

This is NOT a lane verdict: it is a separate read-only process run by the orchestrator against a
pristine detached worktree. It re-derives the nine cases the lane brief named, and it re-runs the
subject's own atomic-requirement test module with raw counts and exit codes. Attribution: the
orchestrator, not an independent checker model.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

WT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/r5s-verify-wt")
OUT = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/VERIFY3")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
sys.path.insert(0, str(WT / "src"))

from pipd_ls_sp import requirements  # noqa: E402

TMP = Path(tempfile.mkdtemp(prefix="r5s-probe-"))


def atoms_for(text: str, name: str):
    p = TMP / f"{name}.txt"
    p.write_text(text, encoding="utf-8")
    return p, requirements.compile_requirements("goal", [str(p)])


def polarities(atoms):
    return [a["risk_guard"]["polarity"] for a in atoms]


cases = []
refusals = {}


def case(cid, expected, fn):
    try:
        exp, act, ok = fn()
        cases.append({"case_id": cid, "expected": exp, "actual": act, "verdict": "CONFIRMED" if ok else "REFUTED"})
    except Exception as exc:  # a typed refusal is a result, not a crash
        cases.append({"case_id": cid, "expected": expected, "actual": f"{type(exc).__name__}: {exc}",
                      "verdict": "UNCERTAIN" if type(exc).__name__ == "IntakeInvalid" else "REFUTED"})


def c1():
    _, a = atoms_for("系統不允許傳送個資。", "c1")
    return "1 atom, MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 1 and polarities(a) == ["MUST NOT"]


def c2():
    _, a = atoms_for("The system should not publish customer secrets.", "c2")
    return "1 atom, MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 1 and polarities(a) == ["MUST NOT"]


def c3():
    _, a = atoms_for("系統不得上傳資料。", "c3")
    return "1 atom, MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 1 and polarities(a) == ["MUST NOT"]


def c4():
    _, a = atoms_for("不得上傳個資，不得對外分享。", "c4")
    return "2 atoms, both MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 2 and set(polarities(a)) == {"MUST NOT"}


def c5():
    _, a = atoms_for("不得上傳資料，保留紀錄。", "c5")
    return "2 atoms, cue-less segment inherits MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 2 and polarities(a) == ["MUST NOT", "MUST NOT"]


def c5b():
    _, a = atoms_for("不得上傳資料，必須保留紀錄。", "c5b")
    return "2 atoms: MUST NOT then MUST (positive modal resets scope)", f"{len(a)} atom(s), {polarities(a)}", len(a) == 2 and polarities(a) == ["MUST NOT", "MUST"]


def c6():
    _, a = atoms_for("不得使用必須的憑證。", "c6")
    return "NOT refused; 1 atom MUST NOT", f"{len(a)} atom(s), {polarities(a)}", len(a) == 1 and polarities(a) == ["MUST NOT"]


def c7():
    res = []
    for name, text in (("domain", "系統不得上傳至 api.example.com。"),
                       ("version", "版本必須為 v1.2.3。"),
                       ("decimal", "限制值為 1.25。")):
        p, a = atoms_for(text, f"c7-{name}")
        src = p.read_text(encoding="utf-8")
        spans_ok = all(src[a0["source_clause"]["span"][0]:a0["source_clause"]["span"][1]] == a0["source_clause"]["source_text"] for a0 in a)
        res.append(f"{name}: {len(a)} atom(s), span_ok={spans_ok}")
    ok = all(r.endswith("1 atom(s), span_ok=True") for r in res)
    return "each input 1 atom with the original span", " | ".join(res), ok


def c8():
    _, a = atoms_for("系統必須備份資料。系統必須驗證資料。", "c8a")
    _, b = atoms_for("Do task A.Task B must run.", "c8b")
    return "2 atoms each", f"cn={len(a)} atoms, en={len(b)} atoms", len(a) == 2 and len(b) == 2


def c9():
    p, a1 = atoms_for("系統不得上傳資料，並且必須驗證紀錄。", "c9")
    a2 = requirements.compile_requirements("goal", [str(p)])
    ids1 = [x["req_id"] for x in a1]
    ids2 = [x["req_id"] for x in a2]
    src = p.read_text(encoding="utf-8")
    spans_ok = all(src[x["source_clause"]["span"][0]:x["source_clause"]["span"][1]] == x["source_clause"]["source_text"] for x in a1)
    return "identical ids on re-compile and spans match the source", f"ids_stable={ids1 == ids2}, span_ok={spans_ok}, n={len(ids1)}", ids1 == ids2 and spans_ok


def c10_ambiguous():
    try:
        atoms_for("必須上傳資料不得外洩。", "c10")
        return "typed refusal (IntakeInvalid)", "compiled without refusal", False
    except Exception as exc:
        return "typed refusal (IntakeInvalid)", f"{type(exc).__name__}", type(exc).__name__ == "IntakeInvalid"


case("C1", "1 atom, MUST NOT", c1)
case("C2", "1 atom, MUST NOT", c2)
case("C3", "1 atom, MUST NOT", c3)
case("C4", "2 atoms, both MUST NOT", c4)
case("C5", "2 atoms, cue-less inherits", c5)
case("C5b", "MUST NOT then MUST on a later positive modal", c5b)
case("C6", "not refused", c6)
case("C7", "single atom + original span", c7)
case("C8", "two real clauses split", c8)
case("C9", "stable ids + honest spans", c9)
case("C10", "ambiguous negation scope refused by type", c10_ambiguous)

env = dict(os.environ, PYTHONPATH=str(WT / "src"), PYTHONDONTWRITEBYTECODE="1")
proc = subprocess.run([PY, "-m", "unittest", "discover", "-s", "tests", "-p", "test_atomic_requirements.py", "-t", ".", "-v"],
                      cwd=str(WT), capture_output=True, text=True, env=env)
tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-4:])

summary = {
    "schema": "R5S-VERIFY-MEASUREMENT/1",
    "attribution": "ORCHESTRATOR_MEASUREMENT (separate read-only process; NOT a lane verdict and NOT model-independent)",
    "captured_utc": datetime.now(timezone.utc).isoformat(),
    "subject_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(WT), capture_output=True, text=True).stdout.strip(),
    "subject_dirty": subprocess.run(["git", "status", "--porcelain"], cwd=str(WT), capture_output=True, text=True).stdout.strip(),
    "file_sha256": {rel: __import__("hashlib").sha256((WT / rel).read_bytes()).hexdigest()
                    for rel in ("src/pipd_ls_sp/requirements.py", "tests/test_atomic_requirements.py")},
    "cases": cases,
    "unittest": {"rc": proc.returncode, "tail": tail},
    "counts": {"confirmed": sum(1 for c in cases if c["verdict"] == "CONFIRMED"),
               "refuted": sum(1 for c in cases if c["verdict"] == "REFUTED"),
               "uncertain": sum(1 for c in cases if c["verdict"] == "UNCERTAIN")},
    "claim_ceiling": "measures the named D1/D2 cases on the frozen commit and re-runs the subject's own test module; it is not an independent checker's verdict and it is not a product acceptance",
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "orchestrator_measurement_r5s.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(summary, indent=1, ensure_ascii=False))
