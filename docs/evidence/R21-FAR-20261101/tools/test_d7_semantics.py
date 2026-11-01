"""D7 contrast test: canonical vs candidate must DIFFER on the disputed fact.

Runs against the candidate module by import (never against canonical), and asserts the property
that was broken: an OAuth-direct attempt must report attribution WITHOUT claiming a usage row.
"""
import hashlib
import importlib.util
import json
import pathlib
import sys

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
CANON = ROOT / "HG-KSEOS" / "scripts" / "hgk-lane-dispatch.py"
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "patches" / "hgk-lane-dispatch.usage-semantics"
CAND = OUT / "hgk_lane_dispatch_candidate.py"

results = {}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


mod = load(CAND, "hgk_lane_dispatch_candidate")

oauth = {"usage_rows_after_offset": 0, "usage_receipt_ok": False, "arm_attribution_ok": True}
billed = {"usage_rows_after_offset": 3, "usage_receipt_ok": True, "usage_provider": "opencode-go"}
empty = {}

v1 = mod.derive_billing_view(oauth)
v2 = mod.derive_billing_view(billed)
v3 = mod.derive_billing_view(empty)

results["T1_oauth_direct_not_billed"] = {
    "view": v1, "pass": v1["usage_receipt_ok"] is False and v1["arm_attribution_ok"] is True
    and v1["billing_evidence"] == "none_local:oauth-direct" and v1["payer"] == "owner-openai-oauth"}
results["T2_ledger_row_billed"] = {
    "view": v2, "pass": v2["usage_receipt_ok"] is True and v2["billing_evidence"] == "usage-row"
    and v2["payer"] == "opencode-go"}
results["T3_nothing_known"] = {
    "view": v3, "pass": v3["usage_receipt_ok"] is False and v3["arm_attribution_ok"] is False
    and v3["billing_evidence"] == "none" and v3["payer"] == "unknown"}

cand_src = CAND.read_text(encoding="utf-8")
canon_src = CANON.read_text(encoding="utf-8")
force_line = 'att["usage_receipt_ok"] = True'
results["T4_canonical_still_forces_the_flag"] = {
    "canonical_occurrences": canon_src.count(force_line),
    "pass": canon_src.count(force_line) == 1}
results["T5_candidate_no_longer_forces_the_flag"] = {
    "candidate_occurrences": cand_src.count(force_line), "pass": cand_src.count(force_line) == 0}
results["T6_candidate_gate_accepts_attribution"] = {
    "pass": 'att.get("usage_receipt_ok") or att.get("arm_attribution_ok")' in cand_src}
results["T7_candidate_states_billing_at_top_level"] = {
    "pass": all(k in cand_src for k in ('receipt["billing_evidence"]', 'receipt["payer"]',
                                        'receipt["arm_attribution_ok"]'))}
results["T8_canonical_bytes_untouched"] = {
    "sha256": hashlib.sha256(CANON.read_bytes()).hexdigest(),
    "pass": hashlib.sha256(CANON.read_bytes()).hexdigest()
    == "524cfd8352df6c1085121d66c4c7d2ba3d7b023aea7e6eca9ded87a53f5c9071"}

# T9: replay the two REAL receipts through the new view and show what the reader now sees.
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
replay = {}
for name in ("PLAN_R21FAR_v2.json", "VERIFY_R21FAR.json"):
    d = json.loads((V / "far_receipts" / name).read_text(encoding="utf-8"))
    a = (d.get("attempts") or [{}])[0]
    view = mod.derive_billing_view({"usage_rows_after_offset": a.get("usage_rows_after_offset"),
                                    "usage_receipt_ok": a.get("usage_rows_after_offset", 0) > 0,
                                    "arm_attribution_ok": bool(a.get("identity_rollout"))})
    replay[name] = {"old_usage_receipt_ok": a.get("usage_receipt_ok"),
                    "old_usage_rows": a.get("usage_rows_after_offset"), "new_view": view}
results["T9_replay_real_receipts"] = {
    "replay": replay,
    "pass": all(r["new_view"]["usage_receipt_ok"] is False and r["new_view"]["arm_attribution_ok"] is True
                for r in replay.values())}

ok = all(v["pass"] for v in results.values())
payload = {"schema": "D7_USAGE_SEMANTICS_TEST/1", "candidate": str(CAND),
           "candidate_sha256": hashlib.sha256(CAND.read_bytes()).hexdigest(),
           "canonical": str(CANON), "canonical_sha256": results["T8_canonical_bytes_untouched"]["sha256"],
           "cases": results, "all_pass": ok,
           "ceiling": "logic-level contrast on a copy; canonical not edited, no dispatch re-run"}
(OUT / "TEST_USAGE_SEMANTICS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")
print(json.dumps({"all_pass": ok, "failing": [k for k, v in results.items() if not v["pass"]],
                  "cases": {k: v["pass"] for k, v in results.items()}}, ensure_ascii=False, indent=1))
