# pipd-s0-contracts

## ADDED Requirements

### Requirement: exact 19/19 machine-contract families
The system SHALL materialize exactly the 19 contract families of §7.3, in source order,
each with a Draft 2020-12 schema whose `required` set enforces the registry's `required_fields`.

#### Scenario: a 20th family is rejected
- **WHEN** the registry is rebuilt with an extra family
- **THEN** `registry.load_registry` raises `ValidationFail`.

#### Scenario: seam-only materialization is preserved
- **WHEN** the registry is read
- **THEN** GENIEProjectionRef is SCHEMA_SEAM_ONLY_UNTIL_S6, ExecutionBindingRef is
  SCHEMA_SEAM_ONLY_UNTIL_S5 and WorkOrderCandidate is REQUIRED_NOW_NONAUTHORITY.
