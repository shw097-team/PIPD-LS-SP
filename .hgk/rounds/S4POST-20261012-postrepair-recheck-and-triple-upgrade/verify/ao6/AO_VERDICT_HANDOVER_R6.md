# AO6 independent acceptance verdict — 2026-10-12

Subject: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`, delivered HEAD `239fead8140222660b42819ab2f89784e5322243`, tree `974df163451a2b64b3bf09c9e17c63c4cd4cd3dd`.

**ADJUDICATION A: PARTIAL.** The requested initial handover snapshot was clean: porcelain emitted no paths, repeated status exited 0, and I observed no untracked paths before creating anything. The original manifest dirt is absent. That closes the narrow initial-dirt observation at this HEAD. It does not close the launch lifecycle: a final receipt commit can introduce dirt after the last status query, and the launcher returns 0 while reporting the earlier `dirty=0`. The claimed manifest postflight copy also does not happen.

**ADJUDICATION B: STILL FAILS OPEN.** R1–R5's original branches now behave as claimed in independent stub replays, but demonstrated new branches return 0 over a failed receipt write, an outside-round staged commit, a failed staged-path query, a dirty final postflight, and invalid receipt contents. A `BASH_ENV` override also restores the qualification/writer route mismatch. No real model was launched anywhere in this investigation.

## Maker claims adjudicated

| Maker claim | Judgment | Independent evidence |
|---|---|---|
| 1. Manifest dirt gone; manifest outside then copied at postflight | PARTIALLY_SUPPORTED | Initial delivery clean; MANIFEST exited 0 and external `MANIFEST_20261012T133019Z.manifest` exists. Matching search in stage-b printed nothing. The source snapshot creates `$MAN` but never copies it. Moving it outside works; claimed copy is NOT_SUPPORTED. |
| 2. R1–R5 closed | PARTIALLY_SUPPORTED | Original-case newest exits: R1=6, R2=2, R3=6, R4=3, R5=0 with matching catalog argv. Broader checks still fail as detailed below. Narrow repairs are SUPPORTED; universal closure is NOT_SUPPORTED. |
| 3. Harness 24/0 and gate 26/0 | SUPPORTED | I executed the delivered scripts against external clones of the exact HEAD with their built-in stubs: `RESULT pass=24 fail=0`, harness exit 0; `RESULT pass=26 fail=0`, gate exit 0. Early failed setup attempts are disclosed. These are assertion counts, not model runs or release acceptance. |
| 4. Per-launch tokens prevent older receipts satisfying gate | PARTIALLY_SUPPORTED | DIFFERENT_TOKEN returns 8 despite an older differently named receipt. However token is only wall-clock second plus lane index, not a unique nonce. A frozen-clock same-token older file was truncated by a failing write, and its empty remaining file satisfied the gate, exit 0. A hook-forged wrong-token/wrong-route/child_exit=99 receipt also satisfied it, exit 0. Universal freshness/authenticity is NOT_SUPPORTED. |

## Scope and host conditions

The initial snapshot preceded the creation of even the external scratch directory. No untracked path appeared in requested porcelain; I did not interpret that as an inventory of ignored files. HEAD and tree were unchanged and status remained empty immediately before writing this report.

Plain cloning failed with dubious ownership, exit 128. I used ONLY the command-scoped exception `git -c safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt clone --no-hardlinks . <external-base>/subject`; it exited 0, and the clone HEAD/tree matched. This permits reading the owner's gitdir for this operation and changes the observation possible under the sandbox identity. I did not set global or delivery safe.directory configuration.

Git Bash inherited disabled argument translation (`MSYS_NO_PATHCONV=1`, `MSYS2_ARG_CONV_EXCL=*`). Native-path `mkdir` failed. I unset those variables only in test subprocesses and used POSIX `/tmp/...` paths with normal Git Bash native argument conversion. Two longer-base harness setups still ended `CLONE_FAILED`, exit 9; their script suppresses the underlying error, so I do not assign a cause. A shorter external base ran to completion. See `raw/initial-and-host.txt`, failed transcripts, and successful clone transcript.

External roots: `C:/Users/user/AppData/Local/Temp/ao6-84de844529bf4b3f98c2bf73b65639cc` and `C:/Users/user/AppData/Local/Temp/a68bba55`. The suite and independent reproduction scripts mutated and committed ONLY external clones. Clone cleanup guards verified the absolute external target before cleanup. Delivery writes are exclusively this round's `verify/ao6/`. No delivery stage, commit, push, tag, merge, configuration change, or tracked-file edit occurred.

I read both launchers, both delivered negative-test scripts, HARNESS_DEFECT_LOG.md, QUALIFICATION_FINDINGS.md and AO5_RESULT.md. They are retained as source snapshots with SHA256 output. I also read the qualification brief and assignment. Maker documents are claim inputs, not acceptance evidence.

## Independent R1–R5 replays

All used `CODEX_BIN` and `GATE_BIN` pointing at an external shell stub that emits Q1_OK/Q2_OK and records argv; it does not call any model. `reproducers/probe.sh` gives complete fixture construction, environment and commands. Raw output follows in the appendices, including each command and exit.

| Replay | Fault/input | Newest original-branch exit | Observed result |
|---|---|---:|---|
| R1 | Exported cp function fails `.exit` copy (23) | 6 | `POSTFLIGHT_RECEIPT_COPY_FAILED` |
| R2 | Exported git function fails `status` (128) | 2 | `REFUSED[2] git status failed; cleanliness cannot be established, refusing to launch R2` |
| R3 | Real `git add outside.txt` before launch | 6 | `STAGED_OUTSIDE_ROUND_REFUSED: outside.txt` |
| R4 | GATE_QUALIFY_RUNS=0 | 3 | `REFUSED[3] GATE_QUALIFY_RUNS must be >= 1, got: 0` |
| R5 | EXECUTE with contradictory ordinary ROUTE_STYLE/base/catalog env | 0 | Both recorded invocations use catalog slug, identical base/catalog, no provider id; ordinary route overrides are resisted. |

## New counterexamples and negative controls

**1. Smallest outside-round bypass (no hook or failed-command injection).** Stage `Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt`, then invoke the current run_lane.sh with a successful shell stub and an existing brief. REGEX_PROOF exits 0. Its preflight commit `b38ed7714ad5ac88b8981bc4fd97c7c7852c1e07` contains that outside path. The filter uses `grep -v "^${RELROUND}/"`; the dot in `.hgk` is a regex wildcard, so `Xhgk` is erroneously inside. This is an alternate path spelling accepted by the regex, not a physical filesystem alias. Complete executed commands are in extra.sh and raw/extra-probes.txt.

Derived compact reproducer (same operations as the executed REGEX_PROOF fixture; prerequisites: external clone, external logs, successful stub):

```bash
rel=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
mkdir -p "$LANE_WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade"
echo outside > "$LANE_WT/Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt"
git -C "$LANE_WT" add Xhgk
bash "$LANE_WT/$rel/stage-b/run_lane.sh" ALIAS2 brief_nt.md verify/ao6
```

**2. Unchecked staged-query failure.** STAGED_QUERY_FAILURE injects exit 128 only for `git diff --cached --name-only`, with a real staged outside.txt. It returns 0 and preflight commit `3c8afc38bafb81928d378c7ac54eec0e31d5e1fc` includes outside.txt. Failed git status is fixed, but failed index enumeration is silently treated as no outside paths. The injected message is suppressed by the launcher's `2>/dev/null`; the exported function and return code are in the reproducer.

**3. Two-commit postflight dirt.** A real external Git post-commit hook creates `AO6_HOOK_DIRT.txt` only on the receipt commit. SECOND_COMMIT returns 0 and prints `POSTFLIGHT:dirty=0`; immediately following real status prints `?? AO6_HOOK_DIRT.txt`. This uses repository-local hook execution and demonstrates the missing final status query. It does not assert that an attacker without hook access can install one in delivery.

**4. Actual receipt filesystem failure.** A child shell stub creates an empty directory at `stage-b/WRITE_fixed.receipt` (LANE_TOKEN=fixed) and exits 0. The launcher emits `Is a directory`, then `RECEIPT_WRITTEN WRITE_fixed.receipt`, and returns 0. Actual status is empty; checks show RECEIPT_IS_DIRECTORY / RECEIPT_IS_NOT_FILE. No printf function injection is needed. This direct-lane counterexample is distinct from the fixed R1 `.exit` copy. I did not run this particular directory fixture through the gate; its gate behavior is NOT_EXECUTED.

**5. Old/empty/forged receipts.** OLD_RECEIPT and the clearer EMPTY_OLD_RECEIPT freeze `date` to model token collision, precommit an older receipt at that same token, and inject failure in the receipt-format printf. Shell output redirection truncates the older file BEFORE printf fails; consequently this does NOT demonstrate preservation of old receipt bytes. EMPTY_OLD_RECEIPT shows 40 bytes before and 0 after, the failure message, and gate exit 0. The mechanism checks existence only, so an empty older pathname is sufficient. This is deterministic injected write failure and clock collision, not a measured natural simultaneous launch rate. FORGED_RECEIPT uses a post-commit hook to replace a receipt with `FORGED child_exit=99 token=wrong route=wrong`; gate returns 0 and following status reports its modification. It proves lack of content validation/authentication under hook access. DIFFERENT_TOKEN is the negative control: older differently named file plus missing current log yields child exit 4, missing-current-receipt message, gate exit 8.

**6. Route environment trust boundary.** R5 resisted direct ROUTE_STYLE/base/catalog environment overrides. BASH_ENV_ROUTE supplies a startup file which sets ROUTE_STYLE=openai only when `$0` is run_lane.sh. Qualification argv is catalog; writer argv is `-m ... -c model_provider="opencode-go"`; gate returns 0 and still announces catalog. This requires caller-controlled BASH_ENV/file access and tests the unfiltered shell-startup environment. I do not equate it with an override by ordinary ROUTE_STYLE alone. The unchanged gate recomputes role route, while the unchanged child trusts startup-mutated env.

**7. Path/submodule/case/ignore controls.** `git add ./outside.txt` normalizes the path and is refused (6). An outside file added via a lowercase spelling of CASEPATH on this Windows filesystem is refused (6). A staged synthetic gitlink outside the round is refused (6). A real external submodule with a committed revision update and staged outside-round gitlink is also refused (6). A force-staged outside file matching `.git/info/exclude` is refused (6); a second fixture uses a committed actual `.gitignore` entry and is refused (6). These particular controls did not defeat the check; all variants are not proven safe. IGNORED_DIRT separately shows ordinary status ignores an untracked excluded file: launcher returns 0, while `git status --porcelain --ignored` prints `!! AO6_IGNORED.txt`. That is a boundary of Git cleanliness, not a staged-file bypass.

**8. Manifest and qualification boundaries.** MANIFEST returns 0 with clean status and creates an external manifest; no matching manifest is in stage-b. SKIP_QUALIFY returns 0 and launches a writer while explicitly printing `QUALIFICATION_SKIPPED_BY_ENV (testing switch; a lane admitted this way is NOT qualified)`. It is an exposed bypass, not a false claim of qualification in that message. FILTER_ONLY returns 0 after the stub prints two sentinel strings. The stub performs no tool calls: qualification actually verifies exit plus substring presence, not provenance of those strings or a structural two-tool trace. Passing it cannot establish future writer behavior, absence of intermittent faults, tool correctness, task correctness, release acceptability, or model identity. Distinct GATE_BIN/CODEX_BIN are also permitted; my stub runs cannot establish model equivalence.

## What I did NOT execute; unsupported claims

- No real Codex/model request, real provider/relay qualification, project test suite, product acceptance test, deployment, release, push, or delivery commit/stage. All supposed model invocations were external shell stubs, including the two suites and every R/adversarial replay.
- No full audit of ignored delivery files, all Git configurations, hooks in delivery, file ACLs, physical junction/symlink containment, UNC/drive/path-length aliases, every Unicode/case spelling, or concurrent real launches. The regex-spelling, dot spelling, and one Windows case spelling are the executed path cases.
- No recursive dirty-submodule execution under the round, nested/malicious submodules, or exhaustive submodule variants. A synthetic outside gitlink and a real staged outside-submodule revision were executed.
- No natural disk-full/ACL receipt fault; I executed a real directory collision and deterministic printf/cp failure injections. No claim that old receipt contents remained intact: the failed redirection truncated them.
- No replay of original AO3/AO4 experiments beyond the delivered suites' cases, and no independent reproduction of maker's model counts, 400 reasoning-content hypothesis, relay websocket fallback, mechanism of intermittency, or original model substitution. Those claims remain NOT_SUPPORTED by this investigation.
- No universal fail-closed, freshness, integrity, physical containment, task correctness, assignment authenticity, or model authenticity finding. Passing R1–R5 controls is finite local evidence only.

**Ceiling:** a stub proves control flow and nothing about a model; a clean git status is not code correctness; passing tests are not release acceptance; I cannot authenticate any model identity.

## Raw evidence appendix

The following outputs are copied verbatim from officer-run commands. Reproducer shell files retain complete setup and environment. Wrapper-level suite exit codes were captured from `$LASTEXITCODE`: HARNESS_EXIT=0, TEST_EXIT=0 for gate. Failed suite setups ended 9. Independent probe wrapper exits were 0; individual subject exits are explicit in their transcripts. Source snapshots retain the exact inspected scripts; no repair was made.

### Initial snapshot and host

```text
Before creating any file/directory, commands executed in delivery:
Get-Location
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain
Raw SHA output:
239fead8140222660b42819ab2f89784e5322243
974df163451a2b64b3bf09c9e17c63c4cd4cd3dd
Raw status output: ZERO BYTES (no paths).
Immediately repeated before creating anything:
git status --porcelain; Write-Output "STATUS_EXIT=$LASTEXITCODE"
Raw output:
STATUS_EXIT=0
Observed untracked paths: NONE in requested porcelain output.
rg was unavailable; initial combined command ended 1 due to missing rg, not Git.
Get-ChildItem -Recurse -File -Filter AGENTS.md returned no paths.

Host workaround:
Plain command: git clone --no-hardlinks . <external-base>/subject
Raw output:
Cloning into 'C:\Users\user\AppData\Local\Temp\ao6-84de844529bf4b3f98c2bf73b65639cc/subject'...
fatal: detected dubious ownership in repository at 'C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt'
'C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt' is owned by:
	DESKTOP-57EO414/user (S-1-5-21-2687334950-3868438633-1592137926-1000)
but the current user is:
	DESKTOP-57EO414/CodexSandboxOffline (S-1-5-21-2687334950-3868438633-1592137926-1004)
To add an exception for this directory, call:

	git config --global --add safe.directory C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt
PLAIN_CLONE_EXIT=128
The suggested global command WAS NOT EXECUTED.
Executed workaround:
git -c safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt clone --no-hardlinks . <external-base>/subject
SAFE_CLONE_EXIT=0
Clone HEAD/tree:
239fead8140222660b42819ab2f89784e5322243
974df163451a2b64b3bf09c9e17c63c4cd4cd3dd
Clone status output: ZERO BYTES.

Shell host workaround:
Initial native-path suite attempt printed:
mkdir: cannot create directory ‘C:/Users/user’: Permission denied
CLONE_FAILED
HARNESS_TEST_EXIT=9
Environment inspection printed:
MSYS_NO_PATHCONV=1
MSYS2_ARG_CONV_EXCL=*
For later tests those two variables were unset in the officer subprocess, paths were /tmp/...,
and Git Bash translated arguments to native Git/Python. No delivery configuration changed.
Two longer-base harness attempts printed CLONE_FAILED / TEST_EXIT=9; underlying error was
suppressed by delivered script. Cause NOT established. Shorter external base completed.
An accidental clone diagnostic with an unset source printed:
fatal: The empty string is not a valid path
It did not produce evidence about the launcher.

Immediately before first delivery evidence write:
git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; git status --porcelain; Write-Output "DELIVERY_STATUS_EXIT=$LASTEXITCODE"
239fead8140222660b42819ab2f89784e5322243
974df163451a2b64b3bf09c9e17c63c4cd4cd3dd
DELIVERY_STATUS_EXIT=0
Status again emitted no paths.
```

### Harness suite

```text
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

RESULT pass=24 fail=0
```

### Gate suite

```text
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

RESULT pass=26 fail=0
```

### Independent R1–R5 and first new probes

```text
COMMAND[R1]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh R1 brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=239fead
R1_LANE=20261012T132956Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
R1 exit=0 log=/tmp/a68bba55/logs/hgk-lanes/R1_20261012T132956Z.log
POSTFLIGHT_RECEIPT_COPY_FAILED receipt=/tmp/a68bba55/logs/hgk-lanes/R1_20261012T132956Z.log.exit
POSTFLIGHT:dirty=0 HEAD=c24a901
R1_LANE_DONE
EXIT[R1]=6
STATUS_EXIT[R1]=0
COMMAND[R2]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh R2 brief_nt.md verify/ao6
REFUSED[2] git status failed; cleanliness cannot be established, refusing to launch R2
REFUSED_R2_DONE
EXIT[R2]=2
STATUS_EXIT[R2]=0
COMMAND[R3]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh R3 brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: outside.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_R3_DONE
EXIT[R3]=6
A  outside.txt
STATUS_EXIT[R3]=0
COMMAND[R4]: env GATE_QUALIFY_RUNS=0 bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
REFUSED[3] GATE_QUALIFY_RUNS must be >= 1, got: 0
GATE_REFUSED_NO_WRITERS_STARTED
EXIT[R4]=3
STATUS_EXIT[R4]=0
COMMAND[R5]: env ROUTE_STYLE=openai ROUTE_BASE_URL=http://bad.invalid ROUTE_CATALOG=bad.json bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=239fead
BRIEF_NT_A__LANE=20261012T133001Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133001Z.log
RECEIPT_WRITTEN BRIEF_NT_A__20261012T133001Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=7aa9f0c
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[R5]=0
STATUS_EXIT[R5]=0
STUB argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/a68bba55/c --sandbox read-only --skip-git-repo-check -
STUB argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/a68bba55/c --sandbox workspace-write --skip-git-repo-check -
COMMAND[SECOND_COMMIT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh SECOND brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=239fead
SECOND_LANE=20261012T133003Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
SECOND exit=0 log=/tmp/a68bba55/logs/hgk-lanes/SECOND_20261012T133003Z.log
RECEIPT_WRITTEN SECOND_20261012T133003Z.receipt
POSTFLIGHT:dirty=0 HEAD=66ba186
SECOND_LANE_DONE
EXIT[SECOND_COMMIT]=0
?? AO6_HOOK_DIRT.txt
STATUS_EXIT[SECOND_COMMIT]=0
COMMAND[REGEX_ALIAS]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh ALIAS brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=19336d3
ALIAS_LANE=20261012T133005Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
ALIAS exit=0 log=/tmp/a68bba55/logs/hgk-lanes/ALIAS_20261012T133005Z.log
RECEIPT_WRITTEN ALIAS_20261012T133005Z.receipt
POSTFLIGHT:dirty=0 HEAD=7a7993f
ALIAS_LANE_DONE
EXIT[REGEX_ALIAS]=0
STATUS_EXIT[REGEX_ALIAS]=0
7a7993fd20f876e4ad9b2f5afc599e7b7a68f1c9 evidence(s4post-b): ALIAS lane receipt 20261012T133005Z (child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS_20261012T133005Z.receipt
acbc99e5e93ed05d148106105468024503247b78 evidence(s4post-b): ALIAS lane output 20261012T133005Z (lane log copied in from outside the worktree; child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS_20261012T133005Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS_20261012T133005Z.log
COMMAND[DOT_ALIAS]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh DOT brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: outside.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_DOT_DONE
EXIT[DOT_ALIAS]=6
A  outside.txt
STATUS_EXIT[DOT_ALIAS]=0
COMMAND[CASE_VARIANT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh CASE brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: casepath/outside.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_CASE_DONE
EXIT[CASE_VARIANT]=6
A  casepath/outside.txt
STATUS_EXIT[CASE_VARIANT]=0
COMMAND[IGNORED_STAGED]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh IGNORE brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: outside.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_IGNORE_DONE
EXIT[IGNORED_STAGED]=6
A  outside.txt
STATUS_EXIT[IGNORED_STAGED]=0
COMMAND[SUBMODULE_GITLINK]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh SUB brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: outside-submodule
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_SUB_DONE
EXIT[SUBMODULE_GITLINK]=6
AD outside-submodule
STATUS_EXIT[SUBMODULE_GITLINK]=0
COMMAND[IGNORED_DIRT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh HIDDEN brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=239fead
HIDDEN_LANE=20261012T133011Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
HIDDEN exit=0 log=/tmp/a68bba55/logs/hgk-lanes/HIDDEN_20261012T133011Z.log
RECEIPT_WRITTEN HIDDEN_20261012T133011Z.receipt
POSTFLIGHT:dirty=0 HEAD=4e20dd9
HIDDEN_LANE_DONE
EXIT[IGNORED_DIRT]=0
STATUS_EXIT[IGNORED_DIRT]=0
!! AO6_IGNORED.txt
256deec10ade8b6c1a270a67129801b4aba93a75
COMMAND[OLD_RECEIPT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=6829951
BRIEF_NT_A__LANE=20000101T000000Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20000101T000000Z.log
INJECT_RECEIPT_WRITE_FAILURE
RECEIPT_WRITTEN BRIEF_NT_A__20000101T000000Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=92f33bd
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[OLD_RECEIPT]=0
STATUS_EXIT[OLD_RECEIPT]=0
e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
COMMAND[FORGED_RECEIPT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=239fead
BRIEF_NT_A__LANE=20261012T133017Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133017Z.log
RECEIPT_WRITTEN BRIEF_NT_A__20261012T133016Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=06d7ea1
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[FORGED_RECEIPT]=0
 M .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/BRIEF_NT_A__20261012T133016Z-0.receipt
STATUS_EXIT[FORGED_RECEIPT]=0
FORGED child_exit=99 token=wrong route=wrong
COMMAND[MANIFEST]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh MANIFEST brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=239fead
MANIFEST_LANE=20261012T133019Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
MANIFEST exit=0 log=/tmp/a68bba55/logs/hgk-lanes/MANIFEST_20261012T133019Z.log
RECEIPT_WRITTEN MANIFEST_20261012T133019Z.receipt
POSTFLIGHT:dirty=0 HEAD=c7ad79c
MANIFEST_LANE_DONE
EXIT[MANIFEST]=0
STATUS_EXIT[MANIFEST]=0
/tmp/a68bba55/logs/hgk-lanes/MANIFEST_20261012T133019Z.manifest
COMMAND[SKIP_QUALIFY]: env GATE_SKIP_QUALIFY=1 bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_SKIPPED_BY_ENV (testing switch; a lane admitted this way is NOT qualified)
PREFLIGHT_CLEAN HEAD=239fead
BRIEF_NT_A__LANE=20261012T133022Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133022Z.log
RECEIPT_WRITTEN BRIEF_NT_A__20261012T133021Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=abd2409
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[SKIP_QUALIFY]=0
STATUS_EXIT[SKIP_QUALIFY]=0
COMMAND[FILTER_ONLY]: env GATE_QUALIFY_ONLY=1 bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
GATE_QUALIFICATION_ONLY_OK role=EXECUTE model=opencode-go/deepseek-v4.1-flash effort=high
EXIT[FILTER_ONLY]=0
STATUS_EXIT[FILTER_ONLY]=0
```

### Further new probes and controls

```text
COMMAND[REGEX_PROOF]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh ALIAS2 brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=b38ed77
ALIAS2_LANE=20261012T133129Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
ALIAS2 exit=0 log=/tmp/a68bba55/logs/hgk-lanes/ALIAS2_20261012T133129Z.log
RECEIPT_WRITTEN ALIAS2_20261012T133129Z.receipt
POSTFLIGHT:dirty=0 HEAD=8b12ed8
ALIAS2_LANE_DONE
EXIT[REGEX_PROOF]=0
STATUS_EXIT=0
8b12ed8de307e452da1f04fedb0edf4fe61866d7 evidence(s4post-b): ALIAS2 lane receipt 20261012T133129Z (child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS2_20261012T133129Z.receipt
1df66217f07c4720920d481a5a98632380246257 evidence(s4post-b): ALIAS2 lane output 20261012T133129Z (lane log copied in from outside the worktree; child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS2_20261012T133129Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/ALIAS2_20261012T133129Z.log
b38ed7714ad5ac88b8981bc4fd97c7c7852c1e07 chore(s4post-b): commit harness artifacts before the ALIAS2 lane handover
Xhgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/outside.txt
COMMAND[STAGED_QUERY_FAILURE]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh QUERY brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=3c8afc3
QUERY_LANE=20261012T133130Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
QUERY exit=0 log=/tmp/a68bba55/logs/hgk-lanes/QUERY_20261012T133130Z.log
RECEIPT_WRITTEN QUERY_20261012T133130Z.receipt
POSTFLIGHT:dirty=0 HEAD=74a88d1
QUERY_LANE_DONE
EXIT[STAGED_QUERY_FAILURE]=0
STATUS_EXIT=0
74a88d1af276a62624a19331824000116a0f2748 evidence(s4post-b): QUERY lane receipt 20261012T133130Z (child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/QUERY_20261012T133130Z.receipt
bf0ae76ba7ac403d08a64884dcc10294258afdee evidence(s4post-b): QUERY lane output 20261012T133130Z (lane log copied in from outside the worktree; child exit 0)
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/QUERY_20261012T133130Z.exit
.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/QUERY_20261012T133130Z.log
3c8afc38bafb81928d378c7ac54eec0e31d5e1fc chore(s4post-b): commit harness artifacts before the QUERY lane handover
outside.txt
COMMAND[GITIGNORE_ENTRY]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh IGNORE2 brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: AO6_ignored_staged.txt
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_IGNORE2_DONE
EXIT[GITIGNORE_ENTRY]=6
A  AO6_ignored_staged.txt
STATUS_EXIT=0
COMMAND[BASH_ENV_ROUTE]: env BASH_ENV=/tmp/a68bba55/route-env.sh bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=239fead
BRIEF_NT_A__LANE=20261012T133134Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133134Z.log
RECEIPT_WRITTEN BRIEF_NT_A__20261012T133134Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=aa9d935
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[BASH_ENV_ROUTE]=0
STATUS_EXIT=0
STUB argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/a68bba55/c --sandbox read-only --skip-git-repo-check -
STUB argv=-m opencode-go/deepseek-v4.1-flash -c model_provider="opencode-go" -c model_reasoning_effort="high" exec --cd /tmp/a68bba55/c --sandbox workspace-write --skip-git-repo-check -
OLD_BEFORE
40 /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/BRIEF_NT_A__20000101T000000Z-0.receipt
OLDER RECEIPT child_exit=99 route=wrong
COMMAND[EMPTY_OLD_RECEIPT]: bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=5415d23
BRIEF_NT_A__LANE=20000101T000000Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20000101T000000Z.log
INJECT_RECEIPT_WRITE_FAILURE
RECEIPT_WRITTEN BRIEF_NT_A__20000101T000000Z-0.receipt
POSTFLIGHT:dirty=0 HEAD=8113792
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high route=catalog
EXIT[EMPTY_OLD_RECEIPT]=0
STATUS_EXIT=0
OLD_AFTER
0 /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/BRIEF_NT_A__20000101T000000Z-0.receipt
COMMAND[DIFFERENT_TOKEN]: env CODEX_BIN=/tmp/a68bba55/delete-log.sh bash /tmp/a68bba55/c/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt_a.md
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high route=catalog
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs_required=1
  qualification attempt 1/1 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high consecutive_runs=1 route=catalog
PREFLIGHT_CLEAN HEAD=cf99928
BRIEF_NT_A__LANE=20261012T133139Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=catalog (declared)
BRIEF_NT_A_ exit=0 log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133139Z.log
POSTFLIGHT_LOG_COPY_FAILED log=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133139Z.log
POSTFLIGHT_RECEIPT_COPY_FAILED receipt=/tmp/a68bba55/logs/hgk-lanes/BRIEF_NT_A__20261012T133139Z.log.exit
POSTFLIGHT:dirty=0 HEAD=cf99928
BRIEF_NT_A__LANE_DONE
CHILD lane=BRIEF_NT_A_ index=0 exit=4
CHILD_RECEIPT_MISSING lane=BRIEF_NT_A_ token=20261012T133139Z-0
LANE_SET_FAILED children_ok=0 any_child_nonzero=1 missing_receipt=1 model=opencode-go/deepseek-v4.1-flash effort=high
EXIT[DIFFERENT_TOKEN]=8
STATUS_EXIT=0
```

### Real submodule control

```text
warning: in the working copy of 'file.txt', LF will be replaced by CRLF the next time Git touches it
Cloning into 'C:/Users/user/AppData/Local/Temp/a68bba55/c/outside-real-submodule'...
done.
SUBMODULE_ADD_EXIT=0
warning: in the working copy of 'file.txt', LF will be replaced by CRLF the next time Git touches it
COMMAND: staged real outside submodule, run_lane.sh REALSUB brief_nt.md verify/ao6
STAGED_OUTSIDE_ROUND_REFUSED: outside-real-submodule
REFUSED[6] harness preflight commit failed; refusing to hand over
REFUSED_REALSUB_DONE
REAL_SUBMODULE_EXIT=6
M  outside-real-submodule
```

### Receipt directory failure

```text
COMMAND: LANE_TOKEN=fixed CODEX_BIN=receipt-dir-stub.sh run_lane.sh WRITE brief_nt.md verify/ao6
PREFLIGHT_CLEAN HEAD=ad7b695
WRITE_LANE=20261012T133254Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high route=openai (declared)
WRITE exit=0 log=/tmp/a68bba55/logs/hgk-lanes/WRITE_20261012T133254Z.log
/tmp/a68bba55/h/clone/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh: line 134: /tmp/a68bba55/h/clone/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/WRITE_fixed.receipt: Is a directory
RECEIPT_WRITTEN WRITE_fixed.receipt
POSTFLIGHT:dirty=0 HEAD=6c7d4a7
WRITE_LANE_DONE
RECEIPT_DIRECTORY_EXIT=0
STATUS_EXIT=0
RECEIPT_IS_DIRECTORY
RECEIPT_IS_NOT_FILE
```

Final delivery state: HEAD/tree unchanged; tracked diff empty; sole observed untracked path is officer-created verify/ao6/. Raw command output in raw/final-delivery-state.txt. This evidence directory was not present in the initial handover snapshot.
