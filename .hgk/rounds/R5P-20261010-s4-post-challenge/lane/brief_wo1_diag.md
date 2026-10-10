# BOUNDED WRITER BRIEF — WO-S4-DIAG-001 (R5P round, EXECUTE lane)

You are the **bounded Codex writer** for one Work Order of the R5P post-challenge S4 focused repair.
Orchestrator: Hermes (PLAN). Control plane: HG-KSEOS. Your model route: opencode-go/deepseek-v4.1-flash
through the sanctioned sealed EXECUTE front door. Claim ceiling of everything you produce: **CANDIDATE /
LOCAL_TESTED only** — never independent acceptance, never release.

## Execution environment

You run INSIDE a disposable Linux container with a mount allowlist (the container is the write-scope
boundary):

- Product repo mounted read-write at `/w` — this is your ONLY writable tree.
- The container has `codex-cli`, `python3` (with `jsonschema`), `pip`, and `venv`, and **no git**.
- Run every command with cwd `/w`.
- The repository is NOT pip-installed in the container. Import the package from the checkout by
  exporting `PYTHONPATH=/w/src` for every python invocation, e.g.
  `PYTHONPATH=/w/src python3 -B -m pipd_ls_sp.cli doctor`
  (the CLI's module entry point is `pipd_ls_sp.cli`; the console script `pipd` maps to
  `pipd_ls_sp.cli:main`).

## Write scope (HARD — do not create, edit or delete anything else)

Allowed to modify/create ONLY:
- `src/pipd_ls_sp/workspace.py`
- `src/pipd_ls_sp/registry.py`
- `tests/test_wheel_distribution.py` (augment only)
- `tests/test_doctor_schema_truth.py` (new file, if you want a dedicated test)
- `src/pipd_ls_sp/cli.py` — ONLY if strictly required to make `doctor` exit non-zero on FAIL
Everything else — `schemas/`, `dist/`, `tools/`, `README.md`, `.hgk/` — is OUT OF SCOPE for this Work Order.
Do not run `git commit`, `git push`, `pip install` into the product tree (installing into a disposable venv under /tmp is allowed and expected), or any destructive command.

## The defect (verified by an external challenge, F-R5-01)

`workspace.doctor(root)` currently does:

```python
reg = registry.load_registry(root / "schemas")     # workspace-local convention only
... for f in reg["families"]: json.loads((root / "schemas" / f"{f['contract']}.schema.json").read_text())
```

But the CLI's real resource resolver is `registry._resolve_schemas_dir()`, whose order is
`$PIPD_SCHEMAS_DIR` → packaged copy inside the installed wheel (`importlib.resources.files("pipd_ls_sp")/"schemas"`)
→ `<repo>/schemas` source fallback. Consequence: install a wheel whose packaged `schemas/` is missing
`ArtifactIdentity.schema.json`, run `pipd doctor` from a healthy workspace, and it prints `verdict=PASS`.
The low-level `registry.load_registry()` does refuse that wheel; the user-facing diagnostic never asks it.

## Required change

1. In `registry.py` add a public reporting function, e.g.

   ```python
   def describe_schemas_source() -> dict[str, Any]:
       """Return {"mode": "OVERRIDE"|"INSTALLED"|"SOURCE"|"NONE", "path": str, "tried": [str, ...]}"""
   ```

   - `OVERRIDE` when `$PIPD_SCHEMAS_DIR` was selected, `INSTALLED` when the packaged copy was selected,
     `SOURCE` when the source-tree fallback was selected, `NONE` when nothing resolved.
   - Reuse the existing `_candidate_schemas_dirs()` / resolution logic rather than duplicating the order.
   - Keep `_resolve_schemas_dir()` semantics unchanged (do not reorder the candidates).

2. In `workspace.py` make `doctor(root)` diagnose BOTH surfaces and AND the verdict:

   - keep the existing workspace-local checks on `<root>/schemas` when it exists;
   - additionally validate the **resolved** root (`describe_schemas_source()`):
     exact member set = `registry.json` + the 19 `<Family>.schema.json` names from `SOURCE_ORDER`;
     each present, parseable, `$schema` containing `2020-12`, and the registry-declared required fields
     enforced by the schema;
   - a missing/unreadable/invalid member at the resolved root is a finding that NAMES the missing family
     and the resolved path, with `verdict = "FAIL"`;
   - the returned dict must carry a new key `schema_source` = the `describe_schemas_source()` payload
     (mode, path, tried) so the operator can see which surface was inspected;
   - never silently fall back to another schemas copy to produce a PASS.

3. `pipd doctor` must exit non-zero when `verdict == "FAIL"` (check `cli.py`: `main()` returns
   `0 if result.get("verdict","PASS") != "FAIL" else 1` — confirm this is the live path for `doctor`
   and fix it only if it is not).

4. Tests: extend `tests/test_wheel_distribution.py` (and/or add `tests/test_doctor_schema_truth.py`) with
   a real mutation test that does NOT touch the repo's own `dist/` wheel:
   - build the wheel into a temp dir with `tools/build_dist.py` (import it by path like the existing test does),
   - copy the wheel, rewrite its zip removing `pipd_ls_sp/schemas/ArtifactIdentity.schema.json`,
     producing TWO variants: (B4a) the RECORD member left unchanged, and (B4b) the RECORD member adjusted
     so the member list stays consistent;
   - install each variant into its own disposable `venv` created under a temp dir (`python3 -m venv`), install the healthy wheel as the control, then run
     `<venv>/bin/python -m pipd_ls_sp.cli doctor` (discover the real entry point from `pyproject.toml` /
     `cli.py`; if the console script is the only entry, run the module form) from a scratch cwd;
   - assert: healthy control → `verdict PASS`, 19 families, exit 0; B4a and B4b → `verdict FAIL`,
     a finding naming `ArtifactIdentity`, exit != 0;
   - if a variant cannot be installed at all, record the typed refusal instead of skipping silently —
     a SKIP is only acceptable with an explicit printed reason and must never be counted as PASS.

## Acceptance evidence you MUST produce before you finish

Run these and paste the raw output into your final message:

1. `PYTHONPATH=/w/src python3 -B -m unittest discover -s tests -t .` (cwd = /w) — report the exact
   pass/fail/skip counts, not a paraphrase.
2. `PYTHONPATH=/w/src python3 -B -m unittest tests.test_wheel_distribution tests.test_doctor_schema_truth -v` (whichever exist).
3. A live demonstration of the BEFORE/AFTER difference on the B4b variant that shows exit code and stdout.
4. `PYTHONPATH=/w/src python3 -B -m pipd_ls_sp.cli doctor` from `/w` on the healthy source tree: exit code +
   the `schema_source` block.

## Output contract

Finish with a single fenced JSON block named `WO_DIAG_RECEIPT` containing:

```json
{"work_order": "WO-S4-DIAG-001",
 "files_changed": ["..."],
 "interpreter": "<absolute path used>",
 "unittest": {"ran": 0, "failures": 0, "errors": 0, "skipped": 0},
 "b4": {"B4a": {"exit": 1, "finding": "..."}, "B4b": {"exit": 1, "finding": "..."}},
 "healthy": {"exit": 0, "families": 19, "mode": "SOURCE"},
 "not_done": ["anything you could not do, with the reason"],
 "claim_ceiling": "CANDIDATE_ONLY"}
```

Be honest: if a step could not be completed, say so in `not_done` with the exact command and error.
Never invent output. Do not touch files outside the write scope.
