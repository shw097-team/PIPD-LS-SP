# FAR-PIPD-R10-OWNERITEMS-003 — the two owner items, adjudicated and executed

Round `R10-20261011-s4-bclass-decisions`. Owner authorised adjudication **and** execution. Both items had
been parked as "owner only"; both are now decided, and one of the two decisions is a **refusal to ratify**.

## Item 1 — the MCP record's shape

### The question

The R10 record `MCP_MATERIALIZATION_DECISION.json` was emitted as `provisional: true`,
`canonical: false`, `ratification_required: true`, carrying an invented schema id. Ratify it or not?

### The decisive fact

This repository has **no generic schema registry**. `schemas/registry.json` is
`PIPD-S0-CONTRACT-REGISTRY/1` — the registry of the **19 S0 contracts**. The MCP row is stage **S2**.
So there is nowhere for a new schema to be ratified, and the natural-looking extension (drop a
`schemas/MCPMaterializationDecision.schema.json` beside the other 20) would create a schema authority
**nobody designed**.

### Adjudication: decline ratification

Ratifying would have been the *subtler second fabrication*. In R9 I refused to **manufacture an object**
to move a counter — `EXISTS != TRUE`. Here the temptation was to **manufacture the authority** that
certifies an object: mint a canonical schema so the artefact stops being provisional. That is the same
act one level up, and it is refused for the same reason.

The record therefore keeps what was true about it and loses what was not:

| field | before | after |
|---|---|---|
| `schema` | invented id | `null` — asserts no schema authority |
| `claims_schema_authority` | (absent) | `false`, stated explicitly |
| `ratification_required` | `true` | `false` — **declined, not pending** |
| `record_kind` | `MATERIALIZATION_DECISION_RECORD` | `EVIDENCE_NOTE_NON_CANONICAL` |

It now names where MCP's state is **canonically** recorded — `TECHNOLOGY_ADMISSIONS.json` CAND-06 and
`CapabilityActivationLedger.json` — instead of competing with them.

**Low-friction rationale:** declining costs nothing and removes a class of future confusion. The
record's *content* (a truthful absence) was never in doubt; only its *pretension* was.

## Item 2 — crosswalk reclassification

### The method fact that decides the route

The crosswalk's statuses are **hard-coded literals in the generator**
(`tools/build_spec_del_crosswalk.py`, e.g. `L["030"] = dict(... status="EVIDENCE_GAP", ...)`), and
`docs/SPEC_DEL_CROSSWALK.json` is regenerated from them. **Editing the JSON would be overwritten.**
The reclassification therefore had to be made in the generator.

Also decisive: the generator marks a row `EVIDENCED` only when **object AND oracle both exist**, and it
*validates* that both resolve — "a pointer at a non-existent oracle path is an unproven claim, not
evidence". So an `EVIDENCED` flip is only legitimate with a **real, runnable** oracle.

### Adjudication and execution

| row | before | after | basis |
|---|---|---|---|
| `DEL-015` | `EVIDENCE_GAP` | **`EVIDENCED`** | object `.hgk/artifacts/s3/ADAPTER_REGISTRY.json` + oracle `tests/test_r10_bclass_evidence.py` (re-derives the registry hash from `ADAPTER_MAPPING` and asserts the counts) |
| `PIPD-SP-SPEC-030` | `EVIDENCE_GAP` | **`EVIDENCED`** | object = the absence record + the canonical admissions object; oracle = the same file (asserts `materialized: false`, `schema: null`, and that CAND-06 corroborates the absence) |
| `PIPD-SP-SPEC-002` | `EVIDENCE_GAP` (unexplained) | **`EVIDENCE_GAP` (adjudicated)** | `first_fail` now records the adjudication: the object is the **external** normative standard this repo implements, and an in-repo copy is the "competing lifecycle SSOT" the row forbids. `evidence_refs` points at this R10 adjudication. |

Measured effect: `status_summary` **EVIDENCED 42 → 44**, **EVIDENCE_GAP 11 → 9**; crosswalk `--check`
**OK (32 SPEC + 25 DEL, 0 violations)**; **DEL-018 unchanged at 0 violations**.

The oracle is **executed**, not asserted: 4 tests, `OK`. An oracle that had never been run would have
made the `EVIDENCED` flip itself an unproven claim.

## What this does NOT mean

- **`EVIDENCED` is not `PASS`.** It is the generator's own word for "object + oracle exist". Two rows
  now have truthful evidence; neither is thereby verified as *correct* engineering.
- `PIPD-SP-SPEC-002` is **not closed**. It is now a gap with a *reason*, still counted as a gap.
- The crosswalk `status_summary` (file `status` axis, 42 -> 44 / 11 -> 9 / 4) is a **different axis**
  from the R9 audit accounting (S4-active axis, 28 -> 30 / 10 -> 8 / 19), **not a contradiction**. R9
  reconciled the two explicitly (`SPEC_DEL_ACTIVE_GAPS_AUDIT.md` lines 26-52: 42 = 28 + 14, 11 = 10 + 1,
  4 = 4, 19 = 14 + 1 + 4, the separating row being `DEL-008`, deferred by stage). The arithmetic still
  holds after this round closed 2 of R9's 10 active rows (`DEL-015`, `PIPD-SP-SPEC-030`): 44 = 30 + 14,
  9 = 8 + 1, 4 = 4, 19 = 14 + 1 + 4. Quoting either figure still requires naming the axis.

### CORRECTION - a claim I made and should not have (found by the checker)

The first version of this FAR asserted that the two axes "do **not** reconcile" and that the difference
was "recorded, not smoothed over". **That was false.** R9 had already reconciled them, with the
arithmetic in writing, and an independent re-count confirmed it. The failure mode is worth naming: in
guarding against *smoothing a discrepancy over*, I *manufactured* one. Declaring something "unreconciled"
is itself an unchecked claim - the same class of error as asserting a PASS without running the check,
pointed the other way. The verification caught it; the FAR did not.
- `DEL-004` was **not** touched and remains an open external dependency.

## Refusals, stated plainly

1. **Refused**: ratifying a canonical schema for the MCP record.
2. **Refused**: creating `schemas/MCPMaterializationDecision.schema.json` and leaving the "registration
   problem" to be discovered later.
3. **Refused**: hand-editing `docs/SPEC_DEL_CROSSWALK.json` (it is generated; the edit would vanish).
4. **Refused**: flipping any row to `EVIDENCED` without a runnable oracle.

**Claim ceiling:** `TWO_OWNER_ITEMS_ADJUDICATED__MCP_SCHEMA_RATIFICATION_DECLINED__CROSSWALK_RECLASSIFIED_VIA_GENERATOR_WITH_EXECUTED_ORACLE`.
