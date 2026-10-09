# PIPD Router Profiles

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
 "doc_id": "PIPD_ROUTER_PROFILES",
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
 "source_hash": "4fb12beb1f804700e9ae751d3ca3b657115258996f4a71524dc3480ecbdb434c",
 "source_objects": [
  {
   "object_id": "PROFILE:TRIO",
   "schema": "PIPD-PROFILE-TRIO/1",
   "schema_version": "1",
   "source_hash": "2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070",
   "source_path": "src/pipd_ls_sp/profiles.py"
  },
  {
   "object_id": "ADAPTER:MAPPING",
   "schema": "PIPD-ADAPTER-MAPPING/1",
   "schema_version": "1",
   "source_hash": "ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab",
   "source_path": "src/pipd_ls_sp/projection.py#ADAPTER_MAPPING"
  }
 ]
}
-->

## Source Objects

| object_id | schema | schema_version | source_path | source_hash |
| --- | --- | --- | --- | --- |
| PROFILE:TRIO | PIPD-PROFILE-TRIO/1 | 1 | src/pipd_ls_sp/profiles.py | 2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070 |
| ADAPTER:MAPPING | PIPD-ADAPTER-MAPPING/1 | 1 | src/pipd_ls_sp/projection.py#ADAPTER_MAPPING | ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab |

## Capability Loss

| loss_id | record_type | capability | reason | severity |
| --- | --- | --- | --- | --- |
| LOSS-WEB-01 | CapabilityLoss | runtime authority | the Web pack is a read-only semantic surface; it executes nothing | DECLARED |

## NACK

| nack_id | record_type | statement | basis |
| --- | --- | --- | --- |
| NACK-WEB-01 | NACK | this document carries contracts and provenance only; it has no runtime effect | claim ceiling: DESIGN/FILE_PRESENT/SCHEMA_VALID only |
| NACK-WEB-02 | NACK | no live HGK/GENIE integration PASS is claimed; S5/S6 seams are fixture/mock only | S5/S6 NOT_AUTHORISED |

## Profile Trio

| profile | artifact_depth | assurance | target_resolution | max_axes |
| --- | --- | --- | --- | --- |
| ASSURED | L4_FAILURE_RECOVERY | deterministic_validator, negative_security, adversarial, independent_checker | runtime | 10 |
| LITE | L1_SCHEMA_CONTRACT | deterministic_validator | package | 3 |
| STANDARD | L3_INTEGRATION_RUNTIME | deterministic_validator, negative_security | integration | 6 |

## Router Axes

| axis |
| --- |
| intent |
| knowledge |
| verification |
| release |
| trust_boundary |
| preexisting_repo |
| profile |
| tech_candidates |
| host_surface |

## Router Matrix

| profile | host_surface | entry_kind |
| --- | --- | --- |
| ASSURED | host:generic-skills | skill_projection |
| ASSURED | host:hgk-receiver | receiver_map |
| ASSURED | host:genie-adapter | object_crosswalk |
| LITE | host:generic-skills | skill_projection |
| STANDARD | host:generic-skills | skill_projection |
| STANDARD | host:hgk-receiver | receiver_map |
| STANDARD | host:genie-adapter | object_crosswalk |

## Profile Binding Sources

| object_id | schema | schema_version | source_hash |
| --- | --- | --- | --- |
| PROFILE:TRIO | PIPD-PROFILE-TRIO/1 | 1 | 2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070 |
| ADAPTER:MAPPING | PIPD-ADAPTER-MAPPING/1 | 1 | ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab |
