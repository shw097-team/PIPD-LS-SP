# Design — R5 S4 normal-user operability repair

## Context

`pipd` is a 13-command pre-execution compiler (總藍圖 §5.9.3). The S4 stage is "a normal user can run the
path end to end on this machine without knowing any internal name". The R4 challenge found that two of
the three P0/P1 defects sit on that path, and that the artefact a user would install is not the artefact
the source tree describes.

## Decision 1 — one resolver, refusal before effect

A single `resolve_output_destination(root, out, *, authorized_roots=None, allow_replace=None)` lives in
`projection.py` (the module that owns surface generation) and is called by both `project` and `export`.
The ordering that matters is: **normalise → refuse → stage → verify → publish**. The old code ordered it
**delete → create → write**, which is why a bad `--out` was destructive rather than rejected.

Denied by construction, case-insensitively on the resolved path:

| Denied class | Why |
|---|---|
| `None` / empty / whitespace | nothing to resolve; an empty `--out` must never fall back to a default |
| leading `/` that is not UNC (`/c/...`, `/tmp/x`) | on Windows that resolves *drive-relative* to `C:\c\Users\...`, i.e. a different directory than the user typed |
| cwd, `Path.home()`, the drive/filesystem root (`resolved.anchor`) | the three catastrophic delete targets |
| the source `root`, any ancestor of `root`, and any descendant at or above cwd | deletes the tree being compiled, or its parent |
| symlink/junction/reparse escape out of an authorised root | TOCTOU-free containment, re-checked at publish |
| a target outside every authorised root, when roots are supplied | "foreign absolute dir" |
| an existing non-empty target when `allow_replace` is false | silent data loss |

`allow_replace=None` resolves to `True` for trusted in-process callers (the documented regeneration
contract) and `False` for the user-facing CLI, so hardening the CLI cannot break the internal tools.

The refusal type is `UnsafeDestination(ProjectionError)` with `code = "UNSAFE_DESTINATION"`; it reaches
`cli.main`'s existing `PipdError` handler and becomes a typed JSON envelope with exit 2.

## Decision 2 — staged publish with a kept backup

```
stage = target.parent / f".{target.name}.pipd-stage-<token>"
write everything into stage -> run existing strict gates against stage
if target exists: os.replace(target, target.pipd-backup-<token>)   # kept
os.replace(stage, target)                                          # atomic, same volume
on failure after the backup move: restore the backup to the original name
```

No `shutil.rmtree` is ever called on a caller-supplied path. The stage directory is a sibling on the same
volume so the final move is an atomic rename, not a cross-device copy.

Generated surfaces carry a `.pipd-generated-surface.json` marker (schema, source root, timestamp). The
marker is excluded from the Web/Host/IR denominators so the 5/5 and 3/3 counts keep their meaning.

## Decision 3 — schemas travel inside the package

`registry._root()` currently returns the *repository* root. Installed, that path does not exist, so a
fresh `pip install` yields a CLI that cannot load its own registry. The resolver becomes, first match
wins: `$PIPD_SCHEMAS_DIR` → `importlib.resources.files("pipd_ls_sp") / "schemas"` → `<repo>/schemas`.
`tools/build_dist.py` maps the repository `schemas/` tree into `pipd_ls_sp/schemas/` inside the wheel, so
the packaged copy is the same 19 files. A miss raises the existing typed `ValidationFail` listing every
location tried, which is the honest failure a user can act on.

## Decision 4 — `export --out` gets a real side effect

`export` gains the same destination resolver plus a bundle writer: a deterministic archive, a manifest
with `rel`/`size`/`sha256` per member, and a checksum file. `--dry-run` prints the plan and writes
nothing. A read-only stdout mode stays separate and explicitly named, so the "did it write?" question
never has an ambiguous answer.

## Decision 5 — acceptance binds to the frozen subject

The acceptance matrix records, per case: frozen commit/tree, wheel sha and selected member shas, exact
argv, stdout/stderr/exit, before/after canaries, and the checker identity. Source-import results and
installed-wheel results are separate columns; a green source run never stands in for an install run.
Dangerous-destination negatives run only against disposable scratch trees — never against the product
working tree.

## Risks and their mitigations

| Risk | Mitigation |
|---|---|
| Over-hardening breaks the internal tools' regeneration contract | `authorized_roots=None` keeps replace-default for in-process callers; only the CLI is strict |
| A stricter resolver rejects legitimate scratch output | positives are exercised against dedicated disposable scratch roots in the same suite |
| The wheel build silently ships stale `schemas/` | member SHAs are recomputed from the zip and compared to the source file SHAs |
| `export` overlaps `project`'s destination logic | one shared resolver, one shared refusal type, no second code path |

## Out of scope

S5 receiver execution, S6 GENIE, S7 JIT, S8 SGM promotion, the 22 un-adopted technology pins, the global
153/160 knowledge sanitisation, the S2 threshold provenance (owner-gated), and any redesign of the 19
schemas / 8×6 Skills / 5 Web documents / 3 Host mocks.
