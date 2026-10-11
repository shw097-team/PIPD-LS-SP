# Independent acceptance — R10 owner-item adjudication (cross-model re-verification)

Round `R10-20261011-s4-bclass-decisions`. Verifier: `openai-codex/gpt-6.1-sol` (medium effort) via
`HG-KSEOS/scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY`. The verifier is a **different model
family from the producer** and re-ran every check itself. It was told to look for reasons to doubt, and
to state what it could not establish.

## Receipts

| field | value |
|---|---|
| `ok` | `true` |
| `required_arm` / `served_arm` | `openai-codex/gpt-6.1-sol` (identical; `used_rank 4`) |
| relay | `openai-p6a1fe3` / `gpt-6.1-sol` / HTTP `200` / effort `medium` |
| nonce | present |
| subject mutation | `mutated=False`, 4041 → 4041 files, digest identical |
| attempts | **exactly one** attempt directory — no parallel writer |

Run history on this same subject, in order:

| run | verdict | cause |
|---|---|---|
| 3 | `FAIL` (2 items) | real artefact defect: a **second** dangling pinned target, only found by re-running after fixing the first |
| 4 | `PASS` 12/12 | after the class was fixed and the over-asserting receipt table was graded by evidence class |
| 5 | `FAIL` (1 item) | **a claim of mine was false** — see below |
| 6 | `PASS` 12/12 | after the false claim was corrected |

## The correction that run 5 forced

Run 5 FAILed one item only, and it was right. The FAR had asserted that two accounting axes "do **not**
reconcile" and that the difference was "recorded, not smoothed over". **That was false.** R9 had already
reconciled them, arithmetic in writing (`SPEC_DEL_ACTIVE_GAPS_AUDIT.md` lines 26-52), confirmed by an
independent re-count.

Corrected and re-derived for this round, which closed 2 of R9's 10 active rows (`DEL-015`,
`PIPD-SP-SPEC-030`):

- file `status` axis: `EVIDENCED 44 / EVIDENCE_GAP 9 / DESIGN_ONLY 4` (Σ 57)
- S4-active axis: `30 / 8 / 19` (Σ 57)
- cross-terms: `44 = 30 + 14`, `9 = 8 + 1`, `4 = 4`, `19 = 14 + 1 + 4`
- the single row separating the two axes remains `DEL-008`, deferred by its `S1/S5` stage, **not closed**

The failure mode is the point: guarding against *smoothing a discrepancy over*, the FAR **manufactured**
one. Declaring something "unreconciled" is itself an unchecked claim — the same class of error as
asserting a PASS without running the check, pointed the other way.

## Claims the verifier reached, per item

Items 1-12 all `PASS` on run 6. Notably item 3 required the verifier to re-derive the S4-active axis
itself from the audit's 10-row list, and item 6 required it to judge whether the correction's admission was
accurate rather than merely apologetic.

## What this verdict does NOT cover (verbatim from the verifier)

- "No requested numbered claim remains unestablished within its stated scope."
- "Live MCP absence and production engineering correctness are not established by the repository oracle."
- "Complete current-worktree publication coverage is not established: the requested validator reports three
  uncovered paths."
- Claim ceiling (verbatim): "PASS covers only the corrected accounting reconciliation, the inspected row
  and validator behavior, the four-test repository oracle, the pinned-subject publication check, and the
  observed remote tag identities, not live capability, production readiness, or complete current-worktree
  publication coverage."

## Standing limits — unchanged by this PASS

- Cross-model verification is a **different model family on the same control plane and the same host**. It
  is **not** external acceptance. `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS` and
  `PRODUCTION_VERIFIED` remain **ungranted**.
- `EVIDENCED` is not `PASS`; a count is not a result.
- Disclosed separately: an earlier verification run was **not** aborted when reported to be (a `taskkill`
  invocation was mangled by the shell and its error was hidden). That run completed in parallel and wrote
  the same output path. The result acted on was confirmed, by its item wording, to be the corrected
  prompt's — but the concurrent write cannot be fully excluded, and is stated here rather than hidden.

**Claim ceiling:**
`R10_OWNER_ITEMS_ADJUDICATED__MCP_SCHEMA_RATIFICATION_DECLINED__CROSSWALK_RECLASSIFIED_WITH_EXECUTED_ORACLE__AXES_CLAIM_CORRECTED__CROSS_MODEL_RE_VERIFIED_PASS_12_OF_12`.
