# INDEPENDENT CHECKER BRIEF — R5P terminal pass (attempt 4, C6 only) — PIPD-LS-SP

Attempt 3: `C2 PASS`, `C8 PASS`, `C6 FAIL (EVIDENCE_GAP)`. C6 was repaired on the strength of your own
wording. **This is the terminal pass of the round**: judge C6 on the new frozen subject, and if anything
remains imperfect, record it as a named residual limitation with your scope instead of asking for another
cycle. Do not re-open C1/C2/C4/C5/C7/C8 — they are settled.

## Subject

| role | value |
|---|---|
| baseline (immutable) | `r5-s4-packreader` @ `0f06eec96386b7349db8b41ac6cf9c7455d326f1` |
| **subject under review now** | **`194f1774e8e852f954d141c48389a74b0f0e302a`** (tree `b1ec0abf4799fdc917aaa23dc75885b302407ee5`) |
| attempt-3 subject | `9caef8ec…` — superseded by this commit |
| only change since attempt 3 | `ACCEPTANCE.md` first-screen banner |

Mounts: `/w` = pristine export of the new subject (read-only, no `.git`), `/round` = round evidence
(read-only), `/briefs` (read-only), `/ao` = your only writable place.

## C6 question, precisely

Your attempt-3 note asked for two things: (1) mark attempt-2's commit/tree/digest as superseded rather
than current, and (2) give an external binding entry point for the current subject — **and you stated that
the file must not be required to self-reference its own digest.**

Verify, on `/w/ACCEPTANCE.md` lines 1–34 and `/w/README.md` first screen:

1. Does the first screen now identify the branch under review, the licence position and the claim ceiling?
2. Are the attempt-2 values explicitly labelled as superseded history, or are they still presented as the
   current subject?
3. Does it give a reproducible external entry point for the current subject's identity — i.e. a path in
   `.hgk/rounds/R5P-20261010-s4-post-challenge/` (which the bound product digest excludes) — and does that
   entry point actually contain the current commit/tree/wheel/digest when you read it?
4. Is the banner stable under further commits to this branch, i.e. does it avoid asserting a digest that a
   subsequent commit would invalidate?

## Deliverable

`AO_VERDICT_V4.json` in `/ao`: `checker_id`, `subject_commit`, `subject_tree`, `checks` (C6 only, with
`verdict`, `evidence` paths, `commands` with exit codes, `note`), `overall`, `classification`,
`residual_limitations` (named, each with scope), `independent_of_maker`, `human_ratification: PENDING`,
`claim_ceiling: CANDIDATE_ONLY`. Log in 繁體中文. If C6 passes, say plainly that the round's document
binding is closed for this subject and name anything you still cannot confirm from a read-only mount.
