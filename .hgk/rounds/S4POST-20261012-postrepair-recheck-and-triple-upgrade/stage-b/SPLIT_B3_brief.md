# Bounded writer — Stage B lane B3: install docs + verify workflow (SHORT RUN, no tool edits)

Allowed writes: `docs/install/README.md`, `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` (both new),
`.github/workflows/public-plugin-verify.yml` (new), and `README.md` (install entry points only).
Do NOT edit any file under `tools/`, `tests/` or `packaging/`.

`docs/install/README.md` - one install SSOT: the Web route, the Agent route, the Web fallback and
its DOC_MOUNT_ONLY limit, and the explicit statement that no public directory listing exists yet so
the fallback is the current Web route.
`docs/install/PIPD_AGENT_INSTALL_PROMPT.md` - one copy-paste prompt that makes a host detect itself,
show the exact paths and diffs, ask for consent, verify REAL discovery rather than file presence,
and report NOT_VERIFIED when only files were copied.
`.github/workflows/public-plugin-verify.yml` - `permissions: contents: read`, SHA-pinned actions, no
`pull_request_target`, no secrets, no tag or publish step, and a negative step that FAILS CLOSED:
require the suite green first, require an actual test failure after the mutation, and require the
failure motive (not merely a non-zero exit). Validate the YAML parses.
`README.md` - only the two install entry points plus a pointer to `docs/install/`.

Finish by pasting verbatim: the YAML parse result, and the lines you added to README.md.
