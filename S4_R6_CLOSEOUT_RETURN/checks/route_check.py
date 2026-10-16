#!/usr/bin/env python3
"""GSTACK / OpenSpec named-method route check for round PIPD-S4-R6-CLOSEOUT-20261016.

Records registry_snapshot() ACTIVE_SELECTED state and route(flow) for the round's flows,
including the negative control (a flow that must NOT be claimed as a named-method route).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
sys.path.insert(0, ROOT + "/src")
from hg_kseos import named_methods as nm  # noqa: E402

OUT = Path("C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/route_check.json")

FLOWS = [
    "r6 closeout brownfield docs migration",
    "r6 security review of the published release identity",
    "r6 plan review of the closeout change set",
    "r6 milestone acceptance of the preview mvp",
    "r6 evidence closure and handover record",
    "r6 unrelated quarterly tax filing",  # negative control: must route NATIVE with no provider
]

rep = {"schema": "HGK-GSTACK-OPENSPEC-ROUTE-CHECK/1", "round": "PIPD-S4-R6-CLOSEOUT-20261016",
       "registry_source_basis": "hg_kseos.named_methods route()/registry_snapshot()"}
snap = nm.registry_snapshot()
rep["registry_snapshot_keys"] = sorted(snap.keys())
rep["active_selected"] = sorted(getattr(nm, "ACTIVE_SELECTED", set()))
rep["named_methods_state"] = {
    k: {"state": getattr(v, "state", None), "provider": getattr(v, "provider", None)}
    for k, v in sorted(nm.NAMED_METHODS.items())
}
rep["routes"] = []
for f in FLOWS:
    d = nm.route(f)
    rep["routes"].append(d)

neg = [r for r in rep["routes"] if "tax filing" in r["flow"]][0]
rep["negative_control"] = {
    "flow": neg["flow"], "route": neg["route"], "provider": neg["provider"],
    "ok": neg["route"] == "NATIVE" and neg["provider"] is None,
}
rep["verdict"] = "ROUTE_CHECK_RECORDED"

OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"active_selected": rep["active_selected"],
                  "routes": [{k: r[k] for k in ("flow", "route", "provider", "state")} for r in rep["routes"]],
                  "negative_control": rep["negative_control"]}, ensure_ascii=False, indent=1))
