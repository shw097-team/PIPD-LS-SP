# pipd-s0-s4-audit-repair

## ADDED Requirements

### Requirement: exact contract reconciliation
The system SHALL make every one of the 19 S0 machine-contract families exactly equal to its registry
declaration: `registry.required_fields == schema.required`, matching `$id` version, owner and
consumer, with the seam-only families still declared seam-only.

#### Scenario: an extra required field is rejected
- **WHEN** a schema declares a required field the registry does not list
- **THEN** the S0 contract test fails with the offending field named.

### Requirement: the eight logical SkillContracts exist
The system SHALL materialise `skills/pipd-route-intake`, `pipd-authority-source`, `pipd-profile-tailor`,
`pipd-pi-compile`, `pipd-pd-bind`, `pipd-execution-contract`, `pipd-assurance-tqaep` and
`pipd-package-project`, each with a `SKILL.md`, `references/contract.md`, `references/examples.md`,
`schemas/input.schema.json`, `schemas/output.schema.json` and `tests/cases.yaml` carrying POS/NEG/EDGE/SEC
cases with first-fail expectations.

#### Scenario: a marker-only skill directory is rejected
- **WHEN** a scanned skill contains only a free-text file and no input/output schema
- **THEN** the skill-pack check fails that skill with a typed reason.

### Requirement: the Web denominator is the five PIPD semantic documents
The system SHALL emit `PIPD_BOOTSTRAP.md`, `PIPD_CANONICAL_CORE.md`, `PIPD_ROUTER_PROFILES.md`,
`PIPD_ARTIFACT_SCHEMAS.md` and `PIPD_EVAL_HANDOFF.md` with source hashes and a capability-loss
record; site UI files are `OPTIONAL_SITE_UI` and SHALL NOT satisfy the Web gate.

#### Scenario: a UI-only pack cannot pass
- **WHEN** only `index.html`, `app.js`, `styles.css`, `manifest.webmanifest` and `README.md` are present
- **THEN** the Web gate fails and names the five missing documents.

### Requirement: the three host adapters perform a real effective load
The system SHALL produce `generic-skills`, `hgk-receiver` and `genie-adapter` projections carrying
field-level contracts, source references, compatibility and capability-loss, and an effective-load
result that a marker-only stub cannot satisfy.

#### Scenario: a marker stub is rejected
- **WHEN** a host file contains only a surface marker with no contract fields
- **THEN** the host projection check fails that host.

### Requirement: atomic requirement compilation
The system SHALL compile a clause-bound atomic requirement IR with stable IDs, source clause,
owner, acceptance cue and distinct oracle/fixture per atom, and SHALL reject semantic collapse of
distinct clauses that share keywords.

#### Scenario: compound clauses do not collapse
- **WHEN** an input contains two distinct clauses that share keywords
- **THEN** two distinct requirement atoms with distinct source clauses are produced.

#### Scenario: a negation is not dropped
- **WHEN** a clause states a prohibition
- **THEN** the atom records a MUST NOT polarity rather than the opposite positive requirement.

### Requirement: PD binds to the real repository context
The system SHALL derive `bind_pd`'s `head`, `tracked_files`, dirty state and `currentness` from the
repository/host itself, treating caller-provided values as claims, and SHALL reject a stale or
spoofed freshness claim.

#### Scenario: a caller-supplied FRESH is rejected
- **WHEN** the caller asserts `currentness: FRESH` while the repository context disagrees
- **THEN** the binder fails with a typed staleness error.

### Requirement: evidence is bound and sealed
The system SHALL produce an evidence manifest that excludes its own entry, carries an outer
immutable seal, and binds every gate to one candidate tuple
(`source_digest, commit_SHA, candidate_bytes, evidence_manifest_SHA, policy_version, checker_id,
runner_digest, stage`).

#### Scenario: a self-referential manifest is rejected
- **WHEN** the manifest contains an entry for its own path
- **THEN** the sealing check fails.

#### Scenario: foreign evidence is rejected
- **WHEN** a receipt belongs to another candidate head
- **THEN** the gate refuses it.

### Requirement: PRE-W3 remains independently closed
The system SHALL keep the PRE-W3 cross-project subject `TEMP_CLOSED` and SHALL NOT derive its
acceptance from S0–S4 evidence.

#### Scenario: no promotion from local evidence
- **WHEN** the S0–S4 programme reports success
- **THEN** PRE-W3 still reports `TEMP_CLOSED` with its own owner and prerequisites.
