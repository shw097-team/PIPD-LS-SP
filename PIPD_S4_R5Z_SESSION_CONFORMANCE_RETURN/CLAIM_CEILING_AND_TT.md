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

- **R5Z-TT-004 (CLOSED)** — the first independent verdict returned `overall=FAIL`
  on check A: three cited locators did not resolve as written (`01_subject/pkg_alignment.json`,
  `PIPD_S4_R4_EVIDENCE_RETURN/05_AXES.md`, a relative `API KEY/...` path) plus two wrong identifiers (README
  commit `2553e1e` instead of the branch's `367203f`; evidence-branch head `51bd8e5` instead of `3f2f095`).
  All five are corrected in the answer document; the FAIL verdict is retained, not overwritten.

## Concurrency observed on the Shared Spine (disclosed, not resolved)
While this round ran, other actors wrote admission rows to the same spine for the same round name:
`REQ-R5Z-SESSION-CONFORMANCE-001` with `TS-R5Z-07..09` (writers `hermes-plan-glm-5.3-flash` /
`codex-cli-glm-5.3-flash`, created 2026-10-14T03:53:03Z) alongside this round's own
`REQ-PIPD-R5Z-CONFORMANCE-001` (04:12:55Z). Spine actors active on 2026-10-14 include
`hermes-plan-glm5.3-flash` (17 events), `lifecycle-controller` (8), `hermes-main-GPT61-SOL-medium-orchestrator` (7).
Consequence: this round's admission is duplicated; the duplication is recorded rather than silently merged or deleted.

- **R5Z-TT-005 (CLOSED on arm5)** — lane arm binding is non-compliant on both dispatched legs:
  EXECUTE receipt `ok=false / ERR_REQUIRED_ARM_NOT_SERVED` (required `opencode-go/deepseek-v4.1-flash`, served
  `openai-codex/gpt-6-luna` rank 3); VERIFY_SECURITY recheck receipt `ok=false / ERR_REQUIRED_ARM_NOT_SERVED`
  (required `opencode-go/glm-5.3-flash`, served `opencode-go/deepseek-v4.1-flash` rank 1, 636 s, nonce present).
  Root cause: the pool (`config/lane-route-slots.candidate.json`) orders `opencode-go/deepseek-v4.1-flash` first for both
  lanes, so an unforced dispatch serves it and the receipt then flags the required-arm mismatch.
  Remedy applied: re-dispatch VERIFY_SECURITY with `--force-rank 3 --require-arm opencode-go/glm-5.3-flash` (arm3);
  EXECUTE was not re-dispatched (its artifacts are digest-validated by direct measurement). Until a receipt shows the
  required arm served, no claim of GLM-5.3-Flash independent verification is made.
- **R5Z-TT-005 raw-column evidence (added)**: `dispatch_receipt.json.attempts.ndjson` for attempt 1 carries a single row
  `rank1 = opencode-go/deepseek-v4.1-flash`, `exit=TIMEOUT` (1800.04 s), `nonce_present=false`; the recheck receipt carries
  `rank1 = opencode-go/deepseek-v4.1-flash`, `exit=0`, `nonce_present=true`. Both verdict files self-report `model: glm-5.3-flash`,
  which the raw rows contradict. Consequence: no GLM-5.3-Flash verdict exists for this round; the two verdicts' *measurements*
  remain valid and reproduce the maker's own recomputation.
- **Ceiling note**: the only receipt-backed facts are the dispatcher receipts themselves and the maker's/checker's direct
  measurements (PKG hashes, ZIP digests, locator resolution). No receipt-backed *independent checker* pass exists yet.

## Receipt-backed verification, final state
A `GLM-5.3-Flash` (opencode-go, forced rank 3) verdict now exists that satisfies every binding condition in the same
turn: `ok=true`, `served_arm == required_arm`, CLEAN subject window, content-bearing `overall=PASS` against the frozen
subject sha `a431ac09…`. See `VERDICT_ARM5_PASS.json`, `LANE_RECEIPT_VERIFY_arm5.json`, `ARM5_AND_CLOSURE.md`.
Nothing else in this round claims OpenAI review, publication, host qualification or third-party verification.
