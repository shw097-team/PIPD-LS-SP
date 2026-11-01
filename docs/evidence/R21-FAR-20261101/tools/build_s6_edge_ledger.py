"""Build the per-Edge effect ledger from 10B, so the OPS denominator stops being a rumour.

The contract says "OPS ECP 32 sub-contracts". No body document states that number (S5_S7_INVENTORY.json
records NOT_LOCATED), so the OPS set is derived here the only way it can be: one row per EDGE section that
declares a HOST_OP effect. Every row carries the doc line it came from, so the count can be re-derived.
"""
import json
import pathlib
import re
import time

BODY = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric"
                    r"\FHS\FHS-MSC\FHS-MSC_PIPD-LS-PKG"
                    r"\FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1\01_FHS-MSC_PIPD-LS-PKG_BODY")
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\ledgers")
SRC = "10B_B1_PI27_PD31.md"


def main():
    lines = (BODY / SRC).read_text(encoding="utf-8", errors="replace").splitlines()
    edges = []
    cur = None
    for i, l in enumerate(lines, 1):
        m = re.match(r"####\s+(EDGE-[A-Z]+-B1-[A-Z0-9-]+)\s*$", l.strip())
        if m:
            cur = {"edge": m.group(1), "line": i, "atom": None, "pd": None, "domain": None,
                   "effect_raw": None, "effect_class": None, "ecp": None, "tqaep": [], "first_fail": None}
            edges.append(cur)
            continue
        if cur is None:
            continue
        t = l.strip()
        m = re.search(r"PI-(B1-[A-Z]\d+)\s*→\s*(PD-\d{2})/", t)
        if m:
            cur["atom"], cur["pd"] = m.group(1), m.group(2)
        m = re.search(r"domain=([A-Z_]+)", t)
        if m:
            cur["domain"] = m.group(1)
        if t.startswith("- effect/ECP"):
            cur["effect_raw"] = t
            if "HOST_OPERATIONS" in t or "HOST_OP" in t:
                cur["effect_class"] = "OPS"
            elif "REPO_WRITE" in t:
                cur["effect_class"] = "DEV"
            elif "USER" in t:
                cur["effect_class"] = "USER"
            elif "OBS" in t or "READ_ONLY" in t:
                cur["effect_class"] = "OBS"
            if cur["effect_class"] is None:
                for suf, cls in (("-OPS", "OPS"), ("-DEV", "DEV"), ("-USER", "USER")):
                    if cur["edge"].endswith(suf):
                        cur["effect_class"] = cls
            cur["ecp"] = "OPS ECP" if "OPS ECP" in t else ("DEV ECP" if "DEV ECP" in t else None)
        if t.startswith("- TQAEP"):
            cur["tqaep"] = re.findall(r"TQ-[A-Z0-9-]+", t)
        if t.startswith("- first_fail"):
            cur["first_fail"] = t.split("：", 1)[-1][:120]

    counts = {}
    for e in edges:
        counts[e["effect_class"] or "UNCLASSIFIED"] = counts.get(e["effect_class"] or "UNCLASSIFIED", 0) + 1
    unclassified = [e["edge"] for e in edges if not e["effect_class"]]
    ops = [e for e in edges if e["effect_class"] == "OPS"]

    doc = {
        "schema": "FHS.R21.S6.EDGE_EFFECT_LEDGER/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": {"file": SRC, "edges_found": len(edges)},
        "effect_counts": counts,
        "ops_denominator": {
            "derived_ops_edges": len(ops),
            "contract_claim": 32,
            "match": len(ops) == 32,
            "note": ("derived from the EDGE sections themselves: every edge whose effect/ECP line names "
                     "HOST_OPERATIONS is an OPS sub-contract; the contract's 32 is neither confirmed nor "
                     "borrowed -- this number is what the body actually declares"),
        },
        "unclassified_edges": unclassified,
        "edges": edges,
    }
    (OUT / "S6_EDGE_EFFECT_LEDGER.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8", newline="\n")
    with open(OUT / "S6_EDGE_EFFECT_LEDGER.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("edge\tatom\tpd\tdomain\teffect_class\tecp\ttqaep\tfirst_fail\tanchor\n")
        for e in edges:
            f.write("\t".join([e["edge"], e["atom"] or "", e["pd"] or "", e["domain"] or "",
                               e["effect_class"] or "UNCLASSIFIED", e["ecp"] or "",
                               ",".join(e["tqaep"]), (e["first_fail"] or "").replace("\t", " "),
                               f"{SRC}#L{e['line']}"] ) + "\n")
    print(json.dumps({"edges": len(edges), "counts": counts, "ops_derived": len(ops),
                      "unclassified": len(unclassified)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
