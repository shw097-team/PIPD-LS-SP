#!/usr/bin/env python3
"""Build the R5Q (Owner Open Source Preview) CAPC contract.

Clone the R5P contract's SHAPE (key sets / enums) and fill this round's content. The validator is
never edited: the contract is the only thing that changes between iterations.

Contract id: PIPD-LS-SP-R5Q-OWNER-OPENSOURCE-PREVIEW-20261010
Oracle sources: the R5P owner-preview execution prompt + the CORRECTED owner GO report.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PIPD = Path(r"C:\Projects\Agent_Workspace\PIPD")
BASE = PIPD / ".hgk" / "rounds" / "R5P-20261010-s4-post-challenge" / "compiler" / "R5P.CONTRACT.json"
KB = Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD")
EXEC_PROMPT = KB / "PROMPT" / "PIPD-LS-SP_HERMES_R5P_OWNER_OPENSOURCE_PREVIEW_EXECUTION_PROMPT_2026-10-10.md"
OWNER_GO = KB / "驗收報告" / "PIPD_LS_SP_R5P_S0-S4_External_Challenge_CORRECTED_OWNER_OpenSource_Preview_GO_2026-10-10.md"
EVIDENCE_MASTER = KB / "實作證據" / "PIPD-LS-SP_R5_POST_CHALLENGE_S4_EXTERNAL_EVIDENCE.md"

TASK_ID = "PIPD-LS-SP-R5Q-OWNER-OPENSOURCE-PREVIEW-20261010"

REQS = [
    ("REQ-PIPD-R5Q-LIC-001", "WO-R5Q-LICENSE-001", "OWNER+LICENSE-FAR",
     "The owner's open-source grant lands as Apache-2.0 across LICENSE, OWNER_LICENSE_DECISION.yaml, "
     "NOTICE, pyproject.toml license metadata, SBOM.cdx.json and PROVENANCE.md, keeping the "
     "corpus-derived vs agent-authored split and asserting no right the owner does not hold."),
    ("REQ-PIPD-R5Q-PKG-002", "WO-R5Q-REBUILD-002", "PIPD-EC",
     "Rebuild the distribution from the frozen release candidate so the shipped artifact carries the "
     "granted SPDX metadata; recompute the wheel sha256, the manifest build_input_commit/released_commit "
     "fields and SHA256SUMS, and do not reuse the superseded bb070a6f identity."),
    ("REQ-PIPD-R5Q-UAT-003", "WO-R5Q-UAT-003", "PIPD-EC",
     "Clean-venv UAT with no PYTHONPATH and outside the repository, run against the ACTUAL released wheel "
     "bytes: doctor positive plus missing-schema typed negative, 19-schema readback, the "
     "intake/compile-pi/bind-pd/compile-ecp/compile-tqaep design chain, validate, project --dry-run with zero "
     "writes, project --out to disposable scratch (5 Web + 3 Host + IR) and export --out with recomputed "
     "archive/manifest/SHA256SUMS."),
    ("REQ-PIPD-R5Q-CRED-004", "WO-R5Q-CREDENTIAL-004", "CREDENTIAL-BROKER",
     "The owner PAT is read only inside process memory from the credential file, used for a minimum-scope "
     "auth probe against shw097-team/PIPD-LS-SP, and never emitted to argv, stdout, logs, prompt, evidence, "
     "git config or any release asset."),
    ("REQ-PIPD-R5Q-PUB-005", "WO-R5Q-GITHUB-005", "RELEASE-OWNER",
     "Publish an immutable tag and a GitHub prerelease bound to the explicit release commit with the "
     "source archive, the wheel and SHA256SUMS, after proving the tag does not already exist."),
    ("REQ-PIPD-R5Q-AO-006", "WO-R5Q-AO-006", "EXTERNAL-VERIFY-LANE",
     "An independent non-Maker checker in a separate process, read-only, re-derives the POST-release "
     "subject from the published bytes: download hash match, clean install, doctor and design chain, "
     "license coverage; the Maker cannot sign its own final verdict."),
    ("REQ-PIPD-R5Q-DOC-007", "WO-R5Q-DOC-007", "DOCS-OWNER",
     "README first screen, Preview Notes and Known Limitations point at the preview tag rather than the "
     "historical R3 main, and disclose DEL-018 exit 1 with its three uncovered test paths, the 12 TT "
     "dispositions, CORR-01..08 and the 28/10/19 SPEC/DEL denominator."),
]

CAPS = [
    ("CAP_R5Q_OWNER_LICENSE_GRANT", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P2", "R5P prompt 8.1 CORR-01", "OWNER_LICENSE_DECISION.yaml E1-E4",
      "R5P owner GO 7.2"],
     "one owner grant that makes LICENSE / SPDX / NOTICE / SBOM / provenance agree on the same identifier"),
    ("CAP_R5Q_RELEASE_CANDIDATE_FREEZE", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P3", "R5P prompt 5 baseline", "R5P prompt 8.1 CORR-07"],
     "an immutable release candidate commit that is NOT the review commit, with build_input/released identity split"),
    ("CAP_R5Q_WHEEL_REBUILD_MANIFEST", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P3", "dist/WHEEL_MANIFEST.json", "tools/build_dist.py"],
     "the shipped wheel carries the granted license metadata and a recomputed hash that is not the old one"),
    ("CAP_R5Q_CLEAN_INSTALL_UAT", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P3", "uat/out2/UAT_MATRIX.json", "R5P owner GO 4"],
     "the ACTUAL released wheel bytes pass an ordinary-user install and command chain outside the repo"),
    ("CAP_R5Q_CREDENTIAL_BROKER", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P5 credential paragraph", "R5P prompt 4 FORBIDDEN"],
     "the token is used in memory only; no secret reaches argv, stdout, logs, evidence or any public asset"),
    ("CAP_R5Q_GITHUB_PRERELEASE", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P5", "R5P prompt 8.2 TT-R5P-14"],
     "a new immutable tag resolves to the explicit release commit and the release is marked prerelease"),
    ("CAP_R5Q_RELEASE_READBACK", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P5 readback clause", "R5P prompt 8.2 TT-R5P-09", "R5P prompt 8.2 TT-R5P-02"],
     "an independent readback of repo/tag/commit/tree/release/assets and asset download hashes"),
    ("CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P6", "R5P prompt 8 CORR-03"],
     "a non-Maker checker issues a bounded preview receipt; no FULL independent PASS is manufactured"),
    ("CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE", "ACTIVE_REQUIRED",
     ["R5P prompt 6 P4", "R5P prompt 8.1 CORR-02", "R5P prompt 8.1 CORR-04",
      "R5P prompt 8.1 CORR-06", "R5P prompt 8.2 TT-R5P-01/02/03/06/08/12/13"],
     "the public notes name DEL-018, the 12 TT disposition rows and the 28/10/19 denominator without washing them to CLOSED"),
    ("CAP_R5Q_SURFACE_ENABLEMENT", "ACTIVE_SELECTED",
     ["owner mandate: KANBAN/SWARM/GSTACK/OPENSPEC + CODEX CLI multi-subagent",
      "R5P contract requested_delivery", "PIPD/openspec/changes"],
     "the round's governance surfaces really exist and read back (board graph, route readback, open spec change)"),
    ("CAP_R5Q_EVIDENCE_PACK", "ACTIVE_REQUIRED",
     ["R5P prompt 8 evidence_return_pack", "R5P prompt 9 final output"],
     "one machine-readable pack plus one human-readable master under the private evidence root, token-free"),
    ("CAP_R5Q_DEL018_GAP_HONEST", "DEFERRED_SOURCE_BACKED",
     ["R5P prompt 6 P4 DEL-018 clause", "R5P prompt 8.1 CORR-02"],
     "build_publication_manifest.py --check --current stays exit 1 and is disclosed, not repaired as an excuse to expand scope"),
    ("CAP_R5Q_S5_S8_SEAMS", "DEFERRED_SOURCE_BACKED",
     ["R5P prompt 4 DEFERRED", "R5P prompt 8.1 CORR-05", "R5P prompt 8.1 CORR-08"],
     "S5-S8/live-host/pre-W3 obligations stay deferred with their typed design seams intact"),
]

JOURNEYS = [
    ("J1_OWNER_GRANT_LANDING", "CAP_R5Q_OWNER_LICENSE_GRANT",
     "The owner's grant is recorded once and every license surface in the tree and the wheel agrees with it.",
     ["one decision record names the identifier and the scope",
      "the build reads the same identifier from LICENSE, metadata and SBOM"],
     ["a release asset whose license text disagrees with LICENSE is not publishable"],
     ["the reader only opens LICENSE, OWNER_LICENSE_DECISION.yaml, NOTICE, pyproject.toml and the wheel METADATA"],
     ["all five surfaces carry the same SPDX identifier and the scope split is stated"],
     ["historical non-grant receipts stay byte-identical; the old decision is not back-dated"]),
    ("J2_CLEAN_INSTALL_USER_PATH", "CAP_R5Q_CLEAN_INSTALL_UAT",
     "An ordinary user in a clean venv outside the repository installs the published wheel and runs the "
     "documented chain without touching the source checkout.",
     ["doctor reports the packaged schema set as healthy",
      "the design-only chain compiles PI, PD, ECP and TQAEP",
      "project --dry-run writes nothing"],
     ["a wheel missing a packaged schema must typed-FAIL non-zero",
      "unsafe --out targets must be refused before any delete"],
     ["the user supplies only a venv, the wheel path and a disposable scratch directory"],
     ["per-command stdout/stderr/exit plus artifact hashes, mode labelled SOURCE or INSTALLED"],
     ["a command that cannot run is recorded NOT_RUN with a named reason, never a silent PASS"]),
    ("J3_PREVIEW_DOWNLOAD", "CAP_R5Q_RELEASE_READBACK",
     "A third party downloads the preview assets from the release page and verifies them against the "
     "published checksums.",
     ["the tag resolves to the release commit that the notes name",
      "the published wheel and source archive hashes match SHA256SUMS"],
     ["a tag that already existed is never moved or force-pushed"],
     ["the reader uses only the public repository and the release page"],
     ["asset names, sizes and sha256 are listed next to the checksum file contents"],
     ["if the network or the API refuses, the half-published state and its resume step are recorded"]),
    ("J4_KNOWN_LIMITATIONS", "CAP_R5Q_KNOWN_LIMITATIONS_DISCLOSURE",
     "A reader of the release notes can tell exactly what is not claimed by this preview.",
     ["DEL-018 is disclosed as an open release-manifest gap with its uncovered test paths",
      "the 12 TT rows keep their owner and trigger"],
     ["the notes must not claim a full gate pass or a production verification"],
     ["the reader reads only the release page and README first screen"],
     ["the notes name the deferred stages and the un-certified host surface"],
     ["no gap is relabelled CLOSED to make the release look complete"]),
    ("J5_INDEPENDENT_PREVIEW_VERIFY", "CAP_R5Q_INDEPENDENT_PREVIEW_VERIFY",
     "A checker that did not author the release reproduces the decisive claims from the published bytes.",
     ["the checker re-derives the download hashes and the install smoke itself"],
     ["the checker is refused if it is the Maker or shares the Maker's identity"],
     ["the checker gets only read-only access and the published subject"],
     ["the verdict names what it re-derived and what it could not"],
     ["a receipt string must never be upgraded to an independent full pass"]),
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def dir_digest(root: Path, cap: int = 200000) -> str:
    """Deterministic structural fingerprint of a directory source (path+size per file).

    Content-hashing a multi-GB knowledge root is neither fast nor useful as a locator; the
    contract only needs a stable, re-derivable identity for the source family.
    """
    h = hashlib.sha256()
    n = 0
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            h.update(f"{rel}\t{p.stat().st_size}\n".encode("utf-8"))
            n += 1
            if n >= cap:
                break
    h.update(f"#files={n}\n".encode("utf-8"))
    return h.hexdigest()


def commit_object_sha256(repo: Path, rev: str) -> str:
    """sha256 over the frozen git commit object of a source repo."""
    import subprocess
    cp = subprocess.run(["git", "-C", str(repo), "cat-file", "commit", rev],
                        capture_output=True)
    return hashlib.sha256(cp.stdout).hexdigest()


def build() -> dict:
    d = json.loads(BASE.read_text(encoding="utf-8"))
    d["schema"] = "CAPC-PROMPT-CONTRACT/1"
    d["task_id"] = TASK_ID

    new_sources = [
        {"governs": True, "id": "F0_R5Q_EXEC_PROMPT", "locator": str(EXEC_PROMPT), "path": str(EXEC_PROMPT),
         "rank": "R0", "role": "NORMATIVE", "sha256": sha(EXEC_PROMPT)},
        {"governs": True, "id": "F1_R5Q_OWNER_GO", "locator": str(OWNER_GO), "path": str(OWNER_GO),
         "rank": "R0", "role": "NORMATIVE", "sha256": sha(OWNER_GO)},
        {"governs": True, "id": "F2_R5Q_EVIDENCE_MASTER", "locator": str(EVIDENCE_MASTER),
         "path": str(EVIDENCE_MASTER), "rank": "R1", "role": "STATE_EVIDENCE",
         "sha256": sha(EVIDENCE_MASTER) if EVIDENCE_MASTER.is_file() else "MISSING"},
        {"governs": True, "id": "F3_PIPD_UPSTREAM", "locator": r"C:/Projects/Agent_Workspace/知識庫",
         "path": r"C:/Projects/Agent_Workspace/知識庫", "rank": "R0", "role": "NORMATIVE",
         "sha256": dir_digest(Path(r"C:/Projects/Agent_Workspace/知識庫"))},
        {"governs": True, "id": "F4_R5Q_PUBLIC_CANDIDATE",
         "locator": "https://github.com/shw097-team/PIPD-LS-SP@2efc84eac8e1939092c748d5b389b6dd72267aef",
         "path": "https://github.com/shw097-team/PIPD-LS-SP@2efc84eac8e1939092c748d5b389b6dd72267aef",
         "rank": "R1", "role": "STATE_EVIDENCE",
         "sha256": commit_object_sha256(PIPD, "2efc84eac8e1939092c748d5b389b6dd72267aef")},
        {"governs": True, "id": "F5_HGK_CONTROL_PLANE", "locator": r"C:/Projects/Agent_Workspace/HG-KSEOS",
         "path": r"C:/Projects/Agent_Workspace/HG-KSEOS", "rank": "R0", "role": "NORMATIVE",
         "sha256": dir_digest(Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/src"))},
        {"governs": True, "id": "F6_FABRIC_CONTRACT", "locator": r"C:/Projects/Agent_Workspace/Fabric",
         "path": r"C:/Projects/Agent_Workspace/Fabric", "rank": "R0", "role": "NORMATIVE",
         "sha256": dir_digest(Path(r"C:/Projects/Agent_Workspace/Fabric/contracts"))},
        {"governs": True, "id": "F7_LOCAL_REPO_TRUTH",
         "locator": r"C:/Projects/Agent_Workspace/PIPD@2efc84eac8e1939092c748d5b389b6dd72267aef",
         "path": r"C:/Projects/Agent_Workspace/PIPD@2efc84eac8e1939092c748d5b389b6dd72267aef",
         "rank": "R0", "role": "STATE_EVIDENCE",
         "sha256": commit_object_sha256(PIPD, "2efc84eac8e1939092c748d5b389b6dd72267aef")},
    ]
    d["authority"]["sources"] = new_sources
    d["source_scan"]["reviewed"] = [
        {"critical": s["role"] == "NORMATIVE", "locator": s["locator"], "role": s["role"],
         "sha256": s["sha256"], "source_family": s["id"], "source_id": s["id"]} for s in new_sources]
    d["source_scan"]["required_source_families"] = [s["id"] for s in new_sources]
    d["source_scan"]["missing"] = []
    d["source_scan"]["normative_claims"] = [
        {"claim_id": "NC-01",
         "locators": ["R5Q prompt 0 machine header", "R5Q prompt 2 authority", "HG-KSEOS/AGENTS.md"],
         "source_ids": ["F0_R5Q_EXEC_PROMPT", "F5_HGK_CONTROL_PLANE", "F6_FABRIC_CONTRACT"],
         "text": "HG-KSEOS is the sole control plane; the canonical Hermes binding is its governed "
                 "runtime/orchestration plane and Fabric is a governance contract surface only. Native "
                 "compiler PASS and a real HGK admission must precede any effectful product write."},
        {"claim_id": "NC-02",
         "locators": ["R5Q prompt 3 claim ceiling", "R5Q owner GO 0", "R5Q owner GO 13"],
         "source_ids": ["F0_R5Q_EXEC_PROMPT", "F1_R5Q_OWNER_GO"],
         "text": "The technical preview GO is already established (GO_WITH_DISCLOSED_LIMITATIONS); the "
                 "remainder of the round is a bounded release, not a new repair wave. The ceiling is "
                 "OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED and never a full gate or production claim."},
        {"claim_id": "NC-03",
         "locators": ["R5Q owner GO 0.1 CORR-01", "R5Q prompt 8.1 CORR-01"],
         "source_ids": ["F1_R5Q_OWNER_GO", "F0_R5Q_EXEC_PROMPT"],
         "text": "A missing license grant is an owner waiting state, not an S4 engineering defect: the "
                 "previous round's negative attribution is withdrawn, and the grant is an owner decision "
                 "that must be recorded before any artifact is called open source."},
        {"claim_id": "NC-04",
         "locators": ["R5Q owner GO 5.1", "R5Q prompt 6 P4", "R5Q prompt 8.1 CORR-02"],
         "source_ids": ["F1_R5Q_OWNER_GO", "F0_R5Q_EXEC_PROMPT"],
         "text": "tools/build_publication_manifest.py --check --current exits 1 for DEL-018 "
                 "RELEASE_MANIFEST@1 and the uncovered paths are tests/test_git_object_reader.py, "
                 "tests/test_doctor_schema_truth.py and tests/test_tqaep_design_positive.py. The failure "
                 "stays FAIL and is disclosed; it does not by itself block the owner's limited preview."},
        {"claim_id": "NC-05",
         "locators": ["R5Q prompt 5 C3", "R5Q prompt 8.1 CORR-07", "dist/WHEEL_MANIFEST.json"],
         "source_ids": ["F0_R5Q_EXEC_PROMPT", "F4_R5Q_PUBLIC_CANDIDATE"],
         "text": "The reviewed candidate is r5p-post-challenge-repair 2efc84e / tree e254ea2 with wheel "
                 "sha256 bb070a6f, while main is still the R3 commit 3aebbbc and the manifest's "
                 "candidate_head 7c5bc585 is an older build identity. A license change produces a NEW "
                 "release commit and a NEW wheel hash; the old hash must not be inherited."},
        {"claim_id": "NC-06",
         "locators": ["R5Q prompt 4 FORBIDDEN", "R5Q prompt 6 P5 credential paragraph"],
         "source_ids": ["F0_R5Q_EXEC_PROMPT"],
         "text": "The owner PAT may be read only in process memory for minimum-scope operations; writing "
                 "its value to argv, stdout, logs, prompts, URLs, git config, manifests or any public or "
                 "private evidence is forbidden, and Fabric may supply policy but must not become a second "
                 "secret reader."},
        {"claim_id": "NC-07",
         "locators": ["R5Q prompt 8.2 TT-R5P-*", "R5Q prompt 8.1 CORR-03/04/05/06/08"],
         "source_ids": ["F0_R5Q_EXEC_PROMPT", "F1_R5Q_OWNER_GO"],
         "text": "The 12 named TT rows and CORR-01..08 each need a current-truth disposition with owner and "
                 "trigger; the SPEC/DEL denominator stays 28 evidenced / 10 active gaps / 19 deferred and no "
                 "row may be mass-relabelled CLOSED because the preview was authorised."},
    ]

    d["intent"].update({
        "goal": "Execute the owner-authorised S4 open-source preview release of PIPD-LS-SP: land the "
                "owner's Apache-2.0 grant across every license surface, freeze a new immutable release "
                "candidate, rebuild and verify the distribution, publish a GitHub prerelease bound to the "
                "explicit commit, read it back externally, obtain an independent non-Maker preview verdict "
                "and return one evidence pack that keeps DEL-018 and the deferred stages honestly open.",
        "non_goals": [
            "不啟動 R6 大修、不刷新全部 57 個 SPEC/DEL 成 PASS、不修好 22 個未啟用外部技術。",
            "不部署 HGK live S5、GENIE S6、JIT S7、SWOF/SGM S8、PRE-W3。",
            "不覆寫 main、不 force-push、不修改或移動既有 tag。",
            "不建立第二個 Repo、不建立第二套 norm authority。",
            "不把 DEL-018 的 exit 1 抹成 PASS，也不為此擴張成新工單。",
            "不以 Maker 自簽取代獨立驗收，不宣稱 G_RELEASE_FULL_PASS 或 PRODUCTION_VERIFIED。",
        ],
        "user_expected_outcome": "一般使用者能在明確的 Preview tag 取得合法授權涵蓋的 source 與可核對 "
                                 "Wheel，在乾淨 venv 依說明安裝，執行 doctor 與 intake→PI→PD→ECP/TQAEP 設計鏈，"
                                 "安全地 project --dry-run／scratch --out 與 export，並清楚知道版本、限制與回報方式。",
        "user_expected_experience": "使用者只需要 Preview tag、wheel/source 檔案、SHA256 與 Python/jsonschema "
                                    "版本；不需要知道 WorkOrder、ExecutionBinding 或 provider 識別。",
        "active_requirement_ids": [r[0] for r in REQS],
        "requested_delivery": ["PROMPT_COMPILER_READBACK", "HGK_ADMISSION_READBACK",
                               "OWNER_PREVIEW_DECISION_PACKET", "R5Q_LICENSE_DECISION_FAR",
                               "R5Q_RELEASE_CANDIDATE_TUPLE", "R5Q_DISTRIBUTION_TUPLE",
                               "R5Q_CLEAN_INSTALL_UAT_MATRIX", "R5Q_GITHUB_PRERELEASE_READBACK",
                               "R5Q_INDEPENDENT_AO_VERDICT", "R5Q_EVIDENCE_PACK",
                               "R5Q_EVIDENCE_MASTER_MD", "R5Q_KANBAN_SWARM_RECEIPT",
                               "R5Q_GSTACK_ROUTE_READBACK", "R5Q_OPENSPEC_CHANGE"],
        "authorized_mutations": [
            "PIPD 產品樹發布相關最小差異：LICENSE、OWNER_LICENSE_DECISION.yaml、NOTICE（新增）、"
            "pyproject.toml、SBOM.cdx.json、PROVENANCE.md、README.md、ACCEPTANCE.md 之授權／版本／限制段落。",
            "PIPD dist/ 重建產物：wheel、*.sha256、SHA256SUMS、WHEEL_MANIFEST.json、source archive。",
            "PIPD .hgk 證據樹：rounds/R5Q-*（preflight、compiler、admission、license、release、uat、ao、evidence）、"
            "kanban、gstack、openspec 變更。",
            "PIPD openspec/changes 下本輪 change。",
            "知識庫 實作相關DOC/PIPD/實作證據 下本輪驗收主檔與 FAR 記錄（不含 Token）。",
            "GitHub shw097-team/PIPD-LS-SP：新增 release 分支/tag 與 prerelease（不得覆寫 main 或既有 tag）。",
        ],
        "forbidden_mutations": [
            "不得讀出 PAT 明文，或把 PAT 寫進 repo URL／logs／stdout／prompt／Manifest／evidence／commit。",
            "不得覆寫 main、force-push 或修改既有 tag。",
            "不得在真 repo/home/cwd/來源祖先執行危險 --out 負例或刪除性試驗。",
            "不得把 corpus/donor 材料自動改用 OSI 授權或宣稱擁有其權利。",
            "不得 Maker 自簽 Independent／Release／Production PASS，或直接改 HGK/Fabric controls 以繞過 Gate。",
            "不得以 Fabric/Hermes 自建第二 norm authority。",
        ],
        "explicit_constraints": [
            "CONTINUATION：只做 affected-only 的發布／文件／封裝修正，不重做 19 Schema／8 Skills／13 CLI。",
            "原生 Prompt Compiler 必須真正執行；FAIL 或 bundle 缺失即 PROMPT_COMPILE_BLOCKED，只准唯讀預檢。",
            "claim 互不繼承：LOCAL_TESTED ≠ INDEPENDENT_ACCEPTED ≠ RELEASED ≠ PRODUCTION_VERIFIED。",
            "新產品二進位不可沿用 bb070a6f 舊 hash；manifest 必須區分 build_input_commit 與 released_commit。",
            "12 TT 與 CORR-01..08 逐一保留 current/closure/deferred、owner、原始證據或限制、重新觸發條件。",
            "DEL-018 維持 FAIL/EVIDENCE_GAP 並在 Preview Notes 明示。",
        ],
        "claim_ceiling": "EXTERNAL_ACCEPTANCE",
        "expected_autonomy": "HIGH",
        "allowed_hitl": ["LICENSE_DECISION", "PUBLICATION_APPROVAL", "CREDENTIAL_GATE",
                         "PERF_THRESHOLD_RATIFICATION", "ORACLE_POLARITY", "SCOPE_EXPANSION"],
    })

    d["changeset"].update({
        "class": "CONTINUATION",
        "baseline_required": True,
        "baseline_verified": True,
        "product_mutation_allowed": True,
        "reuse_prior_pass": True,
        "tracked_mutation": True,
        "scope_expansion_requires_hitl": True,
        "affected_domains": ["LICENSE", "OWNER_LICENSE_DECISION.yaml", "NOTICE", "pyproject.toml",
                             "SBOM.cdx.json", "PROVENANCE.md", "README.md", "ACCEPTANCE.md", "dist", ".hgk"],
        "affected_files": ["LICENSE", "OWNER_LICENSE_DECISION.yaml", "NOTICE", "pyproject.toml", "SBOM.cdx.json",
                           "PROVENANCE.md", "README.md", "ACCEPTANCE.md", "dist/*", ".hgk/**",
                           "openspec/changes/pipd-ls-sp-r5q-owner-opensource-preview/*"],
        "must_not_reopen": [
            "19 schema 結構與 registry exact set",
            "8 個 SkillContract 與 5 份 Web MD 分母",
            "13 CLI 名稱與 3 Golden Pilot fixture",
            "R5 已修的 project --out 安全 resolver 與 export --out 實體輸出",
            "R5P 已修的 doctor schema truth 與 TQAEP design positive",
            "已發布的 GitHub 歷史、既有 tag 與 R3/R4/R5/R5P attestation",
            "HG-KSEOS／Fabric 封存控制面",
        ],
    })

    scope = []
    for cap, disp, locs, _desc in CAPS:
        active = disp.startswith("ACTIVE")
        selected = disp == "ACTIVE_REQUIRED"
        scope.append({
            "action": "QUALIFY" if active else "DESIGN",
            "automatic_route_target": active,
            "canonical_flow_referenced": active,
            "capability": cap,
            "control_authority": False,
            "current_execution_disposition": disp,
            "current_profile_selected": selected,
            "external_method": False,
            "runtime_required_now": selected,
            "source_disposition": "ACTIVE_IN_SOURCE" if active else "SOURCE_BACKED_DEFERRED",
            "source_locators": locs,
            "user_experience_required": selected,
        })
    d["execution_scope"] = scope

    LIFECYCLE = ("bind", "certify", "configure", "discover", "doctor_health", "effective_load", "enable",
                 "fallback", "identify", "independent_qualification", "install_materialize",
                 "negative_security", "pin", "positive_pilot", "rollback_uninstall", "route")
    readiness = []
    for i, (cap, disp, _l, desc) in enumerate(CAPS):
        req_ids = [REQS[i][0]] if i < len(REQS) else []
        readiness.append({
            "acceptance_ids": [f"ACC-{cap}"] + [f"ACC-{rid}" for rid in req_ids],
            "capability": cap,
            "current_verdict": "NOT_READY",
            "lifecycle": {k: "OPEN" for k in LIFECYCLE},
            "required_now": disp == "ACTIVE_REQUIRED",
            "work_required": [f"{REQS[i][1]}: {desc}"] if i < len(REQS) else [desc],
        })
    d["runtime_readiness"] = readiness

    journeys = []
    for jid, cap, goal, auto, neg, manual, visible, recovery in JOURNEYS:
        row = {
            "allowed_hitl": ["LICENSE_DECISION", "PUBLICATION_APPROVAL", "CREDENTIAL_GATE"],
            "expected_automatic_behavior": auto,
            "expected_manual_behavior": manual,
            "expected_visible_result": "; ".join(visible) if isinstance(visible, list) else visible,
            "failure_recovery": recovery,
            "journey_id": jid,
            "negative_behavior": neg,
            "required": True,
            "required_capabilities": [cap],
            "source_expectation_ids": [],
            "source_locators": ["R5Q prompt 6 P1-P6", "R5Q owner GO 13"],
            "user_goal": goal,
        }
        for i, (c, _d, _l, _desc) in enumerate(CAPS[:len(REQS)]):
            if c == cap:
                row["source_expectation_ids"].append(REQS[i][0])
        if jid == "J4_KNOWN_LIMITATIONS":
            row["source_expectation_ids"].append("REQ-PIPD-R5Q-DOC-007")
        if jid == "J5_INDEPENDENT_PREVIEW_VERIFY":
            row["source_expectation_ids"].append("REQ-PIPD-R5Q-AO-006")
        journeys.append(row)
    d["journeys"] = journeys

    def acc(subject_id, subject_type, depth, locators):
        return {"acceptance_id": f"ACC-{subject_id}", "independent_checker_required": True,
                "negative_fixture": f"negative/mutation fixture for {subject_id}",
                "positive_fixture": f"positive fixture for {subject_id}",
                "raw_evidence_required": True,
                "recovery_fixture": f"recovery fixture for {subject_id}",
                "required_depth": depth, "runtime_required": subject_type in ("CAPABILITY", "JOURNEY"),
                "source_locators": locators, "subject_id": subject_id, "subject_type": subject_type,
                "terminal_states": ["INDEPENDENT_CASE_PASS", "INDEPENDENT_CASE_FAIL", "BLOCKED_HITL",
                                    "BLOCKED_EXTERNAL"]}

    accs = []
    for cap, disp, locs, _d in CAPS:
        active = disp.startswith("ACTIVE")
        row = acc(cap, "CAPABILITY", "L3_INTEGRATION_RUNTIME" if active else "L2_UNIT_BEHAVIOR", locs)
        row["runtime_required"] = active
        accs.append(row)
    for rid, wo, owner, _w in REQS:
        accs.append(acc(rid, "REQUIREMENT", "L3_INTEGRATION_RUNTIME", [f"R5Q prompt 6 {wo}"]))
    for jid, _cap, _g, _a, _n, _m, _v, _r in JOURNEYS:
        accs.append(acc(jid, "JOURNEY", "L3_INTEGRATION_RUNTIME", ["R5Q prompt 6 P1-P6"]))
    for did in d["intent"]["requested_delivery"]:
        accs.append(acc(did, "DELIVERABLE", "L1_SCHEMA_CONTRACT", ["R5Q prompt 8 evidence_return_pack"]))
    d["acceptance"] = accs

    base = {"claim_level": "EXTERNAL_ACCEPTANCE",
            "candidate_binding": {"head": "SEE_ROUND_CANDIDATE_TUPLE",
                                  "package_sha256": "SEE_ROUND_CANDIDATE_TUPLE",
                                  "source_hashes": [s["id"] for s in new_sources]},
            "independent_checker": "GPT-6.1-SOL_MEDIUM_OPENAI_OAUTH_INDEPENDENT_OFFICER",
            "invalidation": ["release candidate head change", "wheel bytes change", "license document change",
                             "evidence manifest change", "publication projection change"],
            "producer": "CODEX_BOUNDED_WRITER_DEEPSEEK-V4.1-FLASH", "raw_receipt_required": True,
            "rerun_rule": "affected-only", "runtime_pass_allowed": False,
            "terminal_verdict": "INDEPENDENT_CASE_PASS", "tracked_subject": True}

    gates = [
        ("G-R5Q-PROMPT-COMPILE",
         "python scripts/prompt_contract_compiler.py lint|activation|acceptance|compile <R5Q contract>",
         "native compiler receipts all report verdict PROMPT_COMPILE_PASS", "NATIVE_COMPILER_PASS"),
        ("G-R5Q-HGK-ADMISSION",
         "hg_kseos typed lifecycle admit_requirement + checkpoint on PIPD-LS-SP-20261008",
         "every R5Q requirement reaches FROZEN with a TaskSpec/WorkOrder, no raw SQL", "TYPED_LIFECYCLE"),
        ("G-R5Q-LICENSE-LANDING",
         "diff LICENSE / OWNER_LICENSE_DECISION.yaml / NOTICE / pyproject.toml / SBOM.cdx.json / PROVENANCE.md",
         "one SPDX identifier agrees across every surface and the scope split is stated", "LICENSE_METADATA_CONSISTENCY"),
        ("G-R5Q-WHEEL-REBUILD",
         "tools/build_dist.py rebuild + wheel METADATA + sha256 + WHEEL_MANIFEST + SHA256SUMS",
         "the shipped wheel carries the granted license and a hash that is NOT bb070a6f", "ARTIFACT_IDENTITY"),
        ("G-R5Q-CLEAN-INSTALL-UAT",
         "clean venv, no PYTHONPATH, outside repo, against the actual released wheel bytes",
         "doctor positive + typed negative, 19 schemas, design chain, dry-run zero-write, scratch out",
         "UAT_MATRIX"),
        ("G-R5Q-CREDENTIAL-BROKER",
         "minimum-scope auth probe from process memory + secret scan of the whole evidence set",
         "no token value in argv, stdout, logs, evidence, prompt, git config or any asset", "SECRET_HYGIENE"),
        ("G-R5Q-GITHUB-PRERELEASE",
         "GitHub API: create tag + prerelease bound to the explicit release commit",
         "the tag resolves to the release commit and prerelease=true", "RELEASE_BINDING"),
        ("G-R5Q-RELEASE-READBACK",
         "independent readback of repo/tag/commit/tree/release/assets + asset download hash",
         "download hashes match SHA256SUMS from a source that never used the local release cache",
         "EXTERNAL_READBACK"),
        ("G-R5Q-INDEPENDENT-AO",
         "independent non-Maker checker lane on the POST-release subject, read-only",
         "a bounded preview verdict with its own re-derivation, or PARTIAL/NOT_RUN named",
         "INDEPENDENT_VERDICT"),
        ("G-R5Q-DOCS-LIMITATIONS",
         "README first screen + Preview Notes + Known Limitations vs ACCEPTANCE.md",
         "entry points at the preview tag; DEL-018, the 12 TT, CORR-01..08 and 28/10/19 disclosed",
         "DOCS_CONSISTENCY"),
        ("G-R5Q-SURFACE-EVIDENCE",
         "kanban/SWARM board readback + GSTACK route readback + openspec change artifacts",
         "the board graph, the route readback and the change artifacts exist and read back", "SURFACE_EVIDENCE"),
        ("G-R5Q-EVIDENCE-PACK",
         "evidence_return_pack machine manifest + human master under the private evidence root",
         "pack is complete and token-free; DEL-018 stays FAIL", "EVIDENCE_PACK"),
    ]
    ev = []
    for gid, probe, expected, pred in gates:
        row = dict(base)
        row.update({"gate_id": gid, "command_or_probe": probe, "expected": expected, "predicate": pred})
        ev.append(row)
    d["evidence"] = ev

    d["termination"].update({
        "terminal_states": ["OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED",
                            "PREVIEW_TECHNICAL_GO_OWNER_DECISION_PENDING", "RELEASE_POLICY_BLOCKED",
                            "STOP_SHIP", "BLOCKED_CREDENTIAL", "BLOCKED_HITL", "FAIL"],
        "non_terminal_pause": ["ITERATION_BUDGET_PAUSE", "SESSION_BOUNDARY", "AWAITING_STEER",
                               "SCOPE_EXPANSION_HITL"],
        "retry_budget": 3,
        "rollback_pointer_required": True,
    })
    d["render_policy"] = {"control_corpus_restatement": False, "embedded_control_bodies": [],
                          "max_prompt_chars": 30000, "output_language": "zh-Hant-TW"}
    return d


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "R5Q.CONTRACT.json")
    c = build()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print("wrote", out, len(json.dumps(c)))
