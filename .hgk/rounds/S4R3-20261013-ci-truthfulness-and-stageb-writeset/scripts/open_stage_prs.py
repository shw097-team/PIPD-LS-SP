#!/usr/bin/env python3
"""Push the Stage A evidence follow-up and open the two stacked DRAFT pull requests.

The token is read from the owner-provided file inside this process and used only as an
Authorization header on the three requests below. It is never printed, written to a file, passed as
an argv value or placed in a remote URL. Draft PRs only: this round does not approve a merge.
"""
from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

REPO = "shw097-team/PIPD-LS-SP"
TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
PIPD = Path("C:/Projects/Agent_Workspace/PIPD")
OUT = PIPD / ("worktrees/s4r3b-wt/.hgk/rounds/"
              "S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/09_OWNER_RELEASE")
A = "fix/s4r3-stage-a-ci-truthfulness-20261013"
B = "feat/s4r3-stage-b-distribution-20261013"
BASE_B = "fix/s4r3-stage-a-ci-truthfulness-20261013"

HELPER = ('!f(){ echo username=shw097-team; printf "password=%s\\n" '
          '"$(tr -d "\\r\\n" < "C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")"; }; f')

PR_A_BODY = """Draft. **No merge is approved by this PR.** It exists so that the two P0 findings of
`PIPD-S4-EXT-ACCEPT-R3-20261013` have a runnable subject and a raw log a checker can read.

## What this change set is

Stage A `NARROW_REPAIR` for `S4R3-F001`: the `ci` workflow's test steps piped into `tee`/`tail`
without `pipefail`, so a run whose own log read `FAILED (failures=11, skipped=6)` was reported as a
successful job. The suite really was red on hosted Linux; the gate hid it.

- `.github/workflows/ci.yml`, `.github/workflows/public-plugin-verify.yml` — every real test step now
  runs under `set -euo pipefail`; the provenance step captures its log before `tail`; each mutation
  step keeps its explicit status capture, so a step that is *supposed* to fail still fails loudly.
- `pyproject.toml` — PyYAML declared as the `[test]` extra. `tools/skill_pack_check.py` needs it for
  `skills/*/tests/cases.yaml` and never declared it, so six `test_skill_contracts` tests died with
  `TOOL_MISSING` on a runner that only ran `pip install -e .`. The typed refusal is unchanged.
- `src/pipd_ls_sp/workspace.py` — contain a repair subject by the subject's **own** path flavour. A
  Windows-flavoured `C:/Windows/system32/x.dll` was re-based under the authorised root on POSIX
  because `Path()` treats it as relative there, so the escape passed.
- `examples/first-run/run.sh` — index mode 100644 → 100755. It was not executable in a Linux checkout.
- `examples/first-run/run.ps1` — build the scratch workspace from `[System.IO.Path]::GetTempPath()`
  when the Windows-only `$env:TEMP` is absent, instead of passing `$null` to `Join-Path`.
- `tools/cli_smoke.py` — persist the `IntentCard` that this run's own `intake` produced, rather than
  reading the checked-in `.hgk/artifacts/s1/intent_card.json`, whose source is the author's absolute
  Windows path.
- `tests/test_web_fallback.py` — the blanket `assertFalse(out.exists())` failed the very test that
  proves the symlink gate works: refusing a symlinked destination must *leave it in place*. The
  assertion now separates "created nothing" from "left a pre-existing destination untouched", and
  keeps the sentinel-bytes and `is_symlink` assertions.

## Raw evidence in this branch

`.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/` — the frozen subject's own
13 failures, all 13 mapped to 7 root causes with a paired control each, the paired fault injection
(shipped shape returns 0 on a red suite; repaired shape returns 1), and the repaired suite on Linux
and Windows. `RAW_INDEX.json` carries the digest of every file.

## Claim ceiling

Locally verified: the repairs, on Linux (WSL Ubuntu 24.04, Python 3.12) and Windows (Python 3.11).
`Ran 572 / OK (skipped=4)` and `Ran 108 / OK` on Windows; `Ran 572 / OK (skipped=10)` and
`Ran 108 / OK (skipped=1)` on Linux; CLI smoke 13/13. The hosted run of *this* PR is the
authoritative check and is what a checker should read. Not covered: macOS, host UAT, vendor/portal
validation, S4 acceptance. `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS` **not granted**.
"""

PR_B_BODY = """Draft, stacked on the Stage A repair branch. **No merge is approved by this PR.**

## What this change set is

Stage B `UPGRADE` for `S4R3-F002` and `S4R3-F004`.

**F002 — the write-set gate measured the wrong range.** It took `${PR_BASE_SHA:-${STACKED_BASE_SHA}}`.
GitHub reports the base *branch* tip, so a Stage B branch stacked on the Stage A tip but opened
against `main` measured `main...HEAD` — attributing every Stage A source change to the Stage B
upgrade. That is why the run failed on `tools/verify_evidence_digests.py` and skipped the rest. The
gate now:

- measures its **declared** Stage B base and refuses when that base is missing or is not an ancestor;
- prints the full upstream diff as an inventory that is explicitly *not* the Stage B write set;
- says `STAGE_B_SCOPE_EMPTY` in the log rather than reporting a vacuous pass when the head *is* the base;
- self-tests its own classifier against planted `src/**`, `schemas/**`, `skills/**`, `dist/**`
  (must be refused) and planted Stage B artefacts (must be accepted). A gate that accepts everything
  and a gate that refuses everything otherwise look identical from outside.

The allowlist gains two enumerated single paths, no wildcards: `docs/USER_GUIDE.md`, which the upgrade
blueprint names as the single manual path but the R3 allowlist never listed, and this round's own
evidence directory.

**F004 — the Web route promised a document that was not in the tree.** The built
`docs/install/PIPD_WEB_FALLBACK.md` and its `.sha256` are now committed; the install SSOT records both
plus the command that must reproduce them. The README gains one navigation block and stops competing
with the install SSOT; the shell transcripts stay, labelled as executed evidence rather than as a
second set of instructions. `docs/USER_GUIDE.md` is added as the single user guide. 41 local links
and anchors across README → guide → install SSOT → fixtures check clean.

## Write set

`git diff --name-status 517d7a5d3f00935e1589908f456dfacea8fd8a74...HEAD` lists only Stage B paths, and
nothing under `src/**`, `schemas/**`, `skills/**` or `dist/**`. The local reproduction of the gate is
in `.hgk/rounds/S4R3-.../scripts/writeset_gate_repro.sh`.

## Claim ceiling

`BUILD`-level evidence only. No public plugin listing, no portal scan/review/publish, no vendor
validator run, no host UAT, no new release tag — all `NOT_EXECUTED`. `NO_MERGE`,
`NO_PUBLIC_RELEASE`, `S4_FULL_PASS` **not granted**.
"""


def api(method: str, path: str, token: str, payload: dict | None = None):
    req = urllib.request.Request(
        f"https://api.github.com{path}", method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "hgk-s4r3-round"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body[:400]}
        return e.code, parsed


def main() -> int:
    token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if not token:
        print("PUSH_HOLD: the owner-provided token file is empty"); return 2

    print("=== push the Stage A evidence follow-up (non-force, fast-forward) ===")
    push = subprocess.run(
        ["git", "-c", "credential.helper=", "-c", f"credential.helper={HELPER}",
         "push", "--porcelain", "origin", f"refs/heads/{A}:refs/heads/{A}"],
        cwd=str(PIPD), capture_output=True, text=True, timeout=300,
        env={**__import__("os").environ, "GIT_TERMINAL_PROMPT": "0"})
    print(push.stdout.strip()[-400:] or push.stderr.strip()[-400:])
    print("push_exit", push.returncode)

    tips = {}
    for br in (A, B):
        tips[br] = subprocess.run(["git", "rev-parse", br], cwd=str(PIPD),
                                  capture_output=True, text=True).stdout.strip()
    print("local tips:", json.dumps(tips, indent=1))

    results = []
    for head, base, title, body in (
        (A, "main", "S4R3 Stage A (draft): make CI carry the suite's exit code; repair the 11+2 hosted-Linux failures", PR_A_BODY),
        (B, BASE_B, "S4R3 Stage B (draft, stacked): measure the Stage B write set against its declared base; ship the Web artefact", PR_B_BODY),
    ):
        status, data = api("POST", f"/repos/{REPO}/pulls", token,
                           {"title": title, "head": head, "base": base, "body": body, "draft": True})
        entry = {"head": head, "base": base, "status": status,
                 "number": data.get("number"), "url": data.get("html_url"),
                 "draft": data.get("draft"), "mergeable_state": data.get("mergeable_state"),
                 "message": data.get("message"), "errors": data.get("errors")}
        results.append(entry)
        print(json.dumps(entry, indent=1))

    # read each PR back (a create response is not a readback)
    readback = []
    for entry in results:
        if not entry.get("number"):
            continue
        st, d = api("GET", f"/repos/{REPO}/pulls/{entry['number']}", token)
        readback.append({"number": d.get("number"), "state": d.get("state"), "draft": d.get("draft"),
                         "head_sha": (d.get("head") or {}).get("sha"),
                         "base_ref": (d.get("base") or {}).get("ref"),
                         "mergeable": d.get("mergeable"), "merged": d.get("merged"),
                         "changed_files": d.get("changed_files"),
                         "url": d.get("html_url"), "status": st})
    print("=== readback ===")
    print(json.dumps(readback, indent=1))

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "PR_RECEIPT.json").write_text(json.dumps(
        {"schema_id": "PIPD-S4-R3-PR-RECEIPT/1", "repo": REPO, "local_tips": tips,
         "created": results, "readback": readback,
         "note": "Draft PRs only. Creating a pull request is not an approval, not a merge, not a "
                 "release, and not an acceptance."}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return 0 if all(r.get("number") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
