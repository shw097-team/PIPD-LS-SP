# Evidence branch — PIPD-LS-SP S4 R6 closeout / FAR-R17

This branch carries the **evidence** for the round whose **product change** is on
`fix/s4r6-closeout-doc-identity-and-update-route-20261016` (pull request #18, head `127ec1c`).

Why two branches: the repository's own `verify` gate judges a governed **product** write set and
deliberately refuses a round's receipts inside it ("an exclusion a reviewer can read beats a permission a
reviewer has to notice"). Putting this packet on the product branch made that check red; moving it here
made it green without widening the gate. The earlier product-branch tips (`3e1bc6d`, `5defc64`) are
preserved on this branch rather than destroyed by the rewrite.

## What is here

| Path | What it is |
|---|---|
| `S4_R6_CLOSEOUT_RETURN/` | the round's return packet; `SHA256SUMS` covers every file in it (LF-normalised) |
| `S4_R6_CLOSEOUT_RETURN/R17_RED_GATE_DIAGNOSIS.md` | the red check this round caused, its reproduced cause, and why the two violations were repaired differently |
| `S4_R6_CLOSEOUT_RETURN/R17_MEASUREMENTS.json` | every number the orchestrator and the independent checker measured, labelled by who measured it, with the denominator warning |
| `S4_R6_CLOSEOUT_RETURN/R17_AMENDMENT.diff` | the exact, named write-set amendment |
| `S4_R6_CLOSEOUT_RETURN/R17_check_write_set.py` | re-runnable: reads the allowlist regexes and the declared base **out of the workflow** and classifies `BASE...HEAD` |
| `S4_R6_CLOSEOUT_RETURN/RESIDUAL_UNIVERSE.tsv` | 37 located residual / gap / owner-decision / candidate items |
| `S4_R6_CLOSEOUT_RETURN/DEFECT_DOSSIER.md` | the checker capability gap (closable in-contract) and the pool-order state (owner-ordered, with a fenced candidate diff marked NOT APPLIED) |
| `far-r17/` | the FAR R17 run: decision question, method, findings, verdict (ranked action set), learning, deviations, source inventory, self-evolution delta, the three lane briefs, the lane runner, and the extracted checker verdicts |

## How to verify from a fresh clone

```bash
git fetch origin r6-closeout-evidence-20261016
git show origin/r6-closeout-evidence-20261016:S4_R6_CLOSEOUT_RETURN/SHA256SUMS | sha256sum -c -
```

Then read `S4_R6_CLOSEOUT_RETURN/R17_MEASUREMENTS.json` and re-run any line whose command is given.

## Claim ceiling for this branch

Everything here is **evidence for a candidate**. No merge, tag, release, host qualification or production
claim is made anywhere on this branch. `S4_FULL_PASS` / `HOST_QUALIFIED` / `PRODUCTION` are **NOT_GRANTED**;
private-host UAT is **NOT_RUN**. The independent checker's own ceiling is quoted verbatim in
`far-r17/lane/verify_final/verdict_final.txt`.
