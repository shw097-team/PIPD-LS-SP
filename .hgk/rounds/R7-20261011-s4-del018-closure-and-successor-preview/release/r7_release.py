#!/usr/bin/env python3
"""R7 successor preview driver: stage, publish, read back.

Publishes an immutable tag + prerelease carrying the CE-1/CE-2 repair, under the owner grant already
on record (OWNER_LICENSE_GRANT_R5Q.json): action=create_new_immutable_tag_and_prerelease,
target=explicit release commit, prerelease=true, forbidden = overwrite main / force-push / move or
delete an existing tag / create a second repo.

Credential handling: the token is read from the credential file into process memory only and handed
to nothing but the Authorization header. It is never written to argv, stdout, a log, the release
body, git config or any asset. Nothing here prints it.

Modes:
  --stage     build the local release assets only (source zip, SHA256SUMS, notes, body). No network.
  --publish   push the tag ref and create the prerelease with its assets. Requires the token.
  --readback  ANONYMOUS re-derivation of the published subject (no token): resolve the tag, list the
              release assets, download each, recompute sha256 and compare against the staged values.
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
import urllib.error
import urllib.request

OWNER = "shw097-team"
REPO = "PIPD-LS-SP"
TAG = "v0.1.0-preview.2"
RELEASE_NAME = "v0.1.0-preview.2 - repaired preview (successor to v0.1.0-preview.1)"
SUPERSEDED_TAG = "v0.1.0-preview.1"
TOKEN_FILE = pathlib.Path(r"C:/Projects/Agent_Workspace/API KEY/Fine-grained personal access tokens.txt")
WHEEL = "pipd_ls_sp-0.1.0-py3-none-any.whl"
SOURCE_ZIP = f"pipd-ls-sp-{TAG}-source.zip"
NOTES = f"PREVIEW_NOTES_{TAG}.md"

RELEASE_BODY = """# PIPD-LS-SP {tag}

**This is a repaired successor to `{superseded}`, not a rewrite of it.** `{superseded}` is left
exactly as published; this tag supersedes it, as the owner grant requires.

## What is in these bytes

| | |
|---|---|
| Wheel | `{wheel}` |
| Wheel sha256 | `{wheel_sha}` |
| Built from commit | `{build_input}` |
| Licence | Apache-2.0 |

## What changed relative to {superseded}

`{superseded}` shipped with two defects that made the core chain unusable from an installed wheel
outside the source tree. Both are repaired in these bytes:

1. **CE-1 - `validate` could not find the schemas it shipped with.** Schema resolution is now
   `OVERRIDE -> INSTALLED -> SOURCE`, so a wheel installed into a clean virtual environment resolves
   the schemas packaged *inside the wheel* and reports where it found them.
2. **CE-2 - the compilers' own stdout was not schema-valid.** A non-record sidecar
   (`_profile_meta`) was being emitted into records the schemas reject. The hash-exclusion set and
   the stripped-sidecar set are now separate, so the compilers' own stdout validates.
3. **CE-CODEX-TRACE-WIDENING** - an undeclared `trace` key was accepted on `PD-PKG`/`ECP`/`TQAEP`.
   It is now rejected by `additionalProperties` and named in the findings.

The wheel bytes themselves were unchanged between {superseded} and this tag for the packaging layer;
what changed is the library code inside it.

## DEL-018 is closed in this tree

`RELEASE_MANIFEST@1` had failed since the R3 crosswalk: the publication projection carried no
disposition for every product path in the tree. It now dispositions 252/252 with zero violations and
`--check --current` exits 0. The regeneration removed 1085 stale `.hgk/` round-artifact entries and
**no product path**; that is asserted mechanically, because a manifest that covers less would also
pass.

## Claim ceiling - read this before quoting anything here

Published capability: `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`.

This is **not** a full gate pass. Not granted, and must not be quoted as granted:
`FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`, `S5_RUNTIME_READY`,
`ALL_HOSTS_LIVE_CERTIFIED`. No release signature or build attestation by an external signing
identity is attached, and no host-native (S5-S8) certification has been performed.

## Known limitations

1. The preview is an S4-stage open-source preview, not a production release.
2. DEL-018 is closed in this tree; the superseded tag's failure remains on record against it.
3. The default publication attestation sidecar in the tree attests an R3-era subject, not this tag.
4. No dependency-vulnerability scan result is claimed for this tag beyond the factory scans below.
5. `pip install` from PyPI is not offered; take the wheel from this release and verify its hash.
6. Windows-first: the tooling is verified on Windows with CPython 3.11; other hosts are untested.
7. The `Doctor`/composition surfaces remain the documented S0-S4 scope, not the full S5-S8 chain.

## Factory evidence carried with this tag

- history secret scan over 2339 objects and the worktree: 0 hits, CLEAN
- deny-list scan: PASS, 0 writer usages inside the R4 scope
- full test suite on the release tree: see the round record
- licence: Apache-2.0, with the corpus-derived vs agent-authored split kept in `NOTICE`
"""


def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_token() -> str:
    raw = TOKEN_FILE.read_text(encoding="utf-8-sig")
    toks = re.findall(r"[A-Za-z0-9_\-]{20,}", raw)
    if not toks:
        raise SystemExit("no token found in the credential file")
    return max(toks, key=len)


def api(method: str, path: str, token: str | None, body=None, raw: bytes | None = None,
        ctype: str | None = None):
    url = path if path.startswith("http") else f"https://api.github.com{path}"
    data = None
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "pipd-r7"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    elif raw is not None:
        data = raw
        headers["Content-Type"] = ctype or "application/octet-stream"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:  # noqa: S310
            payload = resp.read()
            return resp.status, (json.loads(payload) if payload.strip().startswith(b"{") else payload)
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()[:400].decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001 - record, never hide
        return 0, f"{type(exc).__name__}: {exc}"


def git(repo: pathlib.Path, *args: str, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(["git", *args], cwd=str(repo), env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=600)


def make_askpass(scratch: pathlib.Path) -> pathlib.Path:
    """A shim that answers git's prompts from the child environment. Contains no secret."""
    sh = scratch / "askpass.sh"
    sh.write_text(
        "#!/bin/sh\n"
        "case \"$1\" in\n"
        "  *Username*) echo x-access-token ;;\n"
        "  *) echo \"${R7_GIT_PAT}\" ;;\n"
        "esac\n", encoding="utf-8", newline="\n")
    sh.chmod(0o700)
    return sh


def release_commit(repo: pathlib.Path) -> str:
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def stage(repo: pathlib.Path, rel: pathlib.Path) -> dict:
    rel.mkdir(parents=True, exist_ok=True)
    commit = release_commit(repo)
    wheel = repo / "dist" / WHEEL
    wheel_sha = sha256_file(wheel)
    manifest = json.loads((repo / "dist" / "WHEEL_MANIFEST.json").read_text(encoding="utf-8"))

    # source archive at the release commit
    src = rel / SOURCE_ZIP
    with open(src, "wb") as fh:
        proc = subprocess.run(["git", "archive", "--format=zip", f"--prefix=pipd-ls-sp-{TAG}/", commit],
                              cwd=str(repo), stdout=fh, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit(f"git archive failed: {proc.stderr[:300]!r}")

    notes = repo / NOTES
    notes.write_text(RELEASE_BODY.format(
        tag=TAG, superseded=SUPERSEDED_TAG, wheel=WHEEL, wheel_sha=wheel_sha,
        build_input=manifest["build_input_commit"], release_commit=commit),
        encoding="utf-8", newline="\n")
    body = RELEASE_BODY.format(
        tag=TAG, superseded=SUPERSEDED_TAG, wheel=WHEEL, wheel_sha=wheel_sha,
        build_input=manifest["build_input_commit"], release_commit=commit)

    lines = []
    for name, path in ((WHEEL, wheel), (SOURCE_ZIP, src), (NOTES, notes)):
        lines.append(f"{sha256_file(path)}  {name}")
    sums = rel / "SHA256SUMS"
    sums.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    (rel / "RELEASE_BODY.md").write_text(body, encoding="utf-8", newline="\n")
    state = {
        "tag": TAG, "superseded_tag": SUPERSEDED_TAG, "release_commit": commit,
        "wheel": WHEEL, "wheel_sha256": wheel_sha,
        "wheel_build_input_commit": manifest["build_input_commit"],
        "assets": {n: sha256_file(p) for n, p in
                   ((WHEEL, wheel), (SOURCE_ZIP, src), ("SHA256SUMS", sums), (NOTES, notes))},
    }
    (rel / "STAGED.json").write_text(json.dumps(state, ensure_ascii=False, indent=1),
                                     encoding="utf-8", newline="")
    return state


def publish(repo: pathlib.Path, rel: pathlib.Path, scratch: pathlib.Path) -> dict:
    state = json.loads((rel / "STAGED.json").read_text(encoding="utf-8"))
    token = load_token()
    out: dict = {"tag": TAG, "release_commit": state["release_commit"],
                 "token_used": bool(token), "token_value_recorded": False, "steps": []}

    # collision check before anything is created
    st, existing = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/tags/{TAG}", token)
    out["steps"].append({"collision_check": st})
    if st == 200:
        out["verdict"] = "REFUSED_TAG_EXISTS"
        return out
    st, sup = api("GET", f"/repos/{OWNER}/{REPO}/git/ref/tags/{SUPERSEDED_TAG}", None)
    sup_sha = sup.get("object", {}).get("sha") if isinstance(sup, dict) else None
    out["superseded_tag_sha256_before"] = sup_sha

    # create the tag ref (immutable: never updated afterwards)
    st, ref = api("POST", f"/repos/{OWNER}/{REPO}/git/refs", token,
                  {"ref": f"refs/tags/{TAG}", "sha": state["release_commit"]})
    out["steps"].append({"create_ref": st})
    if st not in (200, 201):
        out["verdict"] = "REFUSED_TAG_CREATE_FAILED"
        out["detail"] = ref
        return out

    body = (rel / "RELEASE_BODY.md").read_text(encoding="utf-8")
    st, relobj = api("POST", f"/repos/{OWNER}/{REPO}/releases", token,
                     {"tag_name": TAG, "target_commitish": state["release_commit"],
                      "name": RELEASE_NAME, "body": body, "prerelease": True, "draft": False})
    out["steps"].append({"create_release": st})
    if st not in (200, 201):
        out["verdict"] = "REFUSED_RELEASE_CREATE_FAILED"
        out["detail"] = relobj
        return out
    rel_id = relobj["id"]
    out["release_id"] = rel_id

    assets = [(repo / "dist" / WHEEL, "application/octet-stream"),
              (rel / SOURCE_ZIP, "application/zip"),
              (rel / "SHA256SUMS", "text/plain"),
              (repo / NOTES, "text/markdown")]
    uploaded = {}
    for path, ctype in assets:
        st, res = api("POST",
                      f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{rel_id}/assets?name={path.name}",
                      token, raw=path.read_bytes(), ctype=ctype)
        uploaded[path.name] = st
    out["uploaded"] = uploaded
    out["verdict"] = "PUBLISHED" if all(v in (200, 201) for v in uploaded.values()) else "PARTIAL_UPLOAD"
    return out


def readback(repo: pathlib.Path, rel: pathlib.Path, scratch: pathlib.Path) -> dict:
    """ANONYMOUS: no token anywhere in this path."""
    state = json.loads((rel / "STAGED.json").read_text(encoding="utf-8"))
    r: dict = {"tag": TAG, "mode": "ANONYMOUS", "token_used": False}

    refs = git(repo, "ls-remote", f"https://github.com/{OWNER}/{REPO}.git", f"refs/tags/{TAG}*")
    tag_lines = [ln.split("\t") for ln in refs.stdout.strip().splitlines() if ln.strip()]
    r["tag_resolves"] = bool(tag_lines)
    r["tag_refs"] = [{"sha": a, "ref": b} for a, b in tag_lines]
    peeled = [a for a, b in tag_lines if b == f"refs/tags/{TAG}"]

    st, relobj = api("GET", f"/repos/{OWNER}/{REPO}/releases/tags/{TAG}", None)
    r["release_status"] = st
    if st != 200:
        r["verdict"] = "INCONCLUSIVE_RELEASE_UNREADABLE"
        return r
    r["prerelease"] = relobj.get("prerelease")
    r["draft"] = relobj.get("draft")
    r["body_has_claim_ceiling"] = "G_RELEASE_FULL_PASS" in (relobj.get("body") or "")
    r["body_has_known_limitations"] = "Known limitations" in (relobj.get("body") or "")

    ok, bad = {}, {}
    for a in relobj.get("assets", []):
        name = a["name"]
        req = urllib.request.Request(a["browser_download_url"],
                                     headers={"User-Agent": "pipd-r7-readback"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:  # noqa: S310
                blob = resp.read()
        except Exception as exc:  # noqa: BLE001
            bad[name] = f"{type(exc).__name__}: {exc}"
            continue
        got = hashlib.sha256(blob).hexdigest()
        want = state["assets"].get(name)
        if want is None:
            ok[name] = {"downloaded_sha256": got, "staged_sha256": None, "match": None}
        elif got == want:
            ok[name] = {"downloaded_sha256": got, "match": True}
        else:
            bad[name] = {"downloaded_sha256": got, "staged_sha256": want, "match": False}
    r["assets_verified"] = ok
    r["assets_failed"] = bad
    r["tag_points_at_release_commit"] = (peeled[0] == state["release_commit"]) if peeled else None
    r["superseded_tag_still_present"] = "refs/tags/" + SUPERSEDED_TAG in refs.stdout
    r["verdict"] = ("PASS" if ok and not bad and r["tag_points_at_release_commit"]
                    else "FAIL_OR_INCOMPLETE")
    return r


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=pathlib.Path)
    ap.add_argument("--release-dir", required=True, type=pathlib.Path)
    ap.add_argument("--scratch", required=True, type=pathlib.Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--stage", action="store_true")
    g.add_argument("--publish", action="store_true")
    g.add_argument("--readback", action="store_true")
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)

    if args.stage:
        print(json.dumps(stage(args.repo, args.release_dir), ensure_ascii=False, indent=1))
        return 0
    if args.publish:
        res = publish(args.repo, args.release_dir, args.scratch)
        (args.release_dir / "PUBLISH_RECEIPT.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0 if res.get("verdict") == "PUBLISHED" else 1
    res = readback(args.repo, args.release_dir, args.scratch)
    (args.release_dir / "READBACK.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if res.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
