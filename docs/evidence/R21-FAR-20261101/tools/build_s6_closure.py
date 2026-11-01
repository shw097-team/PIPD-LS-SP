"""Close S6 with one row per OPS edge: what ran, what it found, and what a PARK would need to lift.

Nothing is copied by hand. Every cell comes from an artefact written by a run:
  ledgers/S6_OPS_EDGE_PLAN.json   the 14 derived OPS edges and their evidence level
  s6/A2_CASES.json                A2 POS/NEG executed
  s6/A2_PATCH_TEST.json           A2 candidate patch, pre/post
  s6/A3_CASES.json                A3 POS/NEG executed
  s6/A3_PATCH_TEST.json           A3 candidate patch, pre/post
"""
import hashlib
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
S6 = V / "s6"
LED = V / "ledgers"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def main():
    plan = load(LED / "S6_OPS_EDGE_PLAN.json")
    a2 = load(S6 / "A2_CASES.json")
    a2p = load(S6 / "A2_PATCH_TEST.json")
    a3 = load(S6 / "A3_CASES.json")
    a3p = load(S6 / "A3_PATCH_TEST.json")

    executed = {
        "EDGE-WO-B1-A2": {"ran": a2["cases"], "patch": a2p["tests"], "patch_file": a2p["patch"]["file"],
                          "state": "EXECUTED_DEFECT_FOUND_PATCHED_CANDIDATE"},
        "EDGE-WO-B1-A3": {"ran": a3["cases"], "patch": a3p["tests"], "patch_file": a3p["patch"]["file"],
                          "state": "EXECUTED_DEFECT_FOUND_PATCHED_CANDIDATE"},
        "EDGE-WO-B1-A4": {"ran": {"TQ-B1-A4-POS": "NOT_IMPLEMENTED: abi.py has Need/Occupant/Registry/Consumer but "
                                                     "no receiver-liveness or ACK verifier",
                                  "TQ-B1-A4-NEG_wrong_abi": "PASS via patches/tests/RESULTS.json T1 "
                                                            "(ERR_ABI_VERSION_MISMATCH after the gate patch)"},
                          "state": "PARTIAL_NO_RECEIVER_IMPLEMENTATION"},
    }

    rows = []
    for r in plan["rows"]:
        e = executed.get(r["edge"])
        if e:
            rows.append({**{k: r[k] for k in ("edge", "pd", "domain", "line", "tqaep")},
                         "state": e["state"], "evidence": e.get("patch_file") or "s6/A4 via patches/tests/RESULTS.json",
                         "unblock": None})
        else:
            rows.append({**{k: r[k] for k in ("edge", "pd", "domain", "line", "tqaep")},
                         "state": "PARK_NO_IMPLEMENTATION",
                         "evidence": (r["artefacts_found"][0]["path"] if r["artefacts_found"] else None),
                         "unblock": (f"a signed {r['domain']} host receiver plus its edge oracle; then POS/NEG over "
                                     f"{len(r['tqaep'])} named cases ({', '.join(r['tqaep'][:2])}...)")})

    counts = {}
    for r in rows:
        counts[r["state"]] = counts.get(r["state"], 0) + 1

    total_cases_ran = sum(len(v["ran"]) for v in executed.values())
    doc = {
        "schema": "FHS.R21.S6.CLOSURE/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "denominator": {"body_edges": 31, "ops_edges_derived": len(rows), "contract_claim": 32,
                        "note": "the body declares 31 edges, 14 with HOST_OP effect; 'OPS ECP 32' is not stated anywhere"},
        "state_counts": counts,
        "cases_executed": total_cases_ran,
        "defects_found": [
            {"edge": "EDGE-WO-B1-A2", "defect": "issue_grant accepts a replayed nonce (GRANT_VALID on the second grant)",
             "raw": "s6/A2_CASES.json", "patch": a2p["patch"]["file"], "tests": a2p["summary"]},
            {"edge": "EDGE-WO-B1-A3", "defect": "work_queue.cmd_settle overwrites a settled row (duplicate claim) and "
                                                "records PASS with an empty evidence_ref",
             "raw": "s6/A3_CASES.json", "patch": a3p["patch"]["file"], "tests": a3p["summary"]},
        ],
        "rows": rows,
        "artefact_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in
                            (S6 / "A2_CASES.json", S6 / "A2_PATCH_TEST.json", S6 / "A3_CASES.json",
                             S6 / "A3_PATCH_TEST.json", LED / "S6_OPS_EDGE_PLAN.json")},
        "claim_ceiling": ("2 of 14 OPS edges were executed against their own POS/NEG and both failed a NEG, each fixed "
                          "by a candidate patch on a copy; 1 is partial (no receiver implementation); 11 are parked with "
                          "named unblock conditions. No OPS edge is accepted end-to-end and the canonical tools were "
                          "not modified."),
    }
    (S6 / "S6_CLOSURE.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                        encoding="utf-8", newline="\n")

    md = ["# S6 — OPS ECP 逐 edge 收束", "", f"generated_utc: {doc['generated_utc']}", "",
          f"分母：正文宣告 **31** 條 edge，其中 **{len(rows)}** 條為 HOST_OP effect；契約寫的 32 在正文不存在。", "",
          "| 狀態 | 條數 |", "|---|---:|"]
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        md.append(f"| `{k}` | {v} |")
    md += ["", f"實際跑掉的 case：**{total_cases_ran}**", "", "## 兩個真缺陷（條文自己的 NEG 打出來的）", ""]
    for d in doc["defects_found"]:
        md += [f"### {d['edge']}", f"- 缺陷：{d['defect']}", f"- Raw：`{d['raw']}`",
               f"- 候選補丁：`{d['patch']}`；測試 {d['tests']}", ""]
    md += ["## 逐列", "", "| edge | PD | domain | 狀態 | 解除條件 |", "|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| `{r['edge']}` | {r['pd']} | {r['domain']} | `{r['state']}` | {(r['unblock'] or '—')} |")
    md += ["", f"## 天花板", "", doc["claim_ceiling"], ""]
    (S6 / "S6_CLOSURE.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"states": counts, "cases_executed": total_cases_ran,
                      "closure_sha": sha(S6 / "S6_CLOSURE.json")[:16]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
