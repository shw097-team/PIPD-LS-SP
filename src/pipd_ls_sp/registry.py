"""Canonical machine-contract registry (exact 19/19, 總藍圖 §7.3)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import ValidationFail

EXPECTED_FAMILIES = 19

# Fallback exact-set in source order; schemas/registry.json is authoritative when present.
SOURCE_ORDER = [
    "ArtifactIdentity", "AuthorityBinding", "RequirementAtom", "ProfileBinding",
    "TechnologyAdmission", "PI-PKG", "PD-PKG", "TraceLink", "TaskSpecSeed",
    "ConstructionContract", "WorkOrderCandidate", "ECP", "TQAEP",
    "ExecutionHandoff", "EvidenceExpectation", "ClaimCeiling",
    "SurfaceProjectionManifest", "GENIEProjectionRef", "ExecutionBindingRef",
]
SEAM_ONLY = {"GENIEProjectionRef": "SCHEMA_SEAM_ONLY_UNTIL_S6",
             "ExecutionBindingRef": "SCHEMA_SEAM_ONLY_UNTIL_S5"}


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_registry(schemas_dir: Path | None = None) -> dict[str, Any]:
    d = schemas_dir or (_root() / "schemas")
    reg_path = d / "registry.json"
    if not reg_path.is_file():
        raise ValidationFail(f"registry missing: {reg_path}")
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    fams = data.get("families") or []
    if len(fams) != EXPECTED_FAMILIES:
        raise ValidationFail(f"registry family count {len(fams)} != {EXPECTED_FAMILIES}")
    names = [f["contract"] for f in fams]
    if names != SOURCE_ORDER:
        raise ValidationFail("registry family order/name diverges from §7.3 exact set")
    for f in fams:
        if not (d / f"{f['contract']}.schema.json").is_file():
            raise ValidationFail(f"schema file missing for {f['contract']}")
        if not f.get("required_fields"):
            raise ValidationFail(f"{f['contract']} has no required_fields")
    return data


def load_schema(contract: str, schemas_dir: Path | None = None) -> dict[str, Any]:
    d = schemas_dir or (_root() / "schemas")
    return json.loads((d / f"{contract}.schema.json").read_text(encoding="utf-8"))
