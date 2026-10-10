# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin (review candidate)

> ## ⚠️ This branch is the older **R3** snapshot — it is **not** the distribution entry point
>
> The current, owner-authorised open-source preview of PIPD-LS-SP is published on the immutable tag
> **`v0.1.0-preview.1`**, licensed **Apache-2.0**:
>
> **→ https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1**
>
> Install, verification (`SHA256SUMS`), the exact release commit, the licence basis and the
> **known limitations** are all on that release page. Do not install from this branch by default —
> its content, licence metadata and packaging are the pre-grant R3 state.
>
> Everything below was written for the **R3 review candidate** and is kept as a historical
> snapshot, not as the current release description.

Candidate artifact of a governed implementation round. Control plane: **HG-KSEOS**
(project `PIPD-LS-SP-20261008`). Runtime / orchestration plane: **Hermes** under HGK admission.
Contract surface: **Fabric**.

## What is in this tree

| path | what it is |
|---|---|
| `docs/S0_CONTRACT_SPEC.md` | the frozen S0 contract spec that drives the schema set |
| `schemas/` | 19 canonical machine-contract families + `registry.json`, written by the Codex bounded writer |
| `src/pipd_ls_sp/` | the plugin runtime: intake, profile binding, PI→PD→ConstructionContract→ECP/TQAEP pipeline, deterministic validators, 13-command CLI |
| `tests/` | deterministic tests: S0 contract set, LITE vertical slice, negative/adversarial, rollback, secret patterns, tooling guards, quarantine disposition (POS/NEG/EDGE), oracle-disagreement, evidence-MD hard-gate refusal — live count below, never a stale number |
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

## R3 audit-repair status (2026-10-09, FW-10 / FW-12 / R-AUD-008 / R-AUD-012 / R-AUD-013)

True denominators, failures named — no percentage ever hides a hard FAIL:

| area | state | denominator |
|---|---|---|
| unit suite | see `.hgk/artifacts/STATUS_R3.json#tests` | `python -B -m unittest discover -s tests -t .` — real counts + named failing tests, raw log in the round receipt |
| knowledge readiness (`G-KNOWLEDGE-READY`) | **PARTIAL** | 160 unique sources / 153 physically indexed / 7 quarantined by the sanitizer; the 7 are now **owner-dispositioned** (2 `safe-clean`, 5 `safe-reference`, 0 undecided) in `.hgk/knowledge/QUARANTINE_DISPOSITION_R3.json`. The physical number stays 153/160 — it is NOT padded to 160/160 — until `TT-HGK-SANITIZER-UNANCHORED-KEY-PATTERN` closes |
| quarantine negative controls | PASS | a live credential and an unframed injection are **not** released even when claimed harmless; an undecided item stays quarantined (`python tools/quarantine_review.py --report`) |
| TT / CR register | 17 rows | 1 CLOSED (fresh-verified) · 4 PARTIAL · 9 OPEN · 2 OPEN_OWNER_GATE · 1 TEMP_CLOSED — every row carries owner, current state, raw-evidence pointer and explicit close criterion (`.hgk/artifacts/TT_REGISTER.json`) |
| KP rule-polarity (`R-AUD-013`) | OPEN, resolved by the authorised source | `ORACLE_DISAGREEMENT` entry `OD-R3-001`: upper Evidence/Regression requirement prevails over the KP02/KP11/KP12 `MUST NOT` rows; KP files not edited; calibration negative keeps a genuine `MUST NOT` prohibition (`TT-ORACLE-DISAGREEMENT-KP-R04`) |
| PRE-W3 cross-project | **TEMP_CLOSED** | independently closed; never derived from S0–S4 evidence (`TT-PRE-W3-CROSS-PROJECT`, HITL owner required) |
| evidence-MD generator | refusal-protected | `tools/build_evidence_md.py` refuses to print PASS when any hard gate row is FAIL (typed `HARD_GATE_FAIL`, exit 2, no document written) |

## License

No license is granted — see `LICENSE`. The authoritative source corpus declares none; this is
recorded as source gap `TT-PIPD-LICENSE-001`.


## 8. Correction of a wording overclaim (round 2 finding)

README.md previously implied the knowledge layer introduced no new store and was read-only. Both were inaccurate: derived knowledge index built through the HGK SharedSpine typed API; it is a SEPARATE physical SQLite file that carries the HGK schema but contains ZERO governance rows (0 projects/requirements/taskspecs/workorders/events) and is never written by the orchestration plane. Correct description: 'derived, non-authoritative knowledge index' - not 'read-only' and not 'no second store'.
