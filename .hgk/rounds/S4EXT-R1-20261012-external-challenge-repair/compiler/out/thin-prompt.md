# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: S4EXT-R1-20261012-PIPD-LS-SP-NARROW-REPAIR
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: Repair the confirmed S4 findings of the external challenge (F001 release provenance, F002 trace closure, F003 current-release regression pin), disposition O007-O009 and the 57-row SPEC/DEL gaps, assemble the S4_EXTERNAL_RETURN_PACK, and push the repair branch for external acceptance.
Expected outcome: A repair branch whose mount-pack release identity is truthful and independently resolvable, whose validate path refuses a tampered trace bundle, and whose evidence pack lets an external verifier replay every claim from raw logs.
ChangeSet: NARROW_REPAIR
Affected domains: schemas, runtime, tests, docs, examples, dist/mount, release-metadata, governance-evidence

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- 1 PIPD-LS-SP S4 R1 指揮薄 PROMPT_2026-10-12.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP S4 R1｜HERMES／HG-KSEOS／Fabric 受治理施工與驗收指揮薄 PROMPT_2026-10-12.md role=NORMATIVE
- 2 HG-KSEOS/AGENTS.md C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md role=NORMATIVE
- 3 PIPD worktree C:\Projects\Agent_Workspace\PIPD\worktrees\s4ext-r1-wt role=NORMATIVE
- 4 PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1.md role=STATE_EVIDENCE
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: Any new user can run the whole compiler chain in one portable command on Linux/Windows without the author's paths, and can see exactly which claims are maker-local.
Constraints:
- candidate-only writes; no agent self-acceptance
- the published v0.1.1-preview.3 tag and its release assets are immutable
- the credential file is read only at the push step, never through the LLM context
- no new schema family, skill, or CLI verb
Non-goals:
- refactoring PIPD
- a second lifecycle or trace engine
- forced SemVer
- a 12-axis risk engine
- S5-S8 / SQP1 / production activation
- claiming S4 PASS or any release/production promotion
Authorized mutations:
- schemas/TraceLink.schema.json
- schemas/PI-PKG.schema.json
- src/pipd_ls_sp/validate.py
- src/pipd_ls_sp/profiles.py
- tools/build_mount_pack.py
- dist/mount/** (new erratum pack only)
- docs/RELEASE_TUPLE.json
- docs/S4_SPEC_DEL_ADJUDICATION.json
- docs/ERRATUM_2026-10-12_preview3_release_provenance.md
- tests/test_s4ext_*.py
- examples/first-run/run.sh
- examples/first-run/run.ps1
- README.md
- .hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/**
Forbidden mutations:
- remote main
- force-push
- merge
- tag move or delete
- overwriting a published release asset
- the knowledge base
- HG-KSEOS/Fabric policy and control
- any credential body
Claim ceiling: PACKAGE

## 4. Active / Deferred / Forbidden scope
Active:
- TraceLink endpoint typing and bundle graph closure (F002): ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- release provenance identity (F001/G006): ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- portable first-run path (O007): ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- installed wheel distribution (G006): ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- profiles boundary behaviour (O009): ACTIVE_REQUIRED; action=QUALIFY; runtime_required=false
Non-active:
- Web GPT-6 chat host: DEFERRED_SOURCE_BACKED; action=DEFER
- Hermes Agent skill host: DEFERRED_SOURCE_BACKED; action=DEFER
- Codex agent host: DEFERRED_SOURCE_BACKED; action=DEFER
- HG-KSEOS canonical acceptance transition: PROHIBITED; action=PROHIBIT
- S5-S8 GENIE JIT runtimes: PROHIBITED; action=PROHIBIT
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=false
Do not reopen:
- the published v0.1.1-preview.3 tag and assets
- historical FAIL receipts
- the legal legacy version="1" grammar
- the 19-family schema ABI
- sealed S0-S3 scope
- unrelated tests and fixtures
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- TraceLink endpoint typing and bundle graph closure (F002): verdict=NOT_READY; work=close independent_qualification with an external verifier
- release provenance identity (F001/G006): verdict=NOT_READY; work=external verifier re-derives the 8/8 identity from the pushed branch; release owner decides public erratum vs new preview
- portable first-run path (O007): verdict=NOT_READY; work=no Ubuntu/macOS host is available here; the Windows and Git-Bash paths are run
- installed wheel distribution (G006): verdict=NOT_READY; work=external verifier reruns the probe from the downloaded asset bytes
Required user journeys:
- J-01: A brand-new user on Linux/Git-Bash runs the whole compiler chain from a fresh checkout. → one command prints FIRST_RUN_OK and a validate verdict PASS with closure FULL
- J-02: A brand-new user on Windows PowerShell runs the same chain. → FIRST_RUN_OK and validate PASS with every native exit code checked
- J-03: An external verifier re-derives the mount pack's release identity from the frozen tuple and the git tag instead of trusting the pack's own text. → 8/8 documents name release_tag_target; a stale value fails the check
- J-04: A verifier replays the F002 counterexample against an installed distribution. → validate --bundle exits non-zero with CLOSURE findings on the repaired build, while the published build shows the recorded false PASS
Acceptance predicates:
- A-01 subject=release provenance identity (F001/G006) depth=L3_INTEGRATION_RUNTIME
- A-02 subject=TraceLink endpoint typing and bundle graph closure (F002) depth=L3_INTEGRATION_RUNTIME
- A-04 subject=portable first-run path (O007) depth=L3_INTEGRATION_RUNTIME
- A-07 subject=installed wheel distribution (G006) depth=L3_INTEGRATION_RUNTIME
- A-05 subject=profiles boundary behaviour (O009) depth=L2_UNIT_BEHAVIOR
- A-06 subject=J-01 depth=L3_INTEGRATION_RUNTIME
- A-08 subject=J-02 depth=L3_INTEGRATION_RUNTIME
- A-09 subject=J-03 depth=L2_UNIT_BEHAVIOR
- A-10 subject=J-04 depth=L3_INTEGRATION_RUNTIME
- A-11 subject=REQ-F001 depth=L2_UNIT_BEHAVIOR
- A-12 subject=REQ-F002 depth=L3_INTEGRATION_RUNTIME
- A-13 subject=REQ-F003 depth=L2_UNIT_BEHAVIOR
- A-14 subject=REQ-O007 depth=L3_INTEGRATION_RUNTIME
- A-15 subject=REQ-O009 depth=L2_UNIT_BEHAVIOR
- A-16 subject=DEL-REPAIR-BRANCH depth=L2_UNIT_BEHAVIOR
- A-17 subject=DEL-RETURN-PACK depth=L2_UNIT_BEHAVIOR
- A-18 subject=DEL-ERRATUM depth=L2_UNIT_BEHAVIOR
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: owner release/erratum decision, HGK push-gate approval, external verifier acceptance.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: PASS, PARTIAL, FAIL, TEMP_CLOSED.
Nonterminal pauses: PUSH_HOLD, BLOCKED_EXTERNAL, BLOCKED_HITL.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above PACKAGE.
