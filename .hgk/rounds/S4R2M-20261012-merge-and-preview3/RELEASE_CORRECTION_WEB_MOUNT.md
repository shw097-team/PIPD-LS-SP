# RELEASE_CORRECTION — web mount pack identity stamp

**Round** `S4R2M-20261012-merge-and-preview3` · **date** 2026-10-12 (Asia/Taipei)
**Trigger** owner asked for the Web/ChatGPT-installable package; inspection of the shipped artifact
found its own provenance stamp to be wrong.

## Defect

The published asset `PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip` declared itself bound to
release `v0.1.1-preview.3` while naming the **preview.2** commit in all 8 content files:

| field in the pack | pack said | truth |
|---|---|---|
| release identity (label) | `v0.1.1-preview.3` | `v0.1.1-preview.3` |
| tag commit (8/8 files) | `8faa64e581e8c25f5ec355475e29561847da3ead` | `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a` |
| release tree (`README_MOUNT.md`, `PIPD_S4_CORE.md`, `PIPD_SOURCE_MAP.md`) | `58301503` | `91b1156f` |
| `SKILL.md` front-matter `version` | `0.1.0-preview.2` | `0.1.1-preview.3` |

`8faa64e5` is the `v0.1.0-preview.2` tag commit (its tree is indeed `58301503…`), so the stamp was a
carried-over predecessor identity, not a typo in one place. `tools/build_mount_pack.py` is a pure
packager — it does not author these strings — so the stale stamp lived in the pack content, where no
gate was checking that a pack's declared identity matches the release it is shipped under.

Why it matters: the pack's whole proposition is verifiable provenance ("recompute `MANIFEST.sha256`,
bind to release X"). A consumer following that instruction would have bound the content to the wrong
tree. This is the "tag-to-distribution identity must be consistent" requirement from the
2026-10-11 acceptance report, unenforced in the pack path.

## Correction

1. Replaced the tag commit and tree in all 8 content files; fixed the `SKILL.md` `version` field.
2. Rebuilt through the project's own packager (`tools/build_mount_pack.py`), not by hand:
   `BUILD OK … members=9`, `VERIFY PASS`.
3. Regenerated `SHA256SUMS` with **LF** terminators — a first attempt wrote CRLF and was caught and
   corrected before publishing (418 bytes, matching the prior file's size).
4. **Replaced** the two affected assets on the live release. Because a published GitHub asset is
   immutable, this was done as an explicit delete-then-upload and is recorded:
   `deleted_asset_id=631301834` (mount zip, 204) and `631302807` (`SHA256SUMS`, 204).
   `publish_release.py` gained a `--replace` flag so correction is a named, logged act rather than a
   silent overwrite; without the flag it still refuses to touch an existing asset.
5. Re-read everything back **anonymously**; all 5 assets match local.

| asset | before | after |
|---|---|---|
| mount zip | `73c6c7e255846e90…d1dcfde` | `af342d281f02ba04…ec6b504f` |
| `SHA256SUMS` | `da20bdca4e0f03f9…e2eaba51` | `c4230f985c160e83…4051ba9d` |
| wheel, source zip, notes | unchanged | unchanged |

`{"verdict": "RELEASE_VERIFIED", "assets": 5, "all_local_match": true}`

The tag, the release id, the prerelease flag and the other three assets were not touched. The
superseded digests are recorded above rather than erased, and the previous `PUBLISH.log` /
`PUBLISH_ATTEMPT1_TARGET_COMMITISH_500.log` are retained.

## Residual gap, not closed

Nothing in the build or test path asserts *"a pack's declared release identity equals the release it
is shipped under"*. This correction fixed one artifact; the next version bump can carry the stamp
forward again the same way. A guard belongs in `tools/build_mount_pack.py` (or in the release lane)
so the defect cannot silently recur. Not implemented in this round.
