# PIPD Canonical Core Objects

<!--PIPD-DOC-META
{
 "capability_loss": [
  {
   "capability": "runtime authority",
   "loss_id": "LOSS-WEB-01",
   "reason": "the Web pack is a read-only semantic surface; it executes nothing",
   "record_type": "CapabilityLoss",
   "severity": "DECLARED"
  }
 ],
 "denominator": true,
 "doc_id": "PIPD_CANONICAL_CORE",
 "kind": "WEB_DOC",
 "nack": [
  {
   "basis": "claim ceiling: DESIGN/FILE_PRESENT/SCHEMA_VALID only",
   "nack_id": "NACK-WEB-01",
   "record_type": "NACK",
   "statement": "this document carries contracts and provenance only; it has no runtime effect"
  },
  {
   "basis": "S5/S6 NOT_AUTHORISED",
   "nack_id": "NACK-WEB-02",
   "record_type": "NACK",
   "statement": "no live HGK/GENIE integration PASS is claimed; S5/S6 seams are fixture/mock only"
  }
 ],
 "schema": "PIPD-WEB-DOC/1",
 "schema_version": "1",
 "scope": [
  "dist/web/**"
 ],
 "source_hash": "92c311edf883527e573a2dd5c7942ae1279ccf2dc1ad77bab3ac8b5f25d8244c",
 "source_objects": [
  {
   "object_id": "REGISTRY:CONTRACT-FAMILIES",
   "schema": "PIPD-S0-CONTRACT-REGISTRY/1",
   "schema_version": "1",
   "source_hash": "85100a8e5ba6320f6648d33a14099fb999b2c452a94aff1652854d2550065e9d",
   "source_path": "schemas/registry.json"
  },
  {
   "object_id": "S0:ArtifactIdentity",
   "schema": "urn:pipd:s0:ArtifactIdentity:1",
   "schema_version": "1",
   "source_hash": "67d26f18d26307410bf0be5369949eb525d477e053ee3a7091e54b97f6d4ad4c",
   "source_path": "schemas/ArtifactIdentity.schema.json"
  },
  {
   "object_id": "S0:AuthorityBinding",
   "schema": "urn:pipd:s0:AuthorityBinding:1",
   "schema_version": "1",
   "source_hash": "66f1b3ce91d7f12ad6a6350a6628afd6c600e3e7ff62408b714c6fa0f1898ded",
   "source_path": "schemas/AuthorityBinding.schema.json"
  },
  {
   "object_id": "S0:RequirementAtom",
   "schema": "urn:pipd:s0:RequirementAtom:1",
   "schema_version": "1",
   "source_hash": "021f6a30cf178190281176138686447e492640cf97b125f9c21a0aa2fa31c684",
   "source_path": "schemas/RequirementAtom.schema.json"
  },
  {
   "object_id": "S0:ProfileBinding",
   "schema": "urn:pipd:s0:ProfileBinding:1",
   "schema_version": "1",
   "source_hash": "b559fb70bb6ceb9d491c989cb5ec031f44d15bcad5b40e75d6649aa059a93556",
   "source_path": "schemas/ProfileBinding.schema.json"
  },
  {
   "object_id": "S0:TechnologyAdmission",
   "schema": "urn:pipd:s0:TechnologyAdmission:1",
   "schema_version": "1",
   "source_hash": "40703552af4fb14c7aa87dd68ead6eac1cf7d272541fda273cf22b8fb109c4d6",
   "source_path": "schemas/TechnologyAdmission.schema.json"
  },
  {
   "object_id": "S0:PI-PKG",
   "schema": "urn:pipd:s0:PI-PKG:1",
   "schema_version": "1",
   "source_hash": "3e797d4eac04a04fee65add1ca6cb196154490ccd848b9b1cc561f24feaefb57",
   "source_path": "schemas/PI-PKG.schema.json"
  },
  {
   "object_id": "S0:PD-PKG",
   "schema": "urn:pipd:s0:PD-PKG:1",
   "schema_version": "1",
   "source_hash": "37291e8790e03839308a7c36125f9576d14da725a27480c9759ef5362d255541",
   "source_path": "schemas/PD-PKG.schema.json"
  },
  {
   "object_id": "S0:TraceLink",
   "schema": "urn:pipd:s0:TraceLink:1",
   "schema_version": "1",
   "source_hash": "ff6ef713b95a1a2812bd31d2b10cdcc064671c986d29d0e69318dc5a9f54e5e4",
   "source_path": "schemas/TraceLink.schema.json"
  },
  {
   "object_id": "S0:TaskSpecSeed",
   "schema": "urn:pipd:s0:TaskSpecSeed:1",
   "schema_version": "1",
   "source_hash": "c6e086aef0e4f21179cba52c5187c33a3873b18732c669c4d03bcad057e9b6cc",
   "source_path": "schemas/TaskSpecSeed.schema.json"
  },
  {
   "object_id": "S0:ConstructionContract",
   "schema": "urn:pipd:s0:ConstructionContract:1",
   "schema_version": "1",
   "source_hash": "1c56f15abd6e30d06f914f021b0b813f441689f9d47989ef48c7d7325557f0f2",
   "source_path": "schemas/ConstructionContract.schema.json"
  },
  {
   "object_id": "S0:WorkOrderCandidate",
   "schema": "urn:pipd:s0:WorkOrderCandidate:1",
   "schema_version": "1",
   "source_hash": "03a8692f183f106ec7e4739b925c980ba07d68551627ca6af315fa9f9e2caf54",
   "source_path": "schemas/WorkOrderCandidate.schema.json"
  },
  {
   "object_id": "S0:ECP",
   "schema": "urn:pipd:s0:ECP:1",
   "schema_version": "1",
   "source_hash": "7ecd9e92e6d43dba9675bb93ff0dddd178a0a17c8c3bc3f143696594dc945505",
   "source_path": "schemas/ECP.schema.json"
  },
  {
   "object_id": "S0:TQAEP",
   "schema": "urn:pipd:s0:TQAEP:1",
   "schema_version": "1",
   "source_hash": "d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd",
   "source_path": "schemas/TQAEP.schema.json"
  },
  {
   "object_id": "S0:ExecutionHandoff",
   "schema": "urn:pipd:s0:ExecutionHandoff:1",
   "schema_version": "1",
   "source_hash": "7fa36d3e7fe6e7416111b975381a42f3f5ad46cc81d97b610f317548815bd77b",
   "source_path": "schemas/ExecutionHandoff.schema.json"
  },
  {
   "object_id": "S0:EvidenceExpectation",
   "schema": "urn:pipd:s0:EvidenceExpectation:1",
   "schema_version": "1",
   "source_hash": "02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f",
   "source_path": "schemas/EvidenceExpectation.schema.json"
  },
  {
   "object_id": "S0:ClaimCeiling",
   "schema": "urn:pipd:s0:ClaimCeiling:1",
   "schema_version": "1",
   "source_hash": "dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85",
   "source_path": "schemas/ClaimCeiling.schema.json"
  },
  {
   "object_id": "S0:SurfaceProjectionManifest",
   "schema": "urn:pipd:s0:SurfaceProjectionManifest:1",
   "schema_version": "1",
   "source_hash": "87f8057e8dac68f304ed4e9c2dd118a26c69428015769ab09d39398d34dcb57d",
   "source_path": "schemas/SurfaceProjectionManifest.schema.json"
  },
  {
   "object_id": "S0:GENIEProjectionRef",
   "schema": "urn:pipd:s0:GENIEProjectionRef:1",
   "schema_version": "1",
   "source_hash": "22c88a0f9ec4ea4747967546f9a5ea7f19f0285be60ac42567fae2ca0b1c36ed",
   "source_path": "schemas/GENIEProjectionRef.schema.json"
  },
  {
   "object_id": "S0:ExecutionBindingRef",
   "schema": "urn:pipd:s0:ExecutionBindingRef:1",
   "schema_version": "1",
   "source_hash": "7c98cebfee30d9719cb8fd2d565c44120ce8d1be5b231071c19528cae1e95f50",
   "source_path": "schemas/ExecutionBindingRef.schema.json"
  }
 ]
}
-->

## Source Objects

| object_id | schema | schema_version | source_path | source_hash |
| --- | --- | --- | --- | --- |
| REGISTRY:CONTRACT-FAMILIES | PIPD-S0-CONTRACT-REGISTRY/1 | 1 | schemas/registry.json | 85100a8e5ba6320f6648d33a14099fb999b2c452a94aff1652854d2550065e9d |
| S0:ArtifactIdentity | urn:pipd:s0:ArtifactIdentity:1 | 1 | schemas/ArtifactIdentity.schema.json | 67d26f18d26307410bf0be5369949eb525d477e053ee3a7091e54b97f6d4ad4c |
| S0:AuthorityBinding | urn:pipd:s0:AuthorityBinding:1 | 1 | schemas/AuthorityBinding.schema.json | 66f1b3ce91d7f12ad6a6350a6628afd6c600e3e7ff62408b714c6fa0f1898ded |
| S0:RequirementAtom | urn:pipd:s0:RequirementAtom:1 | 1 | schemas/RequirementAtom.schema.json | 021f6a30cf178190281176138686447e492640cf97b125f9c21a0aa2fa31c684 |
| S0:ProfileBinding | urn:pipd:s0:ProfileBinding:1 | 1 | schemas/ProfileBinding.schema.json | b559fb70bb6ceb9d491c989cb5ec031f44d15bcad5b40e75d6649aa059a93556 |
| S0:TechnologyAdmission | urn:pipd:s0:TechnologyAdmission:1 | 1 | schemas/TechnologyAdmission.schema.json | 40703552af4fb14c7aa87dd68ead6eac1cf7d272541fda273cf22b8fb109c4d6 |
| S0:PI-PKG | urn:pipd:s0:PI-PKG:1 | 1 | schemas/PI-PKG.schema.json | 3e797d4eac04a04fee65add1ca6cb196154490ccd848b9b1cc561f24feaefb57 |
| S0:PD-PKG | urn:pipd:s0:PD-PKG:1 | 1 | schemas/PD-PKG.schema.json | 37291e8790e03839308a7c36125f9576d14da725a27480c9759ef5362d255541 |
| S0:TraceLink | urn:pipd:s0:TraceLink:1 | 1 | schemas/TraceLink.schema.json | ff6ef713b95a1a2812bd31d2b10cdcc064671c986d29d0e69318dc5a9f54e5e4 |
| S0:TaskSpecSeed | urn:pipd:s0:TaskSpecSeed:1 | 1 | schemas/TaskSpecSeed.schema.json | c6e086aef0e4f21179cba52c5187c33a3873b18732c669c4d03bcad057e9b6cc |
| S0:ConstructionContract | urn:pipd:s0:ConstructionContract:1 | 1 | schemas/ConstructionContract.schema.json | 1c56f15abd6e30d06f914f021b0b813f441689f9d47989ef48c7d7325557f0f2 |
| S0:WorkOrderCandidate | urn:pipd:s0:WorkOrderCandidate:1 | 1 | schemas/WorkOrderCandidate.schema.json | 03a8692f183f106ec7e4739b925c980ba07d68551627ca6af315fa9f9e2caf54 |
| S0:ECP | urn:pipd:s0:ECP:1 | 1 | schemas/ECP.schema.json | 7ecd9e92e6d43dba9675bb93ff0dddd178a0a17c8c3bc3f143696594dc945505 |
| S0:TQAEP | urn:pipd:s0:TQAEP:1 | 1 | schemas/TQAEP.schema.json | d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd |
| S0:ExecutionHandoff | urn:pipd:s0:ExecutionHandoff:1 | 1 | schemas/ExecutionHandoff.schema.json | 7fa36d3e7fe6e7416111b975381a42f3f5ad46cc81d97b610f317548815bd77b |
| S0:EvidenceExpectation | urn:pipd:s0:EvidenceExpectation:1 | 1 | schemas/EvidenceExpectation.schema.json | 02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f |
| S0:ClaimCeiling | urn:pipd:s0:ClaimCeiling:1 | 1 | schemas/ClaimCeiling.schema.json | dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85 |
| S0:SurfaceProjectionManifest | urn:pipd:s0:SurfaceProjectionManifest:1 | 1 | schemas/SurfaceProjectionManifest.schema.json | 87f8057e8dac68f304ed4e9c2dd118a26c69428015769ab09d39398d34dcb57d |
| S0:GENIEProjectionRef | urn:pipd:s0:GENIEProjectionRef:1 | 1 | schemas/GENIEProjectionRef.schema.json | 22c88a0f9ec4ea4747967546f9a5ea7f19f0285be60ac42567fae2ca0b1c36ed |
| S0:ExecutionBindingRef | urn:pipd:s0:ExecutionBindingRef:1 | 1 | schemas/ExecutionBindingRef.schema.json | 7c98cebfee30d9719cb8fd2d565c44120ce8d1be5b231071c19528cae1e95f50 |

## Capability Loss

| loss_id | record_type | capability | reason | severity |
| --- | --- | --- | --- | --- |
| LOSS-WEB-01 | CapabilityLoss | runtime authority | the Web pack is a read-only semantic surface; it executes nothing | DECLARED |

## NACK

| nack_id | record_type | statement | basis |
| --- | --- | --- | --- |
| NACK-WEB-01 | NACK | this document carries contracts and provenance only; it has no runtime effect | claim ceiling: DESIGN/FILE_PRESENT/SCHEMA_VALID only |
| NACK-WEB-02 | NACK | no live HGK/GENIE integration PASS is claimed; S5/S6 seams are fixture/mock only | S5/S6 NOT_AUTHORISED |

## Contract Families

| index | contract | owner | consumers | materialization | schema_file |
| --- | --- | --- | --- | --- | --- |
| 01 | ArtifactIdentity | PIPD | all planes | REQUIRED_NOW | schemas/ArtifactIdentity.schema.json |
| 02 | AuthorityBinding | PIPD | all compilers/adapters | REQUIRED_NOW | schemas/AuthorityBinding.schema.json |
| 03 | RequirementAtom | PIPD | PI compiler/TQAEP | REQUIRED_NOW | schemas/RequirementAtom.schema.json |
| 04 | ProfileBinding | PIPD | Skills/JIT/HGK | REQUIRED_NOW | schemas/ProfileBinding.schema.json |
| 05 | TechnologyAdmission | PIPD | tool/provider adapters | REQUIRED_NOW | schemas/TechnologyAdmission.schema.json |
| 06 | PI-PKG | PIPD | PD binder | REQUIRED_NOW | schemas/PI-PKG.schema.json |
| 07 | PD-PKG | PIPD | execution handoff | REQUIRED_NOW | schemas/PD-PKG.schema.json |
| 08 | TraceLink | PIPD/TQAEP | validators/checkers | REQUIRED_NOW | schemas/TraceLink.schema.json |
| 09 | TaskSpecSeed | PIPD | receiver adapter | REQUIRED_NOW | schemas/TaskSpecSeed.schema.json |
| 10 | ConstructionContract | PIPD | HGK adapter | REQUIRED_NOW | schemas/ConstructionContract.schema.json |
| 11 | WorkOrderCandidate | PIPD | HGK admission | REQUIRED_NOW_NONAUTHORITY | schemas/WorkOrderCandidate.schema.json |
| 12 | ECP | PIPD/ECP semantics | HGK/TQAEP | REQUIRED_NOW | schemas/ECP.schema.json |
| 13 | TQAEP | PIPD/TQAEP semantics | Independent checker/release | REQUIRED_NOW | schemas/TQAEP.schema.json |
| 14 | ExecutionHandoff | PIPD | HGK/other receiver | REQUIRED_NOW | schemas/ExecutionHandoff.schema.json |
| 15 | EvidenceExpectation | PIPD/TQAEP | HGK/CI/provider | REQUIRED_NOW | schemas/EvidenceExpectation.schema.json |
| 16 | ClaimCeiling | PIPD | all planes | REQUIRED_NOW | schemas/ClaimCeiling.schema.json |
| 17 | SurfaceProjectionManifest | PIPD | surface compiler | REQUIRED_NOW | schemas/SurfaceProjectionManifest.schema.json |
| 18 | GENIEProjectionRef | GENIE adapter | GENIE compiler | SCHEMA_SEAM_ONLY_UNTIL_S6 | schemas/GENIEProjectionRef.schema.json |
| 19 | ExecutionBindingRef | HGK adapter | HGK | SCHEMA_SEAM_ONLY_UNTIL_S5 | schemas/ExecutionBindingRef.schema.json |

## Required Fields — Registry Declaration

| contract | required_fields |
| --- | --- |
| ArtifactIdentity | subject_id, version, content_hash, schema_version, supersedes, invalidates |
| AuthorityBinding | source_id, authority_rank, locator, supersession, conflict_state, subject_id, version, content_hash, schema_version |
| RequirementAtom | req_id, source_clause, owner, acceptance_cue, risk_guard, subject_id, version, content_hash, schema_version |
| ProfileBinding | profile, axes, vetoes, artifact_depth, assurance, subject_id, version, content_hash, schema_version |
| TechnologyAdmission | capability_need, candidate, disposition, pin_license_currentness, fallback_exit, subject_id, version, content_hash, schema_version, technology_id, external_name, capability_slot, license, immutable_pin |
| PI-PKG | stable_semantic_contract, trace, acceptance, subject_id, version, content_hash, schema_version |
| PD-PKG | RepoContext, currentness, late_bound_construction_binding, subject_id, version, content_hash, schema_version |
| TraceLink | from_type, from_id, from_hash, to_type, to_id, to_hash, rationale, subject_id, version, content_hash, schema_version |
| TaskSpecSeed | goal, inputs, outputs, constraints, dependencies, tests, rollback, evidence, subject_id, version, content_hash, schema_version |
| ConstructionContract | subject, writable_scope, expected_changes, tests, rollback, evidence_expectations, subject_id, version, content_hash, schema_version |
| WorkOrderCandidate | candidate_only, subject_id, version, content_hash, schema_version |
| ECP | effect_intent, permission, retries, idempotency, readback, rollback, subject_id, version, content_hash, schema_version |
| TQAEP | tests, oracles, fixtures, acceptance, requalification, subject_id, version, content_hash, schema_version |
| ExecutionHandoff | receiver, abi_version, payload_refs, ack_nack_state, subject_id, version, content_hash, schema_version |
| EvidenceExpectation | expected_evidence_type, producer, postcondition, freshness, claim_effect, subject_id, version, content_hash, schema_version |
| ClaimCeiling | allowed_claims, forbidden_escalation, close_conditions, subject_id, version, content_hash, schema_version |
| SurfaceProjectionManifest | surface, source_hashes, generated_files, parity_loss, stale_rule, subject_id, version, content_hash, schema_version |
| GENIEProjectionRef | target_refs, subject_id, version, content_hash, schema_version |
| ExecutionBindingRef | receiver_binding_id, receiver_binding_version, receiver_binding_hash, lease, state, subject_id, version, content_hash, schema_version |

## Required Fields — Schema Declaration

| object_id | schema_id | schema_draft | required_fields |
| --- | --- | --- | --- |
| S0:ArtifactIdentity | urn:pipd:s0:ArtifactIdentity:1 | https://json-schema.org/draft/2020-12/schema | subject_id, version, content_hash, schema_version, supersedes, invalidates |
| S0:AuthorityBinding | urn:pipd:s0:AuthorityBinding:1 | https://json-schema.org/draft/2020-12/schema | source_id, authority_rank, locator, supersession, conflict_state, subject_id, version, content_hash, schema_version |
| S0:RequirementAtom | urn:pipd:s0:RequirementAtom:1 | https://json-schema.org/draft/2020-12/schema | req_id, source_clause, owner, acceptance_cue, risk_guard, subject_id, version, content_hash, schema_version |
| S0:ProfileBinding | urn:pipd:s0:ProfileBinding:1 | https://json-schema.org/draft/2020-12/schema | profile, axes, vetoes, artifact_depth, assurance, subject_id, version, content_hash, schema_version |
| S0:TechnologyAdmission | urn:pipd:s0:TechnologyAdmission:1 | https://json-schema.org/draft/2020-12/schema | capability_need, candidate, disposition, pin_license_currentness, fallback_exit, subject_id, version, content_hash, schema_version, technology_id, external_name, capability_slot, license, immutable_pin |
| S0:PI-PKG | urn:pipd:s0:PI-PKG:1 | https://json-schema.org/draft/2020-12/schema | stable_semantic_contract, trace, acceptance, subject_id, version, content_hash, schema_version |
| S0:PD-PKG | urn:pipd:s0:PD-PKG:1 | https://json-schema.org/draft/2020-12/schema | RepoContext, currentness, late_bound_construction_binding, subject_id, version, content_hash, schema_version |
| S0:TraceLink | urn:pipd:s0:TraceLink:1 | https://json-schema.org/draft/2020-12/schema | from_type, from_id, from_hash, to_type, to_id, to_hash, rationale, subject_id, version, content_hash, schema_version |
| S0:TaskSpecSeed | urn:pipd:s0:TaskSpecSeed:1 | https://json-schema.org/draft/2020-12/schema | goal, inputs, outputs, constraints, dependencies, tests, rollback, evidence, subject_id, version, content_hash, schema_version |
| S0:ConstructionContract | urn:pipd:s0:ConstructionContract:1 | https://json-schema.org/draft/2020-12/schema | subject, writable_scope, expected_changes, tests, rollback, evidence_expectations, subject_id, version, content_hash, schema_version |
| S0:WorkOrderCandidate | urn:pipd:s0:WorkOrderCandidate:1 | https://json-schema.org/draft/2020-12/schema | candidate_only, subject_id, version, content_hash, schema_version |
| S0:ECP | urn:pipd:s0:ECP:1 | https://json-schema.org/draft/2020-12/schema | effect_intent, permission, retries, idempotency, readback, rollback, subject_id, version, content_hash, schema_version |
| S0:TQAEP | urn:pipd:s0:TQAEP:1 | https://json-schema.org/draft/2020-12/schema | tests, oracles, fixtures, acceptance, requalification, subject_id, version, content_hash, schema_version |
| S0:ExecutionHandoff | urn:pipd:s0:ExecutionHandoff:1 | https://json-schema.org/draft/2020-12/schema | receiver, abi_version, payload_refs, ack_nack_state, subject_id, version, content_hash, schema_version |
| S0:EvidenceExpectation | urn:pipd:s0:EvidenceExpectation:1 | https://json-schema.org/draft/2020-12/schema | expected_evidence_type, producer, postcondition, freshness, claim_effect, subject_id, version, content_hash, schema_version |
| S0:ClaimCeiling | urn:pipd:s0:ClaimCeiling:1 | https://json-schema.org/draft/2020-12/schema | allowed_claims, forbidden_escalation, close_conditions, subject_id, version, content_hash, schema_version |
| S0:SurfaceProjectionManifest | urn:pipd:s0:SurfaceProjectionManifest:1 | https://json-schema.org/draft/2020-12/schema | surface, source_hashes, generated_files, parity_loss, stale_rule, subject_id, version, content_hash, schema_version |
| S0:GENIEProjectionRef | urn:pipd:s0:GENIEProjectionRef:1 | https://json-schema.org/draft/2020-12/schema | target_refs, subject_id, version, content_hash, schema_version |
| S0:ExecutionBindingRef | urn:pipd:s0:ExecutionBindingRef:1 | https://json-schema.org/draft/2020-12/schema | receiver_binding_id, receiver_binding_version, receiver_binding_hash, lease, state, subject_id, version, content_hash, schema_version |
