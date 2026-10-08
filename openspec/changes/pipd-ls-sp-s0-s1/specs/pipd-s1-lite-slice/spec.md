# pipd-s1-lite-slice

## ADDED Requirements

### Requirement: one real LITE vertical slice
The system SHALL compile a natural-language goal into PI-PKG, bind PD-PKG against a real
RepoContext, and emit ConstructionContract + ECP + TQAEP, deterministically.

#### Scenario: replay determinism
- **WHEN** the same goal and sources are compiled twice
- **THEN** every artifact subject_id and content_hash is identical.

#### Scenario: PD requires a RepoContext
- **WHEN** no RepoContext is supplied
- **THEN** `bind_pd` fails closed with REPO_CONTEXT_MISSING.

#### Scenario: maker cannot self-accept
- **WHEN** maker == checker in `compile_tqaep`
- **THEN** TQ_SOD is raised.
