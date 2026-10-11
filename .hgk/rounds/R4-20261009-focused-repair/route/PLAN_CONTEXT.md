# CONTEXT — verified facts for a rapid FAR on the open adjudication items

Every number below was measured on this host on 2026-10-09 against candidate HEAD
`7c5bc585c7d889cd338da853be4efc4b8f07d3b2` (branch `master`, **uncommitted, unpushed**). Treat these as given;
do not re-derive them. Where a measurement fluctuates between runs, both values are shown.

## The governing frame (do not propose anything that breaks it)
- Owner control plane = HG-KSEOS only. `ClaimCeiling = CANDIDATE_ONLY`; `INDEPENDENT_PASS` / `RELEASED` /
  `PRODUCTION_VERIFIED` are all **NOT_GRANTED**.
- An agent must **never** self-accept, self-promote, weaken a gate, or fake a result. Lifting a security
  control (a quarantine), granting a licence, or declaring a release is an **owner authority act**.
- The owner wants **low-resistance engineering**: minimal change, no architecture work, no new machinery,
  and the smallest possible number of decisions. A ruling that requires no engineering action at all is
  the best possible outcome.
- Every ruling you propose must be answerable by the owner in **one line**.

## A1 — Knowledge quarantine
- `QUARANTINE_REVIEW.json`: `quarantined_total = 7`, `owner_decision_required = true`, `verdict = PARTIAL`,
  reason recorded: *"lifting a quarantine is a knowledge-owner authority act; an agent must not self-clear
  a security control"*.
- R3 disposition file: `verdict = DISPOSITION_COMPLETE`; the gate nonetheless stays `PARTIAL` until the
  **sanitizer owner anchors the key pattern** (a candidate is offered in the TT: `(?<![A-Za-z0-9_-])sk-[A-Za-z0-9]{20,}`)
  and the probe re-reads `unique = 160/160`.
- Coverage facts: `unique_input_paths = 160`, `indexed_docs_physical = 153`, `quarantined_by_sanitizer = 7`,
  `released_safe_clean = 2`, `released_safe_reference = 5`, `retained_quarantine = 0`, and the report states
  `physical_coverage: "153/160 — NOT padded"`. **Every one of the 7 has already been individually dispositioned.**
- Scope cost: the sanitizer lives in the **other repo** (`HG-KSEOS/src/hg_kseos/security.py`), so anchoring it
  is a cross-repo WorkOrder, not a change to this candidate. Rebuilding the knowledge index would re-derive a
  136 MB spine.
- Related TTs: `TT-PIPD-KNOWLEDGE-QUARANTINE` (OPEN, SOURCE_GAP),
  `TT-HGK-SANITIZER-UNANCHORED-KEY-PATTERN` (OPEN, CONTROL_PLANE_DEFECT),
  `TT-PIPD-QUARANTINE-VERDICT-LABEL` (OPEN, RECORD_CORRECTNESS).

## A2 — Publication / release / licence
- Published: `main = 3aebbbce948871c07b875ab92acf263d298ecf38` (an R3 candidate mirror). The R4 work is **not
  committed and not pushed**; the remote has zero changes from this round.
- GitHub single-file hard limit = 100 MB. Exactly one file exceeds it:
  `.hgk/rounds/R2-20261009-qualification/execute/knowledge/own-derived.db` = **130.09 MB**.
- `TT-PIPD-LICENSE-001` (OPEN_OWNER_GATE, SOURCE_GAP): close condition = *"declare a license or accept the
  no-license NOTICE"*.
- `TT-PIPD-PUBLICATION-GATE` (OPEN_OWNER_GATE, RELEASE_BLOCKED): close condition = *"an independent lane
  re-verifies the affected edges on the new candidate commit"*.

## A3 — Performance budget provenance
`tools/perf_budget.py --check` → overall `FAIL`. Four rows, **all four carry `source_of_truth: UNPROVENANCED`**:

| metric | measured | budget | verdict |
|---|---|---|---|
| `compile_chain_ms` | 744.5 | 2000 | UNDECIDABLE |
| `validate_19_contracts_ms` | 1.9 | 3000 | UNDECIDABLE |
| `cli_cold_start_ms` | 101.8 | 6000 | UNDECIDABLE |
| `context_bytes_per_artefact` | **343,547** (other runs measured 336,674 and 355,119) | **20,000** | **FAIL, exceeded** |

- No in-repo source of truth exists for any threshold. `TT-PIPD-PERF-CONTEXT-BUDGET-PROVENANCE`
  (OPEN, OWNER_GATE): close condition = *"the owner states a derivation row for the 20000 budget (or a
  corrected budget) and EITHER the c[alculation is shown]..."*.
- The gate is fail-closed and was deliberately restored to fail-closed in this round. **Raising the budget to
  make it green would be weakening a gate** and is forbidden.

## A4 — SPEC/DEL crosswalk evidence gap
- `SPEC_DEL_CROSSWALK.json`: `schema PIPD-SPEC-DEL-CROSSWALK/1`, 57 rows, counts = 32 SPEC + 25 DEL.
- Some rows' source locators could not be resolved, so those rows are recorded as `EVIDENCE_GAP` rather than
  claimed PASS. The documents themselves were **generated** from the canonical IR/trace, not hand-written.

## A5 — The TT register (the roll-up)
- 22 rows, `blocking_count = 18`. Distribution: `open 16`, `open_owner_gate 2`, `partial 2`
  (`PARTIAL_CLOSED` is an alias of `PARTIAL`), `closed 1`, `temp_closed 1`.
- The 20 rows that are not CLOSED, with their classes and close conditions:
  `TT-PIPD-KNOWLEDGE-QUARANTINE` (SOURCE_GAP), `TT-PIPD-AUTHORITY-ASSERT` (EVIDENCE_GAP),
  `TT-PIPD-LICENSE-001` (SOURCE_GAP, owner gate), `TT-PIPD-PREFLIGHT-ORDER` (ADMISSION_ORDER),
  `TT-PIPD-ADMISSION-CHAIN-GAP` (EVIDENCE_GAP), `TT-PIPD-WORKORDER-WORKTREES` (EVIDENCE_GAP),
  `TT-PIPD-TECHADMISSION` (EVIDENCE_GAP, PARTIAL_CLOSED — needs 22 rows with licence/dependency disposition),
  `TT-PIPD-S2-S8` (NOT_RUN — admits S2 as the next WorkOrder), `TT-PIPD-PYCACHE-SECRETSHAPE` (HYGIENE, closed
  in-round by purging bytecode), `TT-HGK-LIFECYCLE-UNLOGGED-TRANSITIONS` (CONTROL_PLANE_DEFECT),
  `TT-HGK-LIFECYCLE-EVIDENCE-UNBOUND` (EVIDENCE_GAP),
  `TT-HGK-ARTIFACT-CONTRACTS-UNREGISTERED` (EVIDENCE_GAP — admit 19 families into the spine),
  `TT-PIPD-PUBLICATION-GATE` (RELEASE_BLOCKED), `TT-HGK-SANITIZER-UNANCHORED-KEY-PATTERN` (CONTROL_PLANE_DEFECT),
  `TT-ORACLE-DISAGREEMENT-KP-R04` (ORACLE_DISAGREEMENT — needs the authorised source to ratify the corrected
  polarity of three R04 oracles), `TT-PRE-W3-CROSS-PROJECT` (TEMP_CLOSED), `TT-PIPD-PERF-CONTEXT-BUDGET-PROVENANCE`
  (OWNER_GATE), `TT-PIPD-QUARANTINE-VERDICT-LABEL` (RECORD_CORRECTNESS — an append-only amendment, or owner
  ratification), `TT-PIPD-GATE-VERDICT-SCOPE-AMBIGUITY` (DESIGN_RESIDUAL — surface a failing hard gate at top
  level), `TT-PIPD-DISCLOSURE-PROSE-STALE` (DOC_CONSISTENCY — reconcile quoted baseline counts),
  `TT-PIPD-WEBCHECK-LAYOUT-DEPENDENCY` (DOC_CONSISTENCY).
- Note several of these are HG-KSEOS-side (the `TT-HGK-*` rows) and therefore outside this candidate's scope.

## V7 — `TT-PIPD-R4-V7-UNTRACKED-GATE-BASELINE`
- The independent acceptance round (W8-VERIFY-3) returned `PARTIAL`: rows V1–V6 and V8 PASS, **V7 NOT_RUN**.
- Reason: two gate tools introduced during this round, `tools/pi_dedup_check.py`
  (sha256 `04e2504ab9d85d91…`) and `tools/deny_list_scan.py` (sha256 `723f896660b175ff…`), are **absent from the
  committed HEAD** — so "the gate was not weakened relative to the committed baseline" cannot be computed.
- The V7 row is the *only* thing keeping the round's acceptance at PARTIAL; everything else passes.
- A commit would also give this round its own baseline for any future round.

## Deliverable
A JSON file `C:\w8v3plan\RULINGS_A1_A5_V7.json` plus a short markdown `C:\w8v3plan\RULINGS.md`, in the shape the
brief specifies. You are a **PLAN/analysis** lane: read-only. Do not modify anything outside `C:\w8v3plan\`.
