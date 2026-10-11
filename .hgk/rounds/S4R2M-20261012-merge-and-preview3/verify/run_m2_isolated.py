#!/usr/bin/env python3
"""S4R2M Gate M2 — isolated focused regression on a disposable writable clone.

Why a clone: a suite that writes ``.pyc.tmp`` beside modules mutates its own subject, and the
independent checker refused to do exactly that on the frozen tree. So the subject of record here is
the candidate worktree, which is only ever *read*; the six named affected modules plus the neighbouring
positives run in a disposable clone built from the same commit, and the subject's digests are compared
before and after.

Everything this script writes goes to the round's evidence directory. Nothing is written into the
subject or into the clone's git history.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SUBJECT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt")
ROUND = SUBJECT / ".hgk/rounds/S4R2M-20261012-merge-and-preview3"
OUT = ROUND / "verify"
CLONE = Path("C:/Projects/Agent_Workspace/var/s4r2m-m2-clone")
PY = Path("C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe")

CANDIDATE = "58a1f334464675081d0573476d70e2165143bdd8"

MODULES = [
    "test_s4r2_affected_only.py",
    "test_postrelease_contract_hardening.py",
    "test_postrelease_quickstart.py",
    "test_postrelease_web_mount.py",
    "test_postrelease_selfbootstrap.py",
    "test_first_run_examples.py",
    "test_ce_repair_regression.py",
    "test_wheel_distribution.py",
    "test_s4r2m_docs_route.py",
]

EXACT_SET = {
    "schemas_and_registry": 20,   # 19 *.schema.json families + registry.json
    "skill_dirs": 8,
    "cli_commands": 13,
}


def run(cmd, cwd, env_extra=None, timeout=1800):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
    if env_extra:
        env.update(env_extra)
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout, env=env)
    return {"cmd": [str(c) for c in cmd], "exit": p.returncode,
            "seconds": round(time.time() - t0, 2),
            "stdout_tail": p.stdout[-1500:], "stderr_tail": p.stderr[-1500:]}


def git(*args, cwd=SUBJECT):
    p = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.stdout.strip()


def snapshot_tree(root: Path) -> dict:
    """Digest every tracked file: this is the read-only subject's byte identity."""
    files = git("ls-tree", "-r", "--name-only", "HEAD").splitlines()
    out = {}
    for rel in files:
        p = root / rel
        if p.is_file():
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    rec: dict = {
        "schema": "PIPD-S4R2M-M2-ISOLATED-REGRESSION/1",
        "round": "S4R2M-20261012-merge-and-preview3",
        "candidate_head": head, "candidate_tree": tree,
        "candidate_head_expected": CANDIDATE,
        "candidate_head_matches": head == CANDIDATE,
        "subject_root": str(SUBJECT), "clone_root": str(CLONE),
        "interpreter": str(PY),
        "claim_ceiling_note": "a green maker-side suite in a writable clone is NOT independent acceptance",
    }

    # 1. subject bytes BEFORE
    before = snapshot_tree(SUBJECT)
    rec["subject_files"] = len(before)
    rec["subject_digest_before"] = hashlib.sha256(
        json.dumps(before, sort_keys=True).encode()).hexdigest()

    # 2. disposable writable clone from the candidate commit
    if CLONE.exists():
        shutil.rmtree(CLONE, ignore_errors=True)
    CLONE.parent.mkdir(parents=True, exist_ok=True)
    rec["clone_create"] = run(["git", "clone", "--no-hardlinks", "--quiet",
                               str(SUBJECT), str(CLONE)], cwd=CLONE.parent)
    rec["clone_checkout"] = run(["git", "checkout", "--quiet", head], cwd=CLONE)
    rec["clone_head"] = git("rev-parse", "HEAD", cwd=CLONE)
    rec["clone_is_byte_equivalent"] = run(
        ["git", "diff", "--stat", head, "--"], cwd=CLONE)["stdout_tail"].strip() == ""

    # 3. affected modules in the clone
    envsrc = {"PYTHONPATH": str(CLONE / "src")}
    rec["modules"] = {}
    for m in MODULES:
        r = run([str(PY), "-m", "unittest", "discover", "-s", "tests", "-p", m, "-v"], CLONE, envsrc)
        tail = [ln for ln in r["stdout_tail"].splitlines() if ln.strip().startswith("Ran ")
                or ln.strip() in ("OK", "FAILED")]
        rec["modules"][m] = {"exit": r["exit"], "seconds": r["seconds"],
                             "summary": " | ".join(tail[-2:]) if tail else r["stdout_tail"][-200:],
                             "stderr_tail": r["stderr_tail"][-400:]}
        (OUT / f"M2_{m}.log").write_text(r["stdout_tail"] + "\n--- STDERR ---\n" + r["stderr_tail"],
                                         encoding="utf-8")

    # 4. exact-set oracle
    schemas = sorted(p.name for p in (CLONE / "schemas").glob("*.schema.json"))
    registry_present = (CLONE / "schemas" / "registry.json").is_file()
    skill_dirs = sorted(p.name for p in (CLONE / "skills").iterdir() if p.is_dir())
    help_run = run([str(PY), "-m", "pipd_ls_sp.cli", "--help"], CLONE, envsrc)
    import re
    m = re.search(r"\{([a-z\-,]+)\}", help_run["stdout_tail"] or "")
    cli = sorted(m.group(1).split(",")) if m else []
    rec["exact_set"] = {
        "schemas_count": len(schemas), "registry_present": registry_present,
        "schemas_and_registry": len(schemas) + (1 if registry_present else 0),
        "expected_schemas_and_registry": EXACT_SET["schemas_and_registry"],
        "skill_dirs_count": len(skill_dirs), "expected_skill_dirs": EXACT_SET["skill_dirs"],
        "skill_dirs": skill_dirs,
        "cli_count": len(cli), "expected_cli": EXACT_SET["cli_commands"], "cli": cli,
    }
    rec["exact_set_ok"] = (
        rec["exact_set"]["schemas_and_registry"] == EXACT_SET["schemas_and_registry"]
        and len(skill_dirs) == EXACT_SET["skill_dirs"]
        and len(cli) == EXACT_SET["cli_commands"])

    # 5. four early ProfileBinding mutants + the legal record, via the real validator
    probe_src = (
        "import json,sys\n"
        "sys.path.insert(0,r'%s')\n"
        "from pipd_ls_sp import pipeline, validate\n"
        "rec,_=pipeline.profile_record('LITE',['intent'])\n"
        "rec=json.loads(json.dumps(rec))\n"
        "out={}\n"
        "legal=validate.validate_record('ProfileBinding',rec,r'%s')\n"
        "out['legal_exit']=0 if not legal else 1\n"
        "out['legal_findings']=legal\n"
        "for name,val in [('axes_str','intent'),('axes_int_item',['intent',42]),('profile_int',42),('vetoes_str','veto')]:\n"
        "    r2=json.loads(json.dumps(rec))\n"
        "    r2[{'axes_str':'axes','axes_int_item':'axes','profile_int':'profile','vetoes_str':'vetoes'}[name]]=val\n"
        "    f=validate.validate_record('ProfileBinding',r2,r'%s')\n"
        "    out[name]={'exit':0 if not f else 1,'findings':f[:2]}\n"
        "print(json.dumps(out))\n"
    ) % (str(CLONE / "src"), str(CLONE / "schemas"), str(CLONE / "schemas"))
    (OUT / "M2_mutant_probe.py").write_text(probe_src, encoding="utf-8")
    pr = run([str(PY), str(OUT / "M2_mutant_probe.py")], CLONE, envsrc)
    try:
        rec["profile_mutants"] = json.loads(pr["stdout_tail"].strip().splitlines()[-1])
    except Exception:
        rec["profile_mutants"] = {"raw": pr["stdout_tail"][-800:], "stderr": pr["stderr_tail"][-400:]}

    # 6. subject bytes AFTER
    after = snapshot_tree(SUBJECT)
    rec["subject_digest_after"] = hashlib.sha256(json.dumps(after, sort_keys=True).encode()).hexdigest()
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    rec["subject_unchanged"] = not changed
    rec["subject_changed_paths"] = changed
    rec["git_status_subject"] = git("status", "--porcelain=v1")
    rec["candidate_receipt_all_modules_exit0"] = all(v["exit"] == 0 for v in rec["modules"].values())

    (OUT / "M2_ISOLATED_REGRESSION.json").write_text(
        json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: rec[k] for k in (
        "candidate_head_matches", "clone_head", "clone_is_byte_equivalent", "subject_files",
        "exact_set_ok", "subject_unchanged", "subject_changed_paths",
        "candidate_receipt_all_modules_exit0")}, indent=1))
    for m, v in rec["modules"].items():
        print(f"  {m:44s} exit={v['exit']}  {v['summary']}")
    print("mutants:", json.dumps(rec["profile_mutants"], ensure_ascii=False)[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
