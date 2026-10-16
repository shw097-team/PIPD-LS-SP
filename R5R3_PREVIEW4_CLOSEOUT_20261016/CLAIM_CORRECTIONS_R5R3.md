# CLAIM CORRECTIONS — round R5R3-20261016-preview4-closeout

An independent acceptance officer (VERIFY/SECURITY lane, CODEX CLI, `required_arm == served_arm ==
opencode-go/deepseek-v4.1-flash`, `used_rank 3`, `nonce_present: true`, `used_seconds 811`, `ok: true`) reviewed
this packet and returned `nonce R5R3-VERIFY-20261016-b7c41e9d` with

```
C1 PASS  C2 PASS  C3 FAIL  C4 FAIL  C5 PASS        over_reach_found: true
```

Its findings are correct and are applied here as **claim corrections**. No frozen subject was rewritten: the
commits, the ZIP digests and the release assets are untouched; what changed is the wording of this round's own
records.

## What the checker confirmed (not changed)

- `C1` / `C2` PASS: it recomputed both rebuilt ZIPs itself — `68,357 B / 545e359a…` at `cc6c193` and
  `68,355 B / 2f9ae010…` at `062d84ae` — and found them corroborated by the `.sha256` sidecars, both
  `RELEASE_RECEIPT.json` files, the frozen ledgers and two further copies staged for the host smoke. The
  round's core new finding is independently reproduced.
- `C5` PASS on the owner-decision request: three decisions, each declared unexecuted, nothing asserted as done.

## Correction 1 — TT-03 (`DRIFT_VALUE`): the "NOT REPRODUCED" wording is WITHDRAWN

The checker's decisive counter-evidence: this packet's own `gstack_readback_epoch19.json` (registry **epoch
19**, taken 03:15Z) carries exactly one drift row — `code DRIFT_VALUE`, `pointer /codex_sha256`, `expected
D13914CED6C7AF174D8D638DB938284231227312104B06A25E9608C632A7DAEC`, `actual e98c516f1c893578…`,
`drift_is_clean: false`. Re-derived in this round: that file does contain the row, and it disagrees with the
epoch-21 probe (`check_drift` = 0 rows, declared sha256 == the live binary).

Corrected disposition (now in `TT_DISPOSITIONS.md`): **REPRODUCED at epoch 19; NOT PRESENT at epoch 21.** The
earlier text reported the clean epoch-21 measurement as though no drift had been reproduced anywhere, while
shipping the artefact that reproduces it. That is the over-reach: a claim must be worded so the packet's own
files cannot refute it.

## Correction 2 — TT-02: "verified from the branch itself" overstated

The packet carries no git-object or remote-branch readback, so an object-level verification claim is not
re-derivable from the packet alone. The disposition now says so explicitly and substitutes what the packet
does support: the amendment is recorded as landed by the previous round's merge, and this round exercised the
same gate positively (PR #17: `verify` **success**, `offline-gate` **success**, `mergeable_state: clean**).

## Correction 3 — the owner-decision request's standing line was narrower than the record

It said the round's only external effect was the evidence push. The record also holds the previous round's
owner-authorised merge of PR #16 (`dba4b19` → `d3bd5456`). Corrected to state the session's external effects
in full, while keeping the ODR's own assertion (nothing executed by the decisions it asks for) intact.

## Correction 4 — hygiene: two "live" probes with no dating

The checker's `C3` FAIL is about consistency, not about either measurement: `raw/` mixed readbacks from
different rounds and epochs, so both could be honestly called "live" while disagreeing (epoch 19 vs 21, SoD
OK vs VIOLATION, drift 1 row vs 0 rows). This packet now ships `ARTIFACT_DATING.md` naming each readback's
epoch and time. The durable fix — one dated subdirectory per measurement — is filed as owner-ready, not
silently applied.

## Disclosures the checker asked for and this packet had not carried

- **A previous round's independent checker verdict is REJECTED.** `CHECKER_VERDICT_WS_C.json` (now copied into
  this packet) records `VERDICT: REJECTED` on the product branch head `4cbb22f`, with `GATE_BAD_COUNT: 0`,
  identity tag/commit/tree MATCH and coverage 6/6, and one finding: the "nothing product-shaped" assertion
  fails against the gate base `f4021ae…` because the range contains already-merged product paths
  (`src/pipd_ls_sp/*.py`, `schemas/ClaimCeiling.schema.json`). That answer was accepted and the record was
  corrected at the time via a `range_semantics` field; the verdict itself was **not** disclosed in this round's
  TT list until now. It also carries the well-known transport gap on its receipt
  (`dispatcher_code: ERR_NO_ARM_EMITTED_NONCE` although the arm ran 268.83 s and its own final message ends with
  the run nonce).
- The WS-C verdict's own not-established items stand as residuals: the VERIFY-probe cause, hosted-CI
  readbacks, and the absence of tag/release effects inside a packet — the same ceiling the new checker restates.

## Residual raised by this round's checker — independently re-derived in this round (CONFIRMED)

The checker reports an outlier inside control plane itself, and this round **re-derived it**:

```
registry.routes.PLAN.model            = gpt-6.1-sol        (provider openai-codex)
config/model-lane-assignment.json
  assignment[0] (lane_group PLAN)     = glm-5.3-flash      (provider opencode-go, effort medium)
  rationale: "Revision 19 owner order 2026-10-15: rank-1 default is now opencode-go/glm-5.3-flash
              (medium) for the in-Hermes PLAN & Orchestrator plane; ..."
check_drift(registry=reg)             = 0 rows
```

Two declarations inside the canonical control plane disagree about which model the PLAN lane defaults to, and
the drift checker reports clean because it compares `projections[].bindings[]` pointers, not the supply field
(`assigned_model`) against the live route. Corroborating detail: `declared_conflicts` is `null`, so the
disagreement is not a declared one. Note the live route also serves `gpt-6.1-sol` while this round's owner
mandate asks for GLM-5.3-Flash on the in-Hermes PLAN plane — i.e. the assignment file already records the
mandated intent and the route does not serve it.

Status: **CONFIRMED control-plane finding, owner-ready.** Classification CANONICAL: resolving it is a route
change with its own affected projections and its own SoD pair, i.e. an owner/WorkOrder act. This round does not
edit the registry.

## Claim ceiling of the corrected packet

Everything above is LOCAL / CANDIDATE-ONLY. The independent checker's own ceiling is accepted verbatim:
*hgk_canonical_acceptance NOT performed; the merge/tag/release/production effects are not verifiable from
within the packet.* The round executes no release, tag, install, publication or promotion.
