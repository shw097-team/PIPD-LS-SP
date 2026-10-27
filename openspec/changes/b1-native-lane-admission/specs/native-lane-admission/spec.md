# native-lane-admission

## ADDED Requirements

### Requirement: Route promotion requires a complete owner-registered entry

A runner route SHALL NOT advance beyond `DISCOVERED` unless a `runner-registry.json` entry exists for
it carrying all nine fields: `runner_id`, `abi_version`, `schema_id`, `executable_path`,
`executable_sha256`, `allowed_os`, `read_scope`, `permission_scope`, `owner_signature`.

#### Scenario: Complete entry promotes the route

- **WHEN** all nine fields resolve and `executable_sha256` matches the binary actually on disk
- **THEN** the route may report `INSTALLED`, and a real invocation receipt may report `INVOKED`

#### Scenario: Partial entry is refused

- **WHEN** any of the nine fields is missing, or the `executable_sha256` does not match the binary
- **THEN** the route stays `BLOCKED_MISSING_RUNNER_OR_BINDING` and the refusal names the missing field

#### Scenario: An agent may not self-register

- **WHEN** the `owner_signature` was produced by the same agent that authored the entry
- **THEN** admission is refused as `SELF_ACCEPT_FORBIDDEN`

### Requirement: Issuer, queue and effect receipts are distinct

The lane SHALL emit `RAW-HGK-ISSUER`, `RAW-HGK-QUEUE` and `RAW-HGK-EFFECT` as separate records bound
to the same subject, and none SHALL be quoted as evidence for another.

#### Scenario: Queue lease is not an effect

- **WHEN** only `RAW-HGK-QUEUE` exists for an operation
- **THEN** the operation's effect state is `NOT_RUN`, not `EFFECT_COMMITTED`

#### Scenario: Revoked credential is refused before spawn

- **WHEN** a revoked token is presented
- **THEN** the executor refuses with `REVOKED_TOKEN_REPLAY` and the world state delta is zero

### Requirement: Independence requires a separate writable surface

A checker verdict SHALL count as `INDEPENDENT_PASS` only if it was produced with a credential distinct
from the maker's and written outside the maker's writable tree.

#### Scenario: Same-orchestration review is not independent

- **WHEN** a different model in the same orchestration writes the verdict into the maker's tree
- **THEN** the receipt is recorded with ceiling `AUTHOR_SIDE_CHECKER_RECEIPT_NOT_INDEPENDENT` and
  G-A6 remains `NOT_RUN`

#### Scenario: Distinct principal closes G-A6

- **WHEN** a distinct principal with a read-only ACL writes a verdict bound to the same subject sha
- **THEN** G-A6 may pass, and `INDEPENDENT_PASS` is claimable for that subject only

### Requirement: Successor must be scheduler-started in another session

G-B SHALL require the successor to be started by the native scheduler from the durable journal, in a
different OS PID/session, after the external helper credential is revoked.

#### Scenario: Same-session replay does not satisfy G-B

- **WHEN** the successor runs in the same session or PID, or is invoked by the external helper
- **THEN** G-B stays `HOLD`

#### Scenario: Unknown effect reconciles, never replays

- **WHEN** an effect landed but the journal commit is missing
- **THEN** the lane reconciles from world state, records `EFFECT_PRESENT_COMMIT_MISSING`, and does not
  re-apply the effect
