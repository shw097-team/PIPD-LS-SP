# pipd-r18-external-engineering-handover

## Why

The S4 R6 closeout round delivered a working candidate (install-doc release-identity pin, the
same-`plugin_id` update route, and a doc-identity guard) and published its evidence on a dedicated
branch. Two gaps remain, both about the reader rather than the product:

1. **The round's own plan documents contradict its evidence.** `TASK_CHECKLIST.md` and
   `DETECTION_CHECKLIST.md` were never back-filled, so a reader who opens the plan first sees a round
   that appears not to have started, while the packet's own rows say otherwise. A verifier who finds
   the contradiction first has found a credibility defect.
2. **Nothing tells an external engineering team how to continue.** The repository carries real
   mechanisms an outsider cannot infer quickly: a **positive write-set gate** in CI that judges
   `git diff --name-only <declared base>...HEAD` against a per-stage allowlist; a **branch model** in
   which round evidence deliberately lives outside the governed product write set; a **lane model**
   whose ordered candidate pool can silently destroy separation of duties; and immutable release
   assets that must never be edited in place.

## What Changes

- `S4_R6_CLOSEOUT_RETURN/TASK_CHECKLIST.md` and `…/DETECTION_CHECKLIST.md` are back-filled so their
  status and evidence columns agree with the executed round. Nothing in them is *rewritten*: each row
  gains the artifact that actually exists, and any row that is genuinely `NOT_RUN`/`DEFERRED`/
  `OWNER_GATE` says so in its own words.
- A new `S4_R6_CLOSEOUT_RETURN/EXTERNAL_ENGINEERING_HANDOVER.md` gives an external team the entry
  path: repository and branch model, the write-set gate and how to reproduce it locally, the lane
  model and its owner-ordered collision, the commands that build and test, a module map with
  extension points, and the standing prohibitions.
- A new `S4_R6_CLOSEOUT_RETURN/ROUND_STATE.json` carries the same facts machine-readably (branch tips,
  immutables, gates, tickets, claim ceiling) so tooling does not have to parse prose.
- These land on the **evidence branch**, never the product branch: the `stage-c` allowlist admits
  product-shaped paths only, and that exclusion is the point.

## Constraints

- No merge, no tag, no release, no change to `main` or to `v0.1.1-preview.4` or its assets.
- The handover document must not assert anything a reader cannot re-run: every factual claim carries
  a named command or a file locator.
- No claim of `S4_FULL_PASS`, `HOST_QUALIFIED` or `PRODUCTION`; private-host UAT stays `NOT_RUN`.
