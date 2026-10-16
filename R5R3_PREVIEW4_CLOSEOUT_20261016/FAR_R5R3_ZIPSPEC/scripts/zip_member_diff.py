# -*- coding: utf-8 -*-
"""Member-by-member diff of the accepted (B) vs rejected (A) plugin archives."""
import hashlib
import json
import os
import zipfile

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout\host_smoke"
A = os.path.join(R, "cand-A-preview4-served.zip")      # rejected by host
B = os.path.join(R, "cand-B-r5y-known-good.zip")       # accepted by host (R5Y)
C = os.path.join(R, "cand-C-variant-a-root-manifest.zip")
D = os.path.join(R, "cand-D-variant-b-minimal.zip")


def members(p):
    out = {}
    with zipfile.ZipFile(p) as z:
        for i in z.infolist():
            data = z.read(i.filename)
            out[i.filename] = {
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "crc": format(i.CRC, "08x"),
                "compress_type": i.compress_type,
                "external_attr": oct(i.external_attr),
                "date_time": i.date_time,
                "data": data,
            }
    return out


ma, mb = members(A), members(B)
print(f"A members={len(ma)} B members={len(mb)}")
only_a = sorted(set(ma) - set(mb))
only_b = sorted(set(mb) - set(ma))
print("only in A (rejected):", only_a)
print("only in B (accepted):", only_b)
print("common:", len(set(ma) & set(mb)))
print()
print("=== DIFFERING COMMON MEMBERS ===")
for n in sorted(set(ma) & set(mb)):
    if ma[n]["sha256"] != mb[n]["sha256"]:
        print(f"  {n}:  A {ma[n]['bytes']}B {ma[n]['sha256'][:16]}  |  B {mb[n]['bytes']}B {mb[n]['sha256'][:16]}")
print()
for label, m in (("ONLY-IN-A", [(n, ma[n]) for n in only_a]), ("ONLY-IN-B", [(n, mb[n]) for n in only_b])):
    for n, e in m:
        print(f"--- {label}: {n} ({e['bytes']}B) ---")
        if e["bytes"] <= 2000:
            try:
                print(e["data"].decode("utf-8")[:1500])
            except Exception:
                print(repr(e["data"][:300]))
        print()
print("=== ALL MEMBERS OF A ===")
for n in sorted(ma):
    print(f"  {ma[n]['bytes']:>7} B  {ma[n]['sha256'][:12]}  {n}")
print("=== ALL MEMBERS OF B ===")
for n in sorted(mb):
    print(f"  {mb[n]['bytes']:>7} B  {mb[n]['sha256'][:12]}  {n}")

for lab, p in (("C", C), ("D", D)):
    if os.path.exists(p):
        m = members(p)
        print(f"=== {lab} members={len(m)} ===")
        for n in sorted(m):
            print(f"  {m[n]['bytes']:>7} B  {m[n]['sha256'][:12]}  {n}")
