# Bounded writer brief — S4EXT-R1 FAR adjudication execution

You are the **bounded writer** (EXECUTE lane) in a governed round. The user authorized executing a FAR
adjudication. You change code; you do not accept your own work and you do not commit.

Repository (cwd, Windows + git-bash/MSYS): `C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt`
Python: use `python` (3.11). Native tools need `C:/...` paths, MSYS `/c/...` paths are NOT translated.

## Hard constraints

- You may create or modify ONLY these five files:
  1. `tools/admit_technologies.py` (modify)
  2. `tools/history_secret_scan.py` (modify)
  3. `tools/verify_evidence_digests.py` (new)
  4. `tests/test_s4ext_artifact_reproducibility.py` (new)
  5. `tests/test_technology_admission.py` (modify - one call site only)
- Do NOT commit, do NOT push, do NOT run `git add`, do NOT create or move branches or tags.
- Do NOT make any existing gate stricter repo-wide. The new digest verifier REPORTS by default.
- Do NOT regenerate or rewrite any file under `.hgk/artifacts/` or `dist/`. Leaving the tracked tree
  byte-identical is part of the requirement: several tests assert on that.
- Keep the diff small and in the existing code style (module docstring, `from __future__` only if the
  file already has it, ASCII-only source, 4-space indent).

## Change 1 — reproducible generation identity (`tools/admit_technologies.py`)

Today the artifact records `candidate_head` from `git rev-parse HEAD` at generation time
(`_candidate_head()` near line 84-86; written near line 490). Because the artifact is committed, the
committed value ends up being an ANCESTOR of HEAD (it is `8ad0fd3254561d5d043a8fa1e9d64918892c751b`,
69 commits behind) and can never reproduce.

- Add an argparse option `--for-commit SHA` (default `None` = today's behaviour).
- `_candidate_head()` must return the override when one was provided, else keep today's behaviour.
- Next to the `candidate_head` field in the emitted payload add `candidate_head_note` (a string):
  state that this is the generation identity, that it names the source revision the artifact was
  generated from, that it is an ANCESTOR of the commit that carries the file and is NOT the release
  tip, and that regenerating with the same `--for-commit` reproduces the file byte-for-byte.
  Follow the wording style of `tools/build_dist.py` around line 191-196.
- Do not change any other field, and do not change the default output path.

## Change 2 — the mandated scanner must be able to stay out of the tree (`tools/history_secret_scan.py`)

`main()` writes to a hardcoded `ROOT / ".hgk" / "artifacts" / "history_secret_scan.json"` (about
lines 122-124). The file has NO argparse at all.

- Add argparse with a single optional `--out PATH`. Default = today's hardcoded path, so behaviour is
  unchanged when the flag is absent.
- Extend the module docstring: the default writes inside the tracked tree, so a verifier that must
  leave the worktree untouched should pass `--out`.
- Do not change anything else (the scan itself, `scan_worktree`, `scan_history`, `printable_summary`).

## Change 3 — NEW `tools/verify_evidence_digests.py`

Purpose: make a silent class visible. No tool or test today recomputes the per-entry sha256 recorded
in `.hgk/artifacts/evidence_manifest.json` against the bytes on disk, and
`tools/build_publication_manifest.py` folds those digests into `crosswalk_digest`. Measured today:
1085 entries, 1044 match, 0 missing, **41 stale** (this is a pre-existing condition; do NOT fix it).

- CLI: `python tools/verify_evidence_digests.py [--manifest PATH] [--json PATH] [--strict]`
  - default manifest = `.hgk/artifacts/evidence_manifest.json`
  - default: print a JSON report to stdout `{"checked":N,"match":N,"missing":N,"stale":[paths],"identity_checks":[...]}` and exit 0
  - `--strict`: exit 1 when `stale` is non-empty (opt-in only)
- Also verify generation-identity fields: for any file whose JSON payload contains `candidate_head`,
  check `git merge-base --is-ancestor <value> HEAD` when the value looks like a resolvable commit;
  record `{"path":..., "candidate_head":..., "is_ancestor": true|false, "error": null|"..."}`.
  Never fail on this (report only).
- Must work from the repository root; never write anything except the optional `--json` output path.

## Change 4 — NEW `tests/test_s4ext_artifact_reproducibility.py`

Follow the house test style (see `tests/test_evidence_manifest.py` for the sys.path bootstrap idiom at
the top of the file — every test file in this repo bootstraps `sys.path`). Tests:

- `T1 reproducible generation identity`: run the generator twice into a TEMPORARY artifact path with
  the same `--for-commit <sha>` (use the tool's existing `--artifact PATH` option if it exists, else
  run it inside a temporary copy of the repo) and assert the two outputs are byte-identical. The
  tracked `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` must NOT change: assert its sha256 before and
  after are equal.
- `T2 scanner stays out of the tree`: run `tools/history_secret_scan.py --out <tmp>/hss.json` and
  assert the tracked `.hgk/artifacts/history_secret_scan.json` sha256 is unchanged and the tmp file
  exists and parses as JSON.
- `T3 the verifier detects staleness`: copy `evidence_manifest.json` to a temp file, corrupt one
  recorded digest, run the verifier with `--manifest <temp>` and assert the corrupted path is reported
  under `stale`; and run it on the real manifest asserting it exits 0 without `--strict` while
  reporting a non-empty `stale` list is NOT required to be empty (do not assert a specific count).
- `T4 the recorded identity is an ancestor`: read `candidate_head` from
  `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` and assert `git merge-base --is-ancestor <value> HEAD`
  exits 0 (skip the test if `git` is unavailable).

## Required before you report back

Run and paste the exact command plus its exit code for:
1. `python -m unittest tests.test_s4ext_artifact_reproducibility`
2. `python -m unittest tests.test_evidence_manifest tests.test_tooling_executes`
3. `python tools/verify_evidence_digests.py` (report the counts it prints)
4. `git status --porcelain` (must show ONLY the two modified files, the two new files, and the two new
   untracked FAR/round artefacts if any; the tracked `.hgk/artifacts/` files must NOT be modified)
5. `git diff --stat`

Then report: files changed, the exact commands and exit codes, anything you could not do, and any
place where the brief was ambiguous. If a test you were asked to write cannot pass without changing
something outside your four allowed files, STOP and report that instead of widening the change.


## Change 5 — the suite must stop rewriting a tracked artifact (one call site)

An independent acceptance officer pinned the exact mechanism of a read-only violation that DID fire
during a mandated run (AO attempt 3, blocking item 1):

  tests/test_technology_admission.py:156 invokes `tools/admit_technologies.py --report` WITHOUT
  `--artifact`, and tools/admit_technologies.py:520 writes the TRACKED
  `.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json`; the suite therefore rewrote the committed
  `candidate_head` 8ad0fd32... -> the current HEAD during `python -m unittest discover -s tests -t .`

- Fix it at the call site: make that invocation write to a temporary path. The tool already ships an
  `--artifact PATH` option (around tools/admit_technologies.py:508-511), so prefer passing
  `--artifact <a tmp file>` over any change to the tool's default behaviour.
- Any assertion in that test that reads the produced artifact must read the temporary file.
- Do not change the tool's default output path and do not weaken the test's assertions.
- If and only if the call site genuinely cannot be redirected, STOP and report that instead.

## Required before you report back (addition)

6. `python -m unittest tests.test_technology_admission`
7. `git status --porcelain` after a FULL suite run must show NO modification under `.hgk/artifacts/`.
   Prove it: capture `git status --porcelain .hgk/artifacts/` before and after running
   `python -m unittest discover -s tests -t .` and paste both.
