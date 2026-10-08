# PIPD-LS-SP S0/S1 — canonical contracts + LITE vertical slice

## Why
The PIPD-LS-SP product root is empty (NEW_IMPLEMENTATION). The governed round must
materialize the frozen design: 19/19 canonical machine-contract families (S0) and one
real LITE intent->PI->PD->ECP/TQAEP vertical slice plus the 13-command compiler surface (S1/S4).

## What changes
- `schemas/`: exactly the 19 families of `PIPD-LS-SP_藍圖.md` §7.3 with a registry.
- `src/pipd_ls_sp/`: deterministic pipeline, validators, profile trio, workspace ops, 13-command CLI.
- `tests/`: positive, negative, security and rollback tests.
- `dist/web/`: 5-file web pack + 3 host projections.

## Impact
Affected specs: pipd-s0-contracts, pipd-s1-lite-slice, pipd-cli-surface.
No change to HG-KSEOS or Fabric control code.
