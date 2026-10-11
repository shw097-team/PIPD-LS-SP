# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-S4-R2-POSTRELEASE-AFFECTED-ONLY-20261011
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Execute one affected-only post-release maintenance round on the published S4 open-source MVP, driven by the second-round reaudit: confirm under its own contract which of F-S4R2-01..12 are already closed by this candidate lineage with fresh positive AND negative evidence, close only the genuinely open deltas (a real copy-paste end-to-end README fixture, the release version identity disclosure and the residual ProfileBinding typing hole), and hand the frozen candidate to an independent checker - without moving the immutable tag.
Expected outcome: A first-time user copy-pastes the README from a clean directory and every line exits 0 on bash and PowerShell; the README points at a fixture that really exists so intake -> compile-pi -> bind-pd -> compile-ecp -> compile-tqaep -> validate can be driven literally; malformed identity, trace and profile inputs are refused by exact typed first-fail; and the repository states where its normative sources live without creating a second SSOT.
ChangeSet: NARROW_REPAIR
Affected domains: README.md, examples, schemas, tests, .hgk

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4_R2_POSTRELEASE_AFFECTED_ONLY_REPAIR_PROMPT_2026-10-11.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4_R2_POSTRELEASE_AFFECTED_ONLY_REPAIR_PROMPT_2026-10-11.md role=NORMATIVE
- R0 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\驗收報告\PIPD_LS_SP_S4_MVP_PostRelease_Independent_Reaudit_Final_2026-10-11.md C:\Projects\Agent_Workspace\知識庫\實作相關DOC\PIPD\驗收報告\PIPD_LS_SP_S4_MVP_PostRelease_Independent_Reaudit_Final_2026-10-11.md role=NORMATIVE
- R3 https://github.com/shw097-team/PIPD-LS-SP@8faa64e581e8c25f5ec355475e29561847da3ead https://github.com/shw097-team/PIPD-LS-SP@8faa64e581e8c25f5ec355475e29561847da3ead role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD role=NORMATIVE
- R3 https://github.com/shw097-team/PIPD-LS-SP@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7 https://github.com/shw097-team/PIPD-LS-SP@4445db5a6d1b3138946fd7c4fe3b712e4faf1af7 role=STATE_EVIDENCE
- R0 C:/Projects/Agent_Workspace/HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS role=NORMATIVE
- R0 C:/Projects/Agent_Workspace/Fabric C:/Projects/Agent_Workspace/Fabric role=NORMATIVE
- R3 C:/Projects/Agent_Workspace/PIPD-postrelease-wt@s4-r2-affected-only-20261011 C:/Projects/Agent_Workspace/PIPD-postrelease-wt@s4-r2-affected-only-20261011 role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: The user needs only a shell, Python >= 3.11 and a ZIP upload; they never need to know WorkOrder, Skill or provider identifiers.
Constraints:
- AFFECTED-ONLY: keep the 19 schema families, 8 logical skills, 13 CLI commands, 5 web / 3 host projections and the clause-bound PI/PD trunk intact.
- A finding already closed with fresh positive and negative evidence is marked ALREADY_CLOSED_WITH_FRESH_POS_NEG and is not rewritten.
- The native prompt compiler must actually run; a missing bundle or a failure means PROMPT_COMPILE_BLOCKED with read-only preflight only.
- No new release: a document-only repair must not rebuild the wheel, and a new tag stays an owner HITL decision.
- Claims do not inherit: LOCAL_TESTED != INDEPENDENT_ACCEPTED != RELEASED, and the checker model is GPT 6.1 SOL-MEDIUM over OpenAI OAuth.
Non-goals:
- No second canonical SSOT, no second control plane, no plan IR, no scheduler.
- No S5 HGK live receiver, S6 GENIE, S7 JIT, S8 SWOF/SGM, PRE-W3 or the 22 inactive external technologies.
- No tag move, no force-push, no rewrite of published release bytes, no rewrite of historical FAIL receipts.
- No new 20th schema family, no 9th logical skill, no 14th CLI command, no MCP server or resident daemon.
- No restatement or cloning of the 11 PKG / 10 DOC / skeleton bodies into the runtime repository.
Authorized mutations:
- Minimal product-tree repair inside C:/Projects/Agent_Workspace/PIPD-postrelease-wt on branch s4-r2-affected-only-20261011: README.md, examples/**, schemas/ProfileBinding.schema.json and any already-affected schema, and new tests under tests/.
- The round evidence tree .hgk/rounds/S4R2-20261011-affected-only/.
- The single acceptance master document under 知識庫/實作相關DOC/PIPD/實作證據/.
Forbidden mutations:
- No second normative authority built from Hermes or Fabric; no self-signed INDEPENDENT_PASS.
- No destructive test against a real user path, no credential in argv/URL/log, no force-push, no history rewrite.
- No editing of any published tag, release asset or previous round's receipt.
- No promotion of this candidate or of the claim ceiling by the maker.
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP_S4R2_CLI_FIRSTUSE_VERIFY: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_COMPILER_REAL_FIXTURE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_WEB_MOUNT_CONSUME: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_PROFILE_TRUST: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_MACHINE_CONTRACT_TYPING: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_SOURCE_BOOTSTRAP: ACTIVE_SELECTED; action=DESIGN; runtime_required=false
- CAP_S4R2_HGK_ADMISSION: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP_S4R2_INDEPENDENT_VERIFY: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
Non-active:
- CAP_S4R2_GITHUB_PUBLICATION: STANDBY; action=DESIGN
- CAP_S4R2_S5_PROVIDERS: NOT_APPLICABLE_SOURCE_BACKED; action=DESIGN
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- the 19 schema family set and registry exactness
- the 8 logical skills and 5 web / 3 host projections
- the 13 CLI command names
- R7/R8 receipts as recorded (SCOPED_PASS / OVERALL_FAIL)
- the published tag v0.1.0-preview.2 and its four release assets
- the HG-KSEOS / Fabric frozen control surfaces
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP_S4R2_CLI_FIRSTUSE_VERIFY: verdict=NOT_READY; work=ACC-CAP_S4R2_CLI_FIRSTUSE_VERIFY: capability CAP_S4R2_CLI_FIRSTUSE_VERIFY
- CAP_S4R2_COMPILER_REAL_FIXTURE: verdict=NOT_READY; work=ACC-CAP_S4R2_COMPILER_REAL_FIXTURE: capability CAP_S4R2_COMPILER_REAL_FIXTURE
- CAP_S4R2_WEB_MOUNT_CONSUME: verdict=NOT_READY; work=ACC-CAP_S4R2_WEB_MOUNT_CONSUME: capability CAP_S4R2_WEB_MOUNT_CONSUME
- CAP_S4R2_PROFILE_TRUST: verdict=NOT_READY; work=ACC-CAP_S4R2_PROFILE_TRUST: capability CAP_S4R2_PROFILE_TRUST
- CAP_S4R2_MACHINE_CONTRACT_TYPING: verdict=NOT_READY; work=ACC-CAP_S4R2_MACHINE_CONTRACT_TYPING: capability CAP_S4R2_MACHINE_CONTRACT_TYPING
- CAP_S4R2_HGK_ADMISSION: verdict=NOT_READY; work=ACC-CAP_S4R2_HGK_ADMISSION: capability CAP_S4R2_HGK_ADMISSION
- CAP_S4R2_INDEPENDENT_VERIFY: verdict=NOT_READY; work=ACC-CAP_S4R2_INDEPENDENT_VERIFY: capability CAP_S4R2_INDEPENDENT_VERIFY
Required user journeys:
- J-CLI-FIRST: In an empty directory outside the repository a first-time user follows the README on bash or PowerShell: download, verify only what was downloaded, install, doctor, init - every line exits 0, and a tampered or missing asset exits non-zero. → exit 0 per line, wheel digest equals the published literal, and a mutated byte stops the block
- J-COMPILER-REAL: A newcomer copies a real, existing fixture and drives intake -> compile-pi -> bind-pd -> compile-ecp -> compile-tqaep -> validate with no placeholder and no fake source; a second replay is digest-stable and a missing source is refused. → a valid chain with verifiable artefact digests, stable on replay
- J-PROFILE-TRUST: Profile selection refuses duplicate or wrong-typed axes with a typed first-fail, and an unknown or unevidenced risk state is reported as NOT_ASSESSED instead of being called safe. → LITE / STANDARD / ASSURED still resolve for legal inputs; illegal ones refuse
- J-MACHINE-CONTRACT: The 19 contract families stay exact; an illegally typed identity/trace value is refused with an accurate first-fail and the earlier CE-1/CE-2 refusals do not regress. → a legal bundle validates with zero findings; int/null/scalar/malformed cases each fail on the right field
- J-WEB-CONSUMER: A web consumer mounts the single versioned pack and gets sourced candidate answers, while native-skill upload and manual document/Knowledge mode are declared separately and a host without native eligibility is reported NOT_RUN. → five recorded cases; refusals stay typed and the claim ceiling is visible
Acceptance predicates:
- ACC-CAP_S4R2_CLI_FIRSTUSE_VERIFY subject=CAP_S4R2_CLI_FIRSTUSE_VERIFY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_COMPILER_REAL_FIXTURE subject=CAP_S4R2_COMPILER_REAL_FIXTURE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_WEB_MOUNT_CONSUME subject=CAP_S4R2_WEB_MOUNT_CONSUME depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_PROFILE_TRUST subject=CAP_S4R2_PROFILE_TRUST depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_MACHINE_CONTRACT_TYPING subject=CAP_S4R2_MACHINE_CONTRACT_TYPING depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_SOURCE_BOOTSTRAP subject=CAP_S4R2_SOURCE_BOOTSTRAP depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_HGK_ADMISSION subject=CAP_S4R2_HGK_ADMISSION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_INDEPENDENT_VERIFY subject=CAP_S4R2_INDEPENDENT_VERIFY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_GITHUB_PUBLICATION subject=CAP_S4R2_GITHUB_PUBLICATION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP_S4R2_S5_PROVIDERS subject=CAP_S4R2_S5_PROVIDERS depth=L3_INTEGRATION_RUNTIME
- ACC-J-CLI-FIRST subject=J-CLI-FIRST depth=L3_INTEGRATION_RUNTIME
- ACC-J-COMPILER-REAL subject=J-COMPILER-REAL depth=L3_INTEGRATION_RUNTIME
- ACC-J-PROFILE-TRUST subject=J-PROFILE-TRUST depth=L3_INTEGRATION_RUNTIME
- ACC-J-MACHINE-CONTRACT subject=J-MACHINE-CONTRACT depth=L3_INTEGRATION_RUNTIME
- ACC-J-WEB-CONSUMER subject=J-WEB-CONSUMER depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2-DOC-001 subject=REQ-S4R2-DOC-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2-WEB-002 subject=REQ-S4R2-WEB-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2-CONTRACT-003 subject=REQ-S4R2-CONTRACT-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2-SOURCE-004 subject=REQ-S4R2-SOURCE-004 depth=L3_INTEGRATION_RUNTIME
- ACC-S4R2_PROMPT_COMPILER_READBACK subject=S4R2_PROMPT_COMPILER_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_HGK_ADMISSION_READBACK subject=S4R2_HGK_ADMISSION_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_FINDING_DISPOSITION subject=S4R2_FINDING_DISPOSITION depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_UAT_MATRIX subject=S4R2_UAT_MATRIX depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_CANDIDATE_TUPLE subject=S4R2_CANDIDATE_TUPLE depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_EVIDENCE_MASTER_MD subject=S4R2_EVIDENCE_MASTER_MD depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_KANBAN_SWARM_RECEIPT subject=S4R2_KANBAN_SWARM_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_OPENSPEC_CHANGE subject=S4R2_OPENSPEC_CHANGE depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_INDEPENDENT_RECEIPT subject=S4R2_INDEPENDENT_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_WEB_MOUNT_READBACK subject=S4R2_WEB_MOUNT_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_RESIDUAL_TYPING_PATCH subject=S4R2_RESIDUAL_TYPING_PATCH depth=L1_SCHEMA_CONTRACT
- ACC-S4R2_PUBLICATION_STATUS subject=S4R2_PUBLICATION_STATUS depth=L1_SCHEMA_CONTRACT
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: NEW_RELEASE_OR_TAG, REMOTE_WRITE, SCOPE_EXPANSION, CREDENTIAL_USE, CLAIM_CEILING_CHANGE.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: S4_R2_AFFECTED_ONLY_CANDIDATE_DELIVERED, FAIL, BLOCKED_HITL, BLOCKED_EXTERNAL, NO_WRITES_TEMP_CLOSED.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, AWAITING_STEER, SCOPE_EXPANSION_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
