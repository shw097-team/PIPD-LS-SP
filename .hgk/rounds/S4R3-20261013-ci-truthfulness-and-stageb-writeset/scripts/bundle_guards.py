#!/usr/bin/env python3
"""Two pre-dispatch guards, so a bundle that cannot support its claim never reaches a checker.

Guard 1 COVERAGE: every claim the bundle puts to a checker must have its required evidence blocks
present in what the bundle actually kept. This is the attempt-8 defect made mechanical: the receipt
claimed a `doctor` log that the same receipt's `blocks_kept` showed was dropped, and only a human
reading both fields noticed.

Guard 2 RECEIPTS: every claim must name a receipt path that exists on disk. A claim with no receipt is
not evidence and must be refused before dispatch, not after a lane run.

Both guards fail closed and return a non-zero exit. `--selftest` runs the positives AND the negatives,
because a guard nothing can fail is not a guard: a coverage check that never refuses would have passed
the attempt-8 bundle too.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

SCHEMA = "HGK-BUNDLE-GUARD/1"


def load(p: str) -> dict:
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def guard_coverage(spec: dict, bundle: dict) -> dict:
    kept = set(bundle.get("blocks_kept") or [])
    offered = set(bundle.get("blocks_offered") or [])
    out = {"guard": "COVERAGE", "refusals": [], "checks": []}
    for c in spec.get("claims", []):
        required = set(c.get("required_blocks") or [])
        missing = sorted(required - kept)
        out["checks"].append({
            "claim_id": c.get("claim_id"), "required": sorted(required),
            "missing_from_kept": missing,
            # A block that was never offered is a different defect from one that was dropped; name it.
            "never_offered": sorted(required - offered) if offered else [],
        })
        if missing:
            out["refusals"].append({
                "claim_id": c.get("claim_id"), "code": "ERR_CLAIM_BLOCK_NOT_KEPT",
                "detail": f"required blocks absent from blocks_kept: {missing}"})
    out["ok"] = not out["refusals"]
    return out


def guard_receipts(spec: dict, root: pathlib.Path) -> dict:
    out = {"guard": "RECEIPTS", "refusals": [], "checks": []}
    for c in spec.get("claims", []):
        paths = c.get("receipt_paths") or []
        resolved, missing = [], []
        for rel in paths:
            p = (root / rel)
            (resolved if p.is_file() else missing).append(rel)
        out["checks"].append({"claim_id": c.get("claim_id"), "declared": len(paths),
                              "resolved": resolved, "missing": missing})
        if not paths:
            out["refusals"].append({"claim_id": c.get("claim_id"),
                                    "code": "ERR_CLAIM_HAS_NO_RECEIPT",
                                    "detail": "no receipt path declared for this claim"})
        elif missing:
            out["refusals"].append({"claim_id": c.get("claim_id"),
                                    "code": "ERR_CLAIM_RECEIPT_UNRESOLVED",
                                    "detail": f"declared receipts do not exist: {missing}"})
    out["ok"] = not out["refusals"]
    return out


def selftest(tmp: pathlib.Path) -> dict:
    tmp.mkdir(parents=True, exist_ok=True)
    real = tmp / "REAL_RECEIPT.txt"
    real.write_text("a receipt that exists\n", encoding="utf-8")
    spec = {"claims": [
        {"claim_id": "C-good", "required_blocks": ["family_receipt", "doctor_receipt"],
         "receipt_paths": ["REAL_RECEIPT.txt"]},
    ]}
    good_bundle = {"blocks_offered": ["family_receipt", "doctor_receipt"],
                   "blocks_kept": ["family_receipt", "doctor_receipt"]}
    cases = []
    # positive: must pass both guards
    cov, rec = guard_coverage(spec, good_bundle), guard_receipts(spec, tmp)
    cases.append({"case": "positive", "expected": "pass", "coverage_ok": cov["ok"],
                  "receipts_ok": rec["ok"], "as_expected": cov["ok"] and rec["ok"]})
    # negative 1: the attempt-8 shape - doctor receipt offered but dropped
    dropped = {"blocks_offered": ["family_receipt", "doctor_receipt"],
               "blocks_kept": ["family_receipt"]}
    cov2 = guard_coverage(spec, dropped)
    cases.append({"case": "negative_dropped_block", "expected": "refuse",
                  "coverage_ok": cov2["ok"], "codes": [r["code"] for r in cov2["refusals"]],
                  "as_expected": not cov2["ok"]})
    # negative 2: a claim with no receipt at all
    spec_norec = {"claims": [{"claim_id": "C-norec", "required_blocks": ["family_receipt"],
                              "receipt_paths": []}]}
    rec2 = guard_receipts(spec_norec, tmp)
    cases.append({"case": "negative_no_receipt", "expected": "refuse", "receipts_ok": rec2["ok"],
                  "codes": [r["code"] for r in rec2["refusals"]], "as_expected": not rec2["ok"]})
    # negative 3: a declared receipt that does not exist
    spec_bad = {"claims": [{"claim_id": "C-missing", "required_blocks": ["family_receipt"],
                            "receipt_paths": ["DOES_NOT_EXIST.txt"]}]}
    rec3 = guard_receipts(spec_bad, tmp)
    cases.append({"case": "negative_missing_receipt_file", "expected": "refuse",
                  "receipts_ok": rec3["ok"], "codes": [r["code"] for r in rec3["refusals"]],
                  "as_expected": not rec3["ok"]})
    return {"schema": SCHEMA, "selftest": cases,
            "all_as_expected": all(c["as_expected"] for c in cases)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["coverage", "receipts", "selftest"])
    ap.add_argument("--spec")
    ap.add_argument("--bundle")
    ap.add_argument("--root", default=".")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.mode == "selftest":
        res = selftest(pathlib.Path(a.root))
        print(json.dumps(res, indent=2, ensure_ascii=False))
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n",
                                           encoding="utf-8")
        return 0 if res["all_as_expected"] else 1
    spec = load(a.spec)
    root = pathlib.Path(a.root)
    res = guard_coverage(spec, load(a.bundle)) if a.mode == "coverage" else guard_receipts(spec, root)
    res["schema"] = SCHEMA
    print(json.dumps(res, indent=2, ensure_ascii=False))
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n",
                                       encoding="utf-8")
    if not res["ok"]:
        print(f"REFUSED: {len(res['refusals'])} refusal(s); nothing may be dispatched for this spec",
              file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
