# s4post-triple-upgrade

## Why

The 2026-10-12 external post-repair recheck (`PIPD-S4-EXTERNAL-POSTREPAIR-RECHECK-20261012-R1`) found
that the public `v0.1.1-preview.3` wheel still ships the false-PASS Trace validator, that `main`'s Web
Mount asset was replaced in place, and that **no repository under either branch has a pipeline**: the
GitHub refs carry zero `.github/` trees and zero Actions runs, while the only cross-host evidence is a
partially-run Codex CLI lane. The triple-upgrade blueprint (R2) turns those findings into one small
change set: a deterministic public Skills-only plugin projection, one Web route plus one Agent route,
and a fail-closed verification surface - without a new stage, a ninth skill, a second trace engine, a
new schema family, MCP, Apps, Actions or Hooks.

## What Changes

- **Stage A (narrow repair)** - `S4POST-INTEGRATION-REPAIR`: port (by path, never by merge) the repair
  branch's strict `TraceLink` fields, endpoint-family match and `validate_bundle` graph closure onto
  `main`; reconcile the release tuple with `main`'s in-place Web Mount correction while preserving the
  first-shipped digest as a historical field; add one minimal read-only CI workflow; and make first-run
  self-locating with typed preconditions. `skills/**` and `src/**` outside the affected compiler paths
  stay untouched.
- **Stage B (upgrade)** - `S4-UX-DISTRIBUTION-UPGRADE-R1`: project the eight existing skills into ONE
  portable, deterministic, fail-closed plugin candidate whose package root manifest is the official
  Agent Plugins 1.0 manifest validated against a byte-locked copy of the vendor schema; generate ONE
  bounded single-document Web fallback with a documented `DOC_MOUNT_ONLY` ceiling; reduce the public
  install surface to exactly two routes (Web, Agent); and add a read-only verification workflow with a
  fail-closed negative step. Every owner-gated input (per-skill frontmatter derivation, publisher
  identity, icon digests, the pinned vendor-schema digest) makes the build REFUSE with a typed reason.
- **No new stage, no ninth skill, no second trace engine, no 20th schema family.** `MCP = OFF`.

## Impact

- Affected specs: `pipd-public-plugin-distribution` (added), `pipd-trace-closure` (modified by Stage A).
- Affected code: `packaging/public-plugin/**`, `tools/{freeze_public_plugin_source,build_public_plugin,build_web_fallback}.py`,
  `tests/test_public_plugin_packaging.py`, `tests/test_web_fallback.py`, `docs/install/**`, `README.md`,
  `.github/workflows/{ci,public-plugin-verify}.yml`; and for Stage A only `src/pipd_ls_sp/{validate,profiles}.py`,
  `schemas/{TraceLink,PI-PKG}.schema.json`, `docs/RELEASE_TUPLE.json`, `examples/first-run/**`.
- Not affected: the canonical lifecycle standard, the DOC/PKG body set, the ECP/TQAEP oracles, the
  published release assets and tags, `dist/**`.
