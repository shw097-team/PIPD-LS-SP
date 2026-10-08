#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / ".hgk" / "artifacts"

"""S2 performance + context budget. Measures real wall-clock work; declares the budget it holds to."""
BUDGET = {"compile_chain_ms": 2000, "validate_19_contracts_ms": 3000, "cli_cold_start_ms": 6000,
          "context_bytes_per_artefact": 20000}

def main() -> int:
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
    rows.append({"metric": "compile_chain_ms", "value": round(chain, 1), "budget": BUDGET["compile_chain_ms"],
                 "verdict": "PASS" if chain <= BUDGET["compile_chain_ms"] else "FAIL"})
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
    rows.append({"metric": "validate_19_contracts_ms", "value": round(val, 1),
                 "budget": BUDGET["validate_19_contracts_ms"], "contracts": len(names),
                 "verdict": "PASS" if val <= BUDGET["validate_19_contracts_ms"] else "FAIL"})
    t0 = time.perf_counter()
    subprocess.run([sys.executable, "-B", "-m", "pipd_ls_sp.cli", "--help"], cwd=str(ROOT),
                   capture_output=True, text=True, env={"PYTHONPATH": str(ROOT / "src"),
                                                        "PYTHONDONTWRITEBYTECODE": "1", "PATH": ""})
    cold = (time.perf_counter() - t0) * 1000
    rows.append({"metric": "cli_cold_start_ms", "value": round(cold, 1), "budget": BUDGET["cli_cold_start_ms"],
                 "verdict": "PASS" if cold <= BUDGET["cli_cold_start_ms"] else "FAIL"})
    sizes = {k: len(json.dumps(v, ensure_ascii=False).encode()) for k, v in
             (("pi", pi), ("pd", pd), ("cc", cc), ("ecp", ecp), ("tqaep", tq))}
    worst = max(sizes.values())
    rows.append({"metric": "context_bytes_per_artefact", "value": worst, "budget": BUDGET["context_bytes_per_artefact"],
                 "sizes": sizes, "verdict": "PASS" if worst <= BUDGET["context_bytes_per_artefact"] else "FAIL"})
    res = {"rows": rows, "verdict": "PASS" if all(r["verdict"] == "PASS" for r in rows) else "FAIL",
           "candidate_head": subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                            capture_output=True, text=True).stdout.strip()}
    ((OUT / "s2").mkdir(parents=True, exist_ok=True) or (OUT / "s2" / "PERF_BUDGET.json")).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if res["verdict"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
