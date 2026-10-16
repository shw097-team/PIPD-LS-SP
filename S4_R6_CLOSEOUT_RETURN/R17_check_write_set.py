#!/usr/bin/env python3
"""Reproduce the public-plugin-verify write-set classifier locally, faithfully.

The ALLOWED / DENIED / EXCLUDED regexes and the declared stage base are READ OUT OF THE WORKFLOW FILE,
so this cannot drift from the gate it reproduces. Run it before pushing a round branch.

usage:
  check_write_set.py <repo> [<head>]
    <repo>  path to the worktree
    <head>  optional commit/ref to judge (default: HEAD)

exit 0 = the declared stage's write set contains no violation; exit 1 = a violation (same classification
the hosted job would print); exit 2 = the classifier could not be extracted (fail closed, never bless).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

WORKFLOW = ".github/workflows/public-plugin-verify.yml"


def git(repo: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.stdout


def extract(wf: str) -> dict:
    stage = re.search(r"^\s*STAGE:\s*(\S+)\s*$", wf, re.M)
    if not stage:
        raise SystemExit("STAGE_UNDECLARED in the workflow")
    st = stage.group(1)
    arm = re.search(rf"^\s*{re.escape(st)}\)\s*$(.*?)^\s*;;", wf, re.M | re.S)
    if not arm:
        raise SystemExit(f"arm {st!r} not found in the workflow")
    body = arm.group(1)
    allowed = re.search(r"ALLOWED='([^']*)'", body)
    denied = re.search(r"DENIED='([^']*)'", body)
    if not (allowed and denied):
        raise SystemExit(f"ALLOWED/DENIED not found for arm {st!r}")
    base = None
    for pat in (rf"STAGE_{st[-1].upper()}_BASE_SHA:\s*(\S+)",):
        m = re.search(pat, wf)
        if m:
            base = m.group(1)
    if base is None:
        m = re.search(r"STAGE_[A-Z]_BASE_SHA:\s*(\S+)", body)
        base = m.group(1) if m else None
    if base is None:
        raise SystemExit(f"declared base for arm {st!r} not found")
    excl = re.search(r"EXCLUDED_PREFIXES='([^']*)'", wf)
    return {"stage": st, "base": base, "allowed": allowed.group(1),
            "denied": denied.group(1), "excluded": excl.group(1) if excl else r"^$"}


def main() -> int:
    repo = sys.argv[1]
    head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    wf = (Path(repo) / WORKFLOW).read_text(encoding="utf-8")
    c = extract(wf)
    print(f"stage={c['stage']}  base={c['base']}  head={git(repo, 'rev-parse', head).strip()}")
    if subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", c["base"], head]).returncode:
        print("BASE_NOT_ANCESTOR: the declared base is not an ancestor of the subject")
        return 1
    changed = git(repo, "diff", "--name-only", f"{c['base']}...{head}").split()
    out_of_set, frozen, excluded = [], [], 0
    for p in changed:
        if re.search(c["excluded"], p):
            excluded += 1
            continue
        if re.search(c["denied"], p):
            frozen.append(p)
        elif not re.search(c["allowed"], p):
            out_of_set.append(p)
    print(f"changed={len(changed)} excluded(.hgk-like)={excluded}")
    for p in frozen:
        print("UPGRADE_WROTE_FROZEN_PATH:", p)
    for p in out_of_set:
        print("UPGRADE_WROTE_OUTSIDE_ALLOWED_SET:", p)
    ok = not frozen and not out_of_set
    print("RESULT:", "PASS (write set is inside the declared arm)" if ok else
          f"FAIL ({len(out_of_set)} outside, {len(frozen)} frozen)")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
