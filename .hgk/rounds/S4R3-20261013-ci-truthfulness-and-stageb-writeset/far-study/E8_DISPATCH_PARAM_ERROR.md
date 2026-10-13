# E8: the checker-arm refusal was my own dispatch parameter error, and I first reported it as an
# environment change

## What happened, in order

1. The FAR round's VERIFY dispatch returned `ERR_LANE_REQUIRED_ARM_ABSENT`: "opencode-go/glm-5.3-flash
   is not in the VERIFY_SECURITY pool". The receipt's identity gate listed exactly one arm, rank 1
   `opencode-go/deepseek-v4.1-flash`.
2. I reported to the user that the pool had changed under us, that attempts 7-14 had used that arm
   earlier in the session, and that the failure was a quota/availability drop. **All three of those
   statements were inferences I had not re-derived, and the third was wrong.**
3. I then measured. The relay still lists `opencode-go/glm-5.3-flash` (87 models, present). The pool
   file `config/lane-route-slots.candidate.json` has not been modified since 2026-10-11. The
   VERIFY_SECURITY `ordered_pool` still carries `opencode-go/glm-5.3-flash` at **rank 3**, feasibility
   **DISPATCHABLE**.
4. Root cause: my new helper `scripts/far_run_lane.py` hard-coded `--force-rank 1` for both lanes. The
   dispatcher matches `--require-arm` against the candidate list **after** `--force-rank` filters it, so
   filtering to rank 1 removed rank 3 from the list and the required arm read as ABSENT. The earlier
   round scripts carried `--force-rank 3 --require-arm opencode-go/glm-5.3-flash` and worked. Nothing in
   the environment changed; my parameter was wrong.

## Why this is recorded as a finding and not fixed silently

The damaging part is not the wrong flag - it is that I narrated a cause (pool changed, quota drop)
before re-deriving it, to the user, as a fact about the environment. That is the same class as the five
earlier instances: **a self-authored claim contradicted by a checkable record**. It is instance 6.

## What actually protected the round

The `--require-arm` guard did. VERIFY_SECURITY rank 1 is `opencode-go/deepseek-v4.1-flash` - the *same*
model as the EXECUTE writer. A dispatch without the required arm would have had the writer's own model
adjudicate its own study, with a clean receipt and no visible defect. The pool's own change log records
this overlap as `recorded_not_enforced`: "deepseek-v4.1-flash is rank 1 (EXECUTE/VERIFY) and ranks 1-2
(PLAN) - the same identity can occupy all three lanes". The guard, not the pool, is what keeps
maker/checker separation here.

## Remediation, landed with this file

`rank_for_arm()` resolves the rank from `lanes[].ordered_pool[]` instead of trusting a literal, and
returns `0` (a rank that cannot match) when the arm is absent, so the dispatcher refuses in-contract
rather than falling through to another arm. The rank is recorded in each invocation receipt.

## The rule this earns

For any lane refusal: dump the pool, the resolved rank filter and the arm's declared rank **before**
naming a cause. An inference about the environment is not evidence about the environment. The previous
instances of this class were caught by other people's checks or by luck; this one was caught only
because a follow-up measurement happened to be cheap.
