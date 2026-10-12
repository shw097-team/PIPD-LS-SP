# Bounded writer brief — FAR adjudication implementation (S4POST round)

You are a **bounded writer**. You may modify ONLY the files listed under "Allowed write set". Anything
else — `skills/**`, `src/**`, `schemas/**`, `dist/**`, `.hgk/artifacts/**`, any release asset, any
other test — is forbidden. If you believe a change outside the set is required, stop and say so in
your final report instead of making it.

## Why this round exists

A prior adjudication round (FAR) decided four items. The owner authorised the three "low-resistance,
high-necessity" ones. You implement exactly those; you do not re-decide them.

- **F-020-A / F-021-A (ADOPT)** a digest checker must first establish *which bytes* a recorded digest
  was computed over, then classify each mismatch by basis, and only fail under a strict flag when a
  mismatch is genuinely unexplained.
- **F-024-A (ADOPT, no behaviour change)** candidate-ancestry checks stay **report-only**: a
  non-ancestor candidate must be reported, never fail the run.
- **F-023-A (ADOPT)** the execute-lane model entitlement must be probed before a long run: a two-turn
  tool-call probe, recorded as a receipt with declared-versus-actual model, and a typed refusal when
  the second turn fails. Do **not** patch any adapter in this repo.

## Allowed write set

- `tools/verify_evidence_digests.py` (modify)
- `tests/test_verify_evidence_digests_basis.py` (new)
- `tools/model_eligibility_probe.py` (new)
- `tests/test_model_eligibility_probe.py` (new)
- `docs/FAR_S4POST_ADJUDICATION_2026-10-12.md` (new)

## Required behaviour

1. **Basis-aware classification** in `tools/verify_evidence_digests.py`.
   For every manifest entry, compare the recorded digest against these bases and record the first one
   that matches: `disk`, `crlf_disk`, `head_blob`, `crlf_head_blob`, `candidate_blob`,
   `crlf_candidate_blob`, else `unexplained`. "crlf" means the byte sequence with lone LF expanded to
   CRLF (and, for the reverse direction, CRLF collapsed to LF) before hashing; implement both
   directions if the recorded digest can only be produced that way, and say in the docstring exactly
   which transformations you implemented. The sealed candidate commit/tree, when a sibling seal exists,
   must be read from it — do not hard-code a candidate.
   CLI contract: default run prints a human report and **exits 0**; `--strict` exits non-zero **only**
   when at least one entry is `unexplained`; `--json` prints exactly
   `{"checked":N,"explained":M,"unexplained":K,"basis_counts":{...}}`. Existing flags and the existing
   output the current tests read must keep working — those tests are already in the tree and must still
   pass (`python -m unittest tests.test_tooling_executes` and any test naming this tool).
2. **Ancestry stays report-only.** Add a test that feeds a non-ancestor candidate head and asserts the
   run exits 0 without `--strict` while the report still names the non-ancestor value. Failing the run
   on a non-ancestor is a regression, not a feature.
3. **`tools/model_eligibility_probe.py`.** Given `--base-url` and `--model`, perform a **two-turn**
   tool-call probe against an OpenAI-compatible endpoint (first request may ask for a tool call; the
   second continues the conversation) and write a receipt JSON containing at minimum
   `{"declared_model":..., "observed_model":..., "turn1":"PASS|FAIL", "turn2":"PASS|FAIL",
   "eligible":true|false, "typed_reason":null|"<code>"}`. Exit 0 when both turns pass; exit 3 with a
   typed reason when the second turn fails for the known `reasoning_content` error class; exit 2 for
   transport/connection errors. Never print or store credentials or tokens.
4. **Tests.** `tests/test_model_eligibility_probe.py` must drive the probe against an in-process stub
   HTTP server built with the standard library only (`http.server`), covering: (a) both turns healthy →
   exit 0 and `eligible: true`; (b) second turn returns HTTP 400 with a `reasoning_content` error body →
   exit 3 and the typed reason recorded; (c) connection refused → exit 2. No network access to any real
   host; no sleeps longer than 1 second; total test runtime under 20 seconds.
5. **`docs/FAR_S4POST_ADJUDICATION_2026-10-12.md`.** Record the four items, and state for each whether
   it is implemented here, deliberately not implemented (with the reason: ancestry change rejected as a
   no-op/downgrade; in-repo adapter patch rejected), or deferred. Include an explicit claim ceiling
   sentence: this is a candidate with local tests only, and no acceptance, release or adaptor-side
   evidence is claimed.

## Rules

- Change no existing test's expectations. If an existing test fails after your change, fix your code,
  not the test. Report the exact suite counts before and after.
- Keep the diff small and idiomatic to the repo's existing style (stdlib only, no new dependencies).
- Do not touch git history, do not commit, do not push, do not create tags, do not run anything that
  needs the network beyond `127.0.0.1`.
- Finish by running, and pasting the raw summary lines of:
  `python -m unittest discover -s tests -t .` and `python -m unittest tests.test_verify_evidence_digests_basis tests.test_model_eligibility_probe tests.test_tooling_executes`.
- Your final message: what you changed (file + why, one line each), the raw test summary lines, any
  test you had to adapt and why it is not a weakening, and anything you could not do.
