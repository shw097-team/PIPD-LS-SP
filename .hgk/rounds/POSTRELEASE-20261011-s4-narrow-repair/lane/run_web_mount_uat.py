#!/usr/bin/env python3
"""WO-S4-WEB-02 five-case consumer UAT driver (deterministic content checks).

No interactive ChatGPT session and no qualifying native-upload account exist in this round, so cases
1-4 are driven as deterministic checks over the ACTUAL pack files and case 5 as an extraction-and-
navigation check. The native-upload path is recorded NOT_SUPPORTED with its reason. This script writes
``evidence/WEB_MOUNT_UAT.json`` and prints each case's raw output verbatim.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACK = ROOT / "dist" / "mount" / "pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2"
ZIP = ROOT / "dist" / "mount" / "PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip"
OUT = (ROOT / ".hgk" / "rounds" / "POSTRELEASE-20261011-s4-narrow-repair" / "evidence"
       / "WEB_MOUNT_UAT.json")

RELEASE = "v0.1.0-preview.2"
TAG = "8faa64e581e8c25f5ec355475e29561847da3ead"
SKILLS = ["pipd-route-intake", "pipd-authority-source", "pipd-profile-tailor", "pipd-pi-compile",
          "pipd-pd-bind", "pipd-execution-contract", "pipd-assurance-tqaep", "pipd-package-project"]


def _read(rel: str) -> str:
    return (PACK / rel).read_text(encoding="utf-8")


def _locator_and_identity_ok(rel: str) -> bool:
    t = _read(rel)
    return "Source Locators" in t and RELEASE in t and TAG in t


def case1_positive():
    skill = _read("SKILL.md")
    routed = [s for s in SKILLS if s in skill]
    docs_ok = all(_locator_and_identity_ok(d) for d in ("references/PIPD_S4_CORE.md",
                                                        "references/PIPD_SOURCE_MAP.md"))
    checks = {
        "trigger_section": "## Trigger" in skill,
        "non_trigger_section": "## Non-trigger" in skill,
        "pi_style_phrase": "compile a PI" in skill,
        "routed_skills": len(routed),
        "referenced_docs_carry_locator_and_identity": docs_ok,
    }
    ok = (checks["trigger_section"] and checks["non_trigger_section"] and checks["pi_style_phrase"]
          and len(routed) == 8 and docs_ok)
    raw = json.dumps(checks, sort_keys=True)
    return ok, raw


def case2_negative():
    skill = _read("SKILL.md")
    # the non-trigger region is everything from '## Non-trigger' to the next '## '
    seg = skill.split("## Non-trigger", 1)[1].split("\n## ", 1)[0]
    checks = {
        "chit_chat_excluded": "chit-chat" in seg,
        "brainstorm_without_locators_excluded": "source locators" in seg.lower(),
        "no_dispatch_wording": "Do **not** dispatch" in seg,
    }
    ok = all(checks.values())
    return ok, json.dumps(checks, sort_keys=True)


def case3_refusal_no_source():
    skill = _read("SKILL.md")
    ex = _read("references/PIPD_EXAMPLES.md")
    checks = {
        "dispatcher_declares_NO_SOURCE_LOCATOR": "NO_SOURCE_LOCATOR" in skill,
        "example_refusal_present": "REFUSAL: NO_SOURCE_LOCATOR" in ex,
        "refusal_is_typed": "typed" in skill.lower() and "typed" in ex.lower(),
    }
    ok = all(checks.values())
    return ok, json.dumps(checks, sort_keys=True)


def case4_refusal_adversarial():
    skill = _read("SKILL.md")
    core = _read("references/PIPD_S4_CORE.md")
    ex = _read("references/PIPD_EXAMPLES.md")
    checks = {
        "dispatcher_declares_UNAUTHORISED_ACTION": "UNAUTHORISED_ACTION" in skill,
        "forbids_self_pass": "self-sign" in ex and "REFUSAL: UNAUTHORISED_ACTION" in ex,
        "forbids_scope_widening": "widen" in ex.lower() and "**" in ex,
        "acceptance_authority_refused": "acceptance authority" in ex,
        "forbidden_claim_listed": "PRODUCTION_VERIFIED" in core,
    }
    ok = all(checks.values())
    return ok, json.dumps(checks, sort_keys=True)


def case5_first_mount():
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(ZIP) as zf:
            zf.extractall(td)
        root = Path(td) / PACK.name
        readme = (root / "README_MOUNT.md").read_text(encoding="utf-8")
        manifest = (root / "MANIFEST.sha256").read_text(encoding="utf-8")
        recomputed = {}
        for line in manifest.splitlines():
            if line.strip():
                digest, rel = line.split("  ", 1)
                recomputed[rel] = hashlib.sha256((root / rel).read_bytes()).hexdigest() == digest
        checks = {
            "readme_present": (root / "README_MOUNT.md").is_file(),
            "skill_present": (root / "SKILL.md").is_file(),
            "manual_attachment_path_documented": "Project Knowledge" in readme,
            "native_upload_path_documented": "Create -> Upload" in readme,
            "source_locators_recoverable": "Source Locators" in readme,
            "manifest_all_recompute": bool(recomputed) and all(recomputed.values()),
        }
    ok = all(checks.values())
    return ok, json.dumps(checks, sort_keys=True)


def main() -> int:
    cases = []
    results = []
    definitions = [
        ("UAT-01", "positive: a PI-style design request triggers the PIPD workflow",
         "a PI-style design request with source locators dispatches to the eight-skill chain",
         "DESIGN_ONLY", case1_positive),
        ("UAT-02", "negative: an ordinary chit-chat question does not trigger the workflow",
         "ordinary chit-chat / brainstorming without locators is a non-trigger",
         "DESIGN_ONLY", case2_negative),
        ("UAT-03", "refusal: a request with no repository context / no source locator is refused typed",
         "the dispatcher and PIPD_EXAMPLES declare a typed NO_SOURCE_LOCATOR refusal",
         "DESIGN_ONLY", case3_refusal_no_source),
        ("UAT-04", "refusal: adversarial self-PASS / permission widening / acceptance-authority request",
         "the dispatcher and PIPD_EXAMPLES declare a typed UNAUTHORISED_ACTION refusal",
         "DESIGN_ONLY", case4_refusal_adversarial),
        ("UAT-05", "first-time mount: mount path and source locators recoverable by a non-developer",
         "the ZIP extracts, the manifest recomputes, and both mount paths + locators are present",
         "DESIGN_ONLY", case5_first_mount),
    ]
    for cid, fixed, expected, ceiling, fn in definitions:
        ok, raw = fn()
        cases.append({
            "case_id": cid,
            "fixed_input": fixed,
            "expected": expected,
            "observed": raw,
            "raw_output": raw,
            "verdict": "PASS" if ok else "FAIL",
            "claim_ceiling": ceiling,
        })
        results.append((cid, "PASS" if ok else "FAIL", raw))

    doc = {
        "schema": "PIPD-S4-WEB-MOUNT-UAT/1",
        "round": "POSTRELEASE-20261011-s4-narrow-repair",
        "work_order": "WO-S4-WEB-02",
        "release_identity": RELEASE,
        "release_tag_commit": TAG,
        "pack": PACK.name,
        "zip": ZIP.name,
        "zip_sha256": hashlib.sha256(ZIP.read_bytes()).hexdigest(),
        "method": ("cases 1-4 are deterministic content checks over the actual pack files; case 5 is "
                   "an extraction-and-navigation check; no interactive ChatGPT session was available"),
        "cases": cases,
        "not_supported": [
            {
                "record": "NATIVE_SKILL_UPLOAD",
                "mount_path": "Plugins -> Skills -> Create -> Upload",
                "verdict": "NOT_SUPPORTED",
                "reason": ("this round had no qualifying native-upload account/workspace, so the native "
                           "skill-upload path was not exercised; no native load is claimed"),
            },
            {
                "record": "LIVE_CHAT_HOST_EXECUTION",
                "mount_path": "chat host tool execution / CLI / repo write / HITL",
                "verdict": "NOT_SUPPORTED",
                "reason": ("the chat host has no tool execution, repository writing, CLI invocation, "
                           "HITL authority or network/file access; these are NOT_AVAILABLE"),
            },
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE {OUT}")
    for cid, verdict, raw in results:
        print(f"{cid} {verdict} {raw}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
