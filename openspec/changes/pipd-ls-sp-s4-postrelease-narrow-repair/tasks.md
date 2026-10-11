# Tasks

> Status legend: `[x]` = done **and re-run by the orchestrator against the frozen candidate** (not merely
> claimed by the writer lane). `[~]` = done as far as the local candidate allows, with the residue named.
> `[ ]` = not done.
>
> Denominator: the four route-out Work Orders of the 2026-10-11 order
> (`S4-UX-01`, `S4-WEB-02`, `S4-CONTRACT-03`, `S4-SELFBOOT-04`) and the ten findings
> `POST-F01..POST-F10` of the independent challenge report (SHA-256 `fc30c230…`).

## S4-UX-01 — quickstart verification and Windows onboarding (`POST-F01`, `POST-F08`, P1)
- [x] 1.1 The README quickstart's checksum step succeeds when only the wheel and `SHA256SUMS` were
      downloaded (select the wheel line before checking), and the alternative full-download variant is
      documented.
- [x] 1.2 A copy-paste PowerShell branch (`Get-FileHash -Algorithm SHA256`) is present against the same
      published digest, plus a separate, explicitly-unverified one-line wheel install.
- [x] 1.3 `pipd --root` is shown before the subcommand everywhere it appears.
- [x] 1.4 Fresh-shell UAT in an empty directory: bash replay POS exit 0; PowerShell replay POS; a
      mutated wheel byte ⇒ check non-zero; missing asset / wrong URL / wrong interpreter ⇒ typed refusal.
- [x] 1.5 The README states the current immutable tag and that `main` is rolling, without touching
      historical receipts.

## S4-WEB-02 — one versioned Web/ChatGPT mount package (`POST-F05`, P1)
- [x] 2.1 Build `highest-one` versioned ZIP: dispatcher `SKILL.md`, `README_MOUNT.md`,
      `PIPD_LS_SP_QUICKSTART_PROMPT.md`, five reference documents, `MANIFEST.sha256`.
- [x] 2.2 `README_MOUNT.md` separates native skill upload from manual attachment fallback and marks
      unavailable host capabilities `NOT_AVAILABLE`.
- [x] 2.3 Every document carries a source locator and the release identity; no token, PII or
      unauthorised body.
- [x] 2.4 Five-case consumer UAT recorded, with `NOT_SUPPORTED` where native upload could not be
      exercised; ZIP hash and manifest recompute identically.

## S4-CONTRACT-03 — identity type and profile fail-closed (`POST-F02`, `POST-F03`, `POST-F04`, P1)
- [x] 3.1 Identity properties (`subject_id`, `version`, `content_hash`, `schema_version`) declare a
      JSON type and pattern in every family that declares them; PI `trace` is an array of `TraceLink`.
- [x] 3.2 The type check is the first-fail for integer/null/text identity and for a text or null trace;
      an undeclared `trace` on PD/ECP/TQAEP stays refused.
- [x] 3.3 `compute_profile` refuses duplicate / non-string / empty / unknown axes typed, and
      `pipeline.profile_record` consumes the same normalisation.
- [x] 3.4 `risk_assessment = NOT_ASSESSED` is emitted when no risk evidence exists; axis count is never
      labelled a risk score; no `LOW_RISK_VERIFIED` is minted.
- [x] 3.5 POS/NEG/EDGE: existing legal PI/PD/ECP/TQAEP and CE-1/CE-2 regression still pass; the 19
      families, 8 skills and 13 CLI commands are unchanged.

## S4-SELFBOOT-04 — pinned source map and replayable self-bootstrap (`POST-F06`, P2)
- [x] 4.1 `docs/NORMATIVE_SOURCE_MAP.md` records owner / version / hash-or-`NOT_PUBLIC` / consumers per
      source family and states it is a derived view over the external canonical SSOT.
- [x] 4.2 `examples/self-bootstrap/` replays a minimal PI→PD→ECP/TQAEP design with the shipped CLI into
      an isolated root and records the real transcript and digests.
- [x] 4.3 A source-missing / stale-context negative is recorded; no hand-written expected JSON stands in
      for a real replay.

## Cross-cutting — governance, evidence, verification
- [x] 5.1 Native prompt compiler `lint` / `activation` / `acceptance` / `compile` return
      `PROMPT_COMPILE_PASS`; the contract hash is recorded.
- [x] 5.2 Admission through the typed HG-KSEOS lifecycle (requirement → FROZEN → taskspec → workorder)
      with a checkpoint; KANBAN + SWARM board graph created and read back; OpenSpec change present.
- [x] 5.3 Affected-only regression plus the full suite on the frozen candidate; exact-set checks for 19
      families / 8 skills / 13 CLI / 5 web / 3 host.
- [x] 5.4 Candidate tuple (commit/tree/product digest/ZIP digest) published and bound to every raw
      receipt.
- [~] 5.5 Independent checker lane (distinct model) re-derives the decisive claims on the frozen
      candidate and returns its own verdict with named `NOT_RUN` rows where it could not run.
- [~] 5.6 Single acceptance master document written, the finding ledger covers `POST-F01..F10`, and the
      publication is either executed under the owner grant with an anonymous read-back, or marked
      `NOT_EXECUTED` with the cause named.

## Round close-out note (orchestrator, 2026-10-11)

`[x]` means the work landed **and** the acceptance command was re-run by the orchestrator against the
frozen candidate, with the raw output kept in
`.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/`.

`5.5` is `[~]`: the independent checker lane ran on candidate `dbe38719` with `gpt-6.1-sol` over
OpenAI OAuth and returned `VERIFY_LANE_SCOPE_ONLY: FAIL` with F01–F12. Its F07 (bash quickstart) and
F03 (cross-root determinism claim) were repaired in iterations 1 and 2; F04/F05/F06/F11/F12 are
disclosed limitations handed to the round-scoped TT register; F01/F08 were operator/verifier process
defects that were remediated (frozen checkout re-cleaned, the verifier's stray global install
uninstalled); F02 was proven to be an environment effect, not a regression, by reproducing the
identical failure profile on the PRE-REPAIR base commit exported as an archive. The re-run of the
checker on the final candidate is the closing step.

`5.6` is `[~]`: the single acceptance master document is written, and the finding ledger covers
10/10 `POST-F01..F10`, but the publication is **NOT_EXECUTED** with the cause named: the only
credential route the order identifies (the owner's fine-grained PAT) returns HTTP 401 on every
endpoint including the target repository, so the run checkpointed `AUTH_BLOCKED`. No workaround, no
higher-privilege token and no alternate account was used, and the released tag was not touched.
