# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin (review candidate)

> **S4 OPEN SOURCE PREVIEW / BETA — licence granted by the owner as `Apache-2.0`.**
>
> The distribution entry point for this preview is the tag **`v0.1.0-preview.1`**, not the default
> branch. `main` carries the historical R3 content plus a front-page pointer to that tag, and must
> not be used to judge this preview.
>
> | what | where |
> |---|---|
> | licence | [`LICENSE`](LICENSE) (verbatim Apache License 2.0); attribution and material-class split in [`NOTICE`](NOTICE) |
> | grant record | [`OWNER_LICENSE_DECISION.yaml`](OWNER_LICENSE_DECISION.yaml) — `decision: Apache-2.0`, effective at the release commit |
> | machine-readable licence | [`SBOM.cdx.json`](SBOM.cdx.json) |
> | what is **not** claimed | [`ACCEPTANCE.md`](ACCEPTANCE.md) and the release notes for the tag |
>
> This is a **preview**, not a production release: `DEL-018` (RELEASE_MANIFEST@1) stays an open
> release-evidence gap, the full S0–S4 independent challenge is `PARTIAL_CHALLENGE`, and S5–S8,
> host-native certification and PRE-W3 are deferred. Nothing above is inherited from any earlier round.

Candidate artifact of a governed implementation round. Control plane: **HG-KSEOS**
(project `PIPD-LS-SP-20261008`). Runtime / orchestration plane: **Hermes** under HGK admission.
Contract surface: **Fabric**.

> **External acceptance entry point:** see [`ACCEPTANCE.md`](ACCEPTANCE.md). It names the branch under
> acceptance, the subject commit, the one defect repaired in the R5 S4 round, the independent verdict and
> the exact commands an external verifier runs — and what is explicitly **not** claimed.

## What is in this tree

| path | what it is |
|---|---|
| `docs/S0_CONTRACT_SPEC.md` | the frozen S0 contract spec that drives the schema set |
| `schemas/` | 19 canonical machine-contract families + `registry.json`, written by the Codex bounded writer |
| `src/pipd_ls_sp/` | the plugin runtime: intake, profile binding, PI→PD→ConstructionContract→ECP/TQAEP pipeline, deterministic validators, 13-command CLI |
| `tests/` | deterministic tests: S0 contract set, LITE vertical slice, negative/adversarial, rollback, secret patterns, tooling guards, quarantine disposition (POS/NEG/EDGE), oracle-disagreement, evidence-MD hard-gate refusal — live count below, never a stale number |
| `tools/` | governed round tooling (knowledge probe, HGK admission driver, kanban receipts, CLI smoke) |
| `LICENSE`, `NOTICE`, `PROVENANCE.md`, `SBOM.cdx.json` | release-gate artifacts (licence text, attribution + material-class split, provenance, machine-readable licence) |
| `PREVIEW_NOTES_v0.1.0-preview.1.md` | preview release notes: what this build is, how to verify it, and what it does not claim |

## Claim ceiling — read this before believing anything

This repository is a **review candidate**. Status words are kept separate on purpose:

| claim | state |
|---|---|
| `PROMPT_COMPILE_PASS` | claimed locally, evidence in `.hgk/preflight/` |
| `HGK_ADMITTED` | claimed locally (HGK lifecycle reached `EXECUTING`) |
| `RUNTIME_READY` | **NOT claimed** |
| `LOCAL_QUALIFIED` | claimed locally (deterministic tests + CLI smoke), scoped to S0/S1 |
| `INDEPENDENT_PASS` | **NOT CLAIMED as a full pass** — an independent verifier that did not build this tree re-derived the published artefact (own anonymous download, own clone) and returned **9/9 claims PASS with no stop-ship counter-example**; the receipt is scoped to the immutable tag/commit/tree/wheel bytes only, and it ran on a different model lane than this round's plan named, so no planned-model SoD is claimed |
| `PUBLICATION_APPROVED` | **GRANTED** for the limited S4 open-source preview: owner licence decision `Apache-2.0` in [`OWNER_LICENSE_DECISION.yaml`](OWNER_LICENSE_DECISION.yaml) (round R5Q, 2026-10-10). Still **NOT claimed**: `G-RELEASE_FULL_PASS` — `DEL-018` remains an open release evidence gap |
| `RELEASED` | limited: `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED` only, at the preview tag |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

**Historical R3 snapshot (kept as history, not the current product state):** `S0` and `S1` are the only stages reached. S2–S8 are not implemented.

> The sentence above is the **R3** snapshot. The branch **current for review** is **`r5p-post-challenge-repair`** (baseline `r5-s4-packreader` @ `0f06eec96386b7349db8b41ac6cf9c7455d326f1`; `main` is still the R3 state). The current acceptance entry point is [`ACCEPTANCE.md`](ACCEPTANCE.md), which names the candidate ceiling: an **`S4` candidate, internal evaluation**, licensed **`LicenseRef-PIPD-Proprietary`** with **no public-use grant** — *historical, superseded by the R5Q owner grant below*. This note upgrades no claim level.
>
> **R5Q (2026-10-10) supersedes the licence sentence above.** The owner granted **`Apache-2.0`** over this repository (record: [`OWNER_LICENSE_DECISION.yaml`](OWNER_LICENSE_DECISION.yaml), study FAR-PIPD-R5Q-LICENSE-001); the grant becomes publicly effective at the release commit carrying it, and **the tag `v0.1.0-preview.1` — not this branch and not `main` — is the distribution entry point for the preview.** The prior no-grant state is retained as history above rather than rewritten. Claim level after the grant is still bounded: `PARTIAL_CHALLENGE`, `DEL-018` open, no `G-RELEASE_FULL_PASS`, no `PRODUCTION_VERIFIED`.

> **Independent acceptance of the published preview (R5Q follow-up):** an independent verifier rebuilt its understanding of `v0.1.0-preview.1` from scratch — anonymous download, its own clone, a clean venv, the published wheel bytes only — and returned **9/9 claims PASS, no stop-ship counter-example**. Two counter-examples were returned by a **second, later** independent run and both were **reproduced by the maker** against the published bytes; they are now disclosed as limitations 6 and 7 of the release: (6) `validate` does not resolve the schemas installed inside the wheel the way `doctor` does — without the global `--root <site-packages>/pipd_ls_sp` it exits 2 with `INPUT_SHAPE_INVALID` looking for `<cwd>/schemas/PI-PKG.schema.json`; (7) a bundle assembled from the four compilers' unmodified stdout is rejected by `validate` because `compile-pi` emits a top-level `_profile_meta` that `PI-PKG` forbids (`additionalProperties: false`) — removing only that sidecar makes the same bundle pass `checked=4, findings=[]`. Both are non-stop-ship (install, licence packaging, `doctor`, the CLI and all artefact hashes are unaffected) and both are **open**: fixing either changes member bytes and needs a superseding release, since published tags are never rewritten. Claim ceiling is unchanged.
>
> **Preview known limitations** (full text in the release notes for `v0.1.0-preview.1`): `DEL-018 RELEASE_MANIFEST@1` remains **FAIL/EVIDENCE_GAP** — `tools/build_publication_manifest.py --check --current` exits 1 and the uncovered paths are `tests/test_git_object_reader.py`, `tests/test_doctor_schema_truth.py`, `tests/test_tqaep_design_positive.py`; the SPEC/DEL denominator stays `28 evidenced / 10 active gaps / 19 deferred`; native Windows symlink/junction/reparse behaviour is not certified beyond the tested scope (`TT-R5P-01`, `TT-R5P-06`); there is no install-time cryptographic readback, only published SHA-256 for manual verification (`TT-R5P-02`); S5 (HGK live), S6 (GENIE), S7 (JIT), S8 (SWOF/SGM), PRE-W3 and the 22 inactive external technologies are deferred; `PRODUCTION_VERIFIED` is not claimed.

**R4 (2026-10-09) keeps every one of those ceilings — nothing below was promoted.**
`INDEPENDENT_PASS`, `PUBLICATION_APPROVED`, `RELEASED` and `PRODUCTION_VERIFIED` remain **NOT CLAIMED**. One repair
delta (the `round_envelope` destination guards) was independently verified by a separate lane whose verdict is **PASS at
the delta level**, with the ceiling still `CANDIDATE_ONLY`; the *round's* acceptance stays **PARTIAL** (V7 `NOT_RUN`).

## R3 audit-repair status — R3 snapshot (2026-10-09, FW-10 / FW-12 / R-AUD-008 / R-AUD-012 / R-AUD-013)

> The counts in this section are the **R3** snapshot and are deliberately left as history. The current register is
> **22 rows / 18 blocking** — see the R4 section below, which supersedes the "17 rows" figure quoted here.

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

## R4 focused-repair status (2026-10-09) — `PIPD-LS-SP-HERMES-R4-FOCUSED-REPAIR-20261009`

Task nature **`NARROW_REPAIR`** (scope `S0-S4_FOCUSED_REPAIR_PLUS_PUBLICATION_EVIDENCE`); R3 functionality is preserved —
the round adds hardening tooling and its evidence, it does not rewrite the pipeline.

### The hard gate that is FAILING — stated here at the top, not buried

`python -B tools/perf_budget.py --check` → **FAIL**. `context_bytes_per_artefact` measures **343,547** against a
**20,000** budget (other runs: 336,674 / 355,119 — the exceedance is stable, it is not noise). All four thresholds carry
`source_of_truth: UNPROVENANCED`, so the three timing rows are `UNDECIDABLE`. Fail-closed behaviour was deliberately
retained and **no threshold was raised** — widening 20,000 to make the gate green would be weakening a gate.
The budget's derivation row is still missing (`TT-PIPD-PERF-CONTEXT-BUDGET-PROVENANCE`).

### Hardening tools added this round (each with its own tests)

| tool | what it enforces |
|---|---|
| `tools/preflight_check.py` | pre-admission preflight over the round's declared scope |
| `tools/round_envelope.py` | freeze/envelope a candidate; destination guards **STOP-1..STOP-6** refuse a blank, empty, cwd, `$HOME`, drive-root, equal-to-source or ancestor destination **before any deletion** |
| `tools/round_selfscan.py` | in-round self-scan of a round's own artifacts |
| `tools/deny_list_scan.py` | deny-list scan of a scope; non-zero exit on a hit |
| `tools/pi_dedup_check.py` | PI duplication check |
| `tools/tt_summary_check.py` | recomputes the TT summary from `tts[]` only (`--assert` / `--write`) |
| `tools/build_spec_del_crosswalk.py`, `tools/build_publication_manifest.py`, `tools/publication_attestation.py` | crosswalk, publication projection and attestation |

### Tests

`python -B -m unittest discover -s tests -q` in a clean environment (with `PYTHONPATH` and `PYTHONHOME` unset) →
**`Ran 256 tests … OK`** (baseline 188 + 68 new). New-surface counts: `test_preflight_check` 35,
`test_round_envelope` **23**, `test_round_selfscan` 10.

### A destructive incident and its long-term repair — disclosed in full

A repair subagent passed an **empty `--dst`**, which normalised to the working directory, and `shutil.rmtree` deleted
tracked files in the repository root before it was caught. The round restored **every** affected artifact byte-identically
from a frozen copy (HEAD, index flags, `.git/config`, `.git/logs/HEAD`, porcelain state) and verified each one
independently. The event is recorded (`PIPD-LS-SP_R4_INCIDENT01_DESTRUCTIVE_DST_2026-10-09.md`) and repaired as
`H2-DEFECT-02` — the STOP-1..STOP-6 destination guards above exist because of it.

**A second instance of the same defect class occurred on the orchestration side during this publication**: a native
`git` received an MSYS-style `/c/...` path, which this host does not translate, and created a clone under `C:\c\`.
It is disclosed in `.hgk/rounds/R4-20261009-focused-repair/H2/raw/INCIDENT02.json`; it caused no product or repository
damage, nothing was pushed from it, and the only credential material it held (a tokenised remote URL in its own
`.git/config`) was deleted with it. It is direct evidence that this defect class is real rather than hypothetical.

### Independent verification of that repair (separate lane, three rounds)

| round | verdict | what it found |
|---|---|---|
| v3 | `FAIL` | the *instrument* aimed a destructive probe at the **real home directory** (the same error class as the incident); a root-mtime-only comparison was too weak to prove "untouched" |
| v4 | `FAIL` (row D1 only) | rows D2–D6 PASS and the test-weakening audit found **none**; D1 FAIL because function-name whitelisting is not semantic verification |
| v5 | **`PASS`** | all six rows PASS once the checker was authorised to read the subject source in full and performed the semantic hunk review itself (`unaccounted_lines: []`) |

Residual, stated plainly: the differential harness is **orchestrator-authored** and is *not* treated as an independent
authority (`sound_oracle: false`); the delta verdict's ceiling is `CANDIDATE_ONLY`.

### Open, honestly

- **The round's acceptance is PARTIAL.** `W8-VERIFY-3` rows V1–V6 and V8 PASS but **V7 is `NOT_RUN`**: two gate tools are
  absent from the committed baseline, so "the gate was not weakened" cannot be computed. **A commit alone cannot convert
  V7 to PASS** — a *new* baseline cannot prove an *absent historical* baseline was preserved.
- **TT register: 22 rows, 18 blocking** (16 open · 2 owner-gate · 2 partial · 1 closed · 1 temp-closed), every row carrying
  owner, current state, raw-evidence pointer and an explicit close criterion.
- **The hardening tools have no automated consumer** in the pipeline (`actual_hgk_consumer: null`): they bite when a human
  exercises them, which is materially weaker than an automated gate. Recorded, not papered over.
- **`EVIDENCE_IDENTITY_MISMATCH`** (unresolved): an earlier external challenge quoted an evidence-file SHA that no version
  in this tree reproduces. Recorded as-is.
- `SPEC/DEL` crosswalk: **42 EVIDENCED / 11 EVIDENCE_GAP / 4 DESIGN_ONLY** of 57 rows — no overall PASS claim.

### Owner adjudication (2026-10-09)

`docs/OWNER_ADJUDICATION_R4_2026-10-09.json` records the six open items (`A1`–`A5`, `V7`) and the ruling executed for each.
**Five required no owner action at all**; the only authority act taken is
`A2 = ACCEPT_EXISTING_NO_LICENSE_NOTICE`, and it **grants nothing**: no licence, no release, no independent pass, no
production verification.

### Reproduce the headline checks

```bash
env -u PYTHONPATH -u PYTHONHOME python -B -m unittest discover -s tests -q     # expect: Ran 256 tests, OK
env -u PYTHONPATH -u PYTHONHOME python -B tools/perf_budget.py --check         # expect: exit 1 — FAIL on context_bytes_per_artefact
env -u PYTHONPATH -u PYTHONHOME python -B tools/deny_list_scan.py              # expect: exit 0, verdict PASS
env -u PYTHONPATH -u PYTHONHOME python -B tools/tt_summary_check.py --assert   # expect: counts agree — total=22, unknown=0, blocking=18
#   The `as_of_candidate` line is bound to the *verified* candidate 7c5bc585, not to the publication tip — the same
#   convention as the previously published tree. A fresh clone therefore reports that one binding as "stale" by
#   design; `--write` rebinds it. The counts are what the assert compares, and they agree.
```

### Publication note

This branch is built **on top of the published `main`** using the same view strategy as R3: the 130.09 MB
`.hgk/rounds/R2-20261009-qualification/execute/knowledge/own-derived.db` is excluded (GitHub's 100 MB single-file hard
limit). **This publication is a candidate for external verification — it is not a release**, and it approves nothing.

## License

No license is granted — see `LICENSE`. The authoritative source corpus declares none; this is
recorded as source gap `TT-PIPD-LICENSE-001`.

R4 note: the owner's adjudication (`docs/OWNER_ADJUDICATION_R4_2026-10-09.json`) accepted this existing no-license
NOTICE (`A2 = ACCEPT_EXISTING_NO_LICENSE_NOTICE`). Accepting the notice does **not** grant a licence — it confirms that
none is granted, so that the licence-disposition question no longer blocks anything.


## 8. Correction of a wording overclaim (round 2 finding)

README.md previously implied the knowledge layer introduced no new store and was read-only. Both were inaccurate: derived knowledge index built through the HGK SharedSpine typed API; it is a SEPARATE physical SQLite file that carries the HGK schema but contains ZERO governance rows (0 projects/requirements/taskspecs/workorders/events) and is never written by the orchestration plane. Correct description: 'derived, non-authoritative knowledge index' - not 'read-only' and not 'no second store'.
