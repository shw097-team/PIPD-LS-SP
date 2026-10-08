# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin (review candidate)

Candidate artifact of a governed implementation round. Control plane: **HG-KSEOS**
(project `PIPD-LS-SP-20261008`). Runtime / orchestration plane: **Hermes** under HGK admission.
Contract surface: **Fabric**.

## What is in this tree

| path | what it is |
|---|---|
| `docs/S0_CONTRACT_SPEC.md` | the frozen S0 contract spec that drives the schema set |
| `schemas/` | 19 canonical machine-contract families + `registry.json`, written by the Codex bounded writer |
| `src/pipd_ls_sp/` | the plugin runtime: intake, profile binding, PI→PD→ConstructionContract→ECP/TQAEP pipeline, deterministic validators, 13-command CLI |
| `tests/` | 22 tests: S0 contract set, LITE vertical slice, negative/adversarial, rollback |
| `tools/` | governed round tooling (knowledge probe, HGK admission driver, kanban receipts, CLI smoke) |
| `LICENSE`, `PROVENANCE.md`, `SBOM.cdx.json` | release-gate artifacts |

## Claim ceiling — read this before believing anything

This repository is a **review candidate**. Status words are kept separate on purpose:

| claim | state |
|---|---|
| `PROMPT_COMPILE_PASS` | claimed locally, evidence in `.hgk/preflight/` |
| `HGK_ADMITTED` | claimed locally (HGK lifecycle reached `EXECUTING`) |
| `RUNTIME_READY` | **NOT claimed** |
| `LOCAL_QUALIFIED` | claimed locally (deterministic tests + CLI smoke), scoped to S0/S1 |
| `INDEPENDENT_PASS` | **NOT CLAIMED by the maker** — pending an independent acceptance officer receipt |
| `PUBLICATION_APPROVED` | **NOT claimed** — no license is declared in the source corpus |
| `RELEASED` | **NOT claimed** |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

`S0` and `S1` are the only stages reached. S2–S8 are not implemented.

## License

No license is granted — see `LICENSE`. The authoritative source corpus declares none; this is
recorded as source gap `TT-PIPD-LICENSE-001`.


## 8. Correction of a wording overclaim (round 2 finding)

README.md previously implied the knowledge layer introduced no new store and was read-only. Both were inaccurate: derived knowledge index built through the HGK SharedSpine typed API; it is a SEPARATE physical SQLite file that carries the HGK schema but contains ZERO governance rows (0 projects/requirements/taskspecs/workorders/events) and is never written by the orchestration plane. Correct description: 'derived, non-authoritative knowledge index' - not 'read-only' and not 'no second store'.
