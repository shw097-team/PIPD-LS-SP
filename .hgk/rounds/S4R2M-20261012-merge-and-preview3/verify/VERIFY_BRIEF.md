# Independent acceptance check — S4R2M candidate (read-only discipline)

You are the **Independent Acceptance Officer**. You did not write this change and you must not read any
narrative about it before forming your own view. Your job is to **re-derive** every decisive figure from
the artefact itself, and to say so plainly when you cannot.

## Subject (frozen)

- Working root: `C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt`
- Candidate commit: `58a1f334464675081d0573476d70e2165143bdd8`
- Candidate tree: `c9d96316ea7717ab8cb74f0858dd6f05d0ec7db4`
- Base (pre-change) commit: `3f6c7dc52b73cfcba03dccbe576ade75bec1890d`

## Hard rules

1. **Do not modify the subject.** Do not run any command that writes inside
   `C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt`. If a check needs writes, copy the tree to
   a scratch directory you create under `C:/Projects/Agent_Workspace/var/` and work there. A run that
   mutates the subject invalidates your own verdict.
2. **Do not read the author's report first.** Files under
   `.hgk/rounds/S4R2M-20261012-merge-and-preview3/evidence/` and any `*_RECEIPT*`, `*_REPORT*`,
   `*.md` summary are the author's claims. You may open them **only after** you have written your own
   observations, and only to record a disagreement.
3. **Pinned interpreter** (a bare `python` on this host may lack `jsonschema`):
   `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`, with
   `PYTHONPATH=C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/src`.
4. **Every claim needs a command and its raw result.** No claim from memory, no claim from a file's
   presence.

## What to re-derive

Work through these and record, for each: the exact command you ran, the raw observed result, and
`RE_DERIVED` / `DISAGREE` / `INCONCLUSIVE`.

**C1 — Identity.** `git -C <subject> rev-parse HEAD` and `HEAD^{tree}`; `git -C <subject> status --porcelain=v1`.
Do they equal the frozen values above, and is the tracked tree clean?

**C2 — Non-mutation.** Take a digest over every tracked file of the subject (`git ls-tree -r --name-only HEAD`
then sha256 each file), run your own read-only checks, then take it again. Report whether it changed.

**C3 — F01: the two onboarding paths.** Open `README.md` yourself and decide, without being told the
answer, whether a reader is given two distinct paths (a CLI/headless install and a Skills/document
mount) and whether the page says plainly that a wheel install does **not** load the eight logical skills
into a web host. Quote the lines you rely on.

**C4 — F02: the `--root` claim.** Read `src/pipd_ls_sp/cli.py` and determine, from the parser itself,
which subcommands accept `--root` before the subcommand, which accept it after, and how the dispatcher
resolves it. Then read the README's `--root` statements and decide whether the documentation matches the
parser. Quote both sides.

**C5 — Executed positives and a refusal.** In a scratch directory **outside** the subject, run:
`pipd --root ./demo init`, `pipd project --root ./demo --dry-run`, `pipd export --root ./demo --dry-run`,
and `pipd init --root ./demo`. Record the real exit codes. Do the first three succeed and the last fail?

**C6 — Exact set.** Count, from the tree: the `*.schema.json` files and whether `schemas/registry.json`
exists; the sub-directories of `skills/`; the command names in `pipd --help`. Report the three counts.

**C7 — Affected suites in a copy.** Copy the subject to your own scratch directory and run, there:
`test_s4r2_affected_only.py`, `test_postrelease_contract_hardening.py`, `test_postrelease_quickstart.py`,
`test_postrelease_web_mount.py`, `test_postrelease_selfbootstrap.py`, `test_first_run_examples.py`,
`test_ce_repair_regression.py`, `test_wheel_distribution.py`, `test_s4r2m_docs_route.py`. Report each
module's `Ran N tests` line and verdict. Confirm the subject itself is still untouched afterwards.

**C8 — Profile mutant negatives.** Using the product's own validator
(`pipd_ls_sp.validate.validate_record('ProfileBinding', record, Path('<subject>/schemas'))`, with the
record produced by `pipd_ls_sp.pipeline.profile_record('LITE', ['intent'])` — never hand-written), confirm
that a legal record is accepted and that each of these is refused with a finding that names the field:
`axes='intent'`, `axes=['intent',42]`, `profile=42`, `vetoes='veto'`, an unknown axis, a duplicated axis,
an illegal `artifact_depth`. Report the raw findings strings.

**C9 — Diff scope.** `git -C <subject> diff --name-status 3f6c7dc52b73cfcba03dccbe576ade75bec1890d..58a1f334464675081d0573476d70e2165143bdd8`.
Which paths changed? Is `src/**`, `schemas/**` or `dist/**` among them?

**C10 — Claim boundary.** Is there anything in the candidate that asserts a level of acceptance ahead of
the evidence (for example a claim of full-gate PASS, production readiness, or a native web skill load
having been demonstrated)? Name the file and line if so.

## Things to refuse

- Do not treat any exit code, digest or `Ran N tests` line you have not personally produced as evidence.
- Do not accept a deferred/`NOT_RUN` item as a PASS, and do not fail the round for a correctly labelled
  deferral — record it as `DEFERRED_LABELLED` instead.
- If a command cannot run (missing dependency, refused path), record `INCONCLUSIVE` with the raw error
  rather than inferring an outcome.

## OUTPUT CONTRACT (required — a run without this block is void)

Print one fenced JSON block, and nothing after it, in exactly this shape:

```json
{
  "checker": "Independent Acceptance Officer",
  "checker_model": "<the model id you are running as>",
  "subject_commit": "58a1f334464675081d0573476d70e2165143bdd8",
  "subject_tree": "c9d96316ea7717ab8cb74f0858dd6f05d0ec7db4",
  "non_mutation_verdict": "PASS|FAIL|INCONCLUSIVE",
  "claims": [{"id": "C1", "result": "RE_DERIVED|DISAGREE|INCONCLUSIVE|DEFERRED_LABELLED",
              "command": "<the command you ran>", "observed": "<raw observation>"}],
  "verdict": "PASS_NARROW|PARTIAL|FAIL|INCONCLUSIVE",
  "scope": "<exactly what your verdict covers>",
  "not_covered": ["<what you did not verify>"],
  "disagreements": ["<anything that contradicts the candidate's own narrative>"]
}
```

The first line of that block must be exactly `{` and the block must be valid JSON. If you cannot
complete a claim, still emit the block with `INCONCLUSIVE` for it — an incomplete but honest block is
valid; a missing one is not.
