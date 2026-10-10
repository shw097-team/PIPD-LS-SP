# pipd-s4-post-challenge-repair

## ADDED Requirements

### Requirement: The environment diagnostic covers the resources the CLI actually loads
The system SHALL diagnose the schema resources that the command-line resolver selects at run time,
not only the workspace-local `schemas/` convention, and SHALL report which surface (override,
installed package, or source tree) was inspected.

#### Scenario: An installed wheel missing a packaged schema is a typed failure
- **WHEN** a wheel whose packaged `schemas/` is missing one `<Family>.schema.json` member — with the
  zip RECORD left unchanged, or adjusted in step — is installed into a disposable virtual environment
  and `pipd doctor` is run from a healthy workspace
- **THEN** the command exits non-zero with `verdict = FAIL` and a finding that names the missing family
  and the inspected schema root

#### Scenario: A healthy environment reports 19 of 19 on both surfaces
- **WHEN** `pipd doctor` runs against a healthy source tree and against a healthy installed wheel
- **THEN** the verdict is `PASS`, the family count is 19, and the report names the resolution mode as
  `SOURCE` or `INSTALLED` respectively

#### Scenario: No silent fallback masks an incomplete install
- **WHEN** the resolved schema root is incomplete
- **THEN** the diagnostic does not fall back to another copy of the schemas to produce a `PASS`

### Requirement: Round evidence is bound to one frozen candidate subject
The system SHALL bind every raw receipt of a repair round to a single immutable candidate tuple
(commit, tree, product digest, wheel digest), and SHALL NOT present a previous round's attestation or
verdict as the current round's receipt.

#### Scenario: A new subject is published
- **WHEN** the round's product changes are frozen
- **THEN** the new commit, tree and product digest are recorded together with the wheel digest, and the
  previous attestation subjects are listed as historical, different tuples

#### Scenario: A mutation of the subject invalidates the receipt
- **WHEN** the frozen candidate bytes change after a receipt was issued
- **THEN** the receipt is invalid and is not reused

### Requirement: Wheel mutation ends in a typed failure, never a silent success
The system SHALL treat a wheel whose packaged Python or schema members were mutated or truncated as a
typed integrity failure at the surface the user invokes.

#### Scenario: A truncated Python member cannot silently pass
- **WHEN** a packaged Python member is truncated
- **THEN** the failure is reported as a typed integrity/start failure rather than only as an interpreter
  traceback, and no command reports `PASS`

#### Scenario: A removed schema member is refused after install
- **WHEN** a packaged schema member is removed and the wheel is reinstalled
- **THEN** the diagnostic gate refuses typed and the environment is not reported healthy

### Requirement: The per-atom context gate resists obligation dilution
The system SHALL evaluate the per-atom context budget against a denominator of unique validated
obligations, and padding a payload with filler or duplicate atoms SHALL NOT reduce the measured
per-obligation cost below the gate.

#### Scenario: Filler cannot turn an over-budget payload green
- **WHEN** an over-budget payload is padded with repeated or semantically empty atoms
- **THEN** the gate still reports the payload as over budget, or reports the padding as an invalid
  measurement, and never as `PASS`

#### Scenario: The historical failure row is preserved
- **WHEN** the gate report is produced
- **THEN** the historical `343547 > 20000` failure remains present and unmodified in the historical
  section, alongside the current objective and its denominator

### Requirement: The design-time TQAEP positive path is exercisable
The system SHALL compile a legal design-time TQAEP candidate whose claim ceiling is
`TQAEP_DESIGNED`, and SHALL NOT derive an independent acceptance from a receipt string.

#### Scenario: A legal design candidate compiles
- **WHEN** a caller supplies a PI plus a checker identity distinct from the maker
- **THEN** `pipd compile-tqaep` produces a design contract with `ClaimCeiling = TQAEP_DESIGNED`

#### Scenario: Separation-of-duties negatives still refuse
- **WHEN** the receipt is missing, marked `SELF_ATTESTED`, or the checker aliases the maker
- **THEN** the command refuses typed with a non-zero exit and no independent-pass artifact is produced

### Requirement: The README first screen states the current stage and rights position
The system SHALL make the README's first screen unambiguous about which branch is current, which entry
point documents acceptance, and that no public-use grant is given, without rewriting historical
receipts.

#### Scenario: A reviewer reading only the first screen can tell the stage
- **WHEN** the README's opening section is read in isolation
- **THEN** the historical snapshot is labelled, the current branch and `ACCEPTANCE.md` entry point are
  named, and the internal-evaluation license position is visible
