# PIPD-LS-SP `v0.1.0-preview.1` — S4 Open Source Preview Notes

**Release kind:** GitHub **prerelease** (`prerelease=true`), immutable tag.
**Licence:** `Apache-2.0` (owner grant, round R5Q, 2026-10-10; study FAR-PIPD-R5Q-LICENSE-001).
**What this is:** the PIPD-LS-SP **Pre-Implementation & Pre-Dev Lifecycle Skills Plugin** — a governed
pre-implementation contract compiler (19 machine-contract families, 8 logical Skills, 5 Web pack + 3
Host projection packs, a 13-command CLI, and the PI → PD → ECP/TQAEP design pipeline).

This is a **preview / beta**. It was published so that real users can install it, run it, and report
real problems. It is **not** a production release and **not** a full independent acceptance.

---

## 1. Install and verify

```bash
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl
pip install "jsonschema>=4.0"                    # declared runtime dependency
pipd --help
```

Verify the download before installing:

```bash
sha256sum -c SHA256SUMS          # Windows: certutil -hashfile <file> SHA256
```

The published checksums are the authoritative binding for the assets attached to this tag. The wheel
also carries its own licence text and attribution inside
`pipd_ls_sp-0.1.0.dist-info/licenses/{LICENSE,NOTICE}`, so the granted licence travels with the binary.

**Supported:** Python `>=3.11`, `jsonschema>=4.0`. Python 3.11.17 / jsonschema 4.26.0 is the measured
combination. No other runtime dependency is declared.

## 2. What was verified for this publication

| item | state |
|---|---|
| deterministic test suite on the release tree | `311 tests, OK (skipped=6)` — run in the round, raw log kept in the round evidence |
| clean-venv, no `PYTHONPATH`, outside the repository, against the actual published wheel bytes | covered by the round UAT matrix (see the round evidence directory) |
| `pipd doctor` positive / missing-schema typed negative | covered |
| `intake → compile-pi → bind-pd → compile-ecp → compile-tqaep` design chain, `validate` | covered (design-only: TQAEP output is a **design contract**, not an executed checker) |
| `project --dry-run` zero write / `project --out <scratch>` / `export --out <scratch>` | covered |
| licence consistency across `LICENSE` / `NOTICE` / `OWNER_LICENSE_DECISION.yaml` / `pyproject.toml` / wheel METADATA / `SBOM.cdx.json` | covered |
| published-asset download hash readback | covered by the round readback record |

## 3. Known limitations — read before you rely on anything

1. **`DEL-018 RELEASE_MANIFEST@1` is an open release-evidence gap.** `tools/build_publication_manifest.py
   --check --current` exits **1** and the uncovered paths are
   `tests/test_git_object_reader.py`, `tests/test_doctor_schema_truth.py`,
   `tests/test_tqaep_design_positive.py`. This publication does **not** claim a green release-manifest
   gate. It is a routine packaging fix for a follow-up, not a functional defect.
2. **Not a full independent acceptance.** `S0_S4_FULL_INDEPENDENT_CHALLENGE = PARTIAL_CHALLENGE`; the
   maker did not sign its own final verdict. The SPEC/DEL denominator stays
   `28 S4_ACTIVE_EVIDENCED / 10 S4_ACTIVE_GAP / 19 DEFERRED_BY_INSTRUCTION` and `EVIDENCED ≠ PASS`.
3. **Windows path edges are not certified beyond the tested scope.** Native symlink / junction /
   reparse-point behaviour, and a dirty dangling symlink under the root, are only partially covered
   (`TT-R5P-01`, `TT-R5P-06`). Use a scratch directory and `--dry-run` when pointing the CLI at paths
   you did not create. A reproducible destructive behaviour would be a stop-ship defect — report it.
4. **No install-time cryptographic readback.** There is no automatic signature/checksum verification
   at import or startup; the published SHA-256 is for manual verification (`TT-R5P-02`).
5. **`TQAEP` is a design-time contract.** A compiled TQAEP says what evidence would be required; it
   does **not** mean a checker executed or that anything was independently accepted.
6. **Deferred stages:** S5 (HGK live receiver / SharedSpine), S6 (GENIE adapter / host parity),
   S7 (JIT routing), S8 (release / promotion / HITL), PRE-W3, the 22 inactive external technologies,
   and full host-native certification are **not** implemented or claimed.
7. **`PRODUCTION_VERIFIED` is not claimed**, and `G-RELEASE_FULL_PASS` is not claimed.
8. **`main` is still the historical R3 snapshot.** Do not judge this preview from the default branch;
   this tag is the entry point.

## 4. What changed for this publication (relative to `r5p-post-challenge-repair`)

- owner licence grant `Apache-2.0` landed across every licence surface (E1–E6 of the grant record);
- `NOTICE` created, carrying the material-class split, the donor-plugin non-assertion (no third-party
  source was copied verbatim — see `PROVENANCE.md`), the third-party component list (`jsonschema` = MIT)
  and the exclusion policy;
- `SBOM.cdx.json` corrected: the project licence is `Apache-2.0` and the `jsonschema` component is now
  recorded with its own `MIT` licence instead of the project's placeholder;
- the wheel builder now reads the SPDX identifier from `OWNER_LICENSE_DECISION.yaml`, emits
  `License-Expression` + `License-File`, and packs `LICENSE`/`NOTICE` into the wheel, so the licence is
  verifiable inside the binary;
- the wheel manifest now separates `build_input_commit` from the released commit identity instead of
  reusing an older build identity (CORR-07);
- README / ACCEPTANCE first screens now point at this tag rather than the R3 `main`.

## 5. Reporting problems

Open an issue on `https://github.com/shw097-team/PIPD-LS-SP/issues` with: the exact command, the
`pipd` version, your Python and `jsonschema` versions, the operating system, the observed output
(including the exit code), and — for anything that looks like data loss or secret exposure — mark it
as a **stop-ship** candidate. Only real counterexamples start a targeted repair; the preview does not
exist to chase a fully green test board.

---

**Claim ceiling for this publication:**
`OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`, with
`FULL_S0_S4_INDEPENDENT_PASS = NOT_GRANTED`, `G_RELEASE_FULL_PASS = NOT_GRANTED`,
`DEL_018 = FAIL/EVIDENCE_GAP`, `PRODUCTION_VERIFIED = NOT_CLAIMED`.
