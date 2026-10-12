# MODEL SUBSTITUTION RECORD — S4POST round (consolidated)

Declared plan (owner mandate): PLAN in Hermes = DeepSeek V4.1 Flash (OPENCODE GO);
EXECUTE writer = Codex CLI on DeepSeek V4.1 Flash (OPENCODE GO);
VERIFY/SECURITY = Codex CLI, checker model GPT 6.1 SOL-MEDIUM (OpenAI OAuth).

This file records every deviation from that declaration, with the evidence, so the declared model and
the model that actually served each lane are never silently different.

## 1. VERIFY lane — NO deviation
Both independent acceptance runs used the declared checker model `gpt-6.1-sol` with
`reasoning_effort=medium` through the OpenAI OAuth path, pinned on the command line, and the lane's
own startup header was read back. Receipts: `verify/AO_VERIFY_SUBJECT_F3C80EC_gpt-6.1-sol_medium.log`
(complete) and `verify/AO_VERIFY_SUBJECT_aac68911ce2f_gpt-6.1-sol_medium.log` (this round's re-run).

## 2. EXECUTE writer lanes — the substitution chain
- **Declared**: `opencode-go/deepseek-v4.1-flash`.
- **Failure D-03 (re-confirmed this round)**: on long multi-turn runs (many tool calls) the adapter
  returns HTTP 400 `Upstream request failed: [invalid_request_error] The 'reasoning_content' in the
  thinking mode must be passed back to the API`. Measured this round on the Stage B continuation lane:
  exit 1 after 57,985 tokens with ZERO deliverables written; the FAR v1 lane had died the same way.
  **A one-turn tool-call probe does NOT predict this** — this round's probe returned PROBE_OK with a
  successful shell tool call and exit 0, and the same model then died on the long run. Transport
  proven ≠ work sustainable. Any future claim "D-03 no longer reproduces" requires a long-run
  positive, not a probe.
- **First substitution (previous round, now withdrawn)**: `opencode-go/deepseek-v4-flash`.
  **Withdrawn because the relay no longer serves it** after the restart. The relay at
  `http://127.0.0.1:10102/v1/models` now lists exactly: `gpt-5.3-codex-spark`, `gpt-5.6-sol`,
  `gpt-5.6-terra`, `gpt-5.6-luna`, `opencode-go/deepseek-v4.1-flash`.
- **New substitution (this round)**: **`gpt-5.6-terra`** for bounded writer lanes.
  Probed with a one-turn tool call before use (PROBE_OK, exit 0). `gpt-5.3-codex-spark` was probed
  and is **NOT usable**: `The 'gpt-5.3-codex-spark' model is not supported when using Codex with a
  ChatGPT account.` Recorded so it is not re-probed.
  SoD check: `gpt-5.6-terra` (writer) ≠ `gpt-6.1-sol` (checker) — the writer/checker split holds.
- **Mitigation applied**: the Stage B work was SPLIT into three short sequential lanes (B1 packaging
  tests, B2 web-fallback tests, B3 docs+workflow) to stay well below the turn count where D-03 trips,
  because the failure correlates with run length, not with the task.

## 3. What is NOT claimed because of this
- The EXECUTE lanes did **not** run on the owner-declared model this round. Every writer-produced
  artifact is therefore labelled with the model that actually served it, and no artifact is claimed
  to be a declared-model product.
- The previous round's WIP artifacts are discarded (not continued) for a different reason: two writer
  lanes ran concurrently in one worktree under two different briefs (v1 and v2), so the files
  corresponded to no single specification and could not be attributed. See
  `far-impl/superseded-concurrent-writers/WHY_DISCARDED.md`. Honest note: that discarded code did pass
  its own tests and its `--json` reproduced the independent measurement exactly
  (`checked 1085, match_raw 1038, benign_eol 5, unexplained 42`, `--strict` exit 1) — but a
  self-written suite over an un-attributable mixture is not evidence of a candidate, so the re-run
  proceeds from the reset state under the v2 brief.
