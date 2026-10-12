#!/usr/bin/env python3
"""S4EXT-R1 TT-S4EXT-001 one-shot repair of the preview.3 mount-pack release identity.

F001 (external challenge R1) proved that all EIGHT documents of
``dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3/`` declared
``tag commit 8faa64e581e8c25f5ec355475e29561847da3ead`` while the real
``v0.1.1-preview.3^{commit}`` is ``cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a``.
The stale value is the v0.1.0-preview.2 tag target, so the preview.3 pack described the PREVIOUS
release's object; ``PIPD_SOURCE_MAP.md`` also carried the preview.2 TREE (``58301503``) instead of
``91b1156f``, and ``SKILL.md``'s front matter still said ``version: 0.1.0-preview.2``.

Root cause: the identity was a hand-copied literal that collapsed two distinct facts ("which commit
the tag points at" and "which commit the distributed bytes were built from") into one string. The
repair (a) keeps them SEPARATE and explicit, (b) points both at the frozen tuple in
``docs/RELEASE_TUPLE.json``, and (c) adds an erratum note so the already published, immutable asset
is not silently replaced.

This script edits the pack SOURCE documents only. The ZIP is rebuilt afterwards by
``tools/build_mount_pack.py`` (the single writer of ``dist/mount/**``).

Run: python apply_release_identity_repair.py --root <repo root>
"""
from __future__ import annotations

import argparse
from pathlib import Path

PACK = "dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3"
TUPLE = "docs/RELEASE_TUPLE.json"

STALE_TAG_COMMIT = "8faa64e581e8c25f5ec355475e29561847da3ead"   # v0.1.0-preview.2 tag target
STALE_TREE_SHORT = "58301503"                                     # v0.1.0-preview.2 tree prefix
STALE_SKILL_VERSION = "0.1.0-preview.2"

TAG_TARGET = "cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a"
BUILD_SOURCE = "cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a"
TREE_SHORT = "91b1156f"

PACK_DOCS = ("README_MOUNT.md", "PIPD_LS_SP_QUICKSTART_PROMPT.md", "SKILL.md",
             "references/PIPD_S4_CORE.md", "references/PIPD_SOURCE_MAP.md",
             "references/PIPD_8_SKILLS_INDEX.md", "references/PIPD_PROFILE_AND_SAFETY.md",
             "references/PIPD_EXAMPLES.md")

IDENTITY_LINE = (f"> Release identity: **v0.1.1-preview.3** — release tag target `{TAG_TARGET}`; "
                 f"build source commit `{BUILD_SOURCE}`.")
ERRATUM_LINE = (
    f"> Published-asset erratum (2026-10-12): the v0.1.1-preview.3 Web Mount ZIP published on "
    f"GitHub declares `{STALE_TAG_COMMIT}` (the v0.1.0-preview.2 tag target) as this release's tag "
    f"commit. That published asset is immutable and is NOT rewritten; this repository source "
    f"carries the corrected identity. Frozen tuple: `{TUPLE}`; disclosure: "
    f"`docs/ERRATUM_2026-10-12_preview3_release_provenance.md`."
)
BOUND_OLD = f"Bound to `v0.1.1-preview.3`, tag commit `{STALE_TAG_COMMIT}`."
BOUND_NEW = (f"Bound to `v0.1.1-preview.3` (release tag target `{TAG_TARGET}`; "
             f"build source commit `{BUILD_SOURCE}`).")

# The release-identity blockquote appears with and without a trailing full stop; the no-period form
# is a SUBSTRING of the period form, so the pair is resolved by longest-first occurrence count.
IDENTITY_VARIANTS = (
    f"> Release identity: **v0.1.1-preview.3** — tag commit `{STALE_TAG_COMMIT}`.",
    f"> Release identity: **v0.1.1-preview.3** — tag commit `{STALE_TAG_COMMIT}`",
)


def _replace_once(text: str, old: str, new: str, where: str) -> str:
    hits = text.count(old)
    if hits != 1:
        raise SystemExit(f"{where}: expected exactly 1 occurrence of {old!r}, found {hits}")
    return text.replace(old, new)


def _replace_optional(text: str, old: str, new: str) -> str:
    """Replace when present; 2+ occurrences are a bug. README_MOUNT has no 'Bound to' sentence."""
    hits = text.count(old)
    if hits == 0:
        return text
    if hits > 1:
        raise SystemExit(f"expected at most 1 occurrence of {old!r}, found {hits}")
    return text.replace(old, new)


def repair_doc(text: str, rel: str) -> str:
    """Apply this document's share of the repair; fails loudly if a pattern is not unique."""
    if rel == "SKILL.md":
        # SKILL.md carries its identity in YAML front matter, not in a blockquote.
        text = _replace_once(
            text, f"release_identity: v0.1.1-preview.3\nrelease_tag_commit: {STALE_TAG_COMMIT}\n",
            f"release_identity: v0.1.1-preview.3\nrelease_tag_target: {TAG_TARGET}\n"
            f"build_source_commit: {BUILD_SOURCE}\n", rel)
        text = _replace_once(text, f"version: {STALE_SKILL_VERSION}\n",
                             "version: 0.1.1-preview.3\n", rel)
        text = _replace_once(
            text,
            f"Bind it to release **v0.1.1-preview.3** (tag commit `{STALE_TAG_COMMIT}`).",
            f"Bind it to release **v0.1.1-preview.3** (release tag target `{TAG_TARGET}`; "
            f"build source commit `{BUILD_SOURCE}`).", rel)
    else:
        old = next((o for o in IDENTITY_VARIANTS if text.count(o) == 1), None)
        if old is None:
            raise SystemExit(f"{rel}: no unique release-identity line found")
        text = text.replace(old, IDENTITY_LINE)

    text = _replace_optional(text, BOUND_OLD, BOUND_NEW)
    text = text.replace(f"(tree `{STALE_TREE_SHORT}`)", f"(tree `{TREE_SHORT}`)")

    if rel == "PIPD_LS_SP_QUICKSTART_PROMPT.md":
        text = _replace_once(text, f"(tag commit {STALE_TAG_COMMIT}).",
                             f"(release tag target {TAG_TARGET}; "
                             f"build source commit {BUILD_SOURCE}).", rel)
    if rel == "README_MOUNT.md":
        text = _replace_once(
            text, f"(tag commit `{STALE_TAG_COMMIT}`):",
            f"(release tag target `{TAG_TARGET}`; build source commit `{BUILD_SOURCE}`):", rel)
    if rel == "references/PIPD_SOURCE_MAP.md":
        text = _replace_once(
            text, f"| tag commit | `{STALE_TAG_COMMIT}` |",
            f"| release tag target | `{TAG_TARGET}` |\n"
            f"| build source commit | `{BUILD_SOURCE}` |\n"
            f"| lineage note | the previously published asset of this release named "
            f"`{STALE_TAG_COMMIT}`, which is the v0.1.0-preview.2 tag target — see "
            f"`docs/ERRATUM_2026-10-12_preview3_release_provenance.md` |", rel)
        text = _replace_once(text, f"| release tree | `{STALE_TREE_SHORT}` |",
                             f"| release tree | `{TREE_SHORT}` |", rel)
    return text


def add_erratum_banner(text: str, rel: str) -> str:
    if ERRATUM_LINE in text:
        raise SystemExit(f"{rel}: erratum line already present")
    lines = text.splitlines(keepends=True)
    if rel == "SKILL.md":
        idx = next(i for i, ln in enumerate(lines) if ln.startswith("# "))
    else:
        idx = next(i for i, ln in enumerate(lines) if ln.startswith("> Release identity:"))
    lines.insert(idx + 1, ERRATUM_LINE + "\n")
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pack = root / PACK
    if not pack.is_dir():
        raise SystemExit(f"pack directory not found: {pack}")

    for rel in PACK_DOCS:
        path = pack / rel
        path.write_text(repair_doc(path.read_text(encoding="utf-8"), rel), encoding="utf-8")
    for rel in ("README_MOUNT.md", "SKILL.md", "references/PIPD_SOURCE_MAP.md"):
        path = pack / rel
        path.write_text(add_erratum_banner(path.read_text(encoding="utf-8"), rel), encoding="utf-8")

    # The stale value may survive ONLY as a disclosure (the erratum banner / the lineage note).
    # Any other line still naming it as THIS release's identity is the defect coming back.
    offenders = []
    for p in sorted(pack.rglob("*")):
        if not p.is_file() or p.name == "MANIFEST.sha256":
            continue
        for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if STALE_TAG_COMMIT in line and "erratum" not in line.lower() \
                    and "lineage note" not in line.lower():
                offenders.append(f"{p.relative_to(root)}:{lineno}: {line.strip()[:90]}")
    if offenders:
        raise SystemExit("stale tag target still asserted as this release's identity:\n  "
                         + "\n  ".join(offenders))
    print(f"repaired {len(PACK_DOCS)} pack documents; the stale identity survives only as disclosure")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
