## Context

`validate` and `doctor` answer the same question — "where are the canonical schemas?" — with two different
mechanisms. That divergence is the whole of CE-1. CE-2 is narrower: a documented stripping step was
implemented in the hashing path and forgotten in the schema-checking path.

## Decisions

### D1 — One resolver, and the workspace still wins when it is real

`validate` goes through the registry resolver rather than a bare `root / "schemas"`. A workspace-local
`schemas/` directory is prepended **only if it contains `registry.json`**, so in-tree development and the
canonical resolution order both keep working. Making the whole `--root/schemas` path an unconditional
first candidate would have let an arbitrary directory shadow the shipped schemas — a silent
wrong-schema failure, which is worse than the loud one being fixed.

### D2 — The sidecar list is a single object, not a repeated literal

The fix for CE-2 is small, but the *reason* it happened is that a five-element list was written by hand in
more than one place and one copy drifted. The repair therefore defines the list once and imports it
everywhere, and a test asserts the two modules reference the same object, so a future copy-paste fails
loudly instead of silently reintroducing the defect.

### D3 — No schema edits, no artefact edits

Adding `_profile_meta` to `PI-PKG.schema.json` would be a canonical contract change and would alter the
schema set inside the wheel; removing the sidecar from the emitted PI-PKG would break
`tools/run_s1_slice.py`, which reads `pi["_profile_meta"]["profile"]`. Both are larger than the defect.
The project's own convention, stated in `pipeline.py`, is that SoD/ceiling data lives inside declared
fields and schemas are not edited to accommodate a sidecar.

### D4 — The published tag stays frozen

`OWNER_LICENSE_DECISION.yaml` records that published tags are never rewritten and a superseding release is
issued instead. This change is therefore a candidate for the *next* release, not a rewrite of
`v0.1.0-preview.1`.

## Risks

- **Wrong-binary risk.** A repaired `src/` does not retroactively change the published wheel. A reader who
  installs `v0.1.0-preview.1` still meets CE-1/CE-2. The public disclosure must say "fixed on the next
  release", not "fixed".
- **Shadowing risk.** Mitigated by D1: a `root/schemas` candidate is accepted only with `registry.json`
  present.
- **Test-only green.** Mitigated by requiring the red state to be captured before the fix and by an
  end-to-end check that runs the installed wheel from outside the repository with unmodified compiler
  output.

## Migration

None. No schema, no data and no published artefact changes shape.
