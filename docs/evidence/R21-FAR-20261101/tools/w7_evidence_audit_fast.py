"""W7 (fast path): map each work-queue row to artefacts that name it, using ripgrep.

The full os.walk version timed out (the var tree is large); rg returns the 872 naming files in
~2 s, so the audit runs on that list instead. Same rule as before: bind only what exists.
"""
import hashlib
import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
DB = ROOT / "HG-KSEOS" / "var" / "shared-spine" / "hg-kseos.db"
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp_evidence"
OUT.mkdir(parents=True, exist_ok=True)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    import sqlite3
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    cols = [c[1] for c in con.execute("pragma table_info(work_queue)")]
    rows = [dict(zip(cols, r)) for r in con.execute("select * from work_queue")]

    out = subprocess.run(["rg", "-l", "WP-FHS-[0-9]+", "var", "HG-KSEOS/ops",
                          "--glob", "*.{json,md,tsv,jsonl,txt}"],
                         cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=300)
    files = [ROOT / f for f in out.stdout.splitlines() if f.strip()]
    files = [f for f in files if f.is_file() and 200 <= f.stat().st_size <= 8_000_000]

    proposals = []
    for r in rows:
        wp = r["wp_id"]
        scored = []
        for p in files:
            rel = str(p.relative_to(ROOT)).replace("\\", "/")
            if rel.startswith("HG-KSEOS/var/shared-spine"):
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if wp in t:
                scored.append((p.stat().st_size, rel, p))
        scored.sort(reverse=True, key=lambda x: x[0])
        best = scored[0] if scored else None
        if r.get("evidence_ref"):
            verdict, why, ev = "KEEP", f"already binds {r.get('evidence_ref')}", r.get("evidence_ref")
        elif best:
            verdict = "BIND" if r["state"] == "PASS" else "BIND_FAIL_STATE"
            why = f"{len(scored)} naming files; largest {best[0]} B"
            ev = {"path": best[1], "sha256": sha(best[2]), "bytes": best[0]}
        else:
            verdict = "UNSUPPORTED_PASS" if r["state"] == "PASS" else "UNSUPPORTED_FAIL"
            why, ev = "no naming artefact on disk", None
        proposals.append({"wp_id": wp, "state": r["state"], "blocker_code": r.get("blocker_code"),
                          "current_evidence_ref": r.get("evidence_ref"), "naming_files": len(scored),
                          "proposal": verdict, "why": why, "evidence": ev})

    payload = {"schema": "WP_EVIDENCE_AUDIT/1",
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "method": "ripgrep -l 'WP-FHS-[0-9]+' over var/ + HG-KSEOS/ops, then exact id match per file",
               "naming_files": len(files), "queue_rows": len(rows),
               "rows_with_evidence_before": sum(1 for r in rows if r.get("evidence_ref")),
               "proposals": proposals}
    (OUT / "CANDIDATE_BINDINGS.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    counts = {}
    for p in proposals:
        counts[p["proposal"]] = counts.get(p["proposal"], 0) + 1
    print(json.dumps({"rows": len(rows), "naming_files": len(files), "counts": counts,
                      "detail": {p["wp_id"]: (p["proposal"], p["naming_files"]) for p in proposals}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
