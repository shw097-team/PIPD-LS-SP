# R5Z claim ceiling / NOT_RUN register / TT register

## Claimed (with raw evidence)
- `PRIVATE_PLUGIN_CREATED_INSTALLED_INVOKED` — owner's own ChatGPT account, 2026-10-14 (`09_ui_*/PRIVATE_PLUGIN_INSTALL.json`).
- `BUILD_CANDIDATE` — ZIP 68,355 B sha256 `2f9ae010…d199`, reproduced this round at the pinned commit `062d84a`.
- `EVIDENCE_PUBLISHED_TO_REMOTE` — branches + remote readback + CI receipts (this round).
- `DOC_SYNC_READMEPAGE` — README private route + ADR-0007, gate-green (PR #8).

## NOT claimed
- `PUBLIC_DIRECTORY_PUBLISHED`, `PUBLIC_CONSUMER_VERIFIED`, `REVIEW_APPROVED`, `MERGE_EXECUTED`, `PREVIEW_RELEASED`, `HOST_QUALIFIED`, `S4_FULL_PASS`.

## NOT_RUN / EVIDENCE_GAP
- PR #3 / PR #5 merge (owner platform action); Preview tag + ReleaseTuple + wheel fresh-install (Release Owner).
- Private plugin uninstall/retract negative case; install on an unrelated account.
- Other hosts (Hermes/Codex GUI/CLI/native) effective-load tests.
- `S4_HOST_QUALIFICATION`.

## TT register
- **R5Z-TT-001 (OPEN)** — PLAN lane model deviation: the owner's lane spec declares PLAN = GLM-5.3-Flash (OPENCODE GO); this session's active model was `deepseek-v4.1-flash` (opencode-go). Consequence: the PLAN leg is made by the same model family as the EXECUTE leg, so PLAN/EXECUTE separation is by *engine* (Hermes vs bounded CODEX CLI worker), not by model identity. Remedy options: (a) accept as declared-separation-by-engine; (b) rebind the session's PLAN model to GLM-5.3-Flash and re-run the conformance question set; (c) record owner waiver.
- **R5Z-TT-002 (CLOSED_THIS_ROUND)** — Evidence packages were not on the remote for external acceptance. Closed by publishing `r5z-evidence-return-20261014` with remote readback.
- **R5Z-TT-003 (CLOSED_THIS_ROUND)** — A branch carrying both the README change and the evidence went red at the Stage-B positive write-set gate. Closed by separating branches; the allowlist was NOT widened.
- Note: the ZIP digest is **commit-bound**; any cross-commit digest comparison is void by construction (recorded so it is not re-raised as a defect).
