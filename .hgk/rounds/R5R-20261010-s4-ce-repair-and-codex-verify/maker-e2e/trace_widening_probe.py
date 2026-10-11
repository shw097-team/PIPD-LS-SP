"""Reproduce the checker's counterexample CE-CODEX-TRACE-WIDENING against the CURRENT tree.

Uses the four records the maker probe captured verbatim from the compilers' own stdout, adds an
undeclared `trace` to PD-PKG / ECP / TQAEP without touching any other field or the content_hash,
and asks the validator what it thinks. Before the fix this printed PASS; it must now print FAIL.
"""
import copy
import json
import pathlib
import sys

REPO = pathlib.Path("C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt")
sys.path.insert(0, str(REPO / "src"))

from pipd_ls_sp import validate as V  # noqa: E402

M = REPO / ".hgk/rounds/R5R-20261010-s4-ce-repair-and-codex-verify/maker-e2e"
base = {}
for name, contract in (("pi", "PI-PKG"), ("pd", "PD-PKG"), ("ecp", "ECP"), ("tqaep", "TQAEP")):
    base[contract] = json.loads((M / f"{name}.json").read_text(encoding="utf-8"))

print("constants:")
print("  HASH_EXCLUDED_FIELDS =", V.HASH_EXCLUDED_FIELDS)
print("  NON_RECORD_SIDECARS  =", V.NON_RECORD_SIDECARS)
print()

print("happy path (untouched stdout bundle, PI-PKG still carries _profile_meta):")
res = V.validate_bundle(copy.deepcopy(base))
print("  PI-PKG has _profile_meta:", "_profile_meta" in base["PI-PKG"])
print("  ->", res["verdict"], "checked=", res["checked"], "findings=", res["findings"])
print()

print("counterexample: undeclared trace added to PD-PKG / ECP / TQAEP (nothing else touched):")
poisoned = copy.deepcopy(base)
for contract in ("PD-PKG", "ECP", "TQAEP"):
    poisoned[contract]["trace"] = {"undeclared": "silently accepted", "not_a_trace_list": True}
    print(f"  {contract}: content_hash unchanged =",
          poisoned[contract]["content_hash"] == base[contract]["content_hash"])
res2 = V.validate_bundle(poisoned)
print("  ->", res2["verdict"], "checked=", res2["checked"])
for f in res2["findings"]:
    print("     ", f)
print()

ok = (res["verdict"] == "PASS" and res["findings"] == []
      and res2["verdict"] == "FAIL"
      and all(any("trace" in f["detail"] for f in res2["findings"] if f["contract"] == c)
              for c in ("PD-PKG", "ECP", "TQAEP")))
print("COUNTEREXAMPLE CLOSED AND CE-2 STILL GREEN:", ok)
