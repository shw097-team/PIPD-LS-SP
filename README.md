# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin (review candidate)

Candidate artifact of a governed implementation round. Control plane: **HG-KSEOS**
(project `PIPD-LS-SP-20261008`). Runtime / orchestration plane: **Hermes** under HGK admission.
Contract surface: **Fabric**.

> **Current round: R5 — S4 user-operability focused repair (2026-10-10).**
> This README leads with R5. The R4 and R3 sections are kept below **as history** and are labelled as such;
> where they disagree with the R5 section, R5 is current.
> **Nothing in this file approves anything.** No ceiling was promoted this round.

## What is in this tree

| path | what it is |
|---|---|
| `docs/S0_CONTRACT_SPEC.md` | the frozen S0 contract spec that drives the schema set |
| `schemas/` | 19 canonical machine-contract families + `registry.json`, written by the Codex bounded writer |
| `src/pipd_ls_sp/` | the plugin runtime: intake, profile binding, PI→PD→ConstructionContract→ECP/TQAEP pipeline, deterministic validators, 13-command CLI |
| `tests/` | deterministic tests: S0 contract set, LITE vertical slice, negative/adversarial, rollback, secret patterns, tooling guards, quarantine disposition (POS/NEG/EDGE), oracle-disagreement, evidence-MD hard-gate refusal, S4 repair surfaces — live count below, never a stale number |
| `tools/` | governed round tooling (knowledge probe, HGK admission driver, kanban receipts, CLI smoke, preflight/round-envelope/self-scan guards, publication projection) |
| `dist/` | the built wheel + `WHEEL_MANIFEST.json` + `.sha256`, and the S1 web/host projections |
| `OWNER_LICENSE_DECISION.yaml`, `docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json` | owner decisions taken this round |
| `LICENSE`, `PROVENANCE.md`, `SBOM.cdx.json` | release-gate artifacts |

## Claim ceiling — read this before believing anything

| claim | state |
|---|---|
| `PROMPT_COMPILE_PASS` | claimed locally, evidence in `.hgk/preflight/` |
| `HGK_ADMITTED` | claimed locally (HGK lifecycle reached `EXECUTING`) |
| `RUNTIME_READY` | **NOT claimed** |
| `LOCAL_QUALIFIED` | claimed locally (deterministic tests + CLI smoke), scoped to S0/S1 |
| `S4_REPAIR_CANDIDATE_LOCAL_TESTED` | claimed locally for R5 — **candidate only** |
| `INDEPENDENT_PASS` | **NOT CLAIMED by the maker** — an independent acceptance officer has been appointed and its verdict is still outstanding |
| `PUBLICATION_APPROVED` | **NOT claimed** — the owner declared a non-granting licence reference; that is not an approval |
| `RELEASED` | **NOT claimed** |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

`S0` and `S1` are the only stages reached. S2–S8 are not implemented.

## R5 (2026-10-10) — S4 user-operability focused repair

Task nature **`NARROW_REPAIR`**, scope `S4_USER_OPERABILITY`. R3/R4 functionality is preserved; the round repairs four
concrete usability/safety defects and publishes the result as a bindable candidate.

### What was repaired

| work order | defect | repair |
|---|---|---|
| `WO1` | `pipd project --out` could be aimed at a dangerous destination and would only discover it *after* it had started deleting | a resolver decides the destination **before any side effect** and refuses with a typed `UnsafeDestination`; the existing non-empty-directory refusal stays, with `--allow-replace` as the explicit opt-in |
| `WO2` | the wheel did not carry the 19 schemas, so an installed package was not self-sufficient and silently depended on the source tree / `PYTHONPATH` | three-layer resource resolution + a registry-driven schema locator; the wheel ships the schemas and a `WHEEL_MANIFEST.json` whose digests are recomputable |
| `WO3` | `pipd export --out` reported success without producing the archive/manifest/checksums | export now writes the archive, manifest and `SHA256SUMS` for real; `--dry-run` performs zero writes; a secret hit produces a typed non-zero exit and no artefacts |
| coordinator | the `export` path took a write branch when it should have been read-only | `cli.py` export read-only branch + `cli_surface_check.py` surface pin |

### The S2 gate: an owner adjudication, not a threshold that was widened

`tools/perf_budget.py --check` previously **FAILED**: `context_bytes_per_artefact` measured **343,547** against a
**20,000** budget. The round did **not** widen 20,000 to make the gate green — it established that the *contract* was
wrong, not the artefact:

- the budget expressed a **per-artefact** limit while the measured quantity is proportional to the number of atoms;
- a lossless-dedup floor computation puts the absolute minimum at **263,653 bytes** (13.2× the stated budget), so
  the 20,000 figure is **unreachable by construction**;
- the owner ruled (`docs/OWNER_ADJUDICATION_R5_S4_2026-10-10.json`): `S2_BUDGET_DEFINITION = PER_ATOM_BYTES(2000)`.
  Measured `bytes_per_atom` = **1,449.6 / 2,000 → PASS**. The three timing rows were downgraded to `ADVISORY`
  (`voting: false`) because their provenance was never established.
- **The historical FAIL is preserved, not deleted.** `context_bytes_per_artefact 343547 > 20000` still appears in the
  gate output as a non-voting `ADVISORY` line, and `--freeze-baseline` guards against silent regression.

### Publication: the candidate is now bindable to the subject that failed external challenge

Before this round the working tree held the R4 content **on disk** while the local history never contained the R4
commits at all: content-correct but **unbindable**, which is why every publication and attestation attempt had to fail.
R5 fixes that at the root:

- this branch is a **descendant of `cd8a06e4c066a40398a4012b7b3908ac11408a2b`** (the `r4-candidate` commit that carries
  the external `FAIL_CHALLENGE`), verified with `git merge-base --is-ancestor` **inside a fresh anonymous clone**;
- the publication projection reconciles with **0 violations** (1,916 entries, 0 uncovered current product paths);
- the credential used to push was used for **exactly one push** and never entered the repository, a commit, a log or a
  report; the repository is public, so every read was anonymous.

### Verification performed this round

| what | result | where the number came from |
|---|---|---|
| UAT-00…12, **source** state | 12 `PASS` + 1 `INFO`, 0 `FAIL` | `.hgk/rounds/R5-20261009-s4-user-operability/uat/UAT_MATRIX.json` |
| UAT-00…12, **installed wheel** state | 13 `PASS` + 1 `INFO`, 0 `FAIL` | same |
| CLI surface | 13/13 commands + 6/6 extras, `PASS` | `tools/cli_surface_check.py` |
| portable install | 14/14 `PASS` | `tools/portable_install_check.py` |
| deny-list scan | exit 0, `PASS` | `tools/deny_list_scan.py` |
| perf gate | exit 0 (adjudicated contract) | `tools/perf_budget.py --check` |
| deterministic in-process checker | `PASS_CHECK_DETERMINISTIC` 17/17, 4 counter-probes held | `.hgk/rounds/.../ao/independent_check.py` |

### Two honest caveats about that table

1. **The in-process checker is an explicitly LOWER grade than an LLM/human checker.** It is deterministic and it tries
   to falsify, but it was authored by the same orchestration that produced the repair, so it is **not** treated as an
   independent authority — see `sound_oracle: false`. It is never presented as `INDEPENDENT_PASS`.
2. **The UAT matrix was executed by the maker**, not by a separate checker. The numbers are real and reproducible, but
   they are *maker-executed* numbers.

### Independent acceptance officer — appointed, verdict outstanding

The owner appointed an **Independent Acceptance Officer (VERIFY / SECURITY)** to be executed through the Codex CLI on
the OpenAI OAuth lane (`gpt-5.6-sol`, reasoning effort `medium`; the owner's naming said "6.1 SOL" — this account
serves the SOL family at generation 5.6). The officer runs against a **fresh anonymous clone of this branch**, read-only
on the subject, writing only to its own output directory.

As of this writing the verdict has **not** been produced, so **no independent acceptance is claimed**. When it lands,
`AO_VERDICT.json` and `AO_REPORT.md` are the authority — not this README.

### Open, honestly

- **R4 findings still open**: `F-R4-PUB-06` (publication projection for the externally audited subject) `blocked`;
  `F-R4-HARNESS-07` `conditional`; `F-R4-TRACE-08` `deferred` (57-row SPEC/DEL crosswalk: 42 `EVIDENCED` /
  11 `EVIDENCE_GAP` / 4 `DESIGN_ONLY` — no overall PASS); `F-R4-GOV-09` `deferred`; `F-R4-RELEASE-10` `out_of_scope`.
  `F-R4-S4-04` is `closed_pending_llm_checker`. Ledger: `.hgk/rounds/R5-.../ledger/R5_S4_FINDING_LEDGER.json`.
- **A maker self-report was caught being false and corrected.** The WO2 lane reported two tests as
  "pre-existing unrelated failures"; on the candidate they pass (`Ran 36 tests OK`). The correction is recorded in
  `.hgk/rounds/R5-.../MAKER_SELFREPORT_CORRECTION_WO2.json`. Nothing was "fixed", because there was nothing wrong.
- **A checker-contamination incident recurred and was fixed at the mount boundary.** A verifier's scratch directory
  lived *inside* the product tree, so the product's own walker tripped over the verifier's venv reparse points. The fix
  is a hard guard that **refuses to start** if the scratch path is inside the product tree — deliberately at the
  boundary, not as a copy filter inside the subject (a filter there would have masked a real product defect).
  See `VERIFIER_SCOPE_INCIDENT.json`.
- **The freshness/anti-staleness zone has only a single, undecided witness.** The behaviour (a bare `FRESH` claim is
  refused as `StaleProvider`; the same claim with the correct epoch is accepted; a spoofed head is refused) appears only
  in a checker's prose log, with no independent reproducer. It is **not** counted as confirmed.
- **`INDEPENDENT_PASS`, `PUBLICATION_APPROVED`, `RELEASED`, `PRODUCTION_VERIFIED` remain NOT CLAIMED.**

## KNOWN DEFECT — the offline object reader cannot read packed objects

**13 of 290 tests fail in a fresh clone of this branch.** The root cause is in the round tooling, not the product:

```
build_publication_manifest.GitObjectUnavailable: object 1a7dc57f9403202c32d1bc01deb1925ac1f6412e
is not a loose object in <clone>/.git and no pack index is consulted offline
```

`tools/build_publication_manifest.py` (and `publication_attestation.py` on top of it) read **loose** git objects
directly and refuse to consult a pack index — a deliberate offline-hardening choice. But **every `git clone` stores
objects in a pack**, so on any normal checkout the whole publication-projection test surface errors out:

```
Ran 290 tests ... FAILED (failures=6, errors=7, skipped=2)
```

- **This is pre-existing, not introduced by R5.** The identical 12 failures reproduce on the *pre-existing*
  `r4-candidate` commit `cd8a06e` in a fresh clone.
- **It is invisible in the authoring working tree** because that tree happens to hold the objects loose. The R4
  section's "Ran 256 tests … OK" figure was measured under exactly that condition and has the same standing.
- Workaround, if you need the tests to pass: `git unpack-objects < .git/objects/pack/*.pack` before running them.
- This is recorded rather than hidden because a number that only reproduces in the author's working tree is not
  evidence.

## Reproduce the headline checks (as measured on this published branch, in a fresh clone)

```bash
git clone --branch r5-s4-candidate https://github.com/shw097-team/PIPD-LS-SP && cd PIPD-LS-SP

env -u PYTHONPATH -u PYTHONHOME python -B -m unittest discover -s tests -q
#   expect: Ran 290 tests, FAILED (failures=6, errors=7, skipped=2)
#   the 13 are all in the publication tooling -> see "KNOWN DEFECT" above

env -u PYTHONPATH -u PYTHONHOME python -B tools/perf_budget.py --check
#   expect: exit 0 — bytes_per_atom 1449.6/2000 is the only voting row;
#           the historical context_bytes_per_artefact 343547 > 20000 stays visible as ADVISORY

env -u PYTHONPATH -u PYTHONHOME python -B tools/deny_list_scan.py
#   expect: exit 0, verdict PASS

env -u PYTHONPATH -u PYTHONHOME python -B tools/cli_surface_check.py
#   expect: 13/13 + 6/6, verdict PASS

env -u PYTHONPATH -u PYTHONHOME python -B tools/portable_install_check.py
#   expect: 14/14, verdict PASS

env -u PYTHONPATH -u PYTHONHOME python -B tools/tt_summary_check.py --assert
#   expect: TT_SUMMARY_ASSERT_FAIL — 1 difference: as_of_candidate.
#   The stored `as_of_candidate` is bound to the *verified* candidate 7c5bc585, not to the publication tip,
#   the same convention as the previously published tree. A fresh clone therefore reports that one binding
#   as "stale" BY DESIGN; `--write` rebinds it. The TT counts themselves agree.

git merge-base --is-ancestor cd8a06e4c066a40398a4012b7b3908ac11408a2b HEAD && echo "lineage OK"
#   expect: lineage OK — this candidate descends from the commit that failed external challenge
```

One test skips in a bare interpreter: `test_installed_package_is_self_sufficient` is skipped when `pip` is unavailable
to the test interpreter. The installed-package self-sufficiency claim therefore rests on `portable_install_check.py`
(14/14) rather than on that test.

---

## R4 focused-repair status (2026-10-09) — kept as history

> The reproduce block in this section reflects the **R4** tree. Its `perf_budget --check` expectation (exit 1) was
> superseded in R5 by the owner adjudication described above.

Task nature **`NARROW_REPAIR`** (scope `S0-S4_FOCUSED_REPAIR_PLUS_PUBLICATION_EVIDENCE`); R3 functionality is preserved —
the round adds hardening tooling and its evidence, it does not rewrite the pipeline.

**R4 (2026-10-09) keeps every ceiling — nothing was promoted.**
`INDEPENDENT_PASS`, `PUBLICATION_APPROVED`, `RELEASED` and `PRODUCTION_VERIFIED` remain **NOT CLAIMED**. One repair
delta (the `round_envelope` destination guards) was independently verified by a separate lane whose verdict is **PASS at
the delta level**, with the ceiling still `CANDIDATE_ONLY`; the *round's* acceptance stayed **PARTIAL** (V7 `NOT_RUN`).

### The hard gate that was failing — stated at the top, not buried

`python -B tools/perf_budget.py --check` → **FAIL**. `context_bytes_per_artefact` measured **343,547** against a
**20,000** budget (other runs: 336,674 / 355,119 — the exceedance was stable, not noise). All four thresholds carried
`source_of_truth: UNPROVENANCED`, so the three timing rows were `UNDECIDABLE`. Fail-closed behaviour was deliberately
retained and **no threshold was raised** — widening 20,000 to make the gate green would have been weakening a gate.
This is the failure R5 later resolved by redefining the contract.

### Hardening tools added in R4 (each with its own tests)

| tool | what it enforces |
|---|---|
| `tools/preflight_check.py` | pre-admission preflight over the round's declared scope |
| `tools/round_envelope.py` | freeze/envelope a candidate; destination guards **STOP-1..STOP-6** refuse a blank, empty, cwd, `$HOME`, drive-root, equal-to-source or ancestor destination **before any deletion** |
| `tools/round_selfscan.py` | in-round self-scan of a round's own artifacts |
| `tools/deny_list_scan.py` | deny-list scan of a scope; non-zero exit on a hit |
| `tools/pi_dedup_check.py` | PI duplication check |
| `tools/tt_summary_check.py` | recomputes the TT summary from `tts[]` only (`--assert` / `--write`) |
| `tools/build_spec_del_crosswalk.py`, `tools/build_publication_manifest.py`, `tools/publication_attestation.py` | crosswalk, publication projection and attestation |

### A destructive incident and its long-term repair — disclosed in full

A repair subagent passed an **empty `--dst`**, which normalised to the working directory, and `shutil.rmtree` deleted
tracked files in the repository root before it was caught. The round restored **every** affected artifact byte-identically
from a frozen copy (HEAD, index flags, `.git/config`, `.git/logs/HEAD`, porcelain state) and verified each one
independently. The event is recorded (`PIPD-LS-SP_R4_INCIDENT01_DESTRUCTIVE_DST_2026-10-09.md`) and repaired as
`H2-DEFECT-02` — the STOP-1..STOP-6 destination guards above exist because of it.

**A second instance of the same defect class occurred on the orchestration side during that publication**: a native
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

### Open, honestly (R4, as of R4)

- **The round's acceptance was PARTIAL.** `W8-VERIFY-3` rows V1–V6 and V8 PASS but **V7 is `NOT_RUN`**: two gate tools
  were absent from the committed baseline, so "the gate was not weakened" could not be computed. **A commit alone cannot
  convert V7 to PASS** — a *new* baseline cannot prove an *absent historical* baseline was preserved.
- **TT register: 22 rows, 18 blocking** at that time, every row carrying owner, current state, raw-evidence pointer and
  an explicit close criterion.
- **The hardening tools have no automated consumer** in the pipeline (`actual_hgk_consumer: null`): they bite when a
  human exercises them, which is materially weaker than an automated gate. Recorded, not papered over.
- **`EVIDENCE_IDENTITY_MISMATCH`** (unresolved): an earlier external challenge quoted an evidence-file SHA that no
  version in this tree reproduces. Recorded as-is.
- `SPEC/DEL` crosswalk: **42 EVIDENCED / 11 EVIDENCE_GAP / 4 DESIGN_ONLY** of 57 rows — no overall PASS claim.

### Owner adjudication (2026-10-09)

`docs/OWNER_ADJUDICATION_R4_2026-10-09.json` records the six open items (`A1`–`A5`, `V7`) and the ruling executed for each.
**Five required no owner action at all**; the only authority act taken was
`A2 = ACCEPT_EXISTING_NO_LICENSE_NOTICE`, and it **grants nothing**: no licence, no release, no independent pass, no
production verification.

### Publication note (R4)

That branch was built **on top of the then-published `main`** using the same view strategy as R3: the 130.09 MB
`.hgk/rounds/R2-20261009-qualification/execute/knowledge/own-derived.db` was excluded (GitHub's 100 MB single-file hard
limit). **That publication was a candidate for external verification — not a release**, and it approved nothing.

## R3 audit-repair status — R3 snapshot (2026-10-09, FW-10 / FW-12 / R-AUD-008 / R-AUD-012 / R-AUD-013) — kept as history

True denominators, failures named — no percentage ever hides a hard FAIL:

| area | state | denominator |
|---|---|---|
| unit suite | see `.hgk/artifacts/STATUS_R3.json#tests` | `python -B -m unittest discover -s tests -t .` — real counts + named failing tests, raw log in the round receipt |
| knowledge readiness (`G-KNOWLEDGE-READY`) | **PARTIAL** | 160 unique sources / 153 physically indexed / 7 quarantined by the sanitizer; the 7 are **owner-dispositioned** (2 `safe-clean`, 5 `safe-reference`, 0 undecided) in `.hgk/knowledge/QUARANTINE_DISPOSITION_R3.json`. The physical number stays 153/160 — it is NOT padded to 160/160 — until `TT-HGK-SANITIZER-UNANCHORED-KEY-PATTERN` closes |
| quarantine negative controls | PASS | a live credential and an unframed injection are **not** released even when claimed harmless; an undecided item stays quarantined (`python tools/quarantine_review.py --report`) |
| TT / CR register | 17 rows | 1 CLOSED (fresh-verified) · 4 PARTIAL · 9 OPEN · 2 OPEN_OWNER_GATE · 1 TEMP_CLOSED — every row carries owner, current state, raw-evidence pointer and explicit close criterion (`.hgk/artifacts/TT_REGISTER.json`) |
| KP rule-polarity (`R-AUD-013`) | OPEN, resolved by the authorised source | `ORACLE_DISAGREEMENT` entry `OD-R3-001`: upper Evidence/Regression requirement prevails over the KP02/KP11/KP12 `MUST NOT` rows; KP files not edited; calibration negative keeps a genuine `MUST NOT` prohibition (`TT-ORACLE-DISAGREEMENT-KP-R04`) |
| PRE-W3 cross-project | **TEMP_CLOSED** | independently closed; never derived from S0–S4 evidence (`TT-PRE-W3-CROSS-PROJECT`, HITL owner required) |
| evidence-MD generator | refusal-protected | `tools/build_evidence_md.py` refuses to print PASS when any hard gate row is FAIL (typed `HARD_GATE_FAIL`, exit 2, no document written) |

## License

**No licence is granted** — see `LICENSE`. The owner's R5 decision
(`OWNER_LICENSE_DECISION.yaml`, `decision: LicenseRef-PIPD-Proprietary`) is **non-granting**: it names a reference so the
disposition is no longer `UNSET`, and it **grants no rights**. The authoritative source corpus declares no licence; that
is recorded as source gap `TT-PIPD-LICENSE-001`.

R4 note: the owner's earlier adjudication (`docs/OWNER_ADJUDICATION_R4_2026-10-09.json`) accepted the existing
no-licence NOTICE (`A2 = ACCEPT_EXISTING_NO_LICENSE_NOTICE`). Accepting the notice did **not** grant a licence — it
confirmed that none is granted, so that the licence-disposition question no longer blocked anything.

## Correction of a wording overclaim (round 2 finding)

README.md previously implied the knowledge layer introduced no new store and was read-only. Both were inaccurate: the
derived knowledge index is built through the HGK SharedSpine typed API; it is a SEPARATE physical SQLite file that
carries the HGK schema but contains ZERO governance rows (0 projects/requirements/taskspecs/workorders/events) and is
never written by the orchestration plane. Correct description: 'derived, non-authoritative knowledge index' — not
'read-only' and not 'no second store'.
