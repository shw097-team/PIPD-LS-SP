# LANE R5-WO3 — `pipd export --out` must actually deliver a portable bundle

You are the admitted bounded EXECUTE writer for PIPD requirement `REQ-PIPD-R5-EXPORT-003`
(HGK workorder `WO-TS-req-pipd-r5-export-003`), discharged from external finding
`F-R4-S4-03` / `S4-USER-EXPORT-003` (P1).

## Environment note (read first)
- Repository root is mounted at `/w`. Work ONLY inside `/w`.
- unittest, not pytest. The image has **no git binary** and no network. Never run `git`, never fetch.
- Run tests in module form: `python3 -m unittest tests.test_export_bundle -v`.
- The R5-WO1 destination hardening is ALREADY in the tree. Read it before you write anything:
  `src/pipd_ls_sp/projection.py::resolve_output_destination` and `cli.py`'s `project` branch.
  Reuse it — do NOT create a second destination policy.

## Confirmed defect (do not re-litigate it, fix it)
`cli.py` `export` ignores `args.out` entirely: the non-dry-run branch is `return
workspace.export_manifest(root)`, and `export_manifest` returns an in-memory dict. So
`pipd export --out <path>` declares in `--dry-run` that it would write `<path>` and then writes
nothing at all. 總藍圖 §5.9.3 defines `pipd export` as a **portable export** delivering an archive,
a manifest and checksums.

## Files you may change (nothing else)
- `src/pipd_ls_sp/cli.py`
- `src/pipd_ls_sp/workspace.py`
- `src/pipd_ls_sp/errors.py` (add typed error classes only; keep every existing class and code)
- `src/pipd_ls_sp/export_bundle.py` (new module — keep it small and dependency-free)
- `tests/test_export_bundle.py` (new)
- `tools/cli_smoke.py` (only if the 13-command smoke needs the new flags; keep all 13 commands)
- You may NOT touch `projection.py`, `pipeline.py`, `registry.py`, `requirements.py`,
  `repo_context.py`, `schemas/`, `dist/`, any other test module, or anything under `.hgk/`
  (except your own scratch under `/w/.hgk/r5-lane-probe/`).

## Required behaviour

### 1. `export --out <path>` really writes a bundle
Write, into the resolved destination directory:
- `<name>.tar.gz` (deterministic: fixed mtime/uid/gid/mode per member, members sorted by rel path,
  no directory entries required) — a portable archive of the manifest's file set;
- `export_manifest.json` — `{"schema": "PIPD-EXPORT-BUNDLE/1", "generated_at", "source_root",
  "file_count", "archive": {"name","size","sha256"}, "files": [{"rel","size","sha256"}...]}` with
  `files` sorted by `rel`;
- `SHA256SUMS` — `<sha>  <rel>` lines, sorted, including the archive itself.
The archive member paths must equal the manifest `rel` values, and every `sha256` in the manifest
must recompute from the archive's member bytes when it is unpacked independently.

### 2. Destination, staging and refusal
- Resolve the destination with the EXISTING `projection.resolve_output_destination`, called before
  any create/delete. Add `export --allow-root` (repeatable, `Path`) and read
  `PIPD_PROJECT_ALLOWED_ROOTS` (os.pathsep-separated); the built-in default root is `<root>/dist`.
  A refusal must reach the CLI as the same typed `UNSAFE_DESTINATION` envelope, exit != 0.
- Stage into a sibling directory on the same volume, verify the staged bundle by re-opening the
  archive and recomputing every member sha, then publish atomically; if the target already existed,
  keep it as `<target>.pipd-backup-<token>` and report the path. **Never `shutil.rmtree` a
  caller-supplied path.**

### 3. Secret / traversal safety
- Reuse `workspace.secret_scan` over the source set. On any hit, write **nothing anywhere** and
  exit non-zero typed (`EXPORT_SECRET_SCAN`).
- Any member whose rel path is absolute, contains `..`, or escapes the source root ⇒ refuse the
  whole export typed, writing nothing.

### 4. Keep the read-only mode distinct and honest
- `export --out ... --dry-run` ⇒ report the plan (destination, file count, manifest sha) and write
  **nothing**.
- `export` **without** `--out` ⇒ keep the current read-only behaviour (return the in-memory manifest
  dict) and SAY SO in the payload: add `"mode": "READ_ONLY_MANIFEST"` and
  `"note": "no --out given: nothing was written; this is the read-only manifest projection"`.
  This keeps `tools/cli_smoke.py`'s 13-command run green — do not break it.

### 5. New tests — `tests/test_export_bundle.py`
Drive the CLI as a subprocess (`[sys.executable, "-B", "-m", "pipd_ls_sp.cli", "--root", <repo>]`,
`PYTHONPATH` = the in-tree `src`, cwd OUTSIDE the repo), each case in its own disposable scratch
tree, and assert:
- `export --out <scratch>/out --allow-root <scratch>` exits 0; the archive, manifest and SHA256SUMS
  exist; unpacking the archive independently reproduces every manifest `rel` with the recorded sha;
- byte replay: two exports of the same frozen source produce the same manifest `files` digest;
- `--dry-run` creates nothing (whole-tree canary before/after identical);
- a planted credential in the exported source set ⇒ non-zero exit, zero files in the destination;
- `--out .`, `--out <repo root>`, `--out <cwd>`, `--out /c/anything`, empty `--out` ⇒ typed
  `UNSAFE_DESTINATION`, exit != 0, canary unchanged;
- a pre-existing non-empty destination without `--allow-replace` ⇒ refused; with it ⇒ published
  and the previous bytes retrievable from the reported backup path.

## Definition of done (report exactly these, with raw output)
1. `python3 -m unittest tests.test_export_bundle -v` → all pass.
2. `python3 -m unittest tests.test_project_destination_safety tests.test_web_pack tests.test_host_projection tests.test_cli_typed_errors -v` → no NEW failures vs the pre-existing git-binary-only ones; state them explicitly.
3. `python3 tools/cli_smoke.py` → report the exit code and the `nonzero_exit` field.
4. A real end-to-end: one `export --out <scratch>` run, the `ls -R` of the destination, and the
   manifest's `file_count` + archive sha.
5. A plain-text list of exactly which files you changed and why. No other file touched.

Do not create commits (there is no git here). Write your final summary as plain text at the end.
