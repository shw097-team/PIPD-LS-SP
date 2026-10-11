# tasks - pipd-ls-sp-r10-bclass-decisions

## 1. Admit (REQ-PIPD-R10-ADMIT-003)

- [x] 1.1 HGK admission via the typed SharedSpine / ProjectLifecycleController API - no raw SQL
- [x] 1.2 6 obligations FROZEN, 0 errors
- [x] 1.3 Kanban, swarm and GSTACK readback written to disk (`kanban/`, `swarm/`, `surface/`)
- [x] 1.4 OpenSpec change written (this file pair)

## 2. Adjudicate the three rows (REQ-PIPD-R10-AUTHORING-001)

- [x] 2.1 Delegate a bounded analysis of the three rows to disk (`evidence/SSOT_ROW_AUTHORING_ANALYSIS.md`)
- [ ] 2.2 Per-row verdict: OWED-BUILDABLE-FAITHFULLY / NOT-OWED-HERE-EXTERNAL / NEEDS-OWNER-DESIGN
- [ ] 2.3 FAR recording the adjudication and what was REFUSED, with the reason
- [ ] 2.4 Verify any authored artefact against the existing material it was derived from

## 3. Credential tooling home (REQ-PIPD-R10-CREDITOOLS-002)

- [x] 3.1 Delegate the migration plan, candidate files and governance-route analysis
- [ ] 3.2 Review the plan; apply the candidate to its determined durable home
- [ ] 3.3 Prove the install works without activating it (selftest on DUMMY credentials only)
- [ ] 3.4 Record the governance route: any control-plane change as its own admitted round
- [ ] 3.5 Enumerate the residual human steps, each with WHY it cannot be automated

## 4. Execute and verify (REQ-PIPD-R10-EXECUTE-004, REQ-PIPD-R10-VERIFY-005)

- [ ] 4.1 Execute the adjudicated outcomes (build only what was adjudicated buildable)
- [ ] 4.2 Independent check on the CODEX CLI VERIFY lane, asserting immutable facts only
- [ ] 4.3 Quote the checker could-not-verify list verbatim

## 5. Close (REQ-PIPD-R10-CLOSURE-006)

- [ ] 5.1 Closing report: claim ceiling, and every open item classified by WHO can close it
- [ ] 5.2 Disclose every side effect, including pushes and control-plane or canonical-store writes
