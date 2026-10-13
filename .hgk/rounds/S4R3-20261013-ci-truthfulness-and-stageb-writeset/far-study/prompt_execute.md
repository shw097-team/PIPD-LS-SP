TASK: produce the FAR decision study specified at the end of this packet. Write the full study to the file C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt/.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/EXECUTE_STUDY_DRAFT.md and ALSO return it as your final message. End your message with the token below on its own line.

TOKEN (required, verbatim, final line): HGK_LANE_NONCE_OK

=== PACKET BEGINS ===

# FAR decision study — bounded-writer packet (EXECUTE lane)

You are the bounded writer for a governed research round. Produce the study described at the end.
Everything below is either a measured fact with its locator, or is explicitly marked as an owner
input. Do not add facts from your own knowledge, do not soften a measured fact, and do not invent an
artifact path. Where a fact is not supplied, write NOT_SUPPLIED rather than filling it.

## 1. Subject

Project `PIPD-LS-SP-20261008`, round `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset`
on repo `shw097-team/PIPD-LS-SP`. Two candidate branches, both still draft:
`fix/s4r3-stage-a-ci-truthfulness-20261013` (Stage A head `5310896e706e01a9cdb0123285bccec75086bcb8`)
and `feat/s4r3-stageb-successor-20261013` (Stage B head `ba27309b50d8623ed9d3ad9b33fe7a4ffb8a9ede`,
superseded by `b32192f566026401d239985029906a80e37a734d` at the time of writing).
Frozen refs, untouched: `main = 224591431a164ab72a9423cd180e417e8a762403`,
tag `v0.1.1-preview.3 = e94cc7f9567acb59de4691ee6166815ac96a9700`.
Stage B is stacked on Stage A: `git merge-base <stage A head> <stage B head>` equals the Stage A head
(measured).

## 2. Measured findings (with locators)

F1. **The write-set allowlist WAS widened, against an admitted obligation that forbids it.**
The admitted requirement `REQ-S4R3X-GATE-FALSIFIABILITY-002` in the canonical spine carries the
wording "The allowlists must not be widened and the frozen-path refusal must still refuse". A
mechanical set-diff of the ALLOWED/DENIED assignments in `.github/workflows/public-plugin-verify.yml`
between the frozen R3 subject `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` and the current heads gives:
stage-b ALLOWED **+2 entries**: `docs/USER_GUIDE.md` and `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`;
stage-b DENIED unchanged (skills/, src/, schemas/, dist/); stage-a is a new stage whose DENIED set
omits `src/` (files there still refused, but by the allowlist rather than a category denial).
The workflow's own inline comment asserts "This change widens NEITHER allowlist" - also false as
written. Locators: `evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt`,
`evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md`. NOT claimed: that either addition was made
to buy a green run; no frozen path became writable for stage-b.

F2. **An independent checker lane was served eight times** (attempts 7-14) on the VERIFY_SECURITY
lane, forced arm `opencode-go/glm-5.3-flash`, read-only sandbox, no escalation. Every verdict is
advisory and NONE is a pass. Best per claim: C2 CONFIRMED (attempt 10), C4 CONFIRMED (attempt 14),
C1 PARTIALLY_CONFIRMED (attempts 11, 12), C3 PARTIALLY_CONFIRMED (attempt 13). No claim is
unexamined. Locators: `evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A7.md`, `_A8.md`, `_A9_A10.md`,
`_A11.md`, `_A12_A13_A14.md`.

F3. **Three verdicts in that series were polluted by this round's own artifacts**: attempt 7's
`C4: REFUTED` came from a bundle mixing receipts from successive heads without labels; attempt 8's
receipt claimed a `doctor` log it had actually dropped; attempt 10's supplied `doctor` log was a bash
error trace for a missing `pipd.exe`. Each is corrected in the named evidence files.

F4. **The C1 shortfall is a co-location gap, not missing work.** The artifact the checker asked for -
a wheel-extracted registry inventory compared file-by-file against the tree, with a negative control -
already exists and was accepted in attempt 11 (`evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md`:
INSTALLED mode, 19 family names equal to the expected set and order, 20 per-file digests identical to
the tree, and a negative where dropping one family turns the verdict FAIL). Attempt 12 did not carry
it, so C1 came back PARTIALLY_CONFIRMED again.

F5. **A receipt pack binds commands to exit codes**, 18 steps, all exit codes as expected, five
negative cases each refused with the intended typed code, wheel route and sdist-to-wheel route both
returning 0: `evidence/12_GATES/RECEIPT_PACK_C1_C2.json`.

F6. **Canonical admission state**: 6 requirements FROZEN / 6 taskspecs ADMITTED / 6 workorders CREATED
for `S4R3X`, plus this study's own 2 requirement / 2 taskspec / 2 workorder rows; every acceptance row
for them is `NOT_RUN`; `evidence_refs` 0; `tt_records` 0. The workorder result entrypoint accepts only
PASS/FAIL, so a PARTIAL verdict cannot be recorded truthfully.

F7. **Spine size and attribution**: `workorders` currently 405. Measured earlier in this session as
393. Attributed: +6 = this session's `S4R3X` rows (created 2026-10-13T09:28Z); +2 = this FAR study's
rows (10:58Z); +4 = four rows created 2026-10-13T09:47-10:06Z by a `STACK-HYGIENE-20261013` round
(ALIGN / DOC / ORPHAN / CLOSE) that this round did not create and cannot attribute to its own record.

F8. **Flags**: `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` all still hold. No merge,
tag, release or archive was performed in this round.

## 3. Pending decisions (all owner-gated; none closable by this round)

D1. Adjudicate F1: correct the statement and keep the sets / narrow the round-directory entry (this
edits the audited Stage A head and needs a fresh verification round) / register the two additions as a
declared, reviewed deviation.
D2. Whether to lift the round's self-imposed pause on further verification-lane dispatches, and
whether to land two mechanical guards first: a pre-dispatch check that `blocks_kept` covers the claim
under test, and a rule that any claim put to a checker must have a receipt in the round.
D3. Land the C1 co-location bundle (F4 artifact + the doctor receipt in one bundle).
D4. Re-cut C3 with the corrected baseline diff and honest wording.
D5. Owner inputs still outstanding: F003 publisher identity / brand assets / vendor validator /
portal submission; four-host UAT (Hermes native skill, Codex desktop, Codex CLI native skill, Claude
Code) NOT_EXECUTED; `.hgk` archive policy (~62 MB); PR #4 (superseded) close-or-keep; final
merge/release release decision.

## 4. Constraint set for your recommendation

Low friction. High engineering necessity. Not over-engineered (a remedy that builds new machinery to
verify machinery must justify itself against the alternative of not building it). Aligned to the task
core: the R3 PROMPT, the external acceptance report, the upstream three-part upgrade blueprint.
Directly usable by an external acceptance officer: they must be able to open an artifact and re-run
something, not read prose about intent.

## 5. Deliverable (return it as your final message; the parent session persists it)

Write, in English:

A. **Status in one paragraph**, distinguishing what is verified, what is advisory-only, and what is
   owner-gated.
B. **A decision table**, one row per D1-D5: item, owner, what unblocks it, cost, risk, the clause or
   promise it restores, and the artifact that would verify the closure.
C. **A ranked remedy plan** for the engineering items only (D2, D3, D4 and any F1 option that needs
   engineering), cheapest-first, each with: action, cost estimate in the round's own units (a lane run,
   a commit, an edit), risk, and the receipt that would show it done.
D. **What may be handed to an external acceptance officer now**, as an explicit list of artifact paths
   plus, for each, the one command or check they can run to falsify it. Then the same list for what may
   NOT be handed over yet, with the reason.
E. **The marginal-value read**: across the rounds under study, how many of the governing documents'
   required-external-evidence items moved (a count with the source of the count), and the single
   sentence that decides the next action.
F. **A DO-NOT list**, lifted from constraints actually stated above (no oracle/threshold/validator/
   denominator relaxation, no merge/tag/release, no widening further).

Keep it under 900 lines. Do not restate the packet; cite it.
