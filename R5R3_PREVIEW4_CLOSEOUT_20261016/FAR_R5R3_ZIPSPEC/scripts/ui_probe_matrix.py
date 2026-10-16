# -*- coding: utf-8 -*-
"""Reusable FDA probe driver: upload ONE candidate archive to the live plugins surface.

Usage:  python ui_probe_matrix.py <candidate.zip> <probe-id>
Emits:  FAR_R5R3_ZIPSPEC/probe_<id>.json   (verbatim host response + evidence)

Mechanics reused from the proven R5Y lane:
  menu    : ExpandCollapsePattern(expand) on 新增  ->  invoke('上傳外掛程式封存檔')
  picker  : background UIA cannot get user activation, so ONE trusted click
            (pywinauto click_input, foreground) on 點選上傳, then the native common
            dialog is filled via UIA ValuePattern and submitted with a trusted ENTER.
  submit  : invoke('新增外掛程式') inside the portal dialog.
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
ART = sys.argv[1]
PID = sys.argv[2] if len(sys.argv) > 2 else "p0"
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


def descend(w):
    try:
        return list(w.descendants())
    except Exception as e:
        print("  descendants err:", str(e)[:60])
        return []


def find(w, name, ctype=None, exact=True):
    for d in descend(w):
        s = nm(d)
        if not s:
            continue
        ok = (s == name) if exact else (name in s)
        if ok and (ctype is None or ct(d) == ctype):
            return d
    return None


def win():
    return Desktop(backend="uia").window(handle=WIN)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def find_picker():
    user32 = ctypes.windll.user32
    PTR = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    hits = []

    def cb(h, lp):
        b = ctypes.create_unicode_buffer(300)
        user32.GetClassNameW(h, b, 300)
        if "32770" in b.value:
            t = ctypes.create_unicode_buffer(300)
            user32.GetWindowTextW(h, t, 300)
            if "開啟" in t.value or "Open" in t.value:
                hits.append(h)
        return True

    user32.EnumWindows(PTR(cb), 0)
    return hits


def url_of(w):
    for e in descend(w):
        if ct(e) == "Edit" and nm(e) == "網址與搜尋列":
            try:
                return e.get_value() or ""
            except Exception:
                return ""
    return ""


def page_text(w):
    seen = []
    for d in descend(w):
        s = nm(d)
        if s and s not in seen:
            seen.append(s)
    return seen


res = {"probe": PID, "artifact": ART, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
try:
    res["artifact_sha256"] = sha256(ART)
    res["artifact_bytes"] = os.path.getsize(ART)
    note(f"artifact {os.path.basename(ART)} sha256={res['artifact_sha256'][:16]} bytes={res['artifact_bytes']}")

    w = win()
    note(f"window title: {w.window_text()!r}")

    # 1. cancel any leftover modal
    for _ in range(3):
        m = find(w, "新增外掛程式", "Window")
        if not m:
            break
        c = find(m, "取消", "Button")
        if c:
            try:
                c.invoke(); note("cancelled leftover modal"); time.sleep(1.2)
            except Exception as e:
                note(f"cancel failed: {str(e)[:50]}")
        else:
            note("no cancel button inside modal")
        w = win()

    # 2. open add-menu
    add = None
    for d in descend(w):
        if ct(d) == "Button" and nm(d) == "新增":
            add = d
            break
    if add is None:
        add = find(w, "新增", "Button")
    note(f"add button found: {add is not None}")
    if add is None:
        raise SystemExit("no 新增 button")
    try:
        add.expand(); note("expand() on 新增")
    except Exception as e:
        note(f"expand fail: {type(e).__name__}:{str(e)[:40]}")
        try:
            add.invoke(); note("invoke() on 新增 instead")
        except Exception as e2:
            note(f"invoke fail: {str(e2)[:40]}")
    time.sleep(1.0)

    w = win()
    up = None
    for d in descend(w):
        s = nm(d)
        if "上傳外掛程式封存檔" in s:
            up = d
            break
    note(f"upload menu item: {up is not None} ({nm(up) if up else '-'})")
    if up is None:
        raise SystemExit("no upload menu item")
    for meth in ("invoke", "click_input"):
        try:
            getattr(up, meth)(); note(f"menu item {meth}() ok"); break
        except Exception as e:
            note(f"menu item {meth}: {str(e)[:50]}")
    time.sleep(1.5)

    # 3. modal -> trusted click on 點選上傳
    w = win()
    pick = None
    for d in descend(w):
        if ct(d) == "Button" and "點選上傳" in nm(d):
            pick = d
            break
    note(f"點選上傳 button: {pick is not None}")
    if pick is None:
        raise SystemExit("no 點選上傳")
    try:
        pick.set_focus(); time.sleep(0.3)
        pick.click_input(); note("click_input() on 點選上傳 (trusted, foreground)")
    except Exception as e:
        note(f"click_input fail: {str(e)[:60]}")

    hs = []
    for _ in range(20):
        time.sleep(0.5)
        hs = find_picker()
        if hs:
            break
    note(f"picker windows: {[hex(h) for h in hs]}")
    if not hs:
        raise SystemExit("picker never opened")

    # 4. fill picker + trusted ENTER
    dlg = Desktop(backend="uia").window(handle=hs[-1])
    edit = None
    for d in descend(dlg):
        if ct(d) == "Edit" and nm(d) == "檔案名稱(N):":
            edit = d
            break
    if edit is None:
        raise SystemExit("no filename edit in picker")
    edit.set_focus(); time.sleep(0.3)
    edit.set_edit_text(ART); time.sleep(0.4)
    try:
        note("picker value: " + repr(edit.iface_value.CurrentValue)[:120])
    except Exception:
        pass
    dlg.set_focus(); time.sleep(0.3)
    dlg.type_keys("{ENTER}"); note("ENTER sent to picker")
    for i in range(24):
        time.sleep(0.5)
        if not find_picker():
            note(f"picker closed after {(i + 1) * 0.5:.1f}s")
            break
    else:
        note("picker STILL OPEN after 12s")

    # 5. read the modal, then submit
    time.sleep(1.5)
    w = win()
    listed = ""
    for d in descend(w):
        s = nm(d)
        if s.lower().endswith(".zip"):
            listed = s
            break
    note(f"modal lists file: {listed!r}")
    submit = None
    m = find(w, "新增外掛程式", "Window")
    if m:
        for d in descend(m):
            if ct(d) == "Button" and nm(d) == "新增外掛程式":
                submit = d
                break
    if submit is None:
        raise SystemExit("no submit button")
    try:
        submit.invoke(); note("invoke() on 新增外掛程式 (submit)")
    except Exception as e:
        note(f"submit invoke fail: {str(e)[:60]}")

    # 6. poll the outcome
    prev_title = (w.window_text() or "")
    outcome = {"host_response_verbatim": None, "title_changes": [], "errors": []}
    for i in range(40):
        time.sleep(1.0)
        w = win()
        t = (w.window_text() or "")
        if t != prev_title:
            outcome["title_changes"].append({"t_s": i + 1, "title": t})
            note(f"[{i + 1}s] title -> {t[:80]!r}")
            prev_title = t
        for d in descend(w):
            s = nm(d)
            if s and any(k in s for k in ("無法", "請再試", "錯誤", "失敗", "不支援", "無效")):
                if s not in outcome["errors"]:
                    outcome["errors"].append(s)
                    note(f"[{i + 1}s] surface says: {s!r}")
        if i in (3, 9, 19, 39):
            note(f"[{i + 1}s] modal={'yes' if find(w, '新增外掛程式', 'Window') else 'no'} url={url_of(w)[:60]}")
        if outcome["errors"] and i >= 4:
            break

    w = win()
    res.update({
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "window_title": w.window_text(),
        "url": url_of(w),
        "modal_present": bool(find(w, "新增外掛程式", "Window")),
        "outcome": outcome,
        "named_nodes_sample": page_text(w)[:120],
        "steps": steps,
        "verdict": ("HOST_REJECTED" if outcome["errors"] else
                    ("HOST_ACCEPTED?" if outcome["title_changes"] else "INCONCLUSIVE")),
        "claim_ceiling": "one UI attempt on one artifact; the surface text is the only host signal",
    })
except SystemExit as e:
    res.update({"aborted": str(e), "steps": steps, "verdict": "ABORTED"})
finally:
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print("verdict:", res.get("verdict"), "->", OUT)
