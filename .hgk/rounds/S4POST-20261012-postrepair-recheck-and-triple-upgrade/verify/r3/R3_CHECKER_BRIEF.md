# Independent acceptance brief — S4POST R3 candidate (owner-mandated VERIFY/SECURITY lane)

You are the **Independent Acceptance Officer** on the owner-declared lane (CODEX CLI, checker model
`gpt-6.1-sol`, OpenAI OAuth, reasoning effort medium). You did **not** write this candidate and you may
**not** repair it. Work **read-only**: write only under `.ao-r3/` in this clone. No network, no git
history changes, no commit, no push, no tag, no publish, no edits to any tracked file.

## Subject (bind exactly, do not accept a moving target)

- Primary subject commit: **`389d3973da73e5740f0b4d290bacb92d1e8982f8`** — branch
  `feat/s4post-triple-upgrade-20261013-r3` (the product changeset, split out of the round's worktree).
- Companion branches (read-only context, do not merge): `feat/s4post-triple-upgrade-20261012-r2`,
  `chore/s4post-verification-harness`.
- `main` must still be **`224591431a164ab72a9423cd180e417e8a762403`** and must be untouched.
- Round directory: `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/`

**Do NOT read** any maker summary, this brief's own claims, or a log as *evidence*. Re-derive every
decisive claim yourself from the tree. If you cannot re-derive something, emit a typed `UNCERTAINTY`
with the reason. If your measurement disagrees with a stated claim, emit a typed `DISAGREEMENT` giving
both numbers — do not average them or pick one.

Interpreter: use `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (3.11.9, has
`jsonschema`). Set `PYTHONPATH` to this clone when running suites.

## Claims to test — each `VERIFIED` / `FAILED` / `INCONCLUSIVE`, each with your own raw output

1. **C1 focused suite** — `python -m unittest discover -s tests -p 'test_s4ext_*.py' -v`. Record the real
   exit code and the literal `Ran N tests` line. Claim under test: 108 tests, OK. A suite you had to edit
   to run is FAILED.
2. **C2 full suite** — `python -m unittest discover -s tests -t .`. Record exit code, `Ran N tests in Xs`
   and the OK/skip line. Claim under test: 572 tests, OK. Record the SKIP COUNT you observe verbatim;
   a different skip count from the maker's is not by itself a failure — say what you saw.
3. **C3 the suites do not mutate the subject** — capture `git status --porcelain` and
   `git status --porcelain --ignored` BEFORE and AFTER running both suites, and report the set
   difference (name the entries, do not just count). Claim under test: zero new entries of either kind.
4. **C4 the documented acceptance commands are executable as written** — open
   `R3_PUBLICATION.md`, take its §3 acceptance block **verbatim**, and execute it in this clone, step by
   step, recording each real exit code. For any step that cannot be executed as written, give the exact
   error. This is the claim the previous independent pass refuted once; test it yourself.
5. **C5 locator negative control must fail closed** — run
   `python verify/tools/check_evidence_locators.py --root . --search-dir . verify/ao12/EXTERNAL_CHALLENGE_REPORT.md`
   with the round directory as cwd. A non-zero exit with `FAIL_LOCATORS_NOT_RERUNNABLE` is the PASS
   condition here (the control's job is to refuse).
6. **C6 locator positive control on THIS subject** — run
   `python verify/tools/check_evidence_locators.py --root . --search-dir . <round>/OWNER_ACTION_REQUEST.md <round>/HARNESS_FREEZE_AND_AO_LOOP_CAP.md`
   from the clone root. Claim under test: exit 0 / `PASS_LOCATORS_IN_TREE`. If it fails, list every
   offender. Do not run it from inside a tree that also carries the companion branches' files — the
   subject is this clone only.
7. **C7 vendor schema provenance** — compare `packaging/public-plugin/vendor-plugin.schema.json` with
   the live official document at `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`
   (claim: 1805 bytes, sha256 `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`,
   byte-identical). If your sandbox has no network, you must NOT speculate: read
   `verify/r3/C1_VENDOR_SCHEMA_PROVENANCE.json`, state that you could not re-derive the fetch, and
   classify the fetch half `INCONCLUSIVE` while still verifying the in-tree bytes yourself.
8. **C8 the evidence pack's hash forms are honest** — for each `commands[]` entry in
   `evidence/EVIDENCE_RETURN_PACK.json`, recompute from the repository both
   `log_sha256_committed_blob` (`git cat-file -p <commit>:<round>/<path>`) and the on-disk form, and
   show that the two differ as declared rather than one being a copy of the other. A recorded
   committed-blob hash equal to the empty-string digest is FAILED.
9. **C9 CI state** — read `.github/workflows/ci.yml` and state whether a "CI is green" claim is
   verifiable from inside an offline clone. If it is not verifiable here, classify it `INCONCLUSIVE`
   naming exactly what would be needed; do not accept the claim and do not call it false.
10. **C10 no unresolved gitlinks at the subject** — `git ls-tree -r HEAD | awk '$1=="160000"'` must be
    empty at the subject, while `main` still carries the four pre-existing ones. Report both counts.
11. **C11 the register's states are supported** — read `00_plan/TT_S4POST_REGISTER.tsv` and, for each row
    whose state asserts a fact you can check locally (e.g. `GREEN_HOSTED_RUNS_VERIFIED`), say whether the
    tree supports it; mark any state you cannot check from here as `UNSUPPORTED_FROM_CLONE` rather than
    agreeing with it.
12. **C12 the FAR study's measured claims are locatable** — in
    `verify/far/FAR_OPEN_ITEMS_ADJUDICATION_20261013.md`, every claim presented as *measured* must point
    at an artifact in this subject. List any "measured" claim with no locatable artifact at this commit.
13. **C13 the round's headline disclosures are accurate** — the round states (a) an earlier CI defect
    made the workflow never actually run, and (b) `public-plugin-verify` is still failing for a base-scope
    reason and is disclosed rather than hidden. From the tree alone, say which of these you can confirm,
    which you cannot, and whether any FAVOURABLE claim is overstated.
14. **C14 nothing favourable is silently rounded up** — name every place where a claim in
    `R3_PUBLICATION.md`, `evidence/EVIDENCE_RETURN_PACK.json` or the FAR study reads stronger than the
    artifacts support. If there are none, say so explicitly.

## Output contract

Write your report to `.ao-r3/EXTERNAL_CHALLENGE_REPORT.md` with these 13 headings in order:
1 Scope and subject binding · 2 Method and raw evidence · 3 What is verified · 4 What failed ·
5 UNCERTAINTY items · 6 DISAGREEMENT items · 7 Claim-by-claim table (C1..C14) · 8 Reproduction
transcript (commands + literal output) · 9 Non-mutation finding · 10 Scope limits (what this verdict
does NOT cover) · 11 Residual risk · 12 Required owner decisions · 13 Verdict.

Also write `.ao-r3/AO_VERDICT.json`:

```json
{"verdict":"<one of PASS_CHALLENGE|FAIL_CHALLENGE|PARTIAL_CHALLENGE|TEMP_CLOSED_CHALLENGE>",
 "subject_commit":"389d3973da73e5740f0b4d290bacb92d1e8982f8","subject_tree":"<read it yourself>",
 "claims":[{"id":"C1","verdict":"VERIFIED|FAILED|INCONCLUSIVE","evidence":"<literal output excerpt>"}],
 "not_verified":["..."],"notes":"..."}
```

`PASS_CHALLENGE` requires every blocking claim (C1, C2, C4, C5, C6, C8, C10) to be VERIFIED; if any is
FAILED the verdict must be `FAIL_CHALLENGE`, and if you could not test enough of them,
`PARTIAL_CHALLENGE`. Print the JSON to stdout as your final output. Your verdict is advisory evidence
to the owner: it grants no release, no pass, and no promotion of any kind.
