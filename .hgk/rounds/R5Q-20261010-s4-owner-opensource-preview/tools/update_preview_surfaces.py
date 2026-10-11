"""Refresh the MUTABLE published surfaces of v0.1.0-preview.1 from the repository.

Only two things move here, and both are mutable by design:
  1. the live release body, re-rendered from release/RELEASE_BODY.md
  2. the PREVIEW_NOTES asset, re-uploaded from the repository copy

Nothing immutable is touched: no tag, no commit, no tree, no wheel. The script prints what it
changed and then re-downloads both surfaces to compare them against the local files, so the claim
"the live surface matches the repository" is evidenced rather than asserted.

  python update_preview_surfaces.py <repo-root>
"""
import hashlib
import importlib.util
import pathlib
import sys

ROUND = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("r5qp", ROUND / "tools" / "r5q_publish.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    repo = pathlib.Path(sys.argv[1]).resolve()
    rel_dir = ROUND / "release"
    # HEAD has moved past the release commit many times. Without this pin the rendered body would
    # advertise whatever commit happens to be checked out, which is exactly the drift the
    # build_input_commit/released_commit split exists to prevent.
    if len(sys.argv) > 2:
        m.RELEASE_COMMIT = sys.argv[2]
    token = m.load_token()

    st, rel = m.api("GET", f"/repos/{m.OWNER}/{m.REPO}/releases/tags/{m.TAG}", token)
    if st != 200 or not isinstance(rel, dict):
        return m.die(f"cannot read the release: {st} {rel}")
    rid = rel["id"]
    print(f"release id={rid} tag={rel['tag_name']} prerelease={rel['prerelease']} draft={rel['draft']}")

    # ---------------------------------------------------------------- body ----
    template = (rel_dir / "RELEASE_BODY.md").read_text(encoding="utf-8")
    body = m.render_release_body(template, repo, rel_dir)
    if "{{" in body:
        return m.die("the rendered body still contains template placeholders")
    st, out = m.api("PATCH", f"/repos/{m.OWNER}/{m.REPO}/releases/{rid}", token, body={"body": body})
    if st != 200:
        return m.die(f"body PATCH failed: {st} {out}")
    print(f"body  PATCH {st}: {len(body)} chars; live now {len(out.get('body', ''))} chars")
    for probe in ("independent acceptance", "not touched", "untouched"):
        print(f"       contains {probe!r}: {probe in out.get('body', '')}")

    # ---------------------------------------------------------------- asset ---
    name = "PREVIEW_NOTES_v0.1.0-preview.1.md"
    local = repo / name
    want = sha(local.read_bytes())
    existing = [a for a in rel.get("assets", []) if a["name"] == name]
    if not existing:
        return m.die(f"asset {name} is not attached to the release — refusing to guess")
    aid = existing[0]["id"]
    if existing[0].get("digest") == f"sha256:{want}":
        print(f"asset already current ({want[:16]}…); not re-uploading")
    else:
        st, out = m.api("DELETE", f"/repos/{m.OWNER}/{m.REPO}/releases/assets/{aid}", token)
        if st not in (204, 200):
            return m.die(f"asset delete failed: {st} {out}")
        url = (f"{m.UPLOADS}/repos/{m.OWNER}/{m.REPO}/releases/{rid}/assets?name={name}")
        st, out = m.api("POST", url, token, raw=local.read_bytes(), ctype="text/markdown")
        if st not in (200, 201):
            return m.die(f"asset upload failed: {st} {out}")
        print(f"asset  re-uploaded {st}: id={out.get('id')} digest={out.get('digest')}")

    # ------------------------------------------------------------- readback ---
    st, rel2 = m.api("GET", f"/repos/{m.OWNER}/{m.REPO}/releases/tags/{m.TAG}", token)
    live_body = rel2.get("body", "")
    a2 = [a for a in rel2.get("assets", []) if a["name"] == name][0]
    print("\n--- verification against the LIVE surface ---")
    print(f"body matches local render : {live_body == body}")
    print(f"asset digest matches local: {a2.get('digest') == 'sha256:' + want}  ({a2.get('digest')})")
    print(f"asset size                : {a2.get('size')} == {local.stat().st_size} "
          f"-> {a2.get('size') == local.stat().st_size}")
    ok = live_body == body and a2.get("digest") == "sha256:" + want
    print(f"\nSURFACES_CURRENT: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
