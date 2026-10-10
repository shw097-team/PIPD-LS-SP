# PIPD-LS-SP `v0.1.0-preview.1` — owner-authorised S4 open-source preview (BETA)

**This is a prerelease, not a production release.** It is the S4 *pre-implementation / pre-dev*
contract compiler, published so that the licence grant, the packaging and the user path can be
checked against real bytes. Read the **Known limitations** below before using it for anything.

| | |
|---|---|
| Licence | **Apache-2.0** — owner grant, round R5Q, 2026-10-10 (`OWNER_LICENSE_DECISION.yaml`) |
| Release commit | `74af152b0c2490901bb1d66488371a2283d50bee` (tree `aa4665ff19e27cbf7dbde06a22853f28eed27ee8`) |
| Wheel build-input commit | `c66be0806155eeae3c997a905885ede1e661571f` |
| Review baseline (unchanged) | `r5p-post-challenge-repair` @ `2efc84eac8e1939092c748d5b389b6dd72267aef` |
| Frozen candidate head | `7c5bc585c7d889cd338da853be4efc4b8f07d3b2` |
| Default branch `main` | **not touched** — it still points at the older R3 line |

The review SHA `bb070a6f…` is the *superseded* wheel. The licence metadata changed the member
composition, so the published wheel is a different artefact; the identity mapping is
`build_input_commit` → `released_commit` → wheel SHA256, never a reused hash. The `candidate_head`
above is the frozen R5P review candidate and is deliberately **not** the release tip.

## Install

Requires Python >= 3.11. The wheel declares `jsonschema>=4.0`.

```sh
python -m venv venv
venv/bin/python -m pip install pipd_ls_sp-0.1.0-py3-none-any.whl   # Windows: venv\Scripts\python
venv/bin/python -m pipd_ls_sp.cli doctor
```

`doctor` must report the schema source it actually loaded. The 19 JSON Schemas travel inside the
wheel, so an installed `pipd` is self-sufficient — there is no `PYTHONPATH` step.

## Verify the bytes before you trust them

```sh
sha256sum -c SHA256SUMS
```

Attached assets:

| Asset | SHA256 |
|---|---|
| `pipd_ls_sp-0.1.0-py3-none-any.whl` | `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60` |
| `pipd-ls-sp-v0.1.0-preview.1-source.zip` | `95f00d91a2a9e2b2ea70e2912a0f325de08638c54c2f8d2d763eb3d142689bc2` |
| `SHA256SUMS` | — |
| `PREVIEW_NOTES_v0.1.0-preview.1.md` | — |

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

Open an issue on this repository with the version (`v0.1.0-preview.1`), the command, the exit code
and the exact output. Real counter-examples start an affected-only repair round; this preview's
scope is deliberately narrow, so please include the reproduction.
