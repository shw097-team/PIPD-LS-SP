#!/usr/bin/env python3
"""S2 performance + context budget. Measures real wall-clock work; declares the budget it holds to.

Every threshold now carries its PROVENANCE: `measurement` (how the value is produced),
`denominator` (what the value is divided by, or "" when it is an absolute bound) and
`source_of_truth` (the file/rule the number is derived from). A threshold with no such rule in the
repo is marked `UNPROVENANCED`. The verdict is **fail-closed**: an *exceeded* budget is always
`FAIL` (provenance cannot turn an over-budget measurement green), a within-budget unprovenanced row
is `UNDECIDABLE` (never PASS), and a within-budget provenanced row is `PASS`. `--check` exits
non-zero whenever any row FAILs. No numeric threshold was raised or lowered by adding this
provenance.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / ".hgk" / "artifacts"

# The numeric thresholds are unchanged; provenance is added alongside them, never folded into them.
#
# R5 S4 owner adjudication (2026-10-10): the four original thresholds were UNPROVENANCED and the
# absolute `context_bytes_per_artefact` row could never pass on a corpus of this size. The owner
# re-specified the budget as a scale-invariant RATE (`bytes_per_atom`) and demoted the original
# absolute row plus the three timing rows to ADVISORY: they stay measured, stay printed, and keep
# their historical verdicts, but they no longer vote on the overall verdict. The historical
# block reports the RECORDED value that the frozen BYTES_PER_ATOM_BASELINE.json supplies for a
# metric (`pi_bytes` = 343,547 for `context_bytes_per_artefact`), so the 343,547 > 20,000 FAIL is
# host-stable; the live reading is kept beside it as `measured_now`, and every row marks whether
# its `value` is `recorded`.
# No threshold was raised or lowered by this change; only which rows vote changed.
PROVENANCE = {
    "compile_chain_ms": {
        "budget": 2000,
        "measurement": "wall-clock perf_counter around intake->compile_pi->bind_pd->"
                       "compile_construction_contract->compile_ecp->compile_tqaep, ms",
        "denominator": "",
        "source_of_truth": "UNPROVENANCED",
        "voting": False,
        "advisory_reason": "no consumer was ever named for this bound; measured headroom 2.35x, "
                           "and no entity in the product depends on the number",
    },
    "validate_19_contracts_ms": {
        "budget": 3000,
        "measurement": "wall-clock perf_counter loading every registry family schema, ms",
        "denominator": "19 registry families (registry.json)",
        "source_of_truth": "UNPROVENANCED",
        "voting": False,
        "advisory_reason": "measured headroom 1,579x - the row cannot fire and carries no signal",
    },
    "cli_cold_start_ms": {
        "budget": 6000,
        "measurement": "wall-clock perf_counter of `python -B -m pipd_ls_sp.cli --help` "
                       "in a fresh interpreter, ms",
        "denominator": "",
        "source_of_truth": "UNPROVENANCED",
        "voting": False,
        "advisory_reason": "measured headroom 51x - the row cannot fire and carries no signal",
    },
    "context_bytes_per_artefact": {
        "budget": 20000,
        "measurement": "max of len(json.dumps(artefact)) in UTF-8 bytes over PI/PD/CC/ECP/TQAEP",
        "denominator": "one artefact (bytes per artefact, not per atom)",
        "source_of_truth": "UNPROVENANCED",
        "voting": False,
        "advisory_reason": "superseded by the owner re-specification of 2026-10-10: the budget is "
                           "now the scale-invariant rate bytes_per_atom. The absolute reading is "
                           "kept because its historical FAIL must stay visible, not to decide.",
        "preserve_history": True,
    },
    # The voting row, per docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json
    # ruling S2_BUDGET_DEFINITION = PER_ATOM_BYTES(2000).
    "bytes_per_atom": {
        "budget": 2000,
        "measurement": "len(json.dumps(PI, ensure_ascii=False)) UTF-8 bytes divided by the number "
                       "of atoms in PI.stable_semantic_contract.atoms",
        "denominator": "one atom (bytes per atom, scale-invariant)",
        "source_of_truth": "docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json#/rulings/S2_BUDGET_DEFINITION",
        "voting": True,
    },
}
BUDGET = {k: v["budget"] for k, v in PROVENANCE.items()}

# Regression guard (R5 of the FAR): the rate must not grow against a frozen baseline. The baseline
# is only written by an explicit --freeze-baseline, so --check never mutates the tree.
BASELINE_FILE = "BYTES_PER_ATOM_BASELINE.json"
REGRESSION_TOLERANCE_PCT = 10.0

# Advisory (historical) metrics whose `value` must come from a FROZEN recording, not from a fresh
# measurement on this host: a recorded verdict that moves with the machine is not a record. Only
# metrics listed here are recorded; everything else keeps its live measurement (recorded: false).
RECORDED_BASELINE = {
    "context_bytes_per_artefact": {
        "file": Path(".hgk", "artifacts", "s2", BASELINE_FILE).as_posix(),
        "field": "pi_bytes",
    },
}


def _verdict(value: float, budget: float, source_of_truth: str) -> str:
    """Decide one threshold's verdict, fail-closed.

    An *exceeded* budget is always FAIL - an over-budget measurement is a fact about the artefact,
    not a statement about whether someone ratified the threshold. Provenance can only downgrade a
    within-budget row (PASS -> UNDECIDABLE); it can never turn an over-budget row green.
    """
    if value > budget:
        return "FAIL"
    if source_of_truth == "UNPROVENANCED":
        return "UNDECIDABLE"
    return "PASS"


UNRATIFIED_NOTE = ("threshold authority is unratified: no in-repo source_of_truth; the row is "
                   "decided by the measurement alone (an over-budget value still FAILs)")


def _row(metric: str, value: float, **extra) -> dict:
    prov = PROVENANCE[metric]
    # The decision uses the UNROUNDED raw measurement; rounding is display-only. Rounding first
    # could hide a real overrun (e.g. raw 2000.04 against a 2000 budget rounds to 2000.0 and would
    # read as within budget). `value`/`value_display` are what gets printed.
    display = round(value, 1) if isinstance(value, float) else value
    row = {"metric": metric, "value": display, "value_display": display,
           "budget": prov["budget"], **extra,
           "measurement": prov["measurement"], "denominator": prov["denominator"],
           "source_of_truth": prov["source_of_truth"],
           "voting": prov.get("voting", True)}
    if "advisory_reason" in prov:
        row["advisory"] = True
        row["advisory_reason"] = prov["advisory_reason"]
    if prov.get("preserve_history"):
        row["preserved"] = True
    row["exceeded"] = value > prov["budget"]
    row["verdict"] = _verdict(value, prov["budget"], prov["source_of_truth"])
    if prov["source_of_truth"] == "UNPROVENANCED":
        row["note"] = UNRATIFIED_NOTE
    return row


def overall_verdict(rows: list[dict]) -> str:
    """Overall verdict: any FAIL dominates; UNDECIDABLE only when nothing failed."""
    if any(r.get("verdict") == "FAIL" for r in rows):
        return "FAIL"
    if any(r.get("verdict") == "UNDECIDABLE" for r in rows):
        return "UNDECIDABLE"
    return "PASS"


def exit_code(verdict: str) -> int:
    """Non-zero iff the overall verdict is FAIL; UNDECIDABLE without any exceeded row is not a
    hard failure."""
    return 1 if verdict == "FAIL" else 0


def _recorded_value(metric: str, baseline: dict | None) -> tuple[object, dict | None]:
    """The RECORDED value for an advisory metric, read from a frozen baseline.

    Returns `(value, origin)` when a recorded baseline supplies the metric, else `(None, None)`.
    Never invents a number: an absent, unreadable, or field-less baseline yields `(None, None)`
    and the caller must fall back to the live measurement *and say so*.
    """
    spec = RECORDED_BASELINE.get(metric)
    if not spec or not baseline or spec["field"] not in baseline:
        return None, None
    return baseline[spec["field"]], {"file": spec["file"], "field": spec["field"]}


def _historical_row(row: dict, baseline: dict | None) -> dict:
    """One `historical` row: the RECORDED value when the baseline supplies one, else the live
    measurement (marked `recorded: false` with a note, never a fabricated record)."""
    metric = row["metric"]
    measured_now = row["value"]
    recorded, origin = _recorded_value(metric, baseline)
    value = measured_now if recorded is None else recorded
    out = {"metric": metric, "value": value, "measured_now": measured_now,
           "recorded": recorded is not None, "origin": origin,
           "budget": row["budget"],
           "verdict": _verdict(value, row["budget"], row["source_of_truth"]),
           "exceeded": value > row["budget"],
           "source_of_truth": row["source_of_truth"]}
    if recorded is None:
        out["note"] = ("no recorded value was available for this metric; `value` is the live "
                       "measurement, not a recorded one")
    return out


def candidate_head(repo: Path | None = None) -> str:
    """Resolve HEAD via `git -C <repo> rev-parse HEAD`; honest fallback only when git is absent."""
    repo = repo or ROOT
    try:
        proc = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
    except (FileNotFoundError, OSError):
        return "UNBOUND_NO_GIT_BINARY"
    if proc.returncode != 0:
        return "UNBOUND_NO_GIT_BINARY"
    head = proc.stdout.strip()
    return head or "UNBOUND_NO_GIT_BINARY"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report each budget entry's verdict; UNDECIDABLE is not a failure")
    ap.add_argument("--freeze-baseline", action="store_true",
                    help="record the current bytes_per_atom as the regression baseline (the only "
                         "mode that writes anything)")
    args = ap.parse_args(argv)

    from pipd_ls_sp import pipeline as P, validate as V
    GOAL = "Implement the lifecycle compiler and verify it against the source spec."
    src = str(ROOT / "docs" / "S0_CONTRACT_SPEC.md")
    rows = []
    t0 = time.perf_counter()
    card = P.intake(GOAL, sources=[src]); pi = P.compile_pi(card, "STANDARD")
    pd = P.bind_pd(pi, {"root": str(ROOT), "head": "x", "tracked_files": 1, "writable_scope": "src/**"})
    cc = P.compile_construction_contract(pd); ecp = P.compile_ecp(pd, pi)
    tq = P.compile_tqaep(pi, ecp, maker="M", checker="C", checker_execution_receipt="r")
    chain = (time.perf_counter() - t0) * 1000
    rows.append(_row("compile_chain_ms", chain))
    import pipd_ls_sp.registry as R
    reg = R.load_registry(ROOT / "schemas"); names = [f["contract"] for f in reg["families"]]
    t0 = time.perf_counter()
    for n in names:
        try:
            V.load_contract_schemas = None
            R.load_schema(n, ROOT / "schemas")
        except Exception:
            pass
    val = (time.perf_counter() - t0) * 1000
    rows.append(_row("validate_19_contracts_ms", val, contracts=len(names)))
    t0 = time.perf_counter()
    subprocess.run([sys.executable, "-B", "-m", "pipd_ls_sp.cli", "--help"], cwd=str(ROOT),
                   capture_output=True, text=True, env={"PYTHONPATH": str(ROOT / "src"),
                                                        "PYTHONDONTWRITEBYTECODE": "1", "PATH": ""})
    cold = (time.perf_counter() - t0) * 1000
    rows.append(_row("cli_cold_start_ms", cold))
    sizes = {k: len(json.dumps(v, ensure_ascii=False).encode()) for k, v in
             (("pi", pi), ("pd", pd), ("cc", cc), ("ecp", ecp), ("tqaep", tq))}
    worst = max(sizes.values())
    rows.append(_row("context_bytes_per_artefact", worst, sizes=sizes))

    # The scale-invariant rate that actually votes, plus its frozen-baseline regression guard.
    atoms = (pi.get("stable_semantic_contract") or {}).get("atoms") or []
    n_atoms = len(atoms)
    pi_bytes = sizes["pi"]
    per_atom = pi_bytes / n_atoms if n_atoms else float("inf")
    base_path = OUT / "s2" / BASELINE_FILE
    baseline = None
    if base_path.exists():
        try:
            baseline = json.loads(base_path.read_text(encoding="utf-8"))
        except Exception:
            baseline = None
    reg_extra: dict = {"pi_bytes": pi_bytes, "atoms": n_atoms}
    if baseline:
        b = float(baseline.get("bytes_per_atom", 0) or 0)
        lim = b * (1 + REGRESSION_TOLERANCE_PCT / 100)
        reg_extra.update({"baseline_bytes_per_atom": b, "tolerance_pct": REGRESSION_TOLERANCE_PCT,
                          "baseline_limit": round(lim, 1),
                          "regression": "REGRESSED" if per_atom > lim else "WITHIN_TOLERANCE"})
    else:
        reg_extra.update({"regression": "UNTESTED",
                          "how_to_freeze": "python -B tools/perf_budget.py --freeze-baseline"})
    per_row = _row("bytes_per_atom", per_atom, **reg_extra)
    if reg_extra["regression"] == "REGRESSED":
        per_row["verdict"] = "FAIL"
        per_row["regression_fail"] = True
    rows.append(per_row)

    voting = [r for r in rows if r.get("voting", True)]
    advisory = [r for r in rows if not r.get("voting", True)]
    historical_rows = [_historical_row(r, baseline) for r in advisory]
    preserved_metrics = {r["metric"] for r in advisory if r.get("preserved")}
    undecidable = [r["metric"] for r in voting if r["verdict"] == "UNDECIDABLE"]
    fails = [r["metric"] for r in voting if r["verdict"] == "FAIL"]
    exceeded = [r["metric"] for r in voting if r.get("exceeded")]
    verdict = overall_verdict(voting)
    res = {"rows": rows, "verdict": verdict,
           "voting_metrics": [r["metric"] for r in voting],
           "advisory_metrics": [r["metric"] for r in advisory],
           "undecidable": undecidable, "failed": fails, "exceeded": exceeded,
           "historical": {
               "note": "measured and printed but non-voting. Where a recorded baseline supplies "
                       "the value for a metric (see that row's `origin`), `value` is the RECORDED "
                       "number and the live reading is kept as `measured_now`; a metric with no "
                       "recorded baseline keeps its live measurement and is marked "
                       "`recorded: false`.",
               "rows": historical_rows,
               "preserved_fails": [r["metric"] for r in historical_rows
                                   if r["metric"] in preserved_metrics and r["verdict"] == "FAIL"],
           },
           "adjudication": {
               "authority": "docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json",
               "ruling": "S2_BUDGET_DEFINITION = PER_ATOM_BYTES(2000); timing rows ADVISORY",
               "artefact_unchanged": True,
           },
           "candidate_head": candidate_head()}
    if not args.check:
        (OUT / "s2").mkdir(parents=True, exist_ok=True)
        (OUT / "s2" / "PERF_BUDGET.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    if args.freeze_baseline:
        (OUT / "s2").mkdir(parents=True, exist_ok=True)
        base_path.write_text(json.dumps(
            {"bytes_per_atom": round(per_atom, 2), "atoms": n_atoms, "pi_bytes": pi_bytes,
             "tolerance_pct": REGRESSION_TOLERANCE_PCT,
             "frozen_head": candidate_head()}, ensure_ascii=False, indent=1),
            encoding="utf-8", newline="")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    # Fail-closed: an exceeded VOTING budget FAILs the run. A regression against the frozen baseline
    # FAILs too. Advisory rows never decide - they cannot turn the gate green either.
    return exit_code(verdict)


if __name__ == "__main__":
    raise SystemExit(main())
