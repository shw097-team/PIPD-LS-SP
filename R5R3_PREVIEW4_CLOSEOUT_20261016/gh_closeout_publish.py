"""Scoped publication for the R5R3 closeout round (argv-safe, no token disclosure).

Same discipline as gh_r5r3_publish.py: the credential is read from the owner's file into memory only;
it never enters argv, the environment, git config, or any log. A repo-scope check runs before any write.

Usage: gh_closeout_publish.py <verify|pr|comment|evidence-branch|evidence-readback> [extra]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

KEY_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
REPO = "shw097-team/PIPD-LS-SP"
ROUND = Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout")
PRODUCT_WT = Path("C:/Projects/wt-r5r3-product-r2")
EVIDENCE_WT = Path("C:/Projects/wt-r5r3-closeout-evidence")
PRODUCT_BRANCH = "docs/r5r3-asset-reproducibility-readback"
EVIDENCE_BRANCH = "r5r3-closeout-evidence-20261016"
PAT = re.compile(r"(github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})")


def token() -> str:
    if not KEY_FILE.is_file():
        sys.exit("OWNER_ACTION_REQUIRED: credential file not found")
    m = PAT.search(KEY_FILE.read_text(encoding="utf-8", errors="ignore"))
    if not m:
        sys.exit("OWNER_ACTION_REQUIRED: no token-shaped credential in the key file")
    return m.group(1)


def _askpass() -> Path:
    impl = ROUND / "_askpass_closeout.py"
    impl.write_text(
        "import re,sys,pathlib\n"
        "PAT=re.compile(r'(github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})')\n"
        f"t=pathlib.Path(r'{KEY_FILE}').read_text(encoding='utf-8',errors='ignore')\n"
        "m=PAT.search(t)\n"
        "sys.stdout.write(m.group(1) if m else '')\n", encoding="utf-8")
    wrapper = ROUND / "_askpass_closeout.cmd"
    wrapper.write_text("@echo off\r\n" f'"{sys.executable}" "{impl}" %*\r\n', encoding="ascii")
    return wrapper


def push_ref(wt: Path, branch: str, dry_run: bool = False) -> dict:
    local = subprocess.run(["git", "-C", str(wt), "rev-parse", branch],
                           capture_output=True, text=True).stdout.strip()
    args = ["git", "-C", str(wt), "-c", "credential.helper=", "-c", "credential.interactive=always",
            "-c", f"core.askPass={_askpass().as_posix()}", "push"]
    if dry_run:
        args.append("--dry-run")
    args += [f"https://github.com/{REPO}.git", f"refs/heads/{branch}:refs/heads/{branch}"]
    env = dict(os.environ, GIT_ASKPASS=_askpass().as_posix(), GIT_TERMINAL_PROMPT="0")
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    err = re.sub(PAT, "[REDACTED]", r.stderr or "")[-500:]
    out = {"branch": branch, "local": local, "rc": r.returncode, "stdout_tail": (r.stdout or "")[-300:],
           "stderr_scrubbed": err, "dry_run": dry_run}
    if not dry_run:
        st, ref = api("GET", f"/repos/{REPO}/git/ref/heads/{branch}")
        remote = (ref.get("object") or {}).get("sha")
        out |= {"remote_http": st, "remote_readback": remote, "readback_matches_local": remote == local}
    return out


def api(method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
    import urllib.error
    import urllib.request
    req = urllib.request.Request(f"https://api.github.com{path}", method=method)
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "hgk-r5r3-closeout")
    body = None
    if payload is not None:
        body = json.dumps(payload).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, body, timeout=45) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"error": "unparseable body"}


def cmd_verify() -> int:
    st, d = api("GET", f"/repos/{REPO}")
    print(json.dumps({"http": st, "full_name": d.get("full_name"), "private": d.get("private"),
                      "permissions": d.get("permissions"), "token_printed": False,
                      "token_in_argv": False}, ensure_ascii=False))
    return 0 if st == 200 and d.get("full_name") == REPO else 1


def cmd_pr() -> int:
    body = (ROUND / "PR_BODY_CLOSEOUT.md").read_text(encoding="utf-8")
    st, d = api("POST", f"/repos/{REPO}/pulls", {
        "title": "R5R3 closeout: preview.4 asset reproducibility, host-refusal discrimination and residual rulings",
        "head": PRODUCT_BRANCH, "base": "main", "body": body})
    print(json.dumps({"http": st, "number": d.get("number"), "url": d.get("html_url"),
                      "state": d.get("state"), "error": d.get("message")}, ensure_ascii=False))
    return 0 if st in (200, 201) else 1


def cmd_comment() -> int:
    number = sys.argv[2]
    body = (ROUND / "PR_COMMENT_CLOSEOUT.md").read_text(encoding="utf-8")
    st, d = api("POST", f"/repos/{REPO}/issues/{number}/comments", {"body": body})
    print(json.dumps({"http": st, "id": d.get("id"), "url": d.get("html_url"),
                      "error": d.get("message")}, ensure_ascii=False))
    return 0 if st in (200, 201) else 1


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if which == "evidence-branch":
        print(json.dumps(push_ref(EVIDENCE_WT, EVIDENCE_BRANCH), ensure_ascii=False))
        raise SystemExit(0)
    if which == "product-branch":
        print(json.dumps(push_ref(PRODUCT_WT, PRODUCT_BRANCH), ensure_ascii=False))
        raise SystemExit(0)
    raise SystemExit({"verify": cmd_verify, "pr": cmd_pr, "comment": cmd_comment}[which]())
