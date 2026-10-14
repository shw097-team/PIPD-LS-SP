#!/usr/bin/env python3
"""Update the stacked Stage B successor PR body (rewrite disclosure + current subject)."""
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

TITLE = "S4R3 Stage B: stacked on the current Stage A tip, packaging identity defects closed"

BODY = """\
Draft. Stacked on `fix/s4r3-stage-a-ci-truthfulness-20261013`. Review/merge order is Stage A first.

## Branch rewrite, disclosed

This branch was published once as `2363bf6` and then **rewritten** to `60273fe` with
`--force-with-lease` (never a bare `--force`). Why: the first head sat on the *previous* Stage A tip
and therefore did not contain the stage-aware write-set gate or the F006 gate that validate it — the
exact defect this branch exists to correct. Stage B is a draft created in this same round, never
reviewed and never accepted, so a linear stack was preferred over carrying a stale base forward. If you
had fetched `2363bf6`, it is superseded; nothing outside this draft branch depends on it. Stage A was
only ever fast-forwarded, and `main` / `v0.1.1-preview.3` are untouched.

## What this branch changes

1. **Stacked on the current Stage A tip** (`5310896`), so the branch contains the CI truthfulness
   guards, the S4R3-F006 packaging repair and the stage-aware write-set gate. The previous head
   (`c52c219`) was a *sibling* of the Stage A repairs, not a descendant: measured with two dots,
   `4647d14..c52c219` still diverged in Stage A's module paths.
2. **`CR-IDENTITY-BIND` closed** (`tools/build_public_plugin.py`). The official manifest's
   `name`/`version`/`license` are now bound to the release bookkeeping. A vendor-schema-valid but
   *different* `name` used to be accepted at exit 0 while the ZIP root and the release receipt still
   carried the bookkeeping's `plugin_id` — one artefact, two contradicting identities.
3. **`CR-EXT-UNREVIEWED` closed** (same file). `extensions` is restricted to the reviewed namespace set
   (`com.openai`, `com.pipd.s4`). The locked vendor schema permits arbitrary object-valued namespaces,
   so an unreviewed one travelled inside the ZIP at exit 0.
4. Seven negative/positive tests cover both, including that a vendor-valid other name is refused, that
   an empty `extensions` is refused, and that the reviewed set is pinned.
5. **Declares `STAGE: stage-b`** in `public-plugin-verify.yml`, so the write-set gate measures this
   branch's own attributable set. That file is byte-identical to Stage A's except this one line. The
   base is resolved by ref, so if Stage A advances this branch goes red with `BASE_NOT_ANCESTOR` until
   it is re-stacked — the invariant, not an accident.

Both identity defects were recorded as OPEN in the previous round's `ACCEPTANCE_RECORD_STAGEB.md`; the
author of this branch did not find them.

## Claim ceiling

- `LOCAL_PACKAGER_PASS_ONLY`. No human publisher identity, brand artwork, official vendor validator,
  Portal scan/review/publish, or host UAT has been executed.
- `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` remain in force. This PR is a proposal
  for independent acceptance, not an acceptance.
"""


def main() -> int:
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()

    def call(method: str, path: str, payload: dict | None = None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            API + path, data=data, method=method,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "hgk-s4r3x",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, json.loads(resp.read().decode() or "{}")
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode() or "{}")

    status, prs = call("GET", f"/repos/{REPO}/pulls?state=open&head=shw097-team:{HEAD}&base={BASE}")
    if status != 200 or not prs:
        print("NO_PR", status, prs)
        return 1
    pr = prs[0]
    status, updated = call("PATCH", f"/repos/{REPO}/pulls/{pr['number']}",
                           {"title": TITLE, "body": BODY})
    print("PATCH", status, updated.get("html_url"), "draft=", updated.get("draft"),
          "head=", (updated.get("head") or {}).get("sha"))
    return 0 if status == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main())
