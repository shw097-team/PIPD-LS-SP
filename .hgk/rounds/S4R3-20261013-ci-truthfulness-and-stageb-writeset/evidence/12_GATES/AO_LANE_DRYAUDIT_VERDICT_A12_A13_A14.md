# Advisory verdicts, attempts 12 to 14 - the three focused bundles

| | a12 `receipts` | a13 `c3` | a14 `c4` |
|---|---|---|---|
| served | ok=True, nonce=True | ok=True, nonce=True | ok=True, nonce=True |
| arm | `opencode-go/glm-5.3-flash` | `opencode-go/glm-5.3-flash` | `opencode-go/glm-5.3-flash` |
| seconds | 102.66 | 108.04 | 33.72 |
| overall | `PARTIALLY_CONFIRMED` | `INCONCLUSIVE` | `PARTIALLY_CONFIRMED` |
| blocks kept | 1/1 | 2/2 | 3/3 |

All three advisory only; none is an acceptance. Every bundle kept every block it offered (checked
because attempt 8 had silently dropped three).

## Per-claim state after eight served runs (7-14)

| claim | best verdict so far | from | what is still missing |
|---|---|---|---|
| C1 | `PARTIALLY_CONFIRMED` | a11, a12 | registry CONTENTS equality: wheel-extracted inventory vs the tree, file by file |
| C2 | `CONFIRMED` | a10 | the CI gate itself invoking the tool, co-located with the negatives |
| C3 | `PARTIALLY_CONFIRMED` | a13 | the Stage B branch's copy of the workflow, a full (not distilled) run receipt, and a baseline diff proving the allowlist was not widened |
| C4 | `CONFIRMED` | a14 | - |

Two claims are now CONFIRMED and no claim is unexamined. The remaining gaps are **co-location gaps**:
the material exists in this round's evidence but has not yet been placed in one argv-sized bundle.

## a12 `receipts`, verbatim

```
No label conflict observed; the single receipt block is claimed as current Stage A and it covers only the C1/C2 side.

C1: PARTIALLY_CONFIRMED - the wheel-route and sdist-to-wheel-route installs both report `mode=INSTALLED`, `families=19`, and doctor exits 0, but the pack does not prove that the shipped wheel's registry is identical to the Stage A tree's registry.
C2: PARTIALLY_CONFIRMED - a committed-looking tool from the current Stage A head runs locally, and five negative doctor fixtures turn the verifier red with the expected typed errors; this bundle still does not show the CI gate itself calling that tool.
C3: INCONCLUSIVE - no write-set gate, allowlist, base-policy, or frozen-path refusal evidence is present.
C4: INCONCLUSIVE - no Stage B head, manifest, release-bookkeeping, or namespace refusal evidence is present.

What I could not verify is the exact registry equality and full family coverage. The receipts establish only a scalar count of 19 and a usable installed path. They do not distinguish a correct registry from a silently reduced one, because a registry could retain 19 family counts while missing individual schema files or having altered schema contents. The exact artefact that would resolve this is an inventory of the installed wheel's `pipd_ls_sp/schemas` contents, generated from the wheel itself and compared file-by-file against the Stage A tree at the current head: family IDs plus per-file SHA256 or equivalent content hashes. A committed registry manifest carrying those expected hashes, with the wheel and sdist-route inventories diffed against it, would be sufficient.

Residual risk is therefore that the positive install signals are genuine but content-blind at the family-count level. The verifier negatives are well attributed and paired, including for doctor verdict, installed mode, family count/type, and a source-checkout path under the deny prefix. The unresolved risk is registry equality rather than gate falsifiability.

VERDICT: PARTIALLY_CONFIRMED
HGK_LANE_NONCE_OK
```

## a13 `c3`, verbatim

```
C1: INCONCLUSIVE — the bundle has no shipped-wheel registry receipt, tree registry receipt, clean-install `mode=INSTALLED` output, doctor exit report, or sdist-to-wheel artifact, so it cannot distinguish a correct registry from a silently reduced one.

C2: INCONCLUSIVE — the bundle has no committed registry-gate invocation and no paired red-case receipt for it.

C3: PARTIALLY_CONFIRMED — the Stage A workflow copy shows the declared-stage/base logic, treats the pull-request base as context only, and includes frozen-path/traversal/unlisted-`src/**` refusals plus allowances. However, the bundled evidence does not include the Stage B branch copy, a full hosted-CI red receipt, or a baseline diff proving no allowlist widening.

C4: INCONCLUSIVE — the Stage B worktree write-set summary does not identify the Stage B head `ba27309b...` and does not contain either of the claimed typed-error refusals.

For the families question, I cannot tell a complete registry from a reduced one in this bundle. The artifact that would is a raw `tools/verify_installed_wheel_registry.py` clean-install receipt comparing the wheel's extracted bundled registry against the tree registry, enumerating every expected family and including a negative receipt where one family is removed or renamed and the same check goes red.

Residual risks: the receipt block is distilled from `WRITE_SET_GATE_LOCAL_AND_CI.txt`, so it is not possible to inspect the full CI output or branch-head correspondence line by line. The Stage A self-test is persuasive for classifier behavior but is not the same evidence as a full hosted red run.

VERDICT: INCONCLUSIVE
HGK_LANE_NONCE_OK
```

## a14 `c4`, verbatim

```
C1: INCONCLUSIVE - the bundle contains no shipped registry artefact, no tree-side registry source, and no CI output to compare.
C2: INCONCLUSIVE - no committed gate tool or negative case is included.
C3: PARTIALLY_CONFIRMED - the declared stage, committed base, and non-governed PR base are visible and frozen paths are refusable, but no prior allowlist is provided to prove no widening occurred.
C4: CONFIRMED - the merge-base evidence supports true stacking, and the Stage B refusal tests expose both defects with typed errors and paired remediation positivity.

Could not verify: the shipped registry equals the registry in the tree, whether Stage A not widening is real, Stage B's workflow copy, and the other claims' operational signals. The registry defect needs a tree-side registry plus an actual install/doctor-family comparison. Residual risks: an undocumented allowlist extension or synchronized registry mismatch could go unnoticed if only intent is documented.

VERDICT: PARTIALLY_CONFIRMED
HGK_LANE_NONCE_OK
```

## Executor's reading

- **C4 CONFIRMED is the round's second confirmation**: "the merge-base evidence supports true stacking,
  and the Stage B refusal tests expose both defects with typed errors and paired remediation
  positivity". The re-pin and both typed refusals (CR-IDENTITY-BIND, CR-EXT-UNREVIEWED) are closed
  from the lane's side.
- **C2's verifier negatives are accepted as well attributed and paired** ("five negative doctor
  fixtures turn the verifier red with the expected typed errors"), with the residual ask being the CI
  gate that calls the tool, not the tool's falsifiability.
- **C1's remaining gap is content, not count** - and note the checker's own words in a12 restate the
  ask that `FAMILY_IDENTITY_RECEIPT.md` already answers (wheel-extracted inventory, per-file digests,
  positive and negative). The receipt exists and was accepted as answering this in a11; a12 simply did
  not carry it. That is a co-location miss, recorded as such.
- **C3 needs three specific additions**, all producible: the Stage B branch's workflow copy, the full
  run receipt instead of a distilled one, and a baseline diff of the ALLOWED set between the frozen R3
  subject and the current head (produced here as C3_ALLOWLIST_BASELINE_DIFF.txt).
- **One self-inflicted process note**: three bundles were dispatched in one run and each answered only
  the claims whose material it carried, so C1/C2/C3/C4 each came back INCONCLUSIVE in the bundles that
  did not carry them. Splitting the audit by claim is right; splitting it by SOURCE rather than by
  CLAIM was my error, and the next bundles are cut by claim.

## Binding

- a12 stdout `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-12-20261013T102433Z\attempt-15056-1791887073-3-stdout.txt` sha256=e018bb44abab5f7f343e5798299bb4cc6179971a94f4ccd1de6e18477a0d5d29
- a13 stdout `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-13-20261013T102618Z\attempt-17896-1791887178-3-stdout.txt` sha256=5447c2469871f9919bf12188203388dc8f8d5585426391f89913201e9f40e868
- a14 stdout `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-14-20261013T102808Z\attempt-3352-1791887288-3-stdout.txt` sha256=212567ef31bfb6cda3ac6b38dc226a69437625cd8e1384a7640c753bc576180c
