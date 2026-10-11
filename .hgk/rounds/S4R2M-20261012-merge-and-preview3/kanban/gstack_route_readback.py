#!/usr/bin/env python3
"""S4R2M named-method route readback (GSTACK / OpenSpec).

Read-only: it imports the control plane's own registry and router and records the decision for the
flows this round actually uses. Nothing here grants authority — every route is an advisory adapter with
`final_authority: False` where the registry says so, and a NATIVE fallback otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
OUT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/.hgk/rounds/"
           "S4R2M-20261012-merge-and-preview3/kanban/S4R2M_GSTACK_OPENSPEC_ROUTE.json")
sys.path.insert(0, str(HGK / "src"))
import hg_kseos.named_methods as nm  # noqa: E402

FLOWS = [
    "brownfield change proposal for the S4-R2M conditional merge",   # -> openspec
    "plan the narrow repair work orders",                            # -> gstack.plan-eng-review
    "review the bounded writer's documentation diff",                # -> gstack.review
    "qa the isolated affected regression",                           # -> gstack.qa
    "security adversarial check of the admitted write-set",          # -> gstack.cso
    "release checklist for the preview.3 gate",                      # -> gstack.ship
    "ambiguity triage of the two documentation blockers",            # -> gstack.office-hours
    "greenfield second control plane",                               # -> XOR greenfield (refused)
    "invent a new scheduling authority for this round",              # -> NATIVE (no mapping)
]

payload = {
    "schema": "PIPD-S4R2M-NAMED-METHOD-ROUTE-CHECK/1",
    "round": "S4R2M-20261012-merge-and-preview3",
    "surface": "HGK_NAMED_METHOD_ROUTER (src/hg_kseos/named_methods.py)",
    "registry_snapshot": nm.registry_snapshot(),
    "activation_invariant_evaluation": nm.evaluate_activation_invariants(),
    "routes": [nm.route(flow) for flow in FLOWS],
    "claim_ceiling": "CANDIDATE_ONLY",
    "what_this_does_not_confer": [
        "a named method is an advisory adapter, never a second control plane, scheduler or spec owner",
        "a gstack or openspec route never promotes this round's artefacts to release or production",
        "HG-KSEOS keeps authority, evidence, checker and release ownership (HGK_GSTACK_ROLE_MAP.yaml hard_deny names gstack Conductor, gstack /spec, gstack /ship and /land-and-deploy as denied)",
        "an unmapped flow routes NATIVE rather than being guessed; the router's own decision object is recorded verbatim, and the few non-zero invariant counters would have failed the round closed",
    ],
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", OUT)
for r in payload["routes"]:
    print(" ", r["flow"][:44].ljust(46), "->", r["provider"] or "NATIVE",
          "| state:", r["state"], "| final_authority:", r["final_authority"])
print("invariants:", json.dumps(payload["activation_invariant_evaluation"], ensure_ascii=False))
