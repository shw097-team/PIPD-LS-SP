# -*- coding: utf-8 -*-
"""Switch to the plugin tab by title and read its install state (read-only apart from the tab switch)."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

W = 0x20622
NEEDLE = sys.argv[1] if len(sys.argv) > 1 else "PIPD-LS-SP Public Skills_P4"
w = Desktop(backend="uia").window(handle=W)


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


tabs = [(nm(d), d) for d in w.descendants(control_type="TabItem")]
print("tabs:", [t for t, _ in tabs])
target = next((d for t, d in tabs if NEEDLE in t), None)
if target is None:
    print("TAB_NOT_FOUND")
    raise SystemExit(2)
try:
    target.click_input()
    print("switched to tab:", nm(target)[:70])
except Exception as e:
    print("tab click failed:", e)
time.sleep(2.5)

print("title:", repr(w.window_text()[:80]))
url = ""
for e in w.descendants(control_type="Edit"):
    if nm(e) == "網址與搜尋列":
        try:
            url = (e.get_value() or "")[:120]
        except Exception:
            pass
print("url:", url)

KEYS = ("安裝", "已安裝", "移除", "解除", "更多操作", "試用", "版本", "關閉對話框", "技能", "提供")
rows = []
for d in w.descendants():
    s = nm(d)
    if s and any(k in s for k in KEYS):
        try:
            r = d.rectangle()
            if r.top < 0:
                continue
            box = f"({r.left},{r.top},{r.right},{r.bottom})"
        except Exception:
            box = ""
        rows.append((r.top if box else 0, ct(d), s[:60], box))
rows.sort()
print(f"--- {len(rows)} state-bearing nodes (on-screen only) ---")
for t, c, s, b in rows[:30]:
    print(f"  {c:<11} {s:<60} {b}")
