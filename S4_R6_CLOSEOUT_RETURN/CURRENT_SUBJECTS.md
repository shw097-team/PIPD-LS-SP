# CURRENT SUBJECTS - read this before acting on any commit id in this packet

This packet was produced across several steps, so earlier documents inside it name the heads that were
current *when they were written*. This file is the single authority for what is current.

| role | ref | current sha |
|---|---|---|
| product head (PR #18) | `origin/fix/s4r6-closeout-doc-identity-and-update-route-20261016` | `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20` |
| evidence head (this packet's branch) | `r6-closeout-evidence-20261016` | `d2f61020706aa379698f251c145e45cf842a83ef` |
| release base | `origin/main` | `d3bd5456afbff21a8c8837994a49f57be3e1b97e` (untouched) |

Superseded heads appearing anywhere in this packet are **history, not current**:

- `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba` - the R17 product head (write-set-gate amendment only), superseded by `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20`.
- `0b50d3edc3c31feff6b674d34e2e3e833aaa7687` - an earlier evidence tip, superseded by `d2f61020706aa379698f251c145e45cf842a83ef`.
- `552bbde073806e254f84e95039f05c9767608aa1` - the first per-round candidate, superseded by both of the above.

## Model-axis independence does NOT exist in this round

By owner order 2026-10-16 (HG-KSEOS registry `SOD006-C3`, `OWNER_ORDERED_IN_FORCE`), the EXECUTE maker and the
VERIFY_SECURITY checker are the **same model identity** (`opencode-go/deepseek-v4.1-flash`). Any statement in this
packet claiming a "different model axis" or "model-axis independent" checker is **false and superseded** by this
statement. What this round does have: process-, lane- and evidence-path independence, plus the no-self-acceptance rule.

Round-relative truths that do not change with the head: `S4_FULL_PASS` / `HOST_QUALIFIED` / `PRODUCTION` =
NOT_GRANTED; private-host UAT = NOT_RUN; merge/tag/release = OWNER GATE only.
