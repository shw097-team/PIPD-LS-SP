# Design — S4-R2M conditional merge and preview.3 gate

## Context

`main` (`4445db5a6d1b3138946fd7c4fe3b712e4faf1af7`) is an ancestor of the S4-R2 candidate head
(`3f6c7dc52b73cfcba03dccbe576ade75bec1890d`), five commits ahead and zero behind; measured in this
round with `git merge-base --is-ancestor`. The frozen product the independent checker actually scored is
`7c00b64960d86fc1e94848c9955c512a3626a85f` (tree `b08b961061f510d1eb78a944307ecaa446d68eed`). The
public release `v0.1.0-preview.2` (`8faa64e581e8c25f5ec355475e29561847da3ead`) is immutable.

## Goals / Non-goals

**Goals.** Land the two documentation corrections, prove the frozen product with a focused isolated
regression, integrate into `main` under owner approval with a readback, and keep the claim ceiling at
`S4_MVP_BETA` with the deferred items named.

**Non-goals.** No S0–S4 rebuild, no re-tag, no byte change to any published asset, no S5+ activation, no
widening of the affected scope beyond the report's two blockers plus the regression.

## Decisions

**Reconcile before building.** Both named blockers were re-derived against the candidate head rather
than taken from the report: the front page has no `CLI vs Skills` section, and `src/pipd_ls_sp/cli.py`
does declare a subcommand-local `--root` (`dest="sub_root"`) for `project` and `export` while the
front page says the global position is mandatory. Both are therefore genuinely open, and both are
closed in one documentation change.

**The regression runs on a copy, never on the frozen subject.** A suite that writes `.pyc.tmp` beside
modules mutates its own subject; the checker's refusal to do that is correct. The round therefore runs
the affected modules in a disposable writable clone built from the frozen candidate head, and the
read-only subject's bytes are compared before and after.

**A version strictly greater than the installed one.** `0.1.0a3`, `0.1.0b3` and `0.1.0rc3` all sort
below `0.1.0` under PEP 440, so they cannot be offered as an upgrade to existing `preview.2` users.
Any `preview.3` distribution therefore carries a version greater than `0.1.0` (for example
`0.1.1a3`), verified with `packaging.version.Version` before the build and by
`importlib.metadata.version` after an isolated install.

**What the round does not confer.** A compiler PASS is gate evidence, not runtime readiness. A maker
measurement is not independent acceptance. A merge is not a release. Publication is not production.

## Risks

- If `main` moves before integration, the correct outcome is `MERGE_DRIFT_BLOCKED` plus an affected-only
  reconciliation, never a forced or rewritten history.
- If no valid write credential is proven, the correct outcome is `MERGE_READY_HITL_PENDING`; the
  candidate is preserved and nothing is recorded as merged.
