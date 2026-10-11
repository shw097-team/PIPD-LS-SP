# Tasks — S4-R2 affected-only repair

## 1. Read-only preflight and reconciliation

- [x] 1.1 Freeze the reaudit report and verify its SHA-256 against the prompt header
- [x] 1.2 Fresh-read GitHub `main`, tag, release assets; confirm no new commits to reconcile
- [x] 1.3 Run each of `F-S4R2-01..12`'s own counterexample against the candidate before writing anything
- [x] 1.4 Record every probe defect as a probe defect (four were found), never as a product defect
- [x] 1.5 Register `F-S4R2-NEW-01` with its counterexample and its earliest owner

## 2. Native prompt-contract compiler (P0 hard gate)

- [x] 2.1 Generate the `C0..C9` contract programmatically so every field is schema-exact
- [x] 2.2 Repair each native lint block in the CONTRACT, never in the tool
- [x] 2.3 `lint` / `activation` / `acceptance` / `compile` / `duplication` → `PROMPT_COMPILE_PASS`
- [x] 2.4 Retain all five raw receipts plus the compiled `thin-prompt.md`

## 3. HGK admission (P0 hard gate)

- [x] 3.1 `hg_kseos doctor` healthy under the canonical root
- [x] 3.2 Reuse the existing PIPD project; do not start a duplicate
- [x] 3.3 Admit the four obligations through the typed lifecycle API (requirement → lease → FROZEN → TaskSpec → WorkOrder)
- [x] 3.4 Bind each WorkOrder to this round's candidate worktree and base head
- [x] 3.5 Take a checkpoint and read the state back with a read-only query

## 4. KANBAN / SWARM / GSTACK / OPENSPEC

- [x] 4.1 Create the round board and write the board readback to disk
- [x] 4.2 Build the SWARM graph (root + four workers + verifier + synthesizer) in one call
- [x] 4.3 Resolve each obligation's named-method route and record what it does not confer
- [x] 4.4 Author this change and validate it `--strict`

## 5. Execute the open deltas (affected-only)

- [x] 5.1 Replace the front page's placeholder block with the real, replayable walk-through
- [x] 5.2 State the distribution-identity hazard with PEP 440 guidance
- [x] 5.3 Type the residual `ProfileBinding` contract fields
- [x] 5.4 Focused tests for 5.1–5.3, each with a negative case
- [x] 5.5 Add `examples/first-run/` inputs so the documented commands resolve without a placeholder

## 6. Regression and freeze

- [x] 6.1 Full suite on the candidate; compare against the base figure on the same interpreter
- [x] 6.2 Exact-set invariants survive: 19 schemas, 8 skills, 13 CLI commands
- [x] 6.3 Freeze the candidate commit and tree; a non-mutation guard measures the checker's effect
- [x] 6.4 Restore any harness-induced dirty files and re-measure

## 7. Independent verification

- [x] 7.1 Independent checker on a different model, separate process, read-only, re-deriving every
      decisive claim rather than reading the maker's report
- [x] 7.2 Record the residual honestly if the checker route is not model-distinct from the maker
- [x] 7.3 Preserve the checker's verdict even when it is `FAIL`

## 8. Evidence and publication

- [x] 8.1 One local acceptance master document carrying the evidence return pack
- [x] 8.2 12/12 finding dispositions and 10/10 work-item dispositions, each with a pointer
- [x] 8.3 Publication attempted under an approved credential; otherwise `NOT_EXECUTED` with cause
- [x] 8.4 TT register for everything left open, each with an owner and a revisit trigger
