# -*- coding: utf-8 -*-
"""Build candidate F: A's members verbatim, ONLY plugin.json's name changed (identity axis),
A's provenance bytes PRESERVED (so the probe separates an id conflict from a provenance-content rule).

Outcome map: ACCEPT => the refusal is an existing-plugin_id conflict; REJECT => the two provenance
members' content is refused regardless of identity.
"""
import hashlib
import json
import os
import zipfile

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
SRC = os.path.join(R, "host_smoke", "cand-A-preview4-served.zip")
OUT = os.path.join(R, "host_smoke", "cand-F-preview4-new-id.zip")
NEW_NAME = "pipd-probe-content-check"
PREFIX = "pipd-ls-sp-public-skills/"

with zipfile.ZipFile(SRC) as z:
    names = z.namelist()
    data = {n: z.read(n) for n in names}
    meta = {i.filename: i for i in z.infolist()}

pj = PREFIX + "plugin.json"
d = json.loads(data[pj].decode("utf-8"))
old_name = d["name"]
d["name"] = NEW_NAME
data[pj] = (json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for n in names:
        s = meta[n]
        zi = zipfile.ZipInfo(n, date_time=s.date_time)
        zi.compress_type = s.compress_type
        zi.external_attr = s.external_attr
        zi.internal_attr = s.internal_attr
        zi.create_system = s.create_system
        z.writestr(zi, data[n])

h = hashlib.sha256()
with open(OUT, "rb") as fh:
    for c in iter(lambda: fh.read(1 << 20), b""):
        h.update(c)
size = os.path.getsize(OUT)

with zipfile.ZipFile(SRC) as za, zipfile.ZipFile(OUT) as zf:
    same = sum(1 for n in za.namelist() if za.read(n) == zf.read(n))
    diff = [n for n in za.namelist() if za.read(n) != zf.read(n)]
    meta_diff = [i.filename for i in za.infolist()
                 if (i.compress_type, i.date_time, i.external_attr, i.create_system) !=
                    (zf.getinfo(i.filename).compress_type, zf.getinfo(i.filename).date_time,
                     zf.getinfo(i.filename).external_attr, zf.getinfo(i.filename).create_system)]

print("output:", OUT)
print("bytes:", size, "sha256:", h.hexdigest())
print("only change: plugin.json name", repr(old_name), "->", repr(NEW_NAME))
print("members identical to A:", same, "differing:", diff)
print("zip metadata differences vs A:", meta_diff)
print("provenance preserved:", json.loads(
    zipfile.ZipFile(OUT).read(PREFIX + "RELEASE_RECEIPT.json"))["source_commit"][:12], "(A value)")
man = {
    "schema": "R5R3/PROBE-CANDIDATE-F/1",
    "path": OUT, "sha256": h.hexdigest(), "bytes": size,
    "derived_from": SRC,
    "only_change": f"plugin.json name {old_name} -> {NEW_NAME}; A's provenance bytes preserved",
    "members_identical_to_A": same, "members_differing": diff,
    "zip_metadata_matches_A": not meta_diff,
    "status": "PROBE ARTIFACT ONLY — not a release, not published",
    "claim_ceiling": "diagnostic candidate; asserts nothing about host behaviour",
}
with open(os.path.join(R, "FAR_R5R3_ZIPSPEC", "CANDIDATE_F_MANIFEST.json"), "w", encoding="utf-8") as fh:
    json.dump(man, fh, ensure_ascii=False, indent=1)
print("manifest written")
