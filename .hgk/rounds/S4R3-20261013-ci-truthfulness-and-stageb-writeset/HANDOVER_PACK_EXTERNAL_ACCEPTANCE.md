# External acceptance handover pack — PIPD-LS-SP S4 R3

Prepared by: the governed maker session (HG-KSEOS control plane; Hermes as the governed
runtime/orchestration plane). Date: 2026-10-13.
**Claim ceiling: this pack is maker-side material. It is not an acceptance, it grants no PASS, and it
changes no flag.** `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` all still hold.

## 0. Read this first — four disclosed deviations

Disclosed here so that finding them does not read as their having been hidden. Each is a real defect
this round found (two of them against its own earlier claims), not a caveat added for comfort.

| # | deviation | exact state | who can close it |
|---|---|---|---|
| **1** | **The write-set allowlist was widened against an admitted obligation.** | The stage-b `ALLOWED` set gained exactly two entries relative to the frozen subject: `docs/USER_GUIDE.md` and the round's own directory. The admitted requirement forbidding widening is `REQ-S4R3X-GATE-FALSIFIABILITY-002` in the canonical spine (FROZEN, wording quoted verbatim in the C3 bundle and re-readable from the spine read-only). The stage-b `DENIED` set is unchanged and no frozen path became writable. **Stage-b-wise only**: stage-a is a new stage whose `DENIED` set omits `src/`, so stage-a paths there are refused by its allowlist rather than by a category denial; the clause must not be read as uniform across both stages. | owner ruling (accept / correct the statement / narrow the entry; the last edits a candidate head) |
| **2** | **Candidate content carries a false statement.** | `.github/workflows/public-plugin-verify.yml` contains the inline comment "This change widens NEITHER allowlist". It is false as written, for the reason above. It has deliberately **not** been edited: doing so would change an audited candidate head and require a fresh verification round. | owner |
| **3** | **The PLAN leg is not on the mandated model.** | The session that produced this round ran `deepseek-v4.1-flash`/`opencode-go`, not the mandated `GPT 6.1 SOL-MEDIUM`/OpenAI OAuth. Measured on the session record, not inferred. | owner (one config command; recorded in `far-study/PLAN_LEG_DIVERGENCE.md`) |
| **4** | **No independent party has verified anything against the tree.** | The checker lane cannot read local files and cannot execute any process (three attempts, all refused `blocked by policy`, measured with its own receipt). Its verdicts audit a bundle's internal consistency; they are not tree-level verification. | external acceptance officer (you), or an owner-enabled read/exec-capable checker |

## 1. Subject — obtain it and resolve the heads yourself

```bash
git clone https://github.com/shw097-team/PIPD-LS-SP.git && cd PIPD-LS-SP
git fetch origin
git rev-parse origin/fix/s4r3-stage-a-ci-truthfulness-20261013   # Stage A candidate
git rev-parse origin/feat/s4r3-stageb-successor-20261013         # Stage B successor (stacked on A)
git ls-remote origin refs/heads/main refs/tags/v0.1.1-preview.3  # the frozen refs
```
As written: Stage A head `5310896e` (unchanged since it was first published); Stage B head `9d3845a`;
`main` `224591431a…` and tag `v0.1.1-preview.3` target both **untouched** by this round. Verify the
stacked relationship yourself: `git merge-base <A> <B>` must equal the Stage A head. Do not take these
short forms on trust - resolve them.

Pull requests: `#5` is the stacked successor (base = Stage A). `#4` is superseded and still open; its
disposition is the owner's.

## 2. Evidence you can re-derive (each with its falsifying check)

Every path is under `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` in the Stage B
worktree. These are the artifacts this round asks you to judge.

| artifact | falsifying check (run it yourself) |
|---|---|
| `evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt` | re-run the two `git show` commands quoted at its top against the frozen subject and both heads; re-parse every `ALLOWED`/`DENIED` assignment; re-diff. This is the receipt for deviation #1. |
| `evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md` | compare its quoted claim against the workflow text: `grep -n "widens NEITHER" .github/workflows/public-plugin-verify.yml` |
| `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md` | `python .hgk/rounds/.../scripts/report_family_identity.py --tree <worktree>`; expect PASS with 19 family names in the expected order and 20 digests equal to the tree; then drop one family from an installed registry and expect FAIL |
| `evidence/12_GATES/RECEIPT_PACK_C1_C2.json` | for each of its 18 steps re-run the recorded `argv` in the recorded `cwd` and compare the observed `rc` to `expected_rc`; the five negative cases must be refused with their recorded typed codes |
| `evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt` | `git merge-base <A> <B>` must equal the Stage A head |
| `evidence/12_GATES/C4_STAGE_B_REFUSAL_TESTS_SOURCE.py` + `C4_REFUSAL_TESTS_RUN.log` | diff the extracted test bodies against `tests/test_public_plugin_packaging.py` at the Stage B head; re-run the two named tests |
| `evidence/12_GATES/writeset_gate_local_final.txt` | re-run `scripts/run_writeset_gate_locally.py` for both stages; expect exit 0 including the planted-violation refusals |
| `evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt` | match each quoted hosted-run line to its run id on GitHub; the wheel-gate winner line must read `mode=INSTALLED` |
| `evidence/12_GATES/GUARD_SELFTEST_RECEIPT.json` | re-run `scripts/bundle_guards.py selftest`; the positive must pass and all three negatives must refuse with their typed codes |
| `evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A*.md` | read as **advisory only**; check the recorded `served_arm`, nonce presence, and per-claim verdict. None is a pass, and see deviation #4 for their ceiling |
| `far-study/` (decision study, capability boundary, retrieval finding, E8, PLAN-leg divergence) | maker-side analysis; the capability probe is itself re-runnable against the lane |
| `scripts/*.py` | the round's re-derivation tools; run each from the committed tree |
| `evidence/12_GATES/HEAD_PROVENANCE_RECEIPT.txt` | re-run `git rev-parse HEAD` in both worktrees and re-run the gate; the receipt's before/after HEADs and the hosted run→SHA map must reproduce |
| `evidence/12_GATES/C3_REVISION_BINDING_RECEIPT.txt` | re-run the two `git rev-parse <rev>:<workflow>` lines and the range diff; the blob identity and the empty path diff must reproduce |
| `evidence/12_GATES/GUARD_SELFTEST_RECEIPT.json` + `GUARD_{COVERAGE,RECEIPTS}_*.json` | re-run `scripts/bundle_guards.py selftest` and the two guard modes; the positive must pass and every negative must refuse |
| `far-study/LANE_RUNS_FINAL_LEDGER.md` | read the attempt table; every "valid" row must show a usage receipt and the nonce, and the two INVALID rows must not be cited anywhere |

### 2b. Claim state after the lane runs (valid turns only)

All four round claims now stand at **CONFIRMED at bundle level**: C1 (a11: C1a-C1d), C3 (a14: C3a-C3e),
plus C2 and C4 from the earlier series. **None of it is an acceptance** - see deviation #4 for the
ceiling. One refinement the checker forced and the round now adopts: the "frozen-path refusals still
refuse" half holds **stage-b-wise**; stage-a's new `DENIED` set omits `src/`, so stage-a relies on its
allowlist rather than a category denial. Do not read that clause as uniform across both stages. Two of
this round's dispatch attempts are recorded as **INVALID** (the prompt failed to name the nonce token);
their content exists but is not cited as a verdict.

## 3. What is explicitly NOT offered

| withheld | reason |
|---|---|
| the candidate heads as an **acceptance subject** | no acceptance row has been run; no capital-P PASS exists anywhere in this round |
| any claim of **independent verification against the tree** | deviation #4 |
| the final C1 and C3 claim bundles as "closed" | C1 had a co-location gap around an artifact that already exists; C3 rested on a claim this round's own diff falsified |
| a PARTIAL workorder result | the spine's workorder entrypoint accepts only PASS/FAIL, so a partial verdict cannot be recorded truthfully |
| the blueprint's 12 `required_external_evidence` items | all are owner/host gates; this round moved **0** of them |
| merge, tag, release, archive | flags hold; none was performed |

## 4. Open owner gates (not maker-side)

F003 publisher identity and brand assets; vendor validator and portal submission; the four-host UAT
(Hermes native skill, Codex desktop, Codex CLI native skill, Claude Code) - `NOT_EXECUTED`; the
blueprint's 12 external-evidence items at 0/12; `.hgk` archive policy (~62 MB); PR #4 disposition; the
final merge/release decision.

## 5. How to report back

The most useful return is per-artifact: which of your checks reproduced, which did not, and the exact
command and output for anything that disagreed. Two specific questions worth answering explicitly:
(a) does the diff in `C3_ALLOWLIST_BASELINE_DIFF.txt` reproduce, and if so is the two-entry widening
acceptable, correctable, or fatal; (b) should the false workflow comment be corrected on the candidate
(which invalidates these heads and needs a fresh round), or left disclosed as-is.
