import pathlib, subprocess, json, hashlib
W=pathlib.Path.cwd(); R='.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'; O=W/R/'verify/ao8'; B=pathlib.Path((O/'external-base.txt').read_text())
H='5f776a694b6369d3e0099545c4421da009081a86'; safe='safe.directory='+W.as_posix()
fs=['stage-b/run_lane.sh','stage-b/run_lanes_gated.sh','verify/harness/run_harness_negative_tests.sh','verify/harness/run_gate_negative_tests.sh']
rows=[]
norm=lambda b:b.replace(b'\r\n',b'\n')
for f in fs:
 original=subprocess.check_output(['git','-c',safe,'show',H+':'+R+'/'+f],cwd=W)
 snapshot=(O/'source-snapshots'/pathlib.Path(f).name).read_bytes()
 current=(W/R/f).read_bytes(); external=(B/'subject'/R/f).read_bytes()
 rows.append(f+' normalized_current_matches_initial='+str(norm(current)==norm(original))+' snapshot_matches_external_subject='+str(snapshot==external)+' normalized_snapshot_matches_external_subject='+str(norm(snapshot)==norm(external))+' normalized_snapshot_matches_initial='+str(norm(snapshot)==norm(original)))
(O/'source-normalized-identity.txt').write_text('COMMAND: git show initial-HEAD:<four sources>; compare bytes with CRLF normalized to LF\nEXIT_CODE: 0\nRAW OUTPUT:\n'+'\n'.join(rows)+'\n',encoding='utf-8')
print('\n'.join(rows))
docs=['verify/ao3/AO_VERDICT_STAGEB_R3.md','verify/ao4/AO_VERDICT_HANDOVER_R4.md','verify/ao5/AO_VERDICT_HANDOVER_R5.md','verify/ao6/AO_VERDICT_HANDOVER_R6.md','verify/ao7/AO7_LANE_FAILURE.md','verify/harness/HARNESS_DEFECT_LOG.md','verify/harness/QUALIFICATION_FINDINGS.md','AO5_RESULT.md','stage-b/OWNER_DECISION_MODEL_DEVIATION.md']
read=[]
for f in docs:
 t=(W/R/f).read_text(encoding='utf-8'); read.append(f+' read_chars='+str(len(t)))
(O/'document-read-inventory.txt').write_text('COMMAND: pathlib.Path.read_text(encoding=utf-8) for each named document; no credential files or ignore rules read\nEXIT_CODE: 0\nRAW OUTPUT:\n'+'\n'.join(read)+'\n',encoding='utf-8')
ex=[]
for f in ['verify/ao7/AO7_LANE_FAILURE.md','stage-b/OWNER_DECISION_MODEL_DEVIATION.md','stage-b/run_lane.sh','stage-b/run_lanes_gated.sh']:
 t=(W/R/f).read_text(encoding='utf-8').splitlines()
 keys=['failed child must','No receipt was','allows exactly','any other model','grep -qx','grep -v -F','[ -n "$LANE_ROLE" ]','printf \'lane=%s','QUALIFIED:-yes','Fixed-string prefix matching via case','unset BASH_ENV ENV']
 ex.append('FILE: '+f)
 ex.extend(str(i+1)+': '+line for i,line in enumerate(t) if any(k in line for k in keys))
(O/'document-code-excerpts.txt').write_text('COMMAND: read named documents/scripts and select named comparison lines\nEXIT_CODE: 0\nRAW OUTPUT:\n'+'\n'.join(ex)+'\n',encoding='utf-8')
report='''# AO8 independent acceptance verdict

Round `S4POST-20261012-postrepair-recheck-and-triple-upgrade`, 2026-10-12 (Asia/Taipei).

**ADJUDICATION A: PARTIAL — unqualified CLOSED is NOT_SUPPORTED.** The initial delivered handover was clean: no porcelain paths, no observed untracked paths, independently repeated exit 0 before evidence creation. The manifest now really is copied. Lifecycle closure remains false: the gate can write qualification logs into the tree and return 0, and the child can return 0 after dirt is introduced after its final status query. The end observation also contains non-officer modified harness evidence. That final dirt is observed, not attributed to this officer or any particular other actor.

**ADJUDICATION B: NOT_SUPPORTED — the launcher still returns success over demonstrated governance failures.** Passing the repaired original branches does not cover substring path admission, regex authorisation, role scope, unchecked receipt fields/conflicts, caller-controlled route/provider/sandbox, or initial shell startup effects. All model/worker invocations below were shell stubs; no real model was launched by this officer.

Tested subject: HEAD `5f776a694b6369d3e0099545c4421da009081a86`, tree `9eb9e957cfa4b1949640154e1fa7733e05cc0f91`. Initial commands used `git -c safe.directory=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt rev-parse HEAD`, `rev-parse 'HEAD^{tree}'`, and `status --porcelain`. Outputs were the two hashes and ZERO BYTES respectively; individually repeated exits were 0/0/0. See `initial.txt`. No ignored-file inventory is inferred from porcelain.

## Claim adjudications

| Claim | Judgment | Evidence |
|---|---|---|
| Handover hygiene CLOSED | PARTIALLY_SUPPORTED | Initial clean observation and M1 copy supported; N-after-final-status and N-TMPDIR-gate-only lifecycle counterexamples, plus delivery-end-status, prevent closure. |
| M1–M9 closed | PARTIALLY_SUPPORTED | Each original mechanism independently replayed below; broader M2, M6, M7, M8/M9 guarantees fail. |
| Harness 34 pass / 0 fail, gate 32 pass / 0 fail | SUPPORTED | Unmodified delivered suites, external clones, stubs: harness-retry exit 0 `RESULT pass=34 fail=0`; gate-retry exit 0 `RESULT pass=32 fail=0`. Counts are assertions. |
| Child re-derives model, effort and route and refuses mismatch unless exact owner value | NOT_SUPPORTED | Optional LANE_ROLE permits complete omission; `.*` is regex-authorised as model and effort although not named; provider/base/catalog are not pinned. Narrow role-given ordinary mismatch refusal is supported. |
| Gate validates receipt content rather than presence | PARTIALLY_SUPPORTED | Empty and original wrong-token/exit/route receipts refused; a clean committed forgery with wrong model, qualified=no, duplicate conflicting exit/route fields is accepted. |
| Newline filenames not covered; transcript can be stubbed | PARTIALLY_SUPPORTED | Stubbed transcript admission independently demonstrated; newline filename case NOT_EXECUTED. The stated newline limitation is not the cause of the demonstrated substring bypass. |

## Independent current M1–M9 replays

Each `.sh` contains the exact fixture and invocation. Each paired `.txt` records command, cwd, exit and raw output and was written immediately after that case finished. PRE configures CODEX_BIN/GATE_BIN as external stubs. The external subject was reset to the initial HEAD between cases; resets and cleans were guarded to stay within the external temp clone, and their subprocess statuses were checked. No delivery reset/clean/stage/commit occurred.

| Case | Latest subject exit | Current result |
|---|---:|---|
| M1 manifest omitted | 0; failed-copy control 6 | M1 manifest exists in committed round; committed and external manifest readbacks match. M1-copy-failure prints POSTFLIGHT_MANIFEST_COPY_FAILED and NO_RECEIPT_WRITTEN, exits 6. |
| M2 Xhgk regex spelling | 6 | STAGED_OUTSIDE_ROUND_REFUSED; broader substring bypass below. |
| M3 failed index enumeration | 6 | STAGED_QUERY_FAILED_REFUSED; injected return 128 is refused. |
| M4 receipt-commit hook dirt | 5 | POSTFLIGHT_DIRTY_REJECTED, POSTFLIGHT:dirty=1, real status `?? M4_DIRT.txt`. |
| M5 receipt destination directory | 6 | RECEIPT_ALREADY_EXISTS_REFUSED and NO_RECEIPT_WRITTEN; no success over directory write collision. |
| M6 original forged wrong fields | 8 | CHILD_RECEIPT_INVALID; child also rejects post-hook dirt. Empty control returns 8/MISSING. |
| M7 original BASH_ENV child route override | 0; direct mismatch 6 | Gate removes startup inheritance before child. M7-worker-log shows catalog writer argv; M7-direct-mismatch refuses openai versus assigned catalog. |
| M8 skip without acknowledgement | 6 | QUALIFICATION_SKIP_UNAUTHORISED; acknowledgement variant admits unqualified lane, exit 0 and qualified=no. |
| M9 two sentinels only | 7 | QUALIFICATION_FAILED exit=0 tool_execs=0; full fabricated transcript still passes, exit 0. |

These are the newest original-branch replays, not inherited AO7 or maker results. Successful stub M1/M7 runs establish repaired control flow, not model authenticity.

## Smallest counterexample: outside-round commit

N-prefix-substring returns **0**, prints clean postflight, and its real `git log -3 --name-only` includes an outside-round file. No hook, failed command, newline, authorization-file edit or startup-file injection is required. Given the retained external clone and successful stub:

```bash
rel=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
mkdir -p "prefix/$rel"
echo outside > "prefix/$rel/outside.txt"
git add prefix
bash "$LANE_WT/$rel/stage-b/run_lane.sh" PREFIX brief_nt.md verify/a8
```

The script uses `grep -v -F -- "${RELROUND}/"`; `-F` fixes regex spelling but searches anywhere, not just at the start. It admits `prefix/.hgk/...`, commits the previously staged outside path, and returns 0. N-prefix-rename also returns 0 after real `git mv README.md "prefix/$REL/moved.md"`. N-prefix-quoted (space name) and N-prefix-tab (Git-quoted name) both return 0. On this Windows/MSYS host the requested tab spelling appears as a private-use character in Git's quoted octal output; this is a quoted-path observation, not proof of native tab/newline filename support. See raw transcripts below.

## New authorisation and receipt mechanisms

N-owner-regex: unchanged owner file, `LANE_MODEL='.*'`, gate and child both print owner-authorised deviation and return **0**. The caller's value is a grep basic regular expression. N-owner-effort-regex directly invokes the child with assigned model/style and `LANE_EFFORT='.*'`: **0**, CHILD_OWNER_AUTHORISED_EFFORT. Neither exact value is named in the delivered record.

N-owner-second-line appends a second authorisation in the external clone: extra-model is admitted, **0**. This requires owner-file modification; it demonstrates lack of single-value/schema enforcement, not permission to modify the real owner's record. N-owner-trailing-space puts a trailing space on both record and requested value: **0**; N-owner-trailing-control requests the unspaced value against that spaced record: **6**. Therefore trailing spaces are literal significant data, not an unspaced-value bypass. A real owner-file symlink setup was attempted and failed with Windows privilege error 1314; symlinked-owner launcher behavior is **NOT_SUPPORTED / NOT_EXECUTED**, rather than inferred from an MSYS copy.

N-owner-other-role requests the EXECUTE-authorised backup model for VERIFY with unchanged owner record: **0**. The record is headed EXECUTE and scopes acceptance to backup writer artifacts, but the code searches the same model line for every role. No role-bound owner authorization is enforced.

N-empty-receipt returns **8**. N-forged-valid-fields uses an external post-commit hook to modify and commit the receipt, making the final tree clean. The resulting body has model=wrong-model, qualified=no, child_exit=0 AND child_exit=99, route=catalog AND route=wrong. The gate returns **0 / LANE_SET_OK**. It requires matching lines to exist but does not enforce unique keys, model or qualification consistency, freshness or provenance. This is a hook-access integrity counterexample, not proof that an unauthenticated remote caller can edit receipts. The original failed-write receipt is now refused; the broader receipt integrity claim is not closed.

## Environment and final-query mechanisms

N-after-final-status exports a git function which creates LATE_DIRT.txt only during the postflight `git rev-parse --short HEAD`, after the status count and after the receipt exists. Launcher **0**, `POSTFLIGHT:dirty=0`; immediate command-bypassing status is `?? LATE_DIRT.txt`. The injected function is the same caller-controlled shell-function mechanism the owner's negative harness uses for command failures. The original receipt-commit ordering bug is repaired; later executable commands can still write after the query. This is a deterministic caller-injection probe, not a natural concurrent race measurement.

N-role-omitted directly calls the child without LANE_ROLE: **0**, arbitrary model/provider/effort and sandbox danger-full-access reach the **stub** argv. No sandbox escape or real model is executed. N-provider-override uses the real gate for VERIFY with LANE_PROVIDER=unassigned: **0**, worker argv includes that provider. N-route-address supplies assigned model/effort/style directly to the child but alternate loopback base/catalog: **0**, worker argv contains those values. The child pins only route style. The normal gated route-spelling case M7 is repaired; direct child entry is wider.

N-TMPDIR-inside returns **3**, but its mkdir already creates an empty in-tree directory (Git does not report empty dirs). N-TMPDIR-gate-only returns **0** after qualification writes into tmp-inside/hgk-lanes; real status reports `?? tmp-inside/`. Gate qualify-only never invokes child containment checks. N-startup-initial gives BASH_ENV a file setting GATE_QUALIFY_ONLY=1: **0**, no writers, GATE_QUALIFICATION_ONLY_OK. Unsetting BASH_ENV inside a script cannot undo its execution before the first script statement. This does not reproduce M7's removed child inheritance; it establishes a remaining initial-entry startup boundary.

N-GATE-PY-override supplies a stub assignment reader in GATE_PY, qualify-only: **0**, ASSIGNMENT reports fake-model/fake-provider/fake-effort. No writer was attempted in this probe; writer bypass via that reader is NOT_SUPPORTED. GATE_BIN and CODEX_BIN were deliberately different stubs in the suites; no binary/model equivalence can be inferred. GATE_QUALIFY_RUNS=0 is refused by the suite (3); reducing it to 1 is accepted in independent replays. GATE_OUTSUB was left as the default; exhaustive OUTSUB aliases were not executed.

## Qualification ceiling and document disagreements

N-qualification-forged emits only fabricated header, two 'succeeded in' lines and sentinels from a shell stub: **0 / QUALIFICATION_PASSED**. It executes no model tool call. The filter cannot authenticate a CLI transcript, model, binary, tool results or route endpoint. It also cannot establish future writer behavior, absence of intermittency, task correctness, or release acceptance. The stored historical qualification counts, upstream 400 mechanism, websocket inference and owner artifact acceptance were read as claims and **NOT independently re-executed or authenticated**.

`AO7_LANE_FAILURE.md` says no receipt was written and that a failed child must not produce one. At the initial tested Git object, historical-AO7-receipt is a real tracked receipt containing child_exit=1 and qualified=yes. N-failed-child-receipt independently returns **7** yet writes child_exit=7 / qualified=yes. Exit propagation works, but the document's receipt claim disagrees with both stored evidence and current code. Absence of an old RECEIPT_WRITTEN message is not evidence of absent receipt. Qualified here describes admission, not successful work, and default direct calls record yes even without gate qualification.

The launcher's comment says fixed-string prefix matching 'via case'; actual code uses unanchored grep -F. The owner's statement 'allows exactly the model named on the authorizes line and nothing else' is falsified by regex and second-line/other-role probes. The claim that identical assigned route is enforced is only supported for the normal gate path; provider override/direct base/catalog remain wider. Both test-count claims are supported; they do not contradict the failures outside their assertion set. M1's claimed copy is now supported, unlike AO6's historical state. See document-code-excerpts.txt and exact source snapshots.

## Host, delivery concurrency, scope and unfinished work

Plain clone exit **128**, dubious ownership. Only `git -c safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt clone --no-hardlinks <delivery> <external-subject>` was used as the clone workaround; it returned **0** and matched HEAD/tree. Read-only delivery queries used a command-scoped delivery-path exception. These exceptions allow reading an otherwise ownership-blocked Git repository, changing what this identity can observe; no global/delivery configuration was changed.

First suite runs using native C:/ paths failed due MSYS/native path behavior: harness exit **1**, pass=5 fail=29; gate exit **1**, pass=3 fail=29. Their raw diagnostics are retained. Later runs used POSIX /tmp paths for shell operations with MSYS_NO_PATHCONV and MSYS2_ARG_CONV_EXCL removed in subprocesses, allowing translation for native Git/Python. Both then passed. This is a disclosed host adjustment, not a script repair. An incidental inline Python source-comparison attempt exited 1 with SyntaxError: unterminated string literal; the file-based comparison succeeded. No safety notice was encountered by this officer; no refused request was retried. Credential files/contents, tokens used as credentials, ignore rules naming them, and environment dumps were not inspected or reproduced. Any such rule is the credential-material rule (redacted).

Concurrent delivery changes moved HEAD to `14871ca6132a3cf3181f00e31013ade70ef3ec4b`, tree `e2619527517bda00d853b8cbc1499f1300826fff`. End status has a modified verify/harness/CHECKER_FAILOVER_TEST_RESULTS.txt outside this officer's write set, plus newer own ao8 files. Some officer files became tracked during the engagement through outside activity; this officer did not stage or commit them. The four inspected scripts still match the initial Git objects after CRLF normalization, and inspected snapshots match external checkout after the same normalization. Initial byte comparisons against Git objects were false because checkout CRLF differs from object LF; both raw and normalized comparisons are retained. This verdict's dynamic testing applies to the pinned initial subject, not to unreviewed concurrent changes or remote state.

All officer delivery writes stayed under this round's verify/ao8. Fixtures, logs, clones, hook changes, reset/clean/add/commit operations and worker binaries lived outside the delivery, under the retained external base in external-base.txt. The suites modify and commit their own external clones. The project test suite was not run; only the two explicitly requested harness suites ran. No delivery tracked source, prior evidence, Git configuration, index, branch, tag, remote or release was deliberately modified. No push, merge, stage or commit was performed in delivery by this officer.

NOT_EXECUTED / NOT_SUPPORTED: real model/provider requests or authentication; project/product tests; release acceptance; original model substitution investigation and historical reliability counts; actual symlink-owner launcher behavior after failed setup; filename-newline handling; exhaustive Unicode/case/UNC/drive/junction/symlink paths; natural disk-full/ACL faults; simultaneous real lanes or natural clock collisions; a full hook/configuration/ignored-file/submodule/ACL audit; exhaustive LANE_*, ROUTE_* or GATE_* inputs; malicious BRIEF/LANE/TOKEN path traversal, general output physical containment, deployment or remote publication checks. No universal failure-path coverage, freshness, receipt authenticity, immutable assignment provenance or code-correctness claim is supported. Work is complete for the reported finite probes; those wider areas remain unfinished/unverified, and the failed symlink setup remains an explicit requested mechanism not executed.

**Ceiling:** a stub proves control flow and nothing about a model; a clean git status is not code correctness; passing tests are not release acceptance; I cannot authenticate any model identity.

## Raw evidence appendix

The following are the officer's exact saved command transcripts (including nonzero exits and setup failures). Case shell files and Python drivers retain setup and invocation details. Receipt tokens here are local wall-clock receipt identifiers, not authentication credentials. No maker assertion is substituted for these runs.

'''
for f in sorted(O.glob('*.txt')):
 report+='### '+f.name+'\n\n```text\n'+f.read_text(encoding='utf-8')+'\n```\n\n'
(O/'AO_VERDICT_HANDOVER_R8.md').write_text(report,encoding='utf-8')
print('REPORT_WRITTEN',len(report))
