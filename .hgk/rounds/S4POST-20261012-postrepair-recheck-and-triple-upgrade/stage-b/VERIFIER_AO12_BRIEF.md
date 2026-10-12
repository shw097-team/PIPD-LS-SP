Use fabric-external-independent-challenge-reviewer.

Review the round-11 repairs as an external clean-room challenger. Do not trust Hermes/HGK/maker PASS
statements. Do not modify the candidate. Re-derive every verdict from frozen authority and raw evidence.

Your skill is installed at `~/.agents/skills/fabric-external-independent-challenge-reviewer`, verified
20/20 package checksums. Follow its own workflow and output contract; this brief supplies only the round
bindings and two working notes that cost the previous officer its run.

## Working note 1 - path adapters, not path warnings (hand this no thought, just use it)

The mismatch runs BOTH ways. A native binary (git, python) cannot resolve an MSYS spelling, and an MSYS
tool cannot create a directory from a native `C:/` argument - the previous officer burned twenty attempts
on `mkdir: cannot create directory 'C:/Users/user': Permission denied` before building the shim below.
Put this on PATH and move on:

```bash
shim=$TMP/shim; mkdir -p "$shim"
for b in mkdir cp; do printf '#!/usr/bin/env bash\na=(); for x in "$@"; do case "$x" in [A-Za-z]:/*) x="$(cygpath -u "$x")";; esac; a+=("$x"); done\nexec /usr/bin/%s "${a[@]}"\n' "$b" > "$shim/$b"; chmod +x "$shim/$b"; done
```

## Working note 2 - write the report incrementally, and quote by locator

The previous officer was killed at the reporting stage by a provider safety notice after writing 157
evidence files, so the round carries NO verdict. Write `verify/ao12/EXTERNAL_CHALLENGE_REPORT.md` EARLY:
create it with the thirteen headings and one line under each before you finish investigating, then update
each section as you go, and record the verdict as soon as you know it. Refer to hostile input by file and
line or by shape rather than pasting the text again. If a provider request is refused with a safety
notice, drop that content, continue, and record it - never resend it.

## Round bindings

- Round: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`, repository `PIPD-LS-SP`.
- Intake: `verify/ao12/EXTERNAL_CHALLENGE_INTAKE.json` (prefilled; its candidate digests are deliberately
  empty - binding them from your own freeze is your Phase A step).
- Gates: `S4-STAGE-B-HANDOVER-CLOSURE`, `S4-MODEL-ROUTING-CONFORMANCE`, `FCR-001..FCR-006`, plus the
  round-11 set below.
- Write set: `verify/ao12/` relative to the round directory ONLY. Clones, fixtures and logs go outside the
  tree in a system temp directory. The maker will not edit the round while you run.
- Read the artifact, not this brief. At dispatch the three suites read 39/0, 52/0 and 27/0; read
  `verify/harness/LAUNCHER_TEST_RESULTS.txt`, `GATE_NEGATIVE_TEST_RESULTS.txt` and
  `CHECKER_FAILOVER_TEST_RESULTS.txt` and report what they say. A disagreement between this brief and an
  artifact is itself a finding.

## What the maker claims

Round 10's officer returned `FAIL_CHALLENGE` (six blocking findings, all repaired) and round 11's officer
was killed by a provider filter before delivering a report, after demonstrating three more holes, which
the maker has now repaired:

1. A hard failure spelled `HTTP 400` beside an incidental quota word switched checker models and reported
   success. Claim: hard-failure markers now cover the HTTP spelling and `malformed payload`.
2. A resolver that cannot decide was treated as outside, letting the gate qualify while writing through a
   junction into the clone. Claim: containment is fail-closed in the gate and the child.
3. Omitting `LANE_ROLE` skipped the child's assignment re-derivation entirely, admitting an unassigned
   model, provider and effort. Claim: the role is now required; a roled lane takes model, provider, effort
   AND route from the assignment; an explicitly different route is refused unless the owner names it.
4. The checker classifier itself matched only quotations (the lane reading the very sources it reviews).
   Claim: it now reads the provider's error channel; and every outcome leaves a committed record, not only
   a failover.
- New cases: `G14a-e` (with a positive control), `G15`, `G16`, `G17`, `A4`, `A5`, `A6`.
- Round 11's partial evidence is at `verify/ao11/` (157 files) with its failure record; AO11 found that the
  current Stage-B manifest binding is still stale - treat that as open, not fixed.

## Attack these hardest

- The junction/containment path, three times repaired and twice falsely passed. Build the junction
  yourself, confirm the log really lands in the worktree, and confirm the refusal names containment rather
  than an unresolvable path or a missing role.
- The classifier: find a lane that a whole-log matcher would misclassify, and one that the new
  error-channel matcher would.
- The four authorisation axes: try to authorise one role with another role's line, and to reach a governed
  worker with an axis the owner never ruled on.
- Any check whose PASS could come from a different refusal than the one asserted.

## Known open items the maker does NOT claim fixed

`FCR-007` current Stage-B binding; filenames containing a newline; a transcript-based qualification
producible by a stub; `CR-IDENTITY-BIND`; `CR-EXT-UNREVIEWED`; no model identity can be authenticated.

## Required output

One report, thirteen headings, verdict from `PASS_CHALLENGE`/`PARTIAL_CHALLENGE`/`FAIL_CHALLENGE`/
`TEMP_CLOSED_CHALLENGE`, at `verify/ao12/EXTERNAL_CHALLENGE_REPORT.md` with the completed intake beside it.
Validate your own bundle with the skill's bundled validator and report its raw output and exit code. Every
finding: severity per the skill's contract plus a locator a third party can re-run.

## Hard rules

Read-only on the candidate (no commit, stage, push, tag, merge, or edit of `stage-b/`, delivered tracked
files or earlier rounds' evidence). You may stub the worker binary; say so wherever you do, and do not
launch a real model or run the product test suite. Quote raw output and exit codes verbatim. Never print
credential-material strings - refer to any such rule as "the credential-material rule (redacted)". State
your ceiling: a stub proves control flow and nothing about a model; a clean `git status` is not code
correctness; passing tests are not release acceptance; you cannot authenticate any model identity. Write
the report even if unfinished, marking what is incomplete.
