#!/usr/bin/env python3
"""Measure what the write-set allowlist MINIMALLY needs, for the stage THIS branch declares.

Correction over the first version: the workflow carries one copy per branch, and that copy declares its
own `STAGE:` plus the bases it needs. The active allowlist pair is selected by the declared stage, and
the governed base is `STAGE_A_BASE_SHA` for stage-a or the resolved `STAGE_B_BASE_REF` for stage-b (the
Stage A head) - not the frozen subject, which is only the baseline the allowlist was historically
compared against.

Narrowing the round-directory entry cannot be argued in prose: it depends on which paths the governed
diff actually contains. This reproduces that diff, classifies every changed path against the sets at the
current head, and tests candidate narrowings by asking whether the diff would still pass. Reads only.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

WF = ".github/workflows/public-plugin-verify.yml"
ROUND = r"\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/"


def sh(args: list[str], cwd: str) -> str:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True).stdout


def main() -> int:
    root = sys.argv[1]
    head = sh(["git", "rev-parse", "HEAD"], root).strip()
    text = sh(["git", "show", f"{head}:{WF}"], root)
    stage = (re.search(r"^\s*STAGE:\s*(\S+)\s*$", text, re.M) or [None, "?"])[1]
    vals = dict(re.findall(r"^\s*(STAGE_A_BASE_SHA|STAGE_B_BASE_REF|PR_BASE_SHA):\s*(\S+)\s*$", text, re.M))
    pairs = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.search(r"^\s*(ALLOWED|DENIED)='\^(.*?)\$?'\s*$", line)
        if m:
            pairs.append({"line": i, "kind": m.group(1), "regex": m.group(2)})
    grouped = [(pairs[i], pairs[i + 1]) for i in range(0, len(pairs) - 1)
               if pairs[i]["kind"] == "ALLOWED" and pairs[i + 1]["kind"] == "DENIED"]

    def resolve(ref: str) -> str | None:
        for cand in (f"refs/heads/{ref}", f"refs/remotes/origin/{ref}", ref):
            try:
                return sh(["git", "rev-parse", "--verify", "--quiet", cand], root).strip() or None
            except subprocess.CalledProcessError:
                continue
        return None

    if stage == "stage-b":
        base = resolve(vals.get("STAGE_B_BASE_REF", "")) or vals.get("STAGE_B_BASE_REF")
    else:
        base = vals.get("STAGE_A_BASE_SHA")
    active = None
    for al, dn in grouped:
        has_src = "src/" in dn["regex"]
        if (stage == "stage-b") == has_src:
            active = (al, dn)
    print(f"HEAD        : {head}")
    print(f"declared    : {stage}   bases: {vals}")
    print(f"governed base resolved: {base}")
    for al, dn in grouped:
        mark = "  <== ACTIVE for this branch" if (al, dn) == active else ""
        print(f"  line {al['line']:>4} ALLOWED {al['regex'][:96]}{mark}")
        print(f"  line {dn['line']:>4} DENIED  {dn['regex'][:96]}")
    if not active or not base:
        print("REFUSING: could not determine the active allowlist pair or the governed base")
        return 2

    al, dn = active
    exc = (re.search(r"EXCLUDED_PREFIXES='([^']*)'", text) or [None, None])[1]
    changed = [p for p in sh(["git", "diff", "--name-only", f"{base}...HEAD"], root).splitlines() if p.strip()]

    def verdict(p: str) -> str:
        if exc and re.search(exc, p):
            return "EXCLUDED"
        if re.search(dn["regex"], p):
            return "DENIED"
        return "ALLOWED" if re.search(al["regex"], p) else "UNLISTED"

    rows = [{"path": p, "verdict": verdict(p)} for p in changed]
    print(f"\n=== governed {stage} write set ({base[:10]}...HEAD): {len(rows)} changed paths ===")
    print(f"   declared exclusion in force: {exc!r}")
    for r in rows:
        if r["verdict"] != "EXCLUDED":
            print(f"   {r['verdict']:<9} {r['path']}")
    n_exc = sum(1 for r in rows if r["verdict"] == "EXCLUDED")
    n_unn = sum(1 for r in rows if r["verdict"] == "UNLISTED")
    n_den = sum(1 for r in rows if r["verdict"] == "DENIED")
    print(f"   EXCLUDED (scaffolding, printed by the gate itself): {n_exc}")
    print(f"   UNLISTED product paths: {n_unn}; DENIED product paths: {n_den}")

    # The headline an external officer needs: net change of each arm versus a named revision.
    def allowed_at(rev: str, want_src: bool) -> str | None:
        t = sh(["git", "show", f"{rev}:{WF}"], root)
        sets = []
        for i, line in enumerate(t.splitlines(), 1):
            m = re.search(r"^\s*(ALLOWED|DENIED)='\^(.*?)\$?'\s*$", line)
            if m:
                sets.append({"line": i, "kind": m.group(1), "regex": m.group(2)})
        for i in range(0, len(sets) - 1):
            if sets[i]["kind"] == "ALLOWED" and sets[i + 1]["kind"] == "DENIED" \
                    and ("src/" in sets[i + 1]["regex"]) == want_src:
                return sets[i]["regex"]
        return None

    def alts(rx: str | None) -> set[str]:
        if not rx:
            return set()
        return {a for a in rx.lstrip("^(").rstrip(")").split("|") if a}

    want_src = (stage == "stage-b")
    cur = alts(al["regex"])
    versus = {}
    for label, rev in (("frozen subject", "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed"),
                       ("previous head 35a68f0", "35a68f0c05a26747c2a1553cb86505ac26909b88")):
        try:
            old = alts(allowed_at(rev, want_src))
        except subprocess.CalledProcessError:
            versus[label] = {"added": None, "removed": None, "error": "revision not readable"}
            continue
        versus[label] = {"added": sorted(cur - old), "removed": sorted(old - cur)}
    print("\n=== net allowlist change versus a named revision (the headline) ===")
    for label, v in versus.items():
        print(f"   vs {label}: added={v.get('added')} removed={v.get('removed')}")
    print("\n=== the removed round-directory entries are gone from BOTH arms at HEAD ===")
    for want in (False, True):
        arm = allowed_at(head, want) or ""
        present = bool(re.search(r"\.hgk/rounds/", arm))
        print(f"   arm with src-denied={want}: round-directory entry present: {present}")

    print("\n=== is the surviving addition needed by this diff? ===")
    docs = [r["path"] for r in rows if r["path"].startswith("docs/") and r["verdict"] != "EXCLUDED"]
    print(f"   docs product paths in range: {docs or 'none'}")
    print(f"   -> removing docs/USER_GUIDE.md from the stage-b arm would leave "
          f"{sum(1 for r in rows if r['path'] == 'docs/USER_GUIDE.md')} path(s) UNLISTED")

    out = pathlib.Path(root) / (".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
                                "/evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json")
    out.write_text(json.dumps({"head": head, "stage": stage, "bases": vals, "resolved_base": base,
                               "active_allowlist": al, "active_denied": dn,
                               "declared_exclusion": exc,
                               "counts": {"changed": len(rows), "excluded": n_exc,
                                          "unlisted_product": n_unn, "denied_product": n_den},
                               "product_rows": [r for r in rows if r["verdict"] != "EXCLUDED"],
                               "net_allowlist_change": versus, "docs_product_paths": docs},
                              indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nreceipt: {out.relative_to(pathlib.Path(root))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
