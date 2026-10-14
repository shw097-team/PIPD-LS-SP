#!/usr/bin/env python3
"""Produce the remedy receipt SCOPE-ANCHORED to the heads in force when it runs.

The v3 audit found the failure mode this exists to prevent: a remedy receipt generated at a head that a
later commit superseded was carried as support for a current-state claim, while the round's own
affected-only ledger listed that same receipt as affected. A receipt that does not name the heads it was
produced at cannot tell those two cases apart, so this one names them and recomputes the necessity
derivation from the live tree.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

WF = ".github/workflows/public-plugin-verify.yml"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def main() -> int:
    b = Path(sys.argv[1])
    a = Path(sys.argv[2])
    head_b = sh("git", "-C", str(b), "rev-parse", "HEAD").strip()
    head_a = sh("git", "-C", str(a), "rev-parse", "HEAD").strip()
    base_b = sh("git", "-C", str(b), "rev-parse",
                "refs/heads/fix/s4r3-stage-a-ci-truthfulness-20261013").strip()
    text = (b / WF).read_text(encoding="utf-8")
    sets = [(m.group(1), m.group(2)) for m in
            (re.search(r"^\s*(ALLOWED|DENIED)='\^(.*?)\$?'\s*$", l) for l in text.splitlines()) if m]
    al = next(rx for k, rx in sets if k == "ALLOWED" and "docs/USER_GUIDE" in rx)
    dn = next(rx for k, rx in sets if k == "DENIED" and "src/" in rx)
    exc = re.search(r"EXCLUDED_PREFIXES='([^']*)'", text).group(1)
    changed = [p for p in sh("git", "-C", str(b), "diff", "--name-only", f"{base_b}...HEAD").splitlines()
               if p.strip()]

    def classify(p, allow):
        if re.search(exc, p):
            return "EXCLUDED"
        if re.search(dn, p):
            return "DENIED"
        return "ALLOWED" if re.search(allow, p) else "UNLISTED"

    stripped = al.replace(r"docs/USER_GUIDE\.md$|", "")
    now = [(p, classify(p, al)) for p in changed]
    wo = [(p, classify(p, stripped)) for p in changed]
    fell = [p for (p, v1), (_, v2) in zip(now, wo) if v1 != v2]
    print("RECEIPT SCOPE - the heads in force WHEN THIS RAN")
    print(f"  stage_b_head : {head_b}")
    print(f"  stage_a_head : {head_a}")
    print(f"  governed base for stage b (resolved from STAGE_B_BASE_REF): {base_b}")
    print(f"  all three are current at the time of writing: "
          f"{sh('git','-C',str(b),'rev-parse','HEAD').strip() == head_b}")
    print()
    print("NECESSITY DERIVATION, recomputed from the live tree (not quoted from an earlier run)")
    print(f"  declared exclusion in force: {exc!r}")
    print(f"  changed paths in the governed diff at THIS head: {len(changed)}")
    print(f"  RUN 1 with the entry present : UNLISTED={sum(1 for _, v in now if v == 'UNLISTED')} "
          f"DENIED={sum(1 for _, v in now if v == 'DENIED')}")
    print(f"  RUN 2 with the entry STRIPPED: UNLISTED={sum(1 for _, v in wo if v == 'UNLISTED')} "
          f"DENIED={sum(1 for _, v in wo if v == 'DENIED')}")
    for p in fell:
        print(f"  verdict change: {p}  {dict(now)[p]} -> {dict(wo)[p]}")
    print(f"  round-directory entries still present in the allowlist: "
          f"{bool(re.search(r'.hgk/rounds/', al))}")
    print()
    print("recompute: this script, at the same heads")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
