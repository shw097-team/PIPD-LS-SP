Use fabric-external-independent-challenge-reviewer.

Review the round-10 repairs as an external clean-room challenger. Do not trust Hermes/HGK/maker PASS
statements. Do not modify the candidate. Re-derive every verdict from frozen authority and raw evidence.

Your skill is installed at `~/.agents/skills/fabric-external-independent-challenge-reviewer`, verified
20/20 package checksums. Follow that skill's own workflow and output contract; this brief supplies only
the round bindings.

## Round bindings

- Round: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`, repository `PIPD-LS-SP`.
- Intake: `verify/ao11/EXTERNAL_CHALLENGE_INTAKE.json` (prefilled, its candidate digests deliberately
  empty - binding them from your own freeze is your Phase A step).
- Requested gates: `S4-STAGE-B-HANDOVER-CLOSURE`, `S4-MODEL-ROUTING-CONFORMANCE`, and the round-10
  repair set `FCR-001..FCR-006`.
- Write set: `verify/ao11/` relative to the round directory ONLY. Clones, fixtures and logs live outside
  the tree in a system temp directory. The maker will not edit the round while you run.

## Read the artifacts, not this brief

The maker's counts below may already be stale. Read the three result files and report what they say; a
disagreement between this brief and an artifact is itself a finding:
`verify/harness/LAUNCHER_TEST_RESULTS.txt`, `verify/harness/GATE_NEGATIVE_TEST_RESULTS.txt`,
`verify/harness/CHECKER_FAILOVER_TEST_RESULTS.txt`. At dispatch they read 38/0, 48/0 and 22/0.

## What the maker claims, none of it on trust

Round 10's officer returned `FAIL_CHALLENGE` with six blocking findings and the maker repaired all six:

1. **FCR-001** the gate's own owner check was a BRE match on a bare key with no value validation and no
   effort axis, so `LANE_MODEL='.*'` was approved. Claim: per-axis, plain-identifier, fixed-string.
2. **FCR-002** an EXECUTE-scoped exception authorised a VERIFY lane. Claim: authorisation lines are role
   qualified and the gate and the child read the same form.
3. **FCR-003** a caller-supplied provider bypassed the check. Claim: provider is a checked axis.
4. **FCR-004** a Windows junction defeated the lexical containment test: the gate wrote its own log inside
   the worktree and returned 0. Claim: containment is now decided by the OS resolver's realpath in both
   the gate and the child. **Attack this hardest.** Two earlier repairs of this same finding were wrong:
   the first probe asked git and was defeated by an ignored directory; the first fixture never created the
   junction and the case passed on an unresolvable path instead. Rebuild the junction yourself, confirm the
   log really lands in the worktree, and confirm the refusal names containment and not a resolve failure.
5. **FCR-005** a protocol 400 whose text carried an incidental quota word switched checker models and
   reported success. Claim: hard-failure markers veto the failover.
6. **FCR-006** the failover record stayed untracked after a successful failover. Claim: it is committed
   and the tree re-read before the wrapper reports.
- New cases: G14a-e (including a positive control that the authorised value still runs), G15, A4, A5.
- The maker's earlier rounds' repairs (anchored prefix, receipt integrity, late HEAD, direct label) were
  independently confirmed by round 10 and are not in scope except as regression.

## Known open items the maker does NOT claim fixed

`FCR-007` current Stage-B binding/manifest ownership; filenames containing a newline; a transcript-based
qualification producible by a stub; a caller that omits `LANE_ROLE`; `CR-IDENTITY-BIND`;
`CR-EXT-UNREVIEWED`; no model identity can be authenticated. Report any of these you can reproduce.

## Required output

- One report following the skill's template with exactly the thirteen required headings and a verdict from
  `PASS_CHALLENGE` / `PARTIAL_CHALLENGE` / `FAIL_CHALLENGE` / `TEMP_CLOSED_CHALLENGE`, written to
  `verify/ao11/EXTERNAL_CHALLENGE_REPORT.md`, with the completed intake alongside it.
- Validate your own bundle with the skill's bundled validator and report its raw output and exit code.
- Every finding: severity per the skill's contract and a locator a third party can re-run.
- Write each case's result into `verify/ao11/` as you finish it, not only at the end.

## Hard rules

- Read-only on the candidate: no commit, stage, push, tag, merge or edit of `stage-b/`, delivered tracked
  files or earlier rounds' evidence.
- You may stub the worker binary (`CODEX_BIN`, `GATE_BIN`) so no model is launched; say so wherever you do.
  Do not launch a real model. Do not run the project's product test suite.
- Quote raw output and exit codes verbatim. A claim you cannot back with a command and its output is not
  supported. Report everything you did not execute.
- Never print credential-material strings; refer to any such rule as "the credential-material rule
  (redacted)". If a provider request is refused with a safety notice, drop that content, continue, record.
- Host conditions to work around and disclose: the lane runs as a different Windows identity than the
  repository owner, so a plain clone fails with `dubious ownership` on the linked worktree's gitdir.
  Native Windows binaries do not translate MSYS-style paths, so anything a native binary must resolve needs
  a native `C:/...` path. Assertions must be fixed-string: this round lost two assertions to a bracket read
  as a character class.
- State your ceiling: a stub proves control flow and nothing about a model; a clean `git status` is not
  code correctness; passing tests are not release acceptance; you cannot authenticate any model identity.
- Write the report even if your work is incomplete, marking clearly what is unfinished.
