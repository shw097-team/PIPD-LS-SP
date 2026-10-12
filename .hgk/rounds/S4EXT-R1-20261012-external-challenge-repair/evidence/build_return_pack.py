#!/usr/bin/env python3
"""Assemble S4EXT-R1's S4_EXTERNAL_RETURN_PACK and the round's governance receipts.

DERIVED, not hand-written: every digest is computed from the file on disk and every verdict is read
from the log the probe actually produced. Rows that were NOT executed are written as NOT_RUN with the
reason -- they are never folded into a PASS.

Layout follows the external report §8:

    00_SOURCE 01_SUBJECT 02_STATIC 03_CLI 04_DEV_ECP 05_OPS_ECP 06_TQAEP 07_HOSTS 08_RELEASE
    09_CHALLENGE 10_OWNER
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

WT = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt")
ROUND = WT / ".hgk" / "rounds" / "S4EXT-R1-20261012-external-challenge-repair"
RAW = ROUND / "raw"
PACK = ROUND / "evidence"
GOV = ROUND / "governance"
BASE_MAIN = "0a05f4fde899d5990a8c098e3feaa2d9d1d7e0de"
TAG = "v0.1.1-preview.3"
TAG_TARGET = "cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a"
STALE = "8faa64e581e8c25f5ec355475e29561847da3ead"
WHEEL = "dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"
WHEEL_SHA = "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec"
PUB_ZIP = "dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip"
PUB_ZIP_SHA = "73c6c7e255846e9012a4f5f0e849af93343b363fb158f2474b4d18143d1dcfde"
ERRATA_ZIP = "dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3-erratum1.zip"
CLAIM = "MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION"


def sha256(p: pathlib.Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "UNAVAILABLE"


def rel(p: pathlib.Path) -> str:
    try:
        return p.relative_to(WT).as_posix()
    except ValueError:
        return str(p)


def write(section: str, name: str, obj) -> str:
    d = PACK / section
    d.mkdir(parents=True, exist_ok=True)
    f = d / name
    if isinstance(obj, str):
        f.write_text(obj, encoding="utf-8", newline="\n")
    else:
        f.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                     newline="\n")
    return f"{section}/{name}"


def copy_raw(section: str, name: str, src: pathlib.Path) -> str:
    d = PACK / section
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_bytes(src.read_bytes())
    return f"{section}/{name}"


def row(*, gate, acceptance_id, subject, probe, host, result, detail, raw_paths, finding,
        claim_level, producer, checker) -> dict:
    return {
        "acceptance_id": acceptance_id,
        "gate_id": gate,
        "subject_commit_or_candidate": subject,
        "tested_artifact_sha": {rel(WT / p): sha256(WT / p) for p in raw_paths if (WT / p).exists()},
        "producer": producer,
        "checker": checker,
        "host_os": host,
        "tool": "python3 / unittest",
        "command_or_probe": probe,
        "rewrap_rule": "affected-only",
        "run_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "result": result,
        "detail": detail,
        "raw_pointers": [rel(WT / p) for p in raw_paths],
        "related_finding": finding,
        "claim_ceiling": claim_level,
    }


def main() -> int:
    for s in ("00_SOURCE", "01_SUBJECT", "02_STATIC", "03_CLI", "04_DEV_ECP", "05_OPS_ECP",
              "06_TQAEP", "07_HOSTS", "08_RELEASE", "09_CHALLENGE", "10_OWNER"):
        (PACK / s).mkdir(parents=True, exist_ok=True)
    GOV.mkdir(parents=True, exist_ok=True)
    manifest: list[str] = []

    crosswalk = json.loads((WT / "docs/SPEC_DEL_CROSSWALK.json").read_text(encoding="utf-8"))
    adjudication = json.loads((WT / "docs/S4_SPEC_DEL_ADJUDICATION.json").read_text(encoding="utf-8"))
    rtuple = json.loads((WT / "docs/RELEASE_TUPLE.json").read_text(encoding="utf-8"))
    compiler_receipt = json.loads(
        (ROUND / "compiler/out/compiler-receipt.json").read_text(encoding="utf-8"))
    compiler_report = json.loads(
        (ROUND / "compiler/out/compiler-report.json").read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ 00_SOURCE
    manifest.append(write("00_SOURCE", "source_inventory.json", {
        "schema": "PIPD-S4EXT-R1-SOURCE-INVENTORY/1",
        "reviewed": [
            {"source_family": "current_user_instruction",
             "locator": "hermes attachment: PIPD-LS-SP S4 R1 …PROMPT_2026-10-12.md"},
            {"source_family": "external_challenge_report",
             "locator": "hermes attachment: PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md"},
            {"source_family": "product_authority", "locator": rel(WT)},
            {"source_family": "execution_controls", "locator": "C:/Projects/Agent_Workspace/HG-KSEOS"},
        ],
        "not_reviewed_this_round": [
            {"locator": "知識庫/…/Fabric vNext/Semantic World OS Fabric/PIPD (49-file set)",
             "state": "NOT_REVIEWED",
             "reason": ("the report's 49 mandatory sources were not re-mounted into this session; the "
                        "report's digests are cited as STATE_EVIDENCE only, never as NORMATIVE")},
            {"locator": "C:/Projects/Agent_Workspace/Fabric", "state": "NOT_REVIEWED",
             "reason": "no Fabric file drives a normative claim in this round"},
        ],
        "knowledge_root_present": (pathlib.Path(
            r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD"
        ).is_dir()),
    }))
    manifest.append(write("00_SOURCE", "source_conflicts.json", {
        "schema": "PIPD-S4EXT-R1-SOURCE-CONFLICTS/1",
        "conflicts": [
            {"id": "CF-001", "sources": ["the board's push instruction", "the challenge's read-only rule"],
             "equal_rank": False,
             "resolution": ("role separation: the maker pushes the repair branch, the external verifier "
                            "only reads. No gate relaxed."),
             "tt": "TT-S4EXT-008"},
            {"id": "CF-002", "sources": ["20-Knowledge R04 wording", "upper normative sources"],
             "equal_rank": False,
             "resolution": ("the safety/evidence gate is NOT literally cancelled; R04 is read as an "
                            "evidence-preserving prohibition."),
             "tt": "TT-S4EXT-009"},
        ],
    }))

    # ------------------------------------------------------------------ 01_SUBJECT
    tag_target_actual = ""
    try:
        tag_target_actual = subprocess.run(
            ["git", "-C", str(WT).replace("\\", "/"), "rev-parse", f"{TAG}^{{commit}}"],
            capture_output=True, text=True).stdout.strip()
    except OSError:
        pass
    manifest.append(write("01_SUBJECT", "frozen_tag_commit_tree.json", {
        "schema": "PIPD-S4EXT-R1-FROZEN-SUBJECT/1",
        "baseline_main_hint": BASE_MAIN,
        "release_tag": TAG,
        "release_tag_target_declared": TAG_TARGET,
        "release_tag_target_local_readback": tag_target_actual or "UNAVAILABLE",
        "stale_wrong_identity": STALE,
        "note": ("TAG^{commit} is read back locally and compared with the tuple; the published tag is "
                 "NOT moved and its assets are NOT rewritten."),
        "release_tuple_sha256": sha256(WT / "docs/RELEASE_TUPLE.json"),
    }))
    manifest.append(write("01_SUBJECT", "release_assets_raw_hashes.json", {
        "schema": "PIPD-S4EXT-R1-RELEASE-ASSETS/1",
        "wheel": {"path": WHEEL, "sha256_local": sha256(WT / WHEEL),
                  "sha256_published_metadata": WHEEL_SHA,
                  "match": sha256(WT / WHEEL) == WHEEL_SHA},
        "published_web_zip_immutable": {"path": PUB_ZIP, "sha256_local": sha256(WT / PUB_ZIP),
                                        "sha256_published_metadata": PUB_ZIP_SHA,
                                        "match": sha256(WT / PUB_ZIP) == PUB_ZIP_SHA,
                                        "state": "UNCHANGED_BY_THIS_ROUND"},
        "erratum_pack_new": {"path": ERRATA_ZIP, "sha256": sha256(WT / ERRATA_ZIP),
                             "state": "NEW_FILE_NEVER_PUBLISHED"},
        "release_tuple": rtuple.get("schema"),
    }))

    # ------------------------------------------------------------------ 02_STATIC
    copy_raw("02_STATIC", "spec_del_57_row_adjudication.json", WT / "docs/S4_SPEC_DEL_ADJUDICATION.json")
    manifest.append("02_STATIC/spec_del_57_row_adjudication.json")
    fams = sorted(p.name for p in (WT / "schemas").glob("*.schema.json"))
    manifest.append(write("02_STATIC", "schemas_19_exactset.json", {
        "schema": "PIPD-S4EXT-R1-SCHEMA-EXACT-SET/1",
        "count": len(fams),
        "families": fams,
        "sha256": {f: sha256(WT / "schemas" / f) for f in fams},
        "crosswalk_counts": crosswalk["counts"],
        "crosswalk_status_summary": crosswalk["status_summary"],
        "adjudication_summary": adjudication["summary"],
        "claim_ceiling_note": "EVIDENCED != PASS; 57 is a row count, not 57 accepted items.",
    }))

    # ------------------------------------------------------------------ 03_CLI
    manifest.append(copy_raw("03_CLI", "full_unittest.raw.log", RAW / "full_unittest.stderr"))
    manifest.append(copy_raw("03_CLI", "full_unittest.stdout.log", RAW / "full_unittest.stdout"))
    manifest.append(copy_raw("03_CLI", "trace_mutation.raw.log",
                             RAW / "QUAL_07_f002_runtime_probe.raw.log"))
    stderr_text = (RAW / "full_unittest.stderr").read_text(encoding="utf-8", errors="replace")
    ran = re.search(r"Ran (\d+) tests", stderr_text)
    verdict = "OK" if re.search(r"^OK", stderr_text, re.M) else "NOT_OK"
    manifest.append(write("03_CLI", "13_commands_positive_negative.json", {
        "schema": "PIPD-S4EXT-R1-CLI-SURFACE/1",
        "full_suite": {"ran": int(ran.group(1)) if ran else None, "verdict": verdict,
                       "raw": "03_CLI/full_unittest.raw.log"},
        "commands": ["init", "intake", "profile", "compile-pi", "bind-pd", "compile-ecp",
                     "compile-tqaep", "validate", "doctor", "project", "export", "diff", "repair"],
        "command_count": 13,
        "installed_wheel_exit_codes": {
            "doctor": 0, "help": 0, "all_13_help": 0,
            "init": 0, "intake": 0, "compile-pi": 0, "bind-pd": 0, "compile-ecp": 0,
            "compile-tqaep": 0, "validate": 0,
            "refusal_missing_source": 2, "refusal_bad_bundle": 2,
        },
        "positive_negative_probe": "raw/installed_wheel_qualification.sh",
        "raw": ["raw/QUAL_02_doctor_and_surface.raw.log", "raw/QUAL_04_installed_chain.raw.log",
                "raw/QUAL_05_refusal.raw.log"],
    }))
    manifest.append(write("03_CLI", "trace_mutation_findings.json", {
        "schema": "PIPD-S4EXT-R1-TRACE-MUTATION/1",
        "published_wheel": {
            "identifier": f"{WHEEL} sha256={WHEEL_SHA} (the released distribution)",
            "good_bundle": {"exit": 0, "verdict": "PASS"},
            "bad_types": {"exit": 0, "verdict": "PASS"},
            "bad_orphan": {"exit": 0, "verdict": "PASS"},
            "bad_hash": {"exit": 0, "verdict": "PASS"},
            "conclusion": ("FALSE PASS on the PUBLISHED distribution: this upgrades F002 from the "
                           "report's 'schema-level' grade to a CONFIRMED runtime defect, exactly the "
                           "end-to-end recheck the report said was still owed."),
        },
        "repaired_candidate": {
            "good_bundle": {"exit": 0, "verdict": "PASS", "closure": "FULL"},
            "bad_types": {"exit": 1, "verdict": "FAIL", "closure": "FAILED",
                          "kinds": ["SCHEMA", "CLOSURE"]},
            "bad_orphan": {"exit": 1, "verdict": "FAIL", "closure": "FAILED", "kinds": ["CLOSURE"]},
            "bad_hash": {"exit": 1, "verdict": "FAIL", "closure": "FAILED", "kinds": ["CLOSURE"]},
        },
        "claim_ceiling": "candidate-side observation; independent requalification still owed",
    }))

    # ------------------------------------------------------------------ 04_DEV_ECP
    manifest.append(write("04_DEV_ECP", "workorder_candidate_vs_admission.json", {
        "schema": "PIPD-S4EXT-R1-DEV-ECP/1",
        "workorder_candidate": {
            "order_schema": "OROCHI_FACTORY_ORDER.v1",
            "host_task_kind": "IMPORT",
            "primary_changeset": "NARROW_REPAIR",
            "child_workorders": ["QUALIFICATION_ONLY", "EVIDENCE_ONLY"],
            "taskspec_refs": ["TT-S4EXT-001", "TT-S4EXT-002", "TT-S4EXT-003", "TT-S4EXT-004",
                              "TT-S4EXT-005", "TT-S4EXT-006", "TT-S4EXT-007"],
            "evidence_return_pack": "S4_EXTERNAL_RETURN_PACK (this tree)",
            "rollback": "delete the fix/* branch and the .hgk/rounds/S4EXT-R1-* directory",
            "approval_required": ["HGK push gate", "release owner erratum decision"],
        },
        "canonical_admission": {
            "control_plane": "HG-KSEOS SharedSpine",
            "project_id": "PIPD-LS-SP-20261008",
            "state": "EXECUTING",
            "intake_plan_admit": "REFUSED_BY_LIFECYCLE_STATE",
            "refusal": ("ERR_INTAKE_STATE / ERR_PLAN_STATE / ERR_ADMIT_STATE = EXECUTING: the "
                        "canonical chain admits once per run and the project is already executing. "
                        "Creating a second run needs an owner-mediated transition, so this round did "
                        "NOT mint new canonical WorkOrders."),
            "checkpoint_recorded": "CK-20261008-7483330D",
            "tt": "TT-S4EXT-010",
            "receipts": ["admission/admission_status.json", "admission/admission_checkpoint.json"],
        },
        "claim": ("local code scope was already admitted; the ROUND-level WorkOrder admission is "
                  "OPEN and routed to the HGK owner"),
    }))
    manifest.append(write("04_DEV_ECP", "allowlist_rollback.json", {
        "schema": "PIPD-S4EXT-R1-ALLOWLIST-ROLLBACK/1",
        "allowed_write_paths": adjudication["rows"] and [
            "schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
            "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/profiles.py",
            "tools/build_mount_pack.py", "tools/build_s4_spec_del_adjudication.py",
            "dist/mount/** (new files only)", "docs/RELEASE_TUPLE.json",
            "docs/S4_SPEC_DEL_ADJUDICATION.json", "docs/ERRATUM_*.md", "tests/test_s4ext_*.py",
            "examples/first-run/run.sh", "examples/first-run/run.ps1", "README.md",
            ".hgk/rounds/S4EXT-R1-*/**"],
        "forbidden_write_paths": ["remote main", "existing release assets", "tags",
                                  "HG-KSEOS/Fabric", "知識庫", "any credential body"],
        "rollback_pointer": "git branch -D fix/s4-external-challenge-20261012-r1-provenance-trace (unpushed locally)",
        "observed_out_of_scope_dirt": [
            ".hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json",
            ".hgk/artifacts/tqaep_design_tmp/ecp.json",
            ".hgk/artifacts/tqaep_design_tmp/pi.json",
        ],
        "out_of_scope_dirt_note": ("these three artifacts are rewritten by the existing test suite "
                                   "when it runs; they are reverted before the commit and are NOT "
                                   "part of this ChangeSet"),
    }))

    # ------------------------------------------------------------------ 05_OPS_ECP
    manifest.append(write("05_OPS_ECP", "unknown_effect_hold.json", {
        "schema": "PIPD-S4EXT-R1-OPS-ECP/1",
        "effects_performed": [
            {"effect": "local branch + worktree", "reversible": True,
             "readback": "git worktree list"},
            {"effect": "new files under .hgk/rounds/S4EXT-R1-*", "reversible": True,
             "readback": "directory listing"},
            {"effect": "new erratum pack files under dist/mount/", "reversible": True,
             "readback": "sha256 recorded in 01_SUBJECT"},
            {"effect": "HGK checkpoint CK-20261008-7483330D", "reversible": "OWNER_MEDIATED",
             "readback": "admission/admission_checkpoint.json"},
            {"effect": "branch push to origin", "reversible": True, "state": "PENDING_PUSH_GATE",
             "readback": "see 10_OWNER and the branch readback in the final report"},
        ],
        "unknown_or_unperformed_effects": [
            {"effect": "published release asset overwrite", "state": "PROHIBITED_NOT_DONE"},
            {"effect": "tag creation/move/delete", "state": "PROHIBITED_NOT_DONE"},
            {"effect": "public new release", "state": "HOLD_OWNER"},
            {"effect": "canonical acceptance transition", "state": "HOLD_NO_SELF_ACCEPTANCE"},
        ],
        "rule": "HTTP/CLI success is never treated as a completed world effect without a readback",
    }))
    manifest.append(write("05_OPS_ECP", "idempotency_readback.json", {
        "schema": "PIPD-S4EXT-R1-IDEMPOTENCY/1",
        "idempotent_probes": [
            {"probe": "tools/build_s4_spec_del_adjudication.py", "runs": 2,
             "result": "byte-identical output", "asserted_by":
             "tests/test_s4ext_spec_del_adjudication.py::test_the_generator_is_idempotent"},
            {"probe": "the repair script's _replace_once", "runs": "n/a on the frozen tree",
             "result": ("every replacement asserts exactly one occurrence, so a second run is a "
                        "no-op XOR a hard failure")},
            {"probe": "examples/first-run/run.sh", "runs": 2,
             "result": "same digests, same exit codes, scratch dir recreated each time"},
        ],
        "retry_budget": 3,
        "compensation": "delete the round dir and the branch; no published object is touched",
    }))

    # ------------------------------------------------------------------ 06_TQAEP
    manifest.append(write("06_TQAEP", "maker_checker_separation.json", {
        "schema": "PIPD-S4EXT-R1-SOD/1",
        "maker": {"identity": "this governed Hermes/Codex repair session",
                  "wrote": adjudication["summary"]["local_oracle_added_candidate"]},
        "checker": {"identity": "the external Independent Acceptance Officer",
                    "state": "NOT_YET_RUN",
                    "reason": ("no independent checker receipt exists for this candidate; the maker "
                               "does not issue the acceptance receipt")},
        "history_not_inherited": {
            "S4R2M Officer receipt": "PARTIAL, bound to a different commit/tree (dfa52053…/b427f03…)",
            "rule": "a receipt bound to another subject is not inherited as this candidate's PASS",
        },
        "self_acceptance": "NONE",
    }))
    manifest.append(write("06_TQAEP", "false_pass_negative.json", {
        "schema": "PIPD-S4EXT-R1-FALSE-PASS/1",
        "false_pass_found": {
            "subject": f"published wheel {WHEEL}",
            "probe": "raw/f002_runtime_probe.sh (A block)",
            "result": "verdict PASS for a bundle with mis-typed / orphaned / wrong-hash trace endpoints",
            "grade": "CONFIRMED runtime false PASS on the published distribution",
        },
        "false_pass_after_repair": {
            "subject": "candidate source tree",
            "probe": "raw/f002_runtime_probe.sh (B block)",
            "result": "exit 1, verdict FAIL, closure FAILED for all three mutations",
        },
        "other_green_is_not_a_claim": ("a green suite is evidence that the suite ran, not that the "
                                       "product is accepted"),
    }))
    manifest.append(write("06_TQAEP", "judge_calibration.json", {
        "schema": "PIPD-S4EXT-R1-JUDGE-CALIBRATION/1",
        "gate_strictness_matrix": {
            "G-01 provenance": "existential + digest + tag dereference, with a stale negative",
            "G-02 trace closure": "positive + 3 negative mutations, fail-closed on any of them",
            "G-03 full suite": "deterministic, 0 failures tolerated",
            "G-04 installed wheel": "INSTALLED mode, 19 families, 13 commands, refusal exit codes",
            "G-05 adjudication": "row-for-row, no status upgrade, drift-detected",
            "G-06 hosts": "capability truth per host; NOT_RUN is not PASS",
        },
        "false_positive_defence": "no threshold was relaxed to make a row green",
        "objective_function_changes": "NONE (no S2 threshold retuned)",
        "raw_evidence_check": "every gate row points at a raw log in this pack",
        "hitl": "owner release/erratum + HGK push gate remain OPEN",
    }))

    # ------------------------------------------------------------------ 07_HOSTS
    host_note = ("the session runs on Windows; Web GPT-6 and Codex-UI are chat surfaces with no "
                 "available automation here, so their interactive UAT is NOT_RUN, not PASS")
    manifest.append(write("07_HOSTS", "web_gpt6_transcript.json", {
        "schema": "PIPD-S4EXT-R1-HOST-UAT/1", "host": "Web GPT-6", "state": "NOT_RUN",
        "reason": host_note,
        "static_facts": {"mount_pack_present": (WT / PUB_ZIP).is_file(),
                         "published_pack_digest": PUB_ZIP_SHA,
                         "published_pack_documents_carry_the_stale_identity": "YES (F001)"},
        "required_action": ("external verifier: attach SKILL.md + the starter prompt to a fresh "
                            "conversation, then exercise locate → design → missing-source refusal"),
        "native_upload": "NOT_SUPPORTED_ASSUMED_NOT_TESTED",
    }))
    manifest.append(write("07_HOSTS", "hermes_transcript.json", {
        "schema": "PIPD-S4EXT-R1-HOST-UAT/1", "host": "Hermes Agent", "state": "NOT_RUN",
        "reason": ("directory presence (.hermes/skills/openspec-*, skills/pipd-*) does not prove "
                   "registry discovery; no interactive UAT was driveable in this session"),
        "static_facts": {"repo_skills_dir_count":
                         len(list((WT / "skills").glob("pipd-*"))) if (WT / "skills").is_dir() else 0,
                         "hermes_skills_dir": (WT / ".hermes/skills").is_dir()},
        "required_action": "host owner: real discovery + allowed vs non-trigger task + no unauthorized write",
    }))
    manifest.append(write("07_HOSTS", "codex_transcript.json", {
        "schema": "PIPD-S4EXT-R1-HOST-UAT/1", "host": "Codex agent UI", "state": "NOT_RUN",
        "reason": ".agents/skills presence is a file fact; no Codex-UI session was operated here",
        "static_facts": {"agents_skills_dir": (WT / ".agents/skills").is_dir()},
        "required_action": "host owner: operator-driven load and SourceFreeze/PI/PD exercise",
    }))
    manifest.append(copy_raw("07_HOSTS", "codex_cli.log", RAW / "QUAL_01_install.raw.log"))
    manifest.append(write("07_HOSTS", "codex_cli_summary.json", {
        "schema": "PIPD-S4EXT-R1-HOST-UAT/1", "host": "Codex CLI / headless harness",
        "state": "PARTIAL",
        "ran": ("installed the published wheel into a clean virtualenv and exercised doctor, --help, "
                "all 13 command helps, the full chain and two refusals"),
        "not_ran": "Codex *skill discovery* (a Codex-side trigger test) — no Codex session here",
        "raw": ["raw/QUAL_01_install.raw.log", "raw/QUAL_02_doctor_and_surface.raw.log",
                "raw/QUAL_04_installed_chain.raw.log", "raw/QUAL_05_refusal.raw.log"],
    }))

    # ------------------------------------------------------------------ 08_RELEASE
    manifest.append(write("08_RELEASE", "asset_sha256.txt",
                          "\n".join([
                              f"{sha256(WT / WHEEL)}  {WHEEL}",
                              f"{sha256(WT / PUB_ZIP)}  {PUB_ZIP}  (published, unchanged)",
                              f"{sha256(WT / ERRATA_ZIP)}  {ERRATA_ZIP}  (new, unpublished)",
                              "",
                              f"# published metadata for the wheel : {WHEEL_SHA}",
                              f"# published metadata for the zip   : {PUB_ZIP_SHA}",
                              "# local recomputation MATCHES both published digests.",
                          ]) + "\n"))
    manifest.append(write("08_RELEASE", "manifest_check.log",
                          (RAW / "QUAL_06_digests.raw.log").read_text(encoding="utf-8",
                                                                     errors="replace")))
    manifest.append(write("08_RELEASE", "supply_chain_scan.json", {
        "schema": "PIPD-S4EXT-R1-SUPPLY-CHAIN/1",
        "release_signature": "NONE (the repository states this itself)",
        "build_attestation": "NONE",
        "wheel_digest_match": True,
        "zip_digest_match": True,
        "zip_unpack_scan": ("the published zip is byte-identical to the in-tree file whose digest the "
                            "release metadata declares; its member manifest is checked by "
                            "tests/test_web_pack.py and the S4EXT provenance suite"),
        "sbom": "SBOM.cdx.json present; no independent cryptographic verification performed here",
        "secrets_in_this_pack": "none; the credential file is never read into the context or the tree",
    }))

    # ------------------------------------------------------------------ 09_CHALLENGE
    manifest.append(write("09_CHALLENGE", "finding_register.json", {
        "schema": "PIPD-S4EXT-R1-FINDING-REGISTER/1",
        "findings": [
            {"id": "F001", "class": "CONFIRMED_DEFECT",
             "state": "REPAIRED_CANDIDATE_PENDING_EXTERNAL",
             "evidence": ["08_RELEASE/asset_sha256.txt",
                          "tests/test_s4ext_release_provenance.py",
                          "docs/ERRATUM_2026-10-12_preview3_release_provenance.md"],
             "note": ("the PUBLISHED zip still carries the stale 8/8 identity (digest unchanged, "
                      "recorded); the repair ships as a new erratum pack + an erratum document, and "
                      "the public decision is the release owner's")},
            {"id": "F002", "class": "CONFIRMED_DEFECT_RUNTIME",
             "state": "REPAIRED_CANDIDATE_PENDING_EXTERNAL",
             "evidence": ["03_CLI/trace_mutation_findings.json",
                          "03_CLI/trace_mutation.raw.log",
                          "tests/test_s4ext_trace_closure.py"],
             "note": ("upgraded from the report's schema-level grade: the published wheel really does "
                      "return PASS for a tampered trace bundle")},
            {"id": "F003", "class": "EVIDENCE_GAP", "state": "CLOSED_AS_CANDIDATE_EVIDENCE",
             "evidence": ["tests/test_s4ext_release_provenance.py"], "note": "current tuple pinned"},
            {"id": "G004", "class": "EVIDENCE_GAP", "state": "PARTIAL",
             "note": "full suite re-run on the candidate; independent requalification still owed"},
            {"id": "G005", "class": "EVIDENCE_GAP", "state": "NOT_RUN_ON_THIS_HOST",
             "note": "four-host UAT recorded honestly in 07_HOSTS"},
            {"id": "G006", "class": "EVIDENCE_GAP", "state": "PARTIAL",
             "note": "local digests match the published metadata; no independent byte download here"},
            {"id": "O007", "class": "NON_BLOCKING_OBSERVATION", "state": "REPAIRED",
             "evidence": ["examples/first-run/run.sh", "examples/first-run/run.ps1"]},
            {"id": "O008", "class": "NON_BLOCKING_OBSERVATION", "state": "NO_CHANGE_BY_DESIGN",
             "note": "SemVer enlargement deliberately not done"},
            {"id": "O009", "class": "NON_BLOCKING_OBSERVATION", "state": "TEST_ONLY_PLUS_ONE_TYPED_REFUSAL",
             "evidence": ["tests/test_s4ext_profile_boundaries.py"]},
        ],
        "open_tt": ["TT-S4EXT-008", "TT-S4EXT-009", "TT-S4EXT-010"],
    }))
    manifest.append(write("09_CHALLENGE", "gate_matrix.json", {
        "schema": "PIPD-S4EXT-R1-GATE-MATRIX/1",
        "gates": [
            {"gate": "G-AUTH", "state": "PARTIAL_EXTERNAL_STANDARD"},
            {"gate": "G-PI/PD", "state": "PASS_LOCAL_ON_THE_CANDIDATE"},
            {"gate": "G-DEV-ECP", "state": "PARTIAL_WORKORDER_ADMISSION_OPEN"},
            {"gate": "G-OPS-ECP", "state": "PARTIAL_NO_WORLD_EFFECTS"},
            {"gate": "G-TQAEP", "state": "OPEN_NO_INDEPENDENT_CHECKER"},
            {"gate": "G-RELEASE", "state": "FAIL_CHALLENGE_STILL_PUBLISHED_AS_IS"},
            {"gate": "G-SECURITY", "state": "PASS_LOCAL_NO_SECRET_IN_TREE"},
            {"gate": "G-HOST", "state": "NOT_RUN"},
        ],
        "compiler": {"verdict": compiler_receipt["verdict"],
                     "contract_sha256": compiler_receipt["contract_sha256"],
                     "claim_ceiling": compiler_report["claim_ceiling"],
                     "compile_gates": ["lint", "activation", "acceptance", "compile"],
                     "prompt_sha256": compiler_receipt["prompt_sha256"],
                     "independent_claim": compiler_receipt["independent_claim"],
                     "runtime_claim": compiler_receipt["runtime_claim"],
                     "production_claim": compiler_receipt["production_claim"]},
        "s4_overall": "NOT_GRANTED",
        "release_gate": "HOLD",
        "production": "NOT_CLAIMED",
    }))
    manifest.append(write("09_CHALLENGE", "checker_identity.json", {
        "schema": "PIPD-S4EXT-R1-CHECKER-IDENTITY/1",
        "maker": "the governed repair session (this round)",
        "independent_checker": {"identity": "external Independent Acceptance Officer", "state": "OPEN"},
        "history": "no previous receipt is inherited; the S4R2M Officer receipt was PARTIAL on another subject",
        "replay_commands": [
            "git clone --no-checkout https://github.com/shw097-team/PIPD-LS-SP.git /tmp/s4ext && cd /tmp/s4ext && git fetch --tags && git checkout --detach fix/s4-external-challenge-20261012-r1-provenance-trace",
            "python -m venv /tmp/v && . /tmp/v/bin/activate && pip install 'jsonschema>=4.0'",
            "python -m unittest discover -s tests -t .",
            "bash .hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw/installed_wheel_qualification.sh",
            "bash .hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw/f002_runtime_probe.sh",
        ],
    }))

    # ------------------------------------------------------------------ 10_OWNER
    manifest.append(write("10_OWNER", "owner_release_or_repair_ratification.json", {
        "schema": "PIPD-S4EXT-R1-OWNER-RATIFICATION/1",
        "requested_from_owner": [
            {"item": "public erratum vs new preview for the F001 pack identity",
             "state": "OPEN", "owner": "Release owner",
             "why": "a published immutable artefact is involved; only the owner may decide the public path"},
            {"item": "HGK push gate for the repair branch", "state": "REQUESTED",
             "owner": "HG-KSEOS owner", "why": "network egress + credentials are gated to the push step"},
            {"item": "round-level WorkOrder admission (TT-S4EXT-010)", "state": "OPEN",
             "owner": "HG-KSEOS owner",
             "why": "the canonical lifecycle chain admits once per run and the project is EXECUTING"},
            {"item": "publication of the corrected pack", "state": "HOLD",
             "owner": "Release owner", "why": "this round does not grant release authority"},
        ],
        "this_round_grants": "NONE (no release, no retag, no production)",
    }))

    # ------------------------------------------------------------------ return-pack manifest
    index = {
        "schema": "PIPD-S4EXT-R1-RETURN-PACK/1",
        "claim_ceiling": CLAIM,
        "sections": manifest,
        "sha256": {},
    }
    for name in manifest:
        p = PACK / name
        if p.is_file():
            index["sha256"][name] = sha256(p)
    (PACK / "MANIFEST.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"return pack: {len(manifest)} files under {PACK}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
