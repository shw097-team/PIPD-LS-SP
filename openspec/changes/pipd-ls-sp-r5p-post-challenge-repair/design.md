# Design — R5P post-challenge S4 focused repair

## Context

The R5 round repaired the three R4 P0/P1 defects (unsafe `project --out`, stale wheel, no-effect
`export --out`) and produced a 25 PASS / 2 INFO UAT matrix. The external challenge then re-ran the
adversarial mutation (B4) against the **installed** wheel and observed `doctor` still reporting PASS.
The cause is structural, not a typo: `workspace.doctor()` validates `<root>/schemas` — the workspace
convention — while the CLI's own resource resolver (`registry._resolve_schemas_dir()`) selects
`PIPD_SCHEMAS_DIR` → packaged `importlib.resources` copy → source tree. The two surfaces can disagree,
and the one the user reads is the weaker one.

## Decision: diagnose the resolver, keep one authoritative resolution path

The repair adds a single reporting function on the registry side and consumes it from `doctor`, so the
diagnostic and the runtime can never drift apart again.

```
describe_schemas_source() -> (dir, mode, tried[])        # registry.py
    mode = OVERRIDE  if $PIPD_SCHEMAS_DIR selected
           INSTALLED if the packaged copy inside the wheel selected
           SOURCE    if <repo>/schemas selected
doctor(root) -> { verdict, findings[], schema_source{mode,path,tried},
                  exact_set{expected,present,missing[]}, families }
```

Rules kept deliberately narrow:

1. `doctor` still validates `<root>/schemas` when that directory exists (workspace hygiene), but the
   **verdict is the AND of both surfaces** — a healthy workspace no longer masks an incomplete install.
2. A missing packaged member produces a finding naming the family and `verdict=FAIL` → CLI exit 1,
   because `cli.main()` maps `verdict == "FAIL"` to a non-zero exit.
3. No fallback is introduced. If resolution fails, the typed `ValidationFail` from the registry is
   surfaced rather than swallowed.
4. The B4 mutations are only ever exercised against a disposable `venv` under the round's scratch root;
   the repository's own `dist/` wheel is never mutated.

## Alternatives rejected

- **Have `doctor` call `load_registry()` with no argument only.** It fixes the B4 case but drops the
  workspace-hygiene check the existing tests rely on, and it hides which surface was inspected.
- **Make `_resolve_schemas_dir()` prefer the source tree.** That would make an installed product read
  the developer's checkout — exactly the "silent fallback" the report forbids.
- **Add an install-time cryptographic readback inside `doctor`.** Out of the S4 scope: it needs a
  release signing/TTL decision (`F-R5-03` conditional), and the round keeps the packaging preflight as
  the typed refusal surface instead of inventing a trust anchor.

## Per-atom gate

The owner's `PER_ATOM_BYTES(2000)` objective is preserved. The addition is an oracle, not a threshold:
a **unique obligation denominator** is computed by canonical atom identity, so padding a payload with
duplicate/filler atoms cannot lower the bytes-per-obligation figure. The historical `343547 > 20000`
row stays in the historical section, unmodified, and the new tests prove padding invariance rather than
re-quoting the threshold.

## Subject binding

The round produces its own tuple. The R5 publication attestation (`commit=d1aad3e…`) and the first AO
subject (`5094939…`) are recorded as *historical, different frozen tuples* and are never presented as
this round's receipt.

## Claim ceiling

Local repair + local UAT + an independent (advisory) checker verdict. Not `RUNTIME_READY`, not
`RELEASED`, not `PRODUCTION_VERIFIED`, not PRE-W3. The license/public-rights item stays a Human owner
gate; the symlink negative stays conditional on a privileged disposable runner.

## Rollback

Product paths revert to the round's baseline commit; the wheel is rebuilt from the reverted tree. The
round's evidence tree keeps the pre-change digests so the rollback target is verifiable, and the
`.pipd-backup-<token>` publish mechanism from R5 remains the in-product rollback pointer.
