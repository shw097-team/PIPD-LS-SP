# Tasks — S4-R2M conditional merge and preview.3 gate

## 1. Read-only preflight and reconciliation

- [x] 1.1 Freeze both source documents (prompt + acceptance report) by path and SHA-256
- [x] 1.2 Fresh `git ls-remote` of `main`, `s4-r2-affected-only-20261011` and the preview tags; confirm no baseline drift
- [x] 1.3 Confirm `main` is an ancestor of the candidate head so a fast-forward is structurally possible
- [x] 1.4 Re-derive both named blockers against the candidate head instead of trusting the report
- [x] 1.5 Read the real `--root` surface in `src/pipd_ls_sp/cli.py` before writing any claim about it

## 2. Native prompt-contract compiler (P0 hard gate)

- [x] 2.1 Generate the C0–C9 contract programmatically so every field is schema-exact
- [x] 2.2 `lint` / `activation` / `acceptance` / `compile` / `duplication` → `PROMPT_COMPILE_PASS`, 0 errors
- [x] 2.3 Retain all four per-stage receipts plus the compiler receipt, the report and the thin prompt
- [x] 2.4 Record the compiler bundle digest and confirm it matches the receipt's `compiler_sha256`

## 3. HGK admission (P0 hard gate)

- [x] 3.1 Reuse the live PIPD project; do not start a duplicate
- [x] 3.2 Admit four obligations through the typed lifecycle API (requirement → lease → FROZEN → TaskSpec → WorkOrder)
- [x] 3.3 Bind each admitted work-set to this round's candidate worktree and base head
- [x] 3.4 Read the binding back with a read-only query and take a checkpoint

## 4. KANBAN / SWARM / GSTACK / OPENSPEC

- [x] 4.1 Create the round board through the native CLI and persist the readback
- [x] 4.2 Build the SWARM graph (root + four workers + verifier + synthesizer) in one call
- [x] 4.3 Record the named-method route readback and what each route does not confer
- [x] 4.4 Record this change proposal

## 5. M1 — documentation change

- [ ] 5.1 Add the `CLI vs Skills` path section between `Start here` and `Quickstart`
- [ ] 5.2 Correct the `--root` statements to the real CLI surface
- [ ] 5.3 Add a docs smoke test asserting both documented positive forms and one refused form
- [ ] 5.4 Prove the diff touches only the admitted paths

## 6. M2 — isolated focused regression

- [ ] 6.1 Freeze the M1 candidate commit and tree
- [ ] 6.2 Build a byte-equivalent writable clone in admitted scratch
- [ ] 6.3 Run the six named affected modules plus the CE and wheel positives
- [ ] 6.4 Re-run the exact-set oracles (19 schemas + registry, 8 skill directories, 13 CLI commands)
- [ ] 6.5 Compare the read-only subject's bytes before and after the run
- [ ] 6.6 Independent officer lane on a different model family re-derives the decisive figures

## 7. M3 — integration (owner gate)

- [ ] 7.1 Produce the one-page merge decision record
- [ ] 7.2 Prove the write credential's repository scope, or record `AUTH_BLOCKED`
- [ ] 7.3 Fast-forward `main` only under owner approval, then read the remote ref back
- [ ] 7.4 Confirm the preview.2 tag and assets are byte-identical afterwards

## 8. M4 — preview.3 release gate (owner-selected only)

- [ ] 8.1 Owner decision: `RELEASE_PREVIEW3=YES` or `NO`
- [ ] 8.2 If YES: PEP 440 version strictly greater than `0.1.0`, wheel, separate mount pack, checksums
- [ ] 8.3 If YES: isolated install, upgrade from `0.1.0`, rollback smoke, anonymous re-download readback
- [ ] 8.4 If NO: record `PREVIEW3_DEFERRED` and stop; create no empty tag
