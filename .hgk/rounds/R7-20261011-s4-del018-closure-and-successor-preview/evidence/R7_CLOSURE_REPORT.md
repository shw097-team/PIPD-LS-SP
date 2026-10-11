# FAR-PIPD-R7-CLOSURE-002 — is every known gap / defect / bug repaired and closed?

Round `R7-20261011-s4-del018-closure-and-successor-preview`. Two questions were put: (1) which of the
three candidate paths should be taken, and (2) are all known gaps, defects and bugs now repaired and
closed. This is the answer to (2). It is written to be falsifiable: every closed item carries the
command that re-derives it, and every open item is named rather than absorbed.

## 1. The direct answer

**No.** Not every known gap is closed, and this report does not claim that it is.

What *is* true after this round: **every gap that was closed earlier but undelivered is now delivered
in a published artefact**, and one long-standing evidence failure (DEL-018) is closed. What is *not*
true: the project has no open gaps. Eight items remain open, one of which is newly surfaced **by this
round** and was not on any prior list.

The two are different claims, and conflating them is the error this report exists to avoid:

- ✔ *"The repaired line is now obtainable and its evidence failure is closed."*
- ✘ *"The project has no remaining gaps."*

## 2. Closed in this round

| Item | What was wrong | Closure evidence (re-runnable) |
|---|---|---|
| **DEL-018 RELEASE_MANIFEST@1** | Since the R3 crosswalk the publication projection carried no disposition for every current-tree product path; `--check --current` exited 1. | `build_publication_manifest.py --check --current` → **exit 0, 252/252, 0 violations** (`execute/del018_check.json`); non-lossy proof 4/4 PASS (`evidence/DEL018_CLOSURE_PROOF.json`, `workorder/r7_del018_proof.py`) |
| **CE-1 delivered** | `validate` could not resolve the schemas its own wheel ships, so a clean install failed outside the source tree. Repaired in R5R but **not published**. | Published wheel `d6c3e295…`; `registry.py` resolves `OVERRIDE → INSTALLED → SOURCE`; independent checker re-runs it on the downloaded wheel (`verify-codex/`) |
| **CE-2 delivered** | The compilers' own stdout was not schema-valid (`_profile_meta` emitted into records the schemas reject). Repaired in R5R but **not published**. | Published wheel contains `validate.py` with `NON_RECORD_SIDECARS`; `HASH_EXCLUDED_FIELDS` and `NON_RECORD_SIDECARS` are now separate sets |
| **CE-CODEX-TRACE-WIDENING delivered** | An undeclared `trace` key was accepted on `PD-PKG`/`ECP`/`TQAEP`. | Closed in R5R; carried by the published wheel (`build_input_commit 1ab17d1`) |
| **The repair being unobtainable** | The defects were fixed on a worktree branch and every downloadable artefact still contained them. | `v0.1.0-preview.2` published at `8faa64e`; all four assets re-downloaded anonymously with matching hashes (`release/READBACK.json`) |

The last row is the one that mattered to the owner: the previous state was a **published preview that
was known-bad**, with the fix existing but inaccessible.

## 3. Newly surfaced in this round (was on no prior list)

| Item | Finding | Severity |
|---|---|---|
| **Stale default publication attestation sidecar** | `tools/publication_attestation.py --verify` **FAILS**. The default sidecar `.hgk/ao/pub/PUBLICATION_SUBJECT_ATTESTATION.json` attests commit `3aebbbc`/tree `1a7dc57f` (`generated_at 2026-10-09`, checker `INDEPENDENT_ACCEPTANCE_OFFICER_R3`) while the pinned published subject is `f4f0a02`/`49082394`. | Evidence-surface staleness. Same family as DEL-018. **Open** — deliberately not "fixed" by rewriting a legacy R3 receipt. Evidence: `evidence/scan_attestation_verify.json` |
| **Two undocumented preconditions of the release-evidence toolchain** | `build_publication_manifest.py` cannot run in a linked worktree (`GIT_DIR = ROOT/".git"`, `.git` being a gitfile), and requires the local ref `r5-s4-candidate` to exist. In a worktree it fails with `cannot resolve ref 'r5-s4-candidate'` — a *different* failure from the one on record. | Usability defect, not a release blocker. Worked around by using a primary-form checkout. **Open** (recorded, not patched — patching would move a product byte) |
| **`main` does not carry the release line** | `main` (`26beacb`) and the release line diverged at `3aebbbc`; the publication projection does not exist on `main` at all. DEL-018 is therefore closed **on the release line**, not on `main`. | Scope clarification with an honesty consequence: anyone testing DEL-018 on `main` gets a different picture. **Open by design** |

## 4. Open items carried forward (unchanged by this round)

1. **No release signature or attestation by an external signing identity.** `cosign`/`sigstore` are
   absent and this host holds no signing identity. Producing one would be an agent self-attestation,
   which the governance forbids. Deferred with the reason recorded, not substituted with a weaker
   proxy.
2. **No dependency lockfile, and the project package itself was not audited.** The audit is over a
   resolved environment, not a pinned closure: the declared dependency is `jsonschema>=4.0` (resolved
   to 4.26.0). A `>=` floor means the audited set is not the set a future installer gets. Separately,
   pip-audit **skipped the project's own package** (`Dependency not found on PyPI and could not be
   audited: pipd-ls-sp (0.1.0)`), so "0 findings" covers the dependency closure and **not** a
   source-level audit of `pipd_ls_sp`. See `evidence/scan_dependency_note.md`.
3. **`PARTIAL_CHALLENGE` remains 28 / 10 / 19** (SPEC / DEL denominators). Not moved by R7.
4. **`FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`,
   `S5_RUNTIME_READY`, `ALL_HOSTS_LIVE_CERTIFIED` are still not granted.** DEL-018's closure removes
   one obstacle to a future formal gate; it does not grant the gate.
5. **No S5–S8 / host-native certification.** Still the documented S0–S4 scope.
6. **`PLAIN`/`EXECUTE` `admission_status` remains UNPROVEN.**
7. **`main`'s own `dist/` wheel is still the R3 build**, not the published release — disclosed in the
   main README since R6.
8. **The shipped wheel's licence metadata and the repo licence** were settled in R5Q; unchanged here.

## 5. Method — how "all known" was bounded

"All known" is only meaningful against an enumerated list, so the sources were:

- `evidence/R5Q_NOT_VERIFIED_LEDGER.md` (the authoritative not-verified ledger, 19,311 chars);
- the R5Q contract's own claim list and `stop_ship_conditions`;
- the R4/R5 contract trees and `.hgk/ao/ao_verdict.json`;
- this round's factory scans and the toolchain's own checks.

Limits of that bound, stated plainly: it covers items **already recorded as gaps**. It cannot prove the
absence of an unrecorded defect, and it does not substitute for the S0–S4 independent pass. A defect
nobody wrote down is, by construction, not in this inventory.

## 6. Claim ceiling

`R7_LOCALLY_AND_INDEPENDENTLY_CHECKED_CANDIDATE_PUBLISHED_UNDER_THE_EXISTING_OWNER_GRANT`.

Publishing capability claimed: `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`, inherited from
the R5Q grant. The maker authored this report and cannot accept its own work; the independent verdict
lives in `verify-codex/` and is reported separately, including anything it could not verify.
