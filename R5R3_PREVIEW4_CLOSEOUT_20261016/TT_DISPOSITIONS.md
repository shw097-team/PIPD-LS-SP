# TT dispositions — round R5R3-20261016

Each row states the live measurement, the disposition, and the residual. Nothing here is inferred from a
prior round's summary; every verdict names the surface it was read from.

## TT-R5R3-01 — credential mechanism for the repository push
**Disposition: REMEDIATED (durable mechanism landed).**
- Mechanism: `push_with_pat.sh` (round dir) encodes the working credential shape once: inline credential
  helper, `credential.helper=` cleared first, `credential.interactive=always`. The token is read from the
  owner's key file at use time; only the file path appears in the process list. No value is written to the
  script, to config, or to any log.
- Proof: a `--dry-run` push through the wrapper authenticates without updating any ref (see
  `raw/push_dryrun.log`), and the round's real evidence push used the same wrapper (proving it in the real
  path, not only in a probe).
- Residual: the key-file path is a host convention, overridable with `PIPD_PAT_FILE`. The wrapper is not a
  credential store and does not rotate anything.

## TT-R5R3-02 — stage-c write-set allowlist amendment
**Disposition: CLOSED (landed on the canonical branch, verified from the branch itself).**
- Surface read: `origin/main` at `d3bd5456`; the merge's delta set is exactly 6 paths and includes
  `.github/workflows/public-plugin-verify.yml`, whose allowlist block on `main` now carries the path this
  round's write set needed.
- Hosted effect: the job's own "wrote only inside its allowed set" step is a positive allowlist; the hosted
  run for the merged generation is green (recorded in the previous round's gate readback).
- Residual: none claimed beyond that generation. A later write set touching a new path would need its own
  amendment — the allowlist is not a blanket permission.

## TT-R5R3-03 — `DRIFT_VALUE` on the GSTACK/readback surface
**Disposition: NOT REPRODUCED (closed as not-reproducible-by-measurement; NOT closed as "fixed").**
Two independent live surfaces were measured, both clean:
1. the declared `codex_sha256` in `config/hermes-codex-lane.json` equals the SHA-256 of the actual
   `codex.exe` at the declared path (`e98c516f1c893578…`, full-value match);
2. `lane_policy.check_drift(registry=reg)` returns **0 rows** against the live registry (epoch 21,
   status CANDIDATE, `source_of_routes.revision` 21).
- Interpretation, stated as interpretation: either the drift was already repaired outside this round, or the
  observation came from a stale copy/pointer that is now superseded. The evidence does not distinguish those
  two, so neither is asserted.
- Residual: if a drift is observed again, it must be quoted with the file, the pointer and the two values.

## New finding raised by this round's measurement (not a TT)
`lane_policy.check_sod(PLAN, VERIFY_SECURITY)` → `SOD_VIOLATION maker_model=gpt-6.1-sol == checker_model=gpt-6.1-sol`
because both lane routes' top-level model is `gpt-6.1-sol` in the live registry. This is a **canonical
configuration collision that predates this round**; `check_drift` cannot see it (it compares projections, not
SoD pairs). Classification: CANONICAL / owner-or-WorkOrder act. The round hands it over and does not patch the
registry from a product round. Claim ceiling: the cross-pair checks that remain OK are
`maker_exe_vs_checker` (deepseek-v4.1-flash != gpt-6.1-sol) and `planner_vs_maker`.

## Mandated model plan for this round — declaration vs observed
- Declaration (owner order, this turn): PLAN & Orchestrator = GLM-5.3-Flash (opencode-go); EXECUTE (CODEX CLI)
  = DeepSeek V4.1 Flash (opencode-go); VERIFY/SECURITY (CODEX CLI) = DeepSeek V4.1 Flash (opencode-go).
- Observed for the PLAN lane: the FAR decision turn was served on `model: glm-5.3-flash`, `source=oneshot`,
  session `20261016_132640_b3d9f2`, ended `agent_close`, exit 0 — read from the runtime's own session store,
  not from the config file.
- Observed for this orchestrating session: the live session model is not GLM-5.3-Flash. The global
  agent-model binding was NOT rewritten by this round; switching the session model is an owner act, offered
  here as a decision.
- **SoD residual from the mandate:** writer and checker are the same model, so model-axis independence
  between EXECUTE and VERIFY/SECURITY is ABSENT. Independence rests on process, entry point, lane, fresh
  context and the checker's obligation to re-derive rather than read the maker's report. Do not read this
  round as having model-level separation.
