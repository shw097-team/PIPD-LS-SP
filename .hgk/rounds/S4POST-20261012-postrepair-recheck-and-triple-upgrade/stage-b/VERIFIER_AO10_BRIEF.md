Use fabric-external-independent-challenge-reviewer.

Review the Stage-B handover closure claim and the governed lane-harness repairs as an external
clean-room challenger. Do not trust Hermes/HGK/maker PASS statements. Do not modify the candidate.
Re-derive the verdict from frozen authority and raw deterministic evidence.

Your skill is installed at `~/.agents/skills/fabric-external-independent-challenge-reviewer` (verified:
20/20 package checksums match, SELF_TEST PASS). Follow that skill's own workflow and output contract;
this brief only supplies the round bindings.

## Round bindings

- Round: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`, repository `PIPD-LS-SP`.
- Intake bundle: `verify/ao10/EXTERNAL_CHALLENGE_INTAKE.json` (prefilled). Its `candidate.commit`,
  `candidate.package_sha256`, `candidate.distribution_digest` and `evidence_manifest_sha256` are
  deliberately EMPTY: filling them from your own freeze is your Phase A step. Do not treat the empty
  values as evidence, and do not accept any digest this brief or another document states - recompute it.
- Requested gates: `S4-STAGE-B-HANDOVER-CLOSURE` and `S4-MODEL-ROUTING-CONFORMANCE`.
- Write set: **`verify/ao10/` relative to the round directory only.** Everything else - clones, stubs,
  fixtures, logs - lives outside the tree in a system temp directory.

## What the maker claims, none of it on trust

1. Stages of previous reviews: round 3 NOT_CLOSED, round 4 PARTIAL, round 5 STILL_NOT_CLOSED,
   round 6 PARTIAL, round 7 no verdict (provider content filter), **round 8 PARTIAL / B NOT_SUPPORTED**,
   round 9 no verdict (the maker stopped the lane). Read `verify/ao8/AO_VERDICT_HANDOVER_R8.md` first.
2. Round 8's six demonstrated mechanisms are closed: the anchored-prefix counterexample (a staged
   `prefix/<round>/outside.txt` was committed and the wrapper returned 0), the regex-shaped owner-record
   match (`LANE_MODEL='.*'` was accepted as authorised), a committed clean-tree receipt carrying
   `model=wrong`, `qualified=no` and duplicated conflicting `child_exit`/`route` lines, the gate's own
   missing log-directory containment, HEAD being read by the last command to run, and `qualified=yes`
   being recorded for direct calls.
3. The suites report: `run_harness_negative_tests.sh` **38 pass / 0 fail**,
   `run_gate_negative_tests.sh` **32 pass / 0 fail**, `run_checker_failover_tests.sh` **14 pass / 0 fail**.
4. The maker's own record `verify/ao7/AO7_LANE_FAILURE.md` was WRONG when it claimed no receipt was
   written; it now carries the correction. Treat any similar claim in any maker document as suspect and
   verify it against the artefact.
5. Known limits the maker does NOT claim to have fixed: filenames containing a newline are not covered by
   the staged-outside check; a transcript-based qualification can still be produced by a stub; a caller who
   omits `LANE_ROLE` entirely is not stopped by the child's re-derivation check.

## Required output

- One report following the skill's template, containing exactly the thirteen required headings, with a
  verdict drawn from `PASS_CHALLENGE` / `PARTIAL_CHALLENGE` / `FAIL_CHALLENGE` / `TEMP_CLOSED_CHALLENGE`.
- Write it as `verify/ao10/EXTERNAL_CHALLENGE_REPORT.md`, and the completed intake as
  `verify/ao10/EXTERNAL_CHALLENGE_INTAKE.json` (rewrite the copy in place with your own bindings).
- Validate your own bundle with the bundled validator, e.g.
  `python ~/.agents/skills/fabric-external-independent-challenge-reviewer/scripts/verify_review_bundle.py --help`
  (discover its real arguments; do not guess), and report its raw output and exit code in your report.
- Every finding needs severity per the skill's contract and a locator a third party can re-run.
- Write each case's result to `verify/ao10/` as you finish it, not only at the end, so an interrupted run
  still leaves evidence.

## Hard rules

- Read-only on the candidate: no commit, stage, push, tag, merge, or edit of `stage-b/`, delivered tracked
  files, or any earlier round's evidence.
- You may replace a worker binary with a stub (`CODEX_BIN`, `GATE_BIN`) so that no model is launched; say so
  wherever you do. Do not launch a real model. Do not run the project's product test suite.
- Report everything you did NOT execute, every contrary example you could NOT reproduce, and anywhere a
  document and the code or logs disagree - that disagreement is itself a finding.
- Quote raw output and exit codes verbatim. A claim you cannot back with a command and its output is not
  supported.
- Never print credential-material strings (tokens, credential files, or ignore rules naming them); refer to
  any such rule as "the credential-material rule (redacted)". If a provider request is refused with a
  safety notice, drop that content, continue, and record it.
- Host conditions you may work around and must disclose: the lane runs as a different Windows identity than
  the repository owner, so a plain clone fails with `dubious ownership` on the linked worktree's gitdir (a
  command-scoped exception works); native Windows binaries do not translate MSYS-style paths, so anything a
  native binary must resolve needs a native `C:/...` path. Do not change the delivery's git configuration.
- State your ceiling: a stub proves control flow and nothing about a model; a clean `git status` is not code
  correctness; passing tests are not release acceptance; you cannot authenticate any model identity.
- Finish by writing the report even if your work is incomplete, marking clearly what is unfinished.
