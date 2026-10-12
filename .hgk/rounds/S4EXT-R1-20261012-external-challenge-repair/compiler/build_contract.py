#!/usr/bin/env python3
"""Build the CAPC prompt contract for PIPD-LS-SP round S4EXT-R1 (compiler gate C0-C9).

The contract is the deterministic input to the bundled HG-KSEOS/general ``construction-acceptance-
prompt-compiler`` (``lint`` -> ``activation`` -> ``acceptance`` -> ``compile``). It is generated rather
than hand-typed so the digests of the reviewed sources are real values, not placeholders.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

WT = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt")
OUT = pathlib.Path(__file__).resolve().parent       # .hgk/rounds/<round>/compiler
PROMPT_DIR = pathlib.Path(
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
    r"attachments")
BOARD = PROMPT_DIR / "PIPD-LS-SP S4 R1｜HERMES／HG-KSEOS／Fabric 受治理施工與驗收指揮薄 PROMPT_2026-10-12.md"
REPORT = PROMPT_DIR / "PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md"
HGK = pathlib.Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
COMPILER = pathlib.Path(
    r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/construction-acceptance-prompt-compiler/"
    r"construction-acceptance-prompt-compiler")


def sha(p: pathlib.Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "UNAVAILABLE"


def src(family: str, sid: str, locator: str, role: str, critical: bool,
        path: pathlib.Path | None = None) -> dict:
    return {"source_family": family, "source_id": sid, "locator": locator,
            "sha256": sha(path) if path else "UNAVAILABLE", "role": role, "critical": critical}


LC = ("identify", "pin", "install_materialize", "configure", "discover", "bind", "route",
      "effective_load", "doctor_health", "positive_pilot", "negative_security", "fallback",
      "rollback_uninstall", "independent_qualification", "certify", "enable")


def lifecycle(**overrides: str) -> dict:
    base = {k: "NOT_APPLICABLE_SOURCE_BACKED" for k in LC}
    base.update(overrides)
    return base


CONTRACT = {
    "schema": "CAPC-PROMPT-CONTRACT/1",
    "task_id": "S4EXT-R1-20261012-PIPD-LS-SP-NARROW-REPAIR",
    "source_scan": {
        "required_source_families": [
            "current_user_instruction", "external_challenge_report", "product_authority",
            "execution_controls", "acceptance_compiler",
        ],
        "reviewed": [
            src("current_user_instruction", "SRC-BOARD", str(BOARD), "NORMATIVE", True,
                BOARD),
            src("external_challenge_report", "SRC-CHALLENGE", str(REPORT), "STATE_EVIDENCE", True,
                REPORT),
            src("product_authority", "SRC-PRODUCT", "C:/Projects/Agent_Workspace/PIPD", "NORMATIVE",
                True, WT / "docs" / "SPEC_DEL_CROSSWALK.json"),
            src("product_authority", "SRC-CROSSWALK", "docs/SPEC_DEL_CROSSWALK.json", "NORMATIVE",
                True, WT / "docs" / "SPEC_DEL_CROSSWALK.json"),
            src("product_authority", "SRC-RELEASE-TUPLE", "docs/RELEASE_TUPLE.json",
                "STATE_EVIDENCE", False, WT / "docs" / "RELEASE_TUPLE.json"),
            src("execution_controls", "SRC-HGK-AGENTS", "HG-KSEOS/AGENTS.md", "NORMATIVE", True,
                HGK / "AGENTS.md"),
            src("execution_controls", "SRC-HGK-SPINE", "HG-KSEOS/src/hg_kseos/spine.py",
                "NORMATIVE", True, HGK / "src" / "hg_kseos" / "spine.py"),
            src("acceptance_compiler", "SRC-COMPILER",
                "construction-acceptance-prompt-compiler_SKILL.md", "NORMATIVE", True,
                COMPILER / "construction-acceptance-prompt-compiler_SKILL.md"),
        ],
        "missing": ["SRC-KB-49", "SRC-FABRIC-POLICY"],
        "normative_claims": [
            {"claim_id": "NC-001",
             "text": ("F001 must be repaired without rewriting the published tag or its assets: the "
                      "build-source commit and the release-tag target become separate, frozen fields."),
             "source_ids": ["SRC-CHALLENGE", "SRC-PRODUCT", "SRC-RELEASE-TUPLE"],
             "locators": [str(REPORT) + "#F001", "docs/RELEASE_TUPLE.json"]},
            {"claim_id": "NC-002",
             "text": ("F002 must fail closed: a bundle whose trace endpoints are mis-typed, orphaned "
                      "or hash-inconsistent must not reach verdict PASS, while legal positive and "
                      "legacy version=\"1\" instances keep passing."),
             "source_ids": ["SRC-CHALLENGE", "SRC-PRODUCT"],
             "locators": [str(REPORT) + "#F002", "src/pipd_ls_sp/validate.py"]},
            {"claim_id": "NC-003",
             "text": ("F003 must be closed by pinning the CURRENT frozen release tuple (not a "
                      "floating branch) and keeping the historical preview.2 regression."),
             "source_ids": ["SRC-CHALLENGE"], "locators": [str(REPORT) + "#F003"]},
            {"claim_id": "NC-004",
             "text": ("Claim ceiling: maker candidate and local tests only, until an external "
                      "verifier requalifies the same frozen subject. No row may be disposed as PASS."),
             "source_ids": ["SRC-BOARD", "SRC-CHALLENGE"],
             "locators": [str(BOARD) + "#3", str(REPORT) + "#10"]},
            {"claim_id": "NC-005",
             "text": ("Scope discipline: no 20th schema family, no 9th skill, no 14th CLI verb, no "
                      "forced SemVer, no 12-axis risk engine, no S5-S8 activation."),
             "source_ids": ["SRC-CHALLENGE", "SRC-BOARD"],
             "locators": [str(REPORT) + "#5", str(BOARD) + "#4"]},
        ],
    },
    "intent": {
        "goal": ("Repair the three confirmed/insufficiently-evidenced S4 findings of the external "
                 "challenge report (F001 release provenance, F002 trace closure, F003 current-release "
                 "regression pin), disposition the observations O007-O009 and the 57-row SPEC/DEL "
                 "gaps, produce the S4_EXTERNAL_RETURN_PACK, and push the repair branch to origin "
                 "for external acceptance."),
        "user_expected_outcome": ("A repair branch whose mount-pack release identity is truthful and "
                                 "independently resolvable, whose validate path refuses a tampered "
                                 "trace bundle, and whose evidence pack lets an external verifier "
                                 "replay every claim from raw logs."),
        "user_expected_experience": ("The user (or any new user) can run the whole compiler chain in "
                                     "one portable command on Linux/Windows without the author's "
                                     "paths, and can see exactly which claims are maker-local."),
        "explicit_constraints": [
            "candidate-only writes; no agent self-acceptance",
            "the published v0.1.1-preview.3 tag and its release assets are immutable",
            "the credential file is read only at the push step, never via the LLM context",
            "no new schema family, skill, or CLI verb",
        ],
        "non_goals": [
            "refactoring PIPD", "a second lifecycle or trace engine", "forced SemVer",
            "a 12-axis risk engine", "S5-S8 / SQP1 / production activation",
            "claiming S4 PASS or any release/production promotion",
        ],
        "authorized_mutations": [
            "schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
            "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/profiles.py",
            "tools/build_mount_pack.py", "dist/mount/** (erratum pack, new file)",
            "docs/RELEASE_TUPLE.json", "docs/S4_SPEC_DEL_ADJUDICATION.json",
            "docs/ERRATUM_2026-10-12_preview3_release_provenance.md",
            "tests/test_s4ext_*.py", "examples/first-run/run.sh", "examples/first-run/run.ps1",
            "README.md", ".hgk/rounds/S4EXT-R1-*/**",
        ],
        "forbidden_mutations": [
            "remote main", "force-push", "merge", "tag move/delete",
            "overwriting a published release asset", "knowledge base",
            "HG-KSEOS/Fabric policy and control", "any credential body",
        ],
        "expected_autonomy": "MEDIUM",
        "allowed_hitl": ["owner release/erratum decision", "HGK push gate approval",
                         "external verifier acceptance"],
        "requested_delivery": [
            "repair branch fix/s4ext-external-challenge-20261012-r1-*",
            "S4_EXTERNAL_RETURN_PACK under the round dir",
            "erratum document for the published preview.3 pack",
        ],
        "active_requirement_ids": ["F001", "F002", "F003", "G004", "G005", "G006",
                                   "O007", "O008", "O009",
                                   "TT-S4EXT-001", "TT-S4EXT-002", "TT-S4EXT-003",
                                   "TT-S4EXT-004", "TT-S4EXT-005", "TT-S4EXT-006",
                                   "TT-S4EXT-007"],
        "claim_ceiling": "PACKAGE",
    },
    "authority": {
        "sources": [
            {"id": "SRC-BOARD", "rank": 1,
             "path": "PIPD-LS-SP S4 R1 指揮薄 PROMPT_2026-10-12.md", "sha256": sha(BOARD),
             "locator": str(BOARD), "role": "NORMATIVE",
             "governs": "this round's authorised scope and claim ceiling"},
            {"id": "SRC-HGK-AGENTS", "rank": 2, "path": "HG-KSEOS/AGENTS.md",
             "sha256": sha(HGK / "AGENTS.md"), "locator": str(HGK / "AGENTS.md"), "role": "NORMATIVE",
             "governs": "the single control plane, admission and push-gate policy"},
            {"id": "SRC-PRODUCT", "rank": 3, "path": "PIPD (worktree)",
             "sha256": "UNAVAILABLE", "locator": str(WT), "role": "NORMATIVE",
             "governs": "product code, schemas, tests and the 57-row crosswalk"},
            {"id": "SRC-CHALLENGE", "rank": 4,
             "path": "PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md", "sha256": sha(REPORT),
             "locator": str(REPORT), "role": "STATE_EVIDENCE",
             "governs": "the findings to close; never a super-SSOT instruction"},
        ],
        "conflicts": [
            {"conflict_id": "CF-001",
             "sources": ["SRC-BOARD", "SRC-CHALLENGE"],
             "equal_rank": False,
             "decision": ("The board's 'push the repair branch' instruction and the challenge's "
                          "'read-only, verifier must not modify the subject' boundary do not "
                          "contradict once roles are separated: the maker pushes the branch, the "
                          "external verifier only reads. No gate is relaxed."),
             "tt_id": "TT-S4EXT-008"},
            {"conflict_id": "CF-002",
             "sources": ["SRC-BOARD"],
             "equal_rank": False,
             "decision": ("The 20-Knowledge R04 'MUST NOT + positive safety obligation' wording is "
                          "resolved in favour of the upper sources: the safety/evidence gate is NOT "
                          "literally cancelled; the obligation is read as an evidence-preserving "
                          "prohibition, recorded as TT-S4EXT-009 for the knowledge owner."),
             "tt_id": "TT-S4EXT-009"},
        ],
        "missing_sources": ["SRC-KB-49", "SRC-FABRIC-POLICY"],
        "native_control_plane_ids": ["HG-KSEOS-SharedSpine"],
        "current_control_plane_id": "HG-KSEOS-SharedSpine",
    },
    "changeset": {
        "class": "NARROW_REPAIR",
        "baseline_required": True,
        "baseline_verified": True,
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
            "examples/first-run/run.sh", "examples/first-run/run.ps1", "README.md",
        ],
        "must_not_reopen": [
            "the published v0.1.1-preview.3 tag and assets", "historical FAIL receipts",
            "the legal legacy version=\"1\" grammar", "the 19-family schema ABI",
            "sealed S0-S3 scope", "unrelated tests and fixtures",
        ],
        "scope_expansion_requires_hitl": True,
        "tracked_mutation": True,
        "product_mutation_allowed": True,
    },
    "execution_scope": [
        {"capability": "TraceLink endpoint typing + bundle graph closure (F002)",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "ACTIVE_REQUIRED",
         "current_profile_selected": True, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": False,
         "runtime_required_now": True,
         "action": "QUALIFY",
         "source_locators": ["schemas/TraceLink.schema.json", "schemas/PI-PKG.schema.json",
                             "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/pipeline.py"],
         "external_method": False, "control_authority": "PIPD core (this repo)"},
        {"capability": "release provenance identity (F001/G006)",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "ACTIVE_REQUIRED",
         "current_profile_selected": True, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": True, "action": "QUALIFY",
         "source_locators": ["dist/mount/**", "docs/RELEASE_TUPLE.json",
                             "docs/ERRATUM_2026-10-12_preview3_release_provenance.md"],
         "external_method": False, "control_authority": "PIPD release owner"},
        {"capability": "profiles.py boundary behaviour (O009)",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "ACTIVE_REQUIRED",
         "current_profile_selected": True, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": False,
         "runtime_required_now": True, "action": "QUALIFY",
         "source_locators": ["src/pipd_ls_sp/profiles.py"], "external_method": False,
         "control_authority": "PIPD core"},
        {"capability": "portable first-run UX (O007)",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "ACTIVE_REQUIRED",
         "current_profile_selected": True, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": True, "action": "QUALIFY",
         "source_locators": ["README.md", "examples/first-run/run.sh", "examples/first-run/run.ps1"],
         "external_method": False, "control_authority": "PIPD DX/docs owner"},
        {"capability": "installed wheel distribution",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "ACTIVE_REQUIRED",
         "current_profile_selected": True, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": True, "action": "QUALIFY",
         "source_locators": ["dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"], "external_method": False,
         "control_authority": "PIPD release package"},
        {"capability": "Web GPT-6 chat host", "source_disposition": "ACTIVE_REQUIRED",
         "current_execution_disposition": "DEFERRED_SOURCE_BACKED",
         "current_profile_selected": False, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": False, "action": "DEFER",
         "source_locators": ["dist/mount/**", "README.md"], "external_method": False,
         "control_authority": "host owner"},
        {"capability": "Hermes Agent skill host", "source_disposition": "ACTIVE_REQUIRED",
         "current_execution_disposition": "DEFERRED_SOURCE_BACKED",
         "current_profile_selected": False, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": False, "action": "DEFER",
         "source_locators": [".hermes/skills/**", "skills/pipd-*/SKILL.md"],
         "external_method": False, "control_authority": "host owner"},
        {"capability": "Codex agent host", "source_disposition": "ACTIVE_REQUIRED",
         "current_execution_disposition": "DEFERRED_SOURCE_BACKED",
         "current_profile_selected": False, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": True,
         "runtime_required_now": False, "action": "DEFER",
         "source_locators": [".agents/skills/**"], "external_method": False,
         "control_authority": "host owner"},
        {"capability": "HG-KSEOS canonical acceptance transition",
         "source_disposition": "ACTIVE_REQUIRED", "current_execution_disposition": "PROHIBITED",
         "current_profile_selected": False, "canonical_flow_referenced": True,
         "automatic_route_target": False, "user_experience_required": False,
         "runtime_required_now": False, "action": "PROHIBIT",
         "source_locators": [str(HGK / "AGENTS.md")], "external_method": False,
         "control_authority": "HG-KSEOS owner"},
        {"capability": "S5-S8 / GENIE / JIT runtimes", "source_disposition": "ACTIVE_REQUIRED",
         "current_execution_disposition": "PROHIBITED", "current_profile_selected": False,
         "canonical_flow_referenced": True, "automatic_route_target": False,
         "user_experience_required": False, "runtime_required_now": False, "action": "PROHIBIT",
         "source_locators": [".hgk/artifacts/s4/S5_S8_BACKLOG.json"], "external_method": False,
         "control_authority": "upstream stage gate"},
    ],
    "runtime_readiness": [
        {"capability": "TraceLink endpoint typing + bundle graph closure (F002)",
         "required_now": True,
         "lifecycle": lifecycle(identify="PASS", pin="PASS", install_materialize="PASS",
                                configure="PASS", discover="PASS", bind="PASS", route="PASS",
                                effective_load="PASS", doctor_health="PASS", positive_pilot="PASS",
                                negative_security="PASS", fallback="PASS", rollback_uninstall="PASS",
                                independent_qualification="OPEN", certify="OPEN", enable="OPEN"),
         "current_verdict": "NOT_READY",
         "work_required": ["close the independent_qualification stage by an external verifier"],
         "acceptance_ids": ["A-02", "A-07"]},
        {"capability": "release provenance identity (F001/G006)", "required_now": True,
         "lifecycle": lifecycle(identify="PASS", pin="PASS", install_materialize="PASS",
                                configure="NOT_APPLICABLE_SOURCE_BACKED", discover="PASS",
                                bind="PASS", route="NOT_APPLICABLE_SOURCE_BACKED",
                                effective_load="PASS", doctor_health="NOT_APPLICABLE_SOURCE_BACKED",
                                positive_pilot="PASS", negative_security="PASS", fallback="PASS",
                                rollback_uninstall="PASS", independent_qualification="OPEN",
                                certify="OPEN", enable="OPEN"),
         "current_verdict": "NOT_READY",
         "work_required": ["external verifier re-derives the 8/8 identity from the pushed branch",
                           "release owner decides public erratum vs new preview"],
         "acceptance_ids": ["A-01", "A-03"]},
        {"capability": "installed wheel distribution", "required_now": True,
         "lifecycle": lifecycle(identify="PASS", pin="PASS", install_materialize="PASS",
                                configure="PASS", discover="PASS", bind="PASS", route="PASS",
                                effective_load="PASS", doctor_health="PASS", positive_pilot="PASS",
                                negative_security="PASS", fallback="PASS", rollback_uninstall="PASS",
                                independent_qualification="OPEN", certify="OPEN", enable="OPEN"),
         "current_verdict": "NOT_READY",
         "work_required": ["external verifier reruns the same probe from the downloaded asset bytes"],
         "acceptance_ids": ["A-07"]},
        {"capability": "portable first-run UX (O007)", "required_now": True,
         "lifecycle": lifecycle(identify="PASS", install_materialize="PASS", discover="PASS",
                                positive_pilot="PASS", negative_security="PASS", fallback="PASS",
                                rollback_uninstall="PASS", independent_qualification="OPEN",
                                certify="OPEN", enable="OPEN"),
         "current_verdict": "NOT_READY",
         "work_required": ["fresh-user Ubuntu/macOS run is not available on this host (Windows only)"],
         "acceptance_ids": ["A-04"]},
        {"capability": "profiles.py boundary behaviour (O009)", "required_now": True,
         "lifecycle": lifecycle(identify="PASS", positive_pilot="PASS", negative_security="PASS",
                                independent_qualification="OPEN", certify="OPEN", enable="OPEN"),
         "current_verdict": "NOT_READY", "work_required": ["independent requalification"],
         "acceptance_ids": ["A-05"]},
    ],
    "journeys": [
        {"journey_id": "J-01", "required": True,
         "user_goal": "A brand-new user on Linux/Git-Bash runs the whole compiler chain from a fresh checkout.",
         "expected_visible_result": ("one command prints FIRST_RUN_OK and a validate verdict PASS with "
                                     "closure FULL"),
         "expected_automatic_behavior": ["path derivation from the script's own location",
                                         "precondition check before any work",
                                         "scratch workspace outside the checkout"],
         "expected_manual_behavior": ["choose the interpreter if python3 is not on PATH"],
         "allowed_hitl": [], "required_capabilities": ["portable first-run UX (O007)",
                                                       "installed wheel distribution"],
         "negative_behavior": "an unusable interpreter halts with PRECONDITION_FAIL and exit 3",
         "failure_recovery": "re-run with PYTHON=<interpreter>",
         "source_expectation_ids": ["O007"], "source_locators": ["examples/first-run/run.sh"]},
        {"journey_id": "J-02", "required": True,
         "user_goal": "A brand-new user on Windows PowerShell runs the same chain.",
         "expected_visible_result": "FIRST_RUN_OK and validate PASS",
         "expected_automatic_behavior": ["$LASTEXITCODE checked after every native call"],
         "expected_manual_behavior": ["bypass the execution policy for the one script"],
         "allowed_hitl": [], "required_capabilities": ["portable first-run UX (O007)"],
         "negative_behavior": "a failing step aborts before the next",
         "failure_recovery": "inspect the printed step log",
         "source_expectation_ids": ["O007"], "source_locators": ["examples/first-run/run.ps1"]},
        {"journey_id": "J-03", "required": True,
         "user_goal": ("An external verifier re-derives the release identity of the mount pack from "
                       "the frozen tuple and the git tag, without trusting the pack's own text."),
         "expected_visible_result": ("8/8 documents name release_tag_target; a stale value fails the "
                                     "check"),
         "expected_automatic_behavior": ["tuple-driven comparison, not a hard-coded literal"],
         "expected_manual_behavior": ["run git rev-parse TAG^{commit}"],
         "allowed_hitl": [], "required_capabilities": ["release provenance identity (F001/G006)"],
         "negative_behavior": "a document carrying the stale commit is refused",
         "failure_recovery": "regenerate the pack from the frozen tuple",
         "source_expectation_ids": ["F001", "F003"],
         "source_locators": ["tests/test_s4ext_release_provenance.py", "docs/RELEASE_TUPLE.json"]},
        {"journey_id": "J-04", "required": True,
         "user_goal": ("A verifier replays the F002 counterexample and observes the repaired "
                       "distribution refusing it."),
         "expected_visible_result": "validate --bundle exits non-zero with CLOSURE findings",
         "expected_automatic_behavior": ["closure runs inside validate_bundle"],
         "expected_manual_behavior": ["feed the tampered bundle"],
         "allowed_hitl": [],
         "required_capabilities": ["TraceLink endpoint typing + bundle graph closure (F002)"],
         "negative_behavior": "mis-typed/orphan/bad-hash endpoints never reach PASS",
         "failure_recovery": "read the findings list",
         "source_expectation_ids": ["F002"],
         "source_locators": ["tests/test_s4ext_trace_closure.py"]},
    ],
    "acceptance": [
        {"acceptance_id": "A-01", "subject_id": "F001", "subject_type": "DELIVERABLE",
         "source_locators": ["dist/mount/**", "docs/RELEASE_TUPLE.json"],
         "runtime_required": False, "required_depth": "L2_UNIT_BEHAVIOR",
         "positive_fixture": "8/8 documents naming release_tag_target",
         "negative_fixture": "a document carrying the stale 8faa64e5 identity",
         "recovery_fixture": "regenerate via tools/build_mount_pack.py",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-02", "subject_id": "F002", "subject_type": "CAPABILITY",
         "source_locators": ["schemas/TraceLink.schema.json", "src/pipd_ls_sp/validate.py"],
         "runtime_required": True, "required_depth": "L3_INTEGRATION_RUNTIME",
         "positive_fixture": "the legal PI/PD/ECP/TQAEP bundle (closure FULL)",
         "negative_fixture": "bad type / orphan / wrong 64-hex hash / duplicated link / extra key",
         "recovery_fixture": "the failing findings list names the edge",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-03", "subject_id": "F003", "subject_type": "DELIVERABLE",
         "source_locators": ["tests/test_s4ext_release_provenance.py"],
         "runtime_required": False, "required_depth": "L2_UNIT_BEHAVIOR",
         "positive_fixture": "current frozen tuple pin",
         "negative_fixture": "wrong-old-tag negative",
         "recovery_fixture": "n/a (static check)",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-04", "subject_id": "O007", "subject_type": "JOURNEY",
         "source_locators": ["examples/first-run/run.sh", "examples/first-run/run.ps1"],
         "runtime_required": True, "required_depth": "L3_INTEGRATION_RUNTIME",
         "positive_fixture": "run.sh / run.ps1 from a foreign cwd",
         "negative_fixture": "unusable interpreter -> exit 3",
         "recovery_fixture": "PYTHON=<interpreter>",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-05", "subject_id": "O009", "subject_type": "CAPABILITY",
         "source_locators": ["src/pipd_ls_sp/profiles.py"],
         "runtime_required": False, "required_depth": "L2_UNIT_BEHAVIOR",
         "positive_fixture": "3/4 and 6/7 axis thresholds, provider-off + complexity",
         "negative_fixture": "non-string requested, unknown axis, duplicate axis, downgrade attempt",
         "recovery_fixture": "typed ProfileVeto",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-06", "subject_id": "TT-S4EXT-007", "subject_type": "DELIVERABLE",
         "source_locators": ["docs/S4_SPEC_DEL_ADJUDICATION.json"],
         "runtime_required": False, "required_depth": "L1_SCHEMA_CONTRACT",
         "positive_fixture": "57 adjudicated rows",
         "negative_fixture": "an un-adjudicated gap row / an upgraded status",
         "recovery_fixture": "regenerate from the crosswalk",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
        {"acceptance_id": "A-07", "subject_id": "G004/G006", "subject_type": "DELIVERABLE",
         "source_locators": ["dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl"],
         "runtime_required": True, "required_depth": "L3_INTEGRATION_RUNTIME",
         "positive_fixture": "pipd doctor PASS, 13 commands, 19 families, full chain",
         "negative_fixture": "missing source refused with exit 2; tampered trace refused",
         "recovery_fixture": "re-create the venv",
         "raw_evidence_required": True, "independent_checker_required": True,
         "terminal_states": ["PASS", "PARTIAL", "FAIL"]},
    ],
    "evidence": [
        {"gate_id": "G-01", "predicate": "8/8 pack documents name the frozen release_tag_target",
         "expected": "no stale identity outside a disclosure line",
         "command_or_probe": "python -m unittest tests.test_s4ext_release_provenance",
         "raw_receipt_required": True, "producer": "PIPD repair owner (maker)",
         "independent_checker": "external verifier",
         "candidate_binding": {"head": "CANDIDATE", "package_sha256": "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec",
                               "source_hashes": {"dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip":
                                                 "73c6c7e255846e9012a4f5f0e849af93343b363fb158f2474b4d18143d1dcfde"}},
         "tracked_subject": "docs/RELEASE_TUPLE.json", "rerun_rule": "affected-only",
         "invalidation": ["any change to the pack docs, the tuple or the generator"],
         "terminal_verdict": "PARTIAL", "runtime_pass_allowed": False, "claim_level": "PACKAGE"},
        {"gate_id": "G-02", "predicate": "a tampered trace bundle must not reach PASS",
         "expected": "exit non-zero with CLOSURE findings; legal bundle still PASS",
         "command_or_probe": "bash .hgk/rounds/S4EXT-R1-*/raw/f002_runtime_probe.sh",
         "raw_receipt_required": True, "producer": "PIPD compiler owner (maker)",
         "independent_checker": "external verifier",
         "candidate_binding": {"head": "CANDIDATE", "package_sha256": "UNAVAILABLE",
                               "source_hashes": {"src/pipd_ls_sp/validate.py": "CANDIDATE"}},
         "tracked_subject": "src/pipd_ls_sp/validate.py", "rerun_rule": "affected-only",
         "invalidation": ["any change to the schemas, validate.py or pipeline.py"],
         "terminal_verdict": "PARTIAL", "runtime_pass_allowed": False, "claim_level": "PACKAGE"},
        {"gate_id": "G-03", "predicate": "full deterministic suite on the frozen candidate",
         "expected": "0 failures, 0 errors",
         "command_or_probe": "python -m unittest discover -s tests -t .",
         "raw_receipt_required": True, "producer": "maker",
         "independent_checker": "external verifier",
         "candidate_binding": {"head": "CANDIDATE", "package_sha256": "UNAVAILABLE",
                               "source_hashes": {"tests": "CANDIDATE"}},
         "tracked_subject": "tests/", "rerun_rule": "full",
         "invalidation": ["any code, schema or test change"],
         "terminal_verdict": "PARTIAL", "runtime_pass_allowed": False, "claim_level": "PACKAGE"},
        {"gate_id": "G-04", "predicate": "installed wheel behaves as a distribution",
         "expected": "doctor PASS in INSTALLED mode, 19 families, chain + refusal",
         "command_or_probe": "bash .hgk/rounds/S4EXT-R1-*/raw/installed_wheel_qualification.sh",
         "raw_receipt_required": True, "producer": "maker",
         "independent_checker": "external verifier",
         "candidate_binding": {"head": "PUBLISHED_SUBJECT",
                               "package_sha256": "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec",
                               "source_hashes": {"dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl":
                                                 "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec"}},
         "tracked_subject": "dist/", "rerun_rule": "full",
         "invalidation": ["a new wheel build"],
         "terminal_verdict": "PARTIAL", "runtime_pass_allowed": False, "claim_level": "PACKAGE"},
        {"gate_id": "G-05", "predicate": "57-row crosswalk adjudicated without status upgrades",
         "expected": "9 gaps + 4 design-only answered; crosswalk read-only",
         "command_or_probe": "python -m unittest tests.test_s4ext_spec_del_adjudication",
         "raw_receipt_required": True, "producer": "maker", "independent_checker": "external verifier",
         "candidate_binding": {"head": "CANDIDATE", "package_sha256": "UNAVAILABLE",
                               "source_hashes": {"docs/SPEC_DEL_CROSSWALK.json": "READ_ONLY"}},
         "tracked_subject": "docs/S4_SPEC_DEL_ADJUDICATION.json", "rerun_rule": "affected-only",
         "invalidation": ["any crosswalk or adjudication change"],
         "terminal_verdict": "PARTIAL", "runtime_pass_allowed": False, "claim_level": "PACKAGE"},
        {"gate_id": "G-06", "predicate": "four-host consumer qualification",
         "expected": "each host: discover/load/positive/negative or an honest NOT_RUN",
         "command_or_probe": "see 07_HOSTS in the return pack",
         "raw_receipt_required": True, "producer": "host owner",
         "independent_checker": "external verifier",
         "candidate_binding": {"head": "CANDIDATE", "package_sha256": "e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec",
                               "source_hashes": {"dist/mount/**": "CANDIDATE"}},
         "tracked_subject": "dist/mount/", "rerun_rule": "affected-only",
         "invalidation": ["host capability change"],
         "terminal_verdict": "BLOCKED_EXTERNAL", "runtime_pass_allowed": False,
         "claim_level": "EXTERNAL_ACCEPTANCE"},
    ],
    "termination": {
        "terminal_states": ["PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"],
        "non_terminal_pause": ["PUSH_HOLD", "BLOCKED_EXTERNAL", "BLOCKED_HITL"],
        "checkpoint_required": True,
        "checkpoint_fields": ["candidate_head", "branch", "open_tt", "raw_log_pointers",
                              "rollback_pointer"],
        "retry_budget": 3,
        "rollback_pointer_required": True,
    },
    "render_policy": {
        "control_corpus_restatement": False,
        "embedded_control_bodies": False,
        "max_prompt_chars": 40000,
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
