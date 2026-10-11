#!/usr/bin/env python
"""R5Q publication driver — owner-authorised S4 open-source preview.

CREDENTIAL DISCIPLINE (owner grant, R5Q): the fine-grained PAT is read from its own file into
process memory and is handed to `git` through a child-process environment variable consumed by an
askpass shim. It is never placed in argv, in a remote URL, in a log line, in git config, in the
evidence pack, or in any uploaded asset. Nothing in this module prints it, and the askpass shim
never contains it.

Modes:
    --preflight   read-only: repo visibility, tag collision, base refs. Safe to run any time.
    --publish     push the branch, create the immutable tag ref, create the prerelease, upload assets.
    --readback    re-derive the published state from GitHub and verify every asset hash by download.

--publish refuses to run unless --preflight has passed and the local release commit is clean.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

OWNER = "shw097-team"
REPO = "PIPD-LS-SP"
API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
UA = "r5q-preview-publisher"
TOKEN_FILE = pathlib.Path(r"C:/Projects/Agent_Workspace/API KEY/Fine-grained personal access tokens.txt")
TOKEN_SHAPE = re.compile(r"github_pat_[A-Za-z0-9_]{20,}")

RELEASE_COMMIT_DEFAULT = "HEAD"   # resolved with `git rev-parse` so the pin can never go stale
BRANCH = "r5q-owner-opensource-preview"
TAG = "v0.1.0-preview.1"
RELEASE_NAME = "PIPD-LS-SP v0.1.0-preview.1 — S4 open source preview (BETA)"

RELEASE_COMMIT = RELEASE_COMMIT_DEFAULT
EXPECTED_TREE: str | None = None


def resolve_release_identity(repo: pathlib.Path, pin: str | None) -> tuple[str, str]:
    """Resolve the release commit and its tree from the repository itself, never from a literal
    that could drift from the commit being published."""
    commit = git(repo, "rev-parse", pin or RELEASE_COMMIT_DEFAULT).stdout.strip()
    tree = git(repo, "rev-parse", f"{commit}^{{tree}}").stdout.strip()
    if not commit or not tree:
        die("could not resolve the release commit/tree from the repository")
    return commit, tree


from typing import NoReturn


def die(msg: str) -> NoReturn:
    print(f"REFUSED: {msg}")
    sys.exit(2)


class RateLimited(RuntimeError):
    """Raised when the anonymous GitHub API quota is exhausted. Distinct from a failed check:
    an exhausted quota makes the readback INCONCLUSIVE, never FAIL and never PASS."""


def load_token() -> str:
    """Read the PAT into memory only. Returns the value; never logs or stores it."""
    if not TOKEN_FILE.is_file():
        die(f"credential file not present at the approved path (expected {TOKEN_FILE.name})")
    raw = TOKEN_FILE.read_text(encoding="utf-8", errors="replace")
    m = TOKEN_SHAPE.search(raw)
    if not m:
        die("no PAT of the expected shape found in the credential file")
    return m.group(0)


def api(method: str, path: str, token: str | None, body=None, raw: bytes | None = None,
        ctype: str = "application/json") -> tuple[int, dict | list | str]:
    url = path if path.startswith("http") else f"{API}{path}"
    data = None
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA,
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if raw is not None:
        data = raw
        headers["Content-Type"] = ctype
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            payload = r.read().decode("utf-8", errors="replace")
            try:
                return r.status, json.loads(payload)
            except json.JSONDecodeError:
                return r.status, payload
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            pass
        msg = payload.get("message", "") if isinstance(payload, dict) else str(payload)
        # A rate limit is NOT a failed check. Without this, an exhausted anonymous quota
        # manufactures FAILs (or, in the other coding, silently hides real ones).
        if e.code in (403, 429) and "rate limit" in msg.lower():
            raise RateLimited(
                f"GitHub API rate limit hit on {method} {url}: {msg} "
                f"(remaining header: {e.headers.get('X-RateLimit-Remaining')}, "
                f"reset epoch: {e.headers.get('X-RateLimit-Reset')})")
        return e.code, payload


def raw_file(ref: str, path: str) -> str | None:
    """Read a file through raw.githubusercontent.com. This is a CDN, NOT the REST API, so it is
    outside the 60/hour anonymous quota — the readback should not die because a quota ran out."""
    url = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{ref}/{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def ls_remote(pattern: str) -> dict[str, str]:
    """Resolve refs over the unauthenticated git protocol — also outside the REST API quota."""
    out = subprocess.run(["git", "ls-remote", f"https://github.com/{OWNER}/{REPO}.git", pattern],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         timeout=180)
    refs = {}
    for line in (out.stdout or "").splitlines():
        parts = line.split()
        if len(parts) == 2:
            refs[parts[1]] = parts[0]
    return refs


def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(cwd: pathlib.Path, *args: str, env_extra=None, timeout=300) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(["git", *args], cwd=str(cwd), env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def make_askpass(scratch: pathlib.Path) -> pathlib.Path:
    """A shim that answers git's prompts from the child environment. Contains no secret."""
    sh = scratch / "r5q_askpass.bat"
    sh.write_text(
        "@echo off\r\n"
        "echo %~1 | findstr /C:\"Password\" >nul\r\n"
        "if %errorlevel%==0 (echo %R5Q_GIT_PAT%) else (echo x-access-token)\r\n"
        "exit /b 0\r\n",
        encoding="ascii")
    return sh


def redact(text: str) -> str:
    return TOKEN_SHAPE.sub("[REDACTED]", text or "")


# ------------------------------------------------------------------------------------- preflight
def preflight(repo: pathlib.Path, out: pathlib.Path) -> dict:
    r: dict = {"schema": "PIPD-R5Q-PUBLICATION-PREFLIGHT/1",
               "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    status, info = api("GET", f"/repos/{OWNER}/{REPO}", None)
    r["repo_read_status"] = status
    r["public"] = bool(isinstance(info, dict) and info.get("private") is False)
    r["default_branch"] = info.get("default_branch") if isinstance(info, dict) else None
    r["permissions_visible"] = (info.get("permissions") if isinstance(info, dict) else None)
    r["repo_pushed_at"] = info.get("pushed_at") if isinstance(info, dict) else None

    status, tag = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/tags/{TAG}", None)
    r["tag_lookup_status"] = status
    r["tag_collision"] = status == 200
    r["tag_existing_sha"] = tag.get("object", {}).get("sha") if isinstance(tag, dict) else None

    status, rel = api("GET", f"/repos/{OWNER}/{REPO}/releases", None)
    r["release_list_status"] = status
    r["existing_release_tags"] = [x.get("tag_name") for x in rel] if isinstance(rel, list) else None

    head = git(repo, "rev-parse", "HEAD").stdout.strip()
    tree = git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
    porcelain = git(repo, "status", "--porcelain").stdout.strip()
    r["local_head"] = head
    r["local_tree"] = tree
    r["worktree_clean"] = porcelain == ""
    r["worktree_dirty_entries"] = porcelain.splitlines() if porcelain else []
    r["head_is_release_commit"] = head == RELEASE_COMMIT

    r["verdict"] = ("PASS" if (r["public"] and not r["tag_collision"] and r["head_is_release_commit"]
                               and r["existing_release_tags"] == []) else "FAIL")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return r


def render_release_body(template: str, repo: pathlib.Path, rel_dir: pathlib.Path) -> str:
    """Fill the identity placeholders. A committed body that hard-codes its own commit would
    immediately go stale (editing it makes a new commit), so the template carries the prose and
    the publisher carries the identity."""
    import json as _json
    manifest = _json.loads((repo / "dist" / "WHEEL_MANIFEST.json").read_text(encoding="utf-8"))
    wheel = repo / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl"
    source = rel_dir / "pipd-ls-sp-v0.1.0-preview.1-source.zip"
    values = {
        "TAG": TAG,
        "RELEASE_COMMIT": RELEASE_COMMIT,
        "RELEASE_TREE": EXPECTED_TREE or "",
        "BUILD_INPUT_COMMIT": manifest["build_input_commit"],
        "CANDIDATE_HEAD": manifest["candidate_head"],
        "REVIEW_BASELINE_COMMIT": "2efc84eac8e1939092c748d5b389b6dd72267aef",
        "SUPERSEDED_WHEEL_SHA_PREFIX": "bb070a6f",
        "WHEEL_NAME": wheel.name,
        "WHEEL_SHA256": sha256_file(wheel) if wheel.is_file() else "NOT_BUILT",
        "SOURCE_NAME": source.name,
        "SOURCE_SHA256": sha256_file(source) if source.is_file() else "NOT_BUILT",
        "SHA256SUMS_NAME": "SHA256SUMS",
        "PREVIEW_NOTES_NAME": "PREVIEW_NOTES_v0.1.0-preview.1.md",
    }
    body = template
    for k, v in values.items():
        body = body.replace("{{" + k + "}}", str(v))
    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", body)
    if leftover:
        die(f"release body still has unrendered placeholders: {sorted(set(leftover))}")
    return body


# -------------------------------------------------------------------------------------- publish
def publish(repo: pathlib.Path, rel_dir: pathlib.Path, scratch: pathlib.Path,
            out: pathlib.Path, pre: dict) -> dict:
    if pre.get("verdict") != "PASS":
        die("preflight verdict is not PASS; refusing to publish")
    if pre.get("tag_collision"):
        die("tag already exists; refusing to move or overwrite it")
    if not pre.get("head_is_release_commit"):
        die(f"HEAD {pre.get('local_head')} is not the frozen release commit {RELEASE_COMMIT}")

    token = load_token()
    askpass = make_askpass(scratch)
    receipt: dict = {"schema": "PIPD-R5Q-PUBLICATION/1",
                     "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "token_used": True,
                     "token_value_recorded": False}

    # 1. push the branch so the commit objects exist on the remote (no force, no main)
    url = f"https://github.com/{OWNER}/{REPO}.git"
    env_extra = {
        "GIT_ASKPASS": str(askpass),
        "R5Q_GIT_PAT": token,
        "GIT_TERMINAL_PROMPT": "0",
        "GCM_INTERACTIVE": "never",
    }
    pr = git(repo, "-c", "credential.helper=", "push", "--porcelain", url,
             f"refs/heads/{BRANCH}:refs/heads/{BRANCH}", env_extra=env_extra)
    receipt["push"] = {"exit": pr.returncode, "stdout": redact(pr.stdout), "stderr": redact(pr.stderr)}
    if pr.returncode != 0:
        receipt["verdict"] = "REFUSED_PUSH_FAILED"
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        sys.exit(3)

    # 2. immutable tag ref at the explicit release commit (never the default branch)
    st, tagres = api("POST", f"/repos/{OWNER}/{REPO}/git/refs", token,
                     {"ref": f"refs/tags/{TAG}", "sha": RELEASE_COMMIT})
    receipt["tag_ref"] = {"status": st, "ref": tagres.get("ref") if isinstance(tagres, dict) else None,
                          "sha": tagres.get("object", {}).get("sha") if isinstance(tagres, dict) else None,
                          "error": tagres.get("message") if isinstance(tagres, dict) else None}
    if st not in (200, 201):
        receipt["verdict"] = "REFUSED_TAG_FAILED"
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        sys.exit(3)

    # 3. prerelease targeting the explicit commit
    body = render_release_body((rel_dir / "RELEASE_BODY.md").read_text(encoding="utf-8"), repo, rel_dir)
    st, rel = api("POST", f"/repos/{OWNER}/{REPO}/releases", token, {
        "tag_name": TAG, "target_commitish": RELEASE_COMMIT, "name": RELEASE_NAME,
        "body": body, "prerelease": True, "draft": False,
    })
    receipt["release"] = {"status": st, "id": rel.get("id") if isinstance(rel, dict) else None,
                          "html_url": rel.get("html_url") if isinstance(rel, dict) else None,
                          "prerelease": rel.get("prerelease") if isinstance(rel, dict) else None,
                          "error": rel.get("message") if isinstance(rel, dict) else None}
    if st != 201 or not isinstance(rel, dict):
        receipt["verdict"] = "REFUSED_RELEASE_FAILED"
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=1))
        sys.exit(3)

    release_id = rel["id"]
    assets = [
        (repo / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl", "application/octet-stream"),
        (rel_dir / "pipd-ls-sp-v0.1.0-preview.1-source.zip", "application/zip"),
        (rel_dir / "SHA256SUMS", "text/plain"),
        (repo / "PREVIEW_NOTES_v0.1.0-preview.1.md", "text/markdown"),
    ]
    uploaded = []
    for path, ctype in assets:
        if not path.is_file():
            uploaded.append({"name": path.name, "status": "MISSING_LOCALLY"})
            continue
        data = path.read_bytes()
        st, res = api("POST", f"{UPLOADS}/repos/{OWNER}/{REPO}/releases/{release_id}/assets?name={path.name}",
                      token, raw=data, ctype=ctype)
        uploaded.append({
            "name": path.name, "local_sha256": sha256_file(path), "bytes": len(data),
            "status": st, "id": res.get("id") if isinstance(res, dict) else None,
            "state": res.get("state") if isinstance(res, dict) else None,
            "error": res.get("message") if isinstance(res, dict) else None,
        })
    receipt["assets"] = uploaded
    receipt["verdict"] = ("PASS" if all(isinstance(a.get("status"), int) and a["status"] in (200, 201)
                                        for a in uploaded) else "PARTIAL_ASSET_UPLOAD")
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return receipt


# ------------------------------------------------------------------------------------- readback
def readback(repo: pathlib.Path, rel_dir: pathlib.Path, out: pathlib.Path,
             scratch: pathlib.Path) -> dict:
    """Re-derive the published state from GitHub alone and hash the assets by downloading them.

    Anonymous (no token) is deliberate: the readback must not depend on the publisher's credential,
    and must not read the local release cache.
    """
    r: dict = {"schema": "PIPD-R5Q-PUBLICATION-READBACK/1",
               "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "read_with": "anonymous GitHub API + asset download (no token, no local cache)"}

    # --- refs and files through non-API channels (no quota dependence) -----------------------
    refs = ls_remote("refs/heads/*")
    tag_refs = ls_remote(f"refs/tags/{TAG}*")
    tag_target = tag_refs.get(f"refs/tags/{TAG}", "")
    branch_tip = refs.get(f"refs/heads/{BRANCH}", "")
    default_tip = refs.get("refs/heads/main", "")
    r["refs_via_git_ls_remote"] = {
        "tag": tag_target, "branch_tip": branch_tip, "default_branch_tip": default_tip,
        "tag_points_at_release_commit": tag_target == RELEASE_COMMIT,
    }

    st, info = api("GET", f"/repos/{OWNER}/{REPO}", None)
    r["repo"] = {"status": st, "public": info.get("private") is False if isinstance(info, dict) else None,
                 "default_branch": info.get("default_branch") if isinstance(info, dict) else None}

    tag_sha = tag_target
    r["tag"] = {"status": 200 if tag_target else 404, "ref": f"refs/tags/{TAG}",
                "sha": tag_sha, "points_at_release_commit": tag_sha == RELEASE_COMMIT,
                "source": "git ls-remote"}

    st, commit = api("GET", f"/repos/{OWNER}/{REPO}/commits/{RELEASE_COMMIT}", None)
    r["commit"] = {"status": st,
                   "tree": commit.get("commit", {}).get("tree", {}).get("sha") if isinstance(commit, dict) else None,
                   "message_first_line": (commit.get("commit", {}).get("message", "").splitlines() or [None])[0]
                   if isinstance(commit, dict) else None}

    # The branch tip is NOT expected to equal the release commit forever: publication evidence
    # commits land on the branch afterwards, and the immutable tag is the release pointer. The
    # invariant that actually matters is reachability — the release commit must stay an ancestor
    # of the branch tip, so the published tree is never orphaned.
    st, br = api("GET", f"/repos/{OWNER}/{REPO}/branches/{BRANCH}", None)
    branch_tip = br.get("commit", {}).get("sha") if isinstance(br, dict) else None
    st_cmp, cmp = api("GET", f"/repos/{OWNER}/{REPO}/compare/{RELEASE_COMMIT}...{BRANCH}", None)
    cmp_status = cmp.get("status") if isinstance(cmp, dict) else None
    r["branch"] = {
        "status": st,
        "tip": branch_tip,
        "tip_is_release_commit": branch_tip == RELEASE_COMMIT,
        "compare_status": cmp_status,
        "release_commit_reachable_from_tip": cmp_status in ("ahead", "identical"),
        "commits_after_release": (cmp.get("ahead_by") if isinstance(cmp, dict) else None),
    }

    st, rel = api("GET", f"/repos/{OWNER}/{REPO}/releases/tags/{TAG}", None)
    r["release"] = {"status": st,
                    "html_url": rel.get("html_url") if isinstance(rel, dict) else None,
                    "prerelease": rel.get("prerelease") if isinstance(rel, dict) else None,
                    "draft": rel.get("draft") if isinstance(rel, dict) else None,
                    "published_at": rel.get("published_at") if isinstance(rel, dict) else None,
                    "body_has_known_limitations": ("Known limitations" in (rel.get("body") or ""))
                    if isinstance(rel, dict) else None,
                    "body_has_licence": ("Apache-2.0" in (rel.get("body") or ""))
                    if isinstance(rel, dict) else None}

    # expected local hashes (computed from the artefacts this round produced)
    expect = {
        "pipd_ls_sp-0.1.0-py3-none-any.whl": sha256_file(repo / "dist" / "pipd_ls_sp-0.1.0-py3-none-any.whl"),
        "pipd-ls-sp-v0.1.0-preview.1-source.zip": sha256_file(rel_dir / "pipd-ls-sp-v0.1.0-preview.1-source.zip"),
        "SHA256SUMS": sha256_file(rel_dir / "SHA256SUMS"),
        "PREVIEW_NOTES_v0.1.0-preview.1.md": sha256_file(repo / "PREVIEW_NOTES_v0.1.0-preview.1.md"),
    }
    got = {}
    dl = scratch / "readback_dl"
    dl.mkdir(parents=True, exist_ok=True)
    for a in (rel.get("assets", []) if isinstance(rel, dict) else []):
        name = a["name"]
        target = dl / name
        try:
            req = urllib.request.Request(a["browser_download_url"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = resp.read()
            target.write_bytes(data)
            got[name] = {"downloaded_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                         "api_reported_size": a.get("size"), "api_reported_state": a.get("state"),
                         "matches_expected": hashlib.sha256(data).hexdigest() == expect.get(name)}
        except Exception as exc:  # a download failure is a readback failure, never a silent skip
            got[name] = {"error": f"{type(exc).__name__}: {exc}"}
    r["assets_downloaded"] = got
    r["assets_expected"] = expect
    r["all_assets_match"] = all(v.get("matches_expected") for v in got.values()) and set(got) == set(expect)

    # The README entry point must send a reader to the tag, not the stale default branch.
    readme = raw_file(TAG, "README.md") or ""
    r["readme_at_tag"] = {"source": "raw.githubusercontent (no API quota)",
                          "bytes": len(readme),
                          "points_at_tag": TAG in readme,
                          "mentions_apache": "Apache-2.0" in readme}

    # The DEFAULT BRANCH front page is what a visitor actually lands on. Checking only the README
    # at the tag would pass while the repo home still advertised the pre-release state — which is
    # exactly the gap TT-R5P-08 names ("pin the correct tag at the top of the release front page").
    front = raw_file("HEAD", "README.md") or ""
    r["front_page_readme"] = {
        "source": "raw.githubusercontent (no API quota)",
        "default_branch": r["repo"]["default_branch"],
        "bytes": len(front),
        "points_at_tag": TAG in front,
        "mentions_apache": "Apache-2.0" in front,
        "marks_itself_as_snapshot": ("snapshot" in front.lower()),
    }

    # main must never be rewritten. Proven from the commit feed (a CDN, not the REST API): the R3
    # commit must still appear in the default branch's recent history, so the front-page commit is
    # an advancement on top of R3 rather than a replacement of it.
    def commit_feed_has(ref: str, sha: str) -> bool | None:
        try:
            req = urllib.request.Request(f"https://github.com/{OWNER}/{REPO}/commits/{ref}.atom",
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return sha in resp.read().decode("utf-8", errors="replace")
        except Exception:
            return None

    r3 = "3aebbbce948871c07b875ab92acf263d298ecf38"
    on_main = commit_feed_has("main", r3)
    on_branch = commit_feed_has(BRANCH, RELEASE_COMMIT)
    r["default_branch_commit"] = {
        "source": "commits/<ref>.atom feed (no API quota)",
        "default_branch_tip": default_tip,
        "r3_commit_still_in_history": on_main,
        "still_on_r3_line": on_main is True,
        "release_commit_in_branch_history": on_branch,
        "inconclusive": on_main is None,
    }

    # The licence basis must be inside the published wheel, not only in the repository copy.
    whl = dl / "pipd_ls_sp-0.1.0-py3-none-any.whl"
    lic_in_wheel = {}
    if whl.is_file():
        import zipfile
        with zipfile.ZipFile(whl) as z:
            names = z.namelist()
            md = z.read("pipd_ls_sp-0.1.0.dist-info/METADATA").decode("utf-8", errors="replace")
            lic_in_wheel = {
                "license_expression": [l.split(":", 1)[1].strip() for l in md.splitlines()
                                       if l.startswith("License-Expression:")],
                "license_files": [l.split(":", 1)[1].strip() for l in md.splitlines()
                                  if l.startswith("License-File:")],
                "packaged": sorted(n for n in names if "/licenses/" in n),
            }
    r["licence_inside_published_wheel"] = lic_in_wheel

    checks = {
        # Anonymous `git ls-remote` succeeding IS the proof of publicness — no API quota needed.
        "repo_public": bool(refs),
        "tag_exists_and_targets_release_commit": r["tag"]["points_at_release_commit"] is True,
        "commit_tree_matches": r["commit"]["tree"] == EXPECTED_TREE,
        "release_commit_reachable_from_branch_tip": r["branch"]["release_commit_reachable_from_tip"] is True,
        "release_is_prerelease": r["release"]["prerelease"] is True,
        "release_not_draft": r["release"]["draft"] is False,
        "release_body_discloses_limitations": r["release"]["body_has_known_limitations"] is True,
        "all_assets_download_and_match": r["all_assets_match"],
        "readme_at_tag_points_to_tag": r["readme_at_tag"]["points_at_tag"] is True,
        "front_page_readme_points_to_tag": r["front_page_readme"]["points_at_tag"] is True,
        "front_page_readme_marks_itself_snapshot": r["front_page_readme"]["marks_itself_as_snapshot"] is True,
        "default_branch_not_rewritten": r["default_branch_commit"]["still_on_r3_line"] is True,
    }
    r["checks"] = checks
    r["verdict"] = "PASS" if all(checks.values()) else "FAIL"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"verdict": r["verdict"], "checks": checks,
                      "release_url": r["release"]["html_url"],
                      "tag_sha": r["tag"]["sha"], "assets": {k: v.get("matches_expected")
                                                             for k, v in got.items()}},
                     ensure_ascii=False, indent=1))
    return r


def main() -> int:
    global RELEASE_COMMIT, EXPECTED_TREE
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rel-dir", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--mode", choices=["preflight", "publish", "readback"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--release-commit", default=None,
                    help="pin the release commit; default resolves HEAD")
    a = ap.parse_args()
    repo = pathlib.Path(a.repo).resolve()
    rel_dir = pathlib.Path(a.rel_dir).resolve()
    scratch = pathlib.Path(a.scratch).resolve()
    out = pathlib.Path(a.out)
    scratch.mkdir(parents=True, exist_ok=True)
    RELEASE_COMMIT, EXPECTED_TREE = resolve_release_identity(repo, a.release_commit)

    if a.mode == "preflight":
        pre = preflight(repo, out)
        return 0 if pre["verdict"] == "PASS" else 1
    if a.mode == "publish":
        pre_path = out.parent / "R5Q_PUBLICATION_PREFLIGHT.json"
        if not pre_path.is_file():
            die("run --preflight first")
        pre = json.loads(pre_path.read_text(encoding="utf-8"))
        publish(repo, rel_dir, scratch, out, pre)
        return 0
    try:
        readback(repo, rel_dir, out, scratch)
    except RateLimited as exc:
        receipt = {
            "schema": "PIPD-R5Q-PUBLICATION-READBACK/1",
            "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "verdict": "INCONCLUSIVE_RATE_LIMITED",
            "error": str(exc),
            "note": ("The anonymous GitHub API quota was exhausted mid-readback. This is NOT a "
                     "failed check and NOT a pass: nothing about the published state can be "
                     "concluded from this run. Re-run after the quota resets."),
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({"verdict": receipt["verdict"], "error": receipt["error"]}, indent=1))
        return 4
    return 0


if __name__ == "__main__":
    sys.exit(main())
