## Context

PIPD-LS-SP is a governed pre-implementation contract compiler. Its S4 stage was already accepted at the
technical level (`GO_WITH_DISCLOSED_LIMITATIONS`). This change is the **publication** step: it converts an
accepted candidate into a legally licensed, bindable, externally verifiable preview distribution without
re-opening any engineering question.

## Goals / Non-Goals

**Goals:** one coherent licence grant across every surface; a binary that carries its own licence; a
build/release identity that cannot be confused; an entry point that cannot resolve to the wrong branch; a
readback that does not trust the publisher's own cache; an honest limitations list.

**Non-Goals:** re-doing product engineering; closing evidence gaps that the owner's risk decision explicitly
accepted as disclosed limitations; promoting any stage.

## Decisions

### D1 — `Apache-2.0`, not `MIT`

Alternatives were scored on: legality of the grant, patent clarity, adoption friction, licence
compatibility (the project consumes an MIT dependency), an attribution mechanism able to carry this
repository's provenance split, trademark protection, and preview simplicity. Apache-2.0 wins on the patent
grant (§3), on the `NOTICE` mechanism (§4(d)) that this repository specifically needs, and on the
trademark non-grant (§6). The accepted cost is the §4(b) modified-file notice obligation, which MIT does
not impose. Full record: `FAR-PIPD-R5Q-LICENSE-001`.

*Rejected:* MIT / BSD-3-Clause (no explicit patent grant); MPL-2.0 (file-level copyleft adds adoption
friction for contract/schema packages meant to be embedded in host runtimes); AGPL-3.0 (directly opposed to
a preview whose purpose is adoption and feedback); dual `Apache-2.0 OR MIT` (pushes the choice downstream
without removing the NOTICE obligation on the Apache branch).

### D2 — the licence lives in one slot and is read by the build

`OWNER_LICENSE_DECISION.yaml` is the single source of truth. `tools/build_dist.py` reads
`decision:` from it rather than hardcoding an identifier, so a future grant change cannot leave the wheel
disagreeing with the tree. The wheel packs `LICENSE` and `NOTICE` into `<dist-info>/licenses/` and emits
`License-Expression` + `License-File`, so the grant is verifiable inside the binary rather than only in the
source tree.

### D3 — build identity and release identity are separated, not aliased

The reviewed candidate (`2efc84e`, wheel `bb070a6f…`) cannot be the release subject, because the licence
change produces new bytes. The wheel manifest therefore records `build_input_commit` (the tree the bytes
were built from), points the released-commit binding at the publication binding instead of pretending the
two are one SHA, and relabels the legacy `candidate_head` as the frozen R5 source identity it actually is.

### D4 — history is preserved, not rewritten

The superseded non-granting owner record, the historical `LicenseRef-PIPD-Proprietary` sentences in README
and ACCEPTANCE, and every earlier round receipt stay byte-identical; the new position is stated as
superseding them, with the effective point named (the release commit).

### D5 — disclosed limitations are the product of the decision, not a failure of it

`DEL-018` remains `FAIL/EVIDENCE_GAP` with its three uncovered test paths named in the public preview
notes. The SPEC/DEL denominator stays `28 / 10 / 19`. The owner's preview decision is a risk-scoped release
decision; it is not a full gate pass, and the published text must not read as one.

## Risks / Trade-offs

| risk | mitigation |
|---|---|
| a claim is read as a full gate pass | every surface states the ceiling; README, ACCEPTANCE, preview notes and the release body all carry the same disclaimer |
| the new wheel hash is mistaken for the old one | `SHA256SUMS` + manifest `build_input_commit` + an explicit "not `bb070a6f`" note in the release body |
| a third party relies on an uncertified platform edge | `TT-R5P-01/06` disclosed with the tested scope and the scratch/dry-run guidance |
| credential exposure during publication | the token is read in process memory only and never written to argv/stdout/logs/evidence/URLs; the whole evidence set is secret-scanned before publication |

## Migration Plan

No migration. Additive publication: a new tag and a new prerelease. Rollback is "do not use the tag"; a
published tag and release are never rewritten destructively — a defect found after publication is fixed in
a superseding release, with the original public version left intact.

## Open Questions

None blocking. Follow-ups (not part of this change): `DEL-018` reseal/rebind, the 10 active evidence gaps,
and the deferred stages.
