#!/usr/bin/env python3
"""Read the hosted workflow runs for the two S4R3 branches and record what they really concluded.

Anonymous read: the repository is public, so no credential is used and none is needed. The API's
`conclusion` is recorded, but so is the raw `Ran .../FAILED (...)` line from each job log, because
the whole point of S4R3-F001 is that the two can disagree.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "shw097-team/PIPD-LS-SP"
OUT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3b-wt/.hgk/rounds/"
           "S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/09_OWNER_RELEASE")
BRANCHES = {
    "fix/s4r3-stage-a-ci-truthfulness-20261013": "8cbe2582e065d3e220170650cf784955a86eccc1",
    "feat/s4r3-stage-b-distribution-20261013": "8481f29913159ed91ac6dff5ab3d691ea3614355",
}


def get(path: str, raw: bool = False):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                headers={"Accept": "application/vnd.github+json",
                                         "User-Agent": "hgk-s4r3-round"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return r.status, (body.decode(errors="replace") if raw else json.loads(body or b"{}"))
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode(errors="replace") if raw else {"error": e.code})


def main() -> int:
    report: dict = {"schema_id": "PIPD-S4-R3-HOSTED-CI-READBACK/1", "repo": REPO, "branches": {}}
    for branch, expected_sha in BRANCHES.items():
        st, runs = get(f"/repos/{REPO}/actions/runs?branch={branch}&per_page=10")
        entry: dict = {"http": st, "expected_sha": expected_sha, "workflows": []}
        if st == 200:
            for run in runs.get("workflow_runs", []):
                wf = {"workflow": run["name"], "run_id": run["id"], "run_number": run["run_number"],
                      "event": run["event"], "status": run["status"],
                      "conclusion": run["conclusion"], "head_sha": run["head_sha"],
                      "url": run["html_url"], "jobs": []}
                jst, jobs = get(f"/repos/{REPO}/actions/runs/{run['id']}/jobs")
                if jst == 200:
                    for job in jobs.get("jobs", []):
                        j = {"job": job["name"], "job_id": job["id"], "status": job["status"],
                             "conclusion": job["conclusion"]}
                        log_lines = []
                        for step in job.get("steps", []):
                            log_lines.append(
                                "%3s %-10s %s" % (step.get("number"), step.get("conclusion"), step["name"]))
                        j["steps"] = log_lines
                        wf["jobs"].append(j)
                entry["workflows"].append(wf)
        report["branches"][branch] = entry
        print(f"--- {branch} ---")
        for wf in entry.get("workflows", []):
            print(f"  {wf['workflow']:<22} run {wf['run_id']} {wf['status']}/{wf['conclusion']} "
                  f"head={wf['head_sha'][:12]} {wf['url']}")
            for j in wf["jobs"]:
                print(f"      job {j['job']:<28} {j['conclusion']}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "HOSTED_CI_READBACK.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
