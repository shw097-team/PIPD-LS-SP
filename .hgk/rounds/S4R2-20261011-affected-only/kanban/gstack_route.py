#!/usr/bin/env python3
"""S4-R2 GSTACK: resolve the named method route for each admitted obligation and record what the
route does and does not confer (a CERTIFIED method is not an authority to publish).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
OUT = Path("C:/Projects/Agent_Workspace/PIPD-postrelease-wt/.hgk/rounds/"
           "S4R2-20261011-affected-only/kanban")
sys.path.insert(0, str(HGK / "src"))

FLOWS = {
    "REQ-S4R2-DOC-001": ("doc_first_use_repair", "S4-DOC-FIRSTUSE-01"),
    "REQ-S4R2-WEB-002": ("web_mount_pack", "S4-WEB-MOUNT-02"),
    "REQ-S4R2-CONTRACT-003": ("contract_hardening", "S4-CONTRACT-HARDEN-03"),
    "REQ-S4R2-SOURCE-004": ("source_bootstrap", "S4-SOURCE-BOOTSTRAP-04"),
}


def main() -> int:
    out = {"schema": "PIPD-S4R2-GSTACK-ROUTE/1", "role_map": None, "routes": {}}
    rm = HGK / "HGK/HGK_GSTACK_ROLE_MAP.yaml"
    out["role_map"] = str(rm.relative_to(HGK)) if rm.exists() else "ABSENT"

    try:
        import yaml  # noqa: F401
        doc = yaml.safe_load(rm.read_text(encoding="utf-8")) if rm.exists() else {}
        out["role_map_top_keys"] = list(doc)[:20] if isinstance(doc, dict) else str(type(doc))
    except Exception as exc:  # noqa: BLE001
        out["role_map_top_keys"] = "ERR(%s)" % exc

    try:
        from hg_kseos import named_methods as nm
        out["named_methods_public"] = [n for n in dir(nm) if not n.startswith("_")][:40]
        resolver = getattr(nm, "route", None) or getattr(nm, "resolve", None)
        out["resolver"] = getattr(resolver, "__name__", None)
        for req, (flow, wo) in FLOWS.items():
            entry = {"flow": flow, "workorder": wo}
            try:
                if resolver is not None:
                    entry["route"] = resolver(flow)
                else:
                    entry["route"] = "NO_RESOLVER_EXPORTED"
            except Exception as exc:  # noqa: BLE001
                entry["route"] = "ERR(%s: %s)" % (type(exc).__name__, exc)
            out["routes"][req] = entry
    except Exception as exc:  # noqa: BLE001
        out["named_methods_error"] = "%s: %s" % (type(exc).__name__, exc)

    out["authority_note"] = (
        "A named-method CERTIFIED verdict is a method-qualification signal only. It carries "
        "final_authority=false: it does not authorise a release, a tag, or a remote push. The "
        "publication step stays STANDBY and requires an owner grant plus a working credential."
    )
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "S4R2_GSTACK_ROUTE.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:2600])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
