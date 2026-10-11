# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin

A governed, contract-first toolkit for the **pre-implementation** stage of a project: it turns a
stated intent into a validated chain of machine-readable artefacts — PI → PD →
ConstructionContract → ECP / TQAEP — each bound to one of **19 canonical JSON Schema families**,
and it refuses to hand you something it cannot check. It ships **8 skills** and a **13-command
CLI** (`init` `intake` `profile` `compile-pi` `bind-pd` `compile-ecp` `compile-tqaep` `validate`
`doctor` `project` `export` `diff` `repair`) that produce and verify those artefacts
deterministically.

Licensed **Apache-2.0**. This repository is an owner-authorised open-source **preview / beta**, not
a production release — read [Claim ceiling](#claim-ceiling) before building on it.

## Start here

| | |
|---|---|
| **Installable preview** | tag **`v0.1.0-preview.2`** — Apache-2.0 |
| **Release page** | https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.2 |
| **Download the tag, not the branch** | `main` now carries the repaired code, but a branch tip is a moving target. The **immutable** bytes are the tag's. |
| **Superseded** | `v0.1.0-preview.1` — still downloadable, but it ships the two defects described below. Use `.2`. |
| **What is not claimed** | [Claim ceiling](#claim-ceiling) and the release notes |

## Quickstart

Copy-paste, from a shell. Requires **Python >= 3.11** and `curl`.

```bash
# 1. Fetch the published artefact and its checksums, from the immutable tag.
BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
curl -fsSLO "$BASE/pipd_ls_sp-0.1.0-py3-none-any.whl"
curl -fsSLO "$BASE/SHA256SUMS"

# 2. Verify the bytes. This is the ONLY integrity check offered: there is no install-time
#    or startup cryptographic readback, and no release signature.
sha256sum -c SHA256SUMS            # expect: pipd_ls_sp-0.1.0-py3-none-any.whl: OK

# 3. Install into a virtual environment.
python -m venv .venv
. .venv/bin/activate               # Windows: .venv\Scripts\activate
python -m pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl

# 4. Check the install, then use it.
pipd doctor                        # expect: {"verdict": "PASS", ...}
pipd --help                        # 13 commands

# 5. Start a project. Both of these lines were executed against the published wheel.
pipd --root ./myproject init      # -> exit 0; creates docs/ schemas/ src/ tests/ dist/
pipd doctor                       # -> {"verdict": "PASS", ...}, and it names the schema source it resolved
```

Beyond that the pipeline is `intake` -> `compile-pi` -> `bind-pd` -> `compile-ecp` /
`compile-tqaep` -> `validate`, and **the middle steps take real inputs, not free text** — verified
against the CLI rather than assumed:

```bash
pipd --root ./myproject intake --goal "<your goal>" --source <a locator that EXISTS>
pipd --root ./myproject compile-pi --intent <path to an intent card>
pipd validate --bundle <path to the assembled bundle>
# NOTE: --root is a GLOBAL option and must precede the subcommand. There is no --intent on
# `intake` and no --root on `validate`; the CLI is deliberately strict and reports exactly what
# it is missing (USAGE_INVALID / AUTHORITY_UNKNOWN) rather than guessing on your behalf.
```

Run `pipd <command> --help` for each command's real flags. `pipd doctor` is the self-check; it
reports which schema source it resolved and refuses to be silent about it.

## What is in this tree

| path | what it is |
|---|---|
| `schemas/` | the **19 canonical machine-contract families** + `registry.json` (Draft 2020-12, `additionalProperties: false`), written by the Codex bounded writer |
| `src/pipd_ls_sp/` | the plugin runtime (12 modules): intake, profile binding, the PI→PD→ConstructionContract→ECP/TQAEP pipeline, deterministic validators, the 13-command CLI |
| `skills/` | the **8 published skills** — `pipd-route-intake`, `pipd-profile-tailor`, `pipd-pi-compile`, `pipd-pd-bind`, `pipd-execution-contract`, `pipd-assurance-tqaep`, `pipd-authority-source`, `pipd-package-project` — each with `SKILL.md`, `references/`, `schemas/` and `tests/cases.yaml` |
| `tests/` | deterministic tests: the S0 contract set, the LITE vertical slice, negative and adversarial cases, rollback, secret patterns, tooling guards, quarantine disposition (POS/NEG/EDGE), oracle-disagreement, evidence-MD hard-gate refusal |
| `tools/` | governed-round tooling: knowledge probe, HGK admission driver, kanban receipts, CLI smoke, publication manifest and attestation, destructive-destination guards |
| `docs/` | `S0_CONTRACT_SPEC.md` (the frozen spec that drives `schemas/`), the round disclosure records, and [`FRONT_PAGE_HISTORY.md`](docs/FRONT_PAGE_HISTORY.md) |
| `fixtures/` | typed negative and golden fixtures used by the tests |
| `openspec/` | the change proposals these rounds implemented |
| `dist/` | **the published build** — wheel `pipd_ls_sp-0.1.0-py3-none-any.whl` (SHA-256 `d6c3e295…`), its `.sha256`, `WHEEL_MANIFEST.json` and `web/` packs |
| `.hgk/` | the rounds' governance record: admission, kanban, knowledge index, preflight, round receipts and surfaces |
| `pyproject.toml` | packaging metadata (`pipd-ls-sp` 0.1.0, `requires-python >= 3.11`, `license = "Apache-2.0"`) |
| `LICENSE`, `NOTICE`, `OWNER_LICENSE_DECISION.yaml`, `SBOM.cdx.json` | the Apache-2.0 grant, its attribution, the owner's operative decision record (`decision: Apache-2.0`) and the machine-readable component inventory |
| `PROVENANCE.md`, `ACCEPTANCE.md` | how the artefacts were produced, and what was accepted |
| `.agents`, `.hermes`, `.gitattributes`, `.gitignore` | agent and repository plumbing |

## Claim ceiling

Status words are kept separate on purpose, and none of them is upgraded by this page.

| claim | state |
|---|---|
| `PROMPT_COMPILE_PASS` | claimed locally, evidence in `.hgk/preflight/` |
| `HGK_ADMITTED` | claimed locally — the HGK lifecycle reached `EXECUTING` |
| `LOCAL_QUALIFIED` | claimed locally (deterministic tests + CLI smoke) |
| `RUNTIME_READY` | **NOT claimed** |
| `INDEPENDENT_PASS` | **NOT claimed as a full pass.** Verifiers working only from published bytes returned scoped receipts — `9/9` on the preview, `6/6` on a defect repair, and a further `PASS` on `v0.1.0-preview.2` — but the S0–S4 challenge as a whole is **`PARTIAL_CHALLENGE`**, not a full pass |
| `PUBLICATION_APPROVED` | **GRANTED for the limited preview only** — owner licence decision `Apache-2.0`. **`G-RELEASE_FULL_PASS` is NOT granted.** |
| `RELEASED` | limited to `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`, at the preview tags |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

**Stage coverage.** S0 and S1 were reached; the S2–S4 work followed. **S5 (HGK live), S6 (GENIE),
S7 (JIT), S8 (SWOF/SGM), PRE-W3 and the 22 inactive external technologies are deferred.**

## Known limitations

Stated here rather than left only on the release page, because they matter when you decide what to
build on this:

1. **No vulnerability or supply-chain scan of this project's own source.** A dependency audit of the
   declared closure found no known advisories, but `pipd-ls-sp` is not on PyPI and was itself
   **skipped** by that audit — the dependency closure was scanned, the source was not. There is also
   **no lock file**, so the audited set is not necessarily the set you will install.
2. **No release signature and no build attestation.** Only a published SHA-256, for manual
   download-consistency checking. That is not provenance, and it does not bind the artefact to a
   builder identity.
3. **The SPEC/DEL denominator stays `28 evidenced / 10 active gaps / 19 deferred` of 57 rows.**
   `EVIDENCED != PASS`; not every applicable row has been individually audited.
4. **`RELEASE_MANIFEST@1` (`DEL-018`)** — was `FAIL` / `EVIDENCE_GAP` on the release line, and was
   **closed** for the published subject by regenerating the projection (`252/252` product paths
   covered, `0` violations); that closure ships in `v0.1.0-preview.2`.
   **On this branch it is `FAIL` by exactly one path.** After the repaired lineage was merged here,
   the tree has `253` product paths and **`docs/FRONT_PAGE_HISTORY.md` has no disposition** in the
   release-evidence manifest, whose enumerated subject predates that file (it arrived with the R6
   front-page rewrite). `tools/build_publication_manifest.py --check --current` therefore exits `1`
   **on `main`** — a release-evidence divergence, not a runtime defect, and it does not touch the
   tagged bytes, which remain `252/252`. Extending the manifest's subject is a release-evidence
   decision and is deliberately **not** taken here.
5. **Native Windows symlink / junction / reparse behaviour is not certified** beyond the tested
   scope (`TT-R5P-01`, `TT-R5P-06`).
6. **`v0.1.0-preview.1` carries two defects**, both reproduced against its published bytes:
   `validate` did not resolve wheel-installed schemas the way `doctor` does (it exited `2` with
   `INPUT_SHAPE_INVALID`, looking for `<cwd>/schemas/PI-PKG.schema.json`), and a bundle assembled
   from the compilers' unmodified stdout was rejected because `compile-pi` emitted a top-level
   `_profile_meta` that `PI-PKG` forbids. **Both are fixed in `v0.1.0-preview.2`.** A published tag
   is never rewritten, which is why the fix arrived as a successor release rather than an edit.

## Licence

**Apache-2.0** (`LICENSE`, `NOTICE`). The owner granted it in round R5Q
(`FAR-PIPD-R5Q-LICENSE-001`); `OWNER_LICENSE_DECISION.yaml` records `decision: Apache-2.0`. The
grant is effective wherever this tree is checked out, including `main`.

## History and evidence

This page is a rewrite, and it has now been rewritten twice — which is itself recorded rather than
hidden.

- **R6** replaced an append-only log (an R3 body, an R4 section, an R5Q banner, a dangling `## 8.`
  fragment) whose sections contradicted each other. The section that held the R3 audit-repair
  snapshot, and the trailing fragment, are preserved **verbatim** in
  [`docs/FRONT_PAGE_HISTORY.md`](docs/FRONT_PAGE_HISTORY.md).
- **R8** merged the repaired lineage into `main` and **re-derived every claim on this page** against
  the merged tree rather than carrying the previous wording over. The pre-merge text asserted five
  things that the merge made false — that this branch's wheel was an old R3 build, that the
  Apache-2.0 grant did not apply here, that `main` was not the distribution entry point, that
  installing from here was "the wrong thing to do", and that the defects were fixed only off-branch.
  A front page that keeps saying those things after the merge is worse than one that says nothing.

The round-by-round record stays in the tree: `docs/ROUND_DISCLOSURE.md`,
`docs/ROUND3_DISCLOSURE.md`, `docs/S0_CONTRACT_SPEC.md`, and the per-round receipts and registers
under `.hgk/`. **Nothing was deleted to make this page read better — the history is moved, not
removed.**
