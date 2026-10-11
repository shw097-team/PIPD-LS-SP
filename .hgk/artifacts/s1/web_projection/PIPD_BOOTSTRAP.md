# PIPD-LS-SP Bootstrap

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
 "doc_id": "PIPD_BOOTSTRAP",
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
 "source_hash": "6c2f263e8b918d5499a9bbe1caff6dc6a154fa39516a8bcbbdbcd78e759057b7",
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
  },
  {
   "object_id": "PROFILE:TRIO",
   "schema": "PIPD-PROFILE-TRIO/1",
   "schema_version": "1",
   "source_hash": "2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070",
   "source_path": "src/pipd_ls_sp/profiles.py"
  },
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
| PROFILE:TRIO | PIPD-PROFILE-TRIO/1 | 1 | src/pipd_ls_sp/profiles.py | 2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070 |
| SEAM:S5 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s5_compat.json | 5aa6aa3e4f360ab6e898e5034ec3871e731ec48137ae8af50fc2138871faf3ec |
| SEAM:S6 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s6_compat.json | a2541b4b73f054d5557dcaeaca1544a3665fb9e5ddcd7264be383b59c4c39b37 |
| SEAM:S7 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s7_compat.json | 185c160092e751e66c075222326378124e7c55f569d725fb64392cebb224b515 |
| SEAM:S8 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s8_compat.json | 53492fe85d88aff6e837572ba90d5b3ccba0fccd6d11375928f307fb072a2ffe |
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

## Canonical Source Inventory

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
| PROFILE:TRIO | PIPD-PROFILE-TRIO/1 | 1 | src/pipd_ls_sp/profiles.py | 2631eac7f6cb2b48dba0ed6628c4d7d7e94b7843ac29353950c2d51172789070 |
| SEAM:S5 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s5_compat.json | 5aa6aa3e4f360ab6e898e5034ec3871e731ec48137ae8af50fc2138871faf3ec |
| SEAM:S6 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s6_compat.json | a2541b4b73f054d5557dcaeaca1544a3665fb9e5ddcd7264be383b59c4c39b37 |
| SEAM:S7 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s7_compat.json | 185c160092e751e66c075222326378124e7c55f569d725fb64392cebb224b515 |
| SEAM:S8 | PIPD-SEAM-COMPAT/1 | 1 | fixtures/s5_s8/s8_compat.json | 53492fe85d88aff6e837572ba90d5b3ccba0fccd6d11375928f307fb072a2ffe |
| ADAPTER:MAPPING | PIPD-ADAPTER-MAPPING/1 | 1 | src/pipd_ls_sp/projection.py#ADAPTER_MAPPING | ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab |

## Host Surfaces

| surface | dir | entry_file | loader | provider_admission_state | live_integration |
| --- | --- | --- | --- | --- | --- |
| host:generic-skills | host_generic-skills | SKILL.md | skill_projection_v1 | FIXTURE_MOCK | false |
| host:hgk-receiver | host_hgk-receiver | receiver-map.json | receiver_map_v1 | OFF | false |
| host:genie-adapter | host_genie-adapter | object-crosswalk.json | object_crosswalk_v1 | OFF | false |

## Web Denominator

| files | kind | count | in_denominator |
| --- | --- | --- | --- |
| PIPD_BOOTSTRAP.md..PIPD_EVAL_HANDOFF.md | WEB_DOC | 5 | true |
| OPTIONAL_SITE_UI/index.html, app.js, styles.css, manifest.webmanifest, README.md | OPTIONAL_SITE_UI | 5 | false |

## Profile Routing

| profile | host_surfaces |
| --- | --- |
| ASSURED | host:generic-skills, host:hgk-receiver, host:genie-adapter |
| LITE | host:generic-skills |
| STANDARD | host:generic-skills, host:hgk-receiver, host:genie-adapter |
