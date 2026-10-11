# INDEPENDENT ACCEPTANCE — cross-model, `openai-codex/gpt-6.1-sol`, round R8

Supersedes, for the cross-model question, the same-model subagent receipt of round R7
(`verify-codex/INDEPENDENT_ACCEPTANCE_R7.md` in the R7 round directory), which was explicitly
ceilinged `INDEPENDENTLY_RE_DERIVED_SAME_MODEL` because it ran on `deepseek-v4.1-flash` /
`opencode-go` — the maker's own model.

## How it was run

`HG-KSEOS/scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY`, i.e. the control plane's own
lane dispatcher, not a hand-rolled invocation.

```
--require-arm openai-codex/gpt-6.1-sol --force-rank 4 --max-candidates 1
--codex-home C:/Users/user/.codex
--sandbox danger-full-access --allow-sandbox-escalation
--guard-subject C:/Projects/Agent_Workspace/PIPD-r7-release
--cwd <scratch> --lane VERIFY_SECURITY --timeout 1500
```

`--force-rank 4 --max-candidates 1` and **not** `--require-arm` alone: see
`far/FAR-PIPD-R8-DISPATCH-004.md`. `--require-arm` verifies an arm but does not select it, so the
first run (receipt preserved as `LANE_RECEIPT_RANK1_WRONGARM.json`) silently executed on rank 1 —
`opencode-go/deepseek-v4.1-flash`, the maker's model — and returned `ok: false`,
`code: ERR_REQUIRED_ARM_NOT_SERVED`. That is the very defect this record exists to remove.

## Lane receipt — what the control plane says it did

| field | value |
|---|---|
| `ok` | **true** |
| `mode` | `forced_rank` |
| `required_arm` | `openai-codex/gpt-6.1-sol` |
| `served_arm` | `openai-codex/gpt-6.1-sol` |
| `used_rank` | 4 |
| `used_transport_model` | `gpt-6.1-sol` |
| `reasoning_effort` | `medium` |
| attempt `exit` / `nonce_present` / `usage_receipt_ok` | `0` / `true` / `true` |
| attempt `usage_provider` / `usage_model` / `usage_status` | `openai-p6a1fe3` / `gpt-6.1-sol` / `200` |
| `used_seconds` | 426.3 |
| stdout bytes / sha256 | 296,871 / `ffad75dd10337324…` |

**The identity of the serving model is corroborated by the relay's own usage log**, not only by the
dispatcher: `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` records a row with
`provider: openai-p6a1fe3`, `requestedModel: gpt-6.1-sol`, `resolvedModel: gpt-6.1-sol`,
`status: 200`, `requestedEffort: medium` inside this run's window. The dispatcher reads that log
itself (`receipt_binding: usage rows appended after this attempt started (byte offset bound)`).

So the checker is a **different model family from PLAN and EXECUTE** — this is cross-model, not
same-model re-derivation.

## Non-mutation guard — the escalated checker was bounded and it held

The checker ran with `danger-full-access` because it had to execute real commands; `workspace-write`
is unusable here (per the dispatcher's own note at the PROBE/TEST seam, under `workspace-write`
**no `command_execution` item is emitted at all and nothing lands**, while the turn still completes
and still echoes the nonce — so an exit code and a nonce are not evidence that anything ran).
`danger-full-access` has no sandbox root, so the guard is the only bound.

```
subject_mutation: mutated = False
  files_before = 3768   files_after = 3768
  added = []   removed = []   changed = []
  digest_before = 6cb7c7c0d4321fcb1fa9…
  digest_after  = 6cb7c7c0d4321fcb1fa9…
  guard_roots   = ["C:/Projects/Agent_Workspace/PIPD-r7-release"]
```

Identical digests. The checker also computed its own protected-tree comparison (3,768 files, none
added/removed/changed) and recorded it in `CHECKER_ACCEPTANCE_VERDICT.json`. Two independent
instruments agree that the subject was not touched.

## The checker's verdict

**`FAIL` — under a strict clean-worktree acceptance gate only.**

Its substantive checks all passed, on the **published bytes**:

- anonymous `git ls-remote`: `main` `26beacb`, `v0.1.0-preview.1` `cc9bf574` (unmoved),
  `v0.1.0-preview.2` `8faa64e`; no `refs/tags/*^{}` peel lines (both tags are **lightweight**);
- anonymous release metadata: release `409307718`, `prerelease: true`, `draft: false`;
- all four assets downloaded and **independently hashed**: wheel `d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f`
  (`expected_match: true`), source zip and preview notes matching the published `SHA256SUMS`;
- **the substantive repair test, on the downloaded wheel**, in a clean venv, from a cwd with no
  `schemas/`: a valid bundle → `exit 0`, `findings: []`, `schema_source.mode: INSTALLED` resolving
  into `…/site-packages/pipd_ls_sp/schemas` (CE-1); and undeclared-`trace` bundles for **PD-PKG,
  ECP and TQAEP each → `exit 1` with a finding naming `trace`** (trace-widening);
- the local regression module read-only: **9 tests ran, 9 passed**.

It failed the run **because `git status --porcelain` was not empty** — reporting
`.hgk/rounds/R8-20261011-s4-main-consolidation/`, i.e. **this round's own untracked directory**,
which I created before launching the audit. The checker could not distinguish "the release is
dirty" from "the auditor's harness left an untracked file", and it was right not to try.

**This is a harness artifact, not a finding against the release.** It is reported rather than
smoothed over. What it means concretely: this run's verdict establishes everything above **except**
worktree cleanliness, and a re-run from a committed tree is what would convert that gate to PASS.

## What the checker said it could NOT verify (its own list)

1. A clean local worktree cannot be certified: the observed porcelain output is nonempty.
2. Equality of the preview.1 ref today does not prove the tag was never moved and restored
   historically.
3. `SHA256SUMS` has no self-entry or independently supplied expected digest; only the assets it
   lists were authenticated against its contents (i.e. it is self-consistent, not externally pinned).
4. The broader `G_RELEASE_FULL_PASS` designation, the full test suite, S5 runtime qualification,
   production readiness, and the historical pre-repair `FileNotFoundError` were not independently
   exercised.

Its claim ceiling, verbatim:

> This verdict covers only the observed public refs and release metadata, four downloaded assets,
> fresh downloaded-wheel schema-resolution and trace-rejection tests, nine local regression tests,
> worktree status, and protected-tree byte preservation at audit time; it grants no broader release
> or production qualification.

## Claim ceiling for this record

`PUBLISHED_PREVIEW2_INDEPENDENTLY_CROSS_MODEL_RE_DERIVED` — scoped to: the published refs, the
published assets' bytes, the installed-wheel behaviour of CE-1 and trace-widening, the nine
regression tests, and the provable non-mutation of the audited tree.

Not granted, and not implied: `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`,
`PRODUCTION_VERIFIED`, `S5_RUNTIME_READY`, any host certification, builder provenance for the
published wheel, that the wheel was built from the source commit its release body names, or that
the local registries equal the tagged build.
