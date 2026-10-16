"""Read-only control-plane probe for round R5R3-20261016.

Drives the LIVE gates from the registry/policy modules (never from a snapshot on disk):
  lane_policy.load_registry / route_for_lane / check_sod / check_drift(registry=...)
  named_methods.registry_snapshot / route / evaluate_activation_invariants
and localises the TT-03 DRIFT_VALUE claim by printing every drift row it finds.

Writes nothing. Prints one JSON object.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "src")

out: dict = {"schema": "R5R3/CONTROL-PLANE-PROBE/1"}

from hg_kseos import lane_policy  # noqa: E402

reg = lane_policy.load_registry()
out["registry"] = {
    "epoch": reg.get("epoch"),
    "status": reg.get("status"),
    "source_of_routes": reg.get("source_of_routes"),
}

routes = {}
for lane in ("PLAN", "EXECUTE", "VERIFY_SECURITY"):
    try:
        r = lane_policy.route_for_lane(reg, lane)
        routes[lane] = {"model": r.get("model"), "provider": r.get("provider"),
                        "effort": r.get("reasoning_effort"),
                        "fallbacks": r.get("fallbacks"),
                        "arms": [{"rank": a.get("rank", a.get("arm")), "model": a.get("model"),
                                  "provider": a.get("provider"), "default": a.get("default")}
                                 for a in (r.get("arms") or [])]}
    except Exception as e:  # noqa: BLE001
        routes[lane] = {"ERROR": f"{type(e).__name__}: {e}"}
out["routes"] = routes

try:
    mk = out["routes"]["EXECUTE"].get("model")
    ck = out["routes"]["VERIFY_SECURITY"].get("model")
    pk = out["routes"]["PLAN"].get("model")
    out["sod"] = {
        "maker_exe_vs_checker": lane_policy.check_sod(mk, ck),
        "planner_vs_checker": lane_policy.check_sod(pk, ck),
        "planner_vs_maker": lane_policy.check_sod(pk, mk),
        "observed_models": {"EXECUTE": mk, "VERIFY_SECURITY": ck, "PLAN": pk},
    }
except Exception as e:  # noqa: BLE001
    out["sod"] = {"ERROR": f"{type(e).__name__}: {e}"}

try:
    drift = lane_policy.check_drift(registry=reg)
    out["drift"] = {"row_count": len(drift), "rows": drift[:20]}
except Exception as e:  # noqa: BLE001
    out["drift"] = {"ERROR": f"{type(e).__name__}: {e}"}

try:
    from hg_kseos import named_methods
    snap = named_methods.registry_snapshot()
    out["named_methods"] = {
        "snapshot_rows": len(snap) if hasattr(snap, "__len__") else None,
        "activation_invariants": named_methods.evaluate_activation_invariants(),
    }
except Exception as e:  # noqa: BLE001
    out["named_methods"] = {"ERROR": f"{type(e).__name__}: {e}"}

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
