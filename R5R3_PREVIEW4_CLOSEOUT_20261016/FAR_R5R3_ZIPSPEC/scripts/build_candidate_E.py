# -*- coding: utf-8 -*-
"""Build candidate E: A's members unchanged except the declared version (identity axis only).

Deterministic packaging per the PIPD contract: DEFLATE level 9, mode 0644, zip mtime 1980-01-01.
"""
import hashlib
import json
import os
import zipfile

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
SRC = os.path.join(R, "host_smoke", "cand-A-preview4-served.zip")
OUT = os.path.join(R, "host_smoke", "cand-E-preview4-version-bumped.zip")
NEW_VER = "0.1.2"
DT = (1980, 1, 1, 0, 0, 0)
PREFIX = "pipd-ls-sp-public-skills/"

with zipfile.ZipFile(SRC) as z:
    names = z.namelist()
    data = {n: z.read(n) for n in names}

changed = []
for n in (PREFIX + "plugin.json", PREFIX + "RELEASE_RECEIPT.json"):
    d = json.loads(data[n].decode("utf-8"))
    old = d.get("version")
    if old is None:
        print("!! no version field in", n)
        continue
    d["version"] = NEW_VER
    data[n] = (json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    changed.append((n, old, NEW_VER, len(data[n])))

meta_src = {}
with zipfile.ZipFile(SRC) as z:
    for i in z.infolist():
        meta_src[i.filename] = i

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for n in names:
        src = meta_src[n]
        zi = zipfile.ZipInfo(n, date_time=src.date_time)
        zi.compress_type = src.compress_type
        zi.external_attr = src.external_attr
        zi.internal_attr = src.internal_attr
        zi.create_system = src.create_system
        z.writestr(zi, data[n])

h = hashlib.sha256()
with open(OUT, "rb") as fh:
    for c in iter(lambda: fh.read(1 << 20), b""):
        h.update(c)
size = os.path.getsize(OUT)

# verify: every member except the two edited ones must be byte-identical to A
same, diff = 0, []
with zipfile.ZipFile(SRC) as za, zipfile.ZipFile(OUT) as ze:
    na, ne = za.namelist(), ze.namelist()
    assert na == ne, ("member list differs", set(na) ^ set(ne))
    for n in na:
        a, e = za.read(n), ze.read(n)
        if a == e:
            same += 1
        else:
            diff.append(n)
    # metadata check
    meta_diff = []
    for i in za.infolist():
        j = ze.getinfo(i.filename)
        if (i.compress_type, i.date_time, i.external_attr, i.create_system) != \
           (j.compress_type, j.date_time, j.external_attr, j.create_system):
            meta_diff.append(i.filename)

print("source:", SRC)
print("output:", OUT)
print("bytes:", size, "sha256:", h.hexdigest())
print("members:", len(na), "identical:", same, "differing:", diff)
print("changed fields:", [(c[0], c[1], c[2]) for c in changed])
print("metadata differences vs A:", meta_diff)
man = {
    "schema": "R5R3/PROBE-CANDIDATE-E/1",
    "path": OUT,
    "sha256": h.hexdigest(),
    "bytes": size,
    "derived_from": {"artifact": SRC, "sha256": "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"},
    "only_change": "declared version 0.1.1 -> 0.1.2 in plugin.json and RELEASE_RECEIPT.json",
    "members_identical_to_A": same,
    "members_differing": diff,
    "zip_metadata_matches_A": not meta_diff,
    "determinism": {"compression": "DEFLATED:9", "zip_mtime": "1980-01-01T00:00:00Z", "mode": "0644"},
    "status": "PROBE ARTIFACT ONLY — not a release, not published, no owner gate touched",
    "claim_ceiling": "a locally built diagnostic candidate; nothing about host behaviour is asserted here",
}
mp = os.path.join(R, "FAR_R5R3_ZIPSPEC", "CANDIDATE_E_MANIFEST.json")
with open(mp, "w", encoding="utf-8") as fh:
    json.dump(man, fh, ensure_ascii=False, indent=1)
print("wrote", mp)
