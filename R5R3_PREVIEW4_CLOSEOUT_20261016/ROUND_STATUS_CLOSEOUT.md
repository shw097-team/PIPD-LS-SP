# R5R3 closeout round — ROUND_STATUS

Round: `R5R3-20261016-preview4-closeout` (continuation of the preview.4 closeout).
Subject of measurement: the released `v0.1.1-preview.4` plugin ZIP and the round's own records.
Canonical branch state at round time: `main` = `d3bd5456` (previous round's merge).

## Verdict summary (all LOCAL / CANDIDATE-ONLY)

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Release plugin ZIP reproducible from its frozen commit | **PASS (local)** | two builds at `cc6c193` → 68,357 B / `545e359a…`, equals the served asset |
| 2 | Previously host-accepted package reproducible | **PASS (local)** | rebuild at `062d84ae` → 68,355 B / `2f9ae010…` |
| 3 | Private-host import of the release ZIP | **UNRESOLVED (no attempt this round)** | cause narrowed: build nondeterminism and manifest drift excluded |
| 4 | TT-R5R3-02 allowlist amendment | **CLOSED** | workflow on `main` carries the added path; merge delta includes the workflow |
| 5 | TT-R5R3-03 `DRIFT_VALUE` | **NOT REPRODUCED** | declared `codex_sha256` == actual binary; `check_drift` = 0 rows |
| 6 | TT-R5R3-01 credential mechanism | **REMEDIATED (local)** | `push_with_pat.sh`; dry-run authenticates, updates no ref |
| 7 | Canonical SoD: PLAN vs VERIFY_SECURITY | **FINDING (pre-existing)** | `check_sod` → `SOD_VIOLATION` (both `gpt-6.1-sol`) |
| 8 | GSTACK named-method plane | **PASS** | 9 rows, all activation invariants 0 |
| 9 | OPENSPEC change record | **PASS** | `openspec validate … --strict` exit 0 |
| 10 | Release assets carry the later repairs | **NO (finding)** | released wheel's `requirements.py` predates them; on `main` only |
| 11 | External acceptance | **PENDING** | this packet; the mandated checker lane's verdict is attached if it ran |

## What this round did NOT do

No release, no tag, no host install, no directory publication, no production promotion, no force-push, no
rewrite of any released byte. Owner gates `NEW_RELEASE`, `PRIVATE_HOST_INSTALL`, `PUBLIC_DIRECTORY`,
`PRODUCTION`, `S4_FULL_PASS` remain NOT_GRANTED and are carried in `OWNER_DECISION_REQUEST.md`.

## Model plan, declared vs observed

- Declared: PLAN/Orchestrator = GLM-5.3-Flash (opencode-go); EXECUTE (CODEX CLI) = DeepSeek V4.1 Flash
  (opencode-go); VERIFY/SECURITY (CODEX CLI) = DeepSeek V4.1 Flash (opencode-go).
- Observed PLAN: served `glm-5.3-flash`, oneshot session `20261016_132640_b3d9f2`, `agent_close`, exit 0.
- Observed orchestrating session model: not GLM-5.3-Flash; the global agent-model binding was not rewritten
  by this round (that is an owner act).
- SoD residual: EXECUTE and VERIFY share one model, so model-axis independence between maker and checker is
  ABSENT; independence is process/lane/context plus re-derivation only.

## Rollback

Evidence and docs only. The one product-tree change is a new `reproducibility` block inside
`docs/install/ASSET_READBACK_v0.1.1-preview.4.json`; revert it with a single `git revert` of the PR's merge
commit. No immutable object was touched.
