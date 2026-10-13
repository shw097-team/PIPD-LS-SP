#!/usr/bin/env python3
"""Fetch the raw job logs of the hosted runs on the Stage A and Stage B candidates.

Anonymous read for run/job metadata; the job-log endpoint needs the owner token, which is read in
process, used only as an Authorization header on api.github.com, and stripped on the redirect to
storage (otherwise the storage host rejects the forwarded token). Nothing is printed but log lines.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

REPO = "shw097-team/PIPD-LS-SP"
TOK = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt").read_text(encoding="utf-8").strip()
OUT = Path(".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/09_OWNER_RELEASE")
RUNS = {38349126621: "stage_a_public_plugin_verify", 38349126601: "stage_a_ci",
        38349130092: "stage_b_public_plugin_verify", 38349130157: "stage_b_ci"}
PATTERNS = (r"Ran [0-9]+ tests", r"^OK", r"^FAILED", r"WRITE_SET", r"UPGRADE_WROTE", r"STAGE_B_",
            r"GATE_SELF_TEST", r"^FAIL: ", r"^ERROR: ", r"Process completed with exit code",
            r"Full unittest suite", r"Focused S4", r"wheel", r"doctor", r"pipefail")


class NoAuthAfterRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and "api.github.com" not in newurl:
            new.headers.pop("Authorization", None)
        return new


OPENER = urllib.request.build_opener(NoAuthAfterRedirect)


def api(path: str, raw: bool = False):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "hgk-s4r3-round",
                                          "Authorization": f"Bearer {TOK}"})
    try:
        with OPENER.open(req, timeout=120) as r:
            b = r.read()
            return r.status, (b.decode(errors="replace") if raw else json.loads(b or b"{}"))
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode(errors="replace") if raw else {"error": e.code})


OUT.mkdir(parents=True, exist_ok=True)
summary = {}
for run_id, label in RUNS.items():
    _, jobs = api(f"/repos/{REPO}/actions/runs/{run_id}/jobs")
    entry = {"run_id": run_id, "jobs": []}
    print(f"\n########## {label}  run {run_id} ##########")
    for job in jobs.get("jobs", []):
        print(f"JOB {job['name']} -> {job['conclusion']}")
        for step in job.get("steps", []):
            print("   %3s %-10s %s" % (step.get("number"), step.get("conclusion"), step["name"]))
        entry["jobs"].append({"job": job["name"], "conclusion": job["conclusion"],
                              "steps": [{"n": s.get("number"), "conclusion": s.get("conclusion"),
                                         "name": s["name"]} for s in job.get("steps", [])]})
        status, logs = api(f"/repos/{REPO}/actions/jobs/{job['id']}/logs", raw=True)
        text = logs if isinstance(logs, str) else ""
        (OUT / f"{label}__job_{job['id']}.raw.log").write_text(text, encoding="utf-8", newline="")
        lines = [re.sub(r"^\S+Z ", "", ln) for ln in text.replace("\r", "").split("\n")]
        keep = [ln for ln in lines if any(re.search(p, ln) for p in PATTERNS)]
        (OUT / f"{label}__job_{job['id']}.selected.txt").write_text("\n".join(keep) + "\n",
                                                                   encoding="utf-8", newline="")
        print(f"   log: {len(text)} bytes, {len(lines)} lines, {len(keep)} selected")
        for ln in keep[:24]:
            print("     |", ln[:200])
    summary[label] = entry
(OUT / "HOSTED_CI_JOB_SUMMARY.json").write_text(
    json.dumps({"schema_id": "PIPD-S4-R3-HOSTED-CI-JOB-SUMMARY/1", "runs": summary},
               indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("\nwrote", OUT / "HOSTED_CI_JOB_SUMMARY.json")
