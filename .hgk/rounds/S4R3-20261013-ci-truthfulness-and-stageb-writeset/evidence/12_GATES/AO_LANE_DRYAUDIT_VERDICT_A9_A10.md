# Advisory verdicts, attempts 9 and 10 - the split audit

Two focused bundles against the same subject, same lane, same forced arm, same read-only sandbox.
Both were SERVED. Verbatim below, with binding. Ceiling first, as always.

## Ceiling and run facts

| | attempt 9 (`code` bundle) | attempt 10 (`evidence` bundle) |
|---|---|---|
| served | `ok: True`, nonce `True` | `ok: True`, nonce `True` |
| arm | `opencode-go/glm-5.3-flash` (forced, == required) | `opencode-go/glm-5.3-flash` (forced, == required) |
| seconds | 87.38 | 51.58 |
| overall | `INCONCLUSIVE` | `PARTIALLY_CONFIRMED` |
| stdout | `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-9-20261013T095031Z\attempt-1584-1791885031-3-stdout.txt` | `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-10-20261013T095201Z\attempt-13272-1791885121-3-stdout.txt` |

Advisory only - never an OracleReceipt, never a canonical acceptance status. `REQ-S4R3X-VERIFY-005`
stays open. The split exists because the dispatcher passes the prompt as a command-line argument, so
one bundle cannot carry both source and raw receipts: attempt 7 carried receipts and no source,
attempt 8 the reverse. Neither is a product change.

## Attempt 9 - `code` bundle, verbatim

```
C1: INCONCLUSIVE - the bundle shows the intended verifier and CI invocation but no raw wheel-doctor receipt or run log proving a clean wheel build reported verdict PASS, mode=INSTALLED, 19 families, and exit 0. The sdist-to-wheel route is not represented here either.

C2: PARTIALLY_CONFIRMED - CI calls the committed `tools/verify_installed_wheel_registry.py` with explicit `--expect-families 19` and a checkout deny-prefix, so a locally callable committed tool is present. However, `tests/test_standard_wheel_schemas.py` is not included, so a negative case actually exists and turns red remains unverified.

C3: INCONCLUSIVE - the public-plugin workflow excerpt shows declared-stage metadata and commentary about the intended scope behavior, but not the classifier logic, complete allowlists, frozen-path rules, or negative self-test required to confirm them.

C4: INCONCLUSIVE - the Stage B packaging excerpt is truncated before it shows tests or typed-error handling for the official-manifest name/version mismatch or non-reviewed extension namespaces, and no re-pin evidence in this bundle confirms Stage B sits on the named Stage A head.

The visible wheel-registry verifier was not relaxable at the assertion points that appear: it requires PASS, mode=INSTALLED, an integer families value, exact equality with 19, and rejects a resolved schemas path under the checkout prefix. I found no visible relaxation there, but that audit is limited to that tool.

For families specifically, no. A successful receipt could prove a count of 19 while still showing a silently reduced registry if names or contents were replaced while preserving the count. The exact artifact missing is a wheel-produced or installed-package schema inventory: the actual `pipd_ls_sp/schemas/` file listing with family names, count, and digests/sizes, comparable against the expected Stage A schemas tree. Raw `wheel-doctor.log` alone would be insufficient.

I could not verify declared-base processing, allowlist contents, frozen-path refusals, Stage B stacking, or the two Stage B refusals because the needed implementation and receipt blocks were omitted or truncated. There are no visible block-label conflicts; the overlapping CI excerpts appear to be the same Stage A excerpt, not contradictory evidence.

Residual risks are that comments may describe a stricter gate than the omitted code implements, that downstream edits could modify `--expect-families`, test fixtures, allowlist entries, or the denied-path classifier without appearing here, and that family count can be a weaker oracle than family identity.

VERDICT: INCONCLUSIVE
HGK_LANE_NONCE_OK
```

## Attempt 10 - `evidence` bundle, verbatim

```
I ran no audit commands; the above call attempt was policy-blocked and is irrelevant to the result below, which is based solely on reading the supplied bundle.

- C1: PARTIALLY_CONFIRMED — The tree listing is labelled only "measurement of Stage A branch" with no committed digests or head binding, so I cannot prove the shipped registry equals this tree listing. Receipts positive: sdist→wheel rc 0, install rc 0, doctor PASS mode=INSTALLED families=19 (the expected family count is asserted nowhere in this bundle). Blocking contradiction: the doctor log is an error trace for a missing `pipd.exe`, with no rc label binding it to the sdist receipt; those blocks cannot be reconciled from labels alone.
- C2: CONFIRMED — f006 gate test log shows a real probe plusياريا six refusals: wrong count, boolean count, mapping, non-PASS verdict, source-mode, checkout-local resolution, all `ok` (negative controls present). Registry mirror tests also show byte-for-byte reproduction plus missing/undeclared refusals. But this evidence is work-tree-relative and unredacted, with no head or path-stability hash to tie to successive `pipd.exeinvoke` runs across machines.
- C3: INCONCLUSIVE — No allowlist content, no write-set gate script, no test logs, no negative controls, and no declared/base vs PR-base evidence is included.
- C4: INCONCLUSIVE — No official manifest content, no release-bookkeeping content, no extension-namespace review list, no stack test, no type-error logs, no Stage A→B re-pin evidence, and no cross-stage test text are included.
- Family distinction: This bundle cannot distinguish a correct registry from a silently reduced one. The tree listing confirms 20 files, not family definitions; the receipts report only a numeric `doctor_families: 19`. The missing artifact is an unredacted head-commit_checked `doctor` output showing the per-family canonical names (the 19 expected family labels), or a committed script with the 19 expected family-name list plus its actual output.

Unverifiable with this bundle: committed vs. shipped registry equality (head-bound tree digests, or wheel-extracted registry digests under the asserted head), Stage A label attribution for the doctor flop, any C3/C4 gate/manifest/registry material.

Residual risk: a genuinely reduced registry would pass every `mode=INSTALLED` positive check while only a family-name-level negative test would catch it; per-stage head and path binding to recover the actual verified artefact cannot be validated from a single work-tree-relative `a83f67f7f47e…` hash alone.

VERDICT: PARTIALLY_CONFIRMED
HGK_LANE_NONCE_OK
```

## What these two settle, read across all four attempts

1. **C2 now has a CONFIRMED from the mandated lane** - attempt 10: the gate's log shows a real probe
   plus six distinct refusals (wrong count, boolean count, mapping, non-PASS verdict, source-mode,
   checkout-local resolution), all `ok`, and the mirror tests show byte-for-byte reproduction plus
   missing/undeclared refusals. This is the strongest single result the lane has produced this round,
   and it is scoped to that gate on that work tree.
2. **C1 is `PARTIALLY_CONFIRMED`** - `rc 0` on the sdist-to-wheel route, install `rc 0`, and a doctor
   line reporting `mode=INSTALLED` with 19 families.
3. **C3 and C4 remain `INCONCLUSIVE` in every attempt.** No bundle has yet carried the write-set
   classifier plus its allowlists plus a refusal receipt (C3), or the Stage B refusal tests plus
   re-pin evidence (C4), inside one argv-sized prompt. This is a bundling limit, stated by the
   checker itself, not a favourable silence.
4. **A defect in MY evidence bundle, reported by the checker and confirmed here.** The `doctor` log
   block I supplied is an error trace about a missing `pipd.exe`, not a passing doctor run. The
   checker flagged the contradiction instead of ignoring it ("the doctor log is an error trace for a
   missing `pipd.exe`, with no rc label binding it to the sdist receipt"). Treated here as a real
   defect in this round's material.
5. **The families question is now sharp and identical across both bundles.** A numeric count cannot
   distinguish a correct registry from a silently reduced one that preserves the count. Both bundles
   name the same missing artefact: an **unredacted, head-committed `doctor` output listing the
   per-family canonical NAMES** (or a committed script holding the 19 expected family names plus its
   actual output), optionally with wheel-extracted registry digests tied to the head. That is the
   work item for the next attempt.
6. **The sandbox held.** Attempt 10's transcript records that it tried to run a command, was
   policy-blocked, and (correctly) excluded that call from its reasoning. No escalation was requested
   or granted, and no substitute checker was used.

## Binding

- attempt 9 stdout: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-9-20261013T095031Z\attempt-1584-1791885031-3-stdout.txt` bytes=2997 sha256=a08411fcdd9a5dcb6196f06c3fdbaaaa47750bb4919661e4e263edd0e884d0ed
- attempt 9 stderr: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-9-20261013T095031Z\attempt-1584-1791885031-3-stderr.txt` bytes=220 sha256=3661eb39b429325d7a3a7e308f8fa3017aeed3042f33a09475d450959d197ca3
- attempt 10 stdout: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-10-20261013T095201Z\attempt-13272-1791885121-3-stdout.txt` bytes=3250 sha256=58dea2e4746e3b5ac84bf38f0b40cffaf429dfc07f111a21feb5ada5a5cb6e9e
- attempt 10 stderr: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-10-20261013T095201Z\attempt-13272-1791885121-3-stderr.txt` bytes=565 sha256=5a0e6bb65eecaeda6d79f2402b1b16739cf8a43d46a1315ea27849da83677d5d
- lane receipts: `ao_lane_dryaudit/stdout_code_a9.txt`, `ao_lane_dryaudit/stdout_evidence_a10.txt`
- invocations: `ao_lane_dryaudit/invocation_code_a9.json`, `ao_lane_dryaudit/invocation_evidence_a10.json`
- earlier verdicts: `evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A7.md`, `..._A8.md`
