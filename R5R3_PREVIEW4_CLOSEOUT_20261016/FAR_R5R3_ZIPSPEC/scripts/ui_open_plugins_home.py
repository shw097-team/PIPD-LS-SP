# -*- coding: utf-8 -*-
"""Navigate back to the plugins HOME (sidebar 外掛程式) and report the add surface."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

WIN = int(sys.argv[1], 16) if len(sys.argv) > 1 else 0x20622
w = Desktop(backend="uia").window(handle=WIN)


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


def url_of(w):
    for e in w.descendants():
        try:
            if (e.element_info.control_type or "") == "Edit" and "網址" in nm(e):
                return e.get_value() or ""
        except Exception:
            continue
    return ""


print("title before:", repr((w.window_text() or "")[:80]))
print("url before:", url_of(w))

sb = None
for d in w.descendants():
    if ct(d) == "Button" and nm(d) == "外掛程式":
        r = d.rectangle()
        if r.left < 600:          # sidebar copy, not the top hyperlink
            sb = d
            break
print("sidebar 外掛程式 button:", sb is not None)
if sb is not None:
    for meth in ("invoke", "click_input"):
        try:
            getattr(sb, meth)()
            print(f"{meth}() ok")
            break
        except Exception as e:
            print(f"{meth}: {str(e)[:50]}")
    time.sleep(3.5)

w = Desktop(backend="uia").window(handle=WIN)
print("title after:", repr((w.window_text() or "")[:80]))
print("url after:", url_of(w))

print("--- add surface scan ---")
hits = []
for d in w.descendants():
    s = nm(d)
    if not s:
        continue
    if any(k in s for k in ("新增", "上傳", "管理", "個人", "公開", "你的雲端", "搜尋外掛")):
        try:
            r = d.rectangle()
            rect = f"({r.left},{r.top},{r.right},{r.bottom})"
        except Exception:
            rect = ""
        hits.append((ct(d), s[:70], rect))
for c, s, r in hits:
    print(f"  {c:<12} {s:<70} {r}")
print("hits:", len(hits))
