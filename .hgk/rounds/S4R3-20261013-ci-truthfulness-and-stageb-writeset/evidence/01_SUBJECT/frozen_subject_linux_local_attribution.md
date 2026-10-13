# Attribution of the frozen-subject local Linux baseline

`evidence/03_CI_TEST/frozen_subject_linux_local_full_baseline.log` — `Ran 572 tests in 35.020s`,
**`FAILED (failures=4, skipped=10)`**, 4 FAIL, 0 ERROR.

## Why this receipt can be attributed to the frozen subject and not to the repair

The run left no commit of its own, so the subject was established from the clone's own reflog
rather than from the file name:

```
e71fee6 HEAD@{2026-10-13 12:32:49 +0800}: clone: from /mnt/c/Projects/Agent_Workspace/PIPD
517d7a5 HEAD@{2026-10-13 12:44:30 +0800}: checkout: moving from feat/s4post-triple-upgrade-20261013-r3
                                              to FETCH_HEAD
```

* `linux_full_baseline.log` mtime: **12:33:35** — 11 minutes *before* the checkout to the Stage A
  candidate `517d7a5` at 12:44:30. The only commit present at that moment was the frozen subject
  `e71fee6`.
* The Stage A run of the identical command is a separate file, `linux_after_full.log`
  (mtime 12:45:25, after the checkout): `Ran 572 tests in 41.888s / OK (skipped=10)`,
  `EXIT_FULL=0`.

So the same command, the same interpreter, the same checkout directory, before and after: 4
failures, then 0.

## The four failures are four of this round's seven root causes

```
FAIL: test_repair_subject_must_also_be_inside_the_authorised_root ... (subject='C:/Windows/system32/x.dll')   -> RC-2
FAIL: test_permission_bits_are_set_on_run_sh (tests.test_s4ext_first_run_portable)                             -> RC-4
FAIL: test_cli_smoke_runs (tests.test_tooling_executes)                                                        -> RC-6
FAIL: test_symlinked_destination_refused_and_target_byte_identical (tests.test_web_fallback)                   -> RC-7
```

The other three root causes cannot fire in this environment, which is why the count is 4 and not 7:
RC-1 is a property of the CI pipeline (a `tee` swallowing an exit status), not of the suite; RC-5 is
the Windows-only `run.ps1` path; and RC-3 (the six skill-contract failures) needs PyYAML to be
*absent* — this interpreter has it, which is exactly why the round also ran the explicit
`TOOL_MISSING` negative with PyYAML blocked on `PYTHONPATH`
(`evidence/03_CI_TEST/yaml_absent_negative.log`).

## Skip sets differ per environment — read the denominators with this in mind

| environment | Ran | skipped | what is skipped |
|---|---|---|---|
| frozen subject, local Linux (this file) | 572 | 10 | includes the two `test_installed_*` tests, which skip with `pip unavailable in test interpreter` |
| Stage A, local Linux | 572 | 10 | same |
| frozen subject, local Windows | 572 | 4 | |
| Stage A, local Windows | 572 | 4 | |
| Stage B, hosted Linux | 572 | 6 | |

**Consequence for claim ceilings:** "green on local Linux" does **not** cover the installed-package
tests — that interpreter has no `pip`, so `test_installed_package_is_self_sufficient` and
`test_installed_doctor_diagnoses_installed_schema_surface` are skipped there. The hosted runner is
the only environment in this round where those two actually execute, and it is precisely there that
`S4R3-F006` shows the installed wheel failing to resolve its schemas surface. A green local run
therefore says nothing at all about the wheel being installable.
