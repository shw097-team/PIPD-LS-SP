# PIPD_S4_CORE — the S4 chain, the 13 commands, the 19 families, the claim ceiling

> Release identity: **v0.1.0-preview.2** — tag commit `8faa64e581e8c25f5ec355475e29561847da3ead`
> (tree `58301503`). Derived, read-only content. This document quotes no normative body.

## The design chain (what a design assistant sketches)

PIPD-LS-SP compiles a governed goal through a fixed chain. On the chat host you help a user **shape**
this chain; you never execute it.

| step | artifact | owner skill | meaning |
| --- | --- | --- | --- |
| 1 | **IntentCard** | `pipd-route-intake` | an unbound goal + source locators captured as a typed intent with requirement atoms |
| 2 | **PI-PKG** | `pipd-pi-compile` | the stable semantic contract: atoms + acceptance + trace links, profile-bound |
| 3 | **PD-PKG** | `pipd-pd-bind` | the PI late-bound to a real **RepoContext** (root, head, tracked files, currentness) |
| 4 | **ConstructionContract** | `pipd-execution-contract` | subject, writable scope, expected changes, tests, rollback, evidence expectations |
| 5 | **ECP** | `pipd-execution-contract` | effect intent, permission, retries, idempotency, readback, rollback |
| 6 | **TQAEP** | `pipd-assurance-tqaep` | tests, oracles, fixtures, acceptance, requalification, with an **independent checker** |
| 7 | **ClaimCeiling** | `pipd-package-project` | allowed claims, forbidden escalations, close conditions + EvidenceExpectation + trace closure |

Supporting skills that sit beside the chain: `pipd-authority-source` (freeze source families into
`AuthorityBinding`) and `pipd-profile-tailor` (resolve requested profile + axes into a `ProfileBinding`).

The chain is **fail-closed at each seam**: a step refuses rather than guessing. Design a step only when
its upstream artifact exists; otherwise emit a typed refusal.

## The 13 CLI commands (executed by an authorised executor, not the chat host)

The shipped CLI — the `pipd` entry point under `src/pipd_ls_sp/cli.py` — exposes exactly **13**
commands. The chat host may *name* them in a plan; it must not claim to run them.

| # | command | purpose | refusal code on the failure path |
| --- | --- | --- | --- |
| 01 | `init` | scaffold a workspace root (`docs/ schemas/ src/ tests`) | `USAGE_INVALID` |
| 02 | `intake` | capture a goal + locators into an IntentCard | `INTAKE_INVALID` |
| 03 | `profile` | resolve the effective profile from requested + axes | `PROFILE_VETO` |
| 04 | `compile-pi` | compile a PI-PKG from a frozen intent | `IO_NOT_FOUND` |
| 05 | `bind-pd` | late-bind a PI-PKG to a RepoContext | `REPO_CONTEXT_MISSING` |
| 06 | `compile-ecp` | emit the ConstructionContract + ECP | `INPUT_SHAPE_INVALID` |
| 07 | `compile-tqaep` | emit the TQAEP assurance plan | `TQ_SOD` |
| 08 | `validate` | validate a record against its family schema | `IO_NOT_FOUND` |
| 09 | `doctor` | report resolved schema source / install health | `USAGE_INVALID` |
| 10 | `project` | project canonical objects onto a surface | `USAGE_INVALID` |
| 11 | `export` | export an artifact bundle | `USAGE_INVALID` |
| 12 | `diff` | semantic diff between artifacts | `DIFF_INCOMPATIBLE_SCHEMA` |
| 13 | `repair` | bounded repair within an admitted scope | `REPAIR_SCOPE` |

`--root` is a **global** option and must precede the subcommand (`pipd --root <dir> <command>`).

## The 19 contract families (schema registry)

`schemas/registry.json` declares exactly **19** families. The family set, the per-family required
fields and the closed-property stance (`additionalProperties: false`) are unchanged by this release.

| # | family | owner | materialization |
| --- | --- | --- | --- |
| 01 | ArtifactIdentity | PIPD | REQUIRED_NOW |
| 02 | AuthorityBinding | PIPD | REQUIRED_NOW |
| 03 | RequirementAtom | PIPD | REQUIRED_NOW |
| 04 | ProfileBinding | PIPD | REQUIRED_NOW |
| 05 | TechnologyAdmission | PIPD | REQUIRED_NOW |
| 06 | PI-PKG | PIPD | REQUIRED_NOW |
| 07 | PD-PKG | PIPD | REQUIRED_NOW |
| 08 | TraceLink | PIPD/TQAEP | REQUIRED_NOW |
| 09 | TaskSpecSeed | PIPD | REQUIRED_NOW |
| 10 | ConstructionContract | PIPD | REQUIRED_NOW |
| 11 | WorkOrderCandidate | PIPD | REQUIRED_NOW_NONAUTHORITY |
| 12 | ECP | PIPD/ECP semantics | REQUIRED_NOW |
| 13 | TQAEP | PIPD/TQAEP semantics | REQUIRED_NOW |
| 14 | ExecutionHandoff | PIPD | REQUIRED_NOW |
| 15 | EvidenceExpectation | PIPD/TQAEP | REQUIRED_NOW |
| 16 | ClaimCeiling | PIPD | REQUIRED_NOW |
| 17 | SurfaceProjectionManifest | PIPD | REQUIRED_NOW |
| 18 | GENIEProjectionRef | GENIE adapter | SCHEMA_SEAM_ONLY_UNTIL_S6 |
| 19 | ExecutionBindingRef | HGK adapter | SCHEMA_SEAM_ONLY_UNTIL_S5 |

Families 18 and 19 are **seam schemas only** until S6/S5 respectively — no live integration is claimed.

## The claim ceiling (read before quoting anything)

This pack and the release it binds to support a **candidate-level** claim only. The published capability
is `OWNER_AUTHORIZED_OPEN_SOURCE_PREVIEW_BETA_PUBLISHED`.

Allowed ceilings for a chat answer:

- `DESIGN_ONLY` — a design sketch derived from these documents;
- `FILE_PRESENT` — a referenced repository path exists;
- `SCHEMA_VALID` — a record validates against its declared family schema.

Explicitly **forbidden** and never to be quoted as granted:

| forbidden claim | why |
| --- | --- |
| `FULL_S0_S4_INDEPENDENT_PASS` | no full independent gate pass exists |
| `G_RELEASE_FULL_PASS` | not granted |
| `PRODUCTION_VERIFIED` | preview only; not production |
| `S5_RUNTIME_READY` | S5 is `NOT_AUTHORISED` |
| `ALL_HOSTS_LIVE_CERTIFIED` | no live host certification |

Unknown risk is `NOT_ASSESSED`, never "low-risk". No release signature or external build attestation is
claimed. See `PIPD_PROFILE_AND_SAFETY.md` and `PIPD_SOURCE_MAP.md`.

## Source Locators

Bound to `v0.1.0-preview.2`, tag commit `8faa64e581e8c25f5ec355475e29561847da3ead`.

| object | source locator |
| --- | --- |
| contract registry (19 families) | `schemas/registry.json` |
| CLI surface (13 commands) | `src/pipd_ls_sp/cli.py`, `.hgk/artifacts/s4/CLI_SURFACE.json` |
| PI/PD/ECP/TQAEP schemas | `schemas/PI-PKG.schema.json`, `PD-PKG.schema.json`, `ECP.schema.json`, `TQAEP.schema.json` |
| claim ceiling | `schemas/ClaimCeiling.schema.json`, `PREVIEW_NOTES_v0.1.0-preview.2.md` |
| web semantic surface | `dist/web/PIPD_CANONICAL_CORE.md`, `dist/web/PIPD_ROUTER_PROFILES.md` |

Derived content; no normative body copied. No token, credential or PII.
