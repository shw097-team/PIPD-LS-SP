"""R5 acceptance-edge probe (case-driven): D1 polarity, D2 clause atoms, TYPE5 claim shapes.

Usage: probe_edges.py <frozen-subject-dir> <cases.json> <scratch-dir>

Deterministic, offline. Writes only inside <scratch-dir>. Compares each observed result with the
case's declared expectation and prints one JSON object: {cases:[...], summary:{...}}.
An observed value that does not match its expectation is a FAIL for that case - never silently
accepted - and a case whose expectation cannot be evaluated is INCONCLUSIVE.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _atoms(mod, text: str, scratch: Path, case_id: str):
    p = scratch / f"case_{case_id}.txt"
    p.write_text(text + "\n", encoding="utf-8")
    return mod.compile_requirements(f"probe {case_id}", [str(p)])


def main() -> int:
    subject = Path(sys.argv[1]).resolve()
    cases_path = Path(sys.argv[2]).resolve()
    scratch = Path(sys.argv[3]).resolve()
    installed = "--installed" in sys.argv[4:]
    scratch.mkdir(parents=True, exist_ok=True)
    if not installed:
        sys.path.insert(0, str(subject / "src"))
    from pipd_ls_sp import requirements as R
    from pipd_ls_sp import validate as V
    import pipd_ls_sp
    pkg_dir = Path(pipd_ls_sp.__file__).parent
    schemas_dir = pkg_dir / "schemas"
    if not schemas_dir.is_dir():  # source tree keeps schemas at the repo root
        schemas_dir = subject / "schemas"

    spec = json.loads(cases_path.read_text(encoding="utf-8"))
    rows = []

    def record(cid, kind, expect, observed, ok):
        rows.append({"id": cid, "kind": kind, "expect": expect,
                     "observed": observed, "match": ok})

    # --- D1 -----------------------------------------------------------------------------------
    for case in spec["d1"]:
        cid = case["id"]
        try:
            atoms = _atoms(R, case["text"], scratch, cid)
            pols = [a["risk_guard"]["polarity"] for a in atoms]
            spans = [a["source_clause"]["span"] for a in atoms]
            obs = {"polarities": pols, "spans": spans,
                   "statements": [a["source_clause"]["text"] for a in atoms],
                   "source_sha256_present": all(a["source_clause"].get("source_sha256")
                                                for a in atoms)}
            if "refuse" in case["expect"]:
                record(cid, "d1", case["expect"], obs, False)
            else:
                record(cid, "d1", case["expect"], obs,
                       pols == case["expect"]["polarities"])
        except Exception as exc:  # noqa: BLE001 - a refusal is an expected outcome here
            obs = {"exception": type(exc).__name__, "message": str(exc)[:200]}
            want = case["expect"].get("refuse")
            record(cid, "d1", case["expect"], obs,
                   bool(want) and type(exc).__name__ == want)

    # --- D2 -----------------------------------------------------------------------------------
    for case in spec["d2"]:
        cid = case["id"]
        try:
            atoms = _atoms(R, case["text"], scratch, cid)
            pols = [a["risk_guard"]["polarity"] for a in atoms]
            spans = [a["source_clause"]["span"] for a in atoms]
            span_ok = all(case["text"][s:e] == a["source_clause"]["text"].strip()
                          or a["source_clause"]["text"].strip() in case["text"][s:e]
                          for a, (s, e) in zip(atoms, spans))
            obs = {"atom_count": len(atoms), "polarities": pols, "spans": spans,
                   "statements": [a["source_clause"]["text"] for a in atoms],
                   "spans_point_into_source": span_ok,
                   "source_sha256_present": all(a["source_clause"].get("source_sha256")
                                                for a in atoms)}
            ok = (len(atoms) == case["expect"]["atom_count"]
                  and (case["expect"].get("polarities") is None
                       or pols == case["expect"]["polarities"])
                  and span_ok)
            record(cid, "d2", case["expect"], obs, ok)
        except Exception as exc:  # noqa: BLE001
            record(cid, "d2", case["expect"],
                   {"exception": type(exc).__name__, "message": str(exc)[:200]}, False)

    # --- TYPE5 --------------------------------------------------------------------------------
    def base(**kw):
        rec = {"allowed_claims": [], "forbidden_escalation": [], "close_conditions": {},
               "subject_id": "subject-00000001", "version": "1.0.0",
               "content_hash": "0" * 64, "schema_version": "ClaimCeiling@1"}
        rec.update(kw)
        return rec

    shapes = {
        "T1_allowed_null": base(allowed_claims=None),
        "T2_forbidden_null": base(forbidden_escalation=None),
        "T3_allowed_dict_item": base(allowed_claims=[{"claim": "RELEASED"}]),
        "T4_forbidden_dict": base(forbidden_escalation=[{"claim": "RELEASED"}]),
        "T5_unknown_claim": base(allowed_claims=["NOT_A_DECLARED_CLAIM"]),
        "POS_allowed_only": base(allowed_claims=["LOCAL_QUALIFIED"]),
        "POS_split_lists": base(allowed_claims=["PROMPT_COMPILE_PASS"],
                                forbidden_escalation=["RELEASED"]),
    }
    for case in spec["type5"]:
        cid = case["id"]
        rec = shapes[cid]
        want = case["expect"]
        native = None
        sem, sch = None, None
        try:
            sem = V.semantic_invariants("ClaimCeiling", rec)
            sch = V.validate_record("ClaimCeiling", rec, schemas_dir)
        except Exception as exc:  # noqa: BLE001 - a native escape is the defect TYPE5 names
            native = f"{type(exc).__name__}: {str(exc)[:160]}"
        obs = {"native_exception": native, "schema_findings": sch, "semantic_findings": sem}
        ok = ((bool(want["native_exception"]) == bool(native))
              and (bool(want["schema_finding"]) == bool(sch))
              and (bool(want["semantic_finding"]) == bool(sem)))
        record(cid, "type5", want, obs, ok)

    passed = sum(1 for r in rows if r["match"])
    out = {"schema": "R5R3-20261016/acceptance-edge-probe/1",
           "subject": str(subject),
           "claim_ceiling": "machine probe; not an acceptance",
           "cases": rows,
           "summary": {"total": len(rows), "match": passed, "fail": len(rows) - passed,
                       "verdict": "PASS" if passed == len(rows) else "FAIL"}}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
