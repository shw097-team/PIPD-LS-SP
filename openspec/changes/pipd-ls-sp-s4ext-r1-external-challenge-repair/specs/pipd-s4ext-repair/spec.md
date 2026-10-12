# pipd-s4ext-repair

## ADDED Requirements

### Requirement: Package release identity is frozen as two separate fields

Every versioned mount-pack document SHALL name both the build-source commit and the release-tag
target, taking both values from a frozen release tuple, and SHALL NOT describe a single commit as
"the tag commit".

#### Scenario: current identity is re-derived, not trusted

- **WHEN** a verifier compares each of the eight pack documents with the frozen tuple and the local
  `git rev-parse <tag>^{commit}` read-back
- **THEN** all eight documents name the tuple's `release_tag_target`, and no document names the
  tuple's `build_source_commit` as the tag target except on a line explicitly marked as a disclosure.

#### Scenario: a stale identity is refused

- **WHEN** a pack document names the superseded commit as the current release identity outside a
  disclosure line
- **THEN** the provenance check fails and the pack is not treated as current.

#### Scenario: the published asset is not rewritten

- **WHEN** the correction is prepared
- **THEN** the published ZIP's bytes and digest are unchanged, and the corrected pack is published as
  a new file with its own digest and an erratum document.

### Requirement: Trace endpoints are typed and bundle closure is part of validation

A trace link SHALL constrain its endpoints to non-blank identifiers and 64-hex hashes within the
declared artifact families, and `validate --bundle` SHALL report whether the bundle's trace graph
closed, failed to close, or was never present.

#### Scenario: a legal bundle closes

- **WHEN** a bundle containing a legal PI/PD/ECP/TQAEP chain (legacy `version="1"` included) is
  validated
- **THEN** the verdict is PASS and the closure state is FULL.

#### Scenario: a tampered trace bundle is refused

- **WHEN** a bundle's trace endpoint is mis-typed, points at a subject absent from the bundle, or
  carries a hash that does not match its endpoint
- **THEN** the verdict is FAIL with closure FAILED and the command exits non-zero.

#### Scenario: a partial bundle states what it is

- **WHEN** a bundle contains no trace edges
- **THEN** the closure state is SCHEMA_ONLY and no trace-closed claim is made.

### Requirement: The current release is pinned by a test, not by a branch

A regression test SHALL derive the release identity from the frozen tuple and SHALL fail when a
document, the tuple, or the local tag dereference disagree.

#### Scenario: floating references are not used

- **WHEN** the provenance test runs
- **THEN** no assertion depends on a branch tip or a network reference.

### Requirement: The compiler chain is runnable by a new user without author paths

The repository SHALL provide first-run entry points that derive every path from their own location,
verify their preconditions, execute the full compiler chain, demonstrate a typed refusal, and report
success only when all of those behaved.

#### Scenario: a precondition failure halts

- **WHEN** no usable interpreter is available
- **THEN** the runner prints `PRECONDITION_FAIL` with a typed reason and exits non-zero without
  writing a partial artefact.

#### Scenario: the chain completes portably

- **WHEN** a new user runs the entry point from a directory outside the checkout
- **THEN** the chain completes, `validate` reports PASS with closure FULL, and the final line is
  `FIRST_RUN_OK`.

### Requirement: Profile computation refuses malformed requests and never mints an approval

`compute_profile` SHALL raise a typed refusal for a malformed request (including a non-string profile
name), SHALL keep its escalation conservative when several triggers fire at once, and SHALL NOT emit
any approval or acceptance field.

#### Scenario: a non-string request is refused

- **WHEN** the requested profile is not a string
- **THEN** a typed `ProfileVeto` is raised and no native `AttributeError` escapes.

### Requirement: The SPEC/DEL crosswalk is adjudicated without being rewritten

A per-row adjudication SHALL exist for every row the crosswalk does not mark EVIDENCED, SHALL leave
the crosswalk's own status and oracle fields untouched, and SHALL NOT present `EVIDENCED` as a pass.

#### Scenario: a new gap cannot be dropped

- **WHEN** a row becomes an EVIDENCE_GAP without an adjudication entry
- **THEN** the adjudication generator fails rather than emitting a default.

#### Scenario: a stage-deferred row is not called blocking

- **WHEN** a row's stage spans a later stage gate
- **THEN** it is recorded as out of this round's scope rather than as S4-blocking.
