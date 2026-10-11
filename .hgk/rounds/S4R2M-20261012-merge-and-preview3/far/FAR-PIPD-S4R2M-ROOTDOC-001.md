# FAR-PIPD-S4R2M-ROOTDOC-001 — is the `--root` finding a CLI defect or a documentation defect?

- **Round:** `S4R2M-20261012-merge-and-preview3`
- **Question type:** adjudication of a known, already-registered finding (`S4R2-POST-F02` / Checker `V2R2-F01`)
- **Autonomy:** in-round FAR study, executed directly (owner authorisation: decide the lowest-resistance,
  highest-engineering-necessity resolution and carry it out)
- **Claim ceiling:** `LOCAL`

## The question

The challenge report says the front page's statement that `--root` is "GLOBAL and must precede the
subcommand" is an over-generalisation. Two readings are possible, and they have very different costs:

1. **CLI defect.** The parser should reject a subcommand-local `--root` everywhere, so the README is
   right and the CLI is wrong.
2. **Documentation defect.** The parser has a deliberate second position for two subcommands, so the
   README is wrong and the CLI is right.

## Evidence taken this round

Read directly from the candidate head `3f6c7dc52b73cfcba03dccbe576ade75bec1890d`
(`src/pipd_ls_sp/cli.py`):

- line 39: the top-level parser adds `--root` with `default=Path.cwd()`.
- lines 66–69: the `project` subparser adds `--root` with `dest="sub_root"` and an inline comment that
  states the intent — "`--root` is a global option, but accept it after the subcommand too so
  `pipd project --out ... --root <root>` is not a usage error."
- lines 75–79: the `export` subparser does the same.
- line 114: the dispatcher resolves `getattr(args, "sub_root", None) or args.root`.

Executed probe (the same four commands the writer lane ran, in a scratch directory outside the tree):

| form | exit |
|---|---|
| `pipd --root ./demo init` | 0 |
| `pipd project --root ./demo --dry-run` | 0 |
| `pipd export --root ./demo --dry-run` | 0 |
| `pipd init --root ./demo` (refused) | 2 |

## Decision

**Reading 2 — documentation defect only. No CLI or schema change is admitted.**

Reasons, in order of weight:

1. The second position is not an accident: it is commented as intentional and it is scoped to exactly
   the two subcommands whose destination is an output path the user may want to name independently of
   the workspace root. Removing it would be a backwards-incompatible surface removal.
2. A removal would also invalidate the already-published `v0.1.0-preview.2` documented behaviour while
   adding no user-visible capability. The narrow repair principle (`PKG-09` affected-only) forbids it.
3. The report itself classifies the finding as `CONFIRMED_DEFECT` against the *README*, with the fix
   being a `P2 tiny` prose change in the same patch as `F01` — not a source change.

The admitted change is therefore: replace the absolute sentence with one that names the two groups of
commands, and keep three documented positives plus one documented refusal, all executed.

## What this decision does not confer

- It does not assert that the CLI's option surface is otherwise correct or documented fully.
- It does not close the broader question of whether a future major version should unify option
  placement; that would be a separate, breaking `UPGRADE` change with its own compatibility analysis.
- It does not modify the frozen product commit, the shipped wheel or any published asset.
