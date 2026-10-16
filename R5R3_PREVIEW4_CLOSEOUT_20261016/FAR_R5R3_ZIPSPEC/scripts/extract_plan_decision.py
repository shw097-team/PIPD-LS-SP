# -*- coding: utf-8 -*-
"""Minimal, disclosed repair of the PLAN lane's JSON, then extract a clean decision file."""
import json
import re

R = r"C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout"
raw = open(R + r"\raw\plan_far_glm.log", encoding="utf-8").read()
i, j = raw.index("{"), raw.rindex("}")
body = raw[i:j + 1]

# repair 1: strip C0 control characters that are illegal inside JSON strings
sanitised = "".join(ch for ch in body if ch == "\n" or ord(ch) >= 32)
try:
    d = json.loads(sanitised)
    how = "control-character sanitation only"
except Exception as e1:
    print("after sanitation still invalid:", str(e1)[:120])
    # repair 2: replace the malformed precondition value with a clean restatement
    fixed = re.sub(r'"precondition_every_probe"\s*:\s*"[^"]*"',
                   '"precondition_every_probe": "Every probe: re-check the file\'s sha256 offline '
                   'against host_smoke/CANDIDATES.json and run zipfile.testzip() clean before upload."',
                   sanitised, count=1, flags=re.S)
    try:
        d = json.loads(fixed)
        how = ("control-character sanitation + replacement of the malformed "
               "discrimination_order.precondition_every_probe value (the lane's output was truncated "
               "there); no other field was altered")
    except Exception as e2:
        print("repair 2 failed:", str(e2)[:160])
        d = None
        how = None

if d:
    out = {"schema": "R5R3/FAR-PLAN-DECISION/1",
           "source_raw": "raw/plan_far_glm.log",
           "repair_disclosure": how,
           "decision": d}
    p = R + r"\FAR_R5R3_ZIPSPEC\PLAN_DECISION.json"
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("wrote", p)
    print("repair:", how)
    print("probes:", [x["probe_id"] for x in d.get("discrimination_order", {}).get("probes", [])])
    print("top keys:", list(d.keys()))
else:
    print("EXTRACTION FAILED — record the raw log only")
