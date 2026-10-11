# pipd-s4r2m-conditional-merge

## ADDED Requirements

### Requirement: The front page routes a reader to exactly one of two consumer paths
The system SHALL present, on the front page, a short section that lets a reader choose between the CLI
path and the Skills path, and SHALL state for each path what the reader actually receives and what the
path does not confer.

#### Scenario: A reader who wants a command-line harness
- **WHEN** a reader selects the CLI path
- **THEN** the page names the immutable wheel and its published digest, requires a Python runtime and a
  virtual environment, and states explicitly that installing the wheel does not load the eight logical
  skills into a web host

#### Scenario: A reader who wants document consumption
- **WHEN** a reader selects the Skills path
- **THEN** the page names the versioned document pack and its digest, distinguishes manual
  document/Knowledge attachment from a host-native skill load, and does not present a manual attachment
  as a native effective-load

### Requirement: The `--root` description matches the shipped command-line surface
The system SHALL describe option placement in the front page only to the extent the shipped parser
behaves that way, and SHALL NOT generalise a correct statement about some subcommands into a rule
about all of them.

#### Scenario: A documented positive form is one the CLI accepts
- **WHEN** a reader copies a documented `--root` form
- **THEN** the form is one that exits 0, and the page states which subcommands additionally accept the
  subcommand-local position

#### Scenario: A form the CLI refuses is not documented as working
- **WHEN** the round verifies a `--root` placement the parser does not accept
- **THEN** the run exits non-zero as a typed usage error and the documentation does not claim otherwise

### Requirement: A regression of the frozen candidate runs on a copy, never on the read-only subject
The system SHALL run any suite that writes into the tree against a disposable writable clone of the
frozen candidate, and SHALL compare the read-only subject's bytes before and after the run.

#### Scenario: The subject is unmodified
- **WHEN** the affected modules finish in the clone
- **THEN** the read-only subject's file set and digests are identical to the values taken before the run

#### Scenario: The exact set is unchanged
- **WHEN** the schemas and registry, the logical skill directories and the CLI command set are counted
- **THEN** they are 19, 8 and 13 respectively, with no additions

### Requirement: A maker measurement and an independent verdict are reported separately
The system SHALL keep the maker's suite figure, the compiler's gate verdict, the checker's verdict and
the merge/release state as four distinct claims with their own evidence.

#### Scenario: No claim is rounded up
- **WHEN** the round reports its result
- **THEN** a compiler PASS is not reported as runtime readiness, a green maker suite is not reported as
  independent acceptance, and an integration is not reported as a release

### Requirement: An unselected release gate produces no artefact
The system SHALL create a `preview.3` tag, wheel or release asset only after an explicit owner
selection, and SHALL record a deferral otherwise.

#### Scenario: The owner defers
- **WHEN** the owner does not select the release gate
- **THEN** the round records `PREVIEW3_DEFERRED`, creates no tag and no draft release, and leaves the
  public `v0.1.0-preview.2` served unchanged

#### Scenario: The owner selects the release gate
- **WHEN** the owner selects a new preview distribution
- **THEN** the distribution carries a PEP 440 version strictly greater than the installed `0.1.0`, the
  mount pack is separately downloadable, and the round reads the published bytes back anonymously
