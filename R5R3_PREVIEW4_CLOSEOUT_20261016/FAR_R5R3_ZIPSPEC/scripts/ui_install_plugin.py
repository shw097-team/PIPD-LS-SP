# -*- coding: utf-8 -*-
"""Install the currently-open plugin: click its 安裝 button, then read the resulting state.

Owner-directed action (PRIVATE_HOST_INSTALL for this one plugin, granted in-session by the owner).
Reads before acting, and prints every state-bearing node before and after so the change is visible.
"""
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


def url():
    for e in w.descendants(control_type="Edit"):
        if nm(e) == "網址與搜尋列":
            try:
                return (e.get_value() or "")[:120]
            except Exception:
                return ""
    return ""


KEYS = ("安裝", "已安裝", "移除", "解除", "更多操作", "試用", "對話", "版本", "無法", "取得")


def state(tag):
    print(f"--- {tag} | title={w.window_text()[:70]!r} | url={url()}")
    for d in w.descendants():
        s = nm(d)
        if s and any(k in s for k in KEYS):
            try:
                r = d.rectangle()
                box = f"({r.left},{r.top},{r.right},{r.bottom})"
            except Exception:
                box = ""
            print(f"    {ct(d):<11} {s[:60]:<60} {box}")


state("BEFORE")

target = None
for d in w.descendants(control_type="Button"):
    s = nm(d)
    if s.startswith("安裝外掛程式") or s.startswith("安裝 PIPD") or s == "安裝":
        target = d
        break
if target is None:
    print("NO_INSTALL_BUTTON_FOUND")
    raise SystemExit(2)

print("install button:", repr(nm(target)))
done = False
try:
    target.invoke()
    done = True
    print("invoke() ok")
except Exception as e:
    print("invoke() failed:", e)
if not done:
    try:
        target.click_input()
        print("click_input() ok")
    except Exception as e:
        print("click_input() failed:", e)

time.sleep(3)
state("AFTER 3s")

# a confirmation dialog may appear: click its primary button
for d in w.descendants(control_type="Button"):
    s = nm(d)
    if s in ("安裝", "確認", "確定", "繼續", "Install", "Confirm"):
        try:
            d.click_input()
            print("confirm clicked:", s)
            time.sleep(3)
        except Exception as e:
            print("confirm failed:", e)
        break
state("FINAL")
