# Engineering decision — best action for the host-refusal finding

Round: R5R3-20261016-preview4-closeout / FAR sub-round. Basis: `FAR_VERDICT.md` (five-artifact matrix).
Selection criteria applied, as the owner specified: 低阻力、高可行、高工程必要性、不過度工程化、對齊本 session
目標與 PIPD-LS-SP / PIPD-PKG 封裝契約、可寫入驗收報告.

## Decision

**Do not change the packaged artifact.** The preview.4 archive is correct as packaged; its plugin-spec surface
is byte-identical to an archive the host accepted, and its provenance metadata is accepted verbatim when the
archive is presented under a new plugin id (probe F). Every packaging change proposed before the probes
("rebuild for spec compliance", "strip the provenance members", "bump the version") is now **excluded by
measurement** — each would have been a change with no causal basis.

The remedy is to change the **add route**, not the bytes, in this order of preference:

| # | action | friction | who | notes |
|---|---|---|---|---|
| R1 | On the existing plugin page, use the **管理 / 更多操作** affordance to replace the installed archive with the preview.4 archive (update route) | one UI action, no packaging change | **OWNER** (mutates the account's install state) | preferred; the affordances observed are `管理` and `更多操作` on the plugin page |
| R2 | Remove the installed `PIPD-LS-SP Public Skills` plugin, then re-add by uploading the preview.4 archive | one UI action, no packaging change | **OWNER** (destructive to the current install) | fallback if no update route exists |
| R3 | If neither exists: re-declare the release under a **distinct plugin id** (a packaging change: unique id per release) | packaging + release change | owner decides; downstream of R1/R2 failure | only if R1/R2 fail — an id change is a product/identity decision, not a bug fix |

**Do not do:** strip or "neutralise" the two provenance members; bump the version; rebuild the archive; change
the layout. All four were probe-tested as irrelevant to the refusal.

## Why this is the minimum sufficient change

The cause is a host-side identity/route condition, not a defect in the artifact. The cheapest action that
actually exercises preview.4's bytes on the live account is the update route (R1). Choosing a packaging change
instead would ship a different artifact to satisfy a hypothetical rule that the evidence has already excluded
— the textbook over-engineering the owner asked to avoid.

## PIPD-PKG contract change (one rule, minimal)

Adopt the PLAN lane's rule, now grounded in a measured cause rather than a hypothesis:

> **Pre-upload identity check.** When packaging a host-upload candidate, record the target account's installed
> `plugin_id` set in the same record. If the candidate's `plugin_id` already exists on the account, the
> candidate is an **UPDATE**, not an ADD: packaging fails closed unless the record names the update route
> (or carries an owner decision to remove the existing install first). The candidate's internal `version`
> field does not by itself make the upload a new identity — measured: bumping it changed nothing.

This converts this failure class from a live-host surprise into a packaging-time refusal, without adding a
framework.

## What this round executed, and what it hands over

Executed (owner-authorised FDA probes, five uploads across five artifacts, each preceded by an offline digest
check against `host_smoke/CANDIDATES.json`): P1 retry of A (refused), P2 upload of B (accepted), P3 upload of E
(refused), P4 upload of D (accepted, plugin created), P5 upload of F (accepted, plugin created). Two probe
candidates (E, F) were built locally with a single-axis content delta each and are **local diagnostics, never
releases**; neither touched the published asset. Caveat applied from the independent checker: E and F match A on
the enumerated record fields and on decompressed bytes, but not on the full archive record (their members were
re-deflated at a lower effective level, so `compress_size`/`header_offset` differ) — see
`CLAIM_CORRECTIONS_FAR.md` CC-1. No remedy conclusion depends on it.

Handed to the owner as a one-action decision: **R1/R2** (they mutate the account's install state — an owner
act under the standing gates `PRIVATE_HOST_INSTALL` / `PRODUCTION`, which remain NOT_GRANTED for the agent).
The round does not perform them.

## Side effects of this sub-round (all disclosed, none hidden)

1. **Account state**: probe P4 created a plugin `pipd-smoke-minimal` (v0.1.0) on the account, and probe P5
   created `Plugin_89654ca2…` (a probe id whose page still shows 安裝外掛程式, i.e. created but not installed).
   Both are probe footprints; each can be removed with one action in the plugins home. P2's accepted upload
   re-sent bytes identical to the installed artifact and is assumed idempotent (not independently verified).
2. **Browser**: one new tab was opened in Chrome window `0x20622`, navigated to the plugins surface, and the
   upload flow was driven with UIA plus the minimum trusted input (one foreground click per upload to open the
   native picker, one trusted ENTER to submit it). The pointer moved during those clicks.
3. **Round files**: new probe/build/read scripts and JSON records in the round directory, plus the FAR
   sub-directory; the OPENSPEC change `pipd-ls-sp-s4r5-host-refusal-far`; board
   `r5r3-zipspec-far-20261016`.
4. **Records corrected**: the round's own `RESEARCH_INPUT.json` carried a wrong `sha256` tail for B; corrected
   in place with the correction disclosed (the defect was caught by the PLAN lane's claim ceiling).

## Acceptance-report wording that is now permitted

「preview.4 的 ZIP 規格面已被逐 byte 與受控上傳證據駁斥為拒收原因；拒收追隨的是帳號上已存在的
`plugin_id` 與『內容不同』的組合；修法為更新／移除後重加的操作路徑，非重新封裝。」
Claim ceiling unchanged: UI-observed, no server-side error detail, mechanism not disclosed by the host.
