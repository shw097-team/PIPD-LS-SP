### R5R3 closeout round — findings pushed for external acceptance

Round `R5R3-20261016-preview4-closeout`. Subject: the released `v0.1.1-preview.4` plugin ZIP and this
round's own records. All verdicts below are **LOCAL / CANDIDATE-ONLY**; none is an acceptance.

| # | Item | Verdict | How to re-derive it |
|---|---|---|---|
| 1 | Release plugin ZIP reproducible from its frozen commit | PASS | build twice at `cc6c193`; both → 68,357 B / `545e359a…` |
| 2 | Previously host-accepted package reproducible | PASS | rebuild at `062d84ae` → 68,355 B / `2f9ae010…` |
| 3 | Private-host import of the release ZIP | UNRESOLVED, not attempted this round | cause narrowed: nondeterminism and manifest drift excluded |
| 4 | TT-02 stage-c allowlist amendment | CLOSED | workflow on `main` carries the added path; merge delta includes it |
| 5 | TT-03 `DRIFT_VALUE` | NOT REPRODUCED | declared `codex_sha256` == actual binary; `check_drift` = 0 rows |
| 6 | TT-01 credential mechanism | REMEDIATED | `push_with_pat.sh`; dry-run authenticates, updates no ref |
| 7 | `check_sod(PLAN, VERIFY_SECURITY)` | FINDING (pre-existing) | probe output in the evidence packet |
| 8 | GSTACK named-method plane | PASS | 9 rows, all activation invariants 0 |
| 9 | OPENSPEC change record | PASS | `openspec validate … --strict` exit 0 |

The round's single product-tree change is the `reproducibility` block in this PR. Everything else is evidence
and governance record on the evidence branch `r5r3-closeout-evidence-20261016`.

Owner gates `NEW_RELEASE`, `PRIVATE_HOST_INSTALL`, `PUBLIC_DIRECTORY`, `PRODUCTION`, `S4_FULL_PASS` remain
NOT_GRANTED; the three one-action decisions are prepared in `OWNER_DECISION_REQUEST.md`.

Model plan for the round: PLAN/Orchestrator = GLM-5.3-Flash, EXECUTE = DeepSeek V4.1 Flash (CODEX CLI),
VERIFY/SECURITY = DeepSeek V4.1 Flash (CODEX CLI). Writer and checker share a model, so model-axis
independence between them is ABSENT; independence is process/lane/context plus re-derivation only. That
residual is disclosed, not papered over.
