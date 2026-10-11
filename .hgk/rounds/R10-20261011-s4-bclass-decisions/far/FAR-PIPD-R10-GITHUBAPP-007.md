# FAR-PIPD-R10-GITHUBAPP-007 — the write path, proven through the broker

Closes the one item that `FAR-PIPD-R10-GITHUBAPP-006` explicitly left unproven: that the credential
broker can **write**, not merely read. That FAR's end-to-end evidence was a `ls-remote` (a read), and it
said so. This one performs a real `git push` with the broker supplying the credential.

## Why this FAR exists at all

After FAR-006 the remaining items were listed as: delete the redundant personal App, retire the PAT, wire
the broker into the write lane, and prove the write. The first two need an interactive GitHub sign-in
(the browser session had been logged out again and would have cost the owner another 2FA round); the third
is a control-plane change needing its own admission. **The fourth needs nobody, and was still dropped.**
Stopping the whole line because *some* of the remainder is out of reach is exactly the over-conservatism
this line has been correcting all round, pointed the other way. So it is done here.

## Method

The credential is supplied only through the broker's child-process environment; the push URL carries no
secret, and the broker redacts git's output and reports `secret_leaked`.

```
python scripts/cred/cred_broker.py run -- push https://github.com/shw097-team/PIPD-LS-SP.git main
```

with `HGK_APP_ID` / `HGK_APP_KEY` / `HGK_APP_INSTALLATION_ID` / `HGK_REPO_SLUG` in the environment
(environment only — never argv). Readback afterwards by an **independent** `ls-remote` that does **not**
use the broker, so the broker is not confirming its own claim.

## Result

See `WRITE_PATH_PROOF.txt` in this directory for the raw receipt of the push and the independent readback.

## The gap this leaves behind, stated as a gap

The broker is now functionally complete and end-to-end proven for **both** read and write, yet it remains
**NON-ACTIVATED**: nothing in the control plane's `config/` references it. That is deliberate — wiring it
into the write lane changes how writes happen and must be its own admitted control-plane round, not a
side effect of a product round. **A working capability that nothing calls is not a delivered capability**,
and this FAR does not claim otherwise.

## The authorisation gap (the same one FAR-005/006 recorded, unchanged)

All four registered ACTIVE routes are XQ / guard-verification scoped. **No route covers browser or GitHub
account operations**, so this work ran under guardrail **condition 1** (the owner's explicit in-turn
authorisation) each time — a per-turn grant, not a standing one. Making this repeatable requires a new
route plus a WorkOrder admitted to the shared spine. The registry's own rule is
`mutation_authority: ADMITTED_HGK_WORKORDER_ONLY`, and the plane's hard invariants include
`MAY NOT SELF-PROMOTE`. **So the route is proposed here and deliberately not created** — self-issuing an
automation authority is the exact act the framework forbids.

## What is honestly still open

| item | who can close it |
|---|---|
| Delete the redundant personal App (ID 5270409, still holds a key pair) | owner — a browser sign-in; ~3 clicks |
| Retire the PAT `HGK-SWOF-ACCEPTANCE-BRIDGE` (now unused; the broker prefers the App) | owner — GitHub UI; closes FAR-PIPD-R9-CREDROT-005's bridge |
| Wire the broker into the write lane / any activation | a separately admitted control-plane round |
| A route for browser/account automation | a WorkOrder admitted to the shared spine |
| `FULL_S0_S4_INDEPENDENT_PASS` / `G_RELEASE_FULL_PASS` / `PRODUCTION_VERIFIED` | external acceptance |

**Claim ceiling:**
`FOUR_OWNER_STEPS_EXECUTED__APP_BROKER_PROVEN_FOR_READ_AND_WRITE_END_TO_END__STILL_NON_ACTIVATED_WITH_NO_ROUTE_COVERING_THIS_WORK_CLASS`.
