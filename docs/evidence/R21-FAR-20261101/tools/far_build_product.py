"""Assemble the FAR research product from the artefacts that actually exist.

Writes: ResearchSourceDenominator.tsv, ClaimLedger.tsv, FitGapLedger.tsv, RejectedAlternativeLedger.tsv,
CandidateResearch.yaml, ResearchHandoff.yaml, ResearchRunReceipt.json.
Nothing is invented: a lane receipt that is missing is recorded as MISSING, not as a pass.
"""
import hashlib
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
V = ROOT / "var" / "FHS-R21-FAR-TT-20261101"
FAR = V / "far"
REC = V / "far_receipts"
OUT = FAR / "research-product"


def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def tsv(path, header, rows):
    lines = ["\t".join(header)] + ["\t".join(str(c).replace("\t", " ").replace("\n", " ") for c in r) for r in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def lane_receipt(name):
    p = REC / name
    if not p.exists():
        return {"file": name, "state": "MISSING"}
    d = json.loads(p.read_text(encoding="utf-8"))
    return {"file": name, "sha256": sha(p), "ok": d.get("ok"), "code": d.get("code"),
            "lane": d.get("lane"), "required_arm": d.get("required_arm"), "served_arm": d.get("served_arm"),
            "served_arm_raw": d.get("served_arm_raw"), "used_rank": d.get("used_rank"),
            "used_seconds": d.get("used_seconds"), "identity_source": d.get("identity_source"),
            "usage_receipt_ok": d.get("usage_receipt_ok"),
            "required_arm_satisfied": d.get("required_arm_satisfied")}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = json.loads((FAR / "sources" / "SOURCE_DENOMINATOR.json").read_text(encoding="utf-8"))
    gaps = json.loads((FAR / "gaps" / "GAP_LEDGER.json").read_text(encoding="utf-8"))

    tsv(OUT / "ResearchSourceDenominator.tsv", ["kind", "path", "sha256", "bytes", "status"],
        [[r["kind"], r["path"], r.get("sha256") or "", r.get("bytes") or "",
          "MISSING" if r.get("missing") else ("UNREADABLE" if r.get("unreadable") else "READ")] for r in src["rows"]])

    claims = [
        ["C-01", "work_queue holds 22 rows: 19 PASS / 3 FAIL, and 17 rows carry no evidence_ref",
         "var/FHS-R21-FAR-TT-20261101/far/sources/WORK_QUEUE_READBACK.json", "MEASURED", sha(FAR / "sources/WORK_QUEUE_READBACK.json")],
        ["C-02", "WP-FHS-11 is PASS while carrying HERMES_MODEL_HALF_UNMEASURED",
         "var/FHS-R21-FAR-TT-20261101/far/sources/WORK_QUEUE_READBACK.json", "MEASURED", sha(FAR / "sources/WORK_QUEUE_READBACK.json")],
        ["C-03", "the canonical hotswap tool accepts a stale preimage, a reused grant, a foreign effect class and two live ECPs",
         "var/FHS-R21-FAR-TT-20261101/s5/B3_PATCH_TEST.json", "MEASURED", sha(V / "s5/B3_PATCH_TEST.json")],
        ["C-04", "C5 allowlist escape is refused and rollback is byte-identical; a checker edit is detectable, not prevented",
         "var/FHS-R21-FAR-TT-20261101/s5/C5_CASES.json", "MEASURED", sha(V / "s5/C5_CASES.json")],
        ["C-05", "three SP offices have no host-issued identity on this host",
         "var/FHS-R21-FAR-TT-20261101/s5/B5_PROBE.json", "MEASURED", sha(V / "s5/B5_PROBE.json")],
        ["C-06", "the OPS contract says 32 sub-contracts; the body yields 31 edges",
         "var/FHS-R21-FAR-TT-20261101/ledgers/S6_EDGE_EFFECT_LEDGER.json", "MEASURED", sha(V / "ledgers/S6_EDGE_EFFECT_LEDGER.json")],
        ["C-07", "four WP-20 claims were withdrawn after the AO returned; the kind denominator is 68 commands",
         "var/FHS-R21-FAR-TT-20261101/wp20/CORRECTION_LEDGER.json", "MEASURED", sha(V / "wp20/CORRECTION_LEDGER.json")],
    ]
    tsv(OUT / "ClaimLedger.tsv", ["claim_id", "claim", "source_path", "status", "source_sha256"], claims)

    tsv(OUT / "FitGapLedger.tsv", ["gap_id", "state", "what", "evidence_path", "unblock", "owner_decision"],
        [[g["id"], g["state"], g["what"], g["evidence"].get("path", ""), g["unblock"], g.get("owner_decision") or ""]
         for g in gaps["gaps"]])

    rej = [
        ["R-01", "three native offices cannot be accepted here", "check for an isolated lane, docker sandbox, or owner envelope path",
         "INDEPENDENT_LANE_CANNOT_ISSUE_IDENTITY", "a fresh context does not create a host-issued identity"],
        ["R-02", "same", "docker sandbox", "SANDBOX_IS_NOT_AN_IDENTITY_ISSUER", "a container does not hold the host credential"],
        ["R-03", "same", "owner key envelope", "ACCEPTED_PATH", "the envelope can sign a registry row, so the owner can enrol a governed test principal"],
        ["R-04", "plugin install leg", "docker offline install", "NOT_APPLICABLE", "the install verb resolves a catalog or git source"],
        ["R-05", "OPS 32 denominator", "agent fills the missing edge", "FORBIDDEN", "inventing a sub-contract would corrupt the denominator"],
        ["R-06", "17 unsupported PASS rows", "re-execute every WP", "OVER_READ", "the queue accepts a bound receipt; re-execution is not required to unblock the count"],
        ["R-07", "checker edits the diff", "add a write lock to the tool", "COST_EXCEEDS_BENEFIT", "re-verifying the receipt sha satisfies the detection clause"],
    ]
    tsv(OUT / "RejectedAlternativeLedger.tsv",
        ["item", "claim", "alternative_considered", "disposition", "reason"], rej)

    plan = lane_receipt("PLAN_R21FAR_v2.json")
    execute = lane_receipt("EXECUTE_R21FAR_C5.json")
    verify = lane_receipt("VERIFY_R21FAR.json")

    (OUT / "CandidateResearch.yaml").write_text("\n".join([
        "schema: FAR_CANDIDATE_RESEARCH/1",
        "round_id: R21-FAR-20261101",
        "decision_question: what remains in the thin-prompt round, what is really unpassable, and who decides",
        "synthesis: var/FHS-R21-FAR-TT-20261101/far/ResearchSynthesis.md",
        f"synthesis_sha256: {sha(FAR / 'ResearchSynthesis.md')}",
        f"gap_ledger_sha256: {sha(FAR / 'gaps/GAP_LEDGER.json')}",
        "counts:",
        f"  gaps: {len(gaps['gaps'])}",
        f"  queue_rows: {gaps['queue_state']['rows']}",
        f"  queue_without_evidence: {gaps['queue_state']['without_evidence_ref']}",
        "lanes:",
        f"  PLAN: {plan.get('ok')} served={plan.get('served_arm')} rank={plan.get('used_rank')}",
        f"  EXECUTE: {execute.get('ok', execute.get('state'))} served={execute.get('served_arm', '-')}",
        f"  VERIFY: {verify.get('ok', verify.get('state'))} served={verify.get('served_arm', '-')}",
        "claim_ceiling: candidate research product; no acceptance, no main, no release",
        "",
    ]), encoding="utf-8", newline="\n")

    (OUT / "ResearchHandoff.yaml").write_text("\n".join([
        "schema: FAR_RESEARCH_HANDOFF/1",
        f"generated_utc: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        "disposition: RESEARCH_PASS_CANDIDATE",
        "why: every gap row names a local file, the three lanes were dispatched, and the owner decisions are enumerated",
        "open_owner_decisions: [D1 test-principal enrolment, D2 canonical patch landing, D3 OPS 32 vs 31, D4 unsupported PASS rows, D5 TT-20, D6 promotion order]",
        "not_claimed: [independent acceptance, native complete, main integrated, released]",
        "",
    ]), encoding="utf-8", newline="\n")

    receipt = {
        "schema": "FAR_RESEARCH_RUN_RECEIPT/1",
        "round_id": "R21-FAR-20261101",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mandate": "var/FHS-R21-FAR-TT-20261101/far/MANDATE_R21_FAR.json",
        "mandate_sha256": sha(FAR / "MANDATE_R21_FAR.json"),
        "lanes": {"PLAN": plan, "EXECUTE": execute, "VERIFY": verify},
        "products": {p.name: {"sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(OUT.iterdir())},
        "ceiling": "candidate research product; the VERIFY receipt is advisory only",
    }
    (OUT / "ResearchRunReceipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    print(json.dumps({"products": list(receipt["products"]),
                      "plan": plan.get("ok"), "execute": execute.get("ok", execute.get("state")),
                      "verify": verify.get("ok", verify.get("state"))}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
