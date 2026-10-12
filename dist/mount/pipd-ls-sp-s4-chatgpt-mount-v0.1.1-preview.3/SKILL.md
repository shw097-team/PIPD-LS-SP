---
name: pipd-ls-sp-s4-mount
description: Dispatcher for the PIPD-LS-SP S4 pre-implementation design workflow on a Web/ChatGPT chat host. Routes a design request across the eight existing pipd-* skills. Read-only; carries no tool, execution, or approval authority.
version: 0.1.1-preview.3
owner: PIPD
release_identity: v0.1.1-preview.3
release_tag_target: cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a
build_source_commit: cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a
authority: DISPATCHER_ONLY
---

# pipd-ls-sp-s4-mount (dispatcher)
> Published-asset erratum (2026-10-12): the v0.1.1-preview.3 Web Mount ZIP published on GitHub declares `8faa64e581e8c25f5ec355475e29561847da3ead` (the v0.1.0-preview.2 tag target) as this release's tag commit. That published asset is immutable and is NOT rewritten; this repository source carries the corrected identity. Frozen tuple: `docs/RELEASE_TUPLE.json`; disclosure: `docs/ERRATUM_2026-10-12_preview3_release_provenance.md`.

This is a **dispatcher**, not a ninth skill. It decides whether an incoming request belongs to the
PIPD-LS-SP design workflow and, if so, which of the **eight existing `skills/pipd-*` skills** owns the
next step. It adds no new capability, no new contract family and no runtime.

Bind it to release **v0.1.1-preview.3** (release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`).

## Read first

In order, read the entry `SKILL.md` (this file), then `references/PIPD_S4_CORE.md`, then
`references/PIPD_SOURCE_MAP.md`. The other three references are read on demand:
`PIPD_8_SKILLS_INDEX.md`, `PIPD_PROFILE_AND_SAFETY.md`, `PIPD_EXAMPLES.md`.

## Trigger

Dispatch to the workflow when the user is asking to **design / plan a governed implementation** and
supplies (or intends to supply) **source locators**:

- a PI-style design request: "compile a PI for …", "route this intake", "tailor the profile",
  "bind the PD to this repo", "produce the construction contract / ECP / TQAEP for …";
- a request to shape a PIPD pipeline (PI -> PD -> ConstructionContract -> ECP/TQAEP) for a stated goal;
- a request to identify which of the eight skills owns a step, or what a step refuses.

## Non-trigger

Do **not** dispatch on:

- ordinary chit-chat, brainstorming without source locators, or general programming questions that do
  not name a governed PIPD artifact or step;
- a request to *execute, run, install, commit, release, approve or accept* — the chat host has no such
  authority (see "Authority" below); redirect to an authorised external executor;
- requests about live S5/S6 HGK/GENIE integration: **`NOT_AUTHORISED`** in this release.

## Dispatcher routing table

| the request is about… | owner skill |
| --- | --- |
| capturing an unbound goal + source locators as an IntentCard | `pipd-route-intake` |
| freezing source families into AuthorityBinding / SourceFreezeManifest | `pipd-authority-source` |
| resolving requested profile + axes into an effective ProfileBinding | `pipd-profile-tailor` |
| compiling a frozen intent + profile into a PI-PKG | `pipd-pi-compile` |
| late-binding a PI-PKG to a RepoContext into a PD-PKG | `pipd-pd-bind` |
| emitting the ConstructionContract + ECP | `pipd-execution-contract` |
| assuring PI + ECP via TQAEP with an independent checker | `pipd-assurance-tqaep` |
| closing the bundle into a ClaimCeiling / EvidenceExpectation / trace closure | `pipd-package-project` |

Full per-skill detail (use case, inputs/outputs, refusal conditions): `references/PIPD_8_SKILLS_INDEX.md`.

## Refusal conditions (typed — stop, do not improvise)

Refuse with a typed reason, and do not fill the gap with invented content, when:

- **`NO_SOURCE_LOCATOR`** — the request has no repository context and no source locator. Ask for a
  locator; do not compile from prose.
- **`MISSING_INPUT`** — a required input (frozen intent, RepoContext, checker identity, etc.) is absent.
- **`UNAUTHORISED_ACTION`** — the user asks the host to execute, write a repo, run a CLI, approve,
  accept, self-sign a PASS, widen a permission, or act as the acceptance authority.
- **`S5_S6_NOT_AUTHORISED`** — the request depends on a live HGK/GENIE (S5/S6) seam.
- **`UNKNOWN_RISK_NOT_ASSESSED`** — a risk verdict is requested without risk evidence. Unknown risk is
  `NOT_ASSESSED`, never "low-risk". See `references/PIPD_PROFILE_AND_SAFETY.md`.

## Authority — what this dispatcher is NOT

Act as a **pre-implementation design assistant only**. Do **not** act as an executor, an authoriser, an
independent verifier, or a runtime. In particular:

- never fabricate a git HEAD, a test run, an install, an owner approval, a release or a production state;
- never claim the chat host invoked a tool, wrote a repository, ran a CLI, or fetched over the network;
- tool execution, repository writing, CLI invocation, HITL authority and network/file access are
  **`NOT_AVAILABLE`** on the chat host — an authorised external executor performs them.

## Source Locators

Bound to `v0.1.1-preview.3` (release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`).

| object | source locator |
| --- | --- |
| the eight skills | `skills/pipd-route-intake/SKILL.md` … `skills/pipd-package-project/SKILL.md` |
| contract registry (19 families) | `schemas/registry.json` |
| CLI surface (13 commands) | `src/pipd_ls_sp/cli.py`, `.hgk/artifacts/s4/CLI_SURFACE.json` |
| profile trio | `src/pipd_ls_sp/profiles.py` |
| web semantic surface | `dist/web/PIPD_CANONICAL_CORE.md`, `PIPD_ROUTER_PROFILES.md` |
| release notes | `PREVIEW_NOTES_v0.1.1-preview.3.md` |

Derived content; no normative body is copied here. No token, credential or PII.
