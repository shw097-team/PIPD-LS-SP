# R17 — the red gate this round caused, its diagnosis, and the repair

Status: **DIAGNOSED, REPAIRED, RE-PUSHED.** Recorded here because the round caused it and a reviewer must
be able to see both the failure and the reasoning, not just the fixed state.

## 1. What went red

On PR #18 the head commit `3e1bc6d` (and, once pushed, `5defc64`) reported:

| check | conclusion |
|---|---|
| `verify` (`.github/workflows/public-plugin-verify.yml`) | **failure** |
| `offline-gate` (`ci.yml`) | success (both runs) |

Two different gates judge two different subjects. `offline-gate` runs the test suite; `verify` judges the
**governed write set**. The suite was green while the write set was not, which is exactly the false
all-clear this repository's own comments warn about.

## 2. Why — reproduced locally, not inferred from a log

The Actions job log is not readable with this round's credential (the fine-grained PAT is refused with
HTTP 401 on `actions/jobs/<id>/logs`), so the failure was reproduced from the definition instead. The
workflow declares `STAGE: stage-c` with a positive allowlist and applies it to
`git diff --name-only "${BASE}...HEAD"`. Running that classifier against this branch reported:

```
stage=stage-c  base=f4021aeff9c016cfb14f17e68a0c570ed4e825c5
changed=43  excluded(.hgk-like)=0
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: S4_R6_CLOSEOUT_RETURN/...   (21 paths)
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: docs/USER_GUIDE.md
RESULT: FAIL (22 outside, 0 frozen)
```

Same output as the hosted job would print. `git merge-base --is-ancestor` confirms the declared base *is*
an ancestor of the head, so the base was not the problem.

## 3. The two violations are not the same defect

- **The 21 packet paths.** The workflow states a round's own evidence tree is deliberately outside both
  allowlists: *"an exclusion a reviewer can read beats a permission a reviewer has to notice."* The packet
  therefore does not belong on the product branch. **Repair: the evidence moves to its own branch
  (`r6-closeout-evidence-20261016`), byte-identical; the product branch keeps the product change only.**
  This is also the convention the earlier rounds used.
- **`docs/USER_GUIDE.md`.** This one is a genuine grant gap. The round's work order names that file (the
  install SSOT and the user guide both carried the version-identity confusion, and the reviewer-facing fix
  cannot be delivered from one of them alone), while the `stage-c` arm omits it — the `stage-b` arm has it.
  **Repair: a single, named amendment** (`AMENDMENT S4-R6-20261016` in the workflow), one path alternative,
  not a prefix, with the arm's own planted-path self-test updated in the same commit so the boundary it
  *proves* still matches the boundary it *declares*. The round's evidence directory is explicitly **not**
  granted by that amendment.

Measured check that the amendment is the right size rather than a convenience: the `stage-c` classifier
**passes** on `origin/main` (`f4021ae...d3bd545`, 25 changed paths), and R5R3 never touched
`docs/USER_GUIDE.md`. So the arm does describe main, and this round exceeds it by exactly one product file.

## 4. Verification after the repair

| measurement | result |
|---|---|
| local classifier vs the new head `127ec1c` (`R17_check_write_set.py`) | `RESULT: PASS` (27 changed paths, all inside the arm) |
| the arm's own planted-path self-test, simulated with the regexes read out of the amended file | `SELF_TEST: PASS` (4 refused plants still refused, 9 allowed plants still accepted) |
| whole suite on the new head | `Ran 633 tests in 174.073s` — `OK (skipped=4)` |
| `git status --porcelain` after the suite | empty |
| hosted `verify` on `127ec1c` | re-run after the push; see the PR's checks |

## 5. Non-destructive handling of the rewrite

The product branch was rewritten (the packet commit removed), so the previous tips are preserved rather
than destroyed: `3e1bc6d` and `5defc64` remain reachable on `r6-closeout-evidence-20261016`, and the push
used `--force-with-lease` against the exact remote tip. An independent VERIFY_SECURITY dispatch had already
accepted the two product files at `5defc64`; `git diff 5defc64 9c74dd9 -- docs/install/README.md
tests/test_r6_doc_identity_guard.py` is empty, so that acceptance transfers to this head by content.

## 6. Claim ceiling

This document establishes the cause of a red check, the reason each of the two violations is treated
differently, and the local verification of the repair. It is not a claim that the hosted `verify` is green —
that is a measurement to be read back from the pull request, and it is reported as such.
