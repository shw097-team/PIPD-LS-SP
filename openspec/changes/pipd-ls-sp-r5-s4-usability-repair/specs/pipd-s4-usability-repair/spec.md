# pipd-s4-usability-repair

## ADDED Requirements

### Requirement: An unsafe output destination is refused before any filesystem mutation
The system SHALL resolve and validate a caller-supplied output destination through a single resolver, and
SHALL refuse — as a typed failure with a non-zero exit — before creating, deleting or replacing anything.

#### Scenario: A dangerous destination is refused typed
- **WHEN** `pipd project --out <path>` names the current directory, a parent, the repository root, the
  user home, the filesystem root, a source ancestor or a foreign absolute directory
- **THEN** the command exits non-zero with `code = "UNSAFE_DESTINATION"` and a message naming the reason
  and the resolved path

#### Scenario: A POSIX-form path is never silently reinterpreted
- **WHEN** `--out` is given in MSYS/POSIX form such as `/c/Users/x` on a Windows host
- **THEN** the resolver refuses it typed instead of resolving it to a drive-relative path

#### Scenario: The refusal is proven side-effect-free
- **WHEN** any unsafe-destination case is exercised against a disposable scratch tree
- **THEN** a before/after canary hash of that tree is byte-identical

#### Scenario: Dry-run uses the same resolver
- **WHEN** `pipd project --dry-run --out <dangerous>` is run
- **THEN** the command refuses typed, exits non-zero, and writes nothing anywhere

### Requirement: Publication of a generated surface is staged and reversible
The system SHALL publish a generated surface by staging to a sibling directory on the same volume,
verifying the staged tree, and atomically replacing the target, keeping the displaced tree.

#### Scenario: A preexisting non-empty target is not destroyed
- **WHEN** the resolved target exists and is non-empty and replacement was not explicitly authorised
- **THEN** the command refuses typed and the target is unchanged

#### Scenario: An authorised replacement keeps the previous bytes
- **WHEN** replacement is authorised and the command succeeds
- **THEN** the previous tree is present under a reported `.pipd-backup-<token>` path and the published
  files are byte-identical to what the same source state produced before

### Requirement: The installed package carries its own contract resources
The system SHALL build a distribution that contains every current Python module and the complete 19-file
schema registry, and SHALL resolve those resources from the installed package rather than the source tree.

#### Scenario: An installed CLI resolves its registry outside the source tree
- **WHEN** the wheel is installed into a fresh isolated environment and the CLI runs from a working
  directory outside the repository with `PYTHONPATH`/`PYTHONHOME` unset
- **THEN** the imported module resolves into site-packages and the registry loads 19/19 families

#### Scenario: A stale or incomplete wheel is refused
- **WHEN** the required modules or schema members are missing from the build inputs
- **THEN** the build fails non-zero naming the missing members, and the legacy wheel is never offered as
  the current distribution

#### Scenario: The build is reproducible
- **WHEN** the same frozen source tree is built twice
- **THEN** the two wheels have the same SHA-256

### Requirement: `export --out` produces a verifiable portable bundle
The system SHALL write a portable archive plus manifest plus checksums to the resolved `--out`, with
deterministic ordering and per-member digests, staged and scanned before publication.

#### Scenario: The bundle is independently verifiable
- **WHEN** `pipd export --out <scratch>` completes
- **THEN** the archive unpacks independently and every member's SHA-256 recomputes to the manifest value

#### Scenario: A failing secret scan produces no artifact
- **WHEN** the export scan finds a credential shape or an invalid member path
- **THEN** zero artifacts are written and the exit status is non-zero and typed

#### Scenario: Dry-run writes nothing
- **WHEN** `pipd export --dry-run --out <scratch>` is run
- **THEN** the plan is reported and no file is created

### Requirement: S4 acceptance is bound to one frozen subject
The system SHALL record, for every S4 acceptance case, the frozen commit/tree, the built wheel identity,
the exact argv, stdout/stderr/exit, before/after filesystem canaries and the checker identity.

#### Scenario: Source and installed-subject results are distinguishable
- **WHEN** the acceptance matrix is produced
- **THEN** results from the source import and results from the installed wheel are reported separately and
  neither substitutes for the other

#### Scenario: Replay identity holds across fresh processes
- **WHEN** the same frozen subject is compiled in two fresh interpreter processes
- **THEN** the normalised canonical output hash is identical

#### Scenario: An unresolved upstream gate stays reported as failed
- **WHEN** the S2 performance gate remains unprovenanced and exceeded
- **THEN** it is reported as `FAIL` in the round evidence and no global PASS is claimed
