"""Generic route runner — one installed executor for every registry route, with typed refusals.

Why this exists: the registry needs every declared route to reach at least `INSTALLED`, but writing
24 bespoke runners would be over-engineering. This dispatcher reports which runner the SIGNED registry
pins for a route; anything without a real effect handler is refused with a typed code instead of
pretending to work. Its own scope is READ_ONLY_PROBE: it never writes on behalf of an unimplemented
effect and never executes an effect itself.

D-8 fix: the previous version matched route names by SUBSTRING, so `native_issuer` resolved to
`issuer_subject_runner.py` and `native_receiver` to `bridge_handoff_runner.py` — the dispatcher
reported `ok:true` for a handler the registry does not pin for that route, which would let one route
borrow another route's evidence (PKG_08 L45: 互不借 PASS). The binding is now an EXACT lookup against
the signed registry, and a route whose pinned executable is this very dispatcher is reported as a
typed refusal rather than a success.

Usage:  python generic_route_runner.py --route OWNER_REGISTERED::native_receiver --root <workroot>
Exit:   0 binding to a real runner reported | 3 typed refusal | 2 bad invocation
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REGISTRY = HERE.parent / "registry" / "runner-registry.json"
SELF = pathlib.Path(__file__).name


def bindings() -> dict[str, str]:
    """route_id -> pinned runner file name, read from the signed registry.

    Read at call time so the dispatcher can never drift from the registry it is part of: if a row is
    re-pointed and re-signed, the dispatcher follows it without a code change.
    """
    try:
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out: dict[str, str] = {}
    for row in reg.get("rows") or []:
        rid = str(row.get("route_id") or "")
        exe = str(row.get("executable_path") or "").replace("\\", "/")
        if rid and exe:
            out[rid] = exe.rsplit("/", 1)[-1]
    return out


def resolve(route: str) -> tuple[str | None, str, str]:
    """Return (route_id, handler, reason). No handler or a self-pinned row yields reason != \"\".

    reason: "" = a real runner is pinned | ROUTE_NOT_REGISTERED | EFFECT_NOT_IMPLEMENTED
    """
    table = bindings()
    if not table:
        return None, "", "REGISTRY_UNREADABLE"
    if route not in table:
        return None, "", "ROUTE_NOT_REGISTERED"
    handler = table[route]
    if handler == SELF:
        return route, handler, "EFFECT_NOT_IMPLEMENTED"
    return route, handler, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--route", required=True)
    ap.add_argument("--root", default="")
    a = ap.parse_args()
    rid, runner, reason = resolve(a.route)
    if reason:
        print(json.dumps({"ok": False, "route": a.route, "error": f"REFUSED_{reason}",
                          "reason": reason,
                          "detail": "no distinct effect handler is pinned for this route in the signed "
                                    "registry; a typed refusal is reported instead of borrowing another "
                                    "route's handler or evidence",
                          "pinned_handler": runner or None,
                          "coverage": "NOT_IMPLEMENTED", "root": a.root or None}, ensure_ascii=False))
        return 3
    print(json.dumps({"ok": True, "route": rid, "handler": runner, "delegated": False,
                      "detail": "exact match against the signed registry; execution stays with the "
                                "handler's own admission path (this dispatcher never executes effects)",
                      "root": a.root or None}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
