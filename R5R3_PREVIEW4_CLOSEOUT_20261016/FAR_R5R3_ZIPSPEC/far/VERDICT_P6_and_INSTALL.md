# P6 — the owner-directed install of preview.4 under the name `PIPD-LS-SP Public Skills_P4`

## Owner instruction of record (verbatim)

「直接用「PIPD-LS-SP Public Skills_P4」的名字，進行安裝」

That instruction is the owner's grant for this one account-mutating action (the standing gate
`PRIVATE_HOST_INSTALL` is not granted to the agent in general; it is honoured here for the single action the
owner named, and for nothing further).

## What was built (candidate G)

`host_smoke/cand-G-preview4-p4-name.zip`, sha256 `25b6b1453fbe6d333d13b0862f3c7dc07e955cf3efb79e856f9117d89161905b`,
68,370 bytes. Derived from A (the `v0.1.1-preview.4` asset, sha256 `545e359a5ca6abc7…`) with exactly two members
changed and no others:

| member | field | from | to |
|---|---|---|---|
| `pipd-ls-sp-public-skills/plugin.json` | `name` (the host's identity key) | `pipd-ls-sp-public-skills` | `pipd-ls-sp-public-skills-p4` |
| `pipd-ls-sp-public-skills/plugin.json` | `extensions.com.openai.interface.displayName` and `…display_name` (both occurrences) | `PIPD-LS-SP Public Skills` | **`PIPD-LS-SP Public Skills_P4`** |
| `pipd-ls-sp-public-skills/plugin.release.json` | `display_name` | `PIPD-LS-SP Public Skills` | **`PIPD-LS-SP Public Skills_P4`** |
| `pipd-ls-sp-public-skills/plugin.release.json` | `plugin_id` | `pipd-ls-sp-public-skills` | `pipd-ls-sp-public-skills-p4` |

Verification before upload: 54 of 56 members byte-identical to A; **0** `compress_size` mismatches and **0** zip-record
metadata mismatches against A (the compression-level discipline the earlier checker's finding demanded); manifest
`FAR_R5R3_ZIPSPEC/CANDIDATE_G_MANIFEST.json`.

**Interpretation disclosed:** the owner asked for the name `PIPD-LS-SP Public Skills_P4`. The host's *identity* field
(`plugin.json .name`) is a slug — an earlier probe proved the identity, not the display string, is what collides — so
the identity was set to `pipd-ls-sp-public-skills-p4` and the requested literal string was placed in every
**display** field. If the owner wanted the literal string in the identity field itself, that is a one-upload retry.

## Outcome (two live actions)

1. **Create (upload / ADD):** accepted. Modal closed at 10 s; window title became
   `PIPD-LS-SP Public Skills_P4 | ChatGPT 外掛程式` at 11 s — the previous rounds' recorded success signature.
   The runner's regex verdict says `HOST_REJECTED` because the benign `無法取得` node appears in accepted flows too;
   that is a known runner defect, so the raw file is kept unedited and this file carries the adjudication.
2. **Install (mount):** the plugin page offered `安裝外掛程式`; activating it opened a consent dialog
   (「…Public Skills_P4 已可使用」/ install to start using it in ChatGPT, with `稍後再說` as the secondary).
   The dialog's buttons are not exposed as named UIA nodes, so the activation was done with a trusted ENTER
   (the primary control is focused in a Chromium modal). The modal closed and the plugin page switched to
   `在對話中試用` + `更多操作` (the installed signature, `安裝外掛程式` gone).

## Independent-looking verification (read after a reload, so nothing is stale)

`已安裝` list now holds five entries: **`PIPD-LS-SP Public Skills_P4`**, `PIPD-LS-SP Public Skills`, `Plugin Creator`,
`Slack`, `GitHub`. Under `你建立的`, **both** PIPD cards show `更多操作` and neither offers `安裝` any more.

## Side effects (all disclosed)

- Account: a **second** installed plugin now carries preview.4's functional content. The earlier R5Y-derived install
  (`PIPD-LS-SP Public Skills`) is untouched and still installed.
- Still present as probe footprints: `pipd-smoke-minimal` (P4) and the probe-named plugin (P5, now also showing
  `更多操作`); the P5 one and `…_P4` both display the same skills. Removing any of these is an owner action.
- Browser: one additional trusted click (the earlier coordinate attempt), one trusted ENTER, one reload, one tab
  switch by the owner mid-flow (disclosed by the owner, not caused by the probe).
- Local: candidate G, `CANDIDATE_G_MANIFEST.json`, `probe_P6.json` (raw), `VERDICT_P6_and_INSTALL.md` (this file),
  logs `raw/probe_P6.log`, `raw/install_G.log`, `raw/install_G_step2.log`, scripts `build_candidate_G.py`,
  `ui_install_plugin.py`, `ui_plugin_tab_state.py`, `ui_personal_tab_read.py`, and two dialog screenshots.

## Claim ceiling

Everything above is UI-observed on a live account: the host exposes no server-side detail, so "installed" means the
personal list and the plugin page present the installed state after a reload — not that a server-side record was
independently read. The content differences between `…_P4` and the earlier install are limited to the identity and
display fields; all functional members remain byte-identical to preview.4.

## Where this leaves the earlier finding

Unchanged and now demonstrated twice: the archive's packaging was never the obstacle. A new identity is accepted and
installable; the same content under the **already-owned** identity is refused. The recommendation to record the
account's installed `plugin_id` set before packaging an upload candidate stands, with the added field map:
**identity = `plugin.json .name`; display = `extensions` display fields + `plugin.release.json .display_name`.**
