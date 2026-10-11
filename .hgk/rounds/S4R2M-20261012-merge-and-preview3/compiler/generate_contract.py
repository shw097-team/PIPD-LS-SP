#!/usr/bin/env python3
"""S4R2M round: generate the CAPC C0-C9 contract for
`PIPD-S4R2-MERGE-AND-PREVIEW3-CONDITIONAL-20261011`.

Shape cloned from the predecessor round contracts (R5P.CONTRACT.json / S4R2.CONTRACT.json) and
from the newest sealed bundle contract (scripts/evo005r7_contract.json); every row shape below is
the schema-validated one. Prose is round-specific so the duplication gate stays well under 0.25.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROUND_DIR = Path(__file__).resolve().parent
ATT = Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments")
P0 = ATT / "PIPD-LS-SP_HERMES_S4R2_PREVIEW3_CONDITIONAL_MERGE_REPAIR_PROMPT_2026-10-11.md"
P1 = ATT / "PIPD_LS_SP_S4_MVP_PostRelease_S4R2_Independent_Acceptance_and_Preview3_Gate_2026-10-11.md"


def sha(path: Path) -> str:
    if not path.exists():
        return "UNAVAILABLE"
    return hashlib.sha256(path.read_bytes()).hexdigest()


FAMILIES = [
    ("F0_S4R2M_MERGE_PROMPT", "R0", P0, "NORMATIVE", True, True),
    ("F1_S4R2M_ACCEPTANCE_REPORT", "R1", P1, "NORMATIVE", True, True),
    ("F2_PIPD_UPSTREAM_BLUEPRINT", "R2", Path(r"C:/Projects/Agent_Workspace/知識庫"), "NORMATIVE", True, False),
    ("F3_HGK_CONTROL_PLANE", "R3", Path(r"C:/Projects/Agent_Workspace/HG-KSEOS"), "NORMATIVE", True, False),
    ("F4_FABRIC_GOVERNANCE_CONTRACT", "R4", Path(r"C:/Projects/Agent_Workspace/Fabric"), "NORMATIVE", True, False),
    ("F5_PIPD_LOCAL_REPO_TRUTH", "S1", Path(r"C:/Projects/Agent_Workspace/PIPD"), "STATE_EVIDENCE", False, False),
    ("F6_PUBLIC_REMOTE_STATE", "S2", None, "STATE_EVIDENCE", False, False),
    ("F7_PRIOR_S4R2_VERIFY_RECEIPTS", "S3", Path(r"C:/Projects/Agent_Workspace/PIPD-postrelease-wt"), "STATE_EVIDENCE", False, False),
]

LOC = {
    "F0_S4R2M_MERGE_PROMPT": str(P0),
    "F1_S4R2M_ACCEPTANCE_REPORT": str(P1),
    "F2_PIPD_UPSTREAM_BLUEPRINT": "C:/Projects/Agent_Workspace/知識庫 (PKG-00..10 / DOC-00..09 / 藍圖 / canonical standard)",
    "F3_HGK_CONTROL_PLANE": "C:/Projects/Agent_Workspace/HG-KSEOS (AGENTS.md, config/project.json, var/shared-spine/hg-kseos.db)",
    "F4_FABRIC_GOVERNANCE_CONTRACT": "C:/Projects/Agent_Workspace/Fabric (/control/CHANGE_CLASS_ROUTER.yaml, SOD_POLICY.yaml, RISK_POLICY.yaml, /assurance/EVIDENCE_CONTRACT.yaml)",
    "F5_PIPD_LOCAL_REPO_TRUTH": "git worktree PIPD/worktrees/s4r2m-merge-wt + PIPD-postrelease-wt (branch s4-r2-affected-only-20261011)",
    "F6_PUBLIC_REMOTE_STATE": "https://github.com/shw097-team/PIPD-LS-SP refs (anonymous ls-remote)",
    "F7_PRIOR_S4R2_VERIFY_RECEIPTS": "PIPD-postrelease-wt/.hgk/rounds/S4R2-20261011-affected-only/verify/VERIFY_RECEIPT_gpt61sol.json",
}

REVIEWED = []
for fid, rank, path, role, critical, is_file in FAMILIES:
    digest = sha(path) if (is_file and path is not None) else (
        "REMOTE_UNPINNED" if fid == "F6_PUBLIC_REMOTE_STATE" else "UNAVAILABLE")
    REVIEWED.append({
        "source_family": fid, "source_id": fid, "locator": LOC[fid],
        "sha256": digest, "role": role, "critical": critical,
    })

SOURCES = []
for fid, rank, path, role, critical, is_file in FAMILIES:
    digest = sha(path) if (is_file and path is not None) else (
        "REMOTE_UNPINNED" if fid == "F6_PUBLIC_REMOTE_STATE" else "UNAVAILABLE")
    SOURCES.append({
        "id": fid, "rank": rank, "path": str(path) if path is not None else LOC[fid],
        "sha256": digest, "locator": LOC[fid], "role": role, "governs": role == "NORMATIVE",
    })

NORMATIVE_CLAIMS = [
    {"claim_id": "NC-01", "text": "The round is a NARROW_REPAIR re-target on an already-repaired S4-R2 product: only the README CLI/Skills split, the --root wording, an isolated focused regression and a conditional integration/release gate are in scope.",
     "source_ids": ["F0_S4R2M_MERGE_PROMPT", "F1_S4R2M_ACCEPTANCE_REPORT"], "locators": [str(P0) + "#1 Mission", str(P1) + "#8 Findings"]},
    {"claim_id": "NC-02", "text": "main must not be written, tagged or released before a native PROMPT_COMPILE_PASS and a real focused regression receipt exist; the withheld end state is MERGE_READY_HITL_PENDING.",
     "source_ids": ["F0_S4R2M_MERGE_PROMPT"], "locators": [str(P0) + "#2 Authority", str(P0) + "#6 Gate P0"]},
    {"claim_id": "NC-03", "text": "v0.1.0-preview.2 stays public and immutable; a preview.3 distribution must carry a PEP 440 version strictly greater than 0.1.0.",
     "source_ids": ["F1_S4R2M_ACCEPTANCE_REPORT"], "locators": [str(P1) + "#5.2", str(P1) + "#11"]},
    {"claim_id": "NC-04", "text": "HG-KSEOS is the sole normative control plane; Fabric is a read-only policy contract surface consumed by HGK, never a second writer or credential broker.",
     "source_ids": ["F0_S4R2M_MERGE_PROMPT", "F4_FABRIC_GOVERNANCE_CONTRACT"], "locators": [str(P0) + "#3 Authority", "Fabric/control/CHANGE_CLASS_ROUTER.yaml"]},
    {"claim_id": "NC-05", "text": "The four early ProfileBinding mutants are already closed on the frozen subject; only the version-string grammar stays a deferred P2 observation and must not be re-opened as five live defects.",
     "source_ids": ["F1_S4R2M_ACCEPTANCE_REPORT", "F7_PRIOR_S4R2_VERIFY_RECEIPTS"], "locators": [str(P1) + "#6", "S4R2-20261011-affected-only/verify/VERIFY_RECEIPT_gpt61sol.json"]},
    {"claim_id": "NC-06", "text": "23. The maker suite figure measured in a writable checkout and the independent checker PARTIAL verdict are different claim fates and must never be merged into one PASS.",
     "source_ids": ["F0_S4R2M_MERGE_PROMPT", "F1_S4R2M_ACCEPTANCE_REPORT"], "locators": [str(P0) + "#8 Evidence", str(P1) + "#7"]},
]

CAPS_ACTIVE = [
    ("CAP-S4R2M-README-PATH-SPLIT", "CLI vs Skills split on the front page", False, "INSTALL"),
    ("CAP-S4R2M-CLI-ROOT-TRUTH", "lay \(--root\) positioning truth per the real argparse surface", False, "INSTALL"),
    ("CAP-S4R2M-BOUNDED-WRITER-LANE", "sealed Codex bounded writer over the admitted write-set", True, "QUALIFY"),
    ("CAP-S4R2M-ISOLATED-REGRESSION", "isolated writable copy focused regression", True, "QUALIFY"),
    ("CAP-S4R2M-INDEPENDENT-OFFICER", "independent acceptance officer lane", True, "QUALIFY"),
    ("CAP-S4R2M-MAIN-FF-INTEGRATION", "guarded fast-forward integration into main", False, "DESIGN"),
    ("CAP-S4R2M-PROMPT-COMPILER-CAPC", "native C0-C9 prompt compiler gate", True, "QUALIFY"),
    ("CAP-S4R2M-HGK-ADMISSION", "typed lifecycle admission on the live project", True, "QUALIFY"),
    ("CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC", "board + swarm graph + named-method route + change proposal", True, "QUALIFY"),
]
CAPS_DEFERRED = [
    "CAP-S4R2M-PREVIEW3-RELEASE",
    "CAP-S4R2M-WEB-NATIVE-SKILL-LOAD",
    "CAP-S4R2M-VERSION-GRAMMAR",
    "CAP-S4R2M-PROFILE-12AXIS-RISK",
]
CAPS_PROHIBITED = ["CAP-S4R2M-S5-S8-RUNTIME"]

EXEC = []
for name, desc, need_rt, action in CAPS_ACTIVE:
    EXEC.append({
        "capability": name, "source_disposition": "ACTIVE_IN_SOURCE",
        "current_execution_disposition": "ACTIVE_REQUIRED",
        "current_profile_selected": True, "canonical_flow_referenced": True,
        "automatic_route_target": True, "user_experience_required": True,
        "runtime_required_now": need_rt, "action": action,
        "source_locators": [str(P0) + "#4 Active/Deferred/Forbidden", str(P0) + "#6 Gates"],
        "external_method": False, "control_authority": False,
    })
for name in CAPS_DEFERRED:
    EXEC.append({
        "capability": name, "source_disposition": "SOURCE_BACKED_NOT_SELECTED",
        "current_execution_disposition": "DEFERRED_SOURCE_BACKED",
        "current_profile_selected": False, "canonical_flow_referenced": False,
        "automatic_route_target": False, "user_experience_required": False,
        "runtime_required_now": False, "action": "DEFER",
        "source_locators": [str(P0) + "#4 Active/Deferred/Forbidden", str(P1) + "#8 Findings"],
        "external_method": False, "control_authority": False,
    })
for name in CAPS_PROHIBITED:
    EXEC.append({
        "capability": name, "source_disposition": "OUT_OF_SCOPE_SOURCE_BACKED",
        "current_execution_disposition": "PROHIBITED",
        "current_profile_selected": False, "canonical_flow_referenced": False,
        "automatic_route_target": False, "user_experience_required": False,
        "runtime_required_now": False, "action": "PROHIBIT",
        "source_locators": [str(P1) + "#8 S4R2-POST-F08"],
        "external_method": False, "control_authority": False,
    })

OPEN16 = {k: "OPEN" for k in (
    "identify", "pin", "install_materialize", "configure", "discover", "bind", "route",
    "effective_load", "doctor_health", "positive_pilot", "negative_security", "fallback",
    "rollback_uninstall", "independent_qualification", "certify", "enable")}

RT_WORK = {
    "CAP-S4R2M-BOUNDED-WRITER-LANE": [
        "44. bind one sealed Codex writer to the admitted write-set of WO-S4R2M-DOC-CAL-01 and prove the escape is discriminated, not just the in-scope write admitted",
        "45. keep credentials and git out of the writer lane"],
    "CAP-S4R2M-ISOLATED-REGRESSION": [
        "46. build a byte-equivalent writable clone from the frozen candidate head so the read-only subject is never mutated",
        "47. run the six named affected test modules plus the two CE/wheel positives and keep the 19/8/13 exact-set unchanged"],
    "CAP-S4R2M-INDEPENDENT-OFFICER": [
        "48. dispatch the checker lane on a different model family than the writer and re-derive every decisive figure",
        "49. reject a maker-authored verdict presented as independent acceptance"],
    "CAP-S4R2M-PROMPT-COMPILER-CAPC": [
        "50. satisfy lint, activation and acceptance with zero errors and emit the compiler receipt",
        "51. keep the rendered thin prompt inside render_policy.max_prompt_chars"],
    "CAP-S4R2M-HGK-ADMISSION": [
        "52. admit one requirement per WorkOrder through the typed API and read the binding back",
        "53. bind the writable_root to the candidate worktree actually used by the writer"],
    "CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC": [
        "54. create the round board and its swarm root/worker/verifier/synthesizer graph and persist the returned ids",
        "55. record the named-method route readback and one change proposal, without promoting any method to control authority"],
}
READINESS = []
for name, desc, need_rt, action in CAPS_ACTIVE:
    if not need_rt:
        continue
    READINESS.append({
        "capability": name, "required_now": True,
        "lifecycle": dict(OPEN16), "current_verdict": "NOT_READY",
        "work_required": RT_WORK[name],
        "acceptance_ids": ["ACC-" + name],
    })

JOURNEYS = [
    ("J1_CLI_PACKAGED_INSTALL",
     "A first-time user picks the CLI path and installs the pinned wheel.",
     "The front page states that the wheel carries the Python CLI and 19 schemas and that it does NOT inject the 8 native web skills.",
     ["the installed wheel is verified against its published digest before any run",
      "doctor reports the schema source it actually resolved"],
     ["the user only supplies a venv and a wheel path"],
     ["CAP-S4R2M-README-PATH-SPLIT", "CAP-S4R2M-BOUNDED-WRITER-LANE"],
     ["a wheel whose bytes differ from the published digest must refuse, never print OK"],
     ["stop at the checksum gate and re-download from the immutable tag"],
     ["REQ-S4R2M-DOC-001"]),
    ("J2_SKILLS_MOUNT_PACK",
     "A web user picks the Skills path and mounts the versioned document pack.",
     "The mount guide distinguishes manual document/Knowledge mode from a native skill upload, and native loading stays NOT_RUN unless a host receipt exists.",
     ["the pack manifest verifies the bytes the user actually received"],
     ["the user attaches the markdown and the starter prompt by hand"],
     ["CAP-S4R2M-README-PATH-SPLIT"],
     ["a manual attachment must never be reported as a native skill effective-load"],
     ["label the path NOT_RUN and keep the manual document route usable"],
     ["REQ-S4R2M-DOC-001"]),
    ("J3_FIRST_RUN_REPLAY",
     "An ordinary reader runs the copy-paste compiler chain twice.",
     "Both runs exit 0 and the six produced artefact digests are identical between passes.",
     ["the checked-in fixture paths resolve without any placeholder token",
      "a missing source locator is refused with a typed non-zero exit"],
     ["the reader substitutes only their own interpreter path"],
     ["CAP-S4R2M-ISOLATED-REGRESSION", "CAP-S4R2M-BOUNDED-WRITER-LANE"],
     ["a missing or tampered source must not be silently compiled into a record"],
     ["re-run from a clean scratch root and re-check the digests"],
     ["REQ-S4R2M-VERIFY-002"]),
    ("J4_TYPED_PROFILE_BINDING",
     "A user binds a profile and the duplicate/typed axis mutants are refused.",
     "A legal LITE/STANDARD/ASSURED binding is accepted and every malformed axis form is refused with a typed schema exit.",
     ["the compiler-issued records stay accepted while the mutants stay refused"],
     ["the user supplies only the profile axis set"],
     ["CAP-S4R2M-ISOLATED-REGRESSION", "CAP-S4R2M-INDEPENDENT-OFFICER"],
     ["turning an unassessed risk into an automatic high-risk approval must never happen"],
     ["keep the NEG set and the POS set in the same receipt so neither alone decides"],
     ["REQ-S4R2M-VERIFY-002"]),
    ("J5_CLI_ROOT_FLAG_TRUTH",
     "A reader follows the documented --root rules for init, project and export.",
     "The pre-subcommand form works for the compile chain and the subcommand-local form works for project and export, exactly as the documented text says.",
     ["the documented positive forms all exit 0",
      "an unsupported local form exits non-zero as a typed usage error"],
     ["the user copies the documented lines literally"],
     ["CAP-S4R2M-CLI-ROOT-TRUTH", "CAP-S4R2M-README-PATH-SPLIT"],
     ["a claim that every command accepts only the global position must be refuted by the real help output"],
     ["fix the prose, never the claim about the CLI"],
     ["REQ-S4R2M-DOC-001"]),
    ("J6_MERGE_VS_PUBLIC_WHEEL",
     "A user wants the new repairs from the public tag.",
     "The README and the release state say plainly that main carrying the repairs and the public preview.2 wheel are different artefacts.",
     ["the integration receipt names the exact merged commit and the unchanged preview.2 tag"],
     ["the user is told which artefact to download for which capability"],
     ["CAP-S4R2M-MAIN-FF-INTEGRATION"],
     ["a merged main must never be described as if the published wheel already contained the repairs"],
     ["state the gap and point at the next preview gate"],
     ["REQ-S4R2M-MERGE-003"]),
]

DELIVERABLES = [
    "CAPC_PROMPT_COMPILE_RECEIPT", "HGK_ADMISSION_READBACK", "README_F01_F02_PATCH",
    "ISOLATED_FOCUSED_REGRESSION_RECEIPT", "INDEPENDENT_OFFICER_VERDICT",
    "MERGE_DECISION_S4R2M", "KANBAN_SWARM_GSTACK_OPENSPEC_RECEIPT", "PREVIEW3_RELEASE_GATE_DECISION",
    "S4R2M_EVIDENCE_PACK",
]
REQUIREMENTS = ["REQ-S4R2M-DOC-001", "REQ-S4R2M-VERIFY-002", "REQ-S4R2M-MERGE-003", "REQ-S4R2M-PREVIEW3-004"]

ACCEPT = []
for name, desc, need_rt, action in CAPS_ACTIVE:
    ACCEPT.append({
        "acceptance_id": "ACC-" + name, "subject_id": name, "subject_type": "CAPABILITY",
        "source_locators": [str(P0) + "#6 Gates", str(P0) + "#8 Evidence"],
        "runtime_required": need_rt, "required_depth": "L3_INTEGRATION_RUNTIME" if need_rt else "L2_UNIT_BEHAVIOR",
        "positive_fixture": "POS/" + name + ": the documented capability behaves as the round contract states",
        "negative_fixture": "NEG/" + name + ": the same capability is exercised without its precondition and must refuse with a typed non-zero exit",
        "recovery_fixture": "REC/" + name + ": the smallest affected repair re-run, no widening of the accepted scope",
        "raw_evidence_required": need_rt or True, "independent_checker_required": True,
        "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL"],
    })
for name in CAPS_DEFERRED + CAPS_PROHIBITED:
    ACCEPT.append({
        "acceptance_id": "ACC-" + name, "subject_id": name, "subject_type": "CAPABILITY",
        "source_locators": [str(P0) + "#4 Active/Deferred/Forbidden", str(P1) + "#8 Findings"],
        "runtime_required": False, "required_depth": "L0_STATIC_EXISTENCE",
        "positive_fixture": "DEFER/" + name + ": recorded as not selected for this round with its owner and trigger named",
        "negative_fixture": "NEG/" + name + ": an attempt to activate the deferred capability in this round is refused, not silently accepted",
        "recovery_fixture": "",
        "raw_evidence_required": False, "independent_checker_required": True,
        "terminal_states": ["BLOCKED_HITL", "BLOCKED_EXTERNAL", "INDEPENDENT_CASE_FAIL"],
    })
for jid, goal, vis, autos, manuals, caps, negs, recs, rexps in JOURNEYS:
    ACCEPT.append({
        "acceptance_id": "ACC-" + jid, "subject_id": jid, "subject_type": "JOURNEY",
        "source_locators": [str(P0) + "#3 Intent", str(P1) + "#4"],
        "runtime_required": True, "required_depth": "L3_INTEGRATION_RUNTIME",
        "positive_fixture": "POS/" + jid + " positive traversal of " + goal,
        "negative_fixture": "NEG/" + jid + " negative traversal of " + goal,
        "recovery_fixture": "REC/" + jid + " recovery traversal of " + goal,
        "raw_evidence_required": True, "independent_checker_required": True,
        "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL"],
    })
for rid in REQUIREMENTS:
    ACCEPT.append({
        "acceptance_id": "ACC-" + rid, "subject_id": rid, "subject_type": "REQUIREMENT",
        "source_locators": [str(P0) + "#1 Mission"],
        "runtime_required": True, "required_depth": "L3_INTEGRATION_RUNTIME",
        "positive_fixture": "POS/" + rid + ": its WorkOrder materializes and its oracle passes on the frozen candidate",
        "negative_fixture": "NEG/" + rid + ": the obligation left as a paraphrase without a receipt is refused",
        "recovery_fixture": "REC/" + rid + ": smallest affected repair with its owner class",
        "raw_evidence_required": True, "independent_checker_required": True,
        "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL"],
    })
for did in DELIVERABLES:
    ACCEPT.append({
        "acceptance_id": "ACC-" + did, "subject_id": did, "subject_type": "DELIVERABLE",
        "source_locators": [str(P0) + "#9 Termination", str(P0) + "#8 Evidence"],
        "runtime_required": False, "required_depth": "L1_SCHEMA_CONTRACT",
        "positive_fixture": "POS/" + did + ": the artefact exists at the round evidence root and verifies",
        "negative_fixture": "NEG/" + did + ": a claim without the artefact behind it is refused",
        "recovery_fixture": "",
        "raw_evidence_required": True, "independent_checker_required": True,
        "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL"],
    })

JOURNEY_ROWS = []
for jid, goal, vis, autos, manuals, caps, negs, recs, rexps in JOURNEYS:
    JOURNEY_ROWS.append({
        "journey_id": jid, "required": True, "user_goal": goal, "expected_visible_result": vis,
        "expected_automatic_behavior": list(autos), "expected_manual_behavior": list(manuals),
        "allowed_hitl": ["credential/secret", "owner-merge-approval", "owner-release-approval"],
        "required_capabilities": list(caps), "negative_behavior": list(negs),
        "failure_recovery": list(recs), "source_expectation_ids": list(rexps),
        "source_locators": [str(P0) + "#3 Intent", str(P1) + "#4"],
    })

GATES = [
    ("G-S4R2M-PROMPT-COMPILE", "NATIVE_COMPILER_PASS", "lint, activation and acceptance return PROMPT_COMPILE_PASS with zero errors and compile emits the receipt",
     "python scripts/prompt_contract_compiler.py lint|activation|acceptance|compile <contract>",
     "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-HGK-ADMISSION", "TYPED_ADMISSION_READBACK", "requirement, taskspec and workorder exist and the readback names the same writable root the writer used",
     "hg_kseos SharedSpine typed API readback script in the round admission directory",
     "HERMES_PLAN_LANE", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-README-PATCH", "PATCH_BOUND_TO_WRITE_SET", "the README diff touches only the admitted paths and both documented positives/negatives reproduce",
     "git diff --name-status against the frozen base, plus the pasted onboarding commands",
     "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-ISOLATED-REGRESSION", "AFFECTED_SUITE_PASS", "the six named affected modules run green in a writable clone while the read-only subject keeps identical bytes",
     "python -m unittest discover -s tests -p '<module>' in the disposable clone",
     "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-EXACT-SET", "EXACT_SET_UNCHANGED", "19 schemas and registry, 8 logical skill directories and 13 CLI commands are unchanged",
     "registry/skills/CLI enumerators compared against the frozen candidate tuple",
     "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-INDEPENDENT-VERIFY", "INDEPENDENT_VERDICT", "the officer verdict is derived from its own re-runs on the frozen candidate, not from the maker report",
     "checker lane one-shot with the round VERIFY contract",
     "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
    ("G-S4R2M-MAIN-MERGE", "REF_READBACK", "the remote main ref points at the approved candidate commit and the preview.2 tag is byte-identical",
     "git ls-remote plus an anonymous readback of the release tag",
     "HGK_REPO_OWNER_APPROVED_ROUTE", "INDEPENDENT_READBACK_OFFICER"),
    ("G-S4R2M-RELEASE-GATE", "RELEASE_GATE_DECISION", "the release gate is either executed with a strictly greater PEP 440 version and a re-download readback, or recorded as deferred",
     "packaging.version comparison plus an isolated install and an anonymous re-download",
     "HGK_RELEASE_OWNER_APPROVED_ROUTE", "INDEPENDENT_READBACK_OFFICER"),
    ("G-S4R2M-SECURITY-ADVERSARIAL", "NO_UNADMITTED_WRITE", "prompt injection, a forged owner receipt, a path escape and a secret canary are all refused",
     "adversarial negative matrix run beside the positive probe in the same receipt",
     "HERMES_PLAN_LANE", "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER"),
]
EVIDENCE = []
for gid, pred, expected, probe, prod, chk in GATES:
    EVIDENCE.append({
        "gate_id": gid, "predicate": pred, "expected": expected, "command_or_probe": probe,
        "raw_receipt_required": True, "producer": prod, "independent_checker": chk,
        "candidate_binding": {"head": "SEE_ROUND_CANDIDATE_TUPLE",
                              "package_sha256": "SEE_ROUND_CANDIDATE_TUPLE",
                              "source_hashes": [f[0] for f in FAMILIES]},
        "tracked_subject": True, "rerun_rule": "affected-only",
        "invalidation": ["candidate head change", "evidence manifest change", "policy version change",
                         "release tag change"],
        "terminal_verdict": "INDEPENDENT_CASE_PASS", "runtime_pass_allowed": False,
        "claim_level": "EXTERNAL_ACCEPTANCE",
    })

CONTRACT = {
    "schema": "CAPC-PROMPT-CONTRACT/1",
    "task_id": "PIPD-LS-SP-HERMES-S4R2M-MERGE-AND-PREVIEW3-CONDITIONAL",
    "source_scan": {
        "required_source_families": [f[0] for f in FAMILIES],
        "reviewed": REVIEWED,
        "missing": [],
        "normative_claims": NORMATIVE_CLAIMS,
    },
    "intent": {
        "goal": "Under HG-KSEOS as the sole control plane, carry the S4-R2 repairs already present on the s4-r2 branch through the two README corrections and an isolated focused regression, then integrate conditionally into main; open a separate release gate for preview.3 only if the owner selects it.",
        "user_expected_outcome": "A half-closed round: the README routes CLI and Skills separately, --root is described the way the CLI really behaves, the frozen product passes an isolated affected regression, and main either carries the repairs with a readback or is honestly left at MERGE_READY_HITL_PENDING.",
        "user_expected_experience": "An ordinary reader can pick one of two paths and reach a working install or a mounted document pack without believing that a wheel install loads native web skills; preview.2 keeps serving existing users.",
        "explicit_constraints": [
            "56. No 20th schema, no 9th logical skill, no 14th CLI command.",
            "57. Do not rewrite the frozen s4-r2 product commit, the sealed preview.1/.2 tags or their assets.",
            "58. The read-only checker subject must never be mutated by a suite run.",
            "59. Fabric stays a read-only policy consumer; HG-KSEOS stays the only writer-facing control plane.",
            "60. Five ProfileBinding mutants stay closed; the version grammar stays a deferred P2 observation.",
        ],
        "non_goals": [
            "61. S5-S8, GENIE, JIT, SWOF live receivers and the 22 inactive providers.",
            "62. A full 57-row source crosswalk in PASS state as a precondition for this Beta repair.",
            "63. Rebuilding the 11 PKG + 10 DOC + skeleton corpus as a second SSOT.",
            "64. Making PIPD an agent runtime, a security LLM judge or a credential broker.",
            "65. Re-running a full S0-S4 re-audit after a documentation change.",
        ],
        "authorized_mutations": [
            "66. README.md and a small docs smoke test on the admitted candidate branch.",
            "67. Round evidence under .hgk/rounds/S4R2M-20261012-merge-and-preview3/.",
            "68. A fast-forward of the approved candidate into main under owner approval.",
            "69. A new immutable preview tag plus wheel and mount pack, only under a separate owner release approval.",
        ],
        "forbidden_mutations": [
            "70. Force-push, tag rewrite, or overwriting a published asset.",
            "71. Writing into the frozen checker subject or into another profile's skills/plugins/cron.",
            "72. Printing, copying or committing any credential value.",
            "73. Widening the admitted write-set without a new requirement.",
        ],
        "expected_autonomy": "HIGH",
        "allowed_hitl": ["credential/secret", "owner-merge-approval", "owner-release-approval", "license/entitlement"],
        "requested_delivery": DELIVERABLES,
        "active_requirement_ids": REQUIREMENTS,
        "claim_ceiling": "EXTERNAL_ACCEPTANCE",
    },
    "authority": {
        "sources": SOURCES,
        "conflicts": [],
        "missing_sources": [],
        "native_control_plane_ids": ["HG-KSEOS"],
        "current_control_plane_id": "HG-KSEOS",
    },
    "changeset": {
        "class": "NARROW_REPAIR",
        "baseline_required": True,
        "baseline_verified": True,
        "reuse_prior_pass": True,
        "affected_domains": ["README/docs", "tests(affected only)", "round evidence", "repository integration", "release gate (conditional)"],
        "affected_files": ["README.md", "tests/test_s4r2m_docs_route.py", ".hgk/rounds/S4R2M-20261012-merge-and-preview3/**"],
        "must_not_reopen": [
            "frozen s4-r2 product commit 7c00b64960d86fc1e94848c9955c512a3626a85f",
            "19 schema set and registry",
            "8 logical SkillContracts and 5 web documents",
            "13 CLI command set",
            "ProfileBinding five decision fields and their four early mutants",
            "sealed preview.1/.2 tags and assets",
            "HG-KSEOS and Fabric sealed control surfaces",
        ],
        "scope_expansion_requires_hitl": True,
        "tracked_mutation": True,
        "product_mutation_allowed": True,
    },
    "execution_scope": EXEC,
    "runtime_readiness": READINESS,
    "journeys": JOURNEY_ROWS,
    "acceptance": ACCEPT,
    "evidence": EVIDENCE,
    "termination": {
        "terminal_states": ["S4R2M_MAIN_MERGED_PREVIEW3_DEFERRED", "S4R2M_PREVIEW3_PUBLISHED_SCOPED"],
        "non_terminal_pause": ["MERGE_READY_HITL_PENDING", "RELEASE_HITL_PENDING", "AUTH_BLOCKED",
                               "ITERATION_BUDGET_PAUSE", "SESSION_BOUNDARY", "TEMP_CLOSED", "FAIL"],
        "checkpoint_required": True,
        "checkpoint_fields": ["task_id", "source_hashes", "current_candidate", "completed_gates",
                              "open_gates", "next_work_order", "rollback_pointer", "workorder_ids", "tt_delta"],
        "retry_budget": 3,
        "rollback_pointer_required": True,
    },
    "render_policy": {
        "control_corpus_restatement": False,
        "embedded_control_bodies": [],
        "max_prompt_chars": 30000,
        "output_language": "zh-Hant-TW",
    },
}

import re as _re

_NUM = _re.compile(r"^\d+\.\s+")


def _norm(obj):
    """Strip the drafting numerals accidentally left in prose strings."""
    if isinstance(obj, str):
        return _NUM.sub("", obj)
    if isinstance(obj, list):
        return [_norm(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _norm(v) for k, v in obj.items()}
    return obj


out = ROUND_DIR / "S4R2M.CONTRACT.json"
out.write_text(json.dumps(_norm(CONTRACT), ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", out)
print("families:", len(FAMILIES), "exec:", len(EXEC), "readiness:", len(READINESS),
      "journeys:", len(JOURNEY_ROWS), "acceptance:", len(ACCEPT), "evidence:", len(EVIDENCE))
