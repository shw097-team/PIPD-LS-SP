# -*- coding: utf-8 -*-
"""Continue a probe from an ALREADY-OPEN native picker: fill -> ENTER -> submit -> read outcome.

Usage: python ui_probe_after_picker.py <artifact.zip> <probe-id>
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

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
ART = sys.argv[1]
PID = sys.argv[2]
WIN = 0x20622
OUT = os.path.join(R, "FAR_R5R3_ZIPSPEC", f"probe_{PID}.json")
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


def win():
    return Desktop(backend="uia").window(handle=WIN)


def find_picker():
    u = ctypes.windll.user32
    PTR = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    hits = []

    def cb(h, lp):
        b = ctypes.create_unicode_buffer(300)
        u.GetClassNameW(h, b, 300)
        if "32770" in b.value:
            t = ctypes.create_unicode_buffer(300)
            u.GetWindowTextW(h, t, 300)
            if "開啟" in t.value or "Open" in t.value:
                hits.append(h)
        return True

    u.EnumWindows(PTR(cb), 0)
    return hits


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


res = {"probe": PID, "artifact": ART, "window": hex(WIN), "resumed_from_open_picker": True,
       "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
try:
    h = sha256(ART)
    res.update({"artifact_sha256": h, "artifact_bytes": os.path.getsize(ART)})
    note(f"artifact {os.path.basename(ART)} {h[:16]}")

    hs = find_picker()
    res["picker_handles_at_resume"] = [hex(x) for x in hs]
    note(f"open pickers: {[hex(x) for x in hs]}")
    if not hs:
        raise SystemExit("no open picker to resume from")

    dlg = Desktop(backend="uia").window(handle=hs[-1])
    edit = None
    for i in range(24):                      # poll for a ready UIA tree
        time.sleep(0.5)
        try:
            for d in dlg.descendants():
                if ct(d) == "Edit" and nm(d) == "檔案名稱(N):":
                    edit = d
                    break
        except Exception as e:
            note(f"enum err: {str(e)[:40]}")
        if edit is not None:
            note(f"filename edit ready after {(i + 1) * 0.5:.1f}s")
            break
    if edit is None:
        raise SystemExit("filename edit never appeared")

    native = ART.replace("/", "\\")
    edit.set_focus(); time.sleep(0.3)
    edit.set_edit_text(native); time.sleep(0.4)
    res["picker_value_written"] = native
    try:
        note("picker value: " + repr(edit.iface_value.CurrentValue)[:120])
    except Exception:
        pass
    dlg.set_focus(); time.sleep(0.3)
    dlg.type_keys("{ENTER}")
    note("ENTER sent")

    closed = False
    for i in range(30):
        time.sleep(0.5)
        if not find_picker():
            note(f"picker closed {(i + 1) * 0.5:.1f}s")
            closed = True
            break
    if not closed:
        note("still open — trying 開啟(O)")
        w2 = win()
        ob = None
        for d in w2.descendants():
            try:
                if ct(d) in ("SplitButton", "Button") and nm(d) == "開啟(O)":
                    ob = d
                    break
            except Exception:
                continue
        note(f"開啟(O): {ob is not None}")
        if ob is not None:
            try:
                ob.click_input(); note("click_input 開啟(O)")
            except Exception as e:
                note("open button: " + str(e)[:50])
            for i in range(20):
                time.sleep(0.5)
                if not find_picker():
                    closed = True
                    note(f"closed after fallback {(i + 1) * 0.5:.1f}s")
                    break
    res["picker_closed"] = closed
    if not closed:
        raise SystemExit("picker would not close; nothing submitted")

    time.sleep(2.0)
    w = win()
    modal_el = None
    for d in w.descendants():
        if ct(d) == "Window" and nm(d) == "新增外掛程式":
            modal_el = d
            break
    listed = []
    if modal_el is not None:
        try:
            listed = [nm(d) for d in modal_el.descendants() if nm(d).lower().endswith(".zip")]
        except Exception:
            pass
    note(f"modal present: {modal_el is not None} lists: {listed}")
    res["modal_listed_files"] = listed
    if modal_el is None:
        raise SystemExit("modal gone after picker — cannot submit")
    submit = None
    for d in modal_el.descendants():
        if ct(d) == "Button" and nm(d) == "新增外掛程式":
            submit = d
            break
    note(f"submit button: {submit is not None}")
    if submit is None:
        raise SystemExit("no submit button")
    for meth in ("click_input", "invoke"):
        try:
            getattr(submit, meth)(); note(f"submit {meth}() ok"); break
        except Exception as e:
            note(f"submit {meth}: {str(e)[:60]}")

    outcome = {"errors": [], "title_changes": [], "modal_gone_at_s": None}
    prev = (win().window_text() or "")
    for i in range(45):
        time.sleep(1.0)
        w = win()
        t = w.window_text() or ""
        if t != prev:
            outcome["title_changes"].append({"t_s": i + 1, "title": t})
            note(f"[{i + 1}s] title -> {t[:80]!r}")
            prev = t
        for e in [nm(d) for d in w.descendants() if "無法" in nm(d) or "請再試" in nm(d)]:
            if e not in outcome["errors"]:
                outcome["errors"].append(e)
                note(f"[{i + 1}s] surface: {e!r}")
        m = any(ct(d) == "Window" and nm(d) == "新增外掛程式" for d in w.descendants())
        if not m and outcome["modal_gone_at_s"] is None:
            outcome["modal_gone_at_s"] = i + 1
            note(f"[{i + 1}s] modal gone")
        if i in (4, 14, 29, 44):
            note(f"[{i + 1}s] modal={'yes' if m else 'no'}")
        if outcome["errors"] and i >= 4:
            break

    res.update({"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "outcome": outcome,
                "verdict": "HOST_REJECTED" if outcome["errors"] else
                           ("HOST_ACCEPTED_OR_CHANGED" if outcome["modal_gone_at_s"] else "INCONCLUSIVE"),
                "claim_ceiling": "one UI attempt on one artifact; the surface text is the only host signal"})
except SystemExit as e:
    res["aborted"] = str(e)
    res.setdefault("verdict", "ABORTED")
finally:
    res["steps"] = steps
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print("verdict:", res.get("verdict"), "->", OUT)
