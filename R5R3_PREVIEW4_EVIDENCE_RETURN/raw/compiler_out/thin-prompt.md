# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: R5R3-PREVIEW4-LIVE-SUBJECT-DELTA-CLOSURE-001
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Re-verify the S4-R5 change set delta-only on its LIVE subject, repair the one defect that is still real (the install route and the release identity record), keep the repair inside documentation/metadata plus a derived guard, and return a machine-readable evidence pack for external acceptance.
Expected outcome: A reader following the front page reaches the bytes the release actually serves; the repository records every served identity and can re-derive it.
ChangeSet: CONTINUATION
Affected domains: install_route_truth, release_identity_recording, documentation_ssot, guard_coverage

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- R1 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP S4 R5｜Hermes／HG-KSEOS 聚焦修補、Preview.4、私人 Plugin ZIP 指揮薄 PROMPT-3.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP S4 R5｜Hermes／HG-KSEOS 聚焦修補、Preview.4、私人 Plugin ZIP 指揮薄 PROMPT-3.md role=NORMATIVE
- R2 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP｜S4 R5 修補後獨立驗收、私人 Plugin ZIP、Preview.4 與階段結案裁決-3.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP｜S4 R5 修補後獨立驗收、私人 Plugin ZIP、Preview.4 與階段結案裁決-3.md role=NORMATIVE
- R3 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\PIPD\PIPD-LS-SP_PIPD-PKG C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\PIPD\PIPD-LS-SP_PIPD-PKG role=NORMATIVE
- R4 C:\Projects\Agent_Workspace\HG-KSEOS\config\lane-routing-registry.yaml C:\Projects\Agent_Workspace\HG-KSEOS\config\lane-routing-registry.yaml role=NORMATIVE
- R5 C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout\raw\served_assets.json C:\Projects\Agent_Workspace\_handover\R5R3-20261016-preview4-closeout\raw\served_assets.json role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: The owner sees one scoped pull request with the round's evidence beside it, and no claim raised above what was measured.
Constraints:
- delta-only: do not redo D1/D2/TYPE5 if already on main
- no product code, no ninth skill, no MCP/Apps/Hooks, no second control plane
- no tag, no release, no merge to main, no in-place asset replacement
- credential never printed, never in argv/env/logs, scoped to one repository and one branch
- every claim carries a locator and raw output
Non-goals:
- public plugin directory publication
- production promotion
- four-host full UAT
- moving .hgk/ out of the repository
- re-cutting a wheel or plugin ZIP
Authorized mutations:
- one isolated branch of shw097-team/PIPD-LS-SP
- documentation/metadata files named in changeset.affected_files
- one derived guard test and one openspec change record
- the evidence pack directory
Forbidden mutations:
- main
- existing tags and their assets
- src/** and schemas/**
- .hgk/ history
- any other repository
Claim ceiling: LOCAL

## 4. Active / Deferred / Forbidden scope
Active:
- HGK_GOVERNANCE_CONTROL_PLANE: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- KANBAN_EXECUTION_BOARD: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- SWARM_FANOUT_SUBAGENTS: ACTIVE_SELECTED; action=USE_NATIVE; runtime_required=true
- GSTACK_NAMED_METHOD_READBACK: ACTIVE_SELECTED; action=QUALIFY; runtime_required=true
- OPENSPEC_CHANGE_RECORD: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CODEX_LANE_EXECUTE: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- CODEX_LANE_VERIFY_SECURITY: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- FAR_AUTONOMOUS_RESEARCH: ACTIVE_SELECTED; action=QUALIFY; runtime_required=true
- GITHUB_SCOPED_BRANCH_PUBLICATION: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
- REPRODUCIBLE_EVIDENCE_RETURN: ACTIVE_REQUIRED; action=USE_NATIVE; runtime_required=true
Non-active:
- GITHUB_TAG_OR_RELEASE_MUTATION: PROHIBITED; action=PROHIBIT
- PRIVATE_CHATGPT_HOST_SMOKE: DEFERRED_SOURCE_BACKED; action=DEFER
- PUBLIC_PLUGIN_DIRECTORY: PROHIBITED; action=PROHIBIT
- D1D2_SEMANTIC_PRODUCT_REPAIR: NOT_APPLICABLE_SOURCE_BACKED; action=NONE
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- v0.1.1-preview.1..4 tags and their assets
- PR #3 and PR #5
- the D1/D2 product repair on main
- the CNV R6/R7 backlog
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- HGK_GOVERNANCE_CONTROL_PLANE: verdict=RUNTIME_READY; work=AGENTS.md and the lane registry read; the control plane is the native governor, not routed; route/method: flow=hgk.lifecycle.admission; target=hgk-native; external=none
- KANBAN_EXECUTION_BOARD: verdict=RUNTIME_READY; work=board + swarm created, root t_38161c1b; route/method: flow=hermes.kanban.swarm; target=hermes-native; external=none
- SWARM_FANOUT_SUBAGENTS: verdict=RUNTIME_READY; work=board r5r3-preview4-closeout-20261016 carries five workers, one verifier and one synthesizer; route/method: flow=hermes.kanban.swarm; target=hermes-native; external=none
- GSTACK_NAMED_METHOD_READBACK: verdict=RUNTIME_READY; work=readback ran; DRIFT_VALUE on codex_sha256 recorded as a projection-staleness finding; route/method: flow=hgk.gstack.route; target=hgk-native; external=hg_kseos lane_policy + named_methods driven read-only
- OPENSPEC_CHANGE_RECORD: verdict=RUNTIME_READY; work=13/13 changes valid, --strict; route/method: flow=openspec.change; target=openspec-native; external=npx openspec validate --strict
- CODEX_LANE_EXECUTE: verdict=RUNTIME_READY; work=required_arm == served_arm == opencode-go/deepseek-v4.1-flash; route/method: flow=hgk.lane.dispatch.EXECUTE; target=hgk-native; external=CODEX CLI, required arm opencode-go/deepseek-v4.1-flash
- CODEX_LANE_VERIFY_SECURITY: verdict=RUNTIME_READY; work=required_arm == served_arm == openai-codex/gpt-6.1-sol; route/method: flow=hgk.lane.dispatch.VERIFY_SECURITY; target=hgk-native; external=CODEX CLI, required arm openai-codex/gpt-6.1-sol
- FAR_AUTONOMOUS_RESEARCH: verdict=RUNTIME_READY; work=run FAR-20261016-011, 16 artifacts; route/method: flow=fabric.far.research; target=fabric-native; external=FAR router route(RESEARCH_LITERATURE_REPO)
- GITHUB_SCOPED_BRANCH_PUBLICATION: verdict=RUNTIME_READY; work=branch pushed with remote readback equal to local; route/method: flow=github.scoped_write; target=github-api+https; external=HTTPS credential helper, one branch, readback
- REPRODUCIBLE_EVIDENCE_RETURN: verdict=RUNTIME_READY; work=PACK_INDEX.json re-derives every stored byte, including in a fresh clone; route/method: flow=hgk.evidence.return; target=hgk-native; external=pack + PACK_INDEX self-hash
Required user journeys:
- UJ-R5R3-DELTA-CLOSURE: Have the S4-R5 change set verified on its live subject and the remaining real defect repaired, without redoing finished work and without inventing authority. → A draft pull request whose route names the served bytes, whose evidence pack self-verifies, and whose status lists every checklist item honestly.
Acceptance predicates:
- ACC-01 subject=CK-02 subject freeze depth=L3_INTEGRATION_RUNTIME
- ACC-02 subject=CK-03/04 D1/D2 edges depth=L3_INTEGRATION_RUNTIME
- ACC-03 subject=CK-05 ClaimCeiling five shapes depth=L3_INTEGRATION_RUNTIME
- ACC-04 subject=CK-07 full suite depth=L3_INTEGRATION_RUNTIME
- ACC-05 subject=CK-07 wheel clean install depth=L3_INTEGRATION_RUNTIME
- ACC-06 subject=CK-11 plugin ZIP safety depth=L3_INTEGRATION_RUNTIME
- ACC-07 subject=CK-12 served-asset readback depth=L3_INTEGRATION_RUNTIME
- ACC-08 subject=CK-13 install route identity depth=L2_UNIT_BEHAVIOR
- ACC-09 subject=CK-06 write scope depth=L2_UNIT_BEHAVIOR
- ACC-10 subject=CK-08 secret and guard discipline depth=L4_FAILURE_RECOVERY
- ACC-11 subject=CK-14 private host smoke depth=L5_REAL_LIFECYCLE_SIDE_EFFECT
- ACC-12 subject=CK-09 scoped publication depth=L3_INTEGRATION_RUNTIME
- ACC-13 subject=CK-01 contract compile depth=L2_UNIT_BEHAVIOR
- ACC-16 subject=UJ-R5R3-DELTA-CLOSURE depth=L3_INTEGRATION_RUNTIME
- ACC-14 subject=CK-15 independent checker depth=L3_INTEGRATION_RUNTIME
- ACC-15 subject=self-research artefact depth=L2_UNIT_BEHAVIOR
- ACC-CAP-HGK_GOVERNANCE_CONTROL_PLANE subject=HGK_GOVERNANCE_CONTROL_PLANE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-KANBAN_EXECUTION_BOARD subject=KANBAN_EXECUTION_BOARD depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-SWARM_FANOUT_SUBAGENTS subject=SWARM_FANOUT_SUBAGENTS depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-GSTACK_NAMED_METHOD_READBACK subject=GSTACK_NAMED_METHOD_READBACK depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-OPENSPEC_CHANGE_RECORD subject=OPENSPEC_CHANGE_RECORD depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-CODEX_LANE_EXECUTE subject=CODEX_LANE_EXECUTE depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-CODEX_LANE_VERIFY_SECURITY subject=CODEX_LANE_VERIFY_SECURITY depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-FAR_AUTONOMOUS_RESEARCH subject=FAR_AUTONOMOUS_RESEARCH depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-GITHUB_SCOPED_BRANCH_PUBLICATION subject=GITHUB_SCOPED_BRANCH_PUBLICATION depth=L3_INTEGRATION_RUNTIME
- ACC-CAP-REPRODUCIBLE_EVIDENCE_RETURN subject=REPRODUCIBLE_EVIDENCE_RETURN depth=L3_INTEGRATION_RUNTIME
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: credential/secret, release owner approval, host account entitlement.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: PASS.
Nonterminal pauses: PARTIAL_RESUMABLE, BLOCKED_HITL, TEMP_CLOSED, FAIL, FAILED_STOP_ESCALATE.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above LOCAL.
