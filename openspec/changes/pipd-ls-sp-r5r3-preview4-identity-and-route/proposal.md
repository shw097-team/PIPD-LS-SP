# pipd-ls-sp-r5r3-preview4-identity-and-route

## Why

The `v0.1.1-preview.4` release is published (2026-10-14) and the S4-R5 focused repair (D1 negation
polarity/scope, D2 clause boundary, ClaimCeiling claim shape) is on `main`. A delta-only re-verification
of the LIVE subject on 2026-10-16 re-derived every data point with real commands and found that the
**code** edges hold but the **distribution identity and its navigation** do not:

- `README.md`'s private-plugin route told a reader to install the in-repo, superseded R5Y evidence-branch
  ZIP — 68,355 bytes / `2f9ae0…` — while the release serves a different byte string, 68,357 bytes /
  `545e359a…`. A reader following the front page downloads, and if they check anything, checks a digest
  no `SHA256SUMS` carries.
- `docs/install/README.md` sent the reader to a `RELEASE_TUPLE_v0.1.1-preview.4.json` **release asset
  that the release does not ship**.
- `docs/RELEASE_TUPLE.json` — whose own purpose statement is "frozen, independently resolvable release
  identities for the distribution surface" — carried **no** entry for the newest release, so nothing in
  the published tree recorded the served digests at all; the only producer record was the release's own
  `SHA256SUMS` asset.

## What Changes

- `README.md`: the private-plugin route names the **release asset** and its served digest; the R5Y build
  is kept and explicitly labelled as superseded history ("do not install it"); the R5Y-time gate row that
  still said "no tag and no release was created" is replaced by the published preview's identity.
- `docs/install/README.md`: the version-pin bullet states the real tag object / target commit / tree and
  points at `docs/RELEASE_TUPLE.json` plus the release's `SHA256SUMS`, with the exact commands that
  re-derive both, instead of naming a non-existent asset.
- `docs/RELEASE_TUPLE.json`: one `v0.1.1-preview.4` entry — tag object, target commit, tree, build source
  commit, the served asset digests for all six assets, and the statement that the release ships no mount
  pack (so `pack_dir`/`zip` are `null` on purpose rather than absent by accident).
- `tests/test_r5r3_install_route_identity.py`: a derived, not hand-written, guard. It re-derives the tag
  facts from git, asserts the served digest is the one the route names, asserts the superseded digest only
  ever appears on a line that says it is superseded, and asserts the install page names no asset the
  release does not carry.

## What does NOT change

No product code (`src/**`, `schemas/**`), no packaging tool, no skill body, no ninth skill, no new
schema family, no CI gate relaxation. `main`'s semantic behaviour is untouched: this change set is
documentation and release identity only.

## Not claimed by this change

`PUBLICATION_APPROVED`, `RELEASED` for any new tag, `S4_FULL_PASS`, `PRODUCTION_VERIFIED`. The
release/main drift recorded in the round report (the served wheel predates the R5R2 clause-boundary
refinement on `main`) is an **owner release decision**, not something this change set resolves.
