"""Adversarial probes for D1b merge behaviour and other edge cases.

Usage: python probe_adv.py <src_root> <out.json>
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
    "all_negated_comma": "系統不得交付遙測資料，不得上傳日誌。",
    "all_negated_comma2": "系統不得外洩個資，不得延遲交付。",
    "all_negated_en": "The system must not log data, must not leak data.",
    "all_negated_yiji": "系統不得外洩個資以及不得延遲。",
    "mixed_comma": "系統必須記錄日誌，不得外洩個資。",
    "mixed_rev": "系統不得外洩個資，必須記錄日誌。",
    "three_agree": "不得A，不得B，不得C。",
    "three_mixed": "必須A，不得B，必須C。",
}


def run(text):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "s.txt"
        p.write_text(text, encoding="utf-8")
        try:
            atoms = R.compile_requirements("g", [str(p)])
        except Exception as exc:  # noqa: BLE001
            return {"exc": type(exc).__name__, "msg": str(exc)}
    return [{"text": a["source_clause"]["text"], "pol": a["risk_guard"]["polarity"]} for a in atoms]


out = {k: run(v) for k, v in CASES.items()}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
