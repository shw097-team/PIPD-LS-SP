# Design

## Context

Three documents constrain this change: the external post-repair recheck (fail-closed, read-only), the
triple-upgrade blueprint R2 (`DOCUMENT_REPAIR_COMPLETED / DESIGN_CANDIDATE`), and the Hermes/HG-KSEOS
command sheet (route-out). The recheck's decisive facts are that the repair branch and `main` diverged,
that the published wheel is not the repaired validator, and that zero CI exists on any ref. The
blueprint's decisive constraint is that this is **one small change set** over the existing PKG-07/08
work packages: no new stage, no ninth skill, no second trace engine, no 20th schema family, `MCP=OFF`.

## Goals / Non-Goals

**Goals**: a deterministic, fail-closed public Skills-only plugin candidate; exactly two install
routes; a verification surface whose negative step cannot pass by accident; every claim bound to a
frozen subject with raw evidence.

**Non-Goals**: publishing anything; a remote MCP server, Apps, Actions or Hooks; rewriting the eight
skill bodies; raising any operation/ECP/TQAEP permission because a plugin shipped; claiming
`PIPD_S4_FULL_PASS`.

## Decisions

1. **Two manifests, one package.** The vendor (Agent Plugins 1.0) schema at
   `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` allows only `$schema, name, version,
   description, author, homepage, repository, license, keywords, extensions` with
   `additionalProperties: false` and `required: ["$schema","name"]`. The package root `plugin.json`
   therefore must be that shape; PIPD's release bookkeeping moves into `extensions["com.pipd.s4"]`.
   A private manifest used as the root would be rejected by the platform, so it is not the root.
2. **The vendor schema is byte-locked.** The bytes are fetched once, committed under
   `packaging/public-plugin/`, and their digest is pinned in the manifest; the builder refuses on any
   mismatch. This is a *lock*, not a vendor-validated validation: the vendor's own validator and the
   Portal scan stay NOT_EXECUTED.
3. **Every skill needs an owner-approved derivation.** None of the eight `SKILL.md` packs is a subset of
   the Agent Skills frontmatter set (`name, description, license, compatibility, metadata,
   allowed-tools`); each carries `version, owner, triggers, schemas, references, tests`. A byte-copy
   projection is therefore impossible, and the builder refuses without one record per skill whose
   `source_sha256` matches the frozen ledger and whose `approved_by` / `approval_receipt` are real.
   The body is asserted unchanged.
4. **Icons are generated deterministically, not committed as opaque binaries.** A stdlib PNG writer
   (zlib + struct, no Pillow) produces a fixed RGBA icon; the decoder checks the signature, the IHDR,
   every chunk CRC and inflates the IDAT. Residual: owner brand assets and the Portal icon scan remain
   NOT_EXECUTED.
5. **Stdlib only.** The blueprint proposed hash-pinned PyYAML / jsonschema / Pillow. This change uses
   an in-repo minimal frontmatter parser, a subset schema validator and a structural PNG decoder
   instead, so the build carries **no third-party dependency** and no network at build time. This is a
   declared deviation; its cost is that the local validators are ours, not the vendors'.
6. **Determinism is asserted, not assumed.** Fixed ZIP date (1980-01-01), mode 0644 and DEFLATED level
   9, with a member-by-member read-back before the archive is promoted.
7. **The negative CI step must fail closed.** A step that only requires a non-zero exit is satisfied by
   deleting the module or by any import error. The step here requires the suite green first, then an
   actual `FAIL:` line, then that the failure motive is the identity/byte binding.

## Risks / Trade-offs

- **Owner gates block a real artifact.** A real build refuses today; the pipeline is therefore proven
  by fixtures and the refusal is recorded. Mitigation: the refusal reasons are typed and the owner has
  a one-action ratification for each.
- **Local validators are not the vendor's.** A locally-correct package could still fail the vendor's
  scan. Mitigation: the vendor schema bytes are locked and the claim ceiling says so.
- **Same-tag asset replacement is historical fact.** The published `preview.3` asset was replaced in
  place; this change preserves the first-shipped digest as a separate historical field and does not
  rewrite the tag. Mitigation: the release owner issues a successor immutable release.

## Migration

No user migration: nothing published changes. Stage B is a stacked candidate on Stage A; the branch is
pushed for external acceptance and is not merged by any agent.
