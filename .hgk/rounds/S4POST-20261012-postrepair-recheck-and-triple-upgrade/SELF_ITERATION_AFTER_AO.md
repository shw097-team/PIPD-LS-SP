# Stage-B self-iteration after the independent acceptance challenge

Subject: the Stage-B candidate that was pushed as `feat/s4post-triple-upgrade-20261012-r2`.
Checker: independent acceptance officer lane, `gpt-6.1-sol` / provider `openai` / reasoning `medium`
(the declared checker model), reported in `verify/ao/AO_VERDICT_STAGEB.md`.

## Verdict of the challenge

`FAIL_CHALLENGE`. Not a claim about the whole upgrade: the officer confirmed the packaging and
fallback suites green, the write-set guard clean, and the pushed commit matching the local HEAD. It
blocked on three findings, and two of them were real defects rather than paperwork.

## Findings and what was done

| ID | Officer finding | Disposition | Evidence |
|---|---|---|---|
| `AO-01` (HIGH) | `tools/build_public_plugin.py` wrote the sidecar, `SOURCE_TO_PLUGIN_MAPPING.json` and `RELEASE_RECEIPT.json` with `Path.write_bytes`. A pre-seeded **hardlink** inside the output directory made the builder truncate and rewrite a file **outside** it, so the build still reported `BUILT`. | **REPAIRED.** All release members are now created with `O_CREAT\|O_EXCL\|O_NOFOLLOW` (`_exclusive_write`) and are written **before** the artifact is promoted, so a pre-seeded member refuses the build while nothing has been published. Only members this call created are rolled back; a pre-existing member is left exactly as found, never deleted. A pre-existing artifact name now refuses with `OUTPUT_ARTIFACT_EXISTS`. | RED: 3/3 new cases fail against the pre-fix tool (`HEAD:tools/build_public_plugin.py`) — `AO01_RED_then_GREEN.log`. GREEN: they pass with the fix. |
| `AO-02` (MEDIUM) | The delivered tree was not clean: round evidence was still untracked at hand-over time, so the officer's freeze refused it. | **REPAIRED.** The evidence is committed, and the round notes say plainly that the freeze refusing a dirty tree is the tool behaving correctly. | `git status --porcelain` clean at the commit that carries this file. |
| `AO-03` (MEDIUM) | The CI write-set step was a frozen-path **blacklist** (`^(skills\|src\|schemas)/`), so `dist/` and any other non-frozen path passed silently; no positive allowlist, the comparison base fell back to `HEAD~1`, and the header claimed the PR filter *was* the allowlist. | **REPAIRED.** The step now carries a positive allowlist plus an explicit `dist/` denial, requires the comparison base to resolve (refusing to guess), defaults to the fixed Stage-A tip for `workflow_dispatch`, and prints the base it used. The header no longer makes the false equivalence; the forbidden privileged trigger is not named anywhere in the file so a grep for it returns nothing. | `WRITE_SET_CLEAN_AGAINST_<base>` on a clean run; the step fails on a seeded out-of-set path. |

## One more thing worth writing down

The officer's own working copies (`verify/ao/candidate-copy/`, `verify/ao/owner-candidate/` — two full
147 MB copies of the subject placed *inside* the subject tree) broke four unrelated tests on the next
full run: `shutil.copytree(ROOT)` walks into them and cannot follow their dangling entries, and the
scanner-stays-out-of-the-tree case sees them as tree pollution. The suite was green before and is
green after they were moved out to the session scratch directory.

Read correctly this is **not** a defect of the candidate: it is the checker's own artifact, and the
first full run after the challenge was red for that reason alone. It is recorded here rather than
quietly cleaned up because a later reader comparing the two full-suite logs needs to know why one of
them has 1 failure and 3 errors. The rule for the next round is that an independent checker copies
the subject **outside** the subject tree.

## State after the iteration

| Item | State |
|---|---|
| Full suite | `Ran 572 tests ... OK (skipped=6)`, exit 0 — `raw/orch_full_suite_after_ao01_fix_clean.log` |
| Focused packaging + fallback | `Ran 47 tests ... OK` (44 before, plus the 3 new `AO-01` cases) |
| Write set | clean against the fixed Stage-A tip `52542c39` |
| Claim ceiling | unchanged: `CODE_CANDIDATE_READY_PENDING_PUBLISH` at best; no Portal, no Host UAT, no `S4_FULL_PASS` |
| Re-verification | dispatched as a fresh independent lane on the new commit, copying the subject outside the tree |
