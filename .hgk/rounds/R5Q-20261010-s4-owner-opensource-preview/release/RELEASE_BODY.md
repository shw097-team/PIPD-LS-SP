# PIPD-LS-SP `{{TAG}}` — owner-authorised S4 open-source preview (BETA)

**This is a prerelease, not a production release.** It is the S4 *pre-implementation / pre-dev*
contract compiler, published so that the licence grant, the packaging and the user path can be
checked against real bytes. Read the **Known limitations** below before using it for anything.

| | |
|---|---|
| Licence | **Apache-2.0** — owner grant, round R5Q, 2026-10-10 (`OWNER_LICENSE_DECISION.yaml`) |
| Release commit | `{{RELEASE_COMMIT}}` (tree `{{RELEASE_TREE}}`) |
| Wheel build-input commit | `{{BUILD_INPUT_COMMIT}}` |
| Review baseline (unchanged) | `r5p-post-challenge-repair` @ `{{REVIEW_BASELINE_COMMIT}}` |
| Frozen candidate head | `{{CANDIDATE_HEAD}}` |
| Default branch `main` | R3 content **preserved**, advanced only by a front-page pointer commit (`3aebbbce` → `de3a1d9`) |

The earlier review wheel `{{SUPERSEDED_WHEEL_SHA_PREFIX}}…` is **superseded**. Licence metadata
changed the member composition, so the published wheel is a different artefact; the identity
mapping is `build_input_commit` → `released_commit` → wheel SHA256, never a reused hash.
`candidate_head` is the frozen R5P review candidate and is deliberately **not** the release tip.

## Install

Requires Python >= 3.11. The wheel declares `jsonschema>=4.0`.

```sh
python -m venv venv
venv/bin/python -m pip install {{WHEEL_NAME}}      # Windows: venv\Scripts\python
venv/bin/python -m pipd_ls_sp.cli doctor
```

`doctor` must report the schema source it actually loaded. The 19 JSON Schemas travel inside the
wheel, so an installed `pipd` is self-sufficient — there is no `PYTHONPATH` step.

## Verify the bytes before you trust them

```sh
sha256sum -c {{SHA256SUMS_NAME}}
```

Attached assets:

| Asset | SHA256 |
|---|---|
| `{{WHEEL_NAME}}` | `{{WHEEL_SHA256}}` |
| `{{SOURCE_NAME}}` | `{{SOURCE_SHA256}}` |
| `{{SHA256SUMS_NAME}}` | — |
| `{{PREVIEW_NOTES_NAME}}` | — |

Inside the wheel, `pipd_ls_sp-0.1.0.dist-info/licenses/` carries `LICENSE`, `NOTICE` and
`OWNER_LICENSE_DECISION.yaml` — the licence basis travels with the binary, so the SPDX id in the
metadata can be traced back to the grant that produced it instead of being taken on faith.

## Licence and rights

- **Granted (Apache-2.0):** the agent-authored engineering output — `src/`, `tests/`, `tools/`,
  `schemas/`, `fixtures/`, `skills/`, `docs/`, `dist/` — and the derived expression authored by the
  governed build from the owner's own governing PIPD corpus.
- **Not asserted:** the three donor Skill plugins (`SDLC_PRW_HLPE` R2, `SWOF_ECP` v2.0.1,
  `SWOF_TQAEP` v2.0.1) are inventoried as **SOURCE references only**; no verbatim copy is claimed.
  See `PROVENANCE.md`.
- **Third-party:** dependencies keep their own licences (`jsonschema` = MIT). The SBOM lists the
  declared dependency set; it does **not** compute a transitive closure, and says so in its own
  scope property.
- **Exclusion policy:** any file later shown to carry third-party rights leaves the grant from the
  moment it is re-proven. Published tags are never rewritten — a superseding release is issued.

## Known limitations

Read these as part of the licence grant, not as fine print.

1. **`DEL-018 RELEASE_MANIFEST@1` remains `FAIL / EVIDENCE_GAP`.** The check
   `tools/build_publication_manifest.py --check --current` exits 1 and is **not** closed by this
   release. Three test files are not covered by it: `test_git_object_reader.py`,
   `test_doctor_schema_truth.py`, `test_tqaep_design_positive.py`. It is disclosed here rather than
   silently upgraded to a release-manifest PASS.
2. **`PARTIAL_CHALLENGE` is maintained.** The 57-row base remains
   `28 evidenced / 10 active gaps / 19 deferred`. Only the rows that affect this preview's
   publication and user path were validated.
3. **TQAEP is a design contract only.** This plugin emits pre-implementation contracts. It does not
   execute HGK WorkOrders and does not run a formal checker acceptance on your behalf. Do not read
   the artefacts as evidence that anything was built, deployed or verified downstream.
4. **Windows, host-native and S5–S8 are not certified.** Junction/symlink behaviour, host-native
   projections and live runtime stages were not exercised. Nothing here certifies them.
5. **The scope is construction-time only.** S4 produces contracts for work that has not been done.

## What this release does not claim

`FULL_S0_S4_INDEPENDENT_PASS`, `ALL_57_SPECS_VERIFIED`, `ALL_HOSTS_LIVE_CERTIFIED`,
`S5_RUNTIME_READY`, `G_RELEASE_FULL_PASS` and `PRODUCTION_VERIFIED` are **NOT GRANTED**.

The highest claim this round can reach is `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED` —
a published, licenced, byte-verifiable preview. Independent acceptance by a verifier that is not
the maker is still pending; until that receipt exists, treat every maker-side PASS as unconfirmed.

## Reporting

Open an issue on this repository with the version (`{{TAG}}`), the command, the exit code and the
exact output. Real counter-examples start an affected-only repair round; this preview's scope is
deliberately narrow, so please include the reproduction.
