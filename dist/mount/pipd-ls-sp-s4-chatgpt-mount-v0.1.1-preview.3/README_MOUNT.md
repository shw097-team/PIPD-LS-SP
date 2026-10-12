# README_MOUNT — mounting the PIPD-LS-SP S4 Web/ChatGPT pack

> Release identity: **v0.1.1-preview.3** — release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`.
> Published-asset erratum (2026-10-12): the v0.1.1-preview.3 Web Mount ZIP published on GitHub declares `8faa64e581e8c25f5ec355475e29561847da3ead` (the v0.1.0-preview.2 tag target) as this release's tag commit. That published asset is immutable and is NOT rewritten; this repository source carries the corrected identity. Frozen tuple: `docs/RELEASE_TUPLE.json`; disclosure: `docs/ERRATUM_2026-10-12_preview3_release_provenance.md`.
> (tree `91b1156f`). This pack is derived, read-only content bound to that release; it is not a new
> authority, a new skill and not a second source of truth.
> Pack directory: `pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3/` · Preview-only, candidate content.

This pack gives a ChatGPT/Web user the entry point, the core semantics, the source map, the skill
index, the profile/safety rules and worked examples needed to use PIPD-LS-SP **as a pre-implementation
design assistant**. It carries instructions and provenance only. It executes nothing.

## What is in the pack

| file | role |
| --- | --- |
| `SKILL.md` | one-page dispatcher: entry point, trigger / non-trigger pairs, refusal conditions, no tool authority |
| `PIPD_LS_SP_QUICKSTART_PROMPT.md` | the short starter prompt to paste into a chat |
| `references/PIPD_S4_CORE.md` | PI -> PD -> ConstructionContract -> ECP/TQAEP chain, the 13 CLI commands, the 19 families, the claim ceiling |
| `references/PIPD_SOURCE_MAP.md` | the external canonical SSOT and how this pack binds to `v0.1.1-preview.3` |
| `references/PIPD_8_SKILLS_INDEX.md` | the eight existing `skills/pipd-*` skills: use case, inputs/outputs, refusal conditions |
| `references/PIPD_PROFILE_AND_SAFETY.md` | LITE / STANDARD / ASSURED; unknown risk is `NOT_ASSESSED` |
| `references/PIPD_EXAMPLES.md` | one normal example, one missing-source refusal, one injection refusal |
| `MANIFEST.sha256` | sha256 of every file above, relative paths, sorted |

## How to mount it — two paths with different guarantees

### Path A — native skill upload (qualifying accounts/workspaces only)

On accounts/workspaces that expose it, the pack can be uploaded through
**`Plugins -> Skills -> Create -> Upload`**. On that path the host registers the pack as a skill and
can surface its `SKILL.md` as a native instruction file.

- Availability: **qualifying accounts/workspaces only**; the control is not present on every plan.
- This round **did not exercise** the native upload path — no qualifying native-upload account was
  available, so no native load is claimed. It is recorded as `NOT_SUPPORTED` in the consumer UAT
  (see `.hgk/.../evidence/WEB_MOUNT_UAT.json`), not as a PASS.

### Path B — manual attachment / Project Knowledge fallback (what an ordinary chat user can do)

With no native control, an ordinary chat user can still use the pack by **attaching the reference
files to the conversation** or **adding them to Project Knowledge**:

1. Put `SKILL.md`, `references/PIPD_S4_CORE.md` and `references/PIPD_SOURCE_MAP.md` into the project's
   knowledge (or attach them to the first message), then paste `PIPD_LS_SP_QUICKSTART_PROMPT.md`.
2. Attach `references/PIPD_8_SKILLS_INDEX.md`, `references/PIPD_PROFILE_AND_SAFETY.md` and
   `references/PIPD_EXAMPLES.md` when the task needs them.
3. Verify the download first: recompute `MANIFEST.sha256` against the extracted files before you rely
   on any of them.

Manual attachment is **not** a native skill installation: the host treats the files as ordinary
context. That is a weaker guarantee than Path A, and it is what this pack is exercised against.

## Capability limits of the chat host (stated, not implied)

The chat host is a **read-only semantic surface**. It does not run PIPD and cannot act for an
authorised executor. Every capability below is `NOT_AVAILABLE` for the chat host:

| host capability | state | note |
| --- | --- | --- |
| tool execution | `NOT_AVAILABLE` | the host runs no tool on the user's behalf from this pack |
| repository writing | `NOT_AVAILABLE` | nothing is written to any repository from the chat host |
| CLI invocation | `NOT_AVAILABLE` | the 13 `pipd` commands run in an authorised executor, not in chat |
| HITL authority (owner approval / acceptance) | `NOT_AVAILABLE` | the host is not the human-in-the-loop authority and cannot approve or accept |
| network / file access | `NOT_AVAILABLE` | the host does not fetch releases or read the user's disk from this pack |

### Where execution actually happens

Tool execution, repository writing, CLI invocation, HITL authority and network/file access happen in an
**authorised external executor** under HG-KSEOS governance — a bounded writer/checker lane on a real
checkout with the pinned interpreter, producing raw receipts bound to the frozen candidate. The chat
host's job is to help a user **design** the work (route it, tailor a profile, sketch the PI/PD/ECP/TQAEP
chain) and then hand a typed, source-located plan to that executor. The host must never claim to have
executed, installed, tested, approved or released anything.

## Source Locators

Derived from, and bound to, the following repository sources at `v0.1.1-preview.3`
(release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`):

| object | source locator |
| --- | --- |
| release notes (immutable tag) | `PREVIEW_NOTES_v0.1.1-preview.3.md` |
| contract registry (19 families) | `schemas/registry.json` |
| CLI surface (13 commands) | `src/pipd_ls_sp/cli.py`, `.hgk/artifacts/s4/CLI_SURFACE.json` |
| the eight skills | `skills/pipd-route-intake/`, `pipd-authority-source/`, `pipd-profile-tailor/`, `pipd-pi-compile/`, `pipd-pd-bind/`, `pipd-execution-contract/`, `pipd-assurance-tqaep/`, `pipd-package-project/` |
| web semantic surface | `dist/web/PIPD_BOOTSTRAP.md`, `PIPD_CANONICAL_CORE.md`, `PIPD_ROUTER_PROFILES.md`, `PIPD_ARTIFACT_SCHEMAS.md`, `PIPD_EVAL_HANDOFF.md` |
| profile trio | `src/pipd_ls_sp/profiles.py` |

This document is derived content. It quotes no normative body; where a normative source matters it is
referenced by locator, not copied. It contains no token, credential, PII or unauthorised normative body.
