#!/usr/bin/env python3
"""Open (or reuse) the stacked draft PR for the Stage B successor branch.

The token is read from the owner's file at runtime and put only into the HTTPS Authorization header;
it is never printed, never passed in argv, and never written to any artifact. GitHub's REST API is used
directly so the operation is one idempotent call that can be re-run.
"""
from __future__ import annotations

import json
import pathlib
import urllib.error
import urllib.request

TOKEN_FILE = pathlib.Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
API = "https://api.github.com"
REPO = "shw097-team/PIPD-LS-SP"
HEAD = "feat/s4r3-stageb-successor-20261013"
BASE = "fix/s4r3-stage-a-ci-truthfulness-20261013"

TITLE = "S4R3 Stage B successor: stacked on the repaired Stage A tip, packaging identity defects closed"

BODY = """\
Draft. Stacked on `fix/s4r3-stage-a-ci-truthfulness-20261013` (base = the repaired Stage A tip
`9772bfa9f949d77a41583b0f2b20a37570a930c2`), **not** on `main`. Review/merge order is Stage A first.

This branch supersedes `feat/s4r3-stage-b-distribution-20261013` (`c52c219`), which was a **sibling**
of the Stage A repairs rather than a descendant: measured with two dots, `4647d14..c52c219` still
diverged in Stage A's module paths, and the branch therefore did not contain the CI truthfulness
guards or the S4R3-F006 packaging repair it is validated by. Rather than force-pushing a public
branch, the product surface was carried onto a new successor branch and the declared base was moved.

## What this branch changes

1. **Declared write-set base moved** to the new Stage A tip in `.github/workflows/public-plugin-verify.yml`
   (`STAGE_B_BASE_SHA`), so the write-set gate compares this branch against the tip it actually sits on.
2. **`CR-IDENTITY-BIND` closed** (`tools/build_public_plugin.py`). The official manifest's
   `name`/`version`/`license` are now bound to the release bookkeeping. Previously a vendor-schema-valid
   but *different* `name` was accepted at exit 0 while the ZIP root directory and the release receipt
   still carried the bookkeeping's `plugin_id` — one artefact, two contradicting identities.
3. **`CR-EXT-UNREVIEWED` closed** (same file). `extensions` is now restricted to the reviewed namespace
   set (`com.openai`, `com.pipd.s4`). The locked vendor schema permits arbitrary object-valued
   namespaces, so an unreviewed one used to travel inside the ZIP at exit 0.
4. Seven negative/positive tests cover both, including that a *vendor-valid* other name is refused,
   that an empty `extensions` is refused, and that the reviewed set is pinned.

Both defects were recorded as OPEN in the previous round's `ACCEPTANCE_RECORD_STAGEB.md`; they were not
found by the author of this branch.

## Claim ceiling

- `LOCAL_PACKAGER_PASS_ONLY`. No human publisher identity, brand artwork, official vendor validator,
  Portal scan/review/publish, or host UAT has been executed.
- `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` remain in force. This PR is a proposal
  for independent acceptance, not an acceptance.
"""


def main() -> int:
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()

    def call(method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            API + path,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "hgk-s4r3x",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode() or "{}")

    status, prs = call("GET", f"/repos/{REPO}/pulls?state=open&head=shw097-team:{HEAD}&base={BASE}")
    if status != 200:
        print("LIST_FAILED", status, prs)
        return 1
    if prs:
        pr = prs[0]
        print(f"EXISTING PR #{pr['number']} {pr['html_url']} draft={pr['draft']}")
        status, pr = call("PATCH", f"/repos/{REPO}/pulls/{pr['number']}",
                          {"title": TITLE, "body": BODY})
        print("PATCH", status, pr.get("html_url"), "draft=", pr.get("draft"), pr.get("message", ""))
        return 0

    status, pr = call("POST", f"/repos/{REPO}/pulls", {
        "title": TITLE, "head": HEAD, "base": BASE, "body": BODY, "draft": True,
    })
    if status not in (200, 201):
        print("CREATE_FAILED", status, pr)
        return 1
    print(f"CREATED PR #{pr['number']} {pr['html_url']} draft={pr['draft']} "
          f"head={pr['head']['sha']} base={pr['base']['ref']}")

    status, allprs = call("GET", f"/repos/{REPO}/pulls?state=open")
    print("--- all open PRs ---")
    for p in sorted(allprs, key=lambda x: x["number"]):
        print(f"  #{p['number']} draft={p['draft']} {p['base']['ref']} <- {p['head']['ref']} "
              f"head_sha={p['head']['sha']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
