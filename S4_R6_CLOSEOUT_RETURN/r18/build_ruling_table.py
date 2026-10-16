"""R18 — turn the independent audit into a per-row ruling table.

Input : r18/AUDIT_REQUIREMENTS.tsv  (produced by a read-only child agent; 115 rows)
Output: r18/REQUIREMENTS_RULING.tsv (one row per audit row + the explicitly declined options)

The ruling is an explicit, reviewable map -- not a heuristic. Every audit row gets exactly one
disposition, and every row whose disposition is "not closed" carries the reason it is not.
"""

from __future__ import annotations

import csv
import pathlib

R = pathlib.Path("C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/r18")
AUDIT = R / "AUDIT_REQUIREMENTS.tsv"
OUT = R / "REQUIREMENTS_RULING.tsv"

EXECUTED = {
    "DOC-LINK-TARGET": ("product + guard",
                        "docs/install/README.md:151 `](RELEASE_TUPLE.json)` -> `](../RELEASE_TUPLE.json)`; "
                        "guard gained check 6 (outgoing relative links must resolve at HEAD) with a paired "
                        "mutation; check 6 reports the defect on the pre-repair text and [] after"),
    "CHECKLIST-CURRENTNESS": ("evidence",
                              "TASK_CHECKLIST.md back-filled (residual `[ ]` = 0) and DETECTION_CHECKLIST.md "
                              "status/checker/candidate columns filled; both mirrored into the packet"),
    "SOURCE-INDEX": ("evidence", "r18/SOURCE_INDEX.json -- locator + sha256 for every contract-declared "
                               "source, the full KnowledgePack bundle and the DOC/PKG families; absences "
                               "carry an explicit SOURCE_GAP verdict"),
    "ECP-DEV": ("evidence", "r18/ECP_DEV.md -- named DEV execution-control-package reference edition"),
    "ECP-OPS": ("evidence", "r18/ECP_OPS.md -- named OPS execution-control-package reference edition"),
    "PACK-07": ("evidence", "S4_R6_CLOSEOUT_RETURN/checker_verdict.json re-bound to the FINAL candidate "
                            "127ec1c with the full dispatch history (4 dispatches) preserved; verdict PASS"),
    "EVIDENCE-HASH-INTEGRITY": ("evidence",
                                "local packet manifest recomputed recursively (28 entries) and verified "
                                "byte-identical to the published evidence-branch manifest; the one CRLF "
                                "divergence (R17_FULL_SUITE_FINAL.txt) normalised to LF"),
    "SOURCE-20KP": ("via SOURCE-INDEX", "KnowledgePack bundle enumerated: 20/20 files present and hashed"),
    "SOURCE-DOC-PKG": ("via SOURCE-INDEX", "blueprint DOC/PKG families enumerated with locator+sha256"),
    "REPORT-SOURCE-INVENTORY": ("via SOURCE-INDEX", "source inventory now machine-readable and complete"),
}

TICKETS = {
    "HGK-BINDING": ("TT-R18-02", "No ExecutionBinding scoped to the PIPD worktree exists; the canonical "
                                 "WorkOrders bind HGK worktrees and the task specs declare network=false "
                                 "while this round did push a branch. Repairing it requires a change in the "
                                 "control plane's own admission, which is not this round's write scope."),
    "HISTORICAL-RAW-CI": ("TT-R18-03", "The historical raw CI logs (624/6 and 108 focused) could not be "
                                       "frozen: the credential available to this round returns HTTP 401 for "
                                       "actions/jobs/<id>/logs. Recorded as SOURCE_GAP with the exact reason."),
    "REGRESSION-RAW": ("TT-R18-03", "The raw historical regression logs are the same credential-bound gap."),
    "REGRESSION-SECURITY-EDGES": ("TT-R18-01",
                                  "No dedicated mechanical negative test exists for 'a ninth skill' or "
                                  "'a cross-root modification'. The ZIP structure was measured (56 entries, "
                                  "8 SKILL.md, single root, no traversal) but a negative test would be new "
                                  "coverage, not a repair."),
    "RETRY-CHECKPOINT": ("TT-R18-01", "Retry/checkpoint coverage is part of the same new-coverage ticket."),
}

DECLINED = [
    ("R18-DECLINED-1", "REJECTED_OVER_ENGINEERING",
     "Put the round's evidence packet inside the product branch's write set",
     "Two independent reasons: the governed write-set gate exists precisely to keep round artifacts out of "
     "the product's own change surface, and amending it to admit them would relax a validator in order to "
     "pass. Doing that also destroys the gate's ability to detect a future round sneaking artifacts in."),
    ("R18-DECLINED-2", "REJECTED_OVER_ENGINEERING",
     "Add a new CI stage arm rather than a single named path amendment",
     "A new arm is new surface, new maintenance and a new self-test for one path. The measured failure was "
     "one product file outside a positive allowlist, so one named path with the planted-path self-test "
     "updated in the same commit was sufficient and is what the gate's own amendment rule prescribes."),
    ("R18-DECLINED-3", "REJECTED_OVER_ENGINEERING",
     "Rewrite or restructure the evidence packet to close PACK-01..08",
     "The audit's own reading is that the packet contents exist and are locatable; the residual is "
     "completeness of individual fields, not a defect a rewrite would fix. A rewrite would also invalidate "
     "every recorded digest for no verifiable gain."),
    ("R18-DECLINED-4", "REJECTED_OVER_ENGINEERING",
     "Re-order the VERIFY_SECURITY lane pool so rank-1 is not the writer's model",
     "The ordering is owner order (SOD006-C3, in force) and the round that measures a registry must not "
     "edit it. Separation of duties was obtained by pinning the arm by identity instead, which is recorded "
     "in the receipts."),
]


def main() -> int:
    rows = list(csv.DictReader(AUDIT.open(encoding="utf-8"), delimiter="\t"))
    out = []
    tally: dict[str, int] = {}

    def add(row_id, source, requirement, audit_status, disposition, action, closure_evidence, reason):
        out.append({
            "id": row_id,
            "source": source,
            "requirement": requirement,
            "audit_status": audit_status,
            "disposition_r18": disposition,
            "action_taken_or_required": action,
            "closure_evidence_locator": closure_evidence,
            "reason_if_not_closed": reason,
        })
        tally[disposition] = tally.get(disposition, 0) + 1

    for r in rows:
        rid, status = (r.get("id") or "").strip(), (r.get("status") or "").strip()
        if not rid:
            continue
        req = (r.get("requirement_verbatim_or_near") or "").strip()[:300]
        gap = (r.get("gap_or_observation") or "").strip()[:300]
        loc = (r.get("evidence_locator") or "").strip()[:200]
        if rid in EXECUTED:
            what, action = EXECUTED[rid]
            add(rid, "audit", req, status, "EXECUTED_R18", action, what, "")
        elif rid in TICKETS:
            tid, reason = TICKETS[rid]
            add(rid, "audit", req, status, f"DEFERRED_TICKET::{tid}", f"opened {tid}", loc, reason)
        elif status == "OWNER_GATE":
            add(rid, "audit", req, status, "OWNER_GATE", "recorded as an owner action", loc, gap)
        elif status == "NOT_APPLICABLE":
            add(rid, "audit", req, status, "NOT_APPLICABLE", "none", loc, gap)
        elif status == "DONE":
            add(rid, "audit", req, status, "ALREADY_SATISFIED", "none", loc, "")
        else:
            add(rid, "audit", req, status, "RECORDED_PARTIAL_UNCLOSED",
                "none taken this round", loc, gap or "audit recorded a partial state")

    for rid, disp, what, why in DECLINED:
        add(rid, "far-018 ruling", what, "N/A", disp, "deliberately not done", "", why)

    fields = list(out[0].keys())
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out)

    print("rows written:", len(out))
    for k in sorted(tally):
        print(f"  {k}: {tally[k]}")
    print("wrote:", OUT, OUT.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
