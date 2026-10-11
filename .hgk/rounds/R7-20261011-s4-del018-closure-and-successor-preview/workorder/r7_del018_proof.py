#!/usr/bin/env python3
"""R7 Path A - DEL-018 closure proof.

DEL-018 RELEASE_MANIFEST@1 fails because build_publication_manifest.py --check --current finds
current-tree product paths that carry no disposition in the publication projection. The prescribed
minimal repair (A section 5.3) is to regenerate the evidence manifest and its seal, rebuild the
publication projection against the current candidate, bind the new commit/tree, and re-check.

This script proves the closure is NOT a coverage reduction. A regenerated manifest that simply
covers fewer paths would also make --check pass, so the entry count dropping is not by itself
evidence of repair. It asserts, from real git objects:

  P1  the tool's --check --current exits 0 and dispositions every current-tree product path
  P2  no PRODUCT-prefixed path present in the superseded manifest is absent from the new one
      (i.e. no product coverage was traded away to buy the pass)
  P3  every path dropped relative to the superseded manifest no longer exists in the working tree
      (i.e. the shrink is staleness removal, not silent scope loss)
  P4  the new manifest is a superset of the current tree's product paths

Exit 0 only if all four hold. Prints a JSON report; writes nothing.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRODUCT_PREFIXES = ("src/", "tools/", "tests/", "schemas/", "skills/", "docs/", "dist/", "fixtures")
MANIFEST = ".hgk/artifacts/evidence_manifest.json"
SUPERSEDED_REV = "HEAD"  # the commit the round branched from


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          encoding="utf-8", check=False).stdout


def main() -> int:
    root = Path(".")
    report: dict = {"step": "del018_closure_proof", "assertions": {}, "failures": []}

    # superseded manifest = the one committed at the branch point
    old_raw = git("show", f"{SUPERSEDED_REV}:{MANIFEST}")
    old = json.loads(old_raw) if old_raw.strip() else {}
    new = json.loads((root / MANIFEST).read_text(encoding="utf-8"))

    report["superseded_rev"] = git("rev-parse", SUPERSEDED_REV).strip()
    report["old_entries"] = len(old)
    report["new_entries"] = len(new)

    # P2 - no product path dropped
    dropped = sorted(set(old) - set(new))
    dropped_product = [p for p in dropped if p.startswith(PRODUCT_PREFIXES)]
    report["dropped_total"] = len(dropped)
    report["dropped_product"] = dropped_product
    report["assertions"]["P2_no_product_path_dropped"] = not dropped_product
    if dropped_product:
        report["failures"].append({"assertion": "P2", "detail": dropped_product[:10]})

    # P3 - every dropped path is gone from the tree
    still_present = [p for p in dropped if (root / p).exists()]
    report["dropped_still_present"] = still_present
    report["assertions"]["P3_dropped_paths_are_stale"] = not still_present
    if still_present:
        report["failures"].append({"assertion": "P3", "detail": still_present[:10]})

    # P1 + P4 - run the tool itself
    proc = subprocess.run([sys.executable, "-B", "tools/build_publication_manifest.py",
                           "--check", "--current"],
                          capture_output=True, text=True, encoding="utf-8", check=False)
    report["check_exit"] = proc.returncode
    try:
        check = json.loads(proc.stdout)
    except Exception:  # noqa: BLE001 - record the raw text rather than hide it
        check = {"raw": proc.stdout[:2000]}
    report["check"] = check
    cov_raw = check.get("current_tree_coverage")
    cov: dict = cov_raw if isinstance(cov_raw, dict) else {}
    report["assertions"]["P1_check_current_exit_0"] = proc.returncode == 0
    report["assertions"]["P4_all_current_product_paths_dispositioned"] = (
        cov.get("uncovered_count") == 0 and cov.get("paths_total") == cov.get("covered"))
    if proc.returncode != 0:
        report["failures"].append({"assertion": "P1", "detail": check.get("violations")})
    if cov.get("uncovered_count"):
        report["failures"].append({"assertion": "P4", "detail": cov.get("uncovered")})

    report["verdict"] = "PASS" if not report["failures"] else "FAIL"
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
