# Design — R3 audit repair

## Context
The audit is a user-supplied defect list. Per its §0.1 it ranks above the project's own r2 design
documents but never replaces `system/developer` instructions or the upper specification. It is
therefore compiled into C0–C9 as family `F0_USER_AUDIT_REPAIR` (rank R0, NORMATIVE) while the
existing corpus keeps its own ranks.

## Decisions
1. **ChangeSet class `NARROW_REPAIR`.** Several dependent components move together (schemas,
   requirement compiler, skills, projections, evidence), but nothing outside the audited S0–S4 scope
   is opened and no architecture is reset.
2. **One requirement → one taskspec → one workorder per FW, plus one per R-AUD finding.** This expands
   the denominator instead of hiding the repair in a "next wave": 15 R-AUD + 12 FW obligations are
   each individually traceable.
3. **Typed projection IR.** Web and Host surfaces are compiled from canonical objects + profile +
   adapter mapping, so "empty payload" and "marker stub" stop being producible.
4. **Evidence manifest** uses canonical self-exclusion plus an outer immutable seal; a manifest that
   contains its own hash entry is not evidence.
5. **PRE-W3 stays `TEMP_CLOSED`.** Its evidence gap is routed to its own authorised owner and is never
   counted as S0–S4 PASS.
6. **No gate denominator changes.** Detectors gain refusal paths (stub, wrong set, extra registry
   field, semantic collapse); they never lose them so a test can pass.

## Risks
- Shared worktree: the admitted WorkOrders all target the PIPD root, so lane writes must stay inside
  their declared WriteSet; conflicts are reported rather than silently merged.
- Historical AO PASS verdicts must not be inherited across candidates: any candidate change
  invalidates the affected edges and requires a fresh independent check.
