#!/usr/bin/env python3
"""Read the hosted CI state for a commit: workflow runs, jobs, conclusions, and failing step text.

Read-only against the public GitHub REST API; no token is needed for these endpoints, but one is used
when present so private/rate-limited calls still work. Output is JSON on stdout plus a short summary.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
REPO = "shw097-team/PIPD-LS-SP"
TOKEN_FILE = pathlib.Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
# Local worktree used only to resolve an abbreviated sha to its full 40-char id.
WORKTREE = pathlib.Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt")


def call(path: str) -> tuple[int, dict | list]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "hgk-s4r3x"}
    try:
        if TOKEN_FILE.exists():
            headers["Authorization"] = "Bearer " + TOKEN_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        pass
    req = urllib.request.Request(API + path, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def resolve_sha(sha: str) -> str:
    """Accept a short sha and resolve it against the local round worktree.

    MEASURED trap: the REST `head_sha` filter matches the FULL 40-char id only. Passing an
    abbreviated id returns `total_count: 0` with HTTP 200 - a silent false negative that reads as
    "no CI ran for this commit" when CI in fact ran and passed. Resolving locally first turns that
    into a real answer.
    """
    if len(sha) >= 40:
        return sha
    try:
        out = subprocess.run(
            ["git", "-C", str(WORKTREE), "rev-parse", sha],
            capture_output=True, text=True, check=True).stdout.strip()
        if len(out) >= 40:
            print(f"[note] resolved short id {sha} -> {out}")
            return out
    except (OSError, subprocess.SubprocessError):
        print(f"[warn] could not resolve {sha} locally; querying the short id anyway "
              f"(a zero result would then be meaningless)")
    return sha


def main() -> int:
    sha = resolve_sha(sys.argv[1])
    status, runs = call(f"/repos/{REPO}/actions/runs?head_sha={sha}&per_page=30")
    if status != 200:
        print("LIST_FAILED", status, runs)
        return 1
    out = {"sha": sha, "total_count": runs["total_count"], "runs": []}
    for run in runs["workflow_runs"]:
        entry = {
            "name": run["name"],
            "id": run["id"],
            "event": run["event"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "head_branch": run["head_branch"],
            "created_at": run["created_at"],
            "html_url": run["html_url"],
            "jobs": [],
        }
        st, jobs = call(f"/repos/{REPO}/actions/runs/{run['id']}/jobs?per_page=50")
        if st == 200:
            for job in jobs["jobs"]:
                entry["jobs"].append({
                    "name": job["name"],
                    "status": job["status"],
                    "conclusion": job["conclusion"],
                    "steps": [{"name": s["name"], "conclusion": s["conclusion"]}
                              for s in job.get("steps", [])],
                })
        out["runs"].append(entry)
    print(json.dumps(out, indent=2, ensure_ascii=False))

    print("\n=== summary ===")
    for run in out["runs"]:
        print(f"{run['conclusion'] or run['status']:<12} {run['name']} ({run['event']}) id={run['id']}")
        for job in run["jobs"]:
            print(f"    {job['conclusion'] or job['status']:<10} {job['name']}")
            for step in job["steps"]:
                if step["conclusion"] not in ("success", "skipped", None):
                    print(f"        FAILED STEP: {step['name']} -> {step['conclusion']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
