#!/usr/bin/env python3
"""Collect the hosted-CI evidence for the steps that actually decide this round, straight from the
job logs. Run/job/step ids are printed alongside, so a reader can re-open them.
"""
from __future__ import annotations

import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
REPO = "shw097-team/PIPD-LS-SP"
TOKEN_FILE = pathlib.Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
OUT = pathlib.Path(
    "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
    "/cache/scratch/pipd-s4r3-exec/ci_step_evidence.txt"
)
STEP_MARKERS = (
    "The installed wheel resolves", "Prove the upgrade wrote", "WRITE_SET_CLEAN",
    "installed-wheel contract registry", "GATE_SELF_TEST", "SCOPE_EMPTY", "UPGRADE_WROTE",
)
SUBJECTS = {
    "5310896e706e01a9cdb0123285bccec75086bcb8": [38365817545, 38365822378, 38365822386],
    "60273fe3dee54d88250e1588892da72aecd222ac": [38365822012, 38365828586, 38365828658],
}


class _StripAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and "api.github.com" not in urllib.parse.urlsplit(newurl).netloc:
            new.headers.pop("Authorization", None)
            new.unredirected_hdrs.pop("Authorization", None)
        return new


def api(path: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "hgk-s4r3x"}
    if TOKEN_FILE.exists():
        headers["Authorization"] = "Bearer " + TOKEN_FILE.read_text(encoding="utf-8").strip()
    req = urllib.request.Request(API + path, headers=headers)
    opener = urllib.request.build_opener(_StripAuthOnRedirect)
    with opener.open(req, timeout=180) as resp:
        return json.loads(resp.read().decode() or "{}")


def main() -> int:
    lines: list[str] = []
    for sha, runs in SUBJECTS.items():
        for run_id in runs:
            jobs = api(f"/repos/{REPO}/actions/runs/{run_id}/jobs?per_page=50")
            for job in jobs["jobs"]:
                steps = {s["name"]: s["conclusion"] for s in job["steps"]}
                interesting = [n for n in steps if n.startswith(STEP_MARKERS[:2])]
                lines.append(f"### {sha} run={run_id} job={job['id']} {job['name']} -> {job['conclusion']}")
                for name in interesting:
                    lines.append(f"    step {steps[name]:<8} {name}")
                try:
                    req = urllib.request.Request(
                        f"{API}/repos/{REPO}/actions/jobs/{job['id']}/logs",
                        headers={"Accept": "application/vnd.github+json", "User-Agent": "hgk-s4r3x",
                                 "Authorization": "Bearer " + TOKEN_FILE.read_text(encoding="utf-8").strip()})
                    opener = urllib.request.build_opener(_StripAuthOnRedirect)
                    with opener.open(req, timeout=180) as resp:
                        text = resp.read().decode("utf-8", "replace")
                except (urllib.error.HTTPError, OSError) as exc:
                    lines.append(f"    (log unavailable: {exc})")
                    continue
                clean = [re.sub(r"^\S+Z\s?", "", ln) for ln in text.splitlines()]
                for ln in clean:
                    if any(m in ln for m in STEP_MARKERS):
                        lines.append(f"      | {ln.strip()}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
