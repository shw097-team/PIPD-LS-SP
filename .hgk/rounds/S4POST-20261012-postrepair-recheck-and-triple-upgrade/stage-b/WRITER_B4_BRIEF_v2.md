# Bounded writer — Stage B lane B4 (resumed round): official Agent Plugins manifest conformance

You are a **bounded writer** working in `C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt`
(branch `feat/s4post-triple-upgrade-20261012`). Change ONLY files under "Allowed write set".

## Why this lane exists (measured, not assumed)
The round downloaded the REAL vendor schema (Agent Plugins 1.0.0) to
`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/vendor/plugin.schema.json`,
sha256 `0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883`, 1805 bytes.
Its constraints: `required: ["$schema","name"]`, `additionalProperties: false`, and the ONLY permitted
top-level properties are `$schema, name, version, description, author, homepage, repository, license,
keywords, extensions`. `name` must match `^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$` with no `--` and no `..`.

The manifest currently emitted as the package root
(`packaging/public-plugin/plugin.json`, schema id `PIPD-PUBLIC-PLUGIN-MANIFEST/1`, keys
`plugin_id/display_name/skills/official_schema_sha256/publisher/icons/release`) is PIPD's OWN internal
manifest. **As the plugin root `plugin.json` it would be REJECTED by the vendor schema.** That is the
gap this lane closes: the package must carry a real Agent Plugins 1.0 root manifest, and PIPD's own
release bookkeeping must move into the vendor-blessed `extensions` namespace.

## Allowed write set (absolute)
- `packaging/public-plugin/plugin.json`              (rewrite as the official-shaped manifest)
- `packaging/public-plugin/plugin.release.json`      (new - PIPD's internal release bookkeeping)
- `packaging/public-plugin/vendor-plugin.schema.json` (new - a byte copy of the downloaded vendor schema)
- `tests/test_public_plugin_packaging.py`            (extend; do not delete existing cases)
- `tools/build_public_plugin.py`                     (fix where a test proves it wrong)
- `docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md` (new, short)

Forbidden: `skills/**`, `src/**`, `schemas/**`, `dist/**`, `README.md`, `docs/install/**`, `.github/**`,
`tests/test_web_fallback.py`, `tools/build_web_fallback.py`, `tools/freeze_public_plugin_source.py`
(read it, do not edit unless a test proves it wrong), git history, commit, push, tag.

## Required behaviour
1. **Two manifests, one package.** The file emitted INSIDE the ZIP as
   `<plugin_id>/plugin.json` must be the official-shaped manifest:
   `{"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": "<plugin name>",
   "version": "<semver>", "description": "...", "repository": "...", "license": "Apache-2.0",
   "keywords": [...], "extensions": {"com.pipd.s4": {...}, "com.openai": {"interface": {...}}}}`.
   PIPD's own release bookkeeping (claim ceiling, portal state, publisher identity record, icon
   digests, the eight skill names, the pinned vendor-schema digest) moves into
   `extensions["com.pipd.s4"]` inside that manifest AND/OR into `plugin.release.json` - your call, but
   the official keys must validate.
2. **Vendor schema lock.** `packaging/public-plugin/vendor-plugin.schema.json` must be a byte copy of
   the downloaded vendor schema, and the builder must (a) require the manifest's `$schema` to equal the
   vendor `$id`, (b) validate the official manifest against the vendor schema with the builder's OWN
   stdlib subset validator (no new dependency), and (c) REFUSE (`VENDOR_SCHEMA_DIGEST_MISMATCH`) when
   the pinned digest does not match the bytes it validated against. Record the pinned digest in the
   manifest's `extensions["com.pipd.s4"]` and in `plugin.release.json`.
   Also REFUSE when the vendor schema's `$id` is not the expected one, and REFUSE an official manifest
   that carries an unknown top-level key (that is the `additionalProperties: false` case).
3. **Owner gates unchanged.** The build must still refuse, in this order, on: missing per-skill
   derivation record, unpinned official/vendor schema digest, unpinned publisher identity, unpinned or
   invalid icon. Keep every existing typed refusal code meaningful; add new codes only where a new
   gate is genuinely new.
4. **Tests.** Extend `tests/test_public_plugin_packaging.py` with: the official manifest validates
   against the vendor schema; an unknown top-level key in the official manifest is REFUSED; a
   mismatch between the pinned vendor digest and the bytes is REFUSED; `name` violating the vendor
   pattern is REFUSED; and the ZIP read-back proves the member named `<plugin_id>/plugin.json` is the
   official-shaped one. Keep every previously green case green.
5. **ADR** (`docs/adr/ADR-0001-public-plugin-manifest-and-derivation.md`, <= 60 lines): record that
   (i) the package root manifest is the official Agent Plugins 1.0 manifest validated against the
   locked vendor schema bytes; (ii) the eight SKILL.md packs carry non-portable frontmatter
   (`version/owner/triggers/schemas/references/tests`), the Agent Skills specification lists exactly
   `name/description/license/compatibility/metadata/allowed-tools`, therefore every skill needs an
   owner-approved derivation record and the build REFUSES without one; (iii) the icon is generated
   deterministically in-repo with a stdlib PNG writer rather than committed as an opaque binary, with
   the residual that owner brand assets and the vendor's own validator / Portal scan remain
   NOT_EXECUTED; (iv) no third-party build dependency is used (stdlib-only validator, PNG decoder and
   YAML-free frontmatter parser), which deviates from the blueprint's Pillow/jsonschema/PyYAML
   proposal and is disclosed as such.

## Rules
- stdlib only; no new dependency; no network. Do not read the network.
- Never weaken an assertion to make code pass; fix the code.
- Finish by pasting VERBATIM: the command and summary line of
  `python -m unittest tests.test_public_plugin_packaging -v`, the final `Ran N tests ... OK/FAILED`
  line of `python -m unittest discover -s tests -t .`, and the exact refusal string for a vendor
  schema digest mismatch.
