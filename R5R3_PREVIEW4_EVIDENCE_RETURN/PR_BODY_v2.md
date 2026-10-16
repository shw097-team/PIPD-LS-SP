# R5R3 — preview.4 install route, release identity, and the round's evidence return

**Claim ceiling: `CANDIDATE_ONLY` / `LOCAL`.** Nothing here is an acceptance, an approval, a new tag or a
release. The subject of this round is the **already-published** `v0.1.1-preview.4` plus the documentation
route that leads a new user to it.

## What was found (on the frozen subject `dba4b19`, delta-only)

The external R5 verdict asked for one bounded patch and one Preview. Following it, this round did **not**
redo `D1` (negation polarity/scope), `D2` (clause boundaries) or the five `ClaimCeiling` shapes: all three
are already merged into `main` and were re-verified rather than re-implemented. What was still wrong was
the **route and the identity record**:

| # | Measured defect | Evidence |
|---|---|---|
| 1 | `docs/install/README.md` tells a reader that the preview.4 identities live in the `v0.1.1-preview.4` entry of `docs/RELEASE_TUPLE.json` — and that entry **did not exist** on `main`. The documented route pointed at nothing. | `grep -c v0.1.1-preview.4 docs/RELEASE_TUPLE.json` → 0 before, 1 after |
| 2 | No record anywhere carried the served asset identities of the release, so nothing in-tree could be checked against `SHA256SUMS`. | 7 served assets, 6 `SHA256SUMS` entries, now all recorded |
| 3 | The front page route to the private plugin ZIP could be read without the digest that the release's own `SHA256SUMS` carries. | README route now names the release asset and its served digest |

A fourth, smaller defect was found **by the repository's own CI** on the first push of this branch and is
the reason the shape of this PR changed — see "CI corrected this PR" below.

## CI corrected this PR (disclosed, not hidden)

The first version of this branch committed the round's evidence tree and an `openspec/` change onto the
product branch. `public-plugin-verify` went **red** on the step *"Prove the upgrade wrote only inside its
allowed set"*: the `stage-c` arm of that gate is a positive allowlist, and neither a round evidence tree
nor `openspec/**` is inside it. That is the gate doing its job, and the repair was not to widen it for
convenience:

- the round's evidence tree and the `openspec` change record **moved off the product branch** (they travel
  on `r5r3-evidence-return-20261016`, the same separate-branch pattern the R5Y evidence return used);
- the identity record was put where the install guide already says it lives: the `v0.1.1-preview.4` entry
  of `docs/RELEASE_TUPLE.json`;
- the served-byte readback landed under `docs/install/` (already inside the arm) as
  `ASSET_READBACK_v0.1.1-preview.4.json`, explicitly marked as a repository-side verification record and
  **not** a release asset;
- **one file** was added to the `stage-c` allowlist (`docs/RELEASE_TUPLE.json`), named as an amendment in
  the workflow comment, mirrored by adding that path to `ALLOWED_PLANTS`, and the arm still refuses
  `skills/` and `packaging/public-plugin/`. The PR filter already listed `docs/RELEASE_TUPLE.json`; the
  allowlist had simply never included the file whose absence broke the documented route.

## Verification (all on the frozen subject, raw output in the evidence return)

- Full suite on this branch: `Ran 624 tests ... OK (skipped=4)`, real exit code `0` — **after** an
  earlier run was red: the first version of the new test file omitted the `src/` bootstrap that
  `tests/test_tooling_executes.py` requires of every test file. Red run and green run are both kept.
- Focused: `tests.test_r5r3_install_route_identity tests.test_s4ext_release_provenance
  tests.test_s4r2m_docs_route tests.test_evidence_md_guards` → `Ran 35 tests ... OK`.
- Tag facts re-derived from git, not typed: tag object `0618d73c725da0d8c3280f99ef369d13741b5197`,
  target `cc6c1930765160697e7e51d6e37735b9220a30db`, tree `7d277a0afaff28b6841836cea3a31ffd0b214d94`.
- Every digest in the new record was recomputed from the bytes GitHub **serves** for the release, then
  compared against the release's own `SHA256SUMS`: 7/7 assets agree; `SHA256SUMS` carries 6 entries and
  the record covers all 6 plus `SHA256SUMS` itself.
- The local `stage-c` gate was simulated before pushing: every changed path is inside the arm,
  `GATE_BAD=0`.
- Mutation control: the guard is not vacuous — moving the served digest inside the download paragraph,
  planting a fake `build_source_commit`, and dropping one `SHA256SUMS`-listed asset from the record each
  turn the focused run red, and the tree is restored afterwards.

## Independent checker

`CODEX CLI`, `openai-codex/gpt-6.1-sol` (the round's declared VERIFY/SECURITY arm; `required_arm ==
served_arm`), read-only. Verdict: **`VERIFIED_WITH_FINDINGS`** — it re-derived the tag and identity facts
independently and then named three real defects in this change set: incomplete digest coverage with an
implied completeness claim, a guard that could pass with a wrong route digest or an invalid build commit,
and a `build_source_commit` field that over-generalised the wheel's provenance to the plugin ZIP. All
three are repaired in this PR; the field now carries `build_source_scope` and the guard binds the digest
to the download paragraph and requires the build commit to exist in git.

## Claim ceiling and what is NOT claimed

- `preview.4` was published **2026-10-14**, before this round; this round creates **no** tag and **no**
  release and does not move any existing one.
- The tag is *correct for the release* and `main` is ahead of it; that gap is disclosed in the record
  rather than reconciled.
- Private ChatGPT host smoke is **not** run here: it needs the account owner's entitlement, so its state
  stays `NOT_SUPPORTED_FOR_ACCOUNT` / `TEMP_CLOSED`. No installation on any account is claimed.
- `PUBLIC_DIRECTORY`, `S4_FULL_PASS`, `PRODUCTION` remain `NOT_GRANTED`.
- Merge is the Owner's decision; this PR is a draft and the branch can be abandoned with no side effect
  on `main`, the tags or the published assets.
