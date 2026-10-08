# pipd-cli-surface

## ADDED Requirements

### Requirement: exactly 13 commands
The `pipd` CLI SHALL expose exactly the 13 commands of §5.9.3 and no more, each mapping to
its declared failure codes.

#### Scenario: command count
- **WHEN** the CLI parser is built
- **THEN** it exposes exactly init, intake, profile, compile-pi, bind-pd, compile-ecp,
  compile-tqaep, validate, doctor, project, export, diff, repair.

#### Scenario: export refuses secrets
- **WHEN** a secret-pattern file is present in the export set
- **THEN** `export` fails with EXPORT_SECRET_SCAN.
