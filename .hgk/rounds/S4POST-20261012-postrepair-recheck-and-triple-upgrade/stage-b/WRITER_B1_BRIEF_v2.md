# Bounded writer — Stage B lane B1 (resumed round): packaging tests + local schema subset

You are a **bounded writer** working in `C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt`
(branch `feat/s4post-triple-upgrade-20261012`). Change ONLY files under "Allowed write set".

## Allowed write set (absolute)
- `tests/test_public_plugin_packaging.py`  (new)
- `packaging/public-plugin/plugin.schema.json`  (new)
- `tools/freeze_public_plugin_source.py`   (fix only where a test proves it wrong)
- `tools/build_public_plugin.py`           (fix only where a test proves it wrong)

Forbidden: `skills/**`, `src/**`, `schemas/**`, `dist/**`, `.hgk/**`, `README.md`, `docs/**`,
`.github/**`, `tests/test_web_fallback.py`, any other test module, git history, commit, push, tag.

## Read first
`tools/freeze_public_plugin_source.py`, `tools/build_public_plugin.py`,
`packaging/public-plugin/plugin.json`, `packaging/public-plugin/derivations.json`.
Both tools are stdlib-only by design. Keep it that way: **no new dependency, no network**.

## Deliverable 1 — `packaging/public-plugin/plugin.schema.json`
A local, digest-pinnable JSON-Schema (draft 2020-12) **subset** that mirrors the constraints the
builder enforces on the manifest, and nothing more: the top-level keys used by
`packaging/public-plugin/plugin.json` (`schema`, `plugin_id`, `display_name`, `version`, `license`,
`skills`, `official_schema_sha256`, `publisher`, `icons`, `release`), with `additionalProperties:
false` at every level, `skills` constraining its eight exact names, and the publisher/icon objects
requiring their fields. State in the file's `description` that it is a LOCALLY AUTHORED SUBSET and
that the vendor schema and the vendor validator remain NOT_EXECUTED. It must parse with the
builder's own `validate_subset` (see `build_public_plugin.py`) and must NOT be claimed to be the
official vendor schema.

## Deliverable 2 — `tests/test_public_plugin_packaging.py`
stdlib `unittest`, temp-directory fixtures, **no network, must never touch the real repo tree**,
must not write under `dist/` or `.hgk/`. Every case must call the real `build_plugin(...)` /
`freeze(...)` functions - never a re-implementation.

Cases (each must be a green test AFTER the code is fixed; the failures are the historical red cases):
1. fake PNG: a valid 8-byte PNG signature followed by a broken body is REFUSED; also a non-PNG file
   is REFUSED. The refusal is `ICON_INVALID` (or a typed refusal of the same kind) and no ZIP is
   produced.
2. unknown plugin-manifest property (`"custom": ...`) is REFUSED as a manifest-schema violation.
3. invalid SKILL frontmatter (no frontmatter / wrong `name`) is REFUSED.
4. `source_commit` null, too short, or not matching the ledger commit is REFUSED
   (`SOURCE_COMMIT_NULL` / `SOURCE_COMMIT_INVALID` / `SOURCE_COMMIT_MISMATCH`).
5. a symlinked output release directory is REFUSED **and the sentinel file behind the symlink is
   byte-identical afterwards**.
6. an extra file inside a skill that is absent from the frozen ledger is REFUSED
   (`SOURCE_SET_CHANGED`) and so is a missing one.
7. a ninth skill directory is REFUSED (`UNEXPECTED_SKILL`).
8. a symlinked / non-regular source member is REFUSED.
9. a dirty worktree at freeze time is REFUSED (`DIRTY_WORKTREE`) - drive the real `freeze()`.
10. two builds from identical inputs are byte-identical: same member set AND order AND per-member
    bytes AND the ZIP sha256; assert the fixed metadata (1980-01-01, 0644, DEFLATED 9).
11. a missing owner derivation record is REFUSED (`OWNER_INPUT_MISSING`), and the refusal is a
    **non-zero exit** through `main()` - assert both the typed code and the exit code.
12. with a complete owner record (matching `source_sha256`, an `approved_by` and an
    `approval_receipt` that are not placeholders) the build SUCCEEDS and the projected `SKILL.md`
    **body is byte-identical** to the source body while only the approved keys move; assert the
    mapping row says `DERIVED_WITH_OWNER_APPROVAL` and that the receipt says
    `claim_ceiling: LOCAL_PACKAGER_PASS_ONLY` and `official_portal_verification: NOT_EXECUTED`.
13. an output root that overlaps the source repo is REFUSED, and so is writing into `dist/`.
14. owner placeholders (`OWNER_INPUT_REQUIRED`) in the publisher identity / icon digest / official
    schema digest each REFUSE.

## Rules
- If a test exposes a real tool defect, FIX THE TOOL. Never weaken an assertion to match the code.
- Do not edit `tests/__init__.py` or add fixtures outside your write set.
- Finish by pasting VERBATIM into your final message: the exact command and its summary line for
  `python -m unittest tests.test_public_plugin_packaging -v`, then for
  `python -m unittest discover -s tests -t .` (the second may be long: paste only its final
  `Ran N tests ... OK/FAILED` line). Also paste the exact typed refusal string the builder prints
  for a missing owner derivation record.
