HGK_LANE_NONCE_OK

# BOUNDED WRITER BRIEF — PIPD S4 R6 FAR-R17 (EXECUTE lane)

You are the **bounded tracked writer** for round `PIPD-S4-R6-CLOSEOUT-20261016` (FAR R17 continuation)
under HG-KSEOS. A human owner is accountable; you are the writer, not the acceptor.

**Publication authority:** any remote write for this round belongs to the admitted HGK WorkOrder
`WO-TS-CLOSEOUT-04`; the orchestrator performs it, not you. Do not push, tag or open anything.

## Workspace

- repository root: `C:/Projects/Agent_Workspace/PIPD-S4R6-wt` (branch
  `fix/s4r6-closeout-doc-identity-and-update-route-20261016`, already pushed; the orchestrator will
  commit and push your edits itself)
- read these first, they define the house style you must match:
  - `tests/test_s4r2m_docs_route.py` — asserts README text and drives the CLI with no network
  - `tests/test_r5r3_install_route_identity.py` — release-identity guard; note how it re-derives tag
    facts from git instead of hard-coding them, and how one docstring records WHY an earlier version of
    the guard was too weak
  - `.github/workflows/ci.yml` — the suite is run by `python -m unittest discover -s tests -t . -v`,
    so a new `tests/test_*.py` file is wired in automatically. **Do not edit any workflow file.**

## Task A — add exactly ONE new test file

Create `tests/test_r6_doc_identity_guard.py`. It is the "single doc-link / release-identity check" the
independent R6 review asked for (`F-R6-01`). Pure stdlib + `unittest`; **no network**; must pass with
`python -m unittest tests.test_r6_doc_identity_guard -v` from the repository root, and it is run by the
existing CI unchanged.

It must verify, for `docs/install/README.md` and `docs/USER_GUIDE.md`:

1. **No cross-release mixing.** Within any single paragraph of `docs/install/README.md`, the
   `v0.1.1-preview.4` release id must not appear together with the `v0.1.1-preview.3` target commit
   `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a` unless the paragraph explicitly marks that commit as
   preview.3 (the words `preview.3` or `preview. 3` in the same paragraph). Derive the preview.3 commit
   mapping by READING `docs/RELEASE_TUPLE.json` — do not hard-code a value that the tuple already
   states; hard-code only the tag names.
2. **Every documented build example names one generation.** For each fenced ```bash block in
   `docs/install/README.md` that contains `--release-id`, extract `--mount-pack`, `--release-id` and
   `--release-commit`. All three present must agree on the same release generation (same `vX.Y.Z-preview.N`
   token), and if a `--mount-pack` path is given, that path must exist in the tree at HEAD; if it does not
   exist, the block must be labelled legacy/historical in the surrounding prose. Report the block's line
   number in the failure message.
3. **No phantom pack.** `docs/install/README.md` must not reference a `dist/mount/` directory that does
   not exist at HEAD. Derive the existing set from the filesystem/git, not from a hand-written list.
4. **In-page anchors resolve.** For both documents, every markdown link of the form `](#fragment)` inside
   the same file must resolve to a heading in that file (GitHub's slug rule: lowercase, drop anything
   that is not alphanumeric/space/hyphen, spaces to hyphens). Report the file and the dangling fragment.
5. **The user guide's ceilings stay honest.** `docs/USER_GUIDE.md` must still contain `NOT_GRANTED` for
   `S4_FULL_PASS` and must not contain the exact sentence fragment `Merge and release are` followed by
   `HOLD`.

**Non-vacuity is mandatory.** A guard that cannot fail is not evidence. For checks 1–4, the test must
build a MUTATED COPY of the document in a `tempfile.TemporaryDirectory()`, write it out, run the same
checking function against that copy, and assert that the check FAILS. Do the mutation in-process by
editing the string you read (e.g. replace the preview.4 target commit with the preview.3 one inside the
pinned paragraph; delete a heading that an anchor points at; point a `--mount-pack` at a
`...preview.4` directory). Each mutated case must be its own test method. Put the checking logic in
module-level pure functions so the tests can call them on either the real file or a mutated copy.

Docstring at the top of the file: state the defect being guarded, cite `F-R6-01`, and say that the
mutation cases exist so the guard is falsifiable — matching the house style of the two files above.

## Task B — one bounded edit to `docs/install/README.md`

The published `v0.1.1-preview.4` release **serves** a `PIPD_WEB_FALLBACK.md` whose own header declares
`release_id: v0.1.1-preview.3` / `release_commit: cbf69756...`, and its served sha256 equals the
committed file's. That is a real provenance drift in an immutable release.

Add a short, clearly-marked note (2–5 sentences) in the existing "Advanced and recovery" area — do not
create a new top-level section. It must name the served document, its sha256
`c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af`, say plainly that the served copy
declares the earlier `v0.1.1-preview.3` provenance, and say that this can only be corrected by a future
release because the file is a frozen asset of `v0.1.1-preview.4`. The note must NOT state or imply that
the release asset has been, or can be, repaired in place. Do not delete any existing sentence.

## Hard bounds

- Create `tests/test_r6_doc_identity_guard.py`; edit `docs/install/README.md`. **No other file.**
- Do not touch `src/`, `schemas/`, `dist/`, `.github/`, `skills/`, `.hgk/`, or any other test file.
- Do not modify the existing `test_s4r2m_docs_route.py` or `test_r5r3_install_route_identity.py`.
- Write LF line endings; do not introduce CRLF.
- Run, and paste the raw output of, these two commands from the repo root:
  - `python -m unittest tests.test_r6_doc_identity_guard -v`
  - `python -m unittest discover -s tests -p 'test_r6*.py' -v`
  If a legacy Python cannot run them, say so and paste the exact error; do not claim a pass you did not see.
- Do not introduce a literal token, PAT or secret anywhere.

## Receipt (plain text, final part of your answer)

```
FILES: <path> (+n/-n) | <path> (+n/-n)
NEW_TESTS: <how many test methods, and which are mutation cases>
RUN: <command> -> exit <n> ; raw last line: <...>
RUN: <command> -> exit <n> ; raw last line: <...>
MUTATIONS: <list the mutations and confirm each makes its check fail>
NOT_DONE: <anything you could not do, with the raw error>
```
