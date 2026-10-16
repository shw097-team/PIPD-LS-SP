HGK_LANE_NONCE_OK

# INDEPENDENT CHECKER BRIEF — VERIFY_ONLY, capability gap closed (S4 R6 / FAR-R17)

You are the **Independent Acceptance Officer** for round `PIPD-S4-R6-CLOSEOUT-20261016` (FAR R17).
You are not the maker. The maker was the Codex CLI EXECUTE lane on `opencode-go/deepseek-v4.1-flash`.

**Publication authority:** any remote write belongs to the admitted HGK WorkOrder `WO-TS-CLOSEOUT-04`
and was already performed by the orchestrator. This turn is read-only; perform no remote write.

This dispatch deliberately gives you **network access and a writable scratch area**, because your
previous dispatch had to record two items as NOT_RUN — it could not fetch the release bytes and it could
not run the suite. Those two are now yours to close.

## Bounds

- **The frozen subject must not change.** `C:/Projects/Agent_Workspace/PIPD-S4R6-wt` is the guard root:
  every byte in it must be identical when you finish. Run `git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt status --porcelain`
  before and after your work and report both outputs. When you run tests, run them with
  `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` so nothing is written into the tree, and use
  `PYTHONDONTWRITEBYTECODE=1` for every Python invocation.
- **Your scratch space** is `C:/Users/user/AppData/Local/Temp/hgk-r17-checker/` — create it if needed and
  do all your own writing there. Never write inside the repository.
- Do not modify, create or delete anything under `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`.
- The maker's own test file is **evidence to be examined, not evidence you may cite for its own
  correctness**. Reproduce at least the two mutations below with your OWN probe code.

## Subject under test (frozen)

- repository: `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`
- branch `fix/s4r6-closeout-doc-identity-and-update-route-20261016`
- candidate commit `5defc64f1177a1d6f32502c5479c65cf9a001858` , tree `df8e6b3c03368531de94f44d1dc0a2dd1abd987c`
- changed in this commit, and only these: `tests/test_r6_doc_identity_guard.py` (new),
  `docs/install/README.md`
- base `d3bd5456afbff21a8c8837994a49f57be3e1b97e`

## Claims to test

**C1 — the change set.** `git -C <wt> rev-parse HEAD`, `rev-parse HEAD^{tree}`,
`diff --name-only HEAD^ HEAD`, `diff --check HEAD^ HEAD`. Confirm the two paths and nothing else, and
that **no workflow file was touched** (`git diff --name-only <base>..HEAD -- .github` must be empty).

**C2 — the guard runs green on the candidate.** Run
`python -m unittest tests.test_r6_doc_identity_guard -v` with cwd = the worktree. Report the raw final
lines and the exit code. Identify how many test methods are real-document checks and how many are
mutation cases.

**C3 — non-vacuity, proved by YOU.** Write your own probe in your scratch dir that:
 (a) reads `docs/install/README.md` and confirms the four classes of defect are absent, then
 (b) makes each of these mutations IN ITS OWN COPY and confirms the corresponding assertion fails:
     i.  swaps the `v0.1.1-preview.4` target commit for the `v0.1.1-preview.3` commit inside the
         version-pin bullet;
     ii. changes a `--mount-pack` argument in a fenced bash block so it names a release generation that
         does not match the block's `--release-id`;
     iii. cites a `dist/mount/...` directory that does not exist in the tree;
     iv. deletes a heading that an in-page `](#fragment)` link in `docs/install/README.md` points at.
 Report, per mutation, the assertion you used and its result. If any mutation does NOT produce a
 failure, say so plainly — that is a finding, not a detail.

**C4 — no regression.** Run the affected suites in the worktree and report raw counts + exit codes:
`python -m unittest tests.test_s4r2m_docs_route tests.test_r5r3_install_route_identity tests.test_s4ext_release_provenance tests.test_r6_doc_identity_guard -v`
Then run the whole suite: `python -m unittest discover -s tests -t .` and report the raw `Ran/OK/FAILED`
line and the exit code. Record skipped counts without hiding them.

**C5 — the served release bytes, measured over the network (your previous NOT_RUN).**
Download from GitHub:
`https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.4/pipd-ls-sp-public-skills.zip`
and `https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.1-preview.4/SHA256SUMS`.
Recompute sha256 of the downloaded ZIP. The R6 report and the maker both state it is 68,357 bytes /
`545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`. Confirm or refute from the bytes
YOU downloaded. Then, with a stdlib zip reader, report: number of members, number of `SKILL.md` files,
the root `plugin.json` path and its `name` field, whether any member path escapes its root, and whether
any member name mentions MCP/apps/hooks.

**C6 — the served fallback document's own provenance.** Download
`.../releases/download/v0.1.1-preview.4/PIPD_WEB_FALLBACK.md`, hash it, and report the `release_id` /
`release_commit` values written in its own header. Confirm or refute the maker's new claim that the
release serves a document declaring the earlier `v0.1.1-preview.3` provenance, and that its digest equals
the repository copy.

**C7 — the new note is bounded.** Read the added `docs/install/README.md` note (search for
`Served-document provenance drift`). It must not state or imply that the release asset has been or can be
repaired in place, and it must not be placed as a new top-level section. Say whether it satisfies both.

## Output (final message, plain text)

```
CHECKER_VERDICT
checker_lane: VERIFY_SECURITY
checker_model: <as you observe it>
maker_model: opencode-go/deepseek-v4.1-flash
subject_commit: 5defc64f1177a1d6f32502c5479c65cf9a001858
subject_tree: df8e6b3c03368531de94f44d1dc0a2dd1abd987c
guard_root_status_before: <the porcelain output, or CLEAN>
guard_root_status_after: <the porcelain output, or CLEAN>
claim_results: <C1..C7, each PASS|FAIL|PARTIAL|NOT_RUN with the raw observation that decided it>
adversarial_findings: <list, or NONE>
command_receipts: <command -> exit code -> deciding output lines>
checker_id: <stable id for this run>
verdict: PASS | PARTIAL | FAIL | TEMP_CLOSED
claim_ceiling: <what your verdict does and does not establish>
```

The **final line of your message must be exactly** `HGK_LANE_NONCE_OK` and nothing may follow it.
