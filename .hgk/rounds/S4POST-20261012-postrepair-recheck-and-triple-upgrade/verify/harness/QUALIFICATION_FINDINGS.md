# Qualification findings: what actually breaks, and how often

Measured with the corrected route (`-c model=<slug>` plus `openai_base_url` and
`model_catalog_json`, no `model_provider`), the identical no-write qualification brief, and the identical
CLI. Raw transcripts: `C:\Users\user\AppData\Local\Temp\qual-repeat\`. Raw run text:
`QUALIFICATION_FLAKINESS.txt`, `QUALIFICATION_MATRIX.txt`.

## The rates

| Configuration | Passes | Two-tool round trips attempted |
|---|---|---|
| assigned model `opencode-go/deepseek-v4.1-flash` at effort `high` | 3 | 6 |
| assigned model `opencode-go/deepseek-v4.1-flash` at effort `none` | 2 | 6 |
| backup model `opencode-go/deepseek-v4-flash` at effort `high` | 6 | 6 |
| checker model `gpt-6.1-sol` at effort `medium`, openai route | 1 | 1 |

Six attempts per configuration is a small sample. These are counts, not reliabilities; do not read
"3 of 6" as "50% reliable".

## What the failure is, exactly

The assigned model's failing runs are **not** a failure to use tools. In
`r_opencode-go_deepseek-v4.1-flash_high_1.log` both shell calls succeeded (the second in 547 ms) and the
rejection then landed on the **next** request:

```
Provider error 400: Upstream request failed: [invalid_request_error]
The `reasoning_content` in the thinking mode must be passed back to the API.
```

`tokens used 479`. So the trigger is not transcript size, not the first turn, and not tool use as such.
It is the continuation request **after a second tool result**, in thinking mode.

## The websocket 426 is exonerated by the same data

Every one of the 18 repeat logs contains exactly one
`ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket: HTTP error: 426 Upgrade
Required`, including **all** the passing runs, including the 6/6 clean backup column. The local relay
refuses the websocket and the client falls back to HTTP; that is routine here, and it is not the failure.
This is direct positive evidence for the FAR study's refutation of the 426 hypothesis.

## Axis separation

- **Model axis**: at the same effort (`high`) and the same route, the assigned model passed 3 of 6 and the
  backup model passed 6 of 6. The model is the differentiating factor in this sample.
- **Effort axis**: the assigned model failed at both `high` (3 of 6) and `none` (2 of 6). Changing the
  effort does not rescue it, so the operator's original mixed change (model **and** effort) was not
  required to escape the failure. This is the control the FAR study recorded as NOT_SEPARABLE; it is now
  separable, and the effort axis is not the cause.

## Consequence for the gate, and the repair

A single qualification is a sample of an intermittent fault, so one pass proves very little: the failure
appeared on roughly half of attempts. `run_lanes_gated.sh` now requires **`GATE_QUALIFY_RUNS`
consecutive passes (default 3)** and aborts the lane set on the first failed attempt. With the measured
per-attempt failure rate, one run would have admitted the lane on about half of attempts; three
consecutive passes make that far less likely, and each additional required pass lowers it further.

The honest limit: this raises the cost of a false admission, it does not eliminate it, and the required
count should be raised where a false admission is expensive. The gate is a filter, not a proof.

## What is still not explained

- **Why it is intermittent.** Nothing here identifies whether the adapter drops `reasoning_content` under a
  race, a retry, or a specific interleaving. The upstream message is a requirement statement, not a cause.
- **What the upstream model actually was.** Still unauthenticated. A flaky lane is not evidence of a
  substituted model, and a healthy lane is not evidence of the assigned one.
- The mechanistic lead from the FAR study - the slug being absent from the relay and registry
  reasoning-content preservation lists - remains untested, and is now the most specific thing to test,
  because a list-driven gate would explain an intermittent, model-specific, size-independent failure.

## The gate demonstrated on the real lanes

One invocation of the gate, requiring 3 consecutive passes, against both roles at the same moment:

```
EXECUTE  model=opencode-go/deepseek-v4.1-flash effort=high
  qualification attempt 1/3 PASS
QUALIFICATION_FAILED ... attempt=2/3 exit=1
GATE_REFUSED_NO_WRITERS_STARTED          EXECUTE_QUALIFY_EXIT=7

VERIFY   model=gpt-6.1-sol effort=medium
  qualification attempt 1/3 PASS
  qualification attempt 2/3 PASS
  qualification attempt 3/3 PASS
QUALIFICATION_PASSED (consecutive_runs=3, two tool round trips each)   VERIFY_QUALIFY_EXIT=0
```

This is the point of the gate: the intermittency shows up **inside** a single gate invocation - attempt 1
clean, attempt 2 rejected - and the flaky lane is refused before any writer starts, while the sound lane is
admitted. Record: `REAL_QUALIFICATION_3CONSEC.txt`.
