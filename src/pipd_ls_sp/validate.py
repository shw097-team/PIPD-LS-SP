"""Deterministic validation: schema + semantic invariants over the 19 families.

Deterministic only: no LLM judge is consulted here (總藍圖 §5.9.1 responsibility split).
"""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from . import registry
from .errors import ValidationFail


def _validator(schema: dict[str, Any]):
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover
        raise ValidationFail(f"jsonschema unavailable: {exc}") from exc
    return Draft202012Validator(schema)


def validate_record(contract: str, record: dict[str, Any], schemas_dir: Path | None = None) -> list[str]:
    """Return a list of deterministic findings; empty list == schema-valid."""
    schema = registry.load_schema(contract, schemas_dir)
    v = _validator(schema)
    findings = []
    for err in sorted(v.iter_errors(record), key=lambda e: list(e.absolute_path)):
        pointer = "/" + "/".join(str(x) for x in err.absolute_path)
        findings.append(f"{contract}{pointer}: {err.message}")
    return findings


def semantic_invariants(contract: str, record: dict[str, Any]) -> list[str]:
    """Semantic invariants that a JSON Schema cannot express."""
    out: list[str] = []
    ident = ("subject_id", "version", "content_hash", "schema_version")
    for field in ident:
        if field not in record:
            out.append(f"{contract}: missing universal identity field {field}")
    sv = str(record.get("schema_version") or "")
    if sv and not (re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", sv) or re.match(r"^[A-Za-z0-9_.-]+@[0-9]+$", sv)):
        out.append(f"{contract}: schema_version must be semver or <Token>@<n>")
    if contract == "ClaimCeiling":
        allowed = set(record.get("allowed_claims", []))
        forbidden = set(record.get("forbidden_escalation", []))
        if allowed & forbidden:
            out.append("ClaimCeiling: a claim cannot be both allowed and forbidden")
    if contract == "WorkOrderCandidate":
        if record.get("candidate_only") is not True:
            out.append("WorkOrderCandidate: candidate_only must be fixed true (never runtime authority)")
    if contract == "GENIEProjectionRef":
        refs = record.get("target_refs")
        want = ("ProductGraph", "Profile", "Bundle", "GENIEArtifact")
        if not isinstance(refs, (list, dict)) or not all(
                any(w in str(x) for x in (refs if isinstance(refs, list) else refs.keys())) for w in want):
            out.append("GENIEProjectionRef: target_refs must cover ProductGraph/Profile/Bundle/GENIEArtifact")
    if contract == "ExecutionBindingRef" and str(record.get("state", "")).upper() == "ACKED":
        if not (record.get("receiver_binding_id") and record.get("receiver_binding_hash")):
            out.append("ExecutionBindingRef: ACK requires a real HGK receiver binding id+hash")
    if contract == "TraceLink":
        for side in ("from", "to"):
            if not (record.get(f"{side}_type") and record.get(f"{side}_id")):
                out.append(f"TraceLink: {side} endpoint incomplete")
    return out


def validate_bundle(bundle: dict[str, dict[str, Any]], schemas_dir: Path | None = None) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    for contract, record in bundle.items():
        for f in validate_record(contract, record, schemas_dir):
            findings.append({"contract": contract, "kind": "SCHEMA", "detail": f})
        for f in semantic_invariants(contract, record):
            findings.append({"contract": contract, "kind": "SEMANTIC", "detail": f})
    return {"verdict": "PASS" if not findings else "FAIL",
            "checked": len(bundle), "findings": findings}
