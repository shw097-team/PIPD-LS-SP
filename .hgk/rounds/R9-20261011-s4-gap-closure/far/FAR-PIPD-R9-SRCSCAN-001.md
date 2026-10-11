# FAR-PIPD-R9-SRCSCAN-001 — scan THIS PROJECT'S OWN SOURCE, which the dependency audit never covered

Round `R9-20261011-s4-gap-closure`, obligation `REQ-PIPD-R9-SRCSCAN-001`.

## 1. The fact pattern

Round R7 recorded "pip-audit 2.10.1, 35 packages, 0 known vulnerabilities" — and in the same breath
recorded that **`pipd-ls-sp` was SKIPPED because it is not on PyPI**. That audit covered the declared
dependency closure only. Taken alone, "no known vulnerabilities" is a statement about other people's
code. Our own 11,439 lines had never been scanned.

## 2. What was run

`bandit` in a clean `uv` venv, over two surfaces separately so the result is attributable:

| surface | LOC | before |
|---|---|---|
| `src/` (the shipped runtime) | 3,499 | 0 HIGH, 0 MEDIUM, 8 LOW |
| `tools/` + `skills/` (round tooling + published skills) | 7,940 | **1 HIGH**, **2 MEDIUM**, 113 LOW |

## 3. The findings that mattered

- **HIGH `B202` — `tools/pi_dedup_check.py:103`**, `tarfile.extractall` with no member validation.
  Assessed honestly: the archive is produced by `git archive HEAD` from the local repo, so this is
  **defence in depth, not a live attack path** — git cannot itself emit a `..` member. It is still a
  real gap, because nothing in the code guaranteed that, and `extractall` is exactly the call whose
  member-selection semantics are version-dependent.
- **MEDIUM `B310` x2 — `tools/github_publish.py:45,59`**, `urlopen` without a scheme allow-list.

## 4. Adjudication and execution

**Fix by construction, not by suppression, wherever construction is available.**

For the HIGH, `extractall` is **gone entirely**. `_extract_archive_members()` walks `tf.getmembers()`
and writes each member by hand, refusing: an empty or `..`-bearing path, an absolute or drive-prefixed
name, any member that is not a regular file or directory (so no symlink, hardlink, device or FIFO can
be materialised), and any resolved target that escapes the destination.

For the two MEDIUMs, `_https_only()` validates the scheme and fails closed before the request opens.
A `# nosec B310` remains on the single site whose argument cannot be a literal, written next to the
guard that justifies it — a suppression that is *documented and bounded*, not a silence.

## 5. Verification — three independent instruments

1. **Scanner, re-run:** HIGH **0**, MEDIUM **0** (LOW 9, all subprocess-related and expected in a
   tooling tree; remaining classes B404/B603/B607).
2. **Functional test against a crafted archive** — the instrument that actually matters, because a
   quiet scanner proves nothing about behaviour:

   | crafted member | result |
   |---|---|
   | `../escape.txt` (traversal) | **REFUSED** — `TarError: unsafe member path refused` |
   | `/tmp/escape.txt` (absolute) | **REFUSED** — `TarError: unsafe member path refused` |
   | symlink pointing at `/etc/passwd` | **REFUSED** — `TarError: non-file member refused` |
   | `ok/a.txt` (benign nested file) | **EXTRACTED** — the fix does not break the real path |

   Nothing was written outside the destination and the destination's parent was not polluted.
3. **Both modules still compile and import** under `python -m py_compile` and a fresh import.

## 6. What this does NOT claim

- It is **not** a clean bill of health. Bandit is a pattern scanner: it cannot find logic errors,
  authorisation mistakes, or vulnerabilities nobody has written a rule for. **An empty finding list
  is a statement about the rule set, not about the code.**
- The LOW findings in `tools/` and `skills/` were counted, not individually triaged. Two `B105`
  hits are false positives on the string literals `'True'` and `'PASS'`.
- No secret-scanning tool was run over the source in this pass (history scanning was a separate R7
  activity with its own stated bounds).
- No lock file exists, so this says nothing about the versions a consumer will actually install.

**Claim ceiling:** `OWN_SOURCE_SCANNED_BANDIT_HIGH_AND_MEDIUM_ZERO_AFTER_REPAIR`.
