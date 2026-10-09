# PIPD-LS-SP S0–S4 — destructive-audit repair (R-AUD-001…015 / FW-01…12)

## Why
The 2026-10-09 external destructive audit (`PIPD_LS_SP_S0_S4_FULL_DESTRUCTIVE_ACCEPTANCE_AUDIT_2026-10-09.md`,
fixed baseline `829c17e87855cd7a1c88bfad1f51f1fdd1fafa5e`) returned `FAIL` for S0/S1/S3 with
confirmed hard blockers, and `TEMP_CLOSED` for the separate PRE-W3 cross-project subject. The
existing S0–S4 artefacts are candidate evidence only: a file being present, non-empty or
schema-valid was accepted as runtime readiness in several gates.

## What changes
- `schemas/`: reconcile `TechnologyAdmission` (registry `required_fields` 9 vs schema `required` 14,
  `$id` version 2 vs the S0 contract's v1 rule) and re-prove all 19 families field-exact.
- `src/pipd_ls_sp/`: replace the five-axis keyword classifier with a clause-bound atomic requirement
  compiler; make `bind_pd` read the real RepoContext/currentness instead of trusting the caller;
  replace hardcoded surface payloads with a typed projection IR.
- `skills/pipd-*/`: materialise the 8 logical SkillContracts (SKILL.md, references/contract.md,
  references/examples.md, schemas/input+output, tests/cases.yaml).
- `dist/web/`: emit the exact five PIPD semantic documents (`PIPD_BOOTSTRAP.md`,
  `PIPD_CANONICAL_CORE.md`, `PIPD_ROUTER_PROFILES.md`, `PIPD_ARTIFACT_SCHEMAS.md`,
  `PIPD_EVAL_HANDOFF.md`) plus three real host adapters; site UI files move to `OPTIONAL_SITE_UI`.
- `tools/`: real effective-load oracles, manifest sealing with canonical self-exclusion, and
  detectors that reject stubs, wrong sets, extra registry fields and semantic collapse.
- `.hgk/`: frozen candidate tuple, TT dispositions, knowledge quarantine per-source disposition and
  a single-file external acceptance evidence MD.

## Non-goals
No S5+ execution, no PRE-W3 promotion (stays `TEMP_CLOSED`), no second control plane, no Fabric
sealed-control edit, no production/release/publication claim.

## Impact
Affected specs: pipd-s0-contracts, pipd-s1-skills, pipd-s3-surfaces, pipd-s4-cli, pipd-evidence.
No change to HG-KSEOS or Fabric control code. Product writes stay inside the PIPD target root under
admitted WorkOrders `WO-TS-req-pipd-r3-fw-01…12` / `WO-TS-req-pipd-r3-aud-001…015`.
