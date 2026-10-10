# Tasks — R5R CE-1/CE-2 repair + CODEX-CLI verification

## 1. Admission and research

- [x] 1.1 HGK admission of the six R5R obligations through the typed SharedSpine lifecycle API.
      `admission/` — 6/6 FROZEN, 0 error, checkpoint `CK-20261008-3927763C`.
- [x] 1.2 FAR quick study root-causing CE-1 and CE-2 from the source, with candidates and a decision.
      `far/R5R_FAR_CE_REPAIR_QUICKSTUDY.md` (`FAR-PIPD-R5R-CE-REPAIR-001`) — accepts A1 + B1.
- [x] 1.3 Record the decision of record in the round evidence pack.
      The FAR names the accepted option and each rejected alternative with the reason it was rejected.

## 2. Repair (EXECUTE lane, via the CODEX CLI)

- [x] 2.1 CE-1: `validate` resolves schemas through the registry resolver, `root/schemas` only when it
      carries `registry.json`, and reports the source it used.
      `registry.resolve_for_validate(root)`; `validate` now returns `schema_source` and fails closed
      with a typed `SCHEMA_RESOLUTION` finding when nothing resolves.
- [x] 2.2 CE-2: the non-record sidecar set is defined once and consumed by `_body_hash`, the
      schema-checking path and `pipeline`; schema validation runs on the stripped copy.
- [x] 2.3 Red state captured before the repair, green state after.
      `execute/red_state.txt` carries the exact CE-1 and CE-2 signatures; `execute/green_state.txt` is
      the same tests green.
- [x] 2.4 Found and repaired by the maker's own end-to-end probe: a **second CE-1-class site** —
      `init_workspace` read the registry out of the `<root>/schemas` directory it had just created
      empty, so `pipd init` failed on any fresh or installed root. Repaired through the same resolver,
      reporting `schema_source` and failing closed with a typed `ValidationFail`.
      `projection.py`'s `root/schemas/registry.json` read is deliberately unchanged and documented as
      out of scope: that function loads the canonical objects from one specified tree.
- [x] 2.5 Closed the independent checker's counterexample `CE-CODEX-TRACE-WIDENING`: split the single
      conflated constant into `HASH_EXCLUDED_FIELDS` (identity + derived `trace` + sidecar, used for
      hashing) and `NON_RECORD_SIDECARS` (`_profile_meta` only, the only set the schema check strips).
      `trace` is schema-enforced again on every contract that does not declare it.

## 3. Regression

- [x] 3.1 A test that fails before the repair on the CE-1 path and passes after.
- [x] 3.2 A test that fails before the repair on the CE-2 path and passes after.
- [x] 3.3 A test asserting the sidecar list has exactly one definition.
- [x] 3.4 The full deterministic suite stays green. 321 tests, `OK (skipped=3)`.
- [x] 3.5 End-to-end: installed wheel, run outside the repository, unmodified compiler output,
      `validate` reaches PASS. `maker-e2e/maker_e2e_transcript.txt` — whole chain exit 0,
      `verdict=PASS checked=4 findings=[]` with PI-PKG still carrying `_profile_meta`.
- [x] 3.6 A test pinning the `init` site: a fresh root with no `schemas/` must succeed and report the
      resolved source.
- [x] 3.7 The `tracked_files` guard repaired rather than the evidence dropped.
      `tests/test_tooling_executes.py` asserted `tracked_files < 1000`; this round's own evidence
      commits took the count from 996 (`9bd33a1`) to 1015, so the absolute cap was replaced by a direct
      assertion that no tracked path is version-control machinery, plus a generous 25,000 sanity bound
      and a test proving the guard fires on a poisoned path list. The bounded writer had first called
      that failure "pre-existing and unrelated"; that verdict was measured to be wrong and is
      corrected in the record.
- [x] 3.8 A test pinning the checker's exact counterexample: an undeclared `trace` on `PD-PKG`, `ECP`
      or `TQAEP` must be rejected.

## 4. Independent verification (VERIFY lane, CODEX CLI)

- [x] 4.1 Executed through the CODEX CLI on GPT 6.1 SOL-MEDIUM (OpenAI OAuth), reasoning effort
      medium, in a dedicated `CODEX_HOME` that is not the EXECUTE lane's.
- [x] 4.2 The checker really installs PIPD-LS-SP and really runs it, with the raw transcript recorded.
      Clean `venv`, install from the wheel, `doctor` exit 0, the whole design chain on independently
      authored inputs, its own scratch git repo for `bind-pd`.
- [x] 4.3 The checker's verdict is its own; the maker does not sign it. First pass: **FAIL**,
      counterexample `CE-CODEX-TRACE-WIDENING`, recorded as-is in `verify-codex/verdict.json` and
      answered by repair 2.5 — never argued away.
- [x] 4.4 The first pass independently confirmed claims 1–7 and 9: clean install, full chain, CE-1,
      CE-2, fail-closed behaviour on three tamper classes, the published tag untouched, and that the
      new `.git`-internals guard is stronger than the size cap it replaced.
- [x] 4.5 Re-verification after the repair: **PASS**, 6/6 claims, zero counterexamples
      (`verify-codex-2/verdict.json`). The checker reused its own byte-exact prior fixtures, tested 15
      further `trace` value variants — all rejected — and confirmed the published wheel rejects the
      same records. It also disclosed that the `_profile_meta` tolerance is not a PI-PKG special case,
      and that PI-PKG's object-permissive `trace` schema is pre-existing behaviour this round did not
      change.

## 5. Disclosure and surfaces

- [x] 5.1 Public disclosure advanced to the repaired state, saying what is fixed and what still applies
      to the already-published preview. The repaired wheel is a local candidate: it is NOT published,
      and `v0.1.0-preview.1` was not rewritten. The already-published preview keeps the CE-1/CE-2
      defects it shipped with; delivering the repair needs a successor release.
- [x] 5.2 KANBAN, SWARM, GSTACK and OPENSPEC receipts recorded in the round.
      KANBAN board `pipd-r5r-20261010` plus swarm root `t_c9975958`; OPENSPEC change
      `pipd-ls-sp-r5r-ce-repair-and-codex-verify` (validated); GSTACK route readback at
      `surface/GSTACK_R5R_ROUTE_READBACK.json`, including the two declared lane-route deviations and
      the four `hard_deny` attestations.
- [x] 5.3 Feasibility finding recorded from the checker's own experience: the wheel ships no README or
      quickstart, and several CLI usages are non-obvious (`--source` takes an existing file locator;
      the compilers print to stdout and must be wrapped by contract family; `bind-pd` needs a
      committed git repo; `compile-tqaep` needs a distinct maker/checker plus a non-empty receipt).
      Recorded, not fixed in this round.

## 6. Not in this round

- [x] 6.1 Cutting a superseding release — the owner's publication decision, not the maker's.
      Confirmed out of scope; this round produced a candidate only. No tag was created, moved or
      deleted and no release or prerelease was created, edited or published.
- [ ] 6.2 `DEL-018 RELEASE_MANIFEST@1` closure.
- [ ] 6.3 S5–S8 live execution and host-native certification.
- [ ] 6.4 Security review (`cso` / `hgk-security`): no supply-chain, dependency or CVE review of the
      repaired wheel was performed.
