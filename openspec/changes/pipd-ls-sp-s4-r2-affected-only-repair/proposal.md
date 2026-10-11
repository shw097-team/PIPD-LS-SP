# pipd-ls-sp-s4-r2-affected-only-repair

## Why

The 2026-10-11 second-round independent reaudit (`PIPD-S4-POSTRELEASE-CHALLENGE-REAUDIT-20261011-R2`,
sha256 `a0cee8741f3d0bd7f5fa84475757e4923fd0dc10ce7167a362a80c048732052c`) raised twelve findings
(`F-S4R2-01..12`) and ten work-item dispositions (`W01..W10`) against the public
`v0.1.0-preview.2` release and rolling `main`. The release stays public and immutable; the report
itself scopes this round to *affected-only maintenance*, not a rebuild.

## What Changes

- Reconciled all twelve findings against the already-frozen candidate lineage instead of opening
  twelve work orders. Nine were already closed by the existing candidate; their closure is asserted
  only on fresh positive **and** negative evidence produced in this round, not on file presence.
- The genuinely open deltas are fixed: the front page no longer shows placeholder commands but points
  at a real, replayable compiler walk-through; the distribution-identity hazard (`.1`/`.2` share the
  `0.1.0` basename while differing in bytes) is stated with PEP 440 guidance; and the residual
  untyped `ProfileBinding` contract fields the duplicate-axes decision rides on are typed.
- One new finding discovered while reconciling (`F-S4R2-NEW-01`) is registered with its counterexample
  and closed under the same write-set, disclosed so nothing is silently widened.
- Nothing is rebuilt, nothing is republished, and no immutable tag or byte is touched.

## Impact

- Affected specs: `pipd-s4-r2-affected-only-repair`
- Affected code: `README.md`, `schemas/ProfileBinding.schema.json`, `tests/`, `examples/first-run/`
- Untouched: the published `v0.1.0-preview.2` tag, commit and wheel, and all prior release assets
