"""Independent D1/D2 probe. Run against a given src root; prints JSON keyed by case.

Usage: python probe_req.py <src_root> <out.json>
"""
import json
import sys
import tempfile
from pathlib import Path

SRC_ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
sys.path.insert(0, str(SRC_ROOT))

from pipd_ls_sp import requirements as R  # noqa: E402

CASES = {
    # --- D1: negation surface ---
    "d1_bu_yunxu": "系統不允許傳送個資。",
    "d1_bu_xuke": "系統不許可傳送個資。",
    "d1_qing_wu": "系統請勿傳送個資。",
    "d1_should_not": "The system should not publish customer secrets.",
    "d1_is_not_allowed": "The system is not allowed to publish customer secrets.",
    "d1_baseline_bude": "系統不得上傳遙測。",
    # --- D1 scope ---
    "d1_scope_comma": "系統必須記錄稽核日誌，不得外洩個資。",
    "d1_scope_yiji": "系統必須記錄日誌以及不得外洩個資。",
    "d1_scope_and": "The system must log events and must not leak data.",
    "d1c_no_boundary": "系統必須不得外洩個資。",
    "d1c_yinggai": "系統應該不得外洩個資。",
    # over-broad refusal candidates (adversarial)
    "adv_noun_bixu": "不得使用必須的憑證。",
    "adv_chinese_conj_er": "系統必須記錄日誌而不得外洩個資。",
    "adv_chinese_conj_bingqie": "系統必須記錄日誌並且不得外洩個資。",
    "adv_bude_xuyao": "不得需要額外授權。",
    # --- D2: token-internal periods ---
    "d2_domain": "系統不得上傳至 api.example.com。",
    "d2_version": "版本必須為 v1.2.3。",
    "d2_decimal": "比例必須為 1.25。",
    "d2_cjk_sentence": "系統必須記錄日誌.版本必須為 1.2。",
    "d2_plain_period_space": "Do task A. Task B must run.",
    "d2_ascii_nospace": "Do task A.Task B must run.",
    "d2_ascii_nospace_digit": "Rate is 5.Use 3.",
    "d2_ascii_nospace_com": "See api.example.com.Next must run.",
    "d2_trailing_period": "The system must log.",
    "d2_eg": "See e.g. the spec.",
}


def run(text: str):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "src.txt"
        p.write_text(text, encoding="utf-8")
        try:
            atoms = R.compile_requirements("goal", [str(p)])
        except Exception as exc:  # noqa: BLE001
            return {"exc": type(exc).__name__, "msg": str(exc)}
    return {
        "n": len(atoms),
        "atoms": [
            {
                "text": a["source_clause"]["text"],
                "polarity": a["risk_guard"]["polarity"],
                "span": a["source_clause"]["span"],
                "clause_id": a["source_clause"]["clause_id"],
                "req_id": a["req_id"],
                "sha": a["source_clause"]["source_sha256"],
                "roundtrip_ok": text[a["source_clause"]["span"][0]:a["source_clause"]["span"][1]]
                                == a["source_clause"]["text"],
            }
            for a in atoms
        ],
    }


out = {name: run(text) for name, text in CASES.items()}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"wrote {OUT} ({len(out)} cases)")
