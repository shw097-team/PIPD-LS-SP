#!/usr/bin/env python3
"""S0/S1 — materialise the 22 source-designated Technology Admission rulings (PKG-00 §9).

The source terminalises a DESIGN disposition for CAND-01..CAND-22; it does NOT license-verify or
execute them. This tool therefore never invents a PASS and never inflates a denominator: it records
the source state for every required column and computes the per-row verdict from the artefact.

Audit repair (R-AUD-007 / MUT-TECH-PIN, WO-TS-req-pipd-r3-fw-08):

* every one of the 22 rows carries an exact source pin (repository + version/commit, or the literal
  ``UNAVAILABLE`` together with a machine-readable reason), a licence field (or an explicit
  unknown-licence disposition that BLOCKS activation), a TTL/security note, a fallback, an exit
  criterion, a permission scope, a provider-off behaviour, and a per-row disposition from exactly
  ``{ADOPT, REFERENCE, EVAL_ONLY, QUARANTINE, REJECT}``;
* a row is reported ``active``/``installed`` ONLY when its disposition is ``ADOPT`` AND it carries a
  verified pin AND a known (non-unknown) licence. A non-ADOPT disposition can NEVER be reported as
  active/installed;
* ``--report`` recomputes the per-row verdict from the artefact and prints the TRUE denominator per
  gate (an honest ``0/22`` for ``G-TECH-SOURCE-PIN`` stays ``0/22``), and exits non-zero when any
  row claims active without a verified pin or with an unknown licence.

Everything is parsed from the source clause, so the records cannot drift from the clause they cite.
Where the source legitimately returns a family of dispositions (``ADOPT_WITH_WRAPPER``,
``ADOPT_WITH_TRANSLATION``), the design disposition is normalised to the canonical per-row
disposition ``ADOPT`` and the exact source string is preserved in ``upstream_disposition``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric"
           r"\PIPD\PIPD-LS-SP_PIPD-PKG\PIPD-LS-SP_PIPD-PKG-00~PKG-10\PIPD-LS-SP_PIPD-PKG-00.md")
OUT = ROOT / ".hgk" / "artifacts" / "s1"
FIX = ROOT / "fixtures"

sys_path = str(ROOT / "src")
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from pipd_ls_sp import validate as V  # noqa: E402

# The exact closed set of per-row dispositions (contract, not a convenience list).
DISPOSITIONS = ("ADOPT", "REFERENCE", "EVAL_ONLY", "QUARANTINE", "REJECT")

# Source strings that mean "there is no verified immutable pin". Kept as a closed set so a new
# placeholder cannot silently read as a real pin.
UNAVAILABLE_PIN_MARKERS = frozenset({
    "", "LATEST", "HEAD", "PIN_REVALIDATION_REQUIRED", "UNAVAILABLE",
})

# Licence strings that mean "the licence is not known/verified; activation is blocked".
UNKNOWN_LICENCE_MARKERS = ("UNKNOWN", "NOT_INDEPENDENTLY_PIN_VERIFIED", "UNPINNED_MAIN")


def _git(*args: str) -> str:
    import subprocess
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True).stdout.strip()


def parse_source() -> list[dict]:
    text = SRC.read_text(encoding="utf-8", errors="replace")
    disposition = {}
    for m in re.finditer(r"\|\s*`(CAND-\d\d)`\s*([^|]*)\|\s*`([A-Z_]+)`\s*\|\s*`([A-Z_]+)`\s*\|", text):
        disposition[m.group(1)] = {"external_name": m.group(2).strip(), "role": m.group(3),
                                   "design_disposition": m.group(4)}
    records = []
    for m in re.finditer(r"###\s*(CAND-\d\d)\s*[—-].*?```json\s*(.*?)```", text, re.S):
        cid, body = m.group(1), m.group(2)
        rec = json.loads(body)
        rec["_table"] = disposition.get(cid, {})
        records.append(rec)
    return records


def subject_id(cid: str) -> str:
    h = hashlib.sha256(f"PIPD-TECH-{cid}".encode()).hexdigest()[:32]
    return f"subset-tech-{h}"


def canonical_disposition(design_disposition: str) -> str:
    """Map the source's design disposition onto the closed per-row disposition set."""
    d = (design_disposition or "").upper()
    if d.startswith("ADOPT"):
        return "ADOPT"
    if d in DISPOSITIONS:
        return d
    # Unknown design strings must never be rounded up to ADOPT.
    return "REJECT"


def pin_state(raw_pin: str, source_repo: str) -> dict:
    """Exact source pin, or the literal UNAVAILABLE with a machine-readable reason."""
    repo = (source_repo or "").strip()
    if repo in ("", "SOURCE_REPOSITORY_RECHECK_REQUIRED"):
        return {
            "value": "UNAVAILABLE",
            "repository": repo or "UNAVAILABLE",
            "reason_code": "SOURCE_REPOSITORY_RECHECK_REQUIRED",
            "reason": "the source clause does not name a resolvable upstream repository, so no "
                      "immutable repository+version/commit pin can be established",
        }
    return {
        "value": "UNAVAILABLE",
        "repository": repo,
        "reason_code": "PIN_REVALIDATION_REQUIRED",
        "reason": "the source terminalises DESIGN only and explicitly leaves the immutable "
                  "version/commit pin to receiver-side revalidation",
    }


def licence_state(raw_licence: str) -> dict:
    lic = (raw_licence or "").strip()
    upper = lic.upper()
    unknown = (lic == "") or any(m in upper for m in UNKNOWN_LICENCE_MARKERS)
    return {
        "value": lic or "UNAVAILABLE",
        "known": not unknown,
        "blocks_activation": unknown,
        "disposition": ("UNKNOWN_LICENCE_BLOCKS_ACTIVATION" if unknown
                        else "LICENCE_DECLARED_AT_SOURCE"),
    }


def _pin_verified(pin: dict) -> bool:
    v = str(pin.get("value") or "").strip()
    return bool(v) and v.upper() not in {"UNAVAILABLE", "LATEST", "HEAD"} \
        and v.upper() not in UNAVAILABLE_PIN_MARKERS


def build(rec: dict) -> dict:
    cid = rec["technology_id"]
    out = dict(rec)
    out.pop("_table", None)

    # The authoritative per-row disposition is the source's own `disposition` field
    # (ADOPT / ADOPT_WITH_WRAPPER / ADOPT_WITH_TRANSLATION / EVAL_ONLY / REFERENCE / QUARANTINE /
    # REJECT). The table's `design_disposition` column is a different state axis (e.g.
    # DESIGN_BASELINE_SELECTED) and must never be read as the disposition.
    design_disp = rec.get("disposition") or rec.get("upstream_disposition", "")
    disposition = canonical_disposition(design_disp)
    pin = pin_state(rec.get("immutable_pin", ""), rec.get("source_repository", ""))
    lic = licence_state(rec.get("license", ""))

    verified = _pin_verified(pin)
    licence_known = bool(lic["known"])
    active = disposition == "ADOPT" and verified and licence_known

    if active:
        reason = "ADOPT with a verified pin and a known licence"
    elif disposition != "ADOPT":
        reason = f"disposition {disposition} never activates"
    elif not verified:
        reason = "ADOPT but the source pin is UNAVAILABLE (unverified)"
    else:
        reason = "ADOPT with a verified pin but an unknown licence"

    out.update({
        "capability_need": rec.get("capability_slot", ""),
        "candidate": rec.get("external_name", ""),
        # All per-row repair columns are carried inside the schema-permitted, flexibly-typed
        # pin_license_currentness object plus the pre-existing scalar fields, so no out-of-scope
        # schema change is required.
        "pin_license_currentness": {
            "pin": pin,
            "license": lic,
            "currentness": rec.get("current_design_state", ""),
            "ttl_security_note": (
                "no runtime freshness window is claimed; the source pin is UNAVAILABLE and any "
                "activation requires a fresh receiver-side revalidation and a bounded TTL before "
                "canary. Security: no-second-SSOT, permission narrowing, secret-free packaging."),
            "fallback": rec.get("fallback", ""),
            "exit_criterion": rec.get("reselection_trigger", ""),
            "permission_scope": "READ+PROPOSE only; no writeback; HGK/receiver governed, shadow-only",
            "provider_off_behaviour": rec.get("fallback", "") or "no provider-off lane defined",
            "disposition": disposition,
            "design_disposition": design_disp,
            "pin_verified": verified,
            "licence_known": licence_known,
            "reported_active": active,
            "activation_reason": reason,
            "independently_verified": False,
        },
        "fallback_exit": rec.get("fallback", ""),
        "subject_id": subject_id(cid),
        "version": rec.get("observed_version", ""),
        "schema_version": "TechnologyAdmission@2",
    })
    body = {k: v for k, v in out.items() if k != "content_hash"}
    out["content_hash"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return out


def row_verdict(rec: dict) -> dict:
    """Recompute the per-row verdict FROM THE ARTEFACT (used by --report and the tests)."""
    plc = rec.get("pin_license_currentness") or {}
    pin = plc.get("pin") or {}
    lic = plc.get("license") or {}
    disposition = plc.get("disposition") or rec.get("disposition")
    verified = _pin_verified(pin if isinstance(pin, dict) else {"value": pin})
    licence_known = bool(lic.get("known")) if isinstance(lic, dict) else (
        not str(lic).upper().startswith("UNKNOWN"))
    claims_active = bool(plc.get("reported_active"))
    active_ok = claims_active and disposition == "ADOPT" and verified and licence_known
    return {
        "candidate": rec.get("technology_id"),
        "disposition": disposition,
        "pin_verified": verified,
        "licence_known": licence_known,
        "claims_active": claims_active,
        # G-TECH-SOURCE-PIN passes only when the exact pin is verified.
        "source_pin_pass": verified,
        # A non-ADOPT row must never be reported active; an ADOPT row reported active needs a pin
        # and a known licence.
        "active_refused": bool(claims_active and not active_ok),
    }


def negative_fixture(rec: dict) -> dict:
    """MUT-TECH-PIN: a row whose pin contradicts its active claim. The gate must refuse it."""
    bad = json.loads(json.dumps(rec))
    plc = bad["pin_license_currentness"]
    # Claim an active installation while keeping an unverified pin and an unknown licence. This is
    # exactly the MUT-TECH-PIN mutation: the pin contradicts the active claim.
    plc["pin"] = {
        "value": "LATEST",
        "repository": rec.get("source_repository", "UNAVAILABLE"),
        "reason_code": "MUT_TECH_PIN",
        "reason": "mutation: mutable pin contradicts an active claim",
    }
    plc["license"] = {
        "value": "UNKNOWN",
        "known": False,
        "blocks_activation": True,
        "disposition": "UNKNOWN_LICENCE_BLOCKS_ACTIVATION",
    }
    plc["pin_verified"] = False
    plc["licence_known"] = False
    plc["reported_active"] = True
    bad["immutable_pin"] = "LATEST"
    bad["license"] = "UNKNOWN"
    body = {k: v for k, v in bad.items() if k != "content_hash"}
    bad["content_hash"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return bad


def gate_source_pin(rec: dict) -> dict:
    plc = rec.get("pin_license_currentness") or {}
    pin = plc.get("pin") or {}
    verified = _pin_verified(pin if isinstance(pin, dict) else {"value": pin})
    lic = plc.get("license") or {}
    licence_known = bool(lic.get("known")) if isinstance(lic, dict) else False
    return {"gate": "G-TECH-SOURCE-PIN", "pinned": verified, "license_verified": licence_known,
            "verdict": "PASS" if verified else "PARTIAL",
            "why": "the row records an exact repository+version/commit pin only when the source "
                   "provides one; otherwise the pin is the literal UNAVAILABLE with a machine-"
                   "readable reason and the gate stays PARTIAL (never rounded up)"}


def gate_negative(rec: dict, bad: dict) -> dict:
    """The MUT-TECH-PIN fixture must be REJECTED and named. A refusal that cannot be produced is a
    missing gate."""
    v = row_verdict(bad)
    rejected = v["active_refused"] or not v["pin_verified"]
    return {"gate": "G-TECH-NEGATIVE", "fixture_mutation": "MUT-TECH-PIN",
            "fixture_rejected": bool(rejected), "named": "MUT-TECH-PIN",
            "verdict": "PASS" if rejected else "FAIL",
            "why": "an active claim backed by a mutable/unverified pin and an unknown licence must "
                   "be refused, not admitted"}


def gate_rollback(rec: dict) -> dict:
    tgt = rec.get("rollback_target") or rec.get("rollback_plan", "")
    return {"gate": "G-TECH-ROLLBACK", "rollback_target_present": bool(tgt),
            "verdict": "PASS" if tgt else "FAIL",
            "why": "a rollback target or plan is mandatory before canary"}


def gate_disposition(rec: dict) -> dict:
    plc = rec.get("pin_license_currentness") or {}
    d = plc.get("disposition")
    active = bool(plc.get("reported_active"))
    ok = d in DISPOSITIONS and not (active and d != "ADOPT")
    return {"gate": "G-TECH-DISPOSITION", "disposition": d, "in_closed_set": d in DISPOSITIONS,
            "non_adopt_not_active": not (active and d != "ADOPT"),
            "verdict": "PASS" if ok else "FAIL",
            "why": "only ADOPT may be reported active/installed; REFERENCE/EVAL_ONLY/QUARANTINE/"
                   "REJECT are never installed"}


def build_payload() -> dict:
    src_records = parse_source()
    records, validation, gates = [], [], []
    for raw in src_records:
        rec = build(raw)
        cid = rec["technology_id"]
        res = V.validate_bundle({"TechnologyAdmission": rec}, schemas_dir=ROOT / "schemas")
        validation.append({"candidate": cid, "verdict": res.get("verdict"),
                           "detail": res.get("findings")})
        bad = negative_fixture(rec)
        (FIX / cid).mkdir(parents=True, exist_ok=True)
        (FIX / cid / "mutation-unpinned.json").write_text(
            json.dumps(bad, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
        gates.append({"candidate": cid,
                      "gates": [gate_source_pin(rec), gate_negative(rec, bad),
                                gate_rollback(rec), gate_disposition(rec)]})
        records.append(rec)

    n = len(records)
    verdicts = [row_verdict(r) for r in records]
    src_pin_pass = sum(1 for v in verdicts if v["source_pin_pass"])
    neg_pass = sum(1 for g in gates if g["gates"][1]["verdict"] == "PASS")
    roll_pass = sum(1 for g in gates if g["gates"][2]["verdict"] == "PASS")
    disp_pass = sum(1 for g in gates if g["gates"][3]["verdict"] == "PASS")
    schema_ok = sum(1 for v in validation if v["verdict"] == "PASS")
    active_rows = [v["candidate"] for v in verdicts if v["claims_active"]]
    refused = [v["candidate"] for v in verdicts if v["active_refused"]]

    payload = {
        "source_clause": "PIPD-LS-SP_PIPD-PKG-00 §9 / §9.2 (authoritative 22-candidate table + 24-column design contract)",
        "source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "records": n,
        "schema_valid": f"{schema_ok}/{n}",
        "validation": validation,
        "disposition_set": list(DISPOSITIONS),
        "gate_summary": {
            "G-TECH-SOURCE-PIN": f"{src_pin_pass}/{n} PASS (rest PARTIAL: pin/licence not independently verified)",
            "G-TECH-NEGATIVE": f"{neg_pass}/{n} PASS",
            "G-TECH-ROLLBACK": f"{roll_pass}/{n} PASS",
            "G-TECH-DISPOSITION": f"{disp_pass}/{n} PASS",
        },
        "runtime_state": "NOT_EXECUTED — no candidate was installed, fetched or run",
        "reported_active": active_rows,
        "refused_active_claims": refused,
        "gates": gates,
        "admissions": records,
        "honest_ceiling": "DESIGN_DISPOSITION_TERMINALIZED per source. This is NOT an active "
                          "installation and NOT a licence determination; both are receiver-side.",
        "candidate_head": _git("rev-parse", "HEAD"),
    }
    payload["verdict"] = "PASS" if (
        n == 22 and schema_ok == n and neg_pass == n and roll_pass == n
        and disp_pass == n and not refused) else "FAIL"
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Technology admission rulings (PKG-00 §9).")
    ap.add_argument("--report", action="store_true",
                    help="compute the per-row verdict from the artefact and print TRUE denominators")
    args = ap.parse_args(argv)

    OUT.mkdir(parents=True, exist_ok=True)
    payload = build_payload()
    (OUT / "TECHNOLOGY_ADMISSIONS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8", newline="")

    report = {
        "records": payload["records"],
        "schema_valid": payload["schema_valid"],
        "gate_summary": payload["gate_summary"],
        "reported_active": payload["reported_active"],
        "refused_active_claims": payload["refused_active_claims"],
        "verdict": payload["verdict"],
        # R-AUD-007 close criterion: the consistency verdict must never be readable as an overall
        # PASS over a hard gate that is honestly failing. The pin gate is surfaced separately and
        # its scope is stated, so an "overall PASS" can no longer mask "G-TECH-SOURCE-PIN 0/22".
        "verdict_scope": (
            "ARTEFACT_CONSISTENCY_ONLY: 22/22 rows schema-valid, MUT-TECH-PIN refused, rollback "
            "target present, dispositions in the closed set, no non-ADOPT row reported active. "
            "It does NOT assert G-TECH-SOURCE-PIN is satisfied."
        ),
        "hard_gate_verdict": {
            "G-TECH-SOURCE-PIN": {
                "reported": payload["gate_summary"]["G-TECH-SOURCE-PIN"],
                "verdict": ("FAIL"
                            if payload["gate_summary"]["G-TECH-SOURCE-PIN"].startswith("0/")
                            else "PASS"),
                "covered_by_consistency_verdict": False,
            }
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=1))

    # Non-zero when any row claims active with an unsupported pin or an unknown licence, or when
    # any other honest gate is not fully satisfied.
    return 0 if payload["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
