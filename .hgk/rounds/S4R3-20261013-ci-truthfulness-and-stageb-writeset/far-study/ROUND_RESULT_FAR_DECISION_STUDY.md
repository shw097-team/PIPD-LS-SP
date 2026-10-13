# FAR study — S4 R3 status, pending decisions, and external-acceptance readiness

Round `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset`, project `PIPD-LS-SP-20261008`.
Workorders `WO-TS-req-s4r3far-decision-study-001` (EXECUTE) and `...-verify-002` (VERIFY), both admitted
at base head `b32192f566026401d239985029906a80e37a734d`, both `CREATED`, both acceptances `NOT_RUN`.
Status: **maker-side study. Not an acceptance. Changes no flag.**

Provenance: assembled by the bounded EXECUTE-lane writer (`codex` lane, forced arm
`opencode-go/deepseek-v4.1-flash`, `danger-full-access`, 257.74 s, nonce present, usage receipt ok) at
`far-study/EXECUTE_STUDY_DRAFT.md`; adjudicated and corrected here by the orchestrator, which re-derived
the mechanical facts itself. The independent check did **not** produce a substantive verification - see
F9 - and that is recorded rather than papered over.

## A. Status

**Verified by this round's own mechanical work, reproducible from committed receipts:**
F006 wheel-registry repair (hosted winner line `mode=INSTALLED`); the declared-stage/base write-set
logic and its planted-violation refusals; the 18-step receipt pack binding commands to exit codes with
five negatives refused by their intended typed codes; the Stage B repin (merge-base measured, not
asserted); the family-identity receipt (INSTALLED mode, name set and order equal to the expected set,
per-file digests equal to the tree, negative control flips to FAIL).

**Verified defect against an admitted obligation:** the stage-b write-set allowlist gained exactly two
entries relative to the frozen subject - `docs/USER_GUIDE.md` and the round's own directory - while the
admitted requirement `REQ-S4R3X-GATE-FALSIFIABILITY-002` states "The allowlists must not be widened…",
and the workflow's inline comment asserts "This change widens NEITHER allowlist". Both statements are
false as written. The stage-b DENIED set is unchanged, and no frozen path became writable.

**Advisory only, and none of them a pass:** eight checker verdicts (attempts 7-14). Best per claim
C2 CONFIRMED, C4 CONFIRMED, C1 and C3 PARTIALLY_CONFIRMED.

**Owner-gated, nothing of it closable here:** every acceptance row (0 run), all 12 blueprint
`required_external_evidence` items (0 moved by this round), and the release decision. `NO_MERGE`,
`NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` all hold.

## B. Pending decisions

| # | item | owner | what unblocks it | cost | risk | clause restored | artifact that verifies closure |
|---|---|---|---|---|---|---|---|
| D1 | the allowlist deviation (F1) | owner ruling | choose: correct the statement / narrow the entry / register as a declared deviation | 1 edit; option 2 adds a head edit + a fresh verification round | option 2 invalidates the audited heads | honesty of the C3 statement vs `REQ-S4R3X-GATE-FALSIFIABILITY-002` | amended workflow comment + re-cut C3 whose wording matches the diff |
| D2 | resume or hold verification dispatches; land the two guards first | owner | decision on the guards | 2 small edits + 1 negative run | guard may be mistaken for catching the original failure | bundle discipline (the attempt-8 defect) | the guard's own negative test |
| D3 | C1 co-location bundle | this round, on the owner's word | assemble accepted family artifact + doctor receipt + sdist receipt in ONE bundle | 1 edit + 1 lane run | low | C1's co-location gap | the bundle itself as a committed artifact |
| D4 | re-cut C3 | this round, on the owner's word | corrected diff + honest wording | 1 edit + 1 lane run | low | the C3 claim's truthfulness | corrected C3 bundle + the diff |
| D5 | owner inputs and host gates | owner / host | F003 publisher identity, brand assets, vendor validator, portal submission; four-host UAT; `.hgk` archive policy; PR #4 disposition; final release | owner-side | n/a | the external-evidence items | each item's own receipt from the provider |
| **D6** | **re-specify the checker lane's role** | owner | accept the lane as a **bundle auditor** (and write prompts that carry the receipt), or enable a read/exec-capable verifier | 0 engineering if accepted as-is | a checker whose ceiling is unstated will be read as a tree-level verifier | the meaning of every lane verdict - and of the independent-verification promise itself | the capability probe `verify/CAPABILITY_PROBE_A6.md` |

## C. Ranked remedy plan (engineering items only)

1. **Correct the statement, register the deviation (D1 option 1) - no head edit.** Amend the workflow
   comment and the round's C3 wording to enumerate the two additions; record F1 as a declared deviation.
   *Cost* 1 edit + 1 commit. *Risk* none to the candidates. *Receipt* the amended text plus the diff.
2. **Land the two mechanical guards (D2).** (a) pre-dispatch check that `blocks_kept` covers the claim
   under test; (b) any claim put to a checker must have a receipt in the bundle. *Cost* 2 edits + 1
   negative run. *Risk* bounded: a passing guard proves the bundle well-formed, not the lane sound.
   *Receipt* the guard's negative test.
3. **Prepare the external handover pack (new, from F9).** The D.1 list below as one committed document,
   each entry with its falsifying command. *Cost* 1 document. *Risk* none. *Receipt* the pack.
4. **C1 co-location bundle (D3).** *Cost* 1 edit + 1 lane run. *Risk* low. *Receipt* the bundle.
5. **Re-cut C3 (D4).** *Cost* 1 edit + 1 lane run. *Risk* low **only if** the target is restated as
   "the bundle carries the diff and the wording matches it" - see F9; a tree-level CONFIRMED is not
   obtainable from this lane. *Receipt* the re-cut bundle.
6. **Narrow the round-directory allowlist entry (D1 option 2) - last.** *Cost* 1 head edit + a fresh
   verification round. *Risk* highest: it invalidates the audited heads. *Receipt* narrowed entry + a new
   verdict on the re-cut head.

Recommended order: **1 → 2 → 3 → 4 → 5 → 6.** Items 1-3 need no lane run and no head edit; item 3 is the
one that actually moves the external-acceptance needle.

## D. External handoff

### D.1 May be handed to an external acceptance officer now

All paths under `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`. Each has a falsifying
check the officer runs themselves - they, unlike this stack's checker lane, can execute commands.

| artifact | falsifying check |
|---|---|
| `evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt` | re-run the two `git show` commands quoted in it against the frozen subject and the current heads, re-parse the `ALLOWED`/`DENIED` assignments, re-diff |
| `evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md` | `grep -n "widens NEITHER allowlist" .github/workflows/public-plugin-verify.yml` and compare to the claim |
| `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md` | run `scripts/report_family_identity.py`; expect PASS; drop one family and expect FAIL |
| `evidence/12_GATES/RECEIPT_PACK_C1_C2.json` | re-run each of the 18 `argv` in its recorded `cwd`; compare `rc` to `expected_rc` |
| `evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt` | `git merge-base <A> <B>` must equal the Stage A head |
| `evidence/12_GATES/{C4_STAGE_B_REFUSAL_TESTS_SOURCE.py,C4_REFUSAL_TESTS_RUN.log}` | diff the extracted test bodies against the Stage B head's test file; re-run the two named tests |
| `evidence/12_GATES/SUBJECTS.json` | `git rev-parse HEAD` + `git ls-remote origin`; compare to the recorded heads |
| `evidence/12_GATES/writeset_gate_local_final.txt` | re-run `scripts/run_writeset_gate_locally.py` for both stages; expect exit 0 + the planted refusals |
| `evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt` | match each quoted hosted-run line to its run id; the wheel-gate winner must read `mode=INSTALLED` |
| `far-study/*` (this study, the E8 finding, the capability boundary, the retrieval finding) | read as maker-side material; the capability probe is itself re-runnable against the lane |
| `scripts/{run_writeset_gate_locally,report_family_identity,read_ci_for_sha,fetch_job_log}.py` | run each; they are the round's re-derivation tools |

### D.2 May NOT be handed over yet

| withheld | reason |
|---|---|
| the two candidate heads as an **acceptance subject** | no acceptance row run; every lane verdict advisory and none a pass |
| the final C1 bundle | co-location gap (D3) |
| the final C3 bundle | rests on wording this round now knows to be false (F1, D4) |
| any claim presented as **independently verified against the tree** | no independent party has touched the tree; the checker lane cannot read or exec (F9) |
| a PARTIAL workorder result | the entrypoint accepts only PASS/FAIL |
| the 12 external-evidence items; any merge/tag/release/archive | owner/host gates; flags hold |

## E. Marginal-value read

The blueprint's Appendix B `required_external_evidence` carries 12 items, recorded at 0/12 in the
previous round's `OWNER_ACTION_REQUEST.md` and restated in its
`verify/far/FAR_S4POST_DEVIATION_AND_REMEDIES_20261013.md`. One item (`REAL_VENDOR_SCHEMA`) advanced to
an evidence-level partial closure in the previous round: the official schema bytes were fetched
(HTTP 200, 1805 bytes) and are byte-identical to the vendored copy - **re-verified in this round by
recomputing the digest of `packaging/public-plugin/vendor-plugin.schema.json`
(`0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`)**; the owner digest pin is still
outstanding. **This round moved 0 of the 12**, and no further checker dispatch can close an owner gate.

Deciding sentence: the next action is the owner's D1/D6 ruling, because the audit trail currently
contains a committed claim its own mechanical diff falsifies, and because the checker lane's verdicts
have been carrying a ceiling nobody had measured until now.

## F. DO-NOT list

Do not widen either allowlist further (admitted obligation). Do not relax any oracle, threshold,
validator, guard, exit code or denominator to buy a PASS. Do not merge, tag, release or archive. Do not
present an advisory verdict as an acceptance. Do not widen the checker: no sandbox escalation, no
substitute arm - note that the substitute at VERIFY rank 1 is the *same model as the EXECUTE writer*, so
an unforced dispatch would have had the writer adjudicate its own work. Do not record a PARTIAL verdict
as a workorder result. Do not claim either allowlist addition was made to buy a green run (not claimed;
the defect is the assertion). Do not build machinery to verify machinery without beating the no-build
option. Do not push `main`, force-push history, or move the frozen refs.

## Findings register (this study)

F1 allowlist widened against an admitted obligation; F2 eight advisory verdicts, none a pass;
F3 three verdicts polluted by this round's own bundles; F4 C1 shortfall = co-location gap;
F5 receipt pack binds commands to exit codes; F6 canonical admission 0 acceptances / 0 evidence_refs;
F7 spine 405 workorders, attributed (+6 S4R3X, +2 FAR, +4 a parallel STACK-HYGIENE round);
F8 flags hold; **F9 the checker lane cannot read local files or execute processes - its ceiling is
bundle auditing, not tree verification; and this round's verify prompt was mis-specified by the maker
accordingly**; F10 the PLAN leg is measured on `deepseek-v4.1-flash`, not the mandated sol-medium route.
