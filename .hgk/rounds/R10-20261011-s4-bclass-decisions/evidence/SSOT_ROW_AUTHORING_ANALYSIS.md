# SSOT row-authoring analysis — the three in-repo OBJECTS_ABSENT rows

Round: `R10-20261011-s4-bclass-decisions`. Read-only analysis; this is the only file written.
Subject: `docs/SPEC_DEL_CROSSWALK.json` on branch `main`.
Purpose: for each of the three crosswalk rows whose required SSOT object does not exist in this
repo, decide whether the project **genuinely owes** the object and whether it can be materialised
**faithfully** from material already in the repo — or whether it is owned elsewhere / would require
invention.

Claim ceiling: this analysis closes **nothing** and promotes **no** row. `EVIDENCED != PASS`; a file
existing does not make a claim true. Every verdict below is a *recommendation*; the acceptance
authority is the owner, and no agent may self-accept.

Hard rules honoured: no crosswalk / schema / validator / evidence file was modified; no SSOT object
was authored; nothing outside the repo was edited; `DEL-004` (`SPEC_REGISTRY@1`, already settled as
EXTERNAL) was not re-examined.

---

## 0. Anchoring facts (opened, not restated from the audit)

- `docs/SPEC_DEL_CROSSWALK.json` — `schema "PIPD-SPEC-DEL-CROSSWALK/1"`, `counts SPEC 32 / DEL 25 =
  total 57`, `status_summary EVIDENCED 42 / EVIDENCE_GAP 11 / DESIGN_ONLY 4`. It is **generated** by
  `tools/build_spec_del_crosswalk.py`, whose docstring says "nothing is invented" and that a row is
  `EVIDENCE_GAP` precisely "where a link cannot be established from objects that actually exist in
  this repo". The three rows below are exactly such rows.
- The blueprint the crosswalk cites, `PIPD-LS-SP_藍圖.md` (sha256
  `a751a9e91dc6d0b7914b…`), is **external** — it lives at
  `C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\…\PIPD-LS-SP_藍圖\PIPD-LS-SP_藍圖.md`
  (`.hgk/preflight/source-manifest.json`, family `F3_PIPD_DESIGN`). This is why the probe's
  `top_citation SRC-a751a9e9…` for the query `PIPD-LIFECYCLE-SPEC` is a hit on the blueprint, not on a
  lifecycle object.
- Workspace-wide search confirms the required names (`PIPD-LIFECYCLE-SPEC`, `SPEC_REGISTRY`,
  `ADAPTER_REGISTRY`, an MCP-materialization object) appear **only** in the crosswalk, its generator,
  a knowledge probe, prior-round evidence, and preflight/contract text — never as an object.

---

## 1. `PIPD-SP-SPEC-002` — `PIPD-LIFECYCLE-SPEC@1.1.0`

### 1.1 The exact crosswalk row (`docs/SPEC_DEL_CROSSWALK.json`, lines 40–62)
```json
{
  "id": "PIPD-SP-SPEC-002",
  "kind": "SPEC",
  "source_locator": "PIPD-LS-SP_藍圖.md §19.2 L1383",
  "normative_summary": "All Skills/packages project PIPD-LIFECYCLE-SPEC@1.1.0; no competing lifecycle SSOT",
  "owner": "PIPD Core",
  "stage": "S0",
  "requirement_refs": ["REQ-PIPD-002"],
  "deliverable_refs": ["DEL-003"],
  "evidence_refs": [],
  "gate": "G-S0-OBJECTS",
  "oracle": "",
  "negative_mutation": "",
  "status": "EVIDENCE_GAP",
  "first_fail": "no lifecycle SSOT object materialized; PIPD-LIFECYCLE-SPEC@1.1.0 appears only in a knowledge probe",
  "tt_refs": ["TT-PIPD-KNOWLEDGE-QUARANTINE"]
}
```
Required object: a materialised `PIPD-LIFECYCLE-SPEC@1.1.0` SSOT object. Fields the row wants
evidenced: the row carries **no** `evidence_refs` — i.e. the row itself declares *nothing* in-repo
evidences it. `deliverable_refs` point at `DEL-003` (`CANONICAL_OBJECT_REGISTRY@1`).

### 1.2 In-repo material actually opened
| path | what it actually says |
|---|---|
| `.hgk/knowledge/RetrievalProbeReport.json` | Positive probe `{"query":"PIPD-LIFECYCLE-SPEC","hits":3,"top_citation":"SRC-a751a9e91dc6d0b7914b#full","verdict":"HIT"}`. A FTS retrieval **hit on the external blueprint**, not an object. |
| `.hgk/preflight/PIPD-LS-SP.CONTRACT.json` (and `_R2`, `_contract_part1/2/3`) | `normative_claims` NC-02: `"PIPD-LS-SP implements PIPD-LIFECYCLE-SPEC@1.1.0 across 11 design packages (PIPD-PKG-00..10)."` with locator `PIPD_LS/PIPD_LS_canonical_standard.md#standard_id=PIPD-LIFECYCLE-SPEC`. |
| `.hgk/preflight/source-manifest.json` (family `F2_PIPD_STANDARD`) | Lists `…/PIPD/PIPD_LS/PIPD_LS_canonical_standard.md`, size 209157, sha256 `6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a`. Path root is `C:\Projects\Agent_Workspace\知識庫\…` — **external to this repo**. |
| `find . -iname '*canonical_standard*'` | **No match inside the repo.** The standard file is not a repo file. |

No `PIPD-LIFECYCLE-SPEC` object exists in this repo at **any** version — not v1.0.0, not v1.1.0.
Every occurrence is either a retrieval-index token or a *reference to* the external standard.

### 1.3 Hypothesis 2 verdict
**CONFIRMED as absent, and the object is not owned here.** The lifecycle standard is a NORMATIVE
source in the external knowledge corpus (`PIPD_LS_canonical_standard.md`,
`standard_id=PIPD-LIFECYCLE-SPEC`), and the preflight contract frames PIPD-LS-SP as the
**implementation of** that standard, not its owner. No v1.0.0 or any other version exists in-repo.

### 1.4 Row verdict — `NOT-OWED-HERE-EXTERNAL`
The lifecycle SSOT is owned by the external standard; this repo **consumes** it. A v1.1.0 object
authored inside the product repo would be a *second* lifecycle SSOT — the exact "competing lifecycle
SSOT" the row's own `normative_summary` forbids. Building it here to move a counter would be the
`EXISTS != TRUE` failure the R10 admission explicitly bans.

*Honest alternative if the owner wants the row evidenced on `main`:* do **not** author the SSOT; author
a thin **projection/reference receipt** that records (a) the external standard's identity — sha256
`6f6aafece90b34e33786647e14fee840f5424893995b3164cbb52953a5c4f14a`, `standard_id=PIPD-LIFECYCLE-SPEC`,
`@1.1.0` — and (b) that every in-repo lifecycle reference resolves to that one external standard
(candidate refs: contract NC-02 locator above). That receipt is a restatement of existing material; it
is **not** the SSOT object and must not be scored as one. Tag that as `NEEDS-OWNER-DESIGN-DECISION`
scope, not a closure.

---

## 2. `PIPD-SP-SPEC-030` — MCP materialization object

### 2.1 The exact crosswalk row (`docs/SPEC_DEL_CROSSWALK.json`, lines 697–717)
```json
{
  "id": "PIPD-SP-SPEC-030",
  "kind": "SPEC",
  "source_locator": "PIPD-LS-SP_藍圖.md §19.2 L1411",
  "normative_summary": "MCP materializes only for live/authenticated/action/dynamic-discovery needs",
  "owner": "Technology Admission / PIPD",
  "stage": "S2",
  "requirement_refs": ["REQ-PIPD-030"],
  "deliverable_refs": ["DEL-015"],
  "evidence_refs": [],
  "gate": "G-S3-HOST/G-S3-WEB",
  "oracle": "",
  "negative_mutation": "",
  "status": "EVIDENCE_GAP",
  "first_fail": "no MCP materialization object exists in the repo; optionality cannot be linked to live objects",
  "tt_refs": []
}
```
Required object: an MCP materialization object. Fields wanted: none declared (`evidence_refs: []`);
`deliverable_refs` point at `DEL-015`.

### 2.2 In-repo material actually opened
| path | what it actually says |
|---|---|
| `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` → CAND-06 (lines ~1318–1394) | `technology_id CAND-06`, `external_name "MCP"`, `capability_slot "external tool connector ABI"`, `disposition "ADOPT_WITH_TRANSLATION"`, **`adapter_materialization_state "DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED"`**, `current_runtime_state "NOT_EXECUTED"`, `current_design_state "OPTIONAL_LATE_BIND"`, `runtime_admission_state "BLOCKED_EXTERNAL_PIN_LICENSE_PENDING"`, pin `UNAVAILABLE` (`PIN_REVALIDATION_REQUIRED`), license `LICENSE_NOT_INDEPENDENTLY_PIN_VERIFIED`, `reported_active false`, `independently_verified false`, `adapter_ref "pack://PIPD-PKG-00/technology/CAND-06/adapter@r2"`. |
| same file, top-level | `overall_verdict "FAIL"`, `runtime_state "NOT_EXECUTED — no candidate was installed, fetched or run"`, `reported_active []`, `user-guard`: "reported_active: [] means NO ROW IS ADMITTED ACTIVE". So **MCP is not installed anywhere.** |
| `.hgk/artifacts/CapabilityActivationLedger.json` | `deferred_profile_gated: ["external SaaS","extra vector DB / KG","MCP","remote execution","tool/model/provider switching","SGM cutover"]`. MCP is explicitly *deferred*. |

There is no MCP server, connector, adapter instance, or materialization record in the repo. The only
MCP facts are the design/admission row and the deferred-ledger entry.

### 2.3 Hypothesis 3 verdict
**CONFIRMED.** Only a technology-admission *design* row exists (`DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED`
/ `NOT_EXECUTED`). MCP is technology that is **not** installed on this host and is explicitly deferred.

### 2.4 Row verdict — `OWED-BUILDABLE-FAITHFULLY` (negative/decisional form only)
The repo owes a *record of the MCP materialization decision state*; it does **not** owe (and cannot
truthfully produce) an object asserting MCP **materialised**. What a materialization object **would
have to assert to be TRUE** is:

> MCP is **not** materialized in this round: `materialized = false`, `materialized_count = 0`, because
> the gating condition — a live / authenticated / action / dynamic-discovery need — is **not present**,
> and the underlying technology is `DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED` / `NOT_EXECUTED` with an
> `UNAVAILABLE` pin and an unverified licence.

A *positive* materialization object ("MCP materialized") would assert something the material refutes —
that would be invention and is **forbidden**. The negative/decisional object is a pure restatement.

**Minimal artefact (if the owner accepts the negative form) — every field traceable:**
```json
{
  "schema": "PIPD-MCP-MATERIALIZATION-DECISION/1",
  "technology_id": "CAND-06",                       // TECHNOLOGY_ADMISSIONS.json CAND-06
  "external_name": "MCP",                           // CAND-06
  "materialization_gate": "live/authenticated/action/dynamic-discovery needs", // crosswalk normative_summary
  "gate_condition_present": false,                  // derived: no such live need exists in repo
  "materialized": false,                            // CAND-06 adapter_materialization_state
  "materialized_count": 0,                          // CAND-06 reported_active:false
  "adapter_materialization_state": "DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED", // CAND-06
  "current_runtime_state": "NOT_EXECUTED",          // CAND-06
  "current_design_state": "OPTIONAL_LATE_BIND",     // CAND-06
  "runtime_admission_state": "BLOCKED_EXTERNAL_PIN_LICENSE_PENDING", // CAND-06
  "pin": "UNAVAILABLE",                             // CAND-06 pin_license_currentness.pin.value
  "license": "LICENSE_NOT_INDEPENDENTLY_PIN_VERIFIED", // CAND-06
  "ledger_disposition": "deferred_profile_gated",   // CapabilityActivationLedger.json (lists "MCP")
  "source_refs": [
    {"path": ".hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json", "record": "CAND-06"},
    {"path": ".hgk/artifacts/CapabilityActivationLedger.json", "field": "deferred_profile_gated"}
  ]
}
```
Note the schema itself does not yet exist; defining it is a design act, so a schema-less or
owner-defined form is required. If the owner reads "materialization object" as "an object proving MCP
*is* materialized", then the row is `NEEDS-OWNER-DESIGN-DECISION` (it cannot be satisfied without
installing MCP, which is out of authorisation).

---

## 3. `DEL-015` — `ADAPTER_REGISTRY@1`

### 3.1 The exact crosswalk row (`docs/SPEC_DEL_CROSSWALK.json`, lines 1066–1084)
```json
{
  "id": "DEL-015",
  "kind": "DEL",
  "source_locator": "PIPD-LS-SP_藍圖.md §27.1 L1873",
  "normative_summary": "ADAPTER_REGISTRY@1 — declared input artifact identities + source hashes; no implicit dependency",
  "owner": "SK-08",
  "stage": "S3",
  "requirement_refs": ["REQ-PIPD-DEL-015"],
  "deliverable_refs": [],
  "evidence_refs": [],
  "gate": "DELIVERABLES_MASTER_LEDGER",
  "oracle": "",
  "negative_mutation": "",
  "status": "EVIDENCE_GAP",
  "first_fail": "no ADAPTER_REGISTRY object materialized; only host projections exist",
  "tt_refs": []
}
```
Required object: `ADAPTER_REGISTRY@1`, owner SK-08 (the same surface/host skill that owns
`DEL-016 SURFACE_PROJECTION_MANIFEST@1` and `DEL-017 WEB_HOST_PROJECTION_PACK@1`). The row wants the
object to declare artifact identities **+ source hashes**, "no implicit dependency". `evidence_refs: []`.

### 3.2 In-repo material actually opened
| path | what it actually says |
|---|---|
| `.hgk/artifacts/s3/HOST_PROJECTIONS.json` | `schema "PIPD-HOST-PROJECTIONS-CHECK/1"`, `verdict "PASS"`, `host_count "3/3"`, `required_hosts ["host:generic-skills","host:genie-adapter","host:hgk-receiver"]`, three `rows` each with `loader` + `effective_load true` + per-ref `source_ref_hashes`; `semantic_parity "PASS"`; per-host `capability_loss`; `mode "FIXTURE_MOCK"` / `live_status "NOT_RUN"`; `claims {adapter_checks: "FIXTURE_MOCK_ONLY", live_status: "NOT_RUN", live_hgk_genie_integration: "NOT_CLAIMED", s5_s6: "NOT_AUTHORISED"}`. **This is a gate CHECK RECEIPT** (`…-CHECK/1`), not a registry object. |
| `src/pipd_ls_sp/projection.py#ADAPTER_MAPPING` (lines 374–481) | The **canonical adapter-mapping source object**: `schema "PIPD-ADAPTER-MAPPING/1"`, `version "1"`, `writable_scope ["dist/web/**"]`, `routing {LITE/STANDARD/ASSURED → host surfaces}`, and `hosts` with 3 entries. Each host carries `dir`, `entry_file`, `entry_kind`, `loader`, `skill_id` (generic-skills), `source_objects`, `required_mappings`, `allowed_permissions`, `provider {provider_id, admission_state, live_integration:false, basis}`, `capability_loss`, `nack`. Its hash is `sha256_text(canonical_json(ADAPTER_MAPPING))` = `ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab` (this is the `ADAPTER:MAPPING` source_ref hash seen in every host projection). |
| `.hgk/artifacts/s1/web_projection/host_*/…` | The three materialised host entries (`SKILL.md`, `receiver-map.json`, `object-crosswalk.json`) — each a `PIPD-HOST-PROJECTION/1` record, each referencing `ADAPTER:MAPPING`. |
| `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` | 22 candidates (`CAND-01..22`) each with `adapter_ref "pack://PIPD-PKG-00/technology/CAND-XX/adapter@r2"` and `adapter_materialization_state "DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED"` — i.e. 22 **declared, not-installed** technology adapters. |

### 3.3 Hypothesis 1 verdict
**CONFIRMED with a correction.** `HOST_PROJECTIONS.json` does exist and does report exactly 3 hosts,
`live_status "NOT_RUN"`, `adapter_checks "FIXTURE_MOCK_ONLY"` — but it is a **check receipt**, not a
registry. The registry-shaped object that *does* exist is the canonical `ADAPTER_MAPPING`
(`PIPD-ADAPTER-MAPPING/1`) in `projection.py`, and it is a real, hashed, source-pinned object.

### 3.4 Row verdict — `OWED-BUILDABLE-FAITHFULLY`
SK-08 owes the deliverable, and a truthful registry is derivable **without inventing any adapter**:
the 3 host adapters exist as contract/fixture entries (from `ADAPTER_MAPPING`), and the 22 technology
adapters exist as *declared* refs with an explicit `NOT_INSTALLED` state. There is **no** live adapter
to claim, and a faithful registry must say so (`materialized 3 / live 0 / FIXTURE_MOCK`). One scope
decision is the owner's: whether `ADAPTER_REGISTRY@1` enumerates *host-surface* adapters (the SK-08
sense) or *technology* adapters (the CAND sense) or both. Either scope is a restatement of existing
material; the risk is only in the definition, not in the facts.

**Minimal artefact — every field traceable to a named existing file:**
```json
{
  "schema": "PIPD-ADAPTER-REGISTRY/1",              // schema not yet defined; owner-defined
  "registry_scope": "host-surface adapters present in this repo (contract/fixture only)",
  "source_refs": [
    {"object_id": "ADAPTER:MAPPING", "schema": "PIPD-ADAPTER-MAPPING/1", "version": "1",
     "source_path": "src/pipd_ls_sp/projection.py#ADAPTER_MAPPING",
     "source_hash": "ae939d979559985dfe692bf7f8638fc571d07013270fc15e734951b37b2af1ab"}
  ],
  "adapters": [
    {"adapter_id": "host:generic-skills", "entry_file": "host_generic-skills/SKILL.md",
     "entry_kind": "skill_projection", "loader": "skill_projection_v1",
     "provider_id": "generic-skill-host", "provider_admission_state": "FIXTURE_MOCK",
     "live_integration": false,
     "allowed_permissions": ["read:canonical-objects","emit:projection"]},
    {"adapter_id": "host:hgk-receiver", "entry_file": "host_hgk-receiver/receiver-map.json",
     "entry_kind": "receiver_map", "loader": "receiver_map_v1",
     "provider_id": "hgk-execution-receiver", "provider_admission_state": "OFF",
     "live_integration": false,
     "allowed_permissions": ["read:canonical-objects","emit:projection","emit:receiver-map"]},
    {"adapter_id": "host:genie-adapter", "entry_file": "host_genie-adapter/object-crosswalk.json",
     "entry_kind": "object_crosswalk", "loader": "object_crosswalk_v1",
     "provider_id": "genie-live-integration", "provider_admission_state": "OFF",
     "live_integration": false,
     "allowed_permissions": ["read:canonical-objects","emit:projection","emit:object-crosswalk"]}
  ],
  "profile_routing": {"LITE":["host:generic-skills"],
                      "STANDARD":["host:generic-skills","host:hgk-receiver","host:genie-adapter"],
                      "ASSURED":["host:generic-skills","host:hgk-receiver","host:genie-adapter"]},
  "install_state": {"declared": 3, "materialized": 3, "live": 0,
                    "mode": "FIXTURE_MOCK", "live_status": "NOT_RUN"},
  "technology_adapters_declared": [   // optional second scope, from TECHNOLOGY_ADMISSIONS.json
    {"candidate": "CAND-01", "adapter_ref": "pack://PIPD-PKG-00/technology/CAND-01/adapter@r2",
     "adapter_materialization_state": "DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED"}
    /* … CAND-01..CAND-22 … */
  ]
}
```
Provenance of each field: `adapters[].*` and `profile_routing` ← `src/pipd_ls_sp/projection.py#ADAPTER_MAPPING`;
`install_state` ← `ADAPTER_MAPPING` providers + `HOST_PROJECTIONS.json` `claims`/`compatibility`;
`technology_adapters_declared` ← `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json`. No field is invented.

---

## 4. Summary

| row | required object | verdict | basis (opened) |
|---|---|---|---|
| `PIPD-SP-SPEC-002` | materialised `PIPD-LIFECYCLE-SPEC@1.1.0` | **NOT-OWED-HERE-EXTERNAL** | Standard `PIPD_LS_canonical_standard.md#standard_id=PIPD-LIFECYCLE-SPEC` (sha256 `6f6aafec…`) is in the external knowledge corpus, not the repo (`source-manifest.json` F2; `find` empty). Repo *implements* it (NC-02). In-repo copy = the forbidden competing SSOT. |
| `PIPD-SP-SPEC-030` | MCP materialization object | **OWED-BUILDABLE-FAITHFULLY** (negative/decisional form) | CAND-06 `DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED` / `NOT_EXECUTED`, pin `UNAVAILABLE`, ledger `deferred_profile_gated`. Truthful object must assert MCP is **not** materialized (0). Positive form = invention → forbidden. |
| `DEL-015` | `ADAPTER_REGISTRY@1` | **OWED-BUILDABLE-FAITHFULLY** | Canonical `ADAPTER_MAPPING` (`PIPD-ADAPTER-MAPPING/1`, hash `ae939d97…`) enumerates 3 host adapters; `HOST_PROJECTIONS.json` is the check receipt (`3/3`, `NOT_RUN`, `FIXTURE_MOCK_ONLY`); 22 technology adapters declared `NOT_INSTALLED`. Registry restates existing material; no adapter invented. Scope (host vs technology) is the owner's call. |

### What this analysis does NOT claim
- No row is closed, promoted, or marked `EVIDENCED`. All three remain `EVIDENCE_GAP`.
- No SSOT object was authored. The two "buildable" verdicts are *recommendations* with a proposed
  minimal form; authoring is the parent/owner's call under its own admission.
- The `OWED-BUILDABLE-FAITHFULLY` verdicts are honestly-conditioned: SPEC-030 is buildable **only** in
  the negative/decisional form; DEL-015 requires an owner scope decision (host-surface vs technology
  adapters). If either condition is rejected, the verdict degrades to `NEEDS-OWNER-DESIGN-DECISION`.
- Crosswalk, generator, schemas and validators were read-only throughout; only this file was written.
