# PIPD-LS-SP S0 Canonical Machine Contract Spec — exact 19/19

Source (NORMATIVE): `PIPD-LS-SP_藍圖.md` §7.3 "Canonical Machine Contracts — exact 19/19"
(sha256 6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a for the
canonical standard; the blueprint file digest is recorded in the source manifest).

Bootstrap order (`.pipd` §5.6.1): 01 standard lock, 02 project manifest, 03 schemas/registry,
04 package index, 05 PI/PD objects, 06 policies/currentness/execution contracts,
07 evidence expectations/conformance, 08 surface/GENIE/execution binding refs.

## Deliverable

Create exactly 19 JSON Schema files under `schemas/`, named `<Contract>.schema.json`,
each Draft 2020-12 (`"$schema": "https://json-schema.org/draft/2020-12/schema"`),
`type: object`, `additionalProperties: false`, with `required` covering **exactly** the
required-field list below plus the four universal identity fields
(`subject_id`, `version`, `content_hash`, `schema_version`) where the row does not already
name them. Each schema must carry `"$id": "urn:pipd:s0:<Contract>:1"` and a
`description` naming the Owner and Consumer from the table.

Also write `schemas/registry.json`:

```json
{"schema": "PIPD-S0-CONTRACT-REGISTRY/1",
 "families": [{"index": "01", "contract": "ArtifactIdentity", "materialization": "REQUIRED_NOW",
               "owner": "PIPD", "consumers": ["all planes"],
               "required_fields": ["subject_id","version","content_hash","schema_version","supersedes","invalidates"],
               "schema_file": "schemas/ArtifactIdentity.schema.json"}, ... all 19 ...]}
```

## The 19 families (exact)

| # | Contract | Materialization | Owner | Consumer | Required fields / invariant |
| --- | --- | --- | --- | --- | --- |
| 01 | ArtifactIdentity | REQUIRED_NOW | PIPD | all planes | subject_id, version, content_hash, schema_version, supersedes, invalidates |
| 02 | AuthorityBinding | REQUIRED_NOW | PIPD | all compilers/adapters | source_id, authority_rank, locator, supersession, conflict_state |
| 03 | RequirementAtom | REQUIRED_NOW | PIPD | PI compiler/TQAEP | req_id, source_clause, owner, acceptance_cue, risk_guard |
| 04 | ProfileBinding | REQUIRED_NOW | PIPD | Skills/JIT/HGK | profile, axes, vetoes, artifact_depth, assurance |
| 05 | TechnologyAdmission | REQUIRED_NOW | PIPD | tool/provider adapters | capability_need, candidate, disposition, pin_license_currentness, fallback_exit |
| 06 | PI-PKG | REQUIRED_NOW | PIPD | PD binder | stable semantic contract, trace, acceptance |
| 07 | PD-PKG | REQUIRED_NOW | PIPD | execution handoff | RepoContext, currentness, late_bound_construction_binding |
| 08 | TraceLink | REQUIRED_NOW | PIPD/TQAEP | validators/checkers | from_type, from_id, from_hash, to_type, to_id, to_hash, rationale |
| 09 | TaskSpecSeed | REQUIRED_NOW | PIPD | receiver adapter | goal, inputs, outputs, constraints, dependencies, tests, rollback, evidence |
| 10 | ConstructionContract | REQUIRED_NOW | PIPD | HGK adapter | subject, writable_scope, expected_changes, tests, rollback, evidence_expectations |
| 11 | WorkOrderCandidate | REQUIRED_NOW_NONAUTHORITY | PIPD | HGK admission | candidate_only marker, never runtime authority |
| 12 | ECP | REQUIRED_NOW | PIPD/ECP semantics | HGK/TQAEP | effect_intent, permission, retries, idempotency, readback, rollback |
| 13 | TQAEP | REQUIRED_NOW | PIPD/TQAEP semantics | Independent checker/release | tests, oracles, fixtures, acceptance, requalification |
| 14 | ExecutionHandoff | REQUIRED_NOW | PIPD | HGK/other receiver | receiver, abi_version, payload_refs, ack_nack_state |
| 15 | EvidenceExpectation | REQUIRED_NOW | PIPD/TQAEP | HGK/CI/provider | expected_evidence_type, producer, postcondition, freshness, claim_effect |
| 16 | ClaimCeiling | REQUIRED_NOW | PIPD | all planes | allowed_claims, forbidden_escalation, close_conditions |
| 17 | SurfaceProjectionManifest | REQUIRED_NOW | PIPD | surface compiler | surface, source_hashes, generated_files, parity_loss, stale_rule |
| 18 | GENIEProjectionRef | SCHEMA_SEAM_ONLY_UNTIL_S6 | GENIE adapter | GENIE compiler | target refs ProductGraph/Profile/Bundle/GENIEArtifact; no truth writeback |
| 19 | ExecutionBindingRef | SCHEMA_SEAM_ONLY_UNTIL_S5 | HGK adapter | HGK | receiver binding id/version/hash/lease/state; ACK only after HGK admission |

## Hard invariants

- Every schema filename must exactly equal `<Contract>.schema.json` with `PI-PKG` → `PI-PKG.schema.json` and `PD-PKG` → `PD-PKG.schema.json`.
- `registry.json` must list all 19 in index order 01..19 and must agree byte-for-byte with the schema files on `required_fields`.
- Do not invent a 20th family, do not rename a family, do not reorder.
- Do not write anything outside `schemas/`.
