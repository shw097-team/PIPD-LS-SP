"""Build the D7 candidate patch for HG-KSEOS/scripts/hgk-lane-dispatch.py.

Defect measured on 2026-11-01 (R21-FAR-20261101):
  an OAuth-direct turn writes NO usage row, so the dispatcher FORCE-SETS usage_receipt_ok=True
  from the codex rollout identity (canonical lines ~3033-3044). Two real receipts then carry
  usage_rows_after_offset=0 / usage_provider=None / usage_receipt_ok=True, and a reader cannot tell
  "an arm answered" from "a usage row was billed".

Fix (semantic separation, no behavioural relaxation):
  * usage_receipt_ok keeps its MEASURED value (False when no ledger row matched);
  * a new arm_attribution_ok carries the rollout-derived fact;
  * billing_evidence + payer state, in the receipt, that no local billing row exists;
  * the serving gate accepts either fact, so OAuth-direct lanes still pass;
  * required_arm_note stops contradicting required_arm_satisfied.

Canonical file is NOT modified: everything lands in this patches/ directory.
"""
import difflib
import json
import pathlib
import py_compile
import re

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
CANON = ROOT / "HG-KSEOS" / "scripts" / "hgk-lane-dispatch.py"
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "patches" / "hgk-lane-dispatch.usage-semantics"
OUT.mkdir(parents=True, exist_ok=True)

src = CANON.read_text(encoding="utf-8")

HELPER = '''

def derive_billing_view(attempt: dict) -> dict:
    """Three facts a receipt must never conflate (D7, R21-FAR-20261101).

    `usage_receipt_ok` answers "did a usage ledger row bind to this attempt?".
    `arm_attribution_ok` answers "did the client record which arm served?".
    `payer` answers "who is billed?", and is only knowable when a row or a declared
    alias says so. An OAuth-direct turn has attribution but NO local billing evidence.
    """
    rows = int(attempt.get("usage_rows_after_offset") or 0)
    measured = bool(attempt.get("usage_receipt_ok"))
    attribution = bool(attempt.get("arm_attribution_ok"))
    if measured:
        billing = "usage-row"
        payer = attempt.get("usage_provider") or "unknown"
    elif attribution:
        billing = "none_local:oauth-direct"
        payer = attempt.get("payer") or "owner-openai-oauth"
    else:
        billing = "none"
        payer = "unknown"
    return {"usage_rows": rows, "usage_receipt_ok": measured,
            "arm_attribution_ok": attribution, "billing_evidence": billing, "payer": payer}

'''

REPLACEMENTS = [
    # 1) stop forcing usage_receipt_ok; record attribution separately
    (
        '''                att["identity_rollout"] = ident["rollout"]
                att["usage_receipt_ok"] = True
                att["identity_note"] = "served arm read from the codex rollout written for this run and cwd"''',
        '''                att["identity_rollout"] = ident["rollout"]
                # D7: a rollout identity proves WHICH arm answered, never that a usage row exists.
                # usage_receipt_ok keeps the measured value (False when no ledger row bound).
                att["arm_attribution_ok"] = True
                att["arm_attribution_source"] = ident["source"]
                att["billing_evidence"] = "none_local:oauth-direct"
                att["identity_note"] = "served arm read from the codex rollout written for this run and cwd"''',
    ),
    # 2) serving gate accepts either fact (no relaxation of the arm guard itself)
    (
        '''        if att.get("exit") == 0 and att.get("nonce_present") and att.get("usage_receipt_ok"):''',
        '''        if att.get("exit") == 0 and att.get("nonce_present") and (
                att.get("usage_receipt_ok") or att.get("arm_attribution_ok")):''',
    ),
    # 3) surface the separated facts at the top level
    (
        '''    receipt["usage_receipt_ok"] = bool(_serving.get("usage_receipt_ok")) if _serving else False''',
        '''    receipt["usage_receipt_ok"] = bool(_serving.get("usage_receipt_ok")) if _serving else False
    # D7: state attribution and billing separately, so "an arm answered" can never be read as
    # "a usage row was billed". A missing ledger row is recorded, not hidden behind a boolean.
    _billing = derive_billing_view(_serving) if _serving else derive_billing_view({})
    receipt["arm_attribution_ok"] = _billing["arm_attribution_ok"]
    receipt["billing_evidence"] = _billing["billing_evidence"]
    receipt["payer"] = _billing["payer"]
    receipt["usage_rows_bound"] = _billing["usage_rows"]''',
    ),
    # 4) a satisfied pin must not carry the "not satisfied" note
    (
        '''        receipt["required_arm"] = str(args.require_arm)
        receipt["required_arm_satisfied"] = False
        receipt["required_arm_note"] = "no arm served; the pin is recorded, not satisfied"''',
        '''        receipt["required_arm"] = str(args.require_arm)
        receipt["required_arm_satisfied"] = False
        receipt["required_arm_note"] = "no arm served; the pin is recorded, not satisfied"
    # D7: drop a stale note once an arm DID serve, otherwise one receipt says both things.''',
    ),
]

patched = src
applied = []
for old, new in REPLACEMENTS:
    n = patched.count(old)
    if n != 1:
        raise SystemExit(f"anchor not unique ({n}): {old.splitlines()[0][:70]}")
    patched = patched.replace(old, new)
    applied.append(old.splitlines()[0].strip()[:60])

# the note fix: clear the note on the positive path
anchor_pos = '''        receipt["required_arm"] = str(args.require_arm)
        receipt["served_arm_raw"] = served_arm_of(used["provider"], used["model"])'''
if patched.count(anchor_pos) != 1:
    raise SystemExit("positive-arm anchor not unique")
patched = patched.replace(
    anchor_pos,
    '''        receipt["required_arm"] = str(args.require_arm)
        receipt.pop("required_arm_note", None)   # D7: a served pin must not keep the refusal note
        receipt["served_arm_raw"] = served_arm_of(used["provider"], used["model"])''')
applied.append("receipt.pop(required_arm_note) on the served path")

# insert the helper before the ARM_ALIASES block (module level, importable)
alias_anchor = "# --- Owner-declared provider ALIASES (FAR-B1-v2, N-6) ---"
if patched.count(alias_anchor) != 1:
    raise SystemExit("alias anchor not unique")
patched = patched.replace(alias_anchor, HELPER.strip("\n") + "\n\n" + alias_anchor)

cand = OUT / "hgk_lane_dispatch_candidate.py"
cand.write_text(patched, encoding="utf-8", newline="\n")
py_compile.compile(str(cand), doraise=True)

diff = "".join(difflib.unified_diff(
    src.splitlines(keepends=True), patched.splitlines(keepends=True),
    fromfile="HG-KSEOS/scripts/hgk-lane-dispatch.py",
    tofile="candidate/hgk_lane_dispatch_candidate.py", n=3))
(OUT / "usage_semantics.patch").write_text(diff, encoding="utf-8", newline="\n")

print(json.dumps({"applied": applied, "candidate_bytes": cand.stat().st_size,
                  "patch_bytes": len(diff), "canonical_unchanged":
                  __import__("hashlib").sha256(CANON.read_bytes()).hexdigest()}, ensure_ascii=False, indent=1))
