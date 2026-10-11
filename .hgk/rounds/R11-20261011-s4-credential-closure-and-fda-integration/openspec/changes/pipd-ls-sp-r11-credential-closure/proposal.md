# proposal - pipd-ls-sp-r11-credential-closure

## Why

R10 ended with three honest gaps:

1. a credential broker whose read and write paths were each exercised end to end in R10 (the write by a
   push that moved a ref; the writer **corroborated, not proven** - see the R11 FAR), and which is
   referenced **zero times** by the control
   plane's `config/` - a working capability nothing calls;
2. two owner-only credential operations never performed: a redundant personal-account GitHub App still
   holding a live key pair, and a long-lived PAT the broker no longer needs;
3. the round's use of desktop automation recorded only in a product round's FAR files, not integrated into
   the automation capability's OWN discipline and evidence surface in the Fabric repository.

## What changes

- `desktop-automation` (REQ-PIPD-R11-FDAEXEC-001): the two remaining operations are executed by driving the
  browser, each confirmed by READBACK from the provider.
- `evidence-integration` (REQ-PIPD-R11-FDAEVID-002): this round's automation use is written into a discipline
  + evidence artefact conforming to the automation team's own evidence contract, stored in that team's
  evidence folder, and the Fabric repository is updated with **only** the paths this round authored.
- `control-plane` (REQ-PIPD-R11-ACTIVATE-003): the broker is either activated, or the reason activation is
  its own round is recorded as the deliverable.

## Governance

Admitted through the typed SharedSpine / ProjectLifecycleController API (no raw SQL): six obligations,
FROZEN, zero errors, project left in EXECUTING. KANBAN / SWARM / GSTACK / OPENSPEC artefacts are written to
disk. The maker does not sign the verdict.

## Out of scope

`FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`, release signing and builder
attestation remain external-acceptor items and are not claimed here.
