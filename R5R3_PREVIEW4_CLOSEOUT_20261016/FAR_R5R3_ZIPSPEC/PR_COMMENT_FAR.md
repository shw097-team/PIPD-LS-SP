## FAR sub-round result — is the ZIP spec the cause of the host refusal?

**Answer: no.** The refusal is an **existing-`plugin_id` conflict on the account**, not a packaging or
plugin-specification defect. Minimum sufficient remedy: the **update route or remove-then-readd** (an owner
one-action step, no product change).

### Controlled matrix (five artifacts, live account, probes executed under the owner's authorisation)

| # | artifact | delta vs the refused archive | outcome |
|---|---|---|---|
| P1 | A = the `v0.1.1-preview.4` asset | none (retry) | REFUSED again in ~2 s ⇒ transience eliminated |
| P2 | B = the archive this account already holds | the accepted install | **ACCEPTED** (previous round's success signature reproduced) |
| P3 | E = A with only the declared version bumped | version axis | REFUSED ⇒ the host identity is not the version field |
| P4 | D = fresh id, minimal 2-member archive | identity axis | **ACCEPTED** ⇒ the surface accepts new plugins |
| P5 | F = A's members, only `plugin.json` name changed, A's provenance preserved | content axis | **ACCEPTED** ⇒ the provenance content is not refused |

The plugin-contract surface (plugin.json, all 8 SKILL.md, references, schemas, icon) is **byte-identical**
between A and B, and B was accepted — so a format/spec violation cannot explain the refusal of those bytes.

### Independent verification

- Lane `VERIFY_SECURITY` via CODEX CLI, arm `opencode-go/deepseek-v4.1-flash` (required == served, rank 1,
  read-only, 186.71 s, usage receipt OK, nonce echoed). Verdict C1–C7 **all PASS**, with two real disagreements
  that were **applied as corrections, not argued**: (1) E/F match A on enumerated record fields and on
  decompressed bytes but not on the full zip record (compression level differed ⇒ `compress_size`/`header_offset`
  differ); (2) the brief said "four probe records" where five exist. Its verdict also states plainly that it
  cannot settle live host behaviour — the host claims stay UI-observed.
- Self-check gate: 10/10 invariants re-derived from local artifacts (`GATE_PASS`), with the ceiling printed.

### Evidence (public, blob-verified)

Branch `r5r3-closeout-evidence-20261016`, commit `ca6d319` — 48 files under
`R5R3_PREVIEW4_CLOSEOUT_20261016/FAR_R5R3_ZIPSPEC/` (verdict, decision, checker verdict + receipt, probe records
P1–P5, candidate E/F manifests, self-check result, learning record, scripts, raw logs, the candidate archives).
Readback: a fresh clone of that commit lists the same 48 blob ids as the local packet.

### Owner decisions outstanding

1. **R1/R2** — update route, or remove the installed plugin and re-add the preview.4 archive (one action each).
2. Two probe plugins were created by P4/P5 (`pipd-smoke-minimal` and one probe-id plugin); one action each to
   remove. Disclosed as round side effects.
3. Gates unchanged: NEW_RELEASE / PRIVATE_HOST_INSTALL / PUBLIC_DIRECTORY / S4_FULL_PASS / PRODUCTION — none
   granted to the agent.

### Environment finding (not a packet defect)

A full checkout of this repository on Windows fails at default `MAX_PATH` (a path under
`.hgk/rounds/R7-…/openspec/changes/…` is too long); the packet readback was therefore done at object/blob level
with `core.longpaths` noted. Reviewers cloning on Windows should set `core.longpaths=true`.
