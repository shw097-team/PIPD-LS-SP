# -*- coding: utf-8 -*-
"""Build candidate G: preview.4's bytes under a NEW identity, displayed as "PIPD-LS-SP Public Skills_P4".

- identity (plugin.json .name, plugin.release.json .plugin_id) -> pipd-ls-sp-public-skills-p4
- display name (plugin.json extensions.com.openai.interface displayName/display_name,
  plugin.release.json .display_name) -> the literal string the owner asked for
- every other member byte-identical to A, and the effective deflate level forced to match A's,
  so identical-content members carry identical compress_size (the checker's CC-1 finding).
"""
import hashlib
import json
import os
import re
import zipfile

ROUND = r"C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout"
SRC = os.path.join(ROUND, "host_smoke", "cand-A-preview4-served.zip")
OUT = os.path.join(ROUND, "host_smoke", "cand-G-preview4-p4-name.zip")
DISPLAY = "PIPD-LS-SP Public Skills_P4"
NEW_NAME = "pipd-ls-sp-public-skills-p4"
OLD_NAME = "pipd-ls-sp-public-skills"
OLD_DISPLAY = "PIPD-LS-SP Public Skills"
LEVEL = 9

PJ = OLD_NAME + "/plugin.json"
PR = OLD_NAME + "/plugin.release.json"

with zipfile.ZipFile(SRC) as z:
    infos = z.infolist()
    data = {i.filename: z.read(i.filename) for i in infos}
orig = dict(data)          # pristine copy for the single-axis verification below

# --- targeted textual edits (no JSON re-dump: keeps every other byte, layout and key order) ---
def sub(b, old, new, expect):
    t = b.decode("utf-8")
    n = t.count(old)
    assert n == expect, f"expected {expect} occurrence(s) of {old!r}, found {n}"
    return t.replace(old, new).encode("utf-8")

# plugin.json: identity + both display fields
data[PJ] = sub(data[PJ], f'"name": "{OLD_NAME}"', f'"name": "{NEW_NAME}"', 1)
data[PJ] = sub(data[PJ], f'"displayName": "{OLD_DISPLAY}"', f'"displayName": "{DISPLAY}"', 1)
data[PJ] = sub(data[PJ], f'"display_name": "{OLD_DISPLAY}"', f'"display_name": "{DISPLAY}"', 2)  # com.openai.interface + com.pipd.s4
# plugin.release.json: display + plugin_id (kept consistent with the new identity)
data[PR] = sub(data[PR], f'"display_name": "{OLD_DISPLAY}"', f'"display_name": "{DISPLAY}"', 1)
data[PR] = sub(data[PR], f'"plugin_id": "{OLD_NAME}"', f'"plugin_id": "{NEW_NAME}"', 1)

# --- rebuild: copy A's ZipInfo fields AND force A's effective deflate level ---
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=LEVEL) as z:
    for i in infos:
        zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = i.external_attr
        zi.create_system = i.create_system
        zi.internal_attr = i.internal_attr
        zi._compresslevel = LEVEL
        z.writestr(zi, data[i.filename])

# --- verify against A ---
with zipfile.ZipFile(OUT) as z:
    infos_g = z.infolist()
    data_g = {i.filename: z.read(i.filename) for i in infos_g}

print(f"members: A={len(infos)} G={len(infos_g)}")
changed = sorted(n for n in orig if orig[n] != data_g[n])
print("changed members:", changed)
assert changed == [PJ, PR], "unexpected changed member set"
print("plugin.json name ->", json.loads(data_g[PJ])["name"])
print("plugin.json displayName ->",
      json.loads(data_g[PJ])["extensions"]["com.openai"]["interface"]["displayName"])
print("release display_name ->", json.loads(data_g[PR])["display_name"],
      "| plugin_id ->", json.loads(data_g[PR])["plugin_id"])

same_content = [n for n in orig if orig[n] == data_g[n]]
size_mismatch = [n for n in same_content
                 if next(x.compress_size for x in infos if x.filename == n)
                 != next(x.compress_size for x in infos_g if x.filename == n)]
print(f"identical-content members: {len(same_content)} | compress_size mismatches vs A: {len(size_mismatch)}")
assert not size_mismatch, f"compression level still differs on {size_mismatch[:5]}"
meta_mismatch = [n for n in orig if (lambda a, b: (a.compress_type, a.date_time, a.external_attr,
                                                    a.create_system) !=
                                                  (b.compress_type, b.date_time, b.external_attr,
                                                   b.create_system))(
    next(x for x in infos if x.filename == n), next(x for x in infos_g if x.filename == n))]
print("zip-record metadata mismatches vs A:", len(meta_mismatch))

h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"G sha256={h} bytes={os.path.getsize(OUT)}")
json.dump({"schema": "PROBE-CANDIDATE/1", "status": "PROBE_ARTIFACT_NOT_A_RELEASE", "file": os.path.basename(OUT),
           "sha256": h, "bytes": os.path.getsize(OUT), "derived_from": {"file": os.path.basename(SRC),
                                                                      "sha256": hashlib.sha256(open(SRC, "rb").read()).hexdigest()},
           "deltas_vs_A": {"members_changed": changed, "identity": NEW_NAME, "display_name": DISPLAY},
           "members_identical_to_A": len(orig) - len(changed),
           "compress_size_mismatches": len(size_mismatch), "metadata_mismatches": len(meta_mismatch)},
          open(os.path.join(ROUND, "FAR_R5R3_ZIPSPEC", "CANDIDATE_G_MANIFEST.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("manifest -> FAR_R5R3_ZIPSPEC/CANDIDATE_G_MANIFEST.json")
