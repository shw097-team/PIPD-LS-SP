# Independent acceptance brief — FAR adjudication candidate

You are the **Independent Acceptance Officer**. You did not write this candidate and you may not
repair it. Work **read-only**: write only under `.ao-far/` in this clone. No network, no git history
changes, no commit, no push, no tag, no publish.

Subject: the FAR adjudication candidate at commit **`ad33c0c679ac329a38cb9b0c0127a51211e3e09e`**
(branch `fix/s4post-far-adjudication-20261012`). File set under test:
`tools/model_eligibility_probe.py`, `tests/test_verify_evidence_digests_basis.py`,
`tests/test_model_eligibility_probe.py`, `docs/FAR_S4POST_ADJUDICATION_2026-10-12.md`, and the
existing gate `tools/verify_evidence_digests.py` (claimed UNCHANGED by the writer).

**Do NOT read** `WRITER_v2b_OUTPUT.log`, `docs/FAR_S4POST_ADJUDICATION_2026-10-12.md`'s summary
claims, or any orchestrator summary as evidence. **Re-derive every decisive claim yourself.** If you
cannot re-derive something, say so with a typed `UNCERTAINTY` rather than repeating it. If your
measurement disagrees with a claim, emit a typed `DISAGREEMENT` with both numbers.

One repository fact to use, not to trust: the sealed candidate commit named in the manifest context
is `f541c3968d8b3fc1d2dfd71bab1b0d56894f05ce`; read the candidate head from the sibling seal if one
exists in the tree rather than hard-coding it.

## Claims to test — each PASS / FAIL / INCONCLUSIVE, with your own raw evidence

- **C1 — suite green at the subject**: run `python -m unittest discover -s tests -t .` yourself.
  Report `Ran N / OK|FAILED (…)` verbatim. A suite that errors, or that you had to edit to run, is FAIL.
- **C2 — the measurement**: run `python tools/verify_evidence_digests.py --json`. The claim is
  `checked 1085, match_raw 1038, benign_eol 5, unexplained 42`. Independently verify the METHOD, not
  the number: pick at least 4 entries from the manifest yourself, compute their digests by hand
  (disk bytes, CRLF/LF variants, and the sealed-candidate blob via `git show <cand>:<path>`), and
  show that the tool's classification of each is what your own computation implies.
- **C3 — the gate is real, not a rubber stamp**: this is the decisive claim. Build a case where a
  recorded digest matches some basis but the content differs **beyond** line endings, and show the
  tool reports it as `unexplained` (never `benign_eol`). Then show `--strict` exits non-zero on this
  tree while the default run exits 0. If you can construct any input for which real content drift is
  reported as benign, that is a FAIL of C3 and it blocks.
- **C4 — the new tests are not vacuous**: for EACH of the two new test modules, disable or defeat the
  behaviour it claims to pin (in a scratch copy, never this clone) and show the module then FAILS;
  restore and show it passes. A module that still passes with its target defeated is FAIL.
- **C5 — no existing expectation was weakened**: diff every test file the candidate touches against
  the base commit `55f15697a6dbc9016239e58dbce1aaf740e0c5d7` and report any changed or deleted
  assertion. State plainly whether `tools/verify_evidence_digests.py` is byte-identical to the base.
- **C6 — write set respected**: list the tracked files the candidate changes relative to the base.
  Any file outside the declared set is FAIL.
- **C7 — no self-mutation**: snapshot the hashes of the candidate's tracked files before and after
  your checks. If they differ, your verdict is self-voiding: report that.

## Output

Write `.ao-far/FAR_VERDICT.json` with `subject`, `tree`, `claims[]` (id, result, evidence, note),
`blocking[]`, `candidate_mutated`, `identity`, `execution_disclosure`, and a `verdict` of
`PASS_CHALLENGE` / `FAIL_CHALLENGE` / `INCONCLUSIVE`. Print the same JSON as your final answer.
Your verdict is an **advisory independent check** — it does not by itself accept, release or promote
anything, and no canonical token may be derived from it. Do not claim otherwise.
