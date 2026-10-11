# WO-S4-CONTRACT-HARDEN-03 (S4-R2) — type the residual ProfileBinding contract fields

You are a bounded writer. Work only inside `C:/Projects/Agent_Workspace/PIPD-postrelease-wt`.

## Write-set (nothing else, do not create other files)
- `schemas/ProfileBinding.schema.json`
- `tests/test_s4r2_affected_only.py` (new)

Do NOT touch `README.md`, `examples/**`, `src/pipd_ls_sp/profiles.py`, or any other schema. Another
writer is editing `README.md` and `examples/first-run/**` at the same time; a collision destroys both.

## Interpreter (pin it by absolute path, it has jsonschema)
`C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
Run tests as
`PYTHONPATH=C:/Projects/Agent_Workspace/PIPD-postrelease-wt/src <python> -m unittest <module> -v`.

## Problem being fixed
The reaudit found the identity/trace fields untyped and the previous round typed the universal identity
fields and the PI trace. Reconciliation then found a residual (`F-S4R2-NEW-01`): in
`schemas/ProfileBinding.schema.json` these properties are still the empty schema `{}` and therefore
accept anything:

```
profile, axes, vetoes, artifact_depth, assurance   →  all currently {}
```

Measured counterexamples on the current tree — all of these are ACCEPTED today by
`pipd_ls_sp.validate.validate_record(...)`, and each must become a typed refusal:
- `axes` as a plain string `"intent"`
- `axes` as a list containing a non-string, e.g. `["intent", 7]`
- `profile` as an integer `7`
- `vetoes` as a string `"none"`

## What to deliver

1. Type the five properties in `schemas/ProfileBinding.schema.json` — the MINIMUM that makes the four
   counterexamples above fail while every legal record still passes:
   - `axes`: an array of strings, each constrained to the real axis vocabulary. Read the real vocabulary
     from `src/pipd_ls_sp/profiles.py` (the `AXES` tuple) — use the REAL axis names, do not invent them.
     Decide and state whether duplicates are a schema-level refusal or stay a runtime refusal in
     `compute_profile()` (the runtime refusal already exists; do not remove it).
   - `profile`: string, constrained to the real profile names if the code defines a closed set.
   - `vetoes`: array (of the real veto shape the code emits — read `profiles.py`).
   - `artifact_depth`: string, matching the real values emitted by `profiles.py`.
   - `assurance`: string, matching the real values (`LITE` / `STANDARD` / `ASSURED`) emitted by
     `profiles.py`.
   Follow the exact conventions already used by the sibling schemas — read one already-hardened schema
   first and match its style (`type`, `minLength`, `pattern`, `enum`, `additionalProperties`). Do not
   add a new schema family and do not change the schema's `$id`.

2. `tests/test_s4r2_affected_only.py` — `unittest`, matching the existing test style, asserting:
   - NEG: each of the four counterexamples above is REFUSED, naming the offending field
   - POS: a legal `ProfileBinding` record (take a real one the code emits — build it by calling the
     code, do not hand-write a guess) still passes
   - REG: the 19-schema exact set is still exactly 19 and unchanged in count
   - REG: the existing profile tests still pass (`tests/test_s0_contracts.py`,
     `tests/test_postrelease_contract_hardening.py` if present)

3. Run, and report, BOTH:
   - your new test module
   - the project's affected regression: `python -m unittest discover -s tests -t .` from the repo root
     with `PYTHONPATH=<repo>/src`. NOTE: the base commit already reports
     `Ran 389 tests ... OK (skipped=3)`; if you see MORE failures than the base, you broke something —
     investigate before reporting.

## Honesty rules (these override any instinct to look finished)
- If typing a field breaks a legal existing fixture, do NOT weaken the schema to make the test green.
  Report the collision: which fixture, which field, why the fixture was legal under the old contract.
- Do not change `src/**` to make a schema pass. The schema is the contract; the runtime already refuses
  duplicates.
- Do not add `additionalProperties: false` to `ProfileBinding` — that is a larger change than this
  finding asks for and would break legal extension. State that you deliberately did not.

## Required final report (print it, keep it short)
- The diff summary of `ProfileBinding.schema.json` (which properties, which types).
- The four counterexamples: command, result, message.
- The test command and its result line (`Ran N tests ... OK`).
- The full-suite result line and the base figure you compared it to.
- Anything you could NOT do, and why.
