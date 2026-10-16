"""R18 — build SOURCE_INDEX.json.

Audit row `SOURCE-INDEX` (NOT_DONE): no complete locator/SHA/read inventory covering all required
KP / DOC / PKG sources. This builds it from the R6 compiler contract's own `authority.sources`
(so the index cannot drift from the contract), then enumerates the full KnowledgePack bundle and the
upstream blueprint DOC/PKG families, hashing what exists and marking what does not as SOURCE_GAP.

Read-only with respect to every source: nothing outside r18/SOURCE_INDEX.json is written.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from datetime import datetime, timezone

R = pathlib.Path("C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016")
CONTRACT = R / "compiler/PIPD-S4R6-CLOSEOUT-CONTRACT.json"
BP = pathlib.Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD")
KP = pathlib.Path(
    "C:/Projects/Agent_Workspace/知識庫/工程基座/"
    "GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack"
)


def sha256_of(p: pathlib.Path) -> str | None:
    try:
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def entry(idx_id: str, path: pathlib.Path, *, family: str, rank: str | None = None) -> dict:
    exists = path.is_file()
    rec: dict = {
        "id": idx_id,
        "family": family,
        "locator": str(path).replace("\\", "/"),
        "exists": exists,
    }
    if rank:
        rec["rank"] = rank
    if exists:
        rec["bytes"] = path.stat().st_size
        rec["sha256"] = sha256_of(path)
        rec["verdict"] = "PRESENT"
    else:
        rec["sha256"] = None
        rec["verdict"] = "SOURCE_GAP"
        rec["gap_reason"] = "locator does not resolve to a regular file at index time"
    return rec


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    authority = contract.get("authority", {})
    entries: list[dict] = []

    # 1. The contract's own declared sources (cannot drift from the contract).
    for s in authority.get("sources", []):
        p = pathlib.Path(s["path"])
        rec = entry(s["id"], p, family="CONTRACT_DECLARED", rank=s.get("rank"))
        declared = s.get("sha256")
        if declared:
            rec["sha256_declared_in_contract"] = declared
            rec["sha256_matches_contract"] = (declared == rec.get("sha256"))
        entries.append(rec)

    # 2. KnowledgePack bundle — full enumeration (the audit expects the whole 20-document set).
    kp_files = sorted(p for p in KP.glob("*") if p.is_file()) if KP.is_dir() else []
    for p in kp_files:
        entries.append(entry(f"KP::{p.name}", p, family="GPTB_KNOWLEDGE_PACK"))
    kp_expected_20 = len(entries) >= 0  # recorded below as a measured fact, never asserted

    # 3. Upstream blueprint DOC-00..09 and PKG-00..10 families.
    for fam, pats in (("BLUEPRINT_DOC", "PIPD_LS_DOC-*"), ("BLUEPRINT_PKG", "PIPD_LS_PKG-*")):
        d = BP / "PIPD_LS"
        found = sorted(p for p in d.glob(pats) if p.is_file()) if d.is_dir() else []
        for i, p in enumerate(found):
            entries.append(entry(f"{fam}::{i + 1:02d}::{p.name}", p, family=fam))
        if not found:
            entries.append(
                {
                    "id": f"{fam}::<family>",
                    "family": fam,
                    "locator": str(d).replace("\\", "/"),
                    "exists": False,
                    "sha256": None,
                    "verdict": "SOURCE_GAP",
                    "gap_reason": "no file in this family resolved at index time",
                }
            )

    # 4. Gaps that are not a missing file but a credential/authority limit, recorded with the reason.
    entries.append(
        {
            "id": "HISTORICAL_RAW_CI::624_108",
            "family": "HISTORICAL_EVIDENCE",
            "locator": "GitHub API /repos/shw097-team/PIPD-LS-SP/actions/jobs/<job_id>/logs",
            "exists": False,
            "sha256": None,
            "verdict": "SOURCE_GAP",
            "gap_reason": "credential bound to this round returns HTTP 401 for job-log download; "
            "the run/job identifiers are known but the raw logs could not be frozen locally",
            "audit_row": "HISTORICAL-RAW-CI",
            "ticket": "TT-R18-03",
        }
    )

    missing_declared = [e for e in entries if e["family"] == "CONTRACT_DECLARED" and not e["exists"]]
    doc = {
        "_what": "Complete locator/SHA/read inventory of every source the round's contract declares as "
        "authority, plus the full KnowledgePack bundle and the upstream blueprint DOC/PKG families.",
        "_why": "Closes audit row SOURCE-INDEX (NOT_DONE): a verifier must be able to walk every source "
        "without reconstructing the compiler contract by hand.",
        "_generated_from": {
            "contract": str(CONTRACT).replace("\\", "/"),
            "contract_sources_count": len(authority.get("sources", [])),
            "knowledgepack_dir": str(KP).replace("\\", "/"),
            "blueprint_dir": str(BP).replace("\\", "/"),
        },
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": {
            "entries": len(entries),
            "present": sum(1 for e in entries if e["verdict"] == "PRESENT"),
            "source_gap": sum(1 for e in entries if e["verdict"] == "SOURCE_GAP"),
            "contract_declared": sum(1 for e in entries if e["family"] == "CONTRACT_DECLARED"),
            "contract_declared_missing": len(missing_declared),
            "knowledgepack_files": len(kp_files),
        },
        "contract_conflicts": authority.get("conflicts", []),
        "contract_missing_sources": authority.get("missing_sources", []),
        "native_control_plane_ids": authority.get("native_control_plane_ids", []),
        "current_control_plane_id": authority.get("current_control_plane_id"),
        "entries": entries,
        "claim_ceiling": "A PRESENT verdict means the locator resolved to a regular file and its sha256 "
        "was computed at generation time. It does NOT mean the file's content was read, endorsed or "
        "authoritative in this round. A SOURCE_GAP is an explicit absence, not a silent omission.",
        "self_binding": "git-blob",
    }

    out = R / "r18/SOURCE_INDEX.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(doc["counts"], ensure_ascii=False, indent=2))
    print("contract_declared_missing:", [e["id"] for e in missing_declared])
    print("wrote:", out, out.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
