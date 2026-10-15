"""Extract the agent message text (the checker verdict) from a lane attempt's raw stdout JSONL."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

R = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close/VERIFY3")


def resolve(p: str) -> Path:
    p = p.replace("\\", "/")
    marker = "/VERIFY3/"
    if marker in p:
        return R / p.split(marker, 1)[1]
    if p.startswith("//"):
        p = p[1:]
    candidates = [Path(p), Path("/c/c" + p[2:]) if p.startswith("/c/") else None]
    for c in candidates:
        if c and c.exists():
            return c
    raise SystemExit(f"not found: {p}")


for receipt, out in (("dispatch_receipt5.json", "checker_verdict_armB2_raw.txt"),
                     ("dispatch_receipt3.json", "checker_verdict_armB_raw.txt"),
                     ("dispatch_receipt2.json", "checker_verdict_armA_raw.txt")):
    rp = R / receipt
    if not rp.exists():
        print(receipt, "absent")
        continue
    d = json.loads(rp.read_text(encoding="utf-8"))
    a = d["attempts"][0]
    print(receipt, "rank", d.get("used_rank"), d.get("used_transport_model"), "ok", d.get("ok"), "secs", d.get("used_seconds"))
    try:
        p = resolve(a["stdout_path"])
    except SystemExit as exc:
        print("  ", exc)
        continue
    msgs = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        it = o.get("item") or {}
        if o.get("type") == "item.completed" and it.get("type") == "agent_message":
            msgs.append(it.get("text", ""))
    text = msgs[-1] if msgs else ""
    (R / out).write_text(text, encoding="utf-8")
    print("  wrote", out, len(text), "bytes")
    print(text[:3000])
    print("=" * 60)
