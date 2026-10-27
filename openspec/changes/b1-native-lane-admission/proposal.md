## Why

The B1 PIPD-LS-PKG round (2026-10-27) executed the 13-verb PIPD toolchain and a real
`READY → CAS lease → executor → effect readback` harness, but **30/30 runner routes stayed
`BLOCKED_MISSING_RUNNER_OR_BINDING`** and G-A item 6 (independent checker) could not be met. The
cause is structural, not a defect in the nine documents:

1. There is no **owner-registered runner registry**: no host surface maps `OWNER_REGISTERED::<domain>`
   to an executable with an ABI version, schema id, sha256 and owner signature. Without it a route can
   only be `DISCOVERED`, never `INSTALLED` or `LOADABLE`, so an executor cannot be named per domain.
2. There is no **native Issuer**: nothing on this host can sign a `WorkOrder` with a Principal /
   Scope / Nonce / TTL binding, so `RAW-HGK-ISSUER` cannot exist and G-B's successor step has no
   trigger.
3. There is no **independent checker principal**: a maker (or a same-model subagent in the same
   orchestration) cannot self-attest independence, so G-A6 and any `INDEPENDENT_PASS` claim stay
   `NOT_RUN` forever regardless of effort.

This proposal does not ask to weaken those requirements. It records the smallest set of host-surface
additions that would let the existing evidence ladder advance, so the next round does not re-derive
the same conclusion.

## What Changes

- **Runner registry contract (nine fields).** A versioned `runner-registry.json` keyed by
  `OWNER_REGISTERED::<domain>` carrying `runner_id`, `abi_version`, `schema_id`, `executable_path`,
  `executable_sha256`, `allowed_os`, `read_scope`, `permission_scope`, `owner_signature`. A route
  without all nine fields MUST stay `BLOCKED_MISSING_RUNNER_OR_BINDING` — partial registration is a
  typed refusal, not a promotion.
- **Issuer binding.** A `policy_epoch` + issuer principal that can bind Principal/Scope/Nonce/TTL to a
  single subject, emitting `RAW-HGK-ISSUER` distinct from queue and effect raws.
- **Checker lane separation.** A checker principal with a read-only ACL and its own credential, whose
  verdict is written outside the maker's writable surface. The maker's own receipt remains a
  `AUTHOR_SIDE_CHECKER_RECEIPT_NOT_INDEPENDENT` record and never counts as `INDEPENDENT_PASS`.
- **G-B successor trigger.** A durable-journal-driven successor start in a *different* OS session/PID
  after the external helper credential is revoked; a same-session replay is explicitly not accepted.

## Impact

- Affected specs: `native-lane-admission` (new), `runner-registry` (new).
- Affected code: none in this change — it is a host-surface contract plus the admission rules that
  read it. The B1 harness (`var/B1-PIPD-PKG-20261027/b1run.py`) already implements the protocol side
  and would consume the registry once it exists.
- Not affected: PIPD's 13 verbs, the nine B1 documents, `claim_ceiling` semantics.
