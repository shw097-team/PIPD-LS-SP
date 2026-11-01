"""S6 / EDGE-WO-B1-A3 (QUEUE_WO): run the edge's criteria against the real queue code, on a copy.

Body, verbatim (10B#L49-52):
  POS  Scan at most K blocked cards, B/C independent advance; CAS generation single holder
  NEG  duplicate claim, starved B/C or stale generation -> LOST_LEASE_OR_DUPLICATE_CLAIM

The queue lives at HG-KSEOS/scripts/work_queue.py and the live spine is the product's own DB, so every case runs
against a byte copy (`queue_copy.db`) with the module's DB global repointed -- the spine is never mutated here.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import pathlib
import shutil
import sqlite3
import sys
import time
from contextlib import redirect_stdout

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
S6 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s6"
WQ = ROOT / "HG-KSEOS" / "scripts" / "work_queue.py"
LIVE_DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("wq_under_test", WQ)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def call(mod, fn, **kw):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = fn(argparse.Namespace(**kw))
    out = buf.getvalue().strip()
    try:
        parsed = json.loads(out.splitlines()[-1]) if out else None
    except json.JSONDecodeError:
        parsed = {"raw": out[:300]}
    return rc, parsed


def main():
    S6.mkdir(parents=True, exist_ok=True)
    copy = S6 / "queue_copy.db"
    shutil.copyfile(LIVE_DB, copy)
    live_rows = sqlite3.connect(f"file:{LIVE_DB}?mode=ro", uri=True).execute(
        "select count(*) from work_queue").fetchone()[0]
    copy_rows = sqlite3.connect(copy).execute("select count(*) from work_queue").fetchone()[0]

    mod = load_module()
    mod.DB = copy

    cases = {}

    # --- POS: bounded scan + independent advance -------------------------------------------
    rc1, next1 = call(mod, mod.cmd_next)
    cases["TQ-B1-A3-POS_scan"] = {
        "claim": "next returns a runnable item while settled failures stay parked",
        "rc": rc1, "result": next1,
        "verdict": "PASS" if rc1 == 0 and next1 and next1.get("wp") else "FAIL_OR_DRAINED",
    }

    drained = not (next1 or {}).get("wp")
    if drained:
        # the live queue holds 19 PASS + 3 settled FAIL, so nothing is runnable: inject a synthetic READY row
        # into the COPY only, then re-scan. Without this the POS case would "pass" by never running.
        con_i = sqlite3.connect(copy)
        con_i.execute("insert or replace into work_queue (wp_id,title,depends_on,effect_class,state,evidence_ref,updated_at)"
                      " values ('WP-FHS-90','A3 synthetic runnable row','','HOST_OP','NOT_RUN',NULL,?)",
                      (time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),))
        con_i.commit(); con_i.close()
        rc1, next1 = call(mod, mod.cmd_next)
        cases["TQ-B1-A3-POS_scan"]["injected_synthetic_row"] = True
        cases["TQ-B1-A3-POS_scan"]["first_scan"] = "QUEUE_DRAINED on the live 22 rows"
        cases["TQ-B1-A3-POS_scan"]["result"] = next1
        cases["TQ-B1-A3-POS_scan"]["verdict"] = ("PASS" if next1.get("wp") == "WP-FHS-90"
                                                 else "FAIL_AFTER_INJECTION")
    wp = (next1 or {}).get("wp")
    if wp:
        rc_s1, s1 = call(mod, mod.cmd_settle, wp=wp, verdict="FAIL", evidence="A3-POS-settled-1")
        rc2, next2 = call(mod, mod.cmd_next)
        cases["TQ-B1-A3-POS_independent_advance"] = {
            "claim": "after parking one item, the scan advances to a different runnable item",
            "settled": s1, "next_after": next2,
            "verdict": "PASS" if next2.get("wp") and next2.get("wp") != wp else
                       ("QUEUE_DRAINED" if next2.get("verdict") == "QUEUE_DRAINED" else "FAIL_STARVED"),
        }
        # --- NEG: duplicate claim on the same item ----------------------------------------
        rc_d1, d1 = call(mod, mod.cmd_settle, wp=wp, verdict="PASS", evidence="A3-NEG-dup-claim")
        rc_d2, d2 = call(mod, mod.cmd_settle, wp=wp, verdict="PASS", evidence="A3-NEG-dup-claim-2")
        after = sqlite3.connect(copy).execute("select state,evidence_ref from work_queue where wp_id=?",
                                              (wp,)).fetchone()
        cases["TQ-B1-A3-NEG_duplicate_claim"] = {
            "claim": "a second settle of the same item must be refused (LOST_LEASE_OR_DUPLICATE_CLAIM)",
            "first": {"rc": rc_d1, **d1}, "second": {"rc": rc_d2, **d2}, "row_after": after,
            "verdict": "PASS" if rc_d2 != 0 else "FAIL_DUPLICATE_ACCEPTED",
        }
        # --- NEG: PASS with no evidence ----------------------------------------------------
        wp2 = (next2 or {}).get("wp")
        if wp2:
            rc_e, e = call(mod, mod.cmd_settle, wp=wp2, verdict="PASS", evidence="")
            cases["TQ-B1-A3-NEG_pass_without_evidence"] = {
                "claim": "a PASS with an empty evidence_ref should not be recordable",
                "result": {"rc": rc_e, **e},
                "verdict": "PASS" if rc_e != 0 else "FAIL_EVIDENCELESS_PASS_ACCEPTED",
            }

    # --- capabilities the body names but the code does not have ---------------------------
    con = sqlite3.connect(copy)
    cols = [r[1] for r in con.execute("pragma table_info(work_queue)")]
    cases["TQ-B1-A3-EDGE_generation_cas"] = {
        "claim": "CAS generation single holder",
        "measured": {"columns": cols, "has_generation": any("gener" in c.lower() for c in cols),
                     "has_lease": any("lease" in c.lower() for c in cols)},
        "verdict": "NOT_IMPLEMENTED" if not any("gener" in c.lower() or "lease" in c.lower() for c in cols) else "PRESENT",
    }
    cases["TQ-B1-A3-EDGE_bounded_k"] = {
        "claim": "scan at most K blocked cards",
        "measured": "cmd_next takes no K argument and returns exactly one item",
        "verdict": "NOT_IMPLEMENTED",
    }

    doc = {
        "schema": "FHS.R21.S6.A3_CASES/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "edge": "EDGE-WO-B1-A3", "pd": "PD-03", "domain": "QUEUE_WO",
        "tool": {"path": "HG-KSEOS/scripts/work_queue.py", "sha256": sha(WQ)},
        "db": {"live": str(LIVE_DB), "live_rows": live_rows, "copy": str(copy), "copy_sha256": sha(copy),
               "copy_rows": copy_rows, "rows_match": live_rows == copy_rows,
               "note": "all mutation happened in the copy; the live spine was opened read-only"},
        "cases": cases,
        "summary": {k: v["verdict"] for k, v in cases.items()},
    }
    (S6 / "A3_CASES.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("rows", live_rows, "==", copy_rows)


if __name__ == "__main__":
    main()
