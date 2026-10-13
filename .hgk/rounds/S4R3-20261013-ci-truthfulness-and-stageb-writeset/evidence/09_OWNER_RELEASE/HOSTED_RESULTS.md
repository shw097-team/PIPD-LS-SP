# S4R3 — hosted results, read from the raw job logs

Everything here is copied from the GitHub job logs of the pushed candidates. The API's `conclusion`
is recorded next to the log's own lines, because the whole point of `S4R3-F001` is that the two can
disagree. Raw log digests are in `hosted_raw_log_digests.txt`; the selected extracts are committed
beside this file, and the full raw logs are retrievable at the run URLs below.

| branch | candidate | workflow | run | job | conclusion |
|---|---|---|---|---|---|
| `fix/s4r3-stage-a-ci-truthfulness-20261013` | `8cbe258` | `ci` | [38349126601](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38349126601) | `offline-gate` | **success** |
| `fix/s4r3-stage-a-ci-truthfulness-20261013` | `8cbe258` | `public-plugin-verify` | [38349126621](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38349126621) | `verify` | failure — see below |
| `feat/s4r3-stage-b-distribution-20261013` | `8481f29` | `ci` | [38349130157](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38349130157) | `offline-gate` | **success** |
| `feat/s4r3-stage-b-distribution-20261013` | `8481f29` | `public-plugin-verify` | [38349130092](https://github.com/shw097-team/PIPD-LS-SP/actions/runs/38349130092) | `verify` | **success** |

## Stage B `ci` — the suite, with its exit code actually attached

All ten steps ran; nothing was skipped:

```
  4 success  Install (declared dependencies only) and record what was resolved
  5 success  Full unittest suite (raw log)              -> Ran 572 tests in 45.392s / OK (skipped=6)
  6 success  Focused S4 repair / closure suites (raw log) -> Ran 108 tests in 6.645s / OK
  7 success  Build the wheel and exercise it in a clean venv with no source on PYTHONPATH
  8 success  Provenance gate is green before it is tested
  9 success  Negative — a mutated pack document must make the provenance gate fail
```

Each of those steps logs `set -euo pipefail` as its first line. At the frozen subject the same two
suite steps reported `FAILED (failures=11, skipped=6)` and `FAILED (failures=2)` while the job was
reported successful; that can no longer happen, because the step now carries the suite's own exit
code. `test_b4_wheel_mutation_installed_doctor_fails`, `test_two_builds_are_byte_identical` and the
package self-sufficiency tests are visible passing in the same log.

## Stage B `public-plugin-verify` — the repaired write-set gate, exercised on the runner

```
STAGE_B_BASE_SHA: 517d7a5d3f00935e1589908f456dfacea8fd8a74
GATE_SELF_TEST_OK: planted src/**, schemas/**, skills/** and dist/** are all refused
GATE_SELF_TEST_OK: planted stage-B artefacts are all allowed
WRITE_SET_CLEAN_AGAINST_517d7a5d3f00935e1589908f456dfacea8fd8a74
```

The steps that the frozen candidate skipped — the three-tool compile, the stdlib-only assertion, the
two new test modules, the full suite, and both negatives — all ran and passed on this run
(`Ran 47 tests / OK (skipped=1)` in the stdlib-only step). At the frozen subject this job failed on
`UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/verify_evidence_digests.py` and skipped everything after it.

## Why the Stage A branch's `public-plugin-verify` is red — and why that is the finding, not a repair failure

The Stage A branch does not contain the Stage B gate repair; that repair is a Stage B write under the
blueprint's allowlist. So the Stage A run executed the **pre-repair** gate, which measured
`main...HEAD`, and its log lists exactly the F002 symptom:

```
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .github/workflows/ci.yml
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: pyproject.toml
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: examples/first-run/run.ps1
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/S4R3-.../evidence/...
UPGRADE_WROTE_FROZEN_PATH: schemas/PI-PKG.schema.json
```

Those are Stage A's own legitimate source repairs being attributed to a Stage B upgrade. A Stage B
gate has no business judging a Stage A change set; the correct vehicle for the repaired gate is the
Stage B branch, and that run is green above. Recorded as an explained non-applicability, not as a
pass and not as a new defect: it is a reproduction of `S4R3-F002` on the pre-repair file.
