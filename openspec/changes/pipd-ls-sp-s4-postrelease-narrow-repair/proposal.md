## Why

Owner engineering decision `S4_MVP_BETA_ACCEPT_WITH_LIMITATIONS` (2026-10-11) keeps
`v0.1.0-preview.2` public and immutable, and routes four narrow repair obligations instead of a
global rewrite. The external challenge named them precisely:

- `POST-F01` — the published `SHA256SUMS` lists **three** assets, but the README quickstart downloads
  one and then runs `sha256sum -c SHA256SUMS`. A verbatim copy-paste therefore exits non-zero with two
  `FAILED open or read` lines. The first thing a new user runs is a failure.
- `POST-F02` — `compute_profile` does not refuse duplicate axes and counts `list(axes)`, while the
  emitted `ProfileBinding` record de-duplicates with `sorted(set(axes))`. The escalation basis and the
  shipped record can therefore describe different axes.
- `POST-F03` — the identity properties `subject_id` / `version` / `content_hash` / `schema_version`
  and the PI `trace` property are declared as empty schemas `{}`, so no JSON type is enforced;
  `validate.semantic_invariants` coerces with `str(...)`, which cannot substitute for a type check.
- `POST-F04` — no risk score or veto evidence reaches `compute_profile`, so LITE cannot imply that a
  per-axis risk assessment ran.
- `POST-F05` — the eight skills exist as repository sources but no separate Web/ChatGPT mount package
  has been published, and a markdown upload is not a native skill installation.
- `POST-F06` — the external canonical standard is the SSOT; the runtime repository owes a pinned
  derived index plus a replayable self-bootstrap, not a competing master copy.

## What Changes

- **The quickstart verifies exactly what it downloaded.** The README SHALL select the wheel line out of
  `SHA256SUMS` before checking it (or download the full listed set), and SHALL ship a copy-paste
  PowerShell branch using `Get-FileHash` against the same published value. A one-line wheel install is
  offered separately and is explicitly labelled as *not* a cryptographic verification.
- **One mount package.** A single versioned ZIP ships a one-page dispatcher `SKILL.md`, five reference
  documents, a starter prompt and `MANIFEST.sha256`, and states the native-upload versus manual-attachment
  paths and their capability limits.
- **Identity fields carry a JSON type.** `subject_id` / `version` / `content_hash` / `schema_version` get
  `type: string` plus the patterns the semantic layer already expects, and `PI-PKG.trace` becomes an
  array of `TraceLink`. The 19-family set, the field set and `additionalProperties: false` are unchanged.
- **The profile path fails closed.** Duplicate, non-string, empty and unknown axes are refused with typed
  errors, `compute_profile` and `pipeline.profile_record` share one normalisation, axis *count* is never
  presented as a risk score, and the record carries `risk_assessment: NOT_ASSESSED` when no risk evidence
  was supplied.
- **Where the normative sources live is stated.** `docs/NORMATIVE_SOURCE_MAP.md` pins the external
  canonical identity/version/hash per source family and maps each to its consumer; `examples/self-bootstrap/`
  replays a minimal PI→PD→ECP/TQAEP design through the shipped CLI plus a source-missing negative.

## Capabilities

### New Capabilities
- `pipd-s4-postrelease-quickstart-truth`: the published onboarding path verifies only artefacts that
  exist on disk, on both bash and PowerShell.
- `pipd-s4-web-mount-pack`: one versioned, self-describing Web/ChatGPT mount package with its own
  manifest hash and a five-case consumer UAT.
- `pipd-s4-contract-type-hardening`: identity/trace JSON types are enforced by the machine contract.
- `pipd-s4-profile-fail-closed`: the profile selector refuses malformed axes and never implies a risk
  score it did not compute.
- `pipd-s4-normative-source-index`: a derived, pinned pointer to the external canonical SSOT plus a
  replayable self-bootstrap.

### Modified Capabilities
- `pipd-ls-sp-s0-s1` (S0 contract set): the field *set* per family is unchanged; only the declared type
  of the identity/trace properties is tightened, so an existing legal record still validates.

## Non-goals

- No rewrite of the 11 PKG or 10 DOC documents; the 16 MB skeleton is not copied into the runtime repo.
- No second authority stack, reducer, plan IR, scheduler, MCP server or resident daemon.
- No 20th schema family, no 9th logical skill, no 14th CLI command.
- No S5 HGK live receiver, S6 GENIE, S7 JIT, S8 SWOF promotion, PRE-W3, or the 22 inactive external
  technologies.
- No tag move, no force-push, no rewrite of published release bytes or historical receipts.
- No maker self-acceptance and no AI prose closing a defect: every claim needs raw evidence bound to
  the frozen candidate.
