# WO-S4R2M-DOC-CAL-01 — front page: two onboarding paths, and `--root` described truthfully

You are a **bounded writer**. Your write-set is exactly these two paths and nothing else:

- `README.md`
- `tests/test_s4r2m_docs_route.py`  (new file)

Do **not** touch `src/**`, `schemas/**`, `dist/**`, `examples/**`, `tools/**`, `pyproject.toml`,
`openspec/**`, `.hgk/**`, or any other test file. Do not create new directories.

## Working root

`C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt`

All paths below are relative to that root. Do not work outside it.

## Interpreter (pin by absolute path — a bare `python` on this host may lack `jsonschema`)

```
PY=C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe
PYTHONPATH=C:/Projects/Agent_Workspace/PIPD/worktrees/s4r2m-merge-wt/src
```

Run the CLI as `"$PY" -m pipd_ls_sp.cli ...` with that `PYTHONPATH`.

## Background you need

Two independent findings are still open on this exact tree. Both were re-derived in this round, so
neither is a guess:

- **F01.** `README.md` has `## Start here`, `## Quickstart`, `### bash / POSIX`,
  `### Windows (PowerShell)`, `### Unverified one-line install (no hash check)`, `### Run it: the whole
  compiler chain, copy-paste`. It says the project "ships 8 skills and 13-command CLI" but never tells a
  reader that those two consumer paths are installed and mounted **differently**. A non-technical reader
  reasonably concludes that `pip install` also makes eight skills appear in a web chat host. It does not.
- **F02.** The README claims `--root` is a **GLOBAL** option that "must precede the subcommand"
  (see the comment on the `pipd --root .\myproject init` line, and the paragraph that begins
  "These are the exact commands that produced the checked-in `examples/first-run/`"). That is true for
  part of the CLI and false as a general rule: `src/pipd_ls_sp/cli.py` adds a **subcommand-local**
  `--root` (`dest="sub_root"`) to `project` and `export`, and the dispatcher resolves
  `getattr(args, "sub_root", None) or args.root`.

Verify both statements yourself against `README.md` and `src/pipd_ls_sp/cli.py` before you start.

## What to deliver

### 1. A new section `## Choose your path: CLI or Skills`

Insert it **between** the existing `## Start here` section and the existing `## Quickstart` heading.
Keep it to roughly 10–20 lines. Do **not** restructure or re-order the rest of the README.

It must give exactly two paths, each with the artefact a reader downloads and the boundary of what that
artefact does:

- **CLI / headless harness** — the immutable wheel published under the `v0.1.0-preview.2` tag, its
  `SHA256SUMS`/published digest, Python ≥ 3.11, a virtual environment, then `pipd doctor`. Say plainly
  that the wheel carries the Python CLI and the 19 installed schemas, and that it does **not** install or
  auto-load the eight logical skills into a web host.
- **Skills / document consumption** — the versioned mount pack
  (`dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip`, with its `.sha256` sidecar and the
  `MANIFEST.sha256` inside the unpacked directory), which currently lives on this candidate branch and
  is **not** a published release asset. Distinguish two sub-options: (a) a host that has a real native
  skill uploader — mark it as **not yet demonstrated here**; (b) manual document/Knowledge attachment
  of `SKILL.md` plus the short starter prompt. State that the document path does not execute `pipd` on
  the reader's machine.

Use only facts you can read in the tree. Do not invent a download URL for the pack and do not claim a
native skill load has been demonstrated.

### 2. Correct the two `--root` statements

Replace the absolute phrasing with what the parser actually does. The accurate statement is:

> For `init`, `intake`, `profile`, `compile-pi`, `bind-pd`, `compile-ecp`, `compile-tqaep`, `validate`
> and `doctor`, `--root` is a global option and must precede the subcommand. `project` and `export`
> **additionally** accept `--root` after the subcommand.

Keep these three documented positives intact and make them ones the CLI really accepts
(confirm each one by running it — see step 4):

```
pipd --root ./demo init
pipd project --root ./demo --dry-run
pipd export --root ./demo --dry-run
```

Do not weaken the existing verified checksum instructions (Bash `sha256sum -c`, PowerShell
`Get-FileHash`) and do not change the published wheel digest.

### 3. `tests/test_s4r2m_docs_route.py`

A `unittest` module, in the same style as the other files in `tests/`. It must:

- parse `README.md` and assert the new `## Choose your path: CLI or Skills` heading exists and sits
  between `## Start here` and `## Quickstart`;
- assert the README no longer contains a claim that `--root` must always precede the subcommand;
- drive the CLI in-process or through `subprocess` to assert the three positives above exit 0;
- assert a form the parser refuses exits non-zero (for example `--root` after the subcommand on `init`);
- assert that a documented Skills-path statement does not claim a native skill load, i.e. the section
  text mentions the manual/Knowledge route and does not assert native loading as demonstrated.

Guard the CLI invocation with an interpreter-independent call (use `sys.executable` plus the repository
`src` on `PYTHONPATH`) so the test does not depend on a machine-specific interpreter path.

### 4. Run what you document

Actually execute, in a scratch directory **outside** the repository:

- `pipd --root <scratch>/demo init`
- `pipd project --root <scratch>/demo --dry-run`
- `pipd export --root <scratch>/demo --dry-run`
- one refused form, e.g. `pipd init --root <scratch>/demo`

Then run your new test module and the two neighbouring modules that must keep passing:

```
"$PY" -m unittest discover -s tests -p 'test_s4r2m_docs_route.py' -v
"$PY" -m unittest discover -s tests -p 'test_postrelease_quickstart.py' -v
"$PY" -m unittest discover -s tests -p 'test_first_run_examples.py' -v
```

## Honesty rules (these override any instinct to look finished)

- Every command you print in the README must be a command you actually ran, with the concrete result
  you actually saw.
- If the real CLI behaviour differs from the paragraph above, describe the **real** behaviour and say so
  in your final report — never bend the README to match an assumption in this brief.
- Never add a CLI command, change a schema, or edit source to make a documented line work.
- Do not fabricate a transcript, a digest or a version number.
- If you cannot complete a step, leave the tree in a coherent state and report the blocker plainly.

## Required final report (print it; keep it under 40 lines)

1. `git status --porcelain=v1` and `git diff --stat` for your two paths only.
2. The exact commands you ran in step 4 with their exit codes (both the successes and the refusal).
3. The three unittest module results, as `Ran N tests ... OK` / `FAILED`.
4. Any place where the real behaviour contradicted this brief.
