# EXTERNAL_CHALLENGE_REPORT

## 1. Review identity

- review_id: FCR-REVIEW-S4POST-AO10; reviewed_at: 2026-10-12T14:59:22.960592+00:00.
- reviewer_surface: external clean-room challenger; installed fabric-external-independent-challenge-reviewer workflow and contracts. No maker memory or copied PASS reasoning.
- project/task: PIPD-LS-SP / S4-UX-DISTRIBUTION-UPGRADE-R1; round S4POST-20261012-postrepair-recheck-and-triple-upgrade.
- gates: S4-STAGE-B-HANDOVER-CLOSURE; S4-MODEL-ROUTING-CONFORMANCE.
- candidate identity: commit `35c5099debfad1fa7a11192de2495c6c359c06f8`, tree `06984281502581e0a9ef97e2fc80c100eef73856`.
- candidate package SHA-256: `2864ac2abda38e0c1f511d8f7c2f8df4430e8dc5b7e3e4a83ec4676290ecd2fe`. Deterministic `git archive --format=tar` of frozen HEAD retained at `C:\Users\user\AppData\Local\Temp\ao10-u9legwpj/candidate.tar`; this is the review snapshot, not a newly built release wheel. Initial wheel hash observation was separated into observed_release_artifacts in intake; final freeze-digests.json is authoritative for this review.
- distribution digest: `af342d281f02ba04f284a1625f4a58a6f2de15549cc182a0c61ce357ec6b504f`, recomputed `dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip`. Historical delivered mount distribution; association to current Stage-B is unresolved, not asserted.
- evidence manifest SHA-256: `2e5a1d19e80ba8759c07c6d1e4b085d3d3ebf67988f1e269965b0266adcfbbe9`, recomputed `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/EVIDENCE_RETURN_PACK.json`. Historical internal subject is quarantined for current acceptance.
- Internal Oracle identity: NO_INTERNAL_ORACLE_IN_THIS_ROUND; package digest not applicable. Historical officers are evidence/summary sources, not current Oracle authority.
- Isolation: external detached clone `C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject`. Test clones, stubs, fixtures, raw suite sublogs and orchestration live in system temp `C:\Users\user\AppData\Local\Temp\ao10-u9legwpj`. Delivery writes are review results/index/report/intake under round verify/ao10 only. No delivery commit/stage/reset/clean/push/tag/merge/source edit or Git configuration change. Test commits/reset/clean occurred only in external clones with resolved paths checked under private system temp. Command-scoped safe.directory used for delivery read/clone.

## 2. Authority/source inventory

All locators below are relative to frozen round unless marked repository-relative. Re-run `git show 35c5099debfad1fa7a11192de2495c6c359c06f8:<repository-relative-path>`; source-inventory.json records exact object SHA-256, presence and normalized checkout comparisons. numbered-sources.txt provides line numbers. Raw hashes retain CRLF/LF distinctions; normalization is only for comparison.

| item | role | locator/digest | status |
|---|---|---|---|
| User review contract | NORMATIVE | User brief: gates, boundaries, no models | Review authority |
| Role/failover assignment | NORMATIVE | stage-b/ROUND_ASSIGNMENT.json; source-inventory.json hash | Read and reconstructed |
| Owner ruling | NORMATIVE | stage-b/OWNER_DECISION_MODEL_DEVIATION.md; same inventory | EXECUTE exception and prohibited failover categories; implementation descriptions are claims |
| Closure/defect records | SUMMARY_CLAIM | ACCEPTANCE_RECORD_STAGEB.md; verify/harness/HARNESS_DEFECT_LOG.md | Handover intent; never proof of closure |
| Qualification study | SUMMARY_CLAIM / historical pointers | verify/harness/QUALIFICATION_FINDINGS.md | Historical model counts/root cause not reauthenticated |
| AO8 review | SUMMARY_CLAIM + historical RAW_EVIDENCE | verify/ao8/AO_VERDICT_HANDOVER_R8.md | Read first, mechanisms independently reconstructed |
| Earlier reviews | SUMMARY_CLAIM / historical evidence | AO3-AO6 intake pointers; AO7 correction and receipt; AO9 doubled-path object | AO3-AO6 full histories not audited; AO7 correction corroborated; AO9 locator disagrees |
| Evidence pack | STATE / SUMMARY_CLAIM | evidence/EVIDENCE_RETURN_PACK.json; hash above | Old Stage-B commit, independent_checker NOT_RUN |
| Installed reviewer skill | NORMATIVE procedure | C:/Users/user/.agents/skills/fabric-external-independent-challenge-reviewer/SKILL.md and referenced contracts/template | Self-test and four bundled unit tests passed |

## 3. Evidence inventory

| evidence_id | type | raw pointer | subject binding | rawness | status |
|---|---|---|---|---|---|
| FREEZE | STATE / RAW_EVIDENCE | freeze.txt, initial-status.txt, clone.txt, pin.txt, candidate-archive.txt, freeze-digests.json | Frozen HEAD/tree/archive | Commands, exits, bytes/digests | Bound |
| SOURCE | RAW_EVIDENCE | source-inventory.json, numbered-sources.txt, repair-diff.txt | Frozen objects; inspected delivery/clone normalized bytes match | Hashes + actual diff | Reviewed |
| SUITES | RAW_EVIDENCE | run_harness_negative_tests-isolated.txt; run_gate_negative_tests-isolated.txt; run_checker_failover_tests-isolated.txt | Frozen scripts, disposable clones | Commands/exits/assertion counts/raw stdout+stderr | 38/0, 34/0, 14/0; each exit 0 |
| CASES | RAW_EVIDENCE | case-isolated.txt + matching reproducer; gate-junction.txt; checker-mixed-failure.txt | Frozen HEAD reset before each case | Immediate raw command/exit/result | Deterministic stub probes |
| HISTORY | RAW_EVIDENCE | historical-ao7-receipt.txt; ao9-frozen.txt; ao9-actual-frozen-locator.txt | Frozen git objects | Raw output/exit | AO7 receipt exists; AO9 intake path wrong |
| END | STATE / RAW_EVIDENCE | delivery-end-identity.txt; delivery-end-status.txt; delivery-boundary.json | Same HEAD/tree | Read-only git commands | Review outputs plus outside-set AO9 move |
| VALIDATOR | RAW_EVIDENCE | skill-self-test.txt; skill-unit-tests.txt; bundle-validation.txt | Installed validator and final bundle | Command/exit/raw output | Readback below |

CODEX_BIN and GATE_BIN are explicitly shell stubs in every suite/probe invocation. Qualification stubs fabricate a header, two tool-success lines and sentinels without model calls; checker failure stub is synthetic. No worker/model identity is authenticated. No provider safety refusal occurred because no provider was called. Historical notices and the suite's fabricated refusal are not retried or worked around.

## 4. Challenge matrix

| gate / predicate | expected | evidence | counter-check | verdict |
|---|---|---|---|---|
| B: staged anchored scope | Reject outside prefix | prefix-isolated.txt | Old staged prefix refused exit 6 | Repaired finite case |
| Routing: literal owner match | Reject regex request before invocation | owner-regex-full-isolated.txt; owner-regex-qualify-only-isolated.txt | Full lane exits 8; qualify-only exits 0 | FCR-001 blocking |
| B/routing: receipt schema | Reject committed wrong/duplicate fields | forged-receipt-isolated.txt | Clean committed forgery refused exit 8 | Repaired finite case |
| B: gate log physical containment | Logs outside candidate | gate-logdir-isolated.txt; gate-junction.txt | Direct parent exit 3; junction returns 0/in-tree log | FCR-004 blocking |
| B: final HEAD/status order | Detect HEAD-query dirt | late-head-isolated.txt | Dirt before final query detected exit 5 | Repaired finite case |
| B: direct qualification label | Default ungated receipt no | direct-qualified-isolated.txt | Exit 0, qualified=no | Repaired default case |
| Routing: role exception | EXECUTE exception cannot authorize VERIFY | other-role-owner-isolated.txt | Wrong checker model accepted exit 0 | FCR-002 blocking |
| Routing: provider | Pin assigned provider | provider-override-isolated.txt | Unassigned provider reaches stub, exit 0 | FCR-003 blocking |
| Routing: checker failover | No switch on protocol 400 | checker-mixed-failure.txt | 400 + incidental quota switches, exit 0 | FCR-005 blocking |
| B: outer wrapper hygiene | Final record covered by postflight | checker-mixed-failure.txt | Failover record untracked after success | FCR-006 blocking |
| Positive checker control | Assigned AO checker medium | checker-primary-effort.txt | Correct model/provider/medium, clean child, exit 0 | Finite positive control |
| Known omitted-role limit | Explicitly bounded ungated entry | role-omitted-isolated.txt | Unassigned tuple admitted, qualified=no, exit 0 | Reproduced known limit |
| Known transcript limit | Stub cannot authenticate model | qualify-only stub probes | Fabricated transcript accepted | Reproduced known limit |
| Current acceptance identity | Fresh bound manifest/distribution | frozen pack + freeze-digests.json | Historical subject/NOT_RUN differs from HEAD | FCR-007 unresolved |
| Assertion baseline | Accurate denominator | isolated suites + frozen raw logs | 38/0, 34/0, 14/0 | FCR-008 count disagreement |

Six claimed closures are separately adjudicated. The old full regex-success example could NOT be reproduced: child refuses 6 and gate exits 8; qualify-only still accepts. Old prefix, forged-receipt, direct-log-parent, late-HEAD and default direct-qualified=yes successful examples could NOT be reproduced; their focused repairs are supported. Physical log containment remains broken through a junction. Newline filename behavior was NOT_EXECUTED.

## 5. Findings

Acceptance IDs below are locator-defined predicates; no independently enumerated subpredicate IDs were supplied. All findings bind the frozen subject. Retained reproducers and raw command/result records make each case rerunnable in a fresh external clone with stubs. Existing PASS reports are not supporting proof.

### FCR-001 — Gate approves regex model and undeclared effort

```json
{
  "finding_id": "FCR-001",
  "title": "Gate approves regex model and undeclared effort",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:purpose",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:authorizes/authorizes_effort",
    "stage-b/run_lanes_gated.sh:55-69"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:purpose",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:authorizes/authorizes_effort",
    "stage-b/run_lanes_gated.sh:55-69"
  ],
  "evidence_ids": [
    "owner-regex-qualify-only-isolated.txt",
    "owner-regex-full-isolated.txt",
    "effort-qualify-only-isolated.txt"
  ],
  "observed": "Qualify-only model=.* and undeclared effort return 0 / OWNER_AUTHORISED_DEVIATION / QUALIFICATION_PASSED. Full regex run returns 8 because child refuses 6.",
  "expected": "Literal exact role-scoped model AND effort authorization before any invocation; invalid request never receives qualification success.",
  "contradiction": "Qualify-only model=.* and undeclared effort return 0 / OWNER_AUTHORISED_DEVIATION / QUALIFICATION_PASSED. Full regex run returns 8 because child refuses 6.; expected Literal exact role-scoped model AND effort authorization before any invocation; invalid request never receives qualification success.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks routing closure.",
  "earliest_owner": "Gate admission",
  "smallest_repair_scope": "Share strict role/model/effort validation with child; test both qualify-only and full entry.",
  "retest_required": [
    "owner-regex-qualify-only-isolated.txt",
    "owner-regex-full-isolated.txt",
    "effort-qualify-only-isolated.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-002 — EXECUTE model exception authorizes VERIFY

```json
{
  "finding_id": "FCR-002",
  "title": "EXECUTE model exception authorizes VERIFY",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.VERIFY",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:EXECUTE/checker scope",
    "stage-b/run_lane.sh:130-163"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.VERIFY",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:EXECUTE/checker scope",
    "stage-b/run_lane.sh:130-163"
  ],
  "evidence_ids": [
    "other-role-owner-isolated.txt"
  ],
  "observed": "VERIFY using EXECUTE backup deepseek-v4-flash returns 0 / LANE_SET_OK; no checker exhaustion or GLM failover occurred.",
  "expected": "EXECUTE exception stays within EXECUTE; checker substitution uses separate owner ruling.",
  "contradiction": "VERIFY using EXECUTE backup deepseek-v4-flash returns 0 / LANE_SET_OK; no checker exhaustion or GLM failover occurred.; expected EXECUTE exception stays within EXECUTE; checker substitution uses separate owner ruling.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks routing closure.",
  "earliest_owner": "Gate and child owner readers",
  "smallest_repair_scope": "Enforce role-bound exception keys and exact values in both components.",
  "retest_required": [
    "other-role-owner-isolated.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-003 — Provider override reaches governed VERIFY worker

```json
{
  "finding_id": "FCR-003",
  "title": "Provider override reaches governed VERIFY worker",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.VERIFY.provider",
    "stage-b/run_lanes_gated.sh:55,77,136",
    "stage-b/run_lane.sh:124,163-173"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.VERIFY.provider",
    "stage-b/run_lanes_gated.sh:55,77,136",
    "stage-b/run_lane.sh:124,163-173"
  ],
  "evidence_ids": [
    "provider-override-isolated.txt"
  ],
  "observed": "LANE_PROVIDER=unassigned reaches worker stub model_provider=\"unassigned\"; gate prints assigned provider=openai yet returns 0.",
  "expected": "Pin assigned provider/full route tuple or explicit scoped exception.",
  "contradiction": "LANE_PROVIDER=unassigned reaches worker stub model_provider=\"unassigned\"; gate prints assigned provider=openai yet returns 0.; expected Pin assigned provider/full route tuple or explicit scoped exception.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks routing conformance; no real provider result inferred.",
  "earliest_owner": "Gate binding and child re-derivation",
  "smallest_repair_scope": "Validate provider at both entries and bind physical route parameters to qualification/receipt.",
  "retest_required": [
    "provider-override-isolated.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-004 — Windows junction bypasses gate log containment

```json
{
  "finding_id": "FCR-004",
  "title": "Windows junction bypasses gate log containment",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE"
  ],
  "acceptance_ids": [
    "user log/write boundary",
    "stage-b/run_lanes_gated.sh:33-41",
    "verify/harness/HARNESS_DEFECT_LOG.md:H1-H3"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "user log/write boundary",
    "stage-b/run_lanes_gated.sh:33-41",
    "verify/harness/HARNESS_DEFECT_LOG.md:H1-H3"
  ],
  "evidence_ids": [
    "gate-logdir-isolated.txt",
    "gate-junction.txt",
    "junction-readback.txt"
  ],
  "observed": "Direct in-tree parent refused 3; external parent/hgk-lanes junction to candidate clone returns 0, writing qualification log into gate-junction-target/ with untracked git status.",
  "expected": "Qualification logs physically outside candidate, including an existing log-directory junction.",
  "contradiction": "Direct in-tree parent refused 3; external parent/hgk-lanes junction to candidate clone returns 0, writing qualification log into gate-junction-target/ with untracked git status.; expected Qualification logs physically outside candidate, including an existing log-directory junction.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks handover closure.",
  "earliest_owner": "Gate containment",
  "smallest_repair_scope": "Resolve actual LOGDIR destination, validate before writing; handle missing path safely; add junction/direct positive-negative controls.",
  "retest_required": [
    "gate-logdir-isolated.txt",
    "gate-junction.txt",
    "junction-readback.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-005 — Protocol failure with incidental quota triggers checker switch

```json
{
  "finding_id": "FCR-005",
  "title": "Protocol failure with incidental quota triggers checker switch",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.does_not_trigger_on",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:Checker failover",
    "stage-b/run_checker_lane.sh:36,62-79"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.does_not_trigger_on",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:Checker failover",
    "stage-b/run_checker_lane.sh:36,62-79"
  ],
  "evidence_ids": [
    "checker-mixed-failure.txt"
  ],
  "observed": "Synthetic primary emits Provider error 400: invalid_request_error; quota mentioned in explanatory context, exits 1. Wrapper matches quota, switches to GLM backup, returns 0.",
  "expected": "Protocol 400 is reported without model switch; incidental exhaustion words cannot override prohibited failure class.",
  "contradiction": "Synthetic primary emits Provider error 400: invalid_request_error; quota mentioned in explanatory context, exits 1. Wrapper matches quota, switches to GLM backup, returns 0.; expected Protocol 400 is reported without model switch; incidental exhaustion words cannot override prohibited failure class.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks routing failover contract; all provider failures here synthetic.",
  "earliest_owner": "Checker failure classifier",
  "smallest_repair_scope": "Use typed failure/exhaustion reason with prohibited-class precedence; test mixed and incidental text.",
  "retest_required": [
    "checker-mixed-failure.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-006 — Checker returns success with dirty failover record

```json
{
  "finding_id": "FCR-006",
  "title": "Checker returns success with dirty failover record",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE"
  ],
  "acceptance_ids": [
    "user S4-STAGE-B-HANDOVER-CLOSURE",
    "verify/harness/HARNESS_DEFECT_LOG.md:H1",
    "stage-b/run_checker_lane.sh:86-108"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "user S4-STAGE-B-HANDOVER-CLOSURE",
    "verify/harness/HARNESS_DEFECT_LOG.md:H1",
    "stage-b/run_checker_lane.sh:86-108"
  ],
  "evidence_ids": [
    "checker-mixed-failure.txt"
  ],
  "observed": "Wrapper writes CHECKER_FAILOVER_AOCHECK.md after child POSTFLIGHT:dirty=0, returns 0; immediate status reports that record untracked.",
  "expected": "All wrapper artifacts included in final hygiene observation before success.",
  "contradiction": "Wrapper writes CHECKER_FAILOVER_AOCHECK.md after child POSTFLIGHT:dirty=0, returns 0; immediate status reports that record untracked.; expected All wrapper artifacts included in final hygiene observation before success.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks outer-wrapper handover closure.",
  "earliest_owner": "Outer checker lifecycle",
  "smallest_repair_scope": "Apply governed record-write/final postflight to outer wrapper with write-fault and success/failure probes.",
  "retest_required": [
    "checker-mixed-failure.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-007 — Historical evidence does not close current Stage-B binding

```json
{
  "finding_id": "FCR-007",
  "title": "Historical evidence does not close current Stage-B binding",
  "classification": "EVIDENCE_GAP",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "evidence/EVIDENCE_RETURN_PACK.json:frozen_subject/independent_checker/open_tt",
    "01_subject/FROZEN_SUBJECT.json",
    "skill exact-subject requirement"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "evidence/EVIDENCE_RETURN_PACK.json:frozen_subject/independent_checker/open_tt",
    "01_subject/FROZEN_SUBJECT.json",
    "skill exact-subject requirement"
  ],
  "evidence_ids": [
    "source-inventory.json",
    "freeze-digests.json",
    "candidate-archive.txt"
  ],
  "observed": "Frozen manifest names Stage-B 32962532b7b7176eafbd3d353ced63a3056027fb and independent_checker NOT_RUN. Reviewed HEAD differs; delivered wheel/ZIP are historical assets, not a validated current Stage-B package.",
  "expected": "Fresh current-subject acceptance evidence and explicit archive/distribution/manifest relationship.",
  "contradiction": "Frozen manifest names Stage-B 32962532b7b7176eafbd3d353ced63a3056027fb and independent_checker NOT_RUN. Reviewed HEAD differs; delivered wheel/ZIP are historical assets, not a validated current Stage-B package.; expected Fresh current-subject acceptance evidence and explicit archive/distribution/manifest relationship.",
  "reproducibility": "EVIDENCE_ONLY",
  "claim_impact": "Caps current aggregate closure; source-bound deterministic probes remain valid.",
  "earliest_owner": "Evidence publisher / acceptance owner",
  "smallest_repair_scope": "Produce a new current canonical index and independent scoped acceptance; retain historical pack unchanged.",
  "retest_required": [
    "source-inventory.json",
    "freeze-digests.json",
    "candidate-archive.txt"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-008 — Brief gate denominator differs from frozen raw results

```json
{
  "finding_id": "FCR-008",
  "title": "Brief gate denominator differs from frozen raw results",
  "classification": "NON_BLOCKING_OBSERVATION",
  "severity": "LOW",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "user maker count claim 32/0",
    "verify/harness/GATE_NEGATIVE_TEST_RESULTS.txt:last line"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "user maker count claim 32/0",
    "verify/harness/GATE_NEGATIVE_TEST_RESULTS.txt:last line"
  ],
  "evidence_ids": [
    "run_gate_negative_tests-isolated.txt",
    "source-inventory.json"
  ],
  "observed": "Frozen log and independent isolated run say RESULT pass=34 fail=0, exit 0; brief says 32/0. Other counts reproduce 38/0 and 14/0.",
  "expected": "Accurate current assertion denominator and source binding.",
  "contradiction": "Frozen log and independent isolated run say RESULT pass=34 fail=0, exit 0; brief says 32/0. Other counts reproduce 38/0 and 14/0.; expected Accurate current assertion denominator and source binding.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Nonblocking summary disagreement; assertions are not release acceptance.",
  "earliest_owner": "Claim summary publisher",
  "smallest_repair_scope": "Correct subsequent summary with exact log/commit; no code repair required.",
  "retest_required": [
    "run_gate_negative_tests-isolated.txt",
    "source-inventory.json"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "RESOLVED"
}
```

### FCR-009 — AO9 intake path missing at freeze and moved during review

```json
{
  "finding_id": "FCR-009",
  "title": "AO9 intake path missing at freeze and moved during review",
  "classification": "EVIDENCE_GAP",
  "severity": "LOW",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "intake raw_evidence AO9 locator",
    "frozen AO9 doubled path"
  ],
  "subject_identity": "35c5099debfad1fa7a11192de2495c6c359c06f8",
  "source_locators": [
    "intake raw_evidence AO9 locator",
    "frozen AO9 doubled path"
  ],
  "evidence_ids": [
    "ao9-frozen.txt",
    "ao9-actual-frozen-locator.txt",
    "delivery-boundary.json"
  ],
  "observed": "verify/ao9/AO9_LANE_STOPPED.md absent at frozen commit (128); verify/verify/ao9/AO9_LANE_STOPPED.md exists (0). End delivery status shows doubled-path deletion and corrected-path untracked file, outside reviewer writes.",
  "expected": "Declared locator resolves on frozen subject; concurrent correction is explicitly uncommitted evidence.",
  "contradiction": "verify/ao9/AO9_LANE_STOPPED.md absent at frozen commit (128); verify/verify/ao9/AO9_LANE_STOPPED.md exists (0). End delivery status shows doubled-path deletion and corrected-path untracked file, outside reviewer writes.; expected Declared locator resolves on frozen subject; concurrent correction is explicitly uncommitted evidence.",
  "reproducibility": "EVIDENCE_ONLY",
  "claim_impact": "Bounded history traceability gap, not evidence of any model verdict.",
  "earliest_owner": "Evidence index publisher",
  "smallest_repair_scope": "Correct a new index and freeze it; retain history; do not silently substitute later file.",
  "retest_required": [
    "ao9-frozen.txt",
    "ao9-actual-frozen-locator.txt",
    "delivery-boundary.json"
  ],
  "regression_required": [
    "three frozen harness suites and affected focused controls"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

## 6. Missing / quarantined evidence

| id | required for | reason | impact |
|---|---|---|---|
| CURRENT_MANIFEST | Aggregate current closure | Old commit and checker NOT_RUN | FCR-007 unresolved |
| CURRENT_DISTRIBUTION | Current package acceptance | Hashed release wheel/ZIP historical; tar is review snapshot | No release conformance inferred |
| MODEL_IDENTITY | Authenticated model routing | Stubs only by instruction | Cannot authenticate model identity |
| AO9_LOCATOR | Frozen history traceability | Doubled path, concurrent correction | FCR-009 |
| RUNTIME_HISTORY | Reliability/causal claim | Historical provider logs not replayed/authenticated | No real model/root-cause verdict |
| FULL_ACCEPTANCE | Product/release/domain edges | Excluded or absent | Public-release HOLD remains |

AO7 correction is corroborated: frozen receipt exists with child_exit=1 and qualified=yes. Old absence claim is struck out in corrected document; no current absence finding is inferred. Qualification describes admission, never work success. Current default ungated calls record no; historical receipt remains unchanged.

Initial status was measured after first review result and showed only freeze.txt; no pristine pre-review observation is claimed. End delivery HEAD/tree are unchanged; status has authorized AO10 outputs plus outside-set AO9 doubled-path deletion/corrected-path untracked file. Reviewer did not write or authenticate that concurrent move. No pristine-delivery, universal no-write or correctness claim is supported by these observations.

## 7. Internal Oracle disagreement

| predicate | Internal Oracle | External challenge | deterministic resolution | status |
|---|---|---|---|---|
| Current gate closure | No current Oracle receipt | FAIL_CHALLENGE | Reproduced contradictions | No Oracle/model debate |
| Maker six closures | Maker claim | Five focused old successes refused; qualify-only regex and junction survive | Independent current probes | Deterministically resolved |
| Suite count | Brief 38/0, 32/0, 14/0 | 38/0, 34/0, 14/0 | Current stored raw + independent run | Stale summary denominator |
| AO8 PARTIAL/B NOT_SUPPORTED | Historical external verdict, different subject | Several mechanisms persist; several repaired | Current frozen fixtures | Historical reasoning not copied |

No Meta-Oracle/HITL debate is needed for deterministic failures. Owner clarification would be needed if future policy intentionally broadens role/provider exceptions; permissive code is not that authorization.

## 8. Gate calibration defense

- objective alignment: finite checks target handover hygiene/admission, not product correctness or served-model identity.
- risk calibration: explicit role/model/provider and physical log containment are material boundaries; positive and negative controls exercised.
- negative/adversarial: prefix, regex, committed forged receipt, late HEAD, direct label, cross-role, provider, junction and mixed checker error. External fixtures, stub workers only.
- regression baseline: current frozen assertions 38/0, 34/0, 14/0; AO8 34/0 and 32/0 on different subject. Counts are assertions, not distinct mandatory gates.
- anti-overfitting: qualify-only avoids child protection; parent-only path check misses a junction; isolated checker categories miss mixed error text. New unseen anti-cases disconfirm broad closure.
- judge calibration: deterministic commands govern findings; no real LLM worker or judge launched.
- HITL/domain calibration: no production/domain authorization inferred; release HOLD remains.
- evaluator integrity: repair-diff.txt records gate/fixture changes against AO8-end commit. Those are candidate edits, not self-validating authority. No separately authenticated evaluator promotion receipt was located; none is claimed.

## 9. Verdict

`FAIL_CHALLENGE`

Both requested gates have confirmed blocking contradictions. Handover closure fails physical gate-log containment and outer-checker artifact lifecycle. Routing conformance fails qualify-only authorization, role exception scope, provider binding and prohibited checker failover. Finite repairs to old prefix/receipt/late-HEAD/default direct-label cases are supported. Current aggregate manifest/distribution acceptance remains unresolved. Verdict applies to frozen subject and finite executed scope.

## 10. Claim ceiling

- local/package: stubs establish finite harness control flow. Snapshot tar identified; historical asset hashes observed, not new Stage-B package acceptance.
- production: no BUILD_PASS, LOCAL_HOST_QUALIFIED, PORTAL_APPROVED, PUBLISHED, PRODUCTION_VERIFIED, PIPD_S4_FULL_PASS or production/deployment authorization. Public release remains FAIL-CLOSED / HOLD.
- live/external side effect: no model/provider call, broker write, deployment/publication/push or product suite.
- A stub proves control flow and nothing about a model; a clean git status is not code correctness; passing tests are not release acceptance; I cannot authenticate any model identity.

## 11. Recommended next route

`RESUME_SMALLEST_REPAIR`

FCR-001/002/003/004 belong to round-owned gate/child admission and physical containment; FCR-005/006 belong to checker classification/final evidence lifecycle. Limit repair to those components and focused external fixtures. Forbid unrelated core/product/release/authority edits and historical evidence rewrites. Frozen reviewed commit is rollback/checkpoint. Run mixed-error, role/provider, qualify-only and junction focused tests, affected three-suite regression and a fresh independent read-only recheck. Route FCR-007/009 separately to evidence owner for a new bound index. Challenger performs no repair or promotion.

## 12. External inspection list

Priority: findings.json; numbered-sources.txt; source-inventory.json; gate-junction.txt/junction-readback.txt; authorization/provider cases; checker-mixed-failure.txt; frozen historical manifest and AO9 locator. Orchestration-locators.json retains system-temp drivers/hashes. Reproducer result records provide shell setup/invocation; replay in a NEW external frozen clone, replace retained temp root, reset only that disposable clone, and explicitly set CODEX_BIN/GATE_BIN to executable stubs to prevent real-model launch.

Host/attempt disclosure: rg unavailable; initial round paths were located under .hgk/rounds. Native C:/ paths passed to MSYS mkdir caused first suite fixture failures: harness 5/33 exit 1, gate 3/31 exit 1, checker 6/8 exit 1. Unsuffixed raw results retained. POSIX /tmp shell paths plus removal of inherited path-conversion overrides allowed native Git/Python conversion; native orchestration/archive/clone arguments use Windows paths. Gate path retry still inherited lane settings (15/19 exit 1). Final isolated runs clear relevant LANE_/GATE_/ROUTE_/STUB_/FO_ settings and startup/path variables without environment dumps. First receipt-forgery probe was stopped by inherited model setting (6); isolated rerun reaches validation (8). Checker suite hardcoded shared temp LOGD was rebound to private temp in an external copy; all suite copies normalize line endings to LF, provenance hashes recorded. Candidate scripts unchanged, normalized frozen-object equivalence verified. A first long report-writing tool call did not start: Windows CreateProcessAsUserW error 206 (command too long); report creation was split into bounded calls. No output from that failed spawn supports a candidate claim.

NOT_EXECUTED / unfinished: real model/provider/route authentication; product tests; release rebuild/exact-set acceptance; domain/portal/deployment/publication/live systems; historical reliability repetitions/upstream causal hypotheses; full AO3-AO6 raw history; AO7 provider transcript/credential-content audit; newline filenames; initial BASH_ENV startup, GATE_PY override and exhaustive base/catalog/sandbox/env aliases; filesystem symlink/UNC/Unicode/case/junction combinations beyond single Windows junction; natural concurrent lanes/clock collisions/disk-full/ACL faults; full hooks/config/index/submodule/ignored-file audit; immutable receipt provenance/freshness; hostile lane/brief/token traversal. Known omitted-role and full fabricated-transcript limits reproduced, not claimed fixed. Work complete for finite probes; broader verification unfinished. Credential files/material and credential-material rules were not inspected or emitted; refer only to the credential-material rule (redacted). No provider refusal received or retried.

Raw excerpts below are verbatim saved result records. Complete earlier failures/retries/reset outputs remain in companion results and independent manifest. Local receipt stamp/token values are correlation IDs, not authentication credentials.

**prefix-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/prefix-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 6
RAW OUTPUT:
STAGED_OUTSIDE_ROUND_REFUSED: prefix/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_PREFIX_DONE
SUBJECT_EXIT=6
prefix/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt
```

**owner-regex-full-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/owner-regex-full-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 8
RAW OUTPUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
OWNER_AUTHORISED_DEVIATION model=.* effort=high assigned=opencode-go/deepseek-v4.1-flash/high record=OWNER_DECISION_MODEL_DEVIATION.md
QUALIFICATION_ROUTE style=catalog model=.* effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=.* effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=35c5099
REFUSED[6] model is not a plain identifier: env=.*
REFUSED_BRIEF_NT_A__DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=6
CHILD_RECEIPT_MISSING lane=BRIEF_NT_A_ token=20261012T144640Z-0 (absent, or not a non-empty regular file)
LANE_SET_FAILED children_ok=0 any_child_nonzero=1 missing_receipt=1 model=.* effort=high
SUBJECT_EXIT=8
```

**owner-regex-qualify-only-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/owner-regex-qualify-only-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
OWNER_AUTHORISED_DEVIATION model=.* effort=high assigned=opencode-go/deepseek-v4.1-flash/high record=OWNER_DECISION_MODEL_DEVIATION.md
QUALIFICATION_ROUTE style=catalog model=.* effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=.* effort=high consecutive_runs=1 route=catalog
GATE_QUALIFICATION_ONLY_OK role=EXECUTE model=.* effort=high
SUBJECT_EXIT=0
```

**forged-receipt-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/forged-receipt-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 8
RAW OUTPUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=35c5099
BRIEF_NT_A__LANE=20261012T144643Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/BRIEF_NT_A__20261012T144643Z.log
POSTFLIGHT:dirty=0 HEAD=4bd5bf3
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
CHILD_RECEIPT_INVALID lane=BRIEF_NT_A_ token=20261012T144643Z-0 failed: child_exit route model qualification
LANE_SET_FAILED children_ok=1 any_child_nonzero=0 missing_receipt=1 model=opencode-go/deepseek-v4.1-flash effort=high
SUBJECT_EXIT=8
lane=BRIEF_NT_A_
stamp=20261012T144643Z
token=20261012T144643Z-0
child_exit=0
model=wrong-model
route=catalog
qualified=no
child_exit=99
route=wrong
```

**gate-logdir-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/gate-logdir-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 3
RAW OUTPUT:
REFUSED[3] gate log dir resolves inside the worktree: /tmp/ao10-u9legwpj/subject/tmp-inside
GATE_REFUSED_NO_WRITERS_STARTED
SUBJECT_EXIT=3
```

**gate-junction.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:\\Users\\user\\AppData\\Local\\Temp\\ao10-u9legwpj\\gate-junction.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
GATE_QUALIFICATION_ONLY_OK role=EXECUTE model=opencode-go/deepseek-v4.1-flash effort=high
SUBJECT_EXIT=0
?? gate-junction-target/
gate-junction-target/qual-20261012T144911Z-75234-EXECUTE-r1-opencode-go_deepseek-v4.1-flash.log
```

**late-head-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/late-head-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 5
RAW OUTPUT:
PREFLIGHT_CLEAN HEAD=35c5099
LATE_LANE=20261012T144646Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
LATE exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/LATE_20261012T144646Z.log
POSTFLIGHT_DIRTY_REJECTED: 1 path(s) still untracked after every commit
POSTFLIGHT:dirty=1 HEAD=55c5e13
LATE_LANE_DONE
SUBJECT_EXIT=5
?? LATE_DIRT.txt
```

**direct-qualified-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/direct-qualified-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
PREFLIGHT_CLEAN HEAD=35c5099
DIRECT_LANE=20261012T144648Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
DIRECT exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/DIRECT_20261012T144648Z.log
POSTFLIGHT:dirty=0 HEAD=6f797bf
DIRECT_LANE_DONE
SUBJECT_EXIT=0
lane=DIRECT
stamp=20261012T144648Z
token=20261012T144648Z
child_exit=0
model=opencode-go/deepseek-v4.1-flash
route=openai
qualified=no
```

**other-role-owner-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/other-role-owner-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
ASSIGNMENT role=VERIFY model=gpt-6.1-sol provider=openai effort=medium route=openai
OWNER_AUTHORISED_DEVIATION model=opencode-go/deepseek-v4-flash effort=medium assigned=gpt-6.1-sol/medium record=OWNER_DECISION_MODEL_DEVIATION.md
QUALIFICATION_ROUTE style=openai model=opencode-go/deepseek-v4-flash effort=medium consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4-flash effort=medium consecutive_runs=1 route=openai
PREFLIGHT_CLEAN HEAD=35c5099
CHILD_OWNER_AUTHORISED_DEVIATION model=opencode-go/deepseek-v4-flash assignment=gpt-6.1-sol
BRIEF_NT_A__LANE=20261012T144651Z MODEL=opencode-go/deepseek-v4-flash provider=openai reasoning=medium route=openai (declared)
BRIEF_NT_A_ exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/BRIEF_NT_A__20261012T144651Z.log
POSTFLIGHT:dirty=0 HEAD=f750cce
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4-flash effort=medium route=openai
SUBJECT_EXIT=0
```

**provider-override-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/provider-override-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
ASSIGNMENT role=VERIFY model=gpt-6.1-sol provider=openai effort=medium route=openai
QUALIFICATION_ROUTE style=openai model=gpt-6.1-sol effort=medium consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=gpt-6.1-sol effort=medium consecutive_runs=1 route=openai
PREFLIGHT_CLEAN HEAD=35c5099
BRIEF_NT_A__LANE=20261012T144654Z MODEL=gpt-6.1-sol provider=unassigned reasoning=medium route=openai (declared)
BRIEF_NT_A_ exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/BRIEF_NT_A__20261012T144654Z.log
POSTFLIGHT:dirty=0 HEAD=b856cbf
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=gpt-6.1-sol effort=medium route=openai
SUBJECT_EXIT=0
stub argv=-m gpt-6.1-sol -c model_provider="unassigned" -c model_reasoning_effort="medium" exec --cd /tmp/ao10-u9legwpj/subject --sandbox workspace-write --skip-git-repo-check -
OpenAI Codex vSTUB
exec Q1 succeeded in 1ms:
exec Q2 succeeded in 1ms:
Q1_OK
Q2_OK
```

**effort-qualify-only-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/effort-qualify-only-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
OWNER_AUTHORISED_DEVIATION model=opencode-go/deepseek-v4-flash effort=unassigned assigned=opencode-go/deepseek-v4.1-flash/high record=OWNER_DECISION_MODEL_DEVIATION.md
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4-flash effort=unassigned consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4-flash effort=unassigned consecutive_runs=1 route=catalog
GATE_QUALIFICATION_ONLY_OK role=EXECUTE model=opencode-go/deepseek-v4-flash effort=unassigned
SUBJECT_EXIT=0
```

**role-omitted-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/role-omitted-isolated.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
PREFLIGHT_CLEAN HEAD=35c5099
OMIT_LANE=20261012T144657Z MODEL=unassigned provider=unassigned reasoning=unassigned route=openai (declared)
OMIT exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/OMIT_20261012T144657Z.log
POSTFLIGHT:dirty=0 HEAD=7636e1a
OMIT_LANE_DONE
SUBJECT_EXIT=0
stub argv=-m unassigned -c model_provider="unassigned" -c model_reasoning_effort="unassigned" exec --cd /tmp/ao10-u9legwpj/subject --sandbox workspace-write --skip-git-repo-check -
OpenAI Codex vSTUB
exec Q1 succeeded in 1ms:
exec Q2 succeeded in 1ms:
Q1_OK
Q2_OK
lane=OMIT
stamp=20261012T144657Z
token=20261012T144657Z
child_exit=0
model=unassigned
route=openai
qualified=no
```

**checker-primary-effort.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:\\Users\\user\\AppData\\Local\\Temp\\ao10-u9legwpj\\checker-primary-effort.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
CHECKER_PRIMARY lane=AOCHECK model=gpt-6.1-sol route=openai
PREFLIGHT_CLEAN HEAD=35c5099
AOCHECK_LANE=20261012T144812Z MODEL=gpt-6.1-sol provider=openai reasoning=medium route=openai (declared)
AOCHECK exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/AOCHECK_20261012T144812Z.log
POSTFLIGHT:dirty=0 HEAD=4e8e4f1
AOCHECK_LANE_DONE
CHECKER_PRIMARY_OK lane=AOCHECK stamp=20261012T144812Z
SUBJECT_EXIT=0
LANE=AOCHECK
MODEL=gpt-6.1-sol
PROVIDER=openai
EFFORT=medium
STAMP=20261012T144812Z
TOKEN=20261012T144812Z
WT=/tmp/ao10-u9legwpj/subject
ROUTE_STYLE=openai
SANDBOX=workspace-write
stub argv=-m gpt-6.1-sol -c model_provider="openai" -c model_reasoning_effort="medium" exec --cd /tmp/ao10-u9legwpj/subject --sandbox workspace-write --skip-git-repo-check -
```

**checker-mixed-failure.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:\\Users\\user\\AppData\\Local\\Temp\\ao10-u9legwpj\\checker-mixed-failure.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
CHECKER_PRIMARY lane=AOCHECK model=gpt-6.1-sol route=openai
PREFLIGHT_CLEAN HEAD=35c5099
AOCHECK_LANE=20261012T144814Z MODEL=gpt-6.1-sol provider=openai reasoning=medium route=openai (declared)
AOCHECK exit=1 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/AOCHECK_20261012T144814Z.log
POSTFLIGHT:dirty=0 HEAD=7365a5d
AOCHECK_LANE_DONE
CHECKER_PRIMARY_EXHAUSTED lane=AOCHECK exit=1 signature=[      1 quota;]
CHECKER_FAILOVER_START lane=AOCHECK model=opencode-go/glm-5.3-flash route=catalog
PREFLIGHT_CLEAN HEAD=7365a5d
AOCHECK_LANE=20261012T144818Z MODEL=opencode-go/glm-5.3-flash provider=opencode-go reasoning=medium route=catalog (declared)
AOCHECK exit=0 log=/tmp/ao10-u9legwpj/logs/hgk-lanes/AOCHECK_20261012T144818Z.log
POSTFLIGHT:dirty=0 HEAD=b3d37f2
AOCHECK_LANE_DONE
CHECKER_FAILOVER_RECORD /tmp/ao10-u9legwpj/subject/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/CHECKER_FAILOVER_AOCHECK.md
CHECKER_BACKUP_OK lane=AOCHECK stamp=20261012T144818Z
SUBJECT_EXIT=0
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/CHECKER_FAILOVER_AOCHECK.md
LANE=AOCHECK
MODEL=gpt-6.1-sol
PROVIDER=openai
EFFORT=medium
STAMP=20261012T144814Z
TOKEN=20261012T144814Z
WT=/tmp/ao10-u9legwpj/subject
ROUTE_STYLE=openai
SANDBOX=workspace-write
LANE=AOCHECK
MODEL=opencode-go/glm-5.3-flash
PROVIDER=opencode-go
EFFORT=medium
STAMP=20261012T144818Z
TOKEN=20261012T144818Z
WT=/tmp/ao10-u9legwpj/subject
ROUTE_STYLE=catalog
SANDBOX=workspace-write
Provider error 400: invalid_request_error; quota mentioned in explanatory context
backup stub success
# Checker failover record - AOCHECK

The owner's ruling of 2026-10-12: if the checker model GPT 6.1 SOL-MEDIUM (OpenAI OAuth) runs out
of quota, the checker model switches to the declared backup GLM-5.3-Flash (OPENCODE GO).

| | model | route | stamp | child exit | lane log |
|---|---|---|---|---|---|
| primary | `gpt-6.1-sol` | `openai` | `20261012T144814Z` | 1 | `/tmp/ao10-u9legwpj/logs/hgk-lanes/AOCHECK_20261012T144814Z.log` |
| backup  | `opencode-go/glm-5.3-flash` | `catalog` | `20261012T144818Z` | 0 | `/tmp/ao10-u9legwpj/logs/hgk-lanes/AOCHECK_20261012T144818Z.log` |

Exhaustion signature matched in the primary log: `      1 quota;`

**This changes the checker's identity.** Any verdict produced under the backup was produced by a
different model than the assigned checker, and the verdict document must say so. The failover does
not transfer, and does not create, any acceptance this round would not otherwise have.
```

**historical-ao7-receipt.txt**

```text
COMMAND: ["git", "show", "35c5099debfad1fa7a11192de2495c6c359c06f8:.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO7_20261012T135739Z.receipt"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
lane=AO7
stamp=20261012T135739Z
token=20261012T135739Z
child_exit=1
model=gpt-6.1-sol
route=openai
qualified=yes
```

**ao9-frozen.txt**

```text
COMMAND: ["git", "show", "35c5099debfad1fa7a11192de2495c6c359c06f8:.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao9/AO9_LANE_STOPPED.md"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 128
RAW OUTPUT:
fatal: path '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao9/AO9_LANE_STOPPED.md' does not exist in '35c5099debfad1fa7a11192de2495c6c359c06f8'
```

**ao9-actual-frozen-locator.txt**

```text
COMMAND: ["git", "show", "35c5099debfad1fa7a11192de2495c6c359c06f8:.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/verify/ao9/AO9_LANE_STOPPED.md"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
# AO9 lane stopped by the maker's own order - no verdict

- Primary checker `gpt-6.1-sol` (openai, OAuth, medium) **exhausted its quota** and the wrapper recorded it:
  `CHECKER_PRIMARY_EXHAUSTED lane=AO9 exit=1 signature=[      2 usage limit;]`.
- The declared backup `opencode-go/glm-5.3-flash` then started and was **stopped mid-run by the maker**
  (`termination_source: process.kill`, exit -15), on the owner's instruction that the GPT quota had
  recovered and that the checker lane must run on `gpt-6.1-sol` again.
- `verify/ao9/` therefore holds **no verdict**. Anything the backup attempt produced before it was stopped
  is partial and is not an adjudication.
- Consequence: round 9 has no verdict, exactly like round 7. Round 10 is dispatched through the canonical
  `fabric-external-independent-challenge-reviewer` lane on the primary checker.
```

**run_harness_negative_tests-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/run_harness_negative_tests.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
### T1 dirty preflight is refused (v1 passed this; regression guard)
PASS T1_DIRTY_REFUSED (exit=2)
PASS T1_says_refused
### T2 missing brief: D1a - refuse BEFORE launch, never fail open
PASS T2_MISSING_BRIEF_REFUSED (exit=3)
PASS T2_no_lane_log_written
PASS T2_child_never_launched
### T3 successful run: log really copied in, commit says so, no stray root dir (D3)
PASS T3_STUB_SUCCESS (exit=0)
PASS T3_log_copied_in
PASS T3_commit_states_copy
PASS T3_per_launch_receipt_written
PASS D3_no_output_dir_at_repo_root
PASS D3_output_dir_is_round_relative
### T4 postflight dirt is REJECTED, not merely printed (D2)
PASS T4_POSTFLIGHT_DIRT_REJECTED (exit=5)
PASS T4_dirt_was_detected
### T5 a non-zero child is propagated, never advertised as success
PASS T5_CHILD_EXIT_PROPAGATED (exit=7)
PASS T5_lane_reports_done
### T6 TMPDIR resolving inside the worktree is refused (F)
PASS T6_TMPDIR_INSIDE_REFUSED (exit=3)
### T7 a failed receipt copy is fatal, not a note (R1)
PASS T7_RECEIPT_COPY_FATAL (exit=6)
PASS T7_names_the_receipt
### T8 a FAILED git status is not a clean worktree (R2)
PASS T8_STATUS_FAILURE_REFUSED (exit=2)
PASS T8_says_status_failed
PASS T8_child_never_launched
### T9 an already staged OUTSIDE-round file is refused (R3)
PASS T9_STAGED_OUTSIDE_REFUSED (exit=6)
PASS T9_names_the_outside_path
PASS T9_outside_file_was_not_committed
### T10 the manifest is really copied into the round (M1)
PASS T10_MANIFEST_RUN (exit=0)
PASS T10_manifest_present_in_round
### T11 a regex-spelling alias of the round is refused (M2)
PASS T11_ALIAS_PREFIX_REFUSED (exit=6)
PASS T11_names_the_outside_path
### T12 a FAILED index enumeration is refused, not read as nothing staged (M3)
PASS T12_STAGED_QUERY_FAILURE_REFUSED (exit=6)
PASS T12_names_the_query
### T13 dirt created by the final commit is detected (M4)
PASS T13_POST_COMMIT_DIRT_REJECTED (exit=5)
PASS T13_names_the_dirt
### T14 a route that disagrees with the assignment is refused (M7)
PASS T14_ROUTE_MISMATCH_REFUSED (exit=6)
PASS T14_names_the_mismatch
### P1 a PREFIX spelling of the round is refused (round-8 smallest counterexample)
PASS P1_PREFIX_SUBSTRING_REFUSED (exit=6)
PASS P1_names_the_outside_path
### P2 a regex-shaped model value must not authorise itself (round-8)
PASS P2_REGEX_MODEL_REFUSED (exit=6)
PASS P2_names_the_reason

RESULT pass=38 fail=0
```

**run_gate_negative_tests-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/run_gate_negative_tests.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
### G1 a deviating model with NO owner record is refused, zero writers
PASS G1_DEVIATION_REFUSED (exit=6)
PASS G1_names_the_decision
PASS G1_started_no_writer
PASS G1_no_writer_ran
### G2 the SAME deviating model, now named in the owner record, is admitted
PASS G2_AUTHORISED_DEVIATION_RUNS (exit=0)
PASS G2_records_the_deviation
PASS G2_lane_set_ok
### G3 a model that cannot survive qualification is refused before any writer
PASS G3_QUALIFICATION_REFUSED (exit=7)
PASS G3_names_qualification
PASS G3_started_no_writer
### G4 children exiting 0,1,0 must aggregate to a failed lane set
PASS G4_LANE_SET_FAILED (exit=8)
PASS G4_says_nonzero
PASS G4_counts_the_failure
### G5 a child that loses its run receipt is a failure even if it exited 0
PASS G5_MISSING_RECEIPT_FAILS (exit=8)
PASS G5_names_missing_receipt
### G6 an unknown role is refused
PASS G6_UNKNOWN_ROLE_REFUSED (exit=3)
### G7 the assignment model with a working qualification passes end to end
PASS G7_HAPPY_PATH (exit=0)
PASS G7_qualification_passed
PASS G7_no_deviation_notice
### G8 zero qualification attempts must NOT be advertised as a qualified lane (R4)
PASS G8_ZERO_RUNS_REFUSED (exit=3)
PASS G8_says_refused
PASS G8_did_not_claim_qualified
### G9 the writer must be launched through the route that was qualified (R5)
PASS G9_EXECUTE_RUNS (exit=0)
PASS G9_child_used_the_catalog_slug
PASS G9_child_did_not_use_a_provider_id
PASS G9_qualification_and_writer_agree
### G10 a truncated / empty receipt must not satisfy the gate (M6)
PASS G10_EMPTY_RECEIPT_REJECTED (exit=8)
PASS G10_says_receipt_rejected
### G11 GATE_SKIP_QUALIFY without an acknowledgement is refused (M8)
PASS G11_SKIP_UNAUTHORISED_REFUSED (exit=6)
PASS G11_names_the_ack
### G12 sentinels without tool executions are not a qualification (M9)
PASS G12_SENTINELS_ONLY_REFUSED (exit=7)
PASS G12_names_qualification
### G13 a committed receipt with duplicated conflicting fields is refused (round-8)
PASS G13_CONFLICTING_RECEIPT_REJECTED (exit=8)
PASS G13_names_the_receipt

RESULT pass=34 fail=0
```

**run_checker_failover_tests-isolated.txt**

```text
COMMAND: ["C:/Program Files/Git/usr/bin/bash.exe", "C:/Users/user/AppData/Local/Temp/ao10-u9legwpj/run_checker_failover_tests.sh"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
### A1 a provider content-filter kill must NOT be worked around by a model switch
PASS A1_nonzero_exit (exit=1)
PASS A1_says_not_exhaustion
PASS A1_did_not_fail_over
PASS A1_no_backup_ok
### A2 a protocol 400 must NOT be worked around by a model switch
PASS B2_says_not_exhaustion
PASS B2_did_not_fail_over
### A3 an exhaustion signal DOES fail over, and records both models
PASS A3_exit_zero (exit=0)
PASS A3_exhaustion_seen
PASS A3_failover_started
PASS A3_backup_ok
PASS A3_record_names_backup
PASS A3_record_names_primary
PASS A3_record_says_identity_changes
PASS A3_no_record_for_the_killed_lane_unneeded
RESULT pass=14 fail=0
```

**skill-self-test.txt**

```text
COMMAND: ["python", "C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\scripts\\verify_review_bundle.py", "--self-test"]
CWD: C:\Users\user\AppData\Local\Temp\ao10-u9legwpj\subject
EXIT_CODE: 0
RAW OUTPUT:
{

  "status": "PASS",

  "skill_sha256": "8125d1c6911397e2183e3f1f436a6df08692a8447b52f704b5c5e17481fca71c",

  "intake_errors": [],

  "report_errors": []

}
```

**skill-unit-tests.txt**

```text
COMMAND: ["python", "-m", "unittest", "tests/test_verify_review_bundle.py"]
CWD: C:\Users\user\.agents\skills\fabric-external-independent-challenge-reviewer
EXIT_CODE: 0
RAW OUTPUT:
....

----------------------------------------------------------------------

Ran 4 tests in 0.014s



OK
```

## 13. Readback

- report path: verify/ao10/EXTERNAL_CHALLENGE_REPORT.md relative to named round.
- bytes and sha256: exact final report byte count/digest recorded in report-readback.json. Embedding a full-file digest in itself is self-referential; independently verify sidecar with hashlib.sha256(report.read_bytes()).
- readback status: final report read back; exactly thirteen template headings checked; final report and completed intake validated by bundled validator. REVIEW_EVIDENCE_MANIFEST.json excludes report/intake/validator/readback to avoid digest cycles and binds candidate_commit.

```text
COMMAND: ["python", "C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\scripts\\verify_review_bundle.py", "--intake", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepair-recheck-and-triple-upgrade\\verify\\ao10\\EXTERNAL_CHALLENGE_INTAKE.json", "--report", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepair-recheck-and-triple-upgrade\\verify\\ao10\\EXTERNAL_CHALLENGE_REPORT.md"]
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
{
  "status": "PASS",
  "errors": []
}
```
