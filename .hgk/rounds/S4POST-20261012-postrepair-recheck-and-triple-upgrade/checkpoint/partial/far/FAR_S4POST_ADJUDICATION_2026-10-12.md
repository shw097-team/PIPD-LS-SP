# FAR adjudication — S4POST implementation record (2026-10-12)

Scope: the four items decided by the prior FAR round and carried into the S4POST round
(`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/`). This document records, for
each item, whether it is implemented here, deliberately not implemented (with the reason), or
deferred. It is an implementation note, not an acceptance artefact.

Note on the brief: the round shipped two writer briefs. `WRITER_BRIEF_v2.md` states it **supersedes
v1** because v1's gate ("accept any matching non-disk basis") rubber-stamps a real post-seal content
edit — the old snapshot still hashes to the recorded digest even after the file genuinely changed.
This implementation follows **v2**: a non-disk basis is only benign when its bytes are EOL-equivalent
to the disk bytes, otherwise the entry is `UNEXPLAINED_DRIFT`. Both briefs agree on everything else.

## F-020-A / F-021-A — basis-aware digest classification (ADOPT): **IMPLEMENTED**

`tools/verify_evidence_digests.py` now establishes *which bytes* each recorded digest was computed
over before it decides anything, then classifies every mismatch:

* bases, first match wins: `disk`, `crlf_disk`, `head_blob`, `crlf_head_blob`, `candidate_blob`,
  `crlf_candidate_blob`, else `unexplained`;
* verdicts: `MATCH_RAW` (`sha256(disk) == recorded`), `BENIGN_EOL` (a basis matches **and** is
  EOL-equivalent to the disk bytes), `UNEXPLAINED_DRIFT` (missing file, no basis matches, or a basis
  matches but the content genuinely changed);
* CRLF transformations implemented, both directions, and named in the module docstring: lone LF ->
  CRLF expansion and CRLF -> LF collapse, applied to the disk bytes and to the `HEAD` / sealed
  candidate blobs;
* the sealed candidate tree/commit is read from the sibling seal `<manifest stem>.seal.json`
  (`candidate.candidate_tree_sha`, then `candidate.repo_commit_sha`) — never hard-coded;
* CLI: default run prints the full report and exits 0; `--strict` exits 1 only when the unexplained
  set is non-empty; `--json` prints the compact
  `{"checked","match_raw","benign_eol","unexplained","basis_counts"}`. Existing flags and the JSON
  keys the in-tree test reads (`checked`, `match`, `missing`, `stale`, `identity_checks`) still work.

Measured on this checkout (`tools/verify_evidence_digests.py --json`):

```json
{"checked":1085,"match_raw":1038,"benign_eol":5,"unexplained":42,"basis_counts":{"disk":1038,"crlf_disk":5,"head_blob":0,"crlf_head_blob":0,"candidate_blob":41,"crlf_candidate_blob":1,"unexplained":0}}
```

`--strict` exits **1** on this tree (its unexplained set is non-empty). This **agrees** with the
independent measurement stated in `WRITER_BRIEF_v2.md` (1085 entries; 1038 raw; 47 mismatching, of
which 5 are EOL-only and 42 are genuine content drift). The 42 drift entries are the 41 whose
recorded digest equals the sealed-candidate blob plus 1 whose digest equals the CRLF form of that
blob; in every case the on-disk content is *not* EOL-equivalent to the matching snapshot, so accepting
the basis on a hash match alone (the v1 gate) would have hidden them. No re-seal is performed and no
manifest is rewritten.

## F-024-A — candidate ancestry stays report-only (ADOPT, no behaviour change): **IMPLEMENTED**

The generation-identity check is unchanged in spirit and stays **report-only**: for every JSON
payload carrying `candidate_head`, the report records `is_ancestor`. A non-ancestor is named in the
report and the run still exits 0 without `--strict`.

The change that would have made a non-ancestor **fatal** was **deliberately not implemented**: it was
adjudicated a **no-op / downgrade**. The committed identity is necessarily an ancestor, and escalating
the few cross-line (non-ancestor) revisions to a hard failure converts a *visible* condition into a
run-breaking one without adding information. `tests/test_verify_evidence_digests_basis.py` pins this:
it feeds a resolvable non-ancestor commit and asserts exit 0, that the value is still named, and that
even `--strict` does not escalate ancestry.

## F-023-A — execute-lane model entitlement probe (ADOPT): **IMPLEMENTED**

`tools/model_eligibility_probe.py` performs a **two-turn** tool-call probe against an
OpenAI-compatible endpoint (`--base-url`, `--model`): turn 1 asks for a tool call; turn 2 continues
that conversation with the tool result. It writes a receipt carrying
`declared_model`, `observed_model`, `turn1`, `turn2`, `eligible`, `typed_reason`. Exit 0 when both
turns pass; exit **3** with the typed reason `reasoning_content_not_echoed` when the second turn
fails for the known `reasoning_content` error class; exit **2** for transport/connection errors. An
`Authorization` header is attached only from `OPENAI_API_KEY`, and the key is never printed, echoed or
stored.

Patching the EXECUTE adapter that drops `reasoning_content` was **deliberately not implemented**: the
adapter is not in this repository, so an in-repo patch is impossible and was rejected; the defect is
escalated to its owner instead. `tests/test_model_eligibility_probe.py` drives the probe against an
in-process `http.server` stub (both turns healthy; second turn HTTP 400 with a `reasoning_content`
body; connection refused) with no real network.

## Items not implemented here / deferred

* Making candidate ancestry fatal — rejected as a no-op/downgrade (see F-024-A).
* An in-repo EXECUTE-adapter patch — rejected; owned outside this repository (see F-023-A).
* Re-sealing or rewriting `evidence_manifest.json` — out of scope; the tool stays report-only.
* Live validation of the probe against a real endpoint, and any adaptor-side or host-side evidence —
  deferred; this round produced local tests only.

## Claim ceiling

This is a **candidate with local tests only**: no acceptance, no release and no adaptor-side evidence
is claimed. A green local suite is not an S4 PASS, not a release, not a host qualification, and not an
independent acceptance; the `--strict` non-zero exit on this tree is a *reported* condition, not a
verdict, and the model probe receipt is a maker-side measurement, not an entitlement guarantee.
