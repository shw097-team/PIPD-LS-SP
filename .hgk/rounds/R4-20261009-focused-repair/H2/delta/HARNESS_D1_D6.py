#!/usr/bin/env python3
"""Deterministic harness for the DELTA D1-D6 checks of the two round_envelope repairs.

Authored by the orchestrator (disclosed). It only *instruments* the checks; the judgement
belongs to the checker lane, which must review this file and re-run at least two probes by hand.

Safety: every probe operates inside a tempfile directory. The blank/whitespace destination probes
chdir into a throwaway directory first, so even a regression in the tool under test cannot reach a
real tree. This harness never touches C:/Projects/Agent_Workspace/PIPD and never touches .git.

Usage:  python -B harness_d1_d6.py            # prints one JSON blob to stdout
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

W = pathlib.Path(r"C:\w8v3delta")
REPAIRED = W / "repo" / "tools" / "round_envelope.py"
ACCEPTED = W / "frozen" / "round_envelope_ACCEPTED.py"
REPAIRED_TEST = W / "repo" / "tests" / "test_round_envelope.py"
ACCEPTED_TEST = W / "frozen" / "test_round_envelope_ACCEPTED.py"
SCRATCH = W / "scratch"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def make_repo(root: pathlib.Path) -> pathlib.Path:
    """A minimal git repo so the tool's git_head() has something to read."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    env = {**os.environ, "GIT_AUTHOR_NAME": "h", "GIT_AUTHOR_EMAIL": "h@l",
           "GIT_COMMITTER_NAME": "h", "GIT_COMMITTER_EMAIL": "h@l"}
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "commit.gpgsign=false", "commit", "-qm", "base"]):
        subprocess.run(cmd, cwd=str(root), env=env, capture_output=True)
    return root


def call_main(mod, argv, cwd: pathlib.Path | None = None):
    """Run the tool's main() in-process, capturing output, optionally from a throwaway cwd."""
    out, err = io.StringIO(), io.StringIO()
    old = os.getcwd()
    try:
        if cwd is not None:
            os.chdir(str(cwd))
        with redirect_stdout(out), redirect_stderr(err):
            code = mod.main(argv)
    finally:
        os.chdir(old)
    return code, out.getvalue(), err.getvalue()


# --------------------------------------------------------------------------- D1
def d1() -> dict:
    acc = ACCEPTED.read_text(encoding="utf-8").splitlines()
    rep = REPAIRED.read_text(encoding="utf-8").splitlines()
    sm = difflib.SequenceMatcher(None, acc, rep, autojunk=False)
    markers = {
        "defect01:normalisation": ["_norm_path", "abspath", "expanduser", "MSYS"],
        "defect01:fail_closed": ["REFUSED", "except OSError", "uncreatable"],
        "defect02:blank_guard": ["is_blank", "blank"],
        "defect02:destination_guard": ["guard_destination", "drive root", "home"],
        "defect02:announce": ["about to be removed", "removing existing destination"],
        "defect02:allow_destroy": ["allow-destroy", "allow_destroy"],
        "tests": ["def test_", "class "],
    }
    hunks, counts = [], {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        text = "\n".join(acc[i1:i2]) + "\n" + "\n".join(rep[j1:j2])
        hit = [k for k, keys in markers.items() if any(x in text for x in keys)]
        cls = ",".join(hit) if hit else "UNDISCLOSED"
        hunks.append({"op": tag, "accepted_lines": [i1 + 1, i2], "repaired_lines": [j1 + 1, j2],
                      "added": len([l for l in rep[j1:j2] if l.strip()]),
                      "removed": len([l for l in acc[i1:i2] if l.strip()]),
                      "classified_as": cls})
        for c in (hit or ["UNDISCLOSED"]):
            counts[c] = counts.get(c, 0) + 1
    src = "\n".join(rep)
    guards = {g: (g in src) for g in ["_within", "_norm_path", "_norm_path(args.dst)", "guard_paths",
                                      "guard_destination", "is_blank", "REFUSED", "allow-destroy"]}
    return {"hunks": hunks, "hunk_counts": counts,
            "undisclosed_hunks": [h for h in hunks if h["classified_as"] == "UNDISCLOSED"],
            "guards_present": guards,
            "changed_lines_total": {"accepted": len(acc), "repaired": len(rep)}}


# --------------------------------------------------------------------------- D2
def d2(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d2_", dir=str(SCRATCH)))
    src = make_repo(tmp / "src")
    # A fresh, unique destination each run: the new --allow-destroy guard rightly refuses to replace an
    # existing non-empty directory, so reusing a name would test that guard instead of the normalisation.
    name = f"probe_msys_{os.getpid()}"
    real = SCRATCH / name
    msys_dst = f"/c/w8v3delta/scratch/{name}"
    if real.exists():
        shutil.rmtree(real)
    removed_first = not real.exists()
    # The buggy behaviour anchors '/c/...' at the DRIVE ROOT, i.e. C:\c\... - so watch C:\c, not anything
    # under scratch. C:\c already exists on this host from August (pre-existing, not ours) - so the
    # decisive evidence is that its mtime does NOT move, not that it is absent.
    literal = pathlib.Path("C:/c")
    before_mtime = literal.stat().st_mtime if literal.exists() else None
    code, out, err = call_main(mod, ["init", "--src", str(src), "--dst", msys_dst,
                                     "--scratch", str(tmp / "scr")])
    after_mtime = literal.stat().st_mtime if literal.exists() else None
    return {"exit": code, "destination_removed_first": removed_first,
            "created_at_drive_path": real.is_dir(),
            "msys_dst_argument": msys_dst, "resolved_expected": str(real),
            "drive_root_c_path": str(literal), "drive_root_c_pre_existing": before_mtime is not None,
            "drive_root_c_mtime_moved": (before_mtime != after_mtime),
            "verdict_note": "MSYS-style --dst must land on C:/w8v3delta/... and must NOT write into C:\\c",
            "stderr_head": err.strip().splitlines()[:2]}


# --------------------------------------------------------------------------- D3
def d3(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d3_", dir=str(SCRATCH)))
    src = make_repo(tmp / "src")
    blocker = tmp / "blocker"
    blocker.write_text("x", encoding="utf-8")          # a FILE where a directory is needed
    bad = blocker / "child" / ("deep" * 3)             # cannot be created
    code, out, err = call_main(mod, ["init", "--src", str(src), "--dst", str(bad),
                                     "--scratch", str(tmp / "scr")])
    return {"exit": code, "single_refusal_line": len(err.strip().splitlines()) == 1,
            "names_path": "REFUSED" in err, "traceback_printed": "Traceback" in err,
            "stderr": err.strip()[:400]}


# --------------------------------------------------------------------------- D4
def d4(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d4_", dir=str(SCRATCH)))
    src = make_repo(tmp / "src")
    cases = {}
    # dst inside src
    cases["dst_inside_src"] = call_main(mod, ["init", "--src", str(src), "--dst", str(src / "copy"),
                                              "--scratch", str(tmp / "s1")])[0]
    # src inside dst
    cases["src_inside_dst"] = call_main(mod, ["init", "--src", str(src), "--dst", str(tmp),
                                              "--scratch", str(tmp / "s2")])[0]
    # scratch inside tree
    cases["scratch_inside_tree"] = call_main(mod, ["init", "--src", str(src),
                                                   "--dst", str(tmp / "copy2"),
                                                   "--scratch", str(src / "scr")])[0]
    # baseline: the ACCEPTED suite against the ACCEPTED tool, in a temp dir where the accepted module
    # is importable under the name the tests expect (`import round_envelope as E`).
    base = pathlib.Path(tempfile.mkdtemp(prefix="d4base_", dir=str(SCRATCH)))
    shutil.copy2(ACCEPTED, base / "round_envelope.py")
    shutil.copy2(ACCEPTED_TEST, base / "test_accepted_baseline.py")
    run2 = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_accepted_baseline", "-v"],
                          cwd=str(base), capture_output=True, text=True,
                          env={**os.environ, "PYTHONPATH": str(base), "PYTHONHOME": ""})
    txt = (run2.stderr or "") + (run2.stdout or "")
    tail2 = [l for l in txt.splitlines() if l.startswith(("Ran", "OK", "FAILED"))]
    return {"refusal_exit_codes": cases, "all_refused": all(v == 2 for v in cases.values()),
            "accepted_baseline_exit": run2.returncode, "accepted_suite_result": tail2}


# --------------------------------------------------------------------------- D5
def d5() -> dict:
    run = subprocess.run([sys.executable, "-B", "-m", "unittest", "tests.test_round_envelope", "-v"],
                         cwd=str(W / "repo"), capture_output=True, text=True,
                         env={**os.environ, "PYTHONPATH": "", "PYTHONHOME": ""})
    txt = (run.stderr or "") + (run.stdout or "")
    lines = [l for l in txt.splitlines() if l.startswith(("Ran", "OK", "FAILED"))]
    return {"exit": run.returncode, "summary": lines, "failures": [l for l in txt.splitlines() if l.startswith(("FAIL:", "ERROR:"))][:5]}


# --------------------------------------------------------------------------- D6
def d6(mod) -> dict:
    """Each probe runs from inside a throwaway cwd so a regression cannot reach anything real."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d6_", dir=str(SCRATCH)))
    outside = tmp / "outside"          # a disposable 'outside' tree to use as --src
    src = make_repo(outside / "src")
    throw = tmp / "throwcwd"           # the cwd for destructive probes
    throw.mkdir()
    res: dict = {}

    def probe(name, argv, cwd, allow=False):
        a = list(argv)
        if allow:
            a.append("--allow-destroy")
        code, out, err = call_main(mod, a, cwd=cwd)
        res[name] = {"exit": code, "refused": "REFUSED" in err, "traceback": "Traceback" in err,
                     "stderr_head": err.strip().splitlines()[:1]}
        return code

    ok = []
    ok.append(probe("blank_dst", ["init", "--src", str(src), "--dst", "", "--scratch", str(tmp / "s")], throw) == 2)
    ok.append(probe("whitespace_dst", ["init", "--src", str(src), "--dst", "   ", "--scratch", str(tmp / "s")], throw) == 2)
    ok.append(probe("blank_dst_with_allow_destroy", ["init", "--src", str(src), "--dst", "", "--scratch", str(tmp / "s")], throw, allow=True) == 2)
    ok.append(probe("dst_equals_cwd", ["init", "--src", str(src), "--dst", str(throw), "--scratch", str(tmp / "s")], throw) == 2)
    ok.append(probe("dst_equals_src", ["init", "--src", str(src), "--dst", str(src), "--scratch", str(tmp / "s")], throw) == 2)
    ok.append(probe("dst_ancestor_of_src", ["init", "--src", str(src), "--dst", str(outside), "--scratch", str(tmp / "s")], throw) == 2)
    ok.append(probe("dst_ancestor_with_allow_destroy", ["init", "--src", str(src), "--dst", str(outside), "--scratch", str(tmp / "s")], throw, allow=True) == 2)
    ok.append(probe("dst_home", ["init", "--src", str(src), "--dst", str(pathlib.Path.home()), "--scratch", str(tmp / "s")], throw) == 2)
    # positive control: a legitimate destination must still succeed
    good = tmp / "legit" / "copy"
    pcode, pout, perr = call_main(mod, ["init", "--src", str(src), "--dst", str(good), "--scratch", str(tmp / "s")], cwd=throw)
    res["positive_control"] = {"exit": pcode, "created": good.is_dir(), "stderr_head": perr.strip().splitlines()[:1]}
    ok.append(pcode == 0 and good.is_dir())
    res["all_guards_held"] = all(ok)
    res["throwaway_cwd_intact"] = throw.is_dir()
    res["src_intact"] = src.is_dir()
    return res


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    rep_mod = load(REPAIRED, "re_under_test")
    result = {
        "harness": "PIPD-DELTA-HARNESS/1",
        "authored_by": "orchestrator (disclosed) - the checker must review this file and re-run >=2 probes by hand",
        "subject": {"repaired_tool": {"path": str(REPAIRED), "sha256": sha(REPAIRED)},
                    "accepted_tool": {"path": str(ACCEPTED), "sha256": sha(ACCEPTED)},
                    "repaired_test": {"path": str(REPAIRED_TEST), "sha256": sha(REPAIRED_TEST)},
                    "accepted_test": {"path": str(ACCEPTED_TEST), "sha256": sha(ACCEPTED_TEST)}},
        "D1": d1(), "D2": d2(rep_mod), "D3": d3(rep_mod), "D4": d4(rep_mod), "D5": d5(), "D6": d6(rep_mod),
    }
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
