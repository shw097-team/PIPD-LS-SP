#!/usr/bin/env python3
"""R6 doc-identity / update-route detector for round PIPD-S4-R6-CLOSEOUT-20261016.

Self-verifying: every CHECK has a paired MUTATION that must make exactly that check fire.
If any mutation fails to fire, the probe is vacuous and the run FAILS (non-vacuity assertion).

Usage:
    python r6_doc_identity_check.py --repo <worktree> [--json-out <path>]

Exit: 0 = all checks pass AND all mutations fire; 2 = a check failed; 3 = a mutation did not fire.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

README = "docs/install/README.md"
GUIDE = "docs/USER_GUIDE.md"

PREVIEW4_TARGET = "cc6c1930765160697e7e51d6e37735b9220a30db"
PREVIEW4_TAGOBJ = "0618d73c725da0d8c3280f99ef369d13741b5197"
PREVIEW3_TARGET = "cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a"
ZIP_SHA = "545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75"

# release generation -> (target commit, mount-pack suffix)
GEN = {
    "v0.1.1-preview.3": (PREVIEW3_TARGET, "v0.1.1-preview.3"),
}


def _blocks_with(text: str, needle: str) -> list[str]:
    """Fenced code blocks containing `needle`."""
    return [b for b in re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.S) if needle in b]


def check_no_mixed_build_example(readme: str) -> list[str]:
    """No build example may pair a release id with a different release's commit/mount pack."""
    errs = []
    for blk in _blocks_with(readme, "--release-id"):
        rid = re.search(r"--release-id\s+(\S+)", blk)
        rcom = re.search(r"--release-commit\s+([0-9a-f]{40})", blk)
        rmp = re.search(r"--mount-pack\s+(\S+)", blk)
        if not (rid and rcom):
            continue
        rid_v, com_v = rid.group(1), rcom.group(1)
        if rid_v == "v0.1.1-preview.4" and com_v != PREVIEW4_TARGET:
            errs.append(f"build example pairs {rid_v} with commit {com_v} (expected {PREVIEW4_TARGET})")
        if rid_v in GEN:
            want_com, want_pack = GEN[rid_v]
            if com_v != want_com:
                errs.append(f"build example pairs {rid_v} with commit {com_v} (expected {want_com})")
            if rmp and not rmp.group(1).endswith(want_pack):
                errs.append(f"build example pairs {rid_v} with mount pack {rmp.group(1)}")
    return errs


def check_header_pin(readme: str) -> list[str]:
    """The version-pin paragraph must not attribute preview.3's target to preview.4."""
    errs = []
    para = readme.split("\n\n")
    pin = [p for p in para if "Version pin for everything on this page" in p]
    if not pin:
        return ["version-pin paragraph not found"]
    p = pin[0]
    flat = " ".join(p.split())
    if "v0.1.1-preview.4" not in flat:
        errs.append("version pin does not name v0.1.1-preview.4")
    if PREVIEW4_TARGET not in flat:
        errs.append("version pin does not carry the preview.4 target commit")
    if re.search(r"preview\.4`?\*\*, release-tag target and\s*\n?\s*build-source commit \*\*`?" + PREVIEW3_TARGET, p):
        errs.append("version pin still attributes the preview.3 commit to preview.4")
    return errs


def check_no_preview4_mount_pack(readme: str) -> list[str]:
    if "pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.4" in readme:
        return ["README references a preview.4 mount pack, which does not exist in the tree"]
    return []


def check_guide_currentness(guide: str) -> list[str]:
    errs = []
    if re.search(r"Merge and release are `HOLD`", guide):
        errs.append("USER_GUIDE still carries the preview.3-era 'Merge and release are `HOLD`' sentence")
    if re.search(r"The source repair exists in the candidate branch; the published wheel does not\s*\n?\s*inherit it", guide):
        errs.append("USER_GUIDE still carries the stale candidate-branch wheel claim")
    if "S4_FULL_PASS" not in guide or "NOT_GRANTED" not in guide:
        errs.append("USER_GUIDE no longer states the S4_FULL_PASS / NOT_GRANTED ceiling")
    if "v0.1.1-preview.4" not in guide:
        errs.append("USER_GUIDE does not mention v0.1.1-preview.4 as published")
    return errs


def check_update_route(readme: str) -> list[str]:
    errs = []
    if "### Updating a plugin you already installed" not in readme:
        errs.append("install SSOT lacks the 'Updating a plugin you already installed' section")
    for needle, why in (
        ("Manage → Update", "no Manage/Update step"),
        ("Upload new version", "no 'Upload new version' alternative"),
        ("plugin_id", "no plugin_id identification step"),
        ("derived candidate", "no derived-candidate disclosure for a new id"),
        ("Rollback", "no rollback step"),
    ):
        if needle not in readme:
            errs.append(f"update route incomplete: {why}")
    if re.search(r"(?:automatically|auto-)\s*(?:generate|create)[a-z ]*new\s+`?plugin_id", readme, re.I):
        errs.append("update route instructs the reader to auto-create a new plugin_id")
    return errs


def check_zip_digest_and_entry(readme: str) -> list[str]:
    errs = []
    if ZIP_SHA not in readme:
        errs.append("install SSOT does not carry the plugin ZIP sha256")
    if "releases/tag/v0.1.1-preview.4" not in readme:
        errs.append("install SSOT does not carry the release download entry")
    if "permission stays `NOT_SUPPORTED_FOR_ACCOUNT`" in readme:
        errs.append("NOT_SUPPORTED_FOR_ACCOUNT downgrade wording drifted")
    return errs


def check_anchor_link(readme: str) -> list[str]:
    """The in-page link target must resolve to the created heading's anchor."""
    if "#updating-a-plugin-you-already-installed" in readme and \
       "### Updating a plugin you already installed" not in readme:
        return ["in-page update link does not resolve to a heading"]
    return []


CHECKS = {
    "no_mixed_build_example": (README, check_no_mixed_build_example),
    "header_pin": (README, check_header_pin),
    "no_preview4_mount_pack": (README, check_no_preview4_mount_pack),
    "update_route": (README, check_update_route),
    "zip_digest_and_entry": (README, check_zip_digest_and_entry),
    "anchor_link": (README, check_anchor_link),
    "guide_currentness": (GUIDE, check_guide_currentness),
}

# Each mutation must make ITS OWN check fire (and is evaluated only against that check).
MUTATIONS = {
    "no_mixed_build_example": (
        README,
        lambda t: t.replace("--release-id v0.1.1-preview.3", "--release-id v0.1.1-preview.4"),
    ),
    "header_pin": (
        README,
        lambda t: t.replace(PREVIEW4_TARGET, PREVIEW3_TARGET),
    ),
    "no_preview4_mount_pack": (
        README,
        lambda t: t.replace("pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3",
                            "pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.4"),
    ),
    "update_route": (
        README,
        lambda t: t.replace("### Updating a plugin you already installed", "### Updating later"),
    ),
    "zip_digest_and_entry": (
        README,
        lambda t: t.replace(ZIP_SHA, "0" * 64),
    ),
    "anchor_link": (
        README,
        lambda t: t.replace("### Updating a plugin you already installed", "### Updating later"),
    ),
    "guide_currentness": (
        GUIDE,
        lambda t: t.replace("- **`S4_FULL_PASS` is `NOT_GRANTED`.**",
                            "- `S4_FULL_PASS` is **NOT GRANTED**. Merge and release are `HOLD`."),
    ),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()
    root = Path(args.repo)
    texts = {p: (root / p).read_text(encoding="utf-8") for p in (README, GUIDE)}

    report: dict = {"schema": "PIPD-R6-DOC-IDENTITY-CHECK/1", "repo": str(root), "checks": [], "mutations": []}
    rc = 0
    for name, (fname, fn) in CHECKS.items():
        errs = fn(texts[fname])
        report["checks"].append({"check": name, "file": fname, "status": "FAIL" if errs else "PASS", "errors": errs})
        if errs:
            rc = 2
    # non-vacuity: every mutation must make its own check fire
    for name, (fname, mut) in MUTATIONS.items():
        mutated = mut(texts[fname])
        fired = bool(CHECKS[name][1](mutated)) if mutated != texts[fname] else False
        report["mutations"].append({"check": name, "mutation_applied": mutated != texts[fname],
                                    "fired": fired, "status": "OK" if fired else "VACUOUS"})
        if not fired:
            rc = 3 if rc == 0 else rc
    report["verdict"] = "PASS" if rc == 0 else ("CHECK_FAILED" if rc == 2 else "PROBE_VACUOUS")
    report["totals"] = {
        "checks": len(report["checks"]),
        "checks_passed": sum(1 for c in report["checks"] if c["status"] == "PASS"),
        "mutations": len(report["mutations"]),
        "mutations_fired": sum(1 for m in report["mutations"] if m["fired"]),
    }
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(out + "\n", encoding="utf-8")
    print(out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
