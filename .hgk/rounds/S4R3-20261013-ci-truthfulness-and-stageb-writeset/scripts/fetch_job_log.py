#!/usr/bin/env python3
"""Fetch a GitHub Actions job log as text and print the failing region.

Usage: fetch_job_log.py <job_id> [out_path] [--grep REGEX]
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
REPO = "shw097-team/PIPD-LS-SP"
TOKEN_FILE = pathlib.Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")


class _StripAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    """GitHub's job-log endpoint 302s to a pre-signed blob URL.

    The signature is in the query string, so forwarding our Authorization header to the blob host makes
    it reject the request with InvalidAuthenticationInfo. Drop the header whenever the redirect leaves
    api.github.com.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and "api.github.com" not in urllib.parse.urlsplit(newurl).netloc:
            new.headers.pop("Authorization", None)
            new.unredirected_hdrs.pop("Authorization", None)
        return new


def main() -> int:
    job_id = sys.argv[1]
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    pattern = None
    if "--grep" in sys.argv:
        pattern = sys.argv[sys.argv.index("--grep") + 1]

    headers = {"Accept": "application/vnd.github+json", "User-Agent": "hgk-s4r3x"}
    if TOKEN_FILE.exists():
        headers["Authorization"] = "Bearer " + TOKEN_FILE.read_text(encoding="utf-8").strip()
    req = urllib.request.Request(f"{API}/repos/{REPO}/actions/jobs/{job_id}/logs", headers=headers)
    opener = urllib.request.build_opener(_StripAuthOnRedirect)
    try:
        with opener.open(req, timeout=180) as resp:
            text = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        print("LOG_FETCH_FAILED", exc.code, exc.read().decode("utf-8", "replace")[:500])
        return 1

    if out:
        out.write_text(text, encoding="utf-8")
        print(f"wrote {out} ({len(text)} chars)")

    lines = text.splitlines()
    if pattern:
        rx = re.compile(pattern)
        hits = [i for i, ln in enumerate(lines) if rx.search(ln)]
        for i in hits:
            lo, hi = max(0, i - 12), min(len(lines), i + 25)
            print(f"----- match at line {i} -----")
            print("\n".join(lines[lo:hi]))
    else:
        print("\n".join(lines[-120:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
