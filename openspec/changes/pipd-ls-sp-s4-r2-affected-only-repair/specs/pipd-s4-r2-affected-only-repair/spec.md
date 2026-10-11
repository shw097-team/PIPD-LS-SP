# pipd-s4-r2-affected-only-repair

## ADDED Requirements

### Requirement: A reaudit finding is closed only on freshly executed positive and negative evidence
The system SHALL treat a reaudit finding as closed only when this round has executed both a positive
case and its matching negative case against the candidate subject, and SHALL record the probe — not
the report — as the thing that failed whenever a probe itself was defective.

#### Scenario: An already-closed finding is proven, not asserted
- **WHEN** a finding is claimed to be closed by the existing candidate
- **THEN** the round ships the executed positive case, its executed negative case, the raw exit codes
  and the exact command, and does not substitute file presence for behaviour

#### Scenario: An open finding is closed by a minimal change
- **WHEN** a finding is still genuinely open
- **THEN** only the smallest change that makes its counterexample fail is admitted, with a regression
  over the affected dependency edges

### Requirement: The front page never shows a placeholder as a runnable example
The system SHALL present a first-run walk-through whose commands can be copied literally, whose inputs
exist in the tree, and which SHALL NOT ship `<placeholder>` tokens in a runnable block.

#### Scenario: The compiler walk-through is replayable
- **WHEN** a reader copies the documented `intake -> compile-pi -> bind-pd -> compile-ecp ->
  compile-tqaep -> validate` sequence
- **THEN** the referenced fixture exists, every step exits 0 with a verifiable trace or digest, and a
  second run reproduces the same digests

#### Scenario: A missing or forged source is refused
- **WHEN** the source locator does not exist, or a receipt is claimed without a source
- **THEN** the step fails with a typed error and no artefact is written

### Requirement: Distribution identity hazards are stated, not implied
The system SHALL state that the `.1` and `.2` preview artefacts share the `0.1.0` distribution basename
while differing in bytes, and SHALL require PEP 440 ordering to be checked against an already-installed
`0.1.0` before any upgrade is claimed.

#### Scenario: A version claim is checked
- **WHEN** a future preview version is proposed
- **THEN** the round states whether it orders strictly greater than `0.1.0` under PEP 440 before
  claiming that pip will upgrade

### Requirement: Contract fields a decision rides on are typed
The system SHALL declare JSON types for the universal identity fields and for any contract field that a
refusal decision depends on, so that a wrongly-typed value is a typed first failure rather than a
silently accepted record.

#### Scenario: A wrongly-typed contract field is refused
- **WHEN** a record carries `axes` as a string or a list containing a non-string, or `profile` as an
  integer
- **THEN** validation fails with a typed violation naming the field

#### Scenario: Legal records do not regress
- **WHEN** every legal PI/PD/ECP/TQAEP record and the 19-schema exact set are validated
- **THEN** they still pass, and the PD/ECP/TQAEP stray-trace refusals from the earlier repair survive
