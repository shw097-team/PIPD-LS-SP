"""Build the R21 FAR gap ledger from measured state only.

Every row must name a file that exists on this host, or an explicit NOT_MEASURED. No row may cite a number that
cannot be recomputed from the file it names.
"""
import hashlib
import json
import pathlib
import sqlite3
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"


def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def rel(p):
    return str(pathlib.Path(p).relative_to(ROOT)).replace("\\", "/")


def artifact(name):
    p = V / name
    return {"path": f"var/FHS-R21-FAR-TT-20261101/{name}", "sha256": sha(p), "bytes": p.stat().st_size if p.exists() else None}


def queue():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute("select * from work_queue order by wp_id")]


def main():
    rows = queue()
    by_id = {r["wp_id"]: r for r in rows}
    gaps = []

    def add(gid, what, evidence, state, cost, unblock, decision=None):
        gaps.append({"id": gid, "what": what, "evidence": evidence, "state": state, "cost": cost,
                     "unblock": unblock, "owner_decision": decision})

    no_ev = [r["wp_id"] for r in rows if not r["evidence_ref"]]
    add("G-01", f"{len(no_ev)} of 22 work_queue rows are PASS with an empty evidence_ref and no per-WP artifact dir",
        artifact("far/sources/WORK_QUEUE_READBACK.json"), "OPEN",
        "the 22-WP pass rate is not defensible; each row needs a bound receipt or a reopen",
        "re-run each WP's own checker against its artifact dir, or reopen the WP and re-execute", "OWNER (reopen authority)")

    add("G-02", "WP-FHS-11 is state=PASS while carrying blocker_code=HERMES_MODEL_HALF_UNMEASURED",
        artifact("far/sources/WORK_QUEUE_READBACK.json"), "INCONSISTENT",
        "a PASS row that admits half the surface was never measured cannot be counted",
        "either measure the model half on a real host request or move the row to FAIL with a named blocker",
        "none if the row is corrected")

    for wp in ("WP-FHS-12", "WP-FHS-13", "WP-FHS-20"):
        r = by_id[wp]
        add(f"G-{wp}", f"{wp} is FAIL with blocker {r['blocker_code']}",
            artifact("far/sources/WORK_QUEUE_READBACK.json"), "OPEN",
            "three of twenty-two WPs cannot be closed; two of them carry owner-envelope and cell evidence already",
            r.get("blocker_unblock") or "unknown", "none until its own checker re-reads")

    add("G-05", "S5 DEV ECP: 5 edges; A8/B3/B4 executed, C5 executed today, B5 measured unprovable on this host",
        artifact("s5/C5_CASES.json"), "PARTIAL",
        "DEV ECP completion cannot be claimed as 5/5 because B5 needs a host that issues SP identities",
        "B5 unblocks only on a host with three real SP identities; the other four are measured",
        "HOST (no local workaround)")

    add("G-06", "Four canonical tool defects measured (stale preimage, reused receipt, foreign effect class, two live ECPs)",
        artifact("s5/B3_PATCH_TEST.json"), "OPEN",
        "candidate patches pass but the canonical tools still accept all four",
        "owner/issuer authorises landing the candidate patch on PIPD/tools/hotswap.py, then a fresh regression",
        "OWNER (repo write on canonical file)")

    add("G-07", "C5: a checker editing the landed diff is detectable via receipt candidate_sha256 but is not prevented",
        artifact("s5/C5_CASES.json"), "DETECTABLE_NOT_PREVENTED",
        "the NEG clause 'checker edits same diff' is only half satisfied",
        "a re-verify step must recompute the sha; enforcement would need a write-lock the tool does not have",
        "none if the re-verify step is mandated")

    add("G-08", "OPS ECP: contract says 32 sub-contracts; the body yields 31 edges (OPS 14 / OBS 10 / DEV 5 / USER 2)",
        artifact("ledgers/S6_EDGE_EFFECT_LEDGER.json"), "NOT_LOCATED",
        "the denominator in the contract cannot be reconciled with the source",
        "owner or the source document must rule where the 32nd comes from; an agent must not invent it",
        "OWNER (source authority)")

    add("G-09", "S6 closure: 2 defects patched as candidates, 1 partial (no receiver ABI/ACK), 11 PARK",
        artifact("s6/S6_CLOSURE.json"), "PARTIAL",
        "11 of 31 edges cannot be exercised without a signed domain receiver and an oracle per edge",
        "each PARK names its own unblock; none is a local engineering gap",
        "OWNER/HOST per edge")

    add("G-10", "TQAEP 282 cases are machine-read with per-case sha, but no case is mapped to a TestClass/OracleType/G00-G14 or executed",
        artifact("ledgers/S5_S7_INVENTORY.json"), "OPEN",
        "the 282 denominator is a source identity, not a run",
        "map and execute the minimal closure; 12 TestClasses / 8 OracleTypes are the axes",
        "none for mapping; execution needs fixtures")

    add("G-11", "Three native offices (TPM / Commander / Challenge) have no host-issued identity on this host",
        artifact("s5/B5_PROBE.json"), "NOFIT_LOCAL",
        "no NATIVE acceptance can be produced locally for any of the three",
        "run each office on a host that issues identities and record command+exit+sha",
        "HOST")

    add("G-12", "AO returned PARTIAL; four of its claims were re-measured by me and confirmed; three findings remain open (F4/F5/F6) and one (F11) was never stated",
        artifact("wp20/AO_0361E484_RETURN.md"), "OPEN",
        "WP-20's ceiling is narrower than reported before the AO returned",
        "F4: give the three negative kinds measured evidence or drop them; F5: classify SIMPLE_AGENT; F6: install leg; F11: state it",
        "none for F4/F11; F6 needs network")

    add("G-13", "PLUGIN install leg never exercised: the fixture is a bundled plugin, not a catalog entry",
        artifact("wp20/PLUGIN_PROBE_V2.json"), "NOT_EXERCISED",
        "the plugin cells can claim list+remove only",
        "install a catalog or git plugin in a throwaway home with dependency bootstrap",
        "none (network)")

    add("G-14", "TT-20 has no record anywhere; 49 FAR/TT rows reconciled earlier",
        artifact("receipts/FAR_TT_RECONCILE.json"), "NO_RECORD",
        "the ledger cannot show 50/50",
        "record TT-20 as NO_RECORD with its provenance, or owner supplies the missing TT",
        "OWNER (record authority)")

    add("G-15", "scripts/review_lock.py is not under version control while the pre-commit hook depends on it",
        {"path": "HG-KSEOS/scripts/review_lock.py", "sha256": sha(ROOT / "HG-KSEOS/scripts/review_lock.py")}, "OPEN",
        "the guard that makes reviewed writes reviewable is itself unversioned",
        "commit it under a proper change with a rollback pointer",
        "OWNER (repo write)")

    add("G-16", "Owner envelope WIN-91b01b7cd918 open, 40 ops, expires 2026-11-01T13:55:31Z",
        {"path": "var/B1-PIPD-PKG-20261027/artifacts/OWNER_WINDOW.json",
         "sha256": sha(ROOT / "var/B1-PIPD-PKG-20261027/artifacts/OWNER_WINDOW.json")}, "OPEN_UNTIL_EXPIRY",
        "any permit / admission bundle / registry row signing after expiry needs a new envelope",
        "reopen the envelope before the first signing op of the next round",
        "OWNER (opens the window)")

    add("G-17", "S8/S9 not started: no three-office evidence set, no four-repo adoption decision, no final report",
        artifact("far/sources/SOURCE_DENOMINATOR.json"), "OPEN",
        "the deliverable cannot be called complete",
        "S8 is blocked by G-11; S9 depends on the adoption decisions in this FAR",
        "OWNER (adoption and release authority)")

    doc = {"schema": "FHS.R21.FAR.GAP_LEDGER/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "sources_read": artifact("far/sources/SOURCE_DENOMINATOR.json"),
           "queue_state": {"rows": len(rows), "pass": sum(1 for r in rows if r["state"] == "PASS"),
                           "fail": sum(1 for r in rows if r["state"] == "FAIL"),
                           "without_evidence_ref": len(no_ev)},
           "gaps": gaps,
           "counts": {s: sum(1 for g in gaps if g["state"] == s) for s in {g["state"] for g in gaps}},
           "claim_ceiling": "author-side inventory; every row names a local file whose sha256 is recorded here"}
    out = V / "far" / "gaps" / "GAP_LEDGER.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"gaps": len(gaps), "counts": doc["counts"], "queue": doc["queue_state"],
                      "sha256": sha(out)[:16]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
