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
**Disposition: CLOSED on the strength of the previous round's recorded merge — NOT re-derivable from this packet.**
- Surface read (this round): `origin/main` at `d3bd5456`; the merge delta set is exactly 6 paths and includes
  `.github/workflows/public-plugin-verify.yml`, whose allowlist block on `main` now carries the path this
  round's write set needed. The hosted gate for that generation is green.
- **Correction after independent check:** an earlier wording said "verified from the branch itself". This
  packet carries no git-object or remote-branch readback of its own, so that phrasing overstated what a reader
  of THIS packet can re-derive. What the packet supports is: the amendment is recorded as landed by the
  previous round's merge, and this round separately exercised the same gate positively (PR #17's `verify` and
  `offline-gate` both succeeded on a write set inside the allowlist).
- Residual: a reviewer wanting object-level proof must re-derive it from the remote; it is not in this pack.

## TT-R5R3-03 — `DRIFT_VALUE` on the GSTACK/readback surface
**Disposition: REPRODUCED at registry epoch 19; NOT PRESENT at epoch 21. The earlier "NOT REPRODUCED" wording is WITHDRAWN.**
- The drift row **is inside this packet**: `raw/gstack_readback.json` (a measurement taken at registry
  **epoch 19**) records `code DRIFT_VALUE`, `path config/hermes-codex-lane.json`, `pointer /codex_sha256`,
  `expected D13914CED6C7AF174D8D638DB938284231227312104B06A25E9608C632A7DAEC`,
  `actual e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e`, `drift_is_clean: false`. That is a
  real, reproduced drift against a registry whose `/codex_sha256` projection then held the older value.
- This round's fresh probe (`raw/control_plane_probe.json`) measures registry **epoch 21**: `check_drift`
  returns **0 rows**, and the declared `codex_sha256` equals the SHA-256 of the actual `codex.exe`
  (`e98c516f1c893578…`, full-value match) — i.e. the projection was advanced to the live binary by an act
  outside this round, or the row is no longer produced. The evidence does not distinguish "repaired" from
  "superseded by a later epoch", so neither is asserted.
- **What went wrong in the first wording:** it reported the clean epoch-21 measurement as though no drift had
  been reproduced anywhere, while the pack it shipped contained the epoch-19 row that reproduces it. The
  corrected disposition above is the fourth shape rule applied: a claim must be stated so the packet's own
  artefacts cannot refute it.
- **Hygiene finding (new):** `raw/` mixes measurements from different rounds and epochs with no dating, so two
  probes can both be honestly labelled "live" while disagreeing. This round's pack therefore ships
  `ARTIFACT_DATING.md` naming each readback's epoch; the underlying hygiene (one dated subdirectory per
  measurement) is an owner-ready process item, not something this round silently fixed.

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
