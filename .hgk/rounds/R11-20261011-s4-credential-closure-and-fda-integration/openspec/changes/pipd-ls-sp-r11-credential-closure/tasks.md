# tasks - pipd-ls-sp-r11-credential-closure

## 1. Admit (REQ-PIPD-R11-ADMIT-004)

- [x] 1.1 HGK admission via the typed SharedSpine / ProjectLifecycleController API - no raw SQL
- [x] 1.2 6 obligations FROZEN, 0 errors, project still EXECUTING
- [x] 1.3 Kanban, swarm and GSTACK readback written to disk (`kanban/`, `swarm/`, `surface/`)
- [x] 1.4 OpenSpec change written (this file pair)

## 2. Execute the remaining credential operations (REQ-PIPD-R11-FDAEXEC-001)

- [ ] 2.1 Delete the redundant personal-account App (readback: absent from the account's app list)
- [ ] 2.2 Retire the long-lived PAT (readback: absent from the account's token list)
- [ ] 2.3 Record, for each, whether the owner's interactive second factor was required

## 3. Integrate into the automation team's evidence surface (REQ-PIPD-R11-FDAEVID-002)

- [ ] 3.1 Read the team's evidence contract and the contract's preflight checker
- [ ] 3.2 Author the discipline + evidence artefact in that contract's form (single MD, raw embedded)
- [ ] 3.3 Run the contract's preflight checker to PASS
- [ ] 3.4 Commit ONLY this round's paths in the Fabric repository

## 4. Adjudicate activation (REQ-PIPD-R11-ACTIVATE-003)

- [ ] 4.1 Determine what a consumer of the broker would have to be, and what it would refuse
- [ ] 4.2 Decide: activate now, or admit activation as its own round - and execute that decision

## 5. Verify and close (REQ-PIPD-R11-VERIFY-005, REQ-PIPD-R11-CLOSURE-006)

- [ ] 5.1 Independent CODEX CLI check, asserting immutable facts only
- [ ] 5.2 Quote the checker's could-not-verify list verbatim
- [ ] 5.3 Closure report: claim ceiling, open items by WHO can close, every side effect disclosed
