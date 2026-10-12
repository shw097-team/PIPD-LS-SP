#!/usr/bin/env python3
"""S4R2M Gate M4 — publish the preview.3 release, then read every asset back anonymously.

Security contract (same as tools/github_publish.py, which it deliberately mirrors):
  * the credential is read from one known file, inside this process only;
  * it never reaches argv, stdout, stderr, a log, a URL or any artefact;
  * only non-sensitive codes are printed.
  * the credential source is overridable with HGK_CRED_FILE, because the hard-coded default in
    this repository points at a long-dead token (recorded as TT-S4R2M-CREDSRC-01).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG, REPO = "shw097-team", "PIPD-LS-SP"
API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
TAG = "v0.1.1-preview.3"
DEFAULT_CRED = Path(r"C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt")

ROUND = Path(__file__).resolve().parent
ASSETS = [
    "pipd_ls_sp-0.1.1a3-py3-none-any.whl",
    "PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip",
    "pipd-ls-sp-v0.1.1-preview.3-source.zip",
    "PREVIEW_NOTES_v0.1.1-preview.3.md",
    "SHA256SUMS",
]


def load_token() -> str | None:
    src = Path(os.environ.get("HGK_CRED_FILE") or DEFAULT_CRED)
    if not src.is_file():
        return None
    data = src.read_bytes()
    m = (re.search(rb"github_pat_[A-Za-z0-9_]{20,}", data)
         or re.search(rb"gh[pousr]_[A-Za-z0-9]{20,}", data))
    return m.group(0).decode("ascii") if m else None


def call(url: str, token: str, method: str = "GET", body=None, raw: bytes | None = None,
         ctype: str = "application/json"):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "hgk-release-lane")
    if data is not None:
        req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            payload = r.read()
            return r.status, (json.loads(payload) if payload else {})
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        return e.code, {"error": detail}
    except Exception as e:  # noqa: BLE001
        return 0, {"error": f"{type(e).__name__}: {e}"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--replace", nargs="*", default=[],
                    help="asset names to delete and re-upload (a published asset is immutable, so "
                         "correcting one is an explicit, recorded act — never a silent overwrite)")
    args = ap.parse_args()
    replace = set(args.replace)

    token = load_token()
    if not token:
        print(json.dumps({"verdict": "AUTH_BLOCKED", "reason": "no credential at the configured source"}))
        return 2
    print(json.dumps({"step": "credential", "result": "LOADED", "secret_printed": False}))

    # 1. the tag must already exist and point where we approved
    st, r = call(f"{API}/repos/{ORG}/{REPO}/git/ref/tags/{TAG}", token)
    if st != 200:
        print(json.dumps({"step": "tag", "result": "MISSING", "status": st, "detail": r.get("error", "")[:150]}))
        return 3
    tag_obj_sha, tag_sha = "", ""
    if isinstance(r, dict):
        obj = r.get("object")
        if isinstance(obj, dict):
            tag_obj_sha = str(obj.get("sha") or "")
            tag_sha = tag_obj_sha
            # an annotated tag's object sha is a TAG object, not a commit; target_commitish must be
            # a commit-ish, so peel it (passing the tag object yields an opaque HTTP 500)
            if obj.get("type") == "tag" and tag_sha:
                st2, r2 = call(f"{API}/repos/{ORG}/{REPO}/git/tags/{tag_sha}", token)
                inner = r2.get("object") if isinstance(r2, dict) else None
                if st2 == 200 and isinstance(inner, dict):
                    tag_sha = str(inner.get("sha") or "")
    print(json.dumps({"step": "tag", "result": "FOUND", "tag": TAG,
                      "tag_object": tag_obj_sha, "commit": tag_sha}))

    # 2. create the release (idempotent: reuse if it already exists)
    st, r = call(f"{API}/repos/{ORG}/{REPO}/releases/tags/{TAG}", token)
    if st == 200:
        rel_id = r["id"]
        print(json.dumps({"step": "release", "result": "ALREADY_EXISTS", "id": rel_id}))
    else:
        notes = (ROUND / "PREVIEW_NOTES_v0.1.1-preview.3.md").read_text(encoding="utf-8")
        st, r = call(f"{API}/repos/{ORG}/{REPO}/releases", token, "POST", {
            "tag_name": TAG, "target_commitish": tag_sha,
            "name": f"PIPD-LS-SP v0.1.1-preview.3 (S4 CLI + Skills)",
            "body": notes, "draft": False, "prerelease": True,
        })
        if st not in (200, 201):
            print(json.dumps({"step": "release", "result": "FAILED", "status": st, "detail": str(r)[:300]}))
            return 4
        rel_id = r["id"]
        print(json.dumps({"step": "release", "result": "CREATED", "id": rel_id, "prerelease": True}))

    # 3. upload each asset (skip if the name is already attached — idempotent re-run)
    st, r = call(f"{API}/repos/{ORG}/{REPO}/releases/{rel_id}/assets?per_page=100", token)
    existing = {a["name"]: a["id"] for a in (r if isinstance(r, list) else [])}
    up = []
    for name in ASSETS:
        p = ROUND / name
        if not p.is_file():
            print(json.dumps({"asset": name, "result": "LOCAL_MISSING"})); return 5
        if name in existing:
            if name not in replace:
                up.append({"asset": name, "result": "ALREADY_UPLOADED", "local_sha256": sha256(p)[:16]})
                continue
            # explicit correction: a published asset is immutable, so the old one is deleted (and
            # its id and prior state recorded) before the corrected bytes are uploaded under the
            # same name. This is the only place an existing asset is ever touched.
            old_id = existing[name]
            dst, dr = call(f"{API}/repos/{ORG}/{REPO}/releases/assets/{old_id}", token, "DELETE")
            print(json.dumps({"step": "replace", "asset": name, "deleted_asset_id": old_id,
                              "delete_status": dst}))
            if dst not in (204, 200):
                print(json.dumps({"asset": name, "result": "DELETE_FAILED", "status": dst,
                                  "detail": str(dr)[:200]})); return 6
        st, r = call(f"{UPLOADS}/repos/{ORG}/{REPO}/releases/{rel_id}/assets?name={name}", token,
                     "POST", raw=p.read_bytes(), ctype="application/octet-stream")
        up.append({"asset": name, "result": "UPLOADED" if st in (200, 201) else "FAILED",
                   "status": st, "local_sha256": sha256(p)[:16],
                   "replaced": name in replace,
                   "detail": "" if st in (200, 201) else str(r)[:200]})
        if st not in (200, 201):
            print(json.dumps({"step": "upload", "assets": up}, ensure_ascii=False)); return 6
    print(json.dumps({"step": "upload", "assets": up}, ensure_ascii=False))

    # 4. ANONYMOUS readback, no credential at all, and recompute every digest
    st, r = call(f"{API}/repos/{ORG}/{REPO}/releases/tags/{TAG}", "none", "GET")
    anon = urllib.request.urlopen(
        f"{API}/repos/{ORG}/{REPO}/releases/tags/{TAG}", timeout=60).read()
    rel = json.loads(anon)
    back = []
    for a in rel["assets"]:
        with urllib.request.urlopen(a["browser_download_url"], timeout=300) as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        local = ROUND / a["name"]
        back.append({"asset": a["name"], "anonymous_size": a["size"],
                     "anonymous_sha256": digest,
                     "matches_local": bool(local.is_file() and digest == sha256(local))})
    print(json.dumps({"step": "anonymous_readback", "tag": TAG, "prerelease": rel["prerelease"],
                      "assets": back}, ensure_ascii=False, indent=1))
    ok = all(b["matches_local"] for b in back) and len(back) == len(ASSETS)
    print(json.dumps({"verdict": "RELEASE_VERIFIED" if ok else "RELEASE_HASH_MISMATCH",
                      "assets": len(back), "all_local_match": ok}))
    return 0 if ok else 7


if __name__ == "__main__":
    sys.exit(main())
