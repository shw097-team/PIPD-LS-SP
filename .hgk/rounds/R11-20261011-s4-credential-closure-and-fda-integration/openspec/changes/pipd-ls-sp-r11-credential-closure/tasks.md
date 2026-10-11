# tasks - pipd-ls-sp-r11-credential-closure

## 1. Admit (REQ-PIPD-R11-ADMIT-004)

- [x] 1.1 HGK admission via the typed SharedSpine / ProjectLifecycleController API - no raw SQL
- [x] 1.2 6 obligations FROZEN, 0 errors, project still EXECUTING
- [x] 1.3 Kanban, swarm and GSTACK readback written to disk (`kanban/`, `swarm/`, `surface/`)
- [x] 1.4 OpenSpec change written (this file pair)

## 2. Execute the remaining credential operations (REQ-PIPD-R11-FDAEXEC-001)

- [x] 2.1 Delete the redundant personal-account App (readback: absent from the account's app list)
- [x] 2.2 Retire the long-lived PAT - **NO-OP, and that is the finding**: the file's token is HTTP 401 and
      is not on the account's token list at all (`shw097`). There was nothing to revoke; the honest
      outcome is "the bridge was already dead", not "we retired it". Recorded in FAR-...-CREDGATE-001.
- [x] 2.3 Record whether the owner's interactive second factor was required: **yes, once** - one login and
      one second-factor entry, spent on the deletion the owner had approved, and the organisation App was
      verified intact afterwards on two independent surfaces.

## 3. Integrate into the automation team's evidence surface (REQ-PIPD-R11-FDAEVID-002)

- [x] 3.1 Read the team's evidence contract and the contract's preflight checker
- [x] 3.2 Author the discipline + evidence artefact in that contract's form (single MD, raw embedded)
- [x] 3.3 Run the contract's preflight checker to PASS - **before AND after** the addition, so the
      untouched sealed three-way binding is proven rather than asserted
- [x] 3.4 Commit ONLY this round's paths in the Fabric repository (2 of them; the working tree's other
      entries were left exactly as found)

## 4. Adjudicate activation (REQ-PIPD-R11-ACTIVATE-003)

- [x] 4.1 Determine what a consumer of the broker would have to be, and what it would refuse
- [x] 4.2 Decide and execute: **activation is NOT performed**; the recorded decision and its reasons (no
      in-repo push path exists, push is contractually forbidden, and the activation surfaces are
      WorkOrder-only) are the deliverable

## 5. Verify and close (REQ-PIPD-R11-VERIFY-005, REQ-PIPD-R11-CLOSURE-006)

- [x] 5.1 Independent CODEX CLI check, asserting immutable facts only - **three dispatches were VOID before
      one was valid**, for four distinct delivery defects now fixed and written up in
      `far/FAR-PIPD-R11-LANEDISPATCH-003.md`
- [x] 5.2 Quote the checker's could-not-verify list verbatim (see the closure report and
      `verify-codex/VOID_ATTEMPT_2_ADVERSARIAL_FINDINGS.json`)
- [x] 5.3 Closure report: claim ceiling, open items by WHO can close, every side effect disclosed
