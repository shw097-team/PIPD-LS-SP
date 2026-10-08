"""Deterministic PI -> PD -> ConstructionContract -> ECP/TQAEP pipeline.

Every artifact conforms EXACTLY to its S0 canonical schema (blueprint 7.3) and carries
ArtifactIdentity so the same input lock reproduces the same ids (G-S4-REPLAY).
No LLM is consulted on this path (5.9.1 responsibility split).
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .errors import (AuthorityUnknown, EffectUnknown, IntakeInvalid, PiSemanticFail,
                     RepoContextMissing, TqOracleFail, TqSodFail, TqTraceFail)
from .profiles import compute_profile
from .util import canonical_json, content_id, sha256_text

CLAIM_LADDER = ["PROMPT_COMPILE_PASS", "HGK_ADMITTED", "RUNTIME_READY", "LOCAL_QUALIFIED",
                "INDEPENDENT_PASS", "PUBLICATION_APPROVED", "RELEASED", "PRODUCTION_VERIFIED"]


def _rec(kind: str, prefix: str, payload: Any, **fields: Any) -> dict[str, Any]:
    """Build a schema-conformant record: identity fields first, then declared fields."""
    rec = {"subject_id": content_id(prefix, payload),
           "version": "1",
           "content_hash": sha256_text(canonical_json(payload)),
           "schema_version": f"{kind}@1"}
    rec.update(fields)
    return rec


# ---------------------------------------------------------------- authority
def freeze_authority(manifest: dict[str, Any]) -> dict[str, Any]:
    families = manifest.get("families") if "families" in manifest else manifest
    if not families:
        raise AuthorityUnknown("no source families in manifest")
    bindings = []
    for fam, spec in sorted(families.items()):
        if not isinstance(spec, dict) or "manifest_sha256" not in spec:
            raise AuthorityUnknown(f"family {fam} lacks a manifest digest")
        if not spec.get("files"):
            raise AuthorityUnknown(f"family {fam} is empty")
        rank = "R1" if fam.startswith(("F1", "F2", "F3", "F5", "F6")) else "R2"
        bindings.append(_rec("AuthorityBinding", "AUTH",
                             {"fam": fam, "digest": spec["manifest_sha256"]},
                             source_id=fam, authority_rank=rank,
                             locator=spec["files"][0]["rel"], supersession="CURRENT",
                             conflict_state="NONE"))
    payload = {"families": sorted(families), "digests": [b["content_hash"] for b in bindings]}
    freeze = _rec("SourceFreezeManifest", "SFM", payload,
                  families=len(bindings), bindings=bindings)
    return {"freeze": freeze, "bindings": bindings}


# ---------------------------------------------------------------- intake
ATOM_RULES = [
    ("REQ-INTENT", "intent", r"(?i)(implement|build|實作|建置|開發|施工)"),
    ("REQ-KNOWLEDGE", "knowledge", r"(?i)(knowledge|source|知識|來源|規格|spec)"),
    ("REQ-VERIFY", "verification", r"(?i)(test|verify|accept|測試|驗收|驗證)"),
    ("REQ-DELIVER", "release", r"(?i)(deliver|publish|release|交付|發佈|發布|公開)"),
    ("REQ-GOVERN", "trust_boundary", r"(?i)(govern|admission|workorder|治理|准入|裁決)"),
]


def intake(goal: str, *, sources: list[str] | None = None,
           constraints: list[str] | None = None, non_goals: list[str] | None = None) -> dict[str, Any]:
    if not goal or not goal.strip():
        raise IntakeInvalid("empty goal")
    sources = list(sources or [])
    if not sources:
        raise AuthorityUnknown("intake requires at least one source locator")
    for s in sources:
        if not Path(s).exists():
            raise AuthorityUnknown(f"source locator does not exist: {s}")
    payload = {"goal": goal.strip(), "sources": sources,
               "constraints": list(constraints or []), "non_goals": list(non_goals or [])}
    card = dict(payload)
    card["subject_id"] = content_id("INTENT", payload)
    card["content_hash"] = sha256_text(canonical_json(payload))
    card["schema_version"] = "IntentCard@1"
    atoms = [{"req_id": rid, "axis": ax} for rid, ax, pat in ATOM_RULES if re.search(pat, goal)]
    if not atoms:
        raise IntakeInvalid("goal produced zero requirement atoms")
    card["atoms"] = atoms
    return card


# ---------------------------------------------------------------- profile binding
def profile_record(profile_name: str, axes: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return (ProfileBinding record, full profile computation); the record is schema-exact."""
    full = compute_profile(profile_name, axes=axes)
    rec = _rec("ProfileBinding", "PB", {"p": full["profile"], "a": sorted(axes)},
               profile=full["profile"], axes=sorted(set(axes)),
               vetoes=full["vetoes"], artifact_depth=full["artifact_depth"],
               assurance=full["assurance"])
    return rec, full


# ---------------------------------------------------------------- PI
def compile_pi(card: dict[str, Any], profile_name: str = "LITE") -> dict[str, Any]:
    pb, profile_meta = profile_record(profile_name, [a["axis"] for a in card["atoms"]])
    atoms = []
    for a in card["atoms"]:
        atoms.append(_rec("RequirementAtom", "ATOM",
                          {"req": a["req_id"], "goal": card["content_hash"]},
                          req_id=a["req_id"], source_clause=card["sources"][0],
                          owner="PIPD-EC",
                          acceptance_cue=f"{a['req_id']} has an oracle and a negative fixture",
                          risk_guard=f"{a['req_id']} cannot self-accept"))
    if not atoms:
        raise PiSemanticFail("PI compiled zero atoms")
    payload = {"intent": card["subject_id"], "atoms": [a["req_id"] for a in atoms],
               "profile": pb["profile"]}
    pi = _rec("PI-PKG", "PI", payload)
    pi["stable_semantic_contract"] = {"contract": "stable", "profile_binding": pb,
                                      "atoms": atoms, "goal": card["goal"]}
    pi["acceptance"] = {"mode": "bound", "oracle_source": "DOC-03 DOMAIN_ORACLES"}
    pi["trace"] = [_rec("TraceLink", "TL", {"f": pi["subject_id"], "t": a["subject_id"]},
                        from_type="PI-PKG", from_id=pi["subject_id"], from_hash=pi["content_hash"],
                        to_type="RequirementAtom", to_id=a["subject_id"],
                        to_hash=a["content_hash"],
                        rationale="PI derives this atom from the frozen intent")
                   for a in atoms]
    pi["_profile_meta"] = profile_meta  # non-record sidecar, stripped before validation
    return pi


def atoms_of(pi: dict[str, Any]) -> list[dict[str, Any]]:
    return pi["stable_semantic_contract"]["atoms"]


def strip_sidecar(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if not k.startswith("_")}


# ---------------------------------------------------------------- PD
def bind_pd(pi: dict[str, Any], repo_context: dict[str, Any] | None) -> dict[str, Any]:
    if not repo_context:
        raise RepoContextMissing("PD late-binding requires a RepoContext")
    root = Path(repo_context["root"])
    if not root.exists():
        raise RepoContextMissing(f"RepoContext root missing: {root}")
    ctx = {"root": str(root), "head": repo_context.get("head", ""),
           "tracked_files": int(repo_context.get("tracked_files", 0))}
    payload = {"pi": pi["subject_id"], "repo": ctx}
    pd = _rec("PD-PKG", "PD", payload)
    pd["RepoContext"] = ctx
    pd["currentness"] = repo_context.get("currentness", "FRESH")
    pd["late_bound_construction_binding"] = {
        "bound_at": "PD", "binding_scope": "affected_only",
        "writable_scope": repo_context.get("writable_scope", "src/**")}
    return pd


# ---------------------------------------------------------------- ECP / TQAEP
def compile_construction_contract(pd: dict[str, Any]) -> dict[str, Any]:
    scope = pd["late_bound_construction_binding"]["writable_scope"]
    if not scope:
        raise EffectUnknown("ConstructionContract requires an explicit writable scope")
    payload = {"pd": pd["subject_id"], "scope": scope}
    return _rec("ConstructionContract", "CC", payload,
                subject=pd["subject_id"], writable_scope=[scope],
                expected_changes=["bounded edits inside writable scope"],
                tests=["tests/test_s1_lite_slice.py"],
                rollback="git revert to baseline commit",
                evidence_expectations=["EVD-POS", "EVD-NEG"])


def compile_ecp(pd: dict[str, Any], pi: dict[str, Any]) -> dict[str, Any]:
    scope = pd["late_bound_construction_binding"]["writable_scope"]
    if not scope:
        raise EffectUnknown("ECP requires an explicit writable scope")
    payload = {"pd": pd["subject_id"], "scope": scope, "pi": pi["subject_id"]}
    return _rec("ECP", "ECP", payload,
                effect_intent="apply bounded edits inside the writable scope",
                permission={"scope": scope, "token_required": True},
                retries={"max": 1, "backoff": "none"},
                idempotency={"key": content_id("IDEM", payload), "guarantee": "at_most_once"},
                readback={"required": True, "kind": "residue_scan"},
                rollback={"pointer": "baseline_commit", "required": True})


def compile_tqaep(pi: dict[str, Any], ecp: dict[str, Any], *, maker: str,
                  checker: str) -> dict[str, Any]:
    if maker == checker:
        raise TqSodFail("maker must not be the independent checker")
    if not pi.get("trace"):
        raise TqTraceFail("TQAEP requires trace links")
    tests, oracles, fixtures = [], [], []
    for atom in atoms_of(pi):
        tests.append({"test_id": f"TEST-{atom['req_id']}", "requirement": atom["req_id"],
                      "oracle": "deterministic assertion on the bound artifact",
                      "positive_fixture": f"fixtures/{atom['req_id']}/positive",
                      "negative_fixture": f"fixtures/{atom['req_id']}/negative",
                      "evidence_expectation": "EVD-" + atom["req_id"]})
        oracles.append(f"TEST-{atom['req_id']}: deterministic assertion on the bound artifact")
        fixtures.append(f"fixtures/{atom['req_id']}/positive")
    if any(not t["oracle"] for t in tests):
        raise TqOracleFail("every TQAEP test needs an oracle")
    payload = {"pi": pi["subject_id"], "ecp": ecp["subject_id"],
               "tests": [t["test_id"] for t in tests]}
    return _rec("TQAEP", "TQAEP", payload,
                tests=tests, oracles=oracles, fixtures=fixtures,
                acceptance=["INDEPENDENT_CASE_PASS"], requalification="affected-only")


# ---------------------------------------------------------------- evidence / claim
def evidence_expectations(tqaep: dict[str, Any], producer: str) -> list[dict[str, Any]]:
    out = []
    for t in tqaep["tests"]:
        out.append(_rec("EvidenceExpectation", "EE", t,
                        expected_evidence_type="RAW_RECEIPT", producer=producer,
                        postcondition=f"{t['test_id']} returned its oracle verdict",
                        freshness="same_candidate_hash", claim_effect="LOCAL"))
    return out


def claim_ceiling(allowed: list[str]) -> dict[str, Any]:
    for c in allowed:
        if c not in CLAIM_LADDER:
            raise PiSemanticFail(f"unknown claim {c}")
    idx = max(CLAIM_LADDER.index(c) for c in allowed)
    payload = {"allowed": sorted(allowed), "idx": idx}
    return _rec("ClaimCeiling", "CCL", payload,
                allowed_claims=sorted(allowed),
                forbidden_escalation=CLAIM_LADDER[idx + 1:],
                close_conditions=["raw receipt bound to candidate hash",
                                  "independent checker verdict"])


# ---------------------------------------------------------------- trace closure
def trace_closure(artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    edges = []
    known: set[str] = set()
    for name, arte in artifacts.items():
        if "subject_id" in arte:
            known.add(arte["subject_id"])
        for atom in (arte.get("stable_semantic_contract", {}) or {}).get("atoms", []) or []:
            known.add(atom["subject_id"])
        for tl in arte.get("trace", []) or []:
            edges.append((name, tl["to_id"]))
    orphans = sorted(t for _, t in edges if t not in known)
    payload = {"artifacts": sorted(artifacts), "edges": len(edges)}
    return _rec("TraceClosureReport", "TRC", payload,
                edges=len(edges), orphans=orphans,
                verdict="PASS" if not orphans and edges else "FAIL")
