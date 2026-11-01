"""W7: audit the 22 work-queue rows against artefacts that actually exist on disk.

For each WP id: find files (json/md/tsv/log) that NAME the id and carry a non-trivial payload, then
propose either a bound evidence_ref (file + sha256) or UNSUPPORTED_PASS. Nothing is decided here;
the caller applies the proposal through `work_queue.py settle`.
"""
import hashlib
import json
import os
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp_evidence"
OUT.mkdir(parents=True, exist_ok=True)

SEARCH_ROOTS = [ROOT / "var", ROOT / "HG-KSEOS" / "ops", ROOT / "HG-KSEOS" / "var"]
EXTS = {".json", ".md", ".tsv", ".jsonl", ".txt"}
MIN_BYTES = 200


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    import sqlite3
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    cols = [c[1] for c in con.execute("pragma table_info(work_queue)")]
    rows = [dict(zip(cols, r)) for r in con.execute("select * from work_queue")]
    ids = [r["wp_id"] for r in rows]

    # one bounded walk, then match every id against file contents
    hits = {i: [] for i in ids}
    scanned = 0
    skipped_big = 0
    for base in SEARCH_ROOTS:
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "node_modules")]
            for fn in filenames:
                p = pathlib.Path(dirpath) / fn
                if p.suffix.lower() not in EXTS:
                    continue
                try:
                    size = p.stat().st_size
                except OSError:
                    continue
                if size < MIN_BYTES or size > 8_000_000:
                    skipped_big += size > 8_000_000
                    continue
                try:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                scanned += 1
                for i in ids:
                    if i in text:
                        hits[i].append(p)

    proposals = []
    for r in rows:
        wp = r["wp_id"]
        cands = hits[wp]
        # prefer the biggest file that is NOT a copy of the queue itself
        scored = []
        for p in cands:
            try:
                b = p.stat().st_size
            except OSError:
                continue
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if "hg-kseos.db" in rel or rel.startswith("HG-KSEOS/var/shared-spine"):
                continue
            scored.append((b, rel, p))
        scored.sort(reverse=True, key=lambda t: t[0])
        best = scored[0] if scored else None
        has_own = bool(r.get("evidence_ref"))
        if has_own:
            verdict, why = "KEEP", f"row already binds {r.get('evidence_ref')}"
            ev = r.get("evidence_ref")
        elif best:
            verdict = "BIND" if r["state"] == "PASS" else "BIND_FAIL_STATE"
            why = f"naming artefact found ({best[0]} B)"
            ev = {"path": best[1], "sha256": sha(best[2]), "bytes": best[0]}
        else:
            verdict, why, ev = "UNSUPPORTED_PASS", "no naming artefact on disk", None
            if r["state"] != "PASS":
                verdict = "UNSUPPORTED_FAIL"
        proposals.append({"wp_id": wp, "state": r["state"], "blocker_code": r.get("blocker_code"),
                          "current_evidence_ref": r.get("evidence_ref"),
                          "candidates_found": len(cands), "proposal": verdict, "why": why,
                          "evidence": ev})

    payload = {"schema": "WP_EVIDENCE_AUDIT/1",
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "queue_rows": len(rows), "files_scanned": scanned, "files_skipped_too_big": skipped_big,
               "rows_with_evidence_before": sum(1 for r in rows if r.get("evidence_ref")),
               "proposals": proposals}
    (OUT / "CANDIDATE_BINDINGS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    counts = {}
    for p in proposals:
        counts[p["proposal"]] = counts.get(p["proposal"], 0) + 1
    print(json.dumps({"rows": len(rows), "files_scanned": scanned, "counts": counts,
                      "bindable": [p["wp_id"] for p in proposals if p["proposal"].startswith("BIND")],
                      "unsupported": [p["wp_id"] for p in proposals if p["proposal"].startswith("UNSUPPORTED")]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
