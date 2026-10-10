# PIPD-LS-SP — Pre-Implementation / Pre-Dev Lifecycle Skills Plugin

A governed, contract-first toolkit for the **pre-implementation** stage of a project: it turns a
stated intent into a validated chain of machine-readable artefacts — PI → PD →
ConstructionContract → ECP / TQAEP — each bound to one of **19 canonical JSON Schema families**,
and it refuses to hand you something it cannot check. It ships **8 skills** and a **13-command
CLI** (`init` `intake` `profile` `compile-pi` `bind-pd` `compile-ecp` `compile-tqaep` `validate`
`doctor` `project` `export` `diff` `repair`) that produce and verify those artefacts
deterministically.

The work was carried out as a governed implementation round: control plane **HG-KSEOS**, runtime
and orchestration plane **Hermes** under HGK admission, contract surface **Fabric**.

## Start here

| | |
|---|---|
| **Installable preview** | tag **`v0.1.0-preview.1`**, licensed **Apache-2.0** — an owner-authorised open-source **preview / beta** |
| **Release page** | https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1 |
| **This branch (`main`)** | the **R3 snapshot**, kept as history. It is **not** the distribution entry point. |
| **What is not claimed** | see [Claim ceiling](#claim-ceiling) and the release notes for the tag |

Three things about this branch are worth knowing before you read anything else:

- **Installing from `main` is the wrong thing to do.** The wheel under `dist/` here is an old R3
  build (SHA-256 `ba84115d…`), not the published one (SHA-256 `c450dbef…`).
- **The Apache-2.0 grant does not apply to this branch.** On `main`, `LICENSE` is a non-grant
  ("licence position") and `OWNER_LICENSE_DECISION.yaml` still reads `decision: UNSET`. The grant
  is effective at the release commit that carries it — the preview tag, not here.
- **A default clone of this repository gives you the old version.** That is why this page exists.

## Getting the preview

```bash
# 1. Download the wheel and the checksums from the release page above:
#      pipd_ls_sp-0.1.0-py3-none-any.whl
#      SHA256SUMS
# 2. Verify the bytes — this is the only integrity check offered. There is no
#    install-time or startup cryptographic readback, and no release signature.
sha256sum -c SHA256SUMS          # expect: pipd_ls_sp-0.1.0-py3-none-any.whl: OK
# 3. Install
python -m pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl
# 4. Check the install and use it
pipd doctor
pipd --help
```

Requires Python **>= 3.11**. The release page also carries `PREVIEW_NOTES_v0.1.0-preview.1.md`
(what the build is, how to verify it, what it does not claim) and a source archive.

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
| `dist/` | **an R3-era build** — wheel, `.sha256`, `WHEEL_MANIFEST.json` and `web/` packs. Not the published preview. |
| `.hgk/` | the rounds' governance record: admission, kanban, knowledge index, preflight, round receipts and surfaces |
| `pyproject.toml` | packaging metadata (`pipd-ls-sp` 0.1.0, `requires-python >= 3.11`, no `license` field on this branch) |
| `LICENSE`, `OWNER_LICENSE_DECISION.yaml`, `SBOM.cdx.json` | the licence position on **this** branch, the (unset) owner decision slot, and the machine-readable component inventory |
| `PROVENANCE.md` | how the artefacts in this tree were produced |
| `.agents`, `.hermes`, `.gitattributes`, `.gitignore` | agent and repository plumbing |

## Claim ceiling

Status words are kept separate on purpose, and none of them is upgraded by this page.

| claim | state |
|---|---|
| `PROMPT_COMPILE_PASS` | claimed locally, evidence in `.hgk/preflight/` |
| `HGK_ADMITTED` | claimed locally — the HGK lifecycle reached `EXECUTING` |
| `LOCAL_QUALIFIED` | claimed locally (deterministic tests + CLI smoke) |
| `RUNTIME_READY` | **NOT claimed** |
| `INDEPENDENT_PASS` | **NOT claimed as a full pass.** Independent verifiers working only from the published bytes have returned scoped receipts — `9/9` on the published preview, and later `6/6` on a defect repair — but the S0–S4 challenge as a whole is **`PARTIAL_CHALLENGE`**, not a full pass |
| `PUBLICATION_APPROVED` | **GRANTED for the limited preview only** — owner licence decision `Apache-2.0`, effective at the release commit. **`G-RELEASE_FULL_PASS` is NOT granted**: `DEL-018` remains an open release-evidence gap |
| `RELEASED` | limited to `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`, at the preview tag |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

**Stage coverage.** S0 and S1 were reached; the S2–S4 work followed. **S5 (HGK live), S6 (GENIE),
S7 (JIT), S8 (SWOF/SGM), PRE-W3 and the 22 inactive external technologies are deferred.**

## Known limitations of the published preview

Stated here rather than left only on the release page, because they matter when you decide what to
build on this:

1. **`DEL-018 RELEASE_MANIFEST@1` is `FAIL` / `EVIDENCE_GAP`.** On the release branch,
   `tools/build_publication_manifest.py --check --current` exits 1; the uncovered paths are
   `tests/test_git_object_reader.py`, `tests/test_doctor_schema_truth.py` and
   `tests/test_tqaep_design_positive.py` — **none of which are in this tree**, since this branch
   is the R3 snapshot. This is a **release-evidence** gap, not a runtime defect — but it is
   unresolved and must be fixed before any formal release gate.
2. **The SPEC/DEL denominator stays `28 evidenced / 10 active gaps / 19 deferred` of 57 rows.**
   `EVIDENCED ≠ PASS`; not every applicable row has been individually audited.
3. **`v0.1.0-preview.1` carries two known defects**, both reproduced against the published bytes:
   - **`validate` does not resolve the schemas installed inside the wheel the way `doctor` does.**
     Without the global `--root`, it exits 2 with `INPUT_SHAPE_INVALID`, looking for
     `<cwd>/schemas/PI-PKG.schema.json`.
   - **A bundle assembled from the four compilers' unmodified stdout is rejected**, because
     `compile-pi` emits a top-level `_profile_meta` that `PI-PKG` forbids
     (`additionalProperties: false`). Removing only that sidecar makes the same bundle pass
     `checked=4, findings=[]`.
4. **Both defects are fixed on a later branch, and neither fix is published.** The repair was
   verified locally and independently re-verified, but a published tag is never rewritten, so
   **nothing you can download today contains the fix** — it will arrive as a superseding release.
5. **No CVE or supply-chain scan has been performed.** The secret-pattern checks and destination
   canaries that ran are not a vulnerability scan.
6. **No release signature and no build attestation.** Only the published SHA-256, for manual
   download-consistency checking — that is not provenance.
7. **Native Windows symlink / junction / reparse behaviour is not certified** beyond the tested
   scope (`TT-R5P-01`, `TT-R5P-06`).

## Licence

On **this branch** no licence is granted: `LICENSE` is a non-grant text and
`OWNER_LICENSE_DECISION.yaml` reads `decision: UNSET`.

The owner granted **Apache-2.0** for the limited S4 open-source preview in round R5Q
(`FAR-PIPD-R5Q-LICENSE-001`). That grant is effective at the release commit that carries it — the
tag `v0.1.0-preview.1` — and the licence text, the attribution in `NOTICE` and the
machine-readable licence all live **on that release**, not on `main`.

## History and evidence

This page is a rewrite. Until round R6 it was an append-only log — an R3 body, an R4 section, an
R5Q banner, and a dangling `## 8.` fragment — which is why parts of it contradicted each other (a
"review candidate" title above an announcement that a licensed preview exists; a "no licence"
section on a repository that had been granted one).

The section that used to hold the R3 audit-repair snapshot, and the trailing fragment, are
preserved **verbatim** in [`docs/FRONT_PAGE_HISTORY.md`](docs/FRONT_PAGE_HISTORY.md). The
round-by-round record stays in the tree: `docs/ROUND_DISCLOSURE.md`,
`docs/ROUND3_DISCLOSURE.md`, `docs/S0_CONTRACT_SPEC.md`, and the per-round receipts and registers
under `.hgk/`. **Nothing was deleted to make this page read better — the history is moved, not
removed.**
