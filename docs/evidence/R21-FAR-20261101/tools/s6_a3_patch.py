"""Candidate patch for the A3 duplicate-claim defect, with the pre/post pair.

Measured (s6/A3_CASES.json): cmd_settle has no state guard, so the same item can be settled twice and the second
write silently replaces the first -- the body's TQ-B1-A3-NEG ("duplicate claim ... LOST_LEASE_OR_DUPLICATE_CLAIM")
is violated. It also accepts a PASS with an empty evidence_ref, which is how a PASS can exist with nothing to check.

Canonical HG-KSEOS/scripts/work_queue.py is NOT edited; the patch targets a copy and the tests run that copy
against a scratch DB (never the spine).
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
PATCH = S6 / "patch"
SRC = ROOT / "HG-KSEOS" / "scripts" / "work_queue.py"
LIVE_DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build():
    PATCH.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")
    old = '''    con = connect()
    cur = con.execute("SELECT state FROM work_queue WHERE wp_id=?", (args.wp,))
    if cur.fetchone() is None:
        print(json.dumps({"error": "UNKNOWN_WP", "wp": args.wp}))
        return 2
    con.execute("UPDATE work_queue SET state=?, evidence_ref=?, updated_at=? WHERE wp_id=?",
                (args.verdict, args.evidence, now(), args.wp))'''
    if old not in text:
        raise SystemExit("settle anchor not found; refusing to guess")
    new = '''    con = connect()
    cur = con.execute("SELECT state, evidence_ref FROM work_queue WHERE wp_id=?", (args.wp,))
    row = cur.fetchone()
    if row is None:
        print(json.dumps({"error": "UNKNOWN_WP", "wp": args.wp}))
        return 2
    prior_state, prior_evidence = row
    # A3: a second settle of an already-terminal item is a duplicate claim, not a correction.
    if prior_state == "PASS":
        print(json.dumps({"error": "ERR_ALREADY_SETTLED", "wp": args.wp, "state": prior_state,
                          "detail": "terminal PASS may not be overwritten; use unsettle with a named reason"}))
        return 7
    if prior_evidence and getattr(args, "evidence", None) == prior_evidence:
        print(json.dumps({"error": "ERR_DUPLICATE_CLAIM", "wp": args.wp, "evidence": prior_evidence}))
        return 7
    if getattr(args, "verdict", None) in ("PASS", "BLOCKED") and not (getattr(args, "evidence", "") or "").strip():
        print(json.dumps({"error": "ERR_EVIDENCE_REQUIRED", "wp": args.wp, "verdict": args.verdict,
                          "detail": "PASS/BLOCKED must name the artefact that proves it"}))
        return 8
    con.execute("UPDATE work_queue SET state=?, evidence_ref=?, updated_at=? WHERE wp_id=?",
                (args.verdict, args.evidence, now(), args.wp))'''
    text2 = text.replace(old, new, 1)
    dst = PATCH / "work_queue.py"
    dst.write_text(text2, encoding="utf-8", newline="\n")
    import difflib
    diff = difflib.unified_diff(text.splitlines(True), text2.splitlines(True),
                                fromfile="a/HG-KSEOS/scripts/work_queue.py",
                                tofile="b/HG-KSEOS/scripts/work_queue.py", n=3)
    (PATCH / "work_queue.settle.patch").write_text("".join(diff), encoding="utf-8", newline="\n")
    return dst


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
    copy = build()
    spec = importlib.util.spec_from_file_location("wq_patched", copy)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    db = S6 / "queue_patch_test.db"
    if db.exists():
        db.unlink()
    shutil.copyfile(LIVE_DB, db)
    mod.DB = db
    con = sqlite3.connect(db)
    con.execute("insert or replace into work_queue (wp_id,title,depends_on,effect_class,state,evidence_ref,updated_at)"
                " values ('WP-FHS-91','A3 patch test row','','HOST_OP','NOT_RUN',NULL,?)",
                (time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),))
    con.commit(); con.close()

    t1 = call(mod, mod.cmd_settle, wp="WP-FHS-91", verdict="PASS", evidence="A3-PATCH-evidence-1")
    t2 = call(mod, mod.cmd_settle, wp="WP-FHS-91", verdict="PASS", evidence="A3-PATCH-evidence-2")
    t3 = call(mod, mod.cmd_settle, wp="WP-FHS-91", verdict="FAIL", evidence="A3-PATCH-overwrite")
    con = sqlite3.connect(db)
    con.execute("insert or replace into work_queue (wp_id,title,depends_on,effect_class,state,evidence_ref,updated_at)"
                " values ('WP-FHS-92','A3 patch test row 2','','HOST_OP','NOT_RUN',NULL,?)",
                (time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()),))
    con.commit(); con.close()
    t4 = call(mod, mod.cmd_settle, wp="WP-FHS-92", verdict="PASS", evidence="")

    tests = {
        "T1_first_settle_accepted": {"expect": "rc=0", "got": {"rc": t1[0], **t1[1]},
                                     "verdict": "PASS" if t1[0] == 0 else "FAIL"},
        "T2_second_settle_refused": {"expect": "rc=7 ERR_ALREADY_SETTLED",
                                     "got": {"rc": t2[0], **t2[1]},
                                     "verdict": "PASS" if t2[0] == 7 else "FAIL"},
        "T3_overwrite_with_fail_refused": {"expect": "rc=7 ERR_ALREADY_SETTLED",
                                           "got": {"rc": t3[0], **t3[1]},
                                           "verdict": "PASS" if t3[0] == 7 else "FAIL"},
        "T4_evidenceless_pass_refused": {"expect": "rc=8 ERR_EVIDENCE_REQUIRED",
                                         "got": {"rc": t4[0], **t4[1]},
                                         "verdict": "PASS" if t4[0] == 8 else "FAIL"},
    }
    doc = {
        "schema": "FHS.R21.S6.A3_PATCH_TEST/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "canonical_untouched": {"path": "HG-KSEOS/scripts/work_queue.py", "sha256": sha(SRC)},
        "patch": {"file": "s6/patch/work_queue.settle.patch",
                  "bytes": (PATCH / "work_queue.settle.patch").stat().st_size,
                  "sha256": sha(PATCH / "work_queue.settle.patch"),
                  "patched_copy_sha256": sha(copy)},
        "pre_state": {"ref": "s6/A3_CASES.json", "duplicate_claim": "FAIL_DUPLICATE_ACCEPTED"},
        "tests": tests,
        "summary": {k: v["verdict"] for k, v in tests.items()},
        "claim_ceiling": ("candidate patch proven on a copy against a scratch DB; the canonical queue tool still "
                          "accepts duplicate claims and evidenceless PASSes until an authorised change lands"),
    }
    (S6 / "A3_PATCH_TEST.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps(doc["summary"], ensure_ascii=False, indent=1))
    print("t2:", t2[0], t2[1].get("error"), "| t4:", t4[0], t4[1].get("error"))


if __name__ == "__main__":
    main()
