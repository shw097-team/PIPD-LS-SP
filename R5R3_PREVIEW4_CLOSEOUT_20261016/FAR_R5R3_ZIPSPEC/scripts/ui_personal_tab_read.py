# -*- coding: utf-8 -*-
"""READ-ONLY (+ one tab click): read the Personal plugins list and its install state."""
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


# click the Personal tab
for d in w.descendants(control_type="TabItem"):
    if nm(d) == "個人":
        try:
            d.click_input()
            print("clicked tab 個人")
        except Exception as e:
            print("tab click failed:", e)
        break
time.sleep(2.5)

print("title:", repr((w.window_text() or "")[:80]))
rows = []
for d in w.descendants():
    s = nm(d)
    if not s:
        continue
    try:
        r = d.rectangle()
    except Exception:
        continue
    if 560 <= r.top <= 1500 and r.left < 3600:
        rows.append((r.top, r.left, ct(d), s[:110]))
rows.sort()
print(f"--- {len(rows)} named nodes in the panel band ---")
for t, l, c, s in rows:
    print(f"  {t:>5} {l:>5} {c:<12} {s}")
