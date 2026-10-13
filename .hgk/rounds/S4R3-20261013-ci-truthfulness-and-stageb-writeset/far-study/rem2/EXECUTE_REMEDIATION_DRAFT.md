# FAR round 2 — F1 allowlist remediation recommendation (EXECUTE lane, bounded writer)

Subject and finding per packet §1–§2. Measurement locator per packet §3:
`evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json`. I add no facts beyond the packet and that
locator.

## A. Recommendation: Option B, and the single measurement that decides it

Recommend **Option B** (packet §4): declare `.hgk/**` out of the PRODUCT write set as a printed
`EXCLUDED_PREFIXES` with a stated reason, remove the `.hgk/rounds/...` entries from both ALLOWED sets,
keep `docs/USER_GUIDE.md$`, and extend the self-test to keep proving product refusal.

The deciding measurement is the classification of the stage-b governed diff at the current head
(packet §3, locator `ALLOWLIST_MINIMUM_MEASUREMENT.json`), read twice off the same 151-path set:

- `docs/USER_GUIDE.md` **is inside the governed diff** (it appears in `docs_paths_in_range` and in
  `changed`) and the diff is `UNLISTED = 0`, `DENIED = 0`. Entry 1 is therefore load-bearing product:
  removing it refuses a path Stage B legitimately ships.
- `143` of the `151` changed paths are under the round directory (`far-study/` 83, `evidence/` 38,
  `scripts/` 18, three files at the round root, `admission/` 1), and **every tested narrowing fails**
  (`evidence/` alone loses 105, `/(evidence|far-study)/` loses 22, `evidence/12_GATES/` loses 105).
  Entry 2 is not a product path; it is the round committing its own working material.

The same measurement therefore forces entry 1 to stay and forces entry 2 out of the product allowlist.
Option A keeps a self-referential allowlist that permits writes to the directory holding the round's
own receipts (packet §2 flag 2; the depth of that self-reference is recorded in
`evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt`). Option C leaves the false comment shipped. Given
the measured minimum product set is `frozen ALLOWED + docs/USER_GUIDE.md$` (widening **+1**), Option B
is the narrowest truthful edit and beats both A (widening +2, false statement repaired but
self-reference kept) and C (widening +2, false statement kept).

## B. Exact edit per branch copy

The write-set step lives in `.github/workflows/public-plugin-verify.yml`, present as its own copy on
both branches (packet §1). Apply the following to **both** copies in one round so the stack is
restored afterwards (packet §5).

### B.1 Entries added and removed (listed separately)

Allowlist entries **added**: none. The product ALLOWED set is only narrowed.

Allowlist entries **removed**:

| Branch copy | `STAGE:` | Entry removed from `ALLOWED` |
|---|---|---|
| Stage B (`feat/s4r3-stageb-successor-20261013`) | `stage-b` | `\.hgk/rounds/S4POST-20261012` |
| Stage B | `stage-b` | `\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` |
| Stage A (`fix/s4r3-stage-a-ci-truthfulness-20261013`) | `stage-a` | `\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` |

Kept on the Stage B copy: `docs/USER_GUIDE\.md$` (packet §3, load-bearing).

New non-product declarations (added to **both** case arms, added once each per copy):

```
EXCLUDED_PREFIXES='^\.hgk/'
EXCLUDED_REASON='round evidence tree is scaffolding, not product'
```

### B.2 Stage B copy — `stage-b` case

In the `stage-b)` arm, replace the `ALLOWED=` assignment (line 118 at head) so the round entries are
gone and declare the exclusion:

```
              ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/USER_GUIDE\.md$|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$)'
              DENIED='^(skills/|src/|schemas/|dist/)'
              EXCLUDED_PREFIXES='^\.hgk/'
              EXCLUDED_REASON='round evidence tree is scaffolding, not product'
```

Add one unlisted-product plant so the classifier self-test still shows an unlisted PRODUCT path is
refused after the exclusion was introduced:

```
              REFUSED_PLANTS='skills/pipd-core/SKILL.md schemas/TraceLink.schema.json dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl src/pipd_ls_sp/validate.py tools/unlisted_product_tool.py'
```

The `DENIED` line is unchanged (`skills/`, `src/`, `schemas/`, `dist/`).

### B.3 Stage A copy — `stage-a` case

In the `stage-a)` arm, drop the round entry from `ALLOWED` and declare the same exclusion:

```
              ALLOWED='^(pyproject\.toml$|setup\.py$|MANIFEST\.in$|src/pipd_ls_sp/workspace\.py$|examples/first-run/run\.(sh|ps1)$|tests/test_web_fallback\.py$|tests/test_standard_wheel_schemas\.py$|tools/cli_smoke\.py$|tools/verify_installed_wheel_registry\.py$|\.github/workflows/(ci|public-plugin-verify)\.yml$)'
              DENIED='^(skills/|schemas/|dist/)'
              EXCLUDED_PREFIXES='^\.hgk/'
              EXCLUDED_REASON='round evidence tree is scaffolding, not product'
```

`REFUSED_PLANTS` already carries `tools/build_public_plugin.py`, which is unlisted for stage-a, so the
unlisted-product refusal is already planted; no change needed. `DENIED` unchanged.

### B.4 Common run section (both copies) — printed exclusion + self-test

The loop below the `esac` is identical on both copies. Insert the exclusion check after the `..`
traversal `case` and before the `DENIED` test, so `.hgk/**` is classified and printed rather than
silently accepted:

```
            if printf '%s' "$path" | grep -Eq "$EXCLUDED_PREFIXES"; then
              echo "EXCLUDED_FROM_PRODUCT_WRITE_SET: $path  reason=${EXCLUDED_REASON}"
              continue
            fi
```

Extend the classifier self-test so a product violation is still refused and the exclusion is proven to
print:

```
          for planted in ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/planted_scaffolding.txt"; do
            if ! printf '%s' "$planted" | grep -Eq "$EXCLUDED_PREFIXES"; then
              echo "GATE_SELF_TEST_FAILED: ${planted} is not classified as scaffolding" >&2; exit 1
            fi
            echo "GATE_SELF_TEST_OK: ${planted} is EXCLUDED_FROM_PRODUCT_WRITE_SET (printed, not silently accepted)"
          done
```

The existing `REFUSED_PLANTS`/`ALLOWED_PLANTS` loops stay; the added `tools/unlisted_product_tool.py`
plant makes the product-refusal half explicit after the exclusion exists. The exclusion only matches
`.hgk/`; `DENIED` and the anchored product `ALLOWED` still classify every other path, so no DENIED,
exit-code or denominator behavior changes.

### B.5 Comment repair (both copies)

Replace the sentence block that currently reads "This change widens NEITHER allowlist" (Stage B copy)
with text that enumerates the additions and states the stage-b-only scope. Because Option B removes the
round entry, the enumeration is: stage-b gained exactly one entry versus the frozen subject
(`docs/USER_GUIDE\.md$`), measured load-bearing; the round-tree entry is removed and `.hgk/**` is
excluded as scaffolding and printed; and the DENIED continuity holds **stage-b-wise only** — stage-a's
DENIED set omits `src/` (packet §2). The Stage A copy carries the same stage-a-appropriate wording.

## C. What must be re-run and re-cut, and what each falsifies

- **Gate self-tests (the classifier self-test inside both workflow copies).** Falsifies a relaxed
  classifier: if `tools/unlisted_product_tool.py` (stage-b) or the unlisted/denied plants stop being
  refused, the exclusion swallowed a product path. Also proves the planted scaffolding path is printed,
  not silently accepted.
- **Local and CI write-set gate run against the new head** (`WRITE_SET_GATE_STEP.yml`,
  `WRITE_SET_GATE_LOCAL_AND_CI.txt`). Falsifies that the 151-path diff still classifies clean with the
  round tree excluded; if it reports `UPGRADE_WROTE_OUTSIDE_ALLOWED_SET` for a `.hgk` path, the
  exclusion print/continue is misplaced.
- **C3 diff receipt re-cut at the new revision** (`C3_ALLOWLIST_BASELINE_DIFF.txt`). Falsifies the
  narrowed-widening claim; it must now show stage-b vs frozen = `+1` (`docs/USER_GUIDE\.md$`) and the
  round entries absent.
- **C4 repin re-cut at the new revision** (`C4_REPIN_AND_DECLARED_BASE.txt`). Falsifies the stacked
  invariant: `git merge-base <A head> <B head>` must equal the new A head after both copies are edited
  (packet §5).
- **Lane verdicts re-cut** (EXECUTE/verify lane outputs under `far-study/`). Falsifies that the verdicts
  were bound to the superseded heads. No acceptance was granted on the current heads, so superseding
  them costs nothing earned.

## D. External acceptance officer gains and loses under Option B

Gains:

- The product ALLOWED set enumerates product paths only, and the widening versus the frozen subject is
  the measured minimum `+1` (`docs/USER_GUIDE\.md$`), which the officer can re-derive from the C3
  receipt.
- The scaffolding boundary is **printed** (`EXCLUDED_FROM_PRODUCT_WRITE_SET` with `reason=`) into the
  gate receipt, so the officer can open the artifact and see which paths were classified as
  non-product.
- The gate no longer permits writes to the directory that holds its own receipts.
- The self-test proves product refusal survives the exclusion.

Loses:

- `.hgk/**` is no longer a governed product path, so the officer must accept the printed exclusion as
  the boundary rather than reading a per-path allowlist entry. The officer must confirm `.hgk/**`
  contains no product path; the measurement shows that for this diff but it becomes a standing
  assertion to maintain.
- One more classifier element (`EXCLUDED_PREFIXES`) to read, and the exclusion reason is a prose claim
  attached to the print, not itself a gate.

## E. DO-NOT list

- Do not add `docs/USER_GUIDE\.md$` removal or any other narrowing of the product allowlist: it is
  measured load-bearing (packet §3).
- Do not keep, re-add, or re-enumerate `.hgk/rounds/...` in either ALLOWED set.
- Do not widen `EXCLUDED_PREFIXES` beyond `.hgk/` in this round.
- Do not touch `DENIED` (`skills/`, `src/`, `schemas/`, `dist/`); do not relax any oracle, threshold,
  validator, guard, exit code or denominator (packet §5).
- Do not edit one branch copy only; both copies change candidate heads (packet §5).
- Do not ship the false "widens NEITHER allowlist" comment.
- Do not merge, tag, release or archive (packet §5).
- Do not claim the DENIED continuity is uniform: it is stage-b-only (packet §2).
