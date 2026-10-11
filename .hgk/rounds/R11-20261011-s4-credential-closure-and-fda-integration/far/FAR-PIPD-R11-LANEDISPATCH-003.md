# FAR-PIPD-R11-LANEDISPATCH-003 — the checker lane could not read its own instructions

Discovered by dispatching a real cross-model check, not by reading the dispatcher. The first R11
verification attempt burned a full model turn and returned a VOID verdict, and the reason is a class
that will hit every future escalated checker.

## What happened

Attempt 1 was dispatched with the lane's role-default sandbox and with the brief passed as a **path**:

```
--lane VERIFY_SECURITY --prompt <path-to-brief> --force-rank 4 --max-candidates 1
--require-arm openai-codex/gpt-6.1-sol
```

Receipt: `ok: false`, `code: ERR_NO_ARM_EMITTED_NONCE`, `nonce_absent_arms:
["openai-codex/gpt-6.1-sol"]`. The usage receipt was fine (`openai-p6a1fe3` / `gpt-6.1-sol` / 200), so the
lane, the relay and the arm all worked. The turn itself was void.

The child's own stdout shows why, and it is worth quoting because the child behaved correctly:

> 目前無法讀取 `…/VERIFY_BRIEF_R11.md`：兩次唯讀嘗試均遭執行政策拒絕。
> **驗證狀態：INCONCLUSIVE／未驗收**。尚未取得 brief 或執行查核，也未修改任何檔案。

Its `stderr` names the rejected command: a `pwsh -NoProfile -Command "Get-Content -LiteralPath '…'"`
**rejected: blocked by policy**. So the child was handed the brief's **path as its prompt text**, tried to
open the file, was blocked by the sandbox's execution policy, and **refused to invent a verdict**. That last
part is the behaviour the governance actually wants: a void attempt, not a green one.

## The two defects

1. **`--prompt` is the prompt TEXT, not a path.** Passing a path produces a checker that is asked to
   verify a document it cannot see. Nothing in the receipt says so: the run looks like a lane problem
   (`ERR_NO_ARM_EMITTED_NONCE`) when it is a delivery problem.
2. **The role-default sandbox for a checker is `read-only`, and on this host `read-only` cannot even
   *read* through the shell** - the approval policy rejects the command outright. So a checker task that
   requires running anything needs `--sandbox danger-full-access --allow-sandbox-escalation`.

## The rule that then applies, and must be satisfied rather than bypassed

The dispatcher refuses an escalated lane that has no measurement bound:

```
ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER  (exit 4)
"an unbounded escalated lane is refused; pass --allow-unguarded-escalation to record the exception explicitly"
```

Two further guards make the naive fix fail, and both are probe-measured in the dispatcher's own source
(`scripts/hgk-lane-dispatch.py`):

- `ERR_GUARD_ROOT_MISSING` / `ERR_GUARD_ROOT_EMPTY` - a guard root that does not resolve, or that
  resolves to **zero files**, is refused **pre-spawn**, because a zero-file snapshot reports
  `mutated: false` over an empty digest pair. **A vacuous guard must never read as a clean subject.**
- `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT` - the harness's own `--json-out` and `--attempt-log-dir`
  must NOT live inside a guard root, or the receipt's own files would count as subject mutations.

## The corrected invocation (executed; this is the template)

```
--lane VERIFY_SECURITY
--prompt "<the brief's CONTENT, not its path>"
--sandbox danger-full-access --allow-sandbox-escalation
--guard-subject C:/Projects/Agent_Workspace/PIPD-r7-release
--guard-subject C:/Projects/Agent_Workspace/HG-KSEOS
--force-rank 4 --max-candidates 1 --require-arm openai-codex/gpt-6.1-sol
--json-out  <scratch, OUTSIDE every guard root>
--attempt-log-dir <scratch, OUTSIDE every guard root>
```

`--allow-unguarded-escalation` was **not** used: the guard is available, so the exception is not needed,
and taking the exception where the bound exists would be exactly the permission-widening this round keeps
refusing.

## Independent corroboration of the sandbox rule

Every successful cross-model run from the previous round carries `sandbox: danger-full-access` and
`sandbox_escalation_authorised: true` with `role_default: read-only` (5 of 5 checked), and one carries a
4041-file `subject_mutation` verdict of `CLEAN`. So the escalated-plus-guarded shape is not this round's
invention; the first R11 attempt simply omitted it.

## A third defect found while applying the fix: the guard crashes on an unreadable file

Widening the guard to the control plane made the dispatcher **crash with a raw traceback** before
spawning anything:

```
File ".../hgk-lane-dispatch.py", line 574, in snapshot_subject
    snap[str(p).replace("\\", "/")] = sha256_file(p)
File ".../hgk-lane-dispatch.py", line 392, in sha256_file
PermissionError: [Errno 13] Permission denied:
    'C:\Projects\Agent_Workspace\HG-KSEOS\var\far-lane-sod-003\evidence\relay-supervisor.cooldown.json.lock'
```

This is the same unreadable path that has blocked a whole-tree integrity snapshot of the control plane
before. Two separate things are wrong here and they should not be merged:

- the file is genuinely unreadable to this process (an environment fact), and
- **the guard has no typed path for it**: it neither skips-and-records nor refuses with a code. It
  raises `PermissionError` out of `main()`, so an operator sees a stack trace and a bare `EXIT=1` with
  no receipt. A guard whose failure mode is a traceback cannot be trusted to have run.

**Disposition taken:** the run was re-dispatched with the **PIPD subject guarded and the control plane
NOT guard-bounded**, and that reduction is **disclosed** rather than glossed: this verdict is bound by
measurement over the product repository only. The control-plane half of the brief is verified by
re-derivation (the checker runs the commands and reports raw output), not by a mutation guard. A latent
defect in the dispatcher's guard is recorded here and **not** repaired in this round: repairing it means
editing the control plane's own dispatcher, which is itself an escalated operation needing its own
admission, not a side effect of a verification run.

## A fourth delivery trap, found on the third attempt: the brief never asked for the nonce

The third dispatch used the corrected shape (content prompt, escalated sandbox, guard) and the child
**did the whole job** - 356 KB of cached input, 9,189 output tokens, a real adversarial verdict covering
C1-C7. The receipt still came back `ERR_NO_ARM_EMITTED_NONCE` (exit 3), because the dispatcher requires
the child's final message to carry the lane nonce and **the brief never told the child to emit it**. The
brief had specified "output JSON, nothing else" - so the child complied exactly and was still voided.

The gate is right to fail closed here: an unverifiable turn must not count. But the defect is in the
brief, and it is the same shape as trap 1: **a required part of the protocol was not transmitted to the
child**. Every brief must state the output contract, including the nonce on its own line before the JSON.

Revision 2 of the brief therefore carries an explicit `OUTPUT CONTRACT` section. Recorded because the
failure mode is invisible in the receipt - it reads like a lane problem, and the work is thrown away
unread.

## Cost, stated rather than hidden

One model turn (48,495 input tokens) was spent to return `INCONCLUSIVE`. It is recorded as a void
attempt, not as a failed check, and the second attempt is dispatched with the shape above. The
monitor-order count for this error CLASS is **1** - the class is fixed and re-run, not repeated.

**Claim ceiling:** `ESCALATED_CHECKER_INVOCATION_TEMPLATE_CORRECTED_AND_EXECUTED__FIRST_ATTEMPT_RECORDED_VOID_NOT_FAILED`.
