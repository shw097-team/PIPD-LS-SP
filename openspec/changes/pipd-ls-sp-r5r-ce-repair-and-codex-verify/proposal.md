## Why

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
