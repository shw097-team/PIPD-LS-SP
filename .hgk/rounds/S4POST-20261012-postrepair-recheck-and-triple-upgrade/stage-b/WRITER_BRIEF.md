# Bounded writer brief — Stage B: public Skills-only plugin projection (S4POST round)

You are a **bounded writer**. Change ONLY files under "Allowed write set". Everything else —
`skills/**`, `src/**`, `schemas/**`, `dist/**`, `.hgk/**`, any existing release asset — is
forbidden. If the work seems to need a change outside the set, stop and report instead.

## Goal

Turn the existing eight skills into a **portable, deterministic, fail-closed plugin package
candidate**, plus a single-file web fallback and installation routes. Nothing here publishes
anything: the deliverable is a *candidate* whose owner-gated inputs are missing on purpose and must
make the build REFUSE rather than warn.

## Ground truth you must respect (already measured, do not re-litigate)

- `skills/pipd-*`: 8 skills, exactly 6 files each, 48 files total, no deviations.
- **Every** `SKILL.md` frontmatter carries the non-portable keys `version`, `owner`, `triggers`,
  `schemas`, `references`, `tests`. None of the eight is a subset of the portable set
  {name, description, license, compatibility, metadata, allowed-tools}. Therefore a byte-copy
  projection is **impossible**: each skill needs an owner-approved derivation record.
- **No image asset exists anywhere in the repo.** Do not add a binary PNG. Generate the icon
  deterministically from a tiny stdlib PNG writer (zlib + struct, no Pillow, no new dependency) and
  validate it by decoding the signature, IHDR, chunk CRCs and inflating IDAT.
- `dist/` holds 41 tracked release assets and must not be written.
- No `packaging/`, no `docs/install/`, no `plugin.json` exists yet.

## Allowed write set

- `tools/freeze_public_plugin_source.py` (new)
- `tools/build_public_plugin.py` (new)
- `tools/build_web_fallback.py` (new)
- `tests/test_public_plugin_packaging.py` (new)
- `tests/test_web_fallback.py` (new)
- `packaging/public-plugin/plugin.schema.json` (new — a local, digest-pinnable schema subset)
- `packaging/public-plugin/plugin.json` (new — candidate manifest with owner placeholders)
- `packaging/public-plugin/derivations.json` (new — empty by design)
- `packaging/public-plugin/assets/` (generated only, never committed as opaque binaries)
- `docs/install/README.md`, `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` (new)
- `README.md` (modify: only the install entry points)
- `.github/workflows/public-plugin-verify.yml` (new)

## Required behaviour

1. **`freeze_public_plugin_source.py`** — emit a frozen source ledger from a clean checkout: repo,
   commit (40 hex), tree (40 hex), the exact eight skill names, and `path -> sha256` for every file
   under them, refusing a dirty worktree, a wrong skill set, a symlink or any non-regular file.
2. **`build_public_plugin.py`** — build the plugin ZIP deterministically:
   - refuse when any owner input is missing: a per-skill derivation record whose `source_sha256`
     matches the frozen ledger, the pinned official-schema digest, the publisher identity, or the
     icons. **Refusal means non-zero exit with a typed reason, never a warning.**
   - refuse any file outside the frozen ledger, any ninth skill, any hidden/special member, and any
     output root that overlaps the repo or is world-writable.
   - fixed ZIP metadata (1980-01-01, mode 0644, DEFLATED level 9) so two builds are byte-identical;
     read the archive back and compare every member before promoting it.
   - emit `SOURCE_TO_PLUGIN_MAPPING.json` (per source file: source sha, destination sha, mode
     EXACT or DERIVED_WITH_OWNER_APPROVAL) and `RELEASE_RECEIPT.json` with
     `claim_ceiling: LOCAL_PACKAGER_PASS_ONLY`, `official_portal_verification: NOT_EXECUTED`.
   - the derived SKILL.md projection must keep the body byte-identical and move only the approved
     keys; assert the body is unchanged.
3. **`build_web_fallback.py`** — one bounded, byte-complete markdown document from a frozen mount
   pack: refuse a manifest/digest mismatch, a symlink, a path escape, an unexpected extra file, a
   document that does not stamp the release identity, and an output above the size cap (**no
   truncation**); write with `O_EXCL` and refuse an existing or symlinked destination; stamp
   `DOC_MOUNT_ONLY` and the member inventory.
4. **Tests** — `tests/test_public_plugin_packaging.py` must include, as green cases after the code,
   the historical red cases: fake PNG (valid magic, invalid body) refused; an extra manifest property
   refused; invalid SKILL frontmatter refused; null or mismatched source commit refused; a symlinked
   release directory refused **with the sentinel file untouched**; an extra source file refused
   ("source set changed"); a ninth skill refused; determinism over two builds; derivation without an
   owner record refused and with a record accepted with the body unchanged; output overlapping the
   repo refused; writing into `dist/` refused.
   `tests/test_web_fallback.py` must cover: exact projection, stale release stamp refused, no
   truncation, bad source digest refused, symlinked destination refused with sentinel intact.
   Tests must be stdlib-only and must not touch the network or the real repo tree (build fixtures in
   a temp directory).
5. **`docs/install/README.md`** — one install SSOT: the Web route and the Agent route, the Web
   fallback with its `DOC_MOUNT_ONLY` limit, and an explicit statement that no public directory
   listing exists yet (so the fallback is the current Web route). **`docs/install/PIPD_AGENT_INSTALL_PROMPT.md`**
   — one copy-paste prompt that makes the host detect itself, show the exact paths and diffs, ask for
   consent, verify real discovery (not file presence) and report `NOT_VERIFIED` when only files were
   copied.
6. **`README.md`** — only the two install entry points plus a pointer to `docs/install/`. Do not
   restate the whole manual.
7. **`.github/workflows/public-plugin-verify.yml`** — read-only (`permissions: contents: read`), SHA-pinned
   actions, no `pull_request_target`, no secrets, no tag/publish step; installs declared deps only,
   runs the two new test modules, and adds a **negative step that fails closed**: it must require the
   suite green first, require an actual test failure after the mutation, and require the failure motive
   to be the specific binding (not merely a non-zero exit).

## Rules

- stdlib only; no new dependencies; no network.
- No git history changes, no commit, no push, no tags; do not touch `dist/`.
- Your own repo-writing must stay inside the allowed set.
- Finish with the raw summary lines of
  `python -m unittest tests.test_public_plugin_packaging tests.test_web_fallback` and of the full
  `python -m unittest discover -s tests -t .`, plus the exact reason string the builder prints when
  the owner inputs are missing.
