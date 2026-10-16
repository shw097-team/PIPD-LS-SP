# Tasks

## 1. Back-fill the round's own plan documents

- [ ] 1.1 `r18/TASK_CHECKLIST.md`: every `[ ]` becomes the status the round actually reached
      (`[x]` / `[-]` NOT_RUN / `[D]` DEFERRED / `OWNER GATE`), each row carrying its evidence ID.
- [ ] 1.2 `r18/DETECTION_CHECKLIST.md`: the status and evidence columns are filled per `CK-nn`.
- [ ] 1.3 Machine check: the count of surviving `[ ]` rows is zero apart from rows explicitly marked
      NOT_RUN / DEFERRED, and every cited evidence ID resolves to a real file (no dangling IDs).
- [ ] 1.4 The back-fill is *audited*, not self-declared: an independent pass re-checks a sample of
      rows against the named artifact.

## 2. Write the external engineering entry document

- [ ] 2.1 Repository and branch model: which branch is the product, which is the evidence, and why.
- [ ] 2.2 The governed write-set gate: the declared stage, the allowlist, the local reproduction
      command, and the amendment rule.
- [ ] 2.3 The lane model: the ordered candidate pool, the owner-ordered rank-1 collision, and how to
      pin an arm by identity.
- [ ] 2.4 Build and test commands, with their expected output.
- [ ] 2.5 Module map and extension points (where a new check, tool or skill goes).
- [ ] 2.6 Open tickets and owner gates, each as a single action.
- [ ] 2.7 Standing prohibitions (immutable release, public directory, no agent self-ratification).

## 3. Machine-readable round state

- [ ] 3.1 `ROUND_STATE.json` with branch tips, immutable identities, gate results, tickets, ceiling.
- [ ] 3.2 Validate it parses and that every SHA it names matches the live remote.

## 4. Independence, publication, closure

- [ ] 4.1 An independent VERIFY dispatch re-runs the handover document's commands and reports which
      claims hold, which do not, and its own ceiling.
- [ ] 4.2 Evidence branch commit with LF normalisation applied **inside the packet only**, then a
      recomputed `SHA256SUMS`; a fresh clone verifies `N/N OK`.
- [ ] 4.3 The product branch is untouched and its hosted `verify` stays green.
- [ ] 4.4 Owner closeout/TT updated with the new tickets and the owner-gated items.
