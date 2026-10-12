# Bounded writer brief — Stage B CONTINUATION (the previous run was stopped mid-flight)

Your previous run was interrupted after producing three tools. They exist and parse:
`tools/freeze_public_plugin_source.py`, `tools/build_public_plugin.py`, `tools/build_web_fallback.py`.
**Nothing else from the brief exists**: no test modules, no `docs/install/`, no
`.github/workflows/public-plugin-verify.yml`, and the required README entry points are unconfirmed.

Allowed write set (unchanged, plus the missing files):
`tools/{freeze_public_plugin_source,build_public_plugin,build_web_fallback}.py`,
`tests/{test_public_plugin_packaging,test_web_fallback}.py`, `packaging/public-plugin/**`,
`docs/install/**`, `README.md` (install entry points only),
`.github/workflows/public-plugin-verify.yml`. **Never** `skills/**`, `src/**`, `schemas/**`, `dist/**`.

## Do this, in order

1. **Read your own three tools** and check them against the requirements below. Where a tool does
   not already behave as required, fix the TOOL — never weaken a requirement to match the code.
2. Write the two test modules. They must be stdlib-only, must build fixtures in a temp directory
   (never against the real repo), must not use the network, and must assert **everything** below:
   - fake PNG (valid 8-byte magic, invalid body) refused; a non-PNG refused;
   - an extra/unknown plugin manifest property refused;
   - invalid SKILL frontmatter refused;
   - a null, short or mismatched source commit refused (40-hex enforced);
   - a symlinked release directory refused **and the sentinel file behind it left untouched**;
   - a changed source set refused (`source set changed`), a ninth skill refused, a symlinked or
     non-regular source file refused, a dirty worktree refused;
   - determinism: two builds byte-identical, member set and order identical;
   - derivation without an owner record refused; with an owner record accepted **and the SKILL.md
     body byte-identical** (only the approved keys differ);
   - the builder refuses to write into `dist/`, and refuses an output root overlapping the repo;
   - web fallback: exact projection, stale release stamp refused, bad source digest refused,
     **no truncation** (over-cap input refused, not shortened), symlinked destination refused with
     the sentinel intact, existing destination refused.
3. Write `docs/install/README.md` (one install SSOT: Web route, Agent route, the Web fallback and
   its `DOC_MOUNT_ONLY` limit, and the explicit statement that no public directory listing exists
   yet), `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` (one copy-paste prompt: detect the host, show
   exact paths and diffs, ask consent, verify real discovery rather than file presence, report
   `NOT_VERIFIED` when only files were copied), and the two README entry points.
4. Write `.github/workflows/public-plugin-verify.yml`: `permissions: contents: read`, SHA-pinned
   actions, no `pull_request_target`, no secrets, no tag/publish step, and a negative step that
   **fails closed** — require the suite green first, require an actual test failure after the
   mutation, and require the failure motive to be the specific binding (not merely a non-zero exit).

## Fail-closed means fail-closed

The owner inputs are deliberately absent: `packaging/public-plugin/derivations.json` is empty and
there is no image asset anywhere in the repo. The builder must therefore **refuse to build** with a
typed, non-zero result and name the missing owner input. A warning, a default, or a synthesised
approval is a FAIL of this task. Generate any icon deterministically with a tiny stdlib PNG writer
(zlib + struct, no Pillow and no new dependency) and validate it by checking the signature, IHDR,
chunk CRCs and inflating IDAT; still refuse to emit a package while the owner inputs are missing.

## Finish with raw output, not prose

```
python -m unittest tests.test_public_plugin_packaging tests.test_web_fallback
python -m unittest discover -s tests -t .
python tools/build_public_plugin.py --help
python tools/build_public_plugin.py <a temp out dir>     # must refuse; paste the exact reason line
```
Paste the summary lines verbatim plus the exact refusal reason. No commit, no push, no tags, and do
not touch `dist/`.
