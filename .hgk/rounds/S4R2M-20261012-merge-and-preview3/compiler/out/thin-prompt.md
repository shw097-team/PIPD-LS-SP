# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: PIPD-LS-SP-HERMES-S4R2M-MERGE-AND-PREVIEW3-CONDITIONAL
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Under HG-KSEOS as the sole control plane, carry the S4-R2 repairs already present on the s4-r2 branch through the two README corrections and an isolated focused regression, then integrate conditionally into main; open a separate release gate for preview.3 only if the owner selects it.
Expected outcome: A half-closed round: the README routes CLI and Skills separately, --root is described the way the CLI really behaves, the frozen product passes an isolated affected regression, and main either carries the repairs with a readback or is honestly left at MERGE_READY_HITL_PENDING.
ChangeSet: NARROW_REPAIR
Affected domains: README/docs, tests(affected only), round evidence, repository integration, release gate (conditional)

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R0 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4R2_PREVIEW3_CONDITIONAL_MERGE_REPAIR_PROMPT_2026-10-11.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP_HERMES_S4R2_PREVIEW3_CONDITIONAL_MERGE_REPAIR_PROMPT_2026-10-11.md role=NORMATIVE
- R1 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_S4_MVP_PostRelease_S4R2_Independent_Acceptance_and_Preview3_Gate_2026-10-11.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD_LS_SP_S4_MVP_PostRelease_S4R2_Independent_Acceptance_and_Preview3_Gate_2026-10-11.md role=NORMATIVE
- R2 C:\Projects\Agent_Workspace\知識庫 C:/Projects/Agent_Workspace/知識庫 (PKG-00..10 / DOC-00..09 / 藍圖 / canonical standard) role=NORMATIVE
- R3 C:\Projects\Agent_Workspace\HG-KSEOS C:/Projects/Agent_Workspace/HG-KSEOS (AGENTS.md, config/project.json, var/shared-spine/hg-kseos.db) role=NORMATIVE
- R4 C:\Projects\Agent_Workspace\Fabric C:/Projects/Agent_Workspace/Fabric (/control/CHANGE_CLASS_ROUTER.yaml, SOD_POLICY.yaml, RISK_POLICY.yaml, /assurance/EVIDENCE_CONTRACT.yaml) role=NORMATIVE
- S1 C:\Projects\Agent_Workspace\PIPD git worktree PIPD/worktrees/s4r2m-merge-wt + PIPD-postrelease-wt (branch s4-r2-affected-only-20261011) role=STATE_EVIDENCE
- S2 https://github.com/shw097-team/PIPD-LS-SP refs (anonymous ls-remote) https://github.com/shw097-team/PIPD-LS-SP refs (anonymous ls-remote) role=STATE_EVIDENCE
- S3 C:\Projects\Agent_Workspace\PIPD-postrelease-wt PIPD-postrelease-wt/.hgk/rounds/S4R2-20261011-affected-only/verify/VERIFY_RECEIPT_gpt61sol.json role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: An ordinary reader can pick one of two paths and reach a working install or a mounted document pack without believing that a wheel install loads native web skills; preview.2 keeps serving existing users.
Constraints:
- No 20th schema, no 9th logical skill, no 14th CLI command.
- Do not rewrite the frozen s4-r2 product commit, the sealed preview.1/.2 tags or their assets.
- The read-only checker subject must never be mutated by a suite run.
- Fabric stays a read-only policy consumer; HG-KSEOS stays the only writer-facing control plane.
- Five ProfileBinding mutants stay closed; the version grammar stays a deferred P2 observation.
Non-goals:
- S5-S8, GENIE, JIT, SWOF live receivers and the 22 inactive providers.
- A full 57-row source crosswalk in PASS state as a precondition for this Beta repair.
- Rebuilding the 11 PKG + 10 DOC + skeleton corpus as a second SSOT.
- Making PIPD an agent runtime, a security LLM judge or a credential broker.
- Re-running a full S0-S4 re-audit after a documentation change.
Authorized mutations:
- README.md and a small docs smoke test on the admitted candidate branch.
- Round evidence under .hgk/rounds/S4R2M-20261012-merge-and-preview3/.
- A fast-forward of the approved candidate into main under owner approval.
- A new immutable preview tag plus wheel and mount pack, only under a separate owner release approval.
Forbidden mutations:
- Force-push, tag rewrite, or overwriting a published asset.
- Writing into the frozen checker subject or into another profile's skills/plugins/cron.
- Printing, copying or committing any credential value.
- Widening the admitted write-set without a new requirement.
Claim ceiling: EXTERNAL_ACCEPTANCE

## 4. Active / Deferred / Forbidden scope
Active:
- CAP-S4R2M-README-PATH-SPLIT: ACTIVE_REQUIRED; action=INSTALL; runtime_required=false
- CAP-S4R2M-CLI-ROOT-TRUTH: ACTIVE_REQUIRED; action=INSTALL; runtime_required=false
- CAP-S4R2M-BOUNDED-WRITER-LANE: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP-S4R2M-ISOLATED-REGRESSION: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP-S4R2M-INDEPENDENT-OFFICER: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP-S4R2M-MAIN-FF-INTEGRATION: ACTIVE_REQUIRED; action=DESIGN; runtime_required=false
- CAP-S4R2M-PROMPT-COMPILER-CAPC: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP-S4R2M-HGK-ADMISSION: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
Non-active:
- CAP-S4R2M-PREVIEW3-RELEASE: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP-S4R2M-WEB-NATIVE-SKILL-LOAD: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP-S4R2M-VERSION-GRAMMAR: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP-S4R2M-PROFILE-12AXIS-RISK: DEFERRED_SOURCE_BACKED; action=DEFER
- CAP-S4R2M-S5-S8-RUNTIME: PROHIBITED; action=PROHIBIT
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- frozen s4-r2 product commit 7c00b64960d86fc1e94848c9955c512a3626a85f
- 19 schema set and registry
- 8 logical SkillContracts and 5 web documents
- 13 CLI command set
- ProfileBinding five decision fields and their four early mutants
- sealed preview.1/.2 tags and assets
- HG-KSEOS and Fabric sealed control surfaces
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- CAP-S4R2M-BOUNDED-WRITER-LANE: verdict=NOT_READY; work=bind one sealed Codex writer to the admitted write-set of WO-S4R2M-DOC-CAL-01 and prove the escape is discriminated, not just the in-scope write admitted; keep credentials and git out of the writer lane
- CAP-S4R2M-ISOLATED-REGRESSION: verdict=NOT_READY; work=build a byte-equivalent writable clone from the frozen candidate head so the read-only subject is never mutated; run the six named affected test modules plus the two CE/wheel positives and keep the 19/8/13 exact-set unchanged
- CAP-S4R2M-INDEPENDENT-OFFICER: verdict=NOT_READY; work=dispatch the checker lane on a different model family than the writer and re-derive every decisive figure; reject a maker-authored verdict presented as independent acceptance
- CAP-S4R2M-PROMPT-COMPILER-CAPC: verdict=NOT_READY; work=satisfy lint, activation and acceptance with zero errors and emit the compiler receipt; keep the rendered thin prompt inside render_policy.max_prompt_chars
- CAP-S4R2M-HGK-ADMISSION: verdict=NOT_READY; work=admit one requirement per WorkOrder through the typed API and read the binding back; bind the writable_root to the candidate worktree actually used by the writer
- CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC: verdict=NOT_READY; work=create the round board and its swarm root/worker/verifier/synthesizer graph and persist the returned ids; record the named-method route readback and one change proposal, without promoting any method to control authority
Required user journeys:
- J1_CLI_PACKAGED_INSTALL: A first-time user picks the CLI path and installs the pinned wheel. → The front page states that the wheel carries the Python CLI and 19 schemas and that it does NOT inject the 8 native web skills.
- J2_SKILLS_MOUNT_PACK: A web user picks the Skills path and mounts the versioned document pack. → The mount guide distinguishes manual document/Knowledge mode from a native skill upload, and native loading stays NOT_RUN unless a host receipt exists.
- J3_FIRST_RUN_REPLAY: An ordinary reader runs the copy-paste compiler chain twice. → Both runs exit 0 and the six produced artefact digests are identical between passes.
- J4_TYPED_PROFILE_BINDING: A user binds a profile and the duplicate/typed axis mutants are refused. → A legal LITE/STANDARD/ASSURED binding is accepted and every malformed axis form is refused with a typed schema exit.
- J5_CLI_ROOT_FLAG_TRUTH: A reader follows the documented --root rules for init, project and export. → The pre-subcommand form works for the compile chain and the subcommand-local form works for project and export, exactly as the documented text says.
- J6_MERGE_VS_PUBLIC_WHEEL: A user wants the new repairs from the public tag. → The README and the release state say plainly that main carrying the repairs and the public preview.2 wheel are different artefacts.
Acceptance predicates:
- ACC-CAP-S4R2M-README-PATH-SPLIT subject=CAP-S4R2M-README-PATH-SPLIT depth=L2_UNIT_BEHAVIOR
- ACC-CAP-S4R2M-CLI-ROOT-TRUTH subject=CAP-S4R2M-CLI-ROOT-TRUTH depth=L2_UNIT_BEHAVIOR
- ACC-CAP-S4R2M-BOUNDED-WRITER-LANE subject=CAP-S4R2M-BOUNDED-WRITER-LANE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-ISOLATED-REGRESSION subject=CAP-S4R2M-ISOLATED-REGRESSION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-INDEPENDENT-OFFICER subject=CAP-S4R2M-INDEPENDENT-OFFICER depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-MAIN-FF-INTEGRATION subject=CAP-S4R2M-MAIN-FF-INTEGRATION depth=L2_UNIT_BEHAVIOR
- ACC-CAP-S4R2M-PROMPT-COMPILER-CAPC subject=CAP-S4R2M-PROMPT-COMPILER-CAPC depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-HGK-ADMISSION subject=CAP-S4R2M-HGK-ADMISSION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC subject=CAP-S4R2M-KANBAN-SWARM-GSTACK-OPENSPEC depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-S4R2M-PREVIEW3-RELEASE subject=CAP-S4R2M-PREVIEW3-RELEASE depth=L0_STATIC_EXISTENCE
- ACC-CAP-S4R2M-WEB-NATIVE-SKILL-LOAD subject=CAP-S4R2M-WEB-NATIVE-SKILL-LOAD depth=L0_STATIC_EXISTENCE
- ACC-CAP-S4R2M-VERSION-GRAMMAR subject=CAP-S4R2M-VERSION-GRAMMAR depth=L0_STATIC_EXISTENCE
- ACC-CAP-S4R2M-PROFILE-12AXIS-RISK subject=CAP-S4R2M-PROFILE-12AXIS-RISK depth=L0_STATIC_EXISTENCE
- ACC-CAP-S4R2M-S5-S8-RUNTIME subject=CAP-S4R2M-S5-S8-RUNTIME depth=L0_STATIC_EXISTENCE
- ACC-J1_CLI_PACKAGED_INSTALL subject=J1_CLI_PACKAGED_INSTALL depth=L3_INTEGRATION_RUNTIME
- ACC-J2_SKILLS_MOUNT_PACK subject=J2_SKILLS_MOUNT_PACK depth=L3_INTEGRATION_RUNTIME
- ACC-J3_FIRST_RUN_REPLAY subject=J3_FIRST_RUN_REPLAY depth=L3_INTEGRATION_RUNTIME
- ACC-J4_TYPED_PROFILE_BINDING subject=J4_TYPED_PROFILE_BINDING depth=L3_INTEGRATION_RUNTIME
- ACC-J5_CLI_ROOT_FLAG_TRUTH subject=J5_CLI_ROOT_FLAG_TRUTH depth=L3_INTEGRATION_RUNTIME
- ACC-J6_MERGE_VS_PUBLIC_WHEEL subject=J6_MERGE_VS_PUBLIC_WHEEL depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2M-DOC-001 subject=REQ-S4R2M-DOC-001 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2M-VERIFY-002 subject=REQ-S4R2M-VERIFY-002 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2M-MERGE-003 subject=REQ-S4R2M-MERGE-003 depth=L3_INTEGRATION_RUNTIME
- ACC-REQ-S4R2M-PREVIEW3-004 subject=REQ-S4R2M-PREVIEW3-004 depth=L3_INTEGRATION_RUNTIME
- ACC-CAPC_PROMPT_COMPILE_RECEIPT subject=CAPC_PROMPT_COMPILE_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-HGK_ADMISSION_READBACK subject=HGK_ADMISSION_READBACK depth=L1_SCHEMA_CONTRACT
- ACC-README_F01_F02_PATCH subject=README_F01_F02_PATCH depth=L1_SCHEMA_CONTRACT
- ACC-ISOLATED_FOCUSED_REGRESSION_RECEIPT subject=ISOLATED_FOCUSED_REGRESSION_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-INDEPENDENT_OFFICER_VERDICT subject=INDEPENDENT_OFFICER_VERDICT depth=L1_SCHEMA_CONTRACT
- ACC-MERGE_DECISION_S4R2M subject=MERGE_DECISION_S4R2M depth=L1_SCHEMA_CONTRACT
- ACC-KANBAN_SWARM_GSTACK_OPENSPEC_RECEIPT subject=KANBAN_SWARM_GSTACK_OPENSPEC_RECEIPT depth=L1_SCHEMA_CONTRACT
- ACC-PREVIEW3_RELEASE_GATE_DECISION subject=PREVIEW3_RELEASE_GATE_DECISION depth=L1_SCHEMA_CONTRACT
- ACC-S4R2M_EVIDENCE_PACK subject=S4R2M_EVIDENCE_PACK depth=L1_SCHEMA_CONTRACT
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: credential/secret, owner-merge-approval, owner-release-approval, license/entitlement.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: S4R2M_MAIN_MERGED_PREVIEW3_DEFERRED, S4R2M_PREVIEW3_PUBLISHED_SCOPED.
Nonterminal pauses: MERGE_READY_HITL_PENDING, RELEASE_HITL_PENDING, AUTH_BLOCKED, ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, TEMP_CLOSED, FAIL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above EXTERNAL_ACCEPTANCE.
