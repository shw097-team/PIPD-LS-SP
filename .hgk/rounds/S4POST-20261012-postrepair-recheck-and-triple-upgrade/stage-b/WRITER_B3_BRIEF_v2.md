# Bounded writer — Stage B lane B3 (resumed round): install docs, verify workflow, README routes

You are a **bounded writer** working in `C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt`
(branch `feat/s4post-triple-upgrade-20261012`). Change ONLY files under "Allowed write set".

## Allowed write set (absolute)
- `docs/install/README.md`                      (new)
- `docs/install/PIPD_AGENT_INSTALL_PROMPT.md`   (new)
- `.github/workflows/public-plugin-verify.yml`  (new)
- `README.md`                                   (install entry points only - replace the install
  section's route list; do not restate the manual, do not delete the existing history/licence text)

Forbidden: `tools/**`, `tests/**`, `packaging/**`, `skills/**`, `src/**`, `schemas/**`, `dist/**`,
`.hgk/**`, git history, commit, push, tag.

## Ground truth you must respect
- The eight skills are `skills/pipd-{route-intake,authority-source,profile-tailor,pi-compile,pd-bind,execution-contract,assurance-tqaep,package-project}`; each has 6 files.
- **No public plugin directory listing exists yet** (no release has been published). So the Web route
  today is the single-document fallback, plus the *conditional* Directory route for the future.
- The web fallback file is produced by `tools/build_web_fallback.py` into a single
  `PIPD_WEB_FALLBACK.md`; its ceiling is `DOC_MOUNT_ONLY` (no Python CLI, no MCP, no repo write, no S4
  acceptance).
- The agent route is one copy-paste prompt. The four supported hosts are Hermes Agent, Codex Desktop
  (GUI), Codex CLI and Claude Code. Web GPT-6 is a *consumer* of the fallback, not an agent host.
- Do not invent a command you cannot justify. Where the exact native command depends on the host
  version, say so and require the host to prove its own version and discovery.

## Deliverable 1 — `docs/install/README.md`
The single install SSOT. Structure:
1. Two main routes only: **Web** and **Agent**, each 3-6 lines. No third route at the top.
2. Web route: state plainly that no public directory listing exists yet, so the current route is the
   single `PIPD_WEB_FALLBACK.md` document, with its `DOC_MOUNT_ONLY` ceiling spelled out. Describe the
   future Directory route as conditional on a published, account-visible listing.
3. Agent route: point at `PIPD_AGENT_INSTALL_PROMPT.md`; state the four hosts and that each host must
   prove real discovery/effective load, not file presence.
4. An explicit "states that are NOT the same" table: `BUILD_PASS` != `PORTAL_APPROVED` != `PUBLISHED`
   != `HOST_QUALIFIED` != `S4_FULL_PASS`, each with its required evidence.
5. Advanced/recovery: version pin, hashes, uninstall/rollback, and how to report a failure. Keep it
   below the two main routes, not on top.

## Deliverable 2 — `docs/install/PIPD_AGENT_INSTALL_PROMPT.md`
One copy-paste prompt (Traditional Chinese, with the English identifiers kept). It must make the host:
detect its own identity/version/OS, resolve the project root, list existing same-name skills,
declare its shell/file/network permissions, then SHOW the exact target paths, the file count to be
written, the diff against existing config, the pinned commit/ZIP digest, and the uninstall path; it
must stop for explicit approval before any write, refuse global writes, refuse to modify
`AGENTS.md`/`CLAUDE.md`, refuse tokens/MCP/commit/publish, and after the write verify **real
discovery and an 8/8 effective load plus one positive and one negative trigger per host**, reporting
`NOT_VERIFIED` when only files were copied. It must end by reporting host/OS/version, the pinned
source, the effective skill count, the refusal cases, and the raw log paths - and must not claim S4
acceptance or that a public plugin was published.

## Deliverable 3 — `.github/workflows/public-plugin-verify.yml`
Read-only CI. Requirements: `permissions: contents: read`; `on: pull_request` limited to the upgrade
paths plus `workflow_dispatch`; actions pinned by full commit SHA with `persist-credentials: false`;
**no** `pull_request_target`, **no** secrets, **no** tag/publish step; a step that proves the upgrade
did not write `skills/**`, `src/**`, `schemas/**`; `python -m py_compile` on the three tools; the two
new test modules plus the full suite; and a **fail-closed negative step** that (a) requires the suite
green first, (b) mutates the pack document and requires a real `FAIL:` line, and (c) requires the
failure motive to be the identity/byte binding - a bare non-zero exit must NOT satisfy it.
The workflow must install no third-party dependency (the tools are stdlib-only) - say so in a comment
instead of pulling a requirements file that does not exist.

## Deliverable 4 — `README.md`
Reduce the install instructions to the two route entries plus a pointer to `docs/install/README.md`.
Keep every other section (licence, history, evidence) intact.

## Rules
- Validate the YAML parses (`python -c "import yaml"` may be unavailable: if so, say which check you
  actually ran instead - do not claim a parse you did not perform).
- Finish by pasting VERBATIM: the YAML parse result, and the exact lines you added to `README.md`.
