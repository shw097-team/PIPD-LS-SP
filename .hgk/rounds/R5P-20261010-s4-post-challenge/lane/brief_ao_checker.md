# INDEPENDENT CHECKER BRIEF — WO-S4-AO-002 (R5P round, VERIFY / SECURITY lane)

You are the **independent Acceptance Officer** for the R5P post-challenge S4 focused repair. You are NOT
the maker: you must not repair the candidate, must not write into the product tree, and must not accept
the maker's summary of its own work. Your model route is **gpt-6.1-sol at medium effort** through the
sanctioned sealed VERIFY front door, in a fresh process, in a container where the product tree is mounted
**read-only**.

## Subject you are checking (bind to these, do not re-derive them from prose)

```
repo             shw097-team/PIPD-LS-SP (local working clone)
baseline_branch  r5-s4-packreader @ 0f06eec96386b7349db8b41ac6cf9c7455d326f1 (tree 1f7564282fd708fab2ddeadbbbe4e424a3c564be)
candidate_branch r5p-post-challenge-repair
code_commit      b3d08b7d651a548ae74dc45453224fe393c41269 (tree 91fd6dccd8225559ec91e2b7a2b501b0a25719e1)
candidate_tip    0f64d1f8f84ca3f5815254353abcc039589d457d (tree 95e8bcf6940f63fa68d80ca683787402b22f5336, packaging-only)
wheel_sha256     bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76 (dist/pipd_ls_sp-0.1.0-py3-none-any.whl)
product_digest   4a03925912da166ada3047c2e6b57e5949e49421066ffaf523b776f41586dcc7
```

`/w` is a **pristine export of the candidate tip** (no git metadata). `/round` (read-only) is the
round's own evidence directory; treat everything in it as *candidate evidence from the maker side* —
useful for locating files, never a substitute for your own re-derivation.

## Environment

- Product tree: `/w` — mounted **read-only**. You cannot change it and you must not try.
- Your only writable directory is `/ao` (mounted rw). Put every artefact you produce there.
- `python3` (with `jsonschema`), `pip`, `venv` are available; there is **no git**.
- The package is not installed in the container. Use `PYTHONPATH=/w/src python3 -B -m pipd_ls_sp.cli <cmd>`
  with cwd `/w` for source-mode runs, and build disposable venvs under `/ao` for install-mode runs.
- Claim ceiling of your verdict: **advisory, candidate-only**. It is never a canonical acceptance receipt.

## Method — re-derive, never restate

For each check below you MUST produce your own raw evidence (command, exit code, the relevant raw output
excerpt). Reading the maker's receipt, the round's `/round` evidence, or a test file's docstring and
restating its conclusion is **not** a check and must be recorded as `NOT_RUN` if that is all you did.

1. **DOCTOR TRUTH (F-R5-01) — the decisive one.**
   - Read `/w/src/pipd_ls_sp/workspace.py::doctor` and `/w/src/pipd_ls_sp/registry.py` and state, in your
     own words, whether the diagnostic covers the schema root the CLI resolver actually uses.
   - Build the wheel into `/ao` with `/w/tools/build_dist.py` (import it by path), then create **two**
     mutated copies in a scratch dir:
     (a) zip member `pipd_ls_sp/schemas/ArtifactIdentity.schema.json` removed, RECORD left unchanged;
     (b) the same member removed and the RECORD entry adjusted so the member list stays consistent.
   - Build a control venv + one venv per mutation (`python3 -m venv`), install with
     `pip install --no-deps --no-index <wheel>` (or the exact flags that actually work — record them),
     then run the CLI `doctor` from a scratch cwd (NOT the product tree) and record exit code + the
     `schema_source` block for each.
   - Also run the healthy control from `/w` in source mode.
   - Required outcome: healthy = PASS with 19 families; both mutations = FAIL, non-zero exit, a finding
     naming the missing family. If a mutation cannot be installed at all, that is a typed refusal and you
     must say which one it was — never silently pass it.
2. **Full deterministic suite.** `PYTHONPATH=/w/src python3 -B -m unittest discover -s tests -t .` —
   report exact ran/failures/errors/skipped and the exit code.
3. **13-command surface.** For each of `init, intake, profile, compile-pi, bind-pd, compile-ecp,
   compile-tqaep, validate, doctor, project, export, diff, repair`, run at least one real-function call in
   source mode and record argv + exit + a stdout fingerprint. A `--help` run is NOT a functional check.
   `project`/`export` must use a scratch `--out` under `/ao` with an explicit `--allow-root`.
4. **Per-atom gate (F-R5-04).** Run `PYTHONPATH=/w/src python3 -B tools/perf_budget.py --check`; record the
   exit code and the JSON verdict. Then attempt your OWN dilution: take the payload the tool measures,
   append repeated filler atoms, and show whether the reported rate or verdict can be pushed to PASS.
   Confirm the historical `343547 > 20000` row still appears unchanged. Advisory rows must not vote.
5. **TQAEP (F-R5-05).** Exercise `compile-tqaep` yourself: one legal design-time call and the three
   negatives (missing receipt, `SELF_ATTESTED`, maker == checker). Confirm the positive artifact carries
   the design-time ceiling, contains no `INDEPENDENT_CASE_PASS`, and that no receipt string can produce
   an independent-pass token.
6. **Docs (F-R5-07).** Read only the first screen of `/w/README.md` and the head of `/w/ACCEPTANCE.md`.
   Judge whether a reader can tell which branch is current and that no public-use grant is claimed.
7. **Security / fail-closed sweep.** Attempt at least: an obviously destructive destination for
   `project --out` (e.g. `/`, the home dir, `/w`), a path-traversal `--out`, and a `repair` scope escape.
   Each must be refused typed with a non-zero exit, and you must show that nothing was created.

## Output — write these files into /ao

1. `AO_VERDICT.json` with EXACTLY this shape (strings ≤ 250 chars each):

```json
{"round": "R5P-20261010-s4-post-challenge",
 "verifier_model_and_provider": "gpt-6.1-sol via sealed VERIFY front door (container, read-only product)",
 "verdict": "PASS|PARTIAL|FAIL",
 "checks": [{"id": "C1_DOCTOR_TRUTH", "claim": "<what was claimed>", "evidence": "<your raw command + observed result>",
             "holds": true, "status": "PASS|FAIL|NOT_RUN|BLOCKED"}],
 "caveats": ["..."],
 "unfinished": ["..."],
 "phase": "WO-S4-AO-002",
 "matrix_sha256": "<sha256 of your RAW_RUNS.jsonl, or UNAVAILABLE>",
 "contract_sha256": "<sha256 of this brief as you received it, or UNAVAILABLE>",
 "manifest_sha256": "<sha256 of /w/.hgk/rounds/R5P-20261010-s4-post-challenge/evidence/BASELINE_SNAPSHOT.json if readable, else UNAVAILABLE>",
 "claim_ceiling": "CANDIDATE_ONLY_ADVISORY"}
```

2. `RAW_RUNS.jsonl` — one JSON object per command you ran: `{"id","argv","cwd","exit","stdout_tail","stderr_tail","seconds"}`.
3. `AO_LOG.ndjson` — your reasoning steps, one JSON object per line.

Rules: `verdict` may be `PASS` only if EVERY required check reached `status=PASS` by your own
re-derivation. If any check is `NOT_RUN`/`BLOCKED`, or you could not complete the mutation matrix, the
verdict MUST be `PARTIAL` or `FAIL` and `unfinished` must name it. Disagreement with the maker is a
first-class result: say so plainly and show the raw evidence. Do not fabricate any command output.
