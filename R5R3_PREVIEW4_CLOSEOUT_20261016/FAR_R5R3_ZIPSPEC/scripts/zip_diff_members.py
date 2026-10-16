# -*- coding: utf-8 -*-
"""Diff the two member files that differ between rejected A and accepted B."""
import difflib
import json
import os
import zipfile

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout\host_smoke"
A = os.path.join(R, "cand-A-preview4-served.zip")
B = os.path.join(R, "cand-B-r5y-known-good.zip")
TARGETS = ["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json",
           "pipd-ls-sp-public-skills/SOURCE_TO_PLUGIN_MAPPING.json"]


def read(p, n):
    with zipfile.ZipFile(p) as z:
        return z.read(n).decode("utf-8")


for n in TARGETS:
    a, b = read(A, n), read(B, n)
    print("=" * 78)
    print("MEMBER:", n, f"(A {len(a)} chars / B {len(b)} chars)")
    print("=" * 78)
    print("--- FULL TEXT OF A (REJECTED) ---")
    print(a)
    print("--- DIFF  B(accepted) -> A(rejected) ---")
    d = difflib.unified_diff(b.splitlines(), a.splitlines(), "B-accepted", "A-rejected",
                             lineterm="", n=2)
    lines = list(d)
    for ln in lines[:200]:
        print(ln)
    print(f"(diff lines: {len(lines)})")

    try:
        ja, jb = json.loads(a), json.loads(b)
        print("--- key-level compare ---")
        keys = sorted(set(ja) | set(jb))
        for k in keys:
            va, vb = json.dumps(ja.get(k), ensure_ascii=False), json.dumps(jb.get(k), ensure_ascii=False)
            if va != vb:
                print(f"  [{k}] A={va[:160]}")
                print(f"  [{k}] B={vb[:160]}")
    except Exception as e:
        print("json parse:", str(e)[:80])
