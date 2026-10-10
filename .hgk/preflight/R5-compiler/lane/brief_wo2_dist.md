# LANE R5-WO2 — `pipd` distributable: current wheel + install-safe schema resources

You are the admitted bounded EXECUTE writer for PIPD requirement `REQ-PIPD-R5-DIST-002`
(HGK workorder `WO-TS-req-pipd-r5-dist-002`), discharged from external finding
`F-R4-S4-02` / `S4-USER-DIST-002` (P0).

## Environment note (read first)
- The repository root is mounted at `/w`. Work ONLY inside `/w`.
- This repository uses **unittest**, not pytest.
- The image has **no git binary** and **no network**. Never fetch anything. Do not run `git`.
- Run only the targeted modules listed below, in module form: `python3 -m unittest tests.test_x -v`.
- `jsonschema` is installed in the image (4.26.0).

## Confirmed defect (do not re-litigate it, fix it)
`dist/WHEEL_MANIFEST.json` records `candidate_head=829c17e...` and a 60,980-byte wheel whose member
manifest lists only old modules. The current source has `requirements.py`, `repo_context.py`,
`projection.py` and 19 `schemas/*.schema.json` that the published wheel does not carry.
Separately `src/pipd_ls_sp/registry.py::_root()` is
`Path(__file__).resolve().parents[2]`, i.e. the *repo root*. Installed into site-packages that
resolves outside the package, so an installed `pipd` cannot find `schemas/registry.json` without
the source checkout. A user who installs the wheel therefore gets a CLI that cannot load its own
contract registry.

## Files you may change (nothing else)
- `tools/build_dist.py`
- `src/pipd_ls_sp/registry.py`
- `pyproject.toml`
- `tools/portable_install_check.py`
- `tests/test_wheel_distribution.py` (new)
- You may NOT touch `src/pipd_ls_sp/cli.py`, `workspace.py`, `projection.py`, `pipeline.py`,
  `errors.py`, any other test module, `schemas/`, or anything under `.hgk/`
  (except your own scratch under `/w/.hgk/r5-lane-probe/`).

## Required behaviour

### 1. Install-safe schema resources (`registry.py`)
- Keep `load_registry(schemas_dir=None)` / `load_schema(...)` signatures and semantics unchanged
  (exact 19-family check, order check, required_fields check).
- Replace `_root()` with a resolver, in this strict order, returning the first that contains
  `registry.json`:
  1. `$PIPD_SCHEMAS_DIR` when set and non-empty (explicit override);
  2. the packaged location, via `importlib.resources.files("pipd_ls_sp") / "schemas"` — use the
     `as_file` / `Path(...)` form that works for a real directory AND for a zipped/re-homed
     install; never assume a filesystem path exists without checking it;
  3. the source-tree fallback `<repo_root>/schemas` (keeps the in-tree tests and tools working).
- A resolver miss must raise the existing typed `ValidationFail` naming every location it tried.
- Keep the module importable with no third-party imports at module import time.

### 2. Wheel content (`tools/build_dist.py`)
- The built wheel must contain, in addition to every `src/pipd_ls_sp/**/*.py`:
  `pipd_ls_sp/schemas/registry.json` and all `pipd_ls_sp/schemas/*.schema.json` (the whole `schemas/`
  tree, mapped into the package).
- Add `pipd_ls_sp/py.typed`-style package-data declaration to `pyproject.toml` (`[tool.setuptools]
  packages` + `package-data` for `pipd_ls_sp` = `["schemas/*.json"]`), and keep the file honest:
  the wheel is hand-built (no build backend offline) — say so in a comment.
- `WHEEL_MANIFEST.json` must record the **frozen candidate identity of the tree it was built from**:
  `candidate_head` (read from `.hgk/rounds/R5-20261009-s4-user-operability/FROZEN_SOURCE.json` when
  that file exists, else `"UNKNOWN_FROZEN_SOURCE"` — never invent a SHA, never shell out to git),
  plus `product_digest` = sha256 over the canonical JSON of `[[relpath, sha256], ...]` for every file
  that went INTO the wheel, and `member_count`.
- Refuse to build when the source tree is missing any of: `schemas/registry.json`, every schema file
  named by that registry, `src/pipd_ls_sp/cli.py`, `src/pipd_ls_sp/requirements.py`,
  `src/pipd_ls_sp/repo_context.py`, `src/pipd_ls_sp/projection.py`. Raise a plain `RuntimeError`
  naming the missing members (this tool has no PipdError dependency) and exit non-zero.
- Keep determinism: fixed zip timestamps, sorted member order — two builds of the same tree must
  produce a byte-identical wheel.
- Delete the stale `dist/pipd_ls_sp-0.1.0-py3-none-any.whl`+`.sha256` only by overwriting them with
  the new build; do not leave the old bytes reachable under the published name.

### 3. Portable install check (`tools/portable_install_check.py`)
Extend it so it proves the installed package is self-sufficient. It must, in a fresh isolated
environment it creates itself:
- `python -m venv <scratch>/venv` → `pip install --no-index --no-deps <wheel>` (jsonschema is not
  installable offline; that is expected and must be reported as a typed limitation, not hidden);
- run from a cwd OUTSIDE the repo with `PYTHONPATH` and `PYTHONHOME` **unset**, invoking
  `<venv>/Scripts/python.exe -c "import pipd_ls_sp, pipd_ls_sp.registry as r; print(pipd_ls_sp.__file__); print(r.load_registry()['schema'])"`
  or equivalent — the import must resolve to site-packages, and the registry must load 19/19 from
  the packaged copy;
- assert `os.path.commonpath([pydir, repo_root]) != repo_root` for the imported module path (i.e.
  it is NOT the source checkout);
- mutating negative: with the packaged `schemas/registry.json` removed, the load must FAIL typed.
Emit a JSON report with per-step `argv`, `exit`, and captured output; exit non-zero on any step fail.

### 4. New tests — `tests/test_wheel_distribution.py`
- Build the wheel into a temp dist dir and assert every required member is present and that the
  recorded member sha equals the sha of the bytes inside the zip (recompute from the archive).
- Assert the wheel contains all four required modules and 19 schema files + `registry.json`.
- Assert `registry.load_registry(<extracted package schemas dir>)` returns 19 families — proving the
  packaged copy is complete and self-consistent.
- Assert determinism: build twice, same sha256.
- Skip-with-explicit-reason (do NOT silently pass) any check that requires a real venv if
  `venv`/`pip` is unavailable in the test interpreter; print the reason.

## Definition of done (report exactly these, with raw output)
1. `python3 -m unittest tests.test_wheel_distribution -v` → all pass.
2. `python3 tools/build_dist.py` → prints the wheel sha + member_count; then
   `python3 -c "..."` proving the built zip contains the 19 schemas and the 4 modules.
3. `python3 -m unittest tests.test_cli_typed_errors tests.test_web_pack tests.test_host_projection -v`
   → no regressions caused by your change (report any pre-existing failure verbatim).
4. `python3 tools/portable_install_check.py` → report its exit code and the JSON report path.
5. A plain-text list of exactly which files you changed and why. No other file touched.

Do not create commits (there is no git here). Write your final summary as plain text at the end.
