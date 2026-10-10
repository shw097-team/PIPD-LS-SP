## ADDED Requirements

### Requirement: The validator resolves schemas the same way the doctor does

`validate` SHALL resolve the canonical schema set through the same mechanism `doctor` uses, so that both
commands agree about where the schemas live, and SHALL report the source it actually resolved.

#### Scenario: an installed wheel is validated from an unrelated directory

- **WHEN** the wheel is installed into a clean environment and `validate` is run from a directory that
  contains no `schemas/` directory and no `--root`
- **THEN** the schemas shipped inside the installed package are used, `validate` reaches a verdict, and
  the reported schema-source mode is `INSTALLED`
- **AND** it does not fail with a missing-file error naming `<cwd>/schemas/PI-PKG.schema.json`

#### Scenario: a workspace carrying its own schemas still wins

- **WHEN** `--root` points at a directory whose `schemas/` contains `registry.json`
- **THEN** that directory's schemas are used in preference to the packaged copy
- **AND** a `schemas/` directory without `registry.json` does not shadow the packaged set

### Requirement: The validator accepts the toolchain's own unmodified output

A validation bundle assembled from the four compilers' unmodified stdout SHALL be accepted, because the
non-record sidecars the pipeline attaches are declared to be stripped before schema validation.

#### Scenario: the compiler output is validated without hand-editing

- **WHEN** a bundle is assembled from the raw output of `compile-pi`, `bind-pd`, `compile-ecp` and
  `compile-tqaep` and passed to `validate`
- **THEN** the verdict is `PASS` with four records checked and no findings
- **AND** the caller did not have to delete `_profile_meta` or otherwise edit the artefacts

#### Scenario: a body edited without re-issuing identity is still caught

- **WHEN** a release-bound record's body is modified without recomputing `content_hash`
- **THEN** validation still reports that the `content_hash` does not match the record body

### Requirement: The non-record sidecar set has exactly one definition

The set of keys treated as non-record sidecars SHALL be defined once and consumed by every code path that
needs it, so the definitions cannot drift apart.

#### Scenario: a consumer reads the sidecar set

- **WHEN** the pipeline and the validator refer to the sidecar set
- **THEN** they refer to the same object rather than to two hand-written copies

### Requirement: The published tag is not rewritten by a repair

A repair SHALL NOT alter the bytes of an already-published tag or release.

#### Scenario: the repair is delivered

- **WHEN** the repair lands
- **THEN** the published tag, its commit, its tree and its wheel bytes are unchanged, and the repair is a
  candidate for a superseding release issued by the owner
