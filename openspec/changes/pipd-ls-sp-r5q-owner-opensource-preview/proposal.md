## Why

The technical review for PIPD-LS-SP's S4 stage returned `S4_OPEN_SOURCE_PREVIEW_TECHNICAL_GO = YES` with
`GO_WITH_DISCLOSED_LIMITATIONS` (`NO_BROAD_REPAIR`), and the corrected owner-facing report withdrew the
earlier mis-attribution that a missing licence was an engineering defect. The owner has now granted an
open-source licence and authorised a limited S4 preview/beta publication. What remained was a bounded
release task, not another repair wave: land one coherent grant across every licence surface, freeze a new
immutable release candidate, rebuild the distribution so the binary carries the granted licence, verify the
actual published bytes from a clean environment, publish a tag + prerelease tied to the explicit commit,
read it back independently, and return one evidence pack that keeps `DEL-018` and the deferred stages
honestly open.

## What Changes

- **One licence, five surfaces.** `LICENSE` becomes the verbatim Apache License 2.0; `NOTICE` is created
  and carries the material-class split, the donor-plugin non-assertion, the third-party component list and
  the exclusion policy; `OWNER_LICENSE_DECISION.yaml` records `decision: Apache-2.0` while preserving the
  superseded non-granting record verbatim; `pyproject.toml` and `SBOM.cdx.json` agree; `PROVENANCE.md`
  gains the licence layer. The `jsonschema` component's licence is corrected from the project's own
  placeholder to its real `MIT`.
- **The licence travels with the binary.** `tools/build_dist.py` reads the SPDX identifier from
  `OWNER_LICENSE_DECISION.yaml`, emits `License-Expression` + `License-File` in the wheel METADATA and
  packs `LICENSE` + `NOTICE` into `<dist-info>/licenses/` (PEP 639).
- **Build identity is no longer disguised as release identity.** The wheel manifest records
  `build_input_commit` separately from the released commit and labels the legacy `candidate_head` as what
  it is (the frozen R5 source identity), instead of letting an older build identity stand in for the
  release tip.
- **The preview has one entry point.** README and ACCEPTANCE first screens point at the preview tag, not
  the historical R3 `main`; `PREVIEW_NOTES_v0.1.0-preview.1.md` carries the install/verify instructions and
  the full known-limitations list.
- **The release is bound, published and read back.** A new immutable tag and a GitHub prerelease bind the
  exact release commit; the published assets are re-read and their hashes recomputed from a source that
  never used the local release cache; an independent non-Maker checker re-derives the decisive claims from
  the published bytes.
- **Nothing is rounded up.** `DEL-018 RELEASE_MANIFEST@1` stays `FAIL/EVIDENCE_GAP` with its three
  uncovered test paths named; the SPEC/DEL denominator stays `28 / 10 / 19`; `G-RELEASE_FULL_PASS`,
  `FULL_S0_S4_INDEPENDENT_PASS` and `PRODUCTION_VERIFIED` remain unclaimed; the 12 TT rows keep their
  owner and trigger.

## Non-goals

- No R6: no re-doing of the 19 schemas, 8 skills, 13 CLI commands, 5 Web / 3 Host packs or the 3 golden
  pilots; no refresh of all 57 SPEC/DEL rows to PASS; no activation of the 22 inactive external
  technologies.
- No S5–S8 or PRE-W3: HGK live receiver, GENIE adapter, JIT routing, SWOF/SGM promotion and the
  cross-project checkpoint stay deferred with their typed design seams.
- No second repository, no `main` overwrite, no force-push, no moving or deleting an existing tag.
- No claim upgrade: this change does not produce, and must not be quoted as, a full independent pass or a
  production verification.
