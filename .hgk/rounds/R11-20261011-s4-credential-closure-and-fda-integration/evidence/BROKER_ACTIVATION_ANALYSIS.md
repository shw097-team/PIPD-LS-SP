# R11 evidence — credential-broker activation analysis

Input to `REQ-PIPD-R11-ACTIVATE-003`. Produced by a bounded fan-out whose result the round then
re-verified itself, with the divergences recorded rather than smoothed over.

## Verdict: DO NOT activate in R11 — admit activation as its own control-plane round

The deliverable of this obligation is the recorded decision and the exact surfaces, not a wiring.

## The measurements (re-run by the round, not merely relayed)

| question | command | result |
|---|---|---|
| does anything outside `scripts/cred/` reference the broker? | `grep -rln -e 'cred_broker' -e 'cred_preflight' <HG-KSEOS> --exclude-dir=.git --exclude-dir=__pycache__` | **4 paths**, broken down below |
| how many does `config/` hold? | `grep -rn -e 'cred_broker' -e 'cred_preflight' -e 'HGK_APP' -e 'HGK_CRED' <HG-KSEOS>/config` | **0** |
| is there a remote to push to? | `git -C <HG-KSEOS> remote -v` | **empty — no remote at all** |

The 4 outside references, classified honestly:

1. `docs/CREDENTIAL_ROTATION_OPERATOR_GUIDE.md` — **documentation**. The only real referrer.
2. `var/far-lane-health-repair-20261011/far-run/FAR-RUN-LANE-HEALTH-013-R5/ExtractionLedger.jsonl` — incidental text.
3. `var/far-lane-health-repair-20261011/writer/dispatch_receipt_pass6.json.logs/attempt-2428-...-stdout.txt` — a run log.
4. `var/shared-spine/hg-kseos.db` — a **binary false positive** in the SQLite file.

**Correction of record:** the fan-out reported "exactly ONE file outside `scripts/cred/`, and it is a
Markdown documentation file". The count is 4; only one is a source referrer. The fan-out's *conclusion*
survives, its *number* did not, and the difference is stated because an exact-count claim that is off by
four is the kind of thing this line has learned to stop rounding.

## Why activation is not a flag to flip here

1. **There is no consumer to wire.** Nothing in the repository performs a git push or any credentialed
   network write, and `AGENTS.md` forbids it in the contract: *"Do not push, merge, deploy, access
   secrets, broaden permissions..."*. `config/project.json` sets `network_default: DENY`. The only place a
   credential-injected push is even prescribed is the operator guide — an out-of-band human/agent action.
   So activation is not "turn on the existing path"; it is **a design decision about whether an in-repo
   push lane should exist at all**, which is governance, not engineering.
2. **The activation surfaces are control-plane mutations.** Activation is an explicit concept here and
   file presence is explicitly NOT it: `config/lane-routing-registry.yaml` carries `status: CANDIDATE`
   and states that *"this registry does not itself confer authority; activation requires an
   HGK-authorized generation binding"*, with a `projections:` block pinning every live site that must
   agree; `config/lane-route-slots.candidate.json` carries an explicit `activation_state` / `activation_costs`;
   `src/hg_kseos/named_methods.py` carries `runtime_required_now`, `current_execution_scope`,
   `ACTIVE_SELECTED` and `evaluate_activation_invariants()`; `registries/PROTECTED_IDENTITY_CLASS_QUALIFICATION.csv`
   carries an `activation` column. Mutation authority for these is WorkOrder-only. The broker appears in
   **none** of them, and its own manifest records `"activation": false`.
3. **Activating it would broaden permission.** Wiring a credential-bearing push capability into a plane
   that contractually forbids push is precisely a permission-broadening change — the opposite of the
   low-resistance engineering decision this round is authorised to take.

## Methodological trap worth keeping

`git grep` is **not sufficient** for this question: most of `config/` is **untracked**, so a git-grep
scan silently skips almost the entire config surface. The 0-count above was obtained by searching the
**working tree**. A control-plane survey that used `git grep` would report a confident zero having read
almost nothing — which is why the count was reproduced independently before being relied on.

## What the round still does NOT know

- Which file would *become* the consumer, if an in-repo push lane were ever authorised.
- Whether an in-repo push lane is intended at all, given the empty remote and `network_default: DENY`.
- The live spine state of `REQ-HGK-CREDBROKER-001` (not queried in this round; its own receipt grades
  that row `RECORDED - NOT INDEPENDENTLY QUERIED`).

**Claim ceiling:** `ACTIVATION_NOT_PERFORMED_BY_DECISION__SURFACES_AND_ZERO-CONSUMER_MEASURED__NO_IN_REPO_PUSH_PATH_EXISTS`.
