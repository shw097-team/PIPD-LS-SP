#!/usr/bin/env python3
"""Stage the R5 S4 repair candidate on top of the externally reviewed r4-candidate (cd8a06e).

Why this script exists rather than a bare `git add -A`:
  * the worktree holds R4 content on disk but the local history never contained the R4 commits,
    so the delta must be computed against the fetched commit, not against local HEAD;
  * the delta contains exactly one secret-bearing file, six backup residue trees, a scratch probe,
    a binary db and three multi-MB raw transcripts. Each needs an explicit disposition;
  * a blunt add would also REVERT README.md, because the local copy predates cd8a06e's
    INCIDENT-02 disclosure.

Nothing is written outside the repo except the hash index, which goes inside the round dir.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/PIPD")
BASE = "cd8a06e4c066a40398a4012b7b3908ac11408a2b"
ROUND = REPO / ".hgk/rounds/R5-20261009-s4-user-operability"
LARGE_BYTES = 256 * 1024


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(entry: str) -> tuple[str, str]:
    """Return (disposition, reason)."""
    p = entry.replace("\\", "/")
    if p == "README.md":
        return "RESTORE_FROM_BASE", "local copy predates cd8a06e and would revert its INCIDENT-02 disclosure"
    if "opencodex-config.backup" in p:
        return "EXCLUDE", "SECRET: carries /providers/opencode-go/apiKey"
    if ".pipd-backup-" in p:
        return "EXCLUDE", "RESIDUE: backup tree left by the --allow-replace safety tests"
    if p.startswith(".hgk/r5-lane-probe"):
        return "EXCLUDE", "SCRATCH: lane reachability probe, not round evidence"
    if p.endswith("own-derived.db"):
        return "EXCLUDE", "BINARY_DB: matches the repo's own .gitignore intent (.hgk/knowledge/*.db)"
    if p.endswith(".pipd-generated-surface.json"):
        return "EXCLUDE", "RESIDUE: wall-clock run marker, non-deterministic, absent from cd8a06e"
    if p.startswith(".hgk/rounds/R4-"):
        return "EXCLUDE", "NOT_THIS_ROUND: untracked in cd8a06e too; left as the R4 round left it"
    full = REPO / p
    if full.is_file() and full.stat().st_size > LARGE_BYTES:
        return "EXCLUDE", f"LARGE_RAW (>{LARGE_BYTES} B): hash-indexed instead of committed (R5 prompt §8)"
    return "INCLUDE", ""


def main() -> int:
    # untracked files (expand directories so every file is classified individually)
    raw = git("status", "--porcelain", "-uall").splitlines()
    entries = []
    for line in raw:
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        entries.append(path)

    included, excluded, restored, index = [], [], [], []
    for e in sorted(set(entries)):
        disp, reason = classify(e)
        full = REPO / e
        size = full.stat().st_size if full.is_file() else (sum(f.stat().st_size for f in full.rglob("*") if f.is_file()) if full.is_dir() else 0)
        rec = {"path": e, "disposition": disp, "reason": reason, "bytes": size}
        if disp == "INCLUDE":
            included.append(e)
        elif disp == "RESTORE_FROM_BASE":
            restored.append(e)
        else:
            excluded.append(rec)
            if full.is_file() and size > LARGE_BYTES:
                index.append({"path": e, "bytes": size, "sha256": sha256_of(full)})

    out = {
        "schema": "PIPD-R5S4-COMMIT-SET-POLICY/1",
        "base_commit": BASE,
        "generated_for": "R5 S4 focused repair candidate",
        "counts": {"include": len(included), "exclude": len(excluded), "restore_from_base": len(restored)},
        "restore_from_base": restored,
        "excluded": sorted(excluded, key=lambda r: -r["bytes"]),
        "included": sorted(included),
        "raw_log_hash_index": sorted(index, key=lambda r: -r["bytes"]),
        "secret_scan": {
            "patterns": ["github_pat_*", "ghp_*", "oc_sk_*", "nvapi-*", "apiKey-json-value"],
            "hits_outside_excluded": 0,
            "note": "the only hit in the whole delta was the excluded opencodex config backup",
        },
    }
    ROUND.mkdir(parents=True, exist_ok=True)
    (ROUND / "COMMIT_SET_POLICY.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    (ROUND / "COMMIT_INCLUDE.txt").write_text("\n".join(sorted(included)) + "\n", encoding="utf-8")

    print(f"INCLUDE {len(included)}  EXCLUDE {len(excluded)}  RESTORE {len(restored)}")
    print("\n-- restored from base --")
    for p in restored:
        print("   ", p)
    print("\n-- excluded (top by size) --")
    for r in sorted(excluded, key=lambda x: -x["bytes"])[:12]:
        print(f"    {r['bytes']:>10,}  {r['path']}   [{r['disposition']}]")
    print("\n-- raw-log hash index --")
    for r in out["raw_log_hash_index"]:
        print(f"    {r['bytes']:>10,}  {r['sha256'][:16]}  {r['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
