# A false green this round produced, and what was changed so it cannot recur

Written by the executor of this round. It is here because the round's whole subject is CI that reported
green while the suite was red, and this round managed to add a *new* instance of the same class before
catching it. Naming it is cheaper than leaving a reader to find it later.

## What happened

The F006 repair added a step to `.github/workflows/ci.yml`:

```
- name: The installed wheel resolves its OWN contract registry (S4R3-F006)
  run: |
    set -euo pipefail
    python - <<'PY'
    ...
    families = doc.get("families")
    assert isinstance(families, dict) and len(families) == 19, (
        f"expected the 19 declared families from the packaged registry, got {families!r}")
    PY
```

`workspace.doctor` reports `families` as the family **count** (an `int`), not as the family list. The
assertion was therefore false for a reason that had nothing to do with the product, and the step failed.
The hosted run said:

```
AssertionError: expected the 19 declared families from the packaged registry, got 19
##[error]Process completed with exit code 1.
```

The wheel, the registry and the repair were all fine. The **gate** was wrong. The local test suite was
green throughout, because the local test asserted the same property against a different source
(`registry.load_registry()` returns a dict) — the two assertions were never the same assertion, and only
one of them was executed anywhere.

## Why it survived local verification

Nothing local ran the CI step. The step's logic existed in exactly one place, inside a YAML heredoc, and
that place is only ever executed by GitHub. A gate that cannot be executed on a workstation cannot be
falsified on a workstation, so its first honest execution was a red hosted run — the same shape as
S4R3-F001, which this round was repairing.

## What changed

1. The assertions moved to `tools/verify_installed_wheel_registry.py`. CI calls the tool; the local test
   suite calls the same tool, with the real document and with mutated copies.
2. `tests/test_standard_wheel_schemas.py` gained `InstalledRegistryGateTests`, which runs the tool as a
   subprocess against the **real** doctor document produced by the built wheel (asserting the summary
   names `mode=INSTALLED families=19`) and against six mutations: a `families` **mapping** (the exact
   error above), a boolean count, a wrong count, `mode=SOURCE`, `verdict=FAIL`, and a resolution path
   pointing back into the checkout. Each must exit non-zero with its own typed code.
3. The gate gained a check the inline version never had: `mode=INSTALLED` alone does not prove the
   schemas came from the wheel, so the resolved path is now required **not** to be inside the checkout
   (`--deny-prefix "$GITHUB_WORKSPACE"`). The hosted log now prints where the registry actually
   resolved:

   ```
   installed-wheel contract registry: mode=INSTALLED families=19 path=/home/runner/work/_temp/wheelvenv/lib/python3.11/site-packages/pipd_ls_sp/schemas
   ```

4. The same discipline was applied to the write-set gate: `scripts/run_writeset_gate_locally.py`
   extracts the step from the workflow file and executes it in each worktree, so the gate that decides
   this round's scope was run locally before it was pushed. Its receipt is in
   `WRITE_SET_GATE_LOCAL_AND_CI.txt`.

## Claim ceiling for this note

This is a self-report by the party that introduced the defect. It is evidence that the failure was
found and that the gate was made locally falsifiable; it is **not** an independent verification that
either gate is now correct, and it does not raise any of the round's flags.
