C3a — Yes. `BLOCK 1` supports exactly two stage-b additions relative to the frozen subject’s allowlist: `docs/USER_GUIDE.md` and `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`. It reports 14 stage-b entries against the 12 frozen-base entries, with two added and none removed.

C3b — Yes for stage-b. `BLOCK 1` shows the frozen stage-b `DENIED` set and current stage-b `DENIED` set are the same: `dist/`, `schemas/`, `skills/`, and `src/`. That supports the stage-b frozen-path refusal. It does not support the stronger claim that every frozen-path denial is unchanged across all stages, because stage-a’s new `DENIED` set omits `src/`; unlisted stage-a `src/` paths are refused by the allowlist mechanism instead.

C3c — No unsupported or overstated part for the corrected wording itself. `BLOCK 2` supports declared-stage/declared-base comparison, `BLOCK 1` supports the exact stage-b widening and stage-b denial continuity, and `BLOCK 4` confirms the admitted requirement explicitly says “The allowlists must not be widened.” The one necessary qualification is that the denial-set claim is firmly stage-b; applying it uniformly to stage-a would overstate `BLOCK 1`.

C3d — Yes. `BLOCK 2` selects behavior from `STAGE`, uses `STAGE_A_BASE_SHA` for stage-a and `STAGE_B_BASE_REF` for stage-b, checks that the chosen base exists and is an ancestor of `HEAD`, and then diffs `${BASE}...HEAD`. `PR_BASE_SHA` is only printed as context and is never selected as the governed base.

C3e — Inconclusive. `BLOCK 5` identifies the worktrees and shows `${BASE}...HEAD` in the local output, but it does not print the commit SHA for either `HEAD`. It also does not provide hosted run IDs or hosted `HEAD` SHAs, and its local source hash covers a receipt/log artifact rather than proving which commit was checked out. `BLOCK 1` names stage-b head `ba27309b50d8623ed9d3ad9b33fe7a4ffb8a9ede`, but no block explicitly ties the refusal receipts’ `HEAD` to that revision. The missing provenance is a run checkout manifest or equivalent block showing `git rev-parse HEAD` for both local worktrees and the hosted CI revision that produced the receipts.

Likewise, `C3c` remains settled against `BLOCK 4`; the no-widening obligation is present verbatim in a FROZEN requirement. `C3e` remains unsettled against `BLOCK 5`.

HGK_LANE_NONCE_OK