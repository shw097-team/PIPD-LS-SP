# Design

## Context

The 2026-10-27 round executed two things for real and hit one wall:

- the **13-verb PIPD toolchain** (`init → intake → profile → compile-pi → bind-pd → compile-ecp →
  compile-tqaep → validate → doctor → project → export → diff → repair`) produced PI/PD/ECP that
  `validate` accepted with zero findings;
- the **native harness** (`b1run.py`) executed 244 declared cases through
  `READY → CAS lease → executor → effect readback`, with an append-only fsynced journal, at-most-once
  replay refusal, UNKNOWN_EFFECT reconcile, and pre-spawn refusal of revoked/foreign/expired tokens.

What it could not do is *name an executor per domain*, because the host has no
`runner-registry.json`. That is the whole difference between "I executed this in my own harness" and
"the host executed this through its own registered runner".

## Goals / Non-Goals

**Goals.** Make the missing admission surfaces explicit and machine-checkable, so a route's state is a
function of evidence rather than of who is asking. Keep every existing refusal: partial registration
must not promote a route.

**Non-Goals.** Not weakening G-A's six-item conjunction, not accepting a maker receipt as an
independent check, not letting the projection write canonical, not collapsing the three GWO domains'
receipts into one generic success.

## Decisions

1. **Registry is the only promotion authority.** `DISCOVERED → INSTALLED → LOADABLE → INVOKED` is a
   ladder, and a route climbs it only with a complete registry entry plus a real invocation receipt.
   Nine fields are required because `executable_sha256` without `owner_signature` is a claim, and
   `owner_signature` without `read_scope`/`permission_scope` is a licence to overreach.

2. **Issuer, queue and effect receipts stay distinct.** The B1 harness already emits
   `RAW-HGK-ISSUER`, `RAW-HGK-QUEUE` and `RAW-HGK-EFFECT` separately for GWO-HGK; a queue lease
   generation is not an effect and must never be quoted as one.

3. **Checker separation is about write access, not model identity.** A different model in the same
   orchestration with the same writable tree is still the maker. The proposal therefore requires a
   distinct credential and a read-only ACL, and records the author-side receipt with an explicit
   `..._NOT_INDEPENDENT` ceiling in the meantime.

4. **At-most-once is journal-scoped and durable.** Replay is refused by reading the journal, so the
   journal must be fsynced per event; the harness does this and the tests assert both the refusal and
   the effect being byte-identical afterwards.

## Risks / Trade-offs

- **Partial registration creep** — mitigated by the typed refusal in 1.5.
- **Receipt borrowing** — mitigated by keeping the three GWO receipt families separate and by
  requiring the same `subject_sha` across them.
- **Silent staleness** — a registry entry whose `executable_sha256` no longer matches the binary must
  fail closed; the harness's `readback()` pattern (hash what landed, never trust the caller) is the
  model for that check.

## Migration Plan

1. Owner signs `runner-registry.json` for the domains that exist today.
2. Re-run the binding probe; expect `BLOCKED → INSTALLED` only where all nine fields resolve.
3. Bind issuer + queue; re-run GWO-HGK against the real lane.
4. Provision the checker principal; re-run G-A6.
5. Only then can a round claim `EXECUTION_ADMITTED` or `INDEPENDENT_PASS`.

## Open Questions

- Which OS session primitive satisfies "different session" for G-B on Windows (new logon session vs
  separate Scheduled Task identity)? Both must be proven with a real PID/session readback, not a name.
- Whether `permission_scope` should be expressed as an ACL diff or a capability token, given the
  existing `UserEffectBoundaryContract` vocabulary.
