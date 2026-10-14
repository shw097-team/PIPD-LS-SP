#!/usr/bin/env python3
"""Emit the family-IDENTITY receipt the verification lane asked for, twice.

Why this exists: the lane said, in three separate audits, that a numeric family count cannot
distinguish a correct registry from a silently reduced one that preserves the count - "19" is asserted
in the code rather than enumerated against anything. It named the artefact that would settle it: an
unredacted, head-committed output listing the per-family canonical NAMES, plus registry digests tied
to the head, taken from the INSTALLED package rather than the work tree.

This tool produces exactly that and nothing weaker. It prints, side by side:

  * the family names the code EXPECTS, in order (the §7.3 exact set), read from the installed module;
  * the family names the INSTALLED registry actually carries, in order;
  * the same inventory for a work tree given on the command line;
  * a per-file sha256 map for both, with the differences named in both directions;
  * named checks, so a mismatch cannot be waved through as a count that happens to match.

Exit status is 1 when any check fails, so a negative case can be demonstrated by running it against a
deliberately altered registry - a receipt nobody can falsify is not a receipt. It is a round script,
not product code: it lives under the round directory and does not touch either audited branch head.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

import pipd_ls_sp.registry as R


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inventory(d: pathlib.Path) -> dict:
    reg = json.loads((d / "registry.json").read_text(encoding="utf-8"))
    fams = reg.get("families") or []
    return {
        "schemas_dir": str(d),
        "family_count": len(fams),
        "family_names_in_order": [f["contract"] for f in fams],
        "required_field_counts": {f["contract"]: len(f.get("required_fields") or []) for f in fams},
        "per_file_sha256": {p.name: sha256(p) for p in sorted(d.glob("*.json"))},
    }


def main() -> int:
    src = R.describe_schemas_source()
    expected = {
        "expected_family_count": getattr(R, "EXPECTED_FAMILIES", None),
        "expected_names_in_order": list(getattr(R, "SOURCE_ORDER", []) or []),
    }
    installed = inventory(pathlib.Path(src["path"])) if src.get("path") else None
    tree_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
    tree = inventory(tree_path) if tree_path and (tree_path / "registry.json").is_file() else None

    checks: dict[str, object] = {}
    if installed and expected["expected_names_in_order"]:
        checks["installed_names_equal_expected_set_and_order"] = (
            installed["family_names_in_order"] == expected["expected_names_in_order"])
        checks["installed_count_equal_expected"] = (
            installed["family_count"] == expected["expected_family_count"])
        checks["installed_names_are_unique"] = (
            len(set(installed["family_names_in_order"])) == len(installed["family_names_in_order"]))
        checks["installed_every_family_has_required_fields"] = all(
            n > 0 for n in installed["required_field_counts"].values())
    if installed and tree:
        per_file = {k: installed["per_file_sha256"].get(k) == v
                    for k, v in tree["per_file_sha256"].items()}
        checks["installed_files_identical_to_tree"] = all(per_file.values())
        checks["per_file_identity"] = per_file
        checks["only_in_installed"] = sorted(set(installed["per_file_sha256"])
                                            - set(tree["per_file_sha256"]))
        checks["only_in_tree"] = sorted(set(tree["per_file_sha256"])
                                        - set(installed["per_file_sha256"]))
    bools = [v for v in checks.values() if isinstance(v, bool)]
    result = {
        "tool": "report_family_identity.py",
        "schemas_source": src,
        "expected": expected,
        "installed": installed,
        "tree": tree,
        "checks": checks,
        "verdict": "PASS" if bools and all(bools) else "FAIL",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
