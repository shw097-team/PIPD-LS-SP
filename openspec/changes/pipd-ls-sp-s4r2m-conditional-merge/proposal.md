# pipd-ls-sp-s4r2m-conditional-merge

## Why

The 2026-10-11 external read-only challenge review
(`PIPD_LS_SP_S4_MVP_PostRelease_S4R2_Independent_Acceptance_and_Preview3_Gate_2026-10-11`)
concluded `GO_CONDITIONAL` for merging the S4-R2 repairs into `main`, `VALUE_POSITIVE / CONDITIONAL GO`
for a later `preview.3`, and `PARTIAL_CHALLENGE` for the machine gates. It named exactly two
documentation blockers before integration: the front page never routes a reader between the CLI path
and the Skills path, and it states the `--root` option's position more absolutely than the shipped
argparse surface behaves. It also required one focused, isolated regression of the frozen product
before any integration, and left the public wheel unchanged until an owner-selected release gate.

## What Changes

- The front page gains one short section that separates the two consumer paths — a pinned wheel for a
  CLI / headless harness, and a versioned document pack for web document consumption — and states each
  path's real capability boundary, including that a wheel install does not load native web skills.
- The `--root` text is corrected to the behaviour the CLI actually has: the global position for the
  compile chain, and the additional subcommand-local form for `project` and `export`.
- One focused regression runs the six named affected test modules plus the exact-set oracles in a
  disposable writable clone, while the read-only checker subject keeps identical bytes.
- `main` receives the approved candidate through a non-rewriting fast-forward under owner approval,
  with a remote ref readback; `v0.1.0-preview.2` stays immutable and publicly served.
- A `preview.3` release gate exists but is only executed if the owner selects it.

## Non-goals

- No 20th schema family, no 9th logical Skill, no 14th CLI command.
- No rewrite of the frozen S4-R2 product commit, the sealed preview tags or their assets.
- No S5–S8 activation, no second control plane, no competing canonical store.
- No re-opening of the four already-closed ProfileBinding mutants, and no version-grammar regex added
  ahead of a declared version contract.

## Impact

- Affected specs: `pipd-s4r2m-conditional-merge`
- Affected code: `README.md`, `tests/test_s4r2m_docs_route.py`
- Untouched: `v0.1.0-preview.2` tag, commit and wheel; the 19-schema set; the 8 logical skills;
  the 13-command CLI surface.
