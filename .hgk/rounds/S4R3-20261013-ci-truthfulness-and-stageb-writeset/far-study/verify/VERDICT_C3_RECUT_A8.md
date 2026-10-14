**C3a — CONFIRMED.** BLOCK 1 reports the stage-b allowlist as 14 entries against a frozen base of 12, with `+ 2 added` and `- 0 removed`. The two named additions are exactly `docs/USER_GUIDE\.md$` and `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`. The entry-level set-diff (not line counts) supports the "exactly two" wording.

**C3b — CONFIRMED.** BLOCK 1 shows the stage-b DENIED set as `skills/`, `src/`, `schemas/`, `dist/`, identical to the frozen base's DENIED set. BLOCK 2 confirms this in the workflow step (`DENIED='^(skills/|src/|schemas/|dist/)'`) and includes self-tests proving planted frozen-path violations are still refused.

**C3c — CONFIRMED / no overstatement found.** All three components of the corrected wording are supported by the inline blocks:
- "gained exactly two entries relative to the frozen subject" — supported by the mechanical set-diff in BLOCK 1.
- "against an admitted requirement whose wording forbids widening" — supported by BLOCK 2's inline comment ("This change widens NEITHER allowlist"), which is an admission in the workflow itself that conflicts with the measured diff.
- "The write-set gate judges the branch's DECLARED stage and base rather than the pull-request base" — supported by BLOCK 2 (see C3d below).
- "the frozen-path refusals still refuse" — supported by BLOCK 2 self-tests and BLOCK 3 receipts.

No part of the corrected wording is unsupported by the blocks as presented.

**C3d — CONFIRMED.** BLOCK 2 shows:
- `STAGE: stage-a` declared in env (branch declares its stage).
- Stage-specific `STAGE_A_BASE_SHA` / `STAGE_B_BASE_REF` used as the governed base, not `PR_BASE_SHA`.
- `PR_BASE_SHA` is explicitly printed as `CONTEXT ONLY, not a governed write set`.
- The actual diff is `git diff --name-only "${BASE}...HEAD"` using the declared base, not the PR base.
- An `BASE_NOT_ANCESTOR` check ties the declared base to the subject.

**C3e — INCONCLUSIVE.** The refusal receipts in BLOCK 3 show governed base SHAs (`e71fee6dd3aa...` for stage-a, `5310896e706e01a9...` for stage-b) and self-test outputs, but do not reproduce the HEAD commit hash at which the gate was run, nor the exact revision of the workflow file used. BLOCK 1 compares the frozen subject against "current Stage A head" and "current stage B head" but names SHA `ba27309b50...` for stage B only in the command listing, not linked to the receipt run. Without a block that explicitly ties the receipt's workflow revision to the revision in the diff, the identical-revision claim cannot be settled from what is inline. The missing block would be a reproduction of the receipt's HEAD SHA alongside the diff's HEAD SHA (or a hash of the workflow file at receipt time matching the diff baseline).

DFN:  d4fc253f

3fara8</arg_value></tool_call>