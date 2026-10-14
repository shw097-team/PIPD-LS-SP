# EXTERNAL_CHALLENGE_REPORT

## 1. Review identity

- review_id: FCR-REVIEW-S4POST-AO12; external clean-room challenger using fabric-external-independent-challenge-reviewer; reviewed 2026-10-12T16:09:04.540726+00:00 (2026-10-13 Asia/Taipei).
- project/task: PIPD-LS-SP / S4-UX-DISTRIBUTION-UPGRADE-R1; round S4POST-20261012-postrepair-recheck-and-triple-upgrade. Gates: S4-STAGE-B-HANDOVER-CLOSURE, S4-MODEL-ROUTING-CONFORMANCE, FCR-001..006 and round-11 repairs.
- candidate commit `2fc17c0a3250ff0b86021f908c5b6ec8bd64886e`; tree `f9007333681c902b09ff9bfb30246448831ddbd5`; archive SHA-256 `ea89eb85df349467f05216236429de534d31c4850ae0a8cf7672297e64a56eec`. `git archive --format=tar --output=<temp>/candidate.tar 2fc17c0a3250ff0b86021f908c5b6ec8bd64886e`: exit 0, stdout/stderr empty. Review snapshot, not release build.
- evidence manifest SHA-256 `2e5a1d19e80ba8759c07c6d1e4b085d3d3ebf67988f1e269965b0266adcfbbe9`; internal historical subject quarantined for current acceptance.
- historical mount ZIP SHA-256 `af342d281f02ba04f284a1625f4a58a6f2de15549cc182a0c61ce357ec6b504f`; wheel `e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec`. Current Stage-B association unproven.
- Internal Oracle: NO_INTERNAL_ORACLE_IN_THIS_ROUND; package digest not applicable. Prior officers are evidence sources, not this run's authority.
- external workspace `C:\Users\user\AppData\Local\Temp\ao12-roo_vkak`. Every clone, fixture, stub, raw log and replay script lives in system temp. Delivery writes exclusively verify/ao12. No candidate stage/commit/tag/push/merge or edit. Git commits/hooks used only in disposable fixtures.
- FROZEN_TRACKED_SHA256.json binds 2,635 initial readable tracked files. Final HEAD/tree and byte comparison found no tracked change outside verify/ao12. Intake completion is authorized there. No real model or product test suite launched.

## 2. Authority/source inventory

| item | role | locator / binding | disposition |
|---|---|---|---|
| User review scope | NORMATIVE | dispatch and hard boundaries | Current review authority |
| Installed reviewer skill | NORMATIVE | C:/Users/user/.agents/skills/fabric-external-independent-challenge-reviewer/SKILL.md and references | Read; bundled checks rerun |
| Assignment | NORMATIVE | stage-b/ROUND_ASSIGNMENT.json | Role tuple, complete route and failover rules |
| Owner ruling | NORMATIVE | stage-b/OWNER_DECISION_MODEL_DEVIATION.md:3-18,29-40 | Exact role/axis values; exhaustion-only switch |
| Own freeze | STATE / RAW_EVIDENCE | FREEZE.json; tracked inventory; external candidate.tar | Bound independently |
| Existing pack | STATE / SUMMARY_CLAIM | evidence/EVIDENCE_RETURN_PACK.json:5-12,18,48 | Historical binding, quarantined |
| Closure/repair reports | SUMMARY_CLAIM | ACCEPTANCE_RECORD_STAGEB.md; HARNESS_DEFECT_LOG.md; QUALIFICATION_FINDINGS.md | Inspected; PASS not adopted |
| Earlier external rounds | SUMMARY_CLAIM / historical evidence | AO10 report; AO11_LANE_FAILURE.md | Older subjects; AO11 has no verdict |
| Current executable code | RAW_EVIDENCE | temp SOURCE_INVENTORY.json; repair-diff.txt; numbered sources | Git blobs, checkout and full clone match after CRLF/LF normalization |

Executable comments are promises, not replacement owner authority. Findings tie predicates to assignment, ruling, user boundary or exact-subject workflow. No RP-002 gate aliases or production authority are invented.

## 3. Evidence inventory

| evidence | type | raw pointer (temp unless marked round) | binding / disposition |
|---|---|---|---|
| Freeze / boundary | STATE / RAW_EVIDENCE | round verify/ao12/FREEZE.json; FINAL_BOUNDARY.json | Exact head/tree, tracked-byte comparison |
| Frozen suite results | RAW_EVIDENCE | round verify/harness/*TEST_RESULTS.txt | Actual files read: 38/0,52/0,27/0; historical exit provenance not independently attested |
| Fresh suite replay | RAW_EVIDENCE | SUITE_RESULTS.json; run_*tests.sh.stdout.txt/.stderr.txt | Frozen code in disposable full clones; 39/0,52/0,27/0, each exit 0 |
| Focused challenges | RAW_EVIDENCE | RESULTS.json; <CASE>/result.json, stdout.txt, stderr.txt | 37 independent fixtures, copied frozen bytes and authority |
| Real junctions | RAW_EVIDENCE | <JUNCTION_CASE>/junction-proof.json | Native mklink /J exit, realpath, alias-log reachability proof |
| Reproducer readback | RAW_EVIDENCE | REPRODUCER_READBACK.json | Fresh-temp status-failure counterexample reproduced |
| Source identity | RAW_EVIDENCE | SOURCE_INVENTORY.json; repair-diff-command.json / repair-diff.txt | Exact blob/checkouts, normalized matches; raw hashes distinct |
| Skill checks | RAW_EVIDENCE | SELF_TEST.json; SKILL_UNIT_TESTS.json | Both exit 0; four skill unit tests |
| Prior AO11 | historical evidence / SUMMARY_CLAIM | round verify/ao11/AO11_LANE_FAILURE.md | No current verdict adopted |

Frozen artifact final lines, verbatim (filenames outside fences identify source):

LAUNCHER_TEST_RESULTS.txt:
```text
RESULT pass=38 fail=0
```
GATE_NEGATIVE_TEST_RESULTS.txt:
```text
RESULT pass=52 fail=0
```
CHECKER_FAILOVER_TEST_RESULTS.txt:
```text
RESULT pass=27 fail=0
```
Independent replay final lines / actual exits:

run_harness_negative_tests.sh:
```text
EXIT_CODE: 0
RESULT pass=39 fail=0
```

run_gate_negative_tests.sh:
```text
EXIT_CODE: 0
RESULT pass=52 fail=0
```

run_checker_failover_tests.sh:
```text
EXIT_CODE: 0
RESULT pass=27 fail=0
```

Counts are assertions, not scenarios. NT6_names_the_containment is in the current launcher suite but absent in frozen result output, explaining 39 vs 38. Gate G15 names containment and excludes resolution failure; G16 names missing role; G17 names undecided containment. A6 has a tracked hard-refusal record. These narrow positives do not cover the findings below.

CODEX_BIN/GATE_BIN are explicitly stubs everywhere. Qualification transcript output is fabricated; it proves no actual tool/model execution. Minimal focused repos copy frozen stage-b authority/code; suite repos clone frozen HEAD. Lexical-pwd and git-status failures are explicitly injected where labeled. No provider call or safety refusal occurred in this review; historical hostile notices are cited by locator and not retried.

Initial suite attempts returned exit 9 and raw CLONE_FAILED because source gitdir ownership was dubious. Exact command-scoped safe.directory for C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt allowed a read-only full-subject clone. No global Git configuration changed; suites cloned the sandbox-owned frozen source. Initial receipts remain at initial-suite-attempt/. Temp checker suite LOGD was rebound from its hard-coded path; other suites use NT_BASE. Code/evaluators in candidate were never changed.

## 4. Challenge matrix

| predicate | expected | independent counter-check | adjudication |
|---|---|---|---|
| FCR-001 literal model/effort | Regex and unruled effort refused | Gate and child exit 6, zero calls; exact owner positive exit 0 | Supported finite repair |
| FCR-002 role crossing | EXECUTE line cannot authorize VERIFY | Gate/child role-cross exit 6, model reason, zero calls | Supported finite repair |
| FCR-003 provider + complete route | Govern every axis | Provider override refused 6; unruled catalog/endpoint reaches worker at exit 0 | Provider repaired; full route FAIL |
| FCR-004 containment | No in-tree logs / unknown admission | Real junction and resolver-failure branches refuse 3, zero worker calls/logs; directory precreation remains | Admission repaired; bounded side effect OPEN |
| FCR-005 HTTP400/malformed payload | No incidental-quota switch | HTTP400_MIXED exit 1, one call, tracked hard-refusal record | A6 finite repair supported |
| FCR-005 trusted error channel | Reviewed quotations cannot authorize | QUOTED_ERROR_REAL_HARD and TAIL_QUOTE_CONTROLFAIL each switch and exit 0 | FAIL |
| FCR-006 wrapper completion | Final checks must be verified | Normal record tracked/clean; injected status failure hides fresh dirt and exits 0 | A5 finite repair supported; broader hygiene FAIL |
| G14a-e | Literal role/axis check plus admission control | Independent gate/child controls and full 52/0 replay | Finite controls supported |
| G15/G17 | Assert containment, not incidental refusal | Actual junction alias-log proof; OS branch forced by labeled lexical-pwd injection; outside resolver failures tested too | Refusal reasons match containment |
| G16 omitted LANE_ROLE | No assignment bypass | Unroled tuple refuses 3, missing-role reason, zero calls | Supported finite repair |
| Child defaults / route | Assignment governs all defaults | EXECUTE/VERIFY correct argv; explicit unruled style refuses 6; default EXECUTE receipt has wrong route | Invocation repaired; record defect FCR-010 |
| A4/A5/A6 | Hard refusal and committed failover | Independent mixed HTTP400 and capacity controls; full 27/0 replay | Finite controls supported |
| 429 positive calibration | Owner exhaustion backup | HTTP429 hard veto, one call, exit 1 | FCR-009 bounded defect |
| Current Stage-B aggregate | Exact manifest/receipt binding | Historical manifest differs from own HEAD/tree | FCR-007 OPEN |
| Known open limits | No proxy elevation | Transcript can be stubbed; newline not tested; CR-IDENTITY-BIND and CR-EXT-UNREVIEWED remain open | Ceiling retained |

Current shell pwd -P resolved native junctions in ordinary cases. Those ordinary junction+failing-resolver cases short-circuited lexically and do NOT prove OS fail-closed logic. Separate OS cases explicitly force lexical pwd behavior, retaining an actual junction, to reach the realpath/undecided branch. Both gate and child then refuse on the intended containment reason. Junction-proof.json records that an independently written alias log really reaches the fixture worktree; current governed lane logs do not appear because admission refuses.

## 5. Findings

FCR-001/002 are resolved for tested finite cases on this exact subject. FCR-003..006 retain lineage while separating supported narrow repairs from residual findings. All findings below use the skill schema; FINDINGS.json duplicates these records. Source locators refer to frozen HEAD. Evidence IDs are temp-relative except own freeze/dispatch files in verify/ao12.

### FCR-003 — Complete catalog route escapes owner authorization

```json
{
  "finding_id": "FCR-003",
  "title": "Complete catalog route escapes owner authorization",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.EXECUTE.route",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:3-7"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.EXECUTE.route",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:3-7",
    "stage-b/run_lane.sh:194-209"
  ],
  "evidence_ids": [
    "CHILD_UNRULED_ENDPOINT/result.json"
  ],
  "observed": "Assigned EXECUTE tuple plus catalog style reaches stub with an unruled base URL and catalog file; exit 0. Style alone is compared; parameters come from environment.",
  "expected": "Complete governed route follows assignment or exact owner ruling.",
  "contradiction": "Assigned EXECUTE tuple plus catalog style reaches stub with an unruled base URL and catalog file; exit 0. Style alone is compared; parameters come from environment. Expected: Complete governed route follows assignment or exact owner ruling.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Blocks full routing conformance; no actual network call or model identity is claimed.",
  "earliest_owner": "Child route construction",
  "smallest_repair_scope": "Validate catalog/base_url and preserve separately authorized checker backup route.",
  "retest_required": [
    "CHILD_UNRULED_ENDPOINT/result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-004 — In-tree directory created before containment refusal

```json
{
  "finding_id": "FCR-004",
  "title": "In-tree directory created before containment refusal",
  "classification": "CONFIRMED_DEFECT",
  "severity": "MEDIUM",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "user boundary: logs/fixtures outside candidate",
    "stage-b/run_lanes_gated.sh:34-59"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "user boundary: logs/fixtures outside candidate",
    "stage-b/run_lanes_gated.sh:34-59",
    "stage-b/run_lane.sh:88-109"
  ],
  "evidence_ids": [
    "CHILD_JUNCTION/result.json",
    "GATE_OS_JUNCTION/result.json",
    "CHILD_OS_JUNCTION/result.json",
    "GATE_OS_UNDECIDED_JUNCTION/result.json",
    "CHILD_OS_UNDECIDED_JUNCTION/result.json"
  ],
  "observed": "Actual native junctions confirmed by alias-log writes. All current tests refuse containment, exit 3, zero worker calls and lane logs. Child mkdir already creates in-tree hgk-lanes; gate does too with explicitly injected lexical pwd behavior.",
  "expected": "Containment admission precedes directory creation; unknown physical containment refuses before writes.",
  "contradiction": "Actual native junctions confirmed by alias-log writes. All current tests refuse containment, exit 3, zero worker calls and lane logs. Child mkdir already creates in-tree hgk-lanes; gate does too with explicitly injected lexical pwd behavior. Expected: Containment admission precedes directory creation; unknown physical containment refuses before writes.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Old successful log-write bypass is not reproduced; bounded side effect remains.",
  "earliest_owner": "Gate and child preflight",
  "smallest_repair_scope": "Check proposed physical destination before mkdir, then verify created destination; cover both entrypoints.",
  "retest_required": [
    "CHILD_JUNCTION/result.json",
    "GATE_OS_JUNCTION/result.json",
    "CHILD_OS_JUNCTION/result.json",
    "GATE_OS_UNDECIDED_JUNCTION/result.json",
    "CHILD_OS_UNDECIDED_JUNCTION/result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-005 — Quoted error prefix and tail text cause unauthorized failover

```json
{
  "finding_id": "FCR-005",
  "title": "Quoted error prefix and tail text cause unauthorized failover",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.does_not_trigger_on",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:29-34"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.does_not_trigger_on",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:29-34",
    "stage-b/run_checker_lane.sh:85-125"
  ],
  "evidence_ids": [
    "QUOTED_ERROR_REAL_HARD/result.json",
    "TAIL_QUOTE_CONTROLFAIL/result.json",
    "QUOTED_ERROR_BLOCKS_QUOTA/result.json"
  ],
  "observed": "Quoted tool-output ERROR line selected while terminal Provider error line omitted: backup invoked and exit 0. Tail fallback uses quoted quota after child control-flow exit 7: backup invoked and exit 0. Quoted hard ERROR also suppresses terminal quota.",
  "expected": "Only terminal primary-provider exhaustion can switch checker; hard/control-flow failure cannot be turned green.",
  "contradiction": "Quoted tool-output ERROR line selected while terminal Provider error line omitted: backup invoked and exit 0. Tail fallback uses quoted quota after child control-flow exit 7: backup invoked and exit 0. Quoted hard ERROR also suppresses terminal quota. Expected: Only terminal primary-provider exhaustion can switch checker; hard/control-flow failure cannot be turned green.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Reopens FCR-005 despite A4/A6 passing.",
  "earliest_owner": "Checker terminal classification",
  "smallest_repair_scope": "Use trusted terminal provider event/channel with provenance; no whole-tail authorization; separate transport recovery.",
  "retest_required": [
    "QUOTED_ERROR_REAL_HARD/result.json",
    "TAIL_QUOTE_CONTROLFAIL/result.json",
    "QUOTED_ERROR_BLOCKS_QUOTA/result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-006 — Failed wrapper status query is treated as clean

```json
{
  "finding_id": "FCR-006",
  "title": "Failed wrapper status query is treated as clean",
  "classification": "CONFIRMED_DEFECT",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "ACCEPTANCE_RECORD_STAGEB.md:127-141",
    "stage-b/run_lane.sh:16-17"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "ACCEPTANCE_RECORD_STAGEB.md:127-141",
    "stage-b/run_lane.sh:16-17",
    "stage-b/run_checker_lane.sh:46-57"
  ],
  "evidence_ids": [
    "WRAPPER_STATUS_FAILURE/result.json",
    "REPRODUCER_READBACK.json"
  ],
  "observed": "External hook writes dirt on wrapper record commit; injected git -C status returns 128/empty. Wrapper says record committed and backup OK, exit 0. Independent native status exits 0 and shows AO12_RECORD_DIRT.txt. Fresh-temp replay reproduces it.",
  "expected": "Failed final cleanliness query is unverifiable, never clean.",
  "contradiction": "External hook writes dirt on wrapper record commit; injected git -C status returns 128/empty. Wrapper says record committed and backup OK, exit 0. Independent native status exits 0 and shows AO12_RECORD_DIRT.txt. Fresh-temp replay reproduces it. Expected: Failed final cleanliness query is unverifiable, never clean.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Reopens FCR-006; record tracked but cleanliness falsely accepted.",
  "earliest_owner": "Checker commit_record",
  "smallest_repair_scope": "Check add/commit/status exit codes and staged scope; port child postflight invariants to wrapper.",
  "retest_required": [
    "WRAPPER_STATUS_FAILURE/result.json",
    "REPRODUCER_READBACK.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-007 — Current Stage-B binding is stale

```json
{
  "finding_id": "FCR-007",
  "title": "Current Stage-B binding is stale",
  "classification": "EVIDENCE_GAP",
  "severity": "HIGH",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "skill exact-subject-binding invariant",
    "evidence/EVIDENCE_RETURN_PACK.json:5-12,18,48-50"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "skill exact-subject-binding invariant",
    "evidence/EVIDENCE_RETURN_PACK.json:5-12,18,48-50"
  ],
  "evidence_ids": [
    "FREEZE.json",
    "SOURCE_INVENTORY.json"
  ],
  "observed": "Manifest commit 32962532b7b7176eafbd3d353ced63a3056027fb / tree 40b9507a97eea29cdc20f55e69cedb34ee8e2302 differ from freeze; verifier remains pending/NOT_RUN. Current distribution association unproven.",
  "expected": "Current aggregate acceptance requires manifest and independent receipt bound to exact subject.",
  "contradiction": "Manifest commit 32962532b7b7176eafbd3d353ced63a3056027fb / tree 40b9507a97eea29cdc20f55e69cedb34ee8e2302 differ from freeze; verifier remains pending/NOT_RUN. Current distribution association unproven. Expected: Current aggregate acceptance requires manifest and independent receipt bound to exact subject.",
  "reproducibility": "EVIDENCE_ONLY",
  "claim_impact": "Known open; alone caps review at PARTIAL_CHALLENGE.",
  "earliest_owner": "Evidence binding / acceptance owner",
  "smallest_repair_scope": "Separately govern current manifest/receipt without overwriting historical evidence.",
  "retest_required": [
    "FREEZE.json",
    "SOURCE_INVENTORY.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-008 — Dispatch counts and intake disagree with artifacts

```json
{
  "finding_id": "FCR-008",
  "title": "Dispatch counts and intake disagree with artifacts",
  "classification": "NON_BLOCKING_OBSERVATION",
  "severity": "LOW",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "user dispatch: report artifact disagreement",
    "verify/harness/LAUNCHER_TEST_RESULTS.txt:final RESULT"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "user dispatch: report artifact disagreement",
    "verify/harness/LAUNCHER_TEST_RESULTS.txt:final RESULT",
    "verify/ao12/INTAKE_AT_DISPATCH.json:candidate,freeze_method"
  ],
  "evidence_ids": [
    "INTAKE_AT_DISPATCH.json",
    "run_harness_negative_tests.sh.result.json"
  ],
  "observed": "Dispatch 39/0 and empty digests conflict with frozen artifact 38/0 and populated AO11 identity. Fresh replay returns 39/0; NT6 containment assertion absent from frozen result explains difference.",
  "expected": "Preserve original metadata and independently bind current subject/counts.",
  "contradiction": "Dispatch 39/0 and empty digests conflict with frozen artifact 38/0 and populated AO11 identity. Fresh replay returns 39/0; NT6 containment assertion absent from frozen result explains difference. Expected: Preserve original metadata and independently bind current subject/counts.",
  "reproducibility": "EVIDENCE_ONLY",
  "claim_impact": "Non-blocking discrepancy; current intake rebound independently.",
  "earliest_owner": "Dispatch / evidence packaging",
  "smallest_repair_scope": "Refresh metadata/results in a maker change; retain originals.",
  "retest_required": [
    "INTAKE_AT_DISPATCH.json",
    "run_harness_negative_tests.sh.result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-009 — Hard-4xx regex vetoes authorized HTTP429 exhaustion

```json
{
  "finding_id": "FCR-009",
  "title": "Hard-4xx regex vetoes authorized HTTP429 exhaustion",
  "classification": "CONFIRMED_DEFECT",
  "severity": "MEDIUM",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.trigger",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:29-34"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:checker_failover.trigger",
    "stage-b/OWNER_DECISION_MODEL_DEVIATION.md:29-34",
    "stage-b/run_checker_lane.sh:35-39,103-118"
  ],
  "evidence_ids": [
    "HTTP429_EXHAUSTION/result.json",
    "RECOVERED_HTTP426_QUOTA/result.json"
  ],
  "observed": "Explicit terminal HTTP429/rate-limit matches both patterns; hard veto wins, exit 1, one worker call. Tested recovered HTTP426 spelling followed by terminal capacity is also vetoed.",
  "expected": "429 exhaustion triggers owner backup; recovered transport notice must not override terminal cause.",
  "contradiction": "Explicit terminal HTTP429/rate-limit matches both patterns; hard veto wins, exit 1, one worker call. Tested recovered HTTP426 spelling followed by terminal capacity is also vetoed. Expected: 429 exhaustion triggers owner backup; recovered transport notice must not override terminal cause.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Bounded availability and positive-calibration failure.",
  "earliest_owner": "Checker hard-failure classification",
  "smallest_repair_scope": "Separate terminal hard protocol failure, exhaustion and recovered transport; retain 400 negative controls.",
  "retest_required": [
    "HTTP429_EXHAUSTION/result.json",
    "RECOVERED_HTTP426_QUOTA/result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### FCR-010 — Default catalog invocation has openai receipt

```json
{
  "finding_id": "FCR-010",
  "title": "Default catalog invocation has openai receipt",
  "classification": "CONFIRMED_DEFECT",
  "severity": "MEDIUM",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.EXECUTE.route",
    "stage-b/run_lane.sh:138-150,204-209,255-256"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "stage-b/ROUND_ASSIGNMENT.json:roles.EXECUTE.route",
    "stage-b/run_lane.sh:138-150,204-209,255-256"
  ],
  "evidence_ids": [
    "CHILD_DEFAULT_EXECUTE/result.json",
    "DEFAULT_ROUTE_READBACK.json"
  ],
  "observed": "Unset ROUTE_STYLE derives catalog invocation, but committed receipt says route=openai from original environment default. Child exits 0.",
  "expected": "Receipt describes actual derived route.",
  "contradiction": "Unset ROUTE_STYLE derives catalog invocation, but committed receipt says route=openai from original environment default. Child exits 0. Expected: Receipt describes actual derived route.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Bounded direct-child evidence inconsistency; gated explicit-style callers avoid it.",
  "earliest_owner": "Child receipt formatting",
  "smallest_repair_scope": "Write derived STYLE; compare default argv, manifest and receipt.",
  "retest_required": [
    "CHILD_DEFAULT_EXECUTE/result.json",
    "DEFAULT_ROUTE_READBACK.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

### AO12-RECORD-SCOPE — Every-outcome wrapper-record claim needs scope

```json
{
  "finding_id": "AO12-RECORD-SCOPE",
  "title": "Every-outcome wrapper-record claim needs scope",
  "classification": "NON_BLOCKING_OBSERVATION",
  "severity": "INFO",
  "gate_ids": [
    "S4-STAGE-B-HANDOVER-CLOSURE",
    "S4-MODEL-ROUTING-CONFORMANCE"
  ],
  "acceptance_ids": [
    "user maker claim 4",
    "stage-b/run_checker_lane.sh:41-42,80-83,120-123"
  ],
  "subject_identity": "2fc17c0a3250ff0b86021f908c5b6ec8bd64886e",
  "source_locators": [
    "user maker claim 4",
    "stage-b/run_checker_lane.sh:41-42,80-83,120-123"
  ],
  "evidence_ids": [
    "PRIMARY_SUCCESS_RECORD/result.json",
    "CONTROLFAIL_RECORD/result.json"
  ],
  "observed": "Primary success exit 0 and ordinary control-flow failure exit 7 leave no CHECKER_* wrapper decision record; both commit child log/manifest/receipt.",
  "expected": "State record guarantee precisely; child evidence exists, wrapper classification record is branch-dependent.",
  "contradiction": "Primary success exit 0 and ordinary control-flow failure exit 7 leave no CHECKER_* wrapper decision record; both commit child log/manifest/receipt. Expected: State record guarantee precisely; child evidence exists, wrapper classification record is branch-dependent.",
  "reproducibility": "REPRODUCED",
  "claim_impact": "Not a missing-all-evidence claim; non-blocking scope observation.",
  "earliest_owner": "Checker record contract",
  "smallest_repair_scope": "Clarify claim or consistently commit wrapper outcome records.",
  "retest_required": [
    "PRIMARY_SUCCESS_RECORD/result.json",
    "CONTROLFAIL_RECORD/result.json"
  ],
  "regression_required": [
    "three frozen harness suites; affected positive/adversarial controls; fresh independent recheck"
  ],
  "oracle_disposition": "NOT_APPLICABLE",
  "status": "OPEN"
}
```

Decisive raw control-flow excerpts, verbatim; synthetic hostile input is referenced by locator rather than reprinted:

```text
QUOTED_ERROR_REAL_HARD
EXIT_CODE: 0
CHECKER_FAILOVER_START lane=QUOTED_ERROR_REAL_HARD model=opencode-go/glm-5.3-flash route=catalog
CHECKER_RECORD_COMMITTED CHECKER_FAILOVER_QUOTED_ERROR_REAL_HARD.md
CHECKER_BACKUP_OK lane=QUOTED_ERROR_REAL_HARD stamp=20261012T155313Z
```

```text
TAIL_QUOTE_CONTROLFAIL
EXIT_CODE: 0
CHECKER_FAILOVER_START lane=TAIL_QUOTE_CONTROLFAIL model=opencode-go/glm-5.3-flash route=catalog
CHECKER_RECORD_COMMITTED CHECKER_FAILOVER_TAIL_QUOTE_CONTROLFAIL.md
CHECKER_BACKUP_OK lane=TAIL_QUOTE_CONTROLFAIL stamp=20261012T155318Z
```

```text
WRAPPER_STATUS_FAILURE
EXIT_CODE: 0
CHECKER_FAILOVER_START lane=WRAPPER_STATUS_FAILURE model=opencode-go/glm-5.3-flash route=catalog
CHECKER_RECORD_COMMITTED CHECKER_FAILOVER_WRAPPER_STATUS_FAILURE.md
CHECKER_BACKUP_OK lane=WRAPPER_STATUS_FAILURE stamp=20261012T155803Z
INDEPENDENT_NATIVE_GIT_STATUS_EXIT_CODE: 0
?? AO12_RECORD_DIRT.txt
```

```text
GATE_OS_JUNCTION
EXIT_CODE: 3
GATE_REFUSED_NO_WRITERS_STARTED
REFUSED[3] gate log dir resolves inside the worktree: /tmp/ao12-roo_vkak/GATE_OS_JUNCTION/junction/hgk-lanes
```

```text
CHILD_OS_JUNCTION
EXIT_CODE: 3
REFUSED[3] lane log dir resolves inside the worktree (realpath): /tmp/ao12-roo_vkak/CHILD_OS_JUNCTION/junction/hgk-lanes
```

```text
GATE_OS_UNDECIDED_JUNCTION
EXIT_CODE: 3
GATE_REFUSED_NO_WRITERS_STARTED
REFUSED[3] containment undecided by the OS resolver: /tmp/ao12-roo_vkak/GATE_OS_UNDECIDED_JUNCTION/junction/hgk-lanes
```

```text
CHILD_OS_UNDECIDED_JUNCTION
EXIT_CODE: 3
REFUSED[3] containment undecided by the OS resolver: log dir=/tmp/ao12-roo_vkak/CHILD_OS_UNDECIDED_JUNCTION/junction/hgk-lanes worktree=C:/Users/user/AppData/Local/Temp/ao12-roo_vkak/CHILD_OS_UNDECIDED_JUNCTION/worktree
```

Replay from repository root: create a fresh system-temp directory using tempfile.mkdtemp, set AO12_REPLAY_TEMP to it, run `python "C:\Users\user\AppData\Local\Temp\ao12-roo_vkak\challenge.py" --case <case-name>`. Fresh workspace per case. Supported cases: QUOTED_ERROR_REAL_HARD, TAIL_QUOTE_CONTROLFAIL, WRAPPER_STATUS_FAILURE, CHILD_UNRULED_ENDPOINT, HTTP429_EXHAUSTION, GATE_OS_JUNCTION, CHILD_OS_JUNCTION, GATE_OS_UNDECIDED_JUNCTION, CHILD_OS_UNDECIDED_JUNCTION, CHILD_DEFAULT_EXECUTE, CONTROLFAIL_RECORD. Runner requires a path under system temp and creates only disposable fixture repositories. Run against frozen commit in section 1 and verify SOURCE_INVENTORY.json hashes. It never calls a live model.

## 6. Missing / quarantined evidence

| id | required for | reason | impact |
|---|---|---|---|
| MISSING_CRITICAL_INPUT current manifest | Current aggregate Stage-B acceptance | Historical subject in supplied pack | FCR-007, unsupported closure |
| Current bound independent aggregate receipt | Release-significant acceptance | No current Internal Oracle; historical heads differ | Cannot elevate harness review |
| Current ZIP association | Distribution conformance | Historical digest only | Quarantined association |
| Model identity | Served-model claim | Only declarations/transcripts | Cannot authenticate any model |
| Newline filenames | Full filename adversarial coverage | NOT_EXECUTED, known open | Not claimed fixed |
| CR-IDENTITY-BIND / CR-EXT-UNREVIEWED | Release readiness | ACCEPTANCE_RECORD_STAGEB.md:55-56 explicitly OPEN | Product builder not rerun; remain open |
| AO11 verdict | Prior adjudication | AO11_LANE_FAILURE.md:3-6,19-28: no report/verdict | Partial evidence only |

Prior 157-file AO11 corpus was not exhaustively re-audited. No historical officer verdict, qualification rate or provider/UAT behavior is reauthenticated. This finite harness challenge is complete; broader evidence edges remain unresolved. Dispatch/artifact conflicts preserved in FCR-008, original intake retained. No authority was invented to close a missing edge.

## 7. Internal Oracle disagreement

| predicate | maker/historical claim | current external result | resolution |
|---|---|---|---|
| HTTP400 / missing role | Repaired | Intended refusal reproduced | Supported finite repair |
| Undecided resolver | Fail-closed | Both entrypoints refuse intended OS branch | Supported admission repair |
| Provider error channel | Trusted classification | Prefix is not provenance; tail still untrusted | FCR-005 OPEN, deterministic failure |
| Full authorization | All axes governed | Endpoint/catalog remain environment-controlled | FCR-003 OPEN |
| Final record hygiene | A5 committed/clean | Ordinary case holds; failed final status hides dirt | FCR-006 OPEN |
| Current binding | Known open | Still stale | FCR-007 OPEN |
| Dispatch metadata | 39/0, empty digests | Frozen 38/0, stale populated intake; replay 39/0 | Preserved and rebound |

No current Internal Oracle exists; oracle_disposition NOT_APPLICABLE. Deterministic reproductions need no model vote or Meta-Oracle. Historical AO10 FAIL is not copied; current FAIL_CHALLENGE follows current bytes and independent fixtures. Prior provider filter notice is cited only at AO11_LANE_FAILURE.md:11-14; no provider request was made or retried here.

## 8. Gate calibration defense

- objective alignment: literal role/axis checks protect authorization; trusted terminal cause, complete route binding and verified wrapper cleanliness remain missing.
- risk calibration: HIGH unauthorized routing/failover and false-clean completion; MEDIUM bounded directory/receipt/availability issues; LOW/INFO metadata/claim-scope observations. Stale aggregate binding HIGH evidence gap.
- negative/adversarial: 37 focused cases, real junctions, failed OS resolver, role/axis crossing, failed final status, mixed hard/quota outcomes, quoted ERROR prefixes and fallback-tail ambiguity. Worker count and refusal reason are checked separately.
- positive cases: assigned EXECUTE/VERIFY defaults and exact owner model/effort controls pass. Terminal capacity permits tracked clean backup record. Quoted non-error-prefixed hard marker plus genuine synthetic ERROR capacity permits expected failover. Explicit HTTP429 positive fails.
- regression baseline: frozen 38/0,52/0,27/0; full-clone replay 39/0,52/0,27/0. Added NT6 assertion is absent from frozen output, recorded instead of silently reconciled.
- anti-overfitting: all replay suites pass while new cases falsify general closure. Whole-log matcher would reject QUOTED_HARD_REAL_QUOTA incorrectly; prefix filter fixes that shape but fails quoted ERROR and terminal Provider error shapes. Tail fallback restores whole-log ambiguity. Stub can still produce qualification.
- judge calibration: commands, hashes, raw exits, argv and independent native status decide findings. No model judge or maker PASS used as closure evidence.
- evaluator integrity: candidate evaluator bytes frozen and unchanged. Temp checker suite hard-coded LOGD rebound; NT_BASE redirects others. Path adapters and fault injections labeled. CRLF/LF differences kept separate from identity equivalence.
- HITL/domain: no release/live/domain authority requested or granted. Earliest component owns deterministic repairs.

## 9. Verdict

`FAIL_CHALLENGE`

Confirmed HIGH defects FCR-003, FCR-005 and FCR-006 block full routing/handover closure. Literal role/axis checks, HTTP400/malformed-payload veto, required role and undecided containment admission are supported for tested finite cases. FCR-007 current Stage-B binding remains an unresolved HIGH evidence gap. No aggregate or release acceptance issued.

## 10. Claim ceiling

A stub proves control flow and nothing about a model. A clean `git status` is not code correctness. Passing tests are not release acceptance. No model identity can be authenticated. Synthetic argv shows requested configuration only; focused fixtures are not product runtime proof.

No BUILD_PASS, LOCAL_HOST_QUALIFIED, PORTAL_APPROVED, PUBLISHED, PRODUCTION_VERIFIED or PIPD_S4_FULL_PASS. Public release remains FAIL-CLOSED / HOLD. No production authorization, live side effect, real model launch or product test-suite execution. HEAD/tree and tracked bytes outside verify/ao12 unchanged.

## 11. Recommended next route

`RESUME_SMALLEST_REPAIR`

Earliest owners: child route derivation (FCR-003), checker terminal classification (FCR-005/009), checker record finalization (FCR-006), log containment preflight / child receipt formatting (FCR-004/010), evidence-binding owner (FCR-007). Limit separately governed maker changes to these components and directly affected harness tests/records. Do not reopen unrelated product, release/package schema, sealed gates or historical evidence. Reviewer performed no repair.

Focused retests: each retained finding case; owner positive controls and assigned defaults; mixed HTTP400/malformed-payload negatives; real junction/undecided resolver at both entrypoints; terminal HTTP429 positive; record tracking plus failed status; default argv/manifest/receipt agreement. Then three harness suites and fresh independent exact-subject recheck. FCR-007 needs current manifest/receipt without rewriting history. Rollback/checkpoint: frozen commit/tree/archive in section 1; candidate untouched so no restoration needed.

## 12. External inspection list

External inspection list (temp-relative unless round stated):

- SOURCE_INVENTORY.json; repair-diff.txt / repair-diff-command.json; numbered stage-b files.
- QUOTED_ERROR_REAL_HARD/synthetic-transcript.txt:2-3 and result.json; TAIL_QUOTE_CONTROLFAIL/synthetic-transcript.txt:2-3 and result.json.
- QUOTED_ERROR_BLOCKS_QUOTA/synthetic-transcript.txt:2-3 and result.json.
- WRAPPER_STATUS_FAILURE/result.json, fixture .git/hooks/post-commit, challenge.py scoped git-status failure; REPRODUCER_READBACK.json fresh-temp confirmation.
- CHILD_UNRULED_ENDPOINT/worker-argv.txt and result.json.
- GATE_OS_JUNCTION/junction-proof.json and result.json; corresponding CHILD_OS_* and undecided cases.
- HTTP429_EXHAUSTION/result.json; RECOVERED_HTTP426_QUOTA/result.json.
- DEFAULT_ROUTE_READBACK.json; default child committed receipt and manifest paths.
- RESULTS.json; SUITE_RESULTS.json; three suite stdout/stderr files; replay_suites.py.
- FINAL_BOUNDARY.json; SELF_TEST.json; SKILL_UNIT_TESTS.json.
- Round evidence/EVIDENCE_RETURN_PACK.json:5-12,18,48 and ACCEPTANCE_RECORD_STAGEB.md:55-56.
- Round verify/ao12 original intake, completed intake, freeze and tracked inventory.
- Round verify/ao11/AO11_LANE_FAILURE.md:3-6,19-38,50-59 (historical filter notice at 11-14 referenced only).

REVIEW_EVIDENCE_MANIFEST.json binds external paths and hashes. Raw logs/fixtures remain in system temp. The credential-material rule (redacted) is referenced by locator/shape; no credential-material string is printed. Reviewer package checks are structural/process evidence, not product runtime acceptance.

Bundled skill self-test and skill unit-test raw receipts:

```text
COMMAND: ["python", "C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\scripts\\verify_review_bundle.py", "--self-test"]
EXIT_CODE: 0
STDOUT:
{
  "status": "PASS",
  "skill_sha256": "8125d1c6911397e2183e3f1f436a6df08692a8447b52f704b5c5e17481fca71c",
  "intake_errors": [],
  "report_errors": []
}
STDERR:
```

```text
COMMAND: ["python", "-m", "unittest", "discover", "-s", "C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\tests", "-p", "test_verify_review_bundle.py"]
EXIT_CODE: 0
STDOUT:
STDERR:
....
----------------------------------------------------------------------
Ran 4 tests in 0.023s

OK
```

## 13. Readback

- report path: round verify/ao12/EXTERNAL_CHALLENGE_REPORT.md; completed intake beside it.
- bytes / SHA-256: final REPORT_READBACK.json sidecar. Full-file hash cannot be embedded in the file itself without a digest cycle.
- readback: thirteen required top-level headings and finding schema inspected. Bundled validator executed successfully; candidate boundary validation is separate.


Bundled validator raw output and exit code:

```text
COMMAND: ["python", "C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\scripts\\verify_review_bundle.py", "--intake", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepair-recheck-and-triple-upgrade\\verify\\ao12\\EXTERNAL_CHALLENGE_INTAKE.json", "--report", "C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepair-recheck-and-triple-upgrade\\verify\\ao12\\EXTERNAL_CHALLENGE_REPORT.md"]
EXIT_CODE: 0
STDOUT:
{
  "status": "PASS",
  "errors": []
}
STDERR:
```
