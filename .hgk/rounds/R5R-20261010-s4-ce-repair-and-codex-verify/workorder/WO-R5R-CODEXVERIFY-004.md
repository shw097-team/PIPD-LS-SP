# VERIFY brief — independent verification by the CODEX CLI (checker lane)

Round: `R5R-20261010-s4-ce-repair-and-codex-verify`
Requirement: `REQ-PIPD-R5R-CODEXVERIFY-004` / `WO-R5R-CODEXVERIFY-004`

You are the **Independent Acceptance Officer**. You did not build this. You must not edit, rebuild,
re-tag or republish anything. Your job is to find out whether the claims below are true, and to say
so plainly — including "I could not verify X".

## Environment

- Shell is git-bash (MSYS). **Native programs (python, git, curl) do not accept `/c/...` paths** —
  always pass `C:/...` forward-slash native paths.
- Write scratch files under
  `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/<your own subdir>`.
  Never under a bare `/tmp`.
- Python: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (3.11.x). `uv` is
  available if you prefer it for the clean venv.
- If `unset PYTHONPATH` is not done, an inherited `PYTHONPATH` can make `import pipd_ls_sp` resolve to
  the wrong tree. Always `unset PYTHONPATH` before running repo commands.
- Run Python as a single-line command with an absolute interpreter path, or write a `.py` file and run
  that. Do not use a heredoc piped into `python -`.

## Subject under test

- Repository: `C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt` (branch `r5r-ce-repair`)
- Distribution to install: `{{WHEEL_PATH}}`
- Its expected SHA256: `{{WHEEL_SHA256}}`
- Baseline for comparison: the already-published wheel
  `https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/pipd_ls_sp-0.1.0-py3-none-any.whl`
  (SHA256 `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60`)

## Claims to test — give PASS / FAIL / INCONCLUSIVE with the raw evidence for each

1. **The wheel installs for real.** Create a clean venv with no `PYTHONPATH`, from a working directory
   outside the repository, and install the subject wheel. Record the exact command and its exit code.
   Then run `python -m pipd_ls_sp.cli doctor`. It must exit 0 and report the schema source it loaded.

2. **PIPD-LS-SP actually runs.** Using only the installed package (not the source tree), execute the
   full design chain with your own inputs — `intake`, `compile-pi`, `bind-pd`, `compile-ecp`,
   `compile-tqaep` — and record every command, stdout and exit code. `bind-pd` needs a git repository;
   create your own scratch one. If any step cannot run, say exactly which and why, and what you tried.

3. **CE-1 is repaired.** From a directory that contains **no** `schemas/` directory, and with **no**
   `--root` argument, run `validate` against a bundle you assembled. It must reach a verdict using the
   schemas installed inside the package, and it must not fail with a missing-file error naming
   `<cwd>/schemas/PI-PKG.schema.json`. Then show that a directory whose `schemas/` contains
   `registry.json` still takes precedence when passed as `--root`.

4. **CE-2 is repaired.** Assemble a bundle from the four compilers' output **exactly as they emitted
   it — do not delete, rename or add any key**. `validate` must return `verdict == "PASS"` with four
   records checked and no findings. Record the raw bundle's key set so a reader can see you did not
   edit it. In particular `_profile_meta` must still be present in the PI-PKG member.

5. **The old behaviour is genuinely gone, not merely tolerated.** Demonstrate at least one of:
   corrupting an installed schema must still make `doctor`/`validate` fail closed with a typed message
   and no traceback; or a release-bound record whose body was edited without re-issuing `content_hash`
   must still be reported. A validator that passes everything is worse than one that fails.

6. **The published tag was not rewritten.** Confirm that
   `https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1` still resolves to release
   commit `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32` and that its published wheel still hashes to
   `c450dbef…`. State how you checked it.

7. **Real-world feasibility.** Say plainly whether a person who is not you could install and use this
   package today, based on what you actually did — including any step that required knowledge not
   present in the package's own documentation.

## Output

Write your full raw log (every command, stdout, stderr, exit code) to
`{{VERIFY_OUT}}/raw_transcript.txt`, and a JSON verdict to `{{VERIFY_OUT}}/verdict.json` with:

```json
{"overall": "PASS | FAIL | INCONCLUSIVE", "claims": [{"id": 1, "verdict": "...", "evidence": "..."}],
 "counterexamples": [], "what_i_did_not_verify": "...", "evaluator": "independent process; did not participate in the build"}
```

End your run with the literal line `VERDICT: PASS`, `VERDICT: FAIL` or `VERDICT: INCONCLUSIVE`, plus
`UNVERIFIED: <claim ids or NONE>` and `REASON: <one line>`. Your verdict is yours alone — do not
soften it to match what the maker expects, and do not claim a PASS for anything you did not run.
