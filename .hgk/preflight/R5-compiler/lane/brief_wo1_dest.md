# LANE R5-WO1 — pipd `project --out` destination safety (fail-closed before any delete)

You are the admitted bounded EXECUTE writer for PIPD requirement `REQ-PIPD-R5-DEST-001`
(HGK workorder `WO-TS-req-pipd-r5-dest-001`), discharged from external finding
`F-R4-S4-01` / `S4-USER-SEC-001` (P0).

## Environment note (read first)
- The repository root is mounted at `/w`. Work ONLY inside `/w`.
- This repository uses **unittest**, not pytest.
- The image has **no git binary**: `git rev-parse HEAD` is unavailable and any test that shells
  out to git will error. Run only the targeted modules listed below, using the module form:
  `python3 -m unittest tests.test_web_pack -v`
- No network access beyond the model endpoint. Never fetch anything.

## Confirmed defect (do not re-litigate it, fix it)
`src/pipd_ls_sp/projection.py` `project_surfaces()` currently does, with no validation at all:

```python
out = Path(out)
if out.exists():
    shutil.rmtree(out)      # <-- unrestricted recursive delete of a caller-supplied path
out.mkdir(parents=True)
```

`src/pipd_ls_sp/cli.py` line ~161 passes `args.out` (an arbitrary user-supplied `--out`) straight
into it, so `pipd project --out <anything>` can recursively delete a directory the user did not
intend to destroy (repo root, cwd, home, a source ancestor, ...). R4 hardened
`tools/round_envelope.py` (STOP-1..6); that does **not** cover this product CLI call chain.

## Files you may change (nothing else)
- `src/pipd_ls_sp/projection.py`
- `src/pipd_ls_sp/workspace.py`
- `src/pipd_ls_sp/cli.py`
- `tests/test_project_destination_safety.py` (new)
- You may NOT touch `src/pipd_ls_sp/errors.py`, `pipeline.py`, `registry.py`, `schemas/`, `tools/`,
  any other test module, or anything under `.hgk/` (except writing your own scratch under
  `/w/.hgk/r5-lane-probe/`).

## Required behaviour

### 1. One shared destination resolver (in `projection.py`)
```python
def resolve_output_destination(root, out, *, authorized_roots=None, allow_replace=None) -> Path
```
`root` is the source/repo root. Semantics:

- **Normalisation / refusal, ALL of these before any filesystem mutation:**
  - `out is None`, empty or whitespace-only -> refuse.
  - A POSIX/MSYS-style absolute path (e.g. `/c/Users/...`, `/tmp/x`) on this Windows host resolves
    to a *wrong* drive-relative path (`C:\c\Users\...`). Detect a leading `/` that is not a UNC
    path and **refuse it typed** (reason mentions MSYS/POSIX form). Never silently reinterpret it.
  - Resolve with `Path(out).expanduser().resolve(strict=False)` and compare case-insensitively
    (`os.path.normcase`) against: the current working directory, `Path.home()`, the filesystem
    root / drive root (`Path(resolved.anchor)`), the source `root` itself, the repo `.git` dir, and
    every **ancestor** of `root`. Each match -> typed refusal.
  - Refuse `out` whose resolved path is a symlink/junction/reparse point escaping outside the
    candidate region (resolve then re-check containment; do not follow a link out of an authorized
    root).
  - Refuse when `resolved == root` or `root` is a descendant of `resolved` (i.e. writing would
    delete the source tree).
- **Authorized roots:** when `authorized_roots` is a non-empty sequence, the resolved target must
  be *strictly inside* one of them (`resolved != the_authorized_root` is allowed only when the
  target is a proper subpath; a target equal to the authorized root itself is allowed too — but
  never when that root is one of the always-denied paths above). Anything outside every authorized
  root (a "foreign absolute dir") -> typed refusal.
- **Preexisting data:** if the resolved target exists and is a non-empty directory (or a file),
  refuse unless `allow_replace` is true. `allow_replace=None` means: **True when
  `authorized_roots is None`** (trusted in-process callers/tools keep the documented regeneration
  contract), **False when `authorized_roots` is supplied** (user-facing CLI).
- **TOCTOU:** re-verify the containment/permission immediately before the publish step (open/stage
  under the OS check); never rely on the check made minutes earlier.
- The refusal must be a **typed** exception: define `class UnsafeDestination(ProjectionError)` in
  `projection.py` with `code = "UNSAFE_DESTINATION"` and a message that names the reason and the
  resolved path. It must reach the CLI as a typed JSON envelope with `verdict: FAIL` and
  `code: UNSAFE_DESTINATION`, exit code != 0 (the existing `PipdError` path in `cli.main` gives 2).
  Add `UNSAFE_DESTINATION` to the `project`/`export` `FAILURE_CODES` string in `cli.py`.
- Never `shutil.rmtree` a caller-supplied path. Publish by **staging + atomic replace**:
  stage into a uniquely named sibling directory on the same volume, write every artefact there,
  run the existing strict gates against the staged tree, then publish:
  1. if the target exists, rename it to `<target>.pipd-backup-<token>` (kept, never deleted) and
     report that path as the rollback pointer;
  2. `os.replace(stage, target)`;
  3. on any failure after step 1, restore the backup back to the original name.
  Files under the published target must be **byte-identical** to what the old code wrote for the
  same source state (the existing byte-determinism and stale-source tests must still pass).

### 2. `project_surfaces` signature (both in `projection.py` and the `workspace.py` wrapper)
```python
def project_surfaces(root, out, *, authorized_roots=None, allow_replace=None) -> dict
```
- Calls the resolver first (so the refusal happens **before** any create/delete).
- Keeps every existing key in the returned dict and adds:
  `"destination": {"resolved": str, "authorized_roots": [...], "replaced": bool,
  "rollback_pointer": str | None, "staged": str}`.
- Adds a generated-surface marker file inside the published target
  (`.pipd-generated-surface.json`, content includes `schema`, `source_root`, `generated_at`).
  It must NOT be counted as one of the Web/Host/IR artefacts by any check.
  Update `check_web_surface` / `check_host_surfaces` (and any glob that iterates the target) so the
  marker never appears in their denominators or strict checks.

### 3. CLI (`cli.py`)
- `project` gains `--allow-root` (repeatable, `Path`) and `--allow-replace` (store_true).
- Authorized roots for a CLI run = the `--allow-root` values plus, when
  `PIPD_PROJECT_ALLOWED_ROOTS` is set in the environment, its `os.pathsep`-separated entries, plus
  the built-in generated surface `<root>/dist`. If `--out` is omitted, the target stays
  `<root>/dist/web` and `allow_replace=True` (it is the project's own generated surface).
- `--dry-run`: run the *same* resolver, report
  `"destination_safety": {"safe": true|false, "code": ..., "resolved": ..., "reason": ...}`.
  A dangerous destination in dry-run must still be a **typed refusal with exit != 0** and must
  write nothing anywhere. A safe dry-run reports the plan and writes nothing.
- `project` must never silently ignore `--out`.

### 4. New tests — `tests/test_project_destination_safety.py`
Drive the CLI as a subprocess exactly like `tests/test_cli_typed_errors.py` does
(`[sys.executable, "-B", "-m", "pipd_ls_sp.cli", ...]` with `PYTHONPATH`/cwd set so the in-tree
package is used). For every case assert: exit code != 0, `code == "UNSAFE_DESTINATION"` in stdout,
and a **before/after canary hash** of the whole touched tree is unchanged.

Negative cases (each in a dedicated disposable scratch tree, NEVER against `/w` itself):
`--out .`, `--out ..`, repo root, the scratch cwd, `$HOME`, the filesystem root, a source
ancestor, a source descendant that is an ancestor of cwd, an existing **non-empty** foreign dir
without `--allow-replace`, a symlink/junction pointing outside the authorized root, `/c/...` MSYS
form, empty and whitespace `--out`.

Positive control: `--out <scratch>/out --allow-root <scratch>` writes the 5 Web documents + 3 host
projections + `PROJECTION_IR.json` (5/5, 3/3), the canary of the *source* tree is unchanged, and a
second run with the same arguments refuses (non-empty) while `--allow-replace` publishes again and
leaves a reported `.pipd-backup-<token>` containing the previous bytes.

Also assert `project --dry-run` on a dangerous destination refuses typed and creates nothing.

## Definition of done (report exactly these, with raw output)
1. `python3 -m unittest tests.test_project_destination_safety -v` -> all pass.
2. `python3 -m unittest tests.test_web_pack tests.test_host_projection tests.test_cli_typed_errors -v`
   -> no regressions (these must pass WITHOUT git; if a pre-existing failure is caused solely by the
   missing git binary, say so explicitly and show the error text instead of hiding it).
3. `python3 -m pipd_ls_sp.cli project --out . --root /w` -> typed refusal, exit != 0.
4. `python3 -m pipd_ls_sp.cli project --dry-run --out /c/anything --root /w` -> typed refusal.
5. A `diff`-style summary of exactly which files you changed and why (no other file touched).

Write your final summary as plain text at the end. Do not create commits (there is no git here).
