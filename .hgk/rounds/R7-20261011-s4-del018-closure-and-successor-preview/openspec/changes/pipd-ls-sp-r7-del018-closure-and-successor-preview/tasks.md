# Tasks — pipd-ls-sp-r7-del018-closure-and-successor-preview

## 1. Adjudication

- [x] 1.1 FAR study over the three candidate paths, with the rejected orders stated  
      `far/FAR-PIPD-R7-ADJUDICATION-001.md`
- [x] 1.2 Establish the true DEL-018 verdict, including that it differs by checkout form  
      `execute/del018_check.json`

## 2. Admission and surfaces

- [x] 2.1 Admit the R7 obligations through the typed SharedSpine / ProjectLifecycleController API (no raw SQL)  
      `admission/r7_admission.json` — 6 requirements FROZEN, 0 errors
- [x] 2.2 Kanban board + Swarm graph for the round  
      board `pipd-r7-20261011`, swarm root `t_ae943f32`
- [x] 2.3 GSTACK route read-back, including the routes that were **not** followed  
      `surface/GSTACK_R7_ROUTE_READBACK.json`
- [x] 2.4 OpenSpec change (this file and `proposal.md`)

## 3. Path A — DEL-018

- [x] 3.1 Regenerate the evidence manifest and its seal
- [x] 3.2 Rebuild the publication projection; bind the new candidate commit/tree
- [x] 3.3 `--check --current` exits 0 with every current-tree product path dispositioned (252/252)
- [x] 3.4 Prove the closure is **not** a coverage reduction (4/4 assertions)
      `workorder/r7_del018_proof.py`, `evidence/DEL018_CLOSURE_PROOF.json`
- [x] 3.5 Commit — `64b9955`

## 4. Path C — scan and attestation

- [x] 4.1 History secret / PII scan — 2339 objects, 0 hits, CLEAN/CLEAN
- [x] 4.2 Deny-list scan — PASS, 0 writer usages inside the R4 scope
- [x] 4.3 Dependency vulnerability scan of the resolved release closure — 35 packages, 0 findings
- [x] 4.4 Attestation verification — **FAILED, surfaced as a new finding** (stale default sidecar attests an R3 subject)
- [ ] 4.5 Release signature / external-identity attestation — **deferred, no signing identity on this host**; not substituted with a weaker proxy

## 5. Path B — successor release

- [x] 5.1 Establish that the repaired wheel already exists (sha256 `d6c3e295…`, `build_input_commit 1ab17d1`)
- [x] 5.2 Stage assets and bind the release commit — `release/STAGED.json`
- [x] 5.3 Collision-check the tag name before use (404)
- [x] 5.4 Publish the immutable tag and prerelease under the existing owner grant  
      `release/PUBLISH_RECEIPT.json` — ref 201, release 409307718, 4 assets 201
- [x] 5.5 Anonymous read-back: tag → release commit, all four asset hashes match  
      `release/READBACK.json`
- [x] 5.6 Verify the grant's prohibitions anonymously: `main` untouched, `v0.1.0-preview.1` unmoved

## 6. Independent acceptance

- [x] 6.1 Dispatch a checker in an isolated context against the **published** bytes
- [ ] 6.2 Re-run the same check on the CODEX CLI VERIFY lane (OpenAI OAuth, gpt-6.1-sol medium) — **not done this round**; the substitute is disclosed as weaker, not equivalent

## 7. Reporting

- [x] 7.1 Closure research report stating plainly that not every gap is closed  
      `evidence/R7_CLOSURE_REPORT.md`
- [x] 7.2 Commit the round record

## Open, carried forward

- Stale default publication attestation sidecar (newly surfaced)
- Two undocumented preconditions of the release-evidence toolchain
- DEL-018 is closed on the release line, **not** on `main` (the lines diverged)
- No signature / external attestation; no dependency lockfile; no S5–S8 certification
- `PARTIAL_CHALLENGE` 28/10/19 unchanged; `G_RELEASE_FULL_PASS` / `PRODUCTION_VERIFIED` not granted
