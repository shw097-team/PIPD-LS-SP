# Lane runs, final ledger — what was served, what counts, and what I got wrong

All runs this round used lane `VERIFY_SECURITY`, forced arm `opencode-go/glm-5.3-flash`, **rank 3**,
sandbox `read-only`, no escalation. A run counts only if the receipt shows a matching usage receipt AND
the nonce the dispatcher requires; anything else is content without a certified turn.

| attempt | bundle | served | s | valid? | outcome |
|---|---|---|---|---|---|
| 3 | C3 (first cut) | — | — | **refused** | `ERR_LANE_REQUIRED_ARM_ABSENT` - my hard-coded `--force-rank 1` |
| 4 | C3 (first cut) | — | — | **refused** | same code; my rank lookup was not lane-scoped (it returned PLAN rank 4) |
| 5 | C1+C3+C4 (first cut) | rank 3 | 152.08 | valid | V1-V10 all `INCONCLUSIVE` - asked for tree re-derivation the lane cannot do |
| 6 | capability probe | rank 3 | 9.10 | valid | proves the lane cannot read files or execute processes |
| 7 | C1 co-located | rank 3 | — | **INVALID** | `ERR_NO_ARM_EMITTED_NONCE` - my prompt omitted the token literal |
| 8 | C3 re-cut | rank 3 | — | **INVALID** | same defect; content was produced, the turn was not certified |
| 9 | C1 co-located (token fixed) | rank 3 | 33.99 | valid | C1a/C1b/C1d CONFIRMED; C1c INCONCLUSIVE |
| 10 | C3 re-cut (token fixed) | rank 3 | 108.13 | valid | C3a/C3b/C3d CONFIRMED; C3c overstated; C3e INCONCLUSIVE |
| 11 | C1 v2 (+ receipt pack block) | rank 3 | 10.59 | valid | **C1a/C1b/C1c/C1d all CONFIRMED** |
| 12 | C3 v2 (+ requirement row) | rank 3 | 125.60 | valid | C3c settled; C3b narrowed to stage-b; C3e still open |
| 13 | C3 v3 (+ HEAD provenance) | rank 3 | 171.82 | valid | C3e still not settled - the diff's revision vs the receipts' head |
| 14 | C3e only (+ revision binding) | rank 3 | 98.32 | valid | **C3e CONFIRMED** |

Receipts: `verify/VERDICT_*_A*.md` and `verify/invocation_VERIFY_SECURITY_a*.json`.

## Final claim state (bundle level, from valid turns only)

- **C1** — the standard build ships the contract registry: **C1a, C1b, C1c, C1d all CONFIRMED** (a9 then
  a11). The path to it was a co-location fix, not new work: the doctor receipt naming its producing
  command was already in this round's receipt pack (steps 5 and 17) and had simply not been carried.
- **C3** — declared-stage/base logic and the measured widening: **C3a, C3b, C3c, C3d, C3e all
  CONFIRMED** (a10 → a12 → a13 → a14), with one refinement the checker forced and the round now adopts:
  the "frozen-path refusals still refuse" half holds **stage-b-wise**; stage-a's new `DENIED` set omits
  `src/`, so stage-a relies on the allowlist mechanism instead of a category denial. The round's wording
  must not be read as uniformity across both stages.
- **C2 and C4** keep their earlier CONFIRMED verdicts from the pre-FAR series (attempts 10 and 14 of that
  series). **Every claim in the round now stands at CONFIRMED at bundle level, and none of it is an
  acceptance.**

## Defects I introduced in this round, stated plainly

1. **Two dispatches were invalid because I wrote "end with the token" without ever naming the token.**
   This is the same defect I had already diagnosed and fixed earlier in the same session for a different
   prompt. Both runs were re-cut with the literal token and re-served; the invalid ones are recorded as
   invalid rather than quietly re-labelled.
2. **My first C1 and C3 bundles did not carry the blocks their own sub-claims needed** - the receipt pack
   for C1c, the admitted requirement's wording for C3c, the HEAD provenance for C3e. Three separate
   co-location gaps, each found by the checker rather than by me. The new COVERAGE guard does **not**
   catch this class: it enforces that the blocks I *declare* are kept, and it cannot know which block a
   sub-claim requires. Its honest ceiling: it prevents the attempt-8 shape (a receipt claiming a block
   that was dropped), not an under-specified spec.
3. **One bundle exceeded my own 29 k argv guard** (37,955 chars). The guard refused it before dispatch;
   the work was re-cut as a focused single-sub-claim bundle instead.
4. **The a7/a8 content is real but not certified.** It is preserved (attempt stdout) and is not cited as
   a verdict anywhere.

## What this ledger does not claim

That any of this is verification of the repository. The lane audits the bundle it is handed (see
`VERIFICATION_LANE_CAPABILITY_BOUNDARY.md`); a CONFIRMED verdict means the inline blocks settle the
sub-claim, nothing more. Tree-level verification remains for the external acceptance officer.

---

## FAR round 2 (the F1 remedy): attempts 20-22

| attempt | lane | purpose | outcome |
|---|---|---|---|
| 20 | EXECUTE | bounded writer: recommend a remedy for F1 from a packet carrying the measurement | served 10,484-byte draft; independently recommended the SAME option as the executed remedy, citing the same deciding measurement. Not treated as authority: the executor's plan was already formed from the measurement and the draft is recorded as corroboration |
| 21 | VERIFY_SECURITY | audit bundle v1 (blocks: gate step, run log, measurement, provenance) | valid turn (rank 3, nonce, usage receipt). **R2/R3/R6 CONFIRMED; R1 REFUTED; R4/R5 INCONCLUSIVE** |
| 22 | VERIFY_SECURITY | audit bundle v2 (corrected R1 wording; the two missing derivations carried) | valid turn (91.09 s, rank 3, nonce). **R1-R6 all CONFIRMED**, each citing the block text that decided it |

### What attempt 21 REFUTED, and why that matters more than the reversal

R1's v1 wording said "no allowlist entry was ADDED by this change". The checker read "this change" against
the frozen subject, found `added: [docs/USER_GUIDE.md$]` in the measurement, and refuted the claim. The
underlying fact was not wrong; MY WORDING WAS AMBIGUOUS about the comparison baseline, and an ambiguous
claim is a defective claim. v1 also asked the checker to accept a necessity derivation it did not carry,
and truncated its own pair diff at 400 chars - so R4 and R5 were INCONCLUSIVE on bundle defects, not on
the remedy. Counted as class **E9 (bundle under-specification), which is now 5 instances this session**,
all found by the checker and none by my own guards.

Lesson recorded rather than narrated: a claim handed to a checker must name its comparison baseline
explicitly, and any figure the claim depends on must be a carried block, not prose. The v2 bundle is what
that rule produces; it also survives a stricter reading, which v1 did not.
