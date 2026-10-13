# Advisory verdict from the mandated verification lane - attempt 8 (re-cut bundle)

Second verdict from the mandated checker, obtained on a bundle re-cut to close the gaps attempt 7
named. Verbatim below. Ceiling first.

## Ceiling and run facts

- Lane `VERIFY_SECURITY`, served arm **`opencode-go/glm-5.3-flash`** (forced rank 3,
  `served_arm == required_arm`), sandbox `read-only`, escalation not authorised,
  26.86 s. `ok: True`, `usage_receipt_ok: True`,
  `nonce_present: True`.
- **Still advisory only** - never an OracleReceipt, never a canonical acceptance status - and the
  overall verdict is again **`INCONCLUSIVE`**, which counts as NOT verified. `REQ-S4R3X-VERIFY-005`
  stays open.
- Method unchanged: text-only dry audit, nothing executed, same lane / arm / sandbox.
- Bundle: 24843 chars, blocks kept ['verify_installed_wheel_registry.py', 'public-plugin-verify.yml', 'ci.yml', 'test_public_plugin_packaging.py'].

## What changed from attempt 7, and what the change proves

1. **C4 is no longer `REFUTED`.** It is now `INCONCLUSIVE`. The refutation in attempt 7 was caused by
   MY bundle mixing receipts from successive heads without labels; with every block labelled and the
   instruction not to judge the current subject from historical material, the checker stopped
   concluding a refutation and instead said it could not audit those two repairs from what it was
   given. That is the correction working - the earlier `REFUTED` line must not be cited as a defect
   finding against the candidate.
2. **C1 moved from `CONFIRMED` to `INCONCLUSIVE`, and that is also a bundling effect, not a
   regression in the product.** Attempt 8 spent its budget on the artefacts the checker had asked for
   (the gate tool, the workflow steps, the Stage B test source), which pushed the raw build receipts
   out of the bundle. The checker said so explicitly and named what would settle it.
3. **The binding constraint is now measured and structural**: the dispatcher takes the prompt as a
   command-line argument, so a bundle cannot carry both source code and raw receipts at the sizes this
   round has. The fix is split runs (a code audit and an evidence audit), not a bigger prompt.

## The verdict, verbatim

```
C1: INCONCLUSIVE - no current-labelled doctor receipt is reproduced; `wheel-doctor.log`, the sdist doctor log, and the relevant wheel wiring/setup.py are absent or omitted, so clean-install mode, family count, exit status, and the sdist route cannot be settled from this bundle.

C2: PARTIALLY_CONFIRMED - the supplied CI file on the current Stage A branch invokes the committed `tools/verify_installed_wheel_registry.py`, and that source is locally runnable and explicitly type-checks the family count; however, no current direct run receipt or negative-case test output is reproduced here, so the negative path is structurally supported but not proved.

C3: INCONCLUSIVE - the shown Stage A copy correctly uses declared `STAGE_A_BASE_SHA` rather than the pull-request base and preserves a path allowlist with frozen-path denials, but more than 16 KB of the workflow is truncated through the enforcement/self-test logic, and no Stage B copy or refusal receipts are supplied; the absence of widening beyond the quoted lists cannot be settled from an excerpt.

C4: INCONCLUSIVE - no Stage B test code defining the manifest/release identity refusal or extension namespace refusal appears in the material. The Stage B block named as that evidence truncated away nearly all of its 43 KB, and the focused test receipt was omitted, so neither repair can be audited from the supplied bundle.

No oracle, threshold, denominator, or validator in the supplied excerpts is visibly relaxed. The regression descriptions identify repairs such as pipefail handling, schema source mode, family type validation, and stage-scoped write-set comparison, rather than loosening assertions. The lack of raw receipts makes a broader clean-bill conclusion impossible.

For the green signals: C1 shows no raw green or paired red. C2 shows the named gate but no actual execution or its paired negative result. C3 and C4 show no validated green and no paired red receipt. The only useful evidentiary signal is the source of the gate, plus an excerpt of its invocation.

Families: the bundle cannot distinguish a correct registry from a silently reduced one. It only documents an expected count of 19 inside the gate. No family manifest, registry listing, doctor JSON, or independent enumeration is included. A raw clean-install doctor JSON showing `schema_source.mode=INSTALLED` and the complete 19-family list—or the registry tree plus a hash/manifest tying it to the wheel—would settle it.

Residual risks: head-labelled context still does not include any current direct operating receipts; omitted logs hide the decisive evidence for C1, C2 negative behavior, C3 enforcement, and C4; Stage B version/base correspondence and stacking relationships are asserted by labels and prose but not settled by raw tree or commit records. The Stage A write-set excerpt also cannot establish that frozen paths remain refused under the complete logic.

VERDICT: INCONCLUSIVE
HGK_LANE_NONCE_OK
```

## Executor's reading, stated separately

- **No claim is verified.** C2 remains `PARTIALLY_CONFIRMED`; C1, C3, C4 are `INCONCLUSIVE`.
- **One genuinely useful negative result**: the checker examined the supplied excerpts against the
  "was anything relaxed?" question and reported that no oracle, threshold, denominator or validator
  in them is visibly relaxed - while stating plainly that the absence of raw receipts prevents a
  clean bill overall. That is the closest thing to a positive finding here, and it is scoped to the
  excerpts, not to the round.
- **It answered the families question the same way twice**, and specifically: the bundle cannot
  distinguish a correct registry from a silently reduced one, because "19" is asserted inside the gate
  rather than enumerated. It named the two artefact sets that would settle it - a raw clean-install
  `doctor` JSON showing `schema_source.mode=INSTALLED` plus the complete family list, or the registry
  tree with a hash/manifest tying it to the wheel. That is a concrete, checkable work item for
  attempt 9, not a matter of opinion.
- **Attempt 9 (not yet run)**: two focused bundles rather than one large one - (a) code audit:
  the gate tool, both workflow steps, the Stage B test source, with per-file excerpts sized to fit;
  (b) evidence audit: the raw `doctor` JSON, the sdist-route receipt, the focused-run log and the
  registry listing/hash. Same lane, same arm, same sandbox.

## Binding

- attempt stdout (quoted above): `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-8-20261013T094141Z\attempt-3068-1791884501-3-stdout.txt`
  bytes=3317, sha256=176f689bc1430efed5387fa8a10b10e8060342af61008e4a396e7a5e969d849e
- attempt stderr: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-8-20261013T094141Z\attempt-3068-1791884501-3-stderr.txt` bytes=220, sha256=8b8437097557bccfa9064a0fc9f486d2405cfe3db89f879f570c233b828c7d01
- lane receipt: `ao_lane_dryaudit/stdout_a8.txt`; invocation `ao_lane_dryaudit/invocation_a8.json`
- prior verdict for comparison: `evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A7.md`
