"""Independent ClaimCeiling probe (validate.py library half + schema half).

Usage: python probe_claim.py <src_root> <schemas_dir> <out.json>
"""
import json
import sys
from pathlib import Path

SRC_ROOT = Path(sys.argv[1])
SCHEMAS = Path(sys.argv[2])
OUT = Path(sys.argv[3])
sys.path.insert(0, str(SRC_ROOT))

from pipd_ls_sp import validate  # noqa: E402

HASH = "a" * 64


def rec(**over):
    base = {
        "allowed_claims": ["LOCAL_QUALIFIED"],
        "forbidden_escalation": ["RELEASED"],
        "close_conditions": [],
        "subject_id": "PIPD-LS-SP",
        "version": "1.0.0",
        "content_hash": HASH,
        "schema_version": "1.1.0",
    }
    base.update(over)
    return base


SHAPES = {
    "legal": rec(),
    "legal_two_allowed": rec(allowed_claims=["HGK_ADMITTED", "LOCAL_QUALIFIED"]),
    "allowed_null": rec(allowed_claims=None),
    "forbidden_null": rec(forbidden_escalation=None),
    "allowed_mapping_item": rec(allowed_claims=[{"claim": "RELEASED"}]),
    "forbidden_mapping_item": rec(forbidden_escalation=[{"claim": "RELEASED"}]),
    "allowed_undeclared": rec(allowed_claims=["NOT_A_DECLARED_CLAIM"]),
    "allowed_string": rec(allowed_claims="RELEASED"),
    "allowed_mapping_value": rec(allowed_claims={"claim": "RELEASED"}),
    "allowed_int_item": rec(allowed_claims=[7]),
    "overlap": rec(allowed_claims=["LOCAL_QUALIFIED"], forbidden_escalation=["LOCAL_QUALIFIED"]),
    "escalation_no_receipt": rec(allowed_claims=["RELEASED"], forbidden_escalation=[]),
}

out = {}
for name, r in SHAPES.items():
    entry = {}
    try:
        entry["semantic"] = validate.semantic_invariants("ClaimCeiling", r)
    except Exception as exc:  # noqa: BLE001
        entry["semantic_exc"] = f"{type(exc).__name__}: {exc}"
    try:
        entry["schema"] = validate.validate_record("ClaimCeiling", r, SCHEMAS)
    except Exception as exc:  # noqa: BLE001
        entry["schema_exc"] = f"{type(exc).__name__}: {exc}"
    out[name] = entry

OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {OUT} ({len(out)} shapes)")
