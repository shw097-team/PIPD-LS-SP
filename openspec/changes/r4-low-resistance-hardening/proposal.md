# R4 low-resistance hardening — preflight (S1), verifier envelope (S2), round self-scan (S3)

## Why

The R4 focused-repair round (`PIPD-LS-SP_HERMES_R4_FOCUSED_REPAIR_PROMPT_2026-10-09`) produced a
`FAIL_CHALLENGE` verdict twice and then burned six further verification attempts, none of which
produced a verdict. The failure analysis
(`知識庫/實作相關DOC/PIPD/實作證據/PIPD-LS-SP_R4_FAILURE_ANALYSIS_FAR_2026-10-09.md`, 22 events,
21 with retained evidence) found the dominant causes are **not product defects**:

| class | events | cause |
|---|---|---|
| C1 execution-substrate drift | 3 | the desktop update replaced the codex binary directory, changed `~/.codex/config.toml`'s model, and broke the sandbox helper — none of it read before a run started |
| C2 network/isolation boundary | 2 (+1) | container→host loopback and `:10102` cross-origin assumptions never asserted |
| C3 image/dependency gap | 2 | no `pytest` in the writer image; a 12-minute suite inside a 25-minute guardrail |
| C4 verifier co-tenancy | 3 | acceptance receipts, brief copies and scratch written **inside** the tree the product's own secret and deny-list scanners police |
| C5 brief insufficiency | 3 | intent-style briefs with no enumerated commands, stop condition or scratch discipline |
| C6 non-determinism | 3 | digests quoted from a tree the suite rewrites; measurements with no git provenance |

Every one of these converts a 10-second environment fact into 8–25 minutes of wasted model time plus a
false reading about the product. Two events (C7) were genuine integrity risks (a forged fixture, a
weakened gate) and were caught and repaired — the hardening below is what would have caught them
earlier, as a pre-condition rather than as a post-mortem.

## What changes

- `tools/preflight_check.py` (**S1**): one command that asserts the execution substrate before any model
  time is spent — python and the suite, git HEAD/dirty, disk, docker daemon, the codex binary path and
  version, the codex sandbox capability (probe for the measured `helper_unknown_error` state), the
  `~/.codex/config.toml` model versus the model the run pass pins, host loopback services, and the suite
  baseline. Emits `PREFLIGHT.json`; non-zero exit on any FAIL.
- `tools/round_envelope.py` (**S2**): a verifier runs only inside a disposable byte-copy, with scratch
  **outside** the tested tree, and the round asserts the product tree's HEAD and dirty count are
  unchanged afterwards; the delta classifier reports MODIFIED / REMOVED / ADDED separately so a mandated
  addition is not misread as drift.
- `tools/round_selfscan.py` (**S3**): before acceptance, the round scans its own new text with the
  product's own scanners (credential shapes and the deny list) and refuses to proceed on a hit — the
  measured cause of two self-inflicted test failures.

## Non-goals

No product behaviour change beyond added tools and their tests; no gate is weakened, no `required` field
or schema constraint removed; no canonical config mutation; the owner gates (licence/publication,
knowledge quarantine `W6`) stay with the owner; no claim of `INDEPENDENT_PASS`, `RELEASED` or
`PRODUCTION_VERIFIED`.

## Impact

- Affected: `tools/`, `tests/` only.
- Unchanged: `src/`, `schemas/`, `fixtures/`, `.hgk/` contents, all existing gates.
- Round claim ceiling: `CANDIDATE_ONLY`.
