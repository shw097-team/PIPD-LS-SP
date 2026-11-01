"""Build the S5/S6/S7 identity inventory from the governing body, with file#line anchors.

Nothing here decides acceptance. It answers one narrow question the contract keeps asking and I kept
answering from memory: how many IDs does the governing body actually enumerate, and where.

Extracted:
  * PIPD lifecycle transitions E3 (PD->DEV), E4 (PD->OPS), E5 (PD->PlannedTQAEP)
  * PD-01..PD-NN slots with their effect class as written in 10B
  * the TQAEP case registry (the "282" claim) by counting `原 Case/SHA` rows in 10A
  * the TQ-B1-* family ids
  * a named record for the "OPS ECP 32 sub-contracts" denominator, which no document I read states
"""
import hashlib
import json
import os
import pathlib
import re
import time

BODY = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric"
                    r"\FHS\FHS-MSC\FHS-MSC_PIPD-LS-PKG"
                    r"\FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1\01_FHS-MSC_PIPD-LS-PKG_BODY")
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\ledgers")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lines(name):
    with open(BODY / name, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    anchors = {}
    for name in ("00_INDEX_AND_DECISION.md", "02_PIPD_LIFECYCLE_AND_TPM.md", "03_ARCHITECTURE_ABI_AND_EFFECT.md",
                 "10A_B1_TQAEP_120_124_38.md", "10B_B1_PI27_PD31.md", "11_WORKPACKAGES_AND_DAG.md"):
        anchors[name] = {"bytes": (BODY / name).stat().st_size, "sha256": sha(BODY / name)}

    # --- E3/E4/E5 live in 02_PIPD_LIFECYCLE_AND_TPM.md -------------------------------------
    ecp = []
    for i, l in enumerate(lines("02_PIPD_LIFECYCLE_AND_TPM.md"), 1):
        if re.search(r"E[345]\s*`PD→", l) or re.search(r"DEV ECP|OPS ECP|PlannedTQAEP", l):
            if re.search(r"E[1-9]\s*`", l):
                ecp.append({"line": i, "text": l.strip()[:220]})

    # --- PD slots and their effect class ---------------------------------------------------
    d10b = lines("10B_B1_PI27_PD31.md")
    pds = {}
    for i, l in enumerate(d10b, 1):
        for m in re.finditer(r"\bPD-(\d{2})\b", l):
            pid = f"PD-{m.group(1)}"
            pds.setdefault(pid, {"id": pid, "first_line": i, "effect_class": None, "atoms": set()})
            for cls in ("OBS", "DEV", "OPS", "USER"):
                if re.search(rf"\b{cls}\b", l):
                    pds[pid]["effect_class"] = pds[pid]["effect_class"] or cls
            for a in re.findall(r"\bA(\d{1,2})\b", l):
                pds[pid]["atoms"].add(f"A{a}")

    # --- the TQAEP registry: count and name the cases 10A actually lists -------------------
    d10a = lines("10A_B1_TQAEP_120_124_38.md")
    case_rows = []
    for i, l in enumerate(d10a, 1):
        m = re.search(r"原 Case/SHA[^`]*`([^`]+)`\s*/\s*`([0-9a-f]{64})`", l)
        if m:
            case_rows.append({"case": m.group(1), "case_sha256": m.group(2), "line": i})
        else:
            m2 = re.search(r"-\s*\*\*原 Case/SHA\*\*[：:]\s*`([^`]+)`", l)
            if m2:
                case_rows.append({"case": m2.group(1), "case_sha256": None, "line": i})
    fam = sorted({c["case"].split("-")[2] if len(c["case"].split("-")) > 2 else c["case"] for c in case_rows})
    registry_header = next((i for i, l in enumerate(d10a, 1) if "282" in l and "Registry" in l), None)

    # --- the "OPS ECP 32" denominator: search every body file, record what exists ----------
    mentions = []
    for name in sorted(p.name for p in BODY.glob("*.md")):
        for i, l in enumerate(lines(name), 1):
            if re.search(r"(32\s*(個|份|項)\s*(OPS|子契約)|OPS[^。\n]{0,12}32\s*個)", l):
                mentions.append({"file": name, "line": i, "text": l.strip()[:200]})

    ledger = {
        "schema": "FHS.R21.S5_S7.INVENTORY/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "body_dir": str(BODY),
        "anchors": anchors,
        "ecp_transitions": ecp,
        "pd_slots": [{"id": v["id"], "first_line": v["first_line"], "effect_class": v["effect_class"],
                      "atoms": sorted(v["atoms"])[:6]} for v in sorted(pds.values(), key=lambda x: x["id"])],
        "pd_slot_count": len(pds),
        "tqaep": {"registry_header_line": registry_header,
                  "cases_named": len(case_rows),
                  "with_case_sha": sum(1 for c in case_rows if c["case_sha256"]),
                  "families": fam[:20],
                  "first_three": case_rows[:3]},
        "ops_32_denominator": {
            "status": "NOT_LOCATED" if not mentions else "LOCATED",
            "evidence": mentions,
            "candidates": ["31 PD slots split OBS/DEV/OPS/USER (10B_B1_PI27_PD31.md#L16)",
                           "31 B1 Edge + 282 Case (12_VERIFICATION_AND_DELIVERY.md#L117)",
                           "27 B1 atoms x effect classes"],
            "rule": "the contract's '32 sub-contracts' is not stated by any body document I read; the OPS subset must be derived per PD slot, not assumed"},
    }
    (OUT / "S5_S7_INVENTORY.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=1) + "\n",
                                              encoding="utf-8", newline="\n")
    with open(OUT / "S5_S7_INVENTORY.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("kind\tid\tanchor\tnote\n")
        for e in ecp:
            f.write(f"ECP\t{e['text'].split()[0]}\t02_PIPD_LIFECYCLE_AND_TPM.md#L{e['line']}\t{e['text'][:90]}\n")
        for v in ledger["pd_slots"]:
            f.write(f"PD\t{v['id']}\t10B_B1_PI27_PD31.md#L{v['first_line']}\teffect={v['effect_class']}\n")
        for c in case_rows[:282]:
            f.write(f"TQAEP_CASE\t{c['case']}\t10A_B1_TQAEP_120_124_38.md#L{c['line']}\tsha={c['case_sha256'] or 'MISSING'}\n")
    print(json.dumps({"ecp_rows": len(ecp), "pd_slots": len(pds), "tqaep_cases_named": len(case_rows),
                      "tqaep_with_sha": sum(1 for c in case_rows if c["case_sha256"]),
                      "ops32": ledger["ops_32_denominator"]["status"],
                      "families": fam[:8]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
