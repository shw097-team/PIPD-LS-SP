# Design — S4 post-release narrow repair

## Context

`v0.1.0-preview.2` is public and immutable (commit `8faa64e5`, tree `58301503`, wheel
`d6c3e295…`). `main` is `4445db5a`, i.e. 40 commits ahead, and is the repair base. The challenge
already reproduced the checksum defect against the **published** `SHA256SUMS`; this round re-derived it
from the same raw bytes before touching anything:

```
d6c3e295…  pipd_ls_sp-0.1.0-py3-none-any.whl
804181f6…  pipd-ls-sp-v0.1.0-preview.2-source.zip
31b68010…  PREVIEW_NOTES_v0.1.0-preview.2.md      <- three lines, one downloaded
```

## Decision 1 — the checksum step covers the download, not the manifest

Two honest shapes exist; both are offered rather than one being silently preferred:

```bash
# A: only the wheel was fetched -> select its line, then check it
grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -
# B: fetch everything the manifest lists, then check the manifest
```

A `sha256sum -c SHA256SUMS` that cannot read a listed file is a *failed* check, so the repair removes
the ambiguity instead of tolerating the exit code. The PowerShell branch uses `Get-FileHash -Algorithm
SHA256` against the same literal published digest, so the two shells cannot disagree about what was
verified. The one-line `pip install <release-url>` shortcut is kept, but labelled: a convenience
install is not a provenance check, and the README must not blur the two.

## Decision 2 — tighten the property, not the family

The S0 schema set was generated with empty `{}` property schemas. Adding a full type model to every
field would be over-engineering and would break legal existing records. The repair touches only the
universal identity fields and the PI trace relation, because those are the fields the semantic layer
already reasons about with `str()` coercion:

```
subject_id / version / content_hash / schema_version  ->  {"type": "string", <pattern>}
PI-PKG.trace (PI only)                                ->  {"type": "array", "items": {"$ref": urn:pipd:s0:TraceLink:1}}
```

`additionalProperties: false` and the required-field lists stay exactly as published; the 19-family
registry is untouched. The type check runs in `validate_record` **before** the semantic check, so a
wrongly-typed record fails at the schema layer and an integer id can no longer pass by string
coercion.

## Decision 3 — one normalisation, and an explicit not-assessed marker

`compute_profile` and `pipeline.profile_record` disagreed about the axis set. The repair moves the
validation and normalisation into `compute_profile` and makes the record consume its output, so the
escalation decision and the shipped record are derived from the same list:

```
compute_profile(requested, axes, provider_off_required)
  - requested not in PROFILES           -> ProfileVeto
  - axes non-list / non-string / empty  -> ProfileVeto / UnsupportedSurface (typed)
  - duplicate axes                      -> ProfileVeto
  - unknown axis                        -> UnsupportedSurface
  - used = normalised list              -> len() drives escalation; record carries the same list
proxy: risk_assessment = "NOT_ASSESSED" unless evidence is supplied
```

Axis *count* stays what it is — a complexity proxy — and is never labelled a risk score. `vetoes`
stays `[]` and the record says so, rather than a manufactured `LOW_RISK_VERIFIED`.

## Decision 4 — a mount package is a deliverable, not a new authority

The ZIP is a derived artefact: it neither adds a ninth logical skill (the `SKILL.md` inside is a
dispatcher over the existing eight) nor a second source of truth. Every document in it carries a
source locator, the pack ties to `v0.1.0-preview.2`, and `MANIFEST.sha256` is recomputable from the
extracted tree. Native skill upload and manual attachment are described as *different* capabilities
with different guarantees, and anything the host cannot do is marked `NOT_AVAILABLE` rather than
implied.

## Decision 5 — pin the pointer, never copy the corpus

`PIPD-LIFECYCLE-SPEC@1.1.0` is the external canonical SSOT. `docs/NORMATIVE_SOURCE_MAP.md` records
owner / version / hash-or-`NOT_PUBLIC` / consumer per source family and states in its own header that
it is a derived view. `examples/self-bootstrap/` proves the *toolchain* is replayable on a minimal
source-constrained input; it does not claim that the unpublished corpus can be reconstructed.

## Residue

- The 16 MB skeleton and the full PKG/DOC bodies stay outside this repository (owner decision).
- No release signature and no build attestation exist; the round does not add one.
- `LITE` still does not execute a per-axis risk assessment; it now says so instead of implying one.
- The native ChatGPT skill upload path depends on account capability and is recorded as observed, not
  guaranteed.
