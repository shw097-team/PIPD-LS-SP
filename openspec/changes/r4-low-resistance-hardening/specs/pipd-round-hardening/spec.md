# pipd-round-hardening

## ADDED Requirements

### Requirement: Preflight asserts the execution substrate before model time is spent
The system SHALL provide a single preflight entry point that verifies the execution substrate the round
depends on and records one machine-readable verdict, failing non-zero only for facts the round cannot run
without.

#### Scenario: An expected HEAD mismatch fails the preflight
- **WHEN** the preflight is given `--expect-head` and the repository HEAD differs
- **THEN** the `git_head` check reports `FAIL` and the process exits non-zero

#### Scenario: A degraded substrate is recorded, not treated as a defect
- **WHEN** the docker daemon is unreachable or the codex sandbox helper reports its setup error
- **THEN** the corresponding check reports `WARN` with a named reason and the preflight still exits zero

#### Scenario: Model drift between the config file and the pinned model is reported
- **WHEN** the model recorded in the codex config file differs from the model passed to the preflight
- **THEN** a `CONFIG_DRIFT` warning is emitted whose detail states that the run must pin its model explicitly

### Requirement: A verifier runs only inside a disposable envelope
The system SHALL run acceptance inside a disposable byte-copy of the candidate, with scratch outside the
tested tree, and SHALL assert afterwards that the product tree's HEAD and dirty count are unchanged.

#### Scenario: A modified or removed file fails the boundary check
- **WHEN** the after-snapshot shows a tracked file modified or removed
- **THEN** the verification reports the classified delta and exits non-zero

#### Scenario: A mandated addition is not reported as drift
- **WHEN** an added path matches an allow-rule supplied by the round
- **THEN** the added set is reported separately and the check exits zero

#### Scenario: A scratch root inside the tested tree is refused
- **WHEN** `--scratch` resolves inside the source or the copy
- **THEN** the command refuses with a non-zero exit

### Requirement: The round self-scans its own text before acceptance
The system SHALL scan the round's own new text for credential shapes and deny-list usage before
acceptance and SHALL refuse to proceed on a hit.

#### Scenario: A credential-shaped string is detected without echoing it
- **WHEN** a scanned file contains a credential-shaped token
- **THEN** the scan reports a hit with a redacted shape label, never the raw value, and exits non-zero

#### Scenario: The scanner's own source carries no literal credential shape
- **WHEN** the scanner's source is scanned
- **THEN** no hit is reported, because the patterns are assembled from fragments at runtime

#### Scenario: A clean round passes
- **WHEN** every scanned file is free of credential shapes and deny-list usage
- **THEN** the verdict is `PASS` and the process exits zero
