#!/usr/bin/env python3
"""DELTA harness v4 for the round_envelope repairs - rewritten to answer every false-pass risk the
independent checker raised against v3.

Authored by the orchestrator (disclosed). v3 was rejected by the checker as an acceptance oracle; the
specific faults it named, and how v4 answers them:

  * "D6 passes Path.home() as --dst; a guard regression can reach the real home"
        -> v4 NEVER passes a real home or drive root to a destructive path. Dangerous destinations
           (home, drive root, cwd, src, ancestor) are tested against the PURE guard functions
           (is_blank / guard_destination / guard_paths), which cannot delete anything. End-to-end
           probes run only with disposable destinations.
  * "Imports and test subprocesses have no deletion confinement"
        -> every end-to-end probe is wrapped in assert_sandbox(); a destination outside the sandbox
           aborts the probe instead of running it.
  * "D2 watches only C:\\c root mtime, not descendants"
        -> v4 takes a RECURSIVE manifest (relative path -> size, mtime_ns, is_dir) before and after and
           diffs it, on both C:\\c and the probe trees.
  * "D4/D6 check exit codes, not diagnostics or no deletion/recreation"
        -> v4 asserts the diagnostic text names the path, and proves (manifest equality) that nothing
           was deleted or recreated.
  * "D6 is_dir cannot prove tree preservation; drive-root refusal untested; fixture git ignores failures"
        -> manifests for preservation, a drive-root refusal unit probe, fixture git return codes asserted.
  * "D1 substring classification can hide unrelated changes"
        -> v4 maps every hunk to the enclosing functions/classes and flags any hunk touching code
           outside the declared repair regions.
  * "passing tests alone cannot rule out test weakening"
        -> v5 adds a test-source audit: pre-existing test names must survive and their assertion counts
           must not shrink.

Usage: python -B harness_d1_d6_v4.py   -> one JSON blob on stdout
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

W = pathlib.Path(r"C:\w8v3delta")
SANDBOX = W / "scratch"
REPAIRED = W / "repo" / "tools" / "round_envelope.py"
ACCEPTED = W / "frozen" / "round_envelope_ACCEPTED.py"
REPAIRED_TEST = W / "repo" / "tests" / "test_round_envelope.py"
ACCEPTED_TEST = W / "frozen" / "test_round_envelope_ACCEPTED.py"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


LAST_TRUNCATED = False


def manifest(root: pathlib.Path, max_entries: int = 60000) -> dict:
    """Recursive (relpath -> (size, mtime_ns, is_dir)) snapshot. Proves 'untouched' for descendants too."""
    global LAST_TRUNCATED
    root = pathlib.Path(root)
    out, n, truncated = {}, 0, False
    if not root.exists():
        LAST_TRUNCATED = False
        return out
    for dirpath, dirnames, filenames in os.walk(root):
        for name in list(dirnames) + list(filenames):
            p = pathlib.Path(dirpath) / name
            try:
                st = p.lstat()
            except OSError:
                continue
            out[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns, stat.S_ISDIR(st.st_mode))
            n += 1
            if n >= max_entries:
                LAST_TRUNCATED = True
                return out
    LAST_TRUNCATED = truncated
    return out


def manifest_diff(before: dict, after: dict) -> dict:
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    return {"added": added[:20], "removed": removed[:20], "changed": changed[:20],
            "counts": {"added": len(added), "removed": len(removed), "changed": len(changed)},
            "identical": not (added or removed or changed)}


def assert_sandbox(p) -> bool:
    """Instrument self-protection: never let a probe aim outside the sandbox."""
    try:
        pathlib.Path(p).resolve().relative_to(SANDBOX.resolve())
        return True
    except (ValueError, OSError):
        return False


def make_repo(root: pathlib.Path) -> tuple[pathlib.Path, dict]:
    root.mkdir(parents=True, exist_ok=True)
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    env = {**os.environ, "GIT_AUTHOR_NAME": "h", "GIT_AUTHOR_EMAIL": "h@l",
           "GIT_COMMITTER_NAME": "h", "GIT_COMMITTER_EMAIL": "h@l"}
    codes = {}
    for label, cmd in (("init", ["git", "init", "-q"]), ("add", ["git", "add", "-A"]),
                       ("commit", ["git", "-c", "commit.gpgsign=false", "commit", "-qm", "base"])):
        r = subprocess.run(cmd, cwd=str(root), env=env, capture_output=True)
        codes[label] = r.returncode
    if any(v != 0 for v in codes.values()):
        raise RuntimeError(f"fixture git failed: {codes}")
    return root, codes


def call_main(mod, argv, cwd=None):
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


# ---------------------------------------------------------------- D1 (semantic hunk mapping)
# The declaration is the repair RECORDS, not a guess: H2_DEFECT_01_REPAIR.json declares the
# normalisation + fail-closed work and says "init scratch-write and snapshot out-write are guarded the
# same way"; H2_DEFECT_02_REPAIR.json declares STOP-1..STOP-5, the new helpers and the module docstring,
# and states that only init destroys a directory (so snapshot/verify needed no destination guard).
DECLARED = {"_norm_path", "guard_paths", "is_blank", "is_fs_root", "guard_destination",
            "cmd_init", "_within", "_build_parser", "main",
            "cmd_snapshot", "cmd_verify", "<module>"}


def _spans(lines):
    spans, cur = [], None
    for i, l in enumerate(lines):
        if re.match(r"^(def |class |async def )", l):
            if cur:
                spans.append((cur[0], cur[1], i - 1))
            nm = l.split("(")[0].replace("def ", "").replace("class ", "").strip()
            cur = (nm, i)
    if cur:
        spans.append((cur[0], cur[1], len(lines) - 1))
    return spans


def _enclosing(spans, i1, i2):
    hit = [n for n, s, e in spans if not (e < i1 or s > i2)]
    return hit or ["<module>"]


def d1() -> dict:
    acc, rep = ACCEPTED.read_text(encoding="utf-8").splitlines(), REPAIRED.read_text(encoding="utf-8").splitlines()
    sa, sr = _spans(acc), _spans(rep)
    sm = difflib.SequenceMatcher(None, acc, rep, autojunk=False)
    hunks, undisclosed = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        fn_acc = _enclosing(sa, i1, max(i1, i2 - 1))
        fn_rep = _enclosing(sr, j1, max(j1, j2 - 1))
        touched = set(fn_acc) | set(fn_rep)
        scope = "declared" if touched <= DECLARED else "UNDISCLOSED"
        h = {"op": tag, "accepted": [i1 + 1, i2], "repaired": [j1 + 1, j2],
             "functions_touched": sorted(touched), "scope": scope,
             "removed_lines": len([l for l in acc[i1:i2] if l.strip()]),
             "added_lines": len([l for l in rep[j1:j2] if l.strip()]),
             "removed_text": [l.strip() for l in acc[i1:i2] if l.strip()][:12],
             "added_text": [l.strip() for l in rep[j1:j2] if l.strip()][:12]}
        hunks.append(h)
        if scope == "UNDISCLOSED":
            undisclosed.append(h)
    rep_src = "\n".join(rep)
    guards = {g: (g in rep_src) for g in
              sorted(DECLARED | {"_norm_path(args.dst)", "guard_destination(src, dst)", "is_blank("})}
    return {"hunk_count": len(hunks), "hunks": hunks, "undisclosed_hunks": undisclosed,
            "unsafe_function_hunks": [h for h in hunks if h["functions_touched"] != ["cmd_init"]
                                      and not set(h["functions_touched"]) & DECLARED],
            "guards_referenced_in_source": guards,
            "note": "scope is now decided by which FUNCTIONS a hunk touches, not by keyword presence"}


# ---------------------------------------------------------------- D2 (normalisation; recursive manifest)
def d2(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d2_", dir=str(SANDBOX)))
    src, _ = make_repo(tmp / "src")
    name = f"probe_msys_{os.getpid()}"
    # Derive the expected native path from the MSYS string exactly as the tool must, so a normalisation
    # regression cannot make the harness watch a different place from the one it creates.
    msys = f"/c/w8v3delta/scratch/{name}"
    real = pathlib.Path(msys.replace("/c/", "C:/", 1))
    if not assert_sandbox(real):                     # assert FIRST ...
        return {"aborted": "destination escaped the sandbox", "destination": str(real)}
    pre_existed = real.exists()
    if pre_existed:
        shutil.rmtree(real)                          # ... and only then delete
    post_rm = real.exists()
    literal = pathlib.Path("C:/c")
    before = manifest(literal); trunc_b = LAST_TRUNCATED
    code, out, err = call_main(mod, ["init", "--src", str(src), "--dst", msys, "--scratch", str(tmp / "scr")])
    after = manifest(literal); trunc_a = LAST_TRUNCATED
    # a normalisation regression would have created C:\c\w8v3delta\... - check that landing zone explicitly
    regression_landing = pathlib.Path("C:/c") / "w8v3delta"
    return {"exit": code, "created_at_drive_path": real.is_dir(), "destination": str(real),
            "msys_argument_passed": msys, "destination_pre_existed": pre_existed, "removed_before_run": post_rm is False,
            "normalisation_regression_landing_created": regression_landing.exists(),
            "drive_root_c_manifest_identical": manifest_diff(before, after)["identical"],
            "drive_root_c_manifest_diff": manifest_diff(before, after)["counts"],
            "drive_root_c_entries": len(before), "manifest_truncated": trunc_b or trunc_a,
            "c_pre_existing": literal.exists(), "stderr_head": err.strip().splitlines()[:2]}


# ---------------------------------------------------------------- D3 (fail-closed diagnostics)
def d3(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d3_", dir=str(SANDBOX)))
    src, _ = make_repo(tmp / "src")
    blocker = tmp / "blocker"
    blocker.write_text("x", encoding="utf-8")
    bad = blocker / "child" / "deep"
    before = manifest(tmp)
    code, out, err = call_main(mod, ["init", "--src", str(src), "--dst", str(bad), "--scratch", str(tmp / "scr")])
    lines = [l for l in err.strip().splitlines() if l.strip()]
    return {"exit": code, "line_count": len(lines), "names_the_path": str(bad) in err,
            "has_REFUSED": "REFUSED" in err, "traceback_printed": "Traceback" in err,
            "no_tree_created_at_bad_path": not bad.exists(),
            "stderr": err.strip()[:300],
            "src_untouched": manifest_diff(before, manifest(tmp))["identical"]}


# ---------------------------------------------------------------- D4 (existing refusals still fire)
def d4(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d4_", dir=str(SANDBOX)))
    src, gitcodes = make_repo(tmp / "src")
    cases = {}
    for label, dst, scratch in (("dst_inside_src", src / "copy", tmp / "s1"),
                                ("src_inside_dst", tmp, tmp / "s2"),
                                ("scratch_inside_tree", tmp / "copy2", src / "scr")):
        if not assert_sandbox(dst if label != "src_inside_dst" else tmp):
            cases[label] = {"aborted": "escaped sandbox"}
            continue
        before = manifest(tmp)
        code, out, err = call_main(mod, ["init", "--src", str(src), "--dst", str(dst), "--scratch", str(scratch)])
        after = manifest(tmp)
        cases[label] = {"exit": code, "has_REFUSED": "REFUSED" in err, "traceback": "Traceback" in err,
                        "src_manifest_unchanged": manifest_diff(before, after)["identical"]}
    base = pathlib.Path(tempfile.mkdtemp(prefix="d4base_", dir=str(SANDBOX)))
    shutil.copy2(ACCEPTED, base / "round_envelope.py")
    shutil.copy2(ACCEPTED_TEST, base / "test_accepted_baseline.py")
    run2 = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_accepted_baseline"],
                          cwd=str(base), capture_output=True, text=True,
                          env={**os.environ, "PYTHONPATH": str(base), "PYTHONHOME": ""})
    txt = (run2.stderr or "") + (run2.stdout or "")
    return {"refusals": cases, "all_refused_with_exit_2": all(c.get("exit") == 2 for c in cases.values()),
            "accepted_baseline_exit": run2.returncode,
            "accepted_baseline_summary": [l for l in txt.splitlines() if l.startswith(("Ran", "OK", "FAILED"))],
            "fixture_git_returncodes": gitcodes}


# ---------------------------------------------------------------- D5 (suite + TEST-SOURCE weakening audit)
def _test_facts(path: pathlib.Path) -> dict:
    src = path.read_text(encoding="utf-8")
    names = re.findall(r"def (test_[A-Za-z0-9_]+)", src)
    blocks = re.split(r"\n(?=    def test_)", src)
    asserts = {}
    for b in blocks:
        m = re.match(r"\s*def (test_[A-Za-z0-9_]+)", b)
        if m:
            asserts[m.group(1)] = len(re.findall(r"\bself\.assert\w*\(|\bassert\b", b))
    return {"names": names, "assert_counts": asserts, "sha256": sha(path)}


def d5() -> dict:
    run = subprocess.run([sys.executable, "-B", "-m", "unittest", "tests.test_round_envelope", "-v"],
                         cwd=str(W / "repo"), capture_output=True, text=True,
                         env={**os.environ, "PYTHONPATH": "", "PYTHONHOME": ""})
    txt = (run.stderr or "") + (run.stdout or "")
    acc, rep = _test_facts(ACCEPTED_TEST), _test_facts(REPAIRED_TEST)
    missing = [n for n in acc["names"] if n not in rep["names"]]
    shrunk = {n: [acc["assert_counts"][n], rep["assert_counts"][n]]
              for n in acc["names"] if n in rep["assert_counts"]
              and rep["assert_counts"].get(n, 0) < acc["assert_counts"][n]}
    return {"exit": run.returncode,
            "summary": [l for l in txt.splitlines() if l.startswith(("Ran", "OK", "FAILED"))],
            "failure_lines": [l for l in txt.splitlines() if l.startswith(("FAIL:", "ERROR:"))][:5],
            "weakening_audit": {"accepted_tests": len(acc["names"]), "repaired_tests": len(rep["names"]),
                                "added": sorted(set(rep["names"]) - set(acc["names"])),
                                "removed_preexisting": missing, "assertions_shrunk": shrunk,
                                "no_test_removed": not missing, "no_assertion_shrunk": not shrunk},
            "test_file_sha256": {"accepted": acc["sha256"], "repaired": rep["sha256"]}}


# ---------------------------------------------------------------- D6 (dangerous destinations, safely)
def d6(mod) -> dict:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="d6_", dir=str(SANDBOX)))
    src, _ = make_repo(tmp / "outside" / "src")
    throw = tmp / "throwcwd"
    throw.mkdir()
    throw_manifest_before = manifest(throw)
    home = pathlib.Path.home().resolve()
    root = pathlib.Path(pathlib.Path.home().anchor).resolve()      # e.g. C:\

    # --- UNIT probes: pure guard functions, zero destruction risk ---------------------------------
    unit = {}
    # NOTE: the cwd probe must use the LIVE process cwd - guard_destination compares against
    # Path.cwd(), so passing an arbitrary directory would not exercise that branch.
    for label, target in (("home", home), ("drive_root", root), ("cwd", pathlib.Path.cwd()),
                          ("equals_src", src), ("ancestor_of_src", tmp / "outside")):
        exc_name = None
        try:
            probs = mod.guard_destination(src, pathlib.Path(target)) + mod.guard_paths(
                src, pathlib.Path(target), tmp / "scr")
        except Exception as exc:  # noqa: BLE001
            probs, exc_name = [], exc.__class__.__name__
        unit[label] = {"target": str(target), "problems": probs[:3],
                       "refused": bool(probs), "exception": exc_name,
                       "refused_by_a_real_problem": bool(probs) and exc_name is None}
    unit["blank"] = {"is_blank('')": bool(mod.is_blank("")), "is_blank('   ')": bool(mod.is_blank("   ")),
                     "is_blank('x')": bool(mod.is_blank("x"))}

    # --- E2E probes: disposable destinations only, manifest-proven ---------------------------------
    e2e = {}

    def probe(label, dst, allow=False, cwd=throw):
        d = pathlib.Path(dst) if dst not in ("", "   ") else None
        if d is not None and not assert_sandbox(d):
            e2e[label] = {"aborted": "destination outside sandbox - probe not run", "target": str(d)}
            return
        argv = ["init", "--src", str(src), "--dst", dst, "--scratch", str(tmp / "s")]
        if allow:
            argv.append("--allow-destroy")
        before = manifest(tmp)
        code, out, err = call_main(mod, argv, cwd=cwd)
        after = manifest(tmp)
        e2e[label] = {"exit": code, "has_REFUSED": "REFUSED" in err, "traceback": "Traceback" in err,
                      "nothing_deleted_or_recreated": manifest_diff(before, after)["identical"],
                      "stderr_head": err.strip().splitlines()[:1]}

    probe("blank_dst", "")
    probe("whitespace_dst", "   ")
    probe("blank_dst_with_allow_destroy", "", allow=True)
    probe("dst_equals_cwd", str(throw))
    probe("dst_equals_src", str(src))
    probe("dst_ancestor_of_src", str(tmp / "outside"))
    probe("dst_ancestor_with_allow_destroy", str(tmp / "outside"), allow=True)
    legit = tmp / "legit" / "copy"
    lcode, lout, lerr = call_main(mod, ["init", "--src", str(src), "--dst", str(legit), "--scratch", str(tmp / "s")],
                                  cwd=throw)
    e2e["positive_control"] = {"exit": lcode, "created": legit.is_dir(),
                               "failed_means_guards_too_strict": lcode != 0}

    return {"unit_probes_no_destruction_risk": unit,
            "unit_all_refused": all(unit[k]["refused"] for k in ("home", "drive_root", "cwd", "equals_src",
                                                                 "ancestor_of_src")),
            "e2e_probes_disposable_only": e2e,
            "e2e_all_held": all(v.get("exit") == 2 and v.get("nothing_deleted_or_recreated", False)
                                and v.get("has_REFUSED") and not v.get("traceback")
                                for k, v in e2e.items() if k != "positive_control"),
            "positive_control_ok": e2e["positive_control"]["exit"] == 0 and e2e["positive_control"]["created"],
            "throwaway_cwd_intact": manifest_diff(throw_manifest_before, manifest(throw))["identical"],
            "real_home_never_passed_to_a_destructive_path": True,
            "drive_root_never_passed_to_a_destructive_path": True}


def main() -> int:
    SANDBOX.mkdir(parents=True, exist_ok=True)
    mod = load(REPAIRED, "re_under_test")
    subject = {"repaired_tool": {"path": str(REPAIRED), "sha256": sha(REPAIRED)},
               "accepted_tool": {"path": str(ACCEPTED), "sha256": sha(ACCEPTED)},
               "repaired_test": {"sha256": sha(REPAIRED_TEST)},
               "accepted_test": {"sha256": sha(ACCEPTED_TEST)}}
    print(json.dumps({"harness": "PIPD-DELTA-HARNESS/5",
                      "authored_by": "orchestrator (disclosed) - checker must review and reproduce >=2 probes by hand",
                      "supersedes": "HARNESS_D1_D6.py (v3) and harness_d1_d6_v4.py - both named deficient by the independent checker", "v5_changes": "D2 asserts the sandbox BEFORE deleting and derives the native path from the MSYS string; fixture git codes asserted; an exception is no longer counted as a refusal; the e2e aggregate also requires the REFUSED diagnostic and no traceback; per-hunk removed/added TEXT emitted so the checker can judge semantics",
                      "subject": subject,
                      "D1": d1(), "D2": d2(mod), "D3": d3(mod), "D4": d4(mod), "D5": d5(), "D6": d6(mod)},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
