#!/usr/bin/env python3
"""Build the CAPC prompt contract for PIPD-LS-SP round S4EXT-R1 (compiler gates C0-C9).

Deterministic input to the bundled ``construction-acceptance-prompt-compiler``
(``lint`` -> ``activation`` -> ``acceptance`` -> ``compile``). Generated, not hand-typed, so the
reviewed-source digests are real values.

Shape constraints the bundled linter enforces (read from ``prompt_contract_compiler.py``):

* exactly ONE ``source_scan.reviewed`` row per required source family, and ``source_scan.missing``
  must be empty for a lint PASS;
* every ACTIVE capability needs an acceptance edge whose ``subject_id`` IS the capability name, a
  closure ``action``, and -- when ``runtime_required_now`` -- a readiness row whose lifecycle carries
  all 16 stages with discover/bind/route/effective_load set;
* a row counts as "selected" if ANY of current_profile_selected / canonical_flow_referenced /
  automatic_route_target / user_experience_required is true, so a DEFERRED/PROHIBITED row must clear
  all four and must not ask for INSTALL/QUALIFY/ENABLE;
* every required journey id, every ``active_requirement_ids`` entry and every ``requested_delivery``
  entry must be an acceptance ``subject_id``;
* runtime acceptance rows need depth >= L2, raw evidence, an independent checker and an independent
  terminal; no terminal state may be a non-terminal proxy word.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

WT = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt")
OUT = pathlib.Path(__file__).resolve().parent
HGK = pathlib.Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
COMPILER = pathlib.Path(
    r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/"
    r"construction-acceptance-prompt-compiler")
PROMPT_DIR = pathlib.Path(
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
    r"attachments")
BOARD = PROMPT_DIR / "PIPD-LS-SP S4 R1｜HERMES／HG-KSEOS／Fabric 受治理施工與驗收指揮薄 PROMPT_2026-10-12.md"
REPORT = PROMPT_DIR / "PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md"

WHEEL_SHA = "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec"
WEBZIP_SHA = "73c6c7e255846e9012a4f5f0e849af93343b363fb158f2474b4d18143d1dcfde"

C1 = "TraceLink endpoint typing and bundle graph closure (F002)"
C2 = "release provenance identity (F001/G006)"
C3 = "portable first-run path (O007)"
C4 = "installed wheel distribution (G006)"
C5 = "profiles boundary behaviour (O009)"

LC = ("identify", "pin", "install_materialize", "configure", "discover", "bind", "route",
      "effective_load", "doctor_health", "positive_pilot", "negative_security", "fallback",
      "rollback_uninstall", "independent_qualification", "certify", "enable")
TERMINALS = ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL"]


def sha(p: pathlib.Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "UNAVAILABLE"


def cap(capability, disposition, action, runtime, locators, visible, authority) -> dict:
    active = disposition in {"ACTIVE_REQUIRED", "ACTIVE_SELECTED"}
    return {
        "capability": capability, "source_disposition": "ACTIVE_REQUIRED",
        "current_execution_disposition": disposition,
        "current_profile_selected": active, "canonical_flow_referenced": active,
        "automatic_route_target": False,
        "user_experience_required": bool(active and visible),
        "runtime_required_now": runtime, "action": action, "source_locators": locators,
        "external_method": False, "control_authority": True, 
    }


def readiness(capability, acceptance_ids, work) -> dict:
    lc = {k: "NOT_APPLICABLE_SOURCE_BACKED" for k in LC}
    lc.update({"identify": "PASS", "pin": "PASS", "install_materialize": "PASS",
               "configure": "PASS", "discover": "PASS", "bind": "PASS", "route": "PASS",
               "effective_load": "PASS", "doctor_health": "PASS", "positive_pilot": "PASS",
               "negative_security": "PASS", "fallback": "PASS", "rollback_uninstall": "PASS",
               "independent_qualification": "OPEN", "certify": "OPEN", "enable": "OPEN"})
    return {"capability": capability, "required_now": True, "lifecycle": lc,
            "current_verdict": "NOT_READY", "work_required": work,
            "acceptance_ids": acceptance_ids}


def acc(aid, subject, stype, depth, runtime, locators, positive, negative, recovery) -> dict:
    return {"acceptance_id": aid, "subject_id": subject, "subject_type": stype,
            "source_locators": locators, "runtime_required": runtime, "required_depth": depth,
            "positive_fixture": positive, "negative_fixture": negative,
            "recovery_fixture": recovery, "raw_evidence_required": True,
            "independent_checker_required": True, "terminal_states": list(TERMINALS)}


def journey(jid, goal, visible, caps, expectations, locators, negative, recovery) -> dict:
    return {"journey_id": jid, "required": True, "user_goal": goal,
            "expected_visible_result": visible,
            "expected_automatic_behavior": ["paths/preconditions derived from the script itself"],
            "expected_manual_behavior": ["supply an interpreter only if PATH lacks one"],
            "allowed_hitl": [], "required_capabilities": caps,
            "negative_behavior": [negative], "failure_recovery": [recovery],
            "source_expectation_ids": expectations,
            "source_locators": locators}


def gate(gid, predicate, expected, probe, producer, checker, subject, head, package_sha,
         source_hashes, rerun, invalidation, verdict, claim) -> dict:
    return {"gate_id": gid, "predicate": predicate, "expected": expected,
            "command_or_probe": probe, "raw_receipt_required": True, "producer": producer,
            "independent_checker": checker,
            "candidate_binding": {"head": head, "package_sha256": package_sha,
                                  "source_hashes": [f"{k}={v}" for k, v in source_hashes.items()]},
            "tracked_subject": True, "rerun_rule": rerun, "invalidation": invalidation,
            "terminal_verdict": verdict, "runtime_pass_allowed": False, "claim_level": claim}


CONTRACT = {
    "schema": "CAPC-PROMPT-CONTRACT/1",
    "task_id": "S4EXT-R1-20261012-PIPD-LS-SP-NARROW-REPAIR",
    "source_scan": {
        "required_source_families": [
            "current_user_instruction", "external_challenge_report", "product_authority",
            "execution_controls", "acceptance_compiler"],
        "reviewed": [
            {"source_family": "current_user_instruction", "source_id": "SRC-BOARD",
             "locator": str(BOARD), "sha256": sha(BOARD), "role": "NORMATIVE", "critical": True},
            {"source_family": "external_challenge_report", "source_id": "SRC-CHALLENGE",
             "locator": str(REPORT), "sha256": sha(REPORT), "role": "STATE_EVIDENCE",
             "critical": True},
            {"source_family": "product_authority", "source_id": "SRC-PRODUCT-WT",
             "locator": str(WT), "sha256": sha(WT / "docs" / "SPEC_DEL_CROSSWALK.json"),
             "role": "NORMATIVE", "critical": True},
            {"source_family": "execution_controls", "source_id": "SRC-HGK-AGENTS",
             "locator": str(HGK / "AGENTS.md"), "sha256": sha(HGK / "AGENTS.md"),
             "role": "NORMATIVE", "critical": True},
            {"source_family": "acceptance_compiler", "source_id": "SRC-COMPILER",
             "locator": str(COMPILER / "construction-acceptance-prompt-compiler_SKILL.md"),
             "sha256": sha(COMPILER / "construction-acceptance-prompt-compiler_SKILL.md"),
             "role": "NORMATIVE", "critical": True}],
        "missing": [],
        "normative_claims": [
            {"claim_id": "NC-001",
             "text": ("F001 must be repaired without rewriting the published tag or its assets: the "
                      "build-source commit and the release-tag target become separate frozen fields "
                      "and the 8/8 pack documents must name the tag target."),
             "source_ids": ["SRC-CHALLENGE", "SRC-PRODUCT-WT"],
             "locators": [str(REPORT) + "#4 F001", "docs/RELEASE_TUPLE.json"]},
            {"claim_id": "NC-002",
             "text": ("F002 must fail closed: a bundle whose trace endpoints are mis-typed, orphaned "
                      "or hash-inconsistent must not reach verdict PASS, while legal positive and "
                      "legacy version=\"1\" instances keep passing."),
             "source_ids": ["SRC-CHALLENGE", "SRC-PRODUCT-WT"],
             "locators": [str(REPORT) + "#4 F002", "src/pipd_ls_sp/validate.py"]},
            {"claim_id": "NC-003",
             "text": ("F003 must be closed by pinning the CURRENT frozen release tuple rather than a "
                      "floating branch, keeping the historical preview.2 regression intact."),
             "source_ids": ["SRC-CHALLENGE"], "locators": [str(REPORT) + "#4 F003"]},
            {"claim_id": "NC-004",
             "text": ("Claim ceiling is PACKAGE: maker candidate and local tests only until an "
                      "external verifier requalifies the same frozen subject. No row may be disposed "
                      "as PASS and S4 stays NOT_GRANTED."),
             "source_ids": ["SRC-BOARD", "SRC-CHALLENGE"],
             "locators": [str(BOARD) + "#3", str(REPORT) + "#10"]},
            {"claim_id": "NC-005",
             "text": ("Scope discipline: no 20th schema family, no 9th skill, no 14th CLI verb, no "
                      "forced SemVer, no 12-axis risk engine, no S5-S8 activation."),
             "source_ids": ["SRC-CHALLENGE", "SRC-BOARD"],
             "locators": [str(REPORT) + "#5", str(BOARD) + "#4"]}],
    },
    "intent": {
        "goal": ("Repair the confirmed S4 findings of the external challenge (F001 release "
                 "provenance, F002 trace closure, F003 current-release regression pin), disposition "
                 "O007-O009 and the 57-row SPEC/DEL gaps, assemble the S4_EXTERNAL_RETURN_PACK, and "
                 "push the repair branch for external acceptance."),
        "user_expected_outcome": ("A repair branch whose mount-pack release identity is truthful and "
                                 "independently resolvable, whose validate path refuses a tampered "
                                 "trace bundle, and whose evidence pack lets an external verifier "
                                 "replay every claim from raw logs."),
        "user_expected_experience": ("Any new user can run the whole compiler chain in one portable "
                                     "command on Linux/Windows without the author's paths, and can "
                                     "see exactly which claims are maker-local."),
        "explicit_constraints": [
            "candidate-only writes; no agent self-acceptance",
            "the published v0.1.1-preview.3 tag and its release assets are immutable",
            "the credential file is read only at the push step, never through the LLM context",
            "no new schema family, skill, or CLI verb"],
        "non_goals": ["refactoring PIPD", "a second lifecycle or trace engine", "forced SemVer",
                      "a 12-axis risk engine", "S5-S8 / SQP1 / production activation",
                      "claiming S4 PASS or any release/production promotion"],
        "authorized_mutations": [
            "schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
            "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/profiles.py",
            "tools/build_mount_pack.py", "dist/mount/** (new erratum pack only)",
            "docs/RELEASE_TUPLE.json", "docs/S4_SPEC_DEL_ADJUDICATION.json",
            "docs/ERRATUM_2026-10-12_preview3_release_provenance.md",
            "tests/test_s4ext_*.py", "examples/first-run/run.sh", "examples/first-run/run.ps1",
            "README.md", ".hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/**"],
        "forbidden_mutations": [
            "remote main", "force-push", "merge", "tag move or delete",
            "overwriting a published release asset", "the knowledge base",
            "HG-KSEOS/Fabric policy and control", "any credential body"],
        "expected_autonomy": "MEDIUM",
        "allowed_hitl": ["owner release/erratum decision", "HGK push-gate approval",
                         "external verifier acceptance"],
        "requested_delivery": ["DEL-REPAIR-BRANCH", "DEL-RETURN-PACK", "DEL-ERRATUM"],
        "active_requirement_ids": ["REQ-F001", "REQ-F002", "REQ-F003", "REQ-O007", "REQ-O009"],
        "claim_ceiling": "PACKAGE",
    },
    "authority": {
        "sources": [
            {"id": "SRC-BOARD", "rank": "1", "path": "PIPD-LS-SP S4 R1 指揮薄 PROMPT_2026-10-12.md",
             "sha256": sha(BOARD), "locator": str(BOARD), "role": "NORMATIVE", "governs": True},
            {"id": "SRC-HGK-AGENTS", "rank": "2", "path": "HG-KSEOS/AGENTS.md",
             "sha256": sha(HGK / "AGENTS.md"), "locator": str(HGK / "AGENTS.md"),
             "role": "NORMATIVE", "governs": True},
            {"id": "SRC-PRODUCT-WT", "rank": "3", "path": "PIPD worktree", "sha256": "UNAVAILABLE",
             "locator": str(WT), "role": "NORMATIVE", "governs": True},
            {"id": "SRC-CHALLENGE", "rank": "4",
             "path": "PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md", "sha256": sha(REPORT),
             "locator": str(REPORT), "role": "STATE_EVIDENCE", "governs": False}],
        "conflicts": [
            {"conflict_id": "CF-001", "sources": ["SRC-BOARD", "SRC-CHALLENGE"],
             "equal_rank": False, "decision": "RESOLVED",
             "tt_id": "TT-S4EXT-008"},
            {"conflict_id": "CF-002", "sources": ["SRC-BOARD", "SRC-CHALLENGE"], "equal_rank": False,
             "decision": "RESOLVED",
             "tt_id": "TT-S4EXT-009"}],
        "missing_sources": [],
        "native_control_plane_ids": ["HG-KSEOS-SharedSpine"],
        "current_control_plane_id": "HG-KSEOS-SharedSpine",
    },
    "changeset": {
        "class": "NARROW_REPAIR", "baseline_required": True, "baseline_verified": True,
        "reuse_prior_pass": False,
        "affected_domains": ["schemas", "runtime", "tests", "docs", "examples", "dist/mount",
                             "release-metadata", "governance-evidence"],
        "affected_files": [
            "schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
            "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/profiles.py",
            "tools/build_mount_pack.py", "docs/RELEASE_TUPLE.json",
            "docs/S4_SPEC_DEL_ADJUDICATION.json",
            "docs/ERRATUM_2026-10-12_preview3_release_provenance.md",
            "tests/test_s4ext_release_provenance.py", "tests/test_s4ext_trace_closure.py",
            "tests/test_s4ext_first_run_portable.py", "tests/test_s4ext_profile_boundaries.py",
            "tests/test_s4ext_spec_del_adjudication.py",
            "examples/first-run/run.sh", "examples/first-run/run.ps1", "README.md"],
        "must_not_reopen": [
            "the published v0.1.1-preview.3 tag and assets", "historical FAIL receipts",
            "the legal legacy version=\"1\" grammar", "the 19-family schema ABI",
            "sealed S0-S3 scope", "unrelated tests and fixtures"],
        "scope_expansion_requires_hitl": True, "tracked_mutation": True,
        "product_mutation_allowed": True,
    },
    "execution_scope": [
        cap(C1, "ACTIVE_REQUIRED", "QUALIFY", True,
            ["schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
             "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/pipeline.py"], False, "PIPD core"),
        cap(C2, "ACTIVE_REQUIRED", "QUALIFY", True,
            ["dist/mount/**", "docs/RELEASE_TUPLE.json",
             "docs/ERRATUM_2026-10-12_preview3_release_provenance.md"], True, "PIPD release owner"),
        cap(C3, "ACTIVE_REQUIRED", "QUALIFY", True,
            ["README.md", "examples/first-run/run.sh", "examples/first-run/run.ps1"], True,
            "PIPD DX/docs owner"),
        cap(C4, "ACTIVE_REQUIRED", "QUALIFY", True,
            ["dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"], True, "PIPD release package"),
        cap(C5, "ACTIVE_REQUIRED", "QUALIFY", False, ["src/pipd_ls_sp/profiles.py"], False,
            "PIPD core"),
        cap("Web GPT-6 chat host", "DEFERRED_SOURCE_BACKED", "DEFER", False,
            ["dist/mount/**", "README.md"], False, "host owner"),
        cap("Hermes Agent skill host", "DEFERRED_SOURCE_BACKED", "DEFER", False,
            [".hermes/skills/**", "skills/pipd-*/SKILL.md"], False, "host owner"),
        cap("Codex agent host", "DEFERRED_SOURCE_BACKED", "DEFER", False,
            [".agents/skills/**"], False, "host owner"),
        cap("HG-KSEOS canonical acceptance transition", "PROHIBITED", "PROHIBIT", False,
            [str(HGK / "AGENTS.md")], False, "HG-KSEOS owner"),
        cap("S5-S8 GENIE JIT runtimes", "PROHIBITED", "PROHIBIT", False,
            [".hgk/artifacts/s4/S5_S8_BACKLOG.json"], False, "upstream stage gate"),
    ],
    "runtime_readiness": [
        readiness(C1, ["A-02", "A-10", "A-12"],
                  ["close independent_qualification with an external verifier"]),
        readiness(C2, ["A-01", "A-09", "A-11", "A-18"],
                  ["external verifier re-derives the 8/8 identity from the pushed branch",
                   "release owner decides public erratum vs new preview"]),
        readiness(C3, ["A-04", "A-06", "A-08", "A-14"],
                  ["no Ubuntu/macOS host is available here; the Windows and Git-Bash paths are run"]),
        readiness(C4, ["A-07"],
                  ["external verifier reruns the probe from the downloaded asset bytes"]),
    ],
    "journeys": [
        journey("J-01",
                "A brand-new user on Linux/Git-Bash runs the whole compiler chain from a fresh "
                "checkout.",
                "one command prints FIRST_RUN_OK and a validate verdict PASS with closure FULL",
                [C3, C4], ["O007"], ["examples/first-run/run.sh", "README.md"],
                "an unusable interpreter halts with PRECONDITION_FAIL and exit 3",
                "re-run with PYTHON=<interpreter>"),
        journey("J-02", "A brand-new user on Windows PowerShell runs the same chain.",
                "FIRST_RUN_OK and validate PASS with every native exit code checked",
                [C3, C4], ["O007"], ["examples/first-run/run.ps1", "README.md"],
                "a failing step aborts before the next", "read the printed step log"),
        journey("J-03",
                "An external verifier re-derives the mount pack's release identity from the frozen "
                "tuple and the git tag instead of trusting the pack's own text.",
                "8/8 documents name release_tag_target; a stale value fails the check",
                [C2], ["F001", "F003"],
                ["docs/RELEASE_TUPLE.json", "tests/test_s4ext_release_provenance.py"],
                "a document carrying the stale commit is refused",
                "regenerate the pack from the frozen tuple"),
        journey("J-04",
                "A verifier replays the F002 counterexample against an installed distribution.",
                "validate --bundle exits non-zero with CLOSURE findings on the repaired build, while "
                "the published build shows the recorded false PASS",
                [C1, C4], ["F002"], ["tests/test_s4ext_trace_closure.py"],
                "mis-typed, orphaned or hash-inconsistent endpoints never reach PASS",
                "read the findings list"),
    ],
    "acceptance": [
        acc("A-01", C2, "CAPABILITY", "L3_INTEGRATION_RUNTIME", True,
            ["dist/mount/**", "docs/RELEASE_TUPLE.json"],
            "8/8 documents naming release_tag_target",
            "a document carrying the stale 8faa64e5 identity",
            "regenerate via tools/build_mount_pack.py"),
        acc("A-02", C1, "CAPABILITY", "L3_INTEGRATION_RUNTIME", True,
            ["schemas/TraceLink.schema.json", "src/pipd_ls_sp/validate.py"],
            "the legal PI/PD/ECP/TQAEP bundle closes FULL",
            "bad type / orphan / wrong 64-hex hash / duplicated link / extra key",
            "the findings list names the offending edge"),
        acc("A-04", C3, "CAPABILITY", "L3_INTEGRATION_RUNTIME", True,
            ["examples/first-run/run.sh", "examples/first-run/run.ps1"],
            "run.sh and run.ps1 from a foreign cwd", "an unusable interpreter exits 3",
            "PYTHON=<interpreter>"),
        acc("A-07", C4, "CAPABILITY", "L3_INTEGRATION_RUNTIME", True,
            ["dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"],
            "pipd doctor PASS in INSTALLED mode, 13 commands, 19 families, full chain",
            "a missing source is refused with exit 2; a tampered trace is refused",
            "re-create the venv"),
        acc("A-05", C5, "CAPABILITY", "L2_UNIT_BEHAVIOR", False,
            ["src/pipd_ls_sp/profiles.py"],
            "3/4 and 6/7 axis thresholds, provider-off plus complexity",
            "non-string requested, unknown axis, duplicate axis, downgrade attempt",
            "typed ProfileVeto"),
        acc("A-06", "J-01", "JOURNEY", "L3_INTEGRATION_RUNTIME", True,
            ["examples/first-run/run.sh"], "the portable chain completes",
            "a broken precondition halts", "re-run with an interpreter"),
        acc("A-08", "J-02", "JOURNEY", "L3_INTEGRATION_RUNTIME", True,
            ["examples/first-run/run.ps1"], "the PowerShell chain completes",
            "a failing step aborts", "read the step log"),
        acc("A-09", "J-03", "JOURNEY", "L2_UNIT_BEHAVIOR", False,
            ["docs/RELEASE_TUPLE.json"], "8/8 identity re-derived", "stale identity refused",
            "regenerate from the tuple"),
        acc("A-10", "J-04", "JOURNEY", "L3_INTEGRATION_RUNTIME", True,
            ["tests/test_s4ext_trace_closure.py"], "the tampered bundle is refused",
            "the published build's false PASS is recorded", "read the findings"),
        acc("A-11", "REQ-F001", "REQUIREMENT", "L2_UNIT_BEHAVIOR", False,
            ["docs/ERRATUM_2026-10-12_preview3_release_provenance.md"],
            "the erratum states the published defect", "the published zip digest is unchanged",
            "n/a (documentation)"),
        acc("A-12", "REQ-F002", "REQUIREMENT", "L3_INTEGRATION_RUNTIME", True,
            ["src/pipd_ls_sp/validate.py"], "closure runs inside validate_bundle",
            "an orphan edge is refused", "read the findings"),
        acc("A-13", "REQ-F003", "REQUIREMENT", "L2_UNIT_BEHAVIOR", False,
            ["tests/test_s4ext_release_provenance.py"], "the current tuple is pinned",
            "the wrong old tag fails", "re-pin from the frozen tuple"),
        acc("A-14", "REQ-O007", "REQUIREMENT", "L3_INTEGRATION_RUNTIME", True,
            ["examples/first-run/run.sh"], "no developer path is required",
            "a missing precondition halts", "supply the interpreter"),
        acc("A-15", "REQ-O009", "REQUIREMENT", "L2_UNIT_BEHAVIOR", False,
            ["src/pipd_ls_sp/profiles.py"], "the documented boundaries hold",
            "a native AttributeError is not raised", "typed refusal"),
        acc("A-16", "DEL-REPAIR-BRANCH", "DELIVERABLE", "L2_UNIT_BEHAVIOR", False,
            ["fix/s4-external-challenge-20261012-r1-provenance-trace"], "the branch is pushed and reads back",
            "a push to main or a force-push is refused", "delete and re-push the branch"),
        acc("A-17", "DEL-RETURN-PACK", "DELIVERABLE", "L2_UNIT_BEHAVIOR", False,
            [".hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/evidence/"],
            "the pack carries every required section",
            "a NOT_RUN row is never counted as PASS", "re-run the producing probe"),
        acc("A-18", "DEL-ERRATUM", "DELIVERABLE", "L2_UNIT_BEHAVIOR", False,
            ["docs/ERRATUM_2026-10-12_preview3_release_provenance.md"],
            "the erratum is additive and cites the published digest",
            "the published asset is not rewritten", "n/a (documentation)"),
    ],
    "evidence": [
        gate("G-01", "8/8 pack documents name the frozen release_tag_target",
             "no stale identity outside an explicit disclosure line",
             "python -m unittest tests.test_s4ext_release_provenance",
             "PIPD repair owner (maker)", "external verifier", "docs/RELEASE_TUPLE.json",
             "CANDIDATE", WHEEL_SHA,
             {"dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip": WEBZIP_SHA},
             "affected-only", ["any change to the pack docs, the tuple or the generator"],
             "PARTIAL", "PACKAGE"),
        gate("G-02", "a tampered trace bundle must not reach PASS",
             "exit non-zero with CLOSURE findings; the legal bundle still PASSes",
             "bash .hgk/rounds/S4EXT-R1-*/raw/f002_runtime_probe.sh",
             "PIPD compiler owner (maker)", "external verifier", "src/pipd_ls_sp/validate.py",
             "CANDIDATE", "UNAVAILABLE", {"src/pipd_ls_sp/validate.py": "CANDIDATE"},
             "affected-only", ["any change to the schemas, validate.py or pipeline.py"],
             "PARTIAL", "PACKAGE"),
        gate("G-03", "the full deterministic suite passes on the frozen candidate",
             "0 failures and 0 errors", "python -m unittest discover -s tests -t .", "maker",
             "external verifier", "tests/", "CANDIDATE", "UNAVAILABLE", {"tests/": "CANDIDATE"},
             "full", ["any code, schema or test change"], "PARTIAL", "PACKAGE"),
        gate("G-04", "the installed wheel behaves as a distribution",
             "doctor PASS in INSTALLED mode, 19 families, chain plus refusal",
             "bash .hgk/rounds/S4EXT-R1-*/raw/installed_wheel_qualification.sh", "maker",
             "external verifier", "dist/", "PUBLISHED_SUBJECT", WHEEL_SHA,
             {"dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl": WHEEL_SHA}, "full",
             ["a new wheel build"], "PARTIAL", "PACKAGE"),
        gate("G-05", "the 57-row crosswalk is adjudicated without status upgrades",
             "9 gaps and 4 design-only rows answered; the crosswalk stays read-only",
             "python -m unittest tests.test_s4ext_spec_del_adjudication", "maker",
             "external verifier", "docs/S4_SPEC_DEL_ADJUDICATION.json", "CANDIDATE", "UNAVAILABLE",
             {"docs/SPEC_DEL_CROSSWALK.json": "READ_ONLY"}, "affected-only",
             ["any crosswalk or adjudication change"], "PARTIAL", "PACKAGE"),
        gate("G-06", "the four-host consumer qualification is recorded honestly",
             "each host: discover/load/positive/negative, or an explicit NOT_RUN",
             "see 07_HOSTS in the return pack", "host owner", "external verifier", "dist/mount/",
             "CANDIDATE", WHEEL_SHA, {"dist/mount/**": "CANDIDATE"}, "affected-only",
             ["a host capability change"], "BLOCKED_EXTERNAL", "PACKAGE"),
    ],
    "termination": {
        "terminal_states": ["PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"],
        "non_terminal_pause": ["PUSH_HOLD", "BLOCKED_EXTERNAL", "BLOCKED_HITL"],
        "checkpoint_required": True,
        "checkpoint_fields": ["task_id", "source_hashes", "current_candidate", "completed_gates",
                              "open_gates", "next_work_order", "rollback_pointer"],
        "retry_budget": 3,
        "rollback_pointer_required": True,
    },
    "render_policy": {
        "control_corpus_restatement": False, "embedded_control_bodies": [],
        "max_prompt_chars": 30000,
        "output_language": "Traditional Chinese with English technical identifiers",
    },
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "S4EXT-R1.CONTRACT.json"
    path.write_text(json.dumps(CONTRACT, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
