# Why the verification lane produced no verdict, and what was actually wrong

This file corrects an earlier, partly wrong reading of the three failed verification-lane attempts.
It is written by the executor of the round.

## The correction

`evidence/12_GATES/AO_LANE_OUTCOME.json` recorded that attempts 2 and 3 ended in
`ERR_NO_ARM_EMITTED_NONCE` and attributed it to the sandbox refusing the checker's `pwsh` command.
The refusal is real - it is in the preserved stderr - but it was **not the decisive cause**, and
describing it that way made an avoidable harness mistake look like a model or sandbox limitation.

The decisive cause:

- `HG-KSEOS/scripts/hgk-lane-dispatch.py` declares the nonce as
  `ap.add_argument("--nonce", default="HGK_LANE_NONCE_OK")`, and its verdict requires that exact
  string to appear inside an assistant message item - carrier `item.completed` / `agent_message`
  (`nonce_in_agent_message`), not merely anywhere in stdout.
- The dispatcher does **not** append the request to the prompt. The caller has to ask the checker to
  echo the token.
- This round's prompts never asked for it, and the driver never overrode the default. An arm could
  therefore answer the question correctly and still read `ERR_NO_ARM_EMITTED_NONCE`.

So the lane failed closed on a token nobody asked for. That is a defect in this round's own
invocation, not evidence about the checker's capability.

## What that changes and what it does not

- It does **not** turn any claim into a verified one. No verdict exists yet; the claim ceiling is
  unchanged.
- It **does** invalidate the earlier wording wherever it said the lane could not serve the checker.
  Attempt 1's 300-second timeout remains a genuine timeout. Attempt 2 is the one that answered in
  prose and declined; it should have been read as "the checker wanted an audit it could perform
  without executing anything".
- It supplies the remediation the checker itself named: a **text-only dry audit** over the captured
  receipts, which needs no tool calls at all.

## Attempt 4 - what was changed, and only that

1. The prompt now ends by asking for the exact token on its own line, which is what the dispatcher
   always required.
2. The prompt states that no command may be executed and that reasoning must be over the supplied
   material only - addressing the sandbox refusals without widening the sandbox. The lane still runs
   with its own `read-only` sandbox and the same forced rank and required arm; nothing about the
   checker's identity or the allowed arm changed.
3. The raw receipts are inlined into the prompt so the audit is possible without a single tool call.

`--allow-sandbox-escalation` was **not** used, and no substitute arm was introduced. If attempt 4
also returns no verdict, the honest record is that the mandated checker produced none, and the
question of who accepts this candidate returns to the owner.

## Status at the time of writing

Attempt 4 was dispatched against the Stage A and Stage B heads of the pushed branches, with its
invocation receipt written next to the run. **Its result is not yet in this file** - this round has
already committed evidence before a producer had stopped once, and will not repeat that.
