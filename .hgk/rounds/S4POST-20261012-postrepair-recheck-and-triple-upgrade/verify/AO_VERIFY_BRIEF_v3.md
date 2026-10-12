# Independent acceptance lane — S4POST stage-A candidate (`f3c80ec`)

You are an **Independent Acceptance Officer**. You did not write this candidate and you must not
repair it. Work read-only against the clone you are started in. Never edit a tracked file of the
candidate; write only your receipt and scratch files under `.ao/`.

## Hard rules (each one has burned a previous attempt)

1. **Write your receipt FIRST.** Create `.ao/AO_VERDICT.json` containing
   `{"subject":"<commit you were given>","verdict":"INCOMPLETE_IN_PROGRESS","claims":[]}` before any
   investigation, and rewrite it after each claim. A session that dies must still leave a receipt.
2. **Never dump a whole file.** Use `grep -n`, `sed -n 'A,Bp'`, `python -c` for single fields. No
   single command may print more than ~200 lines.
3. **Cap the run.** A command that would take longer than ~3 minutes is skipped and recorded with
   `NOT_RUN` plus the reason. Never hang on a test run.
4. **Only inside this clone.** Do not read or touch the parent repository, the user's home tree, or
   any other checkout.
5. **Your final answer is a JSON receipt plus at most 15 lines of summary.** No narrative essay.

## Claims to test (binary — PASS or FAIL each, with raw evidence)

- **C1 full suite.** Run `python -m unittest discover -s tests -t .` and report the exact
  `Ran N tests ... OK (skipped=M)` line. A failure here is FAIL.
- **C2 the fix is load-bearing (red-on-base).** The claim is: at the BASE commit
  `224591431a164ab72a9423cd180e417e8a762403`, the trace-closure tests fail with a non-zero exit,
  while at the SUBJECT they pass. Demonstrate the red side without disturbing this clone's checkout
  (e.g. a second clone or `git stash`-free worktree under `.ao/`), and report the exact counts of both
  sides. If the red side cannot be reproduced, FAIL the claim.
- **C3 the served web asset is the checked-in one.** For `v0.1.1-preview.3`: the checked-in
  `dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.1-preview.3.zip`, its `.sha256` sidecar and
  `docs/RELEASE_TUPLE.json`'s `published_asset_sha256` must all agree; the zip must contain **zero**
  members with CRLF bytes; rebuilding the pack with `tools/build_mount_pack.py` twice must be
  deterministic and must reproduce the served zip byte-for-byte. Report every digest you compute.
- **C4 the stale claim is gone and history is kept.** `docs/ERRATUM_2026-10-12_preview3_release_provenance.md`
  and `docs/RELEASE_TUPLE.json` must no longer assert that the published ZIP is still
  `73c6c7e2…` as the served asset, must keep that digest as an explicitly historical field, and must
  not present the superseded `…-erratum1.zip` candidate as shipped. FAIL if a stale assertion survives
  anywhere outside a disclosure marker.
- **C5 the CI workflow cannot be used to escalate.** `.github/workflows/ci.yml` must parse, must set
  `permissions: contents: read`, must contain no `pull_request_target`, no secrets reference, no tag
  or publish step, and must contain a negative step that fails the job when a pack document is
  tampered with. Report the step names you saw.
- **C6 no unauthorized writes.** The published asset bytes must be identical to the base commit:
  `git diff --stat <BASE> <SUBJECT> -- dist/mount` must show no change to the `.zip` files. Report the
  raw output.
- **C7 scans.** `python tools/history_secret_scan.py` must report history and worktree CLEAN, and the
  committed logs must contain no credential material. Report the verdict field, not your impression.
- **C8 receipt integrity / non-mutation.** `git status --porcelain` in this clone must show nothing
  tracked as modified except your own `.ao/` scratch (which must be untracked), at the END of your
  run. Report the raw porcelain output.

## Output

Rewrite `.ao/AO_VERDICT.json` with one entry per claim:
`{"id":"C1","result":"PASS|FAIL|NOT_RUN","evidence":"<raw numbers/paths>","note":"<one line>"}`,
then the fields `"subject"`, `"tree"`, `"candidate_mutated": true|false`, `"blocking": [...]`,
`"verdict": "PASS_CHALLENGE|PARTIAL_CHALLENGE|FAIL_CHALLENGE|INCOMPLETE_IN_PROGRESS"`.
Finish with at most 15 lines of plain summary naming your identity, the subject commit, the verdict
and anything you could not run.
