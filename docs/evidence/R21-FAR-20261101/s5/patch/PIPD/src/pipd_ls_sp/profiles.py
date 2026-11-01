"""Profile trio: LITE / STANDARD / ASSURED over one canonical truth (總藍圖 §7.3 #04)."""
from __future__ import annotations

from .errors import ProfileVeto, UnsupportedSurface

# axes -> artifact depth floor, required assurance
PROFILES = {
    "LITE": {"artifact_depth": "L1_SCHEMA_CONTRACT", "assurance": ["deterministic_validator"],
             "target_resolution": "package", "max_axes": 3},
    "STANDARD": {"artifact_depth": "L3_INTEGRATION_RUNTIME",
                 "assurance": ["deterministic_validator", "negative_security"],
                 "target_resolution": "integration", "max_axes": 6},
    "ASSURED": {"artifact_depth": "L4_FAILURE_RECOVERY",
                "assurance": ["deterministic_validator", "negative_security", "adversarial",
                              "independent_checker"],
                "target_resolution": "runtime", "max_axes": 10},
}
AXES = ("intent", "knowledge", "verification", "release", "trust_boundary",
        "preexisting_repo", "profile", "tech_candidates", "host_surface")


def compute_profile(requested: str, *, axes: list[str] | None = None,
                    provider_off_required: bool = False) -> dict:
    name = (requested or "").upper()
    if name not in PROFILES:
        raise ProfileVeto(f"unknown profile {requested!r}")
    cfg = PROFILES[name]
    used = list(axes or ["intent"])
    unknown = [a for a in used if a not in AXES]
    if unknown:
        raise UnsupportedSurface(f"unknown axes {unknown}")
    override = None
    # safety veto may ESCALATE depth, never reduce it
    if provider_off_required and name == "LITE":
        override = "STANDARD"
    if len(used) > cfg["max_axes"]:
        override = "ASSURED" if name != "ASSURED" else override
    effective = override or name
    return {"profile": effective,
            "requested_profile": name,
            "escalated": bool(override),
            "escalation_reason": "provider_off_parity" if override == "STANDARD" else
                                 ("axis_complexity" if override == "ASSURED" else None),
            "axes": used,
            "vetoes": [],
            "artifact_depth": PROFILES[effective]["artifact_depth"],
            "assurance": PROFILES[effective]["assurance"],
            "canonical_truth": "single",  # all three profiles read one canonical truth
            }
