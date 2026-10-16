# -*- coding: utf-8 -*-
"""READ-ONLY: dump the named UIA nodes of a Chrome window to find the plugins add surface."""
import sys

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


print("window:", repr((w.window_text() or "")[:90]), "handle", hex(WIN))
rows = []
for d in w.descendants():
    s = nm(d)
    if not s:
        continue
    try:
        r = d.rectangle()
        rect = f"({r.left},{r.top},{r.right},{r.bottom})"
    except Exception:
        rect = ""
    rows.append((ct(d), s, rect))
print(f"named nodes: {len(rows)}")
KEYS = ("外掛", "新增", "上傳", "管理", "安裝", "移除", "刪除", "版本", "Plugin_",
        "plugins", "網址", "搜尋", "返回", "首頁", "個人", "公開", "個人化")
for c, s, r in rows:
    if any(k in s for k in KEYS) or "Plugin_" in s:
        print(f"  {c:<12} {s[:80]:<80} {r}")
print("--- all Buttons ---")
for c, s, r in rows:
    if c in ("Button", "Hyperlink", "TabItem", "MenuItem"):
        print(f"  {c:<12} {s[:70]:<70} {r}")
