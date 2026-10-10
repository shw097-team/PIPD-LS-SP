# R5R-20261010-s4 CE-repair — EXECUTE lane summary (bounded writer)

- Round: `R5R-20261010-s4-ce-repair-and-codex-verify`
- Work order: `WO-R5R-REPAIR-002`
- Requirement: `REQ-PIPD-R5R-REPAIR-002`
- Decision of record: `.hgk/rounds/R5R-.../far/R5R_FAR_CE_REPAIR_QUICKSTUDY.md` §4 (accept A1 + B1)
- Base commit: `9bd33a1` (branch `r5r-ce-repair`)
- Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
- Nothing committed, nothing pushed, no venv built from this repo, no wheel built,
  nothing under `schemas/` edited.

## What I changed, file by file

### `src/pipd_ls_sp/registry.py` — NEW `resolve_for_validate(root)`

One new function that `validate` resolves through. It reuses the EXISTING candidate chain
(`_candidate_schemas_dirs_with_mode`, i.e. `OVERRIDE -> INSTALLED -> SOURCE`) — no second
ordering scheme, the existing order untouched — but inserts a workspace-local `<root>/schemas`
**at the front, and only when it actually contains `registry.json`** (reported as mode
`WORKSPACE`). A `<root>/schemas` without a `registry.json` is skipped exactly like any other
candidate; it never displaces a real copy. Returns the same `(path, mode, tried)` shape as
`_resolve_schemas_dir_and_mode`, and `NONE` with the probe list when nothing resolves.

### `src/pipd_ls_sp/cli.py` — `validate` uses the resolver and reports it

`validate` now calls `registry.resolve_for_validate(root)` instead of passing `root / "schemas"`.
It adds a `schema_source` field `{mode, path, tried}` (same spirit as `doctor`'s field) — no
existing field removed. When nothing resolves, it still refuses (verdict `FAIL`, code
`SCHEMA_RESOLUTION`).

### `src/pipd_ls_sp/validate.py` — single sidecar definition (CE-2)

Added module-level `NON_RECORD_SIDECARS = ("subject_id", "version", "content_hash",
"schema_version", "trace", "_profile_meta")`. `_body_hash` now references it (identical key set
to before, so `content_hash` semantics and the "body edited without re-issuing identity" check
are unchanged). `validate_record` schema-checks a **copy** with the sidecars removed.

Precision point: a sidecar key that the schema itself declares (identity fields and `trace` are
declared *and* required) is **not** removed — only sidecars the schema does not declare (the
genuine non-record sidecar `_profile_meta`) are stripped. This closes CE-2 without weakening any
required-field or `additionalProperties` check. I chose this because a literal "strip the whole
list" implementation broke required-property validation (my first green attempt failed the CE-1
and CE-2 tests with `'trace'/'subject_id'/... is a required property`); the constant still has
exactly one definition, which is what the order's regression test pins.

### `src/pipd_ls_sp/pipeline.py` — references the same object

Imports `NON_RECORD_SIDECARS` from `validate` and uses it in `_seal` where the sidecar is
stripped for hashing. `pipeline.NON_RECORD_SIDECARS is validate.NON_RECORD_SIDECARS` (verified).
I did **not** change `_profile_meta` emission (it stays in the artefact) and did **not** touch any
JSON schema.

### `tests/test_ce_repair_regression.py` — NEW (5 tests)

1. `CE1ValidateSchemaResolutionTests.test_validate_resolves_shipped_schemas_without_workspace_schemas`
   — cwd has no `schemas/`; `validate` must reach a verdict (was `FileNotFoundError` →
   `INPUT_SHAPE_INVALID`/exit 2) and report `schema_source.mode == "SOURCE"`.
2. `...test_workspace_local_schemas_still_takes_precedence` — a workspace-local `schemas/` with
   `registry.json` wins (`mode == "WORKSPACE"`, path == `<ws>/schemas`).
3. `...test_validate_reports_schema_source_mode` — the report names the mode and has keys
   `{mode, path, tried}`.
4. `CE2CompilerStdoutTests.test_compilers_own_stdout_bundle_is_accepted` — a bundle from the real
   `intake → compile-pi → bind-pd → compile-ecp → compile-tqaep` functions (temporary git repo
   for `bind-pd`), PI keeping `_profile_meta`: `verdict == "PASS"`, `checked == 4`,
   `findings == []`.
5. `...test_sidecar_list_has_one_definition` — `pipeline.NON_RECORD_SIDECARS is
   validate.NON_RECORD_SIDECARS` and contains `_profile_meta`.

## Red → green (raw captured output)

Test command (single line, cwd = repo root, `PYTHONPATH` unset):

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest tests.test_ce_repair_regression -v
```

- Before implementing — `execute/red_state.txt`: `Ran 5 tests … FAILED (failures=3, errors=2)`.
  CE-1 failure is the genuine `FileNotFoundError: …/cwd/schemas/PI-PKG.schema.json`; CE-2 failure
  is `Additional properties are not allowed ('_profile_meta' was unexpected)`; the sidecar and
  `schema_source` tests fail with `KeyError`/`AttributeError`.
- After implementing — `execute/green_state.txt`: `Ran 5 tests in 7.575s … OK`.

Full suite (cwd = repo root, `PYTHONPATH` unset):

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest discover -s tests -t .
```

- Before repair (dependency present): `Ran 311 tests … OK (skipped=3)`.
- After repair: `Ran 316 tests in 109.051s … OK (skipped=3)`.

`execute/proposed_patch.diff` is the `git diff` of `src/pipd_ls_sp` for the checker.

## Environment note (disclosed, not hidden)

The designated interpreter did **not** have `jsonschema` installed, so the pre-existing suite ran
red (7 failures / 7 errors, all `TOOL_MISSING/ModuleNotFoundError: jsonschema`) — no `validate`
path could run at all, so a truthful CE-1/CE-2 red→green was impossible without it. `jsonschema`
is a declared dependency (`pyproject.toml`) and a local offline wheelhouse already held it, so I
installed it into the interpreter from the local wheels only (`--no-index`), from
`C:/Projects/Agent_Workspace/HG-KSEOS/var/hermes-disposable/TST-054-001/wheelhouse` (jsonschema
4.26.0 + attrs/referencing/rpds-py/jsonschema-specifications). No network access was used. With the
dependency present the pre-repair tree is otherwise green (311 OK), which is the baseline the
above red→green is measured against.

## Explicit list of things I did NOT do / could NOT do

- Did not commit, did not push.
- Did not build a wheel; did not create a venv for this repo.
- Did not edit anything under `schemas/`.
- Did not remove `_profile_meta` from the emitted artefact; did not add it to any JSON schema; did
  not make the validator tolerate arbitrary unknown keys.
- Did not touch any file outside the scope list. Two `.hgk/artifacts/…` paths are touched by the
  test suite itself (a test rewrites `candidate_head`, another leaves `tqaep_design_tmp/`); I
  reverted the tracked one with `git checkout --` and removed the untracked temp dir, so the
  worktree shows only the four in-scope `src/` edits, the new test file, and the round/openspec
  evidence dirs.
- Did NOT run: the FAR §5 end-to-end "installed wheel outside the repo" check, the CODEX-CLI
  independent VERIFY lane, KANBAN/SWARM/GSTACK/OPENSPEC receipts, disclosure updates, or any
  release. Those are other lanes / the owner's publication decision per the FAR §6 and the
  work order.
- Did not close `DEL-018` and did not advance any claim ceiling.
