# R7 dependency vulnerability scan — result and its exact scope

Two attempts were made. Recorded because the first failed in a way that is easy to misread as a
clean run, and because the second has a scope limit that the headline "0 findings" does not carry.

## Attempt 1 — FAILED (not a result)

`uv venv --python 3.11 audit-venv` creates a virtual environment **without pip**, so the immediate
`./audit-venv/Scripts/python.exe -m pip install pip-audit` could not run:

```
No module named pip
pip-audit install exit=0
No module named pip_audit
```

The `exit=0` printed there is the exit code of the `echo`, not of the install — the install never
happened. **No audit result came from this run.** Superseded by attempt 2.

## Attempt 2 — COMPLETED

Environment: `uv venv --python 3.11`, then `uv pip install --python <venv> pip-audit` (which does not
depend on the venv having its own pip), then the published wheel installed into it.

- Scanner: **pip-audit 2.10.1**
- Audited: 35 packages resolved in that environment, **0 with known vulnerabilities**
- Stdout verdict: `No known vulnerabilities found`
- `audit_exit=0`

Machine-readable output: `evidence/scan_dependency.json`.

### Scope limit — the project's own package was NOT scanned

pip-audit reports, in the same output:

```
Name        Skip Reason
pipd-ls-sp  Dependency not found on PyPI and could not be audited: pipd-ls-sp (0.1.0)
```

So the scan covers the **dependency closure** and **not the project package itself**. The headline
"0 findings" must not be read as "the release was vulnerability-audited". A source-level audit of
`pipd_ls_sp` itself was **not** performed this round and is not claimed.

### Second scope limit — no lockfile

The declared dependency is `jsonschema>=4.0` (resolved to 4.26.0 for this audit). A `>=` floor means
the audited set is one resolution, not the set a future installer necessarily gets. This is the same
limitation recorded in `evidence/R7_CLOSURE_REPORT.md`.

### Third scope limit — the scan environment was synthetic

The scanned environment contains pip-audit's own dependencies alongside the release closure, so the
35-package count is the environment, not the shipped footprint. The release's own resolved closure is
`jsonschema` + `attrs`, `jsonschema-specifications`, `referencing`, `rpds-py`.
