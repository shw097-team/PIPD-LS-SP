## What this changes

One file, +15 lines: `docs/install/ASSET_READBACK_v0.1.1-preview.4.json` gains a `reproducibility` block.

It records a fact an external reviewer can re-derive: the plugin ZIP that release `v0.1.1-preview.4` serves
is the **byte-exact deterministic output of the commit the release tuple already records** (`cc6c193`). Two
independent builds at that commit produce 68,357 B / `545e359a…`, identical to the served asset. The block
carries its own claim ceiling: this proves provenance and determinism of the served bytes, **not** host
acceptance, and **not** that the release carries later commits.

No product source, schema, workflow or test is touched. The release's own identity suite
(`tests/test_r5r3_install_route_identity.py`, 10 tests) passes against this tree.

## Why it matters for the open questions

The private-host import of this release's plugin ZIP was refused server-side on 2026-10-14 with no error
code, and the cause is still unresolved. This change removes build nondeterminism from the candidate causes
and pairs with an offline member-level comparison against the package a previous round installed
successfully: every member shared by the two packages is byte-identical; only two provenance metadata
members differ. Manifest location and manifest fields are therefore excluded as causes, and the surviving
hypothesis is account/platform side.

## What is NOT claimed here

- Not host acceptance. The import is still unproven and the cause still unresolved.
- Not that the release carries later repairs: the served wheel's `requirements.py` predates them; the repairs
  are on `main` only. Whether to cut a successor is an owner decision, not this PR's.
- No release, tag, install, directory publication or production promotion was executed in this round.

## Residuals handed over (details in the evidence return)

1. `NEW_RELEASE` — successor carrying the later repairs; contingent on the import decision.
2. `PRIVATE_HOST_INSTALL` — one consented import attempt of the served package, then (only if refused) the
   previously accepted package, as the discriminating experiment.
3. Canonical SoD finding (pre-existing, not caused by this round): `check_sod(PLAN, VERIFY_SECURITY)`
   reports `SOD_VIOLATION` because both lane routes' top-level model is `gpt-6.1-sol`. Resolving it is a
   canonical route change, i.e. an owner/WorkOrder act.

## Evidence return

Separate evidence branch `r5r3-closeout-evidence-20261016` (directory
`R5R3_PREVIEW4_CLOSEOUT_20261016/`), carrying the build reproduction receipt, the control-plane probe, the
PLAN-lane decision and its serving evidence, the TT dispositions, the runbook and the owner decision request,
indexed by digest in `PACK_INDEX.json`.

Rollback: a single revert of this PR's merge commit. Nothing immutable is touched.
