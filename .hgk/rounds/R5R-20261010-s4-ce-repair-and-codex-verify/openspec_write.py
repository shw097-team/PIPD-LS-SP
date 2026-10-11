import pathlib

BASE = pathlib.Path(__file__).resolve().parents[1] / "openspec" / "changes" / "pipd-ls-sp-r5r-ce-repair-and-codex-verify"
(BASE / "specs" / "pipd-s4-ce-repair").mkdir(parents=True, exist_ok=True)

(BASE / "proposal.md").write_text("""## Why

The R5Q preview was published, and its second independent verification run returned
`COUNTEREXAMPLE_FOUND` rather than a clean pass. Two defects were reproduced by the maker directly
against the published wheel bytes:

- **CE-1** — `validate` does not resolve the schemas the wheel ships, while `doctor` in the same
  environment does. `cli.py` hands `validate` exactly `root / "schemas"` (defaulting to the current
  directory), whereas `doctor` resolves `OVERRIDE -> INSTALLED -> SOURCE` through `registry.py`. A user
  who installs the wheel and runs `validate` from their own directory gets `INPUT_SHAPE_INVALID` /
  `FileNotFoundError: <cwd>/schemas/PI-PKG.schema.json` while `doctor` is green.
- **CE-2** — `validate` rejects a bundle assembled from the four compilers' own unmodified stdout.
  `pipeline.py` attaches `_profile_meta` and its own comment declares it a non-record sidecar
  "stripped before validation"; `validate._body_hash` does exclude it, but `validate_record` schema-checks
  the record unstripped, and `PI-PKG` sets `additionalProperties: false`.

Both are cases of the validator contradicting semantics the codebase already declares. Neither breaks
installation, licence packaging, `doctor`, the CLI or any artefact hash, so neither is stop-ship — but
the published tag is immutable, so a fix can only ship as a superseding artefact.

## What Changes

- **`validate` resolves schemas the way `doctor` does.** A single resolver in `registry.py` keeps the
  existing `OVERRIDE -> INSTALLED -> SOURCE` order and lets a workspace-local `root/schemas` win only
  when it actually carries `registry.json`. The chosen source is reported in `validate`'s own output.
- **The non-record sidecar list exists once.** `NON_RECORD_SIDECARS` is defined in one place and consumed
  by `_body_hash`, `validate_record`/`validate_bundle` and `pipeline`, so schema validation happens on a
  copy with the sidecars removed — the behaviour the comment already claimed.
- **Regression tests pin both behaviours**, each demonstrated failing against the pre-repair tree.
- **Independent verification moves to the CODEX CLI** on the specified checker model (GPT 6.1 SOL-MEDIUM
  via OpenAI OAuth), in its own `CODEX_HOME`, and must really install and really run PIPD-LS-SP.
- **No published tag is rewritten.** `v0.1.0-preview.1` keeps its bytes; the repair is a candidate for a
  superseding release, and whether to cut one remains the owner's decision.

## Impact

- Affected: `src/pipd_ls_sp/{cli,validate,registry,pipeline}.py`, `tests/`, the R5R round evidence and the
  public CE disclosure wording.
- Not affected: `schemas/**` (no schema is edited), the published tag/commit/wheel bytes, the claim
  ceiling, `DEL-018`.
""", encoding="utf-8", newline="")

(BASE / "design.md").write_text("""## Context

`validate` and `doctor` answer the same question — "where are the canonical schemas?" — with two different
mechanisms. That divergence is the whole of CE-1. CE-2 is narrower: a documented stripping step was
implemented in the hashing path and forgotten in the schema-checking path.

## Decisions

### D1 — One resolver, and the workspace still wins when it is real

`validate` goes through the registry resolver rather than a bare `root / "schemas"`. A workspace-local
`schemas/` directory is prepended **only if it contains `registry.json`**, so in-tree development and the
canonical resolution order both keep working. Making the whole `--root/schemas` path an unconditional
first candidate would have let an arbitrary directory shadow the shipped schemas — a silent
wrong-schema failure, which is worse than the loud one being fixed.

### D2 — The sidecar list is a single object, not a repeated literal

The fix for CE-2 is small, but the *reason* it happened is that a five-element list was written by hand in
more than one place and one copy drifted. The repair therefore defines the list once and imports it
everywhere, and a test asserts the two modules reference the same object, so a future copy-paste fails
loudly instead of silently reintroducing the defect.

### D3 — No schema edits, no artefact edits

Adding `_profile_meta` to `PI-PKG.schema.json` would be a canonical contract change and would alter the
schema set inside the wheel; removing the sidecar from the emitted PI-PKG would break
`tools/run_s1_slice.py`, which reads `pi["_profile_meta"]["profile"]`. Both are larger than the defect.
The project's own convention, stated in `pipeline.py`, is that SoD/ceiling data lives inside declared
fields and schemas are not edited to accommodate a sidecar.

### D4 — The published tag stays frozen

`OWNER_LICENSE_DECISION.yaml` records that published tags are never rewritten and a superseding release is
issued instead. This change is therefore a candidate for the *next* release, not a rewrite of
`v0.1.0-preview.1`.

## Risks

- **Wrong-binary risk.** A repaired `src/` does not retroactively change the published wheel. A reader who
  installs `v0.1.0-preview.1` still meets CE-1/CE-2. The public disclosure must say "fixed on the next
  release", not "fixed".
- **Shadowing risk.** Mitigated by D1: a `root/schemas` candidate is accepted only with `registry.json`
  present.
- **Test-only green.** Mitigated by requiring the red state to be captured before the fix and by an
  end-to-end check that runs the installed wheel from outside the repository with unmodified compiler
  output.

## Migration

None. No schema, no data and no published artefact changes shape.
""", encoding="utf-8", newline="")

(BASE / "tasks.md").write_text("""# Tasks — R5R CE-1/CE-2 repair + CODEX-CLI verification

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
""", encoding="utf-8", newline="")

(BASE / "specs" / "pipd-s4-ce-repair" / "spec.md").write_text("""## ADDED Requirements

### Requirement: The validator resolves schemas the same way the doctor does

`validate` SHALL resolve the canonical schema set through the same mechanism `doctor` uses, so that both
commands agree about where the schemas live, and SHALL report the source it actually resolved.

#### Scenario: an installed wheel is validated from an unrelated directory

- **WHEN** the wheel is installed into a clean environment and `validate` is run from a directory that
  contains no `schemas/` directory and no `--root`
- **THEN** the schemas shipped inside the installed package are used, `validate` reaches a verdict, and
  the reported schema-source mode is `INSTALLED`
- **AND** it does not fail with a missing-file error naming `<cwd>/schemas/PI-PKG.schema.json`

#### Scenario: a workspace carrying its own schemas still wins

- **WHEN** `--root` points at a directory whose `schemas/` contains `registry.json`
- **THEN** that directory's schemas are used in preference to the packaged copy
- **AND** a `schemas/` directory without `registry.json` does not shadow the packaged set

### Requirement: The validator accepts the toolchain's own unmodified output

A validation bundle assembled from the four compilers' unmodified stdout SHALL be accepted, because the
non-record sidecars the pipeline attaches are declared to be stripped before schema validation.

#### Scenario: the compiler output is validated without hand-editing

- **WHEN** a bundle is assembled from the raw output of `compile-pi`, `bind-pd`, `compile-ecp` and
  `compile-tqaep` and passed to `validate`
- **THEN** the verdict is `PASS` with four records checked and no findings
- **AND** the caller did not have to delete `_profile_meta` or otherwise edit the artefacts

#### Scenario: a body edited without re-issuing identity is still caught

- **WHEN** a release-bound record's body is modified without recomputing `content_hash`
- **THEN** validation still reports that the `content_hash` does not match the record body

### Requirement: The non-record sidecar set has exactly one definition

The set of keys treated as non-record sidecars SHALL be defined once and consumed by every code path that
needs it, so the definitions cannot drift apart.

#### Scenario: a consumer reads the sidecar set

- **WHEN** the pipeline and the validator refer to the sidecar set
- **THEN** they refer to the same object rather than to two hand-written copies

### Requirement: The published tag is not rewritten by a repair

A repair SHALL NOT alter the bytes of an already-published tag or release.

#### Scenario: the repair is delivered

- **WHEN** the repair lands
- **THEN** the published tag, its commit, its tree and its wheel bytes are unchanged, and the repair is a
  candidate for a superseding release issued by the owner
""", encoding="utf-8", newline="")

print("wrote:", *sorted(str(p.relative_to(BASE.parents[2])) for p in BASE.rglob("*") if p.is_file()), sep="\n  ")
