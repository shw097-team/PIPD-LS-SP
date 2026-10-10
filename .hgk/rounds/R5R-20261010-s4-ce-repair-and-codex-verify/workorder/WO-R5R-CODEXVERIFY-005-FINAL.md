# VERIFY brief 2 — re-verification after the checker's own counterexample was repaired

Round: `R5R-20261010-s4-ce-repair-and-codex-verify`
Requirement: `REQ-PIPD-R5R-CODEXVERIFY-005` / `WO-R5R-CODEXVERIFY-005`

You are the Independent Acceptance Officer again, in a fresh session. In your previous pass you
returned `VERDICT: FAIL` on claim 8 and filed the counterexample `CE-CODEX-TRACE-WIDENING`: adding
an undeclared `trace` key to a `PD-PKG`, `ECP` or `TQAEP` record returned `verdict=PASS` with no
findings, while the published validator rejected the same records. Claims 1-7 and 9 you passed.

The maker took your counterexample as a defect (it was not argued away) and a bounded writer has
since changed `src/pipd_ls_sp/validate.py` to close it. Your job is to decide whether it is
actually closed, and whether closing it broke anything you previously passed.

Do not soften your verdict to be agreeable, and do not accept the fix because the suite is green.
If the widening is still there in any form, say FAIL again.

## Subject under test (NEW artefact — the previous one is superseded)

- Repository: `C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt`, branch `r5r-ce-repair`
- Distribution: `C:/Projects/Agent_Workspace/PIPD-r5r-repair-wt/dist/pipd_ls_sp-0.1.0-py3-none-any.whl`
- Expected SHA256: `d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f`
- Superseded artefact you tested last time: sha256 `ca1f64e5…` (do not re-test it)
- Baseline for comparison, unchanged: published
  `https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.1/pipd_ls_sp-0.1.0-py3-none-any.whl`
  (`c450dbef…`)

## Environment

- git-bash (MSYS); native programs (python, git, curl) need `C:/...` forward-slash paths, never `/c/...`.
- Reuse your own scratch root if it still exists, or make a new one under
  `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/`.
- `unset PYTHONPATH` and `unset PYTHONHOME` before any repo or CLI command.
- Python: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.

## Claims

1. **The counterexample is closed.** Reproduce your EXACT fixture from last time: take the four
   compilers' own stdout, unedited, and separately add an undeclared `trace` (e.g.
   `{"undeclared": "silently accepted", "not_a_trace_list": true}`) to each of `PD-PKG`, `ECP` and
   `TQAEP`, leaving every other field and the original `content_hash` untouched. install the new
   wheel and run the installed `validate`. Each such bundle must now FAIL, and the findings must
   name `trace`. Report the raw output. If any of the three still passes, that is a FAIL.

2. **CE-2 is still repaired.** The same four-record bundle WITHOUT the added `trace` — PI-PKG still
   carrying `_profile_meta` — must still return `verdict=PASS`, `checked=4`, `findings=[]`.

3. **CE-1 is still repaired.** From your scratch cwd with no `schemas/` directory and no `--root`,
   `validate` must still reach a verdict via `schema_source.mode=INSTALLED`, and a `--root` whose
   `schemas/` carries a `registry.json` must still win.

4. **Nothing else regressed.** Re-check that these still fail closed: a record missing a required
   identity field; a record carrying an undeclared junk key that is not `_profile_meta`; a record
   whose body was edited without re-issuing `content_hash`. Also state whether the four-contract
   happy path and `doctor` still exit 0.

5. **The fix is narrow, not a re-widening.** Read the validator source in the new wheel and say
   plainly whether the change closed ONLY the `trace` hole, or whether it also started rejecting
   something legitimate that used to pass. In particular: is `_profile_meta` still tolerated on
   PI-PKG only because it is genuinely non-record, and would the same tolerance now also apply to a
   different contract if the pipeline ever emitted it there? Give your reasoning, not just the suite.

6. **The published release is still untouched.** `v0.1.0-preview.1` must still resolve to
   `cc9bf574c3b3f0f44ea615b5c67ae40d74efee32` with its wheel still hashing to `c450dbef…`.

## Output

Write the full raw log to `C:\Projects\Agent_Workspace\PIPD-r5r-repair-wt\.hgk\rounds\R5R-20261010-s4-ce-repair-and-codex-verify\verify-codex-2/raw_transcript.txt` and a JSON verdict to
`C:\Projects\Agent_Workspace\PIPD-r5r-repair-wt\.hgk\rounds\R5R-20261010-s4-ce-repair-and-codex-verify\verify-codex-2/verdict.json` shaped as:

```json
{"overall": "PASS | FAIL | INCONCLUSIVE",
 "claims": [{"id": 1, "verdict": "...", "evidence": "..."}],
 "counterexamples": [],
 "what_i_did_not_verify": "...",
 "evaluator": "independent process; did not participate in the build"}
```

End with `VERDICT: PASS`, `VERDICT: FAIL` or `VERDICT: INCONCLUSIVE`, then
`UNVERIFIED: <claim ids or NONE>` and `REASON: <one line>`.

Disclose in your verdict that you are the same checker lane which found this counterexample, and
that (a) you did not write the fix, (b) you are re-testing your own finding on a new artefact, and
(c) you have not verified anything outside the claims above.
