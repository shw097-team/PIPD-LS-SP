# Tasks

## S1 — preflight
- [x] 1.1 Implement `tools/preflight_check.py` with checks: python/suite, git HEAD+dirty, disk, docker, codex binary, codex sandbox capability, model pinning/`CONFIG_DRIFT`, loopback services, optional suite baseline
- [x] 1.2 Emit `PREFLIGHT.json` (`PIPD-PREFLIGHT/1`) and a compact table; non-zero exit on any FAIL
- [x] 1.3 `tests/test_preflight_check.py`: exit-code mapping, disk boundary, HEAD/dirty match+mismatch+absent, config drift, schema keys, table rendering, no-literal-credential negative test

## S2 — verifier envelope
- [x] 2.1 Implement `tools/round_envelope.py` (`init` / `snapshot` / `verify`, schema `PIPD-ROUND-ENVELOPE/1`)
- [x] 2.2 Three-way delta classification with allow-rules; mandated addition is not drift
- [x] 2.3 Refuse `--dst` inside `--src` and `--scratch` inside either tree
- [x] 2.4 `tests/test_round_envelope.py`: classification, allow-rules, mandated-addition case, refusals, schema

## S3 — round self-scan
- [x] 3.1 Implement `tools/round_selfscan.py` (fragment-assembled credential patterns, deny-list subprocess fold-in, redacted excerpts, schema `PIPD-ROUND-SELFSCAN/1`)
- [x] 3.2 Non-zero exit on HIT; ignore binary and `.git`; cap per-file size
- [x] 3.3 `tests/test_round_selfscan.py`: detection from fragments, clean pass, binary skip, size cap, redaction, stub deny-scan integration, no-literal-credential negative test

## Round integration
- [x] 4.1 Host acceptance: `python -B -m unittest discover -s tests -q` stays green and grows by the new tests only
- [x] 4.2 Run S1 on the round root and attach `PREFLIGHT.json` as round evidence
- [x] 4.3 Run S3 over the round's own new text and attach the self-scan verdict
- [ ] 4.4 Round-3 independent acceptance (unfinished R4 item) inside the S2 envelope with the checker model pinned explicitly
- [ ] 4.5 Record the route evidence: KANBAN board + SWARM graph, GSTACK role-map route check, this OpenSpec change (`openspec validate --strict`)
- [ ] 4.6 Fold verdicts into the evidence master and the checkpoint; keep `ClaimCeiling = CANDIDATE_ONLY`

## Evidence (as of 2026-10-09, host-verified)
- H1 `tools/preflight_check.py` + 35 tests OK; live verdict PASS/exit 0 (`H1/raw/PREFLIGHT.json`); it recorded the real
  substrate: docker PASS (daemon back), codex_sandbox WARN `SANDBOX_HELPER_BROKEN`, model_pinning PASS, loopback WARN.
- H2 `tools/round_envelope.py` + 11 tests OK; end-to-end CLEAN/DRIFT classification proven, mandated addition is not drift.
  OPEN DEFECT `H2-DEFECT-01` (MSYS-style `--dst` taken as a relative `\c\...` path; deep target then hits MAX_PATH) —
  recorded in `.hgk/rounds/R4-20261009-focused-repair/H2/raw/H2_DEFECT_01.json`, repair deferred so the frozen
  verification subject stays byte-identical.
- H3 `tools/round_selfscan.py` + 10 tests OK; live run over this round's own text found a residual `WRITER_USAGE` in
  `W10/raw/BRIEF.md` (only the `.txt` had been reworded) → data-plane reword (4 literals → 0), gate untouched,
  `deny_list_scan` back to PASS. This is the S3 promise demonstrated on the round itself.
- Host acceptance in a CLEAN env: `env -u PYTHONPATH -u PYTHONHOME python -m unittest discover -s tests -q`
  → Ran 244 tests / OK (baseline 188 + 56 new).
- Finding: the same suite reads 240 / FAILED(errors=1) under a shell that exports PYTHONPATH to the Hermes runtime,
  because that path carries its own `tools` package which shadows `PIPD/tools` for `tests/test_spec_del_crosswalk.py`.
  Environment contamination, not a product regression — the class S1 exists to surface.
