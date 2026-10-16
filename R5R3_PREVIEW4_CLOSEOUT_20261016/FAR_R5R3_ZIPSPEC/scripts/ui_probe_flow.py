# -*- coding: utf-8 -*-
"""Probe flow with navigation: ensure chatgpt.com/plugins, then upload ONE artifact.

Usage: python ui_probe_flow.py <window-handle-hex> <artifact.zip> <probe-id> [--nav]

Phases: (0) optional nav 新分頁->omnibox set_value->trusted ENTER; (1) 新增 expand;
(2) 上傳外掛程式封存檔 invoke; (3) trusted click 點選上傳; (4) picker fill + ENTER;
(5) submit 新增外掛程式; (6) poll and capture the verbatim host response.
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
WIN = int(sys.argv[1], 16)
ART = sys.argv[2]
PID = sys.argv[3]
NAV = "--nav" in sys.argv
OUT = os.path.join(R, "FAR_R5R3_ZIPSPEC", f"probe_{PID}.json")
URL = "https://chatgpt.com/plugins"
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


def desc(w):
    try:
        return list(w.descendants())
    except Exception as e:
        note("descendants err: " + str(e)[:50])
        return []


def win():
    return Desktop(backend="uia").window(handle=WIN)


def url_of(w):
    for e in desc(w):
        if ct(e) == "Edit":
            n = nm(e)
            if "網址" in n or "Address" in n or "omnibox" in n.lower():
                try:
                    return e.get_value() or ""
                except Exception:
                    return ""
    return ""


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


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


res = {"probe": PID, "artifact": ART, "window": hex(WIN), "nav_phase": NAV,
       "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
try:
    h = sha256(ART)
    res.update({"artifact_sha256": h, "artifact_bytes": os.path.getsize(ART)})
    note(f"artifact {os.path.basename(ART)} {h[:16]} {res['artifact_bytes']}B")

    # ---- leftover-dialog hygiene: a previous attempt can leave a picker and/or the modal open
    for hh in find_picker():
        try:
            d0 = Desktop(backend="uia").window(handle=hh)
            d0.set_focus(); time.sleep(0.2)
            d0.type_keys("{ESC}")
            note(f"closed leftover picker {hex(hh)}")
            time.sleep(0.8)
        except Exception as e:
            note(f"picker hygiene {hex(hh)}: {str(e)[:40]}")
    w = win()
    for d in desc(w):
        if ct(d) == "Window" and nm(d) == "新增外掛程式":
            for c in d.descendants():
                if ct(c) == "Button" and nm(c) == "取消":
                    try:
                        c.invoke(); note("cancelled leftover modal"); time.sleep(1.2)
                    except Exception as e:
                        note("cancel failed: " + str(e)[:40])
                    break
            break

    w = win()
    note(f"window title: {w.window_text()!r}")
    note(f"url before: {url_of(w)[:90]!r}")

    if NAV and "chatgpt.com/plugins" not in url_of(w):
        # new tab via the tabstrip button
        nt = None
        for d in desc(w):
            if ct(d) == "Button" and ("新分頁" in nm(d) or "New Tab" in nm(d)):
                nt = d
                break
        note(f"new-tab button: {nt is not None}")
        if nt is not None:
            try:
                nt.invoke(); note("invoke() new tab"); time.sleep(2.5)
            except Exception as e:
                note("new tab invoke: " + str(e)[:50])
        else:
            try:
                nt2 = None
                for d in desc(w):
                    if ct(d) == "TabItem":
                        nt2 = d
                        break
                if nt2 is not None:
                    nt2.click_input(); note("click_input on a tab (fallback)")
            except Exception as e:
                note("tab fallback: " + str(e)[:50])
        w = win()
        box = None
        for d in desc(w):
            if ct(d) == "Edit" and ("網址" in nm(d) or "Address" in nm(d)):
                box = d
                break
        note(f"omnibox: {box is not None}")
        if box is not None:
            try:
                box.set_focus(); time.sleep(0.3)
                box.set_edit_text(URL)
                note("omnibox set to " + URL)
                time.sleep(0.4)
                box.type_keys("{ENTER}")
                note("ENTER sent to omnibox (trusted)")
            except Exception as e:
                note("omnibox drive failed: " + str(e)[:60])
        for i in range(24):
            time.sleep(1.0)
            w = win()
            u = url_of(w)
            if "chatgpt.com/plugins" in u:
                note(f"[{i + 1}s] navigated: {u[:70]!r}")
                break
        else:
            w = win()
            note("navigation unconfirmed; url=" + url_of(w)[:70])

    w = win()
    res["url_before_upload"] = url_of(w)

    # 1. open the add-menu
    add = None
    for d in desc(w):
        if ct(d) == "Button" and nm(d) == "新增":
            add = d
            break
    note(f"add button: {add is not None}")
    if add is None:
        raise SystemExit("no 新增 button on the plugins surface")
    for meth in ("expand", "invoke"):
        try:
            getattr(add, meth)(); note(f"add {meth}() ok"); break
        except Exception as e:
            note(f"add {meth}: {str(e)[:40]}")
    time.sleep(1.2)

    w = win()
    up = None
    for d in desc(w):
        if "上傳外掛程式封存檔" in nm(d):
            up = d
            break
    note(f"upload menu item: {up is not None}")
    if up is None:
        raise SystemExit("no upload menu item")
    for meth in ("invoke", "click_input"):
        try:
            getattr(up, meth)(); note(f"menu {meth}() ok"); break
        except Exception as e:
            note(f"menu {meth}: {str(e)[:40]}")
    time.sleep(1.5)

    # 2. modal -> trusted click on 點選上傳
    w = win()
    pick = None
    for d in desc(w):
        if ct(d) == "Button" and "點選上傳" in nm(d):
            pick = d
            break
    note(f"點選上傳: {pick is not None}")
    if pick is None:
        raise SystemExit("no 點選上傳 in the modal")
    try:
        pick.set_focus(); time.sleep(0.3)
        pick.click_input(); note("trusted click_input on 點選上傳")
    except Exception as e:
        note("click_input failed: " + str(e)[:60])

    hs = []
    for _ in range(24):
        time.sleep(0.5)
        hs = find_picker()
        if hs:
            break
    note(f"picker windows: {[hex(x) for x in hs]}")
    if not hs:
        raise SystemExit("picker never opened")

    # 3. fill picker + ENTER
    dlg = Desktop(backend="uia").window(handle=hs[-1])
    edit = None
    for i in range(24):                      # poll: the UIA tree needs a moment after the dialog appears
        time.sleep(0.5)
        try:
            for d in desc(dlg):
                if ct(d) == "Edit" and nm(d) == "檔案名稱(N):":
                    edit = d
                    break
        except Exception as e:
            note(f"picker enum err: {str(e)[:40]}")
        if edit is not None:
            note(f"filename edit ready after {(i + 1) * 0.5:.1f}s")
            break
    if edit is None:
        raise SystemExit("no filename edit in picker")
    edit.set_focus(); time.sleep(0.3)
    native = ART.replace("/", "\\")          # Win32 common dialogs reject forward slashes
    edit.set_edit_text(native); time.sleep(0.4)
    res["picker_value_written"] = native
    try:
        note("picker value: " + repr(edit.iface_value.CurrentValue)[:120])
    except Exception:
        pass
    dlg.set_focus(); time.sleep(0.3)
    dlg.type_keys("{ENTER}"); note("ENTER sent to picker")
    closed = False
    for i in range(16):
        time.sleep(0.5)
        if not find_picker():
            note(f"picker closed {(i + 1) * 0.5:.1f}s")
            closed = True
            break
    if not closed:
        note("picker STILL OPEN after 8s — falling back to the 開啟(O) button")
        w2 = win()
        ob = None
        for d in desc(w2):
            try:
                if ct(d) in ("SplitButton", "Button") and "開啟(O)" in nm(d):
                    ob = d
                    break
            except Exception:
                continue
        note(f"開啟(O) button: {ob is not None}")
        if ob is not None:
            for meth in ("invoke", "click_input"):
                try:
                    getattr(ob, meth)(); note(f"open button {meth}() ok")
                    break
                except Exception as e:
                    note(f"open button {meth}: {str(e)[:40]}")
        for i in range(16):
            time.sleep(0.5)
            if not find_picker():
                note(f"picker closed after fallback {(i + 1) * 0.5:.1f}s")
                closed = True
                break
    res["picker_closed"] = closed
    if not closed:
        raise SystemExit("picker would not close — probe aborted, nothing submitted")

    # 4. submit
    time.sleep(1.5)
    w = win()
    modal_el = None
    for d in desc(w):
        if ct(d) == "Window" and nm(d) == "新增外掛程式":
            modal_el = d
            break
    listed = []
    if modal_el is not None:
        try:
            listed = [nm(d) for d in modal_el.descendants() if nm(d).lower().endswith(".zip")]
        except Exception:
            listed = []
    note(f"modal lists: {listed}")
    res["modal_listed_files"] = listed
    res["modal_present_at_submit"] = modal_el is not None
    submit = None
    pool = modal_el.descendants() if modal_el is not None else desc(w)
    for d in pool:
        if ct(d) == "Button" and nm(d) == "新增外掛程式":
            submit = d
            break
    if submit is None:
        raise SystemExit("no submit button")
    for meth in ("invoke", "click_input"):
        try:
            getattr(submit, meth)(); note(f"submit {meth}() ok"); break
        except Exception as e:
            note(f"submit {meth}: {str(e)[:60]}")

    # 5. poll
    outcome = {"errors": [], "title_changes": [], "modal_gone_at_s": None}
    prev_title = (win().window_text() or "")
    for i in range(45):
        time.sleep(1.0)
        w = win()
        t = w.window_text() or ""
        if t != prev_title:
            outcome["title_changes"].append({"t_s": i + 1, "title": t})
            note(f"[{i + 1}s] title -> {t[:80]!r}")
            prev_title = t
        for e in [nm(d) for d in desc(w) if "無法" in nm(d) or "請再試" in nm(d)]:
            if e not in outcome["errors"]:
                outcome["errors"].append(e)
                note(f"[{i + 1}s] surface: {e!r}")
        m = any(ct(d) == "Window" and nm(d) == "新增外掛程式" for d in desc(w))
        if not m and outcome["modal_gone_at_s"] is None:
            outcome["modal_gone_at_s"] = i + 1
            note(f"[{i + 1}s] modal gone")
        if i in (4, 14, 29, 44):
            note(f"[{i + 1}s] modal={'yes' if m else 'no'} url={url_of(w)[:50]}")
        if outcome["errors"] and i >= 4:
            break

    w = win()
    res.update({"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "url_after": url_of(w), "window_title_after": w.window_text(),
                "outcome": outcome,
                "verdict": "HOST_REJECTED" if outcome["errors"] else
                           ("HOST_ACCEPTED_OR_CHANGED" if outcome["modal_gone_at_s"] else "INCONCLUSIVE"),
                "claim_ceiling": "one UI attempt; the surface text is the only host signal"})
except SystemExit as e:
    res["aborted"] = str(e)
    res.setdefault("verdict", "ABORTED")
finally:
    res["steps"] = steps
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print("verdict:", res.get("verdict"), "->", OUT)
