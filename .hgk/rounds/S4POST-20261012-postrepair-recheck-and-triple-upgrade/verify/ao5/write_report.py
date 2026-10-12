import pathlib,json,sys,subprocess
B=pathlib.Path(sys.argv[1]);D=pathlib.Path(r'C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt');R='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade';E=D/R/'verify/ao5';res=json.loads((E/'results.json').read_text());parts=[]
def p(s):parts.append(s+'\n')
def raw(n):
 p('Evidence: `'+n+'.txt`\n\n```text\n'+(E/(n+'.txt')).read_text(encoding='utf-8')+'\n```')
def excerpt(file,text):
 full=(D/R/file).read_text(encoding='utf-8')
 if text.startswith("printf 'LANE="):
  lines=full.splitlines(); start=next(i for i,x in enumerate(lines) if x.startswith("printf 'LANE="));text='\n'.join(lines[start:start+2])
 assert text in full
 p('Verbatim source excerpt from `'+file+'` (full read: `required-source-read.txt`, EXIT_CODE=0):\n\n```text\n'+text+'\n```')
p('''# Independent Acceptance Officer — VERIFY / SECURITY, Round 5

Date: 2026-10-12 (Asia/Taipei). Subject: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`.

**ADJUDICATION A: STILL_NOT_CLOSED.** The delivered worktree was dirty before any officer evidence was created. The untracked path was the launcher's AO5 manifest, not this officer's report.

**ADJUDICATION B: enforcement is real on the specifically repaired branches, but still fails open.** The round-4 D1 missing-input/main-log-copy, D2 detected-dirt, D3 ordinary output-placement and F containment probes now return the expected statuses. That does not establish universal fail-closed enforcement. Independently demonstrated counterexamples include suppressed receipt-copy failure, failed Git cleanliness queries treated as clean, preflight committing an already staged outside-round file, and zero-attempt qualification advertised as passed. The gate also qualifies and launches EXECUTE through different invocation routes by default.

The ceiling is **local stub control-flow verification on this host and subject**, with explicit host configuration adjustments below. No model was launched. A stub proves control flow and proves nothing about a model.

## Subject and delivered-state evidence

I recorded HEAD, tree and porcelain status in the first tool call, before creating any file or directory. That call was grouped PowerShell: its tool exit was 0; individual native exits were not recorded. I do not claim otherwise. Subsequent individually exit-coded subprocess observations corroborate the same identity and pre-existing dirt, while also listing my permitted evidence directory.
''')
raw('first-observation');raw('delivery-head');raw('delivery-tree');raw('delivery-status')
p('''HEAD is `c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d`; tree is `d8fe6480f5107bcb01a045783c36b2cd536662c3`. The pre-existing untracked path is:

`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest`.

This falsifies a clean handover for this engagement. I cannot attribute its creator or disprove an earlier temporarily clean instant. A manifest written after preflight is consistent with the launcher source below; that is an inference, not authentication of the historical invocation.
''')
excerpt('stage-b/run_lane.sh', '''printf 'LANE=%s\nMODEL=%s\nPROVIDER=%s\nEFFORT=%s\nSTAMP=%s\nWT=%s\nROUTE_STYLE=%s\n' \
  "$LANE" "$MODEL" "$PROV" "$EFF" "$STAMP" "$WT" "${ROUTE_STYLE:-openai}" > "$S/${LANE}_${STAMP}.manifest"''')
p('''## History and method

I read both earlier verdicts and all five required launcher/harness documents, plus the lane-set gate, assignment and owner record. Full contents and a successful read exit are retained in `required-source-read.txt`. The prior verdicts are historical context, not my evidence of current behavior. I did not re-adjudicate product-code closure or accept their path-set analysis as a fresh result.

All attacks ran in an external system-temp clone checked out at the recorded commit. Before each independent launcher scenario, I reset that clone to the subject and removed only its untracked fixtures. Each reset/clean command and exit is retained. Launcher-created commits occurred only in these external clones; the delivery was never staged, committed, pushed, tagged or merged. Inside the repository, my entire write set is this round's `verify/ao5/`.
''')
raw('clone');raw('checkout');raw('clone-tree');raw('clone-clean');raw('stub-source')
p('''The retained external fixtures live under the path in `temp-location.txt`; the final harness-script clone roots additionally appear in their command/case logs. `audit.py`, `adapt.py`, `supplement.py`, `additional.py` and `results.json` preserve commands and fixture construction. These drivers are evidence, not candidate modifications. The listed commands in the logs use Windows argument notation; use the driver's subprocess argument arrays or the Bash recipes below to reproduce them.

### Host adjustments and unsuccessful attempts

The first clone attempt returned 128 for Git dubious ownership. I retried with a command-scoped `safe.directory` exception for the delivery's worktree metadata, without changing global Git configuration. The original refusal is retained in `host-initial/clone-initial-failure.txt`.

Initial native-path launcher attempts could not create the round-relative output directory and returned 3 before a child; those results do not prove the postflight branch. The environment initially disabled MSYS argument conversion. I removed `MSYS_NO_PATHCONV` and `MSYS2_ARG_CONV_EXCL` from the probe subprocess environment and used `/tmp/...` paths for Bash filesystem operations. No launcher code was changed. These are the conditions for the successful branch probes; the unadjusted host remains a portability limitation.
''')
raw('environment-contract');raw('host-initial/post')
p('''Both requested test scripts initially returned 9 / `CLONE_FAILED` before assertions. A separately captured clone command exposed filename-length failure. The final runs used fresh shorter system-temp directories and inherited `core.longpaths=true` through process-local `GIT_CONFIG_*` settings. This did not modify a repository or global configuration. Earlier failures remain evidence; the final counts below are actual assertion counts, not estimates.
''')
raw('path-diagnostic')
p('''## Required attacks and bounded results

| Attack | Actual launcher exit | Observation ceiling |
| --- | ---: | --- |
| Untracked root dirt | 2 | Stub marker absent, no child or lane log |
| Missing brief | 3 | Stub marker absent, no child or lane log |
| Stub writes root dirt after launch | 5 | Detected dirt rejects completion |
| Ordinary `verify/ao5-probe` output | 0 | Round-relative directory exists; no root directory added |
| TMPDIR inside clone | 3 | No child; resolved log directory refused |
| Stub child returns 7 | 7 | Child nonzero propagated |
| Stub unlinks its opened log | 4 | Main log cannot be copied; metadata-only message |

Exit 0 on a status/inventory command means that observation completed, not that its observed state is acceptable. The root-dirt test is separate from the staged-input bypass below. An in-round dirty file is intentionally committed by preflight, so this is not a promise that every dirty input is refused.
''')
for n in ['dirty','dirty-inventory','missing','missing-inventory','post','post-status','output','output-inventory','output2-root-before','output2-root-after','inside','inside-inventory','child7','copyfail','copyfail-message']:raw(n)
p('''The output2 root-directory snapshots bracket a second isolated successful invocation (`output2.txt`, exit 0). They are equal. Thus the ordinary argument does not add a root directory on this probe. No symlink/junction escape or race is inferred to have passed. The inside-log test creates an empty `tmp-inside/hgk-lanes` directory before refusal; it validates before child/log-file creation, not before all directory creation.

## Residual fail-open findings

### R1 — failed exit-receipt copy still returns 0

This is the smallest direct remaining launcher failure reproducer. I exported a `cp` function which delegates main-log copying unchanged, records a failure marker outside the clone, and returns 23 only for the `.exit` receipt copy. The candidate script was unchanged. This is deterministic fault injection, not a claim that a natural disk failure occurred.

```bash
# Fresh clean external clone at the subject; stub and log/marker paths outside it.
cp() {
  case "$1" in
    *.exit) printf 'EXIT_COPY_RETURN=23\n' >> "$FAILMARKER"; return 23 ;;
    *) command cp "$@" ;;
  esac
}
export -f cp
bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_RECEIPT2 brief_nt.md verify/ao5-probe
# Captured wrapper EXIT_CODE=0; receipt copy return=23; receipt absent.
```

`LANE_WT`, `TMPDIR`, `CODEX_BIN`, `MARKER` and `FAILMARKER` are set by `supplement.py`. The receipt is absent, but the launcher reports a done lane with exit 0 and commits the manifest and main log. The main-log-copy repair works; the adjacent exit-copy error remains explicitly discarded.
''')
excerpt('stage-b/run_lane.sh','''    cp "$LOGEXIT" "$S/${LANE}_${STAMP}.exit" 2>/dev/null || true''')
for n in ['receipt2','receipt2-readback','receipt2-history']:raw(n)
p('''### R2 — Git status failure is treated as a clean worktree

I exported a Git function that delegates every command except `status`; for that command it records an external marker and returns 128. Both cleanliness queries fail; the launcher launches the stub and returns 0 while printing `PREFLIGHT_CLEAN` and `POSTFLIGHT:dirty=0`. This fault injection proves failed cleanliness queries are unchecked. It does not demonstrate corrupt repository state in the delivery.

Small reproducer, with the same clean external clone/stub environment:

```bash
git() {
  if [ "$1" = status ]; then
    printf 'GIT_STATUS_RETURN=128\n' >> "$FAILMARKER"
    return 128
  fi
  command git "$@"
}
export -f git
bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_STATUSFAIL brief_nt.md verify/ao5-probe
# Captured wrapper EXIT_CODE=0; both git-status returns=128.
```

Counting a failed command's empty stdout via `wc -l` yields zero; without checking the query status, the script cannot distinguish clean from unobservable. The relevant source is quoted below.
''')
excerpt('stage-b/run_lane.sh','''DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
[ "$DIRTY" -eq 0 ] || die 2 "worktree not clean before handover: $DIRTY path(s); refusing to launch ${LANE}"''')
raw('statusfail');raw('statusfail-readback')
p('''### R3 — an already staged outside-round file is committed and admitted

In the external clone I created `AO5_OUTSIDE_STAGED` at the root and staged it. Preflight's path-limited `git add` does not restrict the existing index; its `git commit` commits the whole index. It committed that outside-round file under the harness-artifact title, then launched the stub and returned 0. This is a genuine input-state bypass with ordinary Git, not a command override. The staged input was not refused with exit 2.

Small reproducer in a clean external clone:

```bash
printf fixture > "$clone/AO5_OUTSIDE_STAGED"
git -C "$clone" add AO5_OUTSIDE_STAGED
LANE_WT="$clone" TMPDIR="$outside_temp" CODEX_BIN="$stub" MARKER="$marker" \
  bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_STAGED brief_nt.md verify/ao5-probe
# Captured launcher EXIT_CODE=0; preflight commit contains AO5_OUTSIDE_STAGED.
```

The launcher is permitted to commit harness artifacts in its own round. This probe shows its existing-index boundary exceeds that scope; cleanliness after an unauthorized scope sweep is not input refusal.
''')
for n in ['staged-before','staged','staged-history']:raw(n)
p('''### R4 — zero attempts are called successful qualification

With `GATE_QUALIFY_RUNS=0`, no qualification stub is invoked. The lane stub runs, the gate prints `QUALIFICATION_PASSED ... consecutive_runs=0`, then `LANE_SET_OK`, and returns 0. This is input validation failure, distinct from the explicitly named `GATE_SKIP_QUALIFY=1` testing switch. The default of 3 exists, but a configurable count is not validated as a positive integer.

Smallest gate reproducer with the same external stub environment:

```bash
GATE_QUALIFY_RUNS=0 bash "$clone/$RELROUND/stage-b/run_lanes_gated.sh" VERIFY brief_nt.md
# Captured gate EXIT_CODE=0; qualification marker absent; child marker present.
```
''')
raw('qzero');raw('qzero-markers')
p('''### R5 — default EXECUTE qualification and writer routes disagree

With no `ROUTE_STYLE` override, the gate reads EXECUTE's catalog route and sends the qualification stub `-c model=<slug>`, base URL and catalog. It does not pass that role route to `run_lane.sh`, whose default is openai. The writer stub receives `-m <slug> -c model_provider="opencode-go"`, and its manifest would declare the default openai route. The gate still reports success because the stub accepts both argument forms. This proves a control-flow/configuration mismatch; it does not reproduce a real provider failure or authenticate any endpoint.

Small reproducer: unset `ROUTE_STYLE`; invoke `run_lanes_gated.sh EXECUTE brief_nt.md` with separate qualification and writer argv-recording stubs. Both are supplied by the driver. The raw transcript contains earlier native-path attempts as well as the final `candidate2` attempts; only the latter are used for this finding.
''')
raw('route');raw('route-logs')
p('''## Requested harness scripts: actual counts

Only the two explicitly requested harness scripts ran. The product test suite did not run. Both scripts use their own external clones and stubs.

- `run_harness_negative_tests.sh`: **EXIT_CODE=0; pass=15, fail=0**.
- `run_gate_negative_tests.sh`: **EXIT_CODE=0; pass=19, fail=0**.

These are individual assertion counts across T1–T6 and G1–G7, not counts of product tests or proof of complete coverage. Initial setup attempts returned 9 and never reached a result count. All outputs and per-case logs are retained.
''')
raw('harness-tests-final');raw('gate-tests-final')
p('''Coverage ceiling: T2 tests missing input, and T5 tests child failure; neither exercises an otherwise successful lane's failed main-log copy. My `copyfail` probe covers that separately. Neither tests the suppressed receipt-copy error or Git-status failure. T2's built-in no-child check searches wrapper output, whereas the stub normally writes to the redirected log; my independent external marker supplies a stronger no-child observation. Gate G5 deletes the main log, causing the child wrapper to return 4 and its receipt to be absent; it cannot isolate the gate's receipt check independently of child failure. The wildcard receipt lookup can match older receipts, as the code and maker's H6 note acknowledge; I did not execute a stale-receipt mutant.
''')
excerpt('stage-b/run_lanes_gated.sh', '''  if ! ls "$S/${LANE}"_*.exit >/dev/null 2>&1; then echo "CHILD_RECEIPT_MISSING lane=$LANE"; MISSING=1; fi''')
p('''## NOT_EXECUTED and NOT_SUPPORTED maker claims

This section is intentionally separate. An archived assertion is not accepted as an independently reproduced fact.

| Maker document / claim | Independent disposition and evidence needed |
| --- | --- |
| H1: clean handover fixed by committing artifacts and logging externally | **NOT_SUPPORTED as CLOSED.** Initial manifest dirt contradicts this engagement's clean-handover claim. Require a fresh officer's pre-write clean status and an audited sequence that does not create an in-tree manifest before the child observes delivery. Bounded external logging/preflight behavior is supported by the probes. Historical authorship/timing and the earlier evidence-only closure path sets were not re-audited here. |
| H2: repaired D1/D2/D3/F and test coverage | Supported only for the exact branches measured above. **NOT_SUPPORTED as universal fail-closed enforcement** by R1–R4. The table's T2/T5 evidence does not cover failed main-log copy, and ordinary output placement is not a physical containment proof. Require negative cases for receipt-copy/status failures, existing outside-round index entries, and path aliases. |
| H3: the old `pwd -W ... || pwd` emitted two forms and caused the prior check failure | **NOT_SUPPORTED as independently reproduced historical cause.** Current physical/lowercase check refuses the direct inside path. Require the original host command/exit/stdout and a controlled regression run to establish the old resolver behavior; no such regression was executed here. Symlink/junction/alias containment remains untested. |
| H4: same-second qualification collision and irrecoverably lost first log | **NOT_SUPPORTED independently.** Names now contain role/model/pid/run number in observed logs; collision/destruction/recoverability were not tested. Require original collision trace and inventory/backups; an irretrievably lost transcript cannot be reconstructed as evidence. |
| H5: historical misconfigured route caused provider-not-found; corrected route used identically by gate and writers | Historical provider/model outcomes are **NOT_SUPPORTED as independent executions**. The current identical-route assertion is **contradicted** by R5. Require propagating the role route and comparing qualification/child argv, then authorized real endpoint runs for provider behavior. |
| H5 resolution: assigned lane passed attempt 1, failed attempt 2 with original 400; checker passed 3/3 | **NOT_SUPPORTED by my execution.** Require authenticated original raw attempt logs tied to exact CLI/config/subject and, for a fresh behavioral claim, separately authorized real-model repetitions. I did not invoke either model. |
| H6: earlier helper exited 127; reused receipt made a prior assertion vacuous | **NOT_SUPPORTED as recreated history.** Current scripts visibly use `env` and distinct G5 brief names and pass their assertions. Require prior revision/repro logs to establish historical bug behavior. Their green results do not settle all receipt freshness cases. |
| QUALIFICATION_FINDINGS rates: 3/6 high, 2/6 none, 6/6 backup, 1/1 checker | **NOT_SUPPORTED as my measured rates.** I neither reran models nor independently recounted/authenticated those source transcripts. Need preserved complete logs, per-attempt exits/configs, counting method and provenance; fresh rates require separate permitted repetitions. |
| QUALIFICATION_FINDINGS: both shell calls succeeded, second 547 ms, later 400, 479 tokens | **NOT_SUPPORTED independently.** Need the full cited raw transcript and request/response linkage; no request trace was collected here. |
| QUALIFICATION_FINDINGS: every one of 18 logs has one 426; websocket exonerated / HTTP fallback routine | **NOT_SUPPORTED independently.** Need full log census plus transport trace. Even co-occurrence in passing logs would bound a correlation conclusion, not prove universal transport causality. |
| QUALIFICATION_FINDINGS: model differentiates failure; changing effort does not rescue it / effort is not cause | **NOT_SUPPORTED as a causal conclusion.** Need controlled repetitions and adapter/upstream traces isolating axes. Small sample counts alone do not exclude interaction or effort-dependent behavior. |
| QUALIFICATION_FINDINGS: three consecutive passes reduce false admission probability, each added pass lowers it | **NOT_SUPPORTED quantitatively or causally.** Need a justified dependence model and representative data. My default stub run executes three calls; R4 shows the positive-count requirement can be bypassed. |
| QUALIFICATION_FINDINGS: real-lane EXECUTE refusal at 2/3 and VERIFY admission at 3/3 | **NOT_SUPPORTED as this officer's execution.** Need intact `REAL_QUALIFICATION_3CONSEC.txt` and referenced raw logs with provenance or separately authorized replay. Stubs do not establish real model behavior. |
| Assignment described as immutable; owner record described as authorization | **NOT_SUPPORTED as authenticated immutable policy or owner identity.** I read local policy inputs and exercised parsing only. Need independent policy integrity and genuine owner provenance. The maker's own unauthenticated upstream-model and untested mechanistic-lead limits remain limits here. |

**NOT_EXECUTED:** real Codex/model/API/relay calls; genuine two-tool model round trips; model identity authentication; upstream request/adapter tracing; recreation of historical model failures/rates/collision/tool-helper bugs; product test suite; build/package/plugin correctness review; release acceptance; vendor validator; portal/account/host UAT; public publication; remote readback; push/tag/merge; live races or stress tests; symlink/junction/drive-alias escapes; actual disk/permission failure as opposed to deterministic copy/status injection; stale-receipt attack; seal revalidation; re-audit of prior closure commit path sets or every prior-round claim. No production source edits or delivery Git mutations were performed. No claims outside this handover/enforcement question are granted acceptance.

The documents themselves say intermittency mechanism and upstream identity are unexplained, and the preservation-list lead remains untested. I did not test those hypotheses or promote them to findings. Existing logs, local field strings, owner-shaped text and model self-report are not authentication.

## Verdict limits and delivery preservation

I cannot authenticate any model identity. A clean Git status is not code correctness; it omits ignored files and empty directories and is only an instant observation. Passing tests are not release acceptance. Fault injection proves error-path control flow under stated seams, not the frequency of real infrastructure failures. Stub qualification markers do not prove actual tool round trips. This verdict grants no release, merge, publication, product-security or host-qualification approval.

Delivery HEAD/tree stayed at the recorded subject. Individually captured index and tracked-diff commands remained empty. Final status still shows the initial manifest plus my allowed `verify/ao5/`. I did not remove the maker's dirt to manufacture closure.
''')
for n in ['final-delivery-head','final-delivery-tree','final-delivery-index','final-delivery-tracked','final-delivery-status']:raw(n)
p('''**Final adjudication:** A = **STILL_NOT_CLOSED** for the actual handover. B = **bounded repairs demonstrated, universal enforcement rejected**: launcher statuses 0 over receipt-copy return 23 and Git-status returns 128 are explicit remaining fail-open paths; the zero-attempt gate also returns 0 without qualification. The maker's all-fixed assertion must not be accepted at a higher ceiling than these observations.''')
(E/'AO_VERDICT_HANDOVER_R5.md').write_text('\n'.join(parts),encoding='utf-8')
print('REPORT='+str(E/'AO_VERDICT_HANDOVER_R5.md'));print('SIZE='+str((E/'AO_VERDICT_HANDOVER_R5.md').stat().st_size))
