## ADDED Requirements

### Requirement: One recorded owner licence grant

The repository SHALL carry exactly one operative licence decision, recorded in a machine-readable slot,
and every licence surface SHALL agree with it. The superseded decision SHALL be preserved rather than
rewritten or back-dated.

#### Scenario: a reader opens the licence surfaces

- **WHEN** a reader opens `LICENSE`, `NOTICE`, `OWNER_LICENSE_DECISION.yaml`, `pyproject.toml` and
  `SBOM.cdx.json`
- **THEN** all of them name `Apache-2.0` as the project licence, the previous non-granting decision is
  still readable inside the decision slot with its own date, and no surface still presents the repository
  as unlicensed

#### Scenario: a third-party component is listed

- **WHEN** the SBOM lists the `jsonschema` runtime dependency
- **THEN** that component carries its own `MIT` licence, not the project's licence

### Requirement: The granted licence travels with the binary

The built distribution SHALL carry its own licence text and attribution, and SHALL declare its licence in
its metadata, so the grant is verifiable from the installed artefact alone.

#### Scenario: an installed wheel is inspected

- **WHEN** the published wheel is opened and its metadata is read
- **THEN** the metadata declares the SPDX licence expression and the licence files, and the licence text
  and notice are present inside the distribution metadata directory

### Requirement: Build identity is not disguised as release identity

The distribution manifest SHALL record the commit its bytes were built from separately from the commit the
release resolves to, and SHALL NOT present an older build identity as the current release subject.

#### Scenario: a verifier compares identities

- **WHEN** a verifier reads the wheel manifest and the publication binding
- **THEN** the build-input commit and the released commit are distinguishable values, the superseded wheel
  hash is explicitly not claimed for the new artefact, and the legacy candidate-head field is labelled as
  the historical source identity it is

### Requirement: A single unambiguous distribution entry point

The published preview SHALL have one entry point — an immutable tag — and repository-facing text SHALL
direct readers to it rather than to the historical default branch.

#### Scenario: a reader arrives from the release page

- **WHEN** a reader opens the README or the acceptance file at the release commit
- **THEN** the first screen names the preview tag as the distribution entry point, states that the default
  branch is the historical snapshot, and links the licence, the grant record and the known limitations

### Requirement: Disclosed known limitations are part of the release

The preview SHALL publish its known limitations, including the open release-manifest evidence gap and the
deferred stages, and SHALL NOT present them as closed.

#### Scenario: the release notes are read

- **WHEN** a reader opens the preview notes
- **THEN** they find the release-manifest gap named with its uncovered test paths, the recorded SPEC/DEL
  denominator, the un-certified platform edges, the absence of install-time cryptographic readback, the
  deferred stages, and an explicit statement that production verification is not claimed

### Requirement: Credential hygiene during publication

Publication SHALL use the owner credential only inside process memory, and no output of the round —
evidence, logs, manifests, prompts, URLs or assets — SHALL contain its value.

#### Scenario: the evidence set is audited

- **WHEN** the round's evidence set is scanned for credential patterns
- **THEN** no token value is found, and the credential file's own path is the only reference recorded

### Requirement: Independent verification of the published subject

An independent checker distinct from the maker SHALL re-derive the decisive claims from the published
bytes, read-only, and the maker SHALL NOT issue the independent verdict.

#### Scenario: the checker reports

- **WHEN** the independent checker completes
- **THEN** its verdict names what it re-derived itself (download hashes, install, command chain, licence
  coverage), what it could not re-derive, and the bounded claim it does and does not support
