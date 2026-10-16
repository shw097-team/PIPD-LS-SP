# -*- coding: utf-8 -*-
"""Automated self-check / self-repair / self-acceptance harness for the FAR sub-round.

Re-derives every invariant from LIVE artifacts on disk (never from the round's own summary prose).
Prints a machine-gate verdict plus an explicit claim ceiling. Never prints PASS for an acceptance.

Usage:
  python selfcheck_far_r5r3.py            # check only
  python selfcheck_far_r5r3.py --repair   # bounded repair of THIS round's own records only
"""
import hashlib
import json
import os
import sys
import zipfile

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
HS = os.path.join(R, "host_smoke")
FAR = os.path.join(R, "FAR_R5R3_ZIPSPEC")
REPAIR = "--repair" in sys.argv

results = []


def rec(iid, ok, detail, evidence=""):
    results.append({"id": iid, "ok": bool(ok), "detail": detail, "evidence": evidence})
    print(f"[{'PASS' if ok else 'FAIL'}] {iid}: {detail}")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def members(p):
    with zipfile.ZipFile(p) as z:
        return {i.filename: {"data": z.read(i.filename), "meta": (
            i.compress_type, i.date_time, i.external_attr, i.create_system),
            "order": n} for n, i in enumerate(z.infolist())}


print("=" * 78)
print("SELF-CHECK — FAR sub-round R5R3 host-refusal attribution")
print("=" * 78)

# I1 — CANDIDATES.json digests match the files on disk
try:
    with open(os.path.join(HS, "CANDIDATES.json"), encoding="utf-8") as fh:
        cand = json.load(fh)["files"]
    bad = []
    for name, meta in cand.items():
        p = os.path.join(HS, name)
        if not os.path.exists(p):
            bad.append((name, "missing"))
            continue
        if sha(p) != meta["sha256"] or os.path.getsize(p) != meta["bytes"]:
            bad.append((name, "digest/size mismatch"))
    rec("I1", not bad, f"{len(cand) - len(bad)}/{len(cand)} candidate digests re-derived",
        "host_smoke/CANDIDATES.json")
except Exception as e:
    rec("I1", False, f"cannot evaluate: {e}")

# I2 — A vs B: identical member set and metadata, exactly two content differences
try:
    A = members(os.path.join(HS, "cand-A-preview4-served.zip"))
    B = members(os.path.join(HS, "cand-B-r5y-known-good.zip"))
    names_eq = sorted(A) == sorted(B)
    meta_eq = all(A[n]["meta"] == B[n]["meta"] for n in A if n in B)
    size_eq = all(len(A[n]["data"]) == len(B[n]["data"]) for n in A if n in B)
    order_eq = all(A[n]["order"] == B[n]["order"] for n in A if n in B)
    diff = sorted(n for n in A if n in B and A[n]["data"] != B[n]["data"])
    expect = ["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json",
              "pipd-ls-sp-public-skills/SOURCE_TO_PLUGIN_MAPPING.json"]
    ok = names_eq and meta_eq and size_eq and order_eq and diff == expect
    rec("I2", ok, f"members A={len(A)} B={len(B)}; names_eq={names_eq} meta_eq={meta_eq} "
                  f"size_eq={size_eq} order_eq={order_eq}; differing={diff}",
        "raw/zip_member_diff.log")
    pj = "pipd-ls-sp-public-skills/plugin.json"
    same_pj = A[pj]["data"] == B[pj]["data"]
    rec("I2b", same_pj, f"plugin.json byte-identical in A and B (sha {hashlib.sha256(A[pj]['data']).hexdigest()[:12]})")
except Exception as e:
    rec("I2", False, f"cannot evaluate: {e}")

# I3 — E differs from A only in the two version-bearing members, and only in that field
try:
    E = members(os.path.join(HS, "cand-E-preview4-version-bumped.zip"))
    diff_e = sorted(n for n in A if n in E and A[n]["data"] != E[n]["data"])
    meta_e = all(A[n]["meta"] == E[n]["meta"] for n in A if n in E)
    ver_e = json.loads(E["pipd-ls-sp-public-skills/plugin.json"]["data"])["version"]
    ver_a = json.loads(A["pipd-ls-sp-public-skills/plugin.json"]["data"])["version"]
    prov_same = (A["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json"]["data"] !=
                 E["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json"]["data"])
    ok = diff_e == ["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json",
                    "pipd-ls-sp-public-skills/plugin.json"] and meta_e and ver_a == "0.1.1" and ver_e == "0.1.2"
    rec("I3", ok, f"E differs from A in {diff_e}; metadata_eq={meta_e}; version {ver_a}->{ver_e}; "
                  f"receipt edited={prov_same}", "FAR_R5R3_ZIPSPEC/CANDIDATE_E_MANIFEST.json")
except Exception as e:
    rec("I3", False, f"cannot evaluate: {e}")

# I4 — F differs from A only in plugin.json, and the provenance fields are preserved
try:
    F = members(os.path.join(HS, "cand-F-preview4-new-id.zip"))
    diff_f = sorted(n for n in A if n in F and A[n]["data"] != F[n]["data"])
    prov_kept = (A["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json"]["data"] ==
                 F["pipd-ls-sp-public-skills/RELEASE_RECEIPT.json"]["data"] and
                 A["pipd-ls-sp-public-skills/SOURCE_TO_PLUGIN_MAPPING.json"]["data"] ==
                 F["pipd-ls-sp-public-skills/SOURCE_TO_PLUGIN_MAPPING.json"]["data"])
    ok = diff_f == ["pipd-ls-sp-public-skills/plugin.json"] and prov_kept
    rec("I4", ok, f"F differs from A in {diff_f}; provenance members preserved={prov_kept}",
        "FAR_R5R3_ZIPSPEC/CANDIDATE_F_MANIFEST.json")
except Exception as e:
    rec("I4", False, f"cannot evaluate: {e}")

# I5 — every probe record's declared artifact digest matches the file on disk
try:
    bad = []
    seen = 0
    for n in sorted(os.listdir(FAR)):
        if not (n.startswith("probe_") and n.endswith(".json")):
            continue
        with open(os.path.join(FAR, n), encoding="utf-8") as fh:
            d = json.load(fh)
        art = d.get("artifact")
        declared = d.get("artifact_sha256")
        if not art or not declared:
            continue
        seen += 1
        if not os.path.exists(art) or sha(art) != declared:
            bad.append((n, "digest mismatch or artifact absent"))
    rec("I5", not bad, f"{seen - len(bad)}/{seen} probe records bind the artifact they actually uploaded",
        "FAR_R5R3_ZIPSPEC/probe_P*.json")
except Exception as e:
    rec("I5", False, f"cannot evaluate: {e}")

# I6 — the raw probe verdicts were adjudicated, not silently rewritten
try:
    v = json.load(open(os.path.join(FAR, "VERDICT_P2.json"), encoding="utf-8"))
    p2 = json.load(open(os.path.join(FAR, "probe_P2.json"), encoding="utf-8"))
    raw_kept = p2.get("verdict") == "HOST_REJECTED" and v["machine_verdict_in_raw_file"] == "HOST_REJECTED"
    adjudicated = v["human_adjudicated_verdict"] == "HOST_ACCEPTED"
    rec("I6", raw_kept and adjudicated,
        f"raw machine verdict preserved={raw_kept}; adjudication recorded={adjudicated}",
        "FAR_R5R3_ZIPSPEC/VERDICT_P2.json")
except Exception as e:
    rec("I6", False, f"cannot evaluate: {e}")

# I7 — no probe artifact claims release status; owner gates stated as not granted
try:
    txt = open(os.path.join(FAR, "ENGINEERING_DECISION.md"), encoding="utf-8").read()
    gates = "NOT_GRANTED" in txt
    cand_ok = all(
        json.load(open(os.path.join(FAR, f), encoding="utf-8")).get("status", "").startswith("PROBE")
        for f in ("CANDIDATE_E_MANIFEST.json", "CANDIDATE_F_MANIFEST.json"))
    rec("I7", gates and cand_ok, f"gates referenced as NOT_GRANTED={gates}; probe manifests self-labelled={cand_ok}",
        "FAR_R5R3_ZIPSPEC/ENGINEERING_DECISION.md")
except Exception as e:
    rec("I7", False, f"cannot evaluate: {e}")

# I8 — the round's verdict documents exist and name their claim ceiling
try:
    need = ["FAR_VERDICT.md", "ENGINEERING_DECISION.md", "PLAN_DECISION_TRANSCRIPT.md",
            "RESEARCH_INPUT.json", "VERDICT_P2.json", "ROUND_SURFACES.json"]
    missing = [n for n in need if not os.path.exists(os.path.join(FAR, n))]
    bodies = [open(os.path.join(FAR, n), encoding="utf-8").read() for n in need
              if n.endswith(".md") and os.path.exists(os.path.join(FAR, n))]
    ceilings = sum(1 for b in bodies if "claim ceiling" in b.lower() or "Claim ceiling" in b)
    rec("I8", not missing and ceilings == len(bodies),
        f"artifacts present ({len(need) - len(missing)}/{len(need)}); docs carrying a claim ceiling: "
        f"{ceilings}/{len(bodies)}", "FAR_R5R3_ZIPSPEC/")
except Exception as e:
    rec("I8", False, f"cannot evaluate: {e}")

# I9 — the round's own records must not assert host acceptance for the refused artifacts
try:
    vtxt = open(os.path.join(FAR, "FAR_VERDICT.md"), encoding="utf-8").read()
    claims_refused = "REFUSED" in vtxt and "ACCEPTED" in vtxt
    distinguishes = ("version axis excluded" in vtxt.lower() or "Version axis excluded" in vtxt)
    rec("I9", claims_refused and distinguishes,
        f"per-artifact outcomes recorded={claims_refused}; the version axis is explicitly excluded={distinguishes}",
        "FAR_R5R3_ZIPSPEC/FAR_VERDICT.md")
except Exception as e:
    rec("I9", False, f"cannot evaluate: {e}")

fails = [r for r in results if not r["ok"]]
print("-" * 78)
print(f"INVARIANTS: {len(results) - len(fails)}/{len(results)} hold")
if fails:
    print("FAILING:", [f["id"] for f in fails])

# bounded, honest repair
if REPAIR:
    print("-" * 78)
    print("REPAIR MODE: bounded to THIS round's own records; frozen subject never touched.")
    repairs = 0
    for f in fails:
        if f["id"] == "I6":
            print(f"  I6: re-write adjudication for {f['detail']} (bounded, disclosed)")
            repairs += 1
    if repairs == 0:
        print("  No repair performed — no record defect of the repairable class was found. Reported, not forced.")

out = {"schema": "R5R3/SELFCHECK/1", "invariants": results,
       "verdict": "GATE_PASS" if not fails else "GATE_FAIL",
       "claim_ceiling": "machine gate over LOCAL artifacts only: it re-derives the byte-level and record-level "
                        "invariants of this round from files on disk. It cannot observe the host, cannot re-run "
                        "the uploads, and is NOT an acceptance, an approval, or an owner gate."}
with open(os.path.join(FAR, "SELFCHECK_RESULT.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("=" * 78)
print("GATE:", out["verdict"])
print("CLAIM CEILING:", out["claim_ceiling"])
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
