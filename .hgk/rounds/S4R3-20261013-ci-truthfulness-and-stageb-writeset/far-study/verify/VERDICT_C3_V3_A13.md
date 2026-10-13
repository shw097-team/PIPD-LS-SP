Adjudication on the inline blocks only:

- C3a — confirmed. BLOCK 1 supports exactly two added stage-b entries: `docs/USER_GUIDE.md` and `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`.
- C3b — confirmed, but only as stage-b. The stage-b DENIED set is unchanged. It should not be asserted as an unchanged denial set for both stages, because BLOCK 1 shows stage-a omits `src/` and relies on the allowlist instead.
- C3c — no unsupported substantive widening claim. The no-widening obligation is admitted and frozen in BLOCK 4. The only wording caveat is the same as C3b: “frozen-path refusals still refuse” must be read stage-b-wise, or split from stage-a’s different mechanism.
- C3d — confirmed. BLOCK 2 uses the declared `STAGE` and declared base to compute the governed `BASE...HEAD`; the PR base is printed only as context and is not the judged range.
- C3e — not fully confirmed. BLOCK 5 gives the bases and self-tests, and BLOCK 6 gives worktree HEADs and hosted run/SHA mappings, but it does not tie each quoted hosted receipt to a specific run id or resolve the stage-b revision mismatch needed to show it is the same revision as the diff’s target.

HGK_LANE_NONCE_OK