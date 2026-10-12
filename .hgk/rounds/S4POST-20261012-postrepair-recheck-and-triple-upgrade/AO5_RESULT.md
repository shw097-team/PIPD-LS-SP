# AO5 RESULT SUMMARY - round 5, independent handover adjudication

Verdict artifact: `verify/ao5/AO_VERDICT_HANDOVER_R5.md` (70,106 bytes, 128 evidence files).
Lane: `AO5_20261012T130513Z`, checker `gpt-6.1-sol` / provider `openai` (OAuth) / reasoning `medium` -
the declared VERIFY/SECURITY model. Launched by the governed launcher itself, which reported
`PREFLIGHT_CLEAN HEAD=c93a41f` and `POSTFLIGHT:dirty=0 HEAD=f43c130`.

## The verdicts

| | Round 3 | Round 4 | Round 5 |
|---|---|---|---|
| Adjudication A (handover) | NOT_CLOSED | PARTIAL | **STILL_NOT_CLOSED** |
| Adjudication B (enforcement) | - | FAIL on 3 demonstrated branches | **real on the repaired branches, but still fails open** |

AO5's own ceiling statement: local stub control-flow verification on this host and subject; no model was
launched; "a stub proves control flow and proves nothing about a model".

## Why A is STILL_NOT_CLOSED, and it is the maker's fault

The one untracked path present before any officer evidence existed was the **launcher's own lane
manifest**, which v2 wrote into `stage-b/` *after* its clean preflight. The dispatch is now `AO5`-clean of
the officer, so the residual dirt was produced by the harness, not by the officer and not by stale maker
work. **Fixed**: the manifest is written outside the worktree and copied in at postflight, like the lane
log. This entry is not evidence that the fix works; only a later independent round can be.

## Adjudication B: five newly demonstrated fail-open paths, and their disposition

| ID | What AO5 demonstrated | Status |
|---|---|---|
| R1 | an exit-receipt copy failure returned 0 and was only a printed note | **fixed** - a failed receipt copy is fatal (exit 6); T7 |
| R2 | a **failed** `git status` produced empty output, was read as `0` paths, and the wrapper printed `PREFLIGHT_CLEAN` / `POSTFLIGHT:dirty=0` | **fixed** - a nonzero status query is fatal (exit 2); T8 |
| R3 | an already staged **outside-round** file was committed and admitted by the preflight | **fixed** - any staged path outside the round is refused (exit 6); T9 |
| R4 | `GATE_QUALIFY_RUNS=0` invoked no qualification at all yet printed `QUALIFICATION_PASSED ... consecutive_runs=0` and `LANE_SET_OK` | **fixed** - the count must be a positive integer or the gate refuses (exit 3); G8 |
| R5 | the gate qualified EXECUTE through the catalog route but launched the writers through the **default** route - it validated one lane and started another | **fixed** - the role's route is exported to the children, and G9 asserts the child's argv contains the catalog slug and no provider id |

All five are genuine. None was a hypothetical: each came with a command and its raw output. The maker's
previous claim of "universal fail-closed enforcement" is withdrawn; what is claimed now is exactly the
branches covered by T1-T9 and G1-G9, and nothing wider.

## Still open, stated so it is not mistaken for closed

- **Closure is still not independently confirmed.** Three consecutive rounds have each found real
  defects. The loop is converging and is not finished. A round 6 would be required to test these fixes.
- AO5's note that "ordinary output placement is not a physical containment proof" is not rebutted.
- AO5 could not clone the delivery from its sandbox identity
  (`dubious ownership`: lane user `CodexSandboxOffline` vs repo owner `user`), so several attacks were
  run against an external clone it prepared differently. Its report says so itself.
