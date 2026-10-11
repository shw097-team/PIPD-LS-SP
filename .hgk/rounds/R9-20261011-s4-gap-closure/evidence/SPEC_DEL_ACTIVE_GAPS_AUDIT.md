# SPEC/DEL crosswalk — ACTIVE-GAP audit (R9-20261011-s4-gap-closure)

Independent per-row audit of the crosswalk's **active** rows (the standing claim's
"10 active gaps"). Read-only: no crosswalk, schema, validator, or product file was modified.
The only file written is this one.

- Subject inspected: `docs/SPEC_DEL_CROSSWALK.json` on branch `main`, tip `f541c3968d8b3fc1d2dfd71bab1b0d56894f05ce`.
- Claim ceiling: this audit grants **nothing**. `EVIDENCED != PASS`, and a count is not a result.
  Every verdict below is `OPEN (EVIDENCE_GAP)` — none is promoted to PASS.

---

## 1. Denominator — recounted from the file, not restated from prose

The crosswalk is `{"schema":"PIPD-SPEC-DEL-CROSSWALK/1", …}` with a top-level `rows` array of
**57** entries (`counts = SPEC 32 / DEL 25`). Each row carries a `status` field. I counted the
`status` values directly:

| status field (file's own column) | rows |
|---|---|
| `EVIDENCED` | **42** |
| `EVIDENCE_GAP` | **11** |
| `DESIGN_ONLY` | **4** |
| **total** | **57** |

This matches the R4 owner adjudication A4 (`KEEP_CROSSWALK_EVIDENCE_GAPS`, `docs/OWNER_ADJUDICATION_R4_2026-10-09.json`): "42 EVIDENCED / 11 EVIDENCE_GAP / 4 DESIGN_ONLY of 57 rows".

The standing claim under audit is **"28 evidenced / 10 active gaps / 19 deferred"**. That partition
is **not** the file's `status` column; it is a second axis computed in the R5P round by
`stage<=S4` filtering. Source (opened):
`.hgk/rounds/R5P-20261010-s4-post-challenge/evidence/F_R5_06_S4_ACTIVE_ROW_EVIDENCE.json`
(`counts = S4_ACTIVE_EVIDENCED 28 / S4_ACTIVE_GAP 10 / DEFERRED_BY_INSTRUCTION 19`) and
`.hgk/rounds/R5P-20261010-s4-post-challenge/evidence/EXTERNAL_READINESS_FAR.json`
(`documented_denominator.crosswalk`: "57 rows = 32 SPEC + 25 DEL; S4-active 38, of which 28 have a
resolvable oracle+negative in the subject and 10 carry EVIDENCE_GAP, 19 deferred by instruction").

**Reconciliation (the two axes agree, they are not a contradiction):**

| | file `status` column | S4-active axis (R5P) |
|---|---|---|
| evidenced | 42 | 28 |
| active (gap) | 11 | 10 |
| deferred | 4 | 19 |
| total | 57 | 57 |

The difference is exactly the rows whose `stage` spans `S5+`: R5P re-buckets them as
`DEFERRED_BY_INSTRUCTION`. Concretely, 42 = 28 + 14, 11 = 10 + **1**, 4 = 4, and
19 = 14 (evidenced-but-S5-spanning) + 1 (`DEL-008`, which the file marks `EVIDENCE_GAP` but whose
stage `S1/S5` spans S5+) + 4 (`DESIGN_ONLY`). The single row that separates "11 file gaps" from
"10 active gaps" is **DEL-008** — it is deferred by stage, not closed.

**Denominator used by this audit (the active axis): 57 total / 28 evidenced / 10 active / 19 deferred.**
The file's raw status column is 42 / 11 / 4; reporting either alone would hide the stage>S4 re-bucket.

### The 10 active rows (recounted)
`S4_ACTIVE_GAP` set, from `F_R5_06_S4_ACTIVE_ROW_EVIDENCE.json`:
`PIPD-SP-SPEC-002, SPEC-020, SPEC-023, SPEC-030, SPEC-032, DEL-004, DEL-015, DEL-018, DEL-019, DEL-021`.

---

## 2. Per-row disposition

Adjudication rule applied uniformly: a row is **adjudicated** only if the repository contains a
materialised artefact that the row is *about* (its deliverable object, or a dedicated closure
receipt for that row) which I opened and can state the contents of. If the object the row is about
is absent from the repo and no dedicated receipt exists, the row is reported **NOT ADJUDICATED**
(OPEN by absence) — no substitute artefact is stretched over it.

| # | row | kind | stage | gate | evidence path actually opened | what it actually shows | verdict |
|---|---|---|---|---|---|---|---|
| 1 | `PIPD-SP-SPEC-020` | SPEC | S0 | G-TQAEP/G-RELEASE | `SBOM.cdx.json` | CycloneDX 1.5 SBOM, `version 1`, one `components` entry (`jsonschema 4.26.0`, MIT). Property `pipd:sbom_scope` = "declared python dependency set only (no transitive closure computed)". There is **no acceptance oracle** separating supply-chain from functional/security acceptance; the file is a declaration, not a checked claim. | **OPEN — EVIDENCE_GAP confirmed (adjudicated)** |
| 2 | `PIPD-SP-SPEC-023` | SPEC | S0 | G-PACKAGE-DERIVATION | `.hgk/artifacts/PackageDerivationReceipt.json` | schema `PIPD-PACKAGE-DERIVATION-RECEIPT/1`; `declared_topology "11-PKG (PKG-00 .. PKG-10)"`, `observed_count 11`, `count_matches_design true`, per-package `sha256`/`bytes`. Its own `note` states the delivery "does not re-derive a different package count". No oracle **recomputes** the count from a responsibility graph; the receipt asserts the design count. | **OPEN — EVIDENCE_GAP confirmed (adjudicated)** |
| 3 | `PIPD-SP-SPEC-032` | SPEC | S0 | G-PACKAGE-DERIVATION | `.hgk/artifacts/s4/S5_S8_BACKLOG.json` | Four `stages` S5–S8, each `live_effect "NOT_RUN"`, `delivery_gate false`, `claim "DESIGN_ONLY_FOR_NEXT_PHASE"`, with typed seams + compat fixtures; `live_effects_claimed 0`, `verdict "PASS"`. It declares only the **S5..S8 boundary**; package-local construction depth is genuinely downstream. | **OPEN — EVIDENCE_GAP confirmed (adjudicated)** |
| 4 | `DEL-018` | DEL | S4 | DELIVERABLES_MASTER_LEDGER | `.hgk/rounds/R7-…/execute/del018_check.json` (+ `…/evidence/DEL018_CLOSURE_PROOF.json`, `…/evidence/R7_CLOSURE_REPORT.md`) | `check_exit 0`, `verdict PASS`, `current_tree_coverage 252/252, uncovered 0`, `violations []` — **but** `subject_scope` = `PUBLISHED_SUBJECT`, commit `5094939606ba9331ed768743eb5b806ad159e639` / tree `b480182c…`, ref `r5-s4-candidate`. The receipt explicitly says it "does NOT assert coverage of the current worktree". `R7_CLOSURE_REPORT.md` §3 states DEL-018 is closed **on the release line, not on `main`**, and "`main` does not carry the release line". On the audited checkout (`main@f541c39`) the `RELEASE_MANIFEST@1` object is still absent; the crosswalk still records `EVIDENCE_GAP`. | **OPEN on this branch — closure receipt exists but binds a different subject (adjudicated)** |
| 5 | `DEL-019` | DEL | S4 | DELIVERABLES_MASTER_LEDGER | `SBOM.cdx.json` | Same file as row 1. A provenance/SBOM **bundle** is present, but there is no oracle verifying cryptographic/provenance claims — no signature, no attestation, no hash-tree check. `R7_CLOSURE_REPORT.md` §4.1 independently records "no release signature or attestation by an external signing identity". | **OPEN — EVIDENCE_GAP confirmed (adjudicated)** |
| 6 | `DEL-021` | DEL | S2 | DELIVERABLES_MASTER_LEDGER | `.hgk/artifacts/PackageDerivationReceipt.json` | Same file as row 2. The receipt exists, but there is **no deterministic-repartition oracle** — nothing recomputes the package partition and compares it. | **OPEN — EVIDENCE_GAP confirmed (adjudicated)** |

Not-adjudicated rows (evidence absent — see §3):

| # | row | kind | stage | gate | evidence path opened | what it shows | verdict |
|---|---|---|---|---|---|---|---|
| 7 | `PIPD-SP-SPEC-002` | SPEC | S0 | G-S0-OBJECTS | `.hgk/knowledge/RetrievalProbeReport.json` (probe only) | The probe returns a **retrieval HIT** for the query `PIPD-LIFECYCLE-SPEC` (`top_citation SRC-a751a9e9…`). That is a text-index hit, not a materialised SSOT object. No `PIPD-LIFECYCLE-SPEC@1.1.0` object exists anywhere in the repo. | **OPEN — NOT ADJUDICATED (object absent)** |
| 8 | `PIPD-SP-SPEC-030` | SPEC | S2 | G-S3-HOST/G-S3-WEB | `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` (nearest artefact) | CAND-06 "MCP": `adapter_materialization_state "DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED"`, `current_runtime_state "NOT_EXECUTED"`, `current_design_state "OPTIONAL_LATE_BIND"`. This is a **technology-admission design row**, not an MCP materialization object; optionality cannot be linked to any live object. | **OPEN — NOT ADJUDICATED (materialization object absent)** |
| 9 | `DEL-004` | DEL | S0 | DELIVERABLES_MASTER_LEDGER | `schemas/registry.json` (checked, rejected as substitute) | The only registry object in the repo is `PIPD-S0-CONTRACT-REGISTRY/1` — a registry of the 19 **S0 contracts**. It is **not** `SPEC_REGISTRY@1` (a registry of SPECs); the only textual occurrences of `SPEC_REGISTRY` are the crosswalk itself and its generator `tools/build_spec_del_crosswalk.py`. The SPEC registry lives in the external blueprint, out of repo. | **OPEN — NOT ADJUDICATED (object absent)** |
| 10 | `DEL-015` | DEL | S3 | DELIVERABLES_MASTER_LEDGER | `.hgk/artifacts/s3/HOST_PROJECTIONS.json` (nearest artefact) | Shows three host projections (`host:generic-skills`, `host:hgk-receiver`, `host:genie-adapter`), `host_count "3/3"`, `live_status NOT_RUN`, `adapter_checks "FIXTURE_MOCK_ONLY"`. This is the **host projection manifest**, not an `ADAPTER_REGISTRY@1`; no adapter-registry object is materialised. | **OPEN — NOT ADJUDICATED (object absent)** |

---

## 3. Rows I could NOT adjudicate, and why

Four of the ten active rows have **no materialised artefact to open**. Each is a row whose object is
declared absent by the crosswalk's own `first_fail`, and none has a dedicated closure receipt. I am
reporting them OPEN rather than stretching a nearby-but-different artefact over them:

1. **`PIPD-SP-SPEC-002`** — needs a materialised `PIPD-LIFECYCLE-SPEC@1.1.0` SSOT object. It exists
   only as a retrieval hit (`SRC-a751a9e9…`) and as text in contract/knowledge files. No object.
2. **`PIPD-SP-SPEC-030`** — needs an MCP materialization object. The repo holds only a
   technology-admission *design* row (CAND-06, `DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED`).
3. **`DEL-004`** — needs `SPEC_REGISTRY@1`. Absent; `schemas/registry.json` is a *contract* registry,
   a different deliverable, and must not stand in for it.
4. **`DEL-015`** — needs `ADAPTER_REGISTRY@1`. Absent; only host projections exist
   (`HOST_PROJECTIONS.json`).

**Adjudicated: 6 of 10. Not adjudicated (still open by absence): 4 of 10.**

Note on `DEL-018`: it *is* adjudicated because a dedicated closure receipt exists — but the receipt
binds the published release subject, not this `main` worktree, so the row is still OPEN here.

---

## 4. What this audit does NOT claim
- No active row is a PASS. All ten remain `EVIDENCE_GAP`.
- The 28 evidenced rows were **not** re-run row-by-row (out of this audit's scope); only the 10
  active rows were opened individually.
- The crosswalk, its generator, schemas and validators were read-only throughout.
