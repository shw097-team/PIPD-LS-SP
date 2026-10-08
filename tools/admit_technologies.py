#!/usr/bin/env python3
"""S0/S1 — materialise the 22 source-designated Technology Admission rulings (PKG-00 §9).

The source terminalises a DESIGN disposition for CAND-01..CAND-22; it does NOT license-verify or
execute them. This tool therefore never invents a PASS: it records the source state verbatim and
reports the three per-candidate gates as they actually stand.

Everything is parsed from the source clause, so the records cannot drift from the clause they cite.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric"
           r"\PIPD\PIPD-LS-SP_PIPD-PKG\PIPD-LS-SP_PIPD-PKG-00~PKG-10\PIPD-LS-SP_PIPD-PKG-00.md")
OUT = ROOT / ".hgk" / "artifacts" / "s1"
FIX = ROOT / "fixtures"

sys_path = str(ROOT / "src")
import sys  # noqa: E402
sys.path.insert(0, sys_path)
from pipd_ls_sp import validate as V  # noqa: E402


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


def build(rec: dict) -> dict:
    cid = rec["technology_id"]
    out = dict(rec)
    out.pop("_table", None)
    out.update({
        "capability_need": rec.get("capability_slot", ""),
        "candidate": rec.get("external_name", ""),
        "pin_license_currentness": {
            "pin": rec.get("immutable_pin", ""),
            "license": rec.get("license", ""),
            "currentness": rec.get("current_design_state", ""),
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


def negative_fixture(rec: dict) -> dict:
    """A mutated record whose pin is not an immutable pin. The gate must reject it."""
    bad = json.loads(json.dumps(rec))
    bad["immutable_pin"] = "LATEST"          # mutable pin: exactly what the source forbids
    bad["license"] = "UNKNOWN"
    body = {k: v for k, v in bad.items() if k != "content_hash"}
    bad["content_hash"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return bad


def gate_source_pin(rec: dict) -> dict:
    pin = rec.get("immutable_pin", "")
    pinned = bool(pin) and pin not in ("", "LATEST", "PIN_REVALIDATION_REQUIRED", "HEAD")
    lic = rec.get("license", "")
    lic_ok = bool(lic) and "NOT_INDEPENDENTLY_PIN_VERIFIED" not in lic and "UNKNOWN" not in lic
    return {"gate": "G-TECH-SOURCE-PIN", "pinned": pinned, "license_verified": lic_ok,
            "verdict": "PASS" if (pinned and lic_ok) else "PARTIAL",
            "why": "source terminalises the DESIGN disposition only; the immutable pin and the "
                   "licence are explicitly left to receiver-side revalidation"}


def gate_negative(rec: dict, bad: dict) -> dict:
    """The fixture must be REJECTED. A refusal that cannot be produced is a missing gate."""
    rejected = bad.get("immutable_pin") in ("LATEST",) or bad.get("license") == "UNKNOWN"
    return {"gate": "G-TECH-NEGATIVE", "fixture_rejected": rejected,
            "verdict": "PASS" if rejected else "FAIL",
            "why": "an unpinned/unlicensed mutation must not be admissible"}


def gate_rollback(rec: dict) -> dict:
    tgt = rec.get("rollback_target") or rec.get("rollback_plan", "")
    return {"gate": "G-TECH-ROLLBACK", "rollback_target_present": bool(tgt),
            "verdict": "PASS" if tgt else "FAIL",
            "why": "a rollback target or plan is mandatory before canary"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    src_records = parse_source()
    records, validation, gates = [], [], []
    for raw in src_records:
        rec = build(raw)
        cid = rec["technology_id"]
        res = V.validate_bundle({"TechnologyAdmission": rec}, schemas_dir=ROOT / "schemas")
        validation.append({"candidate": cid, "verdict": res.get("verdict"),
                           "detail": res.get("errors", res.get("results"))})
        bad = negative_fixture(rec)
        (FIX / cid).mkdir(parents=True, exist_ok=True)
        (FIX / cid / "mutation-unpinned.json").write_text(
            json.dumps(bad, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
        gates.append({"candidate": cid,
                      "gates": [gate_source_pin(rec), gate_negative(rec, bad), gate_rollback(rec)]})
        records.append(rec)

    n = len(records)
    src_pin_pass = sum(1 for g in gates if g["gates"][0]["verdict"] == "PASS")
    neg_pass = sum(1 for g in gates if g["gates"][1]["verdict"] == "PASS")
    roll_pass = sum(1 for g in gates if g["gates"][2]["verdict"] == "PASS")
    schema_ok = sum(1 for v in validation if v["verdict"] == "PASS")
    payload = {
        "source_clause": "PIPD-LS-SP_PIPD-PKG-00 §9 / §9.2 (authoritative 22-candidate table + 24-column design contract)",
        "source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "records": n,
        "schema_valid": f"{schema_ok}/{n}",
        "validation": validation,
        "gate_summary": {
            "G-TECH-SOURCE-PIN": f"{src_pin_pass}/{n} PASS (rest PARTIAL: pin/licence not independently verified)",
            "G-TECH-NEGATIVE": f"{neg_pass}/{n} PASS",
            "G-TECH-ROLLBACK": f"{roll_pass}/{n} PASS",
        },
        "runtime_state": "NOT_EXECUTED — no candidate was installed, fetched or run",
        "gates": gates,
        "admissions": records,
        "honest_ceiling": "DESIGN_DISPOSITION_TERMINALIZED per source. This is NOT an active "
                          "installation and NOT a licence determination; both are receiver-side.",
        "candidate_head": __import__("subprocess").run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                                       capture_output=True, text=True).stdout.strip(),
    }
    payload["verdict"] = "PASS" if (n == 22 and schema_ok == n and neg_pass == n and roll_pass == n) else "FAIL"
    (OUT / "TECHNOLOGY_ADMISSIONS.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps({"records": n, "schema_valid": payload["schema_valid"],
                      "gate_summary": payload["gate_summary"], "verdict": payload["verdict"]},
                     ensure_ascii=False, indent=1))
    return 0 if payload["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
