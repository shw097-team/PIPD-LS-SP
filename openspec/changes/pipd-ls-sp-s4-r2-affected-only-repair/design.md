# Design — S4-R2 affected-only repair

## Context

The reaudit sampled `main` (`4445db5a6d1b3138946fd7c4fe3b712e4faf1af7`) and the public
`v0.1.0-preview.2` release (`8faa64e581e8c25f5ec355475e29561847da3ead`). A frozen, unpushed candidate
lineage already existed from the previous narrow-repair round
(`0bc7bb4b` / tree `e95e33f008a617faef8881431b27a468f516d409`). The report's own rule — an affected
subject already closed with fresh positive/negative evidence is skipped, not re-done — governs the
whole round.

## Goals / Non-Goals

**Goals.** Close the genuinely open deltas; prove every "already closed" claim by execution; keep the
claim ceiling honest; hand an independent checker a frozen subject and raw commands.

**Non-Goals.** No S0–S4 rebuild, no `preview.2` re-tag or byte change, no competing canonical store,
no S5+ activation, no new machine-contract family, no re-litigation of the preserved R7 scoped PASS /
R8 overall FAIL.

## Decisions

**Reconcile before building.** The single highest-value decision was to run each finding's own
counterexample against the existing candidate *before* writing any work order. Result: nine of twelve
findings were already closed. Only `F-S4R2-05` and `F-S4R2-09` were genuinely open, plus one new
finding (`F-S4R2-NEW-01`) found during reconciliation. That is the difference between a four-obligation
surgical round and a twelve-work-order rework.

**Fresh evidence, not file presence.** "The file exists" is not closure. Each closed finding is
asserted on an executed positive case and its matching negative case, with the raw files retained. The
probe itself was wrong four times before the product was ever in question (invented axis names, a
mis-taken seal helper, a wrong extraction root), which is why probe failures are recorded as probe
failures.

**Residual typing is in write-set, and disclosed.** `ProfileBinding`'s `profile`, `axes`, `vetoes`,
`artifact_depth`, `assurance` were still `{}` in schema. The duplicate-axes finding (`F-S4R2-02`)
is decided inside `compute_profile()` and evidenced in a `ProfileBinding` record, so that schema is
"actually affected" by the admitted `S4-CONTRACT-HARDEN-03` write-set. It is typed here, and the
addition beyond the report's literal wording is disclosed rather than passed off as pre-existing.

**No distribution churn for a docs fix.** A README/schema-candidate change does not justify rebuilding
the wheel. `preview.2` and its bytes stay exactly as published.

**Claim ceiling.** The maker can reach `CANDIDATE_LOCAL_QUALIFIED` only. Independent acceptance,
`FULL_S0_S4_GATE` and `PRODUCTION_VERIFIED` are out of reach for this round and are not asserted.

## Risks / Trade-offs

- **Same-model-family risk on the checker axis** is a live residual: if the checker route is not
  distinct from the maker route, the mitigation is process independence (separate process, fresh
  context, read-only, re-derivation required) with the mandate recorded as an owner-authorised
  deviation — never reported as satisfied independence.
- **The candidate lineage is unpushed.** A checker that only samples GitHub would see the pre-repair
  state; the frozen local subject and its commit/tree are therefore handed over explicitly.
- **Publication is credential-blocked** until a working token exists; the honest terminal state is
  `NOT_EXECUTED` with a named cause, not a narrated push.

## Migration Plan

Rollback is the recorded pre-round branch tip (`546bc2e…`) plus a pointer to the untouched
`v0.1.0-preview.2` tag. No data migration is involved.

## Open Questions

- Whether the owner wants `ProfileBinding`'s remaining contract fields typed in full (a larger schema
  change) — queued as a trigger, not assumed.
- Whether a new preview version will be issued at all; if so, PEP 440 ordering must be checked against
  the already-installed `0.1.0` distribution before any claim of upgradability.
