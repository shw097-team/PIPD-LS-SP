# FAR verdict — is the ZIP spec the cause of the host refusal?

Round: R5R3-20261016-preview4-closeout / FAR sub-round (host-refusal attribution)
Owner question (verbatim): 「FDA 建立 GPT 私人外掛程式時，上傳 ZIP 後 GPT 回應『無法新增外掛程式。請再試一次。』，
是否是 ZIP 的相關規格不符合 GPT 外掛程式建立的要求？」

## Answer

**No.** The plugin-spec surface of the archive is not the cause — refuted by measurement, not by argument.
The refusal is an **existing-plugin-id conflict on the account**: the account already holds the plugin id
`pipd-ls-sp-public-skills` (installed in the R5Y round), and the host refuses to add a *different-content*
archive that declares that same id. The archive's own `version` field does not create a new identity for the
host, while a **byte-identical re-upload is accepted idempotently**.

## Evidence — a five-artifact controlled matrix on the live account

| # | artifact | plugin_id | version | provenance bytes | outcome | probe |
|---|---|---|---|---|---|---|
| B | `cand-B-r5y-known-good.zip` (the R5Y archive, byte-identical to what the account already has) | pipd-ls-sp-public-skills | 0.1.1 | B values | **ACCEPTED** | P2 |
| A | `cand-A-preview4-served.zip` (release `v0.1.1-preview.4`) | pipd-ls-sp-public-skills | 0.1.1 | A values | REFUSED (original + P1 retry) | P1 |
| E | A's members, only `plugin.json` + `RELEASE_RECEIPT.json` `version` → 0.1.2 | pipd-ls-sp-public-skills | 0.1.2 | A values | REFUSED | P3 |
| D | `cand-D-variant-b-minimal.zip` (2 members, fresh id) | pipd-smoke-minimal | 0.1.0 | none | **ACCEPTED** — plugin created | P4 |
| F | A's members, only `plugin.json` `name` changed; **A's provenance bytes preserved** | pipd-probe-content-check (host page id `Plugin_89654ca2…`) | 0.1.1 | A values | **ACCEPTED** — plugin created | P5 |

What each axis move proves:

- **Spec surface excluded.** A's entire plugin-contract surface (plugin.json, all 8 SKILL.md, references,
  schemas, tests, icon, plugin.schema.json, vendor-plugin.schema.json, derivations.json) is **byte-identical**
  to B, which this same host accepted — and accepted again in P2. A format/spec violation cannot explain the
  refusal of bytes the host has already taken.
- **Layout excluded.** A and B have identical member names, sizes, order and zip metadata; B was accepted.
- **Transience excluded.** A was submitted twice (original + P1) and refused both times, the second refusal
  arriving within ~2 s.
- **Version axis excluded.** E changed only the declared version (0.1.1 → 0.1.2), provenance untouched: still
  refused. So the host's identity for the plugin is not the version field inside the archive.
- **Provenance content excluded.** F preserved A's provenance bytes verbatim (`source_commit` `cc6c19307651…`,
  `source_tree` `7d277a0afaff…`, `mapping_sha256` `c26e554c8c27…`) and changed only the plugin name: ACCEPTED,
  and the host created a new plugin page (`Plugin_89654ca2…`).
- **The account does accept new plugins.** D created a fresh plugin; F created another. "The surface refuses
  everything" is eliminated.

### Compression-level caveat (independent checker finding, applied — see `CLAIM_CORRECTIONS_FAR.md` CC-1)

E and F were rebuilt locally. Their members hold A's content, and the enumerated record fields
(name, uncompressed size, compress_type, date_time, external_attr, create_system, ordering) match A's exactly,
but they were re-deflated at a lower effective level, so **every** member's `compress_size`/`header_offset`
differs from A's on the full zip record while the decompressed bytes are identical. The single-axis claim is
therefore true **on the content axis** and not on the whole archive record. A-vs-B (both produced by the round's
own packers) is clean on the full record. No probe conclusion depends on this: the axis each probe moved is a
content axis, and the host decompresses.


The only property that separates the refused pair (A, E) from the accepted trio (B, D, F) is the
**plugin_id `pipd-ls-sp-public-skills` combined with content that differs from the installed install**.

## Acceptance signature used (and the transient that is NOT a failure signal)

The R5Y round recorded its success signature in
`PIPD/PIPD_S4_R5Y_GPT_PLUGIN_EVIDENCE_RETURN/09_ui_fda/PRIVATE_PLUGIN_INSTALL.json` step 6: the modal closes
and the window title becomes the plugin page, URL `chatgpt.com/plugins/Plugin_5ba168f7…`. P2, P4 and P5 all
reproduced that signature; A's refusals instead left the modal open with the verbatim text
`無法新增外掛程式。請再試一次。`.

A transient UIA node reading exactly `無法取得` appeared once in the **accepted** flows (P2, P4, P5) and is
therefore recorded as an unexplained surface transient, **not** as a failure signal. The raw probe runner's
own regex verdict (`HOST_REJECTED` on any node containing 無法) is a probe defect and was adjudicated per
artifact; the raw files keep the unedited machine verdict.

## What is NOT established (claim ceiling)

- **The mechanism is not disclosed by the host.** The refusal text carries no rule id, no field, no per-file
  reason. The attribution above is by controlled elimination over five artifacts, not by reading a host rule.
- Predictions of the same matrix by other mechanisms are not formally excluded. In particular, this round
  cannot distinguish "same plugin_id + different content" from "the host treats a second add for an id it
  already owns as an operation that must go through the update route".
- Install state after the accepted uploads is UI-observed, not API-acknowledged: B's re-upload is assumed
  idempotent because its bytes equal the installed artifact; D's and F's pages were created, and F's page
  still offers 安裝外掛程式 (i.e. created but not installed).
- The account's installed-plugin list could not be read from the automation surface (the main region is not
  exposed as named UIA nodes); the presence of the R5Y plugin is evidenced by the plugins page defaulting to
  its detail page and by the plugin list entry.

## Where this leaves the owner's question

The published `v0.1.1-preview.4` archive is **not** rejected for its packaging or its plugin specification;
it is rejected as a *second add of an id the account already owns with different content*. The minimal,
non-over-engineered remedy is therefore an **operational/route change, not a packaging rewrite** — see
`ENGINEERING_DECISION.md`.
