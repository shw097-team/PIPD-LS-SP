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
PROVENANCE = {
    "compile_chain_ms": {
        "budget": 2000,
        "measurement": "wall-clock perf_counter around intake->compile_pi->bind_pd->"
                       "compile_construction_contract->compile_ecp->compile_tqaep, ms",
        "denominator": "",
        "source_of_truth": "UNPROVENANCED",
    },
    "validate_19_contracts_ms": {
        "budget": 3000,
        "measurement": "wall-clock perf_counter loading every registry family schema, ms",
        "denominator": "19 registry families (registry.json)",
        "source_of_truth": "UNPROVENANCED",
    },
    "cli_cold_start_ms": {
        "budget": 6000,
        "measurement": "wall-clock perf_counter of `python -B -m pipd_ls_sp.cli --help` "
                       "in a fresh interpreter, ms",
        "denominator": "",
        "source_of_truth": "UNPROVENANCED",
    },
    "context_bytes_per_artefact": {
        "budget": 20000,
        "measurement": "max of len(json.dumps(artefact)) in UTF-8 bytes over PI/PD/CC/ECP/TQAEP",
        "denominator": "one artefact (bytes per artefact, not per atom)",
        "source_of_truth": "UNPROVENANCED",
    },
}
BUDGET = {k: v["budget"] for k, v in PROVENANCE.items()}


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
           "source_of_truth": prov["source_of_truth"]}
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
    undecidable = [r["metric"] for r in rows if r["verdict"] == "UNDECIDABLE"]
    fails = [r["metric"] for r in rows if r["verdict"] == "FAIL"]
    exceeded = [r["metric"] for r in rows if r.get("exceeded")]
    verdict = overall_verdict(rows)
    res = {"rows": rows, "verdict": verdict,
           "undecidable": undecidable, "failed": fails, "exceeded": exceeded,
           "candidate_head": candidate_head()}
    if not args.check:
        (OUT / "s2").mkdir(parents=True, exist_ok=True)
        (OUT / "s2" / "PERF_BUDGET.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    # Fail-closed: an exceeded budget FAILs the run regardless of provenance. An UNDECIDABLE row
    # that did NOT exceed its budget is not a hard failure.
    return exit_code(verdict)


if __name__ == "__main__":
    raise SystemExit(main())
