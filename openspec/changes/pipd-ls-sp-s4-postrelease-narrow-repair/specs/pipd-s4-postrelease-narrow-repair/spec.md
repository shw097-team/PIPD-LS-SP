# pipd-s4-postrelease-narrow-repair

## ADDED Requirements

### Requirement: The published quickstart verifies only artefacts it downloaded
The system SHALL present an onboarding path whose checksum step can succeed from the files that step
actually fetched, on both a POSIX shell and PowerShell, and SHALL NOT present a convenience install as
a cryptographic verification.

#### Scenario: A verbatim copy-paste succeeds from an empty directory
- **WHEN** a first-time user copies the README quickstart line by line into an empty directory outside
  the repository on bash, and again on PowerShell
- **THEN** every line exits 0, the wheel's digest equals the published SHA-256, `pipd doctor` reports
  the resolved schema source, and no line attempts to read a file it did not download

#### Scenario: A mutated or missing artefact is a typed failure
- **WHEN** one byte of the downloaded wheel is altered, or the release URL is wrong, or the interpreter
  is older than 3.11
- **THEN** the check exits non-zero with a message naming the failure, and no step reports success

#### Scenario: The convenience install is labelled as unverified
- **WHEN** the README offers a one-line wheel install
- **THEN** that section states that no hash verification was performed and is not presented as the
  secure path

### Requirement: One self-describing Web/ChatGPT mount package exists
The system SHALL publish exactly one versioned mount package containing a one-page dispatcher skill, its
reference documents, a starter prompt and a manifest, and SHALL describe the native skill-upload path
and the manual-attachment path as distinct capabilities.

#### Scenario: The package is complete and hash-recomputable
- **WHEN** the published ZIP is extracted
- **THEN** every manifest entry is present, every file digest recomputes to its recorded value, and
  every document carries a source locator and the release identity it is bound to

#### Scenario: Capability limits are stated, not implied
- **WHEN** the mount documentation describes what the host can do
- **THEN** tool execution, repository writing, CLI invocation, HITL authority and network access are
  each marked available or `NOT_AVAILABLE`, and the pack never claims the host executed an external tool

#### Scenario: The five consumer cases are recorded
- **WHEN** the consumer UAT runs
- **THEN** it records a positive compile trigger, a negative small-talk case, a missing-context
  refusal, a privilege-escalation/self-PASS refusal and a first-time mount, each with raw output, and
  records `NOT_SUPPORTED` where the native upload path could not be exercised

### Requirement: Universal identity and trace fields carry a machine-enforced JSON type
The system SHALL declare a JSON type for `subject_id`, `version`, `content_hash` and `schema_version`
in every family that declares them, and SHALL declare the PI `trace` relation as an array of trace
links, without changing the family set, the required-field lists or the closed-property stance.

#### Scenario: A wrongly-typed identity is refused at the schema layer
- **WHEN** a record supplies an integer or null `subject_id` or `version`, or a `content_hash` that is
  not a 64-character lowercase hex digest
- **THEN** validation reports exactly one first-fail finding naming the contract and the JSON pointer,
  and no `str()` coercion converts the integer into an acceptable identifier

#### Scenario: An undeclared trace stays refused
- **WHEN** a `trace` property is supplied on a family that does not declare it, or the PI `trace` is a
  string or null instead of an array of trace links
- **THEN** the record is refused typed

#### Scenario: Existing legal records still validate
- **WHEN** the compiler's own legal PI/PD/ECP/TQAEP outputs and the CE-1/CE-2 regression bundles are
  validated
- **THEN** they still pass, and the registry still reports the exact same family set

### Requirement: Profile selection fails closed and never implies a risk assessment
The system SHALL refuse duplicate, non-string, empty and unknown profile axes with typed errors, SHALL
derive the escalation decision and the emitted binding from the same normalised axis list, and SHALL
NOT present an axis count as a risk score.

#### Scenario: Duplicate axes are refused
- **WHEN** the same axis is supplied more than once
- **THEN** the selector refuses typed and no profile record is emitted, so the escalation basis and
  the record can never disagree

#### Scenario: An absent risk assessment is stated as absent
- **WHEN** a profile is computed without risk evidence
- **THEN** the emitted record marks the risk assessment as not assessed, and no low-risk or verified
  risk verdict is produced without evidence

### Requirement: The normative source identity is pinned, not copied
The system SHALL publish a derived index that records, per source family, the owning authority, the
version, a hash or an explicit non-public marker, and the consumers, and SHALL state that the external
canonical standard remains the single source of truth.

#### Scenario: The index points at the canonical owner
- **WHEN** the index is read
- **THEN** it names the external canonical standard as the SSOT, marks the index itself as derived, and
  contains no copy of the normative bodies

#### Scenario: A minimal self-bootstrap replays
- **WHEN** the documented self-bootstrap commands run with the shipped CLI into an isolated root
- **THEN** the recorded artefacts and digests are reproduced, a source-missing or stale-context input
  is refused, and the transcript is recorded from a real run rather than a hand-written expectation
