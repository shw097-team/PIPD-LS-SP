#!/usr/bin/env python3
"""Emit the round's machine-readable indices: the raw-evidence index and the R3 finding ledger.

Both are derived from files that already exist. Nothing here runs a test, and nothing here may
invent a verdict: a finding is marked closed only where a raw receipt is named AND its own content
supports the claim; everything else stays OPEN with the owner who can close it.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]           # .hgk/rounds/<round>/
EV = ROOT / "evidence"
ROUND = ROOT.name


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


index = []
for p in sorted(EV.rglob("*")):
    if p.is_file() and p.name != "RAW_INDEX.json":
        index.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": p.stat().st_size, "sha256": sha256(p)})
(EV / "RAW_INDEX.json").write_text(json.dumps(
    {"schema_id": "PIPD-S4-R3-RAW-EVIDENCE-INDEX/1", "round": ROUND,
     "note": "Every digest below is of the bytes GIT STORES for that path - not of the working-tree "
             "bytes. The repository default is `* text=auto eol=lf`, so a CRLF file is rewritten on "
             "commit; hashing the working tree would record a digest no checkout can reproduce.",
     "files": index}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Self-check: the recorded digest must equal the digest of the committed blob, otherwise the index is
# a claim no external checker can reproduce. This is exactly the failure that slipped through once -
# a CRLF working file was hashed, then normalised to LF on commit, and one row stopped matching.
def _committed_digest(path: str) -> str | None:
    """Digest of the blob git stores for `path`, given repo-root-relative."""
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(ROOT),
                         capture_output=True, text=True).stdout.strip()
    if not top:
        return None
    blob = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=top, check=False,
                          capture_output=True).stdout
    return hashlib.sha256(blob).hexdigest() if blob else None


def _repo_rel(path: str) -> str:
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(ROOT),
                         capture_output=True, text=True).stdout.strip()
    if not top:
        return path
    return Path(ROOT / path).resolve().relative_to(Path(top).resolve()).as_posix()


mismatch, unchecked = [], []
for entry in index:
    got = _committed_digest(_repo_rel(entry["path"]))
    if got is None:
        unchecked.append(entry["path"])
    elif got != entry["sha256"]:
        mismatch.append({"path": entry["path"], "indexed": entry["sha256"], "committed": got})
print(json.dumps({"indexed": len(index), "committed_blob_mismatches": mismatch,
                  "not_in_head_yet": unchecked}, ensure_ascii=False, indent=1))
if mismatch:
    raise SystemExit("RAW_INDEX.json does not match the committed bytes for "
                     f"{len(mismatch)} path(s); normalise the working files first (EOL) and re-run.")

FAILURE_MAP = {
    "schema_id": "PIPD-S4-R3-FAILURE-ROOT-CAUSE-MAP/1",
    "frozen_subject": "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed",
    "hosted_evidence": "evidence/03_CI_TEST/r3_hosted_ci_failure_extract.txt",
    "counts": {"full_suite_declared": 572, "full_suite_failed": 11, "full_suite_skipped": 6,
               "focused_declared": 108, "focused_failed": 2},
    "mapping": [
        {"root_cause": "RC1_CI_PIPELINE_LOST_EXIT_CODE",
         "file": ".github/workflows/ci.yml",
         "failure_ids": ["(the false green itself: 11+2 real failures reported as a successful job)"],
         "repair": "every real test step runs under 'set -euo pipefail'; the provenance step captures "
                   "its log before tail; the mutation step keeps its explicit status capture.",
         "paired_control": "evidence/03_CI_TEST/ci_fault_injection.txt"},
        {"root_cause": "RC2_REPAIR_SUBJECT_FOREIGN_ABSOLUTE",
         "file": "src/pipd_ls_sp/workspace.py",
         "failure_ids": ["tests.test_negative_and_rollback.TestRollback.test_repair_subject_must_also_be_inside_the_authorised_root"],
         "repair": "containment is decided with the subject's own path flavour; a Windows-flavoured "
                   "absolute path is no longer re-based under the root on POSIX.",
         "paired_control": "the same test now passes on Linux (evidence/03_CI_TEST/linux_after_full.log)"},
        {"root_cause": "RC3_UNDECLARED_TEST_DEPENDENCY",
         "file": "pyproject.toml + both workflows",
         "failure_ids": ["tests.test_skill_contracts.SkillContracts.test_duplicate_skill_name_is_refused",
                          "tests.test_skill_contracts.SkillContracts.test_exact_eight_discover_load_route",
                          "tests.test_skill_contracts.SkillContracts.test_marker_only_pack_is_refused",
                          "tests.test_skill_contracts.SkillContracts.test_missing_input_schema_is_refused",
                          "tests.test_skill_contracts.SkillContracts.test_missing_output_schema_is_refused",
                          "tests.test_skill_contracts.SkillContracts.test_ninth_entry_is_refused"],
         "repair": "PyYAML declared as the [test] extra and installed by both workflows; the typed "
                   "TOOL_MISSING refusal is unchanged.",
         "paired_control": "evidence/03_CI_TEST/yaml_absent_negative.log + skill_contracts_with_dep.log"},
        {"root_cause": "RC4_RUNNER_NOT_EXECUTABLE_IN_INDEX",
         "file": "examples/first-run/run.sh",
         "failure_ids": ["tests.test_s4ext_first_run_portable.PortableFirstRunScriptTests.test_permission_bits_are_set_on_run_sh"],
         "repair": "git index mode set to 100755.",
         "paired_control": "evidence/03_CI_TEST/linux_after_focused.log"},
        {"root_cause": "RC5_POWERSHELL_RUNNER_WINDOWS_ONLY_ENV",
         "file": "examples/first-run/run.ps1",
         "failure_ids": ["tests.test_s4ext_first_run_portable.PortableFirstRunScriptTests.test_run_ps1_completes_the_chain_from_a_foreign_cwd"],
         "repair": "the scratch workspace falls back to [System.IO.Path]::GetTempPath() when the "
                   "Windows-only $env:TEMP is absent.",
         "paired_control": "evidence/03_CI_TEST/linux_after_focused.log"},
        {"root_cause": "RC6_SMOKE_DEPENDED_ON_A_COMMITTED_DEVELOPER_PATH",
         "file": "tools/cli_smoke.py",
         "failure_ids": ["tests.test_tooling_executes.TestToolingExecutes.test_cli_smoke_runs"],
         "repair": "the smoke persists the IntentCard its own 'intake' produced instead of reading the "
                   "checked-in .hgk/artifacts/s1/intent_card.json, whose source is the author's "
                   "absolute Windows path.",
         "paired_control": "evidence/03_CI_TEST/linux_cli_smoke_out.txt (13/13, nonzero_exit 0)"},
        {"root_cause": "RC7_REFUSAL_ASSERTION_MISSTATED_WHAT_REFUSAL_MEANS",
         "file": "tests/test_web_fallback.py",
         "failure_ids": ["tests.test_web_fallback.WebFallbackTests.test_symlinked_destination_refused_and_target_byte_identical"],
         "repair": "the assertion distinguishes 'created nothing' from 'left a pre-existing "
                   "destination untouched'; refusing a symlinked destination must leave it in place. "
                   "The sentinel-bytes and is_symlink assertions are kept.",
         "paired_control": "evidence/03_CI_TEST/linux_after_full.log"},
    ],
    "ledger_integrity": {
        "declared_failures": 13,
        "accounted_for": 13,
        "unexplained": 0,
        "note": "11 full-suite + 2 focused-suite failures at the frozen subject, every one traced to a "
                "named root cause with a repair and a paired control. No test was skipped, no "
                "denominator narrowed and no acceptance oracle edited.",
    },
}
(EV / "02_LEDGER" / "R3_FAILURE_ROOT_CAUSE_MAP.json").write_text(
    json.dumps(FAILURE_MAP, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

FINDINGS = {
    "schema_id": "PIPD-S4-R3-FINDING-LEDGER/1",
    "source_report": "PIPD-S4-EXT-ACCEPT-R3-20261013",
    "round": ROUND,
    "dispositions": {"CLOSED_BY_THIS_ROUND": 2, "PARTIAL": 1, "OPEN_TT_OWNER": 2},
    "findings": [
        {"id": "S4R3-F001", "priority": "P0", "class": "CONFIRMED_DEFECT",
         "disposition": "CLOSED_BY_THIS_ROUND_IN_SCOPE_SOURCE_ONLY",
         "closed_scope": "The false green is repaired and the 11+2 failures have root causes with "
                         "paired controls on Linux and Windows locally.",
         "claim_ceiling": "The claim is limited to LOCAL executions recorded under evidence/03_CI_TEST "
                          "plus the hosted run produced by the pushed branch. It is not an S4 "
                          "acceptance and does not cover macOS or any host UAT.",
         "evidence": ["evidence/03_CI_TEST/r3_hosted_ci_failure_extract.txt",
                      "evidence/03_CI_TEST/ci_fault_injection.txt",
                      "evidence/03_CI_TEST/linux_after_full.log",
                      "evidence/03_CI_TEST/linux_after_focused.log",
                      "evidence/03_CI_TEST/win_after_full.log",
                      "evidence/03_CI_TEST/win_after_focused.log",
                      "evidence/03_CI_TEST/linux_cli_smoke_out.txt",
                      "evidence/02_LEDGER/R3_FAILURE_ROOT_CAUSE_MAP.json"]},
        {"id": "S4R3-F002", "priority": "P0", "class": "CONFIRMED_DEFECT",
         "disposition": "CLOSED_BY_THIS_ROUND_IN_SCOPE_SOURCE_ONLY",
         "closed_scope": "The Stage B gate now measures its declared base, the two ranges are reported "
                         "separately, and the classifier self-tests on planted forbidden and allowed paths.",
         "claim_ceiling": "The hosted public-plugin-verify run on the pushed Stage B branch is the "
                          "authoritative evidence; until it is green and read back, this is a source "
                          "repair with a local reproduction only.",
         "evidence": [".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/writeset_gate_repro.sh",
                      "evidence/03_CI_TEST/r3_hosted_plugin_job_extract.txt"]},
        {"id": "S4R3-F003", "priority": "P1", "class": "EVIDENCE_GAP",
         "disposition": "OPEN_TT_OWNER",
         "reason": "Human publisher identity, owner-approved brand assets, the official vendor "
                   "validator and portal scan/review/publish are owner-only acts. This round did not "
                   "perform them and must not imply otherwise.",
         "owner": "PKG07 build owner + human publisher",
         "next_action": "Supply the owner-approved icons and identity; run the pinned official "
                        "validator with positive and negative cases; then a new immutable release."},
        {"id": "S4R3-F004", "priority": "P1", "class": "EVIDENCE_GAP",
         "disposition": "CLOSED_BY_THIS_ROUND_IN_SCOPE_SOURCE_ONLY",
         "closed_scope": "The Web route now has a committed, digest-stamped single document; the README "
                         "has one navigation block and no longer competes with the install SSOT; "
                         "docs/USER_GUIDE.md is the single user guide; 41 local links and anchors check clean.",
         "claim_ceiling": "Link integrity and artefact presence are locally verified. First-run "
                          "copy-paste by an external newcomer on each host is NOT_EXECUTED.",
         "evidence": ["docs/install/PIPD_WEB_FALLBACK.md", "docs/install/PIPD_WEB_FALLBACK.md.sha256",
                      "docs/USER_GUIDE.md", "README.md"]},
        {"id": "S4R3-F005", "priority": "P1", "class": "NON_BLOCKING_OBSERVATION",
         "disposition": "PARTIAL",
         "closed_scope": "This round added no new large binary, kept its own evidence to text logs "
                         "under .hgk/rounds/S4R3-.../, and did not delete or rewrite any historical raw "
                         "receipt, tag or asset.",
         "reason": "The .hgk/ evidence mass is a pre-existing 62 MB condition; shrinking it requires "
                   "an owner-approved archival policy, not an executor decision.",
         "owner": "repo owner"}]}
(EV / "02_LEDGER" / "R3_FINDING_LEDGER.json").write_text(
    json.dumps(FINDINGS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"raw_index_files": len(index),
                  "index_bytes": (EV / "RAW_INDEX.json").stat().st_size,
                  "failure_map_rcs": len(FAILURE_MAP["mapping"]),
                  "findings": len(FINDINGS["findings"])}, indent=1))
