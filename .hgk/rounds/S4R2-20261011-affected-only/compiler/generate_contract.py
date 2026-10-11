#!/usr/bin/env python
"""Generate the R2 post-release affected-only CONTRACT.json.

The contract is GENERATED, not hand-written, so every field is schema-exact: each R2 item is
built by cloning the corresponding R1 item (whose key set already passed the native compiler)
and overriding the values. Nothing is invented at lint time.

C0..C9 map onto the native contract this way:
  C0 -> source_scan.required_source_families / reviewed / missing
  C1 -> intent.goal, journeys, acceptance
  C2 -> authority
  C3 -> changeset.class  (exactly one: NARROW_REPAIR)
  C4 -> execution_scope, runtime_readiness   (active / deferred / forbidden, historical kept)
  C5 -> runtime_readiness[*].lifecycle       (named-route readiness edges)
  C6 -> journeys                             (the five user journeys)
  C7 -> acceptance[*] positive/negative/recovery fixtures + terminal states
  C8 -> evidence[*].producer / independent_checker / claim_ceiling
  C9 -> termination
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(r"C:\Projects\Agent_Workspace\PIPD-postrelease-wt")
R1 = REPO / ".hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/compiler/S4POST.CONTRACT.json"
OUT = HERE / "S4R2.CONTRACT.json"

TASK_ID = "PIPD-LS-SP-S4-R2-POSTRELEASE-AFFECTED-ONLY-20261011"
PRODUCER = "HERMES_ORCHESTRATOR_PLAN_LANE_DEEPSEEK-V4.1-FLASH"
CHECKER = "GPT-6.1-SOL-MEDIUM_OPENAI-OAUTH_INDEPENDENT_OFFICER"
WRITER = "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH"
CLAIM = "CANDIDATE_ONLY_UNTIL_INDEPENDENT_AND_HITL"

R2_PROMPT = (r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local"
             r"\hermes\attachments\PIPD-LS-SP_HERMES_S4_R2_POSTRELEASE_AFFECTED_ONLY_REPAIR_PROMPT_2026-10-11.md")
R2_REPORT = (r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\驗收報告"
             r"\PIPD_LS_SP_S4_MVP_PostRelease_Independent_Reaudit_Final_2026-10-11.md")


def sha(p: str) -> str:
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()
    except OSError:
        return "UNAVAILABLE"


FAMILIES = ["F0_S4R2_REPAIR_PROMPT", "F1_S4R2_REAUDIT_REPORT", "F2_RELEASE_SUBJECT_EVIDENCE",
            "F3_PIPD_UPSTREAM_CORPUS", "F4_PUBLIC_ROLLING_MAIN", "F5_HGK_CONTROL_PLANE",
            "F6_FABRIC_CONTRACT", "F7_LOCAL_CANDIDATE_WORKTREE"]

REVIEWED = [
    ("F0_S4R2_REPAIR_PROMPT", "NORMATIVE", R2_PROMPT, sha(R2_PROMPT), True),
    ("F1_S4R2_REAUDIT_REPORT", "NORMATIVE", R2_REPORT, sha(R2_REPORT), True),
    ("F2_RELEASE_SUBJECT_EVIDENCE", "STATE_EVIDENCE",
     "https://github.com/shw097-team/PIPD-LS-SP@8faa64e581e8c25f5ec355475e29561847da3ead",
     "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f", True),
    ("F3_PIPD_UPSTREAM_CORPUS", "NORMATIVE",
     "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD",
     "UNAVAILABLE", True),
    ("F4_PUBLIC_ROLLING_MAIN", "STATE_EVIDENCE",
     "https://github.com/shw097-team/PIPD-LS-SP@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7",
     "UNAVAILABLE", False),
    ("F5_HGK_CONTROL_PLANE", "NORMATIVE", "C:/Projects/Agent_Workspace/HG-KSEOS", "UNAVAILABLE", True),
    ("F6_FABRIC_CONTRACT", "NORMATIVE", "C:/Projects/Agent_Workspace/Fabric", "UNAVAILABLE", True),
    ("F7_LOCAL_CANDIDATE_WORKTREE", "STATE_EVIDENCE",
     "C:/Projects/Agent_Workspace/PIPD-postrelease-wt@s4-r2-affected-only-20261011",
     "UNAVAILABLE", False),
]

NC = [
    ("NC-01", ["F0_S4R2_REPAIR_PROMPT", "F5_HGK_CONTROL_PLANE"],
     "HG-KSEOS remains the sole admission / WorkOrder / evidence / release control plane; Hermes is the admitted runtime orchestrator; Fabric is read-only policy.",
     ["F0 §2.3", "F0 §2.6"]),
    ("NC-02", ["F1_S4R2_REAUDIT_REPORT"],
     "The reaudit returned PARTIAL_CHALLENGE over F-S4R2-01..12; it does not authorise a full S0-S4 pass, and neither this contract nor the round may self-sign one.",
     ["F1 §0", "F1 §9", "F1 §14"]),
    ("NC-03", ["F1_S4R2_REAUDIT_REPORT", "F0_S4R2_REPAIR_PROMPT"],
     "Only affected-only maintenance is in scope; the published v0.1.0-preview.2 tag and its four assets are immutable.",
     ["F1 §10.1", "F0 §1", "F0 §4"]),
    ("NC-04", ["F0_S4R2_REPAIR_PROMPT"],
     "No new release is created without an owner HITL decision; document-only repair must not rebuild the wheel.",
     ["F0 §4 CONDITIONAL", "F0 §5"]),
    ("NC-05", ["F0_S4R2_REPAIR_PROMPT", "F1_S4R2_REAUDIT_REPORT"],
     "A finding already closed with fresh positive AND negative evidence is marked ALREADY_CLOSED_WITH_FRESH_POS_NEG and is not rewritten.",
     ["F0 §2.4", "F0 §5"]),
    ("NC-06", ["F1_S4R2_REAUDIT_REPORT"],
     "S5 HGK live receiver, S6 GENIE, S7 JIT, S8 SWOF/SGM and the 22 inactive providers stay OFF and are never a reason to fail S4.",
     ["F1 §4", "F1 §9 F-S4R2-11"]),
    ("NC-07", ["F0_S4R2_REPAIR_PROMPT"],
     "Independently verifiable evidence only: raw command, raw output, exit code, subject binding. A local suite or a Hermes goal state is not a pass.",
     ["F0 §8", "F0 §9"]),
    ("NC-08", ["F1_S4R2_REAUDIT_REPORT"],
     "An axis count is not a risk score: without risk evidence the honest state is NOT_ASSESSED and LOW_RISK_VERIFIED is never emitted.",
     ["F1 §6.1", "F1 §9 F-S4R2-03"]),
    ("NC-09", ["F1_S4R2_REAUDIT_REPORT"],
     "Uploading an MD is not installing a native skill; the two web consumption modes are declared separately or reported NOT_RUN.",
     ["F1 §4.1", "F1 §12", "F1 §9 F-S4R2-06"]),
]

EXEC_SCOPE = [
    # (capability, action, current_execution_disposition, selected, runtime_required_now, locators, acceptances)
    ("CAP_S4R2_CLI_FIRSTUSE_VERIFY", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 P1", "F1 section 5", "F1 F-S4R2-01"], ["ACC-CAP_S4R2_CLI_FIRSTUSE_VERIFY"]),
    ("CAP_S4R2_COMPILER_REAL_FIXTURE", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 P1", "F1 W05", "F1 F-S4R2-05"], ["ACC-CAP_S4R2_COMPILER_REAL_FIXTURE"]),
    ("CAP_S4R2_WEB_MOUNT_CONSUME", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 P2", "F1 W02", "F1 F-S4R2-06"], ["ACC-CAP_S4R2_WEB_MOUNT_CONSUME"]),
    ("CAP_S4R2_PROFILE_TRUST", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 P3", "F1 section 6.1", "F1 F-S4R2-02"], ["ACC-CAP_S4R2_PROFILE_TRUST"]),
    ("CAP_S4R2_MACHINE_CONTRACT_TYPING", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 P3", "F1 section 6.2", "F1 F-S4R2-04", "F1 F-S4R2-NEW-01"], ["ACC-CAP_S4R2_MACHINE_CONTRACT_TYPING"]),
    ("CAP_S4R2_SOURCE_BOOTSTRAP", "DESIGN", "ACTIVE_SELECTED", True, False,
     ["F0 P4", "F1 W06", "F1 F-S4R2-10"], ["ACC-CAP_S4R2_SOURCE_BOOTSTRAP"]),
    ("CAP_S4R2_HGK_ADMISSION", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 section 2.3", "F0 P0.2"], ["ACC-CAP_S4R2_HGK_ADMISSION"]),
    ("CAP_S4R2_INDEPENDENT_VERIFY", "QUALIFY", "ACTIVE_REQUIRED", True, True,
     ["F0 section 8", "F1 section 3.1"], ["ACC-CAP_S4R2_INDEPENDENT_VERIFY"]),
    ("CAP_S4R2_GITHUB_PUBLICATION", "DESIGN", "STANDBY", False, False,
     ["F0 credentials", "F0 P0.3"], ["ACC-CAP_S4R2_GITHUB_PUBLICATION"]),
    ("CAP_S4R2_S5_PROVIDERS", "DESIGN", "NOT_APPLICABLE_SOURCE_BACKED", False, False,
     ["F1 F-S4R2-11", "F1 section 4"], ["ACC-CAP_S4R2_S5_PROVIDERS"]),
]

REQUIREMENTS = [
    ("REQ-S4R2-DOC-001", "first-run documentation and a literal compiler walk-through",
     ["CAP_S4R2_CLI_FIRSTUSE_VERIFY", "CAP_S4R2_COMPILER_REAL_FIXTURE"]),
    ("REQ-S4R2-WEB-002", "a consumable, capability-labelled web mount pack",
     ["CAP_S4R2_WEB_MOUNT_CONSUME"]),
    ("REQ-S4R2-CONTRACT-003", "typed identity/trace contracts and honest profile risk state",
     ["CAP_S4R2_PROFILE_TRUST", "CAP_S4R2_MACHINE_CONTRACT_TYPING"]),
    ("REQ-S4R2-SOURCE-004", "a pinned external source map and one replayable self-bootstrap",
     ["CAP_S4R2_SOURCE_BOOTSTRAP"]),
]

DELIVERABLES = [
    "S4R2_PROMPT_COMPILER_READBACK", "S4R2_HGK_ADMISSION_READBACK", "S4R2_FINDING_DISPOSITION",
    "S4R2_UAT_MATRIX", "S4R2_CANDIDATE_TUPLE", "S4R2_EVIDENCE_MASTER_MD",
    "S4R2_KANBAN_SWARM_RECEIPT", "S4R2_OPENSPEC_CHANGE", "S4R2_INDEPENDENT_RECEIPT",
    "S4R2_WEB_MOUNT_READBACK", "S4R2_RESIDUAL_TYPING_PATCH", "S4R2_PUBLICATION_STATUS",
]

JOURNEYS = [
    ("J-CLI-FIRST", "In an empty directory outside the repository a first-time user follows the README on bash "
                   "or PowerShell: download, verify only what was downloaded, install, doctor, init - every "
                   "line exits 0, and a tampered or missing asset exits non-zero.",
     ["only the listed assets are fetched", "the checksum covers exactly the fetched set",
      "doctor reports the resolved schema source"],
     ["the user needs a shell and Python >= 3.11"],
     "exit 0 per line, wheel digest equals the published literal, and a mutated byte stops the block",
     ["a missing asset, a wrong URL or a pip-less interpreter must fail loudly"],
     ["re-running a partial download must never report OK for an absent file"],
     ["CAP_S4R2_CLI_FIRSTUSE_VERIFY"], ["REQ-S4R2-DOC-001"],
     ["F0 P1", "F1 §5", "README.md Quickstart"]),
    ("J-COMPILER-REAL", "A newcomer copies a real, existing fixture and drives intake -> compile-pi -> bind-pd -> "
                        "compile-ecp -> compile-tqaep -> validate with no placeholder and no fake source; a second "
                        "replay is digest-stable and a missing source is refused.",
     ["the README points at a fixture that exists in the tree", "every command's flags match the real CLI",
      "the transcript is the raw stdout of a real run"],
     ["the user supplies a disposable directory outside the repository"],
     "a valid chain with verifiable artefact digests, stable on replay",
     ["a fabricated source or receipt must be refused with a typed error"],
     ["typed refusals name the exact missing authority"],
     ["CAP_S4R2_COMPILER_REAL_FIXTURE"], ["REQ-S4R2-DOC-001"],
     ["F0 P1", "F1 §7 W05", "examples/self-bootstrap/"]),
    ("J-PROFILE-TRUST", "Profile selection refuses duplicate or wrong-typed axes with a typed first-fail, and an "
                        "unknown or unevidenced risk state is reported as NOT_ASSESSED instead of being called safe.",
     ["duplicate axes are refused before any escalation math", "the emitted axes equal the effective axes",
      "risk_assessment is honest"],
     ["the user states the profile and axis set"],
     "LITE / STANDARD / ASSURED still resolve for legal inputs; illegal ones refuse",
     ["nine category axes are not twelve calibrated risk axes; LOW_RISK_VERIFIED is never emitted"],
     ["the legal ladder does not regress"],
     ["CAP_S4R2_PROFILE_TRUST"], ["REQ-S4R2-CONTRACT-003"],
     ["F0 P3", "F1 §6.1", "src/pipd_ls_sp/profiles.py"]),
    ("J-MACHINE-CONTRACT", "The 19 contract families stay exact; an illegally typed identity/trace value is refused "
                           "with an accurate first-fail and the earlier CE-1/CE-2 refusals do not regress.",
     ["identity fields carry a JSON type", "the PI trace shape is constrained", "no string-cast leniency"],
     ["the user supplies a bundle or a record"],
     "a legal bundle validates with zero findings; int/null/scalar/malformed cases each fail on the right field",
     ["stray trace keys stay refused for PD/ECP/TQAEP"],
     ["a legal legacy fixture still succeeds"],
     ["CAP_S4R2_MACHINE_CONTRACT_TYPING"], ["REQ-S4R2-CONTRACT-003"],
     ["F0 P3", "F1 §6.2", "schemas/PI-PKG.schema.json"]),
    ("J-WEB-CONSUMER", "A web consumer mounts the single versioned pack and gets sourced candidate answers, while "
                       "native-skill upload and manual document/Knowledge mode are declared separately and a host "
                       "without native eligibility is reported NOT_RUN.",
     ["the dispatcher routes to the references", "the two modes are described separately",
      "the pack never claims host capability it lacks"],
     ["the user attaches the ZIP or uploads the skill, depending on account capability"],
     "five recorded cases; refusals stay typed and the claim ceiling is visible",
     ["the pack must not assert native load from mere file presence"],
     ["a refusal explains what is missing rather than inventing a result"],
     ["CAP_S4R2_WEB_MOUNT_CONSUME"], ["REQ-S4R2-WEB-002"],
     ["F0 P2", "F1 §4.1", "F1 §12", "dist/mount/"]),
]

# Acceptance items are DERIVED from the four subject sets so every declared subject has an
# acceptance edge (PL-009) and no subject_id is invented.
DEPTH_BY_KIND = {"CAPABILITY": "L3_INTEGRATION_RUNTIME", "JOURNEY": "L3_INTEGRATION_RUNTIME",
                 "REQUIREMENT": "L3_INTEGRATION_RUNTIME", "DELIVERABLE": "L1_SCHEMA_CONTRACT"}

GATES = [
    ("G-S4R2-PROMPT-COMPILE", "NATIVE_COMPILER_PASS",
     "python scripts/prompt_contract_compiler.py lint|activation|acceptance|compile <contract>",
     ["CAP_S4R2_HGK_ADMISSION"], ["contract change", "compiler bundle change", "source hash change"]),
    ("G-S4R2-HGK-ADMISSION", "HGK_ADMISSION_TRACE",
     "hg_kseos lifecycle API + kanban board readback",
     ["CAP_S4R2_HGK_ADMISSION"], ["lifecycle state change", "board change"]),
    ("G-S4R2-DOC-FIRSTUSE", "FRESH_SHELL_REPLAY",
     "fresh bash + PowerShell replay of the README quickstart from an empty scratch directory",
     ["CAP_S4R2_CLI_FIRSTUSE_VERIFY"], ["README change", "release asset change"]),
    ("G-S4R2-COMPILER-FIXTURE", "REAL_FIXTURE_REPLAY",
     "drive examples/self-bootstrap/ then the documented CLI chain twice and compare digests",
     ["CAP_S4R2_COMPILER_REAL_FIXTURE"], ["fixture change", "CLI change"]),
    ("G-S4R2-WEB-MOUNT", "PACK_READBACK",
     "extract the mount ZIP, verify MANIFEST.sha256, and run the five recorded consumption cases",
     ["CAP_S4R2_WEB_MOUNT_CONSUME"], ["pack change", "reference change"]),
    ("G-S4R2-CONTRACT-HARDEN", "TYPED_REFUSAL_POS_NEG",
     "positive + negative + mutation probes against profiles and the contract schemas",
     ["CAP_S4R2_PROFILE_TRUST", "CAP_S4R2_MACHINE_CONTRACT_TYPING"],
     ["schema change", "profiles change", "pipeline change"]),
    ("G-S4R2-REGRESSION", "EXACT_SET_AND_SUITE",
     "19/8/13 exact sets plus the affected dependency edges of the full suite",
     ["CAP_S4R2_MACHINE_CONTRACT_TYPING"], ["any product file change"]),
    ("G-S4R2-INDEPENDENT-VERIFY", "INDEPENDENT_SCOPE_RECEIPT",
     "the independent checker lane re-derives the decisive claims on the frozen candidate",
     ["CAP_S4R2_INDEPENDENT_VERIFY"], ["candidate change"]),
    ("G-S4R2-PUBLICATION", "OWNER_GATED_REMOTE_WRITE",
     "credential preflight + broker dry-run + remote readback",
     ["CAP_S4R2_GITHUB_PUBLICATION"], ["credential state change"]),
]


def build() -> dict:
    r1 = json.load(open(R1, encoding="utf-8"))
    t = copy.deepcopy(r1)

    t["task_id"] = TASK_ID
    t["source_scan"]["required_source_families"] = FAMILIES
    t["source_scan"]["reviewed"] = [
        {"source_id": i, "source_family": i, "locator": loc, "role": role, "sha256": h, "critical": c}
        for i, role, loc, h, c in REVIEWED]
    t["source_scan"]["missing"] = []
    t["source_scan"]["normative_claims"] = [
        {"claim_id": cid, "source_ids": sids, "locators": locs, "text": text} for cid, sids, text, locs in NC]

    t["authority"] = copy.deepcopy(r1["authority"])
    t["authority"]["sources"] = [
        {"id": i, "locator": loc, "path": loc, "role": role,
         "rank": "R0" if role == "NORMATIVE" else "R3", "governs": role == "NORMATIVE", "sha256": h}
        for i, role, loc, h, c in REVIEWED]
    t["authority"]["conflicts"] = []
    t["authority"]["missing_sources"] = []

    jt = r1["journeys"][0]
    t["journeys"] = []
    for jid, goal, auto, manual, vis, neg, rec, caps, accs, locs in JOURNEYS:
        j = copy.deepcopy(jt)
        j.update({"journey_id": jid, "required": True, "user_goal": goal,
                  "expected_automatic_behavior": auto, "expected_manual_behavior": manual,
                  "expected_visible_result": vis, "negative_behavior": neg, "failure_recovery": rec,
                  "required_capabilities": caps, "source_locators": locs})
        j["source_expectation_ids"] = [a for a in accs]
        t["journeys"].append(j)

    at = r1["acceptance"][0]

    def acc_item(aid, sid, stype, runtime, locs, states):
        a = copy.deepcopy(at)
        a.update({"acceptance_id": aid, "subject_id": sid, "subject_type": stype,
                  "required_depth": DEPTH_BY_KIND[stype], "runtime_required": runtime,
                  "positive_fixture": f"positive fixture for {sid}",
                  "negative_fixture": f"negative/mutation fixture for {sid}",
                  "recovery_fixture": f"recovery fixture for {sid}",
                  "raw_evidence_required": True, "independent_checker_required": runtime,
                  "source_locators": locs, "terminal_states": states})
        return a

    T_RT = ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL"]
    T_STATIC = ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "NOT_RUN"]
    t["acceptance"] = []
    for cid, action, disp, sel, runtime, locs, accs in EXEC_SCOPE:
        t["acceptance"].append(acc_item(f"ACC-{cid}", cid, "CAPABILITY", runtime, locs,
                                        T_RT if runtime else T_STATIC))
    for jid, goal, auto, manual, vis, neg, rec, caps, reqs, locs in JOURNEYS:
        t["acceptance"].append(acc_item(f"ACC-{jid}", jid, "JOURNEY", True, locs, T_RT))
    for rid, text, caps in REQUIREMENTS:
        t["acceptance"].append(acc_item(f"ACC-{rid}", rid, "REQUIREMENT", False,
                                        ["F0 section 3", "F1 section 9"], T_STATIC))
    for did in DELIVERABLES:
        t["acceptance"].append(acc_item(f"ACC-{did}", did, "DELIVERABLE", False,
                                        ["F0 section 8", "F0 section 9"], T_STATIC))

    xt = r1["execution_scope"][0]
    t["execution_scope"] = []
    for cid, action, disp, sel, runtime, locs, accs in EXEC_SCOPE:
        x = copy.deepcopy(xt)
        x.update({"capability": cid, "action": action, "source_disposition": disp,
                  "current_execution_disposition": disp, "runtime_required_now": runtime,
                  # PL-006: the Activation Bridge takes `selected` as the OR of these four flags,
                  # so a non-active capability must not assert any of them.
                  "current_profile_selected": sel, "automatic_route_target": sel,
                  "canonical_flow_referenced": sel,
                  "control_authority": cid == "CAP_S4R2_HGK_ADMISSION" and sel,
                  "external_method": cid == "CAP_S4R2_GITHUB_PUBLICATION",
                  "user_experience_required": sel,
                  "source_locators": locs})
        t["execution_scope"].append(x)

    rt = r1["runtime_readiness"][0]
    t["runtime_readiness"] = []
    for cid, action, disp, sel, runtime, locs, accs in EXEC_SCOPE:
        r = copy.deepcopy(rt)
        r["capability"] = cid
        r["current_verdict"] = "NOT_READY"
        r["required_now"] = runtime
        stage = "OPEN" if runtime else "NOT_APPLICABLE_SOURCE_BACKED"
        r["lifecycle"] = {k: stage for k in r["lifecycle"]}
        r["acceptance_ids"] = [f"ACC-{cid}"]
        r["work_required"] = ([f"{x}: capability {cid}" for x in accs] if runtime else [])
        t["runtime_readiness"].append(r)

    et = r1["evidence"][0]
    t["evidence"] = []
    for gid, pred, probe, caps, inval in GATES:
        e = copy.deepcopy(et)
        e.update({"gate_id": gid, "predicate": pred, "command_or_probe": probe,
                  "expected": f"{pred}: verdict evidence from {probe}",
                  "producer": WRITER if gid in ("G-S4R2-DOC-FIRSTUSE", "G-S4R2-COMPILER-FIXTURE",
                                                "G-S4R2-WEB-MOUNT", "G-S4R2-CONTRACT-HARDEN")
                              else PRODUCER,
                  "independent_checker": CHECKER, "rerun_rule": "full",
                  "runtime_pass_allowed": False, "invalidation": inval})
        e["candidate_binding"] = {"head": "SEE_ROUND_CANDIDATE_TUPLE",
                                  "package_sha256": "SEE_ROUND_CANDIDATE_TUPLE",
                                  "source_hashes": ["F0_S4R2_REPAIR_PROMPT", "F1_S4R2_REAUDIT_REPORT",
                                                    "F2_RELEASE_SUBJECT_EVIDENCE",
                                                    "F7_LOCAL_CANDIDATE_WORKTREE"]}
        t["evidence"].append(e)

    t["intent"]["goal"] = (
        "Execute one affected-only post-release maintenance round on the published S4 open-source MVP, "
        "driven by the second-round reaudit: confirm under its own contract which of F-S4R2-01..12 are "
        "already closed by this candidate lineage with fresh positive AND negative evidence, close only "
        "the genuinely open deltas (a real copy-paste end-to-end README fixture, the release version "
        "identity disclosure and the residual ProfileBinding typing hole), and hand the frozen candidate "
        "to an independent checker - without moving the immutable tag.")
    t["intent"]["user_expected_outcome"] = (
        "A first-time user copy-pastes the README from a clean directory and every line exits 0 on bash "
        "and PowerShell; the README points at a fixture that really exists so intake -> compile-pi -> "
        "bind-pd -> compile-ecp -> compile-tqaep -> validate can be driven literally; malformed identity, "
        "trace and profile inputs are refused by exact typed first-fail; and the repository states where "
        "its normative sources live without creating a second SSOT.")
    t["intent"]["user_expected_experience"] = (
        "The user needs only a shell, Python >= 3.11 and a ZIP upload; they never need to know WorkOrder, "
        "Skill or provider identifiers.")
    t["intent"]["explicit_constraints"] = [
        "AFFECTED-ONLY: keep the 19 schema families, 8 logical skills, 13 CLI commands, 5 web / 3 host projections and the clause-bound PI/PD trunk intact.",
        "A finding already closed with fresh positive and negative evidence is marked ALREADY_CLOSED_WITH_FRESH_POS_NEG and is not rewritten.",
        "The native prompt compiler must actually run; a missing bundle or a failure means PROMPT_COMPILE_BLOCKED with read-only preflight only.",
        "No new release: a document-only repair must not rebuild the wheel, and a new tag stays an owner HITL decision.",
        "Claims do not inherit: LOCAL_TESTED != INDEPENDENT_ACCEPTED != RELEASED, and the checker model is GPT 6.1 SOL-MEDIUM over OpenAI OAuth.",
    ]
    t["intent"]["non_goals"] = [
        "No second canonical SSOT, no second control plane, no plan IR, no scheduler.",
        "No S5 HGK live receiver, S6 GENIE, S7 JIT, S8 SWOF/SGM, PRE-W3 or the 22 inactive external technologies.",
        "No tag move, no force-push, no rewrite of published release bytes, no rewrite of historical FAIL receipts.",
        "No new 20th schema family, no 9th logical skill, no 14th CLI command, no MCP server or resident daemon.",
        "No restatement or cloning of the 11 PKG / 10 DOC / skeleton bodies into the runtime repository.",
    ]
    t["intent"]["authorized_mutations"] = [
        "Minimal product-tree repair inside C:/Projects/Agent_Workspace/PIPD-postrelease-wt on branch s4-r2-affected-only-20261011: README.md, examples/**, schemas/ProfileBinding.schema.json and any already-affected schema, and new tests under tests/.",
        "The round evidence tree .hgk/rounds/S4R2-20261011-affected-only/.",
        "The single acceptance master document under 知識庫/實作相關DOC/PIPD/實作證據/.",
    ]
    t["intent"]["forbidden_mutations"] = [
        "No second normative authority built from Hermes or Fabric; no self-signed INDEPENDENT_PASS.",
        "No destructive test against a real user path, no credential in argv/URL/log, no force-push, no history rewrite.",
        "No editing of any published tag, release asset or previous round's receipt.",
        "No promotion of this candidate or of the claim ceiling by the maker.",
    ]
    t["intent"]["allowed_hitl"] = ["NEW_RELEASE_OR_TAG", "REMOTE_WRITE", "SCOPE_EXPANSION",
                                   "CREDENTIAL_USE", "CLAIM_CEILING_CHANGE"]
    t["intent"]["requested_delivery"] = list(DELIVERABLES)
    t["intent"]["active_requirement_ids"] = [r[0] for r in REQUIREMENTS]
    t["intent"]["claim_ceiling"] = "EXTERNAL_ACCEPTANCE"
    t["intent"]["expected_autonomy"] = "HIGH"

    t["changeset"] = copy.deepcopy(r1["changeset"])
    t["changeset"]["class"] = "NARROW_REPAIR"
    t["changeset"]["affected_domains"] = ["README.md", "examples", "schemas", "tests", ".hgk"]
    t["changeset"]["affected_files"] = [
        "README.md",
        "schemas/ProfileBinding.schema.json",
        "examples/self-bootstrap/README.md",
        "tests/test_postrelease_quickstart.py",
        "tests/test_s4r2_affected_only.py",
    ]
    t["changeset"]["must_not_reopen"] = [
        "the 19 schema family set and registry exactness",
        "the 8 logical skills and 5 web / 3 host projections",
        "the 13 CLI command names",
        "R7/R8 receipts as recorded (SCOPED_PASS / OVERALL_FAIL)",
        "the published tag v0.1.0-preview.2 and its four release assets",
        "the HG-KSEOS / Fabric frozen control surfaces",
    ]

    t["termination"] = copy.deepcopy(r1["termination"])
    t["termination"]["terminal_states"] = [
        "S4_R2_AFFECTED_ONLY_CANDIDATE_DELIVERED", "FAIL", "BLOCKED_HITL", "BLOCKED_EXTERNAL",
        "NO_WRITES_TEMP_CLOSED"]
    t["termination"]["retry_budget"] = 3
    t["render_policy"] = copy.deepcopy(r1["render_policy"])
    return t


def main() -> int:
    doc = build()
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)
    print("task_id:", doc["task_id"])
    print("families:", len(doc["source_scan"]["required_source_families"]),
          "reviewed:", len(doc["source_scan"]["reviewed"]),
          "missing:", len(doc["source_scan"]["missing"]))
    print("journeys:", len(doc["journeys"]), "acceptance:", len(doc["acceptance"]),
          "evidence:", len(doc["evidence"]), "exec_scope:", len(doc["execution_scope"]))
    print("changeset.class:", doc["changeset"]["class"])
    h = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print("contract_sha256:", h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
