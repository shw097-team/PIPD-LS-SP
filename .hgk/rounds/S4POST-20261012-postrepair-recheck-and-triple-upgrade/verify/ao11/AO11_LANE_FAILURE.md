# AO11 lane failure - no adjudication (provider content filter)

Round 11 ran the canonical `fabric-external-independent-challenge-reviewer` lane on the primary checker
`gpt-6.1-sol` (openai, OAuth, medium) through `run_checker_lane.sh`. The child exited 1 and the wrapper
returned 1. **No `EXTERNAL_CHALLENGE_REPORT.md` was written**, so this round carries **no verdict** - the
same outcome as round 7, and for the same reason.

## Terminal cause, verbatim from the lane log

```
ERROR: This content was flagged for possible cybersecurity risk. If this seems wrong, try rephrasing your
request. If you're doing authorized security work that requires more cyber permissive safeguards, apply
for Daybreak access via https://platform.openai.com/settings/organization/status-and-access before retrying.
ERROR: This content was flagged for possible cybersecurity risk. ...
tokens used
92,667
```

The filter killed the lane at the reporting stage, after it had written 157 evidence files (freeze,
intake, per-case reproducers and raw outputs) but before the report itself.

## What it recorded before dying (verbatim, and NOT an adjudication)

> Two broader counterexamples now reproduce: `HTTP 400: malformed payload; quota remaining 90 percent.`
> triggers a model switch and success, and a failing OS resolver lets the gate qualify while writing
> through the confirmed junction into the clone. Omitting `LANE_ROLE` also admits an unassigned
> model/provider/effort. I'll record these limits alongside the supported repairs and the still-stale
> Stage-B manifest binding.

Three counterexamples, therefore, plus one confirmation:

- **FCR-005 is not closed**: a hard failure spelled `HTTP 400` (not `error 400`/`status 400`) beside a
  quota word still switches models and reports success. The maker's own veto regex misses that spelling.
- **FCR-004 is not closed**: when the OS resolver fails, containment is not decided and the gate qualifies
  while writing through the junction into the clone.
- **The child admits an unroled lane**: omitting `LANE_ROLE` skips its assignment re-derivation entirely,
  so an unassigned model, provider and effort are accepted.
- **FCR-007 confirmed open**: the current Stage-B manifest binding is still stale.

## Also observed, and it is a mechanism working correctly

The wrapper's own output recorded that it did NOT fail over:

```
CHECKER_PRIMARY_FAILED_NOT_EXHAUSTION lane=AO11 exit=1 hard_failure=[400 Bad Request;cybersecurity;error 400;flagged
for possible;invalid_request_error;reasoning_content;status 400;] signature=[     22 quota;     13 429;     10 usage
limit;      8 at capacity;      4 capacity;] - no failover, this is reported not worked around
```

The verdict is right - a content-filter kill must never be worked around by switching models - but the
classification that produced it is unreliable in both directions: every marker it matched came from the
lane QUOTING the sources it was reviewing, not from the lane's own provider call. A textual classifier
over a whole log cannot distinguish a quoted failure from an experienced one.

## Consequence

The 157 files and the three counterexamples are recorded as **partial, machine-generated evidence from an
interrupted lane**, not as findings with a severity and a locator. They are sufficient to drive repair,
which is what the maker does next, and insufficient to close anything.
