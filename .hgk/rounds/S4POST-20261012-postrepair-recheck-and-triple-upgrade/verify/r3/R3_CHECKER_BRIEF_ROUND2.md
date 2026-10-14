# Independent acceptance brief — S4POST R3 **round 2** (owner-mandated VERIFY/SECURITY lane)

You are the **Independent Acceptance Officer** on the owner-declared lane (CODEX CLI, checker model
`gpt-6.1-sol`, OpenAI OAuth, reasoning effort medium). You did **not** write this candidate and you may
**not** repair it. Work **read-only**: write only under `.ao-r3b/` in this clone. No network, no git
history changes, no commit, no push, no tag, no publish, no edits to any tracked file.

## Subject

- **This round's subject**: commit **`5351c5fadca5`** on `feat/s4post-triple-upgrade-20261013-r3`
  (read the full 40-hex sha yourself from HEAD).
- **The previous round's subject** was `3233c817` on the same branch; that round returned
  `FAIL_CHALLENGE` and named exactly the defects the maker now claims to have fixed.
- Round directory: `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/`
- `main` must still be `224591431a164ab72a9423cd180e417e8a762403`.

**A changelog is not evidence.** The maker claims a list of fixes; your job is to test each claim against
the bytes, not to confirm the story. Where you cannot re-derive something, emit a typed `UNCERTAINTY`.
Where your measurement disagrees, emit `DISAGREEMENT` with both numbers.

Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`; set `PYTHONPATH` to this clone.

## Part 1 — did the previous round's defects actually get fixed?

1. **The acceptance block is executable as written** — take `R3_PUBLICATION.md` §3 **verbatim** and run its
   locator commands from the clone root. Claim: the negative control exits non-zero, the positive control
   exits 0, and **no step fails with a path error**. Report every step's real exit code. (Last round one
   step died on a duplicated round prefix.)
2. **The locator tool handles URLs** — read `verify/tools/check_evidence_locators.py` and show that a URL
   inside prose is no longer fragmented into a relative candidate. Test it: a document containing both a
   URL and a resolvable in-tree path must come out `PASS_LOCATORS_IN_TREE`.
3. **The restated non-mutation claim is the accurate one** — capture `git status --porcelain` and its
   `--ignored` form before and after running both suites, and name the entries. The claim under test is now
   narrower: *no new tracked or untracked-non-ignored entries exist, and on a fresh clone the suites create
   the three gitignored `__pycache__/` directories.* Judge that wording as stated, not the old blanket one.
4. **The hash-form labels are honest** — for each `commands[]` entry of `evidence/EVIDENCE_RETURN_PACK.json`,
   recompute the committed-blob digest (`git cat-file -p <commit>:<path>`) and compare it with what a fresh
   clone's disk holds, then reproduce the recorded CRLF form by conversion. Say whether the two labels mean
   what they say. An empty-string digest is FAILED.
5. **The `com.ao3` count is now right** — the maker's record claims THREE files, all of them round-authored,
   and ZERO product-side hits. Scan the tree yourself and check both halves.
6. **The base explanation is now two-part and correct** — the record now claims that `public-plugin-verify`
   exits 1 on **both** the `main` and the declared stacked base, because its deny logic also rejects the
   newly approved `.github/workflows/ci.yml` and four removed gitlink paths, and that only the
   *frozen-path* half is base-sensitive. Verify what you can from the tree and judge the explanation.
7. **Every "measured" claim in the FAR study is locatable** — open
   `verify/far/FAR_OPEN_ITEMS_ADJUDICATION_20261013.md` and `verify/r3/FAR_MEASUREMENT_RECEIPTS.json` and
   spot-check at least four claims against the artifacts they cite. Name what you checked.

## Part 2 — the four owner supplies (new since the previous round)

8. **A1 derivations** — `packaging/public-plugin/derivations.json` must carry one record per skill with
   `source_sha256` equal to the digest **you compute** for that `skills/<name>/SKILL.md`, and the frozen
   ledger (`verify/r3/FROZEN_SOURCE_LEDGER.json`) must agree. Recompute; do not read the recorded values.
9. **A2 vendor digest** — the pinned `official_schema_sha256` must equal the sha256 of
   `packaging/public-plugin/vendor-plugin.schema.json`, in **both** manifests.
10. **A4 icons** — the pinned icon digest must equal the sha256 of the file the generator produces. If you can
    run `tools/build_public_plugin.py --generate-icons` into a temp directory, do so and compare; if the
    sandbox forbids it, verify the pin is not a placeholder and mark the generation half `INCONCLUSIVE`
    rather than guessing.
11. **The build** — **this is the decisive claim.** Run
    `python tools/build_public_plugin.py --source-root . --ledger <the round ledger> --source-commit <the ledger's commit> --out-dir <a temp dir OUTSIDE the repo>`
    and report the literal result. A `REFUSED OWNER_INPUT_REQUIRED` means the supplies are NOT delivered;
    `BUILT … sha256=…` means the typed refusal is genuinely lifted. Record the sha256 you obtain.
12. **A3 publisher** — the publisher record is derived from the repository owner, not a verified human. Judge
    whether `verify/r3/OWNER_SUPPLIES_DELIVERED.json` discloses that honestly, and say what it leaves
    owner-only.
13. **The suites** — run both test suites and report exit codes and the literal `Ran N …` lines.
14. **No favourable claim is rounded up** — name anything in the tree that reads stronger than its artifacts.

## Output contract

Write `.ao-r3b/EXTERNAL_CHALLENGE_REPORT.md` with these 13 headings in order: 1 Scope and subject binding ·
2 Method and raw evidence · 3 What is verified · 4 What failed · 5 UNCERTAINTY items · 6 DISAGREEMENT
items · 7 Claim-by-claim table (1..14) · 8 Reproduction transcript (commands + literal output) ·
9 Non-mutation finding · 10 Scope limits (what this verdict does NOT cover) · 11 Residual risk ·
12 Required owner decisions · 13 Verdict.

Also write `.ao-r3b/AO_VERDICT.json`:

```json
{"verdict":"<PASS_CHALLENGE|FAIL_CHALLENGE|PARTIAL_CHALLENGE|TEMP_CLOSED_CHALLENGE>",
 "subject_commit":"<read HEAD yourself>","subject_tree":"<read it yourself>",
 "claims":[{"id":"1","verdict":"VERIFIED|FAILED|INCONCLUSIVE","evidence":"<literal output>"}],
 "not_verified":["..."],"notes":"..."}
```

`PASS_CHALLENGE` requires claims **1, 2, 4, 5, 8, 10, 11 and 13** all VERIFIED. Anything FAILED there forces
`FAIL_CHALLENGE`; insufficient coverage forces `PARTIAL_CHALLENGE`. Print the JSON as your final output.
Your verdict is advisory evidence to the owner: it grants no release, no pass and no promotion.
