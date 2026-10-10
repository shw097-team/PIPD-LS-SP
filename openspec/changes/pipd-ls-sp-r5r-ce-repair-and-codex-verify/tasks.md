# Tasks — R5R CE-1/CE-2 repair + CODEX-CLI verification

## 1. Admission and research

- [x] 1.1 HGK admission of the six R5R obligations through the typed SharedSpine lifecycle API.
- [x] 1.2 FAR quick study root-causing CE-1 and CE-2 from the source, with candidates and a decision.
- [ ] 1.3 Record the decision of record in the round evidence pack.

## 2. Repair (EXECUTE lane, via the CODEX CLI)

- [ ] 2.1 CE-1: `validate` resolves schemas through the registry resolver, `root/schemas` only when it
      carries `registry.json`, and reports the source it used.
- [ ] 2.2 CE-2: `NON_RECORD_SIDECARS` defined once and consumed by `_body_hash`, the schema-checking path
      and `pipeline`; schema validation runs on the stripped copy.
- [ ] 2.3 Red state captured before the repair, green state after.

## 3. Regression

- [ ] 3.1 A test that fails before the repair on the CE-1 path and passes after.
- [ ] 3.2 A test that fails before the repair on the CE-2 path and passes after.
- [ ] 3.3 A test asserting the sidecar list has exactly one definition.
- [ ] 3.4 The full deterministic suite stays green.
- [ ] 3.5 End-to-end: installed wheel, run outside the repository, unmodified compiler output, `validate`
      reaches PASS.

## 4. Independent verification (VERIFY lane, CODEX CLI)

- [ ] 4.1 Executed through the CODEX CLI on GPT 6.1 SOL-MEDIUM (OpenAI OAuth) in a separate `CODEX_HOME`.
- [ ] 4.2 The checker really installs PIPD-LS-SP and really runs it, with the raw transcript recorded.
- [ ] 4.3 The checker's verdict is its own; the maker does not sign it.

## 5. Disclosure and surfaces

- [ ] 5.1 Public disclosure advanced to the repaired state, saying what is fixed and what still applies to
      the already-published preview.
- [ ] 5.2 KANBAN, SWARM, GSTACK and OPENSPEC receipts recorded in the round.

## 6. Not in this round

- [ ] 6.1 Cutting a superseding release — the owner's publication decision, not the maker's.
- [ ] 6.2 `DEL-018 RELEASE_MANIFEST@1` closure.
- [ ] 6.3 S5–S8 live execution and host-native certification.
