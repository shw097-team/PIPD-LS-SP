#!/usr/bin/env python3
"""Produce this session's closure-and-handover artifacts MECHANICALLY.

Alignment premise: the governing corpus at
知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_PIPD-PKG, specifically
  * PKG-01 3.1/3.2 - adjacent-only transitions, side states TEMP_CLOSED/SUPERSEDED/INVALIDATED, and the
    rule that EXTERNAL gates need actual target-scoped checker-observed evidence rather than
    `expected-evidence://`;
  * PKG-06 DOC-05 - TT route OPEN->ASSIGNED->PATCHED->CHECK_PENDING->CLOSED "only with owner+checker
    evidence", first failure TT_CLOSURE_WITHOUT_CHECKER;
  * PKG-09 DOC-01 - supersession needs old_id/new_id/old_hash/new_hash/supersession_ref and the hard
    invariant old_hash != new_hash && predecessor_matches;
  * PKG-09 DOC-03 - affected-only invalidation: affected == semantic_reverse_closure and
    untouched_not_invalidated, conservative when there is no output delta;
  * PKG-06 DOC-04 - evidence envelope inputs source_file/sha256/version/exact_anchor/observed_at/
    supersedes_hash plus subject/env/epoch/freshness;
  * PKG-10 0.6 - P0-P2 can never be promoted to P3-P5 by text; SELF_PROMOTION_OR_SPLIT_BRAIN blocks;
    PI_READY != PREDEV_READY != EXECUTION_ADMITTED != OPERATIONAL_ACCEPTED != PRODUCTION_PASS.

Nothing here promotes anything. The script MEASURES the session's state and writes what a receiver would
need. Where a normative input is absent (no external qualification issuer, no ADMIT receipt) it records
AWAITING_EXTERNAL rather than an inferred value, because No-Auto-Approval forbids the alternative.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROUND_REL = ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
PRIOR_HEADS = [
    ("5310896e706e01a9cdb0123285bccec75086bcb8", "759b9f0dc880b2f960363b2ceaa68446c770061d",
     "fix/s4r3-stage-a-ci-truthfulness-20261013",
     "F1 remedy edited the gate file, which lives on both branches; Stage A advanced by that one commit"),
    ("35a68f0c05a26747c2a1553cb86505ac26909b88", "46ae548311e7f38d520d4fe98df276d15867939d",
     "feat/s4r3-stageb-successor-20261013",
     "Stage B re-stacked onto the new Stage A head by merge so merge-base(A,B) == A head again"),
    ("46ae548311e7f38d520d4fe98df276d15867939d", "1f94f834897452f52deb74049e8f4efc7dadc4ad",
     "feat/s4r3-stageb-successor-20261013",
     "round evidence, remedy receipts, lane verdicts and the updated handover pack committed"),
]


def sh(*a: str, cwd: str | None = None) -> str:
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    b_root = pathlib.Path(sys.argv[1])
    a_root = pathlib.Path(sys.argv[2])
    out_dir = b_root / ROUND_REL / "evidence/12_GATES"
    out_dir.mkdir(parents=True, exist_ok=True)
    head_a, head_b = sh("git", "-C", str(a_root), "rev-parse", "HEAD"), sh("git", "-C", str(b_root), "rev-parse", "HEAD")
    now = dt.datetime.now(dt.timezone.utc).isoformat()

    # --- 1. supersession ledger (PKG-09 DOC-01 shape) ---------------------------------------------
    sup = []
    for old, new, ref, why in PRIOR_HEADS:
        def resolve(sha: str) -> bool:
            return subprocess.run(["git", "-C", str(b_root), "cat-file", "-e", f"{sha}^{{commit}}"],
                                  capture_output=True).returncode == 0
        old_present, new_present = resolve(old), resolve(new)
        anc = subprocess.run(["git", "-C", str(b_root), "merge-base", "--is-ancestor", old, new],
                             capture_output=True).returncode == 0
        sup.append({
            "old_id": ref, "new_id": ref, "old_hash": old, "new_hash": new,
            "supersession_ref": f"{ref}@{old[:12]}->{new[:12]}",
            "old_hash_present_in_repo": old_present, "new_hash_present_in_repo": new_present,
            "predecessor_matches": anc,
            "invariant": "old_hash != new_hash && predecessor_matches && identity_reuse_not_repurposed",
            "invariant_holds": bool(old != new and anc and old_present and new_present),
            "reason": why, "lineage_fork": False,
            "receipt_required": "explicit owner/consumer receipt per PKG-09 DOC-01; absent -> HOLD and TT",
            "receipt_state": "AWAITING_EXTERNAL"})
    (out_dir / "SUPERSESSION_LEDGER.json").write_text(json.dumps(
        {"schema": "CLOSURE-SUPERSESSION-LEDGER/1", "observed_at": now,
         "current_heads": {"stage_a": head_a, "stage_b": head_b}, "entries": sup,
         "note": "derived from git ancestry, not from prose; a same-hash entry would be an editorial "
                 "no-op and is not listed"}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # --- 2. affected-only invalidation (PKG-09 DOC-03 shape) ---------------------------------------
    # The governed graph edge is: an artifact that cites a revision is affected when that revision is
    # superseded. Impact is computed from the citations actually present in this round's own records.
    ledger_dirs = [b_root / ROUND_REL / "far-study", b_root / ROUND_REL / "evidence/12_GATES"]
    superseded_nodes = {h for old, _, _, _ in PRIOR_HEADS for h in (old, old[:7])}
    current_nodes = {h for h in (head_a, head_b) for h in (h, h[:7])}
    cited: dict[str, list[str]] = {}
    for d in ledger_dirs:
        for p in list(d.rglob("*.md")) + list(d.rglob("*.json")) + list(d.rglob("*.txt")) + list(d.rglob("*.log")):
            if p.stat().st_size > 2_000_000:
                continue
            t = p.read_text(encoding="utf-8", errors="replace")
            hit_sup = sorted({n for n in superseded_nodes if n in t})
            hit_cur = sorted({n for n in current_nodes if n in t})
            if hit_sup or hit_cur:
                cited[p.relative_to(b_root).as_posix()] = hit_sup + [f"CURRENT:{c}" for c in hit_cur]
    # The denominator: a partition claim is unverifiable without the full inventory it partitions.
    scanned, skipped_too_large, not_cited = [], [], []
    for d in ledger_dirs:
        for p in sorted(list(d.rglob("*.md")) + list(d.rglob("*.json")) + list(d.rglob("*.txt"))
                        + list(d.rglob("*.log"))):
            rel = p.relative_to(b_root).as_posix()
            if p.stat().st_size > 2_000_000:
                skipped_too_large.append(rel)
            elif rel not in cited:
                not_cited.append(rel)
            else:
                scanned.append(rel)
    affected, untouched = [], []
    for rel, marks in sorted(cited.items()):
        sup_marks = [m for m in marks if not m.startswith("CURRENT:")]
        row = {"artifact": rel, "cites_superseded": sup_marks,
               "cites_current": [m.split(":", 1)[1] for m in marks if m.startswith("CURRENT:")]}
        (affected if sup_marks else untouched).append(row)
    payload = {
        "schema": "CLOSURE-AFFECTED-ONLY-INVALIDATION/1", "observed_at": now,
        "invariant": "affected == semantic_reverse_closure && untouched_not_invalidated && graph_consistent",
        "graph_edge": "artifact -> revision it cites (edge exists when the artifact text names the sha)",
        "current_heads": {"stage_a": head_a, "stage_b": head_b},
        "superseded_nodes": [{"rev": o, "head_short": o[:7]} for o, _, _, _ in PRIOR_HEADS],
        "affected_count": len(affected), "untouched_count": len(untouched),
        "affected": affected,
        "disposition": "MARKED_SUPERSEDED_AFFECTED_ONLY - never deleted (No-Silent-Loss); a claim carried "
                       "forward must be re-established at the current head, not inherited",
        "conservative_rule_applied": "no output-delta proof exists for these artifacts, so they are "
                                     "invalidated rather than assumed still-current",
        "self_reference_note": "this ledger and the supersession ledger necessarily NAME the superseded "
                               "revisions, so they cite themselves as affected. That is the same class of "
                               "self-reference the round removed from the write-set allowlist, and it is "
                               "declared here rather than hidden: an invalidation ledger that could not "
                               "name what it invalidated would be useless.",
        "untouched": untouched,
        "denominator": {
            "total_files_seen_by_the_scanner": len(scanned) + len(not_cited) + len(skipped_too_large),
            "partition_level_1": {"cited_some_head": len(scanned),
                                  "cited_no_head_at_all": len(not_cited),
                                  "skipped_too_large": len(skipped_too_large)},
            "partition_level_2_within_cited": {"affected": len(affected), "untouched": len(untouched)},
            "reconciles": (len(scanned) + len(not_cited) + len(skipped_too_large)
                           == len(affected) + len(untouched) + len(not_cited) + len(skipped_too_large)),
            "partition_is_exhaustive": (len(affected) + len(untouched)) == len(scanned),
            "cited_a_superseded_revision": len(affected),
            "cited_only_a_current_head": len(untouched),
            "cited_no_head_at_all": not_cited,
            "skipped_too_large_hash_scanner": skipped_too_large,
            "note": "the three sets above partition every file the scanner saw; a file that names no head "
                    "appears in cited_no_head_at_all rather than being silently absent, so the counts can "
                    "be re-derived and checked against the tree",
        },
    }
    (out_dir / "AFFECTED_ONLY_INVALIDATION.json").write_text(
        json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # --- 3. evidence envelope (PKG-06 DOC-04 shape) ------------------------------------------------
    envs = []
    for d in ledger_dirs + [b_root / ROUND_REL]:
        for p in sorted(d.glob("*")):
            if not p.is_file() or p.stat().st_size > 2_000_000:
                continue
            b = p.read_bytes()
            rel = p.relative_to(b_root).as_posix()
            prev = sh("git", "-C", str(b_root), "show", f"{PRIOR_HEADS[-1][0]}:{rel}")
            envs.append({
                "source_file": rel, "sha256": sha256_bytes(b), "bytes": len(b),
                "version": "working-tree", "exact_anchor": f"{rel}:1",
                "observed_at": now,
                "supersedes_hash": sha256_bytes(prev.encode()) if prev else "",
                "subject_id": rel.split("/rounds/")[-1].split("/")[0] if "/rounds/" in rel else ROUND_REL.split("/")[-1],
                "subject_hash": head_b, "subject_version": head_b[:12],
                "host": "windows-11", "env": "maker-worktree", "scope": "round-evidence",
                "epoch": 1,
                "freshness": "FRESH_AT_OBSERVED_AT",
                "signature": "AWAITING_EXTERNAL_QUALIFICATION_ISSUER",
                "claim_class": "AUTHOR_SIDE_DESIGN_RECEIPT",
            })
    (out_dir / "EVIDENCE_ENVELOPE.json").write_text(json.dumps(
        {"schema": "CLOSURE-EVIDENCE-ENVELOPE/1",
         "mandatory_inputs": ["source_file", "sha256", "version", "exact_anchor", "observed_at",
                              "supersedes_hash"],
         "adversarial_class": "FOREIGN_OR_STALE_EVIDENCE -> no promotion, HOLD affected-only",
         "count": len(envs), "envelopes": envs}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"supersession_entries": len(sup),
                      "supersession_all_invariants_hold": all(x["invariant_holds"] for x in sup),
                      "affected_artifacts": len(affected), "untouched_artifacts": len(untouched),
                      "evidence_envelopes": len(envs)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
