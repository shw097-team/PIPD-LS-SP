# Tasks

> Status legend: `[x]` = executed **and re-run by the orchestrator against the frozen candidate**, not
> merely claimed by a writer lane. `[~]` = executed as far as this host allows, with the residue named.
> `[ ]` = not executed.
>
> Owner gates that this change deliberately does NOT clear for the owner: the plugin SemVer, the real
> publisher identity, the eight frontmatter derivation approvals, the icon brand approval, and the
> Portal draft/scan/review/publish acts.

## Stage B - UPG-P01: deterministic public Skills-only projection

- [x] 1.1 `tools/freeze_public_plugin_source.py` emits a frozen ledger (repo, 40-hex commit and tree,
      the exact eight skill names, a `path -> sha256` for every file under them) and refuses a dirty
      worktree, a wrong skill set, a symlink, a dot-file and any non-regular member.
- [x] 1.2 `tools/build_public_plugin.py` assembles the plugin ZIP with fixed metadata and a member
      read-back before promotion, so two builds from identical inputs are byte-identical.
- [x] 1.3 The package root manifest is the official Agent Plugins 1.0 manifest, validated against a
      byte-locked copy of the vendor schema; PIPD's own release bookkeeping lives in the vendor-blessed
      `extensions` namespace.
- [x] 1.4 Every owner-gated input refuses the build with a typed, non-zero reason: missing per-skill
      derivation record, unpinned vendor-schema digest, unpinned publisher identity, unpinned or invalid
      icon, a ninth skill, a source member absent from the ledger, an output root overlapping the repo.
- [x] 1.5 `SOURCE_TO_PLUGIN_MAPPING.json` records, per source file, the source digest, the destination
      digest and whether the projection was `EXACT` or `DERIVED_WITH_OWNER_APPROVAL`; the receipt pins
      `claim_ceiling: LOCAL_PACKAGER_PASS_ONLY` and `official_portal_verification: NOT_EXECUTED`.
- [~] 1.6 A real build from the frozen candidate: attempted and REFUSED at the owner gates, with the
      raw refusal recorded. The complete-pipeline path is proven by the synthetic fixture suite.
- [ ] 1.7 Owner decisions outstanding: plugin SemVer, real publisher identity, eight derivation
      approvals, icon brand assets, and the vendor's own validator / Portal scan.

## Stage B - UPG-P02: two-route install surface

- [x] 2.1 `docs/install/README.md` is the single install SSOT with exactly two main routes (Web,
      Agent), the state table that keeps build/portal/published/host/S4 apart, and recovery below.
- [x] 2.2 `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` is one copy-paste prompt that makes the host
      detect itself, show paths/diffs, obtain consent, verify real discovery and report `NOT_VERIFIED`
      when only files were copied.
- [x] 2.3 `tools/build_web_fallback.py` produces ONE bounded, byte-complete markdown document that
      refuses a stale release stamp, a digest mismatch, an unexpected member, a non-text member, a
      symlinked or existing destination, and any output above the cap - never truncated.
- [x] 2.4 `README.md` carries only the two install entry points plus a pointer to `docs/install/`.

## Stage B - UPG-P03: verification surface

- [x] 3.1 `tests/test_public_plugin_packaging.py` exercises the packaging gates, including the five
      historical red cases (fake PNG, unknown manifest key, invalid skill frontmatter, null/mismatched
      source commit, symlinked output) plus determinism, owner-gate refusal and derivation approval.
- [x] 3.2 `tests/test_web_fallback.py` exercises the fallback gates, including no-truncation, an
      existing destination, a symlinked destination with an untouched sentinel, and a non-text member.
- [x] 3.3 `.github/workflows/public-plugin-verify.yml` is read-only, SHA-pinned, secret-free, carries a
      write-set guard, and ends with a fail-closed negative step that requires an actual failure whose
      motive is the identity/byte binding.
- [ ] 3.4 Real Portal scan/review and the vendor's own validator remain NOT_EXECUTED.

## Round-level obligations

- [x] R.1 HGK/Kanban: the round is on the board `s4post-20261012` with the SWARM root, worker cards,
      a verifier card and a synthesizer card, plus per-ID receipts on disk.
- [x] R.2 GSTACK: the named-method route resolution ran for the round's flows and every activation
      invariant is zero.
- [~] R.3 OPENSPEC: this change is the round's spec ledger, validated by the native CLI.
- [~] R.4 Host UAT: Hermes Agent executed; Codex CLI executed in Stage A; Web and Codex Desktop report
      NOT_RUN / NOT_VERIFIED rather than a fabricated pass.

## R3 remedy round - FAR low-resistance plan (owner order 2026-10-13)

> Appended by the R3 round. Same legend. These entries add to - and do not restate or overwrite - any
> status above. The round's FAR study audited this change against the blueprint, the command PROMPT and
> the external recheck verdict, and recorded six deviations with locators
> (`verify/far/FAR_S4POST_DEVIATION_AND_REMEDIES_20261013.md`).

- [x] R3.R1/R8 Harness freeze + external-round cap declared in `HARNESS_FREEZE_AND_AO_LOOP_CAP.md`:
      no new verification axis, no further acceptance round for this change, residual findings become CR/TT.
- [~] R3.R2 Changeset split: the verification harness is carried by its own branch and the product
      changeset branch keeps the product surface plus the round's result documents. Branch names and the
      exact file counts are recorded in `R3_PUBLICATION.md`; the owner still decides which branch is the
      change under acceptance.
- [x] R3.R3 Evidence Return Pack completed with the three missing PB-090 fields: `commands` (focused
      108/OK, full 572/OK, both raw logs in `verify/r3/raw/` with sha256), `release_assets` (all five
      published `v0.1.1-preview.3` assets re-downloaded anonymously and hashed: 5/5 equal to the
      API-reported digest) and `manifest_sha256`. Integrity vs API metadata only; tag -> source -> asset
      reproducibility stays OPEN.
- [x] R3.R4 `OWNER_ACTION_REQUEST.md`: the four owner supplies, the four owner-only acts, the 12 external
      evidence items and the three design decisions the round declines to answer.
- [~] R3.R5 Minimal read-only CI: the workflow is unchanged; the Draft PR that would give it its first
      real run is attempted and its raw outcome recorded in `R3_PUBLICATION.md`.
- [x] R3.R6 Evidence rerunnability is now an assertion, not a promise:
      `verify/tools/check_evidence_locators.py` run as a positive control (PASS) and against the AO12
      bundle (FAIL: 5 external-only locators including the lane's unreadable temp root and the canonical
      challenge-review contract, which lives outside the tree).
- [x] R3.R7 SoD recorded at identity level: producer `user` (S-1-5-21-...-1000), checker
      `CodexSandboxOffline` (S-1-5-21-...-1004) - different local accounts, so the separation is process +
      identity, not model.
- [x] R3.surfaces: KANBAN board `s4post-r3-remedies` with a SWARM graph (root `t_fc25bc79`, six workers,
      verifier `t_e392ea37`, synthesizer `t_33a81182`) recorded in `kanban/R3_BOARD_EVIDENCE.json`; GSTACK
      route readback executed (`surface/GSTACK_R3_ROUTE_READBACK.json`, all 14 activation invariants 0);
      OpenSpec validated by the native CLI (`surface/OPENSPEC_R3_EVIDENCE.json`).
- [ ] R3.owner The four supplies, the four owner-only acts and the single integrated candidate signature
      remain the owner's; nothing here clears them.

- [x] R3.corrections — two maker claims were found wrong by an independent audit and are corrected here
      rather than rewritten: (1) `R.1` claims the round sits on board `s4post-20261012` "plus per-ID receipts
      on disk"; the only in-tree receipt is `kanban/R3_BOARD_EVIDENCE.json` for board `s4post-r3-remedies`,
      and no per-ID receipt files exist - the SWARM root/worker/verifier/synthesizer ids are real but live
      only inside that JSON. (2) `R3.R5` pointed the reader at a `R3_PR_ATTEMPT.md` that was never written;
      the raw PR/CI outcome now lives in `R3_CI_FIRST_RUN.md` and section 5 of `R3_PUBLICATION.md`.
- [x] R3.surface-audit — the blueprint section 3.3 allowlist was audited by a parallel subagent and every
      HIGH item was re-measured by the maker before being accepted; 7 entries, 3 HIGH, recorded in
      `verify/far/FAR_S3_3_SURFACE_AUDIT_20261013.md` and summarised in `R3_PUBLICATION.md` section 10.
