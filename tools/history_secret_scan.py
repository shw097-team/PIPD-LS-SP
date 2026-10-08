#!/usr/bin/env python3
"""Regenerate .hgk/artifacts/history_secret_scan.json from a FRESH import.

Runs as its own process on purpose: an in-kernel import cache had recorded pattern names from a
superseded revision of workspace.py, so the artifact disagreed with the source it claimed to
describe. Recorded facts must come from the revision being described.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

R = Path(r"C:\Projects\Agent_Workspace\PIPD")
sys.path.insert(0, str(R / "src"))
from pipd_ls_sp.workspace import SECRET_PATTERNS  # noqa: E402

g = lambda *a: subprocess.run(["git", "-C", str(R), *a], capture_output=True, text=True).stdout
rev = g("rev-parse", "HEAD").strip()
src = (R / "src" / "pipd_ls_sp" / "workspace.py").read_bytes()

shas = [l.split()[0] for l in g("rev-list", "--objects", "--all").splitlines() if len(l.split()) > 1]
batch = subprocess.run(["git", "-C", str(R), "cat-file", "--batch"],
                       input="\n".join(shas).encode(), capture_output=True).stdout.decode("utf-8", "replace")

object_hits = {n: len(rx.findall(batch)) for n, rx in SECRET_PATTERNS}
worktree_hits: dict[str, int] = {}
files = 0
for f in R.rglob("*"):
    if not f.is_file() or ".git" in f.parts or "__pycache__" in f.parts:
        continue
    files += 1
    try:
        txt = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    for n, rx in SECRET_PATTERNS:
        c = len(rx.findall(txt))
        if c:
            worktree_hits[f"{n}::{f.relative_to(R)}"] = c

out = {
    "schema": "PIPD-HISTORY-SECRET-SCAN/1",
    # NOTE ON SEMANTICS: this field names the revision whose SOURCE was scanned, which is necessarily a
    # commit EARLIER than the one that carries this file. A file cannot record the SHA of the commit that
    # contains it. A previous version called this `revision`, and an independent checker correctly read
    # that as claiming to be the candidate. `candidate_binding` below states the intended reading.
    "source_revision_scanned": rev,
    "candidate_binding": ("describes the source at source_revision_scanned; this file is committed by a "
                          "subsequent evidence-only commit whose src/ tests/ schemas/ trees are identical "
                          "to source_revision_scanned"),
    "source_file": "src/pipd_ls_sp/workspace.py",
    "source_sha256": __import__("hashlib").sha256(src).hexdigest(),
    "method": "each compiled pattern in pipd_ls_sp.workspace.SECRET_PATTERNS applied to (a) every "
              "worktree file and (b) `git rev-list --objects --all | git cat-file --batch` bytes",
    "pattern_names": [n for n, _ in SECRET_PATTERNS],
    "objects_listed": len(shas),
    "worktree_files_scanned": files,
    "object_hits": object_hits,
    "worktree_hits": worktree_hits,
    "verdict": "PASS" if sum(object_hits.values()) == 0 and not worktree_hits else "FAIL",
    "note": "pattern names and the source hash are read from the revision named above, in a fresh process",
}
p = R / ".hgk" / "artifacts" / "history_secret_scan.json"
p.write_text(json.dumps(out, indent=1), encoding="utf-8", newline="")
print(json.dumps({k: out[k] for k in ("source_revision_scanned", "source_sha256", "pattern_names",
                                      "objects_listed", "worktree_files_scanned", "verdict")}, indent=1))
