# PIPD Evaluation Handoff

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
 "doc_id": "PIPD_EVAL_HANDOFF",
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
 "source_hash": "a6c9b737e756d891ef0c73b7faa65bdaf6e7b1c20499d3e59868ae6ec83865ca",
 "source_objects": [
  {
   "object_id": "SEAM:S5",
   "schema": "PIPD-SEAM-COMPAT/1",
   "schema_version": "1",
   "source_hash": "5aa6aa3e4f360ab6e898e5034ec3871e731ec48137ae8af50fc2138871faf3ec",
   "source_path": "fixtures/s5_s8/s5_compat.json"
  },
  {
   "object_id": "SEAM:S6",
   "schema": "PIPD-SEAM-COMPAT/1",
   "schema_version": "1",
   "source_hash": "a2541b4b73f054d5557dcaeaca1544a3665fb9e5ddcd7264be383b59c4c39b37",
   "source_path": "fixtures/s5_s8/s6_compat.json"
  },
  {
   "object_id": "SEAM:S7",
   "schema": "PIPD-SEAM-COMPAT/1",
   "schema_version": "1",
   "source_hash": "185c160092e751e66c075222326378124e7c55f569d725fb64392cebb224b515",
   "source_path": "fixtures/s5_s8/s7_compat.json"
  },
  {
   "object_id": "SEAM:S8",
   "schema": "PIPD-SEAM-COMPAT/1",
   "schema_version": "1",
   "source_hash": "53492fe85d88aff6e837572ba90d5b3ccba0fccd6d11375928f307fb072a2ffe",
   "source_path": "fixtures/s5_s8/s8_compat.json"
  },
  {
   "object_id": "ADAPTER:MAPPING",
   "schema": "PIPD-ADAPTER-MAPPING/1",
   "schema_version": "1",
   "source_hash": "ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab",
   "source_path": "src/pipd_ls_sp/projection.py#ADAPTER_MAPPING"
  },
  {
   "object_id": "PROFILE:TRIO",
   "schema": "PIPD-PROFILE-TRIO/1",
   "schema_version": "1",
   "source_hash": "2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070",
   "source_path": "src/pipd_ls_sp/profiles.py"
  },
  {
   "object_id": "S0:ClaimCeiling",
   "schema": "urn:pipd:s0:ClaimCeiling:1",
   "schema_version": "1",
   "source_hash": "dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85",
   "source_path": "schemas/ClaimCeiling.schema.json"
  },
  {
   "object_id": "S0:TQAEP",
   "schema": "urn:pipd:s0:TQAEP:1",
   "schema_version": "1",
   "source_hash": "d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd",
   "source_path": "schemas/TQAEP.schema.json"
  },
  {
   "object_id": "S0:EvidenceExpectation",
   "schema": "urn:pipd:s0:EvidenceExpectation:1",
   "schema_version": "1",
   "source_hash": "02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f",
   "source_path": "schemas/EvidenceExpectation.schema.json"
  }
 ]
}
-->

## Source Objects

| object_id | schema | schema_version | source_path | source_hash |
| --- | --- | --- | --- | --- |
| SEAM:S5 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s5_compat.json | 5aa6aa3e4f360ab6e898e5034ec3871e731ec48137ae8af50fc2138871faf3ec |
| SEAM:S6 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s6_compat.json | a2541b4b73f054d5557dcaeaca1544a3665fb9e5ddcd7264be383b59c4c39b37 |
| SEAM:S7 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s7_compat.json | 185c160092e751e66c075222326378124e7c55f569d725fb64392cebb224b515 |
| SEAM:S8 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s8_compat.json | 53492fe85d88aff6e837572ba90d5b3ccba0fccd6d11375928f307fb072a2ffe |
| ADAPTER:MAPPING | PIPD-ADAPTER-MAPPING/1 | 1 | src/pipd_ls_sp/projection.py#ADAPTER_MAPPING | ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab |
| PROFILE:TRIO | PIPD-PROFILE-TRIO/1 | 1 | src/pipd_ls_sp/profiles.py | 2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070 |
| S0:ClaimCeiling | urn:pipd:s0:ClaimCeiling:1 | 1 | schemas/ClaimCeiling.schema.json | dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85 |
| S0:TQAEP | urn:pipd:s0:TQAEP:1 | 1 | schemas/TQAEP.schema.json | d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd |
| S0:EvidenceExpectation | urn:pipd:s0:EvidenceExpectation:1 | 1 | schemas/EvidenceExpectation.schema.json | 02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f |

## Capability Loss

| loss_id | record_type | capability | reason | severity |
| --- | --- | --- | --- | --- |
| LOSS-WEB-01 | CapabilityLoss | runtime authority | the Web pack is a read-only semantic surface; it executes nothing | DECLARED |

## NACK

| nack_id | record_type | statement | basis |
| --- | --- | --- | --- |
| NACK-WEB-01 | NACK | this document carries contracts and provenance only; it has no runtime effect | claim ceiling: DESIGN/FILE_PRESENT/SCHEMA_VALID only |
| NACK-WEB-02 | NACK | no live HGK/GENIE integration PASS is claimed; S5/S6 seams are fixture/mock only | S5/S6 NOT_AUTHORISED |

## Seam Compatibility Fixtures

| stage | seam_schemas | fixture_kind | live_status | asserted |
| --- | --- | --- | --- | --- |
| S5 | ExecutionHandoff, ExecutionBindingRef, ArtifactIdentity | compatibility | NOT_RUN | {"itch_contract_only":true,"no_live_receiver_ack":true,"no_world_effect":true} |
| S6 | GENIEProjectionRef, SurfaceProjectionManifest | compatibility | NOT_RUN | {"itch_contract_only":true,"no_live_receiver_ack":true,"no_world_effect":true} |
| S7 | SurfaceProjectionManifest, ProfileBinding | compatibility | NOT_RUN | {"itch_contract_only":true,"no_live_receiver_ack":true,"no_world_effect":true} |
| S8 | AuthorityBinding, WorkOrderCandidate, TaskSpecSeed | compatibility | NOT_RUN | {"itch_contract_only":true,"no_live_receiver_ack":true,"no_world_effect":true} |

## Eval Oracle Objects

| object_id | schema | schema_version | source_hash |
| --- | --- | --- | --- |
| S0:ClaimCeiling | urn:pipd:s0:ClaimCeiling:1 | 1 | dbb2ce4dd322da99ca3b3067274b85928b995aba59ca3f04802d5e8ba253ab85 |
| S0:TQAEP | urn:pipd:s0:TQAEP:1 | 1 | d14092817befb5e81c470449b9ac5160b6fba7e3fcde450ec00d1cadc21820cd |
| S0:EvidenceExpectation | urn:pipd:s0:EvidenceExpectation:1 | 1 | 02327839c21d5ba24d08dd52f9caa31a07616965c6235cece58487a810b99b7f |

## Gate Entrypoints

| gate | command | mode | denominator |
| --- | --- | --- | --- |
| G-S3-WEB | tools/web_pack_check.py --strict | STRICT_CHECK_ONLY | five PIPD documents; OPTIONAL_SITE_UI excluded |
| G-S3-HOST | tools/host_projection_check.py --strict | STRICT_CHECK_ONLY | three host effective loads; fixture/mock only |

## Profile Assurance

| profile | assurance |
| --- | --- |
| ASSURED | deterministic_validator, negative_security, adversarial, independent_checker |
| LITE | deterministic_validator |
| STANDARD | deterministic_validator, negative_security |

## Claim Ceiling

| claim | state |
| --- | --- |
| adapter_checks | FIXTURE_MOCK_ONLY |
| live_hgk_genie_integration | NOT_CLAIMED |
| live_status | NOT_RUN |
| s5_s6 | NOT_AUTHORISED |
