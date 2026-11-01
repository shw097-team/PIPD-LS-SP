"""W7 v2: row-specific evidence only. A file that names MANY work orders proves nothing about one.

Rejects the v1 heuristic (largest naming file): 11 rows shared one family manifest and 6 shared
another, which is family-level binding - exactly what the round forbids. A row may bind only:
  * a file whose PATH contains the work-order id, or
  * a per-WP queue output under C:/wg/queue/<WP>/output/, or
  * an existing evidence_ref the row already carries.
Everything else is UNSUPPORTED_PASS with the reason recorded.
"""
import hashlib
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp_evidence"
WG = pathlib.Path(r"C:\wg\queue")
OUT.mkdir(parents=True, exist_ok=True)


def sha(p):
    p = pathlib.Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def main():
    import sqlite3
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    cols = [c[1] for c in con.execute("pragma table_info(work_queue)")]
    rows = [dict(zip(cols, r)) for r in con.execute("select * from work_queue")]

    all_files = []
    for base in (ROOT / "var", ROOT / "HG-KSEOS" / "ops"):
        for p in base.rglob("*"):
            try:
                if p.is_file() and p.suffix.lower() in (".json", ".md", ".tsv", ".jsonl") \
                        and 200 <= p.stat().st_size <= 8_000_000:
                    all_files.append(p)
            except OSError:
                continue

    proposals = []
    for r in rows:
        wp = r["wp_id"]
        row_files = [p for p in all_files if wp in str(p)]
        wg_files = []
        wg_dir = WG / wp / "output"
        if wg_dir.is_dir():
            wg_files = [p for p in wg_dir.rglob("*") if p.is_file() and p.stat().st_size >= 100]
        picked = None
        for cand in sorted(row_files + wg_files, key=lambda p: p.stat().st_size, reverse=True):
            picked = cand
            break
        if r.get("evidence_ref"):
            verdict, why, ev = "KEEP", "row already binds an evidence_ref", r.get("evidence_ref")
        elif picked is not None:
            verdict, why = ("BIND" if r["state"] == "PASS" else "BIND_FAIL_STATE"), \
                f"row-specific artefact ({picked.stat().st_size} B, path names the WP)"
            ev = {"path": str(picked.relative_to(ROOT)).replace("\\", "/")
                  if str(picked).startswith(str(ROOT)) else str(picked),
                  "sha256": sha(picked), "bytes": picked.stat().st_size}
        else:
            verdict = "UNSUPPORTED_PASS" if r["state"] == "PASS" else "UNSUPPORTED_FAIL"
            why = "no row-specific artefact; family-level files were rejected by rule"
            ev = None
        proposals.append({"wp_id": wp, "state": r["state"], "blocker_code": r.get("blocker_code"),
                          "current_evidence_ref": r.get("evidence_ref"),
                          "row_specific_files": len(row_files), "wg_output_files": len(wg_files),
                          "proposal": verdict, "why": why, "evidence": ev})

    payload = {"schema": "WP_EVIDENCE_AUDIT/2",
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "rule": "a row binds only a path that names that work order, or its C:/wg/queue output; "
                       "family manifests naming many WPs are rejected",
               "rejected_v1_note": "v1 bound 11 rows to one source_manifest.json and 6 to one r15_atoms949.json",
               "queue_rows": len(rows), "proposals": proposals}
    (OUT / "CANDIDATE_BINDINGS_V2.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8", newline="\n")
    counts = {}
    for p in proposals:
        counts[p["proposal"]] = counts.get(p["proposal"], 0) + 1
    print(json.dumps({"counts": counts,
                      "detail": {p["wp_id"]: [p["proposal"], p["row_specific_files"] + p["wg_output_files"]]
                                 for p in proposals}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
