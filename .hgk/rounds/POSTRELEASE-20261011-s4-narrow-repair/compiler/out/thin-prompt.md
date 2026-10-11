# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-S4-POSTRELEASE-NARROW-REPAIR-20261011
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Execute one minimal post-release maintenance round on the published S4 open-source MVP: repair the README checksum/onboarding defect, ship one versioned ChatGPT/Web mount package, close the identity-type and profile fail-closed contract gaps, and land a pinned normative source map with a replayable minimal self-bootstrap example - without moving the immutable tag.
Expected outcome: A first-time user copy-pastes the README from a clean directory and every line exits 0 on both bash and PowerShell; a Web consumer can mount one ZIP and get sourced candidate answers; malformed identity/trace/profile inputs are refused by exact first-fail type checks; the repository states where its normative sources live without creating a second SSOT.
ChangeSet: NARROW_REPAIR
Affected domains: README.md, schemas, src/pipd_ls_sp, tests, dist, docs, examples, .hgk

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4_POSTRELEASE_MINIMAL_REPAIR_PROMPT_2026-10-11.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4_POSTRELEASE_MINIMAL_REPAIR_PROMPT_2026-10-11.md role=NORMATIVE
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_S4_MVP_OpenSource_PostRelease_Independent_Challenge_Acceptance_2026-10-11.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_S4_MVP_OpenSource_PostRelease_Independent_Challenge_Acceptance_2026-10-11.md role=NORMATIVE
- R0 https://github.com/shw097-team/PIPD-LS-SP@8faa64e581e8c25f5ec355475e29561847da3ead https://github.com/shw097-team/PIPD-LS-SP@8faa64e581e8c25f5ec355475e29561847da3ead role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD role=NORMATIVE
- R1 https://github.com/shw097-team/PIPD-LS-SP@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7 https://github.com/shw097-team/PIPD-LS-SP@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7 role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/Fabric C:/Projects/Agent_Workspace/Fabric role=NORMATIVE
- R1 C:/Projects/Agent_Workspace/PIPD-postrelease-wt C:/Projects/Agent_Workspace/PIPD-postrelease-wt@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7 role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: The user only needs a shell, Python >= 3.11 and a ZIP upload; they never need to know WorkOrder, Skill or provider identifiers.
Constraints:
- NARROW_REPAIR: keep the 19 schema families, 8 logical skills, 13 CLI commands, 5 web / 3 host projections and the clause-bound PI/PD trunk intact.
- The native prompt compiler must actually run; a failure or a missing bundle means PROMPT_COMPILE_BLOCKED with read-only preflight only.
- The sealed EXECUTE lane bounds the writer by write scope, not by prose.
- Claims do not inherit: LOCAL_TESTED != INDEPENDENT_ACCEPTED != RELEASED.
- Publication of a new tag or release asset stays an owner gate.
Non-goals:
- No rewrite of the 11 PKG or 10 DOC documents; no second authority stack, reducer, plan IR or scheduler.
- No S5 HGK live receiver, S6 GENIE, S7 JIT, S8 SWOF promotion, PRE-W3 or the 22 inactive external technologies.
- No tag move, no force-push, no overwrite of published release bytes.
- No new 20th schema family, no 9th logical skill, no 14th CLI command, no MCP server or resident daemon.
- No rewrite of historical FAIL receipts or previous independent attestations.
Authorized mutations:
- Minimal product-tree repair inside C:/Projects/Agent_Workspace/PIPD-postrelease-wt: README.md, schemas/*.schema.json identity/trace properties, src/pipd_ls_sp/profiles.py, src/pipd_ls_sp/pipeline.py, src/pipd_ls_sp/validate.py, new tests, dist/ mount package and MANIFEST, docs/NORMATIVE_SOURCE_MAP.md, examples/self-bootstrap/.
- The round evidence tree .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/.
- The single acceptance master document under 知識庫 實作相關DOC/PIPD/實作證據/.
Forbidden mutations:
- No second normative authority built from Hermes or Fabric; no self-signed INDEPENDENT_PASS.
- No destructive test against the real repository, home directory or source ancestors.
- No PAT in plaintext in any prompt, log, argv, URL, commit or .git/config.
- No widening of the gate denominator to cancel a recorded FAIL.
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_S4POST_QUICKSTART_VERIFY: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4POST_WEB_MOUNT_PACK: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4POST_IDENTITY_TYPE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4POST_PROFILE_FAILCLOSED: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4POST_REGRESSION_EXACT_SETS: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4POST_SOURCE_MAP: ACTIVE_SELECTED; action=DESIGN; runtime_required=false
- CAP_S4POST_SELFBOOT_REPLAY: ACTIVE_SELECTED; action=DESIGN; runtime_required=true
- CAP_S4POST_VERSION_IDENTITY: ACTIVE_SELECTED; action=DESIGN; runtime_required=false
Non-active:
- CAP_S4POST_INDEPENDENT_BUNDLE: DEFERRED_SOURCE_BACKED; action=DESIGN
- CAP_S4POST_S5_S8_RUNTIME: NOT_APPLICABLE_SOURCE_BACKED; action=DESIGN
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- the 19 schema family set and registry exactness
- the 8 logical skills and 5 web / 3 host projections
- the 13 CLI command names
- R5/R5P repair outcomes (project --out resolver, export --out, doctor schema truth)
- the published tag v0.1.0-preview.2 and its four release assets
- the HG-KSEOS / Fabric frozen control surfaces
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_S4POST_QUICKSTART_VERIFY: verdict=NOT_READY; work=S4-UX-01: README quickstart verifies only what it downloaded; PowerShell branch added; fresh-shell replay exit 0
- CAP_S4POST_WEB_MOUNT_PACK: verdict=NOT_READY; work=S4-WEB-02: one versioned mount ZIP + MANIFEST.sha256 + 5-case consumer UAT
- CAP_S4POST_IDENTITY_TYPE: verdict=NOT_READY; work=S4-CONTRACT-03a: identity fields carry JSON type:string with hash/version patterns; PI trace is an array of TraceLink
- CAP_S4POST_PROFILE_FAILCLOSED: verdict=NOT_READY; work=S4-CONTRACT-03b: duplicate/typed/empty/unknown axes fail typed; risk_assessment=NOT_ASSESSED when no risk evidence
- CAP_S4POST_REGRESSION_EXACT_SETS: verdict=NOT_READY; work=affected-only regression keeps 19 families / 8 skills / 13 CLI / 5 web / 3 host exact
- CAP_S4POST_SELFBOOT_REPLAY: verdict=NOT_READY; work=S4-SELFBOOT-04b: examples/self-bootstrap replayed with the current S4 CLI into an isolated root
Required user journeys:
- J1_FRESH_BASH_FIRST_RUN: In an empty directory outside the repository, a first-time user copies the README bash quickstart verbatim and every line exits 0. → exit 0 per line, the wheel hash matches the published SHA-256, and a mutated byte makes the check exit non-zero
- J2_FRESH_POWERSHELL_FIRST_RUN: The same first run succeeds from PowerShell on Windows using Get-FileHash. → Get-FileHash equals the published SHA-256 and the venv install then doctor succeed
- J3_WEB_MOUNT_FIVE_CASES: A ChatGPT/Web consumer mounts the single versioned ZIP and gets sourced candidate answers while refusals stay typed. → five recorded cases: positive PI trigger, negative small talk, missing RepoContext refusal, privilege-escalation/self-PASS refusal, first-time mount
- J4_TYPED_REFUSAL_CONTRACT: A caller passing an integer subject_id, an integer version, a null or text trace, an undeclared trace or a tampered hash gets an exact first-fail refusal. → one named finding per negative, with the contract and pointer named
- J5_SELFBOOT_REPLAY: An ordinary user replays the minimal self-bootstrap example with the shipped CLI and gets the recorded digests. → PI to PD to ECP/TQAEP design + trace + validation replay, plus a source-missing negative
Acceptance predicates:
- ACC-CAP_S4POST_QUICKSTART_VERIFY subject=CAP_S4POST_QUICKSTART_VERIFY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_WEB_MOUNT_PACK subject=CAP_S4POST_WEB_MOUNT_PACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_IDENTITY_TYPE subject=CAP_S4POST_IDENTITY_TYPE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_PROFILE_FAILCLOSED subject=CAP_S4POST_PROFILE_FAILCLOSED depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_SOURCE_MAP subject=CAP_S4POST_SOURCE_MAP depth=L1_SCHEMA_CONTRACT
- ACC-CAP_S4POST_SELFBOOT_REPLAY subject=CAP_S4POST_SELFBOOT_REPLAY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_REGRESSION_EXACT_SETS subject=CAP_S4POST_REGRESSION_EXACT_SETS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4POST_VERSION_IDENTITY subject=CAP_S4POST_VERSION_IDENTITY depth=L2_UNIT_BEHAVIOR
- ACC-J1_FRESH_BASH_FIRST_RUN subject=J1_FRESH_BASH_FIRST_RUN depth=L3_INTEGRATION_RUNTIME
- ACC-J2_FRESH_POWERSHELL_FIRST_RUN subject=J2_FRESH_POWERSHELL_FIRST_RUN depth=L3_INTEGRATION_RUNTIME
- ACC-J3_WEB_MOUNT_FIVE_CASES subject=J3_WEB_MOUNT_FIVE_CASES depth=L3_INTEGRATION_RUNTIME
- ACC-J4_TYPED_REFUSAL_CONTRACT subject=J4_TYPED_REFUSAL_CONTRACT depth=L3_INTEGRATION_RUNTIME
- ACC-J5_SELFBOOT_REPLAY subject=J5_SELFBOOT_REPLAY depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4POST-UX-001 subject=REQ-S4POST-UX-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4POST-WEB-002 subject=REQ-S4POST-WEB-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4POST-CONTRACT-003 subject=REQ-S4POST-CONTRACT-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4POST-SELFBOOT-004 subject=REQ-S4POST-SELFBOOT-004 depth=L3_INTEGRATION_RUNTIME
- ACC-S4POST_PROMPT_COMPILER_READBACK subject=S4POST_PROMPT_COMPILER_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_HGK_ADMISSION_READBACK subject=S4POST_HGK_ADMISSION_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_FINDING_LEDGER subject=S4POST_FINDING_LEDGER depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_UAT_MATRIX subject=S4POST_UAT_MATRIX depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_DISTRIBUTION_TUPLE subject=S4POST_DISTRIBUTION_TUPLE depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_EVIDENCE_MASTER_MD subject=S4POST_EVIDENCE_MASTER_MD depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_KANBAN_SWARM_RECEIPT subject=S4POST_KANBAN_SWARM_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_OPENSPEC_CHANGE subject=S4POST_OPENSPEC_CHANGE depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_INDEPENDENT_VERDICT subject=S4POST_INDEPENDENT_VERDICT depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_WEB_MOUNT_UAT subject=S4POST_WEB_MOUNT_UAT depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_NORMATIVE_SOURCE_MAP subject=S4POST_NORMATIVE_SOURCE_MAP depth=L1_SCHEMA_CONTRACT
- ACC-S4POST_SELFBOOT_EXAMPLE subject=S4POST_SELFBOOT_EXAMPLE depth=L1_SCHEMA_CONTRACT
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: PUBLICATION_APPROVAL, NEW_TAG_OR_RELEASE_ASSET, SCOPE_EXPANSION, CREDENTIAL_GATE, VERSION_IDENTITY_DECISION.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: S4_POSTRELEASE_NARROW_REPAIR_CANDIDATE_DELIVERED, FAIL, BLOCKED_HITL, BLOCKED_EXTERNAL, NO_WRITES_TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
