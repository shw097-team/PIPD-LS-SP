#!/usr/bin/env python3
"""GSTACK surface for round S4POST-20261012-postrepair-recheck-and-triple-upgrade.

The HG-KSEOS GSTACK surface is the *named-method* route resolution in
``src/hg_kseos/named_methods.py`` (registry ``ACTIVE_SELECTED`` + ``route(flow)``), together with its
activation invariants: a canonical flow that names a method which is neither runtime-certified nor
substituted raises a non-zero invariant count. This script runs that deterministic lookup for the
flows this round actually exercises and writes the receipt. It guesses nothing and mutates nothing.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path("C:/Projects/Agent_Workspace/HG-KSEOS")
sys.path.insert(0, str(ROOT / "src"))
from hg_kseos import named_methods as nm  # noqa: E402

ROUND = "S4POST-20261012-postrepair-recheck-and-triple-upgrade"
OUT = pathlib.Path(
    "C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt/.hgk/rounds"
    "/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/10_OWNER"
    "/GSTACK_ROUTE_RESOLUTION.json")

FLOWS = ["brownfield", "greenfield", "ambiguity", "plan", "review", "qa", "security", "release",
         "retro", "repair", "lane-repair", "verify"]


def main() -> int:
    snap = nm.registry_snapshot()
    inv = nm.evaluate_activation_invariants()
    env = nm.invariant_envelope_fields()
    routes = {f: nm.route(f) for f in FLOWS}
    receipt = {
        "schema": "HGK-GSTACK-ROUTE-RESOLUTION/1",
        "round": ROUND,
        "surface": ("src/hg_kseos/named_methods.py route(flow) - deterministic registry lookup, "
                    "never LLM guessing"),
        "active_selected": sorted(nm.ACTIVE_SELECTED),
        "registry_snapshot": snap,
        "flow_routes": routes,
        "flows_this_round_actually_exercises": ["plan", "verify", "security", "review", "repair"],
        "activation_invariants": inv,
        "invariant_envelope_fields": env,
        "invariants_all_zero": all(v == 0 for v in inv.values()),
        "note": ("invariants_all_zero is the check; a non-zero count means a canonical flow names a "
                 "named method that is neither runtime-certified nor substituted"),
        "nonclaims": ["not an acceptance", "a route receipt, not a verdict on any subject",
                      "not a release or publication approval"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(OUT),
                      "invariants_all_zero": receipt["invariants_all_zero"],
                      "invariants": inv,
                      "flows": {k: str(v)[:100] for k, v in routes.items()}},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
