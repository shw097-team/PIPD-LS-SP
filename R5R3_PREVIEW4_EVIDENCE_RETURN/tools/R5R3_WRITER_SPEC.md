# R5R3 WRITER SPEC — preview.4 install-route + release-identity truth (docs/metadata only)

WriteSet (the ONLY files you may change):
- `C:/Projects/wt-r5r3/README.md`
- `C:/Projects/wt-r5r3/docs/install/README.md`
- `C:/Projects/wt-r5r3/docs/RELEASE_TUPLE.json`
- `C:/Projects/wt-r5r3/tests/test_r5r3_install_route_identity.py` (new file)

You may NOT touch `src/**`, `schemas/**`, `packaging/**`, `tools/**`, `.hgk/**`, or anything outside the
worktree `C:/Projects/wt-r5r3`.

## Facts you must not re-derive (measured 2026-10-16 from the served release bytes + git)

| fact | value |
|---|---|
| release tag | `v0.1.1-preview.4` |
| tag object | `0618d73c725da0d8c3280f99ef369d13741b5197` |
| tag target commit | `cc6c1930765160697e7e51d6e37735b9220a30db` |
| tag target tree | `7d277a0afaff28b6841836cea3a31ffd0b214d94` |
| wheel build source commit | `4754d92cc98c0c02b59bf9700d08c0b7bf452e3d` (ancestor of the tag target) |
| served `pipd-ls-sp-public-skills.zip` | 68,357 bytes, sha256 `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75` |
| served `pipd_ls_sp-0.1.1a4-py3-none-any.whl` | 286,978 bytes, sha256 `3b59a985dc9fc1cd4c1c5ca9a7b779122459ab7cadc8f439e17063d6c934cc0c` |
| served `pipd-ls-sp-v0.1.1-preview.4-source.zip` | 32,841,678 bytes, sha256 `f8070971fd1bf8e1c2c3bbe4f59e33d70853a2e8737817931928d35baebee2ca` |
| served `PIPD_WEB_FALLBACK.md` | 42,145 bytes, sha256 `c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af` |
| served `PREVIEW_NOTES_v0.1.1-preview.4.md` | 5,326 bytes, sha256 `96fedfc6fa27bd412e16a0377a509719f41026f891732d197c8848926f423201` |
| served `SHA256SUMS` | 583 bytes, sha256 `0f76502670038ae35bd4f772dc23223f6b47241c3acee2f918d106eaabffe689` (6 entries) |
| superseded R5Y evidence-branch ZIP | 68,355 bytes, sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, frozen at `062d84ae3e951d02b2ba6bb732359b18799d2864` |

The release carries **no** `RELEASE_TUPLE_*.json` asset. Its assets are exactly the seven above.

## HUNK A — `README.md` (the reproducibility block, currently lines 73–75)

Replace exactly these three lines:

```
This produces `out/pipd-ls-sp-public-skills.zip` — **68,355 bytes**, sha256
`2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, **56 entries**, **8 `SKILL.md`**.
Two independent builds are byte-identical. A local packager PASS is not portal approval.
```

with:

```
This reproduces the **historical R5Y build**: `out/pipd-ls-sp-public-skills.zip` — **68,355 bytes**,
sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, **56 entries**, **8 `SKILL.md`**
— the bytes frozen at `062d84ae3e951d02b2ba6bb732359b18799d2864` and attached to the R5Y evidence return.
Those bytes are **superseded as a download**: the artefact a user installs is the `v0.1.1-preview.4`
release asset `pipd-ls-sp-public-skills.zip` — **68,357 bytes**, sha256
`545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`, 56 entries, 8 `SKILL.md`. Two
independent builds are byte-identical. A local packager PASS is not portal approval.
```

## HUNK B — `README.md` (the gate table row, currently line 81)

Replace exactly this one line:

```
| Tag / release | **Pending owner version decision** | No tag and no release was created for the merged candidate |
```

with:

```
| Tag / release | **Superseded by the published preview** | At the R5Y record time no tag had been created for the merged candidate. `v0.1.1-preview.4` (tag object `0618d73c725da0d8c3280f99ef369d13741b5197`, target `cc6c1930765160697e7e51d6e37735b9220a30db`) was published on 2026-10-14 and is the current immutable preview; `main` has since advanced past it, so read the tag's tree — not `main` — for the released bytes |
```

## HUNK C — `README.md` (the private-plugin route, currently lines 139–142)

Replace exactly these four lines:

```
  identity/KYC step. A **private** plugin does not need it. Download the candidate ZIP
  `.hgk/rounds/R5Y-20261014-gpt-plugin-publication/04_package/build/build-a/pipd-ls-sp-public-skills.zip`
  (**68,355 bytes**, sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, single root `pipd-ls-sp-public-skills/`, 8 ×
  `skills/<name>/SKILL.md`, no MCP/Actions/Hooks) and in ChatGPT do: `chatgpt.com/plugins` →
```

with:

```
  identity/KYC step. A **private** plugin does not need it. Download the **release asset**
  `https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.4/pipd-ls-sp-public-skills.zip`
  (**68,357 bytes**, sha256 `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75` — the digest the
  release's own `SHA256SUMS` carries; one plugin root `pipd-ls-sp-public-skills/`, one `plugin.json`, 8 ×
  `skills/<name>/SKILL.md`, no MCP/Actions/Hooks) and in ChatGPT do: `chatgpt.com/plugins` →
```

Then, immediately after the paragraph that ends with
`If the entry is missing or the ZIP is refused, fall back to the single document` +
`  route above.` (currently line 150), append these two lines as their own bullet:

```

  *Superseded artefact, kept only as history:* the R5Y evidence-branch ZIP
  `.hgk/rounds/R5Y-20261014-gpt-plugin-publication/04_package/build/build-a/pipd-ls-sp-public-skills.zip`
  (**68,355 bytes**, sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`) is the
  pre-release build frozen at `062d84ae`. Do not install it: it is not the bytes the release serves, and
  its digest is in no `SHA256SUMS`.
```

## HUNK D — `docs/install/README.md` (the version-pin bullet)

Replace exactly these four lines:

```
- release id **`v0.1.1-preview.4`**; the release-tag target commit and tree are recorded in the
  release's own `RELEASE_TUPLE_v0.1.1-preview.4.json` asset, together with every served asset digest
  (`docs/RELEASE_TUPLE.json` in this tree is the **historical** preview.3 record and is left as-is —
  the tag's tree is never rewritten).
```

with:

```
- release id **`v0.1.1-preview.4`**; its tag object `0618d73c725da0d8c3280f99ef369d13741b5197`
  dereferences to target commit `cc6c1930765160697e7e51d6e37735b9220a30db`, tree
  `7d277a0afaff28b6841836cea3a31ffd0b214d94`. The release carries **no** `RELEASE_TUPLE_*.json` asset;
  its identities live in the `v0.1.1-preview.4` entry of
  [`docs/RELEASE_TUPLE.json`](RELEASE_TUPLE.json) in this tree, and the digests a downloader verifies
  against are the release's own `SHA256SUMS` asset. Both are independently re-derivable:
  `git rev-parse <tag>`, `git rev-parse <tag>^{commit}`, `git rev-parse <tag>^{tree}`, and
  `sha256sum <downloaded asset>` against `SHA256SUMS`. The earlier releases' entries stay as history —
  a tag's tree is never rewritten.
```

## HUNK E — `docs/RELEASE_TUPLE.json` (append one entry to the `releases` array)

Append this object as the LAST element of `releases` (keep the file's existing formatting, 1-space
indent level as used there, and keep every existing entry byte-identical):

```json
{
 "release_id": "v0.1.1-preview.4",
 "tag_object": "0618d73c725da0d8c3280f99ef369d13741b5197",
 "release_tag_target": "cc6c1930765160697e7e51d6e37735b9220a30db",
 "build_source_commit": "4754d92cc98c0c02b59bf9700d08c0b7bf452e3d",
 "tree": "7d277a0afaff28b6841836cea3a31ffd0b214d94",
 "pack_dir": null,
 "zip": null,
 "published_asset_name": "pipd-ls-sp-public-skills.zip",
 "published_asset_sha256": "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75",
 "served_assets": {
  "pipd-ls-sp-public-skills.zip": {"bytes": 68357, "sha256": "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"},
  "pipd_ls_sp-0.1.1a4-py3-none-any.whl": {"bytes": 286978, "sha256": "3b59a985dc9fc1cd4c1c5ca9a7b779122459ab7cadc8f439e17063d6c934cc0c"},
  "pipd-ls-sp-v0.1.1-preview.4-source.zip": {"bytes": 32841678, "sha256": "f8070971fd1bf8e1c2c3bbe4f59e33d70853a2e8737817931928d35baebee2ca"},
  "PIPD_WEB_FALLBACK.md": {"bytes": 42145, "sha256": "c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af"},
  "PREVIEW_NOTES_v0.1.1-preview.4.md": {"bytes": 5326, "sha256": "96fedfc6fa27bd412e16a0377a509719f41026f891732d197c8848926f423201"},
  "SHA256SUMS": {"bytes": 583, "sha256": "0f76502670038ae35bd4f772dc23223f6b47241c3acee2f918d106eaabffe689"}
 },
 "asset_list_source": "SHA256SUMS asset of the release; every digest recomputed from the downloaded bytes 2026-10-16",
 "note": "The release ships no mount pack: pack_dir/zip are null on purpose. published_asset_sha256 names the private skills-only plugin ZIP because that is the distribution surface this entry exists to pin (published_asset_name); the other assets are not dropped - they are in served_assets.",
 "status": "PUBLISHED_ASSETS_RECOMPUTED_AND_MATCHING_SHA256SUMS_20261016"
}
```

## HUNK F — new file `tests/test_r5r3_install_route_identity.py`

Write exactly this file:

```python
"""R5R3: the install route must name the bytes the release actually serves.

The defect this guards: the front page's private-plugin route named an in-repo, superseded
evidence-branch ZIP (68,355 bytes / ``2f9ae0...``) as the download, while the released asset is a
different byte string (68,357 bytes / ``545e359a...``) that the release's own ``SHA256SUMS`` carries -
and ``docs/install/README.md`` pointed at a ``RELEASE_TUPLE_*.json`` asset the release does not ship.
Nothing in the published tree recorded the served identity at all.

Derived, not hand-written: the tuple entry's tag facts are re-derived from git here, exactly as
``test_s4ext_release_provenance`` does for the earlier releases.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEX64 = re.compile(r"\b[0-9a-f]{64}\b")
SERVED_ZIP = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"
SUPERSEDED_ZIP = "2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199"
TAG = "v0.1.1-preview.4"
DISCLOSURE = ("superseded", "historical", "history", "do not install")


def git(*args: str) -> str:
    out = subprocess.run(["git", "-C", str(ROOT).replace("\\", "/"), *args],
                         check=True, capture_output=True, text=True)
    return out.stdout.strip()


class InstallRouteNamesTheServedAssetTests(unittest.TestCase):
    def test_readme_route_names_the_release_asset_and_its_served_digest(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"releases/download/{TAG}/pipd-ls-sp-public-skills.zip", text)
        self.assertIn(SERVED_ZIP, text)

    def test_superseded_digest_is_only_disclosed_as_superseded(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            if SUPERSEDED_ZIP in line:
                low = line.lower()
                self.assertTrue(any(m in low for m in DISCLOSURE),
                                f"README.md:{lineno} names the superseded ZIP without saying so")

    def test_install_readme_does_not_point_at_a_missing_release_asset(self) -> None:
        text = (ROOT / "docs/install/README.md").read_text(encoding="utf-8")
        self.assertNotIn("RELEASE_TUPLE_v0.1.1-preview.4.json", text)
        self.assertIn("RELEASE_TUPLE.json", text)


class TupleRecordsThePreview4IdentityTests(unittest.TestCase):
    def entry(self) -> dict:
        data = json.loads((ROOT / "docs" / "RELEASE_TUPLE.json").read_text(encoding="utf-8"))
        return next(r for r in data["releases"] if r["release_id"] == TAG)

    def test_tag_facts_re_derived_from_git(self) -> None:
        entry = self.entry()
        self.assertEqual(git("rev-parse", TAG), entry["tag_object"])
        self.assertEqual(git("rev-parse", f"{TAG}^{{commit}}"), entry["release_tag_target"])
        self.assertEqual(git("rev-parse", f"{TAG}^{{tree}}"), entry["tree"])
        self.assertIn("build_source_commit", entry)
        self.assertNotEqual(entry["build_source_commit"], entry["release_tag_target"],
                            "the build source and the tag target are separate facts")

    def test_served_asset_digests_are_recorded(self) -> None:
        entry = self.entry()
        self.assertEqual(entry["served_assets"]["pipd-ls-sp-public-skills.zip"]["sha256"], SERVED_ZIP)
        self.assertEqual(entry["published_asset_sha256"], SERVED_ZIP)
        for name, meta in entry["served_assets"].items():
            self.assertRegex(meta["sha256"], r"^[0-9a-f]{64}$", name)
            self.assertGreater(meta["bytes"], 0, name)

    def test_the_superseded_digest_is_not_presented_as_served(self) -> None:
        entry = self.entry()
        digests = {m["sha256"] for m in entry["served_assets"].values()}
        self.assertNotIn(SUPERSEDED_ZIP, digests)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Acceptance command you must run, and paste verbatim

```
cd C:/Projects/wt-r5r3 && set -o pipefail; PYTHONPATH=src \
  C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest \
  tests.test_r5r3_install_route_identity tests.test_s4ext_release_provenance tests.test_s4r2m_docs_route \
  tests.test_evidence_md_guards -v 2>&1 | tail -25; echo "EXIT=$?"
```

Everything must be green. If a test fails because of a fact in this spec, STOP and report the failure
with the raw output - do not edit the test to make it pass.

## Your receipt

Write `C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout/WS_A_RECEIPT.md` with: the
exact edits per file, the acceptance command, its exit code and raw tail, and anything you could not do.
Then print the same summary plus the line `HGK_LANE_NONCE_OK` as your final message.
