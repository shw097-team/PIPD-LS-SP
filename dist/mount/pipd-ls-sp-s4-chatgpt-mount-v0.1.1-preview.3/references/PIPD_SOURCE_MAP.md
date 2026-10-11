# PIPD_SOURCE_MAP — the canonical external SSOT and this pack's binding

> Release identity: **v0.1.1-preview.3** — tag commit `8faa64e581e8c25f5ec355475e29561847da3ead`
> (tree `58301503`). Derived view. This document is a **pointer**, not a master copy: it contains no
> copy of any normative body.

## The single source of truth is external

The canonical normative standard is **`PIPD-LIFECYCLE-SPEC@1.1.0`**, owned outside this runtime
repository. It is the **single source of truth (SSOT)** for the lifecycle. Every runtime artifact here
is a **derived, consumer-side projection** of that standard — the runtime repository does **not** hold a
master copy, and shipping one here would be the competing second SSOT the governance rules forbid.

| property | value |
| --- | --- |
| standard id | `PIPD-LIFECYCLE-SPEC` |
| version | `1.1.0` |
| owner | external canonical authority (outside this repository) |
| content hash | `NOT_PUBLIC` — the normative body is not published in this repository |
| role here | SSOT; this repo is a derived consumer view |

Because the normative body is `NOT_PUBLIC`, an in-repo reader cannot reconstruct it. A consumer pinning
this index must therefore treat the standard as an **external authority referenced by locator**, never
as content this pack can quote.

## How this pack binds to v0.1.1-preview.3

This pack is a **derived artifact** of the immutable release `v0.1.1-preview.3`. It binds by identity,
not by embedding:

| binding surface | value |
| --- | --- |
| release tag | `v0.1.1-preview.3` |
| tag commit | `8faa64e581e8c25f5ec355475e29561847da3ead` |
| release tree | `58301503` |
| published wheel | `pipd_ls_sp-0.1.1a3-py3-none-any.whl` |
| published wheel sha256 | `e8ca509d9014e57536d18bc103d91d06e4cd40e4f2e3ef0cec6a7a083fafe7ec` |
| published capability | `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED` |
| pack self-integrity | `MANIFEST.sha256` (recomputable from the extracted tree) |

The pack is **superseded-safe**: it names the tag it derives from and the tag commit, so a future
release produces a new pack version rather than silently mutating this one. `main` is rolling; pin the
**tag**, not the branch.

## Source-family index (derived)

Per source family: owning authority, version, a hash or an explicit non-public marker, and the
consumers. Hash-or-`NOT_PUBLIC` is stated; nothing is invented.

| source family | owner | version | hash / marker | consumers |
| --- | --- | --- | --- | --- |
| `PIPD-LIFECYCLE-SPEC` (normative standard) | external canonical authority | `1.1.0` | `NOT_PUBLIC` | all skills/packages project it |
| contract registry | PIPD | `1` | `schemas/registry.json` (see its sha256 in `MANIFEST.sha256`) | all planes |
| CLI surface | PIPD-EC | `1` | `src/pipd_ls_sp/cli.py` | executors, `doctor`, gates |
| profile trio | PIPD | `1` | `src/pipd_ls_sp/profiles.py` | Skills/JIT/HGK |
| web semantic surface | PIPD | `1` | `dist/web/PIPD_*.md` | read-only consumers |
| the eight skills | PIPD | `1` | `skills/pipd-*/SKILL.md` | the dispatcher in this pack |

## What this pack does NOT claim

- It does not reconstruct, copy or paraphrase the normative `PIPD-LIFECYCLE-SPEC@1.1.0` body.
- It does not claim a release signature, a build attestation, or a live host certification.
- It does not claim S5/S6 runtime readiness; those seams are `NOT_AUTHORISED`.
- It does not assert that the chat host executed anything.

## Source Locators

Bound to `v0.1.1-preview.3`, tag commit `8faa64e581e8c25f5ec355475e29561847da3ead`.

| object | source locator |
| --- | --- |
| external canonical standard | `PIPD-LIFECYCLE-SPEC@1.1.0` (external; `NOT_PUBLIC`) |
| derived normative-source index (sibling WO) | `docs/NORMATIVE_SOURCE_MAP.md` (produced by WO-S4-SELFBOOT-04) |
| adjudication that it stays external | `tools/build_spec_del_crosswalk.py` row `002` |
| release notes | `PREVIEW_NOTES_v0.1.1-preview.3.md` |
| wheel digest literal | `README.md` quickstart; `SHA256SUMS` on the release |

Derived content; no normative body copied. No token, credential or PII.
