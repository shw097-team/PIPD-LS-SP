# ROUND RESULT — S4R3X (S4R3-F006 repair, gate falsifiability, Stage B successor)

Round id: `S4R3-20261013-ci-truthfulness-and-stageb-writeset` (continued in this session; the gate
receipts for the continuation are in `evidence/12_GATES/`).

## 1. Subjects

| stage | branch | head | declared base |
|---|---|---|---|
| A | `fix/s4r3-stage-a-ci-truthfulness-20261013` | `5310896e706e01a9cdb0123285bccec75086bcb8` | `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` (the frozen report subject) |
| B | `feat/s4r3-stageb-successor-20261013` | `60273fe3dee54d88250e1588892da72aecd222ac` | the Stage A tip, resolved by ref at run time |

Pull requests: A → [#3](https://github.com/shw097-team/PIPD-LS-SP/pull/3) (base `main`, draft),
B → [#5](https://github.com/shw097-team/PIPD-LS-SP/pull/5) (base = the Stage A branch, draft).

`main` = `224591431a164ab72a9423cd180e417e8a762403`; `v0.1.1-preview.3` =
`e94cc7f9567acb59de4691ee6166815ac96a9700`. Neither was moved, tagged, released or force-pushed. Stage A
was only ever fast-forwarded. Stage B was rewritten once, before any review, with
`--force-with-lease`; the disclosure and the superseded head are in `evidence/12_GATES/SUBJECTS.json` and
in the PR body.

## 2. What this continuation changed

### Stage A

1. **S4R3-F006 repaired** (the P0 the previous round left open). The canonical `schemas/` tree lives at
   the repository root, outside the package directory, so `package-data` could not reach it and
   `python -m build` produced a wheel with no registry: a clean-venv `pipd doctor` then reported
   `mode=NONE` / `verdict=FAIL` and exited 1. The repair is an explicit `build_py` hook in `setup.py`
   plus a `MANIFEST.in` that brings `schemas/` into the sdist, so the **standard** build path is
   correct. No oracle, guard, exit code or denominator was weakened or narrowed.
2. **The F006 CI gate was made falsifiable off-CI.** Its first version lived only inside
   `.github/workflows/ci.yml` and asserted the doctor's `families` was a dict when `workspace.doctor`
   reports the family *count*. Nothing local executed it, so it went red on the hosted runner for a
   reason unrelated to the product. The assertions now live in
   `tools/verify_installed_wheel_registry.py`; CI calls it, and the local suite runs it against the real
   doctor document plus six mutations. See `evidence/12_GATES/SELF_CAUGHT_FALSE_GREEN.md`.
3. **S4R3-F002 corrected for Stage A too.** The write-set gate took its scope from the pull request's
   base branch, so Stage A, opened against `main`, was measured as `main...HEAD` — the entire
   triple-upgrade surface — and went red on paths Stage A never wrote. Each branch now **declares its
   stage**; the declared base must be an ancestor of the subject; the pull request base is printed as
   context that is explicitly not the governed write set. Neither stage's allowlist was widened, and the
   classifier self-test still proves planted violations are refused.
4. The gate that decides scope is now itself run locally before push
   (`scripts/run_writeset_gate_locally.py`).

### Stage B

1. **Re-stacked on the current Stage A tip.** The previous Stage B head (`c52c219`) was a *sibling* of
   the Stage A repairs: with two dots, `4647d14..c52c219` still diverged in Stage A's module paths, so
   the branch did not contain the CI guards or the F006 repair it is validated by. The product surface
   was carried over exactly and the branch now sits on `5310896`.
2. **`CR-IDENTITY-BIND` closed.** The official manifest's `name`/`version`/`license` are now bound to the
   release bookkeeping. A vendor-schema-valid but different `name` used to be accepted at exit 0 while
   the ZIP root and the release receipt still carried the bookkeeping's `plugin_id`.
3. **`CR-EXT-UNREVIEWED` closed.** `extensions` is restricted to the reviewed namespace set
   (`com.openai`, `com.pipd.s4`); the locked vendor schema permits arbitrary object-valued namespaces,
   so an unreviewed one travelled inside the ZIP at exit 0.
4. Seven negative/positive tests cover both. The real packaging inputs still build (`BUILT`,
   56 members).

Both `CR-` defects were recorded as OPEN by the previous round's acceptance officer; neither was found
by the author of this branch.

## 3. Raw results

| check | result | source |
|---|---|---|
| Stage A, hosted CI (push and PR): full unittest suite | success | run 38365817545 / 38365822386 |
| Stage A, hosted CI: focused S4 suite | success | run 38365817545 / 38365822386 |
| Stage A, hosted CI: F006 wheel gate | success — `mode=INSTALLED families=19 path=…/site-packages/pipd_ls_sp/schemas` | run 38365817545, job 115190559569 |
| Stage A, hosted CI: write-set gate | success — `WRITE_SET_CLEAN_AGAINST_e71fee6d…`, stage-a self-tests OK | run 38365822378, job 115190576103 |
| Stage B, hosted CI: full/focused suite and F006 gate | success | runs 38365822012 / 38365828586 |
| Stage B, hosted CI: write-set gate | success — `WRITE_SET_CLEAN_AGAINST_5310896…`, stage-b self-tests OK | run 38365828658 |
| local Windows, Stage A full suite | see `evidence/12_GATES/LOCAL_FULL_SUITE_RECEIPTS.txt` | — |
| local Windows, Stage B focused (packaging, tooling, web fallback, wheel) | 74 tests, `OK (skipped=1)` | `win_stageb_focused2.log` |
| local paths: write-set gate, both stages | clean, `2/2` | `writeset_gate_local_final.txt` |

Every CI headline above is a **hosted** result for the exact subject SHA; the winning lines are quoted
verbatim in `evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt`.

## 4. Finding dispositions

| finding | previous | now | basis |
|---|---|---|---|
| F001 CI hid failures | source-only closed | closed, and the harness that reproduced it is exercised on both subjects | hosted runs above; `tests/test_tooling_executes.py`, the CI exit-code steps |
| F002 wrong write-set base | source-only closed for B only | closed for both stages | `WRITE_SET_CLEAN_AGAINST_…` on both heads |
| F003 publisher / brand / vendor / Portal | OPEN_TT_OWNER | **still OPEN** — human identity, artwork, official validator and Portal are owner-supplied | not attempted |
| F004 Web / navigation documentation | source-only closed | closed; the fallback digest matches its `.sha256` and 27 local links resolve | `docs/install/PIPD_WEB_FALLBACK.md` |
| F005 evidence mass | PARTIAL | **PARTIAL** — `.hgk/` is still large; the archive policy needs an owner decision | not attempted |
| F006 wheel ships no schemas | EXPOSED, OPEN | **closed on both branches**, with a local and a hosted gate | wheel gate receipts |
| CR-IDENTITY-BIND | OPEN (Stage B) | closed | builder gates + tests |
| CR-EXT-UNREVIEWED | OPEN (Stage B) | closed | builder gates + tests |
| four-host UAT | NOT_EXECUTED | **NOT_EXECUTED** | not attempted |
| `.hgk` archive policy | owner decision | **owner decision** | not attempted |

## 5. Claim ceiling

This round's work is **locally verified and hosted-CI verified by the project's own pipelines**. That is
not an acceptance:

- No independent acceptance officer verdict is recorded for these two heads yet — see
  `evidence/12_GATES/AO_LANE_OUTCOME.json` for exactly what the mandated VERIFY lane did and did not
  produce this round.
- No human publisher identity, brand artwork, official vendor validator, Portal scan/review/publish, or
  host UAT was executed.
- `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` remain in force. Both pull requests stay
  drafts.
- Nothing in this round was merged, tagged, archived or released.

## 6. Deviations from the requested execution plan (stated plainly)

The round was asked to run under a specific model plan and toolchain: PLAN in Hermes on
`GPT 6.1 SOL-MEDIUM`, EXECUTE handed to the CODEX CLI on `DeepSeek V4.1 Flash`, VERIFY/SECURITY handed to
the CODEX CLI on `GLM-5.3-Flash`, driven with KANBAN/SWARM/GSTACK/OPENSPEC and multiple sub-agents.

What actually happened: PLAN and EXECUTE were both performed by the Hermes agent that holds this
conversation; the CODEX CLI lane was used **only** for the VERIFY_SECURITY role. No sub-agents were
spawned. KANBAN/SWARM/GSTACK were not driven as separate surfaces this round; OpenSpec was not
re-validated.

This is a real deviation and it caps what may be claimed: the Execute separation-of-duties property the
plan was designed to produce does not hold for this round's code, because the same party wrote and
locally verified it. The three-way split that *is* supported by evidence is: author (Hermes) → project
CI on GitHub (independent of this workstation) → the mandated VERIFY lane (best-effort; see the AO
outcome file).

## 7. What the Owner must decide

1. Whether to accept the re-stacked pair, or to require a different stack shape.
2. F003 inputs (publisher identity, brand artwork, official vendor validator, Portal access) and the
   named human responsible for host UAT.
3. F005: the `.hgk/` archive policy and its owner.
4. Whether the Stage A pull request should keep `main` as its base, given that Stage A is the bottom of a
   stack and its own write-set verdict is declared per stage rather than against `main`.
