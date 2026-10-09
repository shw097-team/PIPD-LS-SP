# Design — R4 low-resistance hardening

## Principle

**Make a failure detectable before it costs a run, and make the verifier's footprint invisible to the
product's own guards.** Every design choice below removes a measured failure mode rather than expressing
a preference. Where a control already exists the hardening only decides when it runs, not what it says:
no existing gate, threshold or schema is relaxed anywhere in this change.

## S1 — preflight (`tools/preflight_check.py`)

- One entry point, one JSON artefact (`PREFLIGHT.json`, schema `PIPD-PREFLIGHT/1`), non-zero exit on any
  `FAIL`. `WARN`/`SKIP` do not fail the round — a containerless round is legal, an unreachable docker
  daemon is a fact about the round's isolation and must be *recorded*, not mistaken for a defect.
- Separation of concerns: `FAIL` is reserved for facts the round cannot run without (python, git HEAD,
  disk, the codex binary, an expected-HEAD mismatch). Everything that merely *degrades* isolation or
  convenience is `WARN` with a named reason (`SANDBOX_HELPER_BROKEN`, `CONFIG_DRIFT`, `DOCKER_UNAVAILABLE`).
- The two checks that would have prevented this round's most expensive events are **explicit model pinning**
  (`CONFIG_DRIFT` when `config.toml` disagrees with the model the run passes — two verify runs were
  silently invalidated by exactly this) and the **sandbox capability probe** (the desktop update broke the
  helper; a 10-second probe tells the run to plan for the bypass instead of discovering it at minute 8).
- Checks are pure functions where possible so the suite can test them without docker, codex or a network.

## S2 — verifier envelope (`tools/round_envelope.py`)

- `init` materialises a disposable byte-copy (including `.git`, excluding caches), asserts the copy's HEAD
  equals the source's, and writes the envelope record to a scratch root that is **outside both trees**.
- `snapshot` records HEAD, dirty count and a per-file sha256 manifest of tracked files.
- `verify` classifies the delta as **MODIFIED / REMOVED / ADDED** and fails on MODIFIED/REMOVED or on an
  ADDED path that no allow-rule matches. The three-way classification is not cosmetic: a guarded
  before/after comparison that reports any difference as drift flags the very file the brief mandated,
  and a guard that cries wolf is worse than none because the next real modification is dismissed as the
  usual false alarm.
- Refusals are part of the contract: `--dst` inside `--src` (or vice versa) and a `--scratch` inside either
  tree are refused, because the envelope's entire value is the boundary it asserts.

## S3 — round self-scan (`tools/round_selfscan.py`)

- Runs *before* acceptance over the round's own new text, folding in `tools/deny_list_scan.py` as a
  subprocess when present, and refuses on a hit. Measured cost of skipping it: a receipt's own example
  strings tripped the product's secret scan (2 test failures) and a brief's illustrative flag tripped the
  deny-list scan.
- **Anti-self-reference design:** the credential patterns are assembled from fragments at runtime, because
  writing the literal shape into the scanner's own source would make the scanner's own repository fail the
  product's secret scan. A test asserts the tool's own bytes contain no literal shape.

## Testing strategy

Deterministic units only: no docker, no codex, no network in the suite. Environment probes take injected
strings (a synthetic `git status --porcelain` body, an injected TOML snippet, a stub deny-scan script) so
the boundary and negative cases are testable and stable across hosts. Each new module carries at least one
negative test (exit-code mapping, refusal path, redaction never echoing the raw value).

## Risks and mitigations

- *Preflight false FAIL* → the FAIL set is deliberately minimal and every WARN carries its reason; a FAIL
  names the exact check and the observed value.
- *Envelope copy drift* → `init` asserts HEAD equality at creation and `verify` re-reads the source after
  the checker runs, so a moved source is reported rather than absorbed.
- *Self-scan false positive on legitimate dummy patterns* → the scanner redacts the excerpt to a shape
  label, and the allow-list for round-owned paths is explicit (a hit is reported; suppression is a
  decision in the round record, never a silent default).
