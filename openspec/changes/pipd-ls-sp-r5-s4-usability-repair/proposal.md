# R5 S4 — normal-user operability repair for `pipd project` / `export` / the distributable wheel

## Why

The R4 external challenge report (`PIPD_LS_SP_R4_S4_User_Usability_PostRepair_External_Acceptance_2026-10-09`)
returned `FAIL_CHALLENGE` on the S4 *normal-user* main path of `shw097-team/PIPD-LS-SP@cd8a06e`, with three
`CONFIRMED_DEFECT`s, one `EVIDENCE_GAP` and one standing Gate `FAIL`:

| Finding | Class | Substance |
|---|---|---|
| `F-R4-S4-01` / `S4-USER-SEC-001` | CONFIRMED_DEFECT **P0** | `project_surfaces()` does an unvalidated `shutil.rmtree(out)` on a caller-supplied `--out`; `pipd project --out <anything>` can recursively delete the repo root, cwd or home before any safety check runs |
| `F-R4-S4-02` / `S4-USER-DIST-002` | CONFIRMED_DEFECT **P0** | the published wheel is the R2 build (`candidate_head=829c17e…`, 60,980 B, no `requirements.py`/`repo_context.py`/`projection.py`, no `schemas/`); `registry._root()` resolves outside the package so an installed `pipd` cannot load its own registry |
| `F-R4-S4-03` / `S4-USER-EXPORT-003` | CONFIRMED_DEFECT **P1** | `pipd export --out` ignores `args.out` and returns an in-memory dict; no archive, manifest or checksums ever land |
| `F-R4-S4-04` | EVIDENCE_GAP **P1** | no end-user acceptance matrix is bound to the same frozen subject the wheel is built from |
| `F-R4-S2-05` | GATE FAIL **P1** | context budget 343,547 > 20,000 with unprovenanced thresholds — stays FAIL, must remain visible |

The user-visible consequence is a CLI whose *help* works and whose *destructive* path does not refuse.

## What changes

- **Safe output destination (P0).** One shared `resolve_output_destination()` used by `project` and
  `export`: refuse *before* any create/delete — empty, POSIX/MSYS `/c/…` forms, cwd, home, drive root,
  the source root and its ancestors/descendants, symlink/junction escapes, foreign absolute directories,
  and preexisting non-empty targets without explicit replacement authorisation. Publish by
  stage → verify → atomic replace with the previous tree renamed to a reported `.pipd-backup-<token>`
  (kept, never deleted). A refusal is a typed `UNSAFE_DESTINATION` envelope with a non-zero exit, and
  `--dry-run` runs the *same* resolver while writing nothing anywhere.
- **Real distributable (P0).** `tools/build_dist.py` builds a deterministic wheel that carries every
  current module **and** the 19 schemas inside the package; `registry` resolves its schema tree through
  `importlib.resources` with an explicit `$PIPD_SCHEMAS_DIR` override and a source-tree fallback, so an
  installed `pipd` is self-sufficient. `WHEEL_MANIFEST.json` records the frozen source identity and a
  recomputable product digest; the R2 wheel is refused as an R4/R5 distribution.
- **Real `export --out` (P1).** `export` lands an actual portable archive + manifest + per-member
  SHA-256, deterministically ordered and byte-replayable, staged and scanned before publication; the
  read-only stdout mode stays a distinct, explicitly named mode.
- **S4 end-user acceptance.** UAT-00…12 executed against a fresh isolated install *and* against a source
  import, on three profiles, with two fresh-process replays and the dangerous-destination negatives run
  only in disposable scratch trees.

## Design notes / non-goals

No package-local redesign, no S5–S8 work, no second control plane, no rewrite of the 19 schemas, the
8×6 Skill pack, the 5 Web documents or the 3 typed Host mocks. `G-S2-LOCAL` stays `FAIL`; the S4 result
may be reported as `PARTIAL` at the global level while S4-local safety, install and export are closed.

## Claims

Repair Maker ceiling: `S4_REPAIR_CANDIDATE_LOCAL_TESTED`. `PROMPT_COMPILE_PASS`, `RUNTIME_READY`,
`INDEPENDENT_PASS`, `PUBLICATION_APPROVED`, `RELEASED` and `PRODUCTION_VERIFIED` do not inherit.
