#!/usr/bin/env python3
"""Read the hosted CI state for a commit: workflow runs, jobs, conclusions, and failing step text.

Read-only against the public GitHub REST API; no token is needed for these endpoints, but one is used
when present so private/rate-limited calls still work. Output is JSON on stdout plus a short summary.
"""
from __future__ import annotations

import json
import pathlib
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
REPO = "shw097-team/PIPD-LS-SP"
TOKEN_FILE = pathlib.Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")


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
    """Expand a short SHA before filtering.

    GitHub's `head_sha` filter matches the FULL 40-character value only: a short SHA returns HTTP 200
    with `total_count: 0`, which reads exactly like "no CI ran" and is not. This tool reported 0 runs for
    a commit that in fact had three green runs, so the expansion is mandatory, not a convenience.
    """
    if len(sha) >= 40:
        return sha
    status, data = call(f"/repos/{REPO}/commits/{sha}")
    if status == 200 and isinstance(data, dict) and data.get("sha"):
        return str(data["sha"])
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
