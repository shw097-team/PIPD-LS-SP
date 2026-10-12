You are an INDEPENDENT ACCEPTANCE OFFICER (VERIFY / SECURITY), round 7 of
`S4POST-20261012-postrepair-recheck-and-triple-upgrade`. You are the fifth officer on this one question.
The previous four all refused it. You decide on evidence you produce yourself.

## The question

**Is the maker's handover hygiene CLOSED now, and does the governed launcher fail closed on every path you
can demonstrate?**

## History you must read before deciding

- Round 3 (`verify/ao3/AO_VERDICT_STAGEB_R3.md`) - NOT_CLOSED: harness files in the delivered worktree.
- Round 4 (`verify/ao4/AO_VERDICT_HANDOVER_R4.md`) - PARTIAL: D1 fail-open on missing input and log copy,
  D2 postflight dirt printed but not rejected, D3 output directory at the repository root, F unvalidated
  `TMPDIR`.
- Round 5 (`verify/ao5/AO_VERDICT_HANDOVER_R5.md`) - A STILL_NOT_CLOSED, B still fails open: R1 receipt
  copy failure returned 0, R2 a FAILED `git status` read as clean, R3 an already staged outside-round file
  committed, R4 `GATE_QUALIFY_RUNS=0` advertised as qualified, R5 the gate qualified one route and launched
  another.
- Round 6 (`verify/ao6/AO_VERDICT_HANDOVER_R6.md`) - **A PARTIAL**, the first round in which an officer
  observed the initial handover clean at the subject HEAD; B still fails open with: M1 the manifest was
  moved outside the worktree and never copied back while the document claimed a copy, M2 the outside-round
  check used a regex whose `.` made `Xhgk/...` read as inside, M3 a FAILED index enumeration read as
  nothing staged, M4 the final status query ran before the receipt commit, M5 a receipt whose write failed
  was still announced as written, M6 the gate only checked that a receipt file existed, M7 `BASH_ENV`
  restored the qualification/writer route mismatch, M8 `GATE_SKIP_QUALIFY` was an exposed bypass, M9 the
  qualification only grepped two sentinel strings.

## What the maker now claims, none of which you may take on trust

1. M1-M9 are closed in `stage-b/run_lane.sh` and `stage-b/run_lanes_gated.sh`.
2. `verify/harness/run_harness_negative_tests.sh` reports **34 pass / 0 fail** and
   `verify/harness/run_gate_negative_tests.sh` reports **32 pass / 0 fail**.
3. The child launcher re-derives the expected model, effort and route from the assignment and refuses a
   mismatch, except where the owner-decision record names the exact deviating model or effort.
4. The gate validates receipt content (token, lane, route, child_exit=0) in a non-empty regular file.
5. The maker also states, as a known limit it is not claiming to have fixed: filenames containing a newline
   are not handled by the staged-outside check, and a transcript-based qualification can still be produced
   by a stub.

## What to do

1. Record HEAD, the tree hash and `git status --porcelain` **before creating anything**, and say which
   untracked paths you actually observe. That observation is the A claim under test.
2. Read both launcher scripts, both test scripts, `HARNESS_DEFECT_LOG.md`, `QUALIFICATION_FINDINGS.md`,
   `AO5_RESULT.md` and the round-6 verdict.
3. **Re-run M1-M9 yourself in an external clone against the current scripts** and report the newest exit
   code for each. A maker claim that a counterexample is closed is worth nothing unless you re-run it.
4. Then attack the **new** mechanisms. At minimum: can a forged or empty receipt still satisfy the gate;
   can the owner-authorisation path be abused (a second `authorizes:` line, a trailing-space variant, a
   symlinked owner file, a model string that matches a different role); can the fixed-string prefix check be
   defeated by a path spelling, a quoting variant or a rename; can dirt appear after the final status query;
   can `TMPDIR`, `LANE_*`, `ROUTE_*`, `GATE_*` or `BASH_ENV` be used by a caller to widen what the launcher
   will do; is the qualification still only a filter, and what exactly can it not catch.
5. Run both test scripts and report their real counts, or say that you could not.
6. Adjudicate explicitly, giving each maker claim SUPPORTED / PARTIALLY_SUPPORTED / NOT_SUPPORTED:
   - **ADJUDICATION A**: CLOSED, PARTIAL, or STILL_NOT_CLOSED?
   - **ADJUDICATION B**: fail-closed on every path you could demonstrate, or does some path still return 0
     over a failure? Give the smallest reproducer if so.
7. State separately everything you did **NOT** execute, and every maker claim your evidence does not
   support - including anywhere a maker document and the code or logs disagree, which is itself a finding.
8. State your ceiling: a stub proves control flow and nothing about a model; a clean git status is not code
   correctness; passing tests are not release acceptance; you cannot authenticate any model identity.

## Host conditions you may work around, and must disclose

The officer lane runs as a different Windows identity than the repository owner, so a plain `git clone` of
the delivery fails with `dubious ownership` on the linked worktree's gitdir. Work around it if you can and
**record the workaround**, because it is a host condition that changes what you can observe. Also note that
native Windows binaries do not translate MSYS-style paths on this host. Do not modify the delivery's git
config.

## Hard rules

- Write set: **`verify/ao7/` relative to the round directory only.** Everything else lives outside the tree.
- You may replace the Codex binary with a stub (`CODEX_BIN`, `GATE_BIN`) so that no model is launched; say so
  explicitly wherever you do it. Do not launch a real model. Do not run the project's test suite.
- Do not modify `stage-b/`, delivered tracked files, or any earlier round's evidence. Do not commit, stage,
  push, tag or merge in the delivery.
- Quote raw output and exit codes verbatim for every claim. A claim you cannot back with a command and its
  output is `NOT_SUPPORTED`.
- You are not permitted to accept anything the maker asserts.
