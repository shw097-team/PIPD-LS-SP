#!/usr/bin/env python3
"""Build the R4->R5 closeout PIPD contract (CAPC-PROMPT-CONTRACT/1).

Round: C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5-20261014-s4-r4-closeout
Subject: frozen R4 subjects (main 2245914..., PR3 759b9f0..., PR5 940a37d...).
Lane mandate: PLAN=Hermes weave (glm-5.3-flash/opencode-go), EXECUTE=Codex CLI
(deepseek-v4.1-flash/opencode-go), CHECKER=Codex CLI (glm-5.3-flash/opencode-go).
Outputs compiler/R5X.CONTRACT.json; run native compiler for receipts (R5-04 step).
"""
import json
from pathlib import Path

ROUND = Path(r"C:/Projects/Agent_Workspace/PIPD/.hgk/rounds/R5-20261014-s4-r4-closeout")
SF = json.loads((ROUND / "source-freeze" / "sources_manifest.json").read_text(encoding="utf-8"))

def sha_lookup(suffix):
    for s in SF["sources"]:
        if s["path"].endswith(suffix):
            return s["sha256"]
    return None

def F(id, locator_suffix, role="NORMATIVE", rank="R0", governs=True):
    return {"id": id, "locator": locator_suffix, "role": role, "rank": rank,
            "governs": governs, "sha256": sha_lookup(locator_suffix)}

SRC = [
    F("F0_R4_EXT_ACCEPT_R4_20261013", "PIPD-LS-SP｜S4 R4 驗收報告_20261013-3.md"),
    F("F1_R4_EXECUTION_PROMPT", "PIPD-LS-SP S4 R4｜Hermes  HG-KSEOS  Fabric 合規指揮薄 PROMPT_2026-10-13-3.md"),
    F("F2_PLUGIN_PLAN", "PIPD-LS-SP_GPT外掛程式上架方案-3.md"),
    F("F3_TRIPLE_R2", "PIPD-LS-SP S4｜三合一小型升級藍圖-6.md"),
    F("F4_PKG00", "PIPD-LS-SP_PIPD-PKG-00.md"),
    F("F5_KB11_EVIDENCE", "11_EVIDENCE_REQUIREMENT_MATRIX.md"),
    F("F6_KB12_JUDGE", "12_EVAL_REGRESSION_LLM_JUDGE.md"),
    F("F7_KB16_RELEASE", "16_RELEASE_PACKAGING_CHECKSUM_READBACK.md"),
    F("F8_KB17_UX", "17_UX_ONBOARDING_NO_BRAIN_FLOW.md"),
    F("F9_KB18_TTCR", "18_TT_CR_DRIFT_REGISTER.md"),
    F("F10_HGK_AGENTS", "AGENTS.md", "SUPPORT", "R1", False),
]
SRC = [s for s in SRC if s["sha256"] is not None]

MAIN = "224591431a164ab72a9423cd180e417e8a762403"
STAGE_A = "759b9f0dc880b2f960363b2ceaa68446c770061d"
STAGE_B = "940a37d00d5c1d12dfc9ae5d2325d8837b08501b"

def cap(cid, wording, locators):
    return {"capability": cid, "work_required": [wording], "source_locators": locators,
            "required_now": True, "current_verdict": "NOT_READY",
            "lifecycle": {k: "OPEN" for k in ("identify", "pin", "install_materialize", "configure",
                                              "discover", "bind", "route", "effective_load",
                                              "doctor_health", "positive_pilot", "negative_security",
                                              "fallback", "rollback_uninstall",
                                              "independent_qualification", "certify", "enable")}}

CAPS = [
    cap("CAP_R5X_PLATFORM_DRIFT_PROBE",
        "WO-R5X-001 PLATFORM_DRIFT_PROBE: fetch the current official submission-errors page "
        "(developers.openai.com/plugins/deploy/submission-errors) fresh; record the supported ZIP "
        "manifest formats verbatim into evidence/PLATFORM_DRIFT_PROBE.json with fetch date and "
        "tool version; no local-cached doc decides the shape.",
        ["R4 report §5.1", "Plugin plan §04.1"]),
    cap("CAP_R5X_MANIFEST_MINIMAL_FIT",
        "WO-R5X-002 manifest minimal fit: keep portable root plugin.json as the single SSOT; "
        "produce a minimal distribution projection adding extensions.com.openai.interface listing "
        "fields (displayName/shortDescription/longDescription/developerName) plus 8 skill paths, "
        "with skill bodies byte-identical; one manifest per ZIP.",
        ["Plugin plan §04.1", "R4 report §5.1"],
    ),
    cap("CAP_R5X_ZIP_BUILD_2X",
        "WO-R5X-003 ZIP build 2x: reuse tools/build_public_plugin.py; build the candidate ZIP "
        "twice from the same frozen Stage B head commit; equal SHA256 readbacks; 8/8 skills, "
        "56-member structural shape retained, single root.",
        ["Plugin plan TS-07", "R4 report §5.2"]),
    cap("CAP_R5X_ZIP_NEGATIVES",
        "WO-R5X-004 negative probes PORTAL-01/02/03: plant mcp.json/hooks/.app.json inside a "
        "scratch-copy ZIP and verify the repo validator/build gate refuses; assert one root per "
        "ZIP; record as named refusal (PORTAL-01..03 rows in gates/NEGATIVE_CASES.json).",
        ["Plugin plan §09 PORTAL rows", "R4 report §5.2"]),
    cap("CAP_R5X_PRIVATE_IMPORT_READINESS",
        "WO-R5X-005 private import readiness pack: plugin_private_host_uat.json scaffold with "
        "route A (Plugin Creator) and route B (workspace upload) procedures + acceptance "
        "criteria; actual Web login/upload is HumanGate - agent records NOT_VERIFIED until owner "
        "executes it.",
        ["Plugin plan TS-10 + §11", "R4 report §5.3"]),
    cap("CAP_R5X_RELEASE_TUPLE",
        "WO-R5X-006 release tuple scaffold: wheel_and_release_tuple.json stub with next "
        "candidate SemVer decision fields for the owner; immutable-new-tag rule; no preview.3 "
        "reuse; actual tag/publish is owner-gated.",
        ["R4 report §6.2/§10"]),
    cap("CAP_R5X_EVIDENCE_RETURN",
        "WO-R5X-007 evidence return pack: PIPD_S4_R4_EVIDENCE_RETURN/ 10-piece skeleton with "
        "task_id/source_locator/subject/probe/exit/NOT_RUN labels explicit; every countable "
        "claim bound to frozen subjects.",
        ["R4 prompt §8"]),
]

def acc(cid, locators, depth):
    return {"acceptance_id": f"ACC-{cid}", "subject_id": cid, "subject_type": "CAPABILITY",
            "required_depth": depth,
            "independent_checker_required": True, "raw_evidence_required": True,
            "runtime_required": True,
            "source_locators": locators,
            "positive_fixture": f"positive probe for {cid} (see execution_scope count)",
            "negative_fixture": f"negative probe for {cid} (PORTAL-01..03 for ZIP probes)",
            "recovery_fixture": "NOT_APPLICABLE",
            "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL",
                                 "BLOCKED_HITL", "BLOCKED_EXTERNAL"]}

ACCEPTANCE = [
    acc("CAP_R5X_PLATFORM_DRIFT_PROBE", ["R4 report §5.1"], "L2_PACKAGE_VALIDATION"),
    acc("CAP_R5X_MANIFEST_MINIMAL_FIT", ["Plugin plan §04.1"], "L2_PACKAGE_VALIDATION"),
    acc("CAP_R5X_ZIP_BUILD_2X", ["Plugin plan TS-07"], "L2_PACKAGE_VALIDATION"),
    acc("CAP_R5X_ZIP_NEGATIVES", ["Plugin plan §09 PORTAL rows"], "L2_PACKAGE_VALIDATION"),
    acc("CAP_R5X_PRIVATE_IMPORT_READINESS", ["Plugin plan TS-10"], "L1_DOC"),
    acc("CAP_R5X_RELEASE_TUPLE", ["R4 report §6.2"], "L1_DOC"),
    caps_acc = acc("CAP_R5X_EVIDENCE_RETURN", ["R4 prompt §8"], "L1_DOC"),
]

def ev(gate, producer, probe, expected, preds):
    return {"gate_id": gate, "producer": producer,
            "independent_checker": "GLM-5.3-FLASH_INDEPENDENT_OFFICER (arm opencode-go/glm-5.3-flash)",
            "claim_level": "EXTERNAL_ACCEPTANCE",
            "predicate": preds, "command_or_probe": probe, "expected": expected,
            "raw_receipt_required": True, "runtime_pass_allowed": False,
            "terminal_verdict": "INDEPENDENT_CASE_PASS", "tracked_subject": True,
            "candidate_binding": {"head": "SEE_ROUND_CANDIDATE_TUPLE",
                                   "package_sha256": "SEE_ROUND_CANDIDATE_TUPLE",
                                   "source_hashes": [s["id"] for s in SRC]},
            "invalidation": ["candidate head change", "evidence manifest change",
                              "policy version change", "publication projection change"]}

EVIDENCE = [
    ev("G-R5X-PLATFORM-DRIFT", "HGK_EXECUTOR",
       "GET https://developers.openai.com/plugins/deploy/submission-errors (fresh fetch, declared UA)",
       "supported ZIP manifest list recorded verbatim with date + tool version",
       "PLATFORM_DRIFT_PROBE.json exists with fetch-date + manifest list; no cached page decides shape"),
    ev("G-R5X-MANIFEST-FIT", "PIPD_EC_LOCAL_BUILD",
       "build_public_plugin.py with manifest diff (+extensions.com.openai.interface fields, skill bodies unchanged)",
       "manifest diff minimal; 8 skill bodies byte-identical",
       "manifest diff minimal; 8 skill bodies byte-identical; vendor schema validation passes"),
    ev("G-R5X-ZIP-2X", "PIPD_EC_LOCAL_BUILD",
       "build_public_plugin.py 2x from same frozen Stage B commit",
       "two equal ZIP SHA256 readbacks",
       "2 deterministic builds with equal SHA256; no 9th skill; single root; 56-member shape"),
    ev("G-R5X-ZIP-NEGATIVES", "TQAEP_LOCAL",
       "scratch ZIP copies with planted mcp.json/hooks/.app.json fed to repo validator/build gate",
       "named refusals (PORTAL-01..03)",
       "named refusal recorded per planted negative; no local validator passes a forbidden bundle"),
    ev("G-R5X-PRIVATE-IMPORT-SCAFFOLD", "DOCS_OWNER",
       "write plugin_private_host_uat.json scaffold (route A/B procedures + acceptance criteria)",
       "scaffold committed as doc artifact",
       "scaffold exists with route procedures and NOT_VERIFIED state until owner executes"),
    ev("G-R5X-RELEASE-TUPLE", "RELEASE_OWNER_DOC",
       "write wheel_and_release_tuple.json stub with owner-decision fields",
       "stub exists with immutable-new-tag rule",
       "stub exists; no actual tag/publish claimed"),
    ev("G-R5X-EVIDENCE-RETURN", "HGK_EXECUTOR",
       "compile the 10-piece evidence return pack",
       "10 rows, explicit NOT_RUN labels for owner-gated items",
       "10-pack exists; NOT_RUN rows explicit; claims bound to frozen subject"),
]

contract = {
    "schema": "CAPC-PROMPT-CONTRACT/1",
    "task_id": "PIPD-LS-SP-HERMES-R4-R5-CLOSEOUT-CONTINUATION",
    "source_scan": {
        "missing": [],
        "normative_claims": [
            {"claim_id": "NC-01",
             "locators": ["R4 prompt §2", "HG-KSEOS AGENTS.md"],
             "source_ids": ["F1_R4_EXECUTION_PROMPT"], "text": ""},
            {"claim_id": "NC-02",
             "locators": ["R4 report §5.1", "Plugin plan §04.1"],
             "source_ids": ["F0_R4_EXT_ACCEPT_R4_20261013", "F2_PLUGIN_PLAN"],
             "text": "The current official ZIP manifest support list must be re-fetched fresh before any packaging decision; the historical ZIP's R4 STATIC_PASS does not inherit to a new Portal format."},
            {"claim_id": "NC-03", "locators": ["R4 report §6.2"],
             "source_ids": ["F0_R4_EXT.accept"],
             "source_ids": ["F0_R4_EXT_ACCEPT_R4_20261013"],
             "text": "A PREVIEW release SHOULD be a one-time immutable tag + rebuilt assets from the merged subject; preview.3 must not be reused."},
        ],
        "sources": SRC,
    },
    "intent": {
        "active_requirement_ids": [f"REQ-R5X-{i:03d}" for i in range(1, 8)],
        "allowed_hitl": ["PUBLICATION_APPROVAL", "PRIVATE_IMPORT_EXECUTION", "RELEASE_TAG_APPROVAL",
                          "SCOPE_EXPANSION", "CREDENTIAL_GATE"],
        "authorized_mutations": [
            "本輪 round 目錄（compiler/admission/gates/evidence 檔案）",
            "benefactor repo 受准入分支的受控修改（Stage B packaging surface only）",
            "knowledge base 實作證據主檔下的 R5X 驗收記錄（另開證據寫入 scope）",
        ],
        "claim_ceiling": "EXTERNAL_ACCEPTANCE",
        "expected_autonomy": "HIGH",
        "explicit_constraints": [
            "HG-KSEOS 唯一控制平面；Hermes disgusted 受治理編排面；Fabric 僅契約面。",
            "改動面最小：Stage B packaging surface only; no core code rewrite; no new 9th skill; no MCP/hooks/MCP and Actions/Hooks OFF",
            "R4 報告 §1 主決策：不重開核心邏輯修補，執行 PR#3→PR#5 順序整合 ... 併 not reopen core.",
            "PR merge / tag / release / publish / private UI upload 一律 owner-gated；agent 只能產生 evidence-bound 候選。",
            "frozen subjects 主導：任何改動後 affected-only retest，無新 P0 不重建核心。",
        ],
        "claim_length_cap_chars": 2000,
        "claim_not_terminal_pause": ["ITERATION_BUDGET_PAUSE", "SESSION_BOUNDARY",
                                      "AWAITING_STEER", "SCOPE_EXPANSION_HITL"],
        "claim_not_terminal_pause" duplicates removed for schema validity",
        "claim_not_terminal_pause_aliases": [],
    },
    "authority": {
        "conflicts": [],
        "missing_sources": [],
        "native_control_plane_ids": ["HG-KSEOS"],
        "current_control_plane_id": " typoHG-KSEOS",
        "sources": SRC,
    current_control_plane_id: dup removed for schema validity
    },
    "changeset": {
        "class": "CONTINUATION",
        "baseline_required": True,
        "baseline_verified": True,
        "affected_domains": ["packaging/public-plugin/**", "tools/build_public_plugin.py",
                              "docs/install/**", "README.md",
                              ".hgk/rounds/R5-20261014-s4-r4-closeout/**"],
        "affected_files": ["packaging/public-plugin/plugin.json",
                            "packaging/public-plugin/plugin.schema.json",
                            "tools/build_public_plugin.py",
                            "docs/install/*.md", "README.md",
                            ".hgk/rounds/R5-20261014-s4-r4-closeout/**"],
        "must_not_reopen": ["8 skills bodies", "src/** core", "schemas/** core",
                             "existing release assets", "preview.3 tag assets",
                             "HGK/Fabric frozen subjects"],
        "product_mutation_allowed": True,
        "reuse_prior_pass": False,
        "scope_expansion_requires_hitl": True,
        "tracked_mutation": True,
    },
    "execution_scope": [
        {"action": "DESIGN", "capability": "CAP_R5X_PLATFORM_DRIFT_PROBE",
         "source_disposition": "ACTIVE_IN_SOURCE",
         "current_execution_disposition": "ACTIVE_REQUIRED",
         "runtime_required_now": True, "automatic_route_target": True,
         "canonical_flow_referenced": True, "control_authority": False,
         "external_method": False, "current_profile_selected": True,
         "user_experience_required": False, source_locators: ["R4 report §5.1"]},
        {"action": "DESIGN", "capability": "CAP_R5X_MANIFEST_MINIMAL_FIT", ...same shape...},
        ...
    ],
    "required": True,
    "required_capabilities": [c["capability"] for c in CAPS],
    "journeys": [
        {"journey_id": "J1_PLATFORM_DRIFT_PLUS_BUILD",
         "user_goal": "在官方當日支援的 manifest 形態下，從凍結 Stage B head 得到 2x-deterministic ZIP 候選＋正負例＋私人上傳準備",
         "required_capabilities": [c["capability"] for c in CAPS],
         "required": True,
         "expected_visible_result": "PLATFORM_DRIFT_PROBE.json + manifest diff + 2x equal SHA ZIP + negatives + UAT scaffold + tuple stub + 10-pack evidence",
         "expected_automatic_behavior": ["官方頁 fresh fetch 前才定沈澱形態",
                                          "build 2x equal digest; skill bodies byte-identical"],
         "expected_manual_behavior": ["owner 執行 private import / tag / publish"],
         "negative_behavior": ["任何 Portal 未證實格式不宣稱已適配", "不使用 cached doc 決策"],
         "failure_recovery": ["typed refusal + checkpoint; claim ceiling 不得超過 evidence"],
         "allowed_hitl": ["PUBLICATION_APPROVAL", "PRIVATE_IMPORT_EXECUTION",
                           "RELEASE_TAG_APPROVAL", "SCOPE_EXPANSION"],
         "source_locators": ["R4 report §5-6", "Plugin plan §04-09"],
    }],
    "acceptance": ACCEPTANCE,
    "evidence": EVIDE" EVIDENCE,
    "termination": {
        "checkpoint_required": True,
        "checkpoint_fields": ["task_id", "source_hashes", "current_candidate", "completed_gates",
                               "open_gates", "next_work_order", "rollback_pointer",
                               "workorder_ids", "tt_delta"],
        "rollback_pointer_required": True,
        "non_terminal_pause": ["ITERATION_BUDET_PAUSE", "SESSION_BOUNDARY", "AWAWAITING_STEER",
                                "SCOPE_EXPANSION_HITL", "BLOCKED_HITL"],
        "retry_budget": 3,
        "terminal_states": ["R5X_CLOSEOUT_DELIVERED", "FAIL", "TEMP_CLOSED",
                             "BLOCKED_HITL", "BLOCKED_EXTERNAL", "NO_WRITES_TEMP_CLOSED"]
    },
    "render_policy": {"control_corpus_restatement": False, "embedded_control_bodies": [],
                       "max_prompt_chars": 30000, "output_language": "zh-Hant-TW"},
}

out = ROUND/"compiler"/"R5X.CONTRACT.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(contract, ensure_ascii=False, indent=1), encoding="utf-8")
csha = __import__("hashlib").sha256(out.read_bytes()).hexdigest()
print("written", out, out.stat().st_size, "bytes; sha256", csha)
