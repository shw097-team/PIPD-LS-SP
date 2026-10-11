---
name: pipd-surface-projection
description: Project canonical PIPD objects, profiles and the adapter mapping onto Web and host surfaces with declared capability loss. Fixture/mock contract only; S5/S6 NOT_AUTHORISED.
---

# pipd-surface-projection

<!--PIPD-HOST-RECORD
{
 "capability_loss": [
  {
   "capability": "skill execution authority",
   "loss_id": "LOSS-GS-01",
   "reason": "projection carries the skill contract only; execution stays with the host",
   "record_type": "CapabilityLoss",
   "severity": "DECLARED"
  }
 ],
 "compatibility": {
  "asserted": {
   "itch_contract_only": true,
   "no_live_receiver_ack": true,
   "no_world_effect": true
  },
  "fixture_kind": "compatibility",
  "live_status": "NOT_RUN",
  "mode": "FIXTURE_MOCK",
  "seam_schemas": [
   "SurfaceProjectionManifest",
   "ProfileBinding"
  ],
  "seam_source": "ADAPTER:MAPPING"
 },
 "contract_version": "1",
 "entry_kind": "skill_projection",
 "field_contract": [
  {
   "name": "surface",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "source_hashes",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "generated_files",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "parity_loss",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "stale_rule",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "subject_id",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "version",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "content_hash",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "schema_version",
   "required": true,
   "source_object_id": "S0:SurfaceProjectionManifest",
   "type": "object"
  },
  {
   "name": "profile",
   "required": true,
   "source_object_id": "S0:ProfileBinding",
   "type": "object"
  },
  {
   "name": "axes",
   "required": true,
   "source_object_id": "S0:ProfileBinding",
   "type": "object"
  },
  {
   "name": "vetoes",
   "required": true,
   "source_object_id": "S0:ProfileBinding",
   "type": "object"
  },
  {
   "name": "artifact_depth",
   "required": true,
   "source_object_id": "S0:ProfileBinding",
   "type": "object"
  },
  {
   "name": "assurance",
   "required": true,
   "source_object_id": "S0:ProfileBinding",
   "type": "object"
  }
 ],
 "nack": [
  {
   "basis": "S5/S6 NOT_AUTHORISED",
   "nack_id": "NACK-GS-01",
   "record_type": "NACK",
   "statement": "effective load is a fixture/mock contract load, not a live generic host run"
  },
  {
   "basis": "S5/S6 NOT_AUTHORISED",
   "nack_id": "NACK-GS-02",
   "record_type": "NACK",
   "statement": "no live HGK/GENIE integration PASS is claimed by this projection"
  }
 ],
 "payload": {
  "contract_refs": [
   "S0:SurfaceProjectionManifest",
   "S0:ProfileBinding",
   "PROFILE:TRIO",
   "ADAPTER:MAPPING"
  ],
  "input_object_id": "S0:SurfaceProjectionManifest",
  "non_trigger": [
   "live HGK execution or GENIE integration requests (S5/S6 NOT_AUTHORISED)",
   "requirement compilation or pipeline entry points (owned by another lane)"
  ],
  "output_object_id": "S0:ProfileBinding",
  "skill_id": "pipd-surface-projection",
  "trigger": [
   "user asks to project canonical PIPD objects onto Web or host surfaces",
   "a surface pack or host projection must be (re)generated from canonical sources"
  ]
 },
 "permissions": [
  "read:canonical-objects",
  "emit:projection"
 ],
 "provider": {
  "admission_state": "FIXTURE_MOCK",
  "basis": "adapter checks use fixture/mock contracts only",
  "live_integration": false,
  "provider_id": "generic-skill-host"
 },
 "schema": "PIPD-HOST-PROJECTION/1",
 "schema_version": "1",
 "scope": [
  "dist/web/**"
 ],
 "source_refs": [
  {
   "object_id": "S0:SurfaceProjectionManifest",
   "schema": "urn:pipd:s0:SurfaceProjectionManifest:1",
   "schema_version": "1",
   "source_hash": "87f8057e8dac68f304ed4e9c2dd118a26c69428015769ab09d39398d34dcb57d",
   "source_path": "schemas/SurfaceProjectionManifest.schema.json"
  },
  {
   "object_id": "S0:ProfileBinding",
   "schema": "urn:pipd:s0:ProfileBinding:1",
   "schema_version": "1",
   "source_hash": "b559fb70bb6ceb9d491c989cb5ec031f44d15bcad5b40e75d6649aa059a93556",
   "source_path": "schemas/ProfileBinding.schema.json"
  },
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
 ],
 "surface": "host:generic-skills"
}
-->

## Contract

| field | type | required | source_object_id |
| --- | --- | --- | --- |
| surface | object | true | S0:SurfaceProjectionManifest |
| source_hashes | object | true | S0:SurfaceProjectionManifest |
| generated_files | object | true | S0:SurfaceProjectionManifest |
| parity_loss | object | true | S0:SurfaceProjectionManifest |
| stale_rule | object | true | S0:SurfaceProjectionManifest |
| subject_id | object | true | S0:SurfaceProjectionManifest |
| version | object | true | S0:SurfaceProjectionManifest |
| content_hash | object | true | S0:SurfaceProjectionManifest |
| schema_version | object | true | S0:SurfaceProjectionManifest |
| profile | object | true | S0:ProfileBinding |
| axes | object | true | S0:ProfileBinding |
| vetoes | object | true | S0:ProfileBinding |
| artifact_depth | object | true | S0:ProfileBinding |
| assurance | object | true | S0:ProfileBinding |

| role | object_id |
| --- | --- |
| input | S0:SurfaceProjectionManifest |
| output | S0:ProfileBinding |
| contract_ref | S0:SurfaceProjectionManifest |
| contract_ref | S0:ProfileBinding |
| contract_ref | PROFILE:TRIO |
| contract_ref | ADAPTER:MAPPING |

## Trigger

- user asks to project canonical PIPD objects onto Web or host surfaces
- a surface pack or host projection must be (re)generated from canonical sources

## Non-Trigger

- live HGK execution or GENIE integration requests (S5/S6 NOT_AUTHORISED)
- requirement compilation or pipeline entry points (owned by another lane)

## Capability Loss

| loss_id | capability | reason | severity |
| --- | --- | --- | --- |
| LOSS-GS-01 | skill execution authority | projection carries the skill contract only; execution stays with the host | DECLARED |

## NACK

| nack_id | statement | basis |
| --- | --- | --- |
| NACK-GS-01 | effective load is a fixture/mock contract load, not a live generic host run | S5/S6 NOT_AUTHORISED |
| NACK-GS-02 | no live HGK/GENIE integration PASS is claimed by this projection | S5/S6 NOT_AUTHORISED |
