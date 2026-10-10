#!/usr/bin/env python3
"""Generate the R5 S4 user-operability focused-repair prompt contract.

Clones the KEY SET and enum vocabulary of the last PASSING contract
(.hgk/preflight/R4-compiler/R4.CONTRACT.json) and fills R5 content, per
governed-write-admission/references/prompt-contract-compiler-gate.md §3.

Deterministic: same inputs -> byte-identical output.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\PIPD")
OUT_DIR = ROOT / ".hgk" / "preflight" / "R5-compiler"
R4_PATH = ROOT / ".hgk" / "preflight" / "R4-compiler" / "R4.CONTRACT.json"
ATT = Path(r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments")

TASK_ID = "PIPD-LS-SP-HERMES-R5-S4-USER-OPERABILITY-FOCUSED-REPAIR"
CHECKER = "GPT-6.1-SOL_INDEPENDENT_OFFICER"

F0 = "F0_R5_REPAIR_PROMPT"
F1 = "F1_R4_EXTERNAL_CHALLENGE"
F2 = "F2_R4_EVIDENCE_MASTER"
F3 = "F3_PIPD_UPSTREAM"
F4 = "F4_R4_PUBLIC_CANDIDATE"
F5 = "F5_HGK_CONTROL_PLANE"
F6 = "F6_FABRIC_CONTRACT"
F7 = "F7_LOCAL_REPO_TRUTH"
FAMILIES = [F0, F1, F2, F3, F4, F5, F6, F7]

R5_PROMPT = ATT / "PIPD-LS-SP_HERMES_R5_S4_USER_USABILITY_FOCUSED_REPAIR_PROMPT_2026-10-09.md"
R4_REPORT = ATT / "PIPD_LS_SP_R4_S4_User_Usability_PostRepair_External_Acceptance_2026-10-09.md"
R4_EVIDENCE = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\實作證據\PIPD-LS-SP_R4_FOCUSED_REPAIR_EVIDENCE_2026-10-09.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cap(name, disp, action, runtime_now, locators, external=False):
    return {
        "capability": name,
        "source_disposition": "ACTIVE_IN_SOURCE",
        "current_execution_disposition": disp,
        "current_profile_selected": disp in ("ACTIVE_REQUIRED", "ACTIVE_SELECTED"),
        "canonical_flow_referenced": True,
        "automatic_route_target": True,
        "user_experience_required": True,
        "runtime_required_now": runtime_now,
        "action": action,
        "source_locators": locators,
        "external_method": external,
        "control_authority": False,
    }


def readiness(name, work, acc_ids, verdict="NOT_READY"):
    stages = ["identify", "pin", "install_materialize", "configure", "discover", "bind",
              "route", "effective_load", "doctor_health", "positive_pilot", "negative_security",
              "fallback", "rollback_uninstall", "independent_qualification", "certify", "enable"]
    return {
        "capability": name,
        "required_now": True,
        "lifecycle": {s: ("DONE" if verdict == "RUNTIME_READY" else "OPEN") for s in stages},
        "current_verdict": verdict,
        "work_required": work,
        "acceptance_ids": acc_ids,
    }


def acc(subject_id, subject_type, depth, runtime_required, locators):
    return {
        "acceptance_id": "ACC-" + subject_id,
        "subject_id": subject_id,
        "subject_type": subject_type,
        "source_locators": locators,
        "runtime_required": runtime_required,
        "required_depth": depth,
        "positive_fixture": f"positive fixture for {subject_id}",
        "negative_fixture": f"negative/mutation fixture for {subject_id}",
        "recovery_fixture": f"recovery fixture for {subject_id}",
        "raw_evidence_required": True,
        "independent_checker_required": True,
        "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL",
                            "BLOCKED_HITL", "BLOCKED_EXTERNAL"],
    }


def gate(gate_id, predicate, expected, probe, producer, claim, runtime_pass_allowed=False,
         rerun="full"):
    return {
        "gate_id": gate_id,
        "predicate": predicate,
        "expected": expected,
        "command_or_probe": probe,
        "raw_receipt_required": True,
        "producer": producer,
        "independent_checker": CHECKER,
        "candidate_binding": {
            "head": "SEE_ROUND_CANDIDATE_TUPLE",
            "package_sha256": "SEE_ROUND_CANDIDATE_TUPLE",
            "source_hashes": FAMILIES,
        },
        "tracked_subject": True,
        "rerun_rule": rerun,
        "invalidation": [
            "candidate head change",
            "evidence manifest change",
            "policy version change",
            "publication projection change",
        ],
        "terminal_verdict": "INDEPENDENT_CASE_PASS",
        "runtime_pass_allowed": runtime_pass_allowed,
        "claim_level": claim,
    }


def build() -> dict:
    r4 = json.loads(R4_PATH.read_text(encoding="utf-8"))

    # -------- sources -------------------------------------------------
    src = [
        (F0, str(R5_PROMPT), sha256(R5_PROMPT), "NORMATIVE", "R0",
         str(R5_PROMPT) + " | §0 machine header, §3 write authority, §6 WO-S4-* and UAT-00..12, §9 terminal output"),
        (F1, str(R4_REPORT), sha256(R4_REPORT), "NORMATIVE", "R0",
         str(R4_REPORT) + " | §0 verdict FAIL_CHALLENGE, §3 F-R4-S4-01..04, §4 UAT-00..12, §5 P0/P1 CP rulings, §6 WO table"),
        (F2, str(R4_EVIDENCE), sha256(R4_EVIDENCE), "STATE_EVIDENCE", "R1",
         str(R4_EVIDENCE) + " | R4 round evidence master (historical state, not an oracle)"),
        (F3, r"C:/Projects/Agent_Workspace/知識庫", "UNAVAILABLE", "NORMATIVE", "R0",
         r"C:/Projects/Agent_Workspace/知識庫 | PIPD-LS-SP_藍圖 §2/§5.9.3/§19.1-19.2/§26; PIPD_LS_canonical_standard §0.1/§6.3; PKG-00..10"),
        (F4, "https://github.com/shw097-team/PIPD-LS-SP@cd8a06e4c066a40398a4012b7b3908ac11408a2b",
         "REMOTE_UNPINNED", "STATE_EVIDENCE", "R1",
         "https://github.com/shw097-team/PIPD-LS-SP@cd8a06e4c066a40398a4012b7b3908ac11408a2b (tree a640e656d3c01c7d142695e4dc3e4314efd062df) | external challenge subject; no local git object exists for this commit in " + str(ROOT)),
        (F5, r"C:/Projects/Agent_Workspace/HG-KSEOS", "UNAVAILABLE", "NORMATIVE", "R0",
         r"C:/Projects/Agent_Workspace/HG-KSEOS | AGENTS.md, SharedSpine, ProjectLifecycleController, WorkOrder/ExecutionBinding, doctor"),
        (F6, r"C:/Projects/Agent_Workspace/Fabric", "UNAVAILABLE", "NORMATIVE", "R0",
         r"C:/Projects/Agent_Workspace/Fabric | contract surface only; no second control plane"),
        (F7, "C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2",
         "UNAVAILABLE", "STATE_EVIDENCE", "R0",
         "C:/Projects/Agent_Workspace/PIPD@7c5bc585c7d889cd338da853be4efc4b8f07d3b2 | local HEAD, branch master, unpublished R4 work in the working tree, no git remote configured"),
    ]
    reviewed = [{"source_family": f, "source_id": f, "locator": loc, "sha256": sh,
                 "role": role, "critical": True} for f, loc, sh, role, _rank, _det in src]
    authority_sources = [{"id": f, "rank": rank, "path": loc.split(" | ")[0], "sha256": sh,
                          "locator": loc, "role": role, "governs": True}
                         for f, loc, sh, role, rank, _det in src]

    normative_claims = [
        {"claim_id": "NC-01",
         "text": "HG-KSEOS is the sole WorkOrder admission / reducer / gate control plane; Hermes is the governed orchestration plane and Fabric only the contract surface.",
         "source_ids": [F5, F6], "locators": ["R5 prompt §0 execution subjects", "HG-KSEOS/AGENTS.md"]},
        {"claim_id": "NC-02",
         "text": "pipd project --out must refuse any unsafe destination BEFORE creating, deleting or replacing anything; today projection.project_surfaces rmtree()s the target with no safety check.",
         "source_ids": [F1, F0], "locators": ["R4 report §3 F-R4-S4-01", "R5 prompt §6 WO-S4-DEST-001",
                                              "src/pipd_ls_sp/projection.py L1045-L1057"]},
        {"claim_id": "NC-03",
         "text": "The shipped dist wheel is the R2 artefact and is not equivalent to the R4/R5 source; the 19 schemas and the current modules must resolve from installed package resources, not from the repo root.",
         "source_ids": [F1, F0], "locators": ["R4 report §0 P0 S4-USER-DIST-002", "R5 prompt §6 WO-S4-DIST-002",
                                              "dist/WHEEL_MANIFEST.json", "src/pipd_ls_sp/registry.py L23-L50"]},
        {"claim_id": "NC-04",
         "text": "pipd export --out must deliver a real archive + manifest + checksums at the requested destination, and --dry-run must write nothing; silently ignoring args.out is a contract violation.",
         "source_ids": [F1, F0], "locators": ["R4 report §0 P1 S4-USER-EXPORT-003", "R5 prompt §6 WO-S4-EXPORT-003",
                                              "src/pipd_ls_sp/cli.py L172-L179"]},
        {"claim_id": "NC-05",
         "text": "No writer may run without an OS/container-enforced write scope; when isolation cannot be provided the round stops the writer, keeps the analysis read-only and closes as NO_WRITES/TEMP_CLOSED.",
         "source_ids": [F0], "locators": ["R5 prompt §3 write authority", "R5 prompt §4 FORBIDDEN", "R5 prompt §6 WO-S4-UAT-004"]},
        {"claim_id": "NC-06",
         "text": "The S2 performance gate currently FAILs (343547 bytes against a 20000 budget); it must not be turned green by raising the threshold, deleting requirements or widening scope.",
         "source_ids": [F1, F0], "locators": ["R4 report §0 S2 context budget FAIL", "R5 prompt §6 WO-S2-PERF-005"]},
        {"claim_id": "NC-07",
         "text": "Maker and checker are different identities and claim ceilings do not inherit: local verification is not independent acceptance, and publication is not release.",
         "source_ids": [F1, F0], "locators": ["R5 prompt §3 claim ceiling", "R5 prompt §8 independent AO", "R4 report §9"]},
        {"claim_id": "NC-08",
         "text": "The externally reviewed public subject (GitHub r4-candidate cd8a06e) and the local candidate are different subjects; a new publication projection must be re-bound by fresh readback and no R3/R4 attestation may be inherited.",
         "source_ids": [F1, F0, F4, F7], "locators": ["R4 report §2 identity table", "R5 prompt §6 WO-R4-PUBLISH-006", "R5 prompt §8"]},
    ]

    # -------- intent --------------------------------------------------
    reqs = ["REQ-PIPD-R5-DEST-001", "REQ-PIPD-R5-DIST-002", "REQ-PIPD-R5-EXPORT-003",
            "REQ-PIPD-R5-UAT-004", "REQ-PIPD-R5-PERF-005", "REQ-PIPD-R5-PUBLISH-006",
            "REQ-PIPD-R5-ORCH-007"]
    delivery = ["PROMPT_COMPILER_READBACK", "HGK_ADMISSION_READBACK", "R5_S4_FINDING_LEDGER",
                "R5_S4_UAT_MATRIX", "DISTRIBUTION_AND_PUBLICATION_TUPLE", "R5_S4_EVIDENCE_MASTER_MD"]
    intent = {
        "goal": "在 PIPD 上執行 R5 S4 一般使用者可用性定向修補：處置 R4 外部挑戰報告的 F-R4-S4-01..04 / F-R4-S2-05 / F-R4-PUB-06 / F-R4-HARNESS-07 / F-R4-TRACE-08 / F-R4-GOV-09 / F-R4-RELEASE-10，先修安全的 pipd project --out、與 R5 source 等價的可安裝 wheel、真正落地的 pipd export --out，再於隔離工作區跑 UAT-00..12 正反例與 replay。",
        "user_expected_outcome": "一般使用者不需知道內部 Skill/WorkOrder/Provider 名稱即可完成 Intent -> RequirementAtom -> Profile -> PI -> PD -> ConstructionContract -> ECP/TQAEP -> validate -> Web/Host projections -> portable export，且 pipd 永不因任意 --out 毀損工作樹、永不以舊 wheel 當現行安裝件；未閉合項以 typed blocker 或 owner gate 誠實回報，不宣稱 10/10 PASS。",
        "user_expected_experience": "13 個 CLI 子命令的成功/拒絕/副作用皆有 typed 輸出與可重算雜湊；危險目的地一律 typed UNSAFE_DESTINATION 且 exit != 0；fresh venv 安裝後 19 schemas 實際可載；export --dry-run 零寫入。",
        "explicit_constraints": [
            "HG-KSEOS 為唯一控制平面；Hermes 為受治理編排面；Fabric 僅契約面。",
            "NARROW_REPAIR：保留 19 schemas／8 skills／5 web／3 host mock／13 CLI／3 GP／clause-bound PI/PD 主幹，不得全域重寫，不推進 S5～S8。",
            "任何 writer 必須具 OS/container 強制 write scope；做不到則 NO_WRITES/TEMP_CLOSED。",
            "禁止 danger-full-access 或其他僅憑 PROMPT 聲明限制的無隔離 writer。",
            "不得改驗收閾值湊 PASS、不得刪 requirement、不得改測試成永遠真；S2 perf FAIL 不得抹去。",
            "危險 destination 反例只在 disposable scratch/mock workspace 執行，嚴禁對含重要資料的真目錄執行。",
            "claim 互不繼承：CODE_CHANGED / SCHEMA_VALID / TEST_EXECUTED / FIXTURE_MOCK_QUALIFIED / LOCAL_QUALIFIED / INDEPENDENT_PASS / HUMAN_RATIFIED / PUBLICATION_APPROVED / RELEASED / PRODUCTION_VERIFIED。",
            "PAT 只在必要時由 credentialed handler 使用，明文不得進入 argv／日誌／commit／manifest／聊天。",
        ],
        "non_goals": [
            "重寫 19 schemas／8 Skills／5 Web／3 Host／13 CLI 的既有可行核心。",
            "實作 S5 receiver live、S6 GENIE、S7 JIT、S8 SGM promotion、PRE-W3。",
            "修滿 22 個未 active 技術的 source pins 或清洗 153/160 全域 knowledge。",
            "自動批准 license／release／publication 或關閉任何 owner gate。",
            "force-push、改寫已發布歷史、以 R3/R4 舊 seal 重新標籤新 commit。",
        ],
        "authorized_mutations": [
            "PIPD 產品樹的最小必要修補（src/pipd_ls_sp、tools、tests、schemas、dist、pyproject.toml、fixtures）。",
            "PIPD .hgk 證據樹（preflight 契約/收據、rounds、admission、lane raw logs）。",
            "知識庫 實作相關DOC/PIPD/實作證據 下的 R5 驗收主檔（另開證據寫入 scope）。",
        ],
        "forbidden_mutations": [
            "HG-KSEOS／Fabric 封存控制面（未另取 owner WorkOrder 前不得修改）。",
            "已發布的歷史 commit（不得改寫、不得 force-push）。",
            "PRE-W3 跨專案 frozen subject。",
            "任何 OS 層不可強制的 writer 執行。",
            "任何含明文憑證的檔案、commit、manifest、日誌或輸出。",
        ],
        "expected_autonomy": "HIGH",
        "allowed_hitl": ["LICENSE_DECISION", "PUBLICATION_APPROVAL", "PERF_THRESHOLD_RATIFICATION",
                         "ORACLE_POLARITY", "SCOPE_EXPANSION", "PRE_W3_OWNER", "CREDENTIAL_GATE"],
        "requested_delivery": delivery,
        "active_requirement_ids": reqs,
        "claim_ceiling": "EXTERNAL_ACCEPTANCE",
    }

    # -------- execution scope ----------------------------------------
    loc_dest = ["R5 prompt §6 WO-S4-DEST-001", "R4 report §3 F-R4-S4-01"]
    loc_dist = ["R5 prompt §6 WO-S4-DIST-002", "R4 report §3 F-R4-S4-02"]
    loc_exp = ["R5 prompt §6 WO-S4-EXPORT-003", "R4 report §3 F-R4-S4-03"]
    loc_uat = ["R5 prompt §6 WO-S4-UAT-004", "R4 report §4.1 UAT-00..12"]
    loc_ws = ["R5 prompt §3 write authority", "R5 prompt §6 WO-S4-UAT-004"]
    loc_perf = ["R5 prompt §6 WO-S2-PERF-005", "R4 report §3 F-R4-S2-05"]
    loc_pub = ["R5 prompt §6 WO-R4-PUBLISH-006", "R4 report §3 F-R4-PUB-06"]
    loc_orch = ["R5 prompt §6 WO-HGK-ORCH-007", "R4 report §3 F-R4-HARNESS-07"]

    scope = [
        cap("CAP_R5_PROJECT_DEST_SAFETY", "ACTIVE_REQUIRED", "DESIGN", True, loc_dest),
        cap("CAP_R5_WHEEL_EQUIVALENCE", "ACTIVE_REQUIRED", "INSTALL", True, loc_dist),
        cap("CAP_R5_EXPORT_EFFECT", "ACTIVE_REQUIRED", "DESIGN", True, loc_exp),
        cap("CAP_R5_FRESH_USER_UAT", "ACTIVE_REQUIRED", "QUALIFY", True, loc_uat),
        cap("CAP_R5_WRITESET_ENFORCEMENT", "ACTIVE_REQUIRED", "USE_NATIVE", True, loc_ws),
        cap("CAP_R5_PERF_PROVENANCE", "ACTIVE_REQUIRED", "DESIGN", False, loc_perf),
        cap("CAP_R5_PUBLICATION_TUPLE", "ACTIVE_REQUIRED", "DESIGN", False, loc_pub),
        cap("CAP_R5_NATIVE_ORCH_PATH", "ACTIVE_SELECTED", "QUALIFY", False, loc_orch),
        cap("CAP_R5_OWNER_LICENSE_GATE", "ACTIVE_REQUIRED", "DESIGN", False,
            ["R5 prompt §3 non-goals", "R4 report §5 P3-12"]),
    ]
    reuse_map = {
        "CAP_S0_CONTRACT_SCHEMAS_19": "CAP_R5_SCHEMAS_19",
        "CAP_SKILL_CONTRACTS_8": "CAP_R5_SKILLS_8",
        "CAP_WEB_PACK_5": "CAP_R5_WEB_5",
        "CAP_HOST_PROJECTION_MOCK_3": "CAP_R5_HOST_3",
        "CAP_CLI_13": "CAP_R5_CLI_13_USERPATH",
        "CAP_GOLDEN_PILOTS_3": "CAP_R5_GOLDEN_PILOTS_3",
        "CAP_TECH_DISPOSITIONS_22": "CAP_R5_TECH_DISPOSITIONS_22",
        "CAP_ROLLBACK_DRILL": "CAP_R5_ROLLBACK_DRILL",
        "CAP_PRE_W3_SEPARATE": "CAP_R5_PRE_W3_SEPARATE",
    }
    for old, new in reuse_map.items():
        row = next(r for r in r4["execution_scope"] if r["capability"] == old)
        row = json.loads(json.dumps(row))
        row["capability"] = new
        scope.append(row)

    # -------- runtime readiness --------------------------------------
    readiness_rows = [
        readiness("CAP_R5_PROJECT_DEST_SAFETY",
                  ["WO-S4-DEST-001: 統一 OutputDestination Resolver，拒絕早於任何 create/delete/replace；staging + atomic publish；dry-run 零副作用"],
                  ["ACC-CAP_R5_PROJECT_DEST_SAFETY"]),
        readiness("CAP_R5_WHEEL_EQUIVALENCE",
                  ["WO-S4-DIST-002: 由 frozen candidate 重建 deterministic wheel，含 requirements/repo_context/projection 與 19 schemas 資源；install-safe resource lookup"],
                  ["ACC-CAP_R5_WHEEL_EQUIVALENCE"]),
        readiness("CAP_R5_EXPORT_EFFECT",
                  ["WO-S4-EXPORT-003: export --out 實體落檔 archive+manifest+checksums；--dry-run 零寫入；secret-scan FAIL 零 artifact"],
                  ["ACC-CAP_R5_EXPORT_EFFECT"]),
        readiness("CAP_R5_FRESH_USER_UAT",
                  ["WO-S4-UAT-004: 以新 wheel 與 source import 分別跑 UAT-00..12，紀錄 raw stdout/exit/canary hash/replay"],
                  ["ACC-CAP_R5_FRESH_USER_UAT"]),
        readiness("CAP_R5_WRITESET_ENFORCEMENT",
                  ["container lane (pipd-r4-writer) 負例矩陣：admitted 成功、outside-root/unmounted/symlink 拒絕、secret 不存在、egress DROP"],
                  ["ACC-CAP_R5_WRITESET_ENFORCEMENT"]),
    ]

    # -------- journeys -----------------------------------------------
    journeys = [
        {
            "journey_id": "J1_FRESH_INSTALL_TO_VALIDATE",
            "required": True,
            "user_goal": "從乾淨 venv 安裝 R5 wheel 後，pipd doctor/validate 能載入 19 schemas 並正確拒絕壞 bundle",
            "expected_visible_result": "pipd 指向 site-packages 安裝；19/19 schema 可定位；empty/wrong-owner/orphan trace 為 typed FAIL",
            "expected_automatic_behavior": ["安裝後不依賴 Repo 頂層 schemas 或 PYTHONPATH", "舊 R2 wheel / 缺 schema 被診斷拒絕"],
            "expected_manual_behavior": ["使用者只提供 venv 與 wheel 路徑"],
            "allowed_hitl": ["LICENSE_DECISION"],
            "required_capabilities": ["CAP_R5_WHEEL_EQUIVALENCE", "CAP_R5_SCHEMAS_19", "CAP_R5_CLI_13_USERPATH"],
            "negative_behavior": ["stale wheel 不得產生 phantom PASS", "缺資源不得靜默回退 source checkout"],
            "failure_recovery": ["typed DIST_RESOURCE_MISSING 並保留 checkpoint"],
            "source_expectation_ids": ["REQ-PIPD-R5-DIST-002"],
            "source_locators": ["R5 prompt §6 UAT-00/UAT-04/UAT-10", "R4 report §4.1 UAT-00"],
        },
        {
            "journey_id": "J2_PROJECT_SAFE_WRITE",
            "required": True,
            "user_goal": "以 pipd project 產生 5 Web + 3 Host + IR，且任何危險 --out 都被拒絕且不觸碰工作樹",
            "expected_visible_result": "正常 scratch 目的地 5/5、3/3、IR 寫入且 hash 可重算；危險目的地 typed UNSAFE_DESTINATION exit != 0 且 canary 不變",
            "expected_automatic_behavior": ["安全檢查先於任何 create/delete/replace", "dry-run 只做計畫與安全判定"],
            "expected_manual_behavior": ["使用者指定 dedicated scratch 目錄"],
            "allowed_hitl": ["SCOPE_EXPANSION"],
            "required_capabilities": ["CAP_R5_PROJECT_DEST_SAFETY", "CAP_R5_WEB_5", "CAP_R5_HOST_3"],
            "negative_behavior": ["--out . / .. / repo root / home / source ancestor / symlink escape 一律拒絕", "既有非空輸出預設拒絕"],
            "failure_recovery": ["拒絕後工作樹 before/after canary hash 完全相同"],
            "source_expectation_ids": ["REQ-PIPD-R5-DEST-001"],
            "source_locators": ["R5 prompt §6 UAT-05/UAT-06/UAT-12", "R5 prompt §4.2"],
        },
        {
            "journey_id": "J3_PORTABLE_EXPORT",
            "required": True,
            "user_goal": "pipd export --out 產出可獨立解包的 portable 交付（archive+manifest+checksums）",
            "expected_visible_result": "指定路徑出現 archive 與 manifest；外部可解包並重算 sha256；dry-run 無任何檔案",
            "expected_automatic_behavior": ["先 staging 後原子落地", "secret/PII 掃描失敗則零 artifact"],
            "expected_manual_behavior": ["使用者指定輸出目錄"],
            "allowed_hitl": ["SCOPE_EXPANSION"],
            "required_capabilities": ["CAP_R5_EXPORT_EFFECT", "CAP_R5_PROJECT_DEST_SAFETY"],
            "negative_behavior": ["secret-scan FAIL 或非法路徑 -> 0 artifact + typed nonzero", "不得 silent ignore --out"],
            "failure_recovery": ["typed EXPORT_NO_EFFECT 不得出現；失敗保留 checkpoint"],
            "source_expectation_ids": ["REQ-PIPD-R5-EXPORT-003"],
            "source_locators": ["R5 prompt §6 UAT-07", "R4 report §0 P1"],
        },
        {
            "journey_id": "J4_FULL_S4_CHAIN",
            "required": True,
            "user_goal": "同一 frozen source 完成 intake -> compile-pi -> bind-pd -> compile-ecp/tqaep -> validate 全鏈，並在兩個 fresh process 重播一致",
            "expected_visible_result": "clause-bound RequirementAtom、profile 行為、PD currentness、TQAEP maker!=checker 皆 typed；兩次 replay 正規化 hash 相同",
            "expected_automatic_behavior": ["無來源之規範宣稱被拒絕", "source/version 變更使舊證據失效"],
            "expected_manual_behavior": ["使用者提供來源句與目標 root"],
            "allowed_hitl": ["ORACLE_POLARITY", "PERF_THRESHOLD_RATIFICATION"],
            "required_capabilities": ["CAP_R5_CLI_13_USERPATH", "CAP_R5_SKILLS_8", "CAP_R5_GOLDEN_PILOTS_3"],
            "negative_behavior": ["unbound/no-source 需求必須拒絕", "maker 自簽 checker 不接受"],
            "failure_recovery": ["typed error 並保留 replay 收據"],
            "source_expectation_ids": ["REQ-PIPD-R5-UAT-004", "REQ-PIPD-R5-PERF-005"],
            "source_locators": ["R5 prompt §6 UAT-01/UAT-02/UAT-03/UAT-08/UAT-09/UAT-11", "R4 report §4"],
        },
    ]

    # -------- acceptance ---------------------------------------------
    acceptance = []
    for row in scope:
        name = row["capability"]
        runtime = row["runtime_required_now"]
        depth = "L3_INTEGRATION_RUNTIME" if runtime else "L2_UNIT_BEHAVIOR"
        acceptance.append(acc(name, "CAPABILITY", depth, runtime,
                              row["source_locators"]))
    req_depth = {
        "REQ-PIPD-R5-DEST-001": ("L3_INTEGRATION_RUNTIME", True),
        "REQ-PIPD-R5-DIST-002": ("L3_INTEGRATION_RUNTIME", True),
        "REQ-PIPD-R5-EXPORT-003": ("L3_INTEGRATION_RUNTIME", True),
        "REQ-PIPD-R5-UAT-004": ("L3_INTEGRATION_RUNTIME", True),
        "REQ-PIPD-R5-PERF-005": ("L2_UNIT_BEHAVIOR", False),
        "REQ-PIPD-R5-PUBLISH-006": ("L2_UNIT_BEHAVIOR", False),
        "REQ-PIPD-R5-ORCH-007": ("L2_UNIT_BEHAVIOR", False),
    }
    for rid in reqs:
        depth, runtime = req_depth[rid]
        acceptance.append(acc(rid, "REQUIREMENT", depth, runtime,
                              ["R5 prompt §6 WO table", "R5 prompt §9 terminal output"]))
    for d in delivery:
        acceptance.append(acc(d, "DELIVERABLE", "L2_UNIT_BEHAVIOR", False,
                              ["R5 prompt §9 final output"]))
    for j in journeys:
        acceptance.append(acc(j["journey_id"], "JOURNEY", "L3_INTEGRATION_RUNTIME", True,
                              j["source_locators"]))

    # -------- evidence gates -----------------------------------------
    g = []
    g.append(gate("G-R5-PROMPT-COMPILE", "native compiler receipts present",
                  "lint/activation/acceptance/compile/duplication all 0 error",
                  "python scripts/prompt_contract_compiler.py lint|activation|acceptance|compile <contract>",
                  "HGK_EXECUTOR", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-PROJECT-DEST-SAFETY",
                  "unsafe --out is refused before any create/delete/replace",
                  "all dangerous destinations typed UNSAFE_DESTINATION exit!=0 and canary unchanged",
                  "pidp project negative matrix in a disposable scratch fixture",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-WHEEL-EQUIVALENCE",
                  "installed wheel carries the current modules and the 19 schemas",
                  "fresh venv, non-repo cwd, no PYTHONPATH: 19/19 schemas load",
                  "pip install dist/*.whl in a fresh venv; pipd doctor; python -c registry",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-EXPORT-EFFECT",
                  "export --out writes a real verifiable bundle and dry-run writes nothing",
                  "archive+manifest+checksums present, sha256 recomputable, dry-run zero files",
                  "pipd export --out <scratch> and pipd export --dry-run in a scratch fixture",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-UAT-00-12", "the 13 end-user UAT cases are executed with raw evidence",
                  "each case has positive + negative + side-effect snapshot; no skips",
                  "python tools/run_r5_uat.py --all --raw",
                  "HGK_EXECUTOR", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-WRITESET-ENFORCEMENT",
                  "writer cannot write outside the admitted WriteSet",
                  "outside-root / unmounted / symlink / secret / egress all refused",
                  "container lane negative matrix in the same invocation as the positive probe",
                  "HGK_EXECUTOR", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-CLI-13", "the 13 CLI subcommands keep their functional matrix",
                  "13/13 with at least one business-logic case each",
                  "python -m unittest discover -s tests and the CLI functional matrix",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-SECRETS", "no secret in worktree or history",
                  "0 hits in both scans",
                  "python tools/history_secret_scan.py",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-PERF-BUDGET",
                  "context budget is either provenance-ratified or an honest FAIL",
                  "343547/20000 remains FAIL unless an owner-ratified oracle exists",
                  "python tools/perf_budget.py --check",
                  "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-SCHEMAS-19", "19 machine contracts field-exact", "19/19",
                  "python -m unittest tests.test_registry_reconcile", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-SKILLS-8", "8 skill packs discover/load/route", "8/8 packs",
                  "python -m unittest tests.test_skill_packs", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-WEB-5", "exactly five PIPD web documents", "5/5",
                  "python -m unittest tests.test_web_pack", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-HOST-3", "3 host projection mocks effective-load", "3/3 FIXTURE_MOCK",
                  "python -m unittest tests.test_host_projection", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-SPEC-DEL-CROSSWALK", "57-row crosswalk keeps the original baseline plus the affected delta",
                  "42 EVIDENCED / 11 EVIDENCE_GAP / 4 DESIGN_ONLY with an R5 delta section",
                  "python tools/build_spec_del_crosswalk.py --check", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-PUBLICATION-TUPLE",
                  "publication projection is re-bound to a fresh readback",
                  "commit/tree/product digest present; no R3/R4 seal inherited",
                  "python tools/build_publication_manifest.py --check", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-KNOWLEDGE-READY",
                  "an S4-required knowledge source missing from the index blocks the feature",
                  "blocking gap surfaced as a typed gate, not silently ignored",
                  "python tools/quarantine_review.py --report", "PIPD_EC", "EXTERNAL_ACCEPTANCE"))
    g.append(gate("G-R5-INDEPENDENT-CHALLENGE",
                  "a non-maker officer re-runs the frozen candidate",
                  "all denominators re-run with raw evidence on the same frozen tuple",
                  "independent officer lane on the frozen candidate", "HGK_EXECUTOR",
                  "EXTERNAL_ACCEPTANCE"))

    contract = {
        "schema": "CAPC-PROMPT-CONTRACT/1",
        "task_id": TASK_ID,
        "source_scan": {
            "required_source_families": FAMILIES,
            "reviewed": reviewed,
            "missing": [],
            "normative_claims": normative_claims,
        },
        "intent": intent,
        "authority": {
            "sources": authority_sources,
            "conflicts": [],
            "missing_sources": [],
            "native_control_plane_ids": ["HG-KSEOS"],
            "current_control_plane_id": "HG-KSEOS",
        },
        "changeset": {
            "class": "NARROW_REPAIR",
            "baseline_required": True,
            "baseline_verified": True,
            "reuse_prior_pass": False,
            "affected_domains": ["src/pipd_ls_sp", "tools", "tests", "dist", "schemas", ".hgk", "pyproject.toml"],
            "affected_files": ["src/pipd_ls_sp/*", "tools/*", "tests/*", "dist/*",
                               ".hgk/preflight/R5-*/*", ".hgk/rounds/R5-*/*"],
            "must_not_reopen": [
                "19 schema 結構（TechnologyAdmission required 14/14、closed object）",
                "8 個 SkillContract 與 5 份 Web MD 分母",
                "13 CLI 名稱與 3 Golden Pilot fixture",
                "clause-bound RequirementAtom / negation / compound 既有行為",
                "已發布的 GitHub 歷史與 R3/R4 attestation",
                "HG-KSEOS／Fabric 封存控制面與 PRE-W3 跨專案 frozen subject",
            ],
            "scope_expansion_requires_hitl": True,
            "tracked_mutation": True,
            "product_mutation_allowed": True,
        },
        "execution_scope": scope,
        "runtime_readiness": readiness_rows,
        "journeys": journeys,
        "acceptance": acceptance,
        "evidence": g,
        "termination": {
            "terminal_states": ["R5_S4_USER_OPERABILITY_DELIVERED", "FAIL", "TEMP_CLOSED_PRE_W3",
                                "BLOCKED_HITL", "BLOCKED_EXTERNAL", "NO_WRITES_TEMP_CLOSED"],
            "non_terminal_pause": ["ITERATION_BUDGET_PAUSE", "SESSION_BOUNDARY", "AWAITING_STEER",
                                   "SCOPE_EXPANSION_HITL"],
            "checkpoint_required": True,
            "checkpoint_fields": ["task_id", "source_hashes", "current_candidate", "completed_gates",
                                  "open_gates", "next_work_order", "rollback_pointer",
                                  "workorder_ids", "tt_delta"],
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
    return contract


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = build()
    text = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    target = OUT_DIR / "R5.CONTRACT.json"
    target.write_text(text, encoding="utf-8", newline="")
    print("wrote", target, len(text.encode("utf-8")), "bytes")
    print("sha256", hashlib.sha256(target.read_bytes()).hexdigest())
    print("caps", len(payload["execution_scope"]), "readiness", len(payload["runtime_readiness"]),
          "journeys", len(payload["journeys"]), "acceptance", len(payload["acceptance"]),
          "gates", len(payload["evidence"]))
