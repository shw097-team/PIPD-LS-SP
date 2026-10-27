# Tasks

> Status legend: `[x]` = done and re-verified by re-running the named command. `[~]` = done as far as
> this host allows, with the residue named. `[ ]` = not done (blocked on an Owner action).
>
> Denominator: the three structural gaps observed in the 2026-10-27 B1 round
> (`artifacts/GATES.json`, `artifacts/HOST_BINDINGS.json` route_binding 30/30 BLOCKED).

## 1. Runner registry (`runner-registry`)

- [x] 1.1 Record why every route is blocked, per route, in machine-readable form
      (`artifacts/HOST_BINDINGS.json` route_binding: 30/30 `BLOCKED_MISSING_RUNNER_OR_BINDING`,
      reason `hgk.runner_registry=NOT_FOUND`).
- [x] 1.2 Prove the protocol side works without a registry, so the only missing piece is admission:
      `python run_native.py` → 244/244 declared cases + 4/4 protocol probes
      (`artifacts/NATIVE_HARNESS_SUMMARY.json`).
- [ ] 1.3 Author `runner-registry.json` with all nine fields per domain and an owner signature.
      **Blocked on Owner signing** — no agent may self-sign a runner.
- [ ] 1.4 Re-run the 30-route binding probe and require every route to reach at least `INSTALLED`
      before any `EXECUTION_ADMITTED` claim.
- [ ] 1.5 Negative: a registry entry missing any of the nine fields must produce a typed refusal and
      leave the route `BLOCKED_*`, never a silent promotion.

## 2. Issuer (`native-lane-admission`)

- [x] 2.1 Demonstrate the issuer-side negatives are real: forged nonce, stale nonce, expired TTL each
      refused with zero delta (`artifacts/GWO_E2E.json` → `GWO-HGK.negatives`).
- [ ] 2.2 Bind a real issuer principal + `policy_epoch` that can emit `RAW-HGK-ISSUER` distinct from
      queue and effect raws. **Blocked on Owner binding a principal.**
- [ ] 2.3 Bind the Hermes durable queue so `RAW-HGK-QUEUE` carries a real lease generation and cursor.

## 3. Checker separation

- [x] 3.1 Record the maker-side checker receipt with an explicit non-independence ceiling
      (`AUTHOR_SIDE_CHECKER_RECEIPT_NOT_INDEPENDENT`), so it can never be quoted as `INDEPENDENT_PASS`.
- [ ] 3.2 Provision a checker principal with a read-only ACL and a distinct credential; its verdict
      must land outside the maker's writable tree.
- [ ] 3.3 Re-run G-A6 and require a checker receipt bound to the same subject sha before any
      `INDEPENDENT_PASS` claim.

## 5. ECP@1 expressiveness (`ecp-effect-class`)

- [x] 5.1 Add `effect_class` (enum: `READ_ONLY_PROBE` / `REPOSITORY_WRITE` / `HOST_OPERATIONS` /
      `USER_DATA_EFFECT`) to the ECP contract so DOC-02's per-slot classification is auditable from
      the artifact instead of only from the projection.
      **Blocked on an Owner-sanctioned schema change** — measured gap: `checker_receipt.json` C4.
      **LANDED 2026-10-27 (owner-authorized FAR S1, PIPD commit 38e363b)**: canonical
      `schemas/ECP.schema.json` declares `effect_class` and canonical `pipeline.compile_ecp` emits it
      (`REPOSITORY_WRITE` with a distribution map). Deliberate deviation from this task's wording:
      the field is `{"type":"string"}` plus `x-s0-vocabulary.status=CANDIDATE_VOCABULARY_PENDING_OWNER`,
      NOT an enum — the four value names have 0 hits in SBL KB DOC-00..13 (they come from the delivered
      book set), so freezing them would enshrine an unratified vocabulary. Recheck: checker round 7,
      11/11 PASS, bound to the post-landing bytes.
- [x] 5.2 Add a per-attempt `nonce` and an `issuer`/`subject` binding to ECP so
      `idempotency.guarantee=at_most_once` is enforceable rather than asserted; `retries.max=1` with
      `backoff=none` must be refused unless a nonce is present. Measured gap: C5/C6.
      **LANDED 2026-10-27 (S1)**: canonical ECP emits `nonce{value,strategy=one_time,ttl_s,binding}`,
      `retries.requires_nonce=true`, `idempotency.dedupe_scope=operation_id`. The `issuer`/`subject`
      binding is declared in schema but NOT exercised end-to-end: this host has no native Issuer
      (admission/S3 built a demo-key issuer; same OS user, so it does not discharge this clause).
- [x] 5.3 Record a byte-level digest alongside `content_hash` so provenance stripping is detectable
      (C11). Author-side interim: `pipd-run/artifacts/provenance.json` already carries `file_sha256`.
      **LANDED 2026-10-27 (S1)**: `replay{iterations:2, identity_equal:true}` is sealed body content in
      canonical PI and ECP (C9); `provenance.json` carries `file_sha256` (C11). Round-7 receipt records
      `subject_sha256 == subject_sha256_end`, i.e. the subject was stable across the check.
- [x] 5.4 Make `bind-pd` probe-verify `writable_scope` instead of host-matching it (C8), or mark
      `RepoContext.readiness` as degraded when any caller claim is unverified.
      **LANDED 2026-10-27 (S1)**: canonical `bind_pd` runs `stat + W_OK` and records
      `late_bound_construction_binding.writable_scope_probe`; `verified=true` only on PASS (8/8 slots).


## 4. G-B successor

- [x] 4.1 Prove a revoked credential is refused before spawn with zero effect
      (`NATIVE_HARNESS_SUMMARY.json` → `P4_revoked_replay`).
- [x] 4.2 Prove an UNKNOWN_EFFECT window reconciles from world state without replay
      (`P2_crash_reconcile`, `replayed: false`).
- [ ] 4.3 Start the successor from the durable journal in a different OS PID/session after revocation.
      **Blocked on 2.2 + 2.3**; a same-session replay does not satisfy G-B.
