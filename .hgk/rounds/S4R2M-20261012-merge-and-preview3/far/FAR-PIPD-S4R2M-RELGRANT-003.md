# FAR-PIPD-S4R2M-RELGRANT-003 — which of M3/M4 is already granted, and which needs a new owner act

- **Round:** `S4R2M-20261012-merge-and-preview3`
- **Question type:** grant-scope reading before declaring an owner act required
- **Autonomy:** in-round FAR study, executed directly; the reading is reported to the owner as a
  decision they own
- **Claim ceiling:** `LOCAL`

## The question

Two candidate end states need remote writes: (M3) advance `main` to the approved candidate by
fast-forward; (M4) create a new immutable `v0.1.1-preview.3` tag and prerelease. An earlier round
obtained a standing owner grant. Is either act already inside it?

## The standing grant on record

`R5Q-20261010-s4-owner-opensource-preview/owner/OWNER_LICENSE_GRANT_R5Q.json` →
`publication_authorization`:

- `action: create_new_immutable_tag_and_prerelease`
- `target: explicit release commit (never the default branch)`
- `prerelease: true`, `tag_must_be_collision_checked_before_use: true`
- `forbidden: [overwrite main, force-push, move or delete an existing tag, create a second repository]`
- `claim_ceiling_if_published: OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`

Its `exclusions` also say already published tags are not rewritten — a **superseding** release is
issued instead. That is a direct statement about successors, not only about the first release.

## Reading

**M4 (new tag + prerelease) is inside the existing grant.** The action is named literally; the target
is an explicit release commit, not the default branch; the tag is new, collision-checked, immutable;
nothing forbidden is touched. Executing it under that grant is execution, not self-promotion.
Consequence: it still requires a real release commit, a version strictly greater than `0.1.0`, a
deterministic wheel plus a separately downloadable mount pack, checksums, an isolated install and an
anonymous re-download readback.

**M3 (advancing `main`) is NOT inside that grant.** Its `action` names a tag and a prerelease only, and
its `forbidden` list treats `main` as a separate object that must not be overwritten. Advancing `main`
is neither named nor implied. The governing prompt for this round is also explicit on this point
(`human_gate: REQUIRED_FOR_MAIN_INTEGRATION_AND_PUBLIC_RELEASE`; §7: a general "decide and execute"
instruction does not clear an owner-only gate). **M3 therefore needs a new, explicit owner act.**

This is a reading, not a certainty: "one release grant per tag" is a defensible alternative to "a
standing grant for successor release artefacts". The grant's own `exclusions` wording — *a superseding
release is issued instead* — is what makes the standing reading the more natural one, but the owner
settles which of the two readings governs.

## Consequence for this round

- The round prepares M3 to the point of one owner action (`MERGE_READY_HITL_PENDING`): frozen candidate,
  merge decision record, credential scope proof, a rehearsal that the fast-forward is structurally
  possible, and the exact command that would be run under the broker.
- The round does **not** advance `main` on its own authority.
- The round may execute M4 only after the owner selects the release gate, and only with the version,
  packaging and readback evidence listed above.

## What this reading does not confer

- It does not authorise force-push, history rewrite, tag movement, asset replacement or a second repo.
- It does not authorise publication of anything the licence grant excludes.
- It does not lift any claim ceiling above `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`.
