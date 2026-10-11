# WO-S4-DOC-FIRSTUSE-01 (S4-R2) — a front page whose compiler walk-through is literally runnable

You are a bounded writer. Work only inside `C:/Projects/Agent_Workspace/PIPD-postrelease-wt`.

## Write-set (nothing else, do not create other files)
- `README.md`
- `examples/first-run/**` (new directory)
- `tests/test_first_run_examples.py` (new)

Do NOT touch `src/**`, `schemas/**`, `dist/**`, or any other test file. Another writer is editing
`schemas/ProfileBinding.schema.json` and its tests at the same time; a collision there destroys both.

## Interpreter (pin it by absolute path, it has jsonschema)
`C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
Run the CLI as `python -m pipd_ls_sp.cli ...` with `PYTHONPATH=C:/Projects/Agent_Workspace/PIPD-postrelease-wt/src`.
NEVER use a bare `python` or the `py` launcher.

## Problem being fixed
The reaudit finding `F-S4R2-05` is that the README's compiler section shows placeholders
(`<your goal>`, `<a locator that EXISTS>`, `<path to an intent card>`, `<path to the assembled bundle>`,
`<phase>`) in a block a reader is expected to copy. A reader cannot run it. Line ~112 of the current
README is the block to replace.

## What to deliver

1. **`examples/first-run/` — a real, minimal, self-contained fixture** that the documented commands
   actually use. It must contain real input files checked into the tree (for example a small
   `source.txt` holding the normative clauses, and an `intent.json`). Keep it small: no PII, no
   secrets, no upstream document bodies. Everything the walk-through references must exist in this
   directory — zero placeholders.

2. **A real transcript.** Actually execute, in a scratch directory OUTSIDE the repo, the full chain
   the CLI supports:
   `intake` → `compile-pi` → `bind-pd` → `compile-ecp` → `compile-tqaep` → `validate`
   (check each verb's real flags with `--help` first — `--root` is a GLOBAL option that goes BEFORE the
   subcommand). Capture the REAL stdout/stderr and the REAL artefact digests. Then run the whole chain
   a SECOND time in a fresh directory and confirm the produced digests are identical.

3. **`README.md`**: replace the placeholder block with exactly the commands you ran, using the
   `examples/first-run/` paths, so a reader can copy them literally. State the expected observable
   result of each step (a trace id, a digest, an exit code) — do not paste `<...>` tokens in a runnable
   block. Keep the section short. Also add `examples/` to the "What is in this tree" table if it is
   absent, and correct any statement that contradicts what you observed.

4. **`tests/test_first_run_examples.py`**: a test that drives the documented chain end to end and
   asserts (a) the positive run succeeds, (b) the second run reproduces the same digests, and (c) a
   NEGATIVE case fails — point a source locator at a path that does not exist and assert a typed
   non-zero refusal with no artefact written. Use `unittest`, match the style of the existing tests in
   `tests/`.

## Honesty rules (these override any instinct to look finished)
- If a verb's real flags differ from what the README assumed, fix the README — never invent a flag and
  never add a new CLI command.
- If the CLI genuinely cannot do a step, say so in the README as a known limitation and stop; do not
  fabricate a transcript.
- Every command you print in the README must be a command you actually ran, with the output you
  actually got.

## Required final report (print it, keep it short)
- The exact commands you ran (both passes) and their exit codes.
- The artefacts created and their sha256 digests, pass 1 vs pass 2.
- The negative case: the exact command, the exit code, and the first failure message.
- The test command you ran and its result line (`Ran N tests ... OK`).
- Anything you could NOT do, and why.
