# -*- coding: utf-8 -*-
"""P1 — transient retry of artifact A on the modal that already holds it.

Follows the PLAN decision's P1: the modal still lists cand-A-preview4-served.zip, so the
probe is ONE submit press after an offline digest re-check. Falls back to the full path
if the modal is gone.
"""
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

WIN = 0x1540102
R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
ART = os.path.join(R, "host_smoke", "cand-A-preview4-served.zip")
EXPECT = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"
OUT = os.path.join(R, "FAR_R5R3_ZIPSPEC", "probe_P1.json")
steps = []


def note(s):
    steps.append(s)
    print("  " + s, flush=True)


def nm(d):
    try:
        return (d.element_info.name or "").strip()
    except Exception:
        return ""


def ct(d):
    try:
        return d.element_info.control_type or ""
    except Exception:
        return ""


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


res = {"probe": "P1-TRANSIENT-RETRY-A", "artifact": ART,
       "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
try:
    got = sha256(ART)
    res.update({"artifact_sha256": got, "artifact_bytes": os.path.getsize(ART),
                "digest_gate": "PASS" if got == EXPECT else "FAIL", "expected": EXPECT})
    note(f"offline digest gate: {'PASS' if got == EXPECT else 'FAIL'} ({got[:16]})")
    if got != EXPECT:
        raise SystemExit("digest mismatch — probe capacity zero (falsifier F5)")

    w = Desktop(backend="uia").window(handle=WIN)
    note(f"window title: {w.window_text()!r}")
    modal = None
    for d in w.descendants():
        if ct(d) == "Window" and nm(d) == "新增外掛程式":
            modal = d
            break
    note(f"modal present: {modal is not None}")
    listed = [nm(d) for d in w.descendants() if nm(d).lower().endswith(".zip")]
    res["modal_listed_files"] = listed
    note(f"modal lists: {listed}")

    if modal is None:
        res["verdict"] = "MODAL_ABSENT_FALLBACK_REQUIRED"
        raise SystemExit("modal gone — run ui_probe_matrix.py for the full path")

    prev_errors = [nm(d) for d in w.descendants() if "無法" in nm(d)]
    note(f"pre-existing error nodes: {prev_errors}")

    submit = None
    for d in modal.descendants():
        if ct(d) == "Button" and nm(d) == "新增外掛程式":
            submit = d
            break
    note(f"submit button: {submit is not None}")
    if submit is None:
        raise SystemExit("no submit button")
    try:
        submit.invoke()
        note("invoke() on 新增外掛程式 — P1 submission sent")
    except Exception as e:
        note(f"submit invoke failed: {str(e)[:60]}")

    outcome = {"errors": [], "title_changes": [], "modal_gone_at_s": None}
    prev_title = w.window_text() or ""
    for i in range(45):
        time.sleep(1.0)
        w2 = Desktop(backend="uia").window(handle=WIN)
        t = w2.window_text() or ""
        if t != prev_title:
            outcome["title_changes"].append({"t_s": i + 1, "title": t})
            note(f"[{i + 1}s] title -> {t[:80]!r}")
            prev_title = t
        errs = [nm(d) for d in w2.descendants() if "無法" in nm(d) or "請再試" in nm(d)]
        for e in errs:
            if e not in outcome["errors"]:
                outcome["errors"].append(e)
                note(f"[{i + 1}s] surface: {e!r}")
        m2 = any(ct(d) == "Window" and nm(d) == "新增外掛程式" for d in w2.descendants())
        if not m2 and outcome["modal_gone_at_s"] is None:
            outcome["modal_gone_at_s"] = i + 1
            note(f"[{i + 1}s] modal is GONE")
        if i in (4, 14, 29, 44):
            note(f"[{i + 1}s] modal={'yes' if m2 else 'no'}")
        if outcome["errors"] and i >= 4:
            break

    w2 = Desktop(backend="uia").window(handle=WIN)
    res.update({"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "outcome": outcome, "steps": steps,
                "verdict": "HOST_REJECTED_AGAIN" if outcome["errors"] else
                           ("HOST_ACCEPTED_OR_UNKNOWN" if outcome["modal_gone_at_s"] else "INCONCLUSIVE"),
                "claim_ceiling": "one retry; the surface text is the only host signal available"})
except SystemExit as e:
    res.setdefault("verdict", "ABORTED")
    res["aborted"] = str(e)
finally:
    res["steps"] = steps
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print("P1 verdict:", res.get("verdict"), "->", OUT)
