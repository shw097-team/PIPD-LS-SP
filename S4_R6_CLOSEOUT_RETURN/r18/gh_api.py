"""Read-only GitHub API helper for the round's readback.

The PAT is read from the controlled secret file *inside this process* and placed only into the
request header. It never appears in the command line, in an environment variable of a child
process, or in any log line: the script prints response bodies only, and redacts any token-shaped
substring before printing.

Usage:  python gh_api.py <path-without-leading-slash>
        python gh_api.py repos/shw097-team/PIPD-LS-SP/pulls/18
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

SECRET = pathlib.Path(r"C:\Projects\Agent_Workspace\API KEY\GITHUB-REPO_SHW097-4.txt")
PAT_RE = re.compile(r"(github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})")
API = "https://api.github.com"


def token() -> str:
    m = PAT_RE.search(SECRET.read_text(encoding="utf-8", errors="ignore"))
    if not m:
        raise SystemExit("no token found in the secret file")
    return m.group(1)


def redact(text: str) -> str:
    return PAT_RE.sub("[REDACTED]", text)


def get(path: str, accept: str = "application/vnd.github+json") -> tuple[int, str]:
    req = urllib.request.Request(
        f"{API}/{path.lstrip('/')}",
        headers={
            "Authorization": f"Bearer {token()}",
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "hgk-round-readback",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    status, body = get(sys.argv[1])
    print(f"HTTP {status}")
    try:
        print(redact(json.dumps(json.loads(body), ensure_ascii=False, indent=2))[:6000])
    except json.JSONDecodeError:
        print(redact(body)[:3000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
