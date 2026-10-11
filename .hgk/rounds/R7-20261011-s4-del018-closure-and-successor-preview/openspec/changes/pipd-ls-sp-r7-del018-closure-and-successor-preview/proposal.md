# pipd-ls-sp-r7-del018-closure-and-successor-preview

## Why

`v0.1.0-preview.1` was published carrying two defects (CE-1, CE-2) that make the core chain unusable
from an installed wheel outside the source tree. Those defects were repaired in round R5R on a
worktree branch, but the repair was never delivered: every downloadable artefact still contained the
defects. Separately, `RELEASE_MANIFEST@1` (DEL-018) had failed since the R3 crosswalk — the
publication projection carried no disposition for every current-tree product path.

The owner left the adjudication open: fix DEL-018 first, open a successor release, or scan and attest
first.

## What changes

Evidence surfaces, release scaffolding, and one published artefact. **No runtime, schema, CLI or
packaging byte moves.**

| Change | Nature |
|---|---|
| `.hgk/artifacts/evidence_manifest.json` + `.seal.json` regenerated, projection rebuilt | evidence only |
| `PREVIEW_NOTES_v0.1.0-preview.2.md` added | release documentation |
| Immutable tag `v0.1.0-preview.2` + prerelease with 4 assets | release |
| Round surfaces under `.hgk/rounds/R7-.../` | round record |

## Decision taken

Order **A (DEL-018) → C (scan + attestation) → B (successor release)**, so the published artefact
carries the closure and the scan outcome together. Rationale and the rejected orders are in
`far/FAR-PIPD-R7-ADJUDICATION-001.md`.

## Constraints honoured

- The DEL-018 check is **not** loosened. The evidence is regenerated, and a separate assertion proves
  the regeneration removed only stale paths and no product path — because a manifest that covers less
  would also pass.
- The owner grant is used as written: a **new** immutable tag, an explicit release commit, prerelease
  true; `main` not overwritten, no force-push, no existing tag moved.
- The credential is never written to argv, stdout, logs, the release body, or git config.

## Not in scope

No release signature or external-identity attestation (no signing identity on this host — deferred
with the reason recorded, not substituted). No dependency lockfile. No S5–S8 or host certification.
No grant of `G_RELEASE_FULL_PASS` or `PRODUCTION_VERIFIED`.

## Claim ceiling

`OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`.
