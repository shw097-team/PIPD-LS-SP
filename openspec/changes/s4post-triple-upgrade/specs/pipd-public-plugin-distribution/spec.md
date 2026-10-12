# pipd-public-plugin-distribution

## ADDED Requirements

### Requirement: The plugin package carries the official manifest at its root
The system SHALL emit, as the package-root `plugin.json` inside the plugin archive, a manifest that
validates against the byte-locked Agent Plugins 1.0 vendor schema, and SHALL carry its own release
bookkeeping in the vendor-blessed `extensions` namespace rather than as top-level keys.

#### Scenario: An unknown top-level key is refused
- **WHEN** the official-shaped manifest carries a key outside the vendor schema's permitted set
- **THEN** the build exits non-zero with a typed manifest-schema refusal and writes no archive

#### Scenario: The locked vendor schema digest disagrees with the bytes
- **WHEN** the digest pinned in the manifest does not match the bytes of the local vendor schema copy
- **THEN** the build refuses with a typed vendor-schema-digest refusal

### Requirement: The projection is byte-exact or owner-approved, never silent
The system SHALL copy every non-SKILL source member byte-exactly and SHALL only project a `SKILL.md`
when an owner-approved derivation record exists whose `source_sha256` matches the frozen ledger,
leaving the skill body byte-identical.

#### Scenario: A skill without a derivation record
- **WHEN** the build runs with an empty `derivations.json`
- **THEN** it exits non-zero naming the first skill, in canonical order, that lacks an owner-approved
  record, and no archive is produced

#### Scenario: An approved derivation keeps the body
- **WHEN** a complete owner record is supplied for a skill whose frontmatter carries non-portable keys
- **THEN** the projected `SKILL.md` keeps the body byte-identical, moves only the approved keys, and the
  source-to-plugin mapping marks that row `DERIVED_WITH_OWNER_APPROVAL`

### Requirement: Two builds from identical inputs are byte-identical
The system SHALL write the archive with fixed metadata and SHALL read every member back before
promoting it into place.

#### Scenario: Determinism across two output roots
- **WHEN** the same frozen ledger, manifest, schema, derivations and icons are built twice into
  different output roots
- **THEN** both archives have the same member set, the same member order and the same sha256

### Requirement: The single-document Web fallback is complete or refused
The system SHALL emit exactly one markdown document that embeds every source member verbatim with its
digest, stamps the `DOC_MOUNT_ONLY` ceiling and the member inventory, and SHALL refuse rather than
truncate when the result would exceed the cap.

#### Scenario: The output exceeds the cap
- **WHEN** the composed document would be larger than the approved maximum
- **THEN** the export exits non-zero and the destination file does not exist

#### Scenario: A source member is stale or not text
- **WHEN** a member's digest disagrees with the manifest, or a member is not UTF-8 text, or a document
  does not stamp both the release id and the pinned commit
- **THEN** the export refuses with a typed reason

### Requirement: The install surface is exactly two routes
The system SHALL document one Web route and one Agent route, SHALL state that no public directory
listing exists while the Web route is the fallback, and SHALL keep build, portal, publication, host
qualification and S4 acceptance as separate states.

#### Scenario: A reader looks for the install entry point
- **WHEN** a reader opens the repository front page
- **THEN** only the two routes are presented at the top level, with recovery and version pinning below

### Requirement: The verification workflow fails closed on its negative step
The system SHALL run the packaging and fallback suites in a read-only workflow and SHALL fail the run
unless the mutation produces an actual failure whose motive is the identity or byte binding.

#### Scenario: The negative step is satisfied by an unrelated error
- **WHEN** the mutation step is satisfied only by a non-zero exit, an import error or a deleted module
- **THEN** the step reports failure, because the motive check did not observe the binding failure
