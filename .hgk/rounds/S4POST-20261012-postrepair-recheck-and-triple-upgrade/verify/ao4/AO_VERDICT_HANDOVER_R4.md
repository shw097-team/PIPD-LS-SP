# Independent Acceptance Officer — Handover Hygiene, Round 4

Date: October 12, 2026 (Asia/Taipei).

## Verdict: PARTIAL

**This engagement is clean after excluding only my permitted ao4 evidence. The structural preflight and external-log mechanism is real, not just a one-time cleanup. However, the launcher does not enforce all its own guarantees: it reports successful completion after a failed brief lookup/log copy and after detected postflight dirt, and its documented output-subdirectory argument creates the directory at the repository root. Unqualified closure is not justified.**

Cause answer: **Partially structurally fixed, not merely worked around; the governed launcher still has reproducible enforcement defects, so the cause is not fully closed.**

Subject HEAD: `01efd9923d4a2614d3727d3985c75756aadb78c4`. Tree: `70c3924c1093afca699f848582a2f99c4d79c474`. Round-2 subject independently resolved from the previous officer’s named hash: `07681745a436a7d82e85a0aa494d8165acad92a0`. Ancestor check exit 0. HEAD/tree are unchanged at the end. All launcher invocations, fixture writes, and probe-created commits were in external clones under `C:\Users\user\AppData\Local\Temp\pipd-ao4-0o4bubbo`; no model run or suite was launched in the delivery. No delivery commit, index modification, branch creation, deletion, push, tag, merge, or publication was performed. Inside the delivery, my writes are confined to this report’s ao4 directory.

## 1. Delivered state

My first terminal `git status --porcelain`, before creating evidence, printed no bytes. That initial observation was in a grouped terminal command rather than an individually exit-coded subprocess; it is corroborative, not the sole basis of acceptance. The individually captured final readback follows verbatim (exit 0):

```text
Command: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
Exit: 0
STDOUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao4/
STDERR:
```

The one untracked entry is **my own** allowed directory `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao4/`. There is no other dirty path. **Yes: this time the officer was handed a clean delivery.** Empty directories are not visible to Git; this says nothing about ignored files or future concurrent writes. `delivery-start-status.txt`, `delivery-end-status.txt`, and `final-status.txt` retain all isolated observations.

## 2. Complete history after round 2

There are **4 commits** after the named round-2 subject, in linear parent order. Every path in every commit is under `.hgk/rounds/**`: the evidence-only path claim passes. No product source, tests, tooling, packaging, workflow, README, or docs outside that prefix changes. `outside-round-diff.txt` also records an empty diff and exit 0. Be precise about “code”: these commits do include executable evidence/harness `.sh` and `.py` files inside the round; they are not a claim that no executable text changed. There is no candidate production-code change. `history.txt` has complete messages, parents, statuses, and path sets; the independently generated `paths-1.txt` through `paths-4.txt` use `--no-renames` to avoid hiding paths behind rename abbreviations.

### 1. 4807c111b6077fbe8f82d9edf1abc62a797f079d

Complete path set (44 paths; exit 0):

```text
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/AO2_HANDOVER_CLOSURE.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/09_RELEASE/PUSH_CREDENTIAL_INCIDENT.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO2_20261012T112125Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO2_20261012T112125Z.log
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO2_BRIEF.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao2_lane.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/AO_VERDICT_STAGEB_R2.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_anonymous_remote_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_final_identity_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_identity.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_artifact.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_control.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_mapping.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_receipt.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_sidecar.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_tool_raw.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_artifact.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_control.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_mapping.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_receipt.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_sidecar.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre_fix_extraction.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_candidate.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_dist.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_docs.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_guard_exact.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_missing.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_restore.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_unresolved.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_workflow_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_committed_evidence.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_final_status.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_integrity_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_copy_and_denominators.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_focused_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_full_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/F_claims_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/F_return_pack_raw.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/LOCATION_NOTE.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/audit_driver_raw.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/results.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/run_audit.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/scratch_path.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/uat/hermes/HOST_UAT_HERMES.md
```

### 2. 38f413158dc59f78d5c603fc6e82a8c6449c775f

Complete path set (1 paths; exit 0):

```text
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/AO2_RESULT.md
```

### 3. f1dc870ca7c0805d9d253fecf924ad114e9a7513

Complete path set (112 paths; exit 0):

```text
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO3_20261012T115506Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO3_20261012T115506Z.log
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T115535Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T115535Z.log
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_BRIEF_MODEL_DEVIATION.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO3_BRIEF.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO4_BRIEF.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao3_lane.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_far_lane.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/AO_VERDICT_STAGEB_R3.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/ancestor.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/anonymous-remote.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/ao2-hashes.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/ao2-verdict.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/audit.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/candidate-default-refusal-retry.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/candidate-default-refusal.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/clone.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/closure-paths.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/closure-records.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/code-unchanged-since-r2.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/command-results.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/committed-ao2-paths.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/counts-driver-exit.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/counts-driver-output.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/counts.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-end-identity.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-end-status.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-index-diff.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-status-before.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-status-final.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/delivery-tracked-diff.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/detach.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/discovery-denominator.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/doctor-system-python.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/evidence-driver-exit.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/evidence-driver-output.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/evidence.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/focused.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/full.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/guard-body.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/guard-current-head.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/guard-extracted.sh
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/head.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/history.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/identity-status.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/instructions.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/interpreter.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/local-branch.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/model-logs.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/model-summary-retry.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/model-summary.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/original-root-status.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/original-root-tracked.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-hardlink-0.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-hardlink-1.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-hardlink-2.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-hardlink-3.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-regular-0.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-regular-1.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-regular-2.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-collision-regular-3.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-control.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-guard-allowed.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-guard-frozen.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-guard-outside.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-guard-unresolved.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-extension-readback.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-extension.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-name-readback.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-name.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-version-readback.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-judgement-version.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-ninth-skill.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-output-dist.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-output-overlap.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-rebuild.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-refusal-bad-vendor.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-refusal-missing-derivation.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-refusal-missing-owner.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-refusal-unknown-manifest.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-results.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-source-drift.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-control.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-drift.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-extra.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-hardlink.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-preseeded.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-rebuild.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-size.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probe-web-traversal.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probes-driver-exit.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probes-driver-output.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/probes.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/report-validation.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/repro-identity-exit.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/repro-identity-output.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/repro_identity.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/reviewed-source.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/round-files.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/snapshot-end-identity.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/snapshot-path.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/snapshot-status.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/supplement-driver-exit.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/supplement-driver-output.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/supplement.py
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/system-interpreter.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/system-pip.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/test-counts.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/tree.txt
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/wheel-system-python.txt
```

### 4. 01efd9923d4a2614d3727d3985c75756aadb78c4

Complete path set (6 paths; exit 0):

```text
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/ACCEPTANCE_RECORD_STAGEB.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T121718Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T121718Z.log
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/far/FAR_MODEL_DEVIATION_RESEARCH_RESULT.json
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/far/FAR_MODEL_DEVIATION_SINGLE_EVIDENCE.md
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/far/write_far_reports.py
```


## 3. External launcher attacks

### A. Dirty clone: PASS

The clone started clean at the delivery subject. I created only an untracked root scratch file, then invoked the unchanged launcher with `LANE_WT` pointing to that clone and `TMPDIR` pointing outside the clone under system temp. The brief name was valid, so the refusal, not a missing-input error, prevented reaching the model command.

```text
Command: C:\Program Files\Git\usr\bin\bash.exe C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/dirty/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO4_DIRTY VERIFIER_AO4_BRIEF.md verify/ao4
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao4-0o4bubbo\dirty
Exit: 2
STDOUT:
STDERR:
LANE_REFUSED: 1 dirty path(s) in the delivery; an officer must not be launched against this
?? ao4-scratch.txt
```

Exit **2** is nonzero; the exact refusal message and scratch status are captured. No `PREFLIGHT_CLEAN`, lane-start message, log, or exit artifact was generated; the external log directory is empty, apart from the directory itself (`inventory.json`). HEAD remains the original subject. Source line 45 exits before the model call at line 54. **Property 2 passes this probe.** I did not infer refusal solely from comments.

### B. Clean clone with nonexistent brief: lookup fails, wrapper lies about success

```text
Command: C:\Program Files\Git\usr\bin\bash.exe C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/clean/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO4_MISSING AO4_DELIBERATELY_NONEXISTENT_BRIEF.md verify/ao4
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao4-0o4bubbo\clean
Exit: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=01efd99
AO4_MISSING_LANE=20261012T122958Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared checker)
AO4_MISSING exit=1 log=/tmp/pipd-ao4-0o4bubbo/clean-logs/hgk-lanes/AO4_MISSING_20261012T122958Z.log
POSTFLIGHT:dirty=0 HEAD=561d3de
AO4_MISSING_LANE_DONE
STDERR:
C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/clean/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh: line 54: C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/clean/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO4_DELIBERATELY_NONEXISTENT_BRIEF.md: No such file or directory
cp: cannot stat '/tmp/pipd-ao4-0o4bubbo/clean-logs/hgk-lanes/AO4_MISSING_20261012T122958Z.log': No such file or directory
```

The clean clone has no pending harness artifact; therefore the preflight commit branch is a no-op. The observed `PREFLIGHT_CLEAN` means the worktree check accepted the clean clone, then the script printed its lane metadata and tried opening the input. Bash evaluates `< "$W/$BRIEF"` before `> "$LOGOUT"`; input lookup failed **before the timeout/Codex executable was invoked**. This is not evidence of a real model launch or model success. It proves the clean path reached the input-redirection boundary. It does **not** independently prove a successful run’s log capture or copy.

The wrapper exits **0**, while its own `CODE` is **1**. The log does not exist; `cp` fails. Nevertheless, it commits a `.exit` file with a body claiming “Log copied in from outside the worktree; officer output committed as delivered evidence.” `clean-probe-history.txt` shows the commit contains only that exit file. The concluding echo masks the earlier errors: `set -u` is not an error-propagation mechanism, and there is no final `exit "$CODE"`. **This does not falsify the dirty-preflight test; it falsifies trustworthy completion/error reporting and the unconditional evidence-copy claim.**

Smallest reproducer (in a fresh external clean clone with Git commit identity configured; never in the delivery):

```bash
LANE_WT="$clone" TMPDIR="$external_temp" bash "$clone/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh" AO4_MISSING AO4_DELIBERATELY_NONEXISTENT_BRIEF.md verify/ao4
echo "$?"
```

Observed wrapper status: 0; failed lookup: 1; failed log copy: present in raw stderr.

### C. Harness-commit branch: PASS, bounded to input-redirection boundary

I separately added an untracked harness fixture **inside the round** in another external clone and repeated the missing-brief probe. `harness-before.txt` captures its dirt. `harness-missing-brief.txt` reports `PREFLIGHT_CLEAN HEAD=799110a` before lookup. `harness-probe-history.txt` shows preflight commit `799110a1c9157f6aa0348292e14999d36fae54ea`, containing exactly the harness fixture, with the launcher-generated title “chore(s4post-b): commit harness artifacts before the AO4_HARNESS lane handover”; a separate later commit contains the failed-run exit file. All command exits are recorded; the launcher again returns 0. This directly exercises committing harness artifacts before accepting cleanliness, without launching a model. The script stages **all** round artifacts, not a narrowly validated harness list.

### D. Postflight “assert clean” promise: FAIL

For a bounded deterministic race simulation, I exported a `cp` function in a third clean external clone. It calls real `cp` unchanged, then writes an untracked scratch file outside the round immediately before postflight. The candidate script was not edited. This is a controlled dirt injection, not a claim that the real engagement raced. The missing brief again prevents any actual model run.

```text
Command: C:\Program Files\Git\usr\bin\bash.exe -c cp() { command cp "$@"; printf "postflight dirt fixture\n" > "$LANE_WT/ao4-postflight-scratch.txt"; }; export -f cp; bash "$1" AO4_POST AO4_DELIBERATELY_NONEXISTENT_BRIEF.md verify/ao4 ao4 C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/postflight/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao4-0o4bubbo\postflight
Exit: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=01efd99
AO4_POST_LANE=20261012T123004Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared checker)
AO4_POST exit=1 log=/tmp/pipd-ao4-0o4bubbo/postflight-logs/hgk-lanes/AO4_POST_20261012T123004Z.log
POSTFLIGHT:dirty=1 HEAD=b6918f7
AO4_POST_LANE_DONE
STDERR:
C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/postflight/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh: line 54: C:/Users/user/AppData/Local/Temp/pipd-ao4-0o4bubbo/postflight/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO4_DELIBERATELY_NONEXISTENT_BRIEF.md: No such file or directory
cp: cannot stat '/tmp/pipd-ao4-0o4bubbo/postflight-logs/hgk-lanes/AO4_POST_20261012T123004Z.log': No such file or directory
```

```text
Command: git status --porcelain
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao4-0o4bubbo\postflight
Exit: 0
STDOUT:
?? ao4-postflight-scratch.txt
STDERR:
```

The script detects `POSTFLIGHT:dirty=1`, prints `AO4_POST_LANE_DONE`, and still exits **0**. Line 12 promises to “assert the worktree is clean again”; lines 71–74 only count and print dirt, never reject it. This is the comments/code disagreement, not just the unavoidable possibility of concurrent dirt. Exact shortest executed injection command and raw streams are in `postflight-dirt.txt`; `audit.py` recreates the isolated fixture. The failure means detected dirty delivery can be advertised as a successfully completed lane.

### E. Output directory goes to the wrong tree: FAIL

Line 52 is `mkdir -p "$WT/$OUTSUB" 2>/dev/null || mkdir -p "$R/$OUTSUB"`. With the documented argument `verify/ao4`, the first mkdir succeeds at **repository-root** `verify/ao4`, so the round-relative fallback never executes. `inventory.json` confirms `clean_root_output_exists=true`, `clean_round_output_exists=false` in the clean external clone. This directory is outside the round’s permitted write set. Empty-directory creation alone does not dirty Git, and I did not write evidence there in the real delivery. It contradicts the advertised in-round-output argument and pre-created officer output directory; any later officer file written there would be outside the allowlist and outside the postflight `git add` scope.

### F. Log location, sequencing, and historical trace

`script-numbered.txt` retains source with line numbers. Lines 30–31 build `LOGDIR="${TMPDIR:-$LOCALAPPDATA/Temp}/hgk-lanes"` and `LOGOUT` under it. For this Windows default, and my explicit system-temp overrides, the destination is **outside the worktree**. In the failed-lookup probes only the external `.exit` file is created: do not confuse that with successful runtime log creation. Lines 54–59 wait synchronously for the command and capture its status; line 63 attempts the in-tree log copy only afterward; lines 65–69 then stage/commit round artifacts. The intended ordering is a structural change. But the code does not normalize or validate `TMPDIR` against the worktree, does not check mkdir/copy/commit success, and does not propagate child failure.

A historical harness commit **does exist**: `f1dc870ca7c0805d9d253fecf924ad114e9a7513`, authored October 12, 2026 at 20:17:19 +0800. Its exact title is “chore(s4post-b): commit harness artifacts before the FAR lane handover” and its body is “Fail-closed preflight of the governed lane launcher: an officer must be handed a clean worktree.” These match the launcher’s lines 39–40, including the lane substitution. It adds the governed launcher, committed briefs and prior round evidence. The later `01efd9923d4a2614d3727d3985c75756aadb78c4` has the generated FAR output title and archived FAR log/exit/output paths. `harness-trace.txt`, `history.txt`, `paths-3.txt`, `paths-4.txt`, and `historical-far-log.txt` retain the trace. This corroborates adoption and two-phase history, but commit titles alone cannot establish the precise historical shell invocation or every filesystem write’s timing. The successful-run log-copy branch was **NOT_EXECUTED independently** in this audit.

## 4. Residual risks and non-conclusions

- A concurrent process can create dirt between preflight and the officer’s first observation; no lock or immutable handover boundary exists. The postflight check’s failure to reject observed dirt is a separate demonstrated defect, not an excuse based on that race.
- The launcher cannot make an officer’s verdict independent, truthful, correctly scoped, or substantively competent; clean Git status is not code correctness, test coverage, release acceptance, or publication authorization.
- Git status does not cover ignored files or empty directories; no content integrity/ignored-file inventory is guaranteed.
- `TMPDIR` is trusted, not constrained outside the worktree; output subdirectories are not validated or round-bound. The shown recipe requires a correctly configured outside temp directory.
- `git add -A -- "$RELROUND"` sweeps all round files; `git commit` commits the entire existing index, not just a validated harness subset. Already staged outside-round changes are not separately forbidden. These broader hazards are source findings, not additional executed mutant tests.
- Old ungoverned lane scripts remain tracked. The new script mitigates the root cause only when adopted; no repository-wide enforcement prevents direct bypass.

## Execution gaps

**NOT_EXECUTED:** real Codex/model execution (deliberately prohibited for this probe), independent successful-run logging/copy, automated suite (not relevant to this hygiene question), live concurrent-process race, forced Git/mkdir/copy failure branches beyond the observed missing log, staged-outside-round mutant, in-tree `TMPDIR` mutant, remote readback/publication, and verification of the historical process invocation beyond committed trace. No pass is inferred for these gaps.

Evidence-write tooling note: the first attempted stdin invocation of `apply_patch` failed before writing anything; its immediate Python follow-up exited 1 because the audit file did not exist yet. I then used the apply_patch executable entrypoint with a UTF-8 patch argument; both audit drivers completed with exit 0. These tooling failures did not execute any candidate probe or alter candidate files.

## Acceptance conclusion

**PARTIAL**: delivered-state cleanliness passes, the four-commit evidence-only delta passes, dirty-preflight refusal passes, and harness-before-check ordering is independently exercised. The root cause has a genuine structural mitigation, but the documented launcher still has fail-open postflight/error reporting and incorrect output-directory placement. Do not promote this to CLOSED or treat a zero wrapper exit as proof of clean, complete handover. The missing-brief recipe above is the smallest reproducer for the masked-error symptom; the deterministic postflight injection in `postflight-dirt.txt` proves the unfulfilled cleanliness assertion itself.
