TASK: produce the FAR round 2 recommendation specified at the end of this packet. Write it to C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt/.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/EXECUTE_REMEDIATION_DRAFT.md and ALSO return it as your final message.

FINAL LINE (required, verbatim, nothing after it): output exactly this token on its own line:
HGK_LANE_NONCE_OK

=== PACKET BEGINS ===
# FAR round 2 packet — F1 allowlist remediation (EXECUTE lane, bounded writer)

You are the bounded writer for a governed round. Everything below is a MEASURED fact with its locator,
or is marked as an owner input. Do not add facts from your own knowledge, do not soften a measurement,
and write NOT_SUPPLIED rather than filling a gap.

## 1. The subject

Repo `shw097-team/PIPD-LS-SP`. Branch `feat/s4r3-stageb-successor-20261013`, head
`35a68f0c05a26747c2a1553cb86505ac26909b88`, stacked on the Stage A branch
`fix/s4r3-stage-a-ci-truthfulness-20261013` at `5310896e706e01a9cdb0123285bccec75086bcb8`.
Each branch carries its own copy of `.github/workflows/public-plugin-verify.yml`; that copy declares its
own `STAGE:` and the bases it needs. The file contains the write-set gate: it computes the governed diff
for the declared stage and refuses any changed path that is neither ALLOWED nor DENIED-consistent.

## 2. The finding under remediation

The admitted, FROZEN requirement `REQ-S4R3X-GATE-FALSIFIABILITY-002` says "The allowlists must not be
widened and the frozen-path refusal must still refuse". Measured against the frozen subject
`e71fee6dd3aa73724baec4e8d9cc72127fbe36ed`, the stage-b ALLOWED set gained **two** entries:

1. `docs/USER_GUIDE.md$`
2. `\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`

and the workflow's own inline comment asserts "This change widens NEITHER allowlist", which is false as
written. The stage-b DENIED set is unchanged (`skills/`, `src/`, `schemas/`, `dist/`). Stage-a is a
different stage whose DENIED set omits `src/`; the continuity claim therefore holds **stage-b-wise only**
and must not be read as uniform.

## 3. The measurement that constrains the remedy (locator: evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json)

Method: reproduce the gate's own governed diff for the stage this branch declares, extract the
ALLOWED/DENIED sets from the workflow at the current head, classify every changed path, then test
candidate narrowings by asking whether the diff would still pass.

Measured on branch B (STAGE: stage-b, governed base resolved from `STAGE_B_BASE_REF` = the Stage A head):

- governed diff: **151 changed paths**, of which **UNLISTED = 0** and **DENIED = 0**.
- `docs/USER_GUIDE.md` **is inside that diff** - so entry 1 is load-bearing: removing it would make that
  path UNLISTED and the gate would refuse a path Stage B legitimately ships.
- **143** of the 151 paths are under the round directory: `far-study/` 83, `evidence/` 38, `scripts/` 18,
  three files at the round root, `admission/` 1.
- Narrowing entry 2 to `.../evidence/` alone loses **105** paths; to `.../(evidence|far-study)/` loses
  **22**; to `.../evidence/12_GATES/` loses **105**. Every tested narrowing fails, because the round
  commits its own working material (study, tools, admission record) into that tree as it proceeds.

## 4. Options that follow from the measurement

- **Option A - wording only.** Keep both entries; replace the false comment with one that enumerates the
  two additions, states which one the diff requires, and states the stage-b-only scope of the DENIED
  continuity. Cost: 1 edit per branch copy. Leaves the allowlist widened by 2.
- **Option B - move the scaffolding out of the allowlist instead of permitting it.** Declare `.hgk/**`
  out of the PRODUCT write set explicitly (a printed `EXCLUDED_PREFIXES` with a stated reason: the round
  evidence tree is scaffolding, not product), and **remove** both `.hgk/rounds/...` entries from the
  allowlist, including the pre-existing `.hgk/rounds/S4POST-20261012` one. Then the allowlist enumerates
  product paths only and the widening versus the frozen baseline becomes **+1** (`docs/USER_GUIDE.md`),
  which the diff is measured to require. Cost: ~3 lines per branch copy, plus the self-test must be
  extended to prove that a planted PRODUCT violation is still refused and that the exclusion is printed
  in the receipt so a reviewer sees it.
- **Option C - declared deviation, no edit.** Register the widening and the false comment and change no
  candidate content. Cost: 0 engineering; leaves a false statement in shipped content.

## 5. Constraints

Low friction; high engineering necessity; not over-engineered (a remedy must beat doing nothing);
aligned to the task core (the R3 prompt, the external acceptance report, the upstream blueprint); usable
by an external acceptance officer who must be able to open an artifact and re-run something. No oracle,
threshold, validator, guard, exit code or denominator may be relaxed. No merge, tag, release or archive.

One further constraint that is itself measured: any edit to `.github/workflows/public-plugin-verify.yml`
changes a **candidate head on both branches** (the file exists on A and on B), so the stacked invariant
must be restored (`git merge-base <A> <B>` equal to the A head) and the C3/C4 receipts must be re-cut at
the new revision. No acceptance has been granted on the current heads, so superseding them costs nothing
that has been earned - state this explicitly if you recommend editing.

## 6. Deliverable (return as your final message; the parent persists it)

A. the recommendation among A/B/C with the single measurement that decides it;
B. for the recommended option, the exact edit per branch copy, with the allowlist entries added and
   removed listed separately;
C. what must be re-run and re-cut afterwards (gate self-tests, C3 diff receipt, C4 repin, lane
   verdicts), and what each re-run would falsify;
D. what the external acceptance officer gains and loses under the recommendation;
E. the DO-NOT list.
Keep it under 400 lines. Cite this packet by section; do not restate it.
