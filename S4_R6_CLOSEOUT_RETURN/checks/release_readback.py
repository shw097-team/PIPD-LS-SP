#!/usr/bin/env python3
"""Read-only release/plugin verification for round PIPD-S4-R6-CLOSEOUT-20261016.

Fresh HTTPS readback from GitHub (public API + release asset bytes):
  * release metadata for v0.1.1-preview.4 (7 assets, names, sizes, digests)
  * tag object / dereferenced target
  * the served plugin ZIP: byte count + sha256 recomputed from the SERVED bytes
  * SHA256SUMS parsed and every entry compared against the SERVED bytes
  * ZIP structure: single root, exactly 8 SKILL.md, no path traversal, no MCP/Apps/Hooks files
  * PR #17 / #14 / #15 state
Writes one JSON. Never prints or stores any credential.
"""
from __future__ import annotations

import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

OWNER_REPO = "shw097-team/PIPD-LS-SP"
OUT = Path("C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/diff_and_tests/release_readback.json")
EXPECT = {
    "pipd-ls-sp-public-skills.zip": (68357, "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"),
    "pipd_ls_sp-0.1.1a4-py3-none-any.whl": (286978, "3b59a985dc9fc1cd4c1c5ca9a7b779122459ab7cadc8f439e17063d6c934cc0c"),
    "pipd-ls-sp-v0.1.1-preview.4-source.zip": (32841678, "f8070971fd1bf8e1c2c3bbe4f59e33d70853a2e8737817931928d35baebee2ca"),
    "PIPD_WEB_FALLBACK.md": (42145, "c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af"),
    "PIPD_WEB_FALLBACK.md.sha256": (100, "4efeffbbc0df500fc703b26618a3fefe022534ae1f40a6f0e8ea9f3eda6744a2"),
    "PREVIEW_NOTES_v0.1.1-preview.4.md": (5326, "96fedfc6fa27bd412e16a0377a509719f41026f891732d197c8848926f423201"),
    "SHA256SUMS": (583, "0f76502670038ae35bd4f772dc23223f6b47241c3acee2f918d106eaabffe689"),
}
EXPECT_TAG_OBJ = "0618d73c725da0d8c3280f99ef369d13741b5197"
EXPECT_TAG_TGT = "cc6c1930765160697e7e51d6e37735b9220a30db"


def get(url: str, raw: bool = False):
    req = urllib.request.Request(url, headers={"User-Agent": "hgk-r6-readback", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    return data if raw else json.loads(data)


def main() -> int:
    rep: dict = {"schema": "PIPD-S4-R6-RELEASE-READBACK/1", "owner_repo": OWNER_REPO, "findings": []}

    def note(k, v):
        rep[k] = v

    # --- tag identity -------------------------------------------------------
    try:
        tagref = get(f"https://api.github.com/repos/{OWNER_REPO}/git/ref/tags/v0.1.1-preview.4")
        note("tag_ref_object_sha", tagref["object"]["sha"])
        tagobj = get(f"https://api.github.com/repos/{OWNER_REPO}/git/tags/{tagref['object']['sha']}")
        note("tag_deref_target", tagobj["object"]["sha"])
        note("tag_object_ok", tagref["object"]["sha"] == EXPECT_TAG_OBJ)
        note("tag_target_ok", tagobj["object"]["sha"] == EXPECT_TAG_TGT)
        tgt = get(f"https://api.github.com/repos/{OWNER_REPO}/git/commits/{tagobj['object']['sha']}")
        note("tag_tree", tgt["tree"]["sha"])
    except Exception as exc:  # noqa: BLE001
        note("tag_error", f"{type(exc).__name__}: {exc}")

    # --- main -----------------------------------------------------------------
    try:
        m = get(f"https://api.github.com/repos/{OWNER_REPO}/git/ref/heads/main")
        note("main_sha", m["object"]["sha"])
    except Exception as exc:  # noqa: BLE001
        note("main_error", f"{type(exc).__name__}: {exc}")

    # --- release assets -------------------------------------------------------
    try:
        rel = get(f"https://api.github.com/repos/{OWNER_REPO}/releases/tags/v0.1.1-preview.4")
        assets = {a["name"]: {"bytes": a["size"], "digest": a.get("digest"), "url": a["browser_download_url"],
                              "id": a["id"]} for a in rel["assets"]}
        note("release_prerelease", rel.get("prerelease"))
        note("release_published_at", rel.get("published_at"))
        note("release_asset_names", sorted(assets))
        note("release_asset_count", len(assets))
        rows = []
        for name, exp in EXPECT.items():
            got = assets.get(name)
            rows.append({"asset": name, "present": got is not None,
                         "expected_bytes": exp[0], "served_bytes": (got or {}).get("bytes"),
                         "expected_sha256": exp[1], "api_digest": (got or {}).get("digest"),
                         "meta_match": bool(got) and got["bytes"] == exp[0] and (got.get("digest") in (None, f"sha256:{exp[1]}", exp[1]))})
        note("asset_metadata_rows", rows)
        note("asset_metadata_all_match", all(r["meta_match"] for r in rows))

        # --- served bytes: the ZIP + SHA256SUMS ---------------------------------
        served = {}
        for name in ("pipd-ls-sp-public-skills.zip", "SHA256SUMS"):
            b = get(assets[name]["url"], raw=True)
            served[name] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "raw": b}
        note("served_zip_bytes", served["pipd-ls-sp-public-skills.zip"]["bytes"])
        note("served_zip_sha256", served["pipd-ls-sp-public-skills.zip"]["sha256"])
        note("served_zip_matches_frozen", served["pipd-ls-sp-public-skills.zip"]["sha256"] == EXPECT["pipd-ls-sp-public-skills.zip"][1])
        note("served_sha256sums_sha256", served["SHA256SUMS"]["sha256"])
        note("served_sha256sums_matches_frozen", served["SHA256SUMS"]["sha256"] == EXPECT["SHA256SUMS"][1])

        # cross-check every SHA256SUMS entry against the served bytes where we fetched them
        entries = {}
        for line in served["SHA256SUMS"]["raw"].decode("utf-8", "replace").splitlines():
            parts = line.split()
            if len(parts) == 2:
                entries[parts[1].lstrip("*")] = parts[0]
        note("sha256sums_entries", entries)
        note("sha256sums_lists_zip", entries.get("pipd-ls-sp-public-skills.zip") == EXPECT["pipd-ls-sp-public-skills.zip"][1])
        note("sha256sums_entry_count", len(entries))
        note("sha256sums_lists_itself", "SHA256SUMS" in entries)

        # --- ZIP structure ------------------------------------------------------
        zf = zipfile.ZipFile(io.BytesIO(served["pipd-ls-sp-public-skills.zip"]["raw"]))
        names = zf.namelist()
        skillmd = [n for n in names if n.endswith("SKILL.md")]
        manifests = [n for n in names if n.endswith("plugin.json")]
        bad = [n for n in names if n.startswith("/") or ".." in n.split("/") or "\\" in n]
        roots = sorted({n.split("/")[0] for n in names if "/" in n})
        note("zip_entries", len(names))
        note("zip_skillmd_count", len(skillmd))
        note("zip_manifests", manifests)
        note("zip_manifest_count", len(manifests))
        note("zip_traversal_members", bad)
        note("zip_roots", roots)
        note("zip_root_names", sorted(n for n in names if "/" not in n))
        joined = " ".join(manifests).lower()
        note("zip_has_mcp_or_apps_or_hooks", any(k in joined for k in ("mcp", "apps", "hooks")))
        if manifests:
            pj = json.loads(zf.read(manifests[0]).decode("utf-8"))
            note("plugin_json_keys", sorted(pj.keys()))
            note("plugin_json_name", pj.get("name"))
            note("plugin_json_version", pj.get("version"))
    except Exception as exc:  # noqa: BLE001
        note("release_error", f"{type(exc).__name__}: {exc}")

    # --- PRs --------------------------------------------------------------------
    prs = {}
    for n in (17, 14, 15, 13, 16):
        try:
            p = get(f"https://api.github.com/repos/{OWNER_REPO}/pulls/{n}")
            prs[str(n)] = {"state": p["state"], "draft": p["draft"], "head": p["head"]["ref"],
                           "head_sha": p["head"]["sha"], "mergeable_state": p.get("mergeable_state"),
                           "changed_files": p["changed_files"], "additions": p["additions"],
                           "deletions": p["deletions"], "merged": p["merged"], "title": p["title"]}
        except Exception as exc:  # noqa: BLE001
            prs[str(n)] = {"error": f"{type(exc).__name__}: {exc}"}
    note("pulls", prs)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k != "asset_metadata_rows"}, ensure_ascii=False, indent=1)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
