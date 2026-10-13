# PLAN leg: declared vs observed (measured)

Date of measurement: 2026-10-13 (UTC+8 session), read by readback script
`skills/software-development/governed-stack-audit/scripts/lane-model-readback.py` against
`<HERMES_HOME>/config.yaml` and the session store. This file records a DIVERGENCE, not a fault report:
the mandated model solution for this task names a PLAN model the live session is not running.

| leg | mandated by the work order | declared in config | observed (measurement) | verdict |
|---|---|---|---|---|
| PLAN (this orchestrator session) | `GPT 6.1 SOL-MEDIUM` (OpenAI OAuth) | main loop `opencode-go / deepseek-v4-flash`; `delegation (PLAN)` `opencode-go / deepseek-v4.1-flash`; `auxiliary.kanban_decomposer` and `auxiliary.triage_specifier` `openai-codex / gpt-6.1-sol` | session `20261013_114601_015679`, model `deepseek-v4.1-flash`, provider `opencode-go`, 708 calls, live | **DIVERGENT** |
| EXECUTE | `DeepSeek V4.1 Flash` (opencode-go), via CODEX CLI | lane `EXECUTE`, sandbox `danger-full-access`, child models `execute_lane_child_models = deepseek-v4.1-flash` | lane probe served `opencode-go/deepseek-v4.1-flash` at rank 1, 2.51 s, nonce present, usage receipt ok | ALIGNED |
| VERIFY / SECURITY | `GLM-5.3-Flash` (opencode-go), via CODEX CLI | lane `VERIFY_SECURITY`, sandbox `read-only` | served `opencode-go/glm-5.3-flash` on all eight checkers of attempts 7-14 | ALIGNED |

Evidence that the mandated PLAN route exists and has been used on this host, so the divergence is a
routing choice and not a missing capability: roll-up `gpt-6.1-sol / openai-codex = 109 sessions,
2094 calls`; `glm-5.3-flash / opencode-go = 63 sessions, 2044 calls`.

Why this is recorded rather than silently repaired: the repair that makes the observation match the
mandate is a durable change to the user's Hermes routing configuration, which applies to every future
session, not just this task. Per the governing convention this round has been following (candidate-only
changes, no self-promotion, no unrequested durable mutation), the change is offered with its exact
command and left to the owner:

    python hermes_cli/main.py config set agent.model openai-codex/gpt-6.1-sol
    python hermes_cli/main.py config set agent.provider openai-codex

Claim ceiling: the table states what the surfaces hold as of the measurement. It is not a statement
about which model produced any individual sentence of this round's output, and it is not an acceptance
of the model solution.

Block-class note: this is the first instance of class `E7 - mandated-vs-observed model routing
divergence` in this round. Class `E6 - self-authored claim contradicted by a checkable record` stands
at 5 instances.
