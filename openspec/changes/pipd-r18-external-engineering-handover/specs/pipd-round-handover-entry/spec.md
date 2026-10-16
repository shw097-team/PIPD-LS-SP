# pipd-round-handover-entry

## ADDED Requirements

### Requirement: Round plan documents must agree with round evidence

A round that produces a task checklist and a detection checklist SHALL back-fill their status and
evidence columns before the round closes, so that a reader opening the plan cannot conclude the round
was never executed. A row that was not run SHALL say `NOT_RUN`; a row that requires an owner action
SHALL say `OWNER GATE`; a row that was deliberately deferred SHALL say `DEFERRED`. No row SHALL
remain in the unstarted state at close, and every cited evidence identifier SHALL resolve to an
artifact that exists in the round's evidence set.

#### Scenario: a reader opens the plan before the packet

- **WHEN** a verifier reads the task or detection checklist and then the evidence packet
- **THEN** the two agree on every row's status
- **AND** no row reports unstarted work whose artifact exists, or completed work whose artifact is absent

#### Scenario: an evidence identifier does not resolve

- **WHEN** a checklist row cites an evidence identifier that does not exist in the evidence set
- **THEN** the round reports that row as a defect rather than counting it as satisfied

### Requirement: An external engineering team can continue development from one entry document

The round SHALL publish a single entry document for external engineers that covers the repository and
branch model, the governed write-set gate and its local reproduction, the lane model including any
owner-ordered arm collision, the build and test commands, a module map with extension points, the open
tickets with owner gates, and the standing prohibitions. Every factual claim in it SHALL be
reproducible by a named command or verifiable at a named file locator.

#### Scenario: a newcomer reproduces a claim

- **WHEN** a reader who has never seen the repository follows one of the document's commands in a fresh clone
- **THEN** the command runs and its result matches what the document states, or the document states why the environment differs

#### Scenario: the document asserts something unverifiable

- **WHEN** an independent check finds a factual claim with no command and no file locator
- **THEN** the claim is reported as a defect against the document, not accepted as prose

### Requirement: Round artifacts stay outside the governed product write set

The round's own artifacts SHALL be published on the evidence branch and SHALL NOT be committed to the
product branch, because the product repository's write-set gate admits enumerated product paths only.
A path the round's work order does name and the declared arm omits SHALL be added only as a single
named amendment, mirrored in that arm's planted-path self-test, and disclosed in the pull request.

#### Scenario: a round artifact is placed on the product branch

- **WHEN** the product branch's write-set classifier is run against the declared base
- **THEN** it reports the round artifact outside the allowed set, and the correct response is to move the artifact rather than to widen the arm

#### Scenario: the work order names a file the arm omits

- **WHEN** a required product path falls outside the declared arm
- **THEN** the arm is amended by one named path alternative with its self-test updated in the same commit, and the pull request states that the arm was amended here

### Requirement: Machine-readable round state accompanies the prose entry document

The round SHALL publish a machine-readable state document naming the branch tips, the immutable
release identities, the gate results, the open tickets and the claim ceiling, and every identifier it
carries SHALL match the live remote at the time of publication.

#### Scenario: a tool reads the state document

- **WHEN** a reader or tool resolves a branch tip from the state document and compares it with the remote
- **THEN** they agree, or the state document states which commit it describes
